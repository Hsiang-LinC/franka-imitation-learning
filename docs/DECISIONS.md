# Decisions

Current decisions only. Superseded options (an earlier Isaac Lab/Isaac Sim route,
exercise-first ordering, optional BC-RNN) are kept in Git history.

## D1 · Simulator, task and compute split (revised 2026-11-17)

Current stack: robosuite v1.5.x + MuJoCo 3.x + robomimic v0.5+, with robomimic's
v1.5 Franka datasets. Task ladder: Lift (warm-up) → Can → **Square** (main task);
Transport/ToolHang are optional stretch tasks. Reasons: BC-RNN and Diffusion Policy
share one maintained framework, and Square has published Diffusion Policy results to
sanity-check against. This replaces MimicGen `stack_three_d0`, whose robosuite ≤1.4.1
pin blocked modern MuJoCo and robomimic's Diffusion Policy.

MuJoCo needs no RTX GPU (unlike Isaac Sim): physics runs on CPU and rendering uses
OpenGL via OSMesa (CPU) or EGL. Simulation runs in CLAIX CPU jobs. Offline training
runs in a separate, simulator-free Python environment: **low-dim training on CPU**,
H100 jobs reserved for image-based training (RGB encoders) and phase-2 methods where
CPU is measured too slow. Reason: BC-RNN low-dim Lift trains at ≈5.5 s/epoch on CPU and
does not speed up beyond ~2 cores (docs/BASELINE.md), so a full 2000-epoch run costs
≈13 core-h, while the student GPU quota is 3 GPU-h/month and GPU queues are long.
Datasets and checkpoints move through shared storage with checksums.

## D2 · Baseline first, upstream code reused

Phase 1 reproduces BC-RNN end to end with upstream robomimic entry points;
phase 2 compares ACT and Diffusion Policy; phase 3 runs controlled sweeps and packages
the portfolio. We own configs, Slurm jobs, notebooks and evidence, not copies of
upstream trainers. Gymnasium and FK/IK are optional lessons.

## D3 · Freeze the benchmark before headline comparisons

Phase 1 uses development rollouts. Before ACT/Diffusion headline numbers, freeze the
evaluator, reset lists (ID/OOD) and success predicate. Any protocol change gets a new
version and the affected methods are rerun.

## D4 · Lift warm-up before the main task (2026-11-15)

Run the full replay → train → reload → rollout → video loop on robomimic Lift
(proficient-human, low-dim) first. Lift is short and reliably learnable, so failures
isolate environment/rendering/Slurm problems rather than task difficulty. Use the same
pins as the main task so the environment carries over unchanged. Lift results
are a pipeline check, not portfolio results.

## D5 · Two learning tracks (2026-11-15)

- **Track A, reproduction:** upstream scripts, configs and Slurm jobs produce all
  reported numbers.
- **Track B, understanding:** small from-scratch implementations (diffusion policy,
  action chunking) in notebooks or `src/`, trained on the same low-dim data and compared
  against Track A. They exist to explain mechanisms; they never replace upstream
  results in headline tables unless evaluated under the frozen protocol.

## Open question · ACT implementation (phase 2)

robomimic v0.5 provides BC-RNN and `DiffusionPolicyUNet`; no robomimic version has ACT.
Options before phase 2: LeRobot ACT with a dataset conversion, or a Track B
implementation evaluated under the frozen protocol.
