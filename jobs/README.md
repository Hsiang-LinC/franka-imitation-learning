# CLAIX jobs

Add Slurm scripts after validating the pinned upstream commands and resource settings.
Validated: `replay.sh` (replay check + MP4, CPU job 5813465; Square uses the `sim-square` venv, D6);
`pin_sweep.sh` (replay check with other robosuite/MuJoCo versions layered over `sim`);
`lift_bc_rnn_cpu.sh` (BC-RNN low-dim Lift on CPU, jobs 5824723/5824724).
`lift_eval_cpu.sh` + `eval_checkpoints.py` (paired closed-loop checkpoint evaluation,
jobs 5844550–5844612, 5856229; failure videos 5863826/5863827).
`make_run_config.py` writes a run's resolved robomimic config from a committed one.
Jobs invoke upstream training/replay/rollout entry points with an explicit environment,
configuration and external output location.

Use bounded CPU jobs for simulation, low-dim training and evaluation; image and VLA training runs on cloud GPUs (D1, D11). Disable integrated
simulator rollouts in offline training configs. Do not launch a second allocation when
already in an interactive allocation. Record job ID, resolved command, resource usage
and exit status. Keep node/connection details and personal logs outside Git.
