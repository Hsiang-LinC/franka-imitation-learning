# Baseline: pins, entry points and handoffs

## Candidate pins (not yet installed or validated)

Chosen to match MimicGen's tested stack, so Lift and stack_three share one sim env.

| Component | Pin | Source of the choice |
|---|---|---|
| Python | 3.11.5 (CLAIX module `Python/3.11.5`) | MuJoCo 2.3.2 ships cp311 wheels |
| robosuite | `b9d8d3de5e3dfd1724f4a0e6555246c460407daa` | MimicGen installation docs (tested commit); v1.5+ unsupported |
| MuJoCo | `mujoco==2.3.2` | MimicGen docs: other versions change rendering/dynamics |
| robomimic | `d0b37cf214bd24fb590d182edb6384333f67b661` (v0.3.0 + 26 commits) | MimicGen installation docs |
| MimicGen | pending (needed from stack_three onward) | — |
| Lift data | robomimic `lift/ph/low_dim_v141.hdf5`, `demo_v141.hdf5` (Stanford host, reachable 2026-11-15) | robomimic v0.3.0 dataset registry |
| stack_three data | MimicGen `core/stack_three_d0.hdf5` (Hugging Face) | MimicGen datasets |

Newer robomimic releases (v0.4+) point to robosuite-v1.5 datasets; do not mix them with
these pins. Diffusion Policy version conflict: see [decisions](DECISIONS.md).

## Entry points

Paths are relative to each external checkout; verify flags against the pinned revision.

| Step | Upstream tool |
|---|---|
| Replay actions to MP4 | robomimic `robomimic/scripts/playback_dataset.py` |
| Inspect dataset | robomimic `robomimic/scripts/get_dataset_info.py` |
| Build observations if absent | robomimic `robomimic/scripts/dataset_states_to_obs.py` |
| BC-RNN config (stack_three) | MimicGen `mimicgen/scripts/generate_core_training_configs.py` |
| Train | robomimic `robomimic/scripts/train.py` (integrated rollouts off) |
| Evaluate checkpoint | robomimic `robomimic/scripts/run_trained_agent.py` |

Reading: MimicGen
[reproducing experiments](https://github.com/NVlabs/mimicgen/blob/main/docs/tutorials/reproducing_experiments.md),
robomimic `examples/train_bc_rnn.py`.

## Handoff

```text
dataset + sim pins -> replay MP4 + inspection -> split -> config
  -> H100 training -> run ID + checkpoint + checksum
  -> CPU rollout -> per-episode metrics + videos -> analysis notebook
```

Each step reads persisted inputs. Data, checkpoints, logs and videos live in shared
storage outside Git; commit sanitized configs and summaries without absolute private paths.

## Acceptance

Own trained weights, successful reload, closed-loop successes/trials, representative
failures, recorded commands/configs/checksums. Loss curves or replay videos alone are
insufficient. A low-dim run uses privileged object state; label it as such.
