# Paper 210 — ORACLE-REALIZATION-GAP: The 0.48-Bit Oracle Navigation Sensor Is Unrealized by Every N-Computable Policy

**Verdict name: GAP-PARTIAL** (pre-registered verdict, evaluated verbatim; the post-hoc decomposition strengthens it — see the amendment cycle below).
Round-74 #1 · exp 565 · assessment v317 · script `exp565_oracle_gap.py` (+ JSON/logs/prereg) · seeds 20260824/20260825 · wall 55.8 s · frame reused VERBATIM from exp549 (population/descent/oracle definition), budget = distinct information-bearing queries, menu capped at 295 pre-stated items, residues m ∈ {3..31} sixteen moduli.

The closing question of the Berggren triplet-tree × energy-spectrum campaign (rounds 70–72,
papers 192–197): paper 197's oracle navigation sensor peaks at I(1{d ≤ B}; b₁) = 0.479797 bits
at B = 22758 with hit-rate 0.2053 — is that peak REALIZABLE by any policy whose inputs are
computable from N alone, or only by factor-conditioned posteriors (barrier 6)? Policies:
ADAPTIVE-NB (greedy mutual-information query selection over the 295-item menu), BATTERY
(information-ranked fixed order), BESTSINGLE, cost-0 controls (BASE-RATE logN-decile,
MAGPRIOR-16/64), SHAM (label-shuffled), composition arms (PARONLY-battery = parabola-mirror
features only, MODONLY = residues only), ORACLE-IND (the 1{d≤B} indicator at each ladder B)
and FULL-ORACLE (hint = b₁). Discriminative arms fit on a labeled TRAIN split; test-time
inputs are N-only. n = 3000 per seed (1500 train / 1500 eval); perms 200, bootstrap 1000;
MI reported bias-corrected (obs − pooled-null mean).

**Reproduction gate (deliverable A): PASS BIT-EXACTLY.** The seed-20260824 population
regenerated through exp549's code path matches ALL 11 published fine-grid points of paper 197
to the last digit — peak 0.479797 @ B = 22758 (delta_peak = 0.000000, max fine-grid delta = 0),
0.9-saturation B* = 10420. Fresh seed B reproduces the SHAPE: peak 0.4948 at the same B = 22758
(fresh population; constants need not match, reported only).

**Pre-registered verdicts (verbatim rules from `exp565_prereg.json`): H1 false, H2 not
triggered → GAP-PARTIAL.** Under LENIENT 8-bin pooled crediting, ADAPTIVE-NB/BATTERY realize
pooled eval MI 0.167–0.172 bits = **33.8–35.9% of the peak** (>25%) — but credited on seed A
only; under STRICT crediting (requires z ≥ 3 WITHIN logN-strata control): **0% for every
N-only policy on BOTH seeds**; no policy reached the 50% H2 bar anywhere; sham clean (max raw
0.0020 bits, credited 0 on both seeds).

**Mechanism — declared post-hoc amendment (ledger item A1), documented separately from the
pre-registered verdicts:** the entire lenient pooled signal is the BETWEEN-magnitude-strata
population base-rate channel — I(b₁; logN) created by the population DESIGN (support-edge
coupling in the indep/unilog strata, q ≤ 2²² truncation in the ratio stratum) — read out at low
variance by parabola-mirror ensembles. Evidence: PARONLY-battery 0.161–0.167 ≈ full battery
0.164–0.172 while MODONLY (residues) 0.0008–0.0032 ≈ 0 — residues contribute nothing even at
naive-Bayes joint resolution (extends paper 81's seal); the signal is stable across seeds pooled
(z_pooled +118..+128) yet DIES within logN strata (z_within8 +1.9..+3.1 unstable, z_within32
≤ 2.3); it is flat in B beyond ~64 queries (class exhausts at 295 distinct queries — the
peak-B rungs are flat extrapolation); cost-0 magnitude priors alone carry ≤ 0.008 pooled
(≤ 1.6%). Decisive split: within the 32-logN-bin decomposition the ORACLE carries
within-strata excess **0.3634–0.3687 bits = 73.5–76.8% of the peak** (z = 82–90) while the
best N-only policy carries **0.0009–0.0018 bits = 0.25–0.50% of the oracle's geometric
content** — zero for practical purposes. FULL-ORACLE anchor: hint = b₁ gives 0.9563–0.9627
bits ≈ 200% of peak, the factor-knowledge ceiling.

**Answer to the question: the peak remains UNREALIZED.** It splits into ~74–77% within-strata
GEOMETRY + ~23–26% population-prior slice. The geometric core is realizable only by
factor-conditioned posteriors: the oracle arm realizes it by construction from d = M − isqrt(N),
and computing 1{d ≤ B} for the median sample requires d — median d = 215782 against menu
exhaustion at 295 queries; even a full Fermat scan at the peak budget misses 79.5% of samples
(hit-rate 0.2053). Realizing the sensor REQUIRES factoring; it cannot replace it.

**Barrier map validation:** #6 CIRCULARITY CONFIRMED AND QUANTIFIED — d ≡ factoring, the gap
is 73–77% of the peak, the first quantified circularity measurement in the lab. #2 SYMMETRY
does NOT seal b₁ a priori (b₁ is p↔q-symmetric via max/min, ledger L5) — the residue null here
is EMPIRICAL, established jointly across 16 moduli at naive-Bayes resolution. #5 orthogonality
consistent (no menu query touches the geometric channel). #4 aggregation consistent (the only
realizer of 1{d≤B} is the Ω(d) scan itself). #1/#3/#7/#8 unengaged.

**Ledger:** ONE amendment cycle, disclosed — after the first full run the adaptive/battery
signal was identified as the free magnitude prior; MAGPRIOR arms, z_within32, bias-corrected MI,
and the within-component decomposition were added, the reproduction gate restricted to seed A,
and the pre-registered rules STILL EVALUATED VERBATIM (they fail honestly: H1's "<25% both
seeds" is false under lenient crediting because of the design artifact, hence GAP-PARTIAL
rather than GAP-CONFIRMED). No adverse catches. Honest limits: the between-strata slice (~24%)
is a property of this lab population's size-ratio coupling, not of semiprimes generally; the
BASE-RATE decile arm read 0.0 pooled on both seeds exactly as recorded.

This is a STRENGTHENING of the Berggren-campaign closure, not a breakthrough: rounds 70–72
sealed the tree proposal at four strengths (papers 192–197); this paper seals its last open
face — the unrealized 0.48-bit oracle bound — and converts barrier 6 from a label into a
measured quantity. Barriers 6 (quantified), 2, 4, 5 engaged; now 553 experiments (max id).
Assessment v317.
