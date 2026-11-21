"""Open-loop action replay check for a robomimic dataset.

Question it answers: do the installed simulator pins (robosuite, MuJoCo) reproduce
the recorded demonstrations? Upstream ``playback_dataset.py`` only reports state
divergence; this script also records whether each replayed demo reaches task success.

Input:  a robomimic HDF5 file (``data/demo_*/{states, actions, rewards}`` + env metadata).
Output: a JSON report (versions, summary, per-demo results); exit code 1 if any demo fails.
Pass:   every demo succeeds. Divergence and first-success timing are reported for
        information only, because a different patch version never matches bit for bit.

Usage:
    python jobs/lift_replay_check.py --dataset <low_dim_v15.hdf5> --out <report.json>
    python jobs/lift_replay_check.py ... --limit 5      # quick smoke test
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import h5py
import numpy as np


@dataclass
class DemoResult:
    demo: str
    num_steps: int
    success: bool
    first_success_replay: int | None    # step index i such that success holds after actions[i]
    first_success_recorded: int | None  # same, from the recorded rewards
    max_divergence: float               # max_i ||replayed state - recorded state|| (qpos+qvel)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--dataset", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--limit", type=int, default=None, help="replay only the first N demos")
    return p.parse_args()


def sorted_demo_names(f: h5py.File) -> list[str]:
    return sorted(f["data"].keys(), key=lambda name: int(name.split("_")[1]))


def make_env(env_meta: dict):
    """Build the simulator exactly as the dataset was recorded (env_meta = data.attrs['env_args'])."""
    # Imported here so `--help` works without loading the simulator.
    import robomimic.utils.env_utils as EnvUtils
    import robomimic.utils.obs_utils as ObsUtils

    # robomimic must know each obs key's modality before building an env; obs are unused here.
    ObsUtils.initialize_obs_modality_mapping_from_dict({"low_dim": ["robot0_eef_pos"]})
    return EnvUtils.create_env_from_metadata(
        env_meta=env_meta, render=False, render_offscreen=False, use_image_obs=False
    )


def first_true(flags: np.ndarray) -> int | None:
    idx = np.flatnonzero(flags)
    return int(idx[0]) if idx.size else None


def recorded_first_success(rewards: np.ndarray) -> int | None:
    """Step index of the first success in the recorded demo.

    Lift's sparse reward is 1.0 once the task is solved after actions[i]. Compare with
    ``>= 1.0`` rather than nonzero so a shaped (dense) reward would not count as success.
    """
    return first_true(rewards >= 1.0)


def replay_demo(env, demo: h5py.Group) -> DemoResult:
    states = demo["states"][()]    # (T, 32): recorded simulator snapshots, states[i] is BEFORE actions[i]
    actions = demo["actions"][()]  # (T, 7)
    rewards = demo["rewards"][()]  # (T,)
    T = len(actions)

    # Restore the demo's start. The XML fixes the scene (Lift randomizes cube size per
    # episode); states fixes qpos/qvel. reset_to() already resets when given a model, so
    # env.reset() is redundant; kept because this is the code that ran job 5813465.
    env.reset()
    env.reset_to({"states": states[0], "model": demo.attrs["model_file"]})

    successes = np.zeros(T, dtype=bool)
    divergence = np.zeros(T - 1)
    for i in range(T):
        # Open loop: replay the human's command (25 OSC/MuJoCo substeps), ask the task
        # evaluator (not the reward), and measure drift from the recorded next state.
        # Note: drift is dominated by qvel spikes at contact, not by qpos.
        env.step(actions[i])
        successes[i] = env.is_success()["task"]
        if i < T - 1:
            divergence[i] = np.linalg.norm(env.get_state()["states"] - states[i + 1])

    return DemoResult(
        demo=demo.name.split("/")[-1],
        num_steps=T,
        success=bool(successes.any()),
        first_success_replay=first_true(successes),
        first_success_recorded=recorded_first_success(rewards),
        max_divergence=float(divergence.max()) if divergence.size else 0.0,
    )


def summarize(results: list[DemoResult]) -> dict:
    div = np.array([r.max_divergence for r in results])
    return {
        "n_demos": len(results),
        "n_success": sum(r.success for r in results),
        "failed_demos": [r.demo for r in results if not r.success],
        "n_first_success_match": sum(r.first_success_replay == r.first_success_recorded for r in results),
        "max_divergence_median": float(np.median(div)),
        "max_divergence_max": float(div.max()),
    }


def package_versions(env_meta: dict) -> dict:
    import mujoco
    import robomimic
    import robosuite

    return {
        "robosuite": robosuite.__version__,
        "mujoco": mujoco.__version__,
        "robomimic": robomimic.__version__,
        "numpy": np.__version__,
        "dataset_env_version": env_meta.get("env_version"),
    }


def main() -> int:
    args = parse_args()
    t0 = time.time()
    with h5py.File(args.dataset, "r") as f:
        env_meta = json.loads(f["data"].attrs["env_args"])
        env = make_env(env_meta)
        names = sorted_demo_names(f)[: args.limit]
        results = []
        for k, name in enumerate(names):
            r = replay_demo(env, f[f"data/{name}"])
            results.append(r)
            print(f"[{k + 1}/{len(names)}] {name}: success={r.success} "
                  f"step {r.first_success_replay} vs recorded {r.first_success_recorded}, "
                  f"max div {r.max_divergence:.1e}", flush=True)

    report = {
        "dataset": args.dataset.name,  # file name only: the report may be pasted into public issues
        "versions": package_versions(env_meta),
        "summary": summarize(results),
        "seconds": round(time.time() - t0, 1),
        "per_demo": [asdict(r) for r in results],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2))
    print(json.dumps({k: report[k] for k in ("versions", "summary", "seconds")}, indent=2))
    return 0 if not report["summary"]["failed_demos"] else 1


if __name__ == "__main__":
    sys.exit(main())
