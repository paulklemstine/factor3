# EXP575 GENERATOR-TILT — paper-221 named item L7-a CLOSED (2026-08-24)

**Q:** does the within-window divisor-mass bottom-heavy tilt behind the 1.58x
window-ascending win (hard q<2p balance) exist in realistic generators?
**Verdict (pre-registered rules):** H1 REFUTED decisively; H0's numeric band missed but
H0's CONSEQUENCE HOLDS in stronger form (recorded MIXED/PARTIAL by the literal rules;
refined reading in JSON). On RSA-style pools the tilt is INVERTED — top-heavy.

| pool | n | window | z_mean [CI95] | win_asc/desc S | in_win |
|---|---|---|---|---|---|
| HARD_BAL (control) | 600 | canonical | **0.4114** [0.3887,0.4341] | **1.5896 ±0.0538** | 1.000 |
| RSA_INDEP (b=15) | 600 | canonical | **0.6356** [0.6150,0.6562] | **0.5578 ±0.0217** | 1.000 |
| RATIO4 | 600 | adapt r_max=4.5 | 0.0558 [0.0530,0.0586] | 17.345 ±0.4654 | 0.000 |
| UNIFORM_WIDE | 600 | adapt r_max=8.0 | 0.5979 [0.5765,0.6194] | 0.5505 ±0.0230 | 0.582 |

**Control:** replicates analytic 0.414 and verifier BAL_prime (0.4095–0.4148, 1.5785±0.029)
at shifted bitlen b=11→15 — machinery sound.
**Mechanism:** two independent same-bitlen uniforms have ratio concentrated near 1
(effective median ≈1.25), which pushes min(p,q) HIGH into (√(N/2),√N]; hard balance
(r~U[1,2)) spreads it low. Tilt sign = f(generator's r-law), confirming the md's band-width
law and completing its sweep with the deployed-like cell.
**Consequence (plain):** Lambda-dominance is CONFINED TO ARTIFICIAL HARD-BALANCE POOLS.
RSA-style deployed-like generation carries an ADVERSARIAL (top-heavy) tilt: window-ascending
is always well-defined there (in_win=1.000, unlike paper-137's 21.6% undefined) yet LOSES
~44% to sqrt-descending. Paper-221's caveat stands as final word, upgraded from "tilt
unmeasured" to "tilt adversarial off-balance": any "~free" reorder gain requires the
deployed generator to ENFORCE q<2p balance, and none does. No speed prescription — scoped
reorder-class fact only.
**Ledger catches:** `findings.md` already existed (other work) → wrote exp575_findings.md;
descriptive sign readout added after smoke, rules unmodified (noted in JSON honest_notes);
RATIO4's 17x is the narrow-stratum pinning artifact (needs N-invisible r_max knowledge),
not a deployable order.
Artifacts: exp575_generator_tilt.py, exp575_smoke.log, exp575_full.log, exp575_result.json,
exp575_findings.md (all in ResearchOutput/scripts/2026-08-24-round74/). Not committed.
