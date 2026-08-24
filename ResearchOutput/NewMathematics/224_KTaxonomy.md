# Paper 224 — K-TAXONOMY: GAP-L8 CLOSED — Three k-Quantities Formally Defined and Never Conflated (k_pin · k_opt^cost · k_opt^econ), With an Exact Identity Showing econ ≡ census Under the Anchor Map W ↔ 2(T₀−1) and a +1.000 Resolution of Paper 219's "+~1" Note

**Verdict name: TAXONOMY CLOSED / definitional** for GAP-L8 of paper 219's roadmap,
closing draft items L8 + O5 ("pin exp563's k\* definition … paper must name which").
The lab has used "k\*" for three different quantities across papers 212 → 219 → 563:
the pinning/saturation point, the census total-cost-minimizing stop, and exp563's net-economics
optimum. This paper fixes all three as named, non-interchangeable functionals, proves the two
"optimum" conventions are ONE objective under an exact anchor substitution, shows unconverted
same-number inputs differ by EXACTLY +1.000 query (resolving paper 219's approximate "+~1"
note precisely), and adopts a naming rule that bans the bare symbol.
Round-77 #2 · theory deliverable, NO new physics run · sources: `barrier4_positional_converse_draft.md`
T2(c)/(d) · `exp563_seqhint_compounding.py` H3 block (`A=Tbar−1; et=A/2^k+1+k`) · `exp563_result.json`
· finite check `gapL8_check.py` (<2 s) → **ALL PASS**.

## The three definitions (verbatim from gapL8_k_taxonomy.md)

1. **k_pin := min{k : W/2^k ≤ 1} = ⌈log₂W⌉** — GAIN-SATURATION point. Generating question:
   *after how many adaptive queries do FURTHER queries add zero speedup?* Marginal gain hits
   exactly zero; support fully pinned; s(k≥k_pin)=T₀/E[T_pin] flat. exp563 witness: 100% of N
   pinned at k=20=⌈log₂W⌉ (bitlen-40 ⇒ W=isqrt(N)−1 ∈ [2^19.5, 2^20)); s(≥20)=T₀ exactly.
   Paper 212's "k\*=⌈log₂W⌉" is THIS object, not an optimum.

2. **k_opt^cost := argmin_{k≥0} V(k,W), V(k,W) = k + (W/2^k+1)/2** — COST-OPTIMAL stop
   (T2 census). Generating question: *at what k is TOTAL work (paid queries + expected residual
   top-down scan, uniform prior on support W) minimized?* Verified: dyadic W ⇒ tie set
   {log₂W−2, log₂W−1} with V\* = log₂W + ½ EXACT (W = 2..4096); continuous location
   log₂(W ln2) − 1 = log₂W − 1.5288; sits 1–2 queries BELOW k_pin.

3. **k_opt^econ(T₀,c_q) := argmax_k T₀/[1+c_q·k+(T₀−1)/2^k]** — NET-ECONOMICS optimum
   (exp563 H3). Generating question: *at what k is net speedup maximized once every query is
   PAID c_q against the MEASURED stratum baseline T₀?* Residual charged at full remaining
   expected scan (draw-law anchor), not half-support. Continuous argmin: 2^k = (T₀−1)ln2/c_q ⇒
   **k_opt^econ = log₂((T₀−1)·ln2/c_q)**; c_q = 1 in exp563. Measured 10 (balanced,
   predicted 9.536549) and 18 (unbalanced, predicted 17.597922) — nearest-integer agreement
   in both strata.

## Exact identity and conversion

The two objectives are ONE function after a single anchor substitution (additive constants
never move an argmin):

    E(k; T₀, c_q=1) = 1 + k + (T₀−1)/2^k  ≡  V(k; W=2(T₀−1)) + ½      (pointwise identity)

    ⇒  k_opt^econ(T₀, c_q=1) == k_opt^cost( W = 2(T₀−1) )              (identical sets AND locations)

Factor-2 bookkeeping: T2 prices the residual scan at HALF the remaining support ((s+1)/2,
uniform prior); exp563 charges the FULL remaining expected scan anchored at the measured
T̄₀. Same physics, units one halving step apart. Hence feeding the SAME number A into both
formulas without conversion puts econ EXACTLY +1 above census: continuous locations
log₂(A·ln2) vs log₂(A·ln2) − 1 — paper 219's "+~1 query" note is CONFIRMED at exactly +1.000.
Query-price scaling: k_opt^econ(c_q) = k_opt^econ(1) − log₂ c_q; T2 side k\*_V = log₂(W·ln2/(2c_q)).

## Numerical verification

`gapL8_check.py` ALL PASS (V1–V5):

- W=1024: k_pin=10; census argmin {8,9}, V\*=10.5; econ @ matched anchor T₀=W/2+1=513 → {8,9}
  (identical); naive same-anchor census {7,8} → shift EXACTLY +1.
- W=65536: k_pin=16; census {14,15}, V\*=16.5; econ @ T₀=32769 → {14,15} (identical); naive {13,14}.
- exp563 recorded values reproduce from stored rows: balanced T̄₀=1072.425 → prediction
  9.536549 (= recorded), discrete econ argmin 10 (= recorded); unbalanced T̄₀=286205.89 →
  prediction 17.597922 (= recorded), argmin 18 (= recorded). Matched-anchor census at
  W=2(T̄₀−1) gives the same UNIQUE argmins {10}/{18}: exp563's economic optimum IS the T2
  census stop on the draw-law-anchored width.
- Pin never coincides with either optimum: gap k_pin − max(argmin set) ∈ {1,2} for every
  W ≤ 4096; conflating pin with an optimum overstates the work-optimal budget by 1–2 paid
  queries (exp563 balanced: 20 vs 10).

## Verdicts — which pairs can coincide, which never

- k_opt^cost ↔ k_opt^econ: different questions, IDENTICAL answers once anchors are converted
  (W ↔ 2(T₀−1)); unconverted same-number inputs differ by exactly +1 query (econ stops later).
  The ONLY pair that ever coincides.
- k_pin ↔ k_opt^cost: NEVER coincide (gap ∈ {1,2}, all W ≤ 4096).
- k_pin ↔ k_opt^econ: NEVER coincide (inherits the census bound through the identity).
- No definition subsumes another: marginal-gain-zero / total-work-minimum /
  net-economics-maximum are three distinct functionals; only (cost, econ) are related by an
  exact algebraic map.

## Naming rule adopted

BAN the bare symbol "k\*" in future papers; every occurrence must expand to exactly one of
**k_pin** (alias k_sat), **k_opt^cost** (quoted with its support W), or
**k_opt^econ(T₀,c_q)** (always quoted with anchor and query price). Paper 212's
"k\*=⌈log₂W⌉" retro-reads as k_pin. Draft T2 already complies.

## Verification scope (disclosed)

This is a DEFINITIONAL/TAXONOMY result; no new physics was run for it. Verification =
own check script `gapL8_check.py` ALL PASS plus exact reproduction of previously-recorded
exp563/T2-census values from stored rows (numbers cross-validate against the existing
record). NO separate adversarial verifier was run — a scope judgment, disclosed here per
lab convention.

## Barrier validation

Bookkeeping hygiene serving the barrier-8 audit trail: the taxonomy makes every future
"k-stop" claim name its functional, anchor, and price so cross-paper comparisons cannot
conflate saturation with optimality. Residue cap 4/3 untouched; no complexity claim made;
no breakthrough claimed.

## Bottom line

GAP-L8 closes: the lab's three "k\*"s are now three named quantities with exact conversion
laws between them, one identity (econ ≡ census under W ↔ 2(T₀−1)), one precise constant
(+1.000 for unconverted same-number inputs), and a naming rule that makes the conflation
class impossible to reintroduce silently.
