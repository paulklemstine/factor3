# verifyL4 verdict (2026-08-24, adversarial verifier)

Artifacts checked: gapL4_measure.md, gapL4_check.py, gapL4_result.json (replicated from seed, not rerun — originals untouched), barrier4_positional_converse_draft.md (REVISION), paper 219 witness tables. Machine evidence: `verifyL4_recheck.py` -> `verifyL4_recheck_result.json`.

## Per-item verdicts

1. **F1 r̄-identity — PASS** (one completeness flag). EC_A = P·r̄_R + (1−P)·r̄_C is total-expectation given the committed block-top-down policy; independently validated against simulated protocol-A costs (8 random prior×window cells, max rel err 0.0023). T1a certified form emerges exactly at uniform-within-cells (r̄_B=(|B|+1)/2); finite-M rational `(M+1)/[P(μM+1)+(1−P)((1−μ)M+1)]` algebraically confirmed; D-degrades-to-inequality coherent. FLAG: F1's "corrected master inequality" is incomplete as written — Θ is a literal ellipsis (`Θ=(μP+(1−P)(1−μ))/...`, measure.md line 37) and μ_eff is never defined, so the booked bound itself is unverifiable. A3 replicates exactly (rate .4395, max 1.54, witness 62 vs 21.33; diag err 0.0 is real dyadic-FP exactness). Minor: "violations isolated where predicted" unsupported — violation RATE is highest at HEAD placements (60%/37%/34% head/mid/tail).
2. **F2 derivations — PASS.** s=r^{-1/2} trivially correct; π_s(s)=2b(s^{-2})s^{-3} correct change-of-variables; ∫₁^{(1−μ)^{-2}} r^{-3/2}dr = 2μ ⇒ P=μ/(1−R_max^{−1/2}) exact, linear iff canonical; all four required-R inversions and population captures (55%, 17%, saturation ≲1.11) recompute exactly; T1-tight iff g≡const definitional.
3. **F3 max-min — PARTIAL FAIL (unstated payoff convention).** Tail-corner arithmetic right (brute force confirms adversary max-EC = Pk+(1−P)(M−k)). But "= certified law EXACTLY" holds only under a fixed full-scan-M baseline (never stated); under paper-T1a's own uniform C₀=(M+1)/2 baseline the value is (M+1)/(2Md) → HALF the certified law; under same-prior-descending payoff the adversary strictly beats the claim: mass P at R's bottom + (1−P) at C's bottom gives S=[1−(1−P)μ]/d < 1/d (5.365 < 5.4054 at the anchor locus). Same section's degenerate case S→(M+1)/2M uses the C₀ baseline — internally inconsistent. Genealogy (both laws = corner values under two silence semantics) survives modulo convention.
4. **Paper-219 flag — GENUINE TABLE ERROR (P̂-rounding inconsistency), not formula-version difference, not misreading.** Printed rows (both the T1 "witness numbers" table and the Conjecture-D table):
   - `| α=1 extreme 29.1× | 29.1 | (0.02, 0.9853) | 29.0698 |` — 29.0698 = certified@**0.985**, not @printed 0.9853 (=29.3152); drafted@0.9853=29.0647 also ≠ printed. L4 agent read it correctly.
   - `| frontier 5.19× | 5.1936 | (0.05, 0.85) | 5.1948 |` — **additional unflagged defect**: 5.1948 = superseded DRAFTED form 1/(1−0.95·0.85) under a column headed "certified-silence S_A"; certified@locus = 5.4054.
   - `| trunc-high 6.91× | 6.91 | (0.05, 0.9003) | 6.91 |` — 6.91 = drafted@(0.05,0.9003)=6.9100 (stale form, coincides with measurement).
   - `| trunc-low 4.35× | 4.35 | (0.05, 0.8106) | 4.35 |` — 4.35 = drafted@0.8106=4.3491; prose "(0.05,0.8106)→4.649" is doubly wrong (4.649 = certified@old locus (.115,.87)).
   Feasibility unaffected: μ≤1/S and S_cert@P̂≥S_meas hold for all four anchors.
5. **Ranking F1>F2>F3 — PASS** with caveats: order defensible (F1 core proven; F2 one session; F3 heaviest — corroborated by item-3's convention trap). Caveats: Θ-ellipsis makes F1's remaining theorem more than "hours"; "77× breaks 1/μ" (existence) vs F3 corner (min) are different quantifiers — no contradiction once separated; "62× in the constructed witness" means S=62 (ratio 2.91), sloppy wording.

## Resolution (item 4, one paragraph)

The mismatch is a genuine precision/bookkeeping error inside paper 219's tables, correctly flagged by the L4 agent: the 29.1× row prints locus P̂=0.9853 while its S_A value 29.0698 was computed at the 3-dp rounding P=0.985 (certified form at the printed 0.9853 gives 29.3152; the drafted form gives neither value, ruling out a drafted-vs-certified mix-up for this specific row; the draft's Conjecture-D section itself uses 0.985 consistently). The entire feasibility question lives in the 4th decimal of P̂ — P_implied by measured 29.1 is 0.985037 — exactly as gapL4_measure.md states. Additionally (not flagged by the L4 agent) the other three table rows still carry pre-revision DRAFTED-form law values under a certified-law header, and the 4.35 prose value 4.649 belongs to a stale μ=0.115 locus.

## Recommendation

**Record-with-fixes**: adopt F1-form+F2-calibration framing as proposed; require fixes — (a) define Θ and μ_eff before stating the master inequality, (b) state F3's payoff/baseline convention explicitly, (c) regenerate paper 219's anchor-table S_A values at stored P̂ and relabel or recompute the three stale drafted-value rows, (d) soften "violations isolated where predicted".

Verifier artifacts (only files touched): `verifyL4_recheck.py`, `verifyL4_recheck_result.json`, `verifyL4_verdict.md`.
