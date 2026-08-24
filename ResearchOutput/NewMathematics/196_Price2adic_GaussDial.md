# Paper 196 — PRICE-2ADIC-LETTERS: The Price Tree's Alphabet Lives Where Berggren's Seal Doesn't Look

**Verdict name: PRICE-2ADIC-LETTERS-GAUSS-IS-RESIDUE-DIAL.**
Round-70 #5 · exp 548 · assessment v303 · script `ResearchOutput/scripts/2026-08-21-resume/exp548_price_gauss.py` (+ `exp548_result.json`, `exp548_run.log`) · seeds 20260823 + 3 replication seeds.

## 1. Construction validated before measurement

Brute force (gcd=1, opposite parity, c≤5000): **792 triples**; Price-tree BFS from
(2,1): **792 nodes, 0 duplicates/missing/extra** — uniqueness+completeness PASS.
Derived pair maps **A: (m,n)→(m+n,2n) [det+2], B: (2m,m−n) [det−2], C: (2m,m+n)
[det+2]**, cross-checked against the literature triple matrices (children of (3,4,5):
(5,12,13),(8,15,17),(7,24,25)); the brief's hinted matrix REFUTED ((3,4,5)→(6,6,14),
not Pythagorean). Descent termination 2000/2000; embedding m²−n²=N 2000/2000.

## 2. The dP law corrected

dP mean **24.52**, sd 2.65, range [16,34] — size-driven tightness CONFIRMED, but the
regression slope on log₂(p+q) is **1.211 CI95 [1.120, 1.301]: the circulating 1.4
constant is OUTSIDE the CI**; over-predicts by 3.12 steps mean (RMSE 3.87), R²=0.255
(no single size variable better). Contrast quantified: two population nodes take
**4566 and 7230 Berggren descent steps** against dP≤34.

## 3. The discovery: Price letters are 2-adically VISIBLE

Position-aligned Price↔Berggren letter agreement 0.3995 vs chance 0.3766 (z=+12.60,
effect +0.023 — tiny). Letter marginals at position 0: Price {A .48, B .05, C .47} vs
Berggren {L1 .91, L2 .04, L3 .05}.

The main finding: **Price letters at positions 0 AND 1 are massively determined by
N mod 4/8/16 — |z| up to 1303 at permutation nulls — while mod 2 is vacuous (N odd).**
The "binary/halving" alphabet lives exactly at the 2-adic place. Contrast: Berggren's
b₁ is 3-adically BLIND (worst cell z=+4.57 FAILED replication on 3 fresh seeds:
z=0.11/−0.14/+2.35 — seed fluctuation, null-at-3-adics stands; positive control
N mod 4 → Price-L0 z=+1698 proves the machinery sees real signal).

Placement: the 2-adic letter dials are RESIDUE dials — symmetric, factor-blind by the
standing no-pinning/utility laws (barriers 2/5). They extend the residue-dial map to
the second tree rather than escaping it: BOTH trees' cheap descriptions are sealed,
each at its own adic place.

## 4. GAUSS-DIAL-PROOF

Numeric quadratic Gauss sums vs closed forms: **0 mismatches on all 7625 (a,b,M)
cells** (M ∈ {3,4,5,7,8,9,11,13,16} + composites to 60), shift-invariance 1756/1756,
classical √p·|χ| magnitudes verified. Conclusion (pre-stated sentence, now proven):
*any factoring feature built solely from |G| magnitudes at fixed small moduli is a
pure function of N mod lcm = 720720 — a residue dial, already sealed.* Sharpenings:
on the standard lab range the whole feature vector is **literally constant** (all
factors coprime to 720720) → I(F;·)=0 bits where raw residues carry H=1.000 bit on
[p≡q mod 4] — a full 1-bit gap; DPI-equality holds exactly only when the label is
feature-measurable (verified non-degenerately on an odd-integer population).

Ledger (7 catches): hinted Price matrix refuted pre-use; wrong 2-power base case in
Gauss sums fixed by grid verification; descent guard aborted legitimately at 4566/7230
steps (raised); worst-cell breach resolved by fresh-seed non-replication; MI-equality
framing corrected (data processing); degenerate equality re-tested on an appropriate
population; dP deviation recorded. Barriers: 2/5/8 unchanged — strengthened.

Count line: 550 experiments (max id; exps 548–550 recorded together, out of id order).
Assessment v303.
