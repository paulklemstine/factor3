# Paper 141 — DEGREE-TEN: Full Pinning at the Full Cyclotomic Q(ζ₁₁)

**Verdict name: FULL-PINNING-AT-DEGREE-TEN.**
Round-39 #3 (cron iteration) · exp 473 · assessment v250 · script `ResearchOutput/scripts/2026-08-21-resume/exp473_degree_ten.py` (+ `exp473_result.json`) · seed 20260823.

## 1. The ladder's tenth rung

The abelian cyclotomic ladder stands at degrees 2–6, 8, 9; degree 10 completes via the FULL
cyclotomic field Q(ζ₁₁) — degree 10, Gal C₁₀ ≅ (Z/11)^×, conductor 11 (not a real subfield:
the full class group acts on all ten roots). Pre-stated: T(p) = ord₁₁(p) ∈ {1,2,5,10},
densities {1/10, 1/10, 4/10, 4/10} (class sizes 1,1,4,4), H(T) = H(0.1,0.1,0.4,0.4) =
1.7219 bits; pair-law anchor I_pair(n=10) = 1.2027 from paper 78's exact enumeration.

## 2. Results

**Prime level** (295,946 unramified primes < 2²²): histogram matches densities exactly;
**FULL PINNING** — every class mod 11 degenerate, I(p mod 11; T) = H(T) = 1.7219 EXACTLY
(empirical 1.7221); thickening structural; coprime control flat.

**Polynomial cross-check** (400 primes > 10⁴, sympy factor_list over GF(p)): factor-degree
patterns agree **400/400** with the cycle-structure derivation — an order-t element of C₁₀
acts as 10/t cycles of length t: order 1 → [1¹⁰], order 2 → [2⁵], order 5 → [5,5],
order 10 → [10]. Lossy-nr note: only order 1 fixes roots; patterns separate the rest.

**Semiprime level** (30k draws): I(N mod 11; unordered type-pair) = 1.2002 vs the fresh
class-enumeration law on empirical marginals 1.1999 (dev +0.0003) vs the paper-78
closed-form anchor 1.2027 (dev −0.0025, within the empirical-marginal offset);
which-factor wall 0.0005 (null); split-count projection 0.0586 — the new n = 10 entries
of the g(n)/Is(n) tables.

## 3. What this decides

The abelian full-pinning law now spans degrees 2, 3, 4, 5, 6, 8, 9, 10 — every rung
measured, no exceptions, across real-subfield AND full-cyclotomic constructions.

Method ledger: v1's pattern comparison double-wrapped its expect tuple (`pats != (expect,)`)
— 400/400 false mismatches while PATTERN itself was perfect; residue-vs-type dict lookup in
the pair enumeration; inline takeover after the agent channel's sixth death of the day (the
dying agent recovered the paper-78 anchor first — credited).

Now 473 experiments. Assessment v250.
