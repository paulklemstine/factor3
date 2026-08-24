# Paper 226 — QR-VS-OVERDISPERSION: The Recorded Small-Prime QR Dial Does NOT Explain u≈10 Overdispersion — All Three Dial Forms Land Far Below the Pre-Registered Bars (Best D-Reduction 14.2% vs Required 30%), the Task-Specified Primary Is Orthogonal-by-Construction to the Divisibility Carrier (Cov = 0 Exactly), and ≥86% of the Excess Variance Is N-Structure Beyond Every Recorded Mechanism — a Named Map Entry on the Scale-Smoothness Frontier

**Verdict name: NEW-STRUCTURE-MAP-ENTRY** (pre-registered H0 fires; H1 rejected). This paper
unifies two recorded threads — papers 136/139 (per-N smoothness variance of x²−N pools governed
by the small-prime QR dial, calibrated at bitlen 40–48) and paper 220 / exp569c (per-N candidate
hit-counts at u≈10 heavily OVERDISPERSED: top clusters 600/561/540 vs control-max 359,
exposure-corrected D≈29 in exp567) — and asks the unmeasured question: does the QR dial EXPLAIN
the u≈10 overdispersion, or is there unexplained N-structure? Answer: it does not explain it.
Round-78 #2 · exp 576 · sources: `ResearchOutput/scripts/2026-08-24-round74/exp576_qr_overdispersion.py`
(pre-registration in header BEFORE any data generation) → `exp576_result.json` (+ smoke pair),
wall 368.9 s.

## Population and replication

128 balanced bitlen-96 semiprimes, FRESH master seed **20260826**, with stream-distinctness
ASSERTED AND RECORDED against the two prior seeds: pairwise-disjoint N sets, distinct orderings,
hashes e8d89a29a03779d5 (20260824) / 9cb9cc800ee45a38 (20260825) / 81acc9b5e1be619b (20260826).
150k j-samples per N (19.2M total) through the exp569 gcd-chain primorial tester VERBATIM, cut
10⁶; dials via sympy.jacobi_symbol.

The u≈10 phenomenon itself REPLICATES on the fresh population: mean **76.7 hits/N**,
Var/mean **D_raw = 7.27** (φ_null 7.33; Poisson would be ~1), range 29–172, top-3 clusters
**172/151/130** — exactly the paper-220 envelope rescaled (600/561/540 @ ~600k/N ⇒ ~150/141/126
here). The clustering is real and seed-independent.

## Pre-registration (verbatim from the script header)

> **H1 (QR explains it):** with the PRIMARY dial S_indiv, R2_log ≥ 0.25 AND D_reduction ≥ 30%
> where R2_log = OLS R² of log((hits+0.5)/total) on standardized dial, and D_raw =
> Var(hits)/mean(hits) across N (index of dispersion); D_cond = Var(hits − μ̂_GLM)/mean(hits)
> with μ̂ from a Poisson GLM (log link, offset log(total), covariate dial); D_reduction =
> 1 − D_cond/D_raw ⇒ verdict QR-DIAL-EXPLAINS-OVERDISPERSION.
> **H0 (unexplained):** R2_log < 0.10 OR D_reduction < 10% (primary dial) ⇒ verdict
> NEW-STRUCTURE-MAP-ENTRY (u~10 overdispersion is structure beyond the recorded QR mechanism).
> Otherwise ⇒ PARTIAL (report which leg failed/succeeded; secondaries disclosed).

Sign convention stated up front: dial = COUNT of QR-indicator terms; expected direction POSITIVE.
Three dial forms pre-declared: S_indiv (PRIMARY, task-specified paper-139 form), S_prod
(mechanistic secondary), S139@400 (recorded-form replication, tertiary).

## Results

| dial | R²_log | slope | z | rate/unit | φ_model | D_cond | D-reduction |
|---|---|---|---|---|---|---|---|
| S_indiv (PRIMARY, Σ Jac(ℓ,p)+Jac(ℓ,q)=+1, ℓ≤100) | **0.0127** | NEGATIVE | −2.82 | ×0.9917 | 7.36 | 7.21 | **0.88%** |
| S_prod (=#{ℓ≤100: N is QR mod ℓ}, mechanistic) | **0.0781** | + | 10.91 | ×1.0423 | 6.07 | 6.24 | **14.22%** |
| S139@400 (recorded papers-136/139 bound) | **0.0565** | + | 8.71 | ×1.0188 | 6.59 | 6.62 | **9.07%** |

The PRIMARY dial misses H0's escape hatches on BOTH legs (R²_log = 0.0127 < 0.10 AND
D-red = 0.88% < 10%) — H0 fires cleanly. The mechanistic secondary, which is the quantity that
actually governs divisibility (ℓ | x²−N iff Jac(ℓ,N)=+1), does better and is highly significant
(z = 10.9) yet still removes only ~14% of the excess variance. ALL forms land far below H1's
bars (R²≥0.25, D-red≥30%).

## The analytic orthogonality catch (robustness)

A post-hoc but fully analytic observation that makes the verdict robust to dial choice: under
independent characters, **Cov(S_indiv, S_prod) = 0 EXACTLY** by multinomial algebra (the three
indicator classes A/B/C over primes are multinomial; cross-terms cancel identically). Measured
r(S_indiv, S_prod) = **−0.01** (full matrix: S_indiv~S139 −0.055, S_prod~S139 0.568). The
task-specified primary dial is orthogonal by construction to the divisibility carrier — its null
was predictable before the run — but this cannot rescue H1: the secondaries, which DO carry the
divisibility signal, also miss H1. Verdict unchanged either way.

## Consequence: a named map entry

Stated plainly: **the ≤400 QR dial explains at most ~14% of u≈10 overdispersion; ≥86% is
N-structure beyond every recorded mechanism.** The papers-136/139 line — validated with perfect
shape transfer across bitlen 40–48 — does not extend to scale. This is a new entry on the
scale-smoothness map, not a refutation of the earlier work at its own scale.

Scale-shift hypothesis for WHY the law fades: hits require LPF ≤ 10⁶, but every tested dial
covers ℓ ≤ 400 only. At bitlen 96 the candidate pools span ~2⁴⁹–2⁵¹, so the informative prime
window has shifted into 400..10⁶ — exactly where the dial is blind. Papers 136/139 were
calibrated at bitlen 40–48, where small primes dominate the pool.

**NAMED FOLLOW-UP:** product-form dial over ALL ℓ ≤ 10⁶ (computable directly from p, q mod ℓ;
~78k symbols; cheap). If it captures the residual, papers 136/139 and 220 UNIFY under a
scale-dependent dial bound; if not, the residual is genuinely new N-structure at u≈10.

---

## RIDER — P̂ RESOLUTION-LIMIT NOTE (pertains to paper 225's erratum thread, action (a))

From the completed archival dig (`pthat_extraction.md` in the round74 directory; no recorded file
modified): action (a) of paper 225 ("re-extract raw P̂ for 29.1 from papers 137/143 artifacts")
resolves as **NO RAW P_hit EXISTS IN ANY ARTIFACT**:

- exp467 (paper 137 source): orderings are full REORDERINGS of the candidate list — no committed
  window R exists — and the result stores per-ordering/per-stratum MEAN COSTS only. No hit
  indicator, no window counts.
- exp474 (paper 143 source): EXACT enumeration (M=300) under a DESIGNED oracle contract
  "interval covers J w.p. α" — P_hit ≡ α BY CONSTRUCTION, = **1.000000 exactly** at the 29.1×
  cell. No sampling, no trials.
- Therefore all four booked P̂ are DRAFTED-LAW INVERSIONS of speedups (raw or rounded), recovered
  here to ≤2×10⁻⁴ agreement.

Full-precision anchors extracted from raw cells:

| anchor | raw cell (source) | S_meas | P̂ booked | P̂ cert-law-implied |
|---|---|---|---|---|
| 5.19× frontier | asc 6441.7067 / trunc_desc 1240.3181667, n=30000 | 5.193592154916 | 0.8500 | 0.841617 |
| 6.91× trunc-high | stratum r∈[2,4]: 4524.2355344/654.2900603, n=6732 | 6.914724537168 | 0.9003 | 0.894868 |
| 4.35× trunc-low | stratum r∈[1,1.25): 8021.1223969/1842.6333534, n=9651 | 4.353075657862 | 0.8106 | 0.800308 |
| 29.1× α=1 | exact enum M=300 μ=6 α=1: E_base 100.500555556/E_committed 3.450611111 | 29.125436718134 | 0.9853 | **0.985068** |

(P̂_implied = [(1−μ) − 1/S]/(1−2μ); μ=0.05 rows 1–3, 0.02 row 4.)

Findings:

1. **Paper 225's corrected-table arithmetic is EXACT at all loci** — all four recomputed values
   (5.405405 / 7.156659 / 4.535970 / 29.315197) match to ≥6 decimals.
2. **Feasibility margins hold at full precision**: μ ≤ 1/S_raw true ×4 (0.05 ≤ 0.1925/0.1446/
   0.2297; 0.02 ≤ 0.03433); S_A@booked ≥ S_raw true ×4 (margins +0.212/+0.242/+0.183/+0.190).
3. **But the premise "stored P̂" fails.** The 29.1× cell's design value is α=1 exactly; the
   certified-law-consistent P̂ at full precision is **0.985068** (p225's own P_implied=0.98504
   used the ROUNDED 29.1; the true input 29.125437 shifts it by +3.1×10⁻⁵). Booked 0.9853
   OVERSTATES by ~2.3×10⁻⁴ → printed 29.3152 overstates the certified reading by ~0.19. Same
   provenance caveat applies to rows 1–3 (inverted witnesses, ±2×10⁻⁴ spread).
4. Protocol note: exp474's committed protocol pays the miss branch (interval scanned even on
   miss), matching NEITHER pure protocol-A nor the drafted form — the (μ, P̂) mapping is an
   EFFECTIVE CONVENTION, per p225's own F1/F3 lesson.

**Recommendation:** book all four anchors **"at resolution limit"**, not "at stored P̂" — p225's
own admissibility rule (raw-P̂ stored) is NOT met; the corrected table stands as arithmetic while
its loci carry inversion provenance.

---

## Ledger catches

1. **First-smoke GLM divergence fixed pre-full**: bare Newton IRLS overflowed on the smoke run;
   replaced with Fisher scoring + deviance step-halving BEFORE the full run — caught in smoke,
   no data impact on the full result.
2. **Smoke/full slope-sign instability flagged**: S_indiv slope flipped between smoke (n=16, +)
   and full (n=128, −, z=−2.82) with pseudo-R² ≈ −0.001 throughout. Do NOT cite the negative
   direction as a reversal of paper-139 without replication.
3. **Monitor double-fire**: the run monitor fired twice; the result was verified directly from
   JSON — no data impact.

Honest limits (disclosed in JSON): per-N expected hits small (~77), so Poisson noise attenuates
OLS R² — the GLM carries the inference; single fresh seed; zeros smoothed +0.5 only in the OLS
leg, GLM unsmoothed; no paired controls this pass (the question is cross-N variance, not
cand-vs-control drift).

## Barrier validation

Serving the standing directive's scale-smoothness frontier (u≥6–14 deviations): this experiment
measures whether a RECORDED mechanism survives at scale and finds it does not — opening the
mechanism question "what carries per-N clustering at u≥10" as a named map entry with a cheap,
pre-specified follow-up. Papers 136/139 stand at their own scale (bitlen 40–48); nothing here
contradicts them there. Residue cap 4/3 untouched; no complexity claim made; no breakthrough
claimed.

## Bottom line

exp576 fires pre-registered H0 cleanly: the small-prime QR dial — in its task-specified form
(R² 0.013, D-red 0.9%), its mechanistic product form (14.2%), or its recorded papers-136/139
bound form (9.1%) — explains at most a seventh of u≈10 overdispersion. The phenomenon replicates
fresh-seed at full strength (D=7.27, top-3 172/151/130). Orthogonality of the primary to the
divisibility carrier is exact algebra, so the null is structural, not sampling luck. The
remaining ≥86% is N-structure beyond every recorded mechanism; the scale-shift hypothesis names
where to look next (product-form dial over ℓ≤10⁶). Rider: the four D-witness anchors of papers
137/143 have no stored raw P_hit anywhere — book them at resolution limit; paper 225's erratum
arithmetic and feasibility margins survive full precision intact.
