# exp578 HIT-POSITION-STRUCTURE (round-74) — findings
VERDICT (pre-registered): **H1 POSITIONAL-STRUCTURE-REAL**, amended after the
coordinator-directed magnitude-confound check to **BEYOND-MAGNITUDE**: hit
j-positions deviate from uniform WITHIN-N, and the deviation SURVIVES full
conditioning on v-size — not a smoothness-decay artifact.
Setup: 128 balanced bitlen-96 semiprimes, FRESH master seed 20260828, hash
06931068f8f3ca9b; lineage quartet e8d89a29/9cb9cc80/81acc9b5/a15e2877 REPRODUCED,
pairwise disjoint. 150k j-samples/N on [isqrt+1, 3·isqrt], exp569 tester verbatim,
cut 1e6; every hit position stored (exp578_positions.npz). Wall 363 s.
Dispersion replicated 4th time: mean 74.95 hits/N, D_raw 6.37, min/max 29/136.
LEGS (treatment | paired non-hit control):
(a) pooled KS u vs U[0,1], 9565 hits / 127 HITRICH(≥30) Ns: **D=0.09519,
p=6.9e-76 FIRES** | control D=0.00693, p=0.744 null — pipeline clean.
(b) lag-1..10 spatial autocorr (1000 bins): mean ρ=+0.00283, boot95
[0.00112,0.00475] excludes 0 but « 0.05 bar → no fire | TRUE repaired control
ρ=−0.00112 [−0.00278,0.00051]. No local-clustering component at bin scale.
(c) edge-decile frac 0.2346 vs p0=0.20, binomial p=1.1e-16 but point < 0.25
bar → no fire | control 0.1935 null.
MAGNITUDE CONFOUND CHECK (v=j²−N monotone ⇒ pure decay skews small-u): strata
(bitlen(v)×mantissa-octant); all 9594 hits fall in 8 cells; vs SIZE-MATCHED
non-hits per-cell two-sample KS fires 7/8 cells at p<0.01 (null 0.08), median
cell p=1.9e-5; pooled stratified D=0.10423 ≥ unstratified 0.09519;
within-cell permutation p<0.0005 (0/2000); stratified-edge z=10.08
(2248 obs vs 1858 expected). Decile profile T=[.162,.123,.109,.097,.091,.091,
.090,.084,.081,.072] monotone-declining vs control flat ≈[.10…].
READING: hits concentrate toward small-j ~10× stronger than magnitude predicts;
the positional profile is REAL within-N geometry of the smooth locus of j²−N —
opens "polynomial-sequence local structure" as a carrier for the ~39–61%
unexplained per-N overdispersion. Next: is the u-profile shape universal or
does IT cluster by N (hidden N-level covariate at last measurable in-j)?
Self-catches: CONTROL-arm leg-b mirrored treatment in run 1 (acf read hit
arrays unconditionally) — repaired from npz by exp578_stratified_check.py,
verdict unaffected (leg-b fired nowhere); confound-check rule pre-stated before
running it. Smoke 21.8 s PASS (plumbing only; HITRICH empty as pre-disclosed).
Files: exp578_hit_position.py (pre-reg header + repair annotations),
exp578_smoke.log/_result.json/_positions.npz, exp578_full.log,
exp578_result.json (+magnitude_confound_check block), exp578_positions.npz,
exp578_stratified_check.py, this file.
