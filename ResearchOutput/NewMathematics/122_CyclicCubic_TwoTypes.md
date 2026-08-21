# Paper 122 — CYCLIC-CUBIC-TYPE-CHANNEL: Two Types, Full Pinning

**Verdict name: THE-CYCLIC-CUBIC-IS-FULLY-PINNED.**
Round-32 #3 · exp 448 · assessment v228 · script `/tmp/exp_cycliccubic.py` · log `/tmp/r28n2b.log`.

## 1. A genuinely new structural case

All prior cubic measurements used S₃ fields (three conjugacy classes, three splitting types). This round tests a **cyclic cubic** — Q(ζ₇+ζ₇⁻¹), degree 3, Gal = C₃, conductor 7 — which has only TWO conjugacy classes and therefore only two splitting types: [1,1,1] (splits completely, p ≡ ±1 mod 7) and [3] (irreducible).

## 2. Results

Root-count histogram: {nr=0: 4363 (66%), nr=3: 2178 (33%)} — only two types ✓. H(type) = 0.9179 bits.

**I(p mod 7; type) = 0.9179 = H(T) exactly** — FULL PINNING confirmed for the abelian case ✓. Coprime m=5 flat (0.0001).

Semiprime: I(N mod 7; pair) = 0.4747 bits; wall z = +12517 (genuine structure); which-factor wall = 0.0000 ✓.

## 3. What this decides

The type-channel framework correctly handles the cyclic cubic's simpler structure: only two types (vs three for S₃), each fully determined by p mod 7. The abelian case gives exact pinning with zero within-class entropy — the simplest instance of the general law I = H(T|G^ab-complement).

Now 448 experiments. Assessment v228. Paper 122, issue #209.
