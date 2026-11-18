# Session handoff

## Current state (2026-11-18)

- Phase 1, step 0: **Lift warm-up** (D4) on route B. Sim venv installed and pins
  validated by full Lift ph replay (docs/BASELINE.md). Dataset inspection notebook
  `notebooks/00_lift_warmup.ipynb` done (covers most of 0.2).
- 0.3 done: trainer venv + 200-epoch BC-RNN low-dim Lift run on CPU (jobs 5824723/5824724,
  checkpoints every 20 epochs). Compute decision: low-dim training on CPU, H100 for images (D1).
- 0.4 done: paired rollout evaluation of all 10 checkpoints (seed 0, selection) and the
  selected epoch 200 on fresh seed 1: 49/50 (state-based; docs/BASELINE.md).
- Next hands-on step: review the eval videos for failure modes, then post 0.4 evidence to
  #23 and move to Can (phase 1 step 1).
- GPU: account `default` reaches `c23g`, but the student quota is 3 GPU-h/month.
- Teaching mode: Claude writes a tested skeleton; the user fills TODOs at learning points.
- Two learning tracks agreed (D5). ACT implementation is open for phase 2.
- Lift warm-up is issue #23. Legacy issues #8–#21 still name MimicGen/stack_three.

## Environment facts

- CLAIX: no Anaconda/Conda; use `venv` + `python -m pip`; uv not required. Upstream
  sources are cloned outside the repo, checked out at the pin, then `pip install -e .`.
- Available modules: `Python/3.11.5`, `Python/3.12.3` (default). System Python 3.9.25.
- Rendering: no system libOSMesa. `module load GCCcore/13.3.0 Python/3.11.5 Mesa/24.1.3`
  loads together (login node, 2026-11-15) and Mesa provides `libOSMesa.so.8`.
  OSMesa rendering verified inside a CPU job (5813465).
- Planned locations: upstream checkouts and venvs in `$WORK/franka-il/{src,venvs}`;
  data and runs in `$HPCWORK/franka-il/{data,runs}`.
- `.venvs/franka-foundations` (Python 3.11.5) is only for the optional Gymnasium
  exercise. Its activation scripts were repaired on 2026-11-15 after a path move.
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
