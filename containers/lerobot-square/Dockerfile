# LeRobot + Square simulator image (DECISIONS D9).
# One image for dataset conversion and evaluation on CLAIX (Apptainer, CPU, OSMesa) and for
# training on Vertex AI (Docker, NVIDIA GPU). It holds the environment only: project code is
# bind-mounted (CLAIX) and training uses LeRobot's own entry points.
# Build from the repository root:
#   docker build -f containers/lerobot-square/Dockerfile -t lerobot-square .

# python:3.12-slim-bookworm, pinned by index digest (multi-arch; built for linux/amd64).
FROM python:3.12-slim-bookworm@sha256:44cf1793efa7c7a476bb0f2cff81443f4a072c90c1cb127e2924933daa3e8c64

# Headless MuJoCo rendering: OSMesa (CPU, CLAIX) and EGL (GPU). ffmpeg for video decoding/encoding.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libosmesa6 libegl1 libgles2 libgl1 libglib2.0-0 ffmpeg \
    && rm -rf /var/lib/apt/lists/*

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONUNBUFFERED=1 \
    MUJOCO_GL=osmesa \
    PYOPENGL_PLATFORM=osmesa

# Hashed lock (requirements/lerobot.txt). torch +cu128 wheels come from the PyTorch index; the CUDA 12.8
# runtime ships as pip packages, so the host only needs an NVIDIA driver (none on CPU nodes).
# --no-deps: the lock is complete except opencv-python, which robosuite declares but which would
# overwrite cv2 from LeRobot's opencv-python-headless (both provide the same module).
# Indexes are given here, not in the lock: an --index-url line inside a requirements file makes pip
# drop the command-line extra index, and torch +cu128 is then not found.
# evdev (via robosuite -> pynput) has no wheel and compiles against kernel input headers; the
# compiler is removed again in the same layer.
COPY requirements/lerobot.txt /tmp/lerobot.txt
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libc6-dev linux-libc-dev \
    && python -m pip install --no-deps --require-hashes \
        --index-url https://pypi.org/simple \
        --extra-index-url https://download.pytorch.org/whl/cu128 \
        -r /tmp/lerobot.txt \
    && apt-get purge -y --auto-remove gcc libc6-dev linux-libc-dev \
    && rm -rf /var/lib/apt/lists/* /tmp/lerobot.txt

# robomimic at the project pin (d309eae), for its robosuite env wrapper (reset to recorded states,
# observation processing) used by the replay check and evaluation. --no-deps: its declared pins
# (diffusers 0.11.1, transformers 4.41.2, huggingface_hub 0.23.4) conflict with LeRobot, and the
# env/obs modules need only torch, numpy, tqdm, termcolor and robosuite. The archive is hash-pinned.
RUN python -m pip install --no-deps \
        "robomimic @ https://github.com/ARISE-Initiative/robomimic/archive/d309eaecc18acf4152a830a895a6984b8ac71b05.tar.gz#sha256=840d2ce9a4761be3a757500ed26ae6b598639374447bb4499ba6f154ac0a42f2"

# Fail the build if the stack cannot import or render. GPU rendering (EGL) is checked on GPU hosts only.
COPY containers/lerobot-square/smoke_check.py /opt/smoke_check.py
RUN python /opt/smoke_check.py

WORKDIR /workspace
