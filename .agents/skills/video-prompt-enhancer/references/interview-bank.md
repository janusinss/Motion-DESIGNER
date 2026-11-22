# Dynamic Interview Bank

Use this reference in **Step 1** to ask **2 to 4** sharp, non-redundant scoping questions tailored to the user's raw input.

## Selection Rules

1. **Never repeat answered specs**: If the user already specified duration (`30s`), aspect (`9:16`), reference URL, or engine (`Remotion`), skip that dimension and use the slot for a higher-leverage creative or technical decision.
2. **Hard cap: 2–4 questions**:
   - Clear input with strong anchor (e.g., URL + duration + style) → ask **2** surgical questions (Audio/Sync + Output/Stack nuance).
   - Broad/vague input (e.g., "make a cool video for my app") → ask **4** questions covering Format/Duration, Visual Direction/Archetype, Audio/Voice Strategy, and 3D/VFX Depth.
3. **Always provide a `(Recommended)` first option** grounded in the strongest synergy in `references/catalog.md`.
4. **Offer concrete, mutually exclusive choices** — never ask open-ended essays like "What vibe do you want?"
5. **At least ONE creative question per interview** (from the Creative Question Bank below). Technical specs can be defaulted; the emotional delta and the one true thing cannot be invented as well as the user can supply them.

---

## Creative Question Bank (pick at least 1)

- **Q-Emotion-Delta** — "Where should the viewer start and end emotionally?"
  - Overwhelmed → relieved *(Recommended for productivity/tools)* | Sceptical → convinced | Bored → delighted/amused | Curious → in awe
- **Q-One-True-Thing** — "Which single fact should the whole film be built on?"
  - One real number (e.g. 47 min → 3 lines) *(Recommended)* | One non-obvious behaviour ("unlike X, it…") | One real user moment | The name's meaning / the logo's shape
- **Q-Voice** — "How does this brand/creator sound?"
  - Dry, exact, understated *(Recommended for premium)* | Warm and human | Playful and cheeky | Bold and cinematic
- **Q-Concept-Kind** — "Which kind of film fits best?" (map to `creative-direction.md` Move 3)
  - Let the director pick the strongest after kill tests *(Recommended)* | UI documentary of one real task | Typographic essay | Joke with a character | Stillness that breaks | One unbroken take | Montage of real output
- **Q-Restraint** — "How loud should the craft be?"
  - Quiet confidence: one hero moment, everything else restrained *(Recommended)* | Maximal spectacle with a 3D/VFX hero | Raw, handmade, imperfect texture

## Video Type → Playbook Map (`creative-direction.md` Part C)

| Signals in raw input | Playbook | Archetype section below |
|---|---|---|
| launch, release, "v2 is out", SaaS, new feature | C1 Launch Film | §1 |
| ad, commercial, spot, bumper, 15 s / 30 s | C2 Advertisement | §1 |
| explainer, how it works, educational, onboarding | C3 Explainer | §4 / §5 |
| logo animation, sting, ident, intro | C4 Brand Sting | §1 |
| reel, TikTok, Shorts, vertical, social | C5 Social Short | §1 / §3 |
| demo, walkthrough, tutorial, feature loop | C6 Product Demo | §1 / §2 |
| title sequence, opening credits, intro for a film/show | C7 Title Sequence | §3 / §7 |
| music video, lyric video, visualizer | C8 Music / Lyric | §3 / §6 |
| data, statistics, report, infographic | C9 Data Story | §5 |
| art, generative, loop, abstract, NFT, style piece | C10 Art / Loop | §3 / §6 |
| teaser, countdown, event, coming soon | C11 Teaser | §1 |
| 3D product, render, turntable, hero shot | C12 3D Product Hero | §7 |

Type-specific scoping questions for C2, C5, C7, C8, C9, C11 that are not covered below:
- **C2 Ad — Q-Spot-Length**: 30 s story spot *(Recommended)* | 15 s single idea | 6 s bumper (thumbnail-legible) | 30 + 15 + 6 cut-down set
- **C5 Social — Q-Hook-Style**: Pattern interrupt in the first 0.5 s *(Recommended)* | Seamless loop re-watch | Punchline at the end
- **C7 Title — Q-Motif**: An object from the story's world *(Recommended)* | Typography-in-environment | Abstract graphic system
- **C8 Music — Q-Visual-Rule**: One visual rule per song section *(Recommended)* | Kinetic lyrics as the picture | Audio-reactive generative visuals
- **C9 Data — Q-Hero-Number**: One shocking number opens the film *(Recommended)* | A comparison (before/after) | A trend over time
- **C11 Teaser — Q-Reveal**: Partial glimpse of the mark + date *(Recommended)* | Pure mood, name only at the end | Countdown series

---

## Archetype Detection & Dynamic Question Matrix

### 1. Commercial Product Launch / Feature Promo / Update Film
*Signals: "launch", "v2 is out", "SaaS", "product demo", "brand URL", "ad", "promo", "sting", "CTA"*

- **Q-Engine/Style**:
  - *(Recommended if brand URL provided)* Bespoke anti-template brand film in seek-safe HTML/GSAP (`motionmaxxing` + URL brand capture)
  - Structured SaaS launch/update film in Remotion 4 with dealt house scenes & official logos (`cinetic` + `remotion-*`)
  - Custom editable React video app / `<Player>` (`remotion-best-practices` + `remotion-interactivity`)
- **Q-Format**: `16:9` 1080p 30–45s hero launch *(Recommended)* | `9:16` 15–20s social cut | `1:1` 15s feature loop | Multi-aspect (`16:9` + `9:16`)
- **Q-Audio**:
  - Zero-API-key CC0 track via Openverse + `librosa` beat sync *(Recommended for zero keys)*
  - Voiceover script + `whisperx` word-level captions + ducked music bed
  - ElevenLabs VO + SFX + beat-sync (`motionmaxxing`, requires API key) / Licensed human track (`cinetic`)
  - Procedural offline synth score (`mgaudio` / `music.mjs`, `-14 LUFS`)
- **Q-Hero-Visual**: Real captured product UI + kinetic type *(Recommended)* | Hybrid Blender 3D hero shot + 2D UI overlay | Real-time Three.js/`three.quarks` particle hero

### 2. Reference Clone / Motion Reverse-Engineering
*Signals: "clone", "steal", "match this", "same animation as", URL/MP4/GIF/Lottie reference*

- **Q-Fidelity**:
  - Motion-faithful (±80ms timing/easing parity, adapted to your brand/content) *(Recommended)*
  - Pixel-faithful (≤2% pixel mismatch, exact fonts/colors/spacing)
  - Hybrid (pixel-faithful layout + custom copy/theme)
- **Q-Target-Stack**: React + GSAP *(Recommended)* | Vanilla HTML/CSS/GSAP | Remotion composition | React Three Fiber / Three.js (`--gl` capture)
- **Q-Polish**: Raw parity match only | Match first with `reanimate`, then polish micro-interactions/accessibility with `motion-design` *(Recommended)*

### 3. Artistic Code-Drawn Film / Style Piece / Drawing Lesson
*Signals: "illustration", "art style", "anidoodle", "bauhaus", "cel", "collage", "liquid", "synthwave", "drawing lesson", "10s loop"*

- **Q-System**:
  - Full deterministic story/lesson/art film in 32 styles with offline HTML player (`anidoodle`) *(Recommended)*
  - Fast 10s stylized motion-graphics seed from `resources/mg-styles-15/` (`01-flat-vector`..`22-hud`)
  - Art-history multi-style film or long-scroll canvas (`huashu-art-motion`, 36 styles)
- **Q-Audio**: Built-in procedural score (`anidoodle` `music.mjs` or `mgaudio` `-14 LUFS`) *(Recommended)* | Openverse CC0 track + `librosa` beat-sync | Narrated + auto-subtitled (`narrate.mjs` / `whisperx`)
- **Q-Delivery**: `1920x1080@30` MP4 *(Recommended)* | Seamless loop GIF/WebM/MP4 | Interactive standalone offline HTML (`emit.mjs`)

### 4. Chinese / Bilingual Voiceover Explainer
*Signals: "explainer", "Vox", "Kurzgesagt", "3b1b", "whiteboard", "finance chart", "口播", Chinese/bilingual script*

- **Q-Grammar**:
  - `y2_vox` (editorial card/evidence) | `y1_kurzgesagt` (flat vector science) | `t1_3b1b` (math intuition) | `t3_finance_chart` (data/finance) | `y3_whiteboard` / `y5_kinetic_type`
- **Q-Voice/Timing**: Existing voiceover audio aligned via `whisperx` *(Recommended)* | Script-only timed narration + subtitle safe-zone gating | Bilingual subtitles (CN + EN)
- **Q-Character/Art**: Pure motion graphics + data visuals *(Recommended)* | AI-generated character frames (`huashu-art-motion` `10-角色.md`)

### 5. Math / Algorithmic / CS Diagram Explainer
*Signals: "math", "algorithm", "proof", "graph", "equation", "Manim", "sorting", "neural net", "geometry"*

- **Q-Text-Mode**: Clean `Text`/`MarkupText` typography (works immediately on Windows without LaTeX) *(Recommended)* | Full LaTeX `Tex`/`MathTex` (requires MiKTeX/TeX Live + `dvisvgm` installed)
- **Q-Audio/Pacing**: Silent visual loop | Voiceover + `whisperx` timestamps driving Manim `wait()` beats *(Recommended)* | Offline `mgaudio` ambient pulse + SFX cues
- **Q-Enhancement**: Pure Manim MP4 *(Recommended)* | Hybrid Manim passes composited with kinetic UI titles in Remotion / FFmpeg

### 6. Interactive 3D Web VFX / Particle / Shader Scene
*Signals: "particles", "Three.js", "R3F", "bloom", "VFX", "shader", "interactive 3D", "tweakpane"*

- **Q-Deliverable**:
  - Interactive React Three Fiber app (`three.quarks` + `@react-three/postprocessing` + `tweakpane` live controls) *(Recommended)*
  - Interactive scene + deterministic MP4 video capture (`reanimate` `--clock virtual --gl` + `ffmpeg`)
- **Q-Visual-Focus**: GPU particle bursts/trails (`three.quarks`) + selective Bloom *(Recommended)* | Post-processing look (DOF, chromatic aberration, vignette, tone-mapping) | Audio-reactive particles driven by `librosa` beat/onset JSON

### 7. 3D Blender Asset / Product Turntable / Hybrid 3D+2D Film
*Signals: "Blender", "3D model", "sculpt", "rig", "turntable", "environment", "rain/snow", "3D product render"*

- **Q-Target-Profile**: High-craft cinematic render/turntable (`--profile render`) *(Recommended for video)* | Real-time game/web GLB (`--profile game`) | Hybrid 3D Blender passes + 2D kinetic titles in HTML/GSAP or Remotion
- **Q-Look-Mood**: Studio 3-point product look-dev (`blender-lighting-lookdev`) *(Recommended)* | Time-of-day atmosphere (`blender-time-of-day`) | Weather FX rain/snow/puddles (`blender-weather-fx`) | Stylized/NPR cel-shaded (`blender-stylized-npr`)
- **Q-Execution**: Headless Blender 5.2 CLI (`run_in_blender.py`) *(Recommended)* | Live Blender MCP (`execute_blender_code` + `look`)

### 8. Native Desktop Compositing / Lottie Motion Pipeline
*Signals: "EffectCraft", "Lottie", ".lottie", "compositor", "effect stack", "batch render"*

- **Q-Workflow**: `.ecproj` keyframed effect composition + headless `effectcraft-cli render` *(Recommended)* | Lottie `.json`/`.lottie` import/export & UI motion polish (`motion-design`) | Multi-pass compositing (Blender/Manim renders → EffectCraft → `ffprobe` QA)

---

## Cross-Cutting Fallback Questions (Use Only If Missing)

1. **Duration & Aspect Ratio**: `15–20s 9:16` (Reels/Shorts/TikTok) | `30–45s 16:9` (YouTube/Launch) *(Recommended)* | `10s 1:1` (Loop/Feed)
2. **Audio & Zero-Key Constraint**: Zero-API-key offline (`Openverse CC0` + `librosa` / `mgaudio` / `music.mjs`) *(Recommended)* | Existing audio/VO file (`whisperx` alignment) | Paid TTS/SFX (ElevenLabs) | Silent
3. **Reference / Brand Assets**: Starting from a live URL | Local assets/brand guidelines | Purely from scratch (prompt-directed palette & typography) *(Recommended)*
