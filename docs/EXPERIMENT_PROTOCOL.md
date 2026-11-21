# Experiment protocol

**Dataset.** Record dataset ID/checksum, source license, episode and available source-demo lineage, upstream generation metadata, observation keys/shapes/dtypes, camera preprocessing, action units/frame/convention, control frequency and episode boundaries. Group variants of a source demonstration in one split when lineage is available. Record missing lineage and split by complete episode. Fit normalization on training data. If a method needs a converted dataset format, version the conversion and test temporal alignment, action round-trip and RGB/proprioception pairing.

**Policies.** Use matched RGB + proprioception inputs, action semantics and training split for ACT and Diffusion Policy. Log the predicted chunk length, executed prefix and diffusion denoising steps. Reset model state and pending chunks at every episode reset. BC-RNN is the required phase-1 integration baseline. Label its input modality, including privileged object state. Include it in direct method comparisons only with matched inputs and evaluation.

**Evaluation.** Use development rollouts for phase 1; freeze separate development and held-out ID/OOD reset lists in phase 2 (legacy M6). Define the OOD shift, episode horizon, stack success predicate and failure categories before running the headline evaluation. Run policies on identical test seeds and record per-episode success, failure mode, steps and duration, plus policy inference latency measured on the same hardware. Use the same protocol for all policies. Statistical rules (rationale: `notebooks/00b_lift_eval_analysis.ipynb` §4):

1. Selection seeds choose checkpoints and hyperparameters. Report seeds evaluate only the final chosen setting, once; a seed set used for any choice becomes a selection set.
2. Report successes/trials with a Wilson 95% interval. Compare policies on the same reset seeds with an exact McNemar test on discordant episodes; overlapping intervals are not a test.
3. Fix the episode count before the run from a power analysis that states the smallest difference to detect. Exact McNemar needs at least 6 one-sided discordant episodes for p < 0.05. Separating 98% from 100% needs about 500 episodes; 90% from 98% needs about 100–200.
4. Do not compare methods on tasks where they are near 100%; pick tasks or demo budgets with mid-range success.

**Run record.** Save run ID, commit, dependency versions, hardware, dataset/manifest, config, training seed, checkpoint checksum, evaluation manifest, episode logs, metrics, runtime and cost. Store links in the experiment issue. Record failures such as missed grasp, dropped cube, unstable placement and timeout.

**Ablations.** Compare nested demonstration budgets and action execution horizon in separate sweeps. Keep all other variables fixed within each sweep, and report limited sample sizes and variance. For public reporting, include representative success and failure clips, ACT and Diffusion Policy metrics, and the limits of simulation-only evaluation.
