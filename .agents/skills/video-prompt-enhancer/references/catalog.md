# Motion-DESIGNER Static Curated Catalog (47 Sibling Skills + 18 Resources)

Source of truth for `video-prompt-enhancer`. Every skill path, script, binary, and QA gate below is verified on disk in `Motion-DESIGNER`. Never cite anything outside this catalog unless the user explicitly supplies a custom local file.

---

## 1. Disambiguation & Tie-Breaker Rules

| User Intent | Primary Skill / Tool | Exact Entry Path | Runtime & Output |
|---|---|---|---|
| Clone/match animation from live URL, MP4, GIF, Lottie, Rive, WebGL/Three.js | `reanimate` | `.agents/skills/reanimate/SKILL.md` | Bun + Playwright + `ffmpeg` + pixelmatch; code in target stack |
| UI/UX micro-interactions, easing curves, choreography, motion craft layer | `motion-design` | `.agents/skills/motion-design/SKILL.md` | Craft rules (CSS, Framer Motion, GSAP, Lottie, Spring, Three.js) |
| Structured SaaS/product launch, update ("vX is out"), UI walkthrough, logo sting | `cinetic` | `.agents/skills/cinetic/SKILL.md` | Remotion 4 (default) or HyperFrames; MP4/WebM/GIF/ProRes/SRT |
| Bespoke anti-template brand promo, URL-captured film, kinetic type, CTA | `motionmaxxing` | `.agents/skills/motionmaxxing/SKILL.md` | Seek-safe GSAP HTML or HyperFrames + optional Three.js/ElevenLabs; HTML + MP4 |
| Code-drawn 2D Canvas / 3D Three.js stills, loops, lessons, story films (32 styles) | `anidoodle` | `.agents/skills/anidoodle/SKILL.md` | Node + Playwright + Canvas/Three.js; PNG, MP4/GIF/WebM/APNG, offline HTML |
| Chinese/bilingual explainers (9 grammars, 8 parameterized) or 36 art-style films | `huashu-art-motion` | `.agents/skills/huashu-art-motion/SKILL.md` | `uv` Python + Playwright + HTML/Canvas + `ffmpeg`; 1080p@30 MP4 |
| Canonical 10s MG style seed, `window.renderAt(t)` harness, CC0 Python audio synth | `mg-styles-15` *(pack)* | `resources/mg-styles-15/README.md` | HTML/Canvas/WebGL (+Blender `04`) + Python WAV (`-14 LUFS`) |
| Direct React-video engineering, Studio interactivity, captions, maps, `<Player>` | `remotion-best-practices` | `.agents/skills/remotion-best-practices/SKILL.md` | Per-project Remotion 4 (`npx`); React compositions, Studio, MP4/OTIO |
| Any 3D modeling, sculpting, materials, rigging, animation, VFX, look-dev, export | `blender-core` + `blender-workflow-recipes` | `.agents/skills/blender-core/SKILL.md` | Blender `5.2.2 LTS` (Live MCP or headless CLI) + mandatory `blender-asset-qa` |
| Mathematical/algorithmic animations, graphs, geometric proofs | `manim` *(Python)* | `.venv\Scripts\manim.exe` / `.venv/bin/manim` | Python `3.13.5` Manim Community `0.22.1`; MP4/GIF/PNG |
| Real-time 3D web VFX, GPU particles, postprocessing, live tuning UI | Workspace JS stack | `package.json` | Node ESM: `three`, `three.quarks`, `@react-three/fiber`, `@react-three/postprocessing`, `tweakpane` |
| Native desktop compositing, 308 built-in effects, JSX/CLI/MCP, Lottie I/O | `effectcraft-cli` | `tools/effectcraft/effectcraft-0.24.1-windows-x64-portable/effectcraft-cli.exe` | Pure-Rust EffectCraft `v0.24.1` (`.ecproj` JSON, built-in encoders) |
| CC-licensed media, beat grids, word-level speech timestamps, muxing | `openverse` + `librosa` + `whisperx` + `ffmpeg` | `tools/openverse/openverse_client.py` + `.venv` + `PATH` | Python `.venv` (CUDA RTX 3050) + `ffmpeg`/`ffprobe` |

### Tie-Breakers
1. **Existing reference to match** → `reanimate` first; layer `motion-design` only for post-clone polish.
2. **UI/component motion or easing discipline** → layer `motion-design` alongside any web/Remotion/Three.js/GSAP build.
3. **Commercial launch/promo** → Remotion + dealt house scenes + real licensed music → `cinetic`; URL brand capture / anti-template bespoke HTML+GSAP / ElevenLabs → `motionmaxxing`; custom React video architecture → `remotion-best-practices`.
4. **Artistic / explainer film** → English code-drawn 32 styles / drawing lessons / offline player → `anidoodle`; Chinese/bilingual VO explainers (Vox/Kurzgesagt/3b1b/Finance/Whiteboard) / 36 art styles → `huashu-art-motion`.
5. **10s stylized MG seed, critic rubric, or zero-API-key synth audio** → `resources/mg-styles-15/` (`lib/audio/mgaudio/`).
6. **Any 3D `.blend`/asset task** → enter via `blender-core` (plus `blender-workflow-recipes` for multi-stage jobs) and ALWAYS exit via `blender-asset-qa`.

---

## 2. All 47 Sibling Skills (Exact Paths)

### 2.1 Motion, Art & Cloning (6 Skills + 1 Resource Pack)
- `.agents/skills/reanimate/SKILL.md` — scripts: `scripts/capture.ts` (`--clock virtual --gl --assets`), `scripts/compare.ts`, `scripts/sheet.ts`, `scripts/easing.ts`, `scripts/gl.ts`
- `.agents/skills/motion-design/SKILL.md` — refs: `reference/quality-checklist.md`, `reference/timing-easing-tables.md`, `reference/troubleshooting.md`
- `.agents/skills/cinetic/SKILL.md` — scripts: `scripts/precheck.mjs`, `scripts/lint-film.mjs`, `scripts/copy-check.py`, `scripts/forensics.py`, `scripts/check-sync.py`, `scripts/av-audit.py`
- `.agents/skills/motionmaxxing/SKILL.md` — scripts: `scripts/brand.mjs`, `scripts/voice.py`, `scripts/sync.mjs`, `scripts/mix.py`, `scripts/render.mjs`, `scripts/look.py`, `scripts/lint.mjs`
- `.agents/skills/anidoodle/SKILL.md` — tools: `engine/tools/render.mjs`, `engine/tools/emit.mjs`, `engine/tools/music.mjs`, `engine/tools/narrate.mjs`, `engine/tools/gate.mjs`, `engine/tools/verify-export.mjs`, `engine/tools/ship.mjs`
- `.agents/skills/huashu-art-motion/SKILL.md` — scripts: `scripts/storyboard_lint.py`, `scripts/engine/render.py`, `scripts/qa.py`, `scripts/film_gate.py`, `scripts/subzone_gate.py`, `scripts/deliver.py`
- `resources/mg-styles-15/README.md` *(no `SKILL.md`)* — 15 prompts/demos (`01-flat-vector`, `02-line-art`, `03-isometric`, `04-3d-render`, `05-cel-boil`, `06-collage`, `07-liquid`, `08-morph`, `09-bauhaus`, `10-synthwave`, `12-aurora-glass`, `18-hanazi`, `19-paperclip`, `20-pixel`, `22-hud`), `harness/render.mjs`, `harness/preview.html`, `rubric.md`, `template.md`, `lib/audio/mgaudio/` (`master.py`, `qc.py`)

### 2.2 Blender 5.2+ Skills (28 Skills — `.agents/skills/<name>/SKILL.md`)
1. **Foundation & Orchestration (4)**: `blender-core`, `blender-workflow-recipes`, `blender-scene-setup`, `blender-pipeline-automation`
2. **Modeling, Sculpting & Procedural (5)**: `blender-hardsurface-modeling`, `blender-sculpting`, `blender-retopology-uv`, `blender-geometry-nodes`, `blender-environment-kits`
3. **Materials, Texturing & Baking (4)**: `blender-pbr-materials`, `blender-texturing`, `blender-texture-baking`, `blender-stylized-npr`
4. **Characters, Rigging, Groom & Animation (5)**: `blender-character-rigging`, `blender-facial-shapekeys`, `blender-clothing`, `blender-hair-grooming`, `blender-animation`
5. **Look-Dev, Atmosphere, Physics & Rendering (6)**: `blender-lighting-lookdev`, `blender-time-of-day`, `blender-weather-fx`, `blender-simulation`, `blender-rendering`, `blender-video-editing`
6. **QA, Optimization, Export & Extensions (4)**: `blender-asset-qa`, `blender-game-optimization`, `blender-export-pipelines`, `blender-addon-development`

Key Blender scripts:
- `.agents/skills/blender-core/scripts/env_report.py` (live MCP first call)
- `.agents/skills/blender-core/scripts/run_in_blender.py` (headless CLI runner)
- `.agents/skills/blender-asset-qa/scripts/qa_check.py` (automated QA gate)
- `.agents/skills/blender-asset-qa/scripts/review_shots.py` (multi-angle contact sheet)

### 2.3 Remotion 4 Skills (13 Skills — `.agents/skills/<name>/SKILL.md`)
Entry router: `.agents/skills/remotion-best-practices/SKILL.md`
Specialists: `remotion-create`, `remotion-markup`, `remotion-interactivity` *(always pair with markup)*, `remotion-captions`, `remotion-maps`, `remotion-multimedia`, `remotion-studio`, `remotion-render` *(only when explicit export is requested)*, `remotion-saas`, `remotion-docs`, `remotion-license`, `remotion-upgrade`.
Guardrail: Root `package.json` does NOT install Remotion globally; scaffold per-project via `npx create-video@latest`.

---

## 3. Verified Local Runtimes & Commands (Windows Default + POSIX Equivalent)

- **Python `.venv`** (Python `3.13.5`, `manim 0.22.1`, `librosa 1.0.1`, `whisperx 3.8.6`, `torch 2.8.0+cu128`, CUDA RTX 3050):
  - Windows: `.venv\Scripts\python.exe`, `.venv\Scripts\manim.exe`, `.venv\Scripts\whisperx.exe`
  - macOS/Linux: `.venv/bin/python`, `.venv/bin/manim`, `.venv/bin/whisperx`
  - **Manim LaTeX Caveat**: `latex`/`dvisvgm` is NOT installed on PATH by default. Always direct Manim scenes to use `Text`/`MarkupText` unless the user confirmed LaTeX is installed.
- **Openverse CC Media Client** (zero pip deps):
  - Health: `.venv\Scripts\python.exe tools/openverse/openverse_client.py --check --limit 1`
  - Search: `.venv\Scripts\python.exe tools/openverse/openverse_client.py --type {images,audio} -q "<query>" -n 5 --license cc0 --json`
  - Rule: Always record `license` and `attribution` for downloaded assets.
- **JS/TS 3D Stack** (`package.json`, `"type": "module"`, Node `v22+`):
  - Packages: `three`, `three.quarks`, `@react-three/fiber`, `@react-three/postprocessing`, `postprocessing`, `react`, `react-dom`, `tweakpane`, `@types/*`
  - Verify: `npm ls --depth=0`
- **Blender 5.2+ LTS** (`blender` on PATH):
  - Headless: `.venv\Scripts\python.exe .agents/skills/blender-core/scripts/run_in_blender.py [--blend FILE] <script.py> [-- <args>]`
  - 5.x Rules: Data API (`bpy.data`/`bmesh`/`foreach_get`) over `bpy.ops`; lookup nodes by `type` not localized `name`; `BLENDER_EEVEE` (not `BLENDER_EEVEE_NEXT`), `CYCLES`; channelbags (not `action.fcurves`); `scene.compositing_node_group` (not `scene.node_tree`); Boolean `FLOAT` (not `FAST`); `1 unit = 1m`; apply transforms before modifiers/rigging/baking/export.
- **EffectCraft `v0.24.1`** (local portable binary; gitignored — see `INSTALLATION.md` if missing):
  - Windows CLI: `tools/effectcraft/effectcraft-0.24.1-windows-x64-portable/effectcraft-cli.exe`
  - Subcommands: `info`, `commands`, `exec`, `run`, `props`, `get`, `set`, `render-frame`, `render` (`h264|hevc|av1|prores|webm|png|jpeg|tiff|exr|tga|gif|wav|aiff`), `script` (`.jsx`/`--eval`), `mcp`
- **FFmpeg / FFprobe** (`ffmpeg`, `ffprobe` on PATH):
  - Stream inspect: `ffprobe -v error -show_format -show_streams <file.mp4>`

---

## 3b. Creative Direction References & Concept Tools (verified on disk)

Cite these in Section 3 of a plan when the concept needs depth (see `creative-direction.md`):

| Need | Path |
|---|---|
| PAGE, brand inventory, film kinds, metaphor bank, copy voice | `.agents/skills/motionmaxxing/references/idea.md` |
| Beat roles, "Buys" lines, system decisions, seams, energy curve, storyboard worksheet | `.agents/skills/motionmaxxing/references/director.md` |
| Ground, light, depth, texture, hero-moment toolbox | `.agents/skills/motionmaxxing/references/world.md` |
| Typography in motion / endings / UI demos | `.agents/skills/motionmaxxing/references/type.md`, `close.md`, `ui-demo.md` |
| VO-led timing | `.agents/skills/motionmaxxing/references/sound-sync.md` |
| What reads as AI-made | `.agents/skills/motionmaxxing/references/slop.md`, `.agents/skills/cinetic/references/taste-and-slop.md` |
| Three lenses, kill tests, story devices, arcs by format, end cards | `.agents/skills/cinetic/references/concept-and-story.md` |
| Format recipes, sound, camera, lighting, transitions | `.agents/skills/cinetic/references/formats.md`, `sound.md`, `camera.md`, `lighting.md`, `transitions.md` |
| Durations and easing curves | `.agents/skills/motion-design/reference/timing-easing-tables.md` |

Concept tools:
- `cinetic` art-direction deal (3 contrasting directions): `python3 .agents/skills/cinetic/scripts/deck.py --brief "<one line>" --format <launch|update|...> --pace <calm|crisp> --options 3`
- `motionmaxxing` measured precedent per beat: `python3 .agents/skills/motionmaxxing/scripts/precedent.py query --beat proof --content ui --text "<what the beat shows>"`
- `motionmaxxing` brand capture: `node .agents/skills/motionmaxxing/scripts/brand.mjs <url> film/brand`
- `motionmaxxing` render/still/QA: `node .agents/skills/motionmaxxing/scripts/render.mjs film/index.html --still 1.2,2.4 film/stills` · `render.mjs film/index.html film/final.mp4 --audio film/audio/mix.wav` · `python3 .agents/skills/motionmaxxing/scripts/look.py film/final.mp4 --out film/look-final --expect <s> --expect-audio` · `node .agents/skills/motionmaxxing/scripts/lint.mjs film/index.html`

On Windows, run `python3` commands with `.venv\Scripts\python.exe`.

---

## 4. High-Leverage Synergy Patterns

1. **Beat-Synced & Captioned Film**: `openverse_client.py` (CC0 audio/images) → `librosa` beat/onset JSON → `whisperx` word timestamps → `cinetic` / `remotion-captions`+`remotion-markup` / `motionmaxxing` (`sync.mjs`) / `anidoodle` (`narrate.mjs`) / `huashu-art-motion` (`render.py --spec`) / `manim` → `ffmpeg` mux → `look.py` + `ffprobe`.
2. **Zero-API-Key Deterministic Score**: `resources/mg-styles-15/lib/audio/mgaudio/` (`master.py`, `qc.py`) OR `.agents/skills/anidoodle/engine/tools/music.mjs` → `ffmpeg` mux (`-14 LUFS`, `≤-1.1 dBTP`).
3. **Clone + Craft Upgrade**: `reanimate` (`capture.ts` → `easing.ts` → `compare.ts` → `sheet.ts`) → `motion-design` (`timing-easing-tables.md`, `quality-checklist.md`).
4. **Interactive 3D Web VFX**: `three` + `three.quarks` + `@react-three/fiber` + `@react-three/postprocessing` + `tweakpane` + `motion-design` spring timing (+ optional `reanimate` `capture.ts --clock virtual --gl` for deterministic MP4 capture).
5. **Hybrid 3D + 2D Motion**: `blender-core` → `blender-workflow-recipes` → specialist `blender-*` → `blender-asset-qa` (`qa_check.py` + `review_shots.py`) → composite 2D kinetic titles/UI in Remotion, HTML/GSAP, EffectCraft, or `ffmpeg` (pattern: `resources/mg-styles-15/demos/04-3d-render`).
6. **Native Compositing & Lottie**: `effectcraft-cli` (`.ecproj` / 308 effects / Lottie `.json`/`.lottie`) + `motion-design` timing → `effectcraft-cli render` → `ffprobe` + `look.py`.

---

## 5. Mandatory QA Gates & Pass Thresholds

**Universal Gate**: Never self-certify visual/video/3D output from source code alone. Always render real media and inspect both automated metrics and visual contact sheets.

| Stack / Skill | Required Gate Commands / Scripts | Hard Pass Criteria |
|---|---|---|
| **Blender** | `.agents/skills/blender-asset-qa/scripts/qa_check.py -- --objects <objs> --profile game\|render\|print\|roblox` + `.agents/skills/blender-asset-qa/scripts/review_shots.py` (or MCP `look(mode="angles")`) | `"pass": true` (`0` errors), inspected PNG contact sheet, reported tris/counts/`ob.dimensions` |
| **`motionmaxxing`** | `.agents/skills/motionmaxxing/scripts/look.py` + `scripts/lint.mjs` + eye check on `look/sheet.jpg` logged in `NOTE.md` | G0 render/length/audio, G2 `≤3` flat frames, G3 end hold `≤1.4s` & final shot `≤25%`, G5 `lint.mjs` exit `0` |
| **`cinetic`** | `.agents/skills/cinetic/scripts/precheck.mjs`, `lint-film.mjs`, `copy-check.py`, `forensics.py`, `check-sync.py`, `av-audit.py` | Zero linear-motion/slop/copy/seam/empty-frame/A-V sync failures |
| **`anidoodle`** | `.agents/skills/anidoodle/engine/tools/gate.mjs`, `verify-export.mjs`, `ship.mjs` | Deterministic `(frame, env)`, zero dead air, A/V sync & true peak pass, `ship.mjs` green |
| **`huashu-art-motion`** | `.agents/skills/huashu-art-motion/scripts/storyboard_lint.py` (pre-code), `engine/render.py --spec ... --audit`, `qa.py`, `film_gate.py`, `subzone_gate.py`, `deliver.py` | Pre-code storyboard pass, fast-motion ratio `≥0.035`, no `≥0.3s` flat spans, `≤30%` blue-purple slop frames, subtitle safe-zone clear |
| **`reanimate`** | `.agents/skills/reanimate/scripts/compare.ts`, `sheet.ts`, `easing.ts`, `gl.ts` | Side-by-side proof sheet inspected; timing within `±80ms` (motion-faithful) or pixel diff `≤2%` (pixel-faithful) |
| **`motion-design`** | `.agents/skills/motion-design/reference/quality-checklist.md` | Zero linear spatial motion, zero opacity-only state changes, 1/3 choreography rule, 3 motion layers |
| **`remotion-*`** | `remotion-interactivity` on markup + `remotion-studio` preview + `remotion-render` only on explicit export | Studio-editable layers/timing, clean preview, zero unrequested renders |
| **Any MP4 / Cross-Engine** | `ffprobe -v error -show_format -show_streams <out.mp4>` + `.agents/skills/motionmaxxing/scripts/look.py` (or `film_gate.py`) + `resources/mg-styles-15/lib/audio/mgaudio/qc.py` | Valid non-zero streams, exact fps/duration/res, audio `-14 LUFS` & `≤-1.1 dBTP`, visually verified contact sheet |
