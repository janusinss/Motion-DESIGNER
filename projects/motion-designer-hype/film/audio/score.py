"""Score for the Motion-DESIGNER hype cut: mgaudio (offline, deterministic, CC0 samples), placed on the film's own events.

Run from the repo root:  .venv\\Scripts\\python.exe projects/motion-designer-hype/film/audio/score.py <events.json>
Writes film/audio/mix.wav (-14 LUFS, <= -1.1 dBTP) and film/audio/spec.png.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "resources/mg-styles-15/lib/audio"))
import mgaudio as mg  # noqa: E402
from mgaudio import recipes, sfx  # noqa: E402

HERE = Path(__file__).resolve().parent
ev = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
ev = ev["events"] if isinstance(ev, dict) else ev
FPS = 30
t_of = lambda e: e["frame"] / FPS  # noqa: E731

DROP, OUTRO, DUR = 12.0, 18.0, 20.0
m = recipes.pop(duration=DUR, bpm=120, key='A', mode='minor', prog='i VI III VII', drop=DROP, build=6.0, outro=OUTRO)
f = m.form

# the designed breath: music out for the last half-second before Enter (keystrokes and caret only)
m.mute(11.5, 0.5)

# keystrokes on the real typing events (product input), quiet and close
types = [t_of(e) for e in ev if e["type"] == "type"]
for i, t in enumerate(types):
    m.sfx(sfx.click('soft' if i % 3 else 'mouse'), at=t, gain=-9, pan=-0.15 + 0.3 * (i % 5) / 4)

# Enter: a hard key press at maximum compression, then the hero hit on the drop
press = next(t_of(e) for e in ev if e["type"] == "press")
# the caret blinks through the breath: two near-silent ticks keep it a held breath, not a dropout
for t in (11.6, 11.8):
    m.sfx(sfx.tick('wood'), at=t, gain=-22)
m.sfx(sfx.click('hard'), at=press, gain=-3)
m.sfx(sfx.impact('cinematic'), at=DROP, gain=1, verb=-10)
m.sfx(sfx.sub_drop(), at=DROP, gain=-2)
m.sfx(sfx.whoosh(0.7, 'sci', direction=1, peak=0.45), at=DROP + 0.35, gain=-4)          # the file-in
m.sfx(sfx.ding(f.chord_at(13.1)[-1] + 12), at=13.1, gain=-7)                             # video-director lands

# act 1: a few hand-placed ticks on reframe cuts (not every cut)
cuts = [t_of(e) for e in ev if e["type"] == "cut" and e["frame"] < 300]
for i, t in enumerate(cuts[::3]):
    m.sfx(sfx.tick('hi'), at=t, gain=-10, pan=(-0.4 if i % 2 else 0.4))

# the dive into video-director carries into the doctor output
m.sfx(sfx.transition(0.5, 'whoosh_hit'), at=15.0, gain=-4)
# proofs: in-key blips as the doctor lines print, wood ticks as the PASS lines land
for k, fr in enumerate([4, 7, 10, 15, 22]):
    m.sfx(sfx.blip(int(f.chord_at(15.0)[k % 3]) + 24, 'sine'), at=15.0 + fr / FPS, gain=-11)
for k, fr in enumerate([5, 9, 13, 17, 21]):
    m.sfx(sfx.tick('wood'), at=16.5 + fr / FPS, gain=-9)

# the name: one resolved hit; the recipe's final chord rings out under the hold
m.sfx(sfx.impact('soft'), at=18.0, gain=-3, verb=-12)
m.sfx(sfx.shimmer_hit(f.chord_at(18.1)[-1] + 12), at=18.05, gain=-8)

# -2.5 dBTP: AAC encoding of the hard transients adds ~1.2 dB of inter-sample peak
res = m.export(str(HERE / "mix.wav"), tp=-2.5, spectrogram=str(HERE / "spec.png"))
print(json.dumps({k: res.get(k) for k in ("duration", "lufs", "true_peak", "warnings")}, default=str))
print("bpm", f.bpm, "drop", f.drop, "outro", f.outro)
