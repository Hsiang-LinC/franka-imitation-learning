# Learning notebooks

One notebook per clear purpose, with several notebooks in each phase. These chapters
are planned; no robot notebook has been implemented or executed yet.

| Planned notebook | Inputs | Persisted outputs |
|---|---|---|
| 01_environment_and_replay.ipynb | Pinned upstream stack, source dataset | Environment check, replay evidence/video, dataset provenance |
| 02_bc_rnn_training.ipynb | Inspected observation data, frozen split | Resolved training config, Slurm job/run ID, checkpoint reference |
| 03_baseline_evaluation.ipynb | Checkpoint and development evaluation settings | Per-episode metrics, videos, baseline analysis |
| Later: shared benchmark | Validated baseline/data interfaces | Frozen ID/OOD manifests, conversion validation |
| Later: ACT/Diffusion comparison | Shared dataset/config/evaluator | Matched method results |
| Later: controlled experiments/report | Fixed comparison and sweep settings | Ablation results, figures, report |

Every notebook starts with purpose, prerequisites, explicit kernel/environment, inputs,
outputs and success checks. Short cells inspect data and results. Long tasks use explicit
Slurm submissions; Run All must never silently launch full training. Reopening a chapter
must work from persisted inputs without running earlier notebooks.

There is no one-to-one notebook/script pairing. Several chapters can use the same upstream
script. Use explicit interpreter paths for simulator versus training jobs; never switch
Python environments by installing incompatible stacks into one live kernel. Keep outputs
small and sanitized; reference large artifacts outside Git.
