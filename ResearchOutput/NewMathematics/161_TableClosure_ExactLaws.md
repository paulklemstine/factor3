# Paper 161 — TABLE-CLOSURE FULL: The Exact Asymptotic Constants of the Fork Channels

**Verdict name: EXACT-CONSTANT-LAWS (X/g → 2log₂e/(log₂e−1); the log-form guesses retired).**
Round-43 #1 (cron iteration) · exp 491-full · assessment v270 · script `ResearchOutput/scripts/2026-08-21-resume/exp491_full_table.py` (+ `exp491_full_result.json`, `table.csv`, `ledger.md`) · mpmath dps=50, verified to n = 655360.

## 1. Paper 160's refuted guess becomes exact law

Paper 160 refuted X → 2g but could only report rising ratios. This computation (mpmath at
dps=50) found the true laws and verified them on fresh n up to 655360 at deviations ≤ 3e-6:

> **g·n² → log₂e − 1 = 0.442695** (no log factor at all)
> **X·n² → 2·log₂e = 2.885390**
> **A·n²/log₂n → 1 exactly**
> **(Is − A)·n² → 2log₂e**, equivalently **Is·n² − log₂n → 2log₂e**
> hence **X/g → 2log₂e/(log₂e−1) = 6.51778**

The author's own pre-data scratch expansion predicted X/g → 2 (same as paper 160's H3) — it
had dropped a −2a² term; the exact table refuted it, the corrected constants were derived
post-hoc, then confirmed out-of-sample. Labeled post-hoc throughout.

Also: all four channels collapse at n=2 (g = A = 0.311278 — reproducing the lab's OR cap;
Is = X = 1.000000); the A/X sign flip lives exactly in (7,8); MC tie at n=17 passes at
z = −0.10.

## 2. What this decides

The fork-channel tables are shut twice over: dominance structure exact to n=25 (paper 160),
asymptotic constants exact to n=655360 (this paper). Barriers: (5)/(8) unchanged.

Now 493 experiments. Assessment v270.
