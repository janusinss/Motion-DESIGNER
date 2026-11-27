# NOTE · bench b1 · "One Line" · Motion-DESIGNER hype cut

`film/final.mp4`: 1920x1080, 30 fps, 20.000 s, H.264 + AAC 48 kHz stereo, -14.1 LUFS, -2.2 dBTP (ffprobe and critic_scan). Engine: **motionmaxxing** (seek-safe GSAP runtime). Repo commit e9ebd82. Run unattended per `bench/README.md`. The interview was answered from the brief's "If asked" lines. The hero was self-checked. No operator guidance.

## The one idea
The repo's own pile of skill names becomes one straight line. A flood of the 59 real `.agents/skills/` names (plus real script names and gate words) races past on a dark ground. Then it stops, and one prompt is typed in the breath. On Enter, the light flips and every name travels into a single line, while the eliminated ones leave the frame. The locked engine (`motionmaxxing`) is pulled out of the line in the one accent. The line opens into a window that plays this film's own frames ("One directed film out."). Then the line contracts and becomes the hyphen in **Motion-DESIGNER**.

## Beats (what each buys)
| Time | Beat | Buys |
|---|---|---|
| 0-2.5 s | flood of skill names on 3 depths, "So many ways to make a film." | too many ways in |
| 2.5-4.5 s | families in columns (blender-*, remotion-*) | the real scale |
| 4.5-6 s | scripts and flags crossing, "Which engine? Which cut?" | the real question |
| 6-7 s | 7 engines crash in from 3.5x | engines compete |
| 7-8 s | PASS / WARN / FAIL / UNVERIFIED stamped on the eighths | the gates pile up |
| 8-11 s | 1-beat, then 0.25 s cuts (shortest 0.17-0.25 s), densest wall | overwhelmed |
| 11-12 s | breath: dark pool, prompt typed, then 0.5 s of true silence | waiting with the person |
| 12-14.5 s | HERO: 2-frame light-out, cream key; 9 names snap into one line, 8 exit; the prompt grows to 76 px; `motionmaxxing` extrudes to ~150 px in orange | noise becomes one line: in control |
| 14.5-16 s | the line opens into a 16:9 window: three 0.25 s glimpses of this film, then it fills the frame | one directed film out |
| 16-20 s | the line contracts, pulls "Motion" and "DESIGNER" in from its ends, lands as the orange hyphen at 18.75 s; light sweep and breathe | the name |

## Real vs illustrative
- **Real**: the names in the dark act are the repo's real skill folders, script names, flags and gate words. Some names in the hero line and the ghosted breath (manim, blender, librosa, whisperx, ffmpeg) are real tools the repo uses, but they are not skill folders. The glimpses in the window are stills rendered from this film (`film/glimpse/`).
- **Illustrative**: the prompt "make a 20-second hype film" is the bench brief, paraphrased. No generated images.
- **Sound**: offline mgaudio `techno` recipe at 120 BPM (CC0 VCSL samples + synthesis), built by `film/audio/score.py`. No paid APIs.

## Gates (numbers quoted from scripts)
- `plan_check.py`: PASS (0 fail, 0 unverified); hero centre 66 %; shortest planned shot 0.25 s; breath planned.
- `look.py` (final):
  - G0 PASS (20.00 s, audio present).
  - G2 PASS (one 2-frame dip at 12.00 s, the designed light-out).
  - G3 PASS (final shot 4.00 s = 20 %; ends mid-motion).
  - Cut sync 77 % within ±80 ms.
  - Mean frame-to-frame luma 3.7/255, below the human band. That is a "notice it" question, not a gate.
- `lint.mjs` G5: PASS. Remaining WARNs: D1 left-anchored single words, which are the 6 s engine crash-ins and the mark words in motion.
- G1 / G4, by eye on `look-final/sheet.jpg` and full-size stills at 1.5, 8.0, 13.3, 15.0 and 19.5 s:
  - G1 PASS: the cream act's row is 28 px, the prompt 76 px and the pick about 150 px.
  - **G4 WARN**: at 6-7 s, 7 engine names share the frame at similar size.
  - **Collisions seen**: at 1.5 s, "film." overlaps a wall name (`blender-time-of-day`); at 8.0 s, "cinetic" is cropped by the right edge. These are not fixed (see below).
- `Motion.selfTest`: 600 random jumps, 0 mismatches, 1475 elements.
- `critic_scan.py --cues` (final), all 16 checks PASS, 0 FAIL, 0 UNVERIFIED:
  - peak 12.25 s (61 %), inside the hero span
  - hits_on_sound 4/4 within 53 ms
  - breath_quiet -90.4 dBFS
  - cut_audio_sync 75 %
  - energy CV 0.26
- The round-2 jury marked "audio tail to digital silence" UNVERIFIED because it judged sound from metrics only. Measured on `mix.wav`: the last 0.25 s peak at -32.0 dBFS, and the last 10 ms at -92.8 dBFS (the mgaudio 250 ms fade-out).

## Hero self-check (unattended bench, step 5)
- Hero clip `film/hero.mp4` (10.5-15 s, with sound). I stepped frames every 0.1 s from 11.9 to 13.1 s.
- The light-out, the scatter, the convergence into one line and the accent lift read as one continuous move (16-20 f) at speed.
- The drop's click and impact land on 12.0 / 12.067 s (onset 11.989 s).
- Verdict: reads at speed, sound on. No notes from anyone.
- After round 1, the hero type was enlarged (prompt 40 → 76 px, pick 31 → ~150 px).

## Jury (design-blind motion-critic, fresh subagents, Motion Awards lens)
| Round | Idea | Story | Craft | Design | World | Sound | Orig. | Tech | Lens |
|---|---|---|---|---|---|---|---|---|---|
| r1 (`film/v1`) | 7 | 7 | 7 | 7 | 7 | 7 | 6 | 8 | 6.95 |
| r2 (`film/v2` = final) | 7 | 7 | 7 | 7 | 7 | 7 | 6 | 8 | 6.95 |

- Blind A/B r1 vs r2, judged by a fresh subagent: it picked **r2, clearly**. Reasons: the hero pick reads instantly, the film-in-film callback lands, and the larger lockup works.
- Round 2 did not raise the total, so I stopped after 2 rounds, per motion-critic hard rule 7. Ship thresholds not met (every dimension ≥ 8, Idea + Craft ≥ 9).
- **Invalid assumption**: a held, still poster (≥ 0.5 s) at the hero satisfies the jury. Both juries read the 12.5-14.5 s hold as "a 0.25 s flash, then a still". They wanted the control half to keep moving, and to show a film being made rather than a word turning orange.

## What I would still improve (from the r2 fix list)
1. Keep the hero a move through 14 s (energy > 8). The poster should sit mid-move, not be a held still.
2. Show real directed output in the control half: a typeset title, a chart bar, a 3D turn, carried by the same snap move. Do not recycle the opening frames.
3. Make the build accelerate earlier (cuts at 2.0 / 1.2 / 0.7 s) and fix the text collisions: 1.5 s "film." over a wall name, 8.0-8.5 s "cinetic" cropped, and the 6.0 s smear under the question.
4. Make the lockup arrive by impact (the dash first, then the type slams in), and hold it for 1.0 s.
5. Make the 12 s drop the loudest event (+1 dB sub).

## Files
- Source: `film/index.html` (+ `film/runtime/`, `film/glimpse/`) and `film/audio/score.py`.
- Cue sheet: `cues.json`. Made by `cues.py from-events` from `film/v2/r2.mp4.events.json`. It was then **hand-patched**: `cues.py` read "poster holds 1.2 s" in the PLAN prose as the poster time (1.2), so I set `hero.poster` to 13.3 by hand.
- Plan: `BRIEF.md`, `PLAN.md`, `REFERENCES.md`, `refs/*/like.json`.
- Versions: `film/v1/` (r1 render + src), `film/v2/` (r2 render + src).
- Wall-clock: about 40 min (00:40 to 01:20).

## Blind A/B against the baseline (bench README rule)
- I ran `blind_review.py` on `critic/ab-baseline`, comparing the baseline `projects/motion-designer-hype/film/final.mp4` (a read-only copy in the scratchpad) with this film. Both are 20.0 s, so duration gave nothing away.
- A fresh subagent picked **this film (b1), slight margin**:
  - dark → light arc
  - a clearer problem statement
  - the orange pick as the overwhelmed → control moment
- What counted against it: the text collisions, small type on the cream act, and a long-feeling wordmark section. The baseline's terminal PASS lines were the reviewer's most concrete "proof of control".
- The jury totals point the other way (6.95 vs 7.05), within the drift the README warns about.

## After the run
- `text_overlap.mjs`, built after this run from its jury notes, reports **FAIL** on this film: the headline is covered at 0.4-2.4 s, 2.5-2.9 s, 7.1-8.0 s ("PASS") and 8.0-8.5 s ("cinetic"). The next bench run gates on it.
- `cues.json` poster was set to 13.3 s by hand; `cues.py` now reads it as 12.867 s (frame 386, the start of the held poster).
