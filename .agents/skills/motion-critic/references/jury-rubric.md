# Jury Rubric (Calibrated)

Distilled from how D&AD (idea inspiring? brilliantly executed? does the medium elevate the idea?), The Motion Awards (concept, design, craft), CICLOPE (craft and direction of motion first) and Vimeo Staff Pick (voice, originality, pacing, polish) evaluate moving image, plus the jury prompt in `resources/mg-styles-15/rubric.md`.

## Score Anchors (all dimensions)
| Score | Means |
|---|---|
| 3-4 | broken or confused; reads as unfinished |
| 5 | competent student work; template-level idea |
| 6 | decent template; nothing wrong, nothing memorable |
| 7 | solid professional; a client would approve it |
| 8 | high-end agency; other designers would notice |
| 9 | award shortlist; people send it to each other |
| 10 | best in the world this year |

Most first renders land 5-7. A 9 needs a specific, nameable reason.

## The 8 Dimensions

### 1. Idea & Concept
- 9: one owned idea a viewer retells as an image ("the highlighter that let everything else fall"); the device carries every shot; passes cover-logo, mute, specificity.
- 7: clear message and structure, but the idea could belong to a competitor.
- 5: a topic, not an idea; feature tour; transformation chain by default.
- Evidence: retell sentence, device path visible on the sheet, poster frame.

### 2. Story & Pacing
- 9: frame 0 in motion; beats shorten toward the peak; one hero at 55-80 %; designed breath before the payoff; ending arrives by cause and lands smaller than the climax.
- 7: readable arc, but uniform beat lengths or a soft middle.
- 5: equal-energy beats, logo opener, slide-deck rhythm, ending fades out.
- Evidence: `energy.png` contour, `energy_cv`, `peak_fraction`, `dead_spans_s`, `static_tail_s`.

### 3. Motion Craft
- 9: zero linear spatial motion; spacing, anticipation, overlap, follow-through, arcs; one motion grammar (smear / crisp / shutter); one overshoot payoff; every seam carried at velocity.
- 7: clean eases but generic curves; a few crossfades; some popping.
- 5: linear tweens, opacity-only state changes, jitter, everything bounces.
- Evidence: filmstrips around the fastest move; `.agents/skills/motion-design/reference/quality-checklist.md`.

### 4. Design & Typography
- 9: strong grid and hierarchy; scale is hierarchy (not weight); one accent with one meaning; type in the brand's voice; negative space used as a beat.
- 7: tidy but safe; a second accent creeping in; title-case benefit copy.
- 5: centred title pages, clutter, fallback fonts, copy tells ("Not just X. It's Y.").
- Evidence: full-res frames; banned copy list in `creative-direction.md` Part B.

### 5. World, Light & Finish
- 9: every act has ground + light + depth + texture; a light event per act; no banding/aliasing; material feels physical.
- 7: attractive but flat in places; a card on a void in one beat.
- 5: flat swatch grounds, glow on everything, default blue-purple gradient.
- Evidence: sheet frames; `slop_ratio`.

### 6. Sound & Sync
- 9: sound is direction: world sound, silence before the payoff, drop on the hero, subtraction into the lockup; cuts land on onsets; -14 LUFS ±1, ≤ -1 dBTP; tail to digital silence.
- 7: well-mixed library track, loosely synced.
- 5: music wallpaper; no SFX; clipping; picture ignores the beat.
- Evidence: `audio.integrated_lufs`, `audio.true_peak_dbtp`, `cut_audio_sync`.

### 7. Originality & Voice
- 9: a stylistic decision nobody else in the category would make, justified by the idea; zero category clichés.
- 7: well-executed current trend.
- 5: derivative of a known template or of AI-default aesthetics.
- Evidence: cover-logo / competitor-swap test; banned props list.

### 8. Technical
- 9: exact spec (duration, res, fps), fonts loaded, no dropped frames, clean encode, safe zones respected.
- 5: spec drift, tofu glyphs, black frames, popping assets.
- Evidence: `critic.json` probe + checks; primary skill's native gate.

## Award Lens Weights (sum = 1.0)
| Dimension | D&AD | Motion Awards | CICLOPE | Staff Pick |
|---|---|---|---|---|
| Idea & Concept | 0.25 | 0.20 | 0.10 | 0.15 |
| Story & Pacing | 0.10 | 0.10 | 0.10 | 0.15 |
| Motion Craft | 0.15 | 0.20 | 0.25 | 0.10 |
| Design & Typography | 0.10 | 0.15 | 0.10 | 0.10 |
| World, Light & Finish | 0.10 | 0.10 | 0.20 | 0.10 |
| Sound & Sync | 0.10 | 0.10 | 0.10 | 0.10 |
| Originality & Voice | 0.15 | 0.10 | 0.10 | 0.25 |
| Technical | 0.05 | 0.05 | 0.05 | 0.05 |

Pick the lens by purpose: commercial launch/ad → D&AD · motion/brand/explainer → Motion Awards · craft showpiece, 3D, VFX, music video → CICLOPE · personal/art/loop/short → Staff Pick.

## Ship Thresholds
- **Ship**: every dimension ≥ 8, Idea and Motion Craft ≥ 9, zero FAIL checks, zero Critical flags.
- **Revise**: anything below; next round targets the two lowest-weighted-gap dimensions first.
- **Stop (3 rounds or no gain)**: report the invalid assumption and a 2-option choice per `AGENTS.md` Strike 3.

## Fix-Writing Patterns (concrete, numeric)
- Weak: "Make the ending better." → Strong: "`27.0s` logo fades in from nothing → no cause, reads as template → build the mark from the three strokes merging over 20 f expo-out, hold 1.1 s with a ±1 % W breathing edge."
- Weak: "Pacing feels slow." → Strong: "`8–16s` four beats at ~2.0 s each (`energy_cv` 0.09) → equal energy, no arrival → shorten to 2.6 / 2.0 / 1.4 / 1.0 s and move the hero drop to 63 %."
- Weak: "Add more polish." → Strong: "`4.0–7.6s` flat `#F4F1EA` ground → card-on-void → add 0.03 grain, a window key from top-left, and a 4 px-blurred back transcript plane at 0.6 opacity."
