# NOTE: Motion-DESIGNER hype cut

**Deliverable**: `film/final.mp4`, 1920x1080, 30 fps, 20.00 s, H.264 + AAC 48 kHz, -14.1 LUFS / -1.3 dBTP.
**Engine**: `motionmaxxing` (seek-safe runtime), score by `mgaudio`. Directed with `video-director` (playbook C1b).
**Source**: `film/index.html`, `film/audio/score.py`. Earlier versions are in `film/v1/` and `film/v2/`.

## Gates (final render)
- **look.py**: G0 PASS (20.00 s, audio present). G2 PASS (the 2-frame blackout at 12.0 s is a designed light-out on Enter). G3 PASS (final shot 10 %). Audio flags: none.
- **lint.mjs (G5)**: PASS. T1 warning: the typed prompt is headline-size product input, which is intended.
- **Motion.selfTest**: PASS (24 samples, 136 elements, 0 mismatches).
- **Contact sheet**: checked by eye at `film/look/sheet.jpg`. The stills at 12.2, 13.3, 15.9, 17.4/17.6 and 19.0/19.8 s were checked at full size.

## Independent jury (motion-critic, a fresh subagent each round, Motion Awards lens)
| Round | Render | Total | Checks | Main fixes made after it |
|---|---|---|---|---|
| r1 | draft2 | 6.65 | 1 FAIL (dead span at the end), 2 WARN (peak at 9.75 s, not at the hero) | Blackout + key light at Enter; camera punch centring `video-director`; accelerating cut grid; terminal text no longer clips; live end hold; moving grain |
| r2 | draft3 | 6.70 | all 11 PASS (peak 12.25 s = 61 %) | Longer 0.7 s file-in; list fades into the paper (no clipped rows); terminals at 56 px; READY kick; wordmark set in JetBrains Mono 700 |
| r3 | final | **7.05** | all 11 PASS | Cap reached (3 rounds) |

Round 3 scores: Idea 7, Story 8, Motion Craft 7, Design 7, World 6, Sound 8, Originality 6, Technical 8.
**Ship threshold not met**: the threshold is every dimension ≥ 8 with Idea and Motion Craft ≥ 9. The jury rated it a solid professional cut, not an award entry.

## What would move it (jury r3, not built)
1. **Hero as one move**: the 59 names snap into the column in one continuous, readable gesture with a 0.5 s hold. This is the biggest lever on Idea and Craft.
2. **Choreographed pile, 4-9.5 s**: at most ~7 sharp words, the rest pushed back, with three parallax speeds. The jury also suggested a 0→59 counter, but this film's ban check rules out counters and HUD, so that part is rejected.
3. **The 14.5-18 s proof beat**: show the typed sentence turning into a finished frame, instead of terminal readouts.
4. **The ending**: build the mark from the film's own material, for example the `›` prompt becoming the hyphen, plus a light bloom.
5. **The breath before the drop**: gate it to true digital silence from 11.65 to 11.95 s.

## What the test showed about the repo
- The pipeline ran end to end on Windows: preflight → direction → engine lock → hero first → gates → three independent jury rounds → delivery.
- **Gap found**: mgaudio needs `pedalboard`, which was not in the deps. It is now in `pyproject.toml`, `uv.lock` and `requirements.txt`, checked by `doctor.py`, and listed in AGENTS.md and INSTALLATION.md.
- **Gap found**: AAC encoding adds about 1.2 dB of true peak to transient-heavy mixes. Master to -2.5 dBTP when muxing to AAC. `score.py` does this.
- **Gap found**: two same-frame keyframes on a hard step are not seek-safe; selfTest caught it on the film grain. Hold each value for one frame instead.
- The critic lines on screen are real: they are this film's own r2/r3 check results.
- **Post-delivery source fix (seek safety)**: an every-frame `Motion.selfTest` (600/600) found 1 mismatch on `#cam` at f262, a same-frame camera cut. In `index.html` each shot's slow push now ends 1 frame before the next cut, which gives 0/600 mismatches; `lint.mjs` rule K1 now catches this. The cut keys use a hold-then-jump ease (`CUT`), so `--shutter` sub-frames inside the 1-frame gap never see an in-between pose. Without it, every act-1 cut got a smeared whip frame before it. `final.mp4` was re-rendered from this source with `--shutter 180 --subframes 8` (same pipeline). look.py G0/G2/G3 PASS, critic_scan all PASS, -14.1 LUFS / -1.3 dBTP. The only visible change from the earlier final is that each push ends 1 frame sooner.
