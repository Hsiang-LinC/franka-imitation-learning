# Baseline: pins, entry points and handoffs

## Stack (route B, D1)

Validated 2026-11-16: full open-loop action replay of Lift ph succeeds on these pins
(evidence below). Installed sim env: `requirements/sim.txt`.

| Component | Pin | Why |
|---|---|---|
| Python | CLAIX `Python/3.11.5` (with `GCCcore/13.3.0`) | Wheels exist for all packages below |
| robosuite | v1.5.2 tag, `824ac14cefcfb7ec125fe5eb2e0bad7364466154` | Latest release; v1.5 datasets target it |
| MuJoCo | `mujoco==3.9.0` | robosuite caps `<3.10` on master: 3.10 changed `mj_fullM` and breaks its controllers. The v1.5.2 release lacks the cap, so pin explicitly. Fallback: 3.3.x if replay drifts |
| robomimic | master `d309eaecc18acf4152a830a895a6984b8ac71b05` (2026-08-09) | v0.5.0 + 15 fixes, incl. the current dataset HF repo; has `DiffusionPolicyUNet` |
| PyTorch | sim env `torch==2.15.0+cpu`; trainer env: same version, CUDA build (pending) | Checkpoints must load across envs |
| Lift data | HF `robomimic/robomimic_datasets` `v1.5/lift/ph/demo_v15.hdf5` (sha256 `68f2a8cf…f37`), `low_dim_v15.hdf5` (`2067777c…aeb540`) | Hugging Face LFS hashes, to verify after download |
| Rendering | `Mesa/24.1.3` module, `MUJOCO_GL=osmesa` (verified in a CPU job) | No system libOSMesa on CLAIX |

### Replay validation (Lift ph, `low_dim_v15.hdf5`)

`jobs/lift_replay.sh` (CPU `devel`, job 5813465, 3.5 min, MaxRSS 2.4 GB):
- `jobs/lift_replay_check.py`: **200/200** demos reach task success open-loop; first-success
  step matches the recording for 169, differs by ±1 step for 31. The dataset was recorded on
  robosuite 1.5.1; robomimic's version-mismatch warning is therefore harmless here.
- State drift is dominated by qvel spikes at contact (max qpos error ≈ 0.08, max qvel error
  ≈ 13 on the worst demo); judge replay by task success, not exact state equality.
- Upstream `playback_dataset.py` MP4 of the `20_percent_valid` mask (4 demos): all lifts
  visually confirmed. Use `--filter_key`, not `--n` (unseeded shuffle), and `--video_skip 1`.

### Known install issue: egl_probe (robomimic dependency)

`egl_probe` 1.0.2 declares `cmake_minimum_required(VERSION 2.8.12)`, which CMake ≥4 rejects,
and its `setup.py` calls the `cmake` executable, which is missing in pip's isolated build env.
Verified fix (login node, 2026-11-15): install `setuptools wheel cmake` into the venv, then
`CMAKE_POLICY_VERSION_MINIMUM=3.5 python -m pip install --no-build-isolation egl_probe`
before installing robomimic. On nodes without a GPU, `get_available_devices()` returns `[]`, as expected.

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
