# Session handoff

## Approved direction (2026-11-14)

Baseline-first, three phases: upstream BC-RNN end-to-end reproduction; matched ACT and
Diffusion Policy comparison; controlled improvements and portfolio. Fixed simulated
Franka three-cube task. Measure policy/system execution changes through closed-loop
success and latency. The user learns by implementing with mentor explanation/review.

Use [roadmap](ROADMAP.md), [baseline guide](BASELINE.md) and
[notebook plan](../notebooks/README.md). Current phase: 1, preparation; legacy M0/M3
issues #2/#8. Next learning activity: explain the real upstream data/config/train/rollout
handoffs, then expand environment preparation when requested. Do not resume mandatory
Gymnasium/FK/IK lessons or install/train merely because this restructure is complete.

## Verified and pending

- Optional CartPole exercise previously verified with Python 3.11.5, Gymnasium 1.2.2,
  NumPy 2.2.6 in CPU jobs 5765498/5765504. Seed 42 traces identical; termination at 30
  and time-limit truncation at 5. See [evidence](M1_FIRST_RUN.md).
- Exercise moved to `exercises/gymnasium/episode_trace.py`; contents preserved.
- Robot notebooks, simulator/trainer dependencies, dataset download, action playback,
  BC-RNN training/deployment and all comparison results remain pending.
- Structure now documents upstream reuse; no custom trainer/evaluator or empty src tree.

## Tracking synchronization (2026-11-14)

Issue descriptions/labels now use the three phases. Required BC-RNN #12 and baseline
report #15 belong to M5; #13 is an optional vision extension. M1/M2 are optional.
Native dependency targets: #15 <- #12, #14/#16 <- #15, #17/#21 <- #14 and #16.
Optional FK starts independently of Gymnasium; SmolVLA follows the core portfolio.
Milestone names/descriptions reflect the same phases. No unfinished issue was closed.
#8 remains blocked by open #2, the current compute qualification task.

Project layout, custom fields and manual ordering remain unsynchronized: the GitHub CLI
token lacks read:project (and project edits require project write access). Available
connector tools do not expose Project management. Issue titles/milestones changed at
the source, but their appearance and ordering on the Project could not be verified.

## Session practice

Read the roadmap/context and inspect live Issues and the linked
[Project](https://github.com/users/Hsiang-LinC/projects/3/views/1). Record commands,
versions, sanitized artifact references, actual outcomes and remaining blockers in the
issue. Close only when acceptance criteria pass. Keep local-only edits distinguished
from published commits and external artifacts.
