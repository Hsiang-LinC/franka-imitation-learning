"""Resolve a committed robomimic config into a per-run config.

robomimic's train.py takes the output directory and every hyperparameter from the JSON
config (it has no CLI overrides besides --dataset). Committed configs keep portable
placeholders; a job writes the resolved copy next to the run so the run records exactly
what it trained with (configs/README.md).

Usage:
    python jobs/make_run_config.py BASE.json OUT.json \
        train.output_dir=/abs/path experiment.rollout.enabled=false train.num_epochs=20

Each override is a dotted key path and a JSON value (false, 20, "text", [1, 2]); a value
that is not valid JSON is taken as a plain string. Unknown keys are an error, so a typo
cannot silently add a setting robomimic ignores.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def parse_value(text: str):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def apply_override(config: dict, dotted_key: str, value) -> None:
    *parents, leaf = dotted_key.split(".")
    node = config
    for key in parents:
        if not isinstance(node.get(key), dict):
            raise KeyError(f"{dotted_key}: '{key}' is not a section of the config")
        node = node[key]
    if leaf not in node:
        raise KeyError(f"{dotted_key}: unknown key '{leaf}'")
    node[leaf] = value


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    base, out, *overrides = argv
    config = json.loads(Path(base).read_text())
    for item in overrides:
        key, sep, text = item.partition("=")
        if not sep:
            raise ValueError(f"override '{item}' is not key=value")
        apply_override(config, key, parse_value(text))
        print(f"  {key} = {config_value(config, key)!r}")
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(config, indent=4))
    return 0


def config_value(config: dict, dotted_key: str):
    node = config
    for key in dotted_key.split("."):
        node = node[key]
    return node


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
