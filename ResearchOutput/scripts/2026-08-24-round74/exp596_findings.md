# exp596 COVARIATE-INTERACTIONS — FINAL (verified data)

**Final verdict: H0_ADDITIVE_COMPLETE on CONFIRMED-lineage data.**
Provenance: archived_N_vector_seed20260827.json == exp577 rows[].N order-for-order
(128/128); functional hash reproduces exp586's headline EXACTLY:
R2(y ~ S_sqrt400) = 0.624219 (6 decimals). Counts = exp577 rows[].hits/total,
zero resampling anywhere.

## Registered interaction test (primary)
- Additive model (S_sqrt400 dial + neighbor omega_bar(N+-delta, 1e5-bound)):
  R2_add = 0.6245.
- + pairwise interactions: R2_int = 0.6253.
- DeltaR2 = +0.00079; adjusted DeltaR2 = -0.00227; permutation p = 0.62
  (500 interaction-block shuffles; permuted-y control null, max ctrl dR2 = 0.059).
- Rule: DeltaR2 < 0.02 -> **H0 fires**: the additive model is complete; covariate
  COMBINATIONS absorb none of the residual; the residual is irreducible
  sampling noise at these powers.

## Secondary (exploratory): add stored raw S400 as third class
- DeltaR2 = +0.0018, p = 0.87 -- also null. Dial alone carries essentially all
  predictable variance (~0.62 of 1.0); nothing else adds material signal.

## Design amendment (honest limit on the upgrade)
The parity class was DROPPED: exp577 rows store no hit positions and the
exp581_regen_positions.npz hit/ctl arrays belong to a DIFFERENT generation than
exp577 (its jlo/jhi windows differ from rows[].lo/hi) -- that npz was the root
cause of all earlier hash failures. The additive-completeness claim therefore
covers dial x neighbor (+ raw-S400 in secondary) but NOT a possible pure
parity-interaction carrier, for which no legitimate data exists.

## Ledger catches / resolutions
1. ROOT CAUSE closed: earlier INVALID verdicts came from pairing any pool with
   exp581-npz counts (wrong generation). Never use that npz as exp577-family y.
2. Provenance lesson recorded: string-match + exact headline-R2 reproduction is
   the verification standard; both now pass.
3. Four-way-negative coverage claim COMPLETE (within stated parity limit):
   QR-dial, neighbor, positional, S_indiv individually AND jointly-additive AND
   pairwise-interactions all fail to beat R2 ~= 0.62 -> residual irreducible.

## Artifacts
exp596_covariate_interactions.py | exp596_smoke.log | exp596_result.json
