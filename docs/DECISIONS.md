# Decisions

Current decisions only. Superseded options (an earlier Isaac Lab/Isaac Sim route,
exercise-first ordering, optional BC-RNN) are kept in Git history.

## D1 · Simulator, task and compute split

robosuite + MuJoCo with the public MimicGen `stack_three_d0` dataset as the fixed main
task. It renders on CLAIX CPU nodes (`MUJOCO_GL=osmesa`) without an RTX host. Simulation
(replay, rollout, video) runs in CPU jobs; offline training runs in H100 jobs, in a
separate Python environment. Checkpoints and datasets are exchanged through shared
storage with checksums.

## D2 · Baseline first, upstream code reused

Phase 1 reproduces BC-RNN end to end with upstream MimicGen/robomimic entry points;
phase 2 compares ACT and Diffusion Policy; phase 3 runs controlled sweeps and packages
the portfolio. We own configs, Slurm jobs, notebooks and evidence, not copies of
upstream trainers. Gymnasium and FK/IK are optional lessons.

## D3 · Freeze the benchmark before headline comparisons

Phase 1 uses development rollouts. Before ACT/Diffusion headline numbers, freeze the
evaluator, reset lists (ID/OOD) and success predicate. Any protocol change gets a new
version and the affected methods are rerun.

## D4 · Lift warm-up before stack_three (2026-11-15)

Run the full replay → train → reload → rollout → video loop on robomimic Lift
(proficient-human, low-dim) first. Lift is short and reliably learnable, so failures
isolate environment/rendering/Slurm problems rather than task difficulty. Use the same
pins as the stack_three stack so the environment carries over unchanged. Lift results
are a pipeline check, not portfolio results.

## D5 · Two learning tracks (2026-11-15)

- **Track A, reproduction:** upstream scripts, configs and Slurm jobs produce all
  reported numbers.
- **Track B, understanding:** small from-scratch implementations (diffusion policy,
  action chunking) in notebooks or `src/`, trained on the same low-dim data and compared
  against Track A. They exist to explain mechanisms; they never replace upstream
  results in headline tables unless evaluated under the frozen protocol.

## Open question · Diffusion Policy implementation (phase 2)

`DiffusionPolicyUNet` exists only in robomimic v0.5.0, whose released datasets target
robosuite v1.5. MimicGen does not support robosuite v1.5+. Options to evaluate before
phase 2: robomimic v0.5 in the offline trainer env with rollout in the 1.4.1 sim env
(checkpoint loading compatibility unverified), or a separate DP implementation with a
data conversion. ACT is not in robomimic at any version.
