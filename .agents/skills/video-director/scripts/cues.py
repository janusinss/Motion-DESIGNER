#!/usr/bin/env python3
"""cues.py - one clock for picture, sound and QA: write and check a film's engine-neutral cue sheet (stdlib only).

Schema: ../references/cues.schema.json (seconds everywhere). critic_scan.py --cues reads it.

Usage:
  python cues.py from-events <final.mp4.events.json> [--plan PLAN.md] [--hits "12.0:drop,18.0:name"]
                 [--breath "11.6-11.95"] [--hold "18.7-20"] [--fps 30] [--duration 20] --out cues.json
        motionmaxxing: render.mjs writes <out>.mp4.events.json ({t, frame, type, label}); type "cut" -> cuts,
        "press"/"hit" -> hits. Hero and beats come from PLAN.md (the plan_check.py parser).
  python cues.py from-cinetic <out/cues.json> [--plan PLAN.md] --out cues.json
        cinetic: acts -> beats, cue frames -> hits, structural events -> hits, act boundaries -> cuts.
  python cues.py from-anidoodle <out/<film>.cues.json> [--plan PLAN.md] --out cues.json
  python cues.py validate cues.json
Exit: 0 ok, 1 invalid sheet, 2 bad usage.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from plan_check import beat_table  # noqa: E402


def spans(arg):
    out = []
    for part in (arg or "").split(","):
        m = re.match(r"\s*(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*$", part)
        if m:
            out.append([float(m.group(1)), float(m.group(2))])
    return out


def hits(arg):
    out = []
    for part in (arg or "").split(","):
        if part.strip():
            t, _, label = part.partition(":")
            out.append({"t": float(t), "label": label.strip() or "hit"})
    return out


def from_plan(sheet, plan, fps):
    if not plan:
        return
    text = Path(plan).read_text(encoding="utf-8")
    rows = beat_table(text, fps)
    if rows and "beats" not in sheet:
        sheet["beats"] = [{"t0": round(r["t0"], 3), "t1": round(r["t1"], 3), "role": r.get("role", "")} for r in rows]
    m = re.search(r"hero moment[^\n]*?(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)\s*s", text, re.I)
    if m and "hero" not in sheet:
        sheet["hero"] = {"t0": float(m.group(1)), "t1": float(m.group(2))}
        p = re.search(r"screenshot frame is f\s*(\d+)|poster[^\n]*?(\d+(?:\.\d+)?)\s*s", text, re.I)
        if p:
            sheet["hero"]["poster"] = round(int(p.group(1)) / fps, 3) if p.group(1) else float(p.group(2))


def validate(sheet):
    errs = []
    for k in ("version", "fps", "duration", "cuts"):
        if k not in sheet:
            errs.append(f"missing {k}")
    if errs:
        return errs
    d = sheet["duration"]
    if sheet["version"] != 1:
        errs.append("version must be 1")
    if not (isinstance(sheet["fps"], (int, float)) and sheet["fps"] > 0 and isinstance(d, (int, float)) and d > 0):
        errs.append("fps and duration must be > 0")
    if any(not isinstance(c, (int, float)) or c < 0 or c > d for c in sheet["cuts"]):
        errs.append("cuts must be numbers inside [0, duration]")
    if sheet["cuts"] != sorted(sheet["cuts"]):
        errs.append("cuts must be sorted")
    h = sheet.get("hero")
    if h and not (0 <= h.get("t0", -1) < h.get("t1", -1) <= d):
        errs.append("hero needs 0 <= t0 < t1 <= duration")
    for key in ("breaths", "holds"):
        for s in sheet.get(key, []):
            if len(s) != 2 or not (0 <= s[0] < s[1] <= d):
                errs.append(f"{key} span {s} outside [0, duration] or empty")
    for x in sheet.get("hits", []):
        if not (0 <= x.get("t", -1) <= d):
            errs.append(f"hit {x} outside [0, duration]")
    for b in sheet.get("beats", []):
        if not (0 <= b.get("t0", -1) < b.get("t1", -1) <= d + 1e-6):
            errs.append(f"beat {b} outside [0, duration] or empty")
    return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["from-events", "from-cinetic", "from-anidoodle", "validate"])
    ap.add_argument("src")
    ap.add_argument("--plan")
    ap.add_argument("--hits")
    ap.add_argument("--breath")
    ap.add_argument("--hold")
    ap.add_argument("--fps", type=float)
    ap.add_argument("--duration", type=float)
    ap.add_argument("--out")
    a = ap.parse_args()
    src = Path(a.src)
    if not src.is_file():
        print(f"not found: {src}", file=sys.stderr)
        return 2
    data = json.loads(src.read_text(encoding="utf-8"))
    if a.mode == "validate":
        errs = validate(data)
        print("cues: VALID" if not errs else "cues: INVALID\n  " + "\n  ".join(errs))
        return 1 if errs else 0

    if a.mode == "from-events":
        ev = data["events"] if isinstance(data, dict) else data
        fps = a.fps or (data.get("fps") if isinstance(data, dict) else None) or 30
        dur = a.duration or (data.get("duration") if isinstance(data, dict) else None) or max((e.get("t", 0) for e in ev), default=0)
        t = lambda e: round(e["t"] if "t" in e else e["frame"] / fps, 3)  # noqa: E731
        sheet = {"version": 1, "source": f"motionmaxxing {src.name}", "fps": fps, "duration": dur,
                 "cuts": sorted({t(e) for e in ev if e.get("type") == "cut"}),
                 "hits": [{"t": t(e), "label": e.get("label") or e["type"]} for e in ev if e.get("type") in ("press", "hit")]}
    elif a.mode == "from-cinetic":
        fps = data["fps"]
        acts = data.get("acts", {})
        sheet = {"version": 1, "source": f"cinetic {src.name}", "fps": fps, "duration": round(data["total"] / fps, 3),
                 "beats": [{"t0": round(v["from"] / fps, 3), "t1": round((v["from"] + v["dur"]) / fps, 3), "role": k} for k, v in acts.items()],
                 "cuts": sorted({round(v["from"] / fps, 3) for v in acts.values() if v["from"] > 0}),
                 "hits": [{"t": round(f / fps, 3), "label": k} for k, f in data.get("cue", {}).items()]
                         + [{"t": round(e["f"] / fps, 3), "label": e.get("id") or e.get("kind", "event")} for e in data.get("events", []) if e.get("structural")]}
    else:  # from-anidoodle
        fps = data["fps"]
        sheet = {"version": 1, "source": f"anidoodle {src.name}", "fps": fps, "duration": data["durationS"], "cuts": [],
                 "hits": [{"t": round(c["t"], 3), "label": c.get("name", "cue")} for c in data.get("cues", []) if "t" in c]}

    if a.duration:
        sheet["duration"] = a.duration
    sheet["hits"] = sheet.get("hits", []) + hits(a.hits)
    if a.breath:
        sheet["breaths"] = spans(a.breath)
    if a.hold:
        sheet["holds"] = spans(a.hold)
    from_plan(sheet, a.plan, sheet["fps"])
    errs = validate(sheet)
    if errs:
        print("cues: INVALID\n  " + "\n  ".join(errs), file=sys.stderr)
        return 1
    text = json.dumps(sheet, indent=1)
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")
        print(f"cues: {len(sheet['cuts'])} cuts, {len(sheet['hits'])} hits, hero {sheet.get('hero')}, "
              f"{len(sheet.get('breaths', []))} breaths, {len(sheet.get('holds', []))} holds -> {a.out}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
