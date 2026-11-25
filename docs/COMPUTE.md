# Compute plan

Clone once to a CLAIX filesystem shared by the login and compute nodes. Submit workloads from the login node through Slurm. Store datasets, checkpoints, videos and logs in approved shared storage outside Git. Record quota and retention rules before choosing locations.

| Workload | Preferred compute | Preflight |
|---|---|---|
| Gymnasium, NumPy FK/IK, HDF5 inspection and dataset conversion | Mac or CLAIX CPU | Verify Python, storage and job limits |
| MuJoCo simulation, demonstration playback, policy rollout and MP4 recording | CLAIX CPU | Verify the pinned robosuite environment and OSMesa/EGL rendering with one bounded episode |
| BC-RNN low-dim training | CLAIX CPU | Trainer venv, validated on Lift (docs/BASELINE.md) |
| Image-based ACT, Diffusion Policy and SmolVLA training | GCP Vertex AI Spot L4, container image (DECISIONS D9, D11) | Quota granted, budget kill-switch tested, resume after preemption verified on a pilot |
| Evaluation of LeRobot checkpoints | CLAIX CPU, same image via Apptainer | Square replay 181/200 inside the image |

Keep simulator and trainer dependencies in separate environments. Disable integrated simulator rollouts in offline trainer settings and evaluate saved checkpoints in the simulator environment. Share the versioned dataset, manifest and checkpoint through CLAIX storage. Check hashes across transfers. The core route uses CPU software rendering with `MUJOCO_GL=osmesa`. If the CPU job cannot initialize OSMesa, record the failure and verify the required libraries are available through an approved environment before advancing.

The core roadmap uses no RTX resources. Cloud GPU spend is capped at €50 beyond the GCP credit with an automatic billing kill-switch (D11). Each provisioning step still requires explicit approval. Datasets and checkpoints move through Hugging Face Hub (D10). Large CLAIX transfers run on the copy nodes (`copy23-1/2`), not login nodes.

Notebooks document, inspect and analyze; Slurm runs long jobs independently of the
notebook connection. GPU interactive rendering is an optional development route, pending
display/OpenGL validation; it does not replace the CPU replay acceptance check.
