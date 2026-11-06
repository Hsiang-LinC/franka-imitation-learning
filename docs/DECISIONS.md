# Decisions

## D001 · Separate simulation and policy training

**Context.** Isaac Sim has RTX host requirements. University compute nodes can cover CPU work and may provide compatible GPUs for PyTorch.

**Options.** A single supported RTX host simplifies a tutorial smoke run. Separate simulation and training hosts require a dataset/checkpoint handoff and allow university resources to cover training.

**Decision.** Keep the official Isaac Lab workflow for simulation and use separate environments for training and rollout. Define the handoff with a versioned manifest, checksums and observation/action metadata. Use the university first. Recheck this decision if the pinned official trainer imports simulator-only libraries or if transfer is restricted.

## D002 · Freeze the benchmark before ACT

**Context.** Model comparison requires the same data, observations and rollout protocol.

**Options.** Use the tutorial rollout alone for the baseline, or freeze a reusable evaluator and test manifest after the baseline smoke run.

**Decision.** Use the tutorial rollout for M5 integration and freeze the shared evaluator in M6 before ACT evaluation. Any protocol revision gets a new version and requires rerunning affected comparisons.
