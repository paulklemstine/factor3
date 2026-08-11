# Experiment SS — Dyadic Solenoid & Factoring

> **Paradigm:** Dynamical systems / strange attractors / dyadic solenoid / Čech cohomology
> **Date:** 2026-08-10
> **Verdict:** **REFUTED** — all six hypotheses. A new, clean instance of the
> circularity / free-witness aggregation barrier, expressed via inverse-limit topology.

---

## 1. Mathematical background

The **dyadic solenoid** Σ₂ is the inverse limit of the doubling map of the circle

```
... —×2→  S¹  —×2→  S¹  —×2→  S¹ .
```

It is the simplest genuinely "strange" attractor that is an inverse limit of
1-dimensional pieces (it appears as the Smale solenoid and as a cross-section of
Lorenz-type flows). Its first Čech cohomology is the *direct limit* of the
cohomologies of the circles under the maps induced by doubling:

```
H¹(Σ₂) ≅ colim( ℤ —×2→ ℤ —×2→ ... )  ≅  ℤ[1/2],
```

the additive group of **dyadic rationals** (formalized in
`DyadicSolenoid.lean`). This group is the certificate of chaos: it is **not**
finitely generated, so Σ₂ is not homotopy equivalent to any finite directed
graph. The inverse-limit machinery is formalized in `InverseLimit.lean`.

**The factoring connection.** Shor's algorithm factors N = pq by finding the
multiplicative order r = ord_N(2) (the period of 2^k mod N) via the quantum
Fourier transform, then computing gcd(2^{r/2} − 1, N). The doubling map on the
solenoid is the *topological* avatar of "multiplication by 2". The question is
whether the solenoid's topological/cohomological structure admits a **classical**
read-out of ord_N(2).

**Key structural fact.** The solenoid is interesting *because* the doubling map
is a **non-invertible degree-2 covering**. Its cohomology ℤ[1/2] captures
2-divisibility (the colimit of ×2 on ℤ). This non-invertibility is the *sine qua
non* of everything interesting about Σ₂.

---

## 2. The six hypotheses and their refutations

### S1 — The "mod-N solenoid" (inverse limit of (ℤ/Nℤ, ×2))

**Construction.** Inverse system with obj_n = ℤ/Nℤ and bonding map
bond_n(x) = 2x mod N. The inverse limit is the set of threads
(x₀, x₁, ...) with 2·x_{n+1} ≡ x_n (mod N).

**Prediction.** For odd N, 2 is invertible mod N, so each bond_n is a
**bijection**. Hence each x₀ determines a unique thread; #threads = N for every
depth.

**Result.** Confirmed exactly: #threads(depth 3) = N for N = 15, 21, 35, 65,
91, 493. gcd(N, N) = N — trivial.

**Verdict.** The mod-N solenoid collapses to a single copy of ℤ/Nℤ. The
non-invertible degree-2 structure that makes Σ₂ interesting is **invisible** mod
N. **REFUTED.**

---

### S2 — Squaring-map inverse system on 2^n-torsion

**Construction.** Finite approximation of the solenoid: the 2^n-th roots of
unity. Mod N this is X_n = {x ∈ (ℤ/Nℤ)* : x^{2^n} ≡ 1 mod N}, with bonding map
x ↦ x² (squaring maps 2^{n+1}-torsion onto 2^n-torsion). Threads = compatible
systems of 2^n-th roots.

**Result.** |X_n| = 2^{min(n,v₂(p−1)) + min(n,v₂(q−1))}. The thread count is
4^k for k ≥ 1, determined entirely by the **2-adic valuations** v₂(p−1),
v₂(q−1). Example: N = 493 = 17·29 gives |X_n| = [1, 4, 16, 32, 64], #threads =
64, gcd(64, 493) = 1.

**Verdict.** The invariant reveals v₂(p−1) and v₂(q−1) — the highest power of 2
dividing p−1, q−1. This is **not** ord_p(2) (the full multiplicative order). For
p = 7: v₂(6) = 1 but ord_7(2) = 3. The 2-adic valuation is insufficient to
recover p or q, and being a power of 2 it is coprime to odd N. **REFUTED** (wrong
invariant: 2-adic valuation ≠ multiplicative order).

---

### S3 — Čech cohomology H¹(Σ₂; ℤ/Nℤ)

**Computation.** H¹(Σ₂; ℤ/Nℤ) = colim(ℤ/Nℤ —×2→ ℤ/Nℤ —×2→ ...). Since 2 is
invertible mod N (N odd), ×2 is an **automorphism** of ℤ/Nℤ. The direct limit of
a constant system of isomorphisms is the group itself.

**Result.** H¹(Σ₂; ℤ/Nℤ) ≅ ℤ/Nℤ, of size N. gcd(N, N) = N — trivial.

**Verdict.** The colimit collapses. The 2-divisibility that makes ℤ[1/2]
interesting is invisible in ℤ/Nℤ-cohomology. **REFUTED** (trivial cohomology).

---

### S4 — Smallest universal period (the honest version)

**Construction.** The r-periodic points of ×2 on ℤ/NZ are {x : (2^r − 1)x ≡ 0
mod N}. The smallest r for which **all** of ℤ/Nℤ is r-periodic requires N | 2^r
− 1, i.e. ord_N(2) | r. The smallest such r is ord_N(2) itself.

**Result.** Confirmed exactly: the smallest universal r equals ord_N(2) for all
test semiprimes (N = 15 → 4, 21 → 6, 35 → 12, 9797 → 1200). And
gcd(2^{r/2} − 1, N) does yield a factor (e.g. N = 9797 → 101).

**Verdict.** This is **not a new method** — it is the classical period-finding
problem wearing a topological costume. Finding the smallest universal r *is*
computing ord_N(2), which classically needs O(N) samples (Exp. C confirmed). The
factor revelation is real but costs exponential time. **REFUTED** (reduces to
classical period-finding).

---

### S5 — Poly(log N) samples of the ×2 orbit

**Test.** Evaluate 2^k mod N for k = 1..K with K = O(log N), compute
gcd(2^k − 1, N).

**Result.** For N = 9797 (K = 56), all gcds are 1; ord_N(2) = 1200, so the
first signal needs ~1200 samples. **Honest nuance:** for N = 11413 = 101·113, a
nontrivial gcd (113) appears at k = 28 = ord₁₁₃(2). This is the **Pollard p−1 /
exponential-GCD phenomenon** (Exp. KKK): a factor is revealed when k is a
multiple of ord_p(2). But k = 28 ~ √N, still exponential in log N, and in the
worst case ord_p(2) ~ p ~ √N. This is the known barrier, not an escape.

**Verdict.** No structure is visible in poly(log N) samples in the worst case.
The signal is "spread out" over Θ(N) residues — the free-witness aggregation
barrier. **REFUTED.**

---

### S6 — GCD heuristics on thread counts / orbit data

**Test.** Combine thread counts from all finite approximations (|X_n|, 2^n − 1,
products), take gcd with N.

**Result.** Every natural invariant yields gcd = 1 or N. The |X_n| values are
powers of 2 (coprime to odd N); 2^n − 1 values give nontrivial gcd only when
ord_N(2) | n, i.e. at n = Θ(N).

**Verdict.** All gcds trivial in the poly(log N) range. **REFUTED.**

---

## 3. Meta-analysis: the structural obstruction

The dyadic solenoid Σ₂ is interesting **because** the doubling map is a
non-invertible degree-2 covering. Its cohomology H¹ = ℤ[1/2] captures
2-divisibility (the colimit of ×2 on ℤ).

For factoring N = pq (odd semiprime), the "mod-N" reduction faces an
insurmountable obstruction:

> **THE INVERTIBILITY COLLAPSE.** Multiplication by 2 is **invertible** on
> ℤ/Nℤ (since gcd(2, N) = 1). Therefore:
>   - (a) The mod-N solenoid (ℤ/Nℤ, ×2) has bijective bonding maps. Its inverse
>     limit is a single copy of ℤ/Nℤ — trivial.
>   - (b) H¹(Σ₂; ℤ/Nℤ) = colim(ℤ/Nℤ —×2→ ...) = ℤ/Nℤ — trivial.
>   - (c) The N-torsion of Σ₂ is Ẑ{N} ≅ ℤ/Nℤ — a cyclic group of order N.
>     The r-periodic points (r = ord_N(2)) are ALL of ℤ/Nℤ, detecting r only by
>     the **definition** of ord_N(2) — circular.

The solenoid's 2-adic richness lives over ℤ₂ (the 2-adic integers), where ×2 is
genuinely non-invertible. But reducing mod N (N odd) forces invertibility. The
two structures are **incompatible**:

| Solenoid needs | Factoring needs |
|----------------|-----------------|
| 2 non-invertible (2-adic world) | 2 invertible mod N (mod-N world) |
| H¹ = ℤ[1/2] (2-divisible) | H¹(Σ₂; ℤ/Nℤ) = ℤ/Nℤ (collapses) |
| Non-invertible degree-2 covering | ×2 is a permutation of ℤ/Nℤ |

The only surviving ×2-dynamical invariant mod N is the cycle structure of the
permutation x ↦ 2x on ℤ/Nℤ, whose period at the identity is ord_N(2). Reading
this period classically requires O(N) steps — exactly the free-witness
aggregation / circularity barrier (Exp. C, T, X).

This is the **circularity bottleneck** expressed in the language of dynamical
systems: the solenoid provides a beautiful topological setting for ×2 dynamics,
but the period ord_N(2) it encodes is precisely the quantity whose classical
computation is equivalent to factoring.

---

## 4. Relation to prior experiments and barrier theorems

- **Exp. C (classical spectral period-finding):** needs M ~ ord_N(2) = O(N)
  samples. S4 is the same barrier in solenoid language.
- **Exp. KKK (exponential GCD):** gcd(a^N − a, N) = Pollard p−1. The S5 nuance
  (nontrivial gcd at k = ord_p(2)) is this phenomenon.
- **Exp. RRR (Hopf/linking):** no genuine signal. The Hopf file
  (`HopfEntanglement_Theorems.lean`) is a broken redirect — the Hopf
  fibration structure does not survive mod-N reduction either.
- **Exp. YY/ZZ (Berggren tree):** structural orthogonality — the tree's natural
  coordinate (slope) is orthogonal to factoring (norm). The solenoid's natural
  coordinate (2-adic valuation) is orthogonal to the needed quantity
  (multiplicative order). **Same pattern, different costume.**
- **LLL (polynomial barrier):** polynomial invariants reveal ≤ finitely many
  primes. The solenoid invariants here are "polynomial in 2^k" — they collapse.
- **MMM (symmetry barrier):** factor-revealing asymmetry is uncomputable from N.
  The solenoid's 2-adic structure is symmetric in p, q (depends on both via
  lcm), and reading the asymmetry needs the period.

---

## 5. Honest conclusion

> **The dyadic solenoid does NOT yield a classical factoring method.**

The obstruction is clean and structural:

1. **Mod-N solenoid collapses** — ×2 invertible mod odd N.
2. **Cohomology mod N is trivial** — H¹ = ℤ/Nℤ.
3. **The only surviving invariant** (period of ×2 on ℤ/Nℤ) **is** ord_N(2),
   whose classical computation needs O(N) time — the known exponential barrier.
4. **No poly(log N) read-out exists** — the signal is spread over Θ(N) residues.

This is a **new instance** of the circularity / free-witness aggregation
barrier, expressed via dynamical systems, inverse limits, and Čech cohomology.
It does **not** escape the classification established by experiments A–VVV.
The solenoid's genuine 2-adic structure (H¹ = ℤ[1/2], non-invertible ×2) is
**orthogonal** to the mod-N world (invertible ×2) — a structural orthogonality
analogous to the Berggren-tree result (Exp. YY/ZZ).

**Net assessment:** The solenoid is a beautiful object that *explains why* the
barrier exists (the incompatibility of 2-adic non-invertibility with mod-N
invertibility), but it does not *overcome* the barrier. It is publishable as a
negative-result bridge between dynamical systems and factoring — a clean
topological portrait of the circularity bottleneck.
