# Experiment protocol

**Dataset.** Record dataset ID/checksum, source license, episode and source-demo lineage, generation config, observation keys/shapes/dtypes, camera preprocessing, action units/frame/convention, control frequency and episode boundaries. Group variants of a source demonstration in one split. Fit normalization on training data. Version the Robomimic-to-LeRobot conversion and test temporal alignment, action round-trip and RGB/proprioception pairing.

**Policies.** Use state-based BC-RNN for the first smoke test. Use matched RGB + proprioception inputs, action semantics and training split for the headline BC-RNN versus ACT comparison. Reset policy memory and pending action chunks on every episode reset. Report unmatched state-only comparisons separately.

**Evaluation.** Freeze separate development and held-out ID/OOD reset lists in M6. Define the OOD shift, episode horizon, stack success predicate and failure categories before running the headline evaluation. Run policies on identical test seeds and record per-episode success, failure mode, steps and duration. Aggregate successes/trials and uncertainty, with the same protocol for both policies. Use development episodes for tuning.

**Run record.** Save run ID, commit, dependency versions, hardware, dataset/manifest, config, training seed, checkpoint checksum, evaluation manifest, episode logs, metrics, runtime and cost. Store links in the experiment issue. Record failures such as missed grasp, dropped cube, unstable placement and timeout.

**Ablations.** Compare nested demonstration budgets and ACT execution horizon in separate sweeps. Keep all other variables fixed within each sweep, and report limited sample sizes and variance. For public reporting, include representative success and failure clips, baseline and ACT metrics, and the limits of simulation-only evaluation.
