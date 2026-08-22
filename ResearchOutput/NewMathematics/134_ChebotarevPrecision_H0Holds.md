# Paper 134 — CHEBOTAREV-PRECISION: The Master Table Reproduces Simultaneously

**Verdict name: H0 — PRECISION HOLDS.**
Round-37 #6 · exp 463 · assessment v243 · script `ResearchOutput/scripts/2026-08-21-resume/exp463_precision.py` (+ `exp463_result.json`, `exp463_full_run.log`) · seed 20260821.

## 1. First simultaneous re-measurement of the entire master table

Over ~128 papers the lab measured the type-channel law field by field, across different
rounds, populations, and seeds. This experiment re-measures ALL 15 canonical fields under
ONE protocol — one sieve (295,946 unramified primes < 2²² per field), one seed, fresh law
values computed in-code from explicit permutation groups (conjugacy classes × commutator-
subgroup cosets) — against the pre-stated budget: any field deviating > 0.01 bits from the
law is a FLAG.

## 2. Results

| field | m* | H_meas | H_law | I_meas | I_law | I_recorded | Δ(law) |
|---|---|---|---|---|---|---|---|
| S3a x³+x+1 | 31 | 1.4589 | 1.4591 | 1.0000 | 1.0000 | 1.0000 | −0.0000 |
| S3b x³−x+1 | 23 | 1.4584 | 1.4591 | 1.0000 | 1.0000 | 1.0000 | −0.0000 |
| S3c x³−2 | 3 | 1.4588 | 1.4591 | 1.0000 | 1.0000 | 1.0000 | +0.0000 |
| S3d x³−4x+1 | 229 | 1.4586 | 1.4591 | 0.9998 | 1.0000 | 1.0078 | −0.0002 |
| C3@7 | 7 | 0.9182 | 0.9183 | 0.9182 | 0.9183 | 0.9182 | −0.0001 |
| C3@9 | 9 | 0.9181 | 0.9183 | 0.9181 | 0.9183 | 0.9182 | −0.0002 |
| C3@13 Q(ζ₁₃)⁺ | 13 | 0.9183 | 0.9183 | 0.9183 | 0.9183 | 0.9183 | −0.0000 |
| C4 Φ₅ | 5 | 1.4997 | 1.5000 | 1.4997 | 1.5000 | 1.4989 | −0.0003 |
| C5 Q(ζ₁₁)⁺ | 11 | 0.7221 | 0.7219 | 0.7221 | 0.7219 | 0.7198 | +0.0002 |
| C6 Q(ζ₁₃)⁺ | 13 | 1.9183 | 1.9183 | 1.9183 | 1.9192* | −0.0000 |
| C8 Q(ζ₁₇)⁺ | 17 | 1.7497 | 1.7500 | 1.7497 | 1.7500 | 1.7474 | −0.0003 |
| V4 x⁴−2x²+9 | 8 | 0.8108 | 0.8113 | 0.8108 | 0.8113 | 0.8092 | −0.0005 |
| D4 x⁴−2 | 8 | 1.9051 | 1.9056 | 1.6554 | 1.6556 | 1.6555 | −0.0002 |
| A4 x⁴+8x+12 | 9 | 1.1882 | 1.1887 | 0.9181 | 0.9183 | 0.9188 | −0.0002 |
| F20 x⁵−2 | 5 | 1.6797 | 1.6805 | 1.4997 | 1.5000 | 1.4989 | −0.0003 |

(*C6 recorded column omitted for width; historical 1.9192 vs simultaneous 1.9183.)

**GLOBAL max |I_meas − I_law| = 0.00048 bits — 20× inside tolerance. No flags.**
Hard gates: sympy ground-truth validation 0 mismatches (150 primes × 15 fields); abelian
residue-order dictionaries 100% per-prime agreement on all 7 abelian fields; thickening
S3a m*=31→961: Δ = −0.00044; coprime-modulus flatness (mod 101, six fields spanning all
families) all BELOW the permutation-null bias floor; fresh law constants matched hand-derived
values to 6 decimals on all 10 groups (incl. D₄ = 1.655639, A₄ = 0.918296).

The one anomaly: S3d's RECORDED 1.0078 sits +0.0078 above the exact law value 1.0000 — the
simultaneous re-measurement gives 0.9998 ± 0.001, diagnosing the historical number as
small-population plug-in bias on the sparse 229-class dial (within the pre-stated
max(0.01, 3σ)), not physics and not dictionary drift. C4/F20's recorded 1.4989 vs exact
1.500000 confirms paper 82's "loss exactly 0" reading at higher precision.

## 3. What this decides

The lab's ~128-paper measurement record is internally consistent: the type-channel law
I(p mod m*; T) = H(T) − E[H(T | [G,G]-coset)] reproduces to 5×10⁻⁴ bits across all 15 fields
simultaneously — a VERIFICATION result whose value is the precision statement itself,
extending the reproducibility-audit line (papers 97/103) from stored-seed re-runs to
cross-field simultaneous measurement.

Method ledger (7 catches, ALL before results were produced): D4 generator chosen as a
transposition → closure was S₄ (exposed by pre-stated hand-derived law constants); F20 seeded
with two translations → C₅ not AGL(1,5); polynomial "one" initialized as np.ones_like;
square-and-multiply scanned exponent bits LSB-first under an MSB-first Horner recurrence;
ramified test q²|disc missed squarefree-disc ramified primes; abelian dictionary assert wrong
when distinct cosets share a cycle type; two design misregistrations disclosed (permutation-
null z is a dependence-significance statistic, not a law-deviation statistic; Miller–Madow
correction adopted over null-mean over-correction).

Now 466 experiments. Assessment v243.
