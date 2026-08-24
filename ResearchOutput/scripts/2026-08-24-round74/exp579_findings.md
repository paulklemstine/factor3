# exp579 PROFILE-FORM (round-74) — findings
Question (paper-228/exp578 follow-up a): WHAT FUNCTIONAL FORM is the small-j hit-
position profile exp578 found (deciles .162->.072)?
Data: exp578_positions.npz verbatim (9594 hits + paired controls, 128 Ns, bitlen 96).
50 equal-width u-bins, pooled rate-weighted profile; CLUSTER bootstrap over Ns (2000
reps, seed 20260831) -> per-bin CIs; WLS fits (weights=1/bootSE^2), AICc/BIC +
covariance & bootstrap parameter CIs. BASELINE: Dickman rho(u), u=ln(j^2-N)/ln(1e6),
table verified vs rho(2..5) to 6 decimals. N not stored; s=isqrt(N)=jhi//3 exact
leaves offset r=N-s^2 unknown -> mixture over UNIFORM-r prior (17-pt) + brackets
{0,mid,2s}; du error at v~N O(1e-27).
FAMILY VERDICT: **POWER LAW WINS** — T(x) ~= a*(1+x)^-b, a=0.0295 [boot95
0.0284,0.0307], b=1.104 [0.991,1.218]; Akaike weight 0.987; dAICc: power 0 |
exp 9.2 | logistic 11.5 | linear 16.9. b~=1.1 => density ~1/(1+x), HARMONIC
decline, decisively not linear. Logistic degenerates to exponential (unidentifiable).
RESIDUAL (beyond-magnitude) SHAPE: **PEAKED, NOT a further gradient**. Dickman
absorbs nearly ALL the raw decline: M falls 3.64x first->last bin vs T's 3.25x
(slightly OVER-predicting steepness). R=T/M: 0.80 @x=.01 -> ~1.0 mid -> hump max
1.23 @bin33 (x~.67) -> 0.90 @x=.99. Spearman +0.118 p=0.42 (not monotone);
linear slope on R POSITIVE +0.098 [0.035,0.162]; quadratic beats linear dAICc=50.5,
c-CI wholly<0 [-0.62,-0.14], vertex x=0.59 interior => pre-registered PEAKED rule
fires. Invariant across all three r-brackets: baseline-robust. Control FLAT (CI covers 0).
READING: positional law is harmonic ~1/(1+x) whose bulk IS the smoothness magnitude
gradient; the genuine beyond-Dickman part is a modest (+/-20%) CONCAVE MID-WINDOW
EXCESS with deficits at both ends (esp. small-j: the rho=1 wall region over-predicts
hits) — structure, not a second monotone gradient. Reconciles exp578: coarse
(bitlen x octant) strata could not absorb what continuous rho(u) does.
ONE-LINE LAW: T(x) ~ 0.0295*(1+x)^-1.10; beyond-rho(u) residual = concave hump
(peak ~1.23 at x~0.6), NOT itself declining.
Honest limits: uniform-r prior approximates the true next_prime r-distribution
(r=2s bracket deepens small-j deficit to R=0.51, shape call unchanged); Dickman
treats v=j^2-N as random integers (constant-factor misspecification possible; shape
conclusions offset-invariant); rate-weighted pooling (HITRICH>=30 drops one N);
smoke passes hit a bootstrap-broadcast bug, fixed — FULL ran clean in 10.2 s.
Files: exp579_profile_form.py (pre-registered V1/V2 rules), exp579_result.json, this file.
