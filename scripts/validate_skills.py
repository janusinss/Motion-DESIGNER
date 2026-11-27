#!/usr/bin/env python3
"""validate_skills.py - stdlib-only consistency check for the Motion-DESIGNER skill set.

Checks:
  1. Every .agents/skills/*/SKILL.md opens with YAML frontmatter that has a non-empty
     `name` and `description` (plain, quoted, or block-scalar `>` / `|` values).
  2. Skill names are unique, and each name matches its folder name.
  3. Every skill count stated in AGENTS.md, README.md, INSTALLATION.md, CLAUDE.md and
     video-prompt-enhancer/references/catalog.md equals the real count
     (catalog.md states "sibling" skills: the real count minus video-prompt-enhancer itself).
  4. The plugin manifests in .claude-plugin/ parse as JSON and point at .agents/skills/.

Usage:  python scripts/validate_skills.py [--root DIR] [--json]
Exit 0 when everything matches, 1 on any mismatch.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Anchored count phrases. Each pattern captures the TOTAL skill count only; subcounts such as
# "Blender 5.2+ Skills (28", "HyperFrames Skills (9", "3 local skills" or "9 upstream packs" never match.
TOTAL_PATTERNS = [
    r"\b[Aa]ll (\d+) (?:workspace |agent |Motion-DESIGNER )?skills\b",
    r"\b(\d+) agent skills\b",
    r"\((\d+) Skills\b",
    r"/ (\d+) (?:agent )?skills\b",
    r"Agent%20Skills-(\d+)",
    r"\bexpect (\d+) SKILL\.md\b",
    r"\b(\d+) canonical agent skills\b",
]
SIBLING_PATTERNS = [r"\b(\d+) [Ss]ibling (?:Motion-DESIGNER )?[Ss]kills\b"]

# file -> (patterns, offset from real count, a count must be stated)
DOCS = {
    "AGENTS.md": (TOTAL_PATTERNS, 0, True),
    "README.md": (TOTAL_PATTERNS, 0, True),
    "INSTALLATION.md": (TOTAL_PATTERNS, 0, True),
    "CLAUDE.md": (TOTAL_PATTERNS, 0, False),
    ".agents/skills/video-prompt-enhancer/references/catalog.md": (SIBLING_PATTERNS, -1, True),
    ".claude-plugin/marketplace.json": (TOTAL_PATTERNS, 0, True),
    ".claude-plugin/plugin.json": (TOTAL_PATTERNS, 0, True),
}


def parse_frontmatter(text: str) -> dict[str, str] | None:
    """Minimal YAML frontmatter reader for top-level scalar keys (enough for name/description)."""
    lines = text.lstrip("﻿").splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() in ("---", "..."))
    except StopIteration:
        return None
    body, out, i = lines[1:end], {}, 0
    while i < len(body):
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", body[i])
        if not m:
            i += 1
            continue
        key, val = m.group(1), m.group(2).strip()
        i += 1
        if val[:1] in (">", "|"):  # block scalar: gather indented lines
            parts = []
            while i < len(body) and (not body[i].strip() or body[i][:1] in (" ", "\t")):
                parts.append(body[i].strip())
                i += 1
            val = " ".join(p for p in parts if p)
        else:
            # plain multi-line continuation (indented lines after the key)
            while i < len(body) and body[i][:1] in (" ", "\t") and body[i].strip():
                val += " " + body[i].strip()
                i += 1
            if len(val) >= 2 and val[0] == val[-1] and val[0] in ("'", '"'):
                val = val[1:-1]
        out[key] = val.strip()
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    root = a.root.resolve()

    errors: list[str] = []
    notes: list[str] = []
    skills_dir = root / ".agents/skills"
    files = sorted(skills_dir.glob("*/SKILL.md"))
    real = len(files)
    if not real:
        errors.append(f"no SKILL.md files under {skills_dir}")

    seen: dict[str, str] = {}
    for f in files:
        rel = f.relative_to(root).as_posix()
        fm = parse_frontmatter(f.read_text(encoding="utf-8", errors="replace"))
        if fm is None:
            errors.append(f"{rel}: missing or unterminated YAML frontmatter")
            continue
        name, desc = fm.get("name", ""), fm.get("description", "")
        if not name:
            errors.append(f"{rel}: frontmatter has no `name`")
        if not desc:
            errors.append(f"{rel}: frontmatter has no `description`")
        if not name:
            continue
        if name in seen:
            errors.append(f"{rel}: duplicate name '{name}' (also {seen[name]})")
        seen[name] = rel
        if name != f.parent.name:
            errors.append(f"{rel}: name '{name}' does not match folder '{f.parent.name}'")

    counts: dict[str, list[int]] = {}
    for doc, (patterns, offset, required) in DOCS.items():
        p = root / doc
        if not p.exists():
            errors.append(f"{doc}: file not found")
            continue
        want = real + offset
        hits: list[tuple[int, int]] = []
        for ln, line in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            for pat in patterns:
                hits += [(ln, int(m.group(1))) for m in re.finditer(pat, line)]
        counts[doc] = [n for _, n in hits]
        if not hits:
            (errors if required else notes).append(f"{doc}: no skill count stated" + ("" if required else " (optional)"))
        for ln, n in hits:
            if n != want:
                errors.append(f"{doc}:{ln}: states {n} skills, expected {want}")

    for mf in ("marketplace.json", "plugin.json"):
        p = root / ".claude-plugin" / mf
        if not p.exists():
            notes.append(f".claude-plugin/{mf}: not present")
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f".claude-plugin/{mf}: invalid JSON ({e})")
            continue
        if mf == "plugin.json":
            paths = data.get("skills")
            paths = [paths] if isinstance(paths, str) else (paths or [])
            if not any(Path(root, s).resolve() == skills_dir.resolve() for s in paths):
                errors.append(".claude-plugin/plugin.json: `skills` does not include ./.agents/skills/")

    report = {"skills": real, "names_unique": len(seen) == real, "counts": counts,
              "errors": errors, "notes": notes, "ok": not errors}
    if a.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"skills found: {real} (.agents/skills/*/SKILL.md)")
        for doc, ns in counts.items():
            print(f"  {doc}: {', '.join(map(str, ns)) or '-'}")
        for n in notes:
            print(f"  note: {n}")
        for e in errors:
            print(f"  FAIL: {e}")
        print("OK" if not errors else f"FAILED: {len(errors)} problem(s)")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
