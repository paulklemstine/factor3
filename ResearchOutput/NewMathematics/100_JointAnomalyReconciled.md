# Paper 100 — JOINT-ANOMALY-RECONCILED: Paper 91 Stands, the Rebuild Collapsed

**Verdict name: THE-ORIGINAL-STANDS.**
Round-29 #2 · exp 435 · assessment v211 · script `/tmp/exp_jointreconcile.py` · log `/tmp/r29n2.log` · runtime 5 s.

## 1. The anomaly

Paper 99 flagged a 16× discrepancy: its rebuild of the S₃a@31 × S₃b@23 joint channel read 0.1353 bits against paper 91's recorded 2.1314. An unreconciled discrepancy on a load-bearing number is intolerable; this round ran both constructions side-by-side on the identical population.

## 2. The reconciliation

| construction | distinct labels | H(labels) | I(joint) |
|---|---|---|---|
| paper 91 (`pj = pc_a·10000 + pc_b`) | **36** | 4.6006 | **2.1314** |
| clean-code cross-check | 36 | 4.6006 | **2.1314** |
| paper 99 rebuild (`lab = pc_a·100 + (min·10 + max)`) | **18** | 3.6073 | 0.5830 |

**Paper 91's number is correct**: the clean-code computation reproduces 2.1314 exactly, and the marginals re-verify (I(a) = I(b) = 1.0012). The paper-99 rebuild's label chaining (`·10` compression of the S₃b code inside a `·100` frame) **collided distinct label pairs into shared codes** — 18 distinct labels instead of 36, destroying 0.99 bits of label entropy and, with it, most of the measurable channel. The rebuild's low reading was an encoding artifact, not physics.

## 3. The resolution

- **Paper 91's 2.1314 stands** as the correct S₃a×S₃b joint capacity.
- **Paper 99's flagged anomaly row is retracted**: its 0.1353 measured a collision-degraded encoding, and the "joint-battery product-view" comparison that motivated the flag was invalid (the rebuild measured a corrupted object).
- Paper 99's per-dial routing tables (sum/gap/hint-value) are unaffected — they involve single dials only, and their internally-consistent double computations stand.
- Programme lesson recorded: **chained integer label encodings must be width-checked against their field sizes** — a `·10` frame for a 3-valued code inside a `·100` frame for a 6-valued code silently merges classes. The audit practice of paper 97 (re-run keystone scripts fresh) is what caught this one's sibling.

Now 435 experiments. Assessment v211. Paper 100, issue #192.
