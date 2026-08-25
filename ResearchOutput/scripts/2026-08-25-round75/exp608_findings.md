# exp608 CONIC-ORDER-RIGIDITY v2 (round-75) -- findings
Fleet Bet #2 empirical legs: do Berggren-tree word orders escape the conic
maximal-torus menu? Pre-registered; positive-control gated.

VERDICTS:
  CL1_WEAK_CONFIRMED -- ZERO violations: every word order divides
    K_p = p(p^2-1) (PGL_2(F_p)) across ALL 550 primes < 4000 x 40 random
    words (length<=8). ONE shared modulus caps ALL words => a tree-word order
    method gets a SINGLE smoothness draw per prime -- no ECM variance. THE SEAL.
  CL1_STRONG_REFUTED -- 4973/22000 words have orders dividing NEITHER
    p(p-1) NOR p(p+1) individually (e.g. order 8 @ p=3): word orders MIX the
    split and non-split tori. The fleet's stronger variant is dead.
  CL2_CONFIRMED -- <M1,M2,M3> mod p projected to PGL_2 has order fitting
    {p(p^2-1)/t} at all 17 primes <=60 (p=7->336, p=13->1092, p=19->6840 =
    exact PGL_2(F_p)).
  CL3_CONTAINED + RATE_PARITY_FAILED_IN_SEALING_DIRECTION --
    micro-audit (600 balanced bits-40 semiprimes, seed 20261107, bands
    SEED+263e6/265e6 above true prior ceiling, per-N matched mpz-mul budgets):
    pm1 225/600, pp1 292/600, TREE ARM 0/600 (tree-only successes: 0;
    strata flat: pm1 113/112, pp1 145/147 across (2/p)). The raw-trace tree
    arm has ZERO factoring leverage where the baselines succeed ~40%.

MECHANISM READING: raw word traces hit fixed targets {1,2} with probability
~2/p => expected ~0.003 successes in 600 trials; zero observed = exactly as
the seal predicts. CAVEAT (disclosed): the registered design omitted the
stage-1 targeting step (tr(W^E)-2 after raising each word to E); a targeted
variant is the TRUE Williams analogue and the seal predicts it behaves like
exactly ONE Williams draw at worse constants (2x2 word products cost more
muls per update AND share one order cap => no independence across words).
Either way the conic menu closes the class.

LEDGER CATCHES (six defects caught pre-evidence by the control gate):
  1. v1 generator family WRONG (3x3 triple-space matrices: det 5, no integral
     invariant Q, mod-p groups huge -> BFS blew 8.6 GB; killed). Correct
     object: GL2(Z) moves on (m,n): [[2,-1],[1,0]], [[2,1],[1,0]],
     [[1,2],[0,1]] -- tree-generation verified EXACT (m<=40, parity-corrected
     primitive pairs 331=331).
  2. Stream-band arithmetic initially under-credited exp606's x1e8 leg
     strides; assertion fired pre-data; bands moved to +263e6/265e6.
  3. Control constants invalid on the exponent lattice twice (3*2^18+1 needs
     2^18 | E; E=lcm(1..500) carries only 2^8) -> controls now SEARCHED with
     exact lattice divisibility.
  4. pm1 scalar exponentiation started x=a before squaring on the leading bit
     (double-counts MSB) -> silently computed wrong exponents; found BY THE
     CONTROL.
  5. Lucas matrix ladder multiplied R by A every bit without squaring R ->
     computed tr(A^bitlen(E)); k=5 passed BY ACCIDENT, k=13 exposed it.
  6. Williams mechanics nuance booked: pp1 success requires a seed whose
     discriminant a^2-4 is a NON-RESIDUE mod p (alpha then lives in the
     norm-1 F_{p^2} torus); all-residue seed sets legitimately produce zero.
PROCESS LAW VALIDATED: positive controls are mandatory machinery gates --
six bugs, six catches, zero corrupted evidence.

Wall ~90 s. Sources: exp608_conic_order_rigidity.py (v2),
exp608_result.json, exp608_run.log.
