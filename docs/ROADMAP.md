# Learning roadmap

The approved sequence is baseline first, then comparison, then controlled improvements.
Legacy M0–M9 numbers remain identifiers for existing issues, not mandatory lesson order.
See [baseline flow](BASELINE.md), [session context](PROJECT_CONTEXT.md) and
[GitHub Project](https://github.com/users/Hsiang-LinC/projects/3/views/1).

| Phase | Work and legacy issue numbers | Exit gate |
|---|---|---|
| 1 · End-to-end BC-RNN baseline | M0 compute #2; M3 environment/replay #8–9; M4 data #10–11; M5 BC-RNN #12 (state), #13 (vision when ready); baseline report #15 | Own trained checkpoint reloads into matching simulator; closed-loop evaluation produces success counts and success/failure videos with reproducible settings |
| 2 · ACT and Diffusion Policy comparison | M6 frozen benchmark #14; M7 shared data conversion #16, ACT #17, Diffusion #21 | Both checkpoints evaluated with matched inputs/data/actions and identical held-out reset lists; metrics and limitations reported |
| 3 · Controlled improvement and portfolio | M8 ablations #18 and analysis #19; M9 portfolio #20 | Separate data-budget and execution-horizon sweeps, uncertainty and failure analysis; reproduction instructions, report and videos |

M1 Gymnasium #3–4 and M2 FK/IK #5–7 are optional supporting lessons. S2 SmolVLA #22
remains a stretch goal after the core project. Initial state-only BC-RNN is an integration
baseline; a direct cross-method comparison requires matched observations and evaluation.
#15 is the phase-1 baseline report in M5. It precedes #14; any later matched BC-RNN
comparison must be rerun on the frozen phase-2 evaluator.

## Phase 1 order

1. Understand the upstream entry points and persistent artifacts.
2. Qualify CPU/H100 jobs and shared storage; pin simulator/trainer environments.
3. Download only the selected `stack_three_d0.hdf5`, record provenance/checksum,
   inspect metadata and execute one saved action sequence from its initial state.
4. Inspect observations/actions and freeze episode splits before fitting a model.
5. Run a bounded training smoke check; verify checkpoint saving and reloading.
6. Train BC-RNN and evaluate saved checkpoints separately in the simulator.
7. Record baseline successes/trials, failures, videos and reproduction settings.

Use development rollouts for iteration. Freeze phase-2 held-out ID/OOD cases before
headline comparisons. A short training run proves integration, not task competence.
Issue labels, native dependencies and milestone descriptions are synchronized with this
sequence. Project custom fields/manual ordering remain pending due to missing Project
access. Check live status before executing any issue. No runtime milestone is completed
by this documentation change.
