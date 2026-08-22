# Paper 159 — FACTOR-LOCAL-ET FULL: The Plane Measured — and ECM's Validity Edge

**Verdict name: PLANE-MEASURED-ECM-WALL.**
Round-42 #5 (cron iteration) · exp 486-full · assessment v268 · script `ResearchOutput/scripts/2026-08-21-resume/exp486_full_plane.py` (+ `exp486_full_result.json`) · seed 20260920.

## 1. The full version of paper 154's plane

Bootstrap-CI pooled fits over 6000 draws/arm (bitlen 16/20/24 × balanced/uniform), exact
op-count conventions fixed a priori, every returned factor verified a proper divisor.

## 2. Results

| method–arm | α [95% CI] | reading |
|---|---|---|
| trial division (both arms) | **1.0009 [1.000, 1.002]** | exact |
| Pollard ρ (balanced) | **0.4994 [0.485, 0.510]** | birthday bound to three decimals |
| Fermat (uniform) | **0.9932 [0.992, 0.994]** | the exact p/2 law |
| Fermat (balanced) | 0.734 — non-invariant as predicted; balance explains residuals at r = +0.966 | gap-locality |
| ECM (B1 ∈ {50,100,500}) | **−0.86 to +0.04 across arms** | refuses a single α |

- Arm-invariance (factor-locality) holds to first order for td/ρ; ECM's small Δα is a real
  cofactor fingerprint (success couples both factors' group orders).
- **HEADLINE: the ECM self-destruction wall** — when B1 ≳ min(p,q), every Hasse-window
  order divides lcm(1..B1), all curves degenerate simultaneously, and uncapped E[T] is
  infinite. The honest object is {(α, c)(B1)} behind the validity edge B1 ≲ min(p,q)/2.
- H2b refuted: pre-stated smoothness proxies (lpf/ω of p±1, N±1) capture none of ECM's cost
  drivers — powersmoothness across the whole 4√p Hasse window is what drives it.

## 3. What this decides

Paper 132's residual item (2) closes with a qualification: the unified plane exists for
td/ρ/Fermat as single (α, c) rows (measured exactly where laws exist), and for ECM as a
B1-family behind an explicit validity edge. Barriers: (8) measuring known methods knowingly;
(4) factor-locality's evasion answered constructively.

Method ledger: two superseded runs disclosed (a lean takeover with a TD convention bug and
a wrong-Suyama-denominator run rejected by its mod-12 signature); ECM denominator validated
before final data (ladder-vs-affine match 10/10, mod-12 100/100).

Now 491 experiments. Assessment v268.
