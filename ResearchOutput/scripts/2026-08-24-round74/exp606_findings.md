# exp606 KAPPA-SUFFICIENCY-SCALE (round-74) -- findings

Questions (sharpening exp598c/paper-256's mechanism claim):
C1 REPLICATION: does composition order kappa_i = sum_k P(l_k|v_i) carry the
mixture increment on FRESH populations? C2 SUFFICIENCY: does CELL IDENTITY add
anything material beyond kappa? C3 SCALE: does the kappa law hold at bits
{72, 96, 128}?

PRE-REGISTRATION pinned in-repo BEFORE any full-mode number existed (commit
341af5a; amended through two adversarial pre-run audits that caught FOUR
must-fixes total: (i) stream bands colliding with 598c's own +17e6/+19e6 FULL
streams (~412/512 slots/leg -- identical PCG64 t-draws would have correlated
the replication); (ii) cross-leg collision from consecutive LEG_SEEDs sharing
offsets (default_rng(20261007+31e6+1) == default_rng(20261008+31e6+0)) --
fixed with a *1e8 per-leg stride + pairwise band-disjointness assert;
(iii) incomplete verdict tree (no above-bar/dirty-control branch, machinery_ok
gating nothing, lowpower suppressing nothing); (iv) vacuous-as-written C2
formula + undocumented third permutation in the recomputation recipe).
Registered aggregation rules (pre-data): C3 confirmed iff >=2/3 legs fire;
sufficiency confirmed iff all non-lowpower legs true, refuted iff >=2 false.

Legs: fresh seeds {96: 20261007, 72: 20261008, 128: 20261009} (registry-
verified unused), verbatim make_semiprime, n=512/leg, sizing-pilot ladder
(r_hat 1.48e-2 / 5.467e-2 / 2.703e-3 -> n_hit 50k / 50k / 150k), two
independent streams per N on stride-separated bands, gcd-chain primorial(1e6)
tester, perm seed 606 (500 reps, idx/idy/idc documented call order), pairs
bootstrap seed 607 (B=800). Walls 300 / 287 / 1202 s.

VERDICTS (per registered rules):
  C1 (bits=96 fresh): **H1_KAPPA_CARRIES** -- Delta_kappa = +0.0869,
     perm_p = 1/501 (zero of 500 kappa-row shuffles reach obs), clean control
     (ctrl null max 0.0204 << obs). Replicates 598c's mechanism claim on an
     independent population/stream complex.
  C3 SCALE: **CONFIRMED 3/3** -- H1_KAPPA_CARRIES at ALL THREE widths
     (+0.0869 / +0.0830 / +0.0585; perm_p = 1/501 each; all controls clean).
     The composition-order law is scale-stable across 72 -> 128 bits.
  SLOPE LAW: beta_kappa = -0.380 [-0.483,-0.279] / -0.349 [-0.456,-0.256] /
     -0.325 [-0.432,-0.217] -- NEGATIVE with mutually-overlapping CIs, mean
     -0.351. Richer small-prime composition depth <=> LOWER window smoothness
     rate, ~-0.35 log-rate units per unit expected-popcount, at EVERY scale.
     Sign expectation was pre-stated as NONE (never gated); the stability is
     the striking fact.
  C2 SUFFICIENCY: **MIXED** -- kappa_sufficient TRUE at bits=72 (+0.0071 < bar)
     and 96 (+0.0084), **FALSE at bits=128** (+0.0346 >= 0.02). And the b128
     failure is ITSELF permutation-supported: cells_shuffle_share_ge = 0.006
     (vs 0.226/0.218 at 72/96) -- almost NO cell-label shuffle reaches the
     observed cells-beyond-kappa increment there. At ~2^129-scale v (u~4.5,
     thin smoothness), WHICH small primes divide v starts carrying rate
     structure beyond HOW MANY -- the one-dimensional composition summary
     compresses away identity information that becomes load-bearing exactly
     where smoothness is rare.

MECHANISM PICTURE: papers 227/235/236 dials -> paper 256 cells ->
paper 257 refines to a GRADED LAW: log-rate ~ dial - 0.35*kappa (+ cell
identity only in the thin regime). Negative sign reads naturally once stated:
kappa counts expected DISTINCT small-prime hits of v; conditioning on more
small-prime content spreads the same divisibility mass thinner relative to
the full-1e6-smoothness requirement -- richer shallow structure associates
with poorer DEEP structure in this window.

VERIFICATION: independent from-scratch recompute of every headline stat for
all three legs from verify.npz alone -- permutation nulls replay BIT-EXACTLY
from the documented idx/idy/idc call order, perm_p = 1/501 EXACT everywhere,
verdict tree re-derives identically; hostile adjudicator confirmed chain of
custody (pin predates every artifact by birth times), stride fix necessary
AND sufficient (512 colliding slots demonstrated without it), crash recovery
clean, Bonferroni x3 survives, no overturn found.

LEDGER CATCHES: (1) b128 attempt 1 died in json.dumps on a raw np.bool_
(sufficiency short-circuit False case); fixed with an explicit bool() cast --
statistics-neutral (type-only), rides into this commit disclosed; attempt 1
left only a truncated result JSON, no other artifacts, determinism makes the
rerun bit-reproducible. (2) Docstring version-label drift (v2 text under the
v3 pin name) -- cosmetic, contents verified complete by the adjudicator.
(3) hits_mean b128 = 324/N (>= 300 target, no lowpower flag).

PROCESS LAWS EXERCISED: pin-before-run held (verified cryptographically by
git + filesystem forensics); pre-run audits caught both stream-collision
classes BEFORE any evidentiary byte was drawn.
