# Project context

The core deliverable is a reproducible comparison of LeRobot ACT and Diffusion Policy trained offline from public MimicGen demonstrations and evaluated in the matching robosuite/MuJoCo Franka three-cube stacking task. Gymnasium and planar FK/IK are CPU learning exercises. BC-RNN is an optional reference and SmolVLA is a stretch goal.

## Resume a session

1. Open the [GitHub Project](https://github.com/users/Hsiang-LinC/projects/3/views/1) or [open issues](https://github.com/Hsiang-LinC/franka-imitation-learning/issues?q=is%3Aissue+is%3Aopen) and select the first core issue whose native blockers are closed.
2. Read its acceptance checklist, linked evidence and milestone. Check the latest code and applicable constraints in [Compute](COMPUTE.md) and [Experiment protocol](EXPERIMENT_PROTOCOL.md).
3. Leave the issue with the commands, artifact links and verified outcomes needed by the next session. Close it when its acceptance criteria pass. Keep partial progress and failures in the issue.

CLAIX login and compute nodes share a filesystem. M0 verifies the job environment and M3 verifies the simulator with a bounded action replay. Training and rollout results are pending.
