# Paper 201 — EULER-LOSES: The Two-Squares Factorization Route, Measured

**Verdict name: EULER-LOSES (formula exact, class narrow, cost dominated).**
Round-72 #1 (user-directed Pythagorean/Euler campaign) · exp 557 · assessment v308 · script `ResearchOutput/scripts/2026-08-21-resume/exp557_euler_two_squares.py` (+ `exp557_result.json`, logs) · seed 20260826.

## 1. Existence (Part A)

r₂(N)=4(d₁−d₃) counting over 3000 semiprimes stratified by (p mod 4, q mod 4):
**≥2 essentially distinct representations ⟺ BOTH primes ≡ 1 mod 4 — exactly two
reps there (mean U = 2.0, never more), zero reps in every other class**
(750/750 per cell; eligible fraction of all draws = 0.2500 exactly).
Validation: 60 small cases formula-vs-brute-force 0 mismatches; degenerate y=0/x=y
impossible for odd p<q (asserted).

## 2. Algebra (Parts C + real instances)

The extraction identity derived in-script: Euler's combination reduces to
**gcd(|ad−bc|, N)** via Im(z₁·conj(z₂)) being a multiple of exactly one prime norm
(0<2uv<q bounds proven). Verified **500/500** synthetic constructions and **750/750**
real eligible instances — both extraction variants recover a proper factor ALWAYS.
The algebra was never the problem.

## 3. Cost face (Part B — the verdict)

Eligible-class iteration counts (caps 10⁶, zero censored):

| quantity | median | mean |
|---|---|---|
| first-rep search | 81,132 | 113,359 |
| second-rep extra | 72,215 | 107,251 |
| plain Fermat (same Ns) | 33,749 | 65,819 |
| rep-scan / Fermat | **2.48×** | heavy tail to 202,070× |
| **end-to-end Euler / Fermat** | **5.70×** (q75 33.8×) | max 421,147× |

Finding a sum-of-two-squares representation is another gap scan (~2.5× one Fermat
scan's constants), and Euler pays for two. Plain Fermat dominates on identical
instances; on balanced pairs (Fermat lands in ~1 step) Euler loses catastrophically.
Barrier-8 consistent — no new leverage.

Now 550 experiments (max id). Assessment v308.
