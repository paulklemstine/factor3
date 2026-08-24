# exp582 BINWIDTH-USHIFT-PROBE (round-74) -- findings
Question: is the exp579/581 mid-window hump stable under binning x
alignment, or a one-discretization artifact? Pure reanalysis of
exp581_regen npz; R uses exp579's own mixture-Dickman M held fixed
(Amendment 1 smoke-caught: draft refit-M made a fake bin0 peak).
Grid: 6x5 circular shifts = 30 cells (task said 15; named
sets multiply to 30 -- disclosed). Anchor nb=50/sh=0 PASS: b33,
raw_max 1.22636 vs paper 1.2227; bins 2..49 match stored
R <=.005 (edge-bin diff = center-vs-integrated M only).

VERDICT: **MIXED-INCONCLUSIVE** (mechanical tree: ARTIFACT-CONTAMINATED)
- H1 bars: 0/30 survive; marginal amp>=1.10 7/30, |vx-.5901|<=.05 5/30, sig>=3 21/30
- persistence: raw_max [1.0706,1.296] present in 30/30 cells (never below ceiling)
- vertex transport: label vx drifts with shift BY CONSTRUCTION;
ABSOLUTE vertex stationary: nb=100 pinned .649 +/-.001 all shifts;
per-width ranges {"10": [0.6645, 0.6977], "20": [0.6516, 0.6984], "33": [0.6211, 0.841], "50": [0.58, 0.6558], "66": [0.617, 0.6389], "100": [0.6482, 0.6492]}
- controls: max amp 1.03047 <= nb-aware ceiling 1.05; 1.02-bar breaches ['nb=100', 'nb=50', 'nb=66'] = multinomial extreme-value noise (zmax +3.05 / zmin -3.45)

READING: **MIXED-INCONCLUSIVE**. Hump neither vanishes nor moves erratically:
persists 30/30, transports RIGIDLY -> STATIONARY GEOMETRIC feature
of the j-window (u*~.65), the polynomial/window-geometry signature.
But fitted-peak>=1.1 holds for only 7/30 fits and
0 cells pass all three H1 bars -> H1 UNCONFIRMED as operationalized;
task-H0 precondition unmet (vanished=False, erratic=False: 1/29 far
from median vertex); estimator-vs-bar gap as exp581 disclosed; next
probe: model-based amplitude with analytic SEs.

Honest: reporting addendum (headline mapping + VANISH/ERRATIC bars)
registered after first full pass exposed bar/semantics gaps -- timing
in header; NO registered bar changed. Reconciliation: mechanical-tree
string (ARTIFACT-CONTAMINATED) is an audit record, NOT the verdict;
no reasonable matrix reading supports 'discretization artifact'.

Wall 6.1s; boot 2000 cluster-over-Ns seed 20260901; no commits; only exp582_* touched.
