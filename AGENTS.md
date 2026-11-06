# Project guidance

## Resume and guide the learning plan

At the start of each project session, read [the roadmap](docs/ROADMAP.md) for milestone order and exit criteria, then follow [the session handoff](docs/PROJECT_CONTEXT.md). Check the live GitHub Issues for status, native blockers and acceptance evidence before selecting the next unblocked core task. Use the linked GitHub Project to see the current plan.

When guiding the learner, name the current milestone and issue, explain how it supports the ACT and Diffusion Policy comparison, and suggest one executable next step with a concrete success check. At the end of a work session, record verified evidence and remaining blockers in the issue.

Keep LeRobot training independent of the simulator runtime. Pin the robosuite, MuJoCo, MimicGen and robomimic versions against the selected dataset and check action playback before training. Use CLAIX CPU jobs for simulation and H100 jobs for training. Obtain explicit user approval before spending on or provisioning paid cloud GPUs.

Record commands, versions, seeds, artifact checksums and actual results. Report unrun checks as pending. Keep datasets, credentials, university connection details, logs with personal data, and large model artifacts out of Git. Verify redistribution rights before publishing demo data or model artifacts.
