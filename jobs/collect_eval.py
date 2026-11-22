"""Collect per-episode rows from eval jobs' eval.json into one committed CSV.

Usage (from the repo root, any venv with Python 3):
    python jobs/collect_eval.py can results/can_eval_episodes.csv 0:5949705 1:5950799
Each SEED:JOB names one eval job under $HPCWORK/franka-il/runs/<task>_eval/<JOB>/eval.json.
Failure-filming re-runs duplicate existing rows; leave them out.
"""
import csv
import json
import os
import sys
from pathlib import Path

task, out, *pairs = sys.argv[1:]
root = Path(os.environ["HPCWORK"]) / "franka-il/runs" / f"{task}_eval"
rows = []
for pair in pairs:
    seed, job = map(int, pair.split(":"))
    report = json.loads((root / str(job) / "eval.json").read_text())
    assert report["settings"]["seed"] == seed and report["paired"], (job, report["settings"])
    for r in report["results"]:
        for e in r["episodes"]:
            x, y, _ = e["object_init_pos"]
            rows.append({"seed": seed, "epoch": r["epoch"], "episode": e["episode"],
                         "success": int(e["success"]), "steps": e["steps"],
                         "obj_x": x, "obj_y": y, "init_sha1": e["init_state_sha1"],
                         "eval_job": job})
rows.sort(key=lambda d: (d["seed"], d["epoch"], d["episode"]))
Path(out).parent.mkdir(exist_ok=True)
with open(out, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
print(f"wrote {len(rows)} rows to {out}")
