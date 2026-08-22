# ET-HINTS-REDUCED (round-39, exp 474 rerun) — proofs and closed forms

Work dir /tmp/exp39_ethints only (remnants of the two dead attempts archived in
archive_attempt1and2/; they used a different spec — seed 20260824, M=256/4096,
w-anchored posteriors — and are superseded by this reduced-task spec).

## 1. Model (stipulated by the brief, exactly coherent)
Windows W_a = [a, a+mu-1], a = 1..L, L = M-mu+1. Draw A ~ Unif{1..L}, H ~ Bern(alpha).
Hit: J | (A,H=1) ~ Unif{a..a+mu-1}. Miss: J | (A,H=0) ~ Unif([1,M] \ W_a).
The procedure sees only the named window; cost of outcome J = its position in the
procedure's scan order for that window.
DISCLOSURE (model consequence, not an approximation): under these stipulated
conditionals J's unconditional law is NOT w — marginalizing gives P(J=j) = 1/L on
interior j exactly (edge windows dip slightly). The brief itself prices only E_base
with w, so w enters through the baseline alone. A w-anchored alternative that keeps
J ~ w is priced in stage `alt` as a robustness leg (section 9).

## 2. Baseline
E_base = sum_j j(2(M-j)+1)/M^2 = (M+1)(2M+1)/(6M). Exact identity (selftest-checked).
At M = 10^5: 33333.833335.

## 3. COMMITTED: window ascending, then complement ascending
Rank C(j;a) = j-a+1 (in window); j+mu (j<a); j (j>b).
E[C|hit] = (mu+1)/2, independent of a.
Averaged over A (power sums, exact):
  E_comm(alpha,mu;M) = alpha (mu+1)/2 + (1-alpha) [ (L^2-1)/6 + mu(L-1)/2
      + M(M+1)/2 - ( G(M)-G(mu-1) )/(2L) ] / (M-mu),   G(n)=n(n+1)(n+2)/3.

## 4. INTERLEAVED: inside-out zigzag anchored at the interval's near end a
Order: a; a-1,a+1; a-2,a+2; ... clamped to [1,M], skipped slots compress.
RANK LEMMA (two-sided; verified against constructed orders at every j for 10 (M,a)
cells incl. both boundary regimes): with m=a-j, d=j-a,
  R(a)=1; R(j<a) = m+1+min(m-1, M-a); R(j>a) = d+1+min(d, a-1).
(The one-sided form 2(a-j), 2d+1-max(0,d-a+1) is correct ONLY when the left side
clamps first; it fails for anchors near M — caught by selftest, see ledger.)
Closed form (all pieces quadratic in a, summed exactly via power sums):
  hit: for a >= mu the offset-average is mu^2/mu... precisely
     sum_a H(a) = sum_{a<=min(L,mu-1)} [-a^2/2 + (mu+1/2)a + mu(mu-1)/2]
                  + mu^2 * #{a in [max(1,mu), L]},
     E[R|hit,a] = H(a)/mu.
  miss: sum_a [ U(a) + V(a) ] over three/five quadratic regimes:
     U(a) = a^2-a                       (a <= floor((M+2)/2))
          = -a^2 + 2(M+1)a - (M+1)(M+2)/2   (else);
     V(a) = -a^2/2 + (1/2-mu)a + (M^2+M-mu^2+mu)/2   (a<=mu, needs M-a>=mu)
          = -a^2 + a + (M^2+M)/2 - mu^2                   (mu<a<=floor(M/2))
          = a^2 - 2(M+1)a + (M+1)^2 - mu^2                (a>floor(M/2), a<=M-mu),
     V=0 when M-a<mu. E[R|miss,a] = (U(a)+V(a))/(M-mu).
  E_intl = alpha*Hbar/mu + (1-alpha)*(Ubar+Vbar)/(M-mu).

## 5. BAYES-OPTIMAL ordering == COMMITTED (exact identity)
Given the observed window the posterior takes exactly two values:
q_in = alpha/mu (window), q_out = (1-alpha)/(M-mu) (complement) — independent of a.
By the rearrangement inequality the optimal order puts all q_in items before all
q_out items; within a class any order has equal expected cost. Hence BAYES-OPTIMAL
and COMMITTED coincide EXACTLY (asserted numerically at M=300, diff < 1e-11).
Corollary (hint-blind floor): any ordering independent of the hint has
E[cost] = (M+1)/2 regardless of the posterior (linearity). The hint's entire value
is pushing below (M+1)/2; measured: 20k random perms mean 150.5 +- <=2.02 SEM.
Local=global certificate: adjacent-swap descent changes cost by q_x - q_y per swap,
so its only sinks are posterior-sorted orders; from 50 random starts per anchor the
sink cost exceeded opt by 0.00e+00.

## 6. Verification protocol (all machine-generated, staged checkpoints)
- Selftest: 60 exact Fraction equalities (closed vs brute double sums at 10
  (M,mu) pairs x 3 alphas x 2 procs, tol 1e-12; rank lemma vs constructed orders;
  E_base identity).
- Exhaustive enumeration M=300: brute exact double sums vs closed forms on the full
  16-cell grid: worst relative gap 0.0 (exact to float print precision).
- Monte Carlo M=10^5: seed 20260828, numpy PCG64 single stream, 200k draws/cell,
  16 cells x 2 hinted procedures (+ baseline check): max |z| = 1.30 (committed),
  1.52 (interleaved); E_base MC z = +0.54. Pass rule |z|<=4: ALL PASS.

## 7. Results: speedup table S = E_base / E_cost at M=10^5
BAYES-OPTIMAL (= COMMITTED), exact closed form:
  alpha\mu/M   0.02     0.05     0.1      0.2
  0.50         1.282    1.212    1.111    0.952
  0.75         2.469    2.222    1.905    1.481
  0.90         5.555    4.444    3.333    2.222
  1.00        33.317   13.331    6.666    3.333
INTERLEAVED (same grid):
  0.50         1.259    1.163    1.037    0.867
  0.75         2.341    1.983    1.589    1.157
  0.90         4.837    3.437    2.334    1.448
  1.00        16.724    6.726    3.396    1.739
Notes: (i) interleaved is strictly dominated by committed everywhere on the grid —
the zigzag spends ~2x the steps inside the window to accelerate candidates the
posterior values LESS than window members; (ii) at alpha<=0.5, mu/M>=0.2 the
"hint" procedure is slower than plain ascending scan.

## 8. Crossing of paper 137's 5.19x
Asymptotics: E_comm/M = alpha x/2 + (1-alpha)(1+x-x^2)/2, x=mu/M. Setting
= 1/(3*5.19) = 0.0642254: solvable iff alpha > alpha_min = 1 - 2/(3*5.19)
= 0.87155 — RELIABILITY GATES THE GAIN; no interval width can substitute (at
alpha=0.75 the max achievable speedup, x->0, is 1/(3*(1-alpha)/2) = 2.67x).
Finite-M bisection on the closed form (M=10^5), x*(alpha):
  alpha : 0.88 -> 0.00845 ; 0.90 -> 0.02845 ; 0.92 -> 0.04845 ;
          0.95 -> 0.07845 ; 0.99 -> 0.11845 ; 1.00 -> 0.12845
— to four decimals the crossing obeys the LINEAR LAW x* = alpha - 1 + 2/(3*5.19)
(= alpha - 0.87155; the quadratic correction is O((1-alpha)^2)).
Interleaved reaches 5.19x only at ~half the width: x*(0.90)=0.01503, x*(1.0)=0.06498;
no solution at alpha<=0.75.
ANSWER: paper 137's magnitude-ordering gain of 5.19x corresponds to an effective
interval quality of (alpha ~= 0.90, mu/M ~= 0.028) — or any point on
mu/M = alpha - 0.872 with alpha in [0.872, 1]; e.g. a perfect oracle (alpha=1)
confined to ~12.8% of the list. Nearest grid cells: (0.9, 0.02) -> 5.56x,
(0.9, 0.05) -> 4.44x.

## 9. Robustness: w-anchored alternative model (stage alt, MC seed SEED+1)
J ~ w always; hit-window uniform among containing windows; miss-window uniform
among avoiding windows; committed order. This violates the brief's literal uniform
clauses (positions come out w-weighted) but keeps the TRUE marginal — the opposite
modeling choice. Speedups move UP (target mass concentrates at small j, which the
committed order exploits): (0.9,0.02): 7.62x vs 5.56x; (0.9,0.05): 5.69x vs 4.44x;
(1.0,0.02): 34.02x vs 33.32x; (0.75,0.05): 3.04x vs 2.22x. The stipulated pricing
is therefore the conservative one; the qualitative laws (reliability gate,
committed dominance) are unchanged.

## 10. Barrier note
Positional information escapes the residue cap because the interval correlates
with J directly (paper 138's Thm-A coordinate argument): no residue-class map is
involved. The hint acts on the scan ORDER and cost is order-sensitive, so the
which-factor wall and the abelianized residue caps do not bind here; the value of
the hint is exactly the gap between (M+1)/2 (hint-blind floor) and the priced
expected costs above.

## 11. Method ledger (designed-check catches during THIS rerun)
1. Interleaved rank first written one-sided (left-clamp-only); caught by selftest
   on asymmetric configs (M=30, a=26, j=1) — same error class as dead attempt #1's
   ledger entry; replaced by the exact two-sided min() form.
2. Closed-form regime V_A carried an extra mu in its constant term ((M+1)^2 -
   mu(mu-1) instead of (M+1)^2 - mu^2); caught by closed==brute assertion at
   M=300 (off-by-exactly-3 per anchor over 12 anchors); fixed, now exact.
3. Bayes block first built ONE global order from the hint-MARGINALIZED posterior —
   wrong object (with A uniform every j lies in some window; the marginalized law
   is near-uniform, so "optimal" degenerated to (M+1)/2). Rebuilt conditioned on
   the OBSERVED window; identity with committed then holds exactly.
4. Descent direction sign flipped (sank to the WORST monotone order, +144 over
   opt); caught by sink-gap assert; fixed to descend on d<0.
5. Enum stage compared closed-at-alpha against brute-at-alpha=1/2 (relgap 0.955);
   caught by the 1e-11 relgap assert after tightening; brute recomputed per cell,
   worst relgap now 0.0.
6. Random-permutation mean check first asserted |dev|<=0.05 absolute (SEM ~0.12);
   converted to a 6-SEM z rule; passing at <=2.02 SEM.
7. Dead attempts' remnant result.json was loaded by the resume logic (no "stages"
   key crash); remnants archived, fresh ledger started.
