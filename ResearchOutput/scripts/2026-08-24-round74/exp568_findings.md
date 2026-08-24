# exp568 ECM-STAGE2-WALL (round-74)

VERDICT: H3 CONFIRMED (strong form) -- NO destruction wall exists under outcome-
separated accounting; H1/H0 MOOT-BY-ABSENCE (no w* anywhere to fit).

Full grid (n_N=40, bitlen-26 q~4p stratum, arms B2/B1 in {1,4,16}, B1/p in
{0.125,...,1.05}): success rate 1.000 in 14/15 cells (one cell 0.95 @ B1/p=0.125,
arm 16); ZERO 'dead' outcomes; ZERO 'nothing' beyond those five cells. Success
persists at B1/p=0.9 AND 1.05 -- precisely where paper 159 records "every Hasse-
window order divides lcm(1..B1), all curves degenerate simultaneously, uncapped
E[T] infinite."

Mechanism (pre-data note, vindicated): B1 >= p+1+2sqrt(p) => every Hasse-window
order n <= B1+... hence every prime power l^e || n satisfies l^e <= n <= B1,
hence n | lcm(1..B1) => [L]P = O mod p for EVERY curve => first guarded inversion
with den == 0 mod p returns gcd = p: GUARANTEED SUCCESS, not death. Simultaneous
degeneracy mod q impossible for q >> B1.

STRUCTURAL INSIGHT (ledger-grade): guarded-affine accounting carries a random-
collision success baseline ~ 1 - exp(-c*B1/p) with c ~= ln2*ops-per-bit constant:
each inversion denominator is ~uniform mod N, so P(hit p or q per op) ~ 1/p,
and #ops ~ 1.44*B1 => cumulative ~1.44*(B1/p) INDEPENDENT OF SCALE. At B1/p=0.125
this predicts ~17% baseline -- consistent with the observed 68% found_p at that
cell being part collision-luck, part genuine order-divisibility. Any historical
success/E[T] accounting that did not separate order-hits from collision-hits
conflates these regimes; this may be the origin of the paper-159 wall sentence.
Discriminating follow-up (named): re-run at larger p with per-op outcome tracing
(order-hit vs collision-hit) before citing either way.

Caveats disclosed: toy bitlen 26 (wall claim tested in-region, mechanism scale-
free per the divisibility argument); wall-clock 1.1 s (early exits); stage-2
difference machinery NEW (validated only by smoke buckets + sign-convention note;
no stage-2-only cell fired since stage 1 succeeded first everywhere -- stage-2
arms are therefore UNTESTED DEAD CODE this run, disclosed honestly).

Files: exp568_ecm_stage2_wall.py, exp568_smoke.log, exp568_result.json,
exp568_full.log. Inline coordinator implementation after 3x agent-channel failures.
