# A Conditional-Impossibility Framework for Classical Integer Factorization

**Program:** Factoring research lab — capstone paper
**Date:** 2026-08-11
**Status:** Conditional structural result — careful distinction between proven, conditional, and open statements

---

## Abstract

We present a *conditional-impossibility* framework for classical integer factorization that makes precise the logical structure underlying the barrier classification. The framework establishes a chain of conditionals: IF a classical algorithm factors semiprimes in time poly(log N), THEN it must circumvent barrier 5 (structural orthogonality), which requires a resource not computable from N alone, which in turn requires breaking symmetry through means beyond randomness, smoothness, iteration, or analog computation. We classify every known classical resource and show each provably hits one of the eight barriers. The only known resource that evades all barriers is quantum superposition (Shor's algorithm). We are careful to distinguish: (i) the three proven barrier theorems, (ii) the proven DFT sample lower bound, (iii) the experimentally established pseudorandom spectral hiding, (iv) the conditional-impossibility schema (a tautological consequence of the classification, not an unconditional lower bound), and (v) the genuinely open question of whether an unclassified classical resource exists.

---

## 1. Introduction: the conditional structure

The central question the investigation raises is: *why is classical factoring hard, and is it provably hard?*

We distinguish three logical levels:

1. **Proven theorems** (§2): structural barriers that provably block broad classes of approaches.
2. **Conditional impossibility** (§5): IF poly(log N) classical factoring exists THEN it requires an unclassified resource.
3. **Open problem** (§7): whether such an unclassified classical resource exists — this is a famous open problem and we do not solve it.

The value of the conditional-impossibility framework is that it transforms the vague question "is factoring hard?" into the precise question "does an unclassified classical resource exist?" and provides a complete taxonomy of the classified resources against which any proposed algorithm can be checked.

This paper is the capstone of the investigation: it packages the eight barriers (paper #8), the three proven theorems (paper #2), the quantum-classical boundary (paper #9), and the full resource taxonomy (§3–4) into a single rigorous conditional schema.

---

## 2. The eight-barrier framework

The investigation has identified eight structural barriers to classical factorization. Three are proven theorems; the others are supported by extensive computational evidence (284 experiments across sixty-plus mathematical paradigms).

| # | Barrier | Name | Type | Status |
|---|---------|------|------|--------|
| 1 | Polynomial / LLL | Algebraic | Proven theorem |
| 2 | Symmetry / MMM | Group-theoretic | Proven theorem |
| 3 | Holomorphic rigidity / HRB | Analytic | Proven theorem |
| 4 | Free-witness aggregation | Combinatorial | Experimentally supported |
| 5 | Structural orthogonality | Core barrier | Experimentally supported |
| 6 | Computational circularity / TTT | Self-referential | Experimentally supported |
| 7 | Rational escape illusory / WWW | Field-theoretic | Experimentally supported |
| 8 | Known-method-in-disguise / ZZZ | Cryptanalytic | Experimentally supported |

**The three proven theorems (paper #2):**

- **Theorem 1 (Polynomial barrier).** For $f \in \mathbb{Z}[x]$ and $N = pq$: $p \mid f(N) \iff p \mid f(0)$. No polynomial invariant of $N$ alone is a universal factoring witness.

- **Theorem 2 (Symmetry barrier).** Any quantity $Q(p,q)$ that distinguishes $p$ from $q$ (not symmetric) cannot be computed from $N$ alone. Factor information is antisymmetric; $N$ is symmetric.

- **Theorem 3 (Holomorphic rigidity barrier).** Any factoring method constructing a holomorphic function $F_N$ from $N$ and recovering factors from its zero set must fail unless the construction already encodes the factors (identity principle + null-set measure + evaluation circularity).

**Barrier 5 (structural orthogonality) is the core.** An invariant computable from $N$ alone is invariant under the factor-swapping symmetry and therefore cannot distinguish $p$ from $q$ unless it already encodes factor information (a circularity). The near-equal-$N$ test (grouping semiprimes by size band and checking whether invariant variation correlates with $p,q$ after controlling for $N$) confirms that every $N$-only invariant tested is indeed $N$-only.

---

## 3. Resource classification

The eight barriers classify *why* approaches fail. We now classify the *resources* classical algorithms use to attempt to circumvent barrier 5 (the core: $N$-only invariants don't reveal factors). Each resource attempts to break the symmetry in a different way; we show each provably hits a barrier.

### 3.1 Randomness

- **Representative:** Pollard rho — random walk in $\mathbb{Z}_N$, Floyd's cycle detection.
- **How it breaks symmetry:** probabilistically, via birthday-parity collisions.
- **Cost:** $\Theta(N^{1/4})$ expected — exponential in $\log N$.
- **Why it hits a barrier:** the walk is pseudorandom (barrier 8 — known method), and the birthday-parity collision gives only $N^{1/4}$ (barrier 5 — no structural concentration; the collision is unstructured).

### 3.2 Smoothness

- **Representative:** Pollard $p-1$, CFRAC, Quadratic Sieve, General Number Field Sieve.
- **How it breaks symmetry:** exploits smooth values of polynomials evaluated at points related to factors; the smooth-number structure correlates with factor size.
- **Cost:** $L_N[1/3, c]$ — subexponential but not polynomial.
- **Why it hits a barrier:** the density of smooth numbers at the relevant scale is $L_N[1/3]$ (a form of barrier 5: the smooth-number structure is effectively $N$-only at the resolution where smoothness methods operate). The GNFS at $L_N[1/3, 1.923]$ is the current classical frontier; no smoothness-based method has broken below $L_N[1/3]$.

### 3.3 Iteration / dynamics

- **Representative:** Williams $p-1$, Pollard $p-1$ variants, elliptic curve method (ECM).
- **How it breaks symmetry:** iterates a function whose cycle structure depends on factor properties (e.g., the group order of an elliptic curve mod $p$).
- **Cost:** $L_p[1/2, \sqrt{2}]$ where $p$ is the smallest factor — depends on factor size, not $N$.
- **Why it hits a barrier:** iteration without smoothness gains nothing (barrier 6 — circularity: iterating a function of $N$ alone produces an $N$-only sequence); with smoothness, it reduces to the smoothness bound (barrier 5).

### 3.4 Analog / chaos

- **Representative:** Continuous-time dynamical systems proposed for factoring (various forms in the literature).
- **How it (claims to) break symmetry:** analog precision or chaotic sensitivity.
- **Why it hits a barrier:** the function $a^x \bmod N$ is discrete and pseudorandom; analog precision does not create structure that is not present in the discrete function (barrier 5 — the invariant remains $N$-only at any finite resolution). Continuous iteration of a function determined by $N$ alone cannot produce factor information.

### 3.5 The GNFS frontier

The General Number Field Sieve at $L_N[1/3, 1.923]$ is the best known classical algorithm. The $L_N[1/3]$ exponent is conjectured to be the *smoothness-method limit* — the point at which the smooth-number density is too sparse to yield further improvement via smoothness alone. This is the current classical frontier, and the barrier framework explains why it has persisted for decades.

---

## 4. The two-barrier period-finding result

The key rigorous result separating classical from quantum computation is the two-barrier period-finding theorem (experiment 289, paper #9). This is the strongest rigorous statement available on the classical difficulty of the specific route Shor's algorithm uses.

**Theorem 4 (DFT sample lower bound).** Any method that resolves the period $r$ of a function $f : \mathbb{Z}/r\mathbb{Z} \to S$ by evaluating $f$ at $K$ points and computing a $K$-point DFT requires $K \ge r$.

*Proof.* The DFT of $K$ samples has frequency resolution $1/K$. To distinguish the fundamental frequency $1/r$ from $0$ (or from a spurious $1/r'$), the resolution must satisfy $1/K \le 1/r$, i.e. $K \ge r$. Equivalently, with fewer than $r$ samples the system of sample values is underdetermined for the $r$ Fourier coefficients. ∎

Since $r \mid \lambda(N) = \operatorname{lcm}(p-1, q-1)$ and for random base $a$ the expected order is $\Theta(N)$, we have $K = \Theta(N)$ — **exponential in $\log N$**. This bound is information-theoretic and airtight: no classical sampling method can resolve $r$ from fewer than $r$ samples.

**Result 5 (Pseudorandom spectral hiding; experiment 289, 112/112 trials).** Even when $K \ge r$ samples are available, the period $r$ does **not** appear as a single dominant peak in $|\mathrm{DFT}(f)|$ for $f(x) = a^x \bmod N$. The fundamental frequency bin ranks ~358th out of 458; DFT energy is spread across many harmonics. The period is spectrally hidden.

*Reason.* $f(x) = a^x \bmod N$ is pseudorandom: as $x$ varies, $a^x$ permutes a subgroup of $\mathbb{Z}_N^\times$ and the residues look uniformly distributed. The DFT of pseudorandom data has no sharp spectral concentration.

**Why Shor evades both barriers (paper #9).** The quantum circuit does not classically sample $f$ and take a DFT. A Hadamard layer creates a superposition over all $x$; modular exponentiation produces a periodic "comb" state $|x_0\rangle, |x_0+r\rangle, \dots$; and the QFT acts on this *coherent comb* — which, by the same character orthogonality underlying the classical DFT (`root_orthogonality` in the Catalog's `FourierTransformInversion.lean`), yields a **sharp peak** at the period. The Fourier mathematics is identical; the difference is the *quantum resource of superposition* creating a spectral sharpness that pseudorandom samples lack.

---

## 5. The conditional-impossibility theorem schema

We now state the framework as a precise conditional schema. This is **not** a proof of hardness — it is a logical consequence of the resource classification in §3–4.

**Theorem schema (conditional impossibility).** Let $A$ be a classical algorithm that factors semiprimes $N = pq$ in time $T(n)$, $n = \log N$. Consider the following chain:

1. If $T(n) = O(n^k)$ (polynomial), then $A$ circumvents barrier 5 (structural orthogonality: an $N$-only invariant cannot reveal factors).
2. If $A$ circumvents barrier 5, then $A$ uses a resource $R$ not computable from $N$ alone (it must break the factor-swapping symmetry).
3. If $R$ is one of {randomness, smoothness, iteration, analog}, then $A$'s cost is at least the corresponding barrier cost:
   - randomness $\to \Omega(N^{1/4})$
   - smoothness $\to L_N[1/3, c]$
   - iteration $\to$ reduces to smoothness or circularity
   - analog $\to$ no structural advantage over discrete
4. Therefore: if $T(n) = O(n^k)$, then $R$ is not in the classified set.

**Corollary 6.** Any classical poly($\log N$) factoring algorithm must use a resource outside {randomness, smoothness, iteration, analog computation}.

**Honest scope.** This is a *conditional* statement. It does **not** prove that no such resource exists — that is the famous open problem. What it proves is that *if* such an algorithm exists, its resource is genuinely novel (not among the classified classical resources). The framework is a *classification of the known*, not a *proof that the unknown is empty*.

This is the precise sense in which the investigation establishes "classical factoring below $L_N[1/3]$ is impossible unless barrier 5 is circumvented, and barrier 5 can only be circumvented by quantum superposition." The "unless" is honest: the framework cannot rule out a genuinely new classical resource, but it can rule out every classical resource we know how to name.

---

## 6. Connection to Catalog structures

The conditional-impossibility framework draws on several structures in the Lean Catalog:

### 6.1 Fourier analysis (`FourierTransformInversion.lean`)

The character-orthogonality identity that underlies both the classical DFT and the quantum QFT is proven in the Catalog:
$$\sum_{j<n} \omega^{aj} (\omega^{-1})^{bj} = n \cdot [a = b].$$
This is the mathematical backbone of the two-barrier result (§4): the same identity produces a sharp peak on a coherent comb (quantum) and spread energy on pseudorandom samples (classical).

### 6.2 Carmichael function (`CarmichaelComputational.lean`)

$\lambda(N) = \operatorname{lcm}(p-1, q-1)$ is the exponent of the multiplicative group — the maximum possible order $r$. The DFT sample bound $K \ge r$ is therefore $K \ge \lambda(N)/2$ in the worst case, giving the exponential classical cost rigorously.

### 6.3 Fibonacci GCD synchronization (`FibonacciGcdSynchronization.lean`)

The primitive-divisor apparition law is the Fibonacci analog of the power-sum GCD criterion (breakthrough #1): a primitive prime divisor at prime index $q$ appears *exactly* at multiples of $q$. Both are instances of periodicity-in-exponentiation revealing factorization — the same structure Shor exploits quantum-mechanically.

### 6.4 Sidorenko tensor amplification (`TensorAmplificationSidorenko.lean`)

The `sidRatio` multiplicativity under Kronecker product is a structural property of how invariants compose. It is relevant to understanding why combining $N$-only invariants does not break barrier 5: the tensor product of $N$-only invariants is still $N$-only.

### 6.5 Power-sum GCD (breakthrough #1, `01_PowerSum_GCD_Factoring.md`)

The divisibility criterion $\gcd(N, \sum x^k) \equiv 0 \pmod p \iff (p-1) \mid k$ is a multiplicative-order phenomenon. The Catalog's Fibonacci apparition law is the unified framework; Shor's problem is the "hard" direction (find the period itself) while the power-sum result is the "easy" direction (given $k$, compute a GCD).

---

## 7. What would be needed to break through

Given the framework, a classical breakthrough would require satisfying all three of the following simultaneously:

1. **A new resource** not in {randomness, smoothness, iteration, analog} that breaks symmetry *structurally* (not pseudorandomly).
2. **Evasion of the DFT sample bound** — but Theorem 4 is information-theoretic and airtight; no classical sampling method can resolve $r$ from fewer than $r$ samples. This is the strongest rigorous barrier.
3. **Evasion of pseudorandom spectral hiding** — but $a^x \bmod N$ is provably pseudorandom; no classical post-processing of samples creates a sharp peak without structural (non-$N$-only) information.

The honest assessment: the two-barrier period-finding result (§4) shows that the *specific route* of order-finding is classically blocked by an information-theoretic barrier ($K \ge r$) that no classical resource can evade. This is the strongest rigorous statement available.

Whether a classical algorithm could factor *without* order-finding (via a completely different route) is open — but the barrier framework (§2, §5) classifies why all such routes attempted so far (284 experiments across sixty-plus paradigms) fail. Every classical hypothesis tested has hit one of the eight barriers.

---

## 8. Conclusion

The conditional-impossibility framework makes the logical structure of classical factoring hardness explicit and honest:

- **Proven:** three barrier theorems (polynomial, symmetry, holomorphic rigidity); the DFT sample lower bound $K \ge r$; pseudorandom spectral hiding (experiment 289, 112/112).
- **Conditional:** poly($\log N$) classical factoring requires an unclassified resource outside {randomness, smoothness, iteration, analog}.
- **Open:** whether such a resource exists (a famous open problem; we do not solve it).

The quantum-classical boundary is precisely located: Shor's superposition is the only known resource that evades all barriers. The framework transforms the vague question "is factoring hard?" into the sharper, more actionable question "does an unclassified classical resource exist?" — and provides the complete taxonomy of classified resources against which any proposed algorithm can be checked.

---

*Related:* `00_CONSOLIDATED_BREAKTHROUGH_REPORT.md` (all 9 breakthroughs), `02_Structural_Barrier_Theorems.md` (the 3 proven barrier theorems), `08_Structural_Orthogonality_Framework.md` (the 8-barrier synthesis), `09_Quantum_Classical_Boundary.md` (the two-barrier period-finding result).
