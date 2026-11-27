r"""Offline synth score for bench b1 (mgaudio techno recipe, CC0 VCSL + synthesis). Deterministic.
Run from repo root: .venv\Scripts\python.exe projects/bench-b1-e9ebd82/film/audio/score.py"""
import sys, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'resources', 'mg-styles-15', 'lib', 'audio'))
import mgaudio as mg
from mgaudio import recipes, sfx

OUT = os.path.dirname(os.path.abspath(__file__))
m = recipes.techno(duration=20.0, bpm=120, drop=12.0, build=11.0, outro=18.75)
print('form', m.form.sections, 'bpm', m.form.bpm)

# build: whips and engine hits
for t in (2.5, 4.5):
    m.sfx(sfx.whoosh(0.5, kind='swish', seed=int(t * 10)), at=t, gain=-3)
m.sfx(sfx.impact('punch', size=0.6), at=6.0, gain=-2)
for i, t in enumerate((7.0, 7.25, 7.5, 7.75)):
    m.sfx(sfx.stamp('rubber', seed=i), at=t, gain=-6)
for i, t in enumerate((8.0, 8.5, 9.0, 9.25, 9.5, 9.75, 10.0, 10.25)):
    m.sfx(sfx.swish(0.2, seed=40 + i), at=t, gain=-9)
m.sfx(sfx.riser(3.0, kind='hybrid'), at=11.0, gain=-2)        # riser sync = its end: the noise peaks, then cut to dark
# breath: quiet irregular keystrokes, then true silence 11.5-12.0
m.sfx(sfx.typing(9, rate=20, kind='soft'), at=11.02, gain=-14, verb=None)
# drop
m.sfx(sfx.click('hard'), at=12.0, gain=-4)
m.sfx(sfx.impact('cinematic', size=1.0), at=12.067, gain=2)
m.sfx(sfx.sub_drop(), at=12.067, gain=0)
m.sfx(sfx.whoosh(0.7, kind='heavy', seed=3), at=12.4, gain=-4)
# echoes
m.sfx(sfx.tick('hi'), at=14.5, gain=-6)
m.sfx(sfx.ui('confirm'), at=15.0, gain=-4)
m.sfx(sfx.whoosh(0.5, kind='soft', seed=9), at=16.0, gain=-6)
# mark
m.sfx(sfx.impact('soft', size=0.7), at=18.75, gain=0)
m.sfx(sfx.ding(m.form.chord_at(18.75)[-1] if hasattr(m.form, 'chord_at') else 'A5'), at=18.75, gain=-5)

# designed breath: music + sfx silent 11.5-12.0
m.group('music').region('mute', 11.45, 0.55)
# subtraction into the mark: the groove filters down and drops 7 dB from 16.0 s
m.group('music').automate('lpf', [(0, 20000), (16.0, 20000), (18.7, 1400), (18.76, 20000)])
m.group('music').automate('gain', [(0, 0), (16.0, 0), (18.7, -7), (18.76, 0)])
m.group('sfx').region('mute', 11.45, 0.54)

res = m.export(os.path.join(OUT, 'mix.wav'), for_aac=True, spectrogram=os.path.join(OUT, 'mix.png'))
print(res)
