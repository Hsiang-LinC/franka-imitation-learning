# Franka Cube Stacking · Imitation Learning

A learning portfolio on simulated Franka Panda manipulation. The goal is to reproduce a Robomimic BC-RNN baseline, integrate LeRobot ACT, and compare both on the same Isaac Lab cube-stacking benchmark. This repository starts with the learning plan. Implementation, checkpoints and measured results will be linked as they become available.

| Start here | Purpose |
|---|---|
| [Roadmap](docs/ROADMAP.md) | M0–M9 milestones and acceptance criteria |
| [Project context](docs/PROJECT_CONTEXT.md) | How to resume work in a new session |
| [Compute plan](docs/COMPUTE.md) | University CPU/GPU, RTX simulator and spending approval |
| [Experiment protocol](docs/EXPERIMENT_PROTOCOL.md) | Data, evaluation and reporting rules |
| [Decisions](docs/DECISIONS.md) | Rationale for the simulation/training split |

Track work in [GitHub Issues](https://github.com/Hsiang-LinC/franka-imitation-learning/issues), [Milestones](https://github.com/Hsiang-LinC/franka-imitation-learning/milestones) and the [Project dashboard](https://github.com/Hsiang-LinC/franka-imitation-learning/projects).

Start with the Gymnasium reaching environment and planar arm exercises. Both run on CPU. The first hardware-dependent gate is the Isaac Sim compatibility check in M3.
