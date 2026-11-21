"""Paired closed-loop evaluation of robomimic checkpoints.

Question it answers: how often does each saved checkpoint solve the task when it controls
the robot itself, and which checkpoint is best? (Validation loss cannot answer this.)

Why not upstream ``run_trained_agent.py`` alone: its ``--seed`` seeds only ``np.random`` and
``torch``. robosuite 1.5 places objects with the env's own ``default_rng(env_kwargs["seed"])``,
which is ``None`` in the dataset metadata, so every checkpoint would face different, unrepeatable
initial states (docs/BASELINE.md). This script reuses upstream's checkpoint loaders and
``rollout()`` unchanged and only adds: a seeded env per checkpoint (same initial states for every
checkpoint = paired evaluation), per-episode records and a pairing check.

Input:  checkpoint files (``model_epoch_*.pth``) from robomimic ``train.py``.
Output: a JSON report (versions, settings, per-checkpoint summary and per-episode records);
        optional MP4 of the first episodes per checkpoint.
Pass:   the script finishes and ``paired`` is true. Success rates are results, not pass criteria.

Usage:
    python jobs/eval_checkpoints.py --checkpoints <run>/models/model_epoch_*.pth --out <report.json>
    python jobs/eval_checkpoints.py ... --n_rollouts 3 --horizon 100     # quick smoke test
    python jobs/eval_checkpoints.py ... --video_dir <dir> --video_episodes 5
    python jobs/eval_checkpoints.py ... --video_dir <dir> --video_list 5 35   # chosen episodes only
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from pathlib import Path

import numpy as np


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--checkpoints", type=Path, nargs="+", required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--n_rollouts", type=int, default=50)
    p.add_argument("--horizon", type=int, default=400, help="max steps per episode (20 Hz)")
    p.add_argument("--seed", type=int, default=0, help="env seed (initial states) and policy seed")
    p.add_argument("--video_dir", type=Path, default=None, help="write <ckpt>.mp4 here if given")
    p.add_argument("--video_episodes", type=int, default=5, help="episodes per checkpoint in the MP4")
    p.add_argument("--video_list", type=int, nargs="+", default=None,
                   help="record exactly these episode indices instead (all episodes still run, "
                        "so episode i keeps its paired initial state)")
    p.add_argument("--camera", default="agentview")
    return p.parse_args()


def epoch_of(path: Path) -> int | None:
    m = re.search(r"model_epoch_(\d+)", path.name)
    return int(m.group(1)) if m else None


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def load_policy_and_env(ckpt_path: Path, seed: int, render_offscreen: bool):
    """Restore the policy and build a freshly seeded env from one checkpoint.

    A new env per checkpoint restarts its random generator, so every checkpoint sees the
    same sequence of initial states.
    """
    import torch
    import robomimic.utils.file_utils as FileUtils

    policy, ckpt_dict = FileUtils.policy_from_checkpoint(
        ckpt_path=str(ckpt_path), device=torch.device("cpu"), verbose=False
    )  # RolloutPolicy: policy(ob=obs) -> 7-D action; start_episode() resets the LSTM state
    # env_metadata is the dataset's env_args; env_kwargs are passed to the robosuite env (Lift, ...),
    # which seeds its own placement generator at construction.
    ckpt_dict["env_metadata"]["env_kwargs"]["seed"] = seed
    env, _ = FileUtils.env_from_checkpoint(
        ckpt_dict=ckpt_dict, render=False, render_offscreen=render_offscreen, verbose=False
    )
    return policy, env


# Free joint of the task object, per robosuite env. Can's scene also holds Milk, Bread and
# Cereal (parked, not part of the task), so "the first free joint" would be the wrong object.
TASK_OBJECT_JOINT = {"Lift": "cube_joint0", "PickPlaceCan": "Can_joint0",
                     "NutAssemblySquare": "SquareNut_joint0"}


def object_state_slice(env) -> slice:
    """Where the task object's xyz sits in the flattened state [time, qpos, qvel]."""
    sim = env.env.sim
    start, _ = sim.model.get_joint_qpos_addr(TASK_OBJECT_JOINT[env.name])
    return slice(1 + start, 1 + start + 3)  # +1: states[0] is time


def episode_record(index: int, stats: dict, traj: dict, obj: slice) -> dict:
    """One row of the report for one episode (upstream rollout() returns stats and traj)."""
    # stats: Horizon = steps actually run (rollout stops at the first success),
    #        Success_Rate = 1.0 or 0.0 for one episode.
    # init_state = the full initial MuJoCo state; it is the fingerprint that proves all
    # checkpoints faced the same initial states. object_init_pos is the task object's xyz
    # (cube, can or square nut) for analysis.
    success, steps = stats["Success_Rate"], stats["Horizon"]
    states = np.asarray(traj["initial_state_dict"]["states"])
    return {
        "episode": index,
        "success": bool(success),
        "steps": int(steps),
        "object_init_pos": [round(float(v), 5) for v in states[obj]],
        "init_state_sha1": hashlib.sha1(np.round(states[1:], 6).tobytes()).hexdigest()[:12],
    }


def check_paired(results: list[dict]) -> bool:
    """True if episode i started from the same full initial state for every checkpoint."""
    # Rows = checkpoints, columns = episodes; paired means every column is constant.
    if len(results) <= 1:
        return True
    ref = [e["init_state_sha1"] for e in results[0]["episodes"]]
    return all([e["init_state_sha1"] for e in r["episodes"]] == ref for r in results[1:])


def evaluate_checkpoint(ckpt_path: Path, args) -> dict:
    import imageio
    import torch
    from robomimic.scripts.run_trained_agent import rollout  # upstream loop, unchanged

    if args.video_list is not None:
        record, suffix = set(args.video_list), "_ep" + "-".join(map(str, sorted(set(args.video_list))))
    else:
        record, suffix = set(range(args.video_episodes)), ""
    write_video = args.video_dir is not None and bool(record)
    policy, env = load_policy_and_env(ckpt_path, args.seed, render_offscreen=write_video)
    # Policy-side randomness (GMM mode sampling) uses torch; reseed per checkpoint so episode i
    # draws the same random numbers for every checkpoint.
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)

    writer = None
    if write_video:
        args.video_dir.mkdir(parents=True, exist_ok=True)
        writer = imageio.get_writer(str(args.video_dir / f"{ckpt_path.stem}{suffix}.mp4"), fps=20)

    obj = object_state_slice(env)
    episodes = []
    t0 = time.time()
    for i in range(args.n_rollouts):
        stats, traj = rollout(
            policy=policy, env=env, horizon=args.horizon,
            video_writer=writer if (writer is not None and i in record) else None,
            video_skip=1, camera_names=[args.camera],
        )
        episodes.append(episode_record(i, stats, traj, obj))
    if writer is not None:
        writer.close()

    n_success = sum(e["success"] for e in episodes)
    success_steps = [e["steps"] for e in episodes if e["success"]]
    return {
        "checkpoint": ckpt_path.name,
        "epoch": epoch_of(ckpt_path),
        "sha256": sha256(ckpt_path),
        "n_success": n_success,
        "n_rollouts": len(episodes),
        "success_rate": n_success / len(episodes),
        "mean_steps_success": float(np.mean(success_steps)) if success_steps else None,
        "seconds": round(time.time() - t0, 1),
        "episodes": episodes,
    }


def package_versions() -> dict:
    import mujoco
    import robomimic
    import robosuite
    import torch

    return {"robosuite": robosuite.__version__, "mujoco": mujoco.__version__,
            "robomimic": robomimic.__version__, "torch": torch.__version__}


def main() -> int:
    args = parse_args()
    ckpts = sorted(args.checkpoints, key=lambda p: (epoch_of(p) is None, epoch_of(p) or 0, p.name))
    results = []
    for ckpt in ckpts:
        r = evaluate_checkpoint(ckpt, args)
        results.append(r)
        print(f"{r['checkpoint']}: {r['n_success']}/{r['n_rollouts']} success, "
              f"mean steps (successes) {r['mean_steps_success']}, {r['seconds']} s", flush=True)

    report = {
        "versions": package_versions(),
        "settings": {"n_rollouts": args.n_rollouts, "horizon": args.horizon, "seed": args.seed},
        "paired": check_paired(results),
        "results": results,  # file names only: the report may be pasted into public issues
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2))
    print(f"paired: {report['paired']}")
    return 0 if report["paired"] else 1


if __name__ == "__main__":
    sys.exit(main())
