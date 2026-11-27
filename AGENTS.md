# AGENTS.md

Instructions, operating rules, and skill mappings for AI agents (Codex, Antigravity, and compatible harnesses).

---

## 1. Operating Rules (ADHD Mode & Action-First Execution)

- **Lead with Action**: Place the command, file path, diff, or tool call on Line 1. Zero conversational throat-clearing, intro explanations, or restating the prompt.
- **Numbered Bounded Steps**: Break multi-step work into atomic steps. Maximum one verb/action per step. Zero compound steps (ban "and then", "afterward", "while").
- **Agent Tool Autonomy**: Inside an agent harness, execute tool calls directly rather than asking permission or instructing the user to run commands manually.
- **Concrete Time & Scale**: Never use vague qualifiers ("in a bit", "takes a while"). Ballpark in concrete units ("~10 minutes", "2 files").
- **Visible Wins**: Immediately demonstrate what works and how to verify it (e.g., test commands, curl endpoints).
- **Neutral Error Reporting**: Report strictly: **Location**, **Cause**, and **Fix**. No emotional padding.
- **Cap Lists to 5 Items**: Display at most 5 items per group in user-facing output to prevent cognitive overload.
- **3-Strike Circuit Breaker**:
  - **Strike 3 (Circuit Breaker)**: After 3 failed attempts to fix the same issue, STOP modifying code. Ask before reverting anything; never discard uncommitted work. Output strictly:
    1. **Invalid Assumption**: 1 sentence on what failed.
    2. **Diagnostic Check**: 1 concrete question or a 2-option choice (A/B) to unblock.
- **Blacklist (Zero Filler)**:
  - **Forbidden Openers**: "Sure!", "Great question", "Let me...", "I'll...", "Looking at your...", "To answer your question...", "Certainly".
  - **Forbidden Closers**: "Hope this helps!", "Let me know if you need anything else", "Happy coding!", "Feel free to ask".
  - **Forbidden Recaps**: Do not narrate what code was just written if the diff or edit already shows it.
  - **Prune on Send**: Delete hedging adverbs ("perhaps", "might", "could possibly") and idioms.

---

## 1.5 Creative Director Protocol (Every Video, Animation, or Motion Request)

The bar is award-level work (D&AD, Motion Awards, CICLOPE, Vimeo Staff Pick), not "it renders". Concept comes first; tools come second; the rendered film is judged before delivery. The executable form of this protocol is `.agents/skills/video-director/SKILL.md`; start there for any "make a video" request (preflight: `.venv\Scripts\python.exe .agents/skills/video-director/scripts/doctor.py`).

1. **Direct**: Before any build, run the 10-Move Direction Engine in `.agents/skills/video-prompt-enhancer/references/creative-direction.md` (PAGE → inventory → 3 concepts of different kinds → kill tests → engine lock + engine-ban check → idea/device/grammar → hero moment → system decisions → world per act → energy curve → sound arc). Apply the matching video-type playbook (Part C, C1–C12, plus C1b for fast-paced / hype launch cuts). If the user asked only for a plan, stop after the `video-prompt-enhancer` Prompt-Plan.
2. **Route**: Pick the primary engine from Section 2 that best serves the chosen concept (not the most familiar one), then check the concept against **that engine's own ban list** (Move 4b). Where engines disagree, the locked engine wins; never mix `cinetic` and `motionmaxxing` rules in one film.
3. **Hero first**: Build the hero moment and its hardest seam first; render stills; confirm it reads at speed before building the rest.
4. **Build & render**: Full film at target spec.
5. **Judge**: Run `motion-critic` (`scripts/critic_scan.py` + jury rubric) and the primary skill's native gate on the real render.
6. **Revise**: Apply the ranked fix list; max 3 rounds. Ship when every jury dimension is ≥ 8 and Idea + Motion Craft are ≥ 9 with zero FAIL checks; otherwise report scores honestly.
7. **Never ship** banned props, copy tells, or visual tells from `creative-direction.md` Part B.

---

## 2. Skill Activation & Disambiguation Routing Matrix

Read the matching `.agents/skills/<name>/SKILL.md` before executing any task in that domain.

| User Intent | Primary Skill / Tool | Runtime & Output | Choose Over Overlaps When |
|---|---|---|---|
| Make / create / build / render any video end to end (launch, fast-paced hype cut, ad, reel, explainer, sting, demo, titles, music, data, loop, teaser, 3D hero) | `video-director` | Orchestrator: `scripts/doctor.py` preflight → direction → one locked engine → hero first → native gates → independent `motion-critic` jury → `projects/<slug>/` delivery | Default entry for every build request; it hands off to `video-prompt-enhancer` (plan only), `motion-critic` (review only), or `reanimate` (clone) |
| Enhance/plan/architect a rough video idea into a directed multi-skill Prompt-Plan | `video-prompt-enhancer` | Plan-only (`SKILL.md` + static curated `references/`); outputs copy-pasteable Markdown Prompt-Plan | User explicitly asks to enhance, direct, or architect a video prompt before building (interviews 2–4 questions first; never auto-executes) |
| HTML-to-video with ready blocks (captions, charts, maps, transitions, kinetic type), audio mixing, Figma import, video-file recreation, proven explainer styles, live decks | `hyperframes` -> `hyperframes-cli` / `hyperframes-registry` / `media-use` / `figma` / `reverse-any-video` / `style-sampling` / `remotion-to-hyperframes` / `slideshow` | `npx hyperframes` (Node 22+, FFmpeg); seek-safe HTML compositions, Studio preview, MP4 | A registry block or the audio mixer does the hero job better than hand-building; recreating a video file (no Bun needed, unlike `reanimate`); an "episode in the style of"; porting Remotion/Manim work |
| Critique, review, judge, or iterate any rendered video toward award level | `motion-critic` | `.venv` Python + `ffmpeg`; `sheet.jpg`, `energy.png`, `critic.json` + jury verdict with timecoded fixes | After every render (engine-agnostic), or when the user asks to review/polish/"make it award-level" |
| Clone/match animation from live URL, MP4, GIF, Lottie, Rive, or WebGL/Three.js | `reanimate` | Bun + Playwright + `ffmpeg` + pixelmatch; code in target stack | Reference exists ("clone/steal/match this motion"); motion (±80ms) or pixel (≤2%) fidelity |
| UI/UX micro-interactions, component transitions, scroll/state motion spec | `motion-design` | Design craft rules (CSS, Framer Motion, GSAP, Lottie, Spring, Three.js) | Designing UI transitions or layering Disney/easing/choreography rules onto any build |
| Commercial SaaS/product launch, update ("vX is out"), UI walkthrough, logo sting | `cinetic` | Remotion 4 (default) or HyperFrames; MP4/WebM/GIF/ProRes/SRT | Structured 1–2h launch/update film using dealt house scenes, real licensed music, official logos |
| Bespoke anti-template brand promo, URL-captured launch video, kinetic type, CTA | `motionmaxxing` | Seek-safe GSAP HTML or HyperFrames + optional Three.js/ElevenLabs; HTML + MP4 | Starting from a brand URL, needing anti-slop bespoke concept, ElevenLabs VO/SFX, or plain HTML/GSAP |
| Code-drawn 2D Canvas / 3D Three.js stills, loops, drawing lessons, story films (EN) | `anidoodle` | Node + Playwright + Canvas/Three.js; PNG, MP4/GIF/WebM/APNG, offline HTML | Artistic code-drawn visuals in 32 styles, deterministic `(frame, env)`, procedural score, offline player |
| Chinese/bilingual explainers (Vox, Kurzgesagt, 3b1b, Finance) or art-history films | `huashu-art-motion` | `uv` Python + Playwright + HTML/Canvas + `ffmpeg`; 1080p@30 MP4 | Chinese/bilingual VO explainers (9 grammars, 8 parameterized), 36 art styles, AI character frames |
| Canonical 10s MG style prompt, `window.renderAt(t)` harness, Python synth audio | `resources/mg-styles-15/` | Prompt/demo pack (no `SKILL.md`); HTML/Canvas/WebGL (+Blender 04) + Python WAV | Need proven 10s style seed, jury rubric (`rubric.md`), or zero-API-key CC0 Python audio synth |
| Direct React-video engineering, Studio editing, captions, maps, `<Player>`, render | `remotion-best-practices` -> `remotion-*` | Per-project Remotion 4 (`npx`); React compositions, Studio, MP4/OTIO | Building/editing custom Remotion compositions, SaaS `<Player>`, maps, or captions directly |
| Any 3D modeling, sculpting, materials, rigging, animation, VFX, look-dev, export | `blender-core` -> `blender-workflow-recipes` -> `blender-*` | Blender 5.2.2 LTS (Live MCP or headless CLI) + mandatory `blender-asset-qa` | Any `.blend`, `bpy`, 3D prop/character/environment, turntable, or game-engine export |
| Mathematical/algorithmic animations, graphs, geometric proofs, programmatic diagrams | `.venv\Scripts\manim.exe` | Python 3.13.5 Manim Community `0.22.1`; MP4/GIF/PNG | Programmatic math/algorithmic explainers (use `Text`/`MarkupText`; no LaTeX installed) |
| Interactive real-time 3D web VFX, GPU particles, postprocessing, live tuning UI | Workspace JS stack (`package.json`) | Node ESM: `three`, `three.quarks`, `@react-three/fiber`, `@react-three/postprocessing`, `tweakpane` | Real-time interactive 3D particles/bloom/shaders in browser with live parameter controls |
| Native desktop compositing, 308 built-in effects, headless CLI/JSX/MCP, Lottie I/O | `tools/effectcraft/effectcraft-0.24.1-windows-x64-portable/effectcraft-cli.exe` | Pure-Rust EffectCraft v0.24.1 (`.ecproj` JSON, built-in encoders, no FFmpeg needed) | Fast native compositing, keyframed effect stacks, Lottie `.json`/`.lottie` import/export |
| CC-licensed stock images/audio, beat grids, word-level speech timestamps, muxing | `openverse_client.py`, `librosa`, `whisperx`, `ffmpeg` | `.venv\Scripts\python.exe` (CUDA RTX 3050) + `ffmpeg`/`ffprobe` on PATH | Sourcing CC media, audio beat/onset extraction, word-level forced alignment, transcoding/muxing |

### Tie-Breaker Rules

0. **"Make a video" of any type** -> `video-director` first; it locks one engine below. Fast-paced / hype launch -> playbook C1b (beat-locked cuts from a `librosa` grid, a designed breath before the drop) on `motionmaxxing` or `cinetic`.
1. **Existing reference to replicate** -> a video file -> `reverse-any-video`; a live site, Lottie or WebGL scene -> `reanimate` first; layer `motion-design` only for post-clone polish.
2. **UI/component motion** -> `motion-design` (apply its craft rules alongside Three.js, GSAP, CSS, or Framer Motion).
3. **Commercial promo film**: Remotion + house scene bank -> `cinetic`; brand URL scrape / ElevenLabs VO / anti-template HTML+GSAP -> `motionmaxxing`; custom React video architecture -> `remotion-best-practices`.
4. **Artistic / explainer film**: English code-drawn stills, lessons, 32 styles, offline HTML -> `anidoodle`; Chinese/bilingual VO explainers, 36 art styles, 8 parameterized YouTube/tech grammars -> `huashu-art-motion`.
5. **10s stylized MG seed, independent critic rubric, or zero-API-key synth audio** -> pull directly from `resources/mg-styles-15/`.
6. **Any 3D `.blend`/asset task** -> always enter via `blender-core` (plus `blender-workflow-recipes` for multi-stage jobs) and exit via `blender-asset-qa`.

---

## 3. Full Skill & Resource Catalog (59 Skills + 18 Resources)

All 59 workspace skills reside under `.agents/skills/<skill-name>/SKILL.md`.

### 3.1 Motion, Art, Cloning, Direction, Prompt Planning & Critique Skills (9) + Style Pack

| Skill / Resource | Entry Path | Key Local Scripts / Assets |
|---|---|---|
| `video-director` | `.agents/skills/video-director/SKILL.md` | `scripts/plan_check.py` (PLAN.md vs brief energy, hero window, beat coverage/monotony, designed breath, reference shot band; PASS/WARN/FAIL/UNVERIFIED), repo `LESSONS.md` (read at step 2, appended at delivery), `scripts/cues.py` + `references/cues.schema.json` (one clock: motionmaxxing/cinetic/anidoodle timing → engine-neutral cue sheet), `scripts/doctor.py` (cross-platform preflight: ffmpeg/libx264, Node 22+, Chrome, venv packages, Git Bash, Blender, Bun, LaTeX, EffectCraft, ElevenLabs key, skill-mirror count; `--json`) |
| `motion-critic` | `.agents/skills/motion-critic/SKILL.md` | `scripts/critic_scan.py` (contact sheet, energy curve, hero-peak %, dead spans, end hold + perceived hold, black holes, slop ratio, LUFS/dBTP, cut-onset sync; `--cues` hit/breath/hold checks, `--reference` grammar deltas; PASS/WARN/FAIL/UNVERIFIED), `references/jury-rubric.md` (8 dimensions, 4 award-lens weights, ship thresholds) |
| `video-prompt-enhancer` | `.agents/skills/video-prompt-enhancer/SKILL.md` | `references/creative-direction.md` (10-move direction engine + 12 video-type playbooks), `references/interview-bank.md`, `references/catalog.md`, `references/plan-template.md`, `references/example-plan.md` (plan-only, interview-first) |
| `reanimate` | `.agents/skills/reanimate/SKILL.md` | `scripts/capture.ts` (`--clock virtual --gl --assets`), `compare.ts`, `sheet.ts`, `easing.ts`, `gl.ts` |
| `motion-design` | `.agents/skills/motion-design/SKILL.md` | `reference/quality-checklist.md`, `reference/timing-easing-tables.md`, `reference/troubleshooting.md` |
| `cinetic` | `.agents/skills/cinetic/SKILL.md` | `scripts/precheck.mjs`, `lint-film.mjs`, `copy-check.py`, `forensics.py`, `check-sync.py`, `av-audit.py` |
| `motionmaxxing` | `.agents/skills/motionmaxxing/SKILL.md` | `scripts/brand.mjs`, `voice.py`, `sync.mjs`, `mix.py`, `render.mjs`, `look.py`, `lint.mjs` |
| `anidoodle` | `.agents/skills/anidoodle/SKILL.md` | `engine/tools/render.mjs`, `emit.mjs`, `music.mjs`, `narrate.mjs`, `gate.mjs`, `verify-export.mjs`, `ship.mjs` |
| `huashu-art-motion` | `.agents/skills/huashu-art-motion/SKILL.md` | `scripts/storyboard_lint.py`, `engine/render.py`, `qa.py`, `film_gate.py`, `subzone_gate.py`, `deliver.py` |
| `mg-styles-15` (no `SKILL.md`) | `resources/mg-styles-15/README.md` | 15 prompts/demos, `harness/render.mjs`, `harness/preview.html`, `rubric.md`, `template.md`, `lib/audio/mgaudio/` |

### 3.2 Blender 5.2+ Skills (28, Grouped by Pipeline Stage)

Path pattern: `.agents/skills/<name>/SKILL.md`. Always start with `blender-core` (or `blender-workflow-recipes`) and finish with `blender-asset-qa`.

1. **Foundation & Orchestration (4)**: `blender-core`, `blender-workflow-recipes`, `blender-scene-setup`, `blender-pipeline-automation`
2. **Modeling, Sculpting & Procedural (5)**: `blender-hardsurface-modeling`, `blender-sculpting`, `blender-retopology-uv`, `blender-geometry-nodes`, `blender-environment-kits`
3. **Materials, Texturing & Baking (4)**: `blender-pbr-materials`, `blender-texturing`, `blender-texture-baking`, `blender-stylized-npr`
4. **Characters, Rigging, Groom & Animation (5)**: `blender-character-rigging`, `blender-facial-shapekeys`, `blender-clothing`, `blender-hair-grooming`, `blender-animation`
5. **Look-Dev, Atmosphere, Physics & Rendering (6)**: `blender-lighting-lookdev`, `blender-time-of-day`, `blender-weather-fx`, `blender-simulation`, `blender-rendering`, `blender-video-editing`
6. **QA, Optimization, Export & Extensions (4)**: `blender-asset-qa`, `blender-game-optimization`, `blender-export-pipelines`, `blender-addon-development`

### 3.3 Remotion 4.0.545 Skills (13, Routed via `remotion-best-practices`)

Entry router: `.agents/skills/remotion-best-practices/SKILL.md` (also contains `./remotion-<subskill>/REFERENCE.md`; each specialist also lives at `.agents/skills/remotion-<subskill>/SKILL.md`).

| Specialist Skill | Route When |
|---|---|
| `remotion-create` | New Remotion project or new composition setup |
| `remotion-markup` | React video markup, timing/sequencing, transitions, audio/SFX, 3D, Lottie, fonts, matting |
| `remotion-interactivity` | Default whenever writing/restructuring markup so layers/timing/styles stay Studio-editable |
| `remotion-captions` | Transcribing, importing SRT, displaying and animating captions |
| `remotion-maps` | Static/animated maps, routes, markers, Mapbox/MapLibre/MapTiler/GeoJSON, 3D flyovers |
| `remotion-multimedia` | Browser multimedia via Mediabunny (trim/crop, duration/dimension metadata) |
| `remotion-studio` | Previewing via `npx remotion studio` (open Studio once project runs) |
| `remotion-render` | Exporting video, still, transparent video, or OTIO (invoke only when user explicitly asks to render/export) |
| `remotion-saas` | Remotion web apps (`<Player>`, Lambda/Vercel/Cloudflare/Express/client-side rendering) |
| `remotion-docs` | Searching current Remotion API documentation |
| `remotion-license` | Licensing FAQs, terms, purchasing |
| `remotion-upgrade` | Upgrading Remotion, Mediabunny, and Remotion Agent Skills |

**Remotion Guardrails**: Root `package.json` does not install Remotion globally (scaffold per project via `remotion-create` / `npx`); never overwrite unexpected external user edits.

### 3.3b HyperFrames Skills (9, vendored unmodified from `heygen-com/hyperframes`, Apache-2.0)

Entry: `.agents/skills/hyperframes/SKILL.md` (render contract, work loop, per-video-kind needs). Provenance and update steps: `.agents/skills/hyperframes/UPSTREAM.md`. CLI: `npx hyperframes <command>` (resolved by `hyperframes/scripts/plugin-cli.mjs`; Node 22+, FFmpeg).

| Skill | Route When |
|---|---|
| `hyperframes` | Building any HyperFrames composition (launch film, explainer, music video, charts, maps, vertical clips, title cards, captions, overlays) |
| `hyperframes-cli` | `init`, `check --json`, `timeline`, `snapshot --review`, `preview`, `render`, history and recovery |
| `hyperframes-registry` | ~450 ready blocks/components (transitions, overlays, titles, kinetic type, captions, charts, maps, 3D, camera moves); search before hand-building any named visual, in any engine |
| `media-use` | Music, SFX, images, icons, logos, VO, transcripts, cutouts, grades and placed-audio mixing (HeyGen generation needs sign-in and credits: ask first; free local tools need none) |
| `figma` | A Figma design, frame, logo or brand brought into a video |
| `reverse-any-video` | Rebuild a video file as an editable project, checked frame by frame against the original |
| `style-sampling` | A new episode in a proven style (Collage, Finance, Animated Science, 3D Brand, 3D True Crime explainers) |
| `remotion-to-hyperframes` | Port Remotion, Motion Canvas, Lottie, Three.js, p5.js, canvas or Manim/AE/Blender renders, verified frame by frame |
| `slideshow` | A live deck with presenter mode (`hyperframes present`), not a rendered video |

### 3.4 Complete 18-Resource Workspace Map

- **Agent Skills (9 upstream packs + 3 local skills / 59 skills)**: #1 `reanimate`, #2 `motion-design`, #4 `huashu-art-motion`, #5 `anidoodle`, #6 `cinetic`, #7 `motionmaxxing`, #9 `blender-skills` (28), #17 `remotion-dev/skills` (13), `heygen-com/hyperframes` (9), + local `video-director`, `video-prompt-enhancer` and `motion-critic` -> `.agents/skills/`
- **Local modifications to upstream packs**: `motionmaxxing/scripts/_cdp.mjs` `findChrome()` also checks the standard Windows Chrome paths (additive; re-apply after updating motionmaxxing from upstream).
  Also additive: `motionmaxxing/scripts/lint.mjs` rule K1 flags two keys on the same frame in one `M.kf` list (FAIL on transform props, which are not seek-safe; fix with `[f,v],[f+1,v]`), and `mg-styles-15` mgaudio `Mix.export(..., for_aac=True)` caps true peak at -2.5 dBTP because AAC adds about 1.2 dB (default unchanged).
- **HyperFrames pack**: vendored unmodified (Section 3.3b); also reachable as `cinetic`'s HTML runtime (`new-film.sh --engine hyperframes`). User-global HyperFrames installs never override this file's routing.
- **Prompt & Demo Pack (1)**: #3 `mg-styles-15` -> `resources/mg-styles-15/`
- **Python Stack (3)**: #8 `manim`, #15 `librosa`, #16 `whisperx` -> `.venv/`, `pyproject.toml`, `requirements.txt`, `uv.lock`
- **JS/TS 3D Stack (3)**: #10 `three.quarks`, #11 `@react-three/postprocessing`, #12 `tweakpane` -> `package.json`, `package-lock.json`, `node_modules/`
- **Native Tools & Media API (3)**: #13 `effectcraft` -> `tools/effectcraft/effectcraft-0.24.1-windows-x64-portable/`, #14 Openverse client -> `tools/openverse/openverse_client.py`, #18 `ffmpeg`/`ffprobe` -> system PATH

---

## 4. High-Leverage Multi-Tool Pipelines (Synergies)

1. **Audio-Driven, Beat-Synced & Captioned Video**:
   - Step 1: Fetch CC0/CC audio/images via `.venv\Scripts\python.exe tools/openverse/openverse_client.py` (verify `license` and `attribution`).
   - Step 2: Extract beat/onset timestamps via `.venv\Scripts\python.exe` (`librosa 1.0.1`).
   - Step 3: Generate word-level timestamps on GPU via `.venv\Scripts\whisperx.exe` (`torch 2.8.0+cu128`, CUDA RTX 3050).
   - Step 4: Drive picture timing in `cinetic`, `remotion-captions` + `remotion-markup`, `motionmaxxing` (`scripts/sync.mjs`), `anidoodle` (`engine/tools/narrate.mjs`), `huashu-art-motion` (`scripts/engine/render.py --spec`), or `.venv\Scripts\manim.exe`.
   - Step 5: Mux and validate via `ffmpeg`/`ffprobe` plus cross-engine QA (`.agents/skills/motionmaxxing/scripts/look.py`).
2. **Zero-API-Key Deterministic Audio & SFX Fallback**:
   - Step 1: Synthesize -14 LUFS / ≤-1.1 dBTP tracks and synced SFX via `resources/mg-styles-15/lib/audio/mgaudio/` (103 CC0 VCSL samples, `master.py`, `qc.py`) or `.agents/skills/anidoodle/engine/tools/music.mjs`.
   - Step 2: Mux audio into any rendered MP4 with `ffmpeg` and confirm peak/loudness.
3. **Reference Cloning -> Production Polish**:
   - Step 1: Capture and measure target timing/easing/shaders via `.agents/skills/reanimate/scripts/capture.ts`, `easing.ts`, and `gl.ts`.
   - Step 2: Verify frame parity via `compare.ts` and `sheet.ts`.
   - Step 3: Refine easing, personality, and accessibility for the target codebase via `.agents/skills/motion-design/reference/timing-easing-tables.md` and `quality-checklist.md`.
4. **Interactive 3D Web VFX & Live Tuning**:
   - Step 1: Build real-time particle/bloom scenes with workspace ESM packages (`three`, `three.quarks`, `@react-three/fiber`, `@react-three/postprocessing`).
   - Step 2: Expose live sliders/presets via `tweakpane`.
   - Step 3: Apply weight/timing craft from `motion-design`; verify deterministic frames via `reanimate` (`capture.ts --clock virtual --gl`) when matching a reference.
5. **3D Asset, Scene & Hybrid 3D+2D Motion Pipeline**:
   - Step 1: Route via `blender-core` and `blender-workflow-recipes` to specialist `blender-*` skills.
   - Step 2: Run `.agents/skills/blender-asset-qa/scripts/qa_check.py` and `review_shots.py` until zero errors.
   - Step 3: Export via `blender-export-pipelines`, or composite rendered 3D passes with 2D kinetic type/UI overlays in HTML/GSAP, Remotion, or `ffmpeg` (reference pattern: `resources/mg-styles-15/demos/04-3d-render`).
6. **Native Desktop Compositing & Lottie Automation**:
   - Step 1: Drive `.ecproj` projects, 308 native effects, JSX scripts, or Lottie `.json`/`.lottie` I/O via `tools/effectcraft/effectcraft-0.24.1-windows-x64-portable/effectcraft-cli.exe`.
   - Step 2: Render frames/video directly with built-in encoders (`render-frame` / `render`) or run `mcp` mode.
   - Step 3: Verify output with `ffprobe` and visual sheet inspection (`.agents/skills/motionmaxxing/scripts/look.py`).

---

## 5. Local Runtime & Tool Invocation Cheatsheet (Windows)

### Python Stack (`.venv/`, `pyproject.toml`, `requirements.txt`, `uv.lock`)
- **Interpreter**: `.venv\Scripts\python.exe` (Python `3.13.5`, `requires-python >=3.12,<3.14`; `uv 0.13.1` on PATH).
- **Installed Packages**: `manim 0.22.1`, `librosa 1.0.1`, `whisperx 3.8.6`, `torch 2.8.0+cu128` (`torchaudio~=2.8.0`, `torchvision~=0.23.0` via `pytorch-cu128`), plus the engines' audio/QA/logo packages: `pyloudnorm` (loudness gates, `mgaudio qc.py`), `pedalboard` (mgaudio mix bus), `opencv-python-headless` (`cv2`, cinetic forensics), `brotli` + `uharfbuzz` (cinetic outlined logos).
- **Windows**: `python3` resolves to the Microsoft Store stub, so run every skill's `python3 x.py` as `.venv\Scripts\python.exe x.py`. `bash` on PATH is WSL, so run `.sh` scripts with `"C:\Program Files\Git\bin\bash.exe"`. Run `doctor.py` to confirm.
- **GPU**: CUDA enabled (`torch.cuda.is_available() == True`, `NVIDIA GeForce RTX 3050 Laptop GPU`).
- **CLI Binaries**: `.venv\Scripts\manim.exe`, `.venv\Scripts\manimce.exe`, `.venv\Scripts\whisperx.exe`.
- **Manim LaTeX Caveat**: `latex`, `pdflatex`, `xelatex`, and `dvisvgm` are NOT installed on PATH. Use `Text` / `MarkupText` for Manim scenes; `Tex` / `MathTex` require installing MiKTeX or TeX Live + `dvisvgm`.

### JS/TS 3D Stack (`package.json`, `package-lock.json`, `node_modules/`)
- **Runtime**: `"type": "module"`, `node v22.21.0`, `npm 11.11.1`, `npx` on PATH.
- **Dependencies**: `three ^0.187.0`, `three.quarks ^0.18.0`, `@react-three/fiber ^9.8.2`, `@react-three/postprocessing ^3.2.2`, `postprocessing ^6.39.6`, `react ^19.3.1`, `react-dom ^19.3.1`, `tweakpane ^4.0.5`.
- **DevDependencies**: `@types/three ^0.187.0`, `@types/react ^19.3.0`, `@types/react-dom ^19.3.0`.
- **Verification**: `npm ls --depth=0`.

### Blender 5.2.2 LTS (`blender` on PATH)
- **Install Path**: `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe`.
- **Live MCP First Call**: Run `.agents/skills/blender-core/scripts/env_report.py` via `blender-mcp` `execute_blender_code`.
- **Headless CLI**: `.venv\Scripts\python.exe .agents/skills/blender-core/scripts/run_in_blender.py [--blend FILE] [--user-prefs] <script.py> [-- <args>]` (supports `--expr "..."`, `--which`; emits `@@JSON@@`). Raw fallback: `blender -b in.blend --factory-startup --python-exit-code 1 -P script.py -- args`.
- **Windows Path Note**: In Git Bash, prefix `MSYS_NO_PATHCONV=1` for `//` Blender relative paths (or run in PowerShell).
- **Mandatory 5.x API Rules**: Prefer data API (`bpy.data`/`bmesh`/`foreach_get`) over `bpy.ops` (use `bpy.context.temp_override(...)` if needed); look up nodes by `type`, not localized `name`; engines `BLENDER_EEVEE` (not `BLENDER_EEVEE_NEXT`), `CYCLES`, `BLENDER_WORKBENCH`; channelbags (not `action.fcurves`); `scene.compositing_node_group` (not `scene.node_tree`); Boolean `FLOAT` (not `FAST`); `gpu.init()` in background (no `bgl`); `1 unit = 1m`; apply transforms before modifiers/rigging/baking/export.

### EffectCraft Alpha v0.24.1 (`tools/effectcraft/effectcraft-0.24.1-windows-x64-portable/`)
- **Binaries**: `tools/effectcraft/effectcraft-0.24.1-windows-x64-portable/effectcraft-cli.exe` (CLI/MCP) and `tools/effectcraft/effectcraft-0.24.1-windows-x64-portable/effectcraft.exe` (GUI); checksums in `tools/effectcraft/SHA256SUMS.txt`.
- **Verified Subcommands**: `info`, `commands`, `exec`, `run` (`--args-file`, `--commands`), `props`, `get`, `set`, `render-frame`, `render` (`h264|hevc|av1|prores|webm|png|jpeg|tiff|exr|tga|gif|wav|aiff`, `--template`), `bench`, `script` (`.jsx` / `--eval`), `replay`, `mcp` (`--autosave` | `--bridge PORT`).
- **Common Flags**: `--project F.ecproj | --demo | --empty`, `--save`, `--save-as F`, `--json`, `--gpu`.

### Openverse Media Client (`tools/openverse/openverse_client.py`)
- **Docs**: `tools/openverse/README.md` (stdlib-only Openverse API v1 client).
- **Commands**:
  - Health check: `.venv\Scripts\python.exe tools/openverse/openverse_client.py --check --limit 1`
  - Search: `.venv\Scripts\python.exe tools/openverse/openverse_client.py --type {images,audio} -q "<query>" [-n 5] [--license cc0|by|by-sa] [--json]`
- **Rule**: Always inspect and preserve `license` and `attribution` fields before using downloaded assets.

### System Binaries on PATH
- `ffmpeg` & `ffprobe` (`9.0.2-full_build-www.gyan.dev`), `blender` (`5.2.2 LTS`), `node` (`v22.21.0`), `npm` (`11.11.1`), `npx`, `uv` (`0.13.1`).

---

## 6. Mandatory Quality & Verification Gates

**Preflight**: run `.agents/skills/video-director/scripts/doctor.py` with the venv Python before a build; route only to engines it reports ready.

**Universal Gate**: Never self-certify visual motion, video, or 3D output from source code alone. Render real frames/media and run both automated metrics and visual contact-sheet inspection before marking any task done. **Every video also passes the `motion-critic` jury** (`.venv\Scripts\python.exe .agents/skills/motion-critic/scripts/critic_scan.py <film.mp4> --out <dir>/critic --expect <s> [--hero <s>]` + `references/jury-rubric.md`): ship at every dimension ≥ 8, Idea + Motion Craft ≥ 9, zero FAIL checks; max 3 revision rounds.

| Domain / Skill | Required Pre-Delivery Gate | Pass Condition |
|---|---|---|
| **Blender (`blender-asset-qa`)** | `.agents/skills/blender-asset-qa/scripts/qa_check.py -- --objects <objs> --profile game\|render\|print\|roblox` + visual sheet via `.agents/skills/blender-asset-qa/scripts/review_shots.py` (or live MCP `look(mode="angles")`) | `"pass": true` (0 errors; warnings fixed/justified), inspected PNG contact sheet, hard numbers reported (tris, object/material counts, `ob.dimensions`, non-zero files) |
| **`motionmaxxing`** | `.agents/skills/motionmaxxing/scripts/look.py` + `.agents/skills/motionmaxxing/scripts/lint.mjs` + eye check on generated `look/sheet.jpg` logged in `NOTE.md` | G0 (render/length/audio), G2 (≤3 flat frames), G3 (end hold ≤1.4s & final shot ≤25%), G5 (`lint.mjs` exit 0, no slop/HUD/chrome), G1/G4 verified by eye |
| **`cinetic`** | `.agents/skills/cinetic/scripts/precheck.mjs`, `lint-film.mjs`, `copy-check.py`, `forensics.py`, `check-sync.py`, `av-audit.py` | Zero linear-motion/slop/copy/seam/empty-frame/A-V sync failures |
| **`anidoodle`** | `.agents/skills/anidoodle/engine/tools/gate.mjs`, `verify-export.mjs`, `ship.mjs` | Pure `(frame, env)` determinism, zero dead air, A/V sync & true peak pass, `ship.mjs` unified check green (blind check fails) |
| **`huashu-art-motion`** | `.agents/skills/huashu-art-motion/scripts/storyboard_lint.py` (pre-code), `engine/render.py --spec ... --audit`, `qa.py`, `film_gate.py`, `subzone_gate.py`, `deliver.py` | Storyboard passes before coding; fast-motion ratio ≥0.035, no ≥0.3s blank/flat spans, ≤30% blue-purple slop frames, subtitle safe-zone clear, fingerprinted delivery note |
| **HyperFrames (`hyperframes`)** | `npx hyperframes check --json` + `npx hyperframes snapshot --review` (→ `REVIEW.md`, `references/review.md`); `reverse-any-video` / `remotion-to-hyperframes` frame-by-frame comparison | Zero `check` errors, every warning weighed, review sheet inspected; reconstructions match the original frame by frame |
| **`reanimate`** | `.agents/skills/reanimate/scripts/compare.ts`, `sheet.ts`, `easing.ts`, `gl.ts` | Side-by-side proof sheet inspected; timing within ±80ms (motion-faithful) or pixel diff ≤2% (pixel-faithful) |
| **`motion-design`** | `.agents/skills/motion-design/reference/quality-checklist.md` | Zero linear spatial motion, zero opacity-only state changes, 1/3 choreography compliance, 3 motion layers |
| **`remotion-*`** | `remotion-interactivity` on markup, `remotion-studio` preview, `remotion-render` only on explicit export request | Studio-editable structure, clean preview, zero unrequested renders or overwritten external edits |
| **Any MP4 / Cross-Engine (`mg-styles-15`, Manim, EffectCraft, FFmpeg)** | `ffprobe -v error -show_format -show_streams <file>` + `.agents/skills/motionmaxxing/scripts/look.py` or `.agents/skills/huashu-art-motion/scripts/film_gate.py` + `resources/mg-styles-15/lib/audio/mgaudio/qc.py` / `resources/mg-styles-15/rubric.md` | Valid non-zero video/audio streams, expected fps/duration/resolution, target audio loudness (-14 LUFS, ≤-1.1 dBTP), contact sheet visually verified |
