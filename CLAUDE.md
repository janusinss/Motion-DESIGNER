@AGENTS.md

# Claude Code in Motion-DESIGNER

Everything in `AGENTS.md` applies. This file adds only what is specific to Claude Code.

## 1. Entry points (pick one before any tool call)
| Request | Skill |
|---|---|
| Make / create / build / render any video (launch, hype cut, ad, reel, explainer, sting, demo, titles, music, data, loop, teaser, 3D hero) | `video-director` (preflight → lessons + references → direct → plan-check → lock one engine → hero clip sign-off → gates → design-blind jury + blind A/B → deliver + lesson) |
| Plan, enhance, or direct a video prompt without building | `video-prompt-enhancer` (plan-only) |
| Critique, review, or score a rendered video | `motion-critic` |
| Clone or match an existing animation (site, Lottie, WebGL) | `reanimate` (needs Bun) |
| Recreate a video file · an episode in a proven style · port Remotion/Manim work · a live deck | `reverse-any-video` · `style-sampling` · `remotion-to-hyperframes` · `slideshow` (HyperFrames) |
| Any 3D / `.blend` work | `blender-core` → `blender-workflow-recipes` → … → `blender-asset-qa` |

## 2. Precedence over user-global skills
Inside this repository, `AGENTS.md` routing and the `.claude/skills/` mirror win over anything in `~/.claude/skills/`.
- **HyperFrames** is vendored in `.agents/skills/` (9 skills from `heygen-com/hyperframes`, unmodified; see `hyperframes/UPSTREAM.md`). It is one engine among several: `video-director` picks it per film. Older global installs (`~/.claude/skills/hyperframes-core`, `-animation`, `-audio`, … whose description says "mandatory entry point") are an outdated layout; use the repo copies, and that claim does not apply here. HyperFrames asks once to send a usage note: respect the user's answer. `media-use` generation through HeyGen needs a sign-in and may cost credits: ask first; its free local tools need no account.
- **motionmaxxing**: a global copy may exist. Use `.agents/skills/motionmaxxing`, which carries the Windows Chrome fix in `scripts/_cdp.mjs`.

## 3. Claude Code tools for the protocol
- **Interviews** (`video-prompt-enhancer`, `video-director` step 2): `AskUserQuestion`, 2-4 questions, recommended option first, at least one creative question.
- **Jury**: run `motion-critic` in a fresh `Agent` subagent that did not build the film. Pass it only the file paths, the planned duration and hero time, and the target award lens; it must judge the render, not the plan.
- **Renders and long jobs**: start with `run_in_background`, then wait for the completion notice; do not poll or sleep.
- **Before declaring done**: open the contact sheet (`Read` on `sheet.jpg`) and 3-5 full-size stills yourself. A gate number without a look is not evidence.

## 4. Windows command map (skill docs are written for macOS/Linux)
| Skill docs say | Run here |
|---|---|
| `python3 script.py` | `.venv\Scripts\python.exe script.py` (`python3` is the Microsoft Store stub) |
| `bash script.sh` | `& "C:\Program Files\Git\bin\bash.exe" script.sh` (`bash` on PATH is WSL) |
| `"$SKILL/scripts/x"` | `.agents/skills/<skill>/scripts/x` |
| Chrome for `render.mjs` / `brand.mjs` | found automatically; set `CHROME_PATH` only for a non-standard install |
| cinetic's Python (`scripts/py.mjs`, `frames.mjs python`) | `$env:PYTHON = "$PWD\.venv\Scripts\python.exe"` once per shell (otherwise it picks system Python, which lacks `soundfile`/`cv2`) |
| motionmaxxing step 0 `bash "$SKILL/scripts/providers.sh"` | `doctor.py` below (`providers.sh` ignores Windows Chrome paths and exits 1) |
| Is the toolchain ready? | `.venv\Scripts\python.exe .agents/skills/video-director/scripts/doctor.py` |

## 5. Ask first (limits on "Agent Tool Autonomy")
Act without asking for local building, rendering, and checking. Ask before:
- `git push`, opening PRs, or committing to `main`;
- paid API spend (ElevenLabs voice/music/SFX, image generation);
- downloading binaries or large media (EffectCraft, model weights, stock packs);
- deleting renders, `film/v<N>/` versions, or files the user edited.

## 6. Projects and git
- One folder per film: `projects/<slug>/` (`BRIEF.md`, `PLAN.md`, `film/`, `critic/r<N>/`, `NOTE.md`). Keep `film/v<N>/` before each revision round.
- Commit the editable source, `NOTE.md`, `STORYBOARD.md`, `CREDITS.md`, licensed or CC assets with attribution, and `final.mp4`. Draft renders and `critic/` scans regenerate and are gitignored.
- Copyrighted audio never goes into the repository.

## 7. Skill maintenance
- All workspace skills live canonically in `.agents/skills/<name>/SKILL.md` (Antigravity and Codex read them natively). Claude Code reads the gitignored mirror in `.claude/skills/`.
- After pulling, or after adding a skill: `.\scripts\sync-skills.ps1` (Windows) or `./scripts/sync-skills.sh` (macOS/Linux); add `-Global` / `--global` for `~/.claude/skills`. Edits to existing skills flow through the junctions; new skills need the sync.
- When a skill is added or removed, update every count together: `AGENTS.md`, `README.md`, `INSTALLATION.md`, this file, and `video-prompt-enhancer/references/catalog.md` (its Hard Rule 7 only routes to paths listed there).
