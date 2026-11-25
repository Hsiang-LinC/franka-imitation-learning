"""Build-time smoke check for the lerobot-square image.

Fails loudly if a pinned package is missing or at the wrong version, if the policy classes
used in phases 2-3 cannot be imported, or if MuJoCo cannot render offscreen with the
configured backend. It does not replace the Square replay acceptance check (181/200), which
needs the dataset and runs on CLAIX.
"""

import importlib.metadata as md
import os

EXPECTED = {
    "lerobot": "0.7.0",
    "robosuite": "1.5.1",
    "mujoco": "3.2.7",
}

for name, version in EXPECTED.items():
    found = md.version(name)
    if found != version:
        raise SystemExit(f"{name}: expected {version}, found {found}")

# cv2 must come only from opencv-python-headless (see Dockerfile).
try:
    md.distribution("opencv-python")
except md.PackageNotFoundError:
    pass
else:
    raise SystemExit("opencv-python is installed and would shadow opencv-python-headless")
import cv2  # noqa: E402,F401

# Policy classes used in phases 2-3 (DECISIONS D8, D9).
from lerobot.policies.act.modeling_act import ACTPolicy  # noqa: E402,F401
from lerobot.policies.diffusion.modeling_diffusion import DiffusionPolicy  # noqa: E402,F401
from lerobot.policies.smolvla.modeling_smolvla import SmolVLAPolicy  # noqa: E402,F401

# Offscreen render of an empty scene with the configured backend.
import mujoco  # noqa: E402

model = mujoco.MjModel.from_xml_string(
    "<mujoco><worldbody><light pos='0 0 1'/><geom type='box' size='.1 .1 .1'/></worldbody></mujoco>"
)
data = mujoco.MjData(model)
mujoco.mj_forward(model, data)
with mujoco.Renderer(model, height=84, width=84) as renderer:
    renderer.update_scene(data)
    pixels = renderer.render()
if pixels.shape != (84, 84, 3) or pixels.max() == 0:
    raise SystemExit(f"render failed with MUJOCO_GL={os.environ.get('MUJOCO_GL')}: {pixels.shape}")

# robosuite imports with the pinned MuJoCo (its controllers changed after MuJoCo 3.9), and
# robomimic's env wrapper imports without its declared (conflicting) dependencies.
import robosuite  # noqa: E402,F401
import robomimic.utils.env_utils  # noqa: E402,F401
import robomimic.utils.obs_utils  # noqa: E402,F401

print("smoke check passed:", {k: md.version(k) for k in EXPECTED}, "MUJOCO_GL=" + os.environ["MUJOCO_GL"])
