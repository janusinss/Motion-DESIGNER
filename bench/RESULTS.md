# Benchmark results

Append one row per brief per run; never edit a row. Scores are the final-round lens total from an independent, design-blind `motion-critic` jury. `Dims` = Idea / Story / Craft / Design / World / Sound / Originality / Technical.

| Date | Commit | Brief | Engine | Rounds | Lens total | Dims | FAIL / UNVERIFIED | Notes |
|---|---|---|---|---|---|---|---|---|
| 2026-11-27 | f95659f | b1 (pre-bench prompt, same brief) | motionmaxxing | 3 | **7.05** (Motion Awards) | 7/8/7/7/6/8/6/8 | 0 / 0 | Baseline before Director 2.0; `projects/motion-designer-hype` |
| 2026-11-28 | e9ebd82 | b1 | motionmaxxing | 2 (stopped: r2 did not raise the total; blind A/B picked r2 clearly) | **6.95** (Motion Awards) | 7/7/7/7/7/7/6/8 | 0 / 0 scan (jury: 1 UNVERIFIED, audio tail judged from metrics) | ~40 min wall-clock; r1 6.95 → r2 6.95; `projects/bench-b1-e9ebd82` |
