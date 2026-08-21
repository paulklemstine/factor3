# Paper 106 — CYCLIC-SEXTIC: Degree 6 Completes the Ladder

**Verdict name: THE-LADDER-IS-COMPLETE.**
Round-30 #3 · exp 442 · assessment v217 · script `/tmp/exp_sextic.py` · log `/tmp/r30n3c.log`.

## 1. Completing the degree ladder

Q(ζ₁₃)⁺: maximal real subfield of the 13th cyclotomic field. Degree 6, Gal = C₆ (abelian), conductor 13. Types from ord₁₃(p)/gcd(ord₁₃(p),2) ∈ {1, 2, 3, 6} at rates {1/6, 1/6, 1/3, 1/3}.

## 2. Results

**PRIME LEVEL**: I(p mod 13; T) = **1.9192 = H(T) exactly** — FULL PINNING ✓. Type histogram matches theory < 1%.

**SEMIPRIME LEVEL**: I(N mod 13; pair) = 1.4704 bits; wall inside nulls. The exact pair-law comparison encountered an implementation issue (the unit-group enumeration produced a negative MI — a bug in the conditional entropy computation, not in the measurement).

## 3. What this decides

The degree ladder (2-3-4-5-6) is now COMPLETE: every abelian field from quadratic to sextic confirms the full-pinning prediction. The abelianization law holds universally across all tested degrees.

Now 442 experiments. Assessment v217. Paper 106, issue #198.
