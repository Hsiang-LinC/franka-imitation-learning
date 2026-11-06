# Learning roadmap

Train ACT and Diffusion Policy with the same public demonstrations and compare their closed-loop behavior on the matching Franka three-cube stacking task. Track status, acceptance evidence and prerequisites in [Issues](https://github.com/Hsiang-LinC/franka-imitation-learning/issues) and the [Project dashboard](https://github.com/users/Hsiang-LinC/projects/3/views/1).

| Milestone | Exit gate |
|---|---|
| M0 · Foundation | Tracking is usable and CLAIX storage, CPU and H100 jobs have been checked. |
| M1 · Gymnasium | A seeded 2D reaching environment passes the environment checker and a reference rollout. |
| M2 · Robot kinematics and IK | A tested planar arm reaches feasible targets and handles singular and unreachable targets. |
| M3 · robosuite and MuJoCo | A CLAIX CPU job executes a recorded Franka action sequence from the saved initial state, verifies task success and produces an MP4. |
| M4 · Public demonstrations | Inspect the MimicGen HDF5 and freeze a versioned episode split with synchronized observations and actions. |
| M5 · BC-RNN reference (optional) | Run state or visuomotor BC-RNN as a reference if useful. |
| M6 · Benchmark | Freeze the evaluator and development, ID and OOD test cases before comparing trained policies. The BC-RNN benchmark report is optional. |
| M7 · ACT and Diffusion Policy | Convert one shared dataset, train both policies offline and evaluate both checkpoints through the same simulator interface. |
| M8 · Controlled ablations | Compare success, failures and inference latency, then isolate training data budget and execution horizon in separate sweeps. |
| M9 · Portfolio | Publish reproduction steps, benchmark results, and videos of successful and failed closed-loop rollouts. |
| S2 · SmolVLA (optional) | Run a pilot on the shared benchmark with documented language and input conventions. |

Start M1–M2 on CPU while qualifying CLAIX and preparing M3. For M3, use [MimicGen `stack_three_d0.hdf5`](https://huggingface.co/datasets/amandlek/mimicgen_datasets/tree/main/core) and the [upstream compatibility instructions](https://github.com/NVlabs/mimicgen/blob/main/docs/introduction/installation.md). The [first replay issue](https://github.com/Hsiang-LinC/franka-imitation-learning/issues/9) contains the bounded smoke command. M7 trains on CLAIX H100s and M6–M9 use the CPU simulator for evaluation. See [Compute](COMPUTE.md) and the [Experiment protocol](EXPERIMENT_PROTOCOL.md).
