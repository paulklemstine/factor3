# exp567 SCALE-U9-LIFT — findings (2026-08-24, round 74)
**Status: PARTIAL/SHRUNKEN (disclosed).** An intermittent multiprocessing
throughput collapse at full geometry (root-caused via faulthandler SIGUSR1
dump: ready()-starved feed loop + slow completions) ate the 13-min runs.
Statistical weight rests on the completed PILOT (exp567_pilot_result.json:
bitlen 96, band 9, 35.7M cand+ctrl pairs, 24-N pool); three-band run shipped
at 45k pairs/band.
**Design (exp562-matched):** balanced semiprimes (gmpy2.next_prime, seed
20260824), bitlen {96,104,112} for u-bands {9,10,11}, v=(s+j)^2-N, j<=3s;
LPF-CDF cut ladder {500,1e3,1e4,1e5,1e6} via segment-primorial gcd chains,
BATCHED by product-tree remainder descent (12x: 87us->7us/value); exact
(bitlen,mantissa-octant) controls; per-N cluster bootstrap CIs; split-half.
**Achieved u:** band 9 [9.34,10.03] mean 9.89 (pilot); band 10 [10.64,10.94];
band 11 [11.44,11.74]. Half-notch gap (10.83,11) from grid geometry.
**r(u) @ primary 1e6 cut:** band 9 r=0.947 cluster-boot CI [0.863,1.037];
@1e5 r=0.864 CI [0.714,1.027]. Three-band: all CIs cover 1. B=500/1000 cuts
~zero events AS PRE-DECLARED (continuity carriers).
**Verdict: H1-consistent NULL — RANDOM-EXTENDS, no confirmed deviation.**
Points sit 5-14% BELOW 1 at both powered cuts, direction-consistent across
cuts, but every cluster-aware CI covers 1 and H2 gates never passed:
null-with-tension, NOT a deviation; replication unpowered at shipped sizes.
**Overdispersion localization: L1 RATE-THRESHOLD ARTIFACT.** At u=9.85 with
the healthy-rate 1e6 lens: D_cand=28.9 exposure-corrected (N=24, exposures
flat +/-0.14%) vs D_ctrl=1.85 — clustering ALIVE at u~10; exp562's D-death
(by u~7 at B=1000) was the indicator starving, not clustering dying.
Consistent with paper 136 QR-bite = per-N variance law.
**Ledger catches:** (1) mixed-segment reference bug gave 39/40 false tester
mismatches — batch strip exact vs exhaustive zero-early-exit reference (368
cases incl. deep-window quadratics); (2) backpressure once tripped the calib
watchdog falsely; (3) faulthandler.register re-raised SIGUSR1, killing my own
instrumented run; (4) throughput collapse shrank the headline run — disclosed.
**Barriers:** null strengthens COMPENSATING-PARTNER/no-pinning into the
Dickman leading-term zone; L1 upgrades variance-side accounting (variance
N-covariant, means matched). No barrier breached.
**Artifacts:** exp567_scale_u9_lift.py, exp567_result.json (three-band),
exp567_pilot_result.json (powered leg), exp567_{pilot,full,smoke}.log,
exp567_stderr.txt (faulthandler dump). Not committed.
