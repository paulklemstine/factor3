# Paper 93 — JOINT-WALL-VERIFIED: The Battery's Factor-Blindness Stands

**Verdict name: THE-WALL-WAS-BIAS.**
Round-27 #3 · exp 428 · assessment v204 · script `/tmp/exp_jointwall.py` · log `/tmp/r27n3c.log` · runtime ~60 s.

## 1. Closing the loose end

Paper 92's 4-field joint channel read a which-factor statistic of 0.0469 bits — above every pairwise wall — flagged as suspected sparse-plug-in bias but left untested. An untested caveat on a factor-blindness claim is a debt; this round pays it.

## 2. The test

The exact 4-field joint code (S₃a@31 × S₃b@23 × A₄@9 × D₄@8, CRT-chained) against `bigger = [p > q]`, with a 200-shuffle permutation null:

| quantity | value |
|---|---|
| observed I(bigger; joint code) | 0.0469 bits |
| permutation null mean | **0.0469** |
| null sd | 0.0014 |
| z | **+0.05** |

**The entire reading is sparse-plug-in bias.** The joint contingency table spans tens of thousands of residue-columns against 30k samples; the plug-in estimator inflates by exactly the observed amount regardless of which label carries the rows. The 2-field joint was verified in the same run (0.0011 inside its own null).

## 3. What stands

The battery programme's factor-blindness claim — papers 91–92's synergized, overlapped, super-additive joint channels — **stands with its caveat converted into a verified statement**: the battery's full capacity (8.2246 bits at k = 4, ceiling 9.53) is symmetric trace-routed content with zero detectable which-factor leakage at the permutation-null sensitivity (~±0.003 bits).

## 4. Method note

One process catch disclosed: the first verification build chained only two fields (testing the wrong code — 0.0011, trivially inside its null) before extending to the actual 4-field target. Verify the exact object, not a smaller cousin.

Now 428 experiments. Assessment v204. Paper 93, issue #185.
