# Paper 215 — ECM-STAGE2-WALL: The Recorded Destruction Wall Does Not Exist Under Outcome-Separated Accounting — B1 ≥ p+1+2√p Makes Every Curve Succeed, Not Die (Self-Audit of Paper 159's Headline Sentence)

**Verdict name: H3 CONFIRMED (strong form)** — zero `dead` outcomes in all 600 trials
across the full grid; success is 1.000 in every cell at B1/p ≥ 0.25 and **persists at
B1/p = 0.9 and 1.05** — precisely where paper 159 records *"every Hasse-window order
divides lcm(1..B1), all curves degenerate simultaneously, uncapped E[T] infinite."*
H1/H0 are moot-by-absence: no w* exists anywhere in the grid to fit a slope to.
Round-74 #6 · exp 568 · assessment v322 · script `exp568_ecm_stage2_wall.py` (+ smoke/full logs, result JSON) · seed 20260824 · wall 1.1 s (guarded early exits).

## Question

Paper 159 (FACTOR-LOCAL-ET FULL) headlines an **ECM self-destruction wall**: *when
B1 ≳ min(p,q), every Hasse-window order divides lcm(1..B1), all curves degenerate
simultaneously, and uncapped E[T] is infinite*, with the honest object declared behind
a validity edge B1 ≲ min(p,q)/2. Exp568 asks whether that boundary is a BUDGET law,
an INTRINSIC death — or not a method boundary at all but an ACCOUNTING boundary.

## Pre-registered hypotheses (verbatim, before any data)

- **H1 budget law:** "log w\* vs log(B2/B1) slope CI covers 1 ⇒ wall scales with
  stage-2 coverage; the edge converts to a finite scaling boundary."
- **H0 intrinsic:** "slope CI covers 0 ⇒ wall pinned regardless of downstream width."
- "neither → MIXED." Definition: "w\* = smallest B1/p with success rate < 10% of the
  arm's plateau (success = factor recovered within C=3 curves, stage1+stage2)."
- **H3 (timing disclosed):** "ADDED after reading paper 159's mechanism sentence,
  BEFORE any data": the wall's "all curves degenerate" outcome is a
  DETECTION/ACCOUNTING artifact — specifically gcd(den,N)==N (`dead`) events or
  missing p-vs-q separation — not genuine method failure; with outcome-separated
  accounting ({found_p, found_q, dead, nothing}) success at B1 ≥ min(p,q) is monotone
  in B1 and no collapse exists at any arm. H3 TRUE amends paper 159's headline
  sentence's scope (lite-construction or accounting-specific).
- **Mechanism note driving H3 (recorded pre-data, vindicated below):** if
  B1 ≥ p+1+2√p then EVERY Hasse-window order n satisfies n ≤ B1, hence n | lcm(1..B1)
  (each prime power l^e ‖ n has l^e ≤ n ≤ B1). Then [L]P = O mod p for EVERY curve,
  and the FIRST guarded inversion whose denominator vanishes mod p returns gcd = p —
  **guaranteed success, not death**. Simultaneous infinity mod q needs
  ord(Q mod q) | L too, impossible for q ≫ B1.

## Design

One q ≫ p semiprime stratum (generator: p = nextprime(13-bit odd seed),
q = nextprime(3p + U[1,200)), N ≈ bitlen 26; hi/lo kept within 3 bit-lengths),
n_N = 40 per cell. Grid: B1/p ∈ {1/8, 1/4, 1/2, 0.9, 1.05} (ceil/floor as coded,
floor B1 = 20) × arms B2/B1 ∈ {1 (control: must reproduce the lite/lcm wall
signature), 4, 16}. Machinery: exp488_true_ecm.py's **guarded affine EC ops reused
VERBATIM** (validated there by ladder-vs-affine 10/10 + mod-12 signature 100/100);
true-lcm stage-1 schedule (exp488 prime_power_schedule); NEW true difference-stage
stage-2 (baby V_d = [d]Q for d primes ≤ 97, giant W_i = [iD]Q, denominators batched
into gcd(acc, N) every 256 adds, guarded statuses checked immediately). Accounting is
outcome-separated per trial: {s1_found_p, s1_found_q, s2_*, found_other_gcd, dead,
nothing}.

## Result 1 — the full grid: no wall anywhere

| B1/p | arm B2=B1 | arm 4·B1 | arm 16·B1 |
|---|---|---|---|
| 0.125 | **1.000** | 0.875 (4 nothing, 1 other-gcd) | 0.95 (2 nothing) |
| 0.25 | 1.000 | 1.000 | 1.000 |
| 0.5 | 1.000 | 1.000 | 1.000 |
| 0.9 | **1.000** | **1.000** | **1.000** |
| 1.05 | **1.000** | **1.000** | **1.000** |

(n_N = 40/cell; 600 trials total.) **Zero `dead` outcomes in the entire grid.**
The only sub-1.000 cells sit at the LOWEST edge B1/p = 0.125 — opposite the wall
region — and their misses are `nothing` (budget exhausted), never `dead`. Success is
monotone non-decreasing in B1 in every arm and saturates at 1.000 by B1/p = 0.25.
Every success in every cell is a stage-1 find (s1_found_p/s1_found_q; e.g. at
B1/p = 1.05, arm 1: 29 found-p / 11 found-q — the p-vs-q separation paper 159's
accounting may have lacked works fine here).

**The wall region is exactly where success is perfect.** Paper 159's "uncapped E[T]
infinite" sentence describes B1/p ∈ {0.9, 1.05}: exp568 measures 6/6 cells at 1.000
with zero degeneracy. **H3 confirmed in its strong form; H1/H0 moot-by-absence** — no
cell ever falls below 10% of plateau, so w\* is undefined and the slope test never
arms.

## Result 2 — the mechanism: divisibility converts "degeneracy" into a certificate

The pre-data mechanism note is vindicated verbatim. At B1 ≥ p+1+2√p (true at
B1/p = 1.05 for these p, and effectively approached at 0.9), every Hasse order
n ∈ [p+1−2√p, p+1+2√p] obeys n ≤ B1, hence n divides lcm(1..B1), hence [L]P ≡ O
(mod p) on EVERY curve. A curve "degenerating" mod p is not a failure of the method —
it is the method succeeding with certainty, and the guarded-inversion implementation
detects it as gcd = p on the first vanishing denominator. "All curves degenerate
simultaneously" is therefore mathematically a **success guarantee**, and can only have
been read as death if the detector conflated gcd = p (win) with gcd = N (loss) — i.e.
if it lacked the p-vs-q outcome separation. Simultaneous degeneracy mod q is
impossible for q ≫ B1, so the separated detector cannot even lose both ways.

## Result 3 — STRUCTURAL INSIGHT: the collision baseline any accounting must separate

Guarded-affine accounting carries a **random-collision success baseline** independent
of scale: each inversion denominator is ~uniform mod N, so P(hit p or q per op) ≈ 1/p;
the lcm schedule costs ~1.44·B1 ops; cumulative hit chance ≈ 1 − exp(−c·B1/p) with
c ≈ ln 2 · ops-per-bit constant — a function of the RATIO alone. At B1/p = 0.125 this
predicts a ~17% baseline, consistent with the observed 68% found-p share at that cell
being part collision-luck, part genuine order-divisibility. Any historical
success/E[T] accounting that did not separate order-hits from collision-hits conflates
these regimes; **this is the leading candidate origin of the paper-159 wall sentence**
(the alternative — a genuine lite-construction artifact — is not excluded by this toy
run). Discriminating follow-up, named: re-run at larger p with per-op outcome tracing
(order-hit vs collision-hit) before citing either way.

## Caveats (disclosed prominently)

1. **Stage-2 arms are UNTESTED DEAD CODE this run.** Stage 1 succeeded first in every
   successful trial; the B2/B1 arm dimension exercised only inside the 7 failed
   trials (all at B1/p = 0.125) and never rescued one — zero s2_\* outcomes exist in
   the result JSON. The NEW difference-stage machinery is validated only by smoke
   buckets + sign-convention note. The arm dimension consequently carries no signal:
   cross-arm differences at fixed B1 (1.000 vs 0.875 vs 0.95 at 0.125) are per-cell
   RNG drift in curve draws, not B2 effects. The stage-2 question of H1/H0 remains
   genuinely open and would need a design that suppresses stage 1.
2. **Toy bitlen 26.** The wall claim is tested in-region; the divisibility mechanism
   argument is scale-free, but the collision-baseline constant c is measured at one
   scale only.
3. **Inline coordinator implementation** after 3× agent-channel failures (stall
   watchdog ×2, silent no-write ×1); core EC machinery reused VERBATIM from
   exp488_true_ecm.py.
4. **Ledger catch on the summary layer (recorder):** exp568_findings.md states
   "success 1.000 in 14/15 cells (one cell 0.95)"; the canonical result JSON shows
   TWO sub-1.000 cells (0.875 arm-4 and 0.95 arm-16, both at B1/p = 0.125). Verdict
   unaffected — both sit at the low-B1 edge with zero `dead` — but the JSON is
   canonical and this paper's table follows it.

## Barrier validation

Barrier-8 adjacency (measuring known methods knowingly) — this is a **self-audit** of
a recorded headline, genre precedent: paper 91 stands / paper 99's retraction handled
by side-by-side reconstruction. No new method proposed, no barrier crossed, no
constant shaved. If the named larger-p follow-up confirms, paper 159's wall sentence
receives an **amendment, not a silent rewrite**; until then paper 159 stands as
recorded with this audit appended.

## Conclusion

Under outcome-separated accounting {found_p, found_q, dead, nothing}, the ECM
destruction wall of paper 159 does not exist in the measured region: success is
monotone in B1, perfect at B1/p ≥ 0.25, and exactly 1.000 at B1/p = 0.9 and 1.05
where the record claims uncapped E[T]. The Hasse-window divisibility argument (pre-
registered, vindicated) shows why: B1 ≥ p+1+2√p forces [L]P = O mod p on every curve,
turning "simultaneous degeneracy" into a guaranteed gcd = p win. Any accounting that
could have called this death must have conflated collision-hits with order-hits; the
collision baseline 1 − exp(−c·B1/p) is now on the ledger as what any future ECM
accounting must separate. Now 558 experiments (max id 568). Assessment v322.
