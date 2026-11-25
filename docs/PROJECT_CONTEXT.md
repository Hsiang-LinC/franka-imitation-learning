# Session handoff

## Current state (2026-11-25)

- Phase 1, step 0: **Lift warm-up** (D4) on route B. Sim venv installed and pins
  validated by full Lift ph replay (docs/BASELINE.md). Dataset inspection notebook
  `notebooks/00_lift_warmup.ipynb` done (covers most of 0.2).
- 0.3 done: trainer venv + 200-epoch BC-RNN low-dim Lift run on CPU (jobs 5824723/5824724,
  checkpoints every 20 epochs). Compute: low-dim on CLAIX CPU, image/VLA on cloud GPUs (D1).
- 0.4 done: paired rollout evaluation of all 10 checkpoints (seed 0, selection) and the
  selected epoch 200 on fresh seed 1: 49/50 (state-based; docs/BASELINE.md).
  Failure review done: missed grasps are never recovered (ph demos contain no recovery).
- Phase 1 step 1 (Can/Square replay): per-dataset simulator pins chosen by a MuJoCo
  version sweep (D6): Lift/Can on `sim` (MuJoCo 3.9.0), Square on `sim-square` (3.2.7).
  Square replays 181/200 at best; evidence in docs/BASELINE.md.
- PR #26 (`phase1/can-bc-rnn`): task-generic BC-RNN jobs, Can/Square data notebook,
  Can BC-RNN 2000 epochs (job 5929929) with evaluation and failure cross-check. main was
  merged into it on 2026-11-25 (no history rewrite). Further work sat unpushed on CLAIX,
  which was in maintenance on 2026-11-25. Next: on CLAIX `git pull` that branch, then
  push the rest, finish Square BC-RNN, record evidence in #12/#15.
- Phases 2–3 planned 2026-11-25 (PR #27): LeRobot + container (D9), Hub artifacts (D10),
  GCP Vertex Spot with €50 cap (D11), project page (D12), VLA arms on Square (D8).
- GPU: account `default` reaches `c23g`. The IT Center (2026-06) states a default of 10 GPU-h/month;
  the repo previously recorded 3 (unverified which applies). Image/VLA training moves to cloud (D11).
- CLAIX account remains valid for about one more year (user, 2026-11-25).
- Teaching mode: Claude writes a tested skeleton; the user fills TODOs at learning points.
  The user runs CLAIX jobs and approves every cloud provisioning step.
- Two learning tracks agreed (D5); Track B paused until after phase 2. ACT comes from LeRobot (D9).
- Lift warm-up is issue #23. Legacy issues #8–#21 still name MimicGen/stack_three;
  #22 still reads "optional stretch" (now D8, phase 3).

## Environment facts

- CLAIX: no Anaconda/Conda; use `venv` + `python -m pip`; uv not required. Upstream
  sources are cloned outside the repo, checked out at the pin, then `pip install -e .`.
- Available modules: `Python/3.11.5`, `Python/3.12.3` (default). System Python 3.9.25.
- Rendering: no system libOSMesa. `module load GCCcore/13.3.0 Python/3.11.5 Mesa/24.1.3`
  loads together (login node, 2026-11-15) and Mesa provides `libOSMesa.so.8`.
  OSMesa rendering verified inside a CPU job (5813465).
- Planned locations: upstream checkouts and venvs in `$WORK/franka-il/{src,venvs}`;
  data and runs in `$HPCWORK/franka-il/{data,runs}`.
- Venvs: `$WORK/franka-il/venvs/{sim,sim-square,train}`. The optional Gymnasium venv was
  deleted on 2026-11-21; recreate it from `exercises/gymnasium/README.md` if needed.
  Venvs are location-dependent: recreate rather than move; use explicit interpreter
  paths in Slurm jobs.

## Verified evidence

- Optional CartPole exercise: CPU jobs 5765498/5765504, see
  [exercise guide](../exercises/gymnasium/README.md).
- Lift ph replay: 200/200 open-loop successes + MP4, CPU job 5813465 (docs/BASELINE.md).
- BC-RNN low-dim Lift training on CPU: 200 epochs, ≈5.5 s/epoch (docs/BASELINE.md).
- Closed-loop evaluation: epoch 200 49/50 on a fresh seed, CPU job 5856229 (docs/BASELINE.md).

## Tracking

Issues/milestones follow the three phases with native dependencies
(#15 <- #12; #14/#16 <- #15; #17/#21 <- #14, #16; #8 blocked by #2). GitHub Project
layout/ordering is unsynchronized: the CLI token lacks `read:project`.
