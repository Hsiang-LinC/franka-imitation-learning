# Baseline: pins, entry points and handoffs

## Stack (route B, D1)

Newest versions that should work together, checked 2026-11-15. "Selected" means not
yet installed; a pin becomes "validated" only after action replay succeeds.

| Component | Selected pin | Why |
|---|---|---|
| Python | CLAIX `Python/3.11.5` (with `GCCcore/13.3.0`) | Wheels exist for all packages below |
| robosuite | v1.5.2 tag, `824ac14cefcfb7ec125fe5eb2e0bad7364466154` | Latest release; v1.5 datasets target it |
| MuJoCo | `mujoco==3.9.0` | robosuite caps `<3.10` on master: 3.10 changed `mj_fullM` and breaks its controllers. The v1.5.2 release lacks the cap, so pin explicitly. Fallback: 3.3.x if replay drifts |
| robomimic | master `d309eaecc18acf4152a830a895a6984b8ac71b05` (2026-08-09) | v0.5.0 + 15 fixes, incl. the current dataset HF repo; has `DiffusionPolicyUNet` |
| PyTorch | newest CPU build in the sim env; same version as CUDA build in the trainer env | Checkpoints must load across envs |
| Lift data | HF `robomimic/robomimic_datasets` `v1.5/lift/ph/demo_v15.hdf5` (sha256 `68f2a8cf…f37`), `low_dim_v15.hdf5` (`2067777c…aeb540`) | Hugging Face LFS hashes, to verify after download |
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
