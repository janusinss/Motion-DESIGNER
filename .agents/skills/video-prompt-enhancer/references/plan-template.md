# Directed Video Prompt-Plan Template

In **Step 3**, output **one single copy-pasteable fenced Markdown block** (` ```markdown ... ``` `) following this exact 5-section blueprint. Fill every field with concrete, project-specific values — zero placeholders (`<TBD>`, "nice easing", "cool visuals"). Do NOT output extra narrative walls outside the block.

---

## Output Blueprint

````markdown
# Video Production Plan: [Concise Project Title]

> **Execution Directive**: Follow this plan strictly in order inside `Motion-DESIGNER`. Read every listed `SKILL.md` before writing code, execute each build step with the exact local tools specified, and do not mark complete until every QA gate passes with real rendered media and visual contact-sheet inspection.

## 1. Creative Direction & Specs
- **Objective & Audience**: [1 concrete sentence on what the video achieves and who watches it]
- **Format**: `[WIDTH]x[HEIGHT]` (`[ASPECT]`), `[FPS] fps`, `[DURATION]s` total, deliverable `[MP4 / WebM / GIF / interactive HTML / GLB+MP4]`
- **Visual Identity**:
  - **Palette**: [Exact hex codes or brand URL capture source — avoid generic dark-mode blue/purple AI slop]
  - **Typography**: [Exact font pairing/hierarchy and safe-zone constraints]
  - **Motion Personality**: [Playful / Premium / Corporate / Energetic — exact easing curves, zero linear spatial motion, zero opacity-only transitions, 1/3 choreography compliance]
- **Audio & Timing Anchor**: [Exact source: Openverse CC0 + `librosa` beat grid / `whisperx` VO alignment / `mgaudio` or `music.mjs` offline synth / licensed human track / silent; loudness target `-14 LUFS`, `≤-1.1 dBTP`]
- **Hard Constraints**: [e.g., Manim `Text`/`MarkupText` only (no LaTeX), Remotion per-project `npx` scaffold, zero HUD/deck chrome, attribution logged for CC assets]

## 2. Exact Ordered Skill Chain
Read and apply these skills in strict sequence:
1. `[.agents/skills/<primary>/SKILL.md]` — [Exact ownership & why chosen over overlapping skills]
2. `[.agents/skills/<craft-or-secondary>/SKILL.md]` — [Exact craft/pipeline contribution]
3. `[.agents/skills/<audio-or-3d-or-compositing>/SKILL.md or resource/tool]` — [Only include tools that genuinely elevate this video]
4. `[.agents/skills/<qa-skill>/SKILL.md]` — [Exact pre-delivery verification gate]

## 3. Shot / Beat Timeline
| Timecode | Beat / Shot | Visual Action & Composition | Motion / Camera / Easing | Audio / SFX / Caption Sync |
|---|---|---|---|---|
| `0.0s–2.5s` | Hook | [Concrete visual frame & focal anchor] | [Curve + entry choreography] | [Beat 1 hit / opening hook words] |
| `2.5s–...` | [Beat 2] | [Concrete visual action] | [Transition seam & curve] | [Synced SFX / VO words] |
| `...` | [Climax / Hero] | [Hero moment — real UI / 3D pass / VFX] | [Camera move / timing] | [Peak beat / caption emphasis] |
| `[End]` | CTA / Resolve | [Final lockup; end hold ≤1.4s, final shot ≤25% if `motionmaxxing`] | [Settle curve] | [Tail resolve / clean fade] |

## 4. Step-by-Step Build Commands
Execute atomically (one action per step):
1. **Acquire / Prep Assets & Audio**:
   ```powershell
   # Exact verified commands (e.g., openverse_client.py, brand.mjs, librosa beat extraction, whisperx alignment, or mgaudio/music.mjs)
   ```
2. **Build Core Visuals / 3D / Scenes**:
   ```powershell
   # Exact verified commands (e.g., Remotion scaffold, HTML/GSAP build, Manim CLI, run_in_blender.py, three.quarks/tweakpane app, or effectcraft-cli)
   ```
3. **Sync, Composite & Render Final Output**:
   ```powershell
   # Exact verified render & ffmpeg mux commands producing the final deliverable path
   ```

## 5. Mandatory QA Gates & Pass Criteria
Run every gate below on real rendered output (never self-certify from source code):
1. **Skill-Native Automated Gate(s)**:
   ```powershell
   # Exact verified script(s) from catalog.md (e.g., look.py + lint.mjs / qa_check.py + review_shots.py / precheck.mjs + av-audit.py / gate.mjs + ship.mjs / compare.ts + sheet.ts)
   ```
   - **Pass Condition**: [Exact numeric/boolean criteria from catalog.md]
2. **Stream, Loudness & Visual Contact-Sheet Gate**:
   ```powershell
   ffprobe -v error -show_format -show_streams <output.mp4>
   ```
   - **Pass Condition**: Non-zero video/audio streams matching `[WIDTH]x[HEIGHT]` @ `[FPS] fps` and `[DURATION]s`; audio `-14 LUFS`, `≤-1.1 dBTP` (if audio present); contact sheet visually inspected with zero flat/blank/clipping/overlap defects.
````

---

## Quality Checklist (Verify Silently Before Sending)

- Single copy-pasteable fenced `markdown` block containing all 5 numbered sections?
- Every `SKILL.md` path, script path, and CLI flag matches `references/catalog.md` verbatim?
- Zero unnecessary skills forced in; every included skill has a clear role in Section 2 AND an executable step in Section 4?
- Every shot in Section 3 has concrete visual action, easing/motion intent, and audio/caption alignment?
- Section 5 includes both automated script gates AND visual contact-sheet inspection with hard numeric thresholds?
