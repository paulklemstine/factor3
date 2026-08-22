# Paper 164 — QRLOTTO-DIAL: The Zero-Fit Theory Dial Holds

**Verdict name: THEORY-DIAL-HOLDS (H1 pass; bits sufficient; cascade retired).**
Round-43 #4 (cron iteration) · exp 495 · assessment v273 · script `ResearchOutput/scripts/2026-08-21-resume/exp495_qrlotto_dial.py` (+ `exp495_result.json`) · seed 20260926.

## 1. The consolidation

Paper 163 resolved that the yield dial's pair content is the per-prime QR lottery. Final
question: is a NO-FIT closed-form dial available? T(N) = Σ 2/p over QR primes p ≤ 400 —
pure first-principles footprint, zero fitted coefficients.

## 2. Results (two independent implementations, same design)

- **H1 PASS**: Spearman(T, rate) = **0.755** (coordinator lean) / **0.7264** (agent full);
  OOS R² with one global scale C = **0.541 / 0.5335**.
- **H2 SPLIT**: the 8-bit QR-indicator model meets the 0.45 bar (0.541/0.4634) but LOSES to
  the (w, d) dial by −0.13 — while T-only beats the fitted-bit model. The full p ≤ 400
  support matters; the 9-bit truncation underperforms the theory sum.
- **H3 PASS STRONG**: measured fractions add −0.0131/−0.0039 over the bits — the indicator
  vector is SUFFICIENT (paper 163's lottery confirmed at the marginal level). Lottery table:
  mean n_p | QR = 2/p to four decimals; QNR = 0.0000 exactly.
- Cascade survival variant T₂ UNDERPERFORMS T (0.40 vs 0.53) — retired.
- Combined (bits + fractions + T + T₂) reaches 0.6259, +0.029 over the paper-145 baseline.

## 3. What this decides

**Adopted: T as the closed-form dial** — rate(N) ≈ C·T(N), one scale, no fitting — with
w's full p ≤ 400 support retained over the bit truncation, and the survival cascade retired.
The per-N yield dial's final form is now fully theory-derived: no fitted coefficients beyond
a global scale. Barriers: (5)/(8) unchanged.

Now 496 experiments. Assessment v273.
