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
2. Can and Square: inspect observations/actions; freeze episode splits
   (`notebooks/01_can_square_data.ipynb`, `results/data_manifest.json`).
   Can BC-RNN (2000 epochs, job 5929929) and its failure analysis are in PR #26.
   Square BC-RNN follows the same jobs; its evidence is not yet pushed, so steps 3–5
   stay open here.
   Optional check: do policy failures cluster where replay fails (peg jam)? If so, train
   on the 181 replay-consistent demos vs all 200 and compare on the same reset seeds.
3. Build the BC-RNN low-dim config from robomimic's templates; smoke run; reload check.
4. Full BC-RNN training on CLAIX CPU; evaluate saved checkpoints in `sim-square`.
5. Record successes/trials with Wilson intervals, failure examples, videos and
   settings (#15). Update the README.

## Phases 2–3 order

Rough schedule: steps 2–5 about one week; 6–8 about two; 9 about two; 10 two to three;
11 about one. Re-plan after the step-8 pilot.

6. Container image (D9), built by GitHub Actions; acceptance: Square replay in it statistically consistent with
   `sim-square` (D9).
7. Render 84×84 images from Square states (the Hub has no Square image file), convert to
   LeRobotDataset (images, lossless) and push to the Hub (D10). Tests: alignment,
   round-trip and pairing per the protocol. Open: normalization stats per budget from
   training episodes only (check LeRobot support; else one dataset revision per budget).
   Robosuite evaluation adapter for LeRobot policies.
8. Cloud setup (D11): sign up, quota, budget kill-switch; Lift image pilot that
   resumes after preemption; measure cost per training step and size the sweeps.
9. Freeze the benchmark (#14); train ACT and DP on Square RGB + proprioception,
   3 seeds; evaluate on CLAIX (phase-2 exit).
10. Pretrained VLA vs from scratch on Square across demonstration budgets (D8 arms),
    with inference latency; execution-horizon sweep.
11. Project page and README (D12).

Track B (D5) is paused until after phase 2. Layout added only as steps need it:
`containers/`, `pyproject.toml` + `src/franka_il/` (conversion, rollout adapter),
`tests/`, `cloud/` (Vertex job specs, billing kill-switch).

A short training run proves integration, not task competence. The Lift warm-up has no
dedicated legacy issue yet.
