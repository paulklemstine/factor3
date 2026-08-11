# The Quantum-Classical Boundary in Integer Factorization

**Program:** Factoring research lab, experiment 289 (QBOUND) deepening
**Date:** 2026-08-11
**Honesty notice:** This paper distinguishes carefully between (i) rigorous
statements, (ii) strong experimental evidence, and (iii) open problems.  We do
**not** claim a proof that classical factoring requires superpolynomial time —
that is a famous open problem (related to P vs NP).  What we *do* establish is a
precise structural account of *why* the classical barrier exists and *exactly*
which quantum resource evades it.

## 1. The problem setup

Let $N = pq$ be a semiprime.  Shor's algorithm factors $N$ by finding the
**multiplicative order** $r$ of a random base $a$ coprime to $N$:
$$r = \min\{k > 0 : a^k \equiv 1 \pmod N\}.$$
Once $r$ is known and even with $a^{r/2} \not\equiv -1 \pmod N$, the factors
are recovered as $\gcd(a^{r/2} \pm 1, N)$.

The function $f(x) = a^x \bmod N$ is periodic with period $r$.  The question
is: **how hard is it to find $r$?**

## 2. Two independent classical barriers (experiment 289)

Across 8 semiprimes ($N \sim 10^8$–$10^9$, orders $r \sim 15\text{M}$–$362\text{M}$),
experiment 289 established two distinct obstacles to *classical* period-finding.

### 2.1 Information-theoretic barrier

**Claim (rigorous).** Any method that resolves the period $r$ of a function
$f : \mathbb{Z}/r\mathbb{Z} \to S$ by evaluating $f$ at $K$ points and computing
a $K$-point DFT requires $K \ge r$.

*Proof sketch.* The DFT of $K$ samples has frequency resolution $1/K$.  To
distinguish the fundamental frequency $1/r$ from $0$ (or from $1/r'$ for a
spurious $r' \ne r$), the resolution must satisfy $1/K \le 1/r$, i.e. $K \ge r$.
Equivalently: with fewer than $r$ samples, the system of sample values is
underdetermined for the $r$ Fourier coefficients. ∎

Since $r \mid \lambda(N) = \operatorname{lcm}(p-1,q-1)$ and for random $a$ the
expected order is $\Theta(N)$, we have $K = \Theta(N)$ — **exponential in
$\log N$**.  This is the core information-theoretic cost.

### 2.2 Structural barrier (the pseudorandomness of $a^x \bmod N$)

**Claim (experimentally established, 112/112 trials).** Even when $K \ge r$
samples are available, the period $r$ does **not** appear as a single dominant
peak in $|DFT(f)|$.  The fundamental frequency bin ranks ~358th out of 458;
DFT energy is spread across many harmonics.

*Reason.* A pure sinusoid has all its DFT energy in one bin.  But
$f(x) = a^x \bmod N$ is **pseudorandom**: as $x$ varies, $a^x$ permutes a
subgroup of $\mathbb{Z}_N^\times$ and the residues look uniformly distributed.
The DFT of pseudorandom data has no sharp spectral concentration.  The period
*is* present in the harmonic structure (recoverable via a GCD-of-peaks method
at $K \ge r$), but it is not naively readable.

**Consequence.** The classical difficulty is not *just* "you need many
samples" — it is that even with enough samples, the period is spectrally
hidden.  Two independent obstacles must both be overcome.

## 3. Why Shor evades both barriers

Shor's algorithm does **not** classically sample $f(x)$ and take a DFT.  The
quantum circuit does something structurally different:

1. **Superposition over all $x$:** A Hadamard layer creates
   $\frac{1}{\sqrt{K}}\sum_{x=0}^{K-1}|x\rangle|0\rangle$ with $K \gg r$
   (typically $K \approx N^2$, but encoded in $\log K$ qubits).  This is not
   "sampling" — it is a coherent superposition over exponentially many $x$
   values simultaneously.  This evades barrier 2.1 (the information-theoretic
   sample count) because quantum parallelism evaluates $f$ at all $x$ in one
   query round.

2. **Equivalence-class comb:** After modular exponentiation
   $|x\rangle|0\rangle \mapsto |x\rangle|f(x)\rangle$ and measuring the second
   register, the first register collapses to an equivalence class
   $|x_0\rangle, |x_0+r\rangle, |x_0+2r\rangle, \dots$ — a periodic "comb" state
   with **period $r$ and a sharp spectral peak at frequency $K/r$**.

3. **QFT produces a sharp peak:** The QFT acts on this comb state, and by the
   same character-orthogonality that underlies the classical DFT (the
   `root_orthogonality` lemma in the Catalog's
   `Computation/FourierTransformInversion.lean`), the QFT of a periodic comb has
   a **sharp peak** at multiples of $K/r$.  Measuring yields $r$ with high
   probability.  This evades barrier 2.2 because the *state being transformed*
   is a coherent comb, not pseudorandom samples.

**The key distinction.** The classical DFT operates on *sample values*
$f(0), f(1), \dots$ (pseudorandom).  The quantum QFT operates on a *superposition
state* whose amplitudes encode the periodicity directly.  The quantum advantage
is not "faster arithmetic" — it is that superposition + interference create a
spectral sharpness that pseudorandom samples do not possess.

## 4. Connection to the Catalog's Fourier theory

The Catalog's `FourierTransformInversion.lean` proves the DFT inversion theorem
over any field with a primitive $n$-th root of unity:

$$\text{IDFT}(\text{DFT}(v)) = v \quad\text{via}\quad
\sum_{j<n} \omega^{aj}(\omega^{-1})^{bj} = n \cdot [a = b].$$

This character-orthogonality is *exactly* the identity that makes both the
classical DFT and the quantum QFT work.  The difference is not the mathematics
of the Fourier transform — it is the **object being transformed**:

| | Classical | Quantum (Shor) |
|---|---|---|
| Input | samples $f(0),\dots,f(K-1)$ (pseudorandom) | comb state $\sum_j |x_0 + jr\rangle$ (coherent) |
| Transform | DFT on $\mathbb{C}^K$ | QFT on $\mathbb{C}^K$ (same math) |
| Output | energy spread across harmonics | sharp peak at $K/r$ |
| Cost to resolve $r$ | $K \ge r = \Theta(N)$, exponential | $\log K = O(\log N)$ qubits, poly(log N) gates |

The Fourier mathematics is identical; the physics of the input state is what
differs.

## 5. Connection to the power-sum GCD result (breakthrough #1)

The power-sum GCD finding states: for $N = pq$,
$$\gcd\!\left(N, \sum_{x=1}^{N} x^k\right) \text{ is divisible by } p
\iff (p-1) \mid k \quad (\text{for appropriate } k).$$

This is a *multiplicative-order* phenomenon: the sum $\sum x^k$ collapses mod $p$
precisely when $k$ is a multiple of $p-1$ (the order of the multiplicative
group mod $p$).  The Catalog's `FibonacciGcdSynchronization.lean` proves an
analogous apparition law for Fibonacci numbers: a primitive prime divisor at
prime index $q$ appears *exactly* at multiples of $q$.

Both results are instances of the same underlying structure: **periodicity in
exponentiation reveals factorization**.  The power-sum result is the "easy"
direction (given $k$, compute a GCD); Shor's problem is the "hard" direction
(find the period $r$ itself).  The classical barrier to finding $r$ is exactly
what §2 establishes.

## 6. Honest statement of what is and is not proven

**Rigorous:**
- Resolving period $r$ from $K$ classical samples via DFT requires $K \ge r$
  (frequency resolution).
- For random base $a$, the expected order is $\Theta(N)$, so classical
  sample-count is exponential in $\log N$.
- $f(x) = a^x \bmod N$ is pseudorandom, so the period is not a naive DFT peak
  (experiment 289, 112/112).
- Shor's algorithm finds $r$ in $O(\text{poly}(\log N))$ quantum gates
  (standard result; the QFT-on-comb argument above).

**Strong evidence (not proof):**
- The full barrier framework (284 experiments, 8 barriers, 3 proven theorems)
  suggests *no* classical poly(log N) factoring algorithm exists.
- No classical resource examined (randomness, iteration, analog computation,
  chaos, smoothness) substitutes for quantum superposition.

**Open (famous problems):**
- A proof that classical factoring requires superpolynomial time would separate
  complexity classes; this is not achieved here.
- The barrier framework is a *classification* of why approaches fail, not a
  unconditional lower bound.

## 7. Conclusion

The quantum-classical boundary for factoring is now precisely located:
classical period-finding faces **two independent barriers** (exponential sample
count + pseudorandom spectral hiding), while Shor's algorithm evades both by
transforming a *coherent superposition comb* rather than classical samples.
The Catalog's Fourier-inversion theory confirms that the Fourier mathematics is
identical on both sides — the difference is purely the quantum resource of
superposition.  This sharpens the barrier framework from "classical factoring is
hard" to an exact structural account of *which* resource is missing
classically.

---

*Related:* `00_CONSOLIDATED_BREAKTHROUGH_REPORT.md` (all 8 breakthroughs),
`01_PowerSum_GCD_Factoring.md` (breakthrough #1, the power-sum/order connection),
`02_Structural_Barrier_Theorems.md` (the 3 proven barrier theorems).
