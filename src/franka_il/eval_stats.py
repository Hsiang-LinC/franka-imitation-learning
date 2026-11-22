"""Statistics for paired closed-loop evaluation (moved from notebooks/00b, reused by 02).

Rows of an eval CSV are episodes: seed, epoch, episode, success, steps, ... Every checkpoint
evaluated on one seed faces the same initial states, so episode i is comparable across
checkpoints (jobs/eval_checkpoints.py checks this with a hash of the full initial state).
"""
import csv
from pathlib import Path

import numpy as np
from scipy import stats

INT_COLS = {"seed", "epoch", "episode", "success", "steps", "eval_job"}


def read_rows(path: Path) -> list[dict]:
    with Path(path).open() as fh:
        return [{k: int(v) if k in INT_COLS else (v if k.endswith("sha1") else float(v))
                 for k, v in r.items()} for r in csv.DictReader(fh)]


def to_matrix(rows, seed, key):
    """Return (epochs, M) with M[checkpoint, episode] = row[key] for one seed."""
    sel = [r for r in rows if r["seed"] == seed]
    epochs = np.array(sorted({r["epoch"] for r in sel}))
    n_ep = max(r["episode"] for r in sel) + 1
    M = np.full((len(epochs), n_ep), -1)
    row_of = {e: i for i, e in enumerate(epochs)}
    for r in sel:
        M[row_of[r["epoch"]], r["episode"]] = r[key]
    assert (M >= 0).all(), "missing (epoch, episode) entries"
    return epochs, M


def wilson(k, n, z=1.96):
    """95% Wilson score interval for k successes out of n (arrays allowed)."""
    p = np.asarray(k, dtype=float) / n
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    half = z / denom * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2))
    return center - half, center + half


def discordant(a, b):
    """Episodes where only a succeeds, and where only b succeeds."""
    a, b = np.asarray(a, dtype=bool), np.asarray(b, dtype=bool)
    return np.flatnonzero(a & ~b), np.flatnonzero(~a & b)


def mcnemar_exact(a, b):
    """Two-sided exact McNemar p-value (binomial test on the discordant pairs)."""
    only_a, only_b = discordant(a, b)
    m = len(only_a) + len(only_b)
    return 1.0 if m == 0 else stats.binomtest(len(only_a), m, 0.5).pvalue
