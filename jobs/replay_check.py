"""Open-loop action replay check for a robomimic dataset.

Question it answers: do the installed simulator pins (robosuite, MuJoCo) reproduce
the recorded demonstrations? Upstream ``playback_dataset.py`` only reports state
divergence; this script also records whether each replayed demo reaches task success.

Input:  a robomimic HDF5 file (``data/demo_*/{states, actions, rewards}`` + env metadata).
Output: a JSON report (versions, summary, per-demo results); exit code 1 if any demo fails.
Pass:   every demo succeeds. Divergence and first-success timing are reported for
        information only, because a different patch version never matches bit for bit.

Usage:
    python jobs/replay_check.py --dataset <low_dim_v15.hdf5> --out <report.json>
    python jobs/replay_check.py ... --limit 5      # quick smoke test
    python jobs/replay_check.py ... --demos demo_11 demo_52 --video_dir <dir>
        # chosen demos only; one MP4 each, recorded (left) vs replayed (right), and the step
        # where the replayed object first drifts from the recorded one
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
    object_drift_step: int | None = None  # first step the replayed object is >2 cm from the recorded one
    object_final_gap: float | None = None # replayed vs recorded object position at the last step [m]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--dataset", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--limit", type=int, default=None, help="replay only the first N demos")
    p.add_argument("--demos", nargs="+", default=None, help="replay only these demos (e.g. demo_11)")
    p.add_argument("--video_dir", type=Path, default=None,
                   help="write <demo>.mp4: recorded (left) vs replayed (right), agentview")
    return p.parse_args()


def sorted_demo_names(f: h5py.File) -> list[str]:
    return sorted(f["data"].keys(), key=lambda name: int(name.split("_")[1]))


def make_env(env_meta: dict, render_offscreen: bool = False):
    """Build the simulator exactly as the dataset was recorded (env_meta = data.attrs['env_args'])."""
    # Imported here so `--help` works without loading the simulator.
    import robomimic.utils.env_utils as EnvUtils
    import robomimic.utils.obs_utils as ObsUtils

    # robomimic must know each obs key's modality before building an env; obs are unused here.
    ObsUtils.initialize_obs_modality_mapping_from_dict({"low_dim": ["robot0_eef_pos"]})
    return EnvUtils.create_env_from_metadata(
        env_meta=env_meta, render=False, render_offscreen=render_offscreen, use_image_obs=False
    )


def first_true(flags: np.ndarray) -> int | None:
    idx = np.flatnonzero(flags)
    return int(idx[0]) if idx.size else None


def recorded_first_success(rewards: np.ndarray) -> int | None:
    """Step index of the first success in the recorded demo.

    The robomimic ph datasets store a sparse reward (0/1, checked for Lift, Can and
    Square): 1.0 once the task is solved after actions[i]. Compare with
    ``>= 1.0`` rather than nonzero so a shaped (dense) reward would not count as success.
    """
    return first_true(rewards >= 1.0)


# Free joint of the task object (Can's scene also holds parked Milk, Bread and Cereal).
TASK_OBJECT_JOINT = {"Lift": "cube_joint0", "PickPlaceCan": "Can_joint0",
                     "NutAssemblySquare": "SquareNut_joint0"}


def object_pos(env) -> np.ndarray:
    sim = env.env.sim   # looked up each time: a hard reset rebuilds the sim
    start, _ = sim.model.get_joint_qpos_addr(TASK_OBJECT_JOINT[env.name])
    return sim.data.qpos[start:start + 3].copy()


def frame(env) -> np.ndarray:
    return env.render(mode="rgb_array", height=256, width=256, camera_name="agentview")


def replay_demo(env, demo: h5py.Group, rec_env=None, writer=None) -> DemoResult:
    states = demo["states"][()]    # (T, 32): recorded simulator snapshots, states[i] is BEFORE actions[i]
    actions = demo["actions"][()]  # (T, 7)
    rewards = demo["rewards"][()]  # (T,)
    T = len(actions)

    # Restore the demo's start. The XML fixes the scene (Lift randomizes cube size per
    # episode); states fixes qpos/qvel. reset_to() already resets when given a model, so
    # env.reset() is redundant; kept because this is the code that ran job 5813465.
    env.reset()
    env.reset_to({"states": states[0], "model": demo.attrs["model_file"]})
    if rec_env is not None:   # second env that only shows recorded states (no physics stepping)
        rec_env.reset()
        rec_env.reset_to({"states": states[0], "model": demo.attrs["model_file"]})

    successes = np.zeros(T, dtype=bool)
    divergence = np.zeros(T - 1)
    gap = np.zeros(T)
    for i in range(T):
        if rec_env is not None:
            rec_env.reset_to({"states": states[i]})
            gap[i] = np.linalg.norm(object_pos(env) - object_pos(rec_env))
            if writer is not None:
                writer.append_data(np.concatenate([frame(rec_env), frame(env)], axis=1))
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
        object_drift_step=first_true(gap > 0.02) if rec_env is not None else None,
        object_final_gap=float(gap[-1]) if rec_env is not None else None,
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
        video = args.video_dir is not None
        env = make_env(env_meta, render_offscreen=video)
        rec_env = make_env(env_meta, render_offscreen=video) if args.demos else None
        names = args.demos or sorted_demo_names(f)[: args.limit]
        results = []
        for k, name in enumerate(names):
            writer = None
            if video:
                import imageio
                args.video_dir.mkdir(parents=True, exist_ok=True)
                writer = imageio.get_writer(str(args.video_dir / f"{name}.mp4"), fps=20)
            r = replay_demo(env, f[f"data/{name}"], rec_env, writer)
            if writer is not None:
                writer.close()
            results.append(r)
            print(f"[{k + 1}/{len(names)}] {name}: success={r.success} "
                  f"step {r.first_success_replay} vs recorded {r.first_success_recorded}, "
                  f"max div {r.max_divergence:.1e}"
                  + (f", object drifts >2 cm at step {r.object_drift_step}, final gap "
                     f"{r.object_final_gap:.3f} m" if r.object_final_gap is not None else ""),
                  flush=True)

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
