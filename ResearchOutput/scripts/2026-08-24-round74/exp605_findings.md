# exp605 PROFILE-GENERALITY (round-74) -- findings
Question: is the j^2-N positional smoothness profile (papers 228/229:
power law + left-edge spike) universal across polynomial families?
Population: 128 npz-lineage members, windows [r_k, 3r_k-4] anchored at
the integer k-th root (k=2 reproduces [jlo,3jlo-3] exactly); matched
CRN grids L=3000/N/arm, exact 1e6-cut gcd-chain tester, controls
C=1000/N/arm. PRE-REG in module header before analysis.

VERDICT: **H0-SIDE (family-specific)** -- bars: pair-r>0.8 FAIL,
edge-concentration PASS (4/4 arms), monotone-decline FAIL (via cu3).
- sq2 (8639 hits, rate .0225): bhat +.157 +-.008, ld/ov 1.24x,
  Spearman -.802 (p=2.5e-12)
- qu4 (7603, .0198): bhat +.188 +-.013, ld/ov 1.29x, Spearman -.856
- cu3 (287, .00075): bhat +.065 +-.037 (CI covers 0), Spearman +.019
  (p=.92) -- FLAT, no positional structure detected (thin: 287 hits)
- sq2d probe (248, .00065): bhat +.168, ld/ov 1.47x, shape-consistent
Pairwise normalized-profile r: sq2|qu4 .781 [CI .57-.77],
sq2|cu3 .385, cu3|qu4 .477, sq2~sq2d .495. Controls flat 4/4
(chi2 p .08-.65). Wall 181 s.

MECHANISM (the finding behind the verdict): rate hierarchy
sq2 ~= qu4 (~2e-2) >> sq2d ~= cu3 (~7e-4, 29-34x lower) is EXACTLY
tracked by difference-of-squares factorability: N_rec=jlo^2 makes
v_k=(j^(k/2)-jlo)(j^(k/2)+jlo) split for EVEN k only. The declining
SHAPE is shared by the two factorable families (bhat .16/.19,
rho -.80/-.86, r .78); odd degree or non-square N collapses to
baseline rate with flat-to-shallow profiles. Positional structure is
gated by ARITHMETIC (algebraic factorability of f(j)-N given N's form),
not polynomial degree per se => NOT a universal law at this scale.

LEDGER CATCHES / HONEST LIMITS:
- Lineage: npz stores positions+bounds only, no N -> byte-exact seed-
  20260828 regeneration impossible from permitted inputs. Applicable
  check: v2=(j-jlo)(j+jlo) is N-independent; stored npz HIT positions
  classify smooth under N_rec at .0226 == ctl .0198 (pure independence)
  => original N were NON-SQUARE; reconstruction APPROXIMATE. Papers'
  population was general-N: sq2/qu4 RATE LEVELS do not transfer there;
  on general-N-like arms the locus is weak (ld/ov <= 1.47, shallow),
  so a strong left-edge power-law on this window needs either exact-
  square N or finer-than-window resolution -- flag for 228/229 follow-up.
- cu3/sq2d hit counts (287/248) just above the pre-registered 150
  low-power floor: their null-ish shapes are underpowered, disclosed.
- Smoke caught t-mat broadcast bug + key-name bug (hit_/ctl_ prefixes);
  both fixed pre-full-run. No commits; only exp605_* touched.
