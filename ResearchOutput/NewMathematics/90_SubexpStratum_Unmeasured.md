# Paper 90 — SUBEXP-STRATUM: The Fourth Stratum Stays Unmeasured at Toy Scale

**Verdict name: THE-STRATUM-STAYS-UNMEASURED (an honest inconclusive).**
Round-26 #3 · exp 425 · assessment v201 · script `/tmp/exp_subexpstratum.py` · log `/tmp/r26n3e.log` · runtime < 60 s.

## 1. What was attempted

Paper 89's landscape had three measured strata; the sub-exponential sieve family (L_{1/2}) was cited, not measured. This round attempted to measure its engine — smoothness economics: is P(x² − N is B-smooth) described by the Dickman function across a (N, B) grid; do trials-per-relation follow 1/ρ(u); can the optimal-B trade-off place the stratum's cost curve between Pollard ρ and poly?

## 2. What the measurements showed

With x drawn uniformly in [√N, 2√N] (so x² − N spans N-scale), per-sample u = log(x²−N)/log B, half-bit bins pooled across six (N, B) cells (2400 samples), compared against **numerically integrated** Dickman ρ:

| u | n | empirical | ±1σ | ρ(u) numeric | ratio |
|---|---|---|---|---|---|
| 3.0 | 161 | 0.0124 | 0.0087 | 0.0487 | **0.26** |
| 3.5 | 265 | 0.0302 | 0.0105 | 0.0163 | **1.86** |
| 4.0 | 413 | 0.0073 | 0.0042 | 0.0049 | **1.47** |
| 5.0 | 303 | 0.0033 | 0.0033 | 0.00036 | **9.27** |
| 4.5 / 5.5 / 6.0 | — | 0.0000 | — | 1e-3 – 2e-5 | — |

**Inconclusive**: the ratios scatter non-monotonically (0.26–9.3), most bins are underpowered at ±σ ≈ 100% relative, and the two zero-bins sit where ρ predicts below MC reach. The toy cost model (C(B) = π(B)/ρ(u) + π(B)²) fits d(log₂C)/d(log₂N) = 0.024 — flat, unable to place the stratum between ρ (0.26) and definition-routes (~1): the π(B)² term dominates at sizes where the asymptotic regime hasn't arrived.

## 3. Two real findings inside the null

1. **The leading-term Dickman approximation is invalid at small u.** The commonly-quoted exp(−u(ln u + ln ln u − 1)) gives 0.561 at u = 3 where true ρ(3) = 0.0487 — a **12× error** — and remains off by large factors through u = 6. Any informal smoothness argument using it below u ≈ 8 is quantitatively meaningless. Proper numerical integration (Euler step 5×10⁻⁴ on uρ′(u) = −ρ(u−1)) is cheap and mandatory.
2. **x²−N smoothness is not random-integer smoothness at toy scale.** Even against correct ρ, the ratios are non-monotone in u — consistent with the known structure (primes dividing x²−N are constrained by the quadratic character of N mod ℓ), whose correction factors are O(1) only in the asymptotic regime that toy sizes cannot reach.

## 4. Method ledger

Three process catches: (1) the first design sampled x in a window of width 10³ making x²−N ~ N^{1/2+}-scale while computing u as if N-scale — the entire first comparison was mis-binned (caught by empirical-above-predicted anomalies); (2) a pre-written success VERDICT over contradicting data — replaced by data-computed output before claims; (3) a trailing-quote syntax break from a patch script — caught by ast.parse.

## 5. Barriers

**(a)** clean — horns pre-stated; the null is reported against them. **(b)** clean. **(c)** confronted — 2400 samples across six cells; the honest limit is that MC-feasible smoothness measurement cannot resolve ρ(u) ≪ 10⁻³. **(d)** clean. **(e)** the substance — the inconclusiveness itself quantified (ratios with error bars, underpowered bins identified). **(f)** controlled — all three defects caught before claims. **(g)** fair — the same kernel/statistic conventions as papers 85–86. **(h)** relevance — the negative result delimits what toy measurement can establish: the fourth stratum requires production-scale sieving to measure, and informal Dickman arguments at small u are unsound.

## 6. What closes

Nothing closes — and the round says so. The landscape stands at **three measured strata plus one unmeasured**; the sub-exponential family's position remains cited-theoretical (its L_{1/2} law resting on smoothness statistics that demand production scale to observe). The programme's open targets are unchanged and now explicitly include: the formal barrier-4 converse proof, and a production-scale measurement of the sub-exponential stratum.

Now 425 experiments. Assessment v201. Paper 90, issue #182.
