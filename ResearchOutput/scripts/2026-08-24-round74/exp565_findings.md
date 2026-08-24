# exp565 ORACLE-REALIZATION-GAP — round-74 (2026-08-24)

Script `exp565_oracle_gap.py` · seeds 20260824/20260825 · wall 56 s · prereg `exp565_prereg.json`
Frame reused verbatim from exp549 (population, descent, oracle definition); budget = probe count.

**REPRODUCTION (deliverable A): PASS BIT-EXACTLY.** Seed-20260824 population regenerated from
exp549's code path matches all 11 published fine-grid points to the last digit — peak
I(1{d≤B};b₁)=0.479797 @ B=22758, hit-rate 0.2053, B*(0.9)=10420, delta_peak=0.000000.
Fresh seed B: peak 0.4948 @ 22758 (reported only).

**PRE-REGISTERED VERDICTS (verbatim): H1 false, H2 not triggered → GAP-PARTIAL.**
Adaptive/battery pooled eval MI 0.167–0.172 bits = 33.8–35.9% of peak (>25%), credited under the
8-bin rule on seed A only; strict crediting (+32-bin within-control) = **0% for every N-only
policy on BOTH seeds**; no policy ≥50%; sham clean (max 0.0020 bits, credited 0).

**MECHANISM (post-hoc decomposition, amendment declared after first full run):**
1. The policies' entire pooled signal ≈ I(b₁;logN) of the same population: between-magnitude-strata
   base-rate variation created by the population DESIGN (support-edge coupling in indep/unilog,
   q≤2²² truncation in ratio). It is stable across seeds (+118≤z_pooled≤+128) but dies within
   logN strata (zw8 +1.9..+3.1 unstable, zw32 ≤2.3) and is flat in B after ~64 queries
   (class exhausts at 295 distinct queries; B=16384/22758 rungs are flat extrapolation).
2. Within-32-logN-bin decomposition: ORACLE carries within-strata excess **0.3634–0.3687 bits =
   73.5–76.8% of peak** (z≈41); best N-only policy carries 0.0009–0.0018 bits =
   **0.25–0.50% of the oracle's geometric content** — zero for practical purposes.
3. Composition controls: PARONLY-battery (mirror features) 0.1611–0.1667 ≈ full battery;
   MODONLY (residues) 0.0008–0.0032 ≈ 0 → residues contribute nothing even at naive-Bayes joint
   resolution (paper 81 seal holds jointly); signal = low-variance ensemble read of magnitude mirrors.

**ANSWER TO THE QUESTION:** the 0.4798-bit peak splits into ~74–77% within-strata GEOMETRY +
~23–26% population-prior slice. The geometric core is realizable ONLY by factor-conditioned
posteriors: the oracle arm realizes it by construction from d=M−isqrt(N), and FULL-ORACLE shows
H(b₁)=0.96 bits ≈ 200% of peak is the factor-knowledge ceiling. No N-computable policy realizes
any of it (≤0.5%). Realizing 1{d≤B} requires d, and d median 215782 vs menu exhaustion at 295 —
even a full Fermat scan at the peak budget misses 79.5% of samples.

**BARRIERS:** #6 CIRCULARITY CONFIRMED AND QUANTIFIED (d ≡ factoring; gap = 73–77% of peak).
#5 orthogonality consistent (no query touches the geometric channel). #2 SYMMETRY does NOT seal
b₁ a priori (b₁ is p↔q-symmetric via max/min, ledger L5) — residue null here is EMPIRICAL and
extends paper 81 to joint NB resolution. #4 aggregation consistent (only realizer of 1{d≤B} is
the Ω(d) scan itself). #1/#3/#7/#8 not engaged.

HONEST LIMITS: between-strata slice (~24%) is a property of this lab population's size-ratio
coupling, not of semiprimes generally; MI reported bias-corrected (obs − pooled-null mean);
discriminative arms fit on labeled train split (test-time N-only). LEDGER CATCHES: one amendment
cycle (documented, post-hoc block separate from pre-registered verdicts), none adverse.
ARTIFACTS: exp565_oracle_gap.py, exp565_prereg.json, exp565_smoke.{log,json}, exp565_full.log,
exp565_result.json.
