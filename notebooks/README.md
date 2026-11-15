# Notebooks

Notebooks explain, inspect and analyze. Long training and rollouts run as Slurm jobs
(`jobs/`); Run All must never launch them. Each notebook states purpose, kernel/venv,
inputs, outputs and success checks, and reopens from persisted files without running
earlier notebooks. Keep outputs small and free of private paths.

| Planned notebook | Track | Inputs → outputs |
|---|---|---|
| 00_lift_warmup | A | Lift dataset, replay MP4, checkpoint → inspection notes, rollout results |
| 01_square_data | A | Square ph/mh datasets → obs/action inspection, frozen split |
| 02_bc_rnn_baseline | A | Run ID, checkpoint, rollout metrics → baseline analysis and videos |
| Minimal diffusion policy | B | Low-dim Lift data → own DP, compared with upstream |
| Minimal action chunking (ACT-style) | B | Same data → own chunking policy, compared with upstream |
| Later: method comparison, sweeps, report | A | Frozen evaluator results → figures and write-up |

Track B code can graduate into `src/` once a notebook outgrows it or a job needs it.
Use the kernel matching the work: sim env for replay/rollout inspection, trainer env
for model code. Never install a second stack into a running kernel.
