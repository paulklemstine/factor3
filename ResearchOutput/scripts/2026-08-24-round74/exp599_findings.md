# exp599 CONSECUTIVE-V-DEPENDENCY (round-74) -- findings
Question (exp598 routing): after j-arithmetic carriers died, do mid-window hits
correlate at NEIGHBORING positions in the v/j sequence, or are hit events
independent given position (excess = pure density)?
Data: exp581_regen_positions.npz ONLY (hit_i = hit j-positions per batch,
ctl_i = 4000 control positions, jlo/jhi windows, 128 batches, 9594 hits;
no N stored -> purely positional point-process analysis; frac inside window 1.000).

VERDICT: **H0_PURE_DENSITY** -- no sequence-level structure; positional thread closes.
- PRIMARY (position-conditioned, quadratic-detrended within [0.55,0.75], nb=1000):
  rho(lag) in [-0.0199,-0.0023] over lags 1-20; max |rho| = 0.020 << 0.05 bar;
  cluster-over-Ns bootstrap CI halfwidth <=0.013, every CI straddles 0;
  MC-vs-density-curve p per lag 0.128-0.969. ZERO lags fire.
- SECONDARY (literal global-mean): rho in [-0.0103,+0.0046] -- even more null.
- RUNS: textbook pooled Wald-Wolfowitz Z=+0.850 (p~0.40); MC-calibrated against
  pooled empirical rate curve Z=+0.894 (p~0.37) -- nowhere near p<0.001.
- Lag profile is FLAT and slightly negative (no refractory/excitation either way).
- Robustness: nb=500 max|rho_det|=0.036, nb=2000 0.016 -- no binning artifact.

Controls (pre-committed expectations, all met):
- C1 ctl batches identical treatment: null (max |rho| 0.009 raw / 0.020 det).
- C2 synthetic smooth-hump iid at pooled rate curve: does NOT fire (max 0.014)
  -> Amendment-0 curvature confound quantitatively immaterial at this resolution;
  conditioned and literal readings AGREE, verdict not amendment-dependent.
- C3 injected lag-1 dependence: rho_det(lag1)=0.337, detected massively
  -> a null here means "no dependency", not "test blind".

Consequence plainly: given position, mid-window hits carry NO information about
neighboring positions -- the u*~0.65 excess is fully explained by the smooth
positional density curve (rate heterogeneity only); any future gain must come
from modeling the density curve itself, not from sequential/Markov structure.

Honest: seed-20260828 ctl regeneration attempted (2 canonical recipes) -- both
MISMATCH ctl_0; recipe not recoverable from allowed reads, provenance rests on
sha256 0b1afa509e6b2720...; MC null approximates shared pooled rate across
batches (per-batch rate spread carried by cluster bootstrap instead).

Wall 31.4s (smoke n=16 1.3s); boot 2000 + MC 2000 reps, seed lineage 599_20260828;
no commits; only exp599_* touched.
