# CLAIX jobs

Add Slurm scripts after validating the pinned upstream commands and resource settings.
Validated: `lift_replay.sh` (Lift replay check + MP4, CPU job 5813465).
Jobs invoke upstream training/replay/rollout entry points with an explicit environment,
configuration and external output location.

Use bounded CPU jobs for simulation and H100 jobs for training. Disable integrated
simulator rollouts in offline training configs. Do not launch a second allocation when
already in an interactive allocation. Record job ID, resolved command, resource usage
and exit status. Keep node/connection details and personal logs outside Git.
