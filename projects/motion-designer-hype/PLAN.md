# PLAN: Motion-DESIGNER hype cut (directed with video-director)

## 0. Concept pitch
| # | Kind | One sentence that predicts the screen | Cover-logo | Mute | Specific | Score /15 |
|---|---|---|---|---|---|---|
| Discarded | category costume | a clapperboard snaps, "Lights. Camera. AI." | ✗ | – | ✗ | – |
| A | montage of real material + scale jump | 59 real skill names pile up in chaos on the beat; Enter is pressed and they all snap into one ordered column under `video-director` | ✓ | ✓ | ✓ | 13 |
| B | UI documentary | one prompt typed into Claude Code; the pipeline log scrolls; a render appears; the jury scores it | ✓ | ✗ (log text unreadable at speed) | ✓ | 10 |
| C | typographic essay | AGENTS.md rules recited as kinetic type | ✗ | ✗ | ✗ | 6 |

**Chosen: A**: it owns its material (only this repo has these 59 names) and the drop performs the emotion delta. **Grafted from B**: the typed prompt and its Enter key are the cause of the snap.

**Engine lock (Move 4b)**: `motionmaxxing`. Engine-ban check: PASS vs Never-ship 1-12.
- No HUD or counters: the terminal fragment has no title bar or labels.
- No headline page: the only words are product input and output.
- No stat slide: 59 is never shown as a number.
- No colour flood: one ground for the whole film; the drop is a light event.
- No pinned object: the input line appears in one beat only.
- No web-footer end: name only, 0.6-1.4 s hold.

## 1. Director's treatment
- **Idea**: one prompt puts every tool in order.
- **Device**: the skill names themselves. Path: piled (chaos) → filed into one column (order) → the top row opens into the pipeline output → the output resolves into the name.
- **Grammar**: before Enter, every name sits at a random angle and depth. After Enter, everything moves only vertically, on the grid.
- **Logline**: fifty-nine tangled skill names snap into one line the instant you press Enter.
- **Hero moment**: 12.0-13.5 s (60-68 %). On the Enter press, all 59 names leave the pile and file into one column in 22 f (1 f stagger, whip ease, 40 px y smear). A key light opens over the column and `video-director` lands last on top in the accent. The screenshot frame is f 400.
- **System**: smooth 30 fps clock · directional smear on fast moves only · JetBrains Mono for product text, Inter 600 for the name only · accent `#FF5A1F` = "the one in charge" (`video-director`, then the name) · no carrier · no cursor · the overshoot is spent on the Enter key · scale spent on the hook dive and the name.
- **World**:
| Act | Ground | Light | Depth | Texture | Sound |
|---|---|---|---|---|---|
| 1 pile (0-12 s) | warm paper #ECE9E2 | dim, heavy vignette | names at 3 depths; near ones big and blurred | paper grain | pulse, hats, ticks on landings, rising build |
| 2 order (12-18 s) | same paper | key light pool over the column (light event at the drop) | one sharp plane | grain | drop: kick, bass, supersaw; whoosh on the file-in |
| 3 name (18-20 s) | same paper | pool narrows onto the name | one plane | grain | final hit, chord rings out |
- **Energy curve**: cuts at 30 f → 30 → 15 → 15 → 15 → 8 (build) · typing · 0.5 s breath · drop with the longest shot (3 s) · 2 echo proofs of 45 f · name.
- **Sound arc**: pulse + ticks → snare roll + riser → silence 11.5-12.0 s with keystrokes only → Enter click + impact + crash at 12.0 → full drop → final hit as the name lands → ring out.
- **Ending**: the last PASS line lands; the name arrives from 3.2x oversize, decelerating; hold about 1.1 s with a slow drift.

## 2. Format
1920x1080, 30 fps, 600 f, H.264 + AAC 48 kHz, -14 LUFS, ≤ -1.1 dBTP. Sources: `film/index.html` (motionmaxxing runtime) + `film/audio/mix.wav` (mgaudio, offline, deterministic).

## 3. Skill chain
`video-director` → `video-prompt-enhancer/references/creative-direction.md` (C1b) → `motionmaxxing` (runtime, render, look, lint) → `motion-design` (timings) → `mgaudio` (score + SFX) → `motion-critic` (independent jury).

## 4. Beats
| f | Role | Imp | Buys | Picture (text covered) | Motion | Seam | Sound |
|---|---|---|---|---|---|---|---|
| 0-90 | hook | 2 | there are too many tools | camera already diving through a cloud of mono names at random angles on paper | names crash in from 2.4x (snapSettle 8 f); camera drift + 2 hard reframes on beats | cut on an arriving name | pulse, ticks |
| 90-300 | build | 2 | each one has its own rules | macro crops of single names over a denser pile; cuts shorten 30 → 15 → 8 f | arrivals accelerate; scale jumps between crops | every cut lands on a name mid-arrival | hats, snare roll, riser |
| 300-360 | turn | 2 | you only have to say what you want | a terminal input line cropped by the frame, the prompt typed at real rhythm; then a 0.5 s held breath, caret alive | `M.type` prompt style; breath 345-360 | Enter press at 360, cut at max compression | keystrokes, silence |
| 360-450 | proof / hero | 3 | one prompt puts everything in order | all names file into one column; light opens; `video-director` lands on top in orange | 1 f stagger, whip 22 f, y smear; light kf | dive into the `video-director` row | impact, crash, whoosh, drop |
| 450-495 | proof | 2 | it checks your machine first | real `doctor.py` output printing line by line, macro | lines cascade 3 f apart | the READY line becomes the next frame's top line | blips |
| 495-540 | proof | 2 | it judges its own film | real `critic_scan.py` PASS lines for this film | cascade; each PASS ticks | the last line compresses into the name | ticks |
| 540-600 | name | 3 | this is Motion-DESIGNER | the name in Inter 600 in a narrow light pool | from 3.2x, snapSettle 20 f; drift to 0.96 | – | final hit, ring out |
