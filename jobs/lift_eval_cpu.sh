#!/usr/bin/env bash
# Lift warm-up 0.4: paired closed-loop evaluation of the saved BC-RNN checkpoints (CPU only).
# Every checkpoint faces the same seeded initial states (jobs/eval_checkpoints.py).
#
# Submit from the repo root with the training job's ID (its run folder holds the checkpoints)
# and optionally the epochs to evaluate (default: all saved epochs):
#   mkdir -p "$HPCWORK/franka-il/runs/logs"
#   sbatch --output="$HPCWORK/franka-il/runs/logs/%x-%j.out" jobs/lift_eval_cpu.sh 5824723 "20 40"
#SBATCH --job-name=lift-eval
#SBATCH --partition=devel
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=00:59:00
set -euo pipefail

TRAIN_JOB="${1:?usage: sbatch jobs/lift_eval_cpu.sh <training job ID> [\"epoch epoch ...\"]}"
EPOCHS="${2:-}"

module load GCCcore/13.3.0 Python/3.11.5 Mesa/24.1.3   # Mesa provides libOSMesa (no GPU here)
export MUJOCO_GL=osmesa PYOPENGL_PLATFORM=osmesa
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-2}" MKL_NUM_THREADS="${SLURM_CPUS_PER_TASK:-2}"

PY="$WORK/franka-il/venvs/sim/bin/python"
MODEL_DIR=("$HPCWORK"/franka-il/runs/lift_bc_rnn/"$TRAIN_JOB"/*/*/models)
if [[ -n "$EPOCHS" ]]; then
    MODELS=()
    for e in $EPOCHS; do MODELS+=("${MODEL_DIR[0]}/model_epoch_${e}.pth"); done
else
    MODELS=("${MODEL_DIR[0]}"/model_epoch_*.pth)
fi
OUT="$HPCWORK/franka-il/runs/lift_eval/${SLURM_JOB_ID:-local}"
mkdir -p "$OUT"
echo "job ${SLURM_JOB_ID:-local} on $(hostname) | repo $(git rev-parse --short HEAD) | train job $TRAIN_JOB | ${#MODELS[@]} checkpoints | out $OUT"

# Evaluation settings (0.4 design):
#   50 rollouts (paper): 45/50 still leaves a 95% Wilson interval of 79-96%, so differences
#     of a few episodes between checkpoints are noise.
#   horizon 400 (paper, 20 s) for every checkpoint; steps-to-success is recorded separately.
#   seed 0 = selection set; report the selected checkpoint later on a fresh seed.
#   3 videos per checkpoint: OSMesa rendering is slow, a few episodes show the behaviour.
# Budget (devel stops at 59 min; ~18 env steps/s on a login node): worst case (all fail)
#   50 x 400 / 18 ≈ 19 min per checkpoint, all succeed ≈ 2 min. Pass at most 2 epochs per job
#   unless the epochs are known to succeed.
eval_args=(
    --n_rollouts 50
    --horizon 400
    --seed 0
    --video_episodes 3
)
"$PY" jobs/eval_checkpoints.py \
    --checkpoints "${MODELS[@]}" \
    --out "$OUT/eval.json" \
    --video_dir "$OUT/videos" \
    "${eval_args[@]}"
