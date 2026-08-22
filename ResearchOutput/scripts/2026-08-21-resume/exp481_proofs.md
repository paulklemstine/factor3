# ET-HINTS (round-39, exp 474) — Interval hints in the expected-cost functional

**Canonical run**: seed `20260824`, exact arithmetic (`fractions.Fraction`), MC = numpy
PCG64(20260824), 200k draws/config.
Code: `/tmp/exp39_ethints/et_hints_verify_canonical.py`; machine outputs:
`/tmp/exp39_ethints/et_hints_result_canonical.json` (mirrored to `result.json`).

**File-history disclosure.** A parallel writer ran a *reduced alternate* spec in this
directory (randomized window placement A~Unif{1..L}, miss → uniform complement,
seed 20260828; files `verify.py`, `proofs.md`, archived copies of earlier attempts in
`archive_attempt1and2/`). That model makes the outside posterior **flat**, under which
Bayes-optimal ≡ committed exactly (their §5) — see Appendix B for why this is a
degenerate special case of Thm 3. The present document implements the brief-literal
model (w-anchored target law, both coverage models) and supersedes nothing of theirs;
both runs coexist.

---

## 0. Setup and modeling assumptions (isolated)

Index space j = 1..M (candidates r ∈ [2,√N], M = π(√N)). Target index J ~ w(j) =
(2(M−j)+1)/M², the min-of-two-uniforms law: S(t) := P(J ≥ t) = ((M−t+1)/M)².

An oracle reports an interval [a,b], μ = b−a+1, containing J with probability α.
The scanner **does not observe whether this instance is a hit**; it chooses a fixed
scan order σ (a permutation of 1..M); cost(J=j) = pos_σ(j). All expectations below are
under the posterior π(j) = P(J=j | report), which is the *true* law of J for a
hint-holder. Baseline: ascending scan under the prior, E_base = Σ j·w(j).

Two generation models (the brief's "independent coverage / position-biased" pair):

- **CAL (calibrated)**: π = α·U[a,b] + (1−α)·(w|complement). Posterior mass inside =
  α exactly — the report's coverage claim is honest.
- **POS (position-biased)**: given hit, J|hit ~ w|[a,b]: π_in(j) = α·w(j)/W_in,
  π_out(j) = (1−α)·w(j)/W_out. The hit-branch inherits the prior's shape.

Both are affine in α: π_α = α·g + (1−α)·h with g,h fixed laws (used in Thm 7).

**Joint-existence (calibration capacity).** CAL's conditionals require
P(H=1|J=j) = (α/μ)/w(j) ≤ 1 on [a,b]; hence

> α_cal(a,b) := μ·w(b) = μ(2(M−b)+1)/M².  POS is jointly realizable for every α∈(0,1).

Asymptotics at width fraction x = μ/M: left-placed (b≈xM): α_cal ≈ 2x(1−x);
mid: ≈ x; right-placed (b=M): α_cal = x/M → 0. **Calibration capacity is placement-
monotone decreasing and vanishes entirely for intervals near √N.** [Measured:
headline block of result.json.]

Procedures: `base` (ascending), `com` (interval ascending, then complement ascending),
`int` ("interleaved": interval ascending, then outward rings (a−d, b+d), left cell
first in each pair; after one side exhausts the survivor continues consecutively —
"inside-out from the boundary outward", always complete), `opt` (descending-π).

## 1. Unconditional fragments (no hint model used)

**Lemma 1 (w-law identities).** For w(j) = (2(M−j)+1)/M²:
S(t) = ((M−t+1)/M)²; F(p) := Σ_{j≤p} w(j) = 1 − ((M−p)/M)²;
T(p) := Σ_{j≤p} j·w(j) = [(2M+1)Σ₁ₚj − 2Σ₁ₚj²]/M²; range sums by subtraction.
*Proof.* Direct summation; machine-verified exactly against brute loops (selftest).
∎

**Theorem 2 (baseline).** E_base = Σ_{j=1}^M j·w(j) = (M+1)(2M+1)/(6M) = M/3 + 1/2 + 1/(6M).
*Proof.* T(M) simplification; exact identity check included in selftest. ∎

## 2. Optimality of descending-π ordering

**Theorem 3 (rearrangement / Bayes-optimal procedure).** For any strictly positive pmf π,
min over scan orders of Σ_j π(j)·pos_σ(j) is attained by σ* sorting π descending
(ties arbitrary). Proof: adjacent interchange — swapping neighbors i,i+1 changes cost
by π(later) − π(earlier); a swap strictly helps iff the larger π sits later; any order
not sorted desc admits an improving swap; finiteness ⇒ termination at sorted orders,
which are exactly the local and global optima. ∎

*Machine certification*: (i) exhaustive enumeration of **all M! permutations** at
M = 5,6,7,8 over 12–14 (placement, model, α) configs each — worst relative gap between
sort-desc value and brute minimum: ≤ 2.3e-16 (`exhaustive_optimality`);
(ii) M=64: 20k random permutations all ≥ E_opt − 1e-9 and 20 independent
adjacent-swap descents all converge exactly to E_opt (`random_ordering_certification`);
(iii) hump cells re-certified exhaustively at M=9 across the α grid (Thm 7).

## 3. Committed: closed form and the position-preservation lemma

**Lemma 4 (right-complement position preservation).** Under `com`, outside cells to
the RIGHT of the interval keep their baseline positions: pos(j) = j for j > b; left
cells pay pos(j) = j + μ; interval cell j pays pos = j − a + 1.
*Proof.* com = [a..b] ++ [1..a−1] ++ [b+1..M]; count offsets: μ + (a−1) + (j−b) = j. ∎

**Theorem 5 (committed cost, affine comparison form).**
Let W_in = F(b)−F(a−1), W_out = 1−W_in, A_in^POS = (T_in − (a−1)W_in)/W_in where
T_in = T(b)−T(a−1), and B = (μ·F_L + T_L + T_R)/W_out with F_L = F(a−1),
T_L = T(a−1), T_R = T(M)−T(b). Then

- POS: E_com(α) = α·A_in^POS + (1−α)·B   (affine, slope A−B)
- CAL: E_com(α) = α·(μ+1)/2 + (1−α)·B    (uniform-given-hit inside)

*Proof.* Sum Lemma 4 positions against the two-level-shaped posteriors; inside sums are
Σ_t t/μ or Σ (j−a+1)w(j)/W_in respectively; exact equality with programmatic costs is
asserted over a 77-cell grid including asymmetric and one-sided intervals (selftest). ∎

E_com(0) > E_base whenever the interval displaces prior-heavy cells: committed with a
useless certificate is *worse* than ignoring it — quantified by B − (B-part of base).

## 4. Interleaved ("inside-out"): ring-position lemma

**Lemma 6 (rings with exhaustion).** Let L = a−1, R = M−b, m = min(L,R). Under `int`:
interval cells occupy 1..μ; for d ≤ m: pos(a−d) = μ+2d−1, pos(b+d) = μ+2d; after one
side exhausts the survivor runs consecutively: (R>L) pos(b+d) = μ+L+d for d>L;
(L>R) pos(a−d) = μ+R+d. All outside sums close via F/T (ring_sum).
**Theorem 6 (interleaved cost).** Same affine-in-α forms as Thm 5 with the ring sum
replacing B's complement term: CAL E_int = α(μ+1)/2 + (1−α)·ring/W_out;
POS E_int = α·A_in^POS + (1−α)·ring/W_out. Exactness asserted vs programmatic orders. ∎

**Structural finding (misalignment).** Under both posteriors the outside posterior is
w-shaped (decreasing in j): its mass sits FAR LEFT, while `int` visits far-left cells
LAST (distance d = a−1 ⇒ position ≈ μ+2a). Interleaving is posterior-aligned only when
the interval is at a=1 (where int ≡ com identically). Measured (M=256, 36 POS cells +
feasible CAL): sp_int = sp_com exactly for left-placed intervals and strictly worse
otherwise — down to 0.659 vs 1.120 (x=1/16 right, α=1/4), a 41% relative loss. The
"hedge by alternating" intuition buys nothing and costs up to ~45%.

**Structural finding (opt vs com).** Under POS the two posterior segments carry
constant multipliers m_in = α/W_in, m_out = (1−α)/W_out on a COMMON w-shape, so the
descending-π order merges them by the ratio rule (inside cell j precedes outside cell k
iff w(j)/w(k) ≥ m_out/m_in). Block commitment is optimal iff no crossover occurs
(essentially always for left/mid placements); at the RIGHT edge with low α the
interval's high-w head interleaves ahead of the complement and its low-w tail behind,
giving opt a strict edge (e.g. 1.1201 vs 1.1095 at x=1/16 right, α=1/4). Under the
feasible CAL band com can be strictly WORSE than baseline while opt stays nearer par
(0.821 vs 0.928 at x=1/4 left, α=1/4).

## 5. The hedging hump (E_opt as a function of coverage)

**Theorem 7 (concavity and the hump).** Each fixed order σ has E_σ(α) = ⟨π_α,pos_σ⟩
affine in α (both models); therefore E_opt(α) = min_σ E_σ(α) is **concave piecewise
linear** in α. Consequently intermediate coverage can be strictly worse than BOTH
endpoints: the optimal scanner must pay a complement prefix before the interval AND
the interval block before the complement remainder. At such α the hint can be harmful:
E_opt(α) > E_base even under the Bayes-optimal response.

*Machine evidence:* `hump_exhaustive_M9` — sort-desc optimality re-certified against
all 9! permutations at each of ~30 (model, α) cells; local rises present.
`hump_profiles_M512` — profiles at M=512 for x ∈ {1/16, 1/4} × {left, mid, right} ×
{CAL, POS}: [numeric summary auto-inserted in §9 table].

## 6. Comparison law: Speedup(α, x) and the crossing vs paper 137's 5.19×

**Theorem 8 (two width ceilings, placement-structured).** At α=1 the posterior lives
inside the interval, so the best cost is the α=1 in-interval cost:
- CAL (uniform-given-hit): (μ+1)/2 for every placement ⇒ cap = 2E_base/(μ+1) ≈ **2/(3x)**.
- POS (w-shaped-given-hit): A_in^POS = (T_in − (a−1)W_in)/W_in. For a RIGHT-placed
  interval the truncated w reproduces the min-of-two-uniforms shape: substituting
  t = j−(M−μ+1), A_in = μ(μ−1)(2μ−1)/(6μ²) → **μ/3**, so cap → E_base/(μ/3) ≈ **1/x**.
  Left-placed (w ≈ flat on [1,μ] for x ≪ 1): A_in ≈ (μ+1)/2, cap ≈ 2/(3x).

> Speedup ≥ 5.19 therefore forces x ≤ 2/(3·5.19) = **0.1285** for CAL / uniform /
> left-POS, but only x ≤ ≈ **0.1927** (= 1/5.19) for right-placed position-biased hints.
> Machine caps at M=4096: uniform cap 42.0 / 21.2 / 10.6 / 7.1 / 5.3 / 3.55 at
> x = 1/64 … 3/16; the x=3/16 row is infeasible (cap 3.55) for every model/placement
> EXCEPT POS-right, which still crosses at α* = 0.9963.

**Theorem 9 (crossing inversion).** On any branch where the procedure's order is
fixed, E(α) is affine, so α*(s) = (E_base/s − B)/(A − B) explicitly (Thm 5/6 forms);
for `opt` the branches switch at posterior-ranking thresholds and α*(s) is obtained by
bisection on the exact rational evaluation (40 iterations). Note Speedup(α) is NOT
monotone where the hump (Thm 7) dips below baseline; the bisection reports the FIRST
crossing from below. Full table in §9; headline readings:
α*(5.19) ≈ 0.83 at x=1/64 falling to 0.94–0.996 at x=3/16 — **matching paper 137's
5.19× demands near-certain coverage (α ≳ 0.83) AND width x ≤ 1/8 (x ≤ 3/16 only for
right-placed POS)**.

**Calibration gate (corollary of §0).** Uniform-given-hit CAL can only realize
α ≤ α_cal ≈ 2x(1−x) (left) — e.g. 0.117 at x=1/16, 0.376 at x=1/4 (left), and
x/M → 0 (right). Since α*(5.19) ≥ 0.83 everywhere in the feasible width range, **the
uniform-given-hit calibrated family can NEVER match magnitude-ordering's 5.19× at any
width or placement** — every CAL crossing row is formally solvable as a posterior but
unrealizable as a joint (feasible_CAL flags in the tables). POS faces no such gate
while remaining containment-calibrated (its posterior also puts mass exactly α inside);
the binding dichotomy is the hit-placement SHAPE inside the interval, not the coverage
claim: an oracle that finds J where J is dense (interval's low edge) is
position-biased and unconstrained; one that scatters hits uniformly is capped.

## 7. Bits accounting (is an interval hint worth more than its bit-count?)

KL(report; J) = KL(π‖w) in bits closes in one line per model because π/w is piecewise
constant: POS: I = α·log₂(α/W_in) + (1−α)·log₂((1−α)/W_out); CAL:
I = α·E_{U[in]} log₂(α/(μ w(J))) + (1−α)·log₂((1−α)/W_out).
Compare log₂Speedup per bit in `speedup_table_M256` (KL_bits, log2_sp_opt columns):
[numeric summary in §9]. The naive yardstick log₂(5.19) = 2.376 bits is *not* what the
top cells spend — E[T]-speedup and Shannon bits price different things; see §9/residual.

## 8. Scope statement (ISOLATION-COST / GENERIC-RECOVERY / paper 138 residual)

1. **ISOLATION-COST (oracle query pricing).** The per-query breakeven price of the
   oracle is exactly Δ(α,x,place,model) = E_base − E_hint(procedure); beyond that the
   hint destroys value net of query cost. The hump (Thm 7) makes Δ negative in a band
   of intermediate α for wide/left placements — an oracle can be worth *negative*
   price under partial trust.
2. **GENERIC-RECOVERY taxonomy.** Interval hints are the first priced member of the
   *positional-continuous* class: they act on ORDER, not membership. Trace-set filters
   (paper 138's INTERVAL-HINT result) are exact but no-amplifying at cost parity
   because they reorder nothing; interval hints reorder and thereby escape that parity —
   the functional matters more than the hint's carrier.
3. **Paper 138 residual, stated precisely.** Paper 138 prices external hints linearly
   in which-factor bits with ceiling 2×/dial. Under the E[T] functional an interval
   hint has MI(hint; factor identity) = 0 BY CONSTRUCTION (position channel, barrier-2
   escape: the report correlates with J's index directly, not through any residue map),
   yet purchases up to Speedup_cap(x) ≈ 2/(3x) — unbounded as x→0, no dial counting.
   So the two pricing functionals disagree qualitatively: which-factor pricing assigns
   zero, E[T] pricing assigns the whole cap. The residual gap: **a unified pricing must
   condition intervals on factor-carrying observables (residue-conditioned intervals);
   pure-position hints dominate E[T] while remaining factor-blind, so magnitude-
   ordering's 5.19× is matched by hints carrying NO factor information whatsoever** —
   the 2×/dial ceiling governs filters, not scans.
4. **Barrier line (8) (Fermat/SQUFOF faces).** Scanning near √N IS Fermat's start:
   Fermat commits to the degenerate interval [⌈√N⌉, ∞) — a rightmost interval with
   α = P(p ≥ √N-side | N=pq)... its calibration capacity α_cal = x/M vanishes, which
   is the ET-HINTS explanation of why Fermat's start point carries so little
   exploitable coverage: commitment without coverage.

## 9. Machine results (extracted from et_hints_result_canonical.json)

**Baseline.** E_base(M=256) = 85.8340 = 85 + 513/1536; E_base(300) = 100.5006;
E_base(4096) = 1365.8334. Formula (M+1)(2M+1)/(6M) exact at all M (selftest).

**Optimality certification.** Exhaustive all-permutation enumeration M=5,6,7,8
(12–14 configs each, both models × α ∈ {0.3, 0.9}): worst relative gap between
descending-π value and brute minimum = 1.3e-16 (M=8, 12 configs × 40320 perms).
M=9 hump cells: 31 (model, α) cells × all 362880 perms — all match; **16 of 31 cells
are local rises** (direct hump evidence at certificate scale). M=64: 20k random
permutations all ≥ E_opt − 1e-9; 20/20 swap-descent sinks = E_opt exactly.

**Monte Carlo.** 40 configs (M ∈ {200,1024} × x ∈ {1/16,1/8} × {left,mid,right} ×
{CAL,POS} × 2 α), 200k draws each, seed 20260824, 3 procedures per config = 120
exact-vs-MC comparisons: **max |z| = 2.343** (pass rule |z| < 4). CAL cells clipped to
feasibility; no config violated calibration bounds.

**Speedup table (M=256, POS; sp_opt = sp_com except as noted).**

| x | place | α=0.25 | α=0.50 | α=0.75 | α=1.00 | KL(α=1) bits | log₂sp(α=1) |
|---|-------|--------|--------|--------|--------|--------------|-------------|
| 1/16 | left  | 1.153 | 1.636 | 2.820 | 10.201 | 3.046 | 3.351 |
| 1/16 | mid   | 1.168 | 1.658 | 2.856 | 10.298 | 3.989 | 3.364 |
| 1/16 | right | 1.120ᵒ | 1.607ᵒ | 2.892 | **14.688** | 8.000 | 3.877 |
| 1/8  | left  | 1.017 | 1.392 | 2.207 | 5.317 | 2.093 | 2.410 |
| 1/8  | mid   | 1.040 | 1.423 | 2.254 | 5.419 | 2.989 | 2.438 |
| 1/8  | right | 0.995ᵒ | 1.370ᵒ | 2.311 | 7.683 | 6.000 | 2.942 |
| 1/4  | left  | 0.933 | 1.076 | 1.551 | 2.771 | 1.193 | 1.470 |
| 1/4  | mid   | 1.001 | 1.113 | 1.605 | 2.875 | 1.989 | 1.524 |
| 1/4  | right | 0.876 | 1.092 | 1.676 | 3.931 | 4.000 | 1.975 |

ᵒ = cells where opt strictly beats com (right-edge w-ratio interleaving). sp_int ≤
sp_com everywhere (equal only left-placed), worst 0.659 vs 1.120. CAL feasible cells
at M=256: exactly ONE (x=1/4 left, α=0.25): sp_opt = 0.928, sp_com = 0.821 — **below
par**: within its feasibility band the uniform-given-hit family never accelerates in
the measured grid.

**Hedging hump (M=512, E_base = 171.17; E_opt(α) profiles).**
Worst harmful bands (E_opt > E_base): x=1/4 right POS peak 196.09 at α=0.20 (cap
3.97 at α=1); x=1/4 left CAL peak 187.47 at α=0.30; x=1/4 left POS peak 186.31 at
α=0.30; x=1/16 right POS peak 180.30 at α=0.05. Endpoint values: e.g. x=1/4 right POS
E(0)=154.10 → E(1)=43.17 (speedup 3.97); x=1/16 right POS E(0)=169.91 → E(1)=11.17
(speedup 15.32). Hump ratio (peak/cheaper-endpoint) up to 16.1. CAL profiles are
confined to α ≤ α_cal (n = 3/2/1 cells at x=1/16 left/mid/right) — the hump band is
where CAL lives, another way the calibrated family is trapped.

**Crossing vs paper 137's 5.19× (M=4096, E_base = 1365.83).**

| x | cap (uniform/CAL/left) | α*(5.19) POS opt | α*(5.19) CAL opt | α*(5.19) POS-right opt |
|---|-----|-----|-----|-----|
| 1/64 | 42.03 | 0.8323 | 0.8324 | 0.8285 |
| 1/32 | 21.18 | 0.8565 | 0.8567 | 0.8481 |
| 1/16 | 10.63 | 0.9035 | 0.9044 | 0.8837 |
| 3/32 | 7.10 | 0.9485 | 0.9506 | 0.9157 |
| 1/8 | 5.33 | 0.9915 | 0.9954 | 0.9448 |
| 3/16 | 3.55 | infeasible | infeasible | 0.9963 |

(POS ≡ com α* to ≤ 5e-5 except right-placed; CAL ≡ POS to ≤ 5e-3 as posteriors, but
CAL rows are UNREALIZABLE: α* ≥ 0.83 ≫ α_cal ≤ 2x(1−x) ≤ 0.376.) **The α*(5.19)
curve vs paper 137: an interval hint matches magnitude-ordering's 5.19× iff it is
narrow (x ≤ 1/8; x ≤ 3/16 only right-placed POS) AND nearly certain (α ≥ 0.83–0.996).**

**Bits.** KL at α=1 = log₂(1/W_in) exactly (e.g. 8.000 bits at x=1/16 right, W_in =
(1/16)²) buying log₂ 14.69 = 3.877 bits of E[T]-speedup: the E[T] functional buys
~half its Shannon price at the best cell, and the naive yardstick log₂5.19 = 2.376
bits is crossed only by α ≥ 0.75 narrow-right cells (e.g. 5.19 bits spent at
x=1/16 right α=3/4 for 1.53 bits of speedup — Shannon-expensive, E[T]-cheap).

**Isolation-cost breakeven.** Per-query oracle price ≤ E_base − E_hint; at the hump
peak the hint is worth NEGATIVE (−24.9 at x=1/4 right α=0.20, M=512); at x=1/16
right α=1 it is worth +154.7 per query (M=512 scale).

## 10. Method ledger (all self-caught errors)

1. Interleaved closed form originally assumed permanent left/right pairing; caught by
   the selftest on asymmetric configs; replaced by 3-segment ring_sum.
2. POS posterior initially missed the (1−α) complement mass on the outside
   (summed to 1+α); caught by exact closed-form==programmatic equality checks.
3. CAL had the SAME normalization bug but PASSED those consistency checks (closed
   forms shared the error); caught only by Monte Carlo (z = −72 against normalized
   sampling). Fix: π_out = (1−α)w/W_out; added a hard sum(pi)==1 assertion. Lesson:
   consistency checks certify internal agreement, not model coherence — the stochastic
   cross-check was load-bearing.
4. Debug script once launched exhaustive permutation enumeration at M=64 (64!
   infeasible); killed; redone at M ≤ 10.
5. speedup_table applied the CAL-only calibration skip to POS rows too; caught by
   inspection of the archived run; gated on model=='CAL'.
6. Theorem 8 originally claimed a universal 2/(3x) α=1 ceiling. The M=256 table
   refuted it: POS-right x=1/16 α=1 reached 14.69× > 10.67. Recomputation showed the
   truncated w-shape inside a right-placed interval reproduces min-of-two-uniforms
   (A_in = μ(μ−1)(2μ−1)/(6μ²) → μ/3), giving cap → 1/x and x_crit → 0.1927 for that
   placement. A hand "consistency check" of E_base against the wrong M initially
   disguised the discrepancy as a rounding artifact — the catch came from redoing the
   arithmetic exactly.
7. Process hazards (not mathematics): two infrastructure kills before any output; a
   concurrent writer replaced verify.py/proofs.md mid-run twice, archived earlier
   files, and renamed the model spec; resolved by distinct canonical filenames +
   full deterministic rerun (fixed seed ⇒ byte-identical numbers).

## Appendix A. Verification protocol summary

- Closed forms vs programmatic order costs: exact Fraction equality, 77 cells
  (asymmetric/one-sided/full-guarded grids, both models, 5 α-values).
- Optimality: exhaustive M! enumeration M=5..8 (worst gap ≤ 2.3e-16) and M=9 on all
  hump cells; random-perm dominance (20k perms, M=64) and swap-descent sinks.
- MC: 200k draws/config, seed 20260824, inverse-CDF sampling of π; pass rule |z|<4;
  max |z| observed = 2.343 over 120 comparisons (40 configs × 3 procedures).
- Crossing: bisection on exact rational evaluations at M=4096, 40 iterations.

## Appendix B. Relation to the reduced alternate spec (parallel writer)

Their model (window placement randomized, miss → uniform complement) yields a
two-valued posterior (α/μ in-window, (1−α)/(M−μ) outside). Then the outside ranking is
FLAT, and by Thm 3 every optimal order puts the window first wholesale: Bayes-optimal ≡
committed EXACTLY, and their asymptotic gate α > 1 − 2/(3·5.19) ≈ 0.8715 follows from
setting their E_com/M formula to 1/(3·5.19). Under the brief's w-law the outside
posterior is w-shaped, the equivalence fails (opt strictly beats com in most cells),
and additional structure appears (calibration capacity, hedging hump). The two specs
are the x→flat limit and the w-anchored model respectively; both are internally
coherent answers to "price external interval hints", and they bracket the design space
from opposite ends: their gate says reliability is everything; ours adds WHERE the
window sits and HOW HONEST it may be.
