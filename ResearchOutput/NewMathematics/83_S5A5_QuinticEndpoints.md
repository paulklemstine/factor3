# Paper 83 — S₅/A₅ QUINTIC ENDPOINTS: The Largest Entropy Collapses, the Perfect Group Seals

**Verdict name: THE-TYPE-CHANNEL'S-TWO-EXTREMES.**
Round-24 #4 · exp 418 · assessment v194 · script `/tmp/exp_s5a5quintics.py` · log `/tmp/r24n4k.log` · runtime 150 s.

## 1. The endpoints

Papers 78–82 carried the abelianization law across degrees 2–5 on C₂/C₃/C₄/C₂×C₂ fields. This round closes the transitive-quintic row's two extremes:

- **S₅ via x⁵−x−1** — true discriminant **2869 = 19·151** (not the quartic x⁴−x−1's famous −283; both polynomials are "the classic minimal example" of their degree and the −283 had migrated between them in our notes). Seven factorization types with class sizes {1,10,15,20,20,30,24}/120 give **H(T) = 2.5574 bits — the largest type entropy measured in the program**. Every type determines its sign (odd = {[2,1,1,1], [3,2], [4,1]}), so the law predicts loss 0 and **I₁ = 1.0000 exactly**; pair = 1.0000 (the C₂ cap); odd-type sign fork s-projection = Is(2).
- **A₅ via x⁵+20x+16** (paper 76's object, disc = 32000²): four types {[1⁵] 1/60, [2,2,1] 15/60, [3,1,1] 20/60, [5] 24/60} (the two A₅ classes of 5-cycles share one factorization type), **H(T) = 1.6555 bits** — and the strongest prediction in the program: G^ab trivial ⟹ **I(p mod m; T) = 0 at EVERY modulus**, pair = 0. Paper 76 proved forks flat; the complete multi-state channel must be flatter still.

## 2. Results (all asserts green)

### S₅ — the collapse is exact once the estimator is honest
- Type histogram matches class sizes < 2% on all seven types; H(T) = 2.5573.
- Type-determined sign vs the Kronecker character (2869|p) = (19|p)(151|p): agreement **1.0000** (23k primes).
- **I₁ = 1.2157 sits exactly at its within-sign permutation null 1.2188 (z = −0.85)**. The raw excess over the law's 1.0000 is **entirely sparse-dial plug-in bias (+0.2188)** — at a 2868-class dial with 23k primes, the Miller–Madow inflation dwarfs the effect being measured. The permutation-referenced comparison is the honest gate; the raw-vs-law comparison of earlier rounds only worked because their conductors were small.
- Thickening at m\*² z = +0.00; coprime flat (0.0002).
- Semiprime (400k MC): **I(N mod 2869; pair) = 1.0648 vs its within-sign-product null 1.0639** (z = +2.45, absolute gap 0.0009) — the C₂ cap holds, with the table's ~80k-cell bias again fully absorbed by the null. Odd-type sign-fork s-projection = **1.0023 vs Is(2) = 1.0000**.

### A₅ — the seal is total
- No odd-type readout ever occurs ((3,5), (1,1), (0,4) never appear — an independent pipeline check).
- **I(p mod m; T) at the permutation null for m ∈ {3, 7, 11, 31}: worst |z| = 1.72.** The complete four-state channel — not just the forks of paper 76 — is residue-blind at every modulus tested.
- Semiprime: **I(N mod 7; pair) = 0.0004 ≈ 0** (400k draws). 1.6555 bits of splitting entropy, and N cannot hear a single one of them from any residue direction.

## 3. The measurement ledger (this round's real content)

Eight runs were needed; six distinct defects were caught, each by a designed check rather than luck — recorded here as the protocol's case study:

1. **Dictionary entry**: [3,2] reads (nr, nr₂) = (0,**2**), not (0,4) — one quadratic pair contributes two F_{p²}-roots. Caught by the p=2 crash ([3,2] occurs already at p=2).
2. **Discriminant migration**: disc(x⁵−x−1) = 2869 = 19·151, not −283 (the quartic's value). Caught by repeated factors mod 151 (two roots but empty co-factor ⟹ ramified).
3. **Encoding inversion**: the first sign check read agreement 0.0000 — *perfect* anti-correlation, i.e., the law confirming itself through a flipped coding convention. Exact zeros/doubles demand inspection, not despair.
4. **Sparse-dial bias on the headline statistic**: raw I₁ exceeded the law by +0.216 bits at m\* = 2869 — pure plug-in inflation. Fix: within-sign permutation nulls for I₁ itself (the paper-70 lesson, finally applied to the primary quantity rather than only to thickening).
5. **Null design**: permuting the *labels* (pair codes) within strata deletes the through-stratum coset channel the law predicts (null collapsed to bias-only 0.13 while obs sat at 1.06 — the gap was exactly the 1-bit channel). The correct reference permutes the *data* (Nf) within strata, preserving stratum(Nf′).
6. **Type-system mismatch**: strata computed via `isin(int_ids, string_set)` ≡ all-false ⟹ a global shuffle masquerading as a stratified one. Same root cause would have silently zeroed the s-projection.

Generalized lessons now part of the lab protocol: **(i)** at large conductors every MI — headline or diagnostic — is permutation-referenced; **(ii)** a permutation null must preserve precisely the channel the law predicts and randomize only the finer assignment; **(iii)** exact agreement 0 or 1 flags encoding bugs before physics.

## 4. Barriers

**(a) Circularity — clean.** Predictions pre-stated with exact values; types read from root counts independent of the dial; the A₅ zero-prediction is parameter-free.
**(b) Known-method-in-disguise — clean.** No S₅/A₅ type-channel work in the Catalog (nearest: our own echoes).
**(c) Toy-scale — confronted.** Real S₅/A₅ fields, 23k-prime histograms < 2% from class sizes, 400k-draw MC, four moduli × 200-shuffle nulls for the seal.
**(d) Data leakage — clean.** Fixed seeds throughout.
**(e) Variance/reproducibility — the substance.** All comparisons permutation-referenced at large conductors; the full defect ledger above disclosed; final run ALL_DONE all-green.
**(f) Measurement errors — controlled and survived.** Six defects caught by designed checks; none reached the record's numbers uncorrected.
**(g) Baseline unfairness — clean.** Which-factor walls ≤ 0.0001; coprime flat; the A₅ zero is its own control (the pipeline detects structure wherever G^ab ≠ 1 — papers 78–82).
**(h) Practical relevance — closure.** Symmetric pairs (barrier 2), residue dials only (barrier 5), CRT-sealed (barrier 6), classical Galois/Reciprocity/Chebotarev (barrier 8). For S₅ the entire 2.56-bit type distribution reduces to the single quadratic-residue bit of N mod 2869; for A₅ nothing reduces to anything.

## 5. What closes

The transitive-quintic row is measured on four of five groups — C₅ (paper 79 lineage), F₂₀ (paper 82), S₅, A₅ (this paper) — with D₅ the sole untested group (awaiting a verified D₅ defining polynomial). The abelianization law has now been confirmed at every abelianization type that exists for degrees 2–5: trivial (A₅: total seal), C₂ (S₃/S₄/S₅: the 1-bit cap), C₃ (A₄), C₄ (F₂₀), C₂×C₂ (D₄/V₄), and Cₙ (abelian controls). The type-channel program is complete at every tested group; the frontier returns to the quantum channel (QUBIT-TRADE phase diagram) and the barrier-4 converse.

Now 418 experiments. Assessment v194. Paper 83, issue #175.
