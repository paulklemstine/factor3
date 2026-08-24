# Paper 205 — MODULAR-DYNAMICS: The Projected Tree Is Collision-Free, Class-Confinned, and Trial-Division-Slow

**Verdict name: TRIAL-DIVISION-EQUIVALENT-GUIDANCE-NULL (α=1.007±0.088; no sub-linear regime).**
Round-72 #5 · exp 555 · assessment v312 · script `exp555_modular_dynamics.py` (+ JSON/addendum/logs) · seed 20260826 · matrix gate PASS ((3,4,5)→{5,12,13 / 21,20,29 / 15,8,17}).

## 1. Structure (200 Ns × 200k discoveries)

Expansion is FREE of multiplications (T-coefficients ±1,±2,±3). The mod-N Berggren
tree is **collision-free at scale** (distinct = 3·expanded+1 identically on every N;
no first collision within 200k nodes), out-degree 3, in-degree 1, no component
exhaustion — and **residue-class-confined**: ~99.75% of orbit nodes sit in the two
top classes of the nonzero-coordinate histogram mod 3/5/7 (primitive-triple
congruences survive the projection). Uniform BFS reaches only a crust (median depth
11); hits sit just past it.

## 2. Economics

Order-free dive factors 200/200 within budget: **v\*(N) median 7,013 nodes,
α = 1.007 ± 0.088, intercept −0.05 ⟹ v\* ≈ 0.89·p_min** — TRIAL-DIVISION
scaling, decisively not ρ-like (0.458–0.52); nothing sub-linear seen. Matched
compute (node = 12 mult-units): ~11× worse constants than plain trial division at
the median; no winning bitlen in bits 23–32; Pollard ρ (50% by U≈150–225 units)
dominates by orders of magnitude. Ambient null: random Pythagorean points hit at
4.8e-4 vs orbit density ≈1e-4 — **the orbit UNDER-SAMPLES factor-revealing residues
~5×**: projection erases exactly the order structure that made integer-face search
tractable.

## 3. Guidance null — after the shape-artifact catch

Naive residue-priority "improvements" show z=12–24, but random-order control alone
lifts hit-rate 0.22→0.99 @25k (z=21.8): pure traversal-shape artifact. Honest paired
comparison vs the shape control: all |z|<2 at 25k/50k/100k budgets ⟹
**NO-IMPROVEMENT-BEYOND-NOISE**, confirming the pre-stated seal expectation.
(Yield concentrates in word-depth band ~8–14 and is exactly zero on long DFS tails.)

Ledger: gcd(c−b)/gcd(c+b) identity needed the OR-predicate (rechecked on 400k nodes:
0 violations; 54/54 hits divide exactly one of c±b, matching m≡±n mod p); crossover
fields recomputed honestly; ρ simulator rewritten Brent before production.

## 4. Campaign close

With papers 201–204, every face of the user's triplet-tree proposal is measured:
exact-target circular (sealed), modular descent TD-class (this paper), combining
invalid-as-stated (202), multi-target = TD-in-tree-clothing (203), Euler route
5.7× Fermat (201). Barriers 2/5/8 unchanged throughout.

Now 550 experiments (max id). Assessment v312.
