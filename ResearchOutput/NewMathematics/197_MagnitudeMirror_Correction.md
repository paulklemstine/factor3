# Paper 197 — MAGNITUDE-MIRROR: The Energy-Ascent Channel Retracted; the Tree Sealed Against All Realized Probes

**Verdict name: ENERGY-ASCENT-ARTIFACT (papers 193/195 retracted and replaced).**
Round-70 #6 · exps 549 + 551 · assessment v304 · scripts `exp549_window_frontier.py` + `exp551_magnitude_mirror.py` (+ JSON/npz artifacts) · seeds 20260824 / 20260823.

## 1. The mechanism catch (exp549 L9)

The smoke-run pipeline check REFUTED the assumed mechanism of papers 193/195:
E(a)=a²−N crosses zero between j=0 and j=1 of ANY isqrt-anchored window (the zero is
at √N), NOT at j=d. What sits at a=m (step d) is the Fermat square-HIT. Consequence,
proved as structural identities on every design×budget block (20/20): sign-count and
bracket sensors are CONSTANT across N (exactly one crossing per window) —
**MI(hits;b₁) = MI(bracket;b₁) = 0.000000 exactly**; flip-position ≈ frac(√N) null
(0.0042 bits, z≈−0.7).

## 2. The kill shot (exp551)

Head-to-head on the exp546 population (12 quantile bins, 150 shuffles):

| feature | pooled MI | z | within-fine-(n,m)-cell MI |
|---|---|---|---|
| spectral hratio (exp546's best) | 0.1836 | +124 | 0.0629 |
| **plain log N** | **0.1836** | **+117** | **0.0629** |
| ⌊√N⌋ | 0.1836 | +108 | — |
| frac(√N) | 0.0048 | −0.3 | 0.0426 at z=−0.5 |

And decisively: **MI(spectral feature ; b₁ | log-N decile) = 0.0000 exactly**
(null mean 0, sd 0, z=0.0 over 80 shuffles × 12 strata). The realized "channel" is a
deterministic monotone function of N's own magnitude — information we already have by
knowing N. Its population-level dependence on b₁ is scale stratification (at fixed n,
larger m ⟺ larger ρ ⟺ letter shifts), not extractable structure.

## 3. What survives

- The ORACLE positional bound (factor-derived, not an N-only cell): I(1{d≤B};b₁)
  rises 0.027 @ B=64 → 0.305 @ B=4096 → peaks **0.4798 @ B≈22758** (B* = 10420 gives
  ≥90%); d median 215782, so saturation is driven by letter-3's small-d tail ~20×
  below median. Real geometry — unrealized by any tested probe.
- exp547's cost laws and breakeven pricing (stipulated oracles) unaffected.
- exp548's Price/Gauss results independent (different features, different controls).
- Budget economics: realized MI flat in B down to 64 probes (0.016% of one Fermat
  scan) — now reinterpreted as "flat because it never was channel"; bits-per-probe
  ∝ 1/B exactly.

## 4. Round synthesis — REVERSED in the seals' favor

The energy-ascent question is closed at FOUR strengths: (i) residue dials blind
(paper 81, replicated); (ii) Gauss-magnitude features are residue dials (paper 196);
(iii) sign-count/bracket sensors structurally blind (this paper, proven identities);
(iv) spectral summaries are magnitude mirrors carrying zero bits beyond known-N
(this paper, exact conditional null). The only real content is the factor-derived
oracle bound, which no cheap N-only probe realizes; recovering the path string from
magnitudes would require resolving Gauss digits at every depth — the scan again.
**The Pythagorean tree stands sealed against every realized probe class tested.**

## 5. Method lesson (joins the paper-70 null-design lesson)

Row-shuffle permutation nulls are the WRONG null for deterministic functions of N:
any fine monotone function of N inherits population scale-stratification and flags
z≫3 against a row-shuffle null. The correct controls CONDITION ON MAGNITUDE (log-N
strata / fine (n,m) cells) or test out-of-sample transfer beyond knowing N. Papers
193/195 carry appended errata pointing here.

Count line: 550 experiments (max id). Assessment v304.
