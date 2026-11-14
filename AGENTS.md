# Project guidance

## Goal and teaching workflow

Build an end-to-end imitation-learning project on fixed simulated Franka three-cube
stacking. Study how policy methods, demonstration budgets and action execution settings
affect closed-loop task performance. The robot stays fixed; the learned policy and
its execution settings are the experimental variables.

Follow three phases: (1) upstream BC-RNN baseline, (2) matched ACT and Diffusion Policy
comparison, (3) controlled improvements and portfolio. BC-RNN is required for phase 1.
Gymnasium and FK/IK exercises are optional supporting lessons, not entry gates.

The user is the learner and main implementer. Explain purpose, inputs, outputs and
success checks before each hands-on step. Discuss workflow and scope before creating
new abstractions. Do not jump from planning to installing or training without a user
request to proceed. Carry out explicitly requested repository maintenance normally.

## Resume a session

Read docs/ROADMAP.md, docs/PROJECT_CONTEXT.md and docs/BASELINE.md first. Check live
GitHub Issues, native blockers, acceptance evidence and the linked Project. Retain
legacy M0–M9 issue identities; the three-phase roadmap defines their learning order.
If remote titles/dependencies conflict with the approved plan, report the discrepancy;
do not silently select the old exercise-first path or claim remote tracking is synced.
Name the current phase, legacy milestone/issue and concrete success check. At session
end, record verified evidence and remaining blockers in the relevant issue. Never
close an issue merely because a plan or scaffold exists.

## Repository and upstream boundaries

Use upstream MimicGen configuration generation and robomimic training/rollout code for
the baseline. Pin external repositories by commit; keep their checkouts outside this
repository. Do not copy upstream implementations or introduce local train/evaluate
wrappers without a demonstrated need. Verify entry points against the chosen revision.

Notebooks are learning narratives, small inspections and result analysis. One notebook
has one purpose and explicit prerequisites/outputs. Do not run long training implicitly
with Run All or depend on variables from another notebook. Use persisted manifests,
configs, run IDs and checkpoint paths between chapters. Jobs run upstream entry points
with explicit Python environments. Keep notebook outputs sanitized and small.

Keep configs/ for project experiment settings, jobs/ for Slurm scripts and requirements/
for tested dependencies. Add reusable src/ modules only when integration requires them.
See notebooks/README.md and docs/BASELINE.md for the planned structure and handoffs.

## Compute, compatibility and evidence

Keep simulator and offline training environments separate, including BC-RNN; disable
in-training simulator rollouts when using a simulator-free trainer and evaluate saved
checkpoints separately. Pin robosuite, MuJoCo, MimicGen and robomimic against the dataset.
Verify action playback before training. Use CLAIX CPU jobs for simulation and H100 jobs
for training. GPU interactive display is an optional, separately verified workflow.
Obtain explicit approval before paid cloud GPU provisioning or spend.

Record commands, commits, versions, seeds, artifact checksums and actual outcomes.
Mark unrun checks pending. Keep datasets, credentials, university connection details,
personal logs and large artifacts out of Git. Keep full run artifacts in approved
shared storage outside the checkout. Verify rights before publishing data or models.
Use docs/EXPERIMENT_PROTOCOL.md for comparisons; label state-only baselines separately
from RGB + proprioception experiments. Do not claim improvement from loss alone.
