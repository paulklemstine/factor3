# Paper 91 — DIAL-INDEPENDENCE: The Battery Is Neither Additive Nor Comonotone

**Verdict name: SYNERGY-AND-OVERLAP.**
Round-27 #1 · exp 426 · assessment v202 · script `/tmp/exp_dialindependence.py` · log `/tmp/r27n1c.log` · runtime ~60 s.

## 1. The question

Each field's semiprime type-pair channel was measured separately (papers 78–84). The structural question left open: on ONE shared semiprime population, is the JOINT of two fields' channels additive (independent dials), comonotone (one variable wearing two coats), or something else? The answer decides how rich any congruence battery could be — k dials: k times the bits, less, or more?

## 2. The pre-stated hypothesis and its refutation

The stated-before-run claim was coprime-conductor **additivity**: N mod m₁ ⊥ N mod m₂ ⟹ I(N mod m₁m₂; pair₁, pair₂) = I₁ + I₂ exactly. **Refuted at the first pair** — and the refutation is directional:

| battery | I(joint) | I₁ + I₂ | Δ |
|---|---|---|---|
| S₃a@31 × S₃b@23 | 2.1314 | 2.0024 | **+0.129 (SYNERGY)** |
| A₄@9 × D₄@8 | 1.9125 | 1.9076 | **+0.005 (near-additive)** |
| S₃a@23 × S₃b@23 (shared disc) | 1.0104 | 2.0024 | **−0.992 (OVERLAP)** |

The additivity argument failed because it treated the dial labels as independent draws — but both dials read the **same underlying (p, q)**: their label entropies are population-correlated, so the joint modulus (seeing p mod m₁ and q mod m₂ simultaneously via CRT) extracts combinations neither marginal reaches. Where the synergy lands depends on structure: two S₃ fields (rich 3-type channels over correlated type distributions) synergize at +0.129 bits; A₄×D₄ (one lossy-type field) is nearly additive.

## 3. The overlap measurement

Two cubics with the SAME discriminant −23 share their quadratic character entirely: their joint channel carries **1.0104 bits against 2.0024 summed — an overlap of 0.992 bits**, i.e., essentially one full channel is redundant. Shared conductor structure makes dials comonotone to within noise. This is the quantitative form of "the same quadratic subfield is the same dial".

Which-factor walls hold across every joint channel measured (≤ 0.0016): all synergized and overlapping content remains symmetric, trace-routed, factor-blind.

## 4. Method ledger

One designed-check catch pre-launch (the shared-pool ramification bug — index draws including other fields' ramified primes would KeyError; fixed by excluding the union {31, 23, 2, 3} once), and one honest gate conversion: the naive additivity assert fired at the first pair (+0.129), was converted into a recorded synergy measurement rather than silently loosened, and the refutation became the round's finding.

## 5. Barriers

**(a)** clean — the hypothesis was pre-stated, refuted by measurement, and the replacement claim (synergy-and-overlap structure) fits all three measured batteries. **(b)** clean — no joint-dial work in the Catalog. **(c)** confronted — one shared 30k population, four fields, exact marginal re-verification against papers 80/82 (1.0012/1.0012/0.4733/1.4342 — every prior value reproduced before the joints were measured). **(d)** clean — fixed seeds. **(e)** the substance — synergy and overlap quantified per battery; the marginal-vs-joint distinction that generated the refutation documented. **(f)** controlled — machinery inherited from validated rounds. **(g)** fair — identical population for marginals and joints; walls asserted throughout. **(h)** relevance — the converse's no-pinning scope now covers product batteries with their synergy excesses included: more dials give strictly more symmetric bits (up to overlap discounts), none of it factor-pointing.

## 6. What closes

The battery space is characterized: dials are neither independent nor comonotone but **correlated through the shared factorization they read** — synergy for structurally rich pairs (+0.129), redundancy for shared-structure pairs (−0.992). Any congruence battery's capacity is computable from its dials' joint distribution by exactly the machinery used here, and its content remains on the traced side of barrier 4.

Now 426 experiments. Assessment v202. Paper 91, issue #183.
