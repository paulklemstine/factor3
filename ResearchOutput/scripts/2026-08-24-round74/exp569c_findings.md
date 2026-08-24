# exp569c U9-DRIFT-GATE (round-76 #2) — fresh-seed arbiter, seed 20260825

VERDICT: GATE REJECTED — the candidate sub-1 deviation signal is DEAD.
Randomness stands; the night's tension resolves as measured seed-fluctuation.

Run facts: wall 5296.9 s, 76.8M pairs, band-9 bitlen-96, seed 20260825
(the ONLY seed-20260824-uncontaminated run of the series — pilot/G1/B all
shared 20260824; see paper 220's ledger).

Results (full precision from persisted raw counts):
- cut_1e5 PRIMARY: 2598/76.8M vs ctrl 2252/76.8M => r = 1.1536,
  independent cluster-boot CI95 [1.0540, 1.2611] — EXCLUDES 1 UPWARD.
- cut_1e6: r = 1.0524, CI95 [1.0051, 1.1016] — excludes 1 upward.
- SIGN FLIP vs the correlated family: pilot/G1/B read r ≈ 0.95–0.99
  (deficit); the clean seed reads SURPLUS. Directional instability across
  seeds = no stable deviation. Gate G1 fails by sign, not just magnitude.

AUDIT TRAIL (both pre-disposition alarms resolved):
1. Coordinator false alarm: stored r looked "outside its own CI" — caused by
   coordinator's :.5f TERMINAL formatting collapsing 3.38e-05 to 0.00003;
   raw counts recompute cleanly, point sits inside its CI. Display artifact,
   no script defect (precision patch had worked).
2. Independent 4000-replicate bootstrap from raw counts reproduces stored
   CI to 3 decimals ([1.0540,1.2611] vs [1.0541,1.2686] — percentile
   ordering noise only).
3. Cluster structure: top candidate-N clusters carry 600/561/540 hits vs
   control-max 359 — genuine per-N overdispersion, the mechanism behind
   ±5–15% single-run CI widths. Any single run at this power simply cannot
   resolve a few-percent effect; the b/c contrast measures that scale
   directly.

FINAL SYNTHESIS for the u≈10 question (papers 214→216→220→this):
- No deviation survives: the once-banked sub-1 drift fails its fresh-seed
  gate by SIGN FLIP; the correlated-family deficit is explained by seed-
  shared fluctuation; the clean seed shows an equally-sized surplus.
- Randomness picture STRENGTHENED: papers 130/209/214/216 null line now
  extends through u≈11 with a MEASURED per-run fluctuation envelope
  (roughly ±5–15% at these powers) that any future deviation claim must
  beat by a wide margin — i.e., multi-seed pooling with the new lab-wide
  seed-distinctness rule, not single-run CIs.
- Named follow-up (only if anyone reopens): ≥3 truly distinct seeds pooled
  inverse-variance (sigma_joint ~0.02 achievable) — but the burden of proof
  now includes explaining why seed-a/b saw deficit and seed-c surplus.

Ledger catches: coordinator display-formatting false alarm (above);
pkill self-match killed the first c_-launch (relaunch clean, documented);
seed-parameterization added to script post-correlation-catch (committed
with exp569b artifacts, reused here).

Files: exp569_u9_drift_power.py (patched, seed-parametrized),
exp569_c_result.json (canonical, raw counts persisted), exp569c_full.log.
