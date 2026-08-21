# Paper 99 — THE-SUM-DIFFERENCE-SPLIT: The Factor-Residue Hint Value

**Verdict name: THE-HINT-VALUE-IS-REAL.**
Round-29 #1 · exp 434 · assessment v210 · script `/tmp/exp_sumdiffsplit.py` · log `/tmp/r29n1b.log`.

## 1. The question and the refutation

Each dial's labels are functions of (p mod m\*, q mod m\*), which map bijectively to (s mod m\*, d mod m\*) — sum and gap. The pre-stated hypothesis: the (s,d) view *reconstructs* the product-view channel I(N mod m\*; labels). **Refuted in the interesting direction**: the (s,d) view EXCEEDS it.

## 2. The routing table (S₃a x³+x+1 @31; S₃b replicates)

| view | bits | share of product-view |
|---|---|---|
| product-view (hint-free) = the channel | 1.0012 | 100% |
| sum-view alone (s mod 31) | 0.0391 | 3.9% |
| gap-view alone (d mod 31) | 0.0387 | 3.9% |
| full-residue view (s,d jointly) | 1.5201 | 152% |
| **HINT VALUE = I(s,d) − I(N)** | **+0.5189** | — |

The sum and gap residues **individually carry almost nothing** (~4% each of the channel) — but their **combination carries more than the modulus's own product residue**. The +0.52-bit difference is the **factor-residue hint value**: what knowing s and d separately (equivalently p and q mod 31 — a 2-log₂31-bit factor hint) adds over reading N's residue. S₃b replicates (+0.5099).

## 3. Why this matters

This connects the battery arc to COND-RANK's conditioning-capacity measurements: the hint value quantifies exactly how much label information is locked behind knowing the factor residues — information present in the labels, invisible from N, released only by a factor-residue hint. It also explains the sub-ceiling gaps of papers 80–94 from the other side: the ceiling H(T) counts label entropy; the product-view channel counts what N's residue reaches; the hint value is the bridge.

Anomaly flagged rather than buried: this script's joint-battery product-view reads 0.1353 against paper 91's 2.1314 for the nominally identical quantity — the discrepancy (likely a label-encoding difference in this quick rebuild) is unresolved and the joint row should not be cited until reconciled. The per-dial tables are internally consistent across two independent computations within the run.

## 4. Barriers

**(a)** clean — the reconstruction hypothesis pre-stated and honestly refuted; the replacement measurement (hint value) computed from the same data. **(b)** clean. **(c)** confronted — 30k shared population, two fields, four views each, symmetry verified. **(d)** clean. **(e)** the substance — the refutation directional and interpreted; the anomaly flagged. **(f)** controlled — machinery inherited. **(g)** fair — all views on identical data. **(h)** relevance — the hint value is the exact price of structure-blindness at the residue level, bridging battery capacity to conditioning capacity.

Now 434 experiments. Assessment v210. Paper 99, issue #191.
