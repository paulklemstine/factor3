# exp589 SPIKE-ORIGIN (round-74) -- findings
Question: is the paper-238 left-edge spike (8.6% D1 mass) carried by
tiny-v hits (bitlen(v)<96)? Pure reanalysis of exp581 npz; Ns
regenerated verbatim exp578 seed 20260828; lineage = 128x2 exact
isqrt->jlo/jhi matches + containment (pop_hash recomputed, no ext copy).

VERDICT: **H0-MIXED**
- fraction of D1 spike mass removed by excluding bitlen(v)<96: 1.0000 (DEGENERATE: D1 => v<2^95 provably, see header)
- fit ALL hits:      w_edge=0.0794 CI[0.0702,0.0908] dAICc=374.77
- fit KEPT (v>=2^95): w_edge=0.0403 CI[0.0301,0.0525] dAICc=49.78 (edge anchored at kept left edge u0=0.110)
- D1 mass by v-band (hits/ctl): <80 0/2 (D1 0/2), 80-89 85/1501 (D1 85/1501), 90-95 2288/83972 (D1 1469/49155), >=96 7221/426525 (D1 0/0)
- Band-referenced D1 excess (POST-HOC): <80 +0, 80-89 +0, 90-95 +130, >=96 +0
- subfit bitlen [96,98) (POST-HOC): hits=3386 w_edge=0.0305 dAICc=5.94
- subfit bitlen [98,1073741824) (POST-HOC): hits=3835 w_edge=0.0240 dAICc=-0.40

READING: split outcome: fraction and refit clauses disagree; see numbers above.

Honest: pre-registered mechanical note fired (exclusion clause structurally degenerate; verdict rode on refit clause); kept-fit edge anchor adaptation registered pre-run; own Poisson fitter (nb=50), not paper-238's b_edge parametrization; controls = capped first-4000 non-hits, position-uniform.
Wall 45.72s; boot 2000 cluster-over-Ns seed 20260902; no commits; only exp589_* touched.
