# Experiment protocol

**Dataset.** Record dataset ID/checksum, source license, episode and available source-demo lineage, upstream generation metadata, observation keys/shapes/dtypes, camera preprocessing, action units/frame/convention, control frequency and episode boundaries. Group variants of a source demonstration in one split when lineage is available. Record missing lineage and split by complete episode. Fit normalization on training data. Version the Robomimic-to-LeRobot conversion and test temporal alignment, action round-trip and RGB/proprioception pairing.

**Policies.** Use matched RGB + proprioception inputs, action semantics and training split for ACT and Diffusion Policy. Log the predicted chunk length, executed prefix and diffusion denoising steps. Reset model state and pending chunks at every episode reset. Report BC-RNN separately as an optional reference and label any difference in inputs.

**Evaluation.** Freeze separate development and held-out ID/OOD reset lists in M6. Define the OOD shift, episode horizon, stack success predicate and failure categories before running the headline evaluation. Run policies on identical test seeds and record per-episode success, failure mode, steps and duration, plus policy inference latency measured on the same hardware. Aggregate successes/trials and uncertainty, with the same protocol for both policies. Use development episodes for tuning.

**Run record.** Save run ID, commit, dependency versions, hardware, dataset/manifest, config, training seed, checkpoint checksum, evaluation manifest, episode logs, metrics, runtime and cost. Store links in the experiment issue. Record failures such as missed grasp, dropped cube, unstable placement and timeout.

**Ablations.** Compare nested demonstration budgets and action execution horizon in separate sweeps. Keep all other variables fixed within each sweep, and report limited sample sizes and variance. For public reporting, include representative success and failure clips, ACT and Diffusion Policy metrics, and the limits of simulation-only evaluation.
