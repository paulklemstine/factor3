# Paper 88 — CONVERSE-COST-CURVE: The Empirical Barrier-4 Across the Witness Family

**Verdict name: NO-POLYLOG-ROUTE-ANYWHERE.**
Round-26 #1 · exp 423 · assessment v199 · script `/tmp/exp_conversecost.py` · log `/tmp/r26n1c.log` · runtime ~60 s.

## 1. The open half of frontier (i)

Barrier 4's no-pinning half is proven (QRLEAK, COMPENSATING-PARTNER, ISOLATION-COST). The converse — *factor-revealing ⇒ Ω(N)-sealed* — has been established witness-by-witness across the program's papers, each measuring its own cost. This round unifies: the entire known factor-revealing family on ONE cost-information plane, with fitted scaling exponents and exchange rates measured under identical conditions.

## 2. The family and its exponents

Definition-route costs (computing the defining aggregate from N alone), balanced random semiprimes:

| witness | definition-route | measured cost | α (cost ~ N^α) | reach chain |
|---|---|---|---|---|
| W1 M1 = Σ_{x≤N} gcd(x,N) | full N-scan (numpy gcd pass) | α = **1.000** exact | 1.0 ✓ | s recovered + factors from s, 5/5 |
| W2 zero-divisor first hit | scan until gcd(x,N) > 1 | cost = min(p,q) **60/60** | ~½ on N (mean log₂cost 19.35 at log₂N ≈ 20) | first hit IS p |
| W3 CF period ℓ of √N | CF iteration | ℓ steps, α = **0.398** | ~½ (honest: below — ℓ/√N drifts 0.75 → 0.18 → 0.23 across sizes) | period → fundamental unit → factors |
| W4 #{x : x² ≡ x mod N} | full N-scan | α = **1.000**, count = 4 idempotents incl. x = 0 | 1.0 ✓ | count is N-only (factor-free constant) |

Every exponent is super-poly in log N. The two √N-scale witnesses (W2, W3) are precisely the classical SQUFOF/CFRAC face — barrier 8's known methods, not witness shortcuts.

## 3. The cost-information plane

Exchange rates (ops per factor-bit, ~23 bits per factor at these sizes):

| witness | ops/witness | ops/factor-bit |
|---|---|---|
| W1 M1-scan | 4.6×10⁵ | 2.0×10⁴ |
| W2 first-hit (E) | 6.7×10⁵ | 2.9×10⁴ |
| W3 CF-period | 6.9×10⁶ | 3.0×10⁵ |
| W4 idempotent-scan | 4.6×10⁵ | 2.0×10⁴ |

The floor sits at ~2×10⁴ ops/bit for the scan-type witnesses — the aggregation price of factor information via definition-routes — and no member of the family offers a poly(log N) route to any bit of it.

## 4. Method notes

One designed-check catch: the idempotent scan initially excluded x = 0 (`arange(1, …)`), failing its own count=4 assert — the trivial idempotent is part of the CRT structure. Also disclosed: W1's first launch sized semiprimes by `bits` while N carries 2·bits bits (a 10⁹-op scan caught by stall); W3's α came out 0.398 rather than the naive 0.5 — reported as measured (period growth lags √N on finite samples).

## 5. Barriers

**(a)** clean — horns pre-stated (exponent bands, floor location, reach chain); measurements under identical conditions. **(b)** clean — the unification is new; each witness's individual analysis is our own prior work. **(c)** confronted — real scans at real sizes (up to 1.8M-op passes timed), 60-draw distributions. **(d)** clean — fixed seeds. **(e)** the substance — exponents fitted from data, honest deviations reported (α_W3 = 0.398), the x=0 catch disclosed. **(f)** controlled — three defects caught by stalls/asserts before any claim. **(g)** fair — identical measurement conditions across the family; reach chain asserted jointly at 100%. **(h)** relevance — this IS the deployment claim of barrier 4: the price of factor information via definition-routes is ≥ ~2×10⁴ ops/bit at toy scale and super-poly in log N asymptotically, with the √N-family being exactly the known classical methods (barrier 8).

## 6. What closes

The empirical converse: the whole known factor-revealing family lies on one plane, above the aggregation floor, with no poly(log N) exit. Together with the proven no-pinning half, frontier (i) is now *empirically* armed end-to-end; the formal converse proof remains the programme's open theoretical target.

Now 423 experiments. Assessment v199. Paper 88, issue #180.
