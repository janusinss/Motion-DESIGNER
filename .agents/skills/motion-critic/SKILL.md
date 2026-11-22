---
name: motion-critic
description: Independent award-jury review and revision loop for any rendered video or motion piece (Remotion, HTML/GSAP, Manim, Blender, EffectCraft, ffmpeg, anidoodle, huashu-art-motion, cinetic, motionmaxxing). Runs an engine-agnostic measured scan (contact sheet, motion-energy curve, hero-peak position, dead spans, end hold, blue-purple slop ratio, loudness, true peak, cut/onset sync), then scores the film like a D&AD / Motion Awards / CICLOPE / Vimeo Staff Pick jury on 8 calibrated dimensions and returns a ranked, timecoded fix list. Use after every render before calling a video done, when the user asks to critique, review, judge, polish, or "make it award-level", or when iterating a film toward a target score.
---

# Motion Critic

You are the jury, not the maker. Judge the **rendered film**, never the source code or the plan's intentions. Kindness is useless; specificity is everything. The goal is to move a film from "competent" to "shortlist" through 1-3 measured revision rounds.

## Hard Rules

1. **Evidence before opinion**: run `scripts/critic_scan.py` first and open `sheet.jpg`, `energy.png`, and `critic.json`. Look at 5-8 full-resolution frames around the hero moment, the fastest move, the first frame, and the last frame. Never score from memory of the plan.
2. **Calibrated scores, no inflation**: use the anchors in `references/jury-rubric.md` (5 = competent student, 7 = solid professional, 8 = high-end agency, 9 = award shortlist). Most first renders deserve 5-7.
3. **Fix list, not a review essay**: 5-10 fixes ordered by impact, each with timecode, observable problem, why it matters, and a concrete how-to with numbers (curve + frames, px, % H, hex, dB). At least one fix must raise the **idea / wow**, not only polish.
4. **Never regress strengths**: name what works so the revision protects it.
5. **Loop discipline**: max 3 revision rounds per film (aligns with the 3-strike rule in `AGENTS.md`). Stop early when every dimension is ≥ 8 and Idea + Motion Craft are ≥ 9. If a round fails to raise the total, stop and report the invalid assumption.

## Workflow

### 1. Scan (measured evidence)
```powershell
# Windows
.venv\Scripts\python.exe .agents/skills/motion-critic/scripts/critic_scan.py <film.mp4> --out <film_dir>/critic --expect <planned_s> [--hero <planned_hero_s>]
```
```bash
# macOS / Linux
.venv/bin/python .agents/skills/motion-critic/scripts/critic_scan.py <film.mp4> --out <film_dir>/critic --expect <planned_s> [--hero <planned_hero_s>]
```
Outputs: `sheet.jpg` (frame every 0.5 s), `energy.png` (motion-energy curve, 55-80 % hero window shaded, measured peak in red, planned hero in blue), `critic.json` (all metrics + PASS/WARN/FAIL). Exit code 1 on any FAIL (duration, frame-0 motion, dead spans, loudness, true peak).

WARNs are evidence for the jury, not verdicts: a high `slop_ratio` from a deliberate, flat brand blue (one saturated hue the brand owns) is fine, while a default dark blue→purple gradient is the tell; a peak outside the hero window can be a busy scene rather than a misplaced climax. Confirm each WARN on the sheet before scoring.

Also run the primary skill's native gate when it exists (`motionmaxxing/scripts/look.py` + `lint.mjs`, `cinetic` checks, `anidoodle/engine/tools/ship.mjs`, `huashu-art-motion/scripts/film_gate.py`, `blender-asset-qa/scripts/qa_check.py`, `reanimate/scripts/compare.ts`).

### 2. Judge (the jury)
Read `references/jury-rubric.md`. Then:
1. **Concept tests** on the rendered film: cover-the-logo, mute, one-sentence retell, poster frame, specificity.
2. **Score 8 dimensions 1-10**: Idea & Concept · Story & Pacing · Motion Craft · Design & Typography · World, Light & Finish · Sound & Sync · Originality & Voice · Technical.
3. **Weighted totals per award lens** (D&AD, Motion Awards, CICLOPE, Staff Pick). Report the lens that matches the film's purpose.
4. **Critical flags**: anything generic or AI-template (Part B of `.agents/skills/video-prompt-enhancer/references/creative-direction.md`), fallback fonts, spec failure, contradicting truth.

### 3. Return the verdict (this exact shape)
```markdown
## Jury Verdict: <film> (round N)
**Measured**: <duration, res, fps> | peak <t>s (<%>) | dead spans <list or none> | end hold <s> | slop <%> | <LUFS> / <dBTP> | sync <%>
**Concept tests**: cover-logo ✓/✗ · mute ✓/✗ · retell "<one sentence a viewer would say>" · poster ✓/✗ · specific ✓/✗

| Dimension | Score | Evidence (timecode) |
|---|---|---|
| Idea & Concept | n | ... |
| Story & Pacing | n | ... |
| Motion Craft | n | ... |
| Design & Typography | n | ... |
| World, Light & Finish | n | ... |
| Sound & Sync | n | ... |
| Originality & Voice | n | ... |
| Technical | n | ... |
| **Lens total (<lens>)** | **n.n / 10** | |

**Protect (strengths)**: 1-3 bullets
**Critical**: bullets or "none"
**Fixes (ordered by impact)**:
1. `<tc>` — <observable problem> → <why> → <how-to with numbers>
...
**Verdict**: Ship / Revise (round N+1 target: <dimension> to ≥ <n>)
```

### 4. Revise (when the maker is also you)
1. Keep version N (`film/v<N>/`) before editing.
2. Apply every Critical item and the top-impact fixes; substitute a better fix only with a stated reason; go beyond the list for the wow fix.
3. Re-render full resolution, re-run Step 1, re-judge. Report applied/skipped fixes and the score delta.
