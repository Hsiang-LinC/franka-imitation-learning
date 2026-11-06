# Project guidance

Read docs/PROJECT_CONTEXT.md, the relevant milestone and the selected issue before implementation. GitHub Issues own acceptance criteria and completion evidence. Use native issue dependencies for prerequisites and the linked GitHub Project for planning.

Keep LeRobot training independent of the simulator runtime. Pin the robosuite, MuJoCo, MimicGen and robomimic versions against the selected dataset and check action playback before training. Use CLAIX CPU jobs for simulation and H100 jobs for training. Obtain explicit user approval before spending on or provisioning paid cloud GPUs.

Record commands, versions, seeds, artifact checksums and actual results. Report unrun checks as pending. Keep datasets, credentials, university connection details, logs with personal data, and large model artifacts out of Git. Verify redistribution rights before publishing demo data or model artifacts.
