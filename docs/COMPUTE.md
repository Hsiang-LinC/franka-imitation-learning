# Compute plan

Clone once to a CLAIX filesystem shared by the login and compute nodes. Submit workloads from the login node through Slurm. Store datasets, checkpoints, videos and logs in approved shared storage outside Git. Record quota and retention rules before choosing locations.

| Workload | Preferred compute | Preflight |
|---|---|---|
| Gymnasium, NumPy FK/IK, HDF5 inspection and dataset conversion | Mac or CLAIX CPU | Verify Python, storage and job limits |
| MuJoCo simulation, demonstration playback, policy rollout and MP4 recording | CLAIX CPU | Verify the matching robosuite/MimicGen environment and Linux OSMesa with one bounded episode |
| ACT and Diffusion Policy offline training | CLAIX H100 | Check CUDA/PyTorch access, batch size, checkpoint writes and restart procedure |
| Optional training fallback | Existing Colab allowance, up to the reported 50 CCUs/month when available | Verify entitlement and runtime consumption |

Keep simulator and trainer dependencies in separate environments. Share the versioned dataset, manifest and checkpoint through CLAIX storage. Check hashes across transfers. The core route uses CPU software rendering with `MUJOCO_GL=osmesa`. If the CPU job cannot initialize OSMesa, record the failure and verify the required libraries are available through an approved environment before advancing.

The core roadmap uses no RTX resources. Any later paid cloud GPU provisioning or spend requires explicit approval with a cost cap and shutdown plan.
