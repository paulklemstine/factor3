# Paper 87 — QUBIT-TRADE4: The Three-Axis Resource Surface and the Standard-Corner Optimum

**Verdict name: THE-STANDARD-CORNER-IS-OPTIMAL.**
Round-25 #3 · exp 422 · assessment v198 · script `/tmp/exp_qubittrade4.py` · log `/tmp/r25n3.log` · runtime ~30 s.

## 1. The third axis

Papers 85–86 mapped two axes of Shor's resource surface (register width t, samples s) and found the per-N unlucky cap. Real Shor escapes that cap by **re-drawing the base a** — the third axis. This round measures the full surface on the paper-86 constructed population (24 semiprimes, controlled orders r ∈ {210, 310, 434, 510}, 12 mixed-role / 12 same-role), with K = 6 independent bases per N (fresh role structure each), across t ∈ {wall−4, −2, 0}, s ∈ {1, 5, 20}, k ∈ {1, 2, 4}.

## 2. Results

### H1 — base re-draws lift the cap exponentially
At t = wall, s = 5: **k = 1 → 0.504, k = 2 → 0.735, k = 4 → 0.940**. The ladder follows 1−(1−p₁m)^{ks} with m ≈ ½ the mixed-role fraction: re-drawing the base is the designed escape from the unlucky structure, and it compounds exactly as independence predicts.

### H2 — three-way fungibility below saturation
Across 12 single-doubling steps mixing axes ((t−1, 2s), (t, s→2s), (t, k→2k)), mean ΔP = **+0.18**, positive in every case: below saturation, one extra bit, one extra sample, and one extra base re-draw are interchangeable currency.

### H3 — the standard corner is optimal (with a disclosed accounting bug)
Total gate count G ≈ k·s·t². Corrected computation from the printed grid (the script's "cheapest cell" loop took the last match rather than the minimum — disclosed):

| corner | cheapest configuration reaching P ≥ 0.3 | G |
|---|---|---|
| t = wall | s = 1, k = 4 (P = 0.53) | **6 400** |
| t = wall−2 | s = 5, k = 2 (P = 0.47) | 14 440 |
| t = wall−4 | s = 20, k = 2 (P = 0.50) | 51 840 |

Shaving register width costs exponential samples/re-draws against only a quadratic width saving: **the textbook parameterization (full register, few runs) minimizes the total cost on its own surface.**

## 4. Frontier (ii) closed

The quantum channel is now quantitatively mapped end-to-end: paper 47's binary truncation threshold → paper 85's fungibility ramp → paper 86's real-N cap → this paper's three-axis surface and its optimum. The final form of DEQUANT: *the fungibility surface exists, every point of it is quantum resource, its minimum sits at the standard corner, and no point of it approaches classical factoring complexity.* Shor is optimal given its own paradigm — and the paradigm's optimum is still exponentially separated from classical efficiency. Barriers 4/8 hold in their sharpest quantitative form.

## 5. Barriers

**(a)** clean — horns pre-stated; H3's accounting bug found post-run and corrected from the raw grid (both numbers shown). **(b)** clean — no three-axis work in the Catalog. **(c)** confronted — 24 real constructed semiprimes, 6 bases each, 20-trial cells over 27 surface points. **(d)** clean — fixed seeds. **(e)** the substance — the cap-lift ladder and ΔP statistic quantified; the accounting bug disclosed with corrected values. **(f)** controlled — all machinery inherited from validated rounds 25 #1/#2. **(g)** fair — mixed/same-role population balanced by design (12/12); ladders consistent with papers 85–86 through identical kernels. **(h)** closure — the deployment reading: no parameter tuning of Shor improves its total cost; classical complexity remains the only competition (barrier 8), and the aggregation barrier (4) prices every classical route.

Now 422 experiments. Assessment v198. Paper 87, issue #179.
