# Paper 230 — POSITIONAL-RATE-LINK: H0 INDEPENDENT LAYERS — Hit-Rich and Hit-Poor Ns Carry Statistically Indistinguishable Positional Profiles (Interaction LRT χ² = 51.31 on df = 49, p = 0.383 with Permutation Confirmation p = 0.34 and 0/49 Wald Bins; Pooled Rich-Poor KS D = 0.0462 Clears Raw p = 0.0038 but FAILS the Registered Bonferroni Bar at p_adj = 0.049; Profiles Near-Identical Across Terciles While the Edge-Decile Excess REPLICATES UNIVERSALLY at 0.229/0.245/0.230): Paper 228's Positional Entry and Rate Entry Remain TWO SEPARATE Map Layers

**Verdict name: H0-INDEPENDENT-LAYERS** (pre-registered). Companion analysis (b) of two recorded
together: pure re-analysis of `exp578_positions.npz`, answering paper 228's named follow-up (b) —
*does j-local structure predict WHICH N are hit-rich, linking the positional view to the rate
view?* No new physics. Round-80 #2 · exp 580 · sources:
`ResearchOutput/scripts/2026-08-24-round74/exp580_positional_rate_link.py` (pre-registration in
header BEFORE any split/profile/KS/regression was computed) → `exp580_result.json`,
`exp580_findings.md`; wall 30.5 s, single run after plumbing fixes (no result changed).

## Setup

Data verbatim: exp578's 128 balanced bitlen-96 semiprimes (master seed 20260828), 9594 hits;
u = (j − jlo)/(jhi − jlo). Ns terciled by per-N hit count: **poor ≤ 64 / mid 64–80 / rich ≥ 80**
(sizes **42/42/44**; counts range 29–136, mean 74.95). Two registered test families on the
TREATMENT arm with a matched CONTROL arm requirement:

## Pre-registration (verbatim from the script header)

> H1 (profile-rate coupling): hit-rich vs hit-poor positional profiles DIFFER.
>   Fires iff FIRE_A or FIRE_B below (with matched control-arm null):
>     FIRE_A: any of (a) the 3 pairwise pooled two-sample KS tests between tercile hit-position
>       samples (rich-poor, rich-mid, poor-mid) with Bonferroni x3 has p_adj<0.01, or (b) any
>       per-decile KS (10 deciles x 3 pairs, Bonferroni x30) has p_adj<0.01.
>     FIRE_B: joint LRT of the 49 binned-position x richness interaction terms in the logistic
>       regression hits-in-bin ~ rich + bin + rich*bin (rows = N x 50 bins, rich vs poor terciles
>       only, middle excluded; pre-stated) gives chi2 p<0.01 (df=49) CONFIRMED by label-permutation
>       p<0.05 (500 shuffles of the rich label).
>   => positional and rate views are ONE mechanism seen twice …
> H0: profiles identical across rich/poor terciles (neither family fires, or fires only where the
>   control arm also fires) => positional geometry and rate variance are INDEPENDENT layers ->
>   TWO separate map entries.
> CONTROL ARM (must be null): identical split + stats applied to the PAIRED non-hit controls
>   (ctl_*), grouped by their host N's treatment-derived tercile label, SIZE-MATCHED to that N's
>   hit count … degenerate all-4000-count control split pre-disclosed as unusable.

## Result 1 — Family A: NO FIRE

| test | treatment | reading |
|---|---|---|
| pooled KS rich-poor | **D = 0.0462, raw p = 0.0038** → Bonferroni (13 tests) **p_adj = 0.049** | does NOT clear the 0.01 bar |
| pooled KS rich-mid | D = 0.0250, p = 0.208 | null |
| pooled KS poor-mid | D = 0.0473, p = 0.0065 → fails correction | null |
| per-decile minima (30 tests) | best raw p = 0.425 | nothing anywhere near any bar |

The raw rich-poor p is reported as a descriptive hint only — it fails its own registered
correction. Control family A clean (min p_adj = 0.235).

## Result 2 — Family B: NO FIRE, decisively

Logistic occupancy regression `hits-in-bin ~ rich + bin + rich×bin` (86 rows = 43 Ns × 50 bins,
rich vs poor only, middle excluded pre-stated):

| statistic | treatment | control (size-matched) |
|---|---|---|
| joint LRT χ² (df = 49) | **51.31, p = 0.383** | 71.03, p = 0.0215 |
| label permutation (500 shuffles) | **p = 0.34** | **p = 0.012 — FIRES spuriously** |
| Wald bins at p < 0.05 | 0 of 49 (min p = 0.97) | 1 of 49 |

Treatment is FAR from every bar ⇒ H0 does not rest on the control outcome — but the control arm
fired, which is itself an important catch (ledger item 1).

## Result 3 — the profiles are near-identical; the edge excess replicates universally

Across terciles the profile SHAPES match closely: bin-1 mass 0.0421/0.0467/0.0411
(rich/mid/poor) with overlapping cluster-bootstrap CIs throughout; and paper 228's beyond-magnitude
edge-decile excess REPLICATES inside every tercile — edge fraction **rich 0.2293 / mid 0.2447 /
poor 0.2299**, each ≈ exp578's pooled 0.2346 and far above both U[0,1] (0.20) and the size-matched
controls (≈0.195–0.202). The positional law of papers 228/229 is a property of EVERY rate class,
not a signature of a hit-rich subclass.

## Post-hoc descriptive (NOT confirmatory — labeled after seeing profiles)

Poor-Ns' hits sit at slightly larger mean_u than rich-Ns': poor 0.4556 vs rich 0.4351 (mid 0.4272);
rich-minus-poor **−0.0205, cluster-boot 95% [−0.0337, −0.0075]**. The SIGN FLIPS in the
matched-control arm (+0.0118 [−0.0034, +0.0266]), which is exactly what a real within-N effect
with a confounded-by-design control would do — but this statistic was chosen AFTER inspecting the
profiles, sits BELOW every registered bar, and is therefore a candidate MOTIVE for a powered
follow-up (e.g. continuous count ~ mean_u correlation), not a map claim.

## Ledger catches (all disclosed)

1. **CONTROL FAMILY B FIRED SPURIOUSLY (perm p = 0.012)** on dense size-matched controls:
   sparse tail bins produce quasi-separation (interaction ORs clipped at e^±30, Wald CIs blow up),
   so the occupancy regression is FRAGILE on controls. The pre-registered decision rule already
   anticipated this direction ("fires only where the control arm also fires" ⇒ H0), treatment was
   nowhere near firing, and the KS family (A) control is clean — so **H0 stands without family B**
   — but design-B must be treated as UNRELIABLE for control arms in future use. This flag travels
   with the paper.
2. Control split degeneracy pre-disclosed BEFORE running: control per-N counts are constant 4000 ⇒
   count-based terciling is degenerate; the registered remedy (host-N labels + size-matched draws,
   one seeded draw per N) was used.
3. Regression outcome is bin OCCUPANCY (≥1 hit), not multiplicity; richness main effect absorbs
   level differences so interactions test SHAPE only; middle tercile excluded from the regression
   by pre-statement (used only in KS pairwise); per-bin Wald p-values exploratory (~50 tests), the
   gated statistic is the joint LRT + permutation.
4. Single seed, single bitlen (96), 128 Ns — inherited from exp578, whose stratified check
   established the profile is real beyond magnitude conditioning; no fresh population drawn.
5. Wall 30.5 s single run "after plumbing fixes (no result changed)" — findings-file disclosure;
   no partial-completion ambiguity in the JSON.

## Joint consequence — SEPARATE LAYERS, one now law-complete

Together with companion paper **229**: the positional layer of paper 228 now carries a LAW
(harmonic power-law profile T(x) ≈ 0.0295·(1+x)^(−1.104) whose bulk IS the Dickman gradient, plus
a ±20% concave mid-window excess hump) — and THIS paper shows that layer does not couple to the
rate layer: the small-j locus does not preferentially concentrate around specific N classes at
these bars. Consequently paper 228's map keeps TWO SEPARATE entries — positional (law-complete,
papers 228/229) and rate — and the ~39–61% unexplained per-N overdispersion of papers
220/222/226/227 is NOT carried by profile-shape heterogeneity across hit-rate terciles: whatever
makes some Ns hit-rich is invisible in WHERE their hits land within j. The unexplained-rate
question returns to N-level covariates, now with a cleaner boundary around it.

## Barrier validation

Serving the standing directive's scale-smoothness mechanism frontier AND the factor-local /
non-QR-per-N-structure open problem: this experiment CLOSES a fork cleanly — had rich/poor
profiles differed, the overdispersion hunt would have merged into positional geometry; instead
both halves are measured and the negative is INFORMATIVE (the residual's carrier must affect HOW
MANY smooth values j²−N produces per N, not where along j they sit). H0-route closed with the pipe
validated on family A controls; family B's control fragility is caught and flagged rather than
silently consumed. Residue cap untouched; no complexity claim; no breakthrough claimed — a clean
independence result with a design lesson attached.

## Bottom line

exp580 asks whether the positional geometry of paper 228 concentrates around hit-rich Ns and gets a
pre-registered NO: interaction LRT χ² = 51.31/49, p = 0.383, permutation p = 0.34, 0/49 Wald bins;
pooled rich-poor KS D = 0.0462 dies at Bonferroni p_adj = 0.049 against a 0.01 bar; profiles are
near-identical across terciles while the edge-decile excess replicates universally (0.229/0.245/
0.230). One genuine catch: the regression design fired SPURIOUSLY on dense size-matched controls
(perm p = 0.012, quasi-separation) — flagged fragile rather than used. A post-hoc mean_u gap
(−0.021 [−0.034, −0.007], sign-flipping under matching) is recorded strictly as motive for a
powered follow-up. Verdict: H0 INDEPENDENT LAYERS — paper 228's positional entry (now law-complete
via paper 229) and its rate entry remain separate, and the ~39–61% overdispersion is not explained
by where hits land within j.
