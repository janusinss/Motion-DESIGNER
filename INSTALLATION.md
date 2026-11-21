# Installation Guide

Cross-platform setup instructions (Windows, macOS, Linux) for installing **Motion-DESIGNER** in a fresh environment or bringing its 48 agent skills into another repository.

---

## 1. Prerequisites

| Tool | Required Version | Purpose |
|---|---|---|
| **Git** | Any recent | Clone the repository |
| **Python** + **`uv`** | Python `3.12`–`3.13` (`>=3.12,<3.14`), `uv` recommended | Manim, Librosa, WhisperX, Openverse client, skill QA scripts |
| **Node.js** + **`npm`** | Node `22+`, `npm 10+` | 3D web VFX stack (`three.quarks`, R3F, postprocessing, `tweakpane`), Remotion (`npx`), JS skill tools |
| **FFmpeg** | Latest (`ffmpeg` + `ffprobe` on `PATH`) | Video/audio encoding, muxing, frame extraction, A/V QA |
| **Blender** *(optional)* | `5.2+` LTS (`blender` on `PATH`) | Required only for the 28 `blender-*` 3D skills |
| **Bun + Playwright** *(optional)* | Latest | Used by browser-capture/render skills (`reanimate`, `cinetic`, `motionmaxxing`, `anidoodle`, `huashu-art-motion`) |

Clone the repository first:

```bash
git clone https://github.com/janusinss/Motion-DESIGNER.git
cd Motion-DESIGNER
```

---

## 2. AI Agent Harness Setup

All 48 skills live canonically in `.agents/skills/<name>/SKILL.md`, and all agent rules/routing live in [`AGENTS.md`](./AGENTS.md).

| Harness | Instruction File | Project Skills Path | Global Skills Path | Setup |
|---|---|---|---|---|
| **Antigravity** | `AGENTS.md` | `.agents/skills/<name>/SKILL.md` | `~/.gemini/config/` | Works out of the box |
| **OpenAI Codex** | `AGENTS.md` | `.agents/skills/<name>/SKILL.md` (`.codex/skills/` also supported) | `~/.agents/skills/` (`~/.codex/skills/`) | Works out of the box |
| **Claude Code** | `CLAUDE.md` (`@AGENTS.md` import) | `.claude/skills/<name>/SKILL.md` | `~/.claude/skills/` | Run `scripts/sync-skills.{ps1,sh}` |

### 2.1 Antigravity

Open the cloned `Motion-DESIGNER` directory as your workspace. Antigravity automatically loads `AGENTS.md` and discovers all 48 skills under `.agents/skills/`. No extra step is required.

### 2.2 OpenAI Codex

Run Codex inside `Motion-DESIGNER`. Codex automatically reads `AGENTS.md` and discovers `.agents/skills/<name>/SKILL.md` while walking from `$CWD` up to the repository root.

Optional — expose all 48 skills globally to Codex across every project on your machine:

```powershell
# Windows (PowerShell)
.\scripts\sync-skills.ps1 -Global -Target codex
# Or sync to both ~/.agents/skills and ~/.codex/skills (plus ~/.claude/skills)
.\scripts\sync-skills.ps1 -Global
```

```bash
# macOS / Linux (Bash)
./scripts/sync-skills.sh --global --target codex
# Or sync to ~/.claude/skills, ~/.agents/skills, and ~/.codex/skills
./scripts/sync-skills.sh --global
```

### 2.3 Claude Code

[`CLAUDE.md`](./CLAUDE.md) imports `@AGENTS.md` inline so Claude Code receives the exact same operating rules without duplicating text. Because Claude Code reads skills from `.claude/skills/` (project) or `~/.claude/skills/` (global), run the bundled sync script after cloning:

**Windows (PowerShell)** — uses NTFS directory junctions by default (no Administrator or Developer Mode required):

```powershell
# Project-local (.claude/skills/ — gitignored)
.\scripts\sync-skills.ps1

# Preview without writing
.\scripts\sync-skills.ps1 -DryRun

# User-global (~/.claude/skills, ~/.agents/skills, ~/.codex/skills)
.\scripts\sync-skills.ps1 -Global

# Force-copy instead of junctions
.\scripts\sync-skills.ps1 -Mode copy -Force

# Remove only Motion-DESIGNER skills from target directory
.\scripts\sync-skills.ps1 -Clean
```

**macOS / Linux (Bash)** — uses symlinks by default:

```bash
chmod +x scripts/sync-skills.sh

# Project-local (.claude/skills/ — gitignored)
./scripts/sync-skills.sh

# Preview without writing
./scripts/sync-skills.sh --dry-run

# User-global (~/.claude/skills, ~/.agents/skills, ~/.codex/skills)
./scripts/sync-skills.sh --global

# Copy instead of symlinks
./scripts/sync-skills.sh --mode copy --force

# Remove only Motion-DESIGNER skills from target directory
./scripts/sync-skills.sh --clean
```

Supported flags:
- PowerShell (`scripts/sync-skills.ps1`): `-Global`, `-Target auto|claude|agents|codex|all`, `-Mode auto|junction|symlink|copy`, `-Force`, `-Clean`, `-DryRun`
- Bash (`scripts/sync-skills.sh`): `--global`, `--target auto|claude|agents|codex|all`, `--mode symlink|copy`, `--force`, `--clean`, `--dry-run`

**Manual Fallback (Without Helper Script):**

```powershell
# Windows PowerShell (copy into .claude/skills)
New-Item -ItemType Directory -Path .claude\skills -Force | Out-Null
Copy-Item -Path .agents\skills\* -Destination .claude\skills\ -Recurse -Force
```

```bash
# macOS / Linux (symlink directory)
mkdir -p .claude
ln -s "$(pwd)/.agents/skills" .claude/skills
```

> Keep `.agents/skills/` as the single source of truth; `.claude/skills/` is a generated local mirror and is gitignored.

### 2.4 Installing Skills into Another Existing Repository

Choose one of two options:

1. **Global install (recommended for multi-repo use):** Clone `Motion-DESIGNER` once, then run `.\scripts\sync-skills.ps1 -Global` (Windows) or `./scripts/sync-skills.sh --global` (macOS/Linux). Both scripts operate per-skill and preserve any unrelated skills already in your global directories.
2. **Project-scoped copy:** Copy the canonical files into your target repository root:

```powershell
# Windows (PowerShell) — run from Motion-DESIGNER root
$Target = "C:\path\to\your-project"
New-Item -ItemType Directory -Path (Join-Path $Target ".agents"), (Join-Path $Target "scripts") -Force | Out-Null
Copy-Item -Path .agents\skills -Destination (Join-Path $Target ".agents\skills") -Recurse -Force
Copy-Item -Path AGENTS.md, CLAUDE.md -Destination $Target -Force
Copy-Item -Path scripts\sync-skills.ps1, scripts\sync-skills.sh -Destination (Join-Path $Target "scripts") -Force
```

```bash
# macOS / Linux (Bash) — run from Motion-DESIGNER root
TARGET="/path/to/your-project"
mkdir -p "$TARGET/.agents" "$TARGET/scripts"
cp -R .agents/skills "$TARGET/.agents/"
cp AGENTS.md CLAUDE.md "$TARGET/"
cp scripts/sync-skills.sh scripts/sync-skills.ps1 "$TARGET/scripts/"
```

Then add `.claude/skills/` to the target repo's `.gitignore` and run the sync script if using Claude Code. If you also want the 15 style prompts, demos, and zero-API-key audio synthesizer, copy `resources/mg-styles-15/`.

---

## 3. Python Stack (`manim`, `librosa`, `whisperx`)

Pinned in [`pyproject.toml`](./pyproject.toml) (`requires-python = ">=3.12,<3.14"`): `manim>=0.22.1`, `librosa>=1.0.1`, `whisperx>=3.8.6`, `torch~=2.8.0`, `torchaudio~=2.8.0`, `torchvision~=0.23.0`.

### 3.1 System Libraries for Manim (macOS / Linux)

Install Cairo and Pango headers before installing `manim` if prebuilt wheels are unavailable on your platform:

```bash
# macOS (Homebrew)
brew install cairo pango pkg-config

# Linux (Debian / Ubuntu)
sudo apt update && sudo apt install -y libcairo2-dev libpango1.0-dev pkg-config python3-dev
```

### 3.2 Recommended Install with `uv`

Install `uv` if not already installed (`winget install astral-sh.uv` on Windows, `brew install uv` on macOS, or `curl -LsSf https://astral.sh/uv/install.sh | sh` on Linux).

**Option A — NVIDIA CUDA 12.8 GPU (Windows / Linux x86_64):**

`pyproject.toml` pins `torch`, `torchaudio`, and `torchvision` to the `pytorch-cu128` index (`https://download.pytorch.org/whl/cu128`).

```bash
uv sync --no-install-project
```

**Option B — macOS (Apple Silicon / Intel) or CPU-Only (Windows / Linux):**

The `pytorch-cu128` index does not publish macOS wheels and requires an NVIDIA GPU on Windows/Linux. Create a Python 3.13 venv and install from standard PyPI (MPS on Apple Silicon, CPU on x86_64) or the PyTorch CPU index:

```bash
# macOS (Apple Silicon MPS / Intel)
uv venv .venv --python 3.13
uv pip install --python .venv/bin/python \
  "manim>=0.22.1" "librosa>=1.0.1" "whisperx>=3.8.6" \
  "torch~=2.8.0" "torchaudio~=2.8.0" "torchvision~=0.23.0"
```

```powershell
# Windows CPU-only (PowerShell)
uv venv .venv --python 3.13
uv pip install --python .venv\Scripts\python.exe `
  --extra-index-url https://download.pytorch.org/whl/cpu `
  "manim>=0.22.1" "librosa>=1.0.1" "whisperx>=3.8.6" `
  "torch~=2.8.0" "torchaudio~=2.8.0" "torchvision~=0.23.0"
```

```bash
# Linux CPU-only (Bash)
uv venv .venv --python 3.13
uv pip install --python .venv/bin/python \
  --extra-index-url https://download.pytorch.org/whl/cpu \
  "manim>=0.22.1" "librosa>=1.0.1" "whisperx>=3.8.6" \
  "torch~=2.8.0" "torchaudio~=2.8.0" "torchvision~=0.23.0"
```

### 3.3 `pip` Fallback (`requirements.txt`)

[`requirements.txt`](./requirements.txt) is exported from `uv.lock` with CUDA 12.8 PyTorch pins (`+cu128`).

```powershell
# Windows (CUDA 12.8)
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --extra-index-url https://download.pytorch.org/whl/cu128 -r requirements.txt
```

```bash
# Linux (CUDA 12.8)
python3.13 -m venv .venv
source .venv/bin/activate
pip install --extra-index-url https://download.pytorch.org/whl/cu128 -r requirements.txt
```

```bash
# macOS / CPU-only (install top-level packages without +cu128 pins)
python3.13 -m venv .venv
source .venv/bin/activate
pip install "manim>=0.22.1" "librosa>=1.0.1" "whisperx>=3.8.6" \
  "torch~=2.8.0" "torchaudio~=2.8.0" "torchvision~=0.23.0"
```

### 3.4 Optional LaTeX for Manim (`Tex` / `MathTex`)

`Text` and `MarkupText` work without LaTeX. Install a TeX distribution plus `dvisvgm` only if you render `Tex`/`MathTex` scenes:

```powershell
# Windows
winget install MiKTeX.MiKTeX
```

```bash
# macOS
brew install --cask mactex-no-gui

# Linux (Debian / Ubuntu)
sudo apt install -y texlive-latex-extra texlive-fonts-extra dvisvgm
```

---

## 4. JS/TS 3D Stack (`three.quarks`, `@react-three/postprocessing`, `tweakpane`)

Defined in [`package.json`](./package.json) (`"type": "module"`, Node 22+): `three`, `three.quarks`, `@react-three/fiber`, `@react-three/postprocessing`, `postprocessing`, `react`, `react-dom`, `tweakpane`, plus TypeScript `@types/*`.

```bash
# Clean reproducible install from package-lock.json
npm ci

# Or standard install when adding/updating packages
npm install
```

> **Remotion Note:** Remotion is intentionally excluded from root `package.json`. Scaffold Remotion projects per composition via `npx create-video@latest` (see `.agents/skills/remotion-create/SKILL.md`).

---

## 5. Native Tools & API

### 5.1 FFmpeg (`ffmpeg` & `ffprobe`)

```powershell
# Windows (WinGet)
winget install Gyan.FFmpeg
```

```bash
# macOS (Homebrew)
brew install ffmpeg

# Linux (Debian / Ubuntu)
sudo apt update && sudo apt install -y ffmpeg
```

Restart your terminal after installing on Windows so `ffmpeg` and `ffprobe` appear on `PATH`.

### 5.2 Blender `5.2+` LTS *(Optional)*

Required only for the 28 `blender-*` skills.

```powershell
# Windows
winget install BlenderFoundation.Blender
```

```bash
# macOS
brew install --cask blender

# Linux — download the official tarball from https://www.blender.org/download/ or use Flatpak/Snap
```

Ensure `blender` is on `PATH` (on Windows default install: `C:\Program Files\Blender Foundation\Blender 5.2\`).

### 5.3 EffectCraft `v0.24.1` (`storytold/effectcraft`)

> **Why it is not in Git:** The portable binaries (`effectcraft.exe` at ~108.6 MB and `effectcraft-cli.exe` at ~107.5 MB) exceed GitHub's 100 MB file limit. `tools/effectcraft/effectcraft-*-portable/` is gitignored; only [`tools/effectcraft/SHA256SUMS.txt`](./tools/effectcraft/SHA256SUMS.txt) is tracked in this repository.

Download the matching `v0.24.1` archive from [GitHub Releases](https://github.com/storytold/effectcraft/releases/tag/v0.24.1) and verify its SHA256 checksum against [`tools/effectcraft/SHA256SUMS.txt`](./tools/effectcraft/SHA256SUMS.txt):

**Windows x64 Portable (PowerShell):**

```powershell
$url = "https://github.com/storytold/effectcraft/releases/download/v0.24.1/effectcraft-0.24.1-windows-x64-portable.zip"
$zip = "tools\effectcraft\effectcraft-0.24.1-windows-x64-portable.zip"
$dst = "tools\effectcraft\effectcraft-0.24.1-windows-x64-portable"

Invoke-WebRequest -Uri $url -OutFile $zip
$actual = (Get-FileHash -Algorithm SHA256 $zip).Hash.ToLower()
$expected = "707bb7480783904e153fd71fd43ffaaf806fbbaa7f803090c2d32f5d920bd996"
if ($actual -ne $expected) { throw "SHA256 mismatch: $actual != $expected" }

Expand-Archive -Path $zip -DestinationPath $dst -Force
Remove-Item $zip
```

**macOS Universal (CLI zip or DMG):**

```bash
curl -LO "https://github.com/storytold/effectcraft/releases/download/v0.24.1/effectcraft-cli-0.24.1-macos-universal.zip"
echo "2781eda194372ad47f4c0c7df8b1d38501a3e90bb499282f57e9598a85958673  effectcraft-cli-0.24.1-macos-universal.zip" | shasum -a 256 -c -
unzip effectcraft-cli-0.24.1-macos-universal.zip -d tools/effectcraft/effectcraft-0.24.1-macos-universal
# GUI app: effectcraft-0.24.1-macos-universal.dmg (SHA256 in tools/effectcraft/SHA256SUMS.txt)
```

**Linux x86_64 (`.tar.gz`; `.AppImage`, `.deb`, `.rpm`, `.flatpak`, and `aarch64` also in `SHA256SUMS.txt`):**

```bash
curl -LO "https://github.com/storytold/effectcraft/releases/download/v0.24.1/effectcraft-0.24.1-linux-x86_64.tar.gz"
echo "5ce0393690144227fa9186e82308ad638a6ef6d9f976c996e6d03b5b51b65a7b  effectcraft-0.24.1-linux-x86_64.tar.gz" | sha256sum -c -
mkdir -p tools/effectcraft/effectcraft-0.24.1-linux-x86_64
tar -xzf effectcraft-0.24.1-linux-x86_64.tar.gz -C tools/effectcraft/effectcraft-0.24.1-linux-x86_64
```

**Build from Source via Rust (`cargo`):**

```bash
git clone https://github.com/storytold/effectcraft.git
cd effectcraft
cargo build --release
```

### 5.4 Openverse Media API Client (`tools/openverse/openverse_client.py`)

Uses Python 3.9+ standard library only (`urllib`, `json`, `argparse`) — zero pip dependencies. See [`tools/openverse/README.md`](./tools/openverse/README.md) for all flags.

```bash
# Verify live image + audio connectivity
python tools/openverse/openverse_client.py --check --limit 1

# Search CC0 audio
python tools/openverse/openverse_client.py --type audio -q "ambient synth" --license cc0 -n 3
```

---

## 6. Verification Commands

Run these checks from the repository root to confirm every installed stack is healthy.

### 6.1 Agent Skills & Claude Code Sync

```powershell
# Windows (PowerShell) — expect 48 SKILL.md files and clean dry-run
(Get-ChildItem .agents\skills\*\SKILL.md).Count
.\scripts\sync-skills.ps1 -DryRun
```

```bash
# macOS / Linux (Bash) — expect 48 SKILL.md files and clean dry-run
ls -1 .agents/skills/*/SKILL.md | wc -l
./scripts/sync-skills.sh --dry-run
```

### 6.2 Python Stack

```powershell
# Windows (PowerShell)
.\.venv\Scripts\python.exe -c "from importlib.metadata import version; import manim, librosa, whisperx, torch; print('manim', version('manim'), '| librosa', version('librosa'), '| whisperx', version('whisperx'), '| torch', torch.__version__, '| cuda:', torch.cuda.is_available())"
.\.venv\Scripts\manim.exe --version
.\.venv\Scripts\whisperx.exe --help
```

```bash
# macOS / Linux (Bash)
.venv/bin/python -c "from importlib.metadata import version; import manim, librosa, whisperx, torch; print('manim', version('manim'), '| librosa', version('librosa'), '| whisperx', version('whisperx'), '| torch', torch.__version__, '| cuda:', torch.cuda.is_available(), '| mps:', torch.backends.mps.is_available())"
.venv/bin/manim --version
.venv/bin/whisperx --help
```

### 6.3 JS/TS 3D Stack

```bash
npm ls --depth=0
node --input-type=module -e "for (const m of ['three','three.quarks','@react-three/fiber','@react-three/postprocessing','tweakpane']) await import(m); console.log('JS 3D ESM imports OK')"
```

### 6.4 Native Tools & Openverse API

```powershell
# Windows (PowerShell)
ffmpeg -version | Select-Object -First 1
ffprobe -version | Select-Object -First 1
blender --version | Select-Object -First 1
.\tools\effectcraft\effectcraft-0.24.1-windows-x64-portable\effectcraft-cli.exe --version
.\.venv\Scripts\python.exe tools/openverse/openverse_client.py --check --limit 1
```

```bash
# macOS / Linux (Bash)
ffmpeg -version | head -n 1
ffprobe -version | head -n 1
blender --version | head -n 1
# Adjust path to your installed EffectCraft binary if downloaded:
# ./tools/effectcraft/effectcraft-0.24.1-linux-x86_64/effectcraft-cli --version
.venv/bin/python tools/openverse/openverse_client.py --check --limit 1
```
