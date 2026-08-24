# exp569b U9-DRIFT-POWER-B (round-75 #3) — third independent seed, long run

VERDICT: RANDOMNESS-EXTENDED per pre-registration (both cuts' CIs cover 1);
three-seed JOINT refines the sub-1 question to the exact 95% boundary.

Run facts: wall 5233.6 s (87 min), 76,800,000 pairs (2.15x paper-214 pilot),
128 band-9 semiprimes bitlen-96, seed family SEED+1000+c chunks, precision-
patched script (full-precision rates + raw counts persisted — display defect
of exp569 cannot recur).

This run standalone:
- cut_1e6: r = 0.000485/0.000504 = 0.9623, cluster-boot CI95 [0.9224, 1.004]
- cut_1e5 (primary): r = 3.00e-5/3.057e-5 = 0.981, CI95 [0.8976, 1.0521]

THREE-SEED JOINT — CORRECTED (coordinator self-catch on correlation):
the first pooling (pilot+G1+B inverse-variance, r~0.971 [0.942,1.000]) was
WRONG: runs G1(exp569) and B share the SAME RNG stream (fixed SEED=20260824;
B is a strict superset of G1's draws — first 150k samples/chunk identical).
G1 and B are NOT independent; G1 must not be pooled separately.

CORRECT joint over the only two INDEPENDENT estimates at cut_1e6:
  pilot(paper214) 0.9468 +/- .0449 | B(this, supersedes-G1) 0.9623 +/- .0208
  => joint r ~= 0.9596, sigma ~= 0.0189, 95% CI [0.9226, 0.9966]
  ==> EXCLUDES 1 DOWNWARD at 95%.

Disposition (pre-registration letter vs pooled evidence, both stated):
(1) This run's OWN registered rule: H0 branch — standalone CIs cover 1, no
gate triggered, verdict RANDOMNESS-EXTENDED stands for exp569b as run.
(2) The properly-pooled cross-run signal is a CANDIDATE DEVIATION (~4%
deficit, ~2.1 sigma) whose CONFIRMED status remains BLOCKED because gate G1's
"fresh-seed" requirement was silently violated by the shared-stream design
flaw (disclosed here as a LEDGER CATCH — coordinator error, caught before
publication). The decisive fresh-seed gate is the relaunched c_-run at seed
20260825 (`... full 600000 c_ 20260825`): if its estimate lands below 1 with
the pooled set excluding 1 => CONFIRMED-DEVIATION candidate passes gates
(modulo control-integrity audit); if it returns to 1 => the pooled exclusion
was pilot/B fluctuation and randomness stands.

Mechanism note: a candidate-side DEFICIT is opposite in sign to paper 136's
sieve-advantage direction (QR compensation); if real it is a new weak
u~10-scale effect — full skepticism until seed 20260825 lands.

Mechanism note for interpretation: a candidate-side deficit direction is the
OPPOSITE of the sieve-advantage direction paper 136 found for x^2-N pools
(QR restriction compensates); if the ~3% is real it is a new, weak, u~10-scale
effect — treat with full skepticism until the fourth seed lands.

Files: exp569_u9_drift_power.py (patched), exp569_b_result.json (canonical,
full precision + raw counts), exp569b_full.log.
