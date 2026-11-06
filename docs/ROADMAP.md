# Learning roadmap

Build a reproducible Franka cube-stacking benchmark and compare BC-RNN with ACT. Hours are estimates of active work. Training wait time and infrastructure troubleshooting vary.

Track live status, acceptance evidence and dependencies in [GitHub Issues](https://github.com/Hsiang-LinC/franka-imitation-learning/issues) and the [Project dashboard](https://github.com/users/Hsiang-LinC/projects/3/views/1).

| Milestone | Exit gate | Estimate |
|---|---|---:|
| M0 · Project Foundation | Tracking, compute inventory and experiment conventions are usable. | 2–3h |
| M1 · Gymnasium Fundamentals | A seeded 2D reaching environment passes the Gymnasium checker and a reference rollout. | 3–5h |
| M2 · Robot Kinematics and IK | A tested planar arm reaches feasible targets and handles singular and unreachable targets. | 4–6h |
| M3 · Isaac Lab and Isaac Sim Setup | The pinned Franka task runs headless with IK control, state observations and an RGB frame. | 4–8h |
| M4 · Demonstrations and Mimic | Source and generated episodes replay and a versioned, leakage-checked dataset is ready. | 5–8h |
| M5 · BC-RNN Baseline | Own state and visuomotor checkpoints complete closed-loop rollouts. | 8–15h |
| M6 · Benchmark Framework | A frozen evaluation protocol yields repeatable ID and OOD reports. | 5–8h |
| M7 · ACT Integration | An ACT checkpoint runs on the same task and benchmark as BC-RNN. | 12–20h |
| M8 · Controlled Ablations | Matched comparisons, data budget and execution horizon sweeps are reported. | 6–12h |
| M9 · Portfolio Release | A reader can reproduce a smoke run and audit results and limitations. | 4–8h |
| S1 · Optional Diffusion Policy | A Diffusion Policy pilot uses the frozen benchmark. | Unscheduled |
| S2 · Optional SmolVLA | A SmolVLA pilot uses the frozen benchmark with documented language and input conventions. | Unscheduled |

M1–M2 can run locally or on university CPU nodes. In parallel, M0 can qualify university compute and M3 can check a supported RTX host. Use the official Isaac Lab release documentation for [Mimic and Robomimic](https://isaac-sim.github.io/IsaacLab/main/source/overview/imitation-learning/teleop_imitation.html). M6 freezes the benchmark before ACT evaluation. S1 and S2 do not block M9.

See [Compute](COMPUTE.md) for the paid RTX approval gate and [Experiment protocol](EXPERIMENT_PROTOCOL.md) for the data and policy handoff.
