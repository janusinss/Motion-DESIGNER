#!/usr/bin/env node
// text_overlap.mjs: find text that collides with other text, frame by frame, in a seek-safe HTML film.
//
// Usage: node text_overlap.mjs <film/index.html> [--step 2] [--min-px 18] [--json out.json]
//
// Works on any page that exposes window.__seek(t) (motionmaxxing runtime) or window.renderAt(t)
// (mg-styles-15 harness). HyperFrames / Remotion / video-only films: run the jury instead.
//
// For every sampled frame it measures each visible text element (leaf with its own text, opacity
// product >= 0.35, no blur > 1.5 px, glyph height >= --min-px, on screen) as a rotated rectangle and
// intersects every pair. A pair counts when the overlap covers >= 15 % of the smaller box.
//   FAIL  the frame's HEADLINE is covered by any other text at opacity >= 0.5 for >= 0.2 s: the copy meant to be
//         read is covered. Headline = sharp (opacity >= 0.6, glyph >= 28 px) and within 85 % of the frame's
//         biggest glyph, on a frame with a hierarchy (biggest >= 1.3x the median sharp text, or <= 3 sharp texts).
//   Calibrated on bench-b1 (catches the jury's 1.5 s and 8.0 s collisions) and the hype cut (catches its pile).
//   WARN  any other overlap involving a sharp text for >= 0.2 s: a pile of equal-weight words. Check craft
//         rule K4 (at most ~7 sharp words, the rest pushed back in depth).
// Exit 1 on FAIL. Designed overlaps (a word deliberately set over another) are allowed: justify them in NOTE.md.
import path from 'node:path';
import fs from 'node:fs';
import { pathToFileURL, fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const { launchChrome } = await import(pathToFileURL(path.join(here, '../../motionmaxxing/scripts/_cdp.mjs')).href);

const argv = process.argv.slice(2);
const opt = (k, d) => { const i = argv.indexOf(k); return i >= 0 ? argv[i + 1] : d; };
const file = argv.find(a => !a.startsWith('--') && !argv[argv.indexOf(a) - 1]?.startsWith('--'));
if (!file || !fs.existsSync(file)) { console.error('usage: node text_overlap.mjs <index.html> [--step 2] [--min-px 18] [--json out.json]'); process.exit(2); }
const step = +opt('--step', 2), minPx = +opt('--min-px', 18), jsonOut = opt('--json', null);

const PAGE_FN = `(async (step, minPx) => {
  if (window.__ready) await window.__ready;
  await document.fonts.ready;
  const seek = window.__seek || window.renderAt;
  if (!seek) return { error: 'page has neither window.__seek nor window.renderAt' };
  const fps = (window.Motion && Motion.last && Motion.last.fps) || 30;
  const dur = window.__duration || (window.Motion && Motion.last && Motion.last.duration) || 10;
  const W = innerWidth, H = innerHeight;
  const leaves = [...document.querySelectorAll('body *')].filter(e =>
    !['SCRIPT', 'STYLE', 'NOSCRIPT'].includes(e.tagName) &&
    [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()));
  const mat = e => { let m = new DOMMatrix(); for (let x = e; x && x !== document.documentElement; x = x.parentElement) {
      const t = getComputedStyle(x).transform; if (t && t !== 'none') m = new DOMMatrix(t).multiply(m); } return m; };
  const vis = e => { let o = 1; for (let x = e; x; x = x.parentElement) { const s = getComputedStyle(x);
      if (s.display === 'none' || s.visibility === 'hidden') return 0;
      o *= +s.opacity; const b = /blur\\(([\\d.]+)px/.exec(s.filter); if (b && +b[1] > 1.5) return 0; if (o < 0.05) return 0; } return o; };
  const quad = e => {
    const m = mat(e), sx = Math.hypot(m.a, m.b), sy = Math.hypot(m.c, m.d), ang = Math.atan2(m.b, m.a);
    const r = e.getBoundingClientRect(); if (!r.width || !r.height) return null;
    let w, h;
    if (Math.abs(Math.sin(ang)) < 0.02) {           // upright: tight box from the text itself
      const rg = document.createRange(); rg.selectNodeContents(e); const t = rg.getBoundingClientRect(); w = t.width; h = t.height;
      return { cx: t.left + w / 2, cy: t.top + h / 2, w, h, ang: 0, glyph: parseFloat(getComputedStyle(e).fontSize) * sy };
    }
    // rotated: the text's own advance width (a block element's offsetWidth is its container's width)
    const cs = getComputedStyle(e), ctx = (window.__toCtx = window.__toCtx || document.createElement('canvas').getContext('2d'));
    ctx.font = cs.fontStyle + ' ' + cs.fontWeight + ' ' + cs.fontSize + ' ' + cs.fontFamily;
    const txt = e.textContent.trim(), ls = parseFloat(cs.letterSpacing) || 0;
    w = (ctx.measureText(txt).width + ls * txt.length) * sx; h = parseFloat(cs.fontSize) * sy;
    // the box sits where the text starts in its element (left-aligned unless centred / right-aligned)
    const lw = e.offsetWidth * sx, shift = cs.textAlign === 'center' ? 0 : cs.textAlign === 'right' || cs.textAlign === 'end' ? (lw - w) / 2 : -(lw - w) / 2;
    const cx = r.left + r.width / 2 + Math.cos(ang) * shift, cy = r.top + r.height / 2 + Math.sin(ang) * shift;
    return { cx, cy, w, h, ang, glyph: parseFloat(cs.fontSize) * sy };
    return { cx: r.left + r.width / 2, cy: r.top + r.height / 2, w, h, ang, glyph: parseFloat(getComputedStyle(e).fontSize) * sy };
  };
  const out = [];
  const last = Math.round(dur * fps) - 1;
  for (let f = 0; f <= last; f += step) {
    seek(f / fps);
    const items = [];
    for (const e of leaves) {
      const o = vis(e); if (o < 0.35) continue;
      const q = quad(e); if (!q || q.glyph < minPx) continue;
      if (q.cx + q.w / 2 < 0 || q.cx - q.w / 2 > W || q.cy + q.h / 2 < 0 || q.cy - q.h / 2 > H) continue;
      items.push({ e, o, q, text: e.textContent.trim().slice(0, 32) });
    }
    out.push({ f, items: items.map((it, i) => ({ i: leaves.indexOf(it.e), o: +it.o.toFixed(2), text: it.text, ...it.q })) });
  }
  const contains = {};
  leaves.forEach((a, i) => leaves.forEach((b, j) => { if (i !== j && a.contains(b)) contains[i + ',' + j] = 1; }));
  return { fps, dur, frames: out, contains };
})`;

const ch = await launchChrome({ args: ['--allow-file-access-from-files'], width: 1920, height: 1080 });
let data;
try {
  const p = await ch.newPage();
  await p.goto(pathToFileURL(path.resolve(file)).href);
  data = JSON.parse(await p.eval(`(${PAGE_FN})(${step}, ${minPx}).then(JSON.stringify)`, { timeout: 900000 }));
} finally { try { await ch.close(); } catch {} }
if (data.error) { console.error('error: ' + data.error); process.exit(2); }

// rotated-rectangle intersection (Sutherland-Hodgman on convex quads)
const corners = q => { const c = Math.cos(q.ang), s = Math.sin(q.ang), hw = q.w / 2, hh = q.h / 2;
  return [[-hw, -hh], [hw, -hh], [hw, hh], [-hw, hh]].map(([x, y]) => [q.cx + x * c - y * s, q.cy + x * s + y * c]); };
const area = P => Math.abs(P.reduce((a, p, i) => { const n = P[(i + 1) % P.length]; return a + p[0] * n[1] - n[0] * p[1]; }, 0)) / 2;
const clip = (subj, clipP) => {
  let out = subj;
  for (let i = 0; i < clipP.length && out.length; i++) {
    const A = clipP[i], B = clipP[(i + 1) % clipP.length], inp = out; out = [];
    const side = p => (B[0] - A[0]) * (p[1] - A[1]) - (B[1] - A[1]) * (p[0] - A[0]);
    const sign = side(clipP[(i + 2) % clipP.length]) >= 0 ? 1 : -1;
    const inside = p => sign * side(p) >= 0;
    const cross = (p, q) => { const a = side(p), b = side(q), t = a / (a - b); return [p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t]; };
    for (let k = 0; k < inp.length; k++) {
      const P = inp[k], Q = inp[(k + 1) % inp.length];
      if (inside(Q)) { if (!inside(P)) out.push(cross(P, Q)); out.push(Q); } else if (inside(P)) out.push(cross(P, Q));
    }
  }
  return out;
};
if (opt('--dump', null) != null) {   // debug: print the measured text at one frame
  const fr = data.frames.find(x => x.f >= +opt('--dump'));
  for (const i of fr.items) console.log(`f${fr.f} o=${i.o} glyph=${Math.round(i.glyph)} at ${Math.round(i.cx)},${Math.round(i.cy)} w=${Math.round(i.w)} "${i.text}"`);
  process.exit(0);
}
const prominent = it => it.o >= 0.6 && it.glyph >= 28;

const runs = {};   // key "i,j" -> list of frames with overlap
for (const fr of data.frames) {
  const it = fr.items, P = it.filter(prominent).map(x => x.glyph).sort((a, b) => a - b);
  const maxG = P.length ? P[P.length - 1] : 0, med = P.length ? P[Math.floor(P.length / 2)] : 0;
  // headline = the frame's clear top text: within 85 % of the biggest glyph, and the frame has a hierarchy
  // (biggest >= 1.3x the median sharp text) or so few sharp texts that all of them are meant to be read
  const hier = maxG >= 1.3 * med || P.length <= 3;
  const headline = x => hier && prominent(x) && x.glyph >= 0.85 * maxG;
  for (let a = 0; a < it.length; a++) for (let b = a + 1; b < it.length; b++) {
    const A = it[a], B = it[b];
    if (data.contains[A.i + ',' + B.i] || data.contains[B.i + ',' + A.i]) continue;
    if (Math.hypot(A.cx - B.cx, A.cy - B.cy) > (Math.hypot(A.w, A.h) + Math.hypot(B.w, B.h)) / 2) continue;
    const inter = clip(corners(A), corners(B)); if (inter.length < 3) continue;
    const ov = area(inter) / Math.min(A.w * A.h, B.w * B.h);
    if (ov < 0.15) continue;
    const pa = prominent(A), pb = prominent(B); if (!pa && !pb) continue;
    const sev = (headline(A) && B.o >= 0.5) || (headline(B) && A.o >= 0.5) ? 'FAIL' : 'WARN';
    const key = A.i < B.i ? A.i + ',' + B.i : B.i + ',' + A.i;
    (runs[key] = runs[key] || []).push({ f: fr.f, ov, sev, texts: [A.text, B.text] });
  }
}
const events = [];
for (const list of Object.values(runs)) {
  let cur = null;
  for (const h of list) {
    if (cur && h.f - cur.f1 <= step) { cur.f1 = h.f; cur.ov = Math.max(cur.ov, h.ov); if (h.sev === 'FAIL') cur.sev = 'FAIL'; }
    else { if (cur) events.push(cur); cur = { f0: h.f, f1: h.f, ov: h.ov, sev: h.sev, texts: h.texts }; }
  }
  if (cur) events.push(cur);
}
const fps = data.fps, minRun = 0.2;
const real = events.filter(e => (e.f1 - e.f0 + step) / fps >= minRun).sort((a, b) => a.f0 - b.f0)
  .map(e => ({ t0: +(e.f0 / fps).toFixed(2), t1: +((e.f1 + step) / fps).toFixed(2), sev: e.sev, overlap: +e.ov.toFixed(2), texts: e.texts }));
const nFail = real.filter(e => e.sev === 'FAIL').length, nWarn = real.length - nFail;
const shown = [...real.filter(e => e.sev === 'FAIL'), ...real.filter(e => e.sev === 'WARN')].slice(0, 12);
if (real.length > shown.length) console.log(`(${real.length - shown.length} more WARN overlaps not listed: see --json)`);
for (const e of shown) console.log(`[${e.sev}] ${e.t0.toFixed(2)}-${e.t1.toFixed(2)} s  "${e.texts[0]}" x "${e.texts[1]}"  (${Math.round(e.overlap * 100)} % of the smaller box)`);
console.log(`TEXT OVERLAP: ${nFail ? 'FAIL' : nWarn ? 'WARN' : 'PASS'}  (${nFail} fail, ${nWarn} warn; ${data.frames.length} frames sampled every ${step} f)`);
if (jsonOut) fs.writeFileSync(jsonOut, JSON.stringify({ step, minPx, events: real }, null, 1));
process.exit(nFail ? 1 : 0);
