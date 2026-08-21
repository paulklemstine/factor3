# Paper 86 — QUBIT-TRADE3: The Fungibility Ramp on Real Semiprimes

**Verdict name: THE-RAMP-SURVIVES-CONTACT-WITH-FACTORS.**
Round-25 #2 · exp 421 · assessment v197 · script `/tmp/exp_qubittrade3.py` · log `/tmp/r25n2h.log` · runtime 14 s.

## 1. From abstract periods to actual factors

Paper 85 measured the qubit/sample fungibility ramp on abstract period-finding. This round tests whether it survives when the recovered period must **actually factor a real semiprime**: r = ord_N(a) with certificates converted by gcd(a^{b/2} ± 1, N), over a constructed population of 32 semiprimes with controlled orders r ∈ {210, 310, 434, 510} (primes p ≡ 1 mod r built directly; order-r elements found by projection; **CRT-combined with randomized per-prime orders** d_p, d_q ∈ {r, r/2} so that ord_N(a) = lcm = r while the factoring-relevant role structure varies).

The construction surfaced a structural fact worth stating plainly: if ord_p(a) = ord_q(a) exactly, then a^{r/2} ≡ −1 mod *both* primes and **N never factors from period-r certificates** — the permanently-unlucky case. Real Shor encounters this with probability ~½ per base and simply re-draws a; the experiment builds it into the population deliberately.

## 2. Results

### The ramp survives (factoring metric)
P_factor(s=1) climbs the same ladder: **0.018 → 0.056 → 0.158 → 0.181** across t = wall−4 … wall+2. Certification remains the bottleneck (nocert share 0.3% at/above wall−2 — consistent with paper 85's ramp), and the gcd conversion is free classically.

### Samples compound; a per-N cap binds
s-ladders track independence tightly where the cap allows — wall−2: 0.056 → 0.204 → 0.471 vs 1−(1−0.06)^s = 0.11/0.27/0.46 family — and **saturate at ≈ 0.53**: the product of the certification ramp and the mixed-role population fraction (~⅔). The cap is **per-N structural**: same-role N's (ord_p = ord_q) never factor from period certificates no matter how many samples arrive; only re-drawing a helps. This is the measurable form of Shor's "unlucky base" — and it compresses the exchange law's visibility: t\*(P ≥ 0.5) is reachable only at s = 20 because the ceiling sits barely above 0.5.

### The failure taxonomy (pooled)
| mode | share |
|---|---|
| spurious-or-partial certificate | **0.844** |
| unlucky (a^{r/2} ≡ ±1 both primes) | 0.109 |
| factor found | 0.044 |
| no certificate | 0.003 |

The dominant classical burden is **spurious-certificate filtering** — small denominators pass the 1/(2b²) test constantly — which is precisely the role N-verification plays in the real algorithm. The quantum measurement is rarely the failure point at reasonable t; the classical filter is.

## 3. Method ledger

Four defects caught across six launches, each by a designed gate:
1. **Order blow-up**: naive random semiprimes give r = lcm(p−1, q−1)-scale (~2³⁰), making register simulation impossible → constructed controlled-order semiprimes instead.
2. **Simultaneous-order search impossible** (~10⁻⁷ density) → independent per-prime order elements, CRT-combined (ord_N = lcm guaranteed).
3. **Equal-order construction = permanent unluckiness** (a^{r/2} ≡ −1 mod both primes always) — first measurements were all-zero; randomized roles restore the realistic ½-structure.
4. **Infinite loop on odd half-orders** (`rr % 2 == 0` guard leftover) and **first-certificate early-return** masking later splitting ones — both caught by stall/garbage outputs; plus a hardcoded verdict string replaced by data-computed output before any claim was made.

## 4. Barriers

**(a)** clean — horns pre-stated (ramp persistence, exchange shift, unlucky-half cap, taxonomy); the population design implements the cap rather than assuming it. **(b)** clean — no real-N ramp work in the Catalog. **(c)** confronted — actual semiprimes with exact multiplicative orders, full gcd-based factor extraction, 24-trial cells over a 30-N subset. **(d)** clean — fixed seeds. **(e)** the substance — the cap is measured, not assumed; taxonomy shares quantified; all four defects disclosed. **(f)** controlled — the dishonest-verdict catch (pre-written success text vs contradicting data) replaced by data-computed output. **(g)** fair — nocert/factor shares consistent with paper 85's ramp through the identical kernel; the cap's ⅔-structure is a measured consequence of the constructed roles. **(h)** relevance — this is the deployment metric: Shor's sample-hungry short-register regime factors real N's at the ramp's price, capped by the unlucky-base structure that base re-drawing (cheap classically) removes.

## 5. What closes

The fungibility ramp now extends end-to-end: abstract certification (paper 85) → real factor extraction (this paper) with the same shape, the same independence compounding, and one new structural element — the per-N unlucky cap that sample count cannot move. The quantum channel frontier is quantitatively mapped on both axes; remaining frontier: the barrier-4 converse.

Now 421 experiments. Assessment v197. Paper 86, issue #178.
