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

    # TODO(1) — restore the policy and build a seeded env.
    #   a) policy, ckpt_dict = FileUtils.policy_from_checkpoint(ckpt_path=..., device=..., verbose=False)
    #      This venv is CPU-only: pass torch.device("cpu"). The returned policy is a RolloutPolicy:
    #      call it as policy(ob=obs) -> 7-D action; policy.start_episode() resets the LSTM state.
    #   b) The env description travels inside the checkpoint: ckpt_dict["env_metadata"] is the
    #      same dict as the dataset's data.attrs["env_args"] (you saw it in notebook §3).
    #      Which key of it holds the keyword arguments passed to robosuite's Lift(...)?
    #      Set the "seed" entry there to `seed` *before* building the env.
    #   c) env, _ = FileUtils.env_from_checkpoint(ckpt_dict=ckpt_dict, render=False,
    #                                             render_offscreen=render_offscreen, verbose=False)
    #   Return (policy, env).
    
    # a) checkpoint -> policy（重建網路、載入權重、包成 RolloutPolicy）
    policy, ckpt_dict = FileUtils.policy_from_checkpoint(
        ckpt_path=str(ckpt_path), device=torch.device("cpu"), verbose=False
    )

    # b) 在建 env 之前，把 seed 放進要傳給 Lift(...) 的參數
    ckpt_dict["env_metadata"]["env_kwargs"]["seed"] = seed

    # c) 用同一個 ckpt_dict 重建模擬器
    env, _ = FileUtils.env_from_checkpoint(
        ckpt_dict=ckpt_dict, render=False, render_offscreen=render_offscreen, verbose=False
    )
    return policy, env

def episode_record(index: int, stats: dict, traj: dict) -> dict:
    """One row of the report for one episode (upstream rollout() returns stats and traj)."""
    # TODO(2) — fill the record.
    #   stats = {"Return", "Horizon", "Success_Rate"} for this episode:
    #     Horizon is the number of steps actually run (rollout stops at the first success).
    #     Success_Rate is 1.0 or 0.0 for a single episode.
    #   traj["initial_state_dict"]["states"] is the flat MuJoCo state at the episode start,
    #     laid out as [time, qpos..., qvel...] (notebook §4: qpos = 7 arm hinges, 2 gripper
    #     slides, then the cube's free joint = position xyz + quaternion wxyz).
    #   Store the cube's initial xyz position (3 floats, round to 5 decimals) as
    #   "cube_init_pos". Which slice of `states` is it? It is the fingerprint used to prove
    #   that all checkpoints faced the same initial states.
    success, steps = stats["Success_Rate"], stats["Horizon"]
    states = traj["initial_state_dict"]["states"]
    return {
        "episode": index,
        "success": bool(success),        # bool
        "steps": int(steps),          # int
        # list of 3 floats
        "cube_init_pos": [round(float(v), 5) for v in states[10:13]],
    }


def check_paired(results: list[dict]) -> bool:
    """True if episode i started from the same cube position for every checkpoint."""
    # Rows = checkpoints, columns = episodes; paired means every column is constant.
    # Comparing each row with the first suffices (equality is transitive).
    if len(results) <= 1:
        return True
    if len({len(r["episodes"]) for r in results}) != 1:
        return False
    ref = np.array([e["cube_init_pos"] for e in results[0]["episodes"]])
    return all(
        np.allclose([e["cube_init_pos"] for e in r["episodes"]], ref, atol=1e-6)
        for r in results[1:]
    )


def evaluate_checkpoint(ckpt_path: Path, args) -> dict:
    import imageio
    import torch
    from robomimic.scripts.run_trained_agent import rollout  # upstream loop, unchanged

    write_video = args.video_dir is not None and args.video_episodes > 0
    policy, env = load_policy_and_env(ckpt_path, args.seed, render_offscreen=write_video)
    # Policy-side randomness (GMM mode sampling) uses torch; reseed per checkpoint so episode i
    # draws the same random numbers for every checkpoint.
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)

    writer = None
    if write_video:
        args.video_dir.mkdir(parents=True, exist_ok=True)
        writer = imageio.get_writer(str(args.video_dir / f"{ckpt_path.stem}.mp4"), fps=20)

    episodes = []
    t0 = time.time()
    for i in range(args.n_rollouts):
        stats, traj = rollout(
            policy=policy, env=env, horizon=args.horizon,
            video_writer=writer if (writer is not None and i < args.video_episodes) else None,
            video_skip=1, camera_names=[args.camera],
        )
        episodes.append(episode_record(i, stats, traj))
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
