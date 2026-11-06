# Decisions

## D001 · Separate simulation and policy training

**Context.** Isaac Sim has RTX host requirements. University compute nodes can cover CPU work and may provide compatible GPUs for PyTorch.

**Options.** A single supported RTX host simplifies a tutorial smoke run. Separate simulation and training hosts require a dataset/checkpoint handoff and allow university resources to cover training.

**Decision.** Keep the official Isaac Lab workflow for simulation and use separate environments for training and rollout. Define the handoff with a versioned manifest, checksums and observation/action metadata. Use the university first. Recheck this decision if the pinned official trainer imports simulator-only libraries or if transfer is restricted.

## D002 · Freeze the benchmark before ACT

**Context.** Model comparison requires the same data, observations and rollout protocol.

**Options.** Use the tutorial rollout alone for the baseline, or freeze a reusable evaluator and test manifest after the baseline smoke run.

**Decision.** Use the tutorial rollout for M5 integration and freeze the shared evaluator in M6 before ACT evaluation. Any protocol revision gets a new version and requires rerunning affected comparisons.

## D003 · Use MuJoCo/MimicGen and make ACT and Diffusion Policy core

**Context.** The primary learning goal is understanding and comparing ACT and Diffusion Policy. CLAIX has shared storage, CPU nodes and H100s. The original Isaac Sim path requires an additional supported RTX host to evaluate checkpoints and render videos.

**Convention and options.** Use a published simulator/dataset pair. The original Isaac Lab and Isaac Sim workflow follows NVIDIA's tutorial and offers RTX rendering. The robosuite and MuJoCo workflow follows the published MimicGen benchmark and supports CPU software rendering. It requires a validated environment pin and a shared HDF5-to-LeRobot conversion.

**Decision.** Adopt robosuite and MuJoCo with public MimicGen `stack_three_d0`. This supersedes the simulator choice in D001. Keep separate simulator and training environments on CLAIX. Preserve D002's benchmark freeze and apply it to both policies. BC-RNN is an optional reference. Require ACT and Diffusion Policy for M8 and M9. Keep GitHub issue identities and update native dependencies in place.

**Validation.** First demonstrate action playback, stack success and MP4 output on a CLAIX CPU node. Then verify that the adapter preserves camera timing, action semantics and episode resets before committing to full training.
