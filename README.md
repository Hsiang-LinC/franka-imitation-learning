# Franka Imitation Learning

An end-to-end learning and experiment project on simulated Franka Panda three-cube
stacking. First reproduce an upstream BC-RNN pipeline, then compare ACT and Diffusion
Policy, and investigate demonstration budget and action execution settings.
Progress means measured closed-loop task performance; the robot is held fixed.

## Three phases

1. **End-to-end baseline:** pin the environment, replay a public demonstration, train
   BC-RNN, reload its checkpoint and evaluate closed-loop behavior with metrics/video.
2. **Method comparison:** integrate ACT and Diffusion Policy using matched data,
   observations, action semantics and a frozen evaluator.
3. **Controlled improvements:** test one factor at a time, analyze failures and publish
   a reproducible report with successful and failed rollouts.

The baseline uses existing MimicGen and robomimic code. We own the learning notebooks,
experiment settings, Slurm integration and evidence. Gymnasium and FK/IK are optional
support exercises, introduced when useful.

## Start here

| Resource | Purpose |
|---|---|
| [Baseline guide](docs/BASELINE.md) | Upstream code, execution flow and artifact handoffs |
| [Roadmap](docs/ROADMAP.md) | Three phases, exit gates and existing issue mapping |
| [Notebook plan](notebooks/README.md) | Chapter boundaries, execution and kernel rules |
| [Session context](docs/PROJECT_CONTEXT.md) | Verified state, tracking discrepancies and pending work |
| [Compute](docs/COMPUTE.md) | CPU simulation, H100 training and storage |
| [Experiment protocol](docs/EXPERIMENT_PROTOCOL.md) | Fair comparisons and run records |
| [Decisions](docs/DECISIONS.md) | Design rationale and superseded choices |

## Layout

```text
notebooks/       Learning narratives, inspection and result analysis
configs/         Project settings derived from pinned upstream configurations
jobs/            Slurm submissions invoking upstream tools
requirements/    Tested environment dependencies
exercises/       Optional supporting exercises
docs/           Workflow, evidence and decisions
```

External upstream checkouts and full data/run artifacts live outside this repository.
There is no custom trainer or evaluator yet; no empty src/ framework is required.
Read the directory guides before adding files. Notebook chapters are planned, not
implemented; this reorganization does not install or execute the robot baseline.

## Current status

- Verified: optional headless CartPole exercise, deterministic trace and time-limit
  behavior in CLAIX CPU jobs; see [exercise guide](docs/M1_FIRST_RUN.md).
- Pending: simulator environment, dataset download/inspection, action replay, BC-RNN
  training, checkpoint deployment, evaluation and all method comparisons.
- Current phase: **1 — baseline preparation**, legacy M0/M3 issues #2 and #8.
- Issues, milestones and native dependencies now follow the three phases; Project
  layout/ordering remains pending due to missing Project access.

Track work in [Issues](https://github.com/Hsiang-LinC/franka-imitation-learning/issues)
and the [Project](https://github.com/users/Hsiang-LinC/projects/3/views/1).
