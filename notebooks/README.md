# Notebooks

Jobs do the work, notebooks show and explain it. Training, rollouts, replay and data
validation run as scripts (`jobs/`, via Slurm on CLAIX or `!python jobs/...` on a GPU host);
they write small persisted artifacts (`results/*.csv`, `results/*.json`, run IDs, checkpoint
paths). Notebooks only read those artifacts, so Run All never launches a job and each
notebook reopens without running earlier ones. Each notebook opens with purpose, kernel/venv,
inputs, outputs, runtime and success check. Keep outputs small and free of private paths.

## Chapters

Numbered in reading order; one purpose per notebook.

| Notebook | Track | Inputs → outputs |
|---|---|---|
| 00_lift_warmup | A | Lift dataset, replay MP4 → inspection notes |
| 00b_lift_eval_analysis | A | `results/lift_eval_episodes.csv` → success and paired-outcome figures |
| 01_can_square_data | A | Can and Square ph datasets → object/action/length inspection, `results/data_manifest.json` |
| 02_bc_rnn_baseline | A | Can and Square paired eval results → checkpoint selection, report-seed success, failure clips |
| Minimal diffusion policy | B | Low-dim Lift data → own DP, compared with upstream |
| Minimal action chunking (ACT-style) | B | Same data → own chunking policy, compared with upstream |
| Later: method comparison, sweeps | A | Frozen evaluator results → figures |
| 99_summary | – | Results of all chapters → portfolio overview |

## Videos

Full rollout and replay MP4s stay in run storage (`$HPCWORK/franka-il/runs/...`).
`jobs/make_clips.py` cuts representative episodes (a typical success, one per failure mode)
into small animated WebP clips (160 px, about 100–300 KB; GIF would be ~10× larger) in
`docs/media/`. Notebooks embed them in **markdown** cells
(`![square: jams on peg](../docs/media/square_jam.webp)`), which
GitHub, VS Code and Colab all render without growing the notebook. `IPython.display.Video`
on a run-storage path is for local review only; clear such outputs before committing.

## GPU hosts (Colab, rented GPUs)

`colab/` holds launcher notebooks only: clone the repository at a recorded commit, install
from `requirements/*.txt`, mount persistent storage (Drive) for data and checkpoints so a
disconnected session can resume, run the same `jobs/` scripts, and copy the small result
files back into `results/`. Analysis chapters stay unchanged whatever host produced the
results.

## Shared code

Track B code and helpers used by a second notebook (e.g. Wilson intervals and paired
comparisons from 00b, needed again in 02) move into `src/`. Use the kernel matching the
work: sim env for replay/rollout inspection, trainer env for model code. Never install a
second stack into a running kernel.
