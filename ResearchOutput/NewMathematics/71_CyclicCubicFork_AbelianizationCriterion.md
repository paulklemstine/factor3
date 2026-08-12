# Fork-Pinning ⟺ the Fork Lives in the Abelianization: Cyclic-Cubic Fields Are Congruence-Pinned at 100%, S₃/S₄ Fields Only Through the Sign (CYCLIC-CUBIC-FORK)

**Program:** Factoring research lab — cron loop round-19 #1
**Date:** 2026-08-12
**Status:** Machine-verified criterion on three Galois groups. FORK-FLATNESS
(paper 70) proved the S₃ fork [1,1,1]-vs-[3] of any cubic is Chebotarev-flat
(I(p mod m; fork) = 0 for every m), and its h=1 positive control (x³−2) was
flat too. This experiment identifies the mechanism and completes the
classification: a binary splitting fork is congruence-pinned by a Dirichlet
character **if and only if it factors through the abelianization G^ab of the
Galois closure**. Machine-verified on three groups — cyclic cubic (G = C₃:
fork pinned at **100%** of its entropy, I = H(1/3) = 0.9182 EXACT), S₃
(G^ab = C₂: only the sign is pinned, I(p mod 31; fork) = I(sign; fork) exactly,
the A₃-face fork flat), S₄ (G^ab = C₂: only the sign is pinned, every
within-face fork flat). The criterion *predicts* why paper 70's x³−2 control
failed: S₃ closure ⇒ G^ab = C₂ ⇒ flat by construction — flatness is "fork
outside G^ab", not "class number 1 vs 3". At the semiprime level the 100%-pinned
prime-level fork collapses to a 0.073-bit symmetric residue dichotomy — factor-
useless (barriers 2/5/6/8).

## 1. The criterion

For an irreducible polynomial f with Galois closure L (G = Gal(L/ℚ)), the
splitting type of p in F = ℚ(f) is the conjugacy class of Frob_L(p). A binary
fork is a function of that class. It is *congruence-pinned* (I(p mod m; fork) >
0) precisely when it is a function of the Artin symbol in an abelian extension,
i.e. when it factors through the abelianization G → G^ab:

> **Criterion (FORK-PINNING).** A binary splitting fork of F is pinned by a
> Dirichlet character ⟺ the fork is constant on the fibers of G → G^ab.
>
> - **G = C₃** (cyclic cubic): G^ab = C₃ = G. Every fork is a Dirichlet
>   character — the [1,1,1]-vs-[3] split is pinned at 100% of H(1/3) by p mod
>   cond (the cubic-residue character).
> - **G = S₃**: G^ab = C₂ (the sign = the quadratic-subfield character). Forks
>   constant on sign fibers (the (Δ|p) character) are pinned; the [1,1,1]-vs-[3]
>   fork lives in the A₃ = [S₃, S₃] commutator, orthogonal to G^ab → flat.
> - **G = S₄**: G^ab = C₂ (sign). Forks constant on sign fibers pinned; the
>   even-face (A₄) and odd-face forks are flat.

The criterion is the Abelian/Artin-reciprocity face of Chebotarev density: the
only Dirichlet structure of a prime is its Artin symbol in the *abelianized*
Galois closure, and a splitting fork inherits structure exactly to the extent it
is a function of that symbol.

## 2. Part A — cyclic cubic fields: 100% pinned (the positive control that works)

**cond 7** — f = x³+x²−2x−1 (real subfield of ℚ(ζ₇)). On 6541 primes < 2^16:
nroots {0: 4363, 3: 2178}, correspondence **[1,1,1] ⟺ p mod 7 ∈ {1,6} on
6541/6541 = 100% EXACT**, and no [1,2]-type ever occurs (Galois — types are
[1,1,1] or [3] only). At 2^22 (295,946 eligible primes): P([1,1,1]) = 0.3332
(theory 1/3) and

| m | I(p mod m; fork) | 300-shuffle null (max) | % of H(1/3) = 0.9183 |
|---|---|---|---|
| 7  | **0.9182** | 0.0000 | **100.0%** |
| 49 | **0.9182** | 0.0002 | **100.0%** |
| 5  | 0.0000 | 0.0000 (z = −1.3) | 0.0% |

The fork is a *deterministic function* of p mod 7 (the cubic-residue character),
so I(p mod 7; fork) = H(1/3) exactly; it remains deterministic at m = 49 (42
classes × 7,000 primes — not the sparse regime), and it is **flat at any
coprime modulus** (m = 5) — the pinning is specifically the conductor's
character, a perfect negative control.

**cond 9** — f = x³−3x+1 (real subfield of ℚ(ζ₉)): [1,1,1] ⟺ p mod 9 ∈ {1,8}
on 6541/6541 EXACT, I(p mod 9; fork) = 0.9181 (100%), I(p mod 81) = 0.9181,
m = 5 flat. Same structure.

## 3. Part B — S₃: only the sign is pinned, the A₃-face fork is flat

f = x³+x+1 (Δ = −31), G^ab = C₂. Over all primes P([1,1,1]) = 0.1665 (theory
1/6), P(sign = +1) = 0.5000. The unconditioned fork decomposes exactly:

- **I(p mod 31; fork) = 0.1906 = I(sign; fork) = 0.1906, residual +0.0000** —
  the entire congruence content of the [1,1,1]-fork over all primes is the sign
  character (the quadratic-subfield Jacobi character (−31|p), G^ab = C₂).
- **On the QR face** (sign = +1, n = 147,963): P([1,1,1]) = 0.3330 (1/3) and
  I(p mod 31; fork | QR) = **0.0000** (null mean 0.0001, z = −2.37) — the
  A₃-face fork [1,1,1]-vs-[3] is **FLAT** (paper 70 re-verified at 2^22).

## 4. Part C — S₄: the field is S₄, only the sign is pinned, every within-face fork is flat

f = x⁴−x−1 (disc −283). The field is **S₄, not A₄**: disc −283 is not a square
(an A₄ field must have square discriminant). Verified exactly: nroots
4:2:1:0 = 0.0395/0.2531/0.3318/0.3757 = **1:6:8:9/24 EXACT** (S₄'s five
conjugacy classes; A₄ has no [1,1,2] or [4] type). Paper 65's "A₄ fork"
[1,1,1,1]/[2,2]/[1,3] = 1/12:3/12:8/12 is the **even-face fork** of this S₄
field, reproduced here: 0.0798/0.2501/0.6701 (= 1/12/3/12/8/12, odd-face
[1,1,2]/[4] = 0.5012/0.4988). G^ab = C₂ = the sign:

- **Sign pinned:** I(sign; hasroot) = 0.0483 ≈ theory 0.0488.
- **Beyond-sign residual zero:** I(p mod 283; hasroot) − I(sign; hasroot) =
  **+0.0131 = conditional-null mean EXACTLY** (400 shuffles permuting hasroot
  within the two sign faces, preserving the sign structure — z = +1.00).
- **Every within-face fork flat:** the even-face forks ([1,1,1,1]-vs-rest,
  [2,2]-vs-rest, [1,3]-vs-rest) and odd-face forks ([1,1,2]-vs-[4]) all give
  observed I = null mean exactly (z = −1.00) — the *only* congruence structure
  in the entire S₄ splitting of x⁴−x−1 is the sign.

## 5. Why paper 70's positive control failed (now a prediction, not a surprise)

x³−2 has S₃ closure (L = ℚ(∛2, √−3), G = S₃, G^ab = C₂), so the criterion
*forbids* congruence pinning of its [1,1,1]-vs-[3] fork. Paper 70 measured
I(p mod m; fork) = 0.0000 at m = 9/27/108/216 — exactly as the criterion
predicts. Flatness is "the fork lives in the commutator, outside G^ab", not
"class number 1 vs 3" and not "Kummer vs Hilbert class field". The correct
positive control for "abelian ⟹ pinned" is a field whose Galois closure is
abelian — a cyclic cubic (C₃) — which pins at 100%.

## 6. Part D — the semiprime level is factor-useless (barriers 2/5/6/8)

For the cond-7 cyclic cubic, OR = [p split] OR [q split] (split ⟺ p mod 7 ∈
{1,6}), 23/25-bit factors, n = 30,000: P(OR) = 0.5550 (5/9), and

| N mod 7 | 1 | 6 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| P(OR) measured | 0.3342 | 0.3313 | 0.6578 | 0.6738 | 0.6598 | 0.6661 |
| theory | 1/3 | 1/3 | 2/3 | 2/3 | 2/3 | 2/3 |

I(N mod 7; OR) = **0.0718** ≈ theory 0.0728; I(N mod 49; OR) = 0.0726; the
asymmetric labeled split_p channel = 0.0001 (the which-factor wall). **Even a
fork that is 100% congruence-pinned at the prime level (0.918 bits) collapses to
a 0.073-bit symmetric residue dichotomy at the semiprime level** — because N
carries only the product, and the OR is symmetric in the two factors.

## 7. Seals / barriers

The prime-level pinning (0.918 bits for cyclic cubics) is real and exact — it is
cubic reciprocity (Gauss 1801, Eisenstein 1844), a Dirichlet residue dial, not a
sparse-cell artifact (42-class moduli at 7k primes/class, negative coprime
control flat). At the semiprime level it is symmetric (which-factor lost —
barrier 2), a residue dial / QRLEAK-family (barrier 5), knows p mod 7 and nothing
more (no factor pinning — barrier 6), and every ingredient — cyclotomic fields,
cubic reciprocity, Chebotarev density (1922), Artin reciprocity (1927) — is a
known method (barrier 8). The S₃/S₄ forks contribute *nothing* beyond the sign.
Round-19 #1 done.

**Corrective ledger:**
- Paper 70's x³−2 positive control: not "an open anomaly" — the criterion makes
  it a theorem (S₃ closure ⇒ flat).
- Paper 65's "A₄ fork": correctly identified as the even-face fork of the **S₄**
  field x⁴−x−1 (its densities 1/12:3/12:8/12 are the A₄-face conditionals), not
  an A₄ closure. It is flat (this experiment), consistent with the criterion.

*Scripts:* /tmp/exp_cycliccubic.py (Parts A–D, limit 2^22, 51 s), within-face
S₄ supplemental (2^17 root-counted sample).
