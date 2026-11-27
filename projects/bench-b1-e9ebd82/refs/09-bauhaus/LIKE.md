# Like this clip: the grammar to borrow

Measured from the clip (sha256 7938c337896f, 10 s) by scripts/like.py. These are targets for pace, rhythm, motion and proportion; the film
keeps its own idea sentence, its own direction from the deck, its own copy, colours and pictures.

## The rules

- Borrow grammar: shot lengths and cut rhythm, how often a cut lands on a sound, camera habits, the curve
  families of the main moves, how shots hand over, type scale and how much of the film carries text, motion
  density, the proportions of ground, ink and accent, the blur policy, the tempo.
- Never content: no shot retold one by one, no layout copied frame for frame, no text, no logo, no other
  company's colours (this file records ground tones and proportions, never the clip's hues), no footage, no
  music from the clip.
- The film keeps its own idea sentence and its own direction (python3 scripts/deck.py): the clip shapes the
  timing and the habits inside it, not the concept.
- Check the finished film: `python3 scripts/like.py guard --film out/film.mp4 --clip <clip>` must pass (the
  contact sheets at the same density must not read as a recreation).
- Score closeness to the clip instead of the house grammar: `node scripts/grammar-score.mjs --target out/like.json`.

## The grammar

- **Length and shots:** 10.0 s, 3 shots, median 2.0 s (middle half 2.0-4.0 s, longest 6.0 s), 0.2 cuts a second.
- **Picture changes:** 5 (every 1.633 s at the median, 0.5 a second), 60 % of them without a hard cut (a morph, a carried element, a move into the next layout): keep the rate with your own hand-overs.
- **Cuts and sound:** 100 % of cuts within a frame of a sound; 100 % on a beat, 100 % on a downbeat.
- **Tempo:** 120.06 BPM (track.py).
- **Camera:** moving in 38 % of the film, zooming in 29 %; median camera speed 21.1 px/s at 1080p.
- **Main moves:** 17 moves; front-loaded 24 %, symmetric 53 %, accelerating 24 %, constant 0 %.
- **Hand-overs:** 2 hard cuts, 0 carried, 0 flashes, 0 dips, 0 soft (no cut).
- **Type:** no text read with confidence (lines too unsure to count in 10 % of the film): set the type from the direction, not from the clip.
- **What the pictures show:** picture 4, graphic 2 (one frame of each picture; an estimate).
- **Density:** 2.25 starts a second, 1.992 running at once, idle 6 %.
- **Proportions:** ground 65 %, ink 9 %, accent 11 % of the frame; grounds light 90 %, dark 10 %.
- **Blur:** crisp (fast frames keep 95 % of the still sharpness).

## How to use it

1. Deal the direction as usual; read this grammar into it (shot lengths, the cut rhythm, the camera habits).
2. Write the timeline to the shot band and the cut placement above; set LOOK.blur to the blur policy.
3. Score each render against the clip: `node scripts/grammar-score.mjs --target out/like.json` (with look-audit.py's report).
4. Before delivery: `python3 scripts/like.py guard --film out/film.mp4 --clip <clip>` (with `--scaffold out/scaffold.mp4` when the
   film was made from a template): no frame retold, no composition re-skinned.
