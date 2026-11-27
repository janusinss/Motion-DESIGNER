#!/usr/bin/env python3
"""plan_check.py - check a film's PLAN.md against its brief BEFORE anything is built (stdlib only).

A plan that is calmer than the brief's words, a hero outside the 55-80 % window, or a beat table that repeats one
shot length is cheaper to fix in text than after a render. Every check reports PASS, WARN, FAIL or UNVERIFIED
(could not be measured from the text); an unrun check never counts as a pass.

Usage:
  python plan_check.py projects/<slug>/PLAN.md [--brief projects/<slug>/BRIEF.md] [--duration 20] [--fps 30]
                       [--like out/like.json] [--json plan_check.json]
  --like: a reference's grammar from cinetic `scripts/like.py measure <clip>`; the planned shot lengths are compared
          with its shot band.
Exit: 0 no FAIL, 1 at least one FAIL, 2 bad usage.

What it reads from PLAN.md (the video-prompt-enhancer plan-template layout):
  - the beat table: a markdown table whose first column is a frame range ("0-90") or a second range ("0.0-3.0 s"),
    with optional "Role" and "Imp" columns
  - "Hero moment": a line naming a second range ("12.0-13.5 s")
  - "Energy curve": shot lengths written as "30 f", "0.5 s" in order
  - the format line ("30 fps", "600 f") when --duration/--fps are not given
"""
import argparse
import json
import re
import sys
from pathlib import Path

HIGH = re.compile(r"\b(hype|fast|fast-paced|punchy|energetic|explosive|intense|aggressive|urgent|rapid|frantic|kinetic|bold|hard-hitting|launch cut)\b", re.I)
LOW = re.compile(r"\b(calm|gentle|meditative|slow|serene|quiet|soft|ambient|contemplative|relaxed|peaceful)\b", re.I)
BREATH = re.compile(r"\b(breath|silence|held|hold|pause|drop out|mute)\b", re.I)


def read(p):
    return Path(p).read_text(encoding="utf-8") if p else ""


def parse_rng(cell, fps):
    """'0-90' (frames) or '0.0-3.0 s' / '12-13.5s' (seconds) -> (t0, t1) in seconds, else None."""
    c = cell.replace("–", "-").replace("—", "-").strip().strip("`*")
    m = re.match(r"^(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*(s|sec|f)?\b", c)
    if not m:
        return None
    a, b, unit = float(m.group(1)), float(m.group(2)), (m.group(3) or "")
    if b <= a:
        return None
    if unit.startswith("s") or ("." in m.group(1) + m.group(2) and unit != "f"):
        return a, b
    return a / fps, b / fps


def beat_table(text, fps):
    rows, header = [], None
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            header = None if not line.strip() else header
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        rng = parse_rng(cells[0], fps) if cells else None
        if rng is None:
            header = [c.lower() for c in cells]
            continue
        row = {"t0": rng[0], "t1": rng[1], "cells": cells}
        if header:
            for key, names in (("role", ("role",)), ("imp", ("imp", "importance"))):
                for i, h in enumerate(header):
                    if i < len(cells) and any(h.startswith(n) for n in names):
                        row[key] = cells[i]
        rows.append(row)
    return rows


def shot_lengths(text, fps):
    m = re.search(r"energy curve[^\n]*", text, re.I)
    if not m:
        return []
    out = []
    for v, u in re.findall(r"(\d+(?:\.\d+)?)\s*(f|s)\b", m.group(0)):
        out.append(float(v) / fps if u == "f" else float(v))
    # bare numbers chained by arrows after a unit ("30 f -> 30 -> 15") inherit the first unit
    chain = re.search(r"(\d+(?:\.\d+)?)\s*(f|s)\b((?:\s*(?:->|→)\s*\d+(?:\.\d+)?(?!\s*(?:f|s)\b))+)", m.group(0))
    if chain:
        unit = chain.group(2)
        for v in re.findall(r"(\d+(?:\.\d+)?)", chain.group(3)):
            out.append(float(v) / fps if unit == "f" else float(v))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("plan")
    ap.add_argument("--brief")
    ap.add_argument("--duration", type=float)
    ap.add_argument("--fps", type=float)
    ap.add_argument("--like")
    ap.add_argument("--json")
    a = ap.parse_args()
    if not Path(a.plan).is_file():
        print(f"plan not found: {a.plan}", file=sys.stderr)
        return 2
    plan = read(a.plan)
    brief = read(a.brief) if a.brief else ""
    if not brief:
        sib = Path(a.plan).with_name("BRIEF.md")
        brief = read(sib) if sib.is_file() else ""

    fps = a.fps or float((re.search(r"(\d+(?:\.\d+)?)\s*fps", plan + brief) or [None, 30])[1])
    rows = beat_table(plan, fps)
    dur = a.duration
    if not dur:
        m = re.search(r"(\d+(?:\.\d+)?)\s*s\s*\((\d+)\s*f\)", plan + brief) or re.search(r"(\d+)\s*f\b(?!\))", re.search(r"##\s*2\.\s*Format[^\n]*\n[^\n]*", plan).group(0) if re.search(r"##\s*2\.\s*Format[^\n]*\n[^\n]*", plan) else "")
        if m and m.lastindex and m.lastindex >= 2:
            dur = float(m.group(1))
        elif m:
            dur = float(m.group(1)) / fps
        elif rows:
            dur = max(r["t1"] for r in rows)
    checks = []

    def add(name, status, value):
        checks.append({"name": name, "status": status, "value": value})

    # beats
    if len(rows) < 3:
        add("beat_table", "UNVERIFIED", f"{len(rows)} beat rows parsed (need >= 3 rows whose first cell is a frame or second range)")
    else:
        add("beat_table", "PASS", f"{len(rows)} beats, {rows[0]['t0']:.2f}-{rows[-1]['t1']:.2f} s")
        gaps = [(rows[i]['t1'], rows[i + 1]['t0']) for i in range(len(rows) - 1) if rows[i + 1]['t0'] - rows[i]['t1'] > 0.5]
        if dur and abs(rows[-1]['t1'] - dur) > 0.5:
            gaps.append((rows[-1]['t1'], dur))
        add("beat_coverage", "FAIL" if gaps else "PASS", f"uncovered spans: {[(round(x, 2), round(y, 2)) for x, y in gaps]}" if gaps else f"0-{dur:.2f} s covered")
        lens = [round(r["t1"] - r["t0"], 2) for r in rows]
        run, worst = 1, 1
        for i in range(1, len(lens)):
            run = run + 1 if abs(lens[i] - lens[i - 1]) < 0.05 else 1
            worst = max(worst, run)
        add("beat_monotony", "FAIL" if worst > 4 else ("WARN" if worst == 4 else "PASS"), f"longest run of equal beat lengths: {worst} (beats {lens})")

    # hero
    hero = None
    m = re.search(r"hero moment[^\n]*?(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)\s*s", plan, re.I)
    if m:
        hero = (float(m.group(1)), float(m.group(2)))
    else:
        hr = [r for r in rows if "hero" in r.get("role", "").lower()]
        if hr:
            hero = (hr[0]["t0"], hr[0]["t1"])
    if hero and dur:
        mid = (hero[0] + hero[1]) / 2 / dur
        add("hero_window", "PASS" if 0.55 <= mid <= 0.80 else "FAIL", f"hero {hero[0]:.2f}-{hero[1]:.2f} s, centre at {mid:.0%} (target 55-80 %)")
    else:
        add("hero_window", "UNVERIFIED", "no 'Hero moment ... X-Y s' line and no beat with role 'hero'")
    if rows and hero:
        imps = [(r.get("imp") or "").strip() for r in rows]
        hero_rows = [r for r in rows if r["t0"] < hero[1] and r["t1"] > hero[0]]
        if all(i.isdigit() for i in imps) and hero_rows:
            top = max(int(i) for i in imps)
            hi = max(int((r.get("imp") or "0")) for r in hero_rows)
            add("hero_importance", "PASS" if hi == top else "FAIL", f"hero beat importance {hi}, film max {top}")
        else:
            add("hero_importance", "UNVERIFIED", "no numeric Imp column")

    # energy against the brief's words
    words = brief + "\n" + "\n".join(l for l in plan.splitlines() if re.search(r"emotion|format|playbook|C1b", l, re.I))
    hi_w, lo_w = set(w.lower() for w in HIGH.findall(words)), set(w.lower() for w in LOW.findall(words))
    want = "high" if len(hi_w) > len(lo_w) else ("low" if lo_w else "neutral")
    shots = shot_lengths(plan, fps)
    if not shots:
        add("energy_vs_brief", "UNVERIFIED", f"brief reads {want} ({sorted(hi_w or lo_w)}); no shot lengths in an 'Energy curve' line")
    else:
        mn, mx = min(shots), max(shots)
        accel = any(shots[i + 1] < shots[i] for i in range(len(shots) - 1))
        if want == "high":
            ok = mn <= 0.34 and accel
            add("energy_vs_brief", "PASS" if ok else "FAIL", f"brief reads high ({sorted(hi_w)}); shortest planned shot {mn:.2f} s (need <= 0.34 s), accelerating: {accel}")
        elif want == "low":
            add("energy_vs_brief", "PASS" if mn >= 0.8 else "FAIL", f"brief reads calm ({sorted(lo_w)}); shortest planned shot {mn:.2f} s (need >= 0.8 s)")
        else:
            add("energy_vs_brief", "PASS", f"brief has no energy words; planned shots {mn:.2f}-{mx:.2f} s")
    if want == "high":
        # only where timing is planned: the energy curve, the sound arc and the beat rows (not prose like "hold the brand")
        where = "\n".join(l for l in plan.splitlines() if re.search(r"energy curve|sound arc", l, re.I)) + "\n" + "\n".join(" ".join(r["cells"]) for r in rows)
        hit = BREATH.search(where)
        add("designed_breath", "PASS" if hit else "FAIL", f"breath planned ('{hit.group(0)}')" if hit else "C1b needs a designed breath (silence or hold) before the drop in the energy curve, sound arc or beat table; none named")

    # reference grammar
    if a.like:
        try:
            like = json.loads(read(a.like))
            band = next(iter(like["shot"]["band"].values()))
            if shots:
                med = sorted(shots)[len(shots) // 2]
                lo, hi = band[0] / like["shot"].get("r70", 1.75), band[1] * like["shot"].get("r70", 1.75)
                add("reference_shot_band", "PASS" if lo <= med <= hi else "WARN", f"planned median shot {med:.2f} s vs reference band {band[0]:.2f}-{band[1]:.2f} s (tolerance x{like['shot'].get('r70', 1.75)})")
            else:
                add("reference_shot_band", "UNVERIFIED", "no planned shot lengths to compare")
        except (OSError, KeyError, ValueError, StopIteration) as e:
            add("reference_shot_band", "UNVERIFIED", f"cannot read {a.like}: {e}")

    for c in checks:
        print(f"  {c['status']:<10} {c['name']:<20} {c['value']}")
    fails = [c for c in checks if c["status"] == "FAIL"]
    unver = [c for c in checks if c["status"] == "UNVERIFIED"]
    print(f"PLAN CHECK: {'FAIL' if fails else 'PASS'}  ({len(fails)} fail, {len(unver)} unverified)")
    if a.json:
        Path(a.json).write_text(json.dumps({"pass": not fails, "checks": checks}, indent=2), encoding="utf-8")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
