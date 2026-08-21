# Paper 82 — QUINTIC-TYPE-CHANNEL: The Abelianization Law at Degree Five — F₂₀ and the First C₄ Dial

**Verdict name: THE-ABELIANIZATION-LAW-AT-DEGREE-FIVE.**
Round-24 #3 · exp 417 · assessment v193 · script `/tmp/exp_quintictypechan.py` · log `/tmp/r24n3f.log` · runtime 81 s.

## 1. The object

Paper 80 closed the type-channel program over S₃/S₄/A₄/D₄ with abelian controls V₄/C₄ — every abelianization C₂ or C₃, every dial binary or ternary. The untested transitive groups begin at degree 5, and the natural first object is the **Frobenius group F₂₀ = AGL(1,5)** (order 20) via its simplest defining polynomial **x⁵ − 2**: the program's first **C₄-abelianization** — a quaternary dial. Frob_p acts on the five roots ζ₅^k·2^{1/5} as the affine map k ↦ p·k + c on Z/5: multiplier a = p mod 5, translation c ≠ 0 only when p ≡ 1 mod 5 (and then iff 2 is not a fifth power mod p). The four types and their (nr, nr₂) readouts:

| condition | type | (nr, nr₂) | class size |
|---|---|---|---|
| p ≡ 1 mod 5, 2 a 5th power | [1,1,1,1,1] | (5,5) | 1 |
| p ≡ 1 mod 5, otherwise | [5] | (0,0) | 4 |
| p ≡ 2 or 3 mod 5 | [1,4] | (1,1) | 5 + 5 |
| p ≡ 4 mod 5 | [1,2,2] | (1,5) | 5 |

G^ab = C₄ carried by the quartic character mod 5; coset = the C₄-valuation V(p mod 5): 1→0, 2→1, 4→2, 3→3.

## 2. Predictions (stated before the run)

- **H1 (prime law)**: I(p mod 5; T) = I(T; coset) = **1.5000 exactly** — H(T) = H(1/20, 4/20, 10/20, 5/20) = 1.6805 collapses through the 2-bit dial; the [1,4] type *merges* the two order-4 cosets {2,3}, so the loss is E[H(coset|T)] = P([1,4])·H(1/2,1/2) = **exactly 0.5 bit**.
- **H2 (semiprime law)**: I(N mod 5; unordered pair) = class-enumeration value = **1.2500 exactly** (H(pair) = 2.7160, H(cond) = 1.4660); the [1,2,2]-fork is coset-determined (⟺ p ≡ 4 mod 5, rate 1/4) ⟹ its s-projection must equal **Is(4) = 0.2947** — an *order-4* pinned fork realized on a non-abelian field.
- **H3 (C₅ control)**: Q(ζ₁₁)⁺ (conductor 11), 2-state type {1,5} at rates {1/5, 4/5}: I₁ = H(1/5, 4/5) = 0.7220; pair = Is(5) = 0.2027 (paper 79's f=11 entry).
- **H4 (discipline)**: within-coset flatness (only the p ≡ 1 stratum carries residual structure), permutation-referenced thickening, coprime flat, which-factor walls zero.

## 3. Results (all asserts green)

### Prime level (~23k primes per field)

| field | G | G^ab | #types | H(T) | I₁ measured | law | dial H(coset) | loss |
|---|---|---|---|---|---|---|---|---|
| F₂₀ x⁵−2 | F₂₀ | C₄ | 4 | 1.6805 | **1.4989** | 1.5000 ✓ | 2.0000 | **0.5** |
| C₅ Q(ζ₁₁)⁺ [control] | C₅ | C₅ | 2 | 0.7219 | **0.7198** | 0.7219 ✓ | 3.3219 | 2.6000 |

F₂₀ discipline: within-coset flatness at the p≡1 stratum z = +0.00; thickening m\*² = 25 agrees with its permutation null to 0.0001; coprime m=3 flat (0.0001).

### Semiprime level (400k MC, unramified pools)

| field | I(N mod m\*; pair) | law | dial-pair | which-factor | pinned-fork s-proj |
|---|---|---|---|---|---|
| F₂₀ x⁵−2 | **1.2462** | 1.2500 ✓ | 2.0000 | 0.0000 | **0.2915 = Is(4)** ✓ |
| C₅ Q(ζ₁₁)⁺ | **0.2026** | 0.2027 = Is(5) ✓ | 3.3219 | 0.0000 | 0.2026 = Is(5) ✓ |

- The F₂₀ type pair reads **1.25 of the 2-bit dial** — the largest fraction of any merged-type field in the program (S₃/S₄ read 1.0 of 1.0; A₄ 0.47 of 1.585; D₄ 1.43 of 2.0).
- **Is(4) on a non-abelian field**: the [1,2,2] fork is pinned by the order-4 quartic character alone — the split-count law's order-4 case was previously realized only on abelian fields (V₄/Q(ζ₈), paper 77/79) and the joint-AND D₄ fork (paper 77); F₂₀ realizes it through a genuine cyclic order-4 character.
- The C₅ control reproduces the abelian regression line end to end (pair = Is(5), paper 79's f=11 entry) inside the identical pipeline.

## 4. Method notes

- **Quintic type dictionary via F_{p²}-root counting**: (5,5)→[1,1,1,1,1], (1,1)→[1,4], **(1,5)→[1,2,2]**, (0,0)→[5]. Note (1,5), not (1,3): both quadratic pairs' roots live in F_{p²}\F_p and join the linear root — a degree-5 correction of the quartic-carried intuition.
- **Coset-label discipline — the round's instructive failure**: the first run labeled the multiplier-3 family with coset 2 and multiplier-4 with coset 3 (swapped relative to the C₄ valuation V). This is **invisible at the prime level** — both merged classes share the type [1,4], so I₁ is unchanged — but corrupts the semiprime pair enumeration (law 1.1250 vs true 1.2500). The 400k MC caught it: measured 1.2462 disagreed with the (wrong) law beyond tolerance while sitting on the corrected value. Lesson recorded: **the pair law is the discriminating test of coset bookkeeping precisely where type-merging hides it.**
- Harness bugs caught and fixed across runs: little-endian reversal of const-first coefficient lists; the (1,3) dictionary carryover; a non-variadic character-product lambda. All measurement-side machinery identical to papers 80–81.

## 5. Barriers

**(a) Circularity — clean.** All four horns with exact values stated before the run; types read from root counts independent of the dial.
**(b) Known-method-in-disguise — clean.** No quintic splitting-type channel work in the Catalog (nearest: our own #723–#728, #797's parity-gap echo); Kummer theory and affine-action classification are classical structure, not factorization moves.
**(c) Toy-scale — confronted.** Real F₂₀ field (x⁵−2), ~23k-prime histograms matching class sizes < 2%, 400k-draw MC.
**(d) Data leakage — clean.** Fixed seeds, deterministic enumeration.
**(e) Variance/reproducibility — the substance.** All margins quantified (I₁ −0.0011; pair −0.0038; s-proj −0.0032); the coset-swap episode documented as part of the record.
**(f) Measurement errors — controlled and survived.** Four harness defects caught by asserts/MC-law disagreement across five runs; final run ALL_DONE with every assert green.
**(g) Baseline unfairness — clean.** C₅ abelian control reproduces paper 79 through the identical pipeline; coprime flat; walls zero.
**(h) Practical relevance — the closure extended.** Symmetric pairs (which-factor 0.0000, barrier 2); pure residue dial at the quartic conductor (barrier 5); N-computable only behind the CRT split (barrier 6); Kummer/affine/Frobenius classical (barrier 8).

## 6. What closes

The abelianization law now spans **degrees 2–5** and abelianizations **C₂, C₃, C₄, C₂×C₂, Cₙ**: I(p mod m\*; T) = I(T; coset) at the prime level, the pair law verbatim at the semiprime level, with the type-vs-dial gap always exactly E[H(coset|T)] — the entropy of the cosets the type cannot tell apart. Remaining rows above it: S₅/A₅ generic quintics (G^ab = C₂ predicted 1.0 / perfect predicted 0 — both already exercised at lower degree), and the exceptional G₂₀/G₂₆... no — the program's type-channel face is complete at every tested group; the frontier returns to the quantum channel (QUBIT-TRADE phase diagram) and the barrier-4 converse.

Now 417 experiments. Assessment v193. Paper 82, issue #174.
