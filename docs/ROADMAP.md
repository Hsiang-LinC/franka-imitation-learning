# Learning roadmap

Baseline first, then method comparison, then controlled improvements
([decisions](DECISIONS.md)). Legacy M0–M9 numbers identify existing GitHub issues; the
phases below define the order. Live status:
[Issues](https://github.com/Hsiang-LinC/franka-imitation-learning/issues) and
[Project](https://github.com/users/Hsiang-LinC/projects/3/views/1).

| Phase | Legacy issues | Exit gate |
|---|---|---|
| 1 · BC-RNN baseline | M0 compute #2; M3 env/replay #8–9; M4 data #10–11; M5 BC-RNN #12 (state), #13 (vision, optional); report #15 | Own checkpoint reloads into the matching simulator; closed-loop success counts and success/failure videos with recorded settings |
| 2 · ACT vs Diffusion Policy | M6 frozen benchmark #14; M7 data #16, ACT #17, Diffusion #21 | Both methods evaluated on Square with matched RGB + proprioception inputs (D7), data, actions and identical held-out resets |
| 3 · Improvements + portfolio | M8 ablations #18, analysis #19; pretrained VLA PEFT #22 (D8); M9 portfolio #20 | Data-budget sweep that includes a PEFT-fine-tuned pretrained VLA, execution-horizon sweep, both with uncertainty; failure analysis, reproducible report and videos |

Optional: M1 Gymnasium #3–4, M2 FK/IK #5–7. Stretch after the portfolio: LIBERO (D8).

## Phase 1 order

0. **Lift warm-up** (D4), done: replay, BC-RNN low-dim training on CPU, reload,
   rollout with video.
1. Can and Square (ph) datasets downloaded with source and checksum; per-dataset
   simulator pins chosen by replay (D6), done.
2. Square: inspect observations/actions; freeze episode splits. (Can training skipped.)
   Steps 2–5 were run on CLAIX (2000-epoch training; failure analysis in progress);
   evidence is not yet pushed, so they stay open here.
3. Build the BC-RNN low-dim config from robomimic's templates; smoke run; reload check.
4. Full BC-RNN training on CLAIX CPU; evaluate saved checkpoints in `sim-square`.
5. Record successes/trials with Wilson intervals, failure examples, videos and
   settings (#15). Update the README.

## Phases 2–3 order

6. Container image (D9); acceptance: Square replay 181/200 inside it.
7. robomimic → LeRobotDataset conversion (images, lossless) pushed to the Hub (D10),
   with the protocol's alignment, round-trip and pairing tests; robosuite evaluation
   adapter for LeRobot policies.
8. Cloud setup (D11): sign up, quota, budget kill-switch; Lift image pilot that
   resumes after preemption; measure cost per training step and size the sweeps.
9. Freeze the benchmark (#14); train ACT and DP on Square RGB + proprioception,
   3 seeds; evaluate on CLAIX (phase-2 exit).
10. Pretrained VLA vs from scratch on Square across demonstration budgets (D8 arms),
    with inference latency; execution-horizon sweep.
11. Project page and README (D12).

Track B (D5) is paused until after phase 2.

A short training run proves integration, not task competence. The Lift warm-up has no
dedicated legacy issue yet.
