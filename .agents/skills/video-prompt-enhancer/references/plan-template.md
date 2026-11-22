# Directed Video Prompt-Plan Template

In **Step 4**, output **one copy-pasteable fenced Markdown block** following this 7-section blueprint. Fill every field with concrete, project-specific values: no `<TBD>`, no "nice easing", no "cool visuals". See `references/example-plan.md` for the expected depth.

---

## Output Blueprint

````markdown
# [Film Title]: Director's Treatment & Production Plan

> **Execution Directive**: Build this film inside `Motion-DESIGNER` in strict order. Read every listed `SKILL.md` first. Protect the concept: if a technical shortcut would weaken the idea, device, grammar, or hero moment, stop and flag it instead. Do not mark complete until every QA gate and the creative review pass on real rendered media.

## 0. Concept Pitch
| # | Film Kind | One sentence that predicts the screen | Cover-logo | Mute | Specific | Score /15 |
|---|---|---|---|---|---|---|
| Discarded first idea | [category costume] | [the obvious version] | ✗ | – | ✗ | – |
| A | [kind] | [sentence] | ✓/✗ | ✓/✗ | ✓/✗ | [n] |
| B | [kind] | [sentence] | ✓/✗ | ✓/✗ | ✓/✗ | [n] |
| C | [kind] | [sentence] | ✓/✗ | ✓/✗ | ✓/✗ | [n] |

**Chosen: [A/B/C]**, because [one line on ownership + buildability]. **Grafted from [loser]:** [one element].

## 1. Director's Treatment
- **PAGE**: Problem [situation] · Audience [who, where, state] · Goal [one action/thought] · Emotion [start → end]
- **The one true thing**: [real feature / behaviour / number this film is built on]
- **Idea** (≤ 8 words): [...]
- **Device**: [owned object with states] → path: [link → link → link → mark]
- **Grammar** (the rule the form obeys): [...]
- **Logline** (≤ 15 words, seen): [...]
- **Idea sentence**: In this film, **[only-this-subject thing]** becomes **[device]**.
- **Hero moment** (the screenshot frame): [frame/timecode at 60–75 %], made by [≥ 3 quantities: frames, px, degrees, factors]
- **System decisions**: Clock [smooth 30 / on twos / 60] · Motion grammar [smear / crisp / shutter] · Type [family, weights, role scale % H] · Accent [hex] = [one meaning] · Carrier [object or none] · Cursor [design or n/a] · Overshoot spent on [one object] · Scale spent on [one or two moments]
- **World per act**:
  | Act | Ground | Light (+ light event) | Depth | Texture | Sound |
  |---|---|---|---|---|---|
  | 1 | | | | | |
  | 2 | | | | | |
  | 3 | | | | | |
- **Energy curve**: [beat lengths shortening toward the peak, e.g. 4.0 → 3.2 → 2.4 → 1.6 s → hero → 2.5 s resolve]
- **Sound arc**: world sound [...] → first hit [beat, downbeat] → silence [where, how long] → drop [hero moment] → subtraction into the lockup → tail to digital silence
- **Ending**: the mark arrives by [cause], built from [last element], hold [0.6–1.4 s] with [living element]; final frame = poster
- **Banned for this film**: [5 category clichés] + Part B tells

## 2. Format & Specs
- `[W]x[H]` (`[aspect]`), `[fps] fps`, `[duration]s` (`[frames]` f), deliverables `[MP4 / 9:16 cut / loop / HTML / GLB]`
- Palette: [hex + role + proportion] · Typography: [family, sizes in % H, safe zones]
- Audio: [source + licence/attribution] at `-14 LUFS`, `≤ -1.1 dBTP`
- Constraints: [e.g. Manim `Text` only, Remotion per-project `npx`, no HUD/chrome, real UI only]

## 3. Exact Ordered Skill Chain
1. `[.agents/skills/<primary>/SKILL.md]`: [ownership + why over overlapping skills]
2. `[.agents/skills/motion-design/SKILL.md]`: [curves, choreography, timing tables]
3. `[audio / 3D / VFX / compositing skill or tool]`: [only if the concept needs it]
4. `[craft references to read]`: [e.g. motionmaxxing `references/idea.md`, cinetic `references/concept-and-story.md`]
5. `[QA skill / scripts]`: [exact gate]

## 4. Shot-by-Shot Timeline
| # | Timecode (frames) | Role | Imp. | Buys: the viewer… | Picture (text covered) | Cause → Action → Result | Motion Spec (curve, duration, travel, camera) | On-screen copy / VO | Seam Out (carried element + exit state) | Sound Sync |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.0–[x]s ([f]) | hook | 2 | | | | | | | |
| 2 | | turn | 2 | | | | | | | |
| 3 | | proof | 3 (hero) | | | | | | | |
| 4 | | cta | 1 | | | | | | | |

## 5. Step-by-Step Build Commands
1. **Concept & assets**
   ```powershell
   # verified commands: brand.mjs / deck.py / openverse_client.py / librosa beat grid / whisperx / mgaudio / music.mjs
   ```
2. **Build scenes / 3D / VFX**
   ```powershell
   # verified commands: Remotion npx scaffold / HTML-GSAP build / manim / run_in_blender.py / three.quarks app / effectcraft-cli
   ```
3. **Sync, composite, render**
   ```powershell
   # verified render + ffmpeg mux producing the final path
   ```

## 6. Mandatory QA Gates & Creative Review
1. **Skill-native gates**
   ```powershell
   # exact scripts from catalog.md
   ```
   Pass: [numeric/boolean thresholds]
2. **Stream & loudness**
   ```powershell
   ffprobe -v error -show_format -show_streams <output.mp4>
   ```
   Pass: `[W]x[H]` @ `[fps]`, `[duration]s`, non-zero streams, `-14 LUFS`, `≤ -1.1 dBTP`
3. **Creative review on the rendered contact sheet** (every box must be YES)
   - [ ] Cover the logo: still unmistakably this brand/subject
   - [ ] Mute: picture alone tells problem → result
   - [ ] Frame 0 in motion; no logo/title opener
   - [ ] Hero moment lands at [timecode] and is the strongest frame
   - [ ] ≤ 25 % of beats at importance 3; beats shorten toward the peak
   - [ ] Every seam carried; zero crossfades or flashes
   - [ ] Accent appears on ≤ 1 element per scene with one meaning
   - [ ] Zero banned props, copy tells, or visual tells
   - [ ] Final frame works as a poster at 480 px wide
````

---

## Quality Checklist (Verify Silently Before Sending)

- One fenced `markdown` block with Sections 0–6, nothing generic left.
- Section 0 shows three concepts of different kinds with honest test results and a reasoned pick.
- Section 1 names a device with states, a grammar, a hero moment with ≥ 3 quantities, and a world per act.
- Every timeline row has Buys, picture-with-text-covered, cause → action → result, a curve + duration, a seam, and a sound cue.
- Every path, script, and flag matches `references/catalog.md` / `references/creative-direction.md`.
