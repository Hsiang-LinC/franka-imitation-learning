# Experiment configurations

Store project-specific settings derived from pinned upstream configuration generators.
`lift/bc_rnn_low_dim.json` is the unmodified paper config from robomimic `d309eae`:
`python robomimic/scripts/generate_paper_configs.py --dataset_dir DATA_DIR --output_dir OUTPUT_DIR`
(file `core/lift/ph/low_dim/bc_rnn.json`). Jobs resolve it per run with
`jobs/make_run_config.py` and list their overrides in the job script.

Use the same trainer for different experiments; express policy parameters, seeds and
budgets through configs rather than copied scripts. Resolve external storage paths at
execution time and save the resolved configuration with the run, outside Git. Commit
only sanitized portable settings. Phase 2 adds matched ACT/Diffusion and evaluation
configs; do not create speculative placeholders now.
