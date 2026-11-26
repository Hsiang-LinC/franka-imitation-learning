#!/usr/bin/env bash
# Paired closed-loop evaluation of saved BC-RNN checkpoints (CPU only).
# Every checkpoint faces the same seeded initial states (jobs/eval_checkpoints.py).
#
# Args: TASK TRAIN_JOB ["epoch epoch ..."] [SEED] ["episode ..."]
#   TRAIN_JOB = the training job's ID (its run folder holds the checkpoints);
#   epochs default to all saved ones, seed to 0, videos to the first 3 episodes.
# Submit from the repo root:
#   mkdir -p "$HPCWORK/franka-il/runs/logs"
#   sbatch --job-name=lift-eval --output="$HPCWORK/franka-il/runs/logs/%x-%j.out" jobs/eval_cpu.sh lift 5824723 "20 40"
#   sbatch ... jobs/eval_cpu.sh lift 5824723 200 1    # report the selected epoch on a fresh seed
#   sbatch ... jobs/eval_cpu.sh lift 5824723 180 0 5  # re-run and film only episode 5 (failure review)
#SBATCH --job-name=eval
#SBATCH --partition=devel
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=00:59:00
set -euo pipefail

usage='usage: sbatch jobs/eval_cpu.sh TASK TRAIN_JOB ["epoch epoch ..."] [seed] ["episode ..."]'
TASK="${1:?$usage}"
TRAIN_JOB="${2:?$usage}"
EPOCHS="${3:-}"
SEED="${4:-0}"
VIDEO_LIST="${5:-}"   # episode indices to film; default: the first 3 episodes

module load GCCcore/13.3.0 Python/3.11.5 Mesa/24.1.3   # Mesa provides libOSMesa (no GPU here)
export MUJOCO_GL=osmesa PYOPENGL_PLATFORM=osmesa
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-2}" MKL_NUM_THREADS="${SLURM_CPUS_PER_TASK:-2}"

# Per-dataset pins (DECISIONS D6): Square replays best on robosuite 1.5.1 + MuJoCo 3.2.7.
case "$TASK" in square) SIM=sim-square ;; *) SIM=sim ;; esac
PY="$WORK/franka-il/venvs/$SIM/bin/python"
MODEL_DIR=("$HPCWORK"/franka-il/runs/"${TASK}"_bc_rnn/"$TRAIN_JOB"/*/*/models)
if [[ -n "$EPOCHS" ]]; then
    MODELS=()
    for e in $EPOCHS; do MODELS+=("${MODEL_DIR[0]}/model_epoch_${e}.pth"); done
else
    MODELS=("${MODEL_DIR[0]}"/model_epoch_*.pth)
fi
OUT="$HPCWORK/franka-il/runs/${TASK}_eval/${SLURM_JOB_ID:-local}"
mkdir -p "$OUT"
echo "task $TASK | env $SIM | job ${SLURM_JOB_ID:-local} on $(hostname) | repo $(git rev-parse --short HEAD) | train job $TRAIN_JOB | seed $SEED | videos ${VIDEO_LIST:-first 3} | ${#MODELS[@]} checkpoints | out $OUT"

# Evaluation settings (Lift 0.4 design):
#   50 rollouts (paper): 45/50 still leaves a 95% Wilson interval of 79-96%, so differences
#     of a few episodes between checkpoints are noise.
#   horizon 400 (paper, 20 s) for every checkpoint; steps-to-success is recorded separately.
#   seed 0 = selection set; report the selected checkpoint later on a fresh seed.
#   3 videos per checkpoint: OSMesa rendering is slow, a few episodes show the behaviour.
# Budget (devel stops at 59 min): on Lift one checkpoint took 1.5 min (50/50 successes) to
#   5 min (1/50), video included (jobs 5844550-5844612). Longer tasks need fewer checkpoints
#   per job, or a regular partition (-p c23ms -t ...).
eval_args=(
    --n_rollouts 50
    --horizon 400
    --seed "$SEED"
    --video_episodes 3
)
# shellcheck disable=SC2206  # word-split the episode list on purpose
[[ -n "$VIDEO_LIST" ]] && eval_args+=(--video_list $VIDEO_LIST)
"$PY" jobs/eval_checkpoints.py \
    --checkpoints "${MODELS[@]}" \
    --out "$OUT/eval.json" \
    --video_dir "$OUT/videos" \
    "${eval_args[@]}"
