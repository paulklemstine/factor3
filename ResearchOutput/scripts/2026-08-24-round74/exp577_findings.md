# exp577 PRODUCT-DIAL-SCALESHIFT (round-74) — findings [REVERIFIED]
VERDICT (pre-registered): **WINDOW-STRONGER-NOT-SHIFTED** — H1 scale-shift
REFUTED; H0 cannot fire (the <=400 dial alone clears the 30% bar this seed).
Setup: 128 balanced bitlen-96 semiprimes, FRESH master seed 20260827; prior trio
hashes e8d89a29a03779d5/9cb9cc800ee45a38/81acc9b5e1be619b REPRODUCED exactly,
new a15e2877dd1dac7a, pairwise disjoint. 150k j-samples/N, exp569 tester verbatim,
cut 1e6; wall 380.8 s. Overdispersion replicated 3rd time: mean 77.6, D_raw 4.90, top3 135/135/130.
SWEEP CURVE (cumulative QR-count dial vs log-rate), R2/D-red: B=400 .3207/33.4%
| 4000 .0241/2.4% | 4e4 .0150/1.7% | 1e5 .0000/0.0% | 1e6 .0277/4.1%. NO shift
past 400: extension DILUTES (equal-weight counting buries primes informative
~1/l). B* = 400.
WEIGHTED dial sum_{QR l<=B} 1/l: W400 R2=.4731/D-red 48.1%; W1e6 .4786/48.5%
(z~16.8); corr(W1e6,W400)=0.999 — signal SATURATES by 400 once weighted; window
location scale-INDEPENDENT, weight is the law.
REVISION 2026-08-24 (post verifyL7b; cite verifyL7b_result.json):
1. LEDGER CATCH on exp576/paper-226 SECONDARIES confirmed+completed: both are
   composite-bottom forms, (l|N)=(l|lo)(l|hi), tied to the mechanistic Legendre
   dial (N mod l|l) by a reciprocity sign flipping iff l=3 mod 4 AND N=3 mod 4
   (52.3% of N; flip rate 100%, 2680/2680). Flipped forms weak HERE with same
   hits/machinery — S_prod@100 .030/4.1%, S139@400 .0456/5.5% (verifier
   reproduces) vs clean C400 .3207/33.4% — paper-226's published weakness is an
   ARTIFACT of dial form, not absence of QR signal.
2. CORRECTION TO MY DRAFT + verifier addendum: the strong object is the CLEAN
   bound-100 Legendre dial (C100clean R2=.3728/D-red 34.45%/r-vs-C400=.476);
   verifyL7b's "formA" column IS this clean dial (its build_cols codes
   gjac(lo%p,p)*gjac(hi%p,p)=(N|p) while its own audit defines form-A=(l|lo)
   (l|hi)) — label swap; r(flippedP100,C400)=0.058 stands for the flipped form.
   Addendum leg "removing l=2 makes formA strong" REJECTED empirically: flipped
   form without l=2 stays weak (.0322/4.34%; l=2 shifts counts by 0/1 only).
   Pre-reg header "signs cancel in the product" was FALSE; annotated in-script.
3. STILL OPEN: exp576 PRIMARY S_indiv nulls here too (.0019/0.09%, z=0.72) —
   flip mechanism inapplicable (no composite bottom); unresolved.
CONSEQUENCE (both readings): count dial @400 explains 33.4% of raw dispersion
(=42.1% of excess-above-Poisson); W1e6 48.5% raw (=61.0% of excess); residual
~51.4% raw / ~39.0% excess, still overdispersed (D_cond>1). Paper 226's ">=86%
new structure" shrinks to ~39–58% (dial/reading dependent). Follow-up: adopt
1/l-weighted product dial as canonical scale-smoothness covariate.
Self-catches: l=2 even-modulus crash caught in smoke; first-draft T1 bound mismatch and corr-/n slips fixed pre-ledger.
Files: exp577_product_dial.py (pre-reg header + REVISION annotation), exp577_smoke.log/_result.json, exp577_full.log, exp577_result.json, exp577_diagnostics.py/.log/.json (incl revision block), this file.
