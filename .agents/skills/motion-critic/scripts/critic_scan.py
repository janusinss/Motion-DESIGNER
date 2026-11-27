#!/usr/bin/env python3
"""critic_scan.py: engine-agnostic measured evidence for the motion-critic jury.

Works on any rendered MP4/WebM/MOV (Remotion, HTML/GSAP, Manim, Blender, EffectCraft, ffmpeg).
Produces, in --out:
  sheet.jpg     contact sheet (one frame every --sheet-every s, timestamped)
  energy.png    motion-energy curve with the 60-75 % hero window shaded and the peak marked
  critic.json   all metrics + PASS/WARN/FAIL checks

Requires: ffmpeg + ffprobe on PATH, numpy, Pillow (librosa optional, for audio onset sync).

Usage:
  python critic_scan.py film/final.mp4 --out film/critic --expect 30 [--hero 19.6] [--fps-sample 12]
                        [--cues cues.json] [--reference ref_critic.json]
  --cues       the film's cue sheet (video-director/scripts/cues.py; schema video-director/references/cues.schema.json):
               authored cuts replace detected ones for cut sync, the hero span replaces --hero, hits are checked
               against sound onsets, breaths against true quiet, holds against perceived motion.
  --reference  a critic.json made by this script on a reference film: energy-curve correlation, peak position and
               median shot length are reported as deltas (grammar targets, never pass/fail on taste).

Statuses: PASS, WARN, FAIL, UNVERIFIED (the check could not run: missing input or library). An unrun check is
never reported as a pass. Exit 1 on any FAIL.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

DEAD_EPS = 0.35          # mean abs luma diff (0-255) below which a sample counts as static
DEAD_SPAN_S = 0.5        # static span (not at the very end) longer than this is a dead frame stretch
END_HOLD_MAX_S = 1.4     # static tail longer than this reads as a frozen ending
HERO_WINDOW = (0.55, 0.80)
SLOP_HUE = (0.58, 0.80)  # blue -> purple band in HSV hue (0-1)
SLOP_FRAME_SHARE = 0.40  # a frame is "slop-tinted" if > 40 % of saturated pixels sit in the band
SLOP_FILM_MAX = 0.30     # fail when > 30 % of sheet frames are slop-tinted
SYNC_TOL_S = 0.10
PERCEIVED_EPS = 0.5      # smoothed mean abs luma diff at 48 px width: below this a hold reads as frozen to a viewer
                         # (film grain and sub-pixel jitter average out at 48 px; measured: a grain-only hold 0.07-0.14,
                         # a slow 7 % scale drift 0.2-0.7, real moves > 1)
BREATH_MAX_DBFS = -30.0  # peak level allowed inside a designed breath
BLACK_FAIL_S = 0.5       # a black run this long inside the film is a hole, not a flash


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, check=False)


def probe(path: Path) -> dict:
    p = run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)])
    if p.returncode != 0:
        sys.exit(f"[FAIL] ffprobe could not read {path}: {p.stderr.decode(errors='replace')[:300]}")
    info = json.loads(p.stdout)
    v = next((s for s in info["streams"] if s.get("codec_type") == "video"), None)
    a = next((s for s in info["streams"] if s.get("codec_type") == "audio"), None)
    if v is None:
        sys.exit("[FAIL] no video stream")
    num, den = (v.get("avg_frame_rate") or v.get("r_frame_rate") or "0/1").split("/")
    fps = float(num) / float(den) if float(den) else 0.0
    dur = float(info["format"].get("duration") or v.get("duration") or 0.0)
    return {"width": int(v["width"]), "height": int(v["height"]), "fps": round(fps, 3),
            "duration": round(dur, 3), "has_audio": a is not None,
            "video_codec": v.get("codec_name"), "audio_codec": a.get("codec_name") if a else None}


def read_frames(path: Path, fps: float, width: int, gray: bool) -> tuple[np.ndarray, int]:
    pix = "gray" if gray else "rgb24"
    ch = 1 if gray else 3
    cmd = ["ffmpeg", "-v", "error", "-i", str(path), "-vf",
           f"fps={fps},scale={width}:-2:flags=area,format={pix}", "-f", "rawvideo", "-"]
    p = run(cmd)
    if p.returncode != 0:
        sys.exit(f"[FAIL] ffmpeg decode failed: {p.stderr.decode(errors='replace')[:300]}")
    # derive height from a single probe frame
    probe_cmd = ["ffmpeg", "-v", "error", "-i", str(path), "-frames:v", "1", "-vf",
                 f"scale={width}:-2:flags=area,format={pix}", "-f", "rawvideo", "-"]
    one = run(probe_cmd).stdout
    h = len(one) // (width * ch)
    n = len(p.stdout) // (width * h * ch)
    arr = np.frombuffer(p.stdout[: n * width * h * ch], dtype=np.uint8)
    shape = (n, h, width) if gray else (n, h, width, ch)
    return arr.reshape(shape), h


def spans(mask: np.ndarray, dt: float) -> list[tuple[float, float]]:
    out, start = [], None
    for i, m in enumerate(mask):
        if m and start is None:
            start = i
        elif not m and start is not None:
            out.append((start * dt, i * dt))
            start = None
    if start is not None:
        out.append((start * dt, len(mask) * dt))
    return out


def font(size: int):
    for name in ("arial.ttf", "DejaVuSans.ttf", "Helvetica.ttc"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def contact_sheet(frames: np.ndarray, every: float, out: Path, cols: int = 6) -> None:
    n, h, w, _ = frames.shape
    rows = math.ceil(n / cols)
    pad, label = 6, 18
    sheet = Image.new("RGB", (cols * (w + pad) + pad, rows * (h + label + pad) + pad), (18, 18, 18))
    draw, f = ImageDraw.Draw(sheet), font(13)
    for i in range(n):
        r, c = divmod(i, cols)
        x, y = pad + c * (w + pad), pad + r * (h + label + pad)
        sheet.paste(Image.fromarray(frames[i]), (x, y + label))
        draw.text((x + 2, y + 2), f"{i * every:5.1f}s", fill=(235, 235, 235), font=f)
    sheet.save(out, quality=88)


def slop_share(frames: np.ndarray) -> list[float]:
    shares = []
    for fr in frames:
        hsv = np.asarray(Image.fromarray(fr).convert("HSV"), dtype=np.float32) / 255.0
        hcol, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
        sat = (s > 0.25) & (v > 0.20)
        total = int(sat.sum())
        if total < 0.05 * sat.size:
            shares.append(0.0)
            continue
        band = sat & (hcol >= SLOP_HUE[0]) & (hcol <= SLOP_HUE[1])
        shares.append(float(band.sum()) / total)
    return shares


def energy_plot(t: np.ndarray, e: np.ndarray, dur: float, peak_t: float, hero_t: float | None,
                cuts: list[float], out: Path) -> None:
    W, H, m = 1200, 320, 40
    img = Image.new("RGB", (W, H), (250, 248, 243))
    d, f = ImageDraw.Draw(img), font(14)
    x = lambda s: m + (W - 2 * m) * (s / dur if dur else 0)
    emax = float(e.max()) or 1.0
    y = lambda v: H - m - (H - 2 * m) * (v / emax)
    d.rectangle([x(dur * HERO_WINDOW[0]), m, x(dur * HERO_WINDOW[1]), H - m], fill=(255, 236, 160))
    for c in cuts:
        d.line([x(c), m, x(c), H - m], fill=(200, 200, 200), width=1)
    pts = [(x(float(ti)), y(float(ei))) for ti, ei in zip(t, e)]
    if len(pts) > 1:
        d.line(pts, fill=(28, 27, 25), width=2)
    d.line([x(peak_t), m, x(peak_t), H - m], fill=(214, 40, 40), width=2)
    if hero_t is not None:
        d.line([x(hero_t), m, x(hero_t), H - m], fill=(40, 110, 214), width=2)
    d.text((m, 10), f"motion energy | red = measured peak {peak_t:.2f}s | yellow = 55-80 % hero window"
                    + (f" | blue = planned hero {hero_t:.2f}s" if hero_t is not None else ""),
           fill=(28, 27, 25), font=f)
    d.text((m, H - m + 8), "0s", fill=(90, 90, 90), font=f)
    d.text((W - m - 40, H - m + 8), f"{dur:.1f}s", fill=(90, 90, 90), font=f)
    img.save(out)


def loudness(path: Path) -> dict:
    p = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"])
    txt = p.stderr.decode(errors="replace")
    summary = txt[txt.rfind("Summary:"):] if "Summary:" in txt else txt
    i = re.search(r"I:\s*(-?[\d.]+)\s*LUFS", summary)
    tp = re.search(r"Peak:\s*(-?[\d.]+)\s*dBFS", summary)
    return {"integrated_lufs": float(i.group(1)) if i else None,
            "true_peak_dbtp": float(tp.group(1)) if tp else None}


def audio_onsets(path: Path, out_dir: Path) -> list[float] | None:
    try:
        import librosa  # noqa: PLC0415
    except ImportError:
        return None
    wav = out_dir / "_audio.wav"
    if run(["ffmpeg", "-v", "error", "-y", "-i", str(path), "-vn", "-ac", "1", "-ar", "22050", str(wav)]).returncode:
        return None
    y, sr = librosa.load(str(wav), sr=22050)
    wav.unlink(missing_ok=True)
    return [round(float(v), 3) for v in librosa.onset.onset_detect(y=y, sr=sr, units="time", backtrack=False)]


def black_runs(path: Path) -> list[tuple[float, float]] | None:
    p = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-vf", "blackdetect=d=0.15:pix_th=0.10",
             "-an", "-f", "null", "-"])
    if p.returncode != 0:
        return None
    txt = p.stderr.decode(errors="replace")
    return [(float(a), float(b)) for a, b in re.findall(r"black_start:([\d.]+)\s+black_end:([\d.]+)", txt)]


def audio_peaks(path: Path, spans_s: list[list[float]]) -> list[float] | None:
    """peak dBFS inside each span (mono mix), or None when the audio cannot be decoded."""
    p = run(["ffmpeg", "-v", "error", "-i", str(path), "-vn", "-ac", "1", "-ar", "24000", "-f", "f32le", "-"])
    if p.returncode != 0 or not p.stdout:
        return None
    y = np.frombuffer(p.stdout, dtype=np.float32)
    out = []
    for t0, t1 in spans_s:
        seg = y[int(t0 * 24000): int(t1 * 24000)]
        pk = float(np.abs(seg).max()) if len(seg) else 0.0
        out.append(round(20 * math.log10(pk), 1) if pk > 0 else -120.0)
    return out


def resample(curve: list[float], n: int = 40) -> np.ndarray:
    c = np.asarray(curve, dtype=float)
    if len(c) < 2:
        return np.zeros(n)
    return np.interp(np.linspace(0, len(c) - 1, n), np.arange(len(c)), c)


def main() -> int:
    ap = argparse.ArgumentParser(description="Measured evidence for the motion-critic jury.")
    ap.add_argument("video", type=Path)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--expect", type=float, default=None, help="planned duration in seconds")
    ap.add_argument("--hero", type=float, default=None, help="planned hero-moment time in seconds")
    ap.add_argument("--fps-sample", type=float, default=12.0)
    ap.add_argument("--sheet-every", type=float, default=0.5)
    ap.add_argument("--cues", type=Path, default=None, help="cue sheet (video-director cues.py)")
    ap.add_argument("--reference", type=Path, default=None, help="critic.json of a reference film")
    a = ap.parse_args()
    cues = json.loads(a.cues.read_text(encoding="utf-8")) if a.cues else None
    if cues and a.hero is None and cues.get("hero"):
        h = cues["hero"]
        a.hero = h.get("poster", (h["t0"] + h["t1"]) / 2)

    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        sys.exit("[FAIL] ffmpeg/ffprobe not on PATH")
    out = a.out or a.video.with_name(a.video.stem + "_critic")
    out.mkdir(parents=True, exist_ok=True)

    info = probe(a.video)
    dur = info["duration"]
    dt = 1.0 / a.fps_sample

    gray, _ = read_frames(a.video, a.fps_sample, 160, gray=True)
    g = gray.astype(np.int16)
    diff = np.abs(np.diff(g, axis=0)).mean(axis=(1, 2)) if len(g) > 1 else np.zeros(1)
    t = np.arange(len(diff)) * dt + dt
    win = max(1, int(round(0.5 / dt)))
    smooth = np.convolve(diff, np.ones(win) / win, mode="same")
    peak_i = int(np.argmax(smooth))
    peak_t = float(t[peak_i])
    peak_frac = peak_t / dur if dur else 0.0

    mu, sd = float(diff.mean()), float(diff.std())
    cut_idx = np.where(diff > mu + 3 * sd)[0] if sd > 0 else np.array([], dtype=int)
    cuts = [round(float(t[i]), 3) for i in cut_idx]

    static = diff < DEAD_EPS
    st_spans = spans(static, dt)
    tail = st_spans[-1][1] - st_spans[-1][0] if st_spans and st_spans[-1][1] >= len(diff) * dt - dt else 0.0
    dead = [(round(s, 2), round(e, 2)) for s, e in st_spans
            if e - s >= DEAD_SPAN_S and not (e >= len(diff) * dt - dt)]
    if tail > END_HOLD_MAX_S + 1.0:  # a frozen ending far past the allowed hold is a dead stretch, not a hold
        end_t = len(diff) * dt
        dead.append((round(end_t - tail, 2), round(end_t, 2)))
    frame0_motion = float(diff[: max(1, int(0.3 / dt))].mean())

    # perceived motion: at 48 px grain and jitter average out, so a hold kept "alive" only by grain reads as frozen
    g48, _ = read_frames(a.video, a.fps_sample, 48, gray=True)
    d48 = np.abs(np.diff(g48.astype(np.int16), axis=0)).mean(axis=(1, 2)) if len(g48) > 1 else np.zeros(1)
    s48 = np.convolve(d48, np.ones(win) / win, mode="same")
    p_spans = spans(s48 < PERCEIVED_EPS, dt)
    p_tail = p_spans[-1][1] - p_spans[-1][0] if p_spans and p_spans[-1][1] >= len(d48) * dt - dt else 0.0
    perceived_holds = [(round(s, 2), round(e, 2)) for s, e in p_spans if e - s >= 1.0]

    # equal-energy tell: compare energy of 4 equal quarters
    q = np.array_split(smooth, 4)
    quarter_means = [round(float(x.mean()), 3) for x in q]
    energy_cv = float(np.std(quarter_means) / (np.mean(quarter_means) or 1))

    colour, _ = read_frames(a.video, 1.0 / a.sheet_every, 320, gray=False)
    contact_sheet(colour, a.sheet_every, out / "sheet.jpg")
    shares = slop_share(colour)
    slop_frames = sum(1 for s in shares if s > SLOP_FRAME_SHARE)
    slop_ratio = slop_frames / len(shares) if shares else 0.0

    energy_plot(t, smooth, dur, peak_t, a.hero, cuts, out / "energy.png")

    sync_cuts = [float(c) for c in cues["cuts"]] if cues and cues.get("cuts") else cuts
    audio = {"present": info["has_audio"]}
    sync, onsets = None, None
    if info["has_audio"]:
        audio.update(loudness(a.video))
        onsets = audio_onsets(a.video, out)
        if onsets is not None:
            audio["onset_count"] = len(onsets)
            if sync_cuts:
                hits = sum(1 for c in sync_cuts if any(abs(c - o) <= SYNC_TOL_S for o in onsets))
                sync = round(hits / len(sync_cuts), 3)
    blacks = black_runs(a.video)
    shots = np.diff([0.0] + sorted(sync_cuts) + [dur]) if dur else np.array([])
    median_shot = round(float(np.median(shots)), 3) if len(shots) else None

    checks = []

    def chk(name, ok, detail, warn_only=False):
        checks.append({"check": name, "status": "PASS" if ok else ("WARN" if warn_only else "FAIL"), "detail": detail})

    def unverified(name, why):
        checks.append({"check": name, "status": "UNVERIFIED", "detail": why})

    if a.expect is not None:
        chk("duration", abs(dur - a.expect) <= max(0.1, 1.0 / max(info["fps"], 1)),
            f"{dur:.2f}s vs planned {a.expect:.2f}s")
    else:
        unverified("duration", "no --expect given")
    chk("frame0_in_motion", frame0_motion >= DEAD_EPS, f"mean diff first 0.3s = {frame0_motion:.2f}")
    chk("no_dead_spans", not dead, f"static spans >= {DEAD_SPAN_S}s: {dead}" if dead else "none")
    chk("end_hold", tail <= END_HOLD_MAX_S, f"static tail {tail:.2f}s (max {END_HOLD_MAX_S}s)", warn_only=True)
    chk("end_hold_perceived", p_tail <= END_HOLD_MAX_S,
        f"tail that reads as held at 48 px (grain ignored): {p_tail:.2f}s (max {END_HOLD_MAX_S}s); "
        f"other perceived holds >= 1 s: {[h for h in perceived_holds if h[1] < len(d48) * dt - dt]}", warn_only=True)
    if blacks is None:
        unverified("black_frames", "blackdetect failed")
    else:
        inner = [(round(s, 2), round(e, 2)) for s, e in blacks if s > 0.05 and e < dur - 0.05]
        long_ = [b for b in inner if b[1] - b[0] >= BLACK_FAIL_S]
        checks.append({"check": "black_frames", "status": "FAIL" if long_ else ("WARN" if inner else "PASS"),
                       "detail": f"black runs >= 0.15 s inside the film: {inner}" if inner else "none >= 0.15 s"})
    chk("peak_in_hero_window", HERO_WINDOW[0] <= peak_frac <= HERO_WINDOW[1],
        f"measured peak {peak_t:.2f}s = {peak_frac * 100:.0f}% of runtime", warn_only=True)
    hspan = cues.get("hero") if cues else None
    if hspan:
        chk("peak_matches_planned_hero", hspan["t0"] - 0.25 <= peak_t <= hspan["t1"] + 0.25,
            f"measured {peak_t:.2f}s vs planned hero span {hspan['t0']:.2f}-{hspan['t1']:.2f}s (±0.25 s)", warn_only=True)
    elif a.hero is not None:
        chk("peak_matches_planned_hero", abs(peak_t - a.hero) <= 0.75,
            f"measured {peak_t:.2f}s vs planned {a.hero:.2f}s", warn_only=True)
    chk("energy_contour", energy_cv >= 0.15,
        f"quarter energy {quarter_means}, CV {energy_cv:.2f} (< 0.15 = equal-energy beats)", warn_only=True)
    chk("blue_purple_slop", slop_ratio <= SLOP_FILM_MAX,
        f"{slop_frames}/{len(shares)} sheet frames dominated by blue-purple ({slop_ratio * 100:.0f}%)", warn_only=True)
    if info["has_audio"]:
        lufs, tp = audio.get("integrated_lufs"), audio.get("true_peak_dbtp")
        if lufs is not None:
            chk("loudness", abs(lufs + 14) <= 1.0, f"{lufs:.1f} LUFS (target -14 ±1)")
        else:
            unverified("loudness", "ebur128 summary not parsed")
        if tp is not None:
            chk("true_peak", tp <= -1.0, f"{tp:.1f} dBTP (max -1.0)")
        else:
            unverified("true_peak", "ebur128 summary not parsed")
        src = "authored cues" if cues and cues.get("cuts") else "detected"
        if sync is not None:
            chk("cut_audio_sync", sync >= 0.6, f"{sync * 100:.0f}% of {len(sync_cuts)} {src} cuts within ±{SYNC_TOL_S}s of an onset",
                warn_only=True)
        else:
            unverified("cut_audio_sync", "librosa missing" if onsets is None else "no cuts")
        if cues and cues.get("hits"):
            if onsets is None:
                unverified("hits_on_sound", "librosa missing")
            else:
                tol = 1.0 / cues.get("fps", info["fps"] or 30) + 0.02
                miss = [h for h in cues["hits"] if not any(abs(h["t"] - o) <= tol for o in onsets)]
                chk("hits_on_sound", not miss, f"{len(cues['hits']) - len(miss)}/{len(cues['hits'])} cue hits have a sound onset within ±{tol * 1000:.0f} ms"
                    + (f"; missed: {[(m.get('label'), m['t']) for m in miss]}" if miss else ""), warn_only=True)
        if cues and cues.get("breaths"):
            pk = audio_peaks(a.video, cues["breaths"])
            if pk is None:
                unverified("breath_quiet", "audio decode failed")
            else:
                loud = [(s, p) for s, p in zip(cues["breaths"], pk) if p > BREATH_MAX_DBFS]
                chk("breath_quiet", not loud, f"peak in designed breaths {list(zip(cues['breaths'], pk))} dBFS (max {BREATH_MAX_DBFS})",
                    warn_only=True)
    else:
        chk("audio_present", False, "no audio stream", warn_only=True)
    if cues and cues.get("holds"):
        bad = []
        for h0, h1 in cues["holds"]:
            i0, i1 = int(h0 / dt), int(h1 / dt)
            seg = s48[i0:i1]
            if h1 - h0 > END_HOLD_MAX_S and len(seg) and float(seg.mean()) < PERCEIVED_EPS:
                bad.append((h0, h1, round(float(seg.mean()), 2)))
        chk("holds_alive", not bad, f"designed holds longer than {END_HOLD_MAX_S}s that read frozen (span, 48 px motion): {bad}" if bad
            else "every designed hold > 1.4 s carries visible motion", warn_only=True)

    ref = None
    if a.reference:
        try:
            ref = json.loads(a.reference.read_text(encoding="utf-8"))
            mine = report_curve = [round(float(x.mean()), 3) for x in np.array_split(smooth, max(1, int(dur / 0.5)))]
            ra, rb = resample(mine), resample(ref.get("energy_curve_0p5s", []))
            corr = float(np.corrcoef(ra, rb)[0, 1]) if ra.std() and rb.std() else 0.0
            ref_med = ref.get("median_shot_s")
            ratio = (median_shot / ref_med) if (median_shot and ref_med) else None
            ref = {"file": str(a.reference), "energy_corr": round(corr, 2), "peak_fraction_delta": round(peak_frac - ref.get("peak_fraction", peak_frac), 2),
                   "median_shot_ratio": round(ratio, 2) if ratio else None}
            chk("reference_grammar", corr >= 0.3 and (ratio is None or 0.5 <= ratio <= 2.0),
                f"energy-curve correlation {corr:.2f} (>= 0.3), peak position delta {ref['peak_fraction_delta']:+.2f}, "
                f"median shot {median_shot}s vs reference {ref_med}s", warn_only=True)
        except (OSError, ValueError, KeyError) as e:
            unverified("reference_grammar", f"cannot read {a.reference}: {e}")

    report = {"video": str(a.video), "probe": info, "sample_fps": a.fps_sample,
              "peak_time_s": round(peak_t, 3), "peak_fraction": round(peak_frac, 3),
              "cuts_s": cuts, "dead_spans_s": dead, "static_tail_s": round(tail, 2),
              "energy_quarters": quarter_means, "energy_cv": round(energy_cv, 3),
              "energy_curve_0p5s": [round(float(x.mean()), 3) for x in np.array_split(smooth, max(1, int(dur / 0.5)))],
              "slop_ratio": round(slop_ratio, 3), "audio": audio, "cut_audio_sync": sync,
              "median_shot_s": median_shot, "perceived_tail_s": round(p_tail, 2), "perceived_holds_s": perceived_holds,
              "black_runs_s": blacks, "cues": str(a.cues) if a.cues else None, "reference": ref,
              "checks": checks, "artifacts": {"sheet": str(out / "sheet.jpg"), "energy": str(out / "energy.png")}}
    (out / "critic.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"{a.video} | {info['width']}x{info['height']} @ {info['fps']} fps | {dur:.2f}s | audio={info['has_audio']}")
    for c in checks:
        print(f"[{c['status']}] {c['check']}: {c['detail']}")
    n_unv = sum(1 for c in checks if c["status"] == "UNVERIFIED")
    if n_unv:
        print(f"{n_unv} check(s) UNVERIFIED: not run, so not passed")
    print(f"artifacts: {out / 'sheet.jpg'} | {out / 'energy.png'} | {out / 'critic.json'}")
    return 1 if any(c["status"] == "FAIL" for c in checks) else 0


if __name__ == "__main__":
    raise SystemExit(main())
