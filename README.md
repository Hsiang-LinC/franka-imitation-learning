# Franka Imitation Learning

Hands-on imitation learning on simulated Franka Panda three-cube stacking (robosuite +
MuJoCo, MimicGen data). Reproduce a BC-RNN baseline, compare ACT and Diffusion Policy
under matched conditions, then study demonstration budget and action execution horizon.
Progress is measured by closed-loop task success, not training loss.

## Plan

1. **Baseline:** Lift warm-up, then BC-RNN on `stack_three_d0`: replay, train, reload,
   evaluate with metrics and video.
2. **Method comparison:** ACT and Diffusion Policy with matched data, observations,
   actions and a frozen evaluator.
3. **Controlled improvements:** one-factor sweeps, failure analysis, reproducible report.

Two tracks run side by side: upstream code (MimicGen/robomimic) produces reported
results; small from-scratch implementations explain how the methods work.

| Doc | Purpose |
|---|---|
| [Roadmap](docs/ROADMAP.md) | Phases, exit gates, issue mapping |
| [Baseline](docs/BASELINE.md) | Version pins, upstream entry points, handoffs |
| [Session context](docs/PROJECT_CONTEXT.md) | Current state and next step |
| [Decisions](docs/DECISIONS.md) | Current design decisions and open questions |
| [Compute](docs/COMPUTE.md) | CPU simulation, H100 training, storage |
| [Experiment protocol](docs/EXPERIMENT_PROTOCOL.md) | Fair comparisons and run records |

## Layout

```text
notebooks/     Inspection, from-scratch learning implementations, result analysis
configs/       Experiment settings derived from pinned upstream configs
jobs/          Slurm scripts calling upstream entry points
requirements/  Tested dependency pins per environment
exercises/     Optional supporting exercises
docs/          Plan, decisions and evidence
```

Upstream checkouts, datasets, checkpoints and videos live outside this repository.

## Status

Phase 1, Lift warm-up: pins selected, robot environment not yet installed. No
replay, training or evaluation has run.
Track work in [Issues](https://github.com/Hsiang-LinC/franka-imitation-learning/issues)
and the [Project](https://github.com/users/Hsiang-LinC/projects/3/views/1).
