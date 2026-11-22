"""Cut one episode out of an eval MP4 into a small GIF for docs/media/ (notebooks/README.md).

An eval MP4 holds the filmed episodes back to back, one frame per environment step, so the
episode boundaries follow from the steps recorded in eval.json.
Usage (sim venv, which has imageio + ffmpeg):
    python jobs/make_clips.py EVAL_DIR CHECKPOINT_STEM EPISODE OUT.gif [--speed 4] [--size 200]
    e.g. ... $HPCWORK/franka-il/runs/can_eval/5950806 model_epoch_1300_ep4-36 36 docs/media/can_fail_ep36.gif
"""
import argparse
import json
import re
from pathlib import Path

import imageio.v2 as imageio
from PIL import Image

p = argparse.ArgumentParser()
p.add_argument("eval_dir", type=Path)
p.add_argument("video_stem", help="MP4 name without extension, e.g. model_epoch_2000")
p.add_argument("episode", type=int)
p.add_argument("out", type=Path)
p.add_argument("--speed", type=int, default=4, help="keep every n-th frame (played at 10 fps x n)")
p.add_argument("--size", type=int, default=200)
p.add_argument("--colors", type=int, default=48)
args = p.parse_args()

report = json.loads((args.eval_dir / "eval.json").read_text())
m = re.fullmatch(r"(model_epoch_\d+)(?:_ep([\d-]+))?", args.video_stem)   # suffix from --video_list
result = next(r for r in report["results"] if r["checkpoint"] == m[1] + ".pth")
filmed = sorted(map(int, m[2].split("-"))) if m[2] else list(range(3))   # eval_cpu.sh films 3
assert args.episode in filmed, f"episode {args.episode} not in video ({filmed})"
steps = {e["episode"]: e["steps"] for e in result["episodes"]}
start = sum(steps[i] for i in filmed if i < args.episode)
stop = start + steps[args.episode]

reader = imageio.get_reader(str(args.eval_dir / "videos" / f"{args.video_stem}.mp4"))
frames = [Image.fromarray(f).resize((args.size, args.size), Image.BILINEAR)
          for i, f in enumerate(reader) if start <= i < stop and (i - start) % args.speed == 0]
# One shared palette (from a mid-episode frame), no dithering: keeps the GIF small and stable.
palette = frames[len(frames) // 2].quantize(colors=args.colors, method=Image.Quantize.MEDIANCUT)
frames = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]
args.out.parent.mkdir(parents=True, exist_ok=True)
frames[0].save(args.out, save_all=True, append_images=frames[1:], duration=100, loop=0,
               optimize=True)   # 10 fps, loops forever
ep = next(e for e in result["episodes"] if e["episode"] == args.episode)
print(f"{args.out}: episode {args.episode}, {'success' if ep['success'] else 'failure'} "
      f"after {ep['steps']} steps, {len(frames)} frames, {args.out.stat().st_size // 1024} KB")
