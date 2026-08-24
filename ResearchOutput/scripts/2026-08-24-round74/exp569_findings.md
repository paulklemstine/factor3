# exp569 U9-DRIFT-POWER (round-74)

VERDICT: RANDOMNESS-EXTENDED (pre-registered H0 branch). No gate triggered.

Band-9 (bitlen-96) independent-seed replication of paper 214's banked sub-1 drift:
- cut_1e6 secondary (best powered): r = 0.0005/0.000506 ≈ 0.99, cluster-boot
  CI95 [0.919, 1.010] over 128 clusters, 19.2M pairs — TIGHT, covers 1.
- cut_1e5 PRIMARY per pre-registration: r_cand stored as "0.0" by 4-dp rounding
  (DISPLAY DEFECT disclosed; true value CI-pinned to [2.66e-5, 3.56e-5] =
  CI x rate_ctrl 3.1e-5); ratio CI95 [0.8571, 1.1488], excludes_1 FALSE -> H0.
- POOLED WITH PAPER 214 PILOT: independent estimates at matched conditions
  (r@1e6: 0.947 [0.863,1.037] pilot vs 0.99 [0.919,1.010] here) are mutually
  consistent; joint point ~0.97. The sub-1 tension SOFTENS toward null -- the
  banked drift does not replicate downward at matched conditions. Residual
  tension status: downgraded from "banked" to "open at reduced weight"; a
  decisive test still needs the 10-30x power run (unreachable tonight --
  throughput-limited to ~1x pilot power at 76.4us/val).

Role honesty: this run is GATE G1 (fresh-seed replication) by pre-run reframe;
G2 control-integrity is satisfied by construction (paired bitlen+mantissa-head
matching; single tester code path both populations).

Ledger catches (coordinator-as-experimenter):
1. DISPLAY DEFECT: result JSON stores round(r,4) -> r~3e-5 prints as "0.0";
   raw hit counts NOT persisted (unrecoverable post-hoc). Script patched for
   any rerun; paper must cite CI-implied bounds, not the stored 0.0.
2. wall 1467s vs ~1104s estimate: candidate j^2-N strips slower than randoms.
3. Throughput reality: 76.4us/val => 10-30x-power goal unreachable in wall cap;
   role reframed PRE-RUN (scoping, not verdict-fitting) as documented in-script.

Files: exp569_u9_drift_power.py, exp569_smoke_result.json, exp569_result.json,
exp569_full.log. Inline coordinator implementation after agent-channel failures.
