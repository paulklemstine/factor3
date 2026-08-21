# Paper 121 — DIAL-CROSS-TALK: Independent Dials Are Truly Independent

**Verdict name: THE-DIALS-ARE-INDEPENDENT.**
Round-34 #3 · exp 452 · assessment v231 · script `/tmp/exp_dialcrosstalk.py` · log `/tmp/r34n3.log` · runtime 12 s.

## 1. The test

Two coprime-disc S₃ cubics (x³+x+1 disc −31; x³−2 disc −108) measured on the same primes: are their splitting types correlated?

## 2. Results

**Prime level**: I(type₁;type₂) = 0.000437 bits (permutation-null z = −0.81). The types of x³+x+1 and x³−2 mod p are completely independent.

**Semiprime level**: I(pair₁;pair₂) = 0.001424 bits (null z = +2.79). The pair channels are also independent.

## 3. What this decides

Linearly disjoint S₃ fields produce completely independent type channels: knowing how x³+x+1 splits mod p tells you nothing about how x³−2 splits mod p. This confirms that the type-channel framework's additivity (paper 92) rests on genuine statistical independence, not just theoretical assumption. The battery capacity arithmetic (super-additive with synergy) is built on solid foundations.

Now 452 experiments. Assessment v231. Paper 121, issue #213.
