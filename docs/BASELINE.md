# Baseline: upstream code and execution flow

## Scope

Fixed task: Franka three-cube stacking, public MimicGen `stack_three_d0.hdf5`.
First method: robomimic BC-RNN. Use published demonstrations; generating new MimicGen
data is not required for phase 1. The upstream pipeline exists, but has not been
validated in this project. All robot installation/training/rollout checks are pending.

## Sources and entry points

Paths below are relative to each external checkout. Links describe upstream branches;
commands and configuration fields must be checked against pinned revisions before use.

| Work | Existing code/resource | Project adaptation |
|---|---|---|
| Install compatible stack | [MimicGen installation](https://github.com/NVlabs/mimicgen/blob/main/docs/introduction/installation.md) | Pin full dependency set and verify CLAIX CPU rendering/H100 training |
| Download data | [MimicGen core datasets](https://huggingface.co/datasets/amandlek/mimicgen_datasets/tree/main/core) | Only selected file; record source revision, license and checksum |
| Replay actions | robomimic [playback_dataset.py](https://github.com/ARISE-Initiative/robomimic/blob/master/robomimic/scripts/playback_dataset.py) | Saved initial state, action replay, separate task-success check, MP4 |
| Build observations if absent | robomimic [dataset_states_to_obs.py](https://github.com/ARISE-Initiative/robomimic/blob/master/robomimic/scripts/dataset_states_to_obs.py) | Inspect stored keys first; regenerate only what is needed |
| Generate BC-RNN config | MimicGen [generate_core_training_configs.py](https://github.com/NVlabs/mimicgen/blob/main/mimicgen/scripts/generate_core_training_configs.py) | Select stack_three D0, map downloaded path, set output paths and chosen modality |
| Train | robomimic [train.py](https://github.com/ARISE-Initiative/robomimic/blob/master/robomimic/scripts/train.py) | Config and Slurm job; disable integrated rollout for offline-only training |
| Deploy/evaluate | robomimic [run_trained_agent.py](https://github.com/ARISE-Initiative/robomimic/blob/master/robomimic/scripts/run_trained_agent.py) | Explicit checkpoint, reset/seed protocol, rollout horizon, metrics and video |

The [official reproduction tutorial](https://github.com/NVlabs/mimicgen/blob/main/docs/tutorials/reproducing_experiments.md)
connects downloaded data to BC-RNN learning. The generic
[train_bc_rnn.py example](https://github.com/ARISE-Initiative/robomimic/blob/master/examples/train_bc_rnn.py)
is supplementary reading, not a second independent implementation to maintain.

## Persistent handoff

```text
source dataset + simulator pins
  -> validated action replay + data inspection
  -> observation dataset + versioned episode split
  -> BC-RNN config + offline H100 training
  -> run ID + checkpoint + checksum
  -> CPU closed-loop rollout
  -> per-episode metrics + videos -> notebook analysis
```

Each step reads saved inputs; no step depends on another notebook's live variables.
Keep full data, manifests with private paths, logs, checkpoints and videos in approved
shared storage outside Git. Commit sanitized settings, source revisions and summaries.
Never put absolute university paths or secrets into a public notebook/config.

## Ownership and environment boundaries

- External upstream checkouts retain their original code and pinned revision.
- `configs/` owns our resolved experimental choices; `jobs/` invokes upstream entry points.
- `notebooks/` explains and inspects the workflow; it does not duplicate training loops.
- Offline training must not import/initialize a simulator accidentally. Check the pinned
  trainer with rollout disabled; any remaining simulator-only import is a preflight blocker.
- Record Python, PyTorch/CUDA and package versions independently per environment.
- Introduce local reusable modules only when conversion or policy integration requires them.

## Baseline acceptance

A saved-state video or decreasing training loss alone is insufficient. Require own
trained weights, successful checkpoint reload, closed-loop trials with successes/trials,
representative failures, command/config records and artifact checksums. Do not promise
a success-rate threshold before measuring the first complete run.

A state-based first run may use privileged object state. Label it explicitly; later
RGB + proprioception comparisons must not attribute input advantages to policy methods.
