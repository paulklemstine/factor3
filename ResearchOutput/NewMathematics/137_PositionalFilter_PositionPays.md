# Paper 137 — POSITIONAL-FILTER: Position Pays 5.19× — the Stratum Beyond the Residue Cap Is Live

**Verdict name: POSITION-PAYS-5.19X (positional-cap guess refuted).**
Round-38 #3 · exp 467 · assessment v246 · script `ResearchOutput/scripts/2026-08-21-resume/exp467_positional_filter.py` (+ `result.json`) · seed 20260821.

## 1. The stratum paper 132 left open

Paper 132 proved the barrier-4 converse for RESIDUE information (cap 4/3, batteries
included) and named what escapes it: witnesses whose ordering uses N beyond residues —
magnitude/position information. This experiment prices that stratum: orderings of trial
division's candidate list induced by N-computable magnitude features, measured as expected
divisibility-test counts on 30,000 random semiprimes (p,q ∈ [2^15, 2^17], 5 batches).

## 2. Results

| ordering | speedup | test-only |
|---|---|---|
| ascending (baseline) | 1.0000 | — |
| **sqrt-descending** (= Fermat's visitation order on divisibility tests) | **5.1936×** | 5.1570× |
| truncation-pruned ascending | 4.8010× | 4.8143× |
| learned Bayes (top-10-bit features, train/test split) | 3.72 all | **3.3735×** |
| learned bucket selector | 5.29 all | 5.03 — does NOT beat plain descending out-of-sample |
| SHAM (wrong-N pairing) | 1.45–1.76× | — |

Real beats sham 3.16× — the gain is genuine N-dependence. **Two separable mechanisms with
OPPOSITE gradients** across balance strata q/p ∈ [1,1.25] / [1.25,2] / [2,4]:
- (a) **Fermat-type balance bet** (sqrt-descending): 20.67× / 4.74× / 1.97× — concentrated
  at near-squares, exactly the pre-stated H1 shape;
- (b) **range truncation** (truncation-pruned ascending): 4.35× / 4.73× / 6.91× — the finite
  pool makes feasibility r ≥ N/2^17, which N's magnitude reveals; runs the OPPOSITE way.

The learned Bayes ordering (3.37× test-only) refuted my own pre-stated smooth-posterior
theorem ("magnitude-Bayes collapses to ascending"): the designed check d1 ≡ ascending passed
30000/30000 exactly — the collapse holds for the smooth posterior 1/(r·log(N/r)) and FAILS at
the pool's truncation edge. The honest computable frontier is plain sqrt-descending: the
learned selector's apparent edge (5.29×) was train-inflation (5.03× test).

## 3. What this decides

Paper 132's converse cap genuinely stops at residues: N-computable MAGNITUDE information buys
a real, sham-controlled 5.19× expected trial-division speedup — bounded not by a universal
constant but by the population's ratio structure (20.67× at near-squares, 1.97× unbalanced).
The barrier map now reads: residues cap at 4/3 (theorem); position pays 5.19× here
(measurement, mechanism decomposed); the two strata are separated by exactly the
uniform-marginal lemma's scope. Accounting: expected divisibility-test counts (information),
not wall-clock; features O(1) per N. Barrier lines: (8) FERMAT-IN-DISGUISE named and measured
— the winning order IS Fermat's, applied to trial division's test; (2) the gain is the p/q
symmetry broken at the √N pivot; (4) clean aggregation, no single ordering dominates both
regimes.

Method ledger (7): ML#4 — my pre-stated theorem refuted by pool truncation, disclosed with
the passing d1≡asc control; ML#6 — a vacuous feature (identically 1+O(1/√N)) caught and
replaced; plus five mechanical catches, all in the script header.

Now 469 experiments. Assessment v246.
