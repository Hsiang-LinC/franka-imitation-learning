#!/usr/bin/env bash
# Validate the simulator pins against a robomimic v1.5 ph dataset (CPU only).
# TASK = lift | can | square (first argument, default lift).
#   A. open-loop replay of every demo + task-success check  -> replay_check.json
#   B. upstream playback of 4 fixed demos rendered to MP4   -> replay_20pct_valid.mp4
#
# Submit from the repo root, with the log kept outside Git (#SBATCH lines cannot expand variables):
#   mkdir -p "$HPCWORK/franka-il/runs/logs"
#   sbatch --job-name=can-replay --output="$HPCWORK/franka-il/runs/logs/%x-%j.out" jobs/replay.sh can
#SBATCH --job-name=replay
#SBATCH --partition=devel
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=00:30:00
set -euo pipefail

module load GCCcore/13.3.0 Python/3.11.5 Mesa/24.1.3   # Mesa provides libOSMesa (no GPU here)
export MUJOCO_GL=osmesa PYOPENGL_PLATFORM=osmesa

TASK="${1:-lift}"
PY="$WORK/franka-il/venvs/sim/bin/python"
ROBOMIMIC="$WORK/franka-il/src/robomimic"
DATA="$HPCWORK/franka-il/data/robomimic_v15/$TASK/ph/low_dim_v15.hdf5"
OUT="$HPCWORK/franka-il/runs/${TASK}_replay/${SLURM_JOB_ID:-local}"
mkdir -p "$OUT"
echo "task $TASK | job ${SLURM_JOB_ID:-local} on $(hostname) | repo $(git rev-parse --short HEAD) | out $OUT"

# A. Full replay check. Keep going if some demos fail so the video still renders;
#    the job's exit code reports A's verdict at the end.
status=0
"$PY" jobs/replay_check.py --dataset "$DATA" --out "$OUT/replay_check.json" || status=$?

# B. Upstream MP4. --filter_key picks a fixed dataset mask (4 demos) instead of --n, which
#    samples demos with an unseeded shuffle. --video_skip 1 keeps real-time speed (writer is 20 fps).
"$PY" "$ROBOMIMIC/robomimic/scripts/playback_dataset.py" \
    --dataset "$DATA" \
    --use-actions \
    --filter_key 20_percent_valid \
    --render_image_names agentview \
    --video_skip 1 \
    --video_path "$OUT/replay_20pct_valid.mp4"

exit "$status"
