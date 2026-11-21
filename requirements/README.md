# Python environments

`foundations.txt` pins the tested optional CartPole exercise environment (Python 3.11.5).
It is not a robot simulation or training environment.

`sim.txt` pins the simulator env for Lift and Can; `sim-square.txt` pins the Square
simulator env (robosuite 1.5.1 + MuJoCo 3.2.7, docs/DECISIONS.md D6). Editable
robosuite/robomimic installs are listed in each header; see docs/BASELINE.md. `train.txt` pins the simulator-free offline
trainer env (validated on CPU). Its H100 PyTorch/CUDA compatibility is still unverified. Notebook kernels must identify
their environment; installing Jupyter alone does not install the robot stack.

CLAIX setup uses standard Python `venv` and `python -m pip`; Anaconda/Conda
is not permitted. No uv dependency is needed. For source packages, clone upstream
outside the repository, checkout the selected commit, then install into the active
venv with `python -m pip install -e .`. Cloning alone does not install dependencies.
