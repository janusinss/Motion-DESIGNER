# Benchmark: five fixed briefs

Proof that a change to the repo makes better films, not just different ones. Each repo version that changes how films are made (a skill, a gate, a rule) runs the same five briefs end to end through `video-director` and records the independent jury scores in `RESULTS.md`.

## Rules
- Run each brief exactly as written in `briefs/`, in a fresh session, with the defaults the brief states (no extra guidance from the operator). Answer the director's interview with the brief's "If asked" lines.
- The jury is `motion-critic` in a fresh subagent, design-blind, lens as stated in the brief, max 3 rounds, `critic_scan.py --cues` on the final.
- Record per brief: repo commit, engine, rounds, final lens total, the 8 dimension scores, FAIL/UNVERIFIED count, wall-clock time. Never edit an earlier row.
- Films go to `projects/bench-<id>-<commit>/` (only `final.mp4`, `NOTE.md`, source and cue sheet are kept; drafts and critic scans are gitignored).
- **Target**: median lens total ≥ 8.0 across the five, every film with zero FAIL. Baseline: 7.05 (one film, pre-Director 2.0).
- Compare versions with a blind A/B (`motionmaxxing/scripts/blind_review.py`) of the same brief, not only by score: a score can drift between juries.

## Briefs
| id | Type (Part C) | Length | Lens | File |
|---|---|---|---|---|
| b1 | C1b fast-paced hype launch | 20 s, 16:9 | Motion Awards | `briefs/b1-hype.md` |
| b2 | C2 ad | 15 s, 9:16 | CICLOPE | `briefs/b2-ad.md` |
| b3 | C3 explainer | 45 s, 16:9 | Staff Pick | `briefs/b3-explainer.md` |
| b4 | C4 logo sting | 6 s, 16:9 | Motion Awards | `briefs/b4-sting.md` |
| b5 | C9 data story | 30 s, 16:9 | D&AD | `briefs/b5-data.md` |
