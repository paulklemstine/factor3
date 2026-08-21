# Paper 113 — ÉTALE-DIAL: The Type Channel for Reducible Polynomials

**Verdict name: THE-COMPOSITE-CAPTURES-THE-UNION.**
Round-32 #2 · exp 448 · assessment v224 · script `/tmp/exp_etaledial.py` · log `/tmp/r32n2.log` · runtime 7 s.

## 1. Extending to étale algebras

All prior type-channel measurements used irreducible polynomials (fields). This round tests a reducible polynomial f(x) = (x³−2)(x²−3), corresponding to the étale algebra ℚ(∛2) × ℚ(√3). The splitting pattern of f mod p jointly encodes both components' splitting behaviors.

## 2. Results

At m = 3:
- x³−2 alone: I = **1.0000** (sign character at conductor 3)
- x²−3 alone: I = **0.0000** (its conductor is 12, not 3)
- Composite: I = **1.0000** (= the informative component)
- Sub-additivity: composite ≤ sum ✓

Semiprime level: composite pair = 1.0000; wall z = +0.91 ✓.

The composite dial correctly captures the union: it equals the informative component, while the uninformative one adds zero. This confirms that the type-channel framework extends to reducible polynomials (étale algebras) with the expected additivity properties.

Now 448 experiments. Assessment v224. Paper 113, issue #205.
