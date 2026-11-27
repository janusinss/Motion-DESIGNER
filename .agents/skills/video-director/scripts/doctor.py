#!/usr/bin/env python3
"""doctor.py - cross-platform preflight for Motion-DESIGNER video work.

Checks every tool the video engines call, on Windows, macOS and Linux, and says
which engines are ready. Stdlib only; run it with the workspace venv so the
Python checks see the right packages:

    Windows:      .venv\\Scripts\\python.exe .agents/skills/video-director/scripts/doctor.py
    macOS/Linux:  .venv/bin/python .agents/skills/video-director/scripts/doctor.py

Flags: --json (machine-readable report), --root <repo root> (default: auto).
Exit code 1 when a hard requirement (ffmpeg, ffprobe, node 22+, Chrome, core
Python packages) is missing; optional tools only produce notes.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

IS_WIN = platform.system() == "Windows"

# Packages the engines' Python scripts import (cinetic compatibility line,
# motionmaxxing look.py/mix.py, motion-critic, mgaudio qc.py, Manim, WhisperX).
CORE_PY = ["numpy", "scipy", "soundfile", "pyloudnorm", "cv2", "librosa", "PIL"]
EXTRA_PY = ["fontTools", "brotli", "uharfbuzz", "manim", "whisperx", "torch"]


def run(cmd: list[str], timeout: int = 20) -> str | None:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.SubprocessError):
        return None
    out = (p.stdout or "") + (p.stderr or "")
    return out.strip() if p.returncode == 0 else None


def first_line(s: str | None) -> str:
    return s.splitlines()[0].strip() if s else ""


def find_chrome() -> str | None:
    cands = [os.environ.get("CHROME_PATH")]
    if IS_WIN:
        for env in ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA"):
            base = os.environ.get(env)
            if base:
                cands.append(str(Path(base) / "Google/Chrome/Application/chrome.exe"))
    else:
        cands += ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                  "/Applications/Chromium.app/Contents/MacOS/Chromium",
                  shutil.which("google-chrome"), shutil.which("chromium"), shutil.which("chromium-browser")]
    return next((c for c in cands if c and Path(c).exists()), None)


def find_git_bash() -> str | None:
    """Git Bash, not WSL's System32\\bash.exe (which cannot see Windows node/ffmpeg the same way)."""
    if not IS_WIN:
        return shutil.which("bash")
    for base in (os.environ.get("PROGRAMFILES"), os.environ.get("PROGRAMFILES(X86)"), os.environ.get("LOCALAPPDATA")):
        if base:
            for rel in ("Git/bin/bash.exe", "Programs/Git/bin/bash.exe"):
                p = Path(base) / rel
                if p.exists():
                    return str(p)
    return None


def venv_python(root: Path) -> Path | None:
    p = root / (".venv/Scripts/python.exe" if IS_WIN else ".venv/bin/python")
    return p if p.exists() else None


def py_modules(py: Path, mods: list[str]) -> dict[str, bool]:
    if Path(sys.executable).resolve() == py.resolve():
        return {m: importlib.util.find_spec(m) is not None for m in mods}
    code = "import importlib.util,json,sys;print(json.dumps({m: importlib.util.find_spec(m) is not None for m in sys.argv[1:]}))"
    out = run([str(py), "-c", code, *mods], timeout=60)
    try:
        return json.loads(out.splitlines()[-1]) if out else {m: False for m in mods}
    except json.JSONDecodeError:
        return {m: False for m in mods}


def main() -> int:
    ap = argparse.ArgumentParser(description="Motion-DESIGNER video preflight")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[4])
    a = ap.parse_args()
    root = a.root.resolve()

    r: dict = {"root": str(root), "os": platform.system(), "hard": {}, "optional": {}, "engines": {}, "notes": []}
    hard, opt = r["hard"], r["optional"]

    hard["ffmpeg"] = first_line(run(["ffmpeg", "-hide_banner", "-version"])) or None
    hard["ffprobe"] = first_line(run(["ffprobe", "-hide_banner", "-version"])) or None
    enc = run(["ffmpeg", "-hide_banner", "-encoders"]) or ""
    hard["libx264"] = "libx264" in enc
    nv = first_line(run(["node", "--version"]))
    hard["node22"] = nv if nv and nv.lstrip("v").split(".")[0].isdigit() and int(nv.lstrip("v").split(".")[0]) >= 22 else None
    hard["chrome"] = find_chrome()

    py = venv_python(root)
    hard["venv_python"] = str(py) if py else None
    mods = py_modules(py, CORE_PY + EXTRA_PY) if py else {}
    hard["python_core"] = {m: mods.get(m, False) for m in CORE_PY}
    opt["python_extra"] = {m: mods.get(m, False) for m in EXTRA_PY}
    if py and mods.get("torch"):
        cuda = run([str(py), "-c", "import torch;print(torch.cuda.is_available())"], timeout=90)
        opt["torch_cuda"] = (cuda or "").strip().endswith("True")

    opt["git_bash"] = find_git_bash()
    opt["blender"] = first_line(run(["blender", "--version"], timeout=60)) or None
    opt["bun"] = first_line(run(["bun", "--version"])) or None
    opt["latex"] = bool(shutil.which("latex") and shutil.which("dvisvgm"))
    ec = root / "tools/effectcraft/effectcraft-0.24.1-windows-x64-portable/effectcraft-cli.exe"
    opt["effectcraft"] = str(ec) if ec.exists() else None
    opt["elevenlabs_key"] = bool(os.environ.get("ELEVENLABS_API_KEY"))

    src = root / ".agents/skills"
    mirror = root / ".claude/skills"
    n_src = len(list(src.glob("*/SKILL.md"))) if src.exists() else 0
    n_mir = len(list(mirror.glob("*/SKILL.md"))) if mirror.exists() else 0
    opt["skills"] = {"source": n_src, "claude_mirror": n_mir}

    core_ok = bool(py) and all(hard["python_core"].values())
    base = all([hard["ffmpeg"], hard["ffprobe"], hard["libx264"], hard["node22"]])
    sh_ok = (not IS_WIN) or bool(opt["git_bash"])
    r["engines"] = {
        "motionmaxxing": base and bool(hard["chrome"]) and core_ok,
        "cinetic": base and core_ok and sh_ok,
        "remotion": base,
        "hyperframes": base and (root / ".agents/skills/hyperframes/scripts/plugin-cli.mjs").exists(),
        "anidoodle": base,
        "huashu-art-motion": base and core_ok,
        "manim": bool(opt["python_extra"].get("manim")),
        "motion-critic": bool(hard["ffmpeg"] and hard["ffprobe"]) and core_ok,
        "blender": bool(opt["blender"]),
        "reanimate": bool(opt["bun"]),
        "effectcraft": bool(opt["effectcraft"]),
    }

    n = r["notes"]
    if IS_WIN:
        n.append("Windows: `python3` is usually the Microsoft Store stub; run skill scripts with .venv\\Scripts\\python.exe.")
        if opt["git_bash"]:
            n.append(f"Windows: run .sh scripts with Git Bash ({opt['git_bash']}); `bash` on PATH may be WSL.")
        else:
            n.append("Windows: Git Bash not found; cinetic's .sh scripts (new-film.sh, render.sh) need it.")
    if not hard["chrome"]:
        n.append("Chrome not found: install Google Chrome or set CHROME_PATH (motionmaxxing render/brand capture).")
    if not opt["elevenlabs_key"]:
        n.append("No ELEVENLABS_API_KEY: motionmaxxing voice/music/SFX fall back to CC0 + mgaudio (sound-sync.md section 9).")
    if not opt["bun"]:
        n.append("Bun not installed: reanimate (clone a reference animation) is unavailable.")
    if not opt["latex"]:
        n.append("No LaTeX + dvisvgm: Manim must use Text/MarkupText, not Tex/MathTex.")
    if n_src and n_mir < n_src:
        n.append(f"Claude Code mirror has {n_mir}/{n_src} skills: run scripts/sync-skills.ps1 (Windows) or scripts/sync-skills.sh.")

    missing = [k for k, v in hard.items() if (not v) or (isinstance(v, dict) and not all(v.values()))]
    r["ready"] = not missing
    r["missing_hard"] = missing

    if a.json:
        print(json.dumps(r, indent=2))
    else:
        mark = lambda ok: "OK  " if ok else "MISS"
        print(f"Motion-DESIGNER doctor ({r['os']})  root: {root}")
        print("\nHard requirements")
        for k, v in hard.items():
            if isinstance(v, dict):
                bad = [m for m, ok in v.items() if not ok]
                print(f"  {mark(not bad)} {k}: {'all present' if not bad else 'missing ' + ', '.join(bad)}")
            else:
                print(f"  {mark(bool(v))} {k}: {v if isinstance(v, str) else ('yes' if v else 'no')}")
        print("\nOptional")
        for k, v in opt.items():
            if isinstance(v, dict):
                print(f"  ---- {k}: " + ", ".join(f"{m}={'y' if ok else 'n'}" if isinstance(ok, bool) else f"{m}={ok}" for m, ok in v.items()))
            else:
                print(f"  {mark(bool(v))} {k}: {v if isinstance(v, str) else ('yes' if v else 'no')}")
        print("\nEngines ready: " + ", ".join(k for k, v in r["engines"].items() if v))
        blocked = [k for k, v in r["engines"].items() if not v]
        if blocked:
            print("Engines blocked: " + ", ".join(blocked))
        for line in n:
            print("  note: " + line)
        print("\nREADY" if r["ready"] else "\nNOT READY: missing " + ", ".join(missing))
    return 0 if r["ready"] else 1


if __name__ == "__main__":
    sys.exit(main())
