# Compute plan

| Workload | Preferred compute | Preflight |
|---|---|---|
| Gymnasium, NumPy FK/IK, schema tests, data preprocessing and analysis | Local Mac or university CPU nodes | Record Python and package versions, job limits and storage policy |
| PyTorch smoke tests and BC-RNN, ACT or optional policy training | University CPU for smoke tests, compatible university GPU nodes for full runs | Check the approved scheduler, GPU/backend, driver/CUDA/PyTorch compatibility, VRAM and checkpoint storage |
| Isaac Sim startup, headless rollouts, demonstration replay/generation and camera rendering | Supported RTX Linux host, using institutional hardware if available | Match the selected Isaac Sim and Isaac Lab releases, then verify driver, GPU/VRAM, asset access and headless camera output |
| Optional training fallback | Existing Colab allowance, up to the reported 50 CCUs/month when available | Verify current entitlement and runtime consumption. Save checkpoints to durable storage |

RT cores are required by the supported Isaac Sim configuration. Headless execution still needs a supported host. A non-RTX GPU may be suitable for training while being unsupported for Isaac Sim. See the [Isaac Sim requirements](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/requirements.html) for the chosen version.

Transfer a versioned dataset manifest and data from simulation to training. Return the checkpoint, configuration and normalization metadata to the simulator for rollouts. Check SHA-256 on transfer and keep artifacts in approved storage.

Use paid RTX cloud only for Isaac Sim or RTX rendering and only after explicit approval. Before provisioning or spending, record the exact workload, hardware, quoted price, maximum runtime and cost cap, storage charges, and shutdown/deletion plan in M3. Track actual GPU hours, CCUs or cost per run.
