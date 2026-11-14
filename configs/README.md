# Experiment configurations

Store project-specific settings derived from pinned upstream configuration generators.
No BC-RNN config is validated yet. Add it after inspecting dataset paths, observation
keys and the selected upstream revision. Record its upstream source and modifications.

Use the same trainer for different experiments; express policy parameters, seeds and
budgets through configs rather than copied scripts. Resolve external storage paths at
execution time and save the resolved configuration with the run, outside Git. Commit
only sanitized portable settings. Phase 2 adds matched ACT/Diffusion and evaluation
configs; do not create speculative placeholders now.
