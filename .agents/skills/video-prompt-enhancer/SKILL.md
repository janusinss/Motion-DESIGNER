---
name: video-prompt-enhancer
description: Transform a user's rough video or motion-design idea into a deeply directed, copy-pasteable execution Prompt-Plan utilizing the optimal multi-skill synergy stack across all 47 Motion-DESIGNER skills and 18 local tools. Explicitly invoke when the user asks to enhance, plan, direct, or architect a video prompt (or calls `video-prompt-enhancer`). Always interviews first with 2–4 dynamic scoping questions and outputs a standalone Markdown Prompt-Plan without auto-executing.
---

# Video Prompt Enhancer

Turn raw, under-specified video ideas into **production-grade, agent-ready Markdown Prompt-Plans** that orchestrate the exact skills, local runtimes, audio/beat pipelines, shot choreography, and mandatory QA gates in `Motion-DESIGNER`.

## Hard Rules (Non-Negotiable)

1. **PLAN-ONLY — NEVER AUTO-EXECUTE**: Do NOT create video projects, write animation code, download media, or render files during this skill. Stop after outputting the enhanced Prompt-Plan so the user can review, tweak, or paste it into any agent (Antigravity, Codex, Claude Code).
2. **ALWAYS INTERVIEW FIRST (2–4 Dynamic Questions)**: Never skip straight to the plan. Detect the video archetype from the user's raw input, consult `references/interview-bank.md`, and ask **2 to 4** targeted scoping questions covering only critical missing decisions.
   - If the harness provides an interactive question tool (e.g., `ask_question`), use it with `(Recommended)` on the first option.
   - Otherwise, ask 2–4 concise numbered multiple-choice questions in plain Markdown with a bold **(Recommended)** option per question.
   - Never ask about details the user already stated in their raw prompt.
3. **OPTIMAL MULTI-SKILL SYNERGY (NO BLOAT)**: Consult `references/catalog.md` and combine every complementary skill/tool that genuinely elevates the video (primary renderer + `motion-design` craft + audio/VO/beat sync + 3D/VFX/compositing only when fitting + mandatory QA gates). Never force irrelevant stacks into a plan just to check boxes.
4. **ZERO HALLUCINATED PATHS OR FLAGS**: Every `SKILL.md` path, script path, CLI binary, and QA gate in the outputted Prompt-Plan MUST come verbatim from `references/catalog.md`.
5. **CONCRETE DIRECTORIAL PRECISION**: Ban vague phrases ("make it smooth", "cool effects", "nice music", "good pacing"). Specify exact duration, resolution, fps, aspect ratio, easing/motion personality, timecoded beat cuts, loudness (`-14 LUFS`, `≤-1.1 dBTP`), and numeric QA pass thresholds.

---

## 3-Step Execution Workflow

### Step 1 — Classify & Interview Dynamically
1. Read `references/interview-bank.md`.
2. Classify the user's raw input into 1 primary archetype (plus any secondary hybrid layer, e.g., Blender 3D + Remotion 2D overlay):
   - Commercial Launch / Product Promo (`cinetic` vs `motionmaxxing` vs `remotion-*`)
   - Reference Clone / Motion Match (`reanimate` + `motion-design`)
   - Code-Drawn Art / Story / Style Film (`anidoodle` or `resources/mg-styles-15/`)
   - Chinese / Bilingual Explainer (`huashu-art-motion`)
   - Math / Algorithmic Explainer (`manim`)
   - Interactive 3D Web VFX (`three.quarks` + `@react-three/postprocessing` + `tweakpane`)
   - 3D Asset / Scene / Hybrid 3D+2D (`blender-core` → `blender-workflow-recipes` → `blender-*`)
   - Native Compositing / Lottie Pipeline (`effectcraft-cli` + `ffmpeg`)
3. Ask **2–4** dynamic, non-redundant scoping questions tailored to that archetype (skipping anything already given) and wait for the user's answers.

### Step 2 — Assemble Optimal Multi-Skill Synergy Stack
1. Read `references/catalog.md`.
2. Lock the **Primary Engine Skill / Runtime** using the Tie-Breaker Rules in `references/catalog.md`.
3. Layer complementary skills & local tools only where they add concrete craft:
   - **Motion Craft Layer**: Always layer `motion-design` for easing curves, choreography (1/3 rule), timing tables, and zero-linear-motion discipline when UI/camera/component motion is involved.
   - **Audio / Beat / Speech Layer**: Choose the exact audio source matching the user's answer:
     - Stock CC0/CC music or SFX → `tools/openverse/openverse_client.py` + `librosa` beat/onset grid
     - Zero-API-key deterministic offline synth → `resources/mg-styles-15/lib/audio/mgaudio/` or `.agents/skills/anidoodle/engine/tools/music.mjs`
     - Spoken voiceover / synced captions → `whisperx` (CUDA) word timestamps → `remotion-captions` / `motionmaxxing` (`scripts/sync.mjs`) / `anidoodle` (`narrate.mjs`) / `huashu-art-motion` (`render.py --spec`)
     - Commercial licensed human music → `cinetic` licensed-track workflow (generated music disallowed in `cinetic`)
   - **3D / VFX / Compositing Layer** (only when fitting):
     - Hero 3D passes / product renders → `blender-core` → `blender-workflow-recipes` → specialist `blender-*` → `blender-asset-qa`
     - Real-time GPU particles / bloom / live controls → `three` + `three.quarks` + `@react-three/fiber` + `@react-three/postprocessing` + `tweakpane`
     - Fast native compositing / Lottie `.json`/`.lottie` I/O → `effectcraft-cli` + `ffmpeg`
   - **Mandatory QA Gate Layer**: Attach the exact skill-native verification scripts + universal `ffprobe` & visual contact-sheet inspection gate from `references/catalog.md`.

### Step 3 — Emit the Directed Markdown Prompt-Plan
1. Read `references/plan-template.md`.
2. Output **one single copy-pasteable Markdown code block** (` ```markdown ... ``` `) containing all 5 required sections:
   1. **Creative Direction & Specs**
   2. **Exact Ordered Skill Chain** (exact `.agents/skills/<name>/SKILL.md` paths)
   3. **Shot / Beat Timeline** (timecoded beats, visuals, motion/easing, audio/SFX, captions)
   4. **Step-by-Step Build Commands** (concrete verified local commands)
   5. **Mandatory QA Gates & Pass Criteria** (automated scripts + contact-sheet eye check + hard thresholds)
3. Self-check before sending:
   - Did you avoid executing/building anything? (Must be YES.)
   - Are all paths/scripts/flags verified against `references/catalog.md`? (Must be YES.)
   - Are all placeholders replaced with concrete numbers, timings, and commands tailored to the user's answers? (Must be YES.)
   - If Manim is selected, did you explicitly instruct `Text`/`MarkupText` (not `Tex`/`MathTex`) unless LaTeX + `dvisvgm` is installed? (Must be YES.)
   - If Remotion is selected, did you include `remotion-interactivity` and remind the agent to scaffold per-project via `npx` (never global root install)? (Must be YES.)
