#!/usr/bin/env bash
# BC-RNN low-dim training on CPU (upstream robomimic train.py, simulator-free trainer venv,
# no in-training rollouts; checkpoints are evaluated separately with jobs/eval_cpu.sh).
#
# Args: TASK [EPOCHS] [SAVE_EVERY]   TASK = lift | can | square; defaults: paper 2000 epochs,
# a checkpoint every 100 epochs. Submit from the repo root; the default partition (devel,
# 59 min) only fits short runs, so pass a regular partition and time for full runs:
#   mkdir -p "$HPCWORK/franka-il/runs/logs"
#   sbatch -p c23ms -t 05:00:00 --job-name=can-bcrnn \
#       --output="$HPCWORK/franka-il/runs/logs/%x-%j.out" jobs/bc_rnn_cpu.sh can
#   sbatch --job-name=can-bcrnn-smoke --output=... jobs/bc_rnn_cpu.sh can 2 1   # smoke test
#SBATCH --job-name=bcrnn-cpu
#SBATCH --partition=devel
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=00:59:00
set -euo pipefail

module load GCCcore/13.3.0 Python/3.11.5

# PyTorch would otherwise start one thread per core of the whole node (96), not per
# allocated core, and the threads would fight over the few cores Slurm gave us.
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-4}" MKL_NUM_THREADS="${SLURM_CPUS_PER_TASK:-4}"

TASK="${1:?usage: jobs/bc_rnn_cpu.sh TASK [EPOCHS] [SAVE_EVERY]}"
EPOCHS="${2:-2000}"
SAVE_EVERY="${3:-100}"
PY="$WORK/franka-il/venvs/train/bin/python"
TRAIN="$WORK/franka-il/src/robomimic/robomimic/scripts/train.py"
DATA="$HPCWORK/franka-il/data/robomimic_v15/$TASK/ph/low_dim_v15.hdf5"
RUN="$HPCWORK/franka-il/runs/${TASK}_bc_rnn/${SLURM_JOB_ID:-local}"
mkdir -p "$RUN"
echo "task $TASK | job ${SLURM_JOB_ID:-local} on $(hostname) | cpus $OMP_NUM_THREADS | epochs $EPOCHS, save every $SAVE_EVERY | repo $(git rev-parse --short HEAD) | run $RUN"

# Resolve the committed paper config (configs/<task>/bc_rnn_low_dim.json, unchanged upstream
# output) into this run's config. Everything not listed keeps the paper value.
# Measured on Lift (jobs 5824723/5824724): ~5.5 s per training epoch (100 steps of batch 100),
# no gain beyond ~2 cores; the cost per step does not depend on the task's episode length.
overrides=(
    train.output_dir="$RUN"
    experiment.name="${TASK}_bc_rnn_cpu${OMP_NUM_THREADS}"
    train.cuda=false                      # robomimic falls back to CPU anyway; set so the run records it
    experiment.rollout.enabled=false      # trainer venv has no robosuite/MuJoCo; evaluate checkpoints separately
    train.num_epochs="$EPOCHS"            # paper: 2000
    experiment.save.every_n_epochs="$SAVE_EVERY" # paper: 50; checkpoints for rollout selection
)
"$PY" jobs/make_run_config.py "configs/$TASK/bc_rnn_low_dim.json" "$RUN/config.json" "${overrides[@]}"

"$PY" "$TRAIN" --config "$RUN/config.json" --dataset "$DATA"

# Cost summary: robomimic logs Time_Epoch in minutes, alternating train (100 steps) and
# validation (10 steps) epochs; the larger values are the training epochs.
grep -h "Time_Epoch" "$RUN"/*/*/logs/log.txt | tail -n 5 || true
sha256sum "$RUN"/*/*/models/*.pth
