# Motion-DESIGNER

All-in-one AI motion design, 3D graphics, animation, and audiovisual production workspace combining **18 curated resources** and **59 agent skills** under one canonical routing architecture.

![Antigravity](https://img.shields.io/badge/Antigravity-Native-brightgreen) ![OpenAI Codex](https://img.shields.io/badge/OpenAI%20Codex-Native-brightgreen) ![Claude Code](https://img.shields.io/badge/Claude%20Code-CLAUDE.md%20%2B%20Sync-blue) ![Skills](https://img.shields.io/badge/Agent%20Skills-59-informational) ![Resources](https://img.shields.io/badge/Resources-18-informational)

---

## Harness Compatibility

| AI Harness | Instructions | Skills Discovery | Setup Needed |
|---|---|---|---|
| **Antigravity** | [`AGENTS.md`](./AGENTS.md) | `.agents/skills/<name>/SKILL.md` | None (native out of the box) |
| **OpenAI Codex** | [`AGENTS.md`](./AGENTS.md) | `.agents/skills/<name>/SKILL.md` | None (native out of the box) |
| **Claude Code** | [`CLAUDE.md`](./CLAUDE.md) (`@AGENTS.md`) | `.claude/skills/<name>/SKILL.md` or `~/.claude/skills/` | Run `scripts/sync-skills.ps1` or `scripts/sync-skills.sh` |

---

## What's Included (18 Resources / 59 Agent Skills)

- **Motion, Art, Cloning, Direction, Prompt Planning & Critique Skills (9 skills + 1 style pack)**:
  - `video-director` (end-to-end entry point for any video: preflight `doctor.py`, direction, one locked engine, hero first, native gates, independent jury, delivery), `motion-critic` (award-jury review loop: measured scan + 8-dimension calibrated scoring + timecoded fix list), `video-prompt-enhancer` (interview-first creative director and prompt planner targeting the full skill stack), `reanimate`, `motion-design`, `cinetic`, `motionmaxxing`, `anidoodle`, `huashu-art-motion`
  - `resources/mg-styles-15/` — 15 canonical 10s motion-graphics style prompts/demos, `window.renderAt(t)` render harness, critic rubric, and zero-API-key Python audio synthesizer (`lib/audio/mgaudio/`)
- **Blender 5.2+ 3D Pipeline Skills (28 skills)**: Full modeling, sculpting, retopo/UV, Geometry Nodes, PBR/NPR materials, rigging, facial blendshapes, clothing, grooming, animation, look-dev, weather/physics, rendering, QA (`blender-asset-qa`), and engine export
- **Remotion 4 Skills (13 skills)**: Routed via `remotion-best-practices` covering project scaffolding, markup, Studio interactivity, captions, maps, Mediabunny, rendering, and SaaS `<Player>`
- **HyperFrames Skills (9 skills, Apache-2.0, vendored from `heygen-com/hyperframes`)**: `hyperframes` (HTML rendered to video), `hyperframes-cli`, `hyperframes-registry` (~450 ready blocks: captions, charts, maps, transitions, kinetic type), `media-use` (music, SFX, VO, grades, audio mixing), `figma`, `reverse-any-video`, `style-sampling`, `remotion-to-hyperframes`, `slideshow`
- **Python Audio / Math / Alignment Stack (3)**: `manim`, `librosa`, `whisperx` (`pyproject.toml`, `uv.lock`, `requirements.txt`)
- **JS/TS Real-Time 3D Web VFX Stack (3)**: `three.quarks`, `@react-three/postprocessing` (+ `three`, `@react-three/fiber`, `react`), `tweakpane` (`package.json`, `package-lock.json`)
- **Native Tools & Media API (3)**: `FFmpeg`/`ffprobe` (system PATH), `EffectCraft v0.24.1` (release checksums in `tools/effectcraft/SHA256SUMS.txt`; portable binaries gitignored), and `Openverse API v1` stdlib client (`tools/openverse/openverse_client.py`)

---

## Quick Start

1. **Clone the repo:**
   ```bash
   git clone https://github.com/janusinss/Motion-DESIGNER.git
   cd Motion-DESIGNER
   ```
2. **Claude Code users** — expose all 59 skills to `.claude/skills/` (or add `-Global` / `--global` for user-wide availability):
   ```powershell
   # Windows (PowerShell)
   .\scripts\sync-skills.ps1
   ```
   ```bash
   # macOS / Linux (Bash)
   ./scripts/sync-skills.sh
   ```
3. **Install Python & JS dependencies:**
   ```bash
   uv sync --no-install-project   # NVIDIA CUDA 12.8; see INSTALLATION.md for macOS / CPU-only
   npm ci
   ```

See **[`INSTALLATION.md`](./INSTALLATION.md)** for full cross-platform instructions (Windows, macOS, Linux), CPU/macOS PyTorch setup, EffectCraft `v0.24.1` binary download + SHA256 verification, installing skills into other repositories, and verification commands.

---

## Quick Links

- **[`INSTALLATION.md`](./INSTALLATION.md)** — Full cross-platform installation, harness setup, and verification guide
- **[`AGENTS.md`](./AGENTS.md)** — Canonical agent operating rules, skill disambiguation matrix, pipelines, and quality gates
- **[`CLAUDE.md`](./CLAUDE.md)** — Claude Code entry file (`@AGENTS.md` import + entry points, precedence over global skills, Windows command map, jury-in-a-subagent, ask-first rules)
- **[`resources/mg-styles-15/README.md`](./resources/mg-styles-15/README.md)** — 15 motion-graphics style prompts, harness, rubric, and Python synth audio library
- **[`tools/openverse/README.md`](./tools/openverse/README.md)** — Creative Commons image/audio search client documentation

---

## Repository Layout

```text
Motion-DESIGNER/
├── AGENTS.md                  # Canonical rules, routing matrix & QA gates (Antigravity / Codex / Claude)
├── CLAUDE.md                  # Claude Code entry file importing @AGENTS.md
├── INSTALLATION.md            # Cross-platform setup & verification guide
├── README.md                  # This overview
├── pyproject.toml             # Python stack manifest (manim, librosa, whisperx, PyTorch)
├── uv.lock                    # Locked Python dependencies for uv
├── requirements.txt           # Exported pip fallback requirements
├── projects/                  # One folder per film (BRIEF, PLAN, film/, NOTE); see video-director
├── package.json               # JS/TS 3D stack manifest (three.quarks, R3F, postprocessing, tweakpane)
├── package-lock.json          # Locked npm dependencies
├── .agents/
│   └── skills/                # 59 canonical agent skills (<skill-name>/SKILL.md)
├── scripts/
│   ├── sync-skills.ps1        # Windows skill mirror/junction helper (Claude Code & global targets)
│   └── sync-skills.sh         # macOS/Linux skill symlink/copy helper (Claude Code & global targets)
├── resources/
│   └── mg-styles-15/          # 15 MG style prompts/demos, render harness, rubric & CC0 audio synth
└── tools/
    ├── effectcraft/
    │   └── SHA256SUMS.txt     # Official v0.24.1 release checksums (portable binaries gitignored)
    └── openverse/
        ├── openverse_client.py
        └── README.md
```

> Local directories created after install (`.venv/`, `node_modules/`, `.claude/skills/`, and downloaded `tools/effectcraft/effectcraft-*-portable/` binaries) are gitignored.
