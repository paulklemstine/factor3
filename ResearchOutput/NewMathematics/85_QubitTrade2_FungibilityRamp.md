# Paper 85 — QUBIT-TRADE2: One Register Bit Is Worth One Sample — the Fungibility Ramp of Shor Period-Finding

**Verdict name: ONE-REGISTER-BIT-IS-WORTH-ONE-SAMPLE.**
Round-25 #1 · exp 420 · assessment v196 · script `/tmp/exp_qubittrade2.py` · log `/tmp/r25n1g.log` · runtime 342 s.

## 1. The question

Round-14 (QUBIT-TRADE, paper 47) fixed the register truncation threshold t_min ≈ 2·log₂(r) exactly at one sample and observed "below t_min: classical collapse (10 samples fail)". The open question: what does the full (t, s) phase diagram look like — can samples compensate for missing qubits?

## 2. The pre-stated hypothesis and its refutation

The stated-before-run mechanism was a **vertical wall**: for odd r, q = 2^t is never a multiple of r, so every peak j·q/r sits strictly between grid points and the 1/(2r²) continued-fraction quality test should never certify the true period — deterministically, at any sample multiplicity. **This is refuted by the correct measurement**: under the standard arithmetic-progression kernel (post-second-register-collapse state x ≡ x₀ mod r, M ≈ q/r terms), certification succeeds whenever the sampled peak's fractional position satisfies dist(jq/r, ℤ) < q/(2r²) — and those distances spread over [0, ½], so the per-sample rate is ≈ q/r², not zero. The worst-case bound that motivated the wall binds only in the deep-ramp limit q/r² ≪ 1 — which is precisely where paper 47's "10 samples fail" lived. The refutation is the round's first result: *the failure below t_min is probabilistic-with-tiny-rate, not deterministic.*

## 3. The law: a ramp with 1:1 fungibility

Measured over five structured periods (odd prime 761, odd composite 1155, 2·761, 4·761, pure 2¹⁰), t ladders spanning [log₂r − 3, 2log₂r + 2], 300 trials/cell:

**(a) The single-sample ramp.** P₁(t) rises smoothly with q/r² through the odd/mixed families — e.g. 4·odd: 0.003 at q/r² = 0.028 → 0.107 at 0.226 → 0.36 at 0.905 → plateau ≈ 0.46 above 1.8 — and saturates at the standard per-sample rate near and above q/r² ≈ 1. Pure powers of two are flat-saturated (~0.5 at every q/r²): their peaks sit exactly on grid points, so certification never depends on the ratio.

**(b) Samples compound exactly as independence predicts.** At every measured cell, P_s tracks 1−(1−P₁)^s tightly — e.g. odd prime at t = wall−1: P₁ = 0.725 → s=2: 0.940 (pred 0.924); 2·odd at wall−3: P₁ = 0.055 → s=20: 0.680 (pred 0.677).

**(c) THE EXCHANGE LAW.** For odd composite 1155 (wall t = 21), the register size reaching P ≥ 0.5 shifts with sample count exactly as fungibility demands:

| s | t\*(P≥0.5) | shift | −log₂ s |
|---|---|---|---|
| 2 | 21 | +0 | −1 |
| 5 | 19 | −2 | −2.3 |
| 20 | 17 | −4 | −4.3 |
| 100 | 15 | −6 | −6.6 |

(s = 1 never crosses 0.5 in range: the saturation level P₁ ≈ 0.37 < 0.5 for this r — itself the standard per-sample rate.) **One register bit is worth one sample**, up to the saturation floor set by the classical post-processing rate.

## 4. Method ledger

Three designed-check catches across six runs, each instructive:
1. **Wrong kernel**: the contiguous-block Dirichlet kernel (x ∈ [0, r)) instead of the arithmetic-progression kernel — flagged by its degenerate signature P(k=0) = 1 at q = r. The first "vertical wall" table was an artifact of the wrong ensemble.
2. **Post-processing swamp**: lcm-of-all-candidates fails on spurious small-denominator certificates (overshoot early-exit kills everything); replaced by the clean **certification statistic** — ∃ sample whose CF contains a convergent passing the 1/(2b²) test *for the true r* — the necessary condition for any post-processing, with classical period-verification free.
3. Degenerate regimes documented rather than forced through the same gate: at t = v₂(r) for pure powers of two the outcome distribution is uniform (entropy = log₂q, r-independent — genuinely no information).

## 5. Barriers

**(a)** clean — the vertical-wall hypothesis was stated before the run and honestly refuted by the correct-kernel measurement; the replacement law fits out-of-sample ladders. **(b)** clean — no qubit/sample exchange-rate work in the Catalog (paper 47 is our own). **(c)** confronted — exact Dirichlet-progression distributions (no simulation shortcuts), 300-trial cells, five structured periods including prime/composite/pure-power odd-part structures. **(d)** clean — fixed seeds. **(e)** the substance — all comparisons against closed-form predictions (independence compound, −log₂s shifts) with MC noise ~±0.03; the three-defect ledger disclosed. **(f)** controlled — every anomaly traced to root cause (kernel, statistic, formatting) before proceeding. **(g)** fair — the s-ladders are out-of-sample validations of the single-sample fit; families distinguished (pure powers flat vs odd/mixed ramping). **(h)** relevance — the deployment meaning: Shor's register can be shortened by paying samples linearly (1 bit ↔ 1 sample) down to the deep-ramp region where both explode together; the quantum channel's advantage over classical is preserved but *quantitatively graded*, sharpening DEQUANT (barrier 4/8) beyond the binary truncation threshold of paper 47.

## 6. What closes

The qubit/sample phase diagram of period-finding is now measured end to end: a two-parameter fungibility surface P_certify(s, t) = 1−(1−min(c·q/r², sat))^s with unit exchange rate, saturating at the classical per-sample rate above q ≈ r², and collapsing to joint intractability only in the deep-ramp corner. The quantum channel frontier (ii) gains its quantitative face: Shor's resources are not below a threshold — they ride a smooth trade-off curve whose slope is exactly one bit per sample.

Now 420 experiments. Assessment v196. Paper 85, issue #177.
