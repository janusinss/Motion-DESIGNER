#!/usr/bin/env python3
"""build_looks.py - build the look catalogue (references/looks/) from the rendered mg-styles-15 gallery.

For each style: its name, the score its own jury gave, its signature features (from prompts/<id>.md), and its
measured grammar (critic_scan.py on videos/<id>.mp4: median shot, energy peak position, energy contour, cut count).
The metrics JSON per look is the `--reference` input for critic_scan.py and a target for plan_check.py.
The videos are MIT (resources/mg-styles-15/LICENSE); only derived numbers are written here.

Usage (repo root):  .venv\\Scripts\\python.exe .agents/skills/video-director/scripts/build_looks.py [--only 01,09]
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
MG = ROOT / "resources/mg-styles-15"
OUT = Path(__file__).resolve().parents[1] / "references/looks"
SCAN = ROOT / ".agents/skills/motion-critic/scripts/critic_scan.py"

# which video types each look serves first (creative-direction.md Part C ids) and the engine that builds it best here
FIT = {
    "01": ("C3 explainer · C4 sting · C2 ad", "motionmaxxing / anidoodle"),
    "02": ("C3 explainer · C7 titles · C10 loop", "anidoodle"),
    "03": ("C6 demo · C3 explainer · C9 data", "motionmaxxing (Three.js) / HyperFrames"),
    "04": ("C12 3D hero · C1 launch", "Blender → motionmaxxing type"),
    "05": ("C8 music · C10 loop · C5 social", "anidoodle"),
    "06": ("C2 ad · C5 social · C8 music", "motionmaxxing / HyperFrames"),
    "07": ("C4 sting · C10 loop · C1 launch", "motionmaxxing (WebGL)"),
    "08": ("C4 sting · C1 launch", "motionmaxxing"),
    "09": ("C1b hype · C2 ad · C7 titles", "motionmaxxing"),
    "10": ("C8 music · C11 teaser", "motionmaxxing (WebGL)"),
    "12": ("C1 launch · C6 demo (UI glass)", "motionmaxxing / HyperFrames"),
    "18": ("C3 explainer (ZH) · C7 titles", "huashu-art-motion"),
    "19": ("C5 social · C2 ad", "anidoodle"),
    "20": ("C5 social · C11 teaser · C8 music", "anidoodle / motionmaxxing"),
    "22": ("C11 teaser · C9 data (use with care: HUD is banned in motionmaxxing films)", "HyperFrames"),
}


def section(text, head):
    m = re.search(rf"^# {re.escape(head)}[^\n]*\n(.*?)(?=^# |\Z)", text, re.S | re.M)
    return m.group(1).strip() if m else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only")
    a = ap.parse_args()
    only = set(a.only.split(",")) if a.only else None
    (OUT / "metrics").mkdir(parents=True, exist_ok=True)
    rows = []
    for p in sorted((MG / "prompts").glob("*.md")):
        lid = p.stem.split("-")[0]
        if only and lid not in only:
            continue
        txt = p.read_text(encoding="utf-8")
        title = txt.splitlines()[0].lstrip("# ").strip()
        # titles are "<Chinese name> <English name>": keep the trailing run without CJK characters
        m_en = re.search(r"([A-Za-z0-9][A-Za-z0-9 /().,&'+-]*)$", re.split(r"[　-鿿＀-￯]", title)[-1].strip())
        en = m_en.group(1).strip() if m_en else title
        score = re.search(r"(\d+\.\d+)\s*/\s*10", txt)
        # the section is plain lines (first = overview, then visual features and key techniques)
        feats = [l.strip() for l in section(txt, "Signature features").splitlines()[1:] if l.strip()]
        video = MG / "videos" / f"{p.stem}.mp4"
        metrics = None
        if video.is_file():
            tmp = OUT / "metrics" / f"_{p.stem}"
            r = subprocess.run([sys.executable, str(SCAN), str(video), "--out", str(tmp)], capture_output=True, text=True)
            cj = tmp / "critic.json"
            if cj.is_file():
                d = json.loads(cj.read_text(encoding="utf-8"))
                keep = {k: d[k] for k in ("peak_fraction", "cuts_s", "energy_quarters", "energy_cv", "energy_curve_0p5s",
                                          "median_shot_s", "perceived_holds_s", "slop_ratio", "probe") if k in d}
                keep["source"] = f"resources/mg-styles-15/videos/{video.name} (MIT)"
                (OUT / "metrics" / f"{p.stem}.json").write_text(json.dumps(keep, indent=1), encoding="utf-8")
                metrics = keep
            for f in tmp.glob("*"):
                f.unlink()
            tmp.rmdir()
            if r.returncode not in (0, 1):
                print(r.stderr[-400:], file=sys.stderr)
        rows.append((lid, p.stem, en, score.group(1) if score else "–", feats[:3], metrics))
        print(f"{p.stem}: {'measured' if metrics else 'no video'}")

    lines = ["# Look catalogue", "",
             "Pick a look at `video-director` step 2.3 by watching its film, not by its name. Each row links the full style prompt (signature features, rules, craft checklist), the source demo and the rendered 10 s film from `resources/mg-styles-15` (MIT).",
             "`metrics/<id>.json` is that film scanned by `critic_scan.py`: pass it as `--reference` to compare your film's energy curve, peak position and median shot with the look's.",
             "Measured numbers are from 10 s films; scale shot lengths, not the curve shape, for longer films. Generated by `scripts/build_looks.py`; rerun after the gallery changes.", "",
             "More looks without a rendered film: `anidoodle/references/styles/INDEX.md` (31 cards), `huashu-art-motion` style cards (36), `hyperframes-registry` (search by name).", "",
             "| Look | Own jury | Fits (Part C) | Engine here | Median shot | Peak at | Energy CV | Film |",
             "|---|---|---|---|---|---|---|---|"]
    for lid, stem, en, sc, feats, m in rows:
        fit, eng = FIT.get(lid, ("–", "–"))
        ms = f"{m['median_shot_s']:.2f} s" if m and m.get("median_shot_s") else "–"
        pk = f"{m['peak_fraction'] * 100:.0f} %" if m else "–"
        cv = f"{m['energy_cv']:.2f}" if m else "–"
        lines.append(f"| [{en}](../../../../../resources/mg-styles-15/prompts/{stem}.md) | {sc} | {fit} | {eng} | {ms} | {pk} | {cv} | "
                     f"[mp4](../../../../../resources/mg-styles-15/videos/{stem}.mp4) · [demo](../../../../../resources/mg-styles-15/demos/{stem}/) |")
    lines += ["", "## Signature features (first three per look)", ""]
    for lid, stem, en, sc, feats, m in rows:
        lines.append(f"- **{en}**: " + ("; ".join(f.rstrip('.') for f in feats) if feats else "see the prompt"))
    (OUT / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT / 'INDEX.md'} ({len(rows)} looks)")


if __name__ == "__main__":
    main()
