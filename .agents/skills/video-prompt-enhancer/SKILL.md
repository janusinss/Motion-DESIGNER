---
name: video-prompt-enhancer
description: Transform a user's rough video or motion-design idea into an award-level, deeply directed, copy-pasteable Prompt-Plan for any video type (launch film, ad/commercial, explainer, brand sting, social short, product demo, title sequence, music/lyric video, data story, art loop, teaser, 3D product hero). Develops a real creative concept (PAGE, three competing concepts, kill tests, device, grammar, hero moment, world, energy curve, sound arc) and then routes it to the optimal multi-skill stack across all 47 Motion-DESIGNER skills and 18 local tools. Explicitly invoke when the user asks to enhance, plan, direct, or architect a video prompt (or calls `video-prompt-enhancer`). Always interviews first with 2-4 dynamic scoping questions and outputs a standalone Markdown Prompt-Plan without auto-executing.
---

# Video Prompt Enhancer

Turn a raw, under-specified video idea into a **director's treatment plus an execution plan**: a creative concept strong enough to win awards, written so precisely that any agent (Antigravity, Codex, Claude Code) can build it shot by shot with the exact skills, tools, and QA gates in `Motion-DESIGNER`.

**Priority order: creative direction first, technical routing second.** A perfect pipeline that renders a generic film is a failed plan.

## Hard Rules (Non-Negotiable)

1. **PLAN-ONLY, NEVER AUTO-EXECUTE**: Do not scaffold projects, write animation code, download media, or render during this skill. Stop after the Prompt-Plan so the user can review, edit, or paste it into any agent.
2. **ALWAYS INTERVIEW FIRST (2-4 Dynamic Questions)**: Detect the video type, consult `references/interview-bank.md`, and ask 2-4 targeted questions about only the decisions that are missing. At least one question must be **creative** (emotion delta, the one true thing, brand voice, or concept direction), not just technical.
   - If the harness has an interactive question tool (e.g. `ask_question`), use it with `(Recommended)` on the first option.
   - Otherwise ask 2-4 numbered multiple-choice questions in Markdown, each with a bold **(Recommended)** option.
   - Never ask about anything the user already stated.
3. **CONCEPT BEFORE STACK**: Run the 10-Move Direction Engine in `references/creative-direction.md` before choosing tools. Every plan must contain: PAGE, three concepts of different kinds with kill-test results, the chosen concept triad (idea, device, grammar), logline, hero moment, system decisions, world per act, energy curve, and sound arc.
4. **TYPE-SPECIFIC DIRECTION**: Apply the matching playbook from `references/creative-direction.md` Part C (C1-C12). Its arc, proportions, winning shapes, and traps override generic defaults.
5. **AWARD BAR**: Reject anything in `references/creative-direction.md` Part B (banned props, copy tells, visual tells). No vague direction: never write "smooth", "cool effects", "nice music", "dynamic", "engaging" without a measurable spec.
6. **OPTIMAL SYNERGY, NO BLOAT**: Combine every complementary skill that genuinely elevates *this* concept (primary engine + `motion-design` craft + audio/VO/beat sync + 3D/VFX/compositing only when the concept needs it + mandatory QA gates). Never add a tool to tick a box.
7. **ZERO HALLUCINATED PATHS OR FLAGS**: Every `SKILL.md` path, script, CLI flag, and QA gate must come verbatim from `references/catalog.md` or `references/creative-direction.md`.

---

## 4-Step Workflow

### Step 1: Classify and Interview
1. Read `references/interview-bank.md`.
2. Classify the input into one primary video type (C1-C12) plus any hybrid layer (e.g. 3D product hero inside a launch film).
3. Ask 2-4 non-redundant questions (at least one creative). Wait for answers.

### Step 2: Direct the Film (Creative Direction Engine)
1. Read `references/creative-direction.md`.
2. Run Moves 1-10 in order: PAGE → Inventory → three concepts of different kinds → kill tests and scoring → concept triad + logline + idea sentence → hero moment and signature shot → system decisions → world per act → energy curve, importance budget, seams → sound arc and ending.
3. Apply the matching Part C playbook for arc, proportions, and traps.
4. When the user gave no brand or subject details, invent specific, plausible ones and mark them `[editable assumption]` instead of staying generic.

### Step 3: Route to the Optimal Skill Stack
1. Read `references/catalog.md`.
2. Lock the primary engine using the Tie-Breaker Rules; it must suit the chosen concept (e.g. a held lit-material shot → Blender; a typographic essay in brand voice → `motionmaxxing`; a structured chapters launch with house scenes → `cinetic`; a VO explainer in Chinese → `huashu-art-motion`).
3. Layer only what the concept needs:
   - **Craft**: `motion-design` for curves, choreography, and timing tables (always, when anything moves on screen).
   - **Audio/sync**: Openverse CC0 + `librosa` beat grid · `mgaudio` / `music.mjs` offline score · `whisperx` VO word timing · `cinetic` licensed track · ElevenLabs in `motionmaxxing` (needs a key).
   - **3D/VFX/compositing**: `blender-*` chain for lit hero renders · `three.quarks` + `@react-three/postprocessing` + `tweakpane` for real-time particles · `effectcraft-cli` + `ffmpeg` for native compositing and Lottie.
   - **Concept tools**: `cinetic/scripts/deck.py` to deal art directions; `motionmaxxing/scripts/precedent.py` for measured timing precedent.
   - **QA**: skill-native gates plus the universal `ffprobe` and contact-sheet gate.

### Step 4: Emit the Directed Prompt-Plan
1. Read `references/plan-template.md` (and `references/example-plan.md` for the expected depth).
2. Output **one copy-pasteable fenced Markdown block** with all 7 sections:
   0. Concept Pitch (three concepts, kill tests, pick and reason)
   1. Director's Treatment (PAGE, triad, logline, hero moment, system decisions, world per act, energy curve, sound arc, ending)
   2. Format and Specs
   3. Exact Ordered Skill Chain
   4. Shot-by-Shot Timeline (timecode, role, importance, Buys, picture, cause → action → result, motion spec, seam, sound)
   5. Step-by-Step Build Commands
   6. Mandatory QA Gates and Creative Review
3. After the block, add at most 3 lines: the strongest alternative concept in one sentence, and which `[editable assumption]` matters most.
4. Self-check before sending (all must be YES):
   - Nothing was built or executed.
   - The chosen concept passed cover-the-logo, mute, one-sentence, and specificity tests, with results written.
   - Every shot has a picture-with-text-covered, a Buys line, a motion spec with curve + duration, a seam, and a sound cue.
   - ≤ 25 % of beats are importance 3; the hero moment sits at 60-75 % of runtime; frame 0 is already in motion; the ending arrives by cause.
   - Zero banned props, copy tells, or visual tells from Part B.
   - All paths, scripts, and flags match `references/catalog.md` / `references/creative-direction.md`.
   - Manim plans use `Text`/`MarkupText` unless LaTeX + `dvisvgm` is confirmed; Remotion plans include `remotion-interactivity` and per-project `npx` scaffolding.
