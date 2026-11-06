# Franka Cube Stacking · Imitation Learning

A learning portfolio on simulated Franka Panda manipulation. Train ACT and Diffusion Policy offline from the same public MimicGen demonstrations, then compare their closed-loop performance on Franka three-cube stacking in robosuite and MuJoCo. This repository starts with the learning plan. Implementation, checkpoints and measured results will be linked as they become available.

| Start here | Purpose |
|---|---|
| [Roadmap](docs/ROADMAP.md) | M0–M9 milestones and acceptance criteria |
| [Project context](docs/PROJECT_CONTEXT.md) | How to resume work in a new session |
| [Compute plan](docs/COMPUTE.md) | CLAIX shared storage, CPU simulation and H100 training |
| [Experiment protocol](docs/EXPERIMENT_PROTOCOL.md) | Data, evaluation and reporting rules |
| [Decisions](docs/DECISIONS.md) | Rationale for the simulation/training split |

Track work in [GitHub Issues](https://github.com/Hsiang-LinC/franka-imitation-learning/issues), [Milestones](https://github.com/Hsiang-LinC/franka-imitation-learning/milestones) and the [Project dashboard](https://github.com/users/Hsiang-LinC/projects/3/views/1).

The owner’s Project includes the [Work Board](https://github.com/users/Hsiang-LinC/projects/3/views/1), [Milestones table](https://github.com/users/Hsiang-LinC/projects/3/views/2), and [Experiments view](https://github.com/users/Hsiang-LinC/projects/3/views/3). Public readers can follow the repository’s Issues and Milestones.

Start with the [Gymnasium rollout exercise](https://github.com/Hsiang-LinC/franka-imitation-learning/issues/3), then work through the reaching environment and planar arm exercises. Both run on CPU. In parallel, confirm CLAIX access in [M0.2](https://github.com/Hsiang-LinC/franka-imitation-learning/issues/2). The first simulator gate is [replaying one demonstration and recording a video on CPU](https://github.com/Hsiang-LinC/franka-imitation-learning/issues/9).
