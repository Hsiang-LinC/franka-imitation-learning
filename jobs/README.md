# CLAIX jobs

Add Slurm scripts after validating the pinned upstream commands and resource settings.
Validated: `lift_replay.sh` (Lift replay check + MP4, CPU job 5813465);
`lift_bc_rnn_cpu.sh` (BC-RNN low-dim Lift on CPU, jobs 5824723/5824724).
`lift_eval_cpu.sh` + `eval_checkpoints.py` (paired closed-loop checkpoint evaluation,
jobs 5844550–5844612, 5856229).
`make_run_config.py` writes a run's resolved robomimic config from a committed one.
Jobs invoke upstream training/replay/rollout entry points with an explicit environment,
configuration and external output location.

Use bounded CPU jobs for simulation and low-dim training, H100 jobs for image training (D1). Disable integrated
simulator rollouts in offline training configs. Do not launch a second allocation when
already in an interactive allocation. Record job ID, resolved command, resource usage
and exit status. Keep node/connection details and personal logs outside Git.
