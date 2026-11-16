# Python environments

`foundations.txt` pins the tested optional CartPole exercise environment (Python 3.11.5).
It is not a robot simulation or training environment.

`sim.txt` pins the validated simulator env (robosuite/robomimic editable installs are
listed in its header; see docs/BASELINE.md). The offline trainer env is pending.
Record PyTorch/CUDA compatibility for H100 separately. Notebook kernels must identify
their environment; installing Jupyter alone does not install the robot stack.

CLAIX setup uses standard Python `venv` and `python -m pip`; Anaconda/Conda
is not permitted. No uv dependency is needed. For source packages, clone upstream
outside the repository, checkout the selected commit, then install into the active
venv with `python -m pip install -e .`. Cloning alone does not install dependencies.
