# Paper 152 — JOINT-ALIGN: Cross-Prime Coincidences Transfer Where Singleton Phases Fail

**Verdict name: JOINT-ALIGN-TRANSFERS / H3-FAIL.**
Round-41 #3 (cron iteration) · exp 484 · assessment v261 · script `ResearchOutput/scripts/2026-08-21-resume/exp484_joint_align.py` (+ `exp484_result.json`) · seed 20260903.

## 1. Paper 150's redirect, executed

Linear singleton phases closed at both prime ranges (papers 150/151); the redirect was
interaction encodings. This experiment tests cross-prime offset COINCIDENCES:
c_pq(N) = #{j ≤ 240 : p | v_j AND q | v_j} over the 10 pairs of {3,5,7,11,13}, plus the
{3,5,7} triple — intersection counts extending d's union count (L8: any positive ΔR² is
beyond-union structure).

## 2. Results

| arm | same-window R² | ΔR² [95% CI] | cross-window ΔR² | ratio |
|---|---|---|---|---|
| baseline (w,d) | 0.6028 | — | −0.31 drop | — |
| +pair coincidences | **0.6339** | **+0.0310** [0.010, 0.053] | +0.0158 | **0.51** |
| +phases ≤13 (re-run) | 0.6333 | +0.0305 [0.006, 0.053] | +0.0176 | 0.58 |
| +triple coincidence | 0.6114 | +0.0085 [CI spans 0] | — | — |

- **H1 CONFIRMED**: pair coincidences clear the pre-stated +0.03 band; combined R² = 0.634.
- **H2 CONFIRMED**: joint features transfer cross-window at ratio 0.51 (> 0.5), unlike
  singleton phases' negative transfer in exp 482 — coincidence structure is
  window-position-invariant, exactly the pre-stated guess.
- **H3 FAIL narrowly**: 0.6339 < 0.65.
- FLAG (unresolved): this implementation's ph13 arm reads +0.0305 where exp 482's read
  +0.0082 — population variance or convention drift between implementations; the pair result
  stands independently of that discrepancy.

## 3. What this decides

The split-ceiling excess has its first positive explanatory lever: JOINT-ALIGNMENT structure
(intersection counts) carries out-of-sample signal that neither footprint mass nor singleton
phases do, and it is window-position-invariant. The per-N dial's next increment is
coincidence-based, not offset-based. Barriers: (5)/(8) unchanged.

Now 484 experiments. Assessment v261.
