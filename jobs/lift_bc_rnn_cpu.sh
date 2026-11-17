#!/usr/bin/env bash
# Lift warm-up 0.3: short BC-RNN low-dim training on CPU to measure cost per epoch.
# Upstream robomimic train.py, simulator-free trainer venv, no in-training rollouts.
#
# Submit from the repo root; choose the core count on the command line to compare speed:
#   mkdir -p "$HPCWORK/franka-il/runs/logs"
#   sbatch -c 4 --output="$HPCWORK/franka-il/runs/logs/%x-%j.out" jobs/lift_bc_rnn_cpu.sh
#   sbatch -c 8 --output="$HPCWORK/franka-il/runs/logs/%x-%j.out" jobs/lift_bc_rnn_cpu.sh
#SBATCH --job-name=lift-bcrnn-cpu
#SBATCH --partition=devel
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=00:59:00
set -euo pipefail

module load GCCcore/13.3.0 Python/3.11.5

# PyTorch would otherwise start one thread per core of the whole node (96), not per
# allocated core, and the threads would fight over the few cores Slurm gave us.
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-4}" MKL_NUM_THREADS="${SLURM_CPUS_PER_TASK:-4}"

PY="$WORK/franka-il/venvs/train/bin/python"
TRAIN="$WORK/franka-il/src/robomimic/robomimic/scripts/train.py"
DATA="$HPCWORK/franka-il/data/robomimic_v15/lift/ph/low_dim_v15.hdf5"
RUN="$HPCWORK/franka-il/runs/lift_bc_rnn/${SLURM_JOB_ID:-local}"
mkdir -p "$RUN"
echo "job ${SLURM_JOB_ID:-local} on $(hostname) | cpus $OMP_NUM_THREADS | repo $(git rev-parse --short HEAD) | run $RUN"

# Resolve the committed paper config (configs/lift/bc_rnn_low_dim.json, unchanged upstream
# output) into this run's config. Everything not listed keeps the paper value.
# Measured 2026-11-17 (jobs 5824723/5824724): ~5.5 s per training epoch, no gain beyond
# ~2 cores; 200 epochs take ~20 min (docs/BASELINE.md).
overrides=(
    train.output_dir="$RUN"
    experiment.name="lift_bc_rnn_cpu${OMP_NUM_THREADS}"
    train.cuda=false                 # robomimic falls back to CPU anyway; set so the run records it
    experiment.rollout.enabled=false # trainer venv has no robosuite/MuJoCo; evaluate checkpoints in 0.4
    train.num_epochs=200             # paper: 2000; short run to measure cost per epoch
    experiment.save.every_n_epochs=20 # paper: 50; gives 10 checkpoints for rollout selection
)
"$PY" jobs/make_run_config.py configs/lift/bc_rnn_low_dim.json "$RUN/config.json" "${overrides[@]}"

"$PY" "$TRAIN" --config "$RUN/config.json" --dataset "$DATA"

# Cost summary: robomimic logs Time_Epoch in minutes, alternating train (100 steps) and
# validation (10 steps) epochs; the larger values are the training epochs.
grep -h "Time_Epoch" "$RUN"/*/*/logs/log.txt | tail -n 5 || true
