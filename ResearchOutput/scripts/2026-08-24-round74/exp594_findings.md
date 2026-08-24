# exp594 EDGE-KERNEL-CAP — paper-238 censored spike steepness → H0 (unidentifiable)

Pre-registration (H1 identified-spike / H0 cap-ladder) written in exp594_edge_cap.py header BEFORE fitting.
Data: 128 trials, hits pooled after per-trial normalization x=(p-jlo)/(jhi-jlo), n=9594; control pooled + subsampled to same n.
Model T(x)=A(1+x)^(-b_bulk)+K(1+x)^(-b_edge), cap delta on b_edge; geometric-binned Pearson chi2, multi-start NLS, AICc (k=1/3).

Treatment d_aicc vs single law (caps 10/20/40/80): -99.6 / -99.6 / -101.3 / -101.3 — kernel hugely retained at every cap; b_single=1.160 (paper ref ~1.10 replicated).
b_edge point per cap: 0.833* / 0.833* / 40.000 (=cap, interior=False) / 40.464.
  *caps 10/20 fall into a ROLE-SWAPPED optimum: b_bulk rides its own bound (~30) as the spike, b_edge absorbs the smooth part — within ~2 AICc of the edge-spike solution (second unidentified direction).
Bootstrap at best cap 80 (n=300): b_edge = 40.46, CI [15.2, 80.0], cap-hit frac 26.7%. Cap-40 boot (n=100): CI [14.8, 40.0], cap-hit 60%.
Control: NO kernel at any cap (d_aicc +4.85, edge weight ~8e-7, b_single~0.084 ~ uniform) — control prediction confirmed.

VERDICT: H0_SPIKE_STEEPNESS_UNIDENTIFIABLE. traj_ok False (pinned at cap 40); degeneracy NOT excluded (CI reaches cap at best cap); only exclusion that holds: b_edge != single-law 1.16.
Identified content = lower-bound ladder: b_edge >~ 15 at n~9.6k, robustly >> bulk; upper limit unbounded by data.
Consequence plainly: paper 238's edge kernel is REAL (delta-AICc > 90, absent in matched controls) but its registered cap delta=10 was a hard censor — the likelihood keeps climbing past every raised cap, so b_edge must be carried as a lower bound (>~15), never a point value. Posthoc 22.5 (paper) vs ~40 (here): estimator-dependent absolutes, identical censoring diagnosis.

Artifacts: exp594_edge_cap.py | exp594_smoke.log | exp594_full_run.log | exp594_result.json
