# Learning roadmap

Baseline first, then method comparison, then controlled improvements
([decisions](DECISIONS.md)). Legacy M0–M9 numbers identify existing GitHub issues; the
phases below define the order. Live status:
[Issues](https://github.com/Hsiang-LinC/franka-imitation-learning/issues) and
[Project](https://github.com/users/Hsiang-LinC/projects/3/views/1).

| Phase | Legacy issues | Exit gate |
|---|---|---|
| 1 · BC-RNN baseline | M0 compute #2; M3 env/replay #8–9; M4 data #10–11; M5 BC-RNN #12 (state), #13 (vision, optional); report #15 | Own checkpoint reloads into the matching simulator; closed-loop success counts and success/failure videos with recorded settings |
| 2 · ACT vs Diffusion Policy | M6 frozen benchmark #14; M7 data #16, ACT #17, Diffusion #21 | Both methods evaluated with matched inputs, data, actions and identical held-out resets |
| 3 · Improvements + portfolio | M8 ablations #18, analysis #19; M9 portfolio #20 | Data-budget and execution-horizon sweeps with uncertainty, failure analysis, reproducible report and videos |

Optional: M1 Gymnasium #3–4, M2 FK/IK #5–7. Stretch after phase 3: S2 SmolVLA #22.

## Phase 1 order

0. **Lift warm-up** (D4): pin the sim env, replay one Lift demo to MP4 on a CPU job,
   train BC-RNN low-dim briefly on H100, reload the checkpoint, roll out with video.
1. Download Can, then Square (ph) datasets; record source and checksum; replay one demo.
2. Inspect observations/actions; freeze episode splits.
3. Build the BC-RNN config from robomimic's templates; training smoke run; reload check.
4. Full BC-RNN training; evaluate saved checkpoints separately in the simulator.
5. Record successes/trials, failure examples, videos and settings (#15).

## Track B (understanding, alongside phases 1–2)

Minimal from-scratch diffusion policy and action-chunking policy on low-dim data,
first on Lift, compared with upstream results (D5).

A short training run proves integration, not task competence. The Lift warm-up has no
dedicated legacy issue yet.
