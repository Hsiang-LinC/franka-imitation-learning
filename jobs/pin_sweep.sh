#!/usr/bin/env bash
# Pin sweep: rerun the open-loop replay check under other robosuite / MuJoCo versions (CPU only).
# Question: are replay failures (Square ph 162/200 on robosuite 1.5.2 + MuJoCo 3.9.0) caused by
# the version mismatch with the recording (robosuite 1.5.1, MuJoCo unknown), or by action replay itself?
#
# The sim venv stays unchanged. Other versions are layered on top through PYTHONPATH, which
# Python searches before the venv's editable robosuite finder and its installed mujoco:
#   robosuite: a git worktree of the pinned tag (outside this repo), e.g. src/robosuite-v1.5.1
#   mujoco:    pip install --no-deps --target "$WORK/franka-il/overlays/mujoco-<ver>" mujoco==<ver>
# "venv" as an argument keeps the venv's own package. replay_check.json records the versions loaded.
#
# Args: TASK ROBOSUITE MUJOCO, e.g.  square v1.5.1 3.2.7   |   square venv 3.3.0
#   mkdir -p "$HPCWORK/franka-il/runs/logs"
#   sbatch --job-name=sq-rs151-mj327 --output="$HPCWORK/franka-il/runs/logs/%x-%j.out" \
#       jobs/pin_sweep.sh square v1.5.1 3.2.7
#SBATCH --job-name=pin-sweep
#SBATCH --partition=devel
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=00:30:00
set -euo pipefail

module load GCCcore/13.3.0 Python/3.11.5 Mesa/24.1.3
export MUJOCO_GL=osmesa PYOPENGL_PLATFORM=osmesa

TASK="$1" RS="$2" MJ="$3"
PY="$WORK/franka-il/venvs/sim/bin/python"
DATA="$HPCWORK/franka-il/data/robomimic_v15/$TASK/ph/low_dim_v15.hdf5"
OUT="$HPCWORK/franka-il/runs/${TASK}_pin_sweep/rs-${RS}_mj-${MJ}/${SLURM_JOB_ID:-local}"

overlay=()
[[ "$RS" != venv ]] && overlay+=("$WORK/franka-il/src/robosuite-$RS")
[[ "$MJ" != venv ]] && overlay+=("$WORK/franka-il/overlays/mujoco-$MJ")
for d in "${overlay[@]}"; do [[ -d "$d" ]] || { echo "missing overlay $d" >&2; exit 2; }; done
export PYTHONPATH="$(IFS=:; echo "${overlay[*]}")"

mkdir -p "$OUT"
echo "task $TASK | robosuite $RS | mujoco $MJ | job ${SLURM_JOB_ID:-local} on $(hostname) | out $OUT"
echo "repo $(git rev-parse --short HEAD), dirty files: $(git status --porcelain | wc -l)"
sha256sum jobs/replay_check.py jobs/pin_sweep.sh
"$PY" -c "import mujoco, robosuite; print('loaded', robosuite.__version__, robosuite.__file__, mujoco.__version__, mujoco.__file__)"

"$PY" jobs/replay_check.py --dataset "$DATA" --out "$OUT/replay_check.json" "${@:4}"
