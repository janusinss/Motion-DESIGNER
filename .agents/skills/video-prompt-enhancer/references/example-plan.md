# Worked Example: Expected Depth of a Prompt-Plan

**Raw user input**: "make a launch video for my AI meeting notes app"

**Interview answers (Step 1)**: 30 s `16:9` + `9:16` cut · start feeling "drowning in meeting recaps" → end feeling "relieved, nothing missed" · bespoke HTML/GSAP from scratch (no URL) · zero-API-key audio.

**Invented specifics** (no brand supplied): app name **Margin**, mark = a single highlighter stroke, voice = dry, lowercase, exact. Non-obvious behaviour: unlike a transcriber that writes everything, Margin keeps only the decisions and who owns them.

---

````markdown
# Margin: "47 Minutes, 3 Lines": Director's Treatment & Production Plan

> **Execution Directive**: Build this film inside `Motion-DESIGNER` in strict order. Read every listed `SKILL.md` first. Protect the concept: if a technical shortcut would weaken the idea, device, grammar, or hero moment, stop and flag it instead. Do not mark complete until every QA gate and the creative review pass on real rendered media.

## 0. Concept Pitch
| # | Film Kind | One sentence that predicts the screen | Cover-logo | Mute | Specific | Score /15 |
|---|---|---|---|---|---|---|
| Discarded first idea | transformation chain | a waveform morphs into a glowing AI orb that spits out a summary card | ✗ | ✗ | ✗ | – |
| A | stillness that breaks | a full transcript page sits silent; one highlighter stroke crosses it and every unmarked line sinks away | ✓ | ✓ | ✓ | 13 |
| B | counter as spine | a meeting timer runs 00:00 → 47:12 while lines pile up, then collapses to "3" | ✓ | ✓ | ✗ (any summarizer) | 9 |
| C | joke with a character | a tired intern's notebook fills until the pen faints; Margin finishes the page | ✗ | ✓ | ✗ | 7 |

**Chosen: A**, because the highlighter is Margin's own UI state and its mark, so no competitor can run this film, and it builds in pure HTML/GSAP type. **Grafted from B:** the `47:12` timestamp as the opening's single number.

## 1. Director's Treatment
- **PAGE**: Problem: after a 47-minute call nobody remembers who owns what · Audience: team leads on a muted LinkedIn/X feed and the launch page, 30 s attention · Goal: "Margin keeps only the decisions"; click Try · Emotion: overwhelmed → relieved
- **The one true thing**: 47 minutes of transcript reduced to 3 owned decisions
- **Idea**: Only the decisions survive.
- **Device**: the yellow highlighter stroke (Margin's real highlight state) → path: cursor-thin stroke on line 212 → stroke marks decision 1 → 2 → 3 → the three strokes slide together into one → the stroke IS the Margin mark
- **Grammar**: nothing in the film is ever added; it only falls away. Element count strictly decreases after the turn.
- **Logline**: A highlighter crosses 47 minutes of transcript, and everything it misses sinks.
- **Idea sentence**: In this film, **the decisions Margin keeps** become **the only lines the highlighter touches**.
- **Hero moment**: 19.6 s (frame 588, 65 %): 1,400 unmarked transcript lines drop 1.2 H under gravity over 34 f with 6–40 px smear while 3 highlighted lines hold perfectly still at 0.5 W, 7 % H
- **System decisions**: Clock smooth 30 fps · Motion grammar directional smear on fast moves only · Type Söhne-class grotesk 400/550, lowercase sentence case, transcript 1.6 % H, statement 9 % H, hero line 16 % H · Accent `#FFE14D` = "kept" (only on the 3 decisions, never decorative) · Carrier: the stroke · Cursor: n/a (no UI chrome) · Overshoot: once, the mark's final 4 % settle · Scale spent on: the hero line at 16 % H and the macro push into line 212
- **World per act**:
  | Act | Ground | Light (+ light event) | Depth | Texture | Sound |
  |---|---|---|---|---|---|
  | 1 Problem | warm off-white paper `#F4F1EA`, dense transcript | soft window key from top-left, 3200 K | transcript planes at 3 depths, back plane 4 px blur | paper fibre + 0.03 grain | room tone, faint keyboard, a clock tick |
  | 2 Turn | same paper | key narrows to a pool following the stroke (light event) | foreground stroke sharp, page softens | ink bleed on highlight edges | tick stops; 0.6 s silence |
  | 3 Resolve | paper emptied to 3 lines, then the mark | pool opens back to full key | single plane, shadow under the mark | grain only | one soft felt-tip squeak + warm piano chord |
- **Energy curve**: 4.2 → 3.4 → 2.6 → 1.8 s beats → hero drop (1.1 s) → 2.8 s resolve
- **Sound arc**: room tone + tick → first hit = highlighter squeak on the turn (downbeat, 10.0 s) → 0.6 s silence at 18.9 s → low thud + chord on the hero drop (19.6 s) → music filters down as the mark forms → tail to digital silence by 30.0 s
- **Ending**: the three strokes slide together (cause: the last decision lands) into the single-stroke mark at 0.5 W; "margin" wordmark types in at 9 % H; 1.1 s alive hold, stroke edge breathing ±1 % W; final frame = poster
- **Banned for this film**: waveforms, AI orb/sparkle, robot, chat bubbles, calendar icons + all Part B tells

## 2. Format & Specs
- `1920x1080` (`16:9`) and `1080x1920` (`9:16`), `30 fps`, `30.0s` (`900` f), deliverables `film/final.mp4` + `film/final-9x16.mp4` + editable `film/index.html`
- Palette: paper `#F4F1EA` 80 % · ink `#1C1B19` 18 % · accent `#FFE14D` 2 % ("kept") · Typography as in Section 1; 9:16 safe zone keeps type inside the centre 80 % W
- Audio: Openverse CC0 solo piano track (licence + attribution logged in `film/NOTE.md`) at `-14 LUFS`, `≤ -1.1 dBTP`
- Constraints: no UI chrome or HUD, no numbered chapters, lowercase copy, real transcript text (not lorem ipsum)

## 3. Exact Ordered Skill Chain
1. `.agents/skills/motionmaxxing/SKILL.md`: primary engine; bespoke seek-safe HTML/GSAP typographic film from scratch, chosen over `cinetic` because the concept is an anti-template type essay, not a house-scene launch
2. `.agents/skills/motion-design/SKILL.md`: Premium personality, expo-out entrances, gravity ease-in on the fall, 1/3 choreography for the three decisions
3. `tools/openverse/openverse_client.py` + `librosa`: CC0 piano source + beat grid so the turn and the hero drop land on downbeats
4. Craft references: `.agents/skills/motionmaxxing/references/idea.md`, `director.md`, `type.md`, `world.md`, `close.md`
5. QA: `.agents/skills/motionmaxxing/scripts/look.py` + `scripts/lint.mjs` + `motion-design/reference/quality-checklist.md`

## 4. Shot-by-Shot Timeline
| # | Timecode (frames) | Role | Imp. | Buys: the viewer… | Picture (text covered) | Cause → Action → Result | Motion Spec | On-screen copy / VO | Seam Out | Sound Sync |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.0–4.2 s (0–126) | hook | 2 | feels the weight of a whole meeting before reading a word | a dense transcript page already scrolling up at frame 0, cropped on all four edges, warm paper | meeting runs → lines stack → page overflows the frame | continuous scroll 3 px/f accelerating to 9 px/f, ease-in quad; camera slow push 1.00 → 1.06 | `47:12` at 1.6 % H, top-left, the only legible text | scroll velocity 9 px/f carried into beat 2 | room tone, keyboard, clock tick on every 2nd beat |
| 2 | 4.2–7.6 s (126–228) | problem | 1 | recognises the pain: nobody can find what was decided | macro on the same page; lines blur past faster than reading | velocity rises → text becomes grey texture | scroll 9 → 22 px/f; 2–8 px vertical smear; push 1.06 → 1.35 | "who owns the launch date?" at 9 % H, lowercase, sits still while text rushes behind | line 212 slows into frame centre at 0.5 W | tick tightens to every beat |
| 3 | 7.6–10.2 s (228–306) | turn | 3 | sees the product act: something can find it | scroll brakes; one line holds at centre; a cursor-thin yellow stroke appears at its left edge | stop → stroke draws → line 212 is marked "kept" | scroll decel 22 → 0 px/f over 18 f, expo-out; stroke draws 0 → 100 % line width in 14 f, expo-out | "margin keeps the decisions." at 9 % H | stroke at 0.5 W, 7 % H, still | tick stops dead at 10.0 s; highlighter squeak on the stroke's first frame |
| 4 | 10.2–12.8 s (306–384) | proof | 2 | believes it finds more than one, with owners | camera pulls back 1.35 → 0.92; two more lines get stroked, owner names stay sharp | stroke 1 lands → page scrolls 640 lines → stroke 2 → 3 | pull-back 26 f, ease-in-out cubic; strokes 12 f each, expo-out, staggered 1/3 rule | owner names: "dana · launch date", "li · budget", "ops · vendor" at 2.4 % H | three strokes hold, page still full | two softer squeaks on downbeats |
| 5 | 12.8–15.2 s (384–456) | proof | 2 | trusts nothing was invented: these are real lines | rack focus: unmarked text softens to 6 px blur, decisions stay sharp | focus shift → unmarked text recedes | rack focus 20 f, ease-in-out sine; unmarked opacity holds at 100 % (no opacity-only state change) | none (picture carries it) | blur level 6 px carried | piano enters, low register |
| 6 | 15.2–18.9 s (456–567) | build | 1 | senses that something is about to give | page trembles 1–2 px; the pool of light narrows onto the three lines | light event → frame tension | light pool radius 1.0 → 0.45 H over 3.7 s, ease-in quad; tremor 1–2 px | "everything else?" at 9 % H, appears on its first word | tremor amplitude peaks at 2 px | piano holds a suspended chord; 0.6 s silence from 18.9 s |
| 7 | 18.9–20.0 s (567–600) | hero | 3 | feels the relief physically: the noise is gone | 1,400 unmarked lines drop out of frame under gravity; three highlighted lines hang perfectly still | silence ends → gravity releases → only decisions remain | fall 1.2 H over 34 f, gravity ease-in cubic; 6–40 px directional smear; three lines static | none | three lines static on empty paper | low thud + warm chord on frame 588 |
| 8 | 20.0–24.4 s (600–732) | promise | 2 | understands the value in one sentence | three lines on empty paper; pool reopens to full warm key | quiet → line reflows → statement | lines re-space 30 f, expo-out; statement types word by word at 5 f per word | "47 minutes. 3 lines. nothing missed." echoing the `47:12` hook | three strokes begin to slide toward centre | piano melody, sparse |
| 9 | 24.4–30.0 s (732–900) | cta | 2 | knows whose film this is and what to do | three strokes merge into one stroke = the Margin mark; wordmark beside it | last decision lands → strokes merge → mark forms | merge 20 f, expo-out with one 4 % overshoot settle; wordmark types 12 f; alive hold 1.1 s, stroke edge breathes ±1 % W | "margin" wordmark 9 % H · "try it on your next call." 5 % H | n/a (final frame = poster) | music filters down; felt-tip squeak on the merge; tail to silence |

## 5. Step-by-Step Build Commands
1. **Concept & audio**
   ```powershell
   .venv\Scripts\python.exe tools/openverse/openverse_client.py --type audio -q "solo piano minimal" --license cc0 -n 5 --json
   .venv\Scripts\python.exe -c "import librosa, json; y, sr = librosa.load('film/audio/music.wav'); t, b = librosa.beat.beat_track(y=y, sr=sr); json.dump({'tempo': float(t[0] if hasattr(t, '__len__') else t), 'beats': librosa.frames_to_time(b, sr=sr).tolist()}, open('film/beats.json', 'w'))"
   ```
2. **Build the hero first, then the film**
   ```powershell
   # copy .agents/skills/motionmaxxing/templates/film.html -> film/index.html and runtime/ -> film/runtime/
   node .agents/skills/motionmaxxing/scripts/render.mjs film/index.html --still 10.0,19.6,27.0 film/stills
   node .agents/skills/motionmaxxing/scripts/render.mjs film/index.html film/draft.mp4 --scale 0.5
   ```
3. **Render final with mixed audio**
   ```powershell
   node .agents/skills/motionmaxxing/scripts/render.mjs film/index.html film/final.mp4 --audio film/audio/music.wav --shutter 180 --subframes 8 --grain 0.03
   ```

## 6. Mandatory QA Gates & Creative Review
1. **Skill-native gates**
   ```powershell
   .venv\Scripts\python.exe .agents/skills/motionmaxxing/scripts/look.py film/final.mp4 --out film/look-final --expect 30 --expect-audio
   node .agents/skills/motionmaxxing/scripts/lint.mjs film/index.html
   ```
   Pass: G0 render/length/audio · G2 ≤ 3 flat frames · G3 end hold ≤ 1.4 s and CTA ≤ 25 % · G5 `lint.mjs` exit 0 · eye check of `film/look-final/sheet.jpg` logged in `film/NOTE.md`
2. **Stream & loudness**
   ```powershell
   ffprobe -v error -show_format -show_streams film/final.mp4
   ```
   Pass: `1920x1080` @ `30 fps`, `30.0s`, non-zero video + audio streams, `-14 LUFS`, `≤ -1.1 dBTP`
3. **Creative review on the rendered contact sheet**
   - [ ] Cover the logo: the highlighter-only-the-decisions idea still reads as Margin
   - [ ] Mute: full page → one stroke → everything falls → three lines → mark
   - [ ] Frame 0 already scrolling; no logo or title opener
   - [ ] Hero drop lands at 19.6 s and is the strongest frame
   - [ ] 2 of 9 beats at importance 3 (22 %); beats shorten toward the peak
   - [ ] Every seam carried by velocity, line 212, or the stroke; zero crossfades
   - [ ] Yellow only on kept decisions and the mark
   - [ ] Zero waveforms, orbs, sparkles, chat bubbles, or banned copy tells
   - [ ] Final frame reads as a poster at 480 px wide
````

**Strongest alternative**: B (counter as spine) if the user wants a harder, data-led tone.
**Most important editable assumption**: the app name and the highlighter mark; swap in the real brand's own UI highlight state.
