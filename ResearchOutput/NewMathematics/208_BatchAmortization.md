# Paper 208 — BATCH-AMORTIZATION: Batch Smoothness-Testing Wins Its Phase (+10.4%) but Testing Is Only 11.6% of the Work

**Verdict name: BATCH-WINS-TESTING.**
Round-73 #3 · exp 561 · assessment v315 · script `exp561_batch.py` (+ JSON/log) · seed 20260827 · wall 140 s · audit PASS 500/500.

The amortization question, isolated: does batching the B=100 smoothness test (product
tree over a pool of k candidates) beat solo trial division, and by how much can it
possibly matter per factor? Population 512 distinct N (256 semiprime / 256 general,
bitlen 40), batch pools k ∈ {1, 8, 64, 512}, two pre-stated cost models (flat: every
executed bigint mul/mod/div/add/Euclid/MR-step/GF2-XOR = 1 op; word: width-aware with
skipped reductions free) plus wall clock.

**Batch wins its phase — in the flat model only.** Best Δ_k = +0.1041 at k=512; batch
beats solo at every measured pool size (crossover vs solo: always below). The WORD
model REVERSES at large k (Δ = −62.6 at k=512): the product tree's big-int
intermediates dominate once widths grow, and the word-model crossover sits at
M* ≈ 1715 candidates (log2 M* = 10.74) — below that batch wins, above it solo.
Wall-clock delta is only +0.24%: GMP-level reality sits near the word model's warning.

**E1 confirmed with the bound quantified.** Solo testing is 11.56% of per-factor ops
(non-testing 88.44%), so the saving is CAPPED at +11.6% even if testing were made
completely free — the realized +0.104 sits just under the cap. The finding phase is
strictly per-N by construction (relation yield and rho work identical across arms;
this IS the "finding does not amortize" term). Honest QS note: qs_splits_total = 0 —
at bitlen 40 with FB ≤ 100 the per-N yield is far below the 26 relations QS needs;
rho carries factoring identically in every arm.

**Audit (H_AUDIT) exact-match pass:** batch-detected smooth set == per-item trial-
division set on 500 samples — tree-vs-trial 0 mismatches, direct-vs-trial 0, vector
0/0. No ledger catches this run.

Honest validation against the barrier map: this is constant-shaving on a KNOWN method
(product-tree batch smoothness testing is standard QS/NFS machinery — barrier 8), NOT
an asymptotic result; it moves no exponent and is bounded above by an 11.6% share of
a known-method pipeline. Recorded value = calibration of where batching helps inside
the method stratum, plus a real deployment caveat (word-model sign flip past k≈1715).
Consistent with the standing asymptotic-goal directive: recorded as engineering
calibration, not class movement. Barriers 8 unchanged. Now 551 experiments (max id).
Assessment v315.
