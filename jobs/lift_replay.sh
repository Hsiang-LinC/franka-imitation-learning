#!/usr/bin/env bash
# Lift warm-up 0.1d: validate the simulator pins against the Lift ph dataset (CPU only).
#   A. open-loop replay of every demo + task-success check  -> replay_check.json
#   B. upstream playback of 4 fixed demos rendered to MP4   -> replay_20pct_valid.mp4
#
# Submit from the repo root, with the log kept outside Git (#SBATCH lines cannot expand variables):
#   mkdir -p "$HPCWORK/franka-il/runs/logs"
#   sbatch --output="$HPCWORK/franka-il/runs/logs/%x-%j.out" jobs/lift_replay.sh
#SBATCH --job-name=lift-replay
#SBATCH --partition=devel
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=00:30:00
set -euo pipefail

module load GCCcore/13.3.0 Python/3.11.5 Mesa/24.1.3   # Mesa provides libOSMesa (no GPU here)
export MUJOCO_GL=osmesa PYOPENGL_PLATFORM=osmesa

PY="$WORK/franka-il/venvs/sim/bin/python"
ROBOMIMIC="$WORK/franka-il/src/robomimic"
DATA="$HPCWORK/franka-il/data/robomimic_v15/lift/ph/low_dim_v15.hdf5"
OUT="$HPCWORK/franka-il/runs/lift_replay/${SLURM_JOB_ID:-local}"
mkdir -p "$OUT"
echo "job ${SLURM_JOB_ID:-local} on $(hostname) | repo $(git rev-parse --short HEAD) | out $OUT"

# A. Full replay check. Keep going if some demos fail so the video still renders;
#    the job's exit code reports A's verdict at the end.
status=0
"$PY" jobs/lift_replay_check.py --dataset "$DATA" --out "$OUT/replay_check.json" || status=$?

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
