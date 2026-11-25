# Containers

`lerobot-square/` is the single environment for phases 2–3 (DECISIONS D9). It is used for
dataset conversion and evaluation on CLAIX (Apptainer, CPU, OSMesa) and for training on
Vertex AI (Docker, GPU). The image holds only the environment. Project code is
bind-mounted on CLAIX.

| Component | Pin | Source |
|---|---|---|
| Base | `python:3.12-slim-bookworm` by digest | Dockerfile |
| LeRobot | 0.7.0 (tag commit `410c095`), extras `training,dataset,smolvla,diffusion,peft` | `requirements/lerobot.in` |
| Simulator | robosuite 1.5.1 + MuJoCo 3.2.7 (Square pin, D6) | same |
| torch | 2.11.0+cu128; the CUDA runtime comes from pip wheels, so the host needs only a driver | `requirements/lerobot.txt` (hashed lock) |
| robomimic | `d309eae`, installed `--no-deps` for its env wrapper only | Dockerfile (hash-pinned archive) |

The lock is generated with `uv pip compile`, using the command in the header of
`requirements/lerobot.txt`. It excludes `opencv-python`, because robosuite declares it and it
would shadow LeRobot's `opencv-python-headless`. Change `lerobot.in`, regenerate the lock, and
never edit the lock by hand.

## Build

CI (`.github/workflows/container.yml`) builds every pull request that touches the image and
runs `smoke_check.py` inside it. Pushes to `main` also publish
`ghcr.io/hsiang-linc/franka-il-lerobot-square`, and the job summary records the digest.
Always refer to the image by that digest, not by a tag.

Local build, from the repository root:

```bash
docker build --platform linux/amd64 -f containers/lerobot-square/Dockerfile -t lerobot-square:dev .
```

## CLAIX (Apptainer)

Pull on a login or copy node, because batch-node internet access is unverified (#2). Store the
SIF on `$HPCWORK`:

```bash
apptainer pull "$HPCWORK/franka-il/images/lerobot-square_<digest12>.sif" \
    docker://ghcr.io/hsiang-linc/franka-il-lerobot-square@sha256:<digest>
```

Run with the repository and data bind-mounted. `--cleanenv` keeps CLAIX modules and venvs out
of the container:

```bash
apptainer exec --cleanenv --bind "$PWD:/workspace,$HPCWORK/franka-il:/data" \
    "$HPCWORK/franka-il/images/lerobot-square_<digest12>.sif" \
    python jobs/replay_check.py --dataset /data/data/robomimic_v15/square/ph/low_dim_v15.hdf5 \
        --out /data/runs/square_replay_container/replay_check.json
```

**Acceptance (#28):** this replay reproduces 181/200, and the failing demos are the same ones as
in `sim-square` (docs/BASELINE.md). If it does not, the image differs from the validated
simulator and must not be used for evaluation.
