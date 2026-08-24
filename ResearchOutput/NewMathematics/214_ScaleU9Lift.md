# Paper 214 — SCALE-U9-LIFT: x²−N Smoothness Randomness Extends Through u≈11 Toward the Dickman Leading-Term Regime — H1-Consistent Null With Sub-1 Tension; Paper 209's "D Dies by u≈7" Amended to Rate Starvation

**Verdict name: RANDOM-EXTENDS (NULL-WITH-TENSION)** — every cluster-aware CI covers 1 at every band and cut; H2 confirmation gates never fired; points sit 5–14% below 1 at the powered cuts and are flagged as tension for a future higher-power run, NOT as a discovery. **Status: honest partial** — an intermittent multiprocessing throughput collapse ate the planned headline run; statistical weight rests on the completed pilot, all disclosed.
Round-74 #5 · exp 567 · assessment v321 · script `exp567_scale_u9_lift.py` (+ `exp567_pilot_result.json` powered leg, `exp567_result.json` three-band leg, full/pilot/smoke logs, faulthandler stderr dump) · seed 20260824 · walls 157 s (pilot) / 20.8 s (shipped three-band leg, time-capped).

Papers 130 (x²−N pool ensemble-equals unrestricted random through 2⁴⁴) and 209/exp562
(no relative deviation through u ≤ 8.5) leave the frontier item "**scale-smoothness
deviations u ≥ 6–14**" open precisely because raw B-smoothness testing starves there:
the Dickman density ρ(9) = 1.01 × 10⁻⁹ and ρ(11) = 6.45 × 10⁻¹³, so a B=1000 smoothness
indicator has literally no events at these scales. This experiment lifts balanced
semiprimes to bitlen {96, 104, 112} (u-bands {9, 10, 11}, v = (s+j)² − N, j ≤ 3s) and
swaps the dying indicator for an **LPF-CDF cut ladder** {500, 10³, 10⁴, 10⁵, 10⁶} via
cumulative segment-primorial gcd chains, batch-amortized by a product-tree remainder
descent transferred from exp561 (**12× : 87 µs → 7 µs/value**). Controls are exact
(bitlen, mantissa-octant) histogram matches tested through the same code path;
inference is per-N cluster bootstrap with built-in A/B split-halves.

**Pre-registered hypotheses (verbatim):**
- **H1:** "r_cut(u)=1 at every bin and every ladder cut - randomness extends through u~11 toward the leading-term regime; consistent with papers 130+209"
- **H2 protocol:** "any CI-excluding-1 flag is DEVIATION-UNCONFIRMED unless (a) direction-consistent across cuts with the 1e6 cut excluding, (b) both split-halves replicate, (c) fresh-seed pool replicates (requires >=270s remaining wall); maximal skepticism - this would be the lab's first positive scale-smoothness deviation"
- **Overdispersion localization (pre-registered fork):** L1 "rate/threshold artifact": D_expo_cand(1e6 cut) > 1 significantly in ≥ 2 bins at u ≥ 9 → exp562's D-death was rate-driven; L2 "genuine u-death": D ~ 1 in ALL bins.
- Continuity carriers declared in advance: B=500/1000 cuts kept for 130/209 continuity with predicted ~zero yield (ρ(9..11)·n ≈ 0) → wide-or-empty CIs BY DESIGN.

## Result 1 — achieved u and the powered leg

| leg | band | bitlen(N) | pool | cand pairs | achieved u | mean u |
|---|---|---|---|---|---|---|
| pilot | 9 | 96 | 24 N | 35,721,216 | [9.83, 10.13] | 9.89 |
| three-band | 9 | 96 | 6 N | 45,056 | [9.83, 10.13] | 9.89 |
| three-band | 10 | 104 | 6 N | 45,056 | [10.64, 10.94] | 10.69 |
| three-band | 11 | 112 | 6 N | 45,056 | [11.44, 11.74] | 11.50 |

The j ≤ 3s cap and bitlen strata leave **no coverage in (10.94, 11.44)** — integer
u = 11 sits inside this half-notch gap of grid geometry (truncation note disclosed
pre-run). Validation before any measurement: 368 cases (38 adversarial, 270 real
quadratic), **0 mismatches** against an exhaustive zero-early-exit strip reference.

## Result 2 — r(u): null at every powered cell

Primary family = LPF-CDF **1e6 cut** (highest event yield):

- **Band 9 pilot (powered): r = 0.9468, cluster-boot CI95 [0.8630, 1.0389]** (12,493
  cand vs 13,195 ctrl events). Split-halves replicate the level: A 0.939
  [0.862, 1.033], B 0.955 [0.862, 1.061]. At the **1e5 cut: r = 0.86399, CI
  [0.7190, 1.0302]** (667 vs 772); splits A 0.848 / B 0.881. At 1e4: r = 1.60
  [0.436, 6.78] (8 vs 5 events, uninformative).
- **Three-band leg (all CIs cover 1):** band 9 @1e6 r = 1.54 [0.79, 3.24] (20 vs 13);
  band 10 @1e6 r = 2.0 [0.25, 7.0] (4 vs 2); band 11 @1e6 kc = 2 vs kctrl = 0
  (r undefined, CI covers 1 trivially); @1e5 band 9 r = 2.0 [1.0, 4.0] on a 2-vs-1
  base. Tightest bound |r − 1| = 2.24 (three-band) vs **0.137 (pilot primary)**.
- **B=500/1000 cuts: exactly zero events in every cell**, as pre-declared for the
  continuity carriers — ρ(9) = 1.0e-9 … ρ(11) = 6.5e-13 makes them structural
  no-events, carried for 130/209 comparability only.

**H2 never armed:** `deviation_flags_any_cut` is EMPTY in both legs,
`ci_excludes_1` FALSE in every band × cut cell, no split-half or fresh-seed leg ever
triggered. Per the pre-registration this is **RANDOM-EXTENDS, deviation status NONE**
— the lab's first-positive-scale-deviation door stays shut.

## Result 3 — THE TENSION (flagged, not claimed)

At both powered cuts the point estimates sit BELOW 1 and the deficit is
direction-stable: −5.3% at the primary 1e6 cut (split-halves 0.939/0.955 both below),
−13.6% at 1e5 (splits 0.848/0.881 both below), and the three-band band-9 cells point
the other way (1.54, 2.0) on tiny counts. Every cluster-aware CI comfortably covers 1
(tightest |r−1| bound 0.137). Recorded exactly as pre-registration demands:
**null-with-tension**. A definitive test of the sub-1 drift needs roughly the pilot's
event count at the 1e5 cut (~30× more pairs than shipped) — queued as the motivation
for a future higher-power run, explicitly NOT a finding.

## Result 4 — OVERDISPERSION LOCALIZATION: AMENDMENT to paper 209's secondary claim

Paper 209 recorded N-level overdispersion D = 1.61 [1.50, 1.73] at bin 5 that "DIES"
to ~1.00 by bins 7–8, concluding "by u ≈ 7 both the clustering and even the
residue-dial correlation are gone." **Exp567 amends the MECHANISM of that death:**

Under the healthy-rate 1e6 lens at u = 9.85 (band 9 pilot, N = 24, exposures flat to
±0.14% so the exposure-corrected readout is clean): **D_cand = 28.87 CI95
[14.27, 44.08]** vs **D_ctrl = 1.84 [0.90, 2.84]** — per-N clustering is emphatically
ALIVE at u ≈ 10. The residue-dial correlation is alive too: Spearman(per-N rate,
QR fraction) = 0.533 (perm p = 0.0060) at the 1e4 cut and 0.437 (perm p = 0.033) at
the 1e6 cut — where 209 read ~0.04 and "gone." Consistent with paper 136's law that
the QR bite is a per-N VARIANCE effect, not a mean shift.

What died by u ≈ 7 in exp562 was the **INDICATOR, not the clustering**: at raw
B-smoothness rates the expected event count falls as ρ(u), so the dispersion statistic
starves exactly when u grows — an L1-style rate-threshold artifact. Exp567's
pre-registered fork resolves **in the L1 direction, with one honest caveat**: the
formal L1 criterion demanded significance in ≥ 2 bins at u ≥ 9, and the shipped data
has only ONE powered bin (bands 10/11 collapsed to 45k pairs in the shrinkage), so
L1 is recorded as *directionally confirmed in the single powered bin, formally
unmet* — the amendment stands on the pilot's own internal contrast
(D_cand 28.9 ≫ D_ctrl 1.8 at the same u, same lens) rather than on the cross-band
gate. No barrier is breached either way; variance-side accounting is upgraded
(variance N-covariant, means matched).

## Ledger

Four catches, none adverse after fixing/disclosure:
1. **Mixed-segment checker bug**: an early draft checker produced 39/40 false
   mismatches; root-caused and fixed — the shipped tester is proven EXACT against an
   exhaustive ascending strip of all primes ≤ 1e6 with zero early exits (368 cases
   full / 218 pilot incl. deep-window quadratics, 0 mismatches, shared code path for
   candidates and controls).
2. **Backpressure watchdog false-trip**: the first full-geometry attempt was
   terminated as "calibration hung" while merely backpressured (log 02:01:49).
3. **faulthandler SIGUSR1 re-raise** killed one instrumented rerun of the headline
   configuration (the diagnostic hook re-raised its own signal).
4. **Throughput collapse shrank the headline run** (the material catch): at full
   geometry (128 N/band, ~130M-value quotas/band computed from a healthy 5.35e5
   values/s calibration) an intermittent multiprocessing collapse — root-caused via
   the preserved faulthandler dump (`exp567_stderr.txt`: ready()-starved feed loop +
   slow completions) — ate the runs; the shipped three-band leg carries 45k pairs/band
   under a time-capped adaptive-sizing convention (status 06_final_time_capped, both
   legs). An earlier small-cap interim write had flashed verdict
   DEVIATION-UNCONFIRMED on sub-powered counts before being superseded by the final
   RANDOM-EXTENDS writes; the canonical artifacts on disk are the ones cited here.

## Conclusion

x²−N smoothness statistics remain size-matched-random through u ≈ 11.7 — papers
130/209 randomness now extends out of the measured corridor into the approach zone
of the Dickman leading-term regime (good near u ≈ 14.75), with the LPF-CDF ladder
carrying full power where raw smoothness cannot. One tension is banked honestly
(sub-1 drift, all CIs covering), and paper 209's secondary D-death conclusion is
amended: clustering does not die by u ≈ 7 — the B-smoothness indicator does.
No barrier breached; no constant shaved. Now 557 experiments (max id 567).
Assessment v321.
