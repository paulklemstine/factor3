# Paper 193 — ENERGY-ASCENT: A Magnitude Channel Sees the Berggren Letters

**Verdict name: ENERGY-ASCENT-SIGNAL (H1 refuted — dependence real, mechanism positional, value bounded).**
Round-70 #2 · exp 546 (+ exp546b coordinator scale control) · assessment v300 · scripts `ResearchOutput/scripts/2026-08-21-resume/exp546_energy_ascent_oracle.py` + `exp546b_scale_control.py` (+ `exp546_result.json`, `exp546_data.npz`) · seed 20260823.

## 1. The question

The Berggren line was CLOSED at three strengths: N-node embedding exact-but-circular
(exp 391), slope coordinates orthogonal, branch position ADICALLY SEALED (exp 416:
N mod 3^k carries zero letter-information, worst z=+2.51). All seals are RESIDUE
seals. Open question: does a non-residue channel — the magnitude spectrum of N-derived
sequences — see the branch letters?

## 2. Result: yes, it does

Population: 3000 odd semiprimes (indep/unilog/ratio strata ×1000; p∈[2^14,2^18],
q∈[2^16,2^22]). Pipeline exactness asserted: descent strings via the parent-interval
law, re-ascent lands on (m,n) 3000/3000; Fermat identity m²−n²=pq exact.

Best cell (Fermat-window energy spectrum E(a)=a²−N on isqrt-anchored window W=4096,
height-ratio summary × b₁):

| statistic | value |
|---|---|
| MI(feature ; b₁) | **0.1836 bits** = 19.0% of H(b₁)=0.9642 |
| permutation null z (300 row-shuffles) | **+109 to +120** |
| flagged cells of 225 tested | 69 at z≥3 (chance expectation ≈0.3) |
| joint (b₁,b₂) MI | up to **0.2736 bits** (z≈85) |
| dB-quartile target | OOS acc 0.334 vs chance 0.25 AND majority 0.264 |

**Skew honesty:** b₁ is 78.3% letter-1; on the raw b₁ target the OOS accuracy (0.777)
only MATCHES the always-majority baseline (0.783). The load-bearing evidence is the
dependence itself (MI vs permutation null) plus the minority-structure targets
(joint12, dB-quartile), which beat both chance and their majority baselines out-of-
sample. One flagged cell (z=3.26) failed its OOS gate — the gate works in both
directions.

## 3. Controls — the seals stand

- POSITIVE: factor-derived ratio band → b₁ EXACT, 3000/3000, I=H(b₁).
- NEGATIVE: N mod 3/9/27 features worst z=+1.97 over 15 cells — paper 81's metric
  blindness replicates inside this pipeline.
- GAUSS-MAGNITUDE features (closed-form residue-determined): max z=1.30 over 45
  cells — fully null, as pre-stated.

## 4. Coordinator scale control (exp546b, independent)

The pooled row-shuffle test can be fooled by scale confounding (feature and target
both tracking absolute magnitude). It survives:

| control | MI | z |
|---|---|---|
| pooled (200 shuffles) | 0.1836 | +109 |
| **within-log(n)-bin shuffles** (8 bins, 200) | **0.2104** | **+100** |
| within design strata (3×) | 0.129–0.236 | — |
| within NON-hit class only (n=2732) | 0.1139 vs null 0.0060 | strong |

The channel is not scale, not stratification, and not merely the coarse hit/no-hit
threshold — spectral shape carries ~0.11 bits among non-hits.

## 5. Mechanism: a positional sensor, not a new dial

E(a)=a²−N crosses zero at j=d=m−⌊√N⌋ (the Fermat distance). Hit-in-window rate by
letter: {b₁=1: 0.000, b₁=2: 0.019, b₁=3: 0.673}; corr(log(d+1), log ρ) = **−0.917**
(analytic d ≈ n/(2ρ)). The fixed-window spectrum is a noisy positional readout of the
parabola's zero-crossing distance — which pins the ratio band, which IS the letter.

**Placement in the barrier map:** this does NOT break the residues-cap theorem or any
residue seal — those never covered magnitude/position channels, and paper 132's
residual-gap list explicitly left "positional witnesses" open. The channel joins the
already-measured POSITION family (paper 137: sqrt-descending pays 5.19×; paper 143:
interval hints coverage×width): tree letters are sealed against residues, OPEN to
position, exactly as the map predicts.

## 6. Value and cost

Bounded: 19% of b₁ entropy; direct hit-detection at W=4096 would carry I(hit;b₁)=
0.3035 bits — an optimized window placement closing 0.18→0.30 is the named follow-up.
Cost: ~4.2 ms/N for all spectra (W≤4096 parabola samples) — cheap per draw, but the
window evaluation IS a partial Fermat scan; whether oracle-ascent with this accuracy
beats blind 3^dB and plain Fermat is priced by exp547's (α, c) phase diagram.

Ledger catches: L1 task Gauss formula had no N-dependence (fixed via N mod M′ phases);
L4 smoke-run 1-based letter codes crashed the OOS gate; L5 majority baseline added;
L6 mechanism probe added post-signal. Barriers: 5 amended in scope ("orthogonal" =
residue-adic dials blind, magnitude-position channel open and priced); 2/4/8 unchanged.

Now 546 experiments. Assessment v300.

---

**ERRATUM (2026-08-23, superseded by papers 196–197):** §2's "channel exists" claim is
RETRACTED as an extractable channel and §5's mechanism wording was WRONG. E(a)=a²−N
crosses zero between j=0 and j=1 of any isqrt-anchored window (zero at √N), NOT at
j=d — the event at a=m is the Fermat square-HIT; sign-count sensors are structurally
constant (proven identities). exp551 shows the realized spectral feature is EXACTLY a
magnitude mirror of N: MI(feature ; b₁ | log-N decile) = 0.0000, identical to plain
log N head-to-head. The §5 hit-rate/oracle table stands as a factor-derived bound.
See papers 197 (correction) and 550-recording ledger for the method lesson: row-shuffle
nulls are the wrong null for deterministic functions of N.
