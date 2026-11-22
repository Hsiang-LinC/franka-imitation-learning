"""Cut one episode out of an eval MP4 (or take a whole replay MP4) into a small GIF for
docs/media/ (notebooks/README.md).

An eval MP4 holds the filmed episodes back to back, one frame per environment step, so the
episode boundaries follow from the steps recorded in eval.json. A replay MP4
(jobs/replay.sh TASK DEMOS) holds one demo, recorded | replayed side by side.
Usage (sim venv, which has imageio + ffmpeg):
    python jobs/make_clips.py EVAL_DIR CHECKPOINT_STEM EPISODE OUT.gif [--speed 4] [--size 200]
    python jobs/make_clips.py REPLAY.mp4 OUT.gif [--speed 2]
    e.g. ... $HPCWORK/franka-il/runs/can_eval/5950806 model_epoch_1300_ep4-36 36 docs/media/can_fail_ep36.gif
"""
import argparse
import json
import re
from pathlib import Path

import imageio.v2 as imageio
from PIL import Image

p = argparse.ArgumentParser()
p.add_argument("source", nargs="+", help="EVAL_DIR CHECKPOINT_STEM EPISODE, or one replay MP4")
p.add_argument("out", type=Path)
p.add_argument("--speed", type=int, default=4, help="keep every n-th frame (played at 10 fps x n)")
p.add_argument("--size", type=int, default=200, help="frame height in pixels")
p.add_argument("--colors", type=int, default=48)
args = p.parse_args()

if len(args.source) == 1:                                    # whole replay MP4
    video, start, stop, note = Path(args.source[0]), 0, None, "whole video"
else:
    eval_dir, video_stem, episode = Path(args.source[0]), args.source[1], int(args.source[2])
    report = json.loads((eval_dir / "eval.json").read_text())
    m = re.fullmatch(r"(model_epoch_\d+)(?:_ep([\d-]+))?", video_stem)   # suffix from --video_list
    result = next(r for r in report["results"] if r["checkpoint"] == m[1] + ".pth")
    filmed = sorted(map(int, m[2].split("-"))) if m[2] else list(range(3))   # eval_cpu.sh films 3
    assert episode in filmed, f"episode {episode} not in video ({filmed})"
    steps = {e["episode"]: e["steps"] for e in result["episodes"]}
    start = sum(steps[i] for i in filmed if i < episode)
    stop = start + steps[episode]
    video = eval_dir / "videos" / f"{video_stem}.mp4"
    ep = next(e for e in result["episodes"] if e["episode"] == episode)
    note = f"episode {episode}, {'success' if ep['success'] else 'failure'} after {ep['steps']} steps"

frames = []
for i, f in enumerate(imageio.get_reader(str(video))):
    if i >= start and (stop is None or i < stop) and (i - start) % args.speed == 0:
        h, w = f.shape[:2]
        frames.append(Image.fromarray(f).resize((args.size * w // h, args.size), Image.BILINEAR))
# One shared palette (from a mid-episode frame), no dithering: keeps the GIF small and stable.
palette = frames[len(frames) // 2].quantize(colors=args.colors, method=Image.Quantize.MEDIANCUT)
frames = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]
args.out.parent.mkdir(parents=True, exist_ok=True)
frames[0].save(args.out, save_all=True, append_images=frames[1:], duration=100, loop=0,
               optimize=True)   # 10 fps, loops forever
print(f"{args.out}: {note}, {len(frames)} frames, {args.out.stat().st_size // 1024} KB")
