---
name: video-director
description: Default entry point inside Motion-DESIGNER for making, directing, or finishing any video end to end - launch film, fast-paced/hype launch cut, ad or commercial spot, social reel, explainer, logo sting, product demo, title sequence, music/lyric video, data story, art loop, teaser, or 3D product hero. Runs preflight, directs the concept (video-prompt-enhancer engine), locks ONE engine (motionmaxxing, cinetic, HyperFrames, Remotion, anidoodle, huashu-art-motion, Manim, Blender) and checks the concept against that engine's own bans, builds the hero moment first, runs the engine's native gates, sends the render to an independent motion-critic jury for up to 3 revision rounds, and delivers final.mp4 + NOTE.md. Use this before reaching for hyperframes, cinetic, motionmaxxing, or any global video skill whenever the request is "make/create/build/render a video" in this repository. For a plan only, it hands off to video-prompt-enhancer.
---

# Video Director

You are the director running the whole job. You choose the order of work and which engine builds it. The craft lives in the existing skills; this skill makes sure they run **in the right order, with one engine, and are judged by someone else**. Read `AGENTS.md` §1.5 (Creative Director Protocol): this skill is its executable form.

`REPO` = repository root. `ENGINE` = `.agents/skills/<locked engine>`. Windows: Python is `.venv\Scripts\python.exe` (never `python3`), `.sh` scripts run with `& "C:\Program Files\Git\bin\bash.exe"` in PowerShell (never the WSL `bash`). motionmaxxing step 0 (`providers.sh`) does not know Windows Chrome paths; use `doctor.py` (step 0 below) instead.

## 0. Preflight (≈30 s)
```powershell
.venv\Scripts\python.exe .agents/skills/video-director/scripts/doctor.py
```
```bash
.venv/bin/python .agents/skills/video-director/scripts/doctor.py
```
It lists which engines are ready. A blocked engine is not an option in step 3; say so in one line and route around it. Missing ElevenLabs key: no VO/generated music; use CC0 + `librosa`, or `mgaudio`.

## 1. Classify the request
| Signal | Do |
|---|---|
| "plan / enhance / direct / write a prompt" only | Hand off to `video-prompt-enhancer` and stop after its Prompt-Plan. |
| "critique / review / judge" an existing video | Hand off to `motion-critic`. |
| "clone / match / copy this animation" from a live site or Lottie/WebGL | `reanimate` first (needs Bun), then this flow from step 5. |
| "recreate / remake this video" from a video file | `reverse-any-video` (HyperFrames, frame-by-frame check against the original). |
| "an episode in the style of" (collage, finance, science, 3D brand, true-crime explainers) | `style-sampling` (HyperFrames). |
| port existing Remotion / Motion Canvas / Lottie / Manim work | `remotion-to-hyperframes`. |
| a deck or live presentation, not a rendered video | `slideshow` (HyperFrames). |
| make / create / build / render a video | Continue below. |

Map the brief to one playbook in `.agents/skills/video-prompt-enhancer/references/creative-direction.md` Part C: C1 launch · **C1b fast-paced / hype launch** · C2 ad (6/15/30 s) · C3 explainer · C4 sting · C5 social · C6 demo · C7 titles · C8 music · C9 data · C10 art loop · C11 teaser · C12 3D hero.

## 2. Direct (concept before tools)
1. Ask the 2-4 scoping questions from `video-prompt-enhancer/references/interview-bank.md`, only for decisions the brief leaves open, with at least one creative question. In Claude Code use `AskUserQuestion`, with the recommended option first. If the brief already answers them, skip the interview and state your assumptions.
2. Run the 10-move Direction Engine (`creative-direction.md` Part A, including **Move 4b**) and apply the matching Part C playbook.
3. Write `projects/<slug>/BRIEF.md` (PAGE, one true thing, format) and `projects/<slug>/PLAN.md` (the `plan-template.md` sections 0-4). Unlike the planner, you continue building after the plan.

## 3. Lock ONE engine (Move 4b)
| Video type | Default engine | Switch when |
|---|---|---|
| C1 launch · C1b hype · C2 ad · C4 sting · C11 teaser | `motionmaxxing` (brand URL capture, seek-safe GSAP, `look.py` + `lint.mjs`) | the brief wants Remotion, house scenes, a licensed track, chapters → `cinetic` |
| C6 demo / UI walkthrough | `cinetic` (UI walkthrough + feature-loop formats) | bespoke brand-voice film from a URL → `motionmaxxing` |
| C5 social / reel | the C1/C2 engine at 1080x1920, composed for 9:16 | an illustrated loop → `anidoodle` |
| C3 explainer | `anidoodle` (EN), `huashu-art-motion` (ZH / bilingual), Manim (math) | captions over a React build → `remotion-best-practices` |
| C7 titles · C12 3D hero | `blender-core` → `blender-workflow-recipes`, then 2D type in the promo engine | — |
| C8 music · C10 art loop | `anidoodle` / `resources/mg-styles-15/` (+ `three.quarks` for audio-reactive) | lyrics-led → `remotion-captions` |
| C9 data story | Manim (`Text`/`MarkupText`) or `huashu-art-motion` `t3_finance_chart` | charts / maps from ready blocks → HyperFrames + `hyperframes-registry` |
| Captioned vertical clips, overlays, title cards, a Figma design brought to life | `hyperframes` (+ `hyperframes-registry` blocks, `figma`) | a bespoke brand film from a URL → `motionmaxxing` |

**HyperFrames** (`hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use`) is a full engine here, not a runtime under the others. Pick it when a ready block (one of ~450: captions, charts, maps, transitions, kinetic type) or its audio mixer does the hero job better than hand-building. Before hand-building any named visual (CRT, glitch, film grain, chart, terminal window) in any engine, search `hyperframes-registry` first. Its native gate is `npx hyperframes check --json` plus `snapshot --review` → `REVIEW.md`. HyperFrames' house style never overrides `motionmaxxing` or `cinetic` rules in a film locked to those engines.

Then read `ENGINE/SKILL.md` in full and check the concept against **its** ban list (motionmaxxing "Never ship", cinetic "Hard bans"). Where engines disagree (serif type, colour floods, word timing, centred lines, generated music), the locked engine wins; never mix the two promo engines' rules in one film. Write `engine-ban check: PASS` (or what changed) into `PLAN.md`.

## 4. Lay out the project
```
projects/<slug>/
  BRIEF.md  PLAN.md          # step 2
  film/                      # the engine's own layout (motionmaxxing: index.html, runtime/, STORYBOARD.md, audio/, look/)
  critic/                    # motion-critic output per round: critic/r1, critic/r2 ...
  NOTE.md                    # delivery note (engine format), written last
```
- `motionmaxxing`: copy `ENGINE/templates/film.html` → `projects/<slug>/film/index.html` and `ENGINE/runtime/` → `projects/<slug>/film/runtime/`.
- `cinetic` (from `ENGINE`, absolute target path): `& "C:\Program Files\Git\bin\bash.exe" scripts/new-film.sh "<REPO>/projects/<slug>/film" --name "<Product>" [--size 1080x1920] [--pace crisp] [--bpm N]`. Set `PYTHON` to the venv interpreter first (`$env:PYTHON = "<REPO>\.venv\Scripts\python.exe"`, or `export PYTHON=<REPO>/.venv/bin/python`), or cinetic picks a system Python without `soundfile`/`cv2`. `earshot` (cinetic's sound listener) lives in its own venv (`EARSHOT_PYTHON`); without it the sound check is advisory.
- Remotion (direct): `remotion-create` (per-project `npx`; nothing installs at the repo root).
- Others: follow `ENGINE/SKILL.md`; keep outputs under `projects/<slug>/`.

## 5. Hero first
Build the hero moment (60-75 % of runtime) and its hardest seam **before anything else**. Render 3-5 stills around it and look at them. If it does not read at speed, change the idea or the staging now. The rest of the film is built around a hero that already works.

## 6. Build, then the engine's native gate
Build the full film at target spec with the sound cut to picture, following `ENGINE/SKILL.md` step by step. Run the engine's own gate (`AGENTS.md` §6) and fix every FAIL before the jury sees it. Never self-certify from source code.

## 7. Independent jury (max 3 rounds)
The maker does not judge its own film. In Claude Code, run `motion-critic` in a **fresh subagent** that did not build the film. Give it only the paths, the planned numbers and the target lens:
```powershell
.venv\Scripts\python.exe .agents/skills/motion-critic/scripts/critic_scan.py projects/<slug>/film/final.mp4 --out projects/<slug>/critic/r1 --expect <s> --hero <s>
```
Apply the ranked fix list (Critical items first, plus at least one fix that raises the idea), re-render, and re-judge into `critic/r2`. Ship when every dimension is ≥ 8, Idea + Motion Craft are ≥ 9, and no check FAILs. After round 3, or a round that does not raise the total, stop and report the scores honestly.

## 8. Deliver
- `final.mp4` at spec (verify with `ffprobe -v error -show_format -show_streams`), the editable source, and `NOTE.md` in the engine's format: the one idea, beats and what each buys, what is real vs illustrative, gate numbers quoted from scripts, the jury scores per round, and what you would still improve.
- Other aspect ratios are **re-composed** from source at the new size, never letterboxed or centre-cropped.
- Licences: record every CC/licensed asset with its attribution in `CREDITS.md`. Copyrighted audio never goes into the repository.
- Ask before pushing, before any paid API spend (ElevenLabs, image generation, HeyGen generation via `media-use`), and before downloading binaries. HyperFrames asks once whether to send its usage note; respect the answer.

## Time budget (for a 15-30 s film)
Preflight + direction 15 % · hero stills by 30 % · full draft with sound by 50 % · gates + jury rounds 50-85 % · final render + NOTE 85-100 %. A 2 h job keeps this shape; renders are slow, so cut every later look from one early full draft.
