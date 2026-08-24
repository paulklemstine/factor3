# Paper 211 — ORBIT-DIAL-CAP-TEST: The Mod-N Orbit's Revealed Residue Set Carries Zero Factor Information, and Its Cap-Beating Read Is a Blind Parity Skip

**Verdict name: CAP-EXCEEDED-BY-UNIVERSAL-EXCLUSION-DIAL** (H1 confirmed with one scope refinement; pre-registered verdict rules evaluated verbatim).
Round-74 #2 · exp 564 · assessment v318 · script `exp564_orbit_dial.py` (+ smoke/full logs + JSON) · seed 20260824 · wall 76.4 s (cap 20 min) · population n = 800 bitlen-40 semiprimes (500 balanced / 300 ratio-4; bitlens 39–41; train half 383 / test half 417), moduli m ∈ {3, 4, 5, 7, 8, 16}, 12 units/node, 300 shuffles, 800 bootstrap, permutation nulls stratified by logN decile.

The third and final open face of the Berggren triplet-tree campaign: exp555 (paper 205)
measured the mod-N Berggren orbit as collision-free and class-confined but
**under-sampling** — its revealed-residue set visits only a subset of classes per modulus.
The standing question: does WHICH subset varies with N carry per-N factor information, and
if used as a candidate filter (keep only candidates in revealed classes), does the dial
beat the residue cap 4/3 (barrier 4)? Two arms: the exp555 ROOT component (Berggren tree
from the canonical seed) and GENERIC components (random Pythagorean seed points mod N,
expanded with identical child maps).

**Pre-registered hypotheses (verbatim):**
- **H1:** "orbit revealed-set MI fully accounted for by ordinary residue-dial content;
  measured speedup <= 4/3 within CI; = matched-random dial (barrier-4 converse scope)"
- **H2:** "speedup significantly > 4/3 surviving fresh-seed replication + sham
  co-inflation + N-computability check"

## Design amendments — disclosed before the full run (result `honest_notes`)

1. **The root component's task premise FAILS at toy scale.** The exp555 root BFS never
   wraps mod N at bitlen-40 budgets: depth ≈ 9, coordinates ~10⁴ ≪ N ~10¹², so the
   revealed set is **N-INVARIANT across all 800 N at every one of the six moduli**
   (distinct values across population = 1, modal share = 1.0). There is no
   N-dependent subset to test for information; the root arm is retained as a
   characterization arm only.
2. **The live H1/H2 test therefore runs on generic components**: 10 random Pythagorean
   seeds × 1500 nodes each, reduced mod N — these wrap immediately and give genuinely
   N-dependent revealed sets. Characterization result: supports **saturate instantly**
   — exactly m classes present at every modulus (sa-classes mean = min = max = m for
   m = 3..16), component length uniform (min = max = 15 010); all variation lives in
   frequencies/orbit-length, none in support. Budget-saturation check on the root arm:
   q50 = 5 of 5 classes @ m = 5, 8 of 16 @ m = 16 — the under-sampling exp555 saw is a
   FIXED structural truncation, not an N-dependent one.

## Result 1 — zero per-N factor information (H1 information clause CONFIRMED)

Full-population MI table over 48 cells (features sa/sabc/topshare/saE/complen × moduli ×
sources), logN-decile-stratified permutation nulls: **max |z| joint = +2.29**
(topshare@16, MI 0.092 bits vs joint), **max |z| conditional = +1.78**, every feature MI
≤ 0.09 bits against ordinary residue-dial baselines I(N mod m; p mod m) = **1.00–3.00
bits**. Train-half selection found nothing that survived (selected cell falls back to the
root sa@4 table with train |z| = null; universal-table train share = 1.0 → the selected
cell is itself N-invariant). Nothing beyond ordinary residue content — the orbit joins
the closed residue-dial family.

## Result 2 — the filter law holds, and ORBIT = UNIV exactly

Filter test at θ = ½ on sqrt-descending trial division, paper-132 law accounting
(miss → flat T₀ fallback):

| Arm | gross speedup [95% CI] | failure rate | net-loaded |
|---|---|---|---|
| RAND-MATCH | **1.3387** [1.3008, 1.382] | 0.516 | 0.317 |
| SHAM | 1.3142 [1.2717, 1.3579] | 0.540 | 0.541 |
| ORBIT | 2.0000 [2.0, 2.0] | **0.000** | 0.753 |
| UNIV (fixed parity dial) | 2.0000 [2.0, 2.0] | 0.000 | 0.753 |
| CRT-AND | 2.0000 [2.0, 2.0] | 0.000 | 0.753 |
| ORBIT-COMP (sanity) | 1.0000 | 1.000 | 0.204 |

- **Cap-law check: confirmed to ~0.4%.** RAND-MATCH reads 1.3387 vs prediction 4/3 =
  1.3333 (CI brackets it); SHAM co-inflation control clean (CI also brackets 4/3;
  ORBIT − SHAM gross gap = 0.686 is the deterministic-exclusion margin, not inflation).
- **ORBIT beats 4/3 ONLY as the parity skip.** The paired z of ORBIT vs UNIV is **0.0
  EXACTLY** — on every single N the orbit-derived exclusion table coincides with the
  fixed universal dial: the root-orbit legs are always odd, so excluding even classes
  never drops an odd factor p (failure rate 0.000). It is an N-invariant universal
  exclusion table computable blind from N alone, with zero per-N information — hence a
  constant-shave, **NOT a barrier event**. Paired z vs RAND-MATCH = +29.2 (the
  determinism gap, not an information gap).
- **Every arm NET-loaded < 1** (0.20–0.75): build cost at 12 units/node plus membership
  testing exceeds scan savings — paper 131's lesson replicated yet again. Replication
  gate not triggered (H2 gate false).

## Scope note for barrier 4 (new, stated in the paper)

The residues-cap-4/3 theorem presumes **P(p kept) = θ exchangeability** between keep
probability and kept fraction. A *deterministic* exclusion escapes via P(p kept) = 1
while keeping only half the candidates: an N-invariant structural dial can exceed 4/3
without carrying any information. The cap law bounds INFORMATION-BEARING dials;
blind structural exclusions sit outside its premises and are worth exactly their
constant factor — here 2×, already available as plain odd-candidate sieving.

## Barrier map validation

#2 consistent (orbit features p↔q-symmetric, no signal either way). #4 UPHELD with the
scope note above — no information-bearing dial beats the cap. #5 EXTENDED: position
orthogonality now covers mod-N orbit projections (support saturation ⇒ no positional
content beyond frequencies). #6 restated: the orbit's structure IS primitive-triple
congruences — the "under-sampled classes" are congruence shadows, restating rather than
evading circularity. #8 unchanged. **N-computability audit: recompute-identical 3/3 on
both arms** (start consts + linear maps + reduction mod N; component RNG keyed by
(SEED, N); no factor in any code path).

## Ledger

Three catches, all fixed BEFORE the full run, none adverse after: empty-walk BFS bug
(children never enqueued — caught by the timing probe), odd-multiplier population-split
bug (empty train half), g-unbound ×2. Runtime 76.4 s.

## Conclusion — campaign CLOSED

This closes the THIRD face of the user's Berggren triplet-tree proposal ("mod-N orbit
residue under-sampling", opened by exp555/paper 205): the under-sampling is real but
N-invariant at toy scale, saturates generically, and carries zero factor information.
With paper 199 (two-tree closure synthesis of the four-strength seal, papers 192–197),
paper 205 (modular dynamics), and paper 210 (oracle bound unrealized), **ALL faces of
the triplet-tree proposal are now measured** — every proposed channel (node identity,
coordinates, adic position, energy ascent, modular dynamics, oracle navigation, orbit
residues) terminates in a null or a restatement of known residue/parity structure. No
breakthrough; the campaign closes honestly. Now 554 experiments (max id 565).
Assessment v318.
