# Python environments

`foundations.txt` pins the tested optional CartPole exercise environment (Python 3.11.5).
It is not a robot simulation or training environment.

Simulator and offline trainer environments are pending. Select compatible upstream
commits and record Python/package versions before creating their dependency files.
Record PyTorch/CUDA compatibility for H100 separately. Notebook kernels must identify
their environment; installing Jupyter alone does not install the robot stack.

CLAIX setup uses standard Python `venv` and `python -m pip`; Anaconda/Conda
is not permitted. No uv dependency is needed. For source packages, clone upstream
outside the repository, checkout the selected commit, then install into the active
venv with `python -m pip install -e .`. Cloning alone does not install dependencies.
