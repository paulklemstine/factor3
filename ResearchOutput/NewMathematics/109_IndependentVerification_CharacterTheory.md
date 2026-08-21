# Paper 109 — INDEPENDENT-VERIFICATION: The Character-Theoretic Proof of Paper 80

**Verdict name: THE-CHARACTER-CAPTURES-EXACTLY-ONE-BIT.**
Round-31 #2 · exp 445 · assessment v220.

## 1. Beyond reproducibility

Papers 97 and 103 verified reproducibility by re-running stored scripts. This round goes further: a **pure character-theoretic derivation** of paper 80's key result, using no Monte Carlo, no shared code, and no stored data.

## 2. The derivation

For S₃ x³+x+1 (disc = −31, G = S₃, G^ab = C₂):

**Chebotarev densities**: P('111') = 1/6, P('12') = 1/2, P('3') = 1/3.
H(T) = 1.4591 bits.

**The sign character**: (−31|p) determines whether the Frobenius is even or odd. Odd (15 residues) ⟹ type = '12' always. Even (15 residues) ⟹ type ∈ {'111' (1/3), '3' (2/3)}.

**The computation**: H(type | sign) = (1/2)·0 + (1/2)·H(1/3, 2/3) = (1/2)·0.9183 = 0.4591.

**I(p mod 31; type) = H(T) − H(T|sign) = 1.4591 − 0.4591 = 1.0000 EXACTLY.**

## 3. Why the residue scan showed mixed types

The scan found 15 residues with mixed types (some primes give '111', others '12'). This is **expected and correct**: the sign character only separates even from odd Frobenius; within the even class, the split between identity and 3-cycles is residue-independent (Chebotarev within the A₃ subextension). The "mixed" residues are exactly the 15 even-sign residues, each showing both '111' and '3' types.

## 4. What this decides

Paper 80's key result (I = 1.0000 for S₃a@31) is **proven from character theory**, not just measured. The proof generalizes: for ANY S₃ field, I(p mod |disc|; type) = H(type) − H(type | sign) = 1 bit exactly, because the abelianization is C₂ and the sign character captures exactly 1 bit. The remaining H(type) − 1 bits are locked behind the non-abelian structure, inaccessible from any residue.

Now 445 experiments. Assessment v220. Paper 109, issue #201.
