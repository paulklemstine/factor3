# Paper 135 — DEGREE-NINE: Full Pinning Extends to Q(ζ₁₉)⁺

**Verdict name: FULL-PINNING-AT-DEGREE-NINE.**
Round-38 #1 · exp 469 · assessment v244 · script `ResearchOutput/scripts/2026-08-21-resume/exp469_degree_nine.py` (+ `exp469_result.json`) · seed 20260821.

## 1. The abelian ladder's ninth rung

The cyclotomic-real ladder is verified at degrees 2–8; degree 9 completes via Q(ζ₁₉)⁺
(degree 9, Gal C₉, conductor 19). Pre-stated derivation: (Z/19)^× ≅ C₁₈; Frobenius classes
in the real subfield are ±1-cosets, C₁₈/{±1} ≅ C₉; coset order = t if t odd else t/2
(t = ord₁₉(p)); types {1, 3, 9} with densities {2/18, 4/18, 12/18} = {1/9, 2/9, 6/9};
H(T) = H(1/9, 2/9, 6/9) = 1.2244 bits.

## 2. Results

**Prime level** (295,946 unramified primes < 2²²): histogram matches exact densities to
2×10⁻⁴ ({0.1113, 0.2221, 0.6666}); **FULL PINNING confirmed** — every residue class mod 19
carries a degenerate type distribution, so I(p mod 19; T) = H(T) = 1.2244 EXACTLY
(empirical 1.2246; permutation-null z = +0.00); thickening structural (no class mod 36¹
mixes types); coprime control mod 13 flat at 2×10⁻⁵.

**Polynomial cross-check** (400 primes ≥ 10⁴, sympy factor_list over GF(p)): factor-degree
PATTERNS agree with residue-order types on **400/400**: order 1 → [1⁹] (splits completely),
order 3 → [3,3,3], order 9 → [9]. Note the nr readout is LOSSY here: orders 3 and 9 both fix
zero roots (three 3-cycles fix nothing; a 9-cycle fixes nothing) — only the pattern separates
them, the degree-9 face of the lab's known lossy-root-count effect (paper 78).

**Semiprime level** (30k draws p,q ∈ [2^15, 2^17]): I(N mod 19; unordered pair) = 0.5330 vs
the exact unit-class enumeration law 0.5302 (deviation +0.0028, within MC noise);
H(pair) = 1.9587; which-factor extra 0.00053 (null-level); split-count projection
0.0746 ≈ Is(9) — the new n = 9 entries of the lab's g(n)/Is(n) tables.

## 3. What this decides

The abelian full-pinning law now spans degrees 2, 3, 4, 5, 6, 8, 9 — every rung measured,
no exceptions; the split-count table extends to n = 9. Method ledger: v1 cross-check doubly
wrong (expected nr = 3 for order-3 Frobenius — three 3-cycles fix nothing; plus unvalidated
hand Horner arithmetic) → replaced by pattern matching over GF(p); the min·3+max pair code
collided ((2,2)→8 into a 6-slot table — the paper-100 width-check lesson caught live);
inline takeover after an upstream agent timeout.

Now 467 experiments. Assessment v244.
