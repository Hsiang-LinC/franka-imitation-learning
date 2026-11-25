# Decisions

Current decisions only. Superseded options (an earlier Isaac Lab/Isaac Sim route,
exercise-first ordering, optional BC-RNN) are kept in Git history.

## D1 · Simulator, task and compute split (revised 2026-11-25)

Current stack: robosuite v1.5.x + MuJoCo 3.x + robomimic v0.5+, with robomimic's
v1.5 Franka datasets. Task ladder: Lift (warm-up) → Can → **Square** (main task);
Transport/ToolHang are optional stretch tasks. Reasons: robomimic provides the BC-RNN
baseline and the datasets, and Square has published Diffusion Policy results to
sanity-check against. This replaces MimicGen `stack_three_d0`, whose robosuite ≤1.4.1
pin blocked modern MuJoCo and robomimic's Diffusion Policy. Phase-2/3 policies train in
LeRobot (D9).

MuJoCo needs no RTX GPU (unlike Isaac Sim): physics runs on CPU and rendering uses
OpenGL via OSMesa (CPU) or EGL. **CLAIX CPU** runs simulation, replay, low-dim training,
rollout evaluation and analysis. **Rented cloud GPUs** run image-based and VLA training
(D11). CLAIX GPUs are used only for short checks. Reasons: BC-RNN low-dim Lift trains at
≈5.5 s/epoch on CPU and does not speed up beyond ~2 cores (docs/BASELINE.md), so a full
2000-epoch run costs ≈13 core-h; the default CLAIX GPU quota (10 GPU-h/month per the IT
Center, 2026-06; repo previously recorded 3) and queue times cannot cover image training,
and Colab quota was checked and is insufficient.

## D2 · Baseline first, upstream code reused

Phase 1 reproduces BC-RNN end to end with upstream robomimic entry points;
phase 2 compares ACT and Diffusion Policy; phase 3 runs controlled sweeps and packages
the portfolio. We own configs, Slurm jobs, notebooks and evidence, not copies of
upstream trainers. Gymnasium and FK/IK are optional lessons.

## D3 · Freeze the benchmark before headline comparisons

Phase 1 uses development rollouts. Before ACT/Diffusion headline numbers, freeze the
evaluator, reset lists (ID/OOD) and success predicate. Any protocol change gets a new
version and the affected methods are rerun.

## D4 · Lift warm-up before the main task (2026-11-15)

Run the full replay → train → reload → rollout → video loop on robomimic Lift
(proficient-human, low-dim) first. Lift is short and reliably learnable, so failures
isolate environment/rendering/Slurm problems rather than task difficulty. Use the same
pipeline (scripts, rendering, Slurm setup) as the main task; simulator versions follow D6.
Lift results are a pipeline check, not portfolio results.

## D5 · Two learning tracks (2026-11-15)

- **Track A, reproduction:** upstream scripts, configs and Slurm jobs produce all
  reported numbers.
- **Track B, understanding:** small from-scratch implementations (diffusion policy,
  action chunking) in notebooks or `src/`, trained on the same low-dim data and compared
  against Track A. They exist to explain mechanisms; they never replace upstream
  results in headline tables unless evaluated under the frozen protocol.

## D6 · Simulator pins per dataset (2026-11-21)

Pin robosuite and MuJoCo separately for each dataset. Pick the combination on which the
most demos succeed under open-loop action replay. On a tie, pick the newer version. Only
combinations that satisfy each package's declared dependencies count. robomimic and the
trainer env stay shared.

## D7 · Phase-2 headline comparison uses RGB + proprioception (2026-11-25)

ACT and Diffusion Policy are compared on Square with camera images plus proprioception,
not privileged object state. Reasons: pretrained VLAs (D8) consume images, so only an
image-based baseline is comparable with them; state-only results do not show
vision-based manipulation. Low-dim runs stay useful for pipeline checks and Track B and
are labelled state-only. Image training runs on cloud GPUs (D1, D11).

## D8 · Pretrained VLA fine-tuning moves into phase 3 (2026-11-25)

Fine-tune an open pretrained VLA with PEFT (LoRA) on the same Square data. Evaluate it under
the frozen protocol (D3) alongside the from-scratch policies at several demonstration
budgets. Question: how does pretraining change data efficiency compared with training from
scratch? This replaces the former stretch goal S2 (#22).

Design (chosen 2026-11-25): Square only. The arms differ only in initialisation and are
trained on the same demonstration subsets:
- Diffusion Policy from scratch;
- SmolVLA from a VLM-only init (no robot pretraining, as in the SmolVLA paper's LIBERO runs);
- `smolvla_base` + LoRA (pretrained on SO-100 data, other embodiment);
- optional: `pi0_base` + LoRA at one budget (Franka in its pretraining; ≈3B, needs >22.5 GB).
Question: does cross-embodiment robot pretraining help on a new robot and task? Robot
pretraining has been measured on the real SO100 only, and π0 on Meta-World did not
benefit, so either outcome is informative. All arms use 84×84 inputs (SmolVLA upsamples;
reported as a limitation). Budgets and seeds are sized after the cloud pilot (D11).
Rejected: LIBERO for phase 3. It would need a second simulator pin (robosuite 1.4.0) and
benchmark, its main suites are near ceiling, and LeRobot ACT/DP are not
language-conditioned. LIBERO is a stretch after the portfolio.

## D9 · LeRobot hosts phase-2/3 policies, run from one container (2026-11-25)

ACT, Diffusion Policy and SmolVLA train in LeRobot (v0.7.0, pinned by commit). One dataset
conversion serves all three, ACT and DP share the ResNet18 encoder at native 84×84
resolution, and LeRobot is the ecosystem pretrained VLAs ship in. robomimic stays for
BC-RNN and the datasets. One robomimic Diffusion Policy run at full budget checks the
LeRobot DP result. Rejected: robomimic DP plus LeRobot ACT (two trainers, unmatched
encoders).

LeRobot needs Python ≥3.12, so it cannot share the 3.11 venvs. One container image
(LeRobot + robosuite 1.5.1 + MuJoCo 3.2.7 + OSMesa) does conversion, cloud training
(Docker) and CLAIX evaluation (Apptainer). This deviates from the venv convention because
the same image must run on both sides. Acceptance: Square ph replay reproduces 181/200
inside the container (D6). GitHub Actions builds the image once and pushes the same digest
to ghcr.io (CLAIX pulls it) and to Artifact Registry (Vertex documents only that source). The existing venvs stay for robomimic work.

Phase 2 uses each method's recommended hyperparameters. The chunk length is studied in
the phase-3 execution-horizon sweep. Tracking uses LeRobot's built-in Trackio (v0.7.0
removed W&B). Track B is paused until after phase 2.

## D10 · Hugging Face Hub is the artifact hub (2026-11-25)

Every artifact has exactly one home:

| Artifact | Home |
|---|---|
| Upstream raw datasets | `robomimic/robomimic_datasets` on the Hub, pinned revision + SHA256 (unchanged, read-only) |
| Derived datasets (rendered images, LeRobotDataset conversion) | Own private Hub dataset repo |
| Checkpoints behind a reported result, from any trainer (incl. CLAIX BC-RNN) | Own private Hub model repo |
| Intermediate training checkpoints | Cloud bucket during the run (cleared after), or CLAIX `$HPCWORK` |
| Rollout videos and episode logs | CLAIX `$HPCWORK`; selected clips as release assets (D12) |
| Code, configs, split/budget manifests, checksums | Git |
| Run evidence | The relevant GitHub issue |

This follows the LeRobot convention (`repo_id` + revision). CLAIX and cloud jobs read and
write the same place. Demonstration budgets are episode lists in a manifest, not dataset
copies. Repos go public only after the dataset and model licenses are verified.

## D11 · Cloud GPU: GCP Vertex AI Spot with a spend cap (2026-11-25)

Training is submitted as containerised Vertex AI custom jobs on Spot L4 GPUs in an EU
region (the cloud equivalent of Slurm). Jobs checkpoint regularly and resume after
preemption. Funding: the GCP $300 new-customer credit, which covers GPUs only after the
account is upgraded to paid and expires 90 days after sign-up. So sign up when the
pilot is ready (roadmap step 5), then request GPU quota immediately.

Cap: at most €50 of own money beyond the credit. A budget alert fires at 50/90/100 %, and
a Pub/Sub-triggered function disables billing at the cap (GCP budgets alone only alert).
Fallback if GPU quota is refused: RunPod or Vast.ai L4 under the same cap. Rejected:
- Azure for Students (no GPU quota on student subscriptions);
- AWS free plan (GPU instances excluded);
- Google research credits (PhD or faculty only);
- Colab (insufficient quota).
Each provisioning step still needs explicit approval.

## D12 · Results are presented as a project page (2026-11-25)

Analysis notebooks are the single source. Quarto renders them to a GitHub Pages project
page with figures and clips. The README carries a headline clip, the results table and
links. Videos are hosted as release or Hub assets, not in notebook outputs. This follows
the paper-plus-project-page convention of the Diffusion Policy and ACT papers.
