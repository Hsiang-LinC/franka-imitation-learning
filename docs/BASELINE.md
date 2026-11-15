# Baseline: pins, entry points and handoffs

## Stack (route B, D1)

Use the newest versions that pass action replay on the robomimic v1.5 datasets. Exact
commits are recorded here once validated.

| Component | Candidate | Constraint |
|---|---|---|
| Python | CLAIX `Python/3.11.5` (with `GCCcore/13.3.0`) | Must have wheels for MuJoCo/torch |
| robosuite | v1.5.2 (latest release, 2025-12) | Requires `mujoco>=3.3.0` |
| MuJoCo | newest 3.x accepted by robosuite | 4.x untested by robosuite; validate by replay |
| robomimic | v0.5.0 or newer master | Provides BC-RNN and `DiffusionPolicyUNet` |
| Datasets | robomimic v1.5 `lift`, `can`, `square` (ph, mh) | Generated for robosuite v1.5 |
| Rendering | `Mesa/24.1.3` module (OSMesa) or EGL | No system libOSMesa on CLAIX |

## Entry points (robomimic; verify flags at the pinned revision)

| Step | Tool |
|---|---|
| Download datasets | `robomimic/scripts/download_datasets.py` |
| Inspect dataset | `robomimic/scripts/get_dataset_info.py` |
| Replay actions to MP4 | `robomimic/scripts/playback_dataset.py` |
| Build observations if absent | `robomimic/scripts/dataset_states_to_obs.py` |
| Train BC-RNN / Diffusion Policy | `robomimic/scripts/train.py` with configs from `robomimic/exps/templates/` |
| Evaluate checkpoint | `robomimic/scripts/run_trained_agent.py` |

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
