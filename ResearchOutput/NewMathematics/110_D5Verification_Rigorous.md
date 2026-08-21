# Paper 110 — D₅-VERIFICATION: Rigorous Galois Group Confirmation

**Verdict name: THE-DIAL-IS-D₅.**
Round-32 #1 · exp 446 · assessment v221 · script `/tmp/exp_d5verify_simple.py`.

## 1. The verification

All four candidate quintics from paper 84 rigorously verified using sympy:

| polynomial | discriminant | square? | irreducible? | Gal |
|---|---|---|---|---|
| x⁵+11x−44 | 11 754 029 056 = 108 416² | ✓ | ✓ | order 10 (D₅) |
| x⁵+11x+44 | 11 754 029 056 = 108 416² | ✓ | ✓ | order 10 (D₅) |
| x⁵+20x−32 | 4 096 000 000 = 64 000² | ✓ | ✓ | order 10 (D₅) |
| x⁵+20x+32 | 4 096 000 000 = 64 000² | ✓ | ✓ | order 10 (D₅) |

Sympy's `galois_group` function returns **order 10** — exactly D₅ (dihedral of order 10). The discriminants being perfect squares confirm D₅ ⊆ A₅ (reflections act as double-transpositions, which are even).

## 2. The root-count signature

Root counts match D₅'s expected signature: {nr=0: 40%, nr=1: 50%, nr=5: 10%} — corresponding to rotations (irreducible), reflections (one linear factor), and identity (splits completely).

## 3. What closes

The degree ladder is now complete AND verified: degrees 2–6 all have measured type channels with rigorously confirmed Galois groups. The D₅ type-pair channel at the correct conductor remains open (requires identifying the quadratic subfield's conductor), but the group-theoretic verification is complete.

Now 446 experiments. Assessment v221. Paper 110, issue #202.
