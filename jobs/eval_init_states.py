"""Rebuild the initial object poses of a seeded evaluation without running a policy.

jobs/eval_checkpoints.py seeds the robosuite env; upstream rollout() then calls env.reset()
and env.reset_to(state) per episode, and reset_to() resets once more, so each episode draws
two placements and keeps the first. Repeating that sequence gives the same initial states;
the script checks this against the eval CSV (x, y) before writing.

Usage (sim venv for Lift/Can, sim-square for Square; seconds, no rendering):
    python jobs/eval_init_states.py can results/can_eval_episodes.csv results/can_eval_init_states.csv 0 1
"""
import csv
import json
import os
import sys
from pathlib import Path

import h5py
import numpy as np
from scipy.spatial.transform import Rotation

task, eval_csv, out = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
seeds = [int(x) for x in sys.argv[4:]]
JOINT = {"lift": "cube_joint0", "can": "Can_joint0", "square": "SquareNut_joint0"}[task]

import robomimic.utils.env_utils as EnvUtils
import robomimic.utils.obs_utils as ObsUtils

ObsUtils.initialize_obs_modality_mapping_from_dict({"low_dim": ["robot0_eef_pos", "object"]})
data = Path(os.environ["HPCWORK"]) / f"franka-il/data/robomimic_v15/{task}/ph/low_dim_v15.hdf5"
with h5py.File(data, "r") as f:
    meta = json.loads(f["data"].attrs["env_args"])
rows = []
for seed in seeds:
    meta["env_kwargs"]["seed"] = seed      # a fresh env per seed, as in the eval job
    env = EnvUtils.create_env_from_metadata(env_meta=meta, render=False, render_offscreen=False,
                                            use_image_obs=False)
    with eval_csv.open() as fh:
        ref = {int(r["episode"]): (float(r["obj_x"]), float(r["obj_y"]))
               for r in csv.DictReader(fh) if int(r["seed"]) == seed}
    for i in range(len(ref)):
        env.reset()
        env.reset_to(env.get_state())          # same calls as upstream rollout()
        sim = env.env.sim                      # a hard reset rebuilds the sim: look it up each time
        addr, _ = sim.model.get_joint_qpos_addr(JOINT)
        q = sim.data.qpos[addr:addr + 7]       # x y z, quaternion wxyz
        yaw = Rotation.from_quat(np.roll(q[3:7], -1)).as_euler("xyz", degrees=True)[2]
        assert np.abs(np.array(ref[i]) - q[:2]).max() < 1e-4, f"seed {seed} episode {i} does not match"
        rows.append({"seed": seed, "episode": i, "obj_x": round(float(q[0]), 5),
                     "obj_y": round(float(q[1]), 5), "obj_yaw_deg": round(float(yaw), 1)})

out.parent.mkdir(exist_ok=True)
with out.open("w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
print(f"wrote {len(rows)} rows to {out}; all match {eval_csv.name}")
