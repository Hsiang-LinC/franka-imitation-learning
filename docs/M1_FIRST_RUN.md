# Optional M1.1: first Gymnasium rollout

Issue: https://github.com/Hsiang-LinC/franka-imitation-learning/issues/3

This exercise runs CartPole with random actions. It does not train a policy.
The shared reset/step/episode-end loop will later support ACT and Diffusion Policy evaluation.

## Environment

Verified Python 3.11.5. Use a Python 3.11 interpreter to create the environment if absent:

```bash
python3.11 -m venv .venvs/franka-foundations
.venvs/franka-foundations/bin/python -m pip install -r requirements/foundations.txt
```

The current project-local environment already has these dependencies installed.
No GPU or display is required. From the repository root, inside an existing CPU allocation:

```bash
.venvs/franka-foundations/bin/python exercises/gymnasium/episode_trace.py --seed 42
.venvs/franka-foundations/bin/python exercises/gymnasium/episode_trace.py --seed 42 --max-steps 5
```

Alternatively, request a short CPU job from a login shell:

```bash
srun --partition=devel --nodes=1 --ntasks=1 --cpus-per-task=1 --mem=1G --time=00:02:00 --propagate=NONE .venvs/franka-foundations/bin/python exercises/gymnasium/episode_trace.py --seed 42
```

Do not request a second allocation when already inside an interactive allocation.

## Read the trace

- Observation: cart position, cart velocity, pole angle, pole angular velocity.
- Action: 0 pushes left; 1 pushes right. Actions are random, not learned.
- `reset(seed=42)` starts an episode and returns the first observation and diagnostic `info`.
- `step(action)` returns the next observation, reward, `terminated`, `truncated`, and `info`.
- `terminated` means an ending defined by the task (here, cart/pole failure).
- `truncated` means an external limit (here, the configured step limit).
- Stop when either flag is true. Reset before taking another episode's actions.
- `info` is empty in this example; other environments can expose diagnostic values.
- Seed both reset and action sampling: they have separate random generators.

Official API reference: https://gymnasium.farama.org/introduction/basic_usage/

## Verified evidence (2026-11-14)

Python 3.11.5, Gymnasium 1.2.2, NumPy 2.2.6; all installed dependencies pinned in
`requirements/foundations.txt`. `pip check` passed.

- CPU Slurm job 5765498: seed 42, max steps 50; ended at step 30, return 30,
  terminated=true, truncated=false. An RLIMIT_NOFILE propagation warning appeared,
  but the rollout completed with exit code 0.
- CPU Slurm job 5765504: repeated the exact trace byte for byte and verified
  max steps 5 ends at step 5, return 5, terminated=false, truncated=true.
  This job used `--propagate=NONE` and completed without that warning.
- Local ignored artifacts: `runs/m1/seed42.txt` and `runs/m1/seed42-limit5.txt`.
- SHA256 seed42.txt: `d402fefc80bf344c1f553e4e049ee2c78a655e42669f04210005d68e093bee58`.
- SHA256 seed42-limit5.txt: `31b34f1a93140579213e76522d2b6f8ce0f1119a21cfca745c7b0ae0828aaa17`.

Pending: learner rerun and explanation of the two ending flags. GUI rendering has not
been installed or tested. M1.2 custom 2D reaching and its environment checker are pending.
M0 compute qualification and the M3 simulator environment remain separate work.

The exercise was moved during the baseline-first reorganization. Historical checksums
refer to the captured trace; source contents were preserved. This lesson is optional.
