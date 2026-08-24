# GAP-L8 CLOSED — k-TAXONOMY: k_pin vs k_opt^cost vs k_opt^econ

Closes draft items L8 + O5 ("pin exp563's k* definition ... paper must name which").
Finite check: `gapL8_check.py` (runs <2 s) → ALL PASS. Sources: barrier4_positional_converse_draft.md
T2(c)/(d), exp563_seqhint_compounding.py (H3 block: `A=Tbar-1; et=A/2^k+1+k`), exp563_result.json.

## (a) Formal definitions — three distinct questions

1. **k_pin := min{k : W/2^k <= 1} = ceil(log2 W)** (asymptotically log2 W) — GAIN-SATURATION point.
   Generating question: *after how many adaptive queries do FURTHER queries add zero speedup?*
   Marginal gain hits EXACTLY zero: support fully pinned, zero bits remain; s(k>=k_pin)=T0/E[T_pin]
   flat. exp563 witness: 100% of N pinned at k=20=ceil(log2 W) (bitlen-40 => W=isqrt(N)-1 in
   [2^19.5,2^20)); s(>=20)=T0 exactly. Paper 212's "k* = ceil(log2 W)" is THIS object, not an optimum.

2. **k_opt^cost := argmin_{k>=0} V(k,W)**, V(k,W)=k+(W/2^k+1)/2 — COST-OPTIMAL stop (T2 census).
   Generating question: *at what k is TOTAL work (paid queries + expected residual top-down scan,
   uniform prior on support W) minimized?* VERIFIED (recheck + gapL8_check): dyadic W => tie set
   {log2W-2, log2W-1} with V*=log2W+1/2 EXACT (2..4096); relaxed continuous location
   log2(W ln2)-1 = log2W-1.5288; sits 1-2 queries BELOW k_pin (gap in {1,2} for every W<=4096).

3. **k_opt^econ(T0,c_q) := argmax_k T0/[1+c_q*k+(T0-1)/2^k]** — NET-ECONOMICS optimum (exp563 H3).
   Generating question: *at what k is net speedup maximized once every query is PAID c_q against the
   MEASURED stratum baseline T0?* Residual charged at full remaining expected scan (draw-law anchor),
   not half-support. Continuous argmin of 1+c_q*k+(T0-1)/2^k: 2^k=(T0-1)*ln2/c_q =>
   **k_opt^econ = log2((T0-1)*ln2/c_q)**; c_q=1 in exp563. Measured 10 (balanced, pred 9.536549) and
   18 (unbalanced, pred 17.597922) — nearest-integer agreement in both strata.

## (b) Conversion formulas between conventions (exact, numerically verified)

The two objectives are ONE function after a single anchor substitution (additive constants never
move an argmin):

    E(k; T0, c_q=1) = 1 + k + (T0-1)/2^k  ==  V(k; W=2*(T0-1)) + 1/2   (pointwise identity)

    =>  k_opt^econ(T0, c_q=1) == k_opt^census( W = 2*(T0-1) )        (identical sets AND locations)

Factor-2 bookkeeping: T2 prices the residual scan at HALF the remaining support ((s+1)/2, uniform
prior); exp563 charges the FULL remaining expected scan anchored at the measured Tbar_0. Same
physics, units one halving step apart. Hence feeding the SAME number A into both formulas without
conversion puts econ EXACTLY +1 above census: continuous locations log2(A ln2) vs log2(A ln2)-1.
Query-price scaling: k_opt^econ(c_q) = k_opt^econ(1) - log2(c_q); T2 side k*_V = log2(W ln2/(2 c_q)).

Numeric verification (`gapL8_check.py`, ALL PASS):
- W=1024:  k_pin=10; census argmin {8,9}, V*=10.5; econ @ matched anchor T0=W/2+1=513 -> {8,9}
  (identical); naive same-anchor census {7,8} -> shift EXACTLY +1.
- W=65536: k_pin=16; census {14,15}, V*=16.5; econ @ T0=32769 -> {14,15} (identical); naive {13,14}.
- exp563 recorded values reproduce from stored rows: balanced Tbar_0=1072.425 -> pred 9.536549
  (=recorded), discrete econ argmin 10 (=recorded); unbalanced Tbar_0=286205.89 -> pred 17.597922
  (=recorded), argmin 18 (=recorded). Matched-anchor census at W=2*(Tbar_0-1) gives the same UNIQUE
  argmins {10}/{18}: exp563's economic optimum IS the T2 census stop on the draw-law-anchored width.
- Task's "+~1 query" claim CONFIRMED exactly (+1.000): under exp563's own convention (its anchor
  number A=T0-1 read as a T2 support width), k_opt^econ(A) - k_opt^cost(A) = +1, both continuous and
  on discrete argmin sets. (Balanced-stratum physical gap vs the naive W=isqrt(N)-1 census is larger,
  ~8-9 queries, because the draw-law anchor Tbar_0 << W/4 — concentration, not convention.)

## (c) Naming recommendation for future papers

BAN the bare symbol "k*"; every occurrence must expand to exactly one of:
- **k_pin** (alias k_sat) — saturation/pinning point log2 W; NEVER described as optimal;
- **k_opt^cost** — T2 census total-cost-minimizing stop, quoted with its support W;
- **k_opt^econ(T0, c_q)** — net-economics stop, ALWAYS quoted with anchor and query price.
Paper 212's "k*=ceil(log2 W)" is retroactively read as k_pin. Draft T2 already complies.

## (d) Verdicts — which pairs can coincide, which never

- k_opt^cost <-> k_opt^econ: different questions, IDENTICAL answers once anchors are converted
  (W <-> 2(T0-1)); unconverted same-number inputs differ by exactly +1 query (econ stops later).
  This is the ONLY pair that ever coincides.
- k_pin <-> k_opt^cost: NEVER coincide — census stops 1-2 queries short of full pinning (gap in
  {1,2}, all W<=4096); conflating them overstates the work-optimal budget.
- k_pin <-> k_opt^econ: NEVER coincide (inherits the census bound through the identity); stopping at
  k_pin wastes paid queries — exp563 balanced: 20 vs 10.
- No definition subsumes another: marginal-gain-zero / total-work-minimum / net-economics-maximum
  are three distinct functionals; only (cost, econ) are related by an exact algebraic map.
