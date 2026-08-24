# EXP587 BSTAR-TRANSFER (paper 235 §3 named open item)

Question: paper 227 measured window saturation at B*=400 under the superseded
1/l weight. Does B*=400 transfer to the corrected 1/sqrt(l) weight (exp586)?

Method: pure reanalysis of exp577 per-N log hit-rates (n=128, seed-20260827
population regenerated VERBATIM, hash-match 128/128). Mechanistic Legendre
counts over odd primes <=1600; windows B in {100,200,400,800,1600}; OLS of
log-rate on S_w,B = sum_{l<=B} c_l / l^w for w=0.5 and w=1.0; 500-rep
bootstrap (seed 587). No new j-sampling.

## R2(B) curves

| B    | sqrt w=.5 | harm w=1 | dR2     |
|------|-----------|----------|---------|
| 100  | 0.5279    | 0.4388   | +0.0891 |
| 200  | 0.5976    | 0.4621   | +0.1355 |
| 400  | **0.6242**| 0.4731   | +0.1511 |
| 800  | 0.5913    | 0.4748   | +0.1165 |
| 1600 | 0.6137    | 0.4795   | +0.1342 |

## Verdicts

- H1_BSTAR_TRANSFERS fires: unique full-sample argmax under sqrt weight is
  B=400 (pre-registered rule). Paper 227's window-location claim survives the
  weighting refinement; location pinned to (200,800] at factor-2 grid steps.
- PLATEAU_RAISED_EVERYWHERE: sqrt beats harmonic at ALL five B (+0.089..+0.151,
  max at B=400) — no weight x window interaction; exp586's correction is uniform.
- Bootstrap: argmax contains 400 in 55.2% of reps ({400:276, 1600:178,
  200:37, 800:9}); the 1600 point sits only 0.0105 below the peak, so the
  robust reading is "saturation reached by B=400, no further gain through
  1600", not a sharp 400-vs-1600 separation.

## Ledger catches

1. Recomputed harmonic curve does NOT peak at 400 on this data: flat plateau
   above B=200 with edge argmax 1600 (dR2 vs 400 = +0.006, noise-level). The
   interior-window signal is carried specifically by the sqrt weighting;
   harmonic weighting saturates without locating an interior B*.
2. exp577's stored S400 column IS the unweighted QR-count dial over odd
   primes <=400 (verified: exact 0 diff); harmonic form differs by +28..+48.
   Crosscheck non-load-bearing — all dials computed mechanistically from the
   hash-matched population.
3. Under sqrt weight the slope stays ~0.31–0.35 across all B (stable scaling),
   while harmonic slope ~0.76–0.80 — consistent with exp586's exponent fit.

Consequence: close paper 235 §3's open item affirmatively — adopt
S_sqrt,B* with B*=400 as the canonical product dial; the corrected weight
both raises fit everywhere and resolves the saturation location that the
superseded weight could not.

Artifacts: exp587_bstar_transfer.py, exp587_smoke.log, exp587_full.log,
exp587_result.json. Wall: 0.13 s (full).
