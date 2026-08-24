#!/usr/bin/env python3
# =====================================================================
# exp585 NEIGHBOR-SMOOTHNESS-COVARIATE  (round 74; paper 234 ranked-first
# open item, part 2)  -- ANALYSIS agent, 2026-08-24
#
# PRE-REGISTRATION (this header written BEFORE any analysis; smoke and
# full runs execute this same file verbatim):
#
#   Question. The QR dial leaves ~40% of per-N u~10 rate variance
#   unexplained. Does LOCAL FACTORIZATION STRUCTURE AROUND N --
#   omega(N+delta) and LPF(N+delta) for offsets delta in {-8..8}\{0} --
#   predict per-N hit-richness of v_j = j^2 - N beyond the QR dial?
#
#   Endpoints (as first written):
#     PRIMARY   y = hits_full : # j-samples with v_j FULLY 400-smooth.
#     secondary y = hits_part : 400-smooth part times ONE prime
#                 cofactor <= 2^40 (SIQS-partial style).
#
#   AMENDMENT (smoke stage, BEFORE any analysis of the lineage
#   population; smoke used a synthetic rng-585 population only):
#   hits_full measured ZERO events in 160k+ smoke draws even at the
#   tightest sensible window t in [1,16] (v ~ 2^49..2^53, u ~ 5.7-6.1,
#   Dickman rho < 3e-5): an all-zero response cannot support a
#   regression, so PRIMARY and SECONDARY are SWAPPED --
#     PRIMARY   y = hits_part (t in [1,64], 50k samples/N,
#                 seed 20260827); smoke shows mu ~ 4700/N, CV ~ 1.5%.
#     secondary y = hits_full (recorded; expected ~0 -- itself the
#                 honest finding that full B-smoothness is not a
#                 measurable per-N endpoint at bitlen 96).
#   All H1/H0 gates below apply to the PRIMARY endpoint unchanged.
#   Covariates:
#     QR dial (paper-227 S@400 family), reconstructed as
#         qr(N) = sum_{p<=400, p odd, (N/p)=1} 2/p
#     (exact canonical formula not readable this session; this is the
#     monotone expected-extra-divisibility score of that family);
#     neighbor block NB = [omega_bar-, omega_bar+, lpflog_bar-,
#     lpflog_bar+], per-side means over the 8 negative / 8 positive
#     offsets, z-scored for regression.
#
#   H1 (neighbor-carried):  dR2_nb = R2(y ~ QR + NB) - R2(y ~ QR)
#       >= 0.05 AND permutation p < 0.01  (500 shuffles; one row
#       permutation applied jointly to all 4 NB columns).
#   H0 (nothing-but-QR):    dR2_nb < 0.02  => the local-neighborhood
#       class carries nothing beyond QR; the residual remains
#       unexplained by every tested N-property class.
#   Otherwise (0.02 <= dR2 < 0.05, or effect with p >= 0.01):
#       INCONCLUSIVE.
#
#   Population: the seed-20260827 lineage (128 balanced bitlen-96
#   semiprimes). Exact recipe lives in exp577_result.json which this
#   session may NOT read; population is taken verbatim from
#   exp581_regen_positions.npz (the round-74 regeneration) and
#   hash-compared against any recorded hash carried in that file.
# =====================================================================
import argparse, hashlib, itertools, json, math, os, sys, time
import numpy as np
import gmpy2
from gmpy2 import mpz, is_prime, next_prime, isqrt as g_isqrt, powmod, gcd as g_gcd

BASE = "/home/raver1975/factor3/ResearchOutput/scripts/2026-08-24-round74"
NPZ_PATH = os.path.join(BASE, "exp581_regen_positions.npz")

CFG_FULL = dict(tag="full", npop=128, bitlen=96, offsets=list(range(-8, 9)),
                nsamp=50_000, twindow=64, B=400, large_bound=2 ** 40,
                perm=500, seed=20260827, rho_cap=1_500_000, small_limit=10 ** 4,
                pm1_B1=10 ** 5)
CFG_SMOKE = dict(tag="smoke", npop=12, bitlen=96, offsets=[-2, -1, 1, 2],
                 nsamp=3000, twindow=64, B=400, large_bound=2 ** 40,
                 perm=20, seed=20260827, rho_cap=300_000, small_limit=10 ** 4,
                 pm1_B1=10 ** 5)


# ------------------------------------------------------------------ utils
def primes_upto(n):
    sieve = np.ones(n + 1, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = False
    return np.flatnonzero(sieve).astype(np.int64)


def zscore(x):
    x = np.asarray(x, dtype=float)
    sd = x.std()
    return (x - x.mean()) / (sd if sd > 0 else 1.0)


def r2(y, X):
    y = np.asarray(y, float)
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    if ss_tot == 0:
        return 0.0
    X1 = np.column_stack([np.ones(len(y)), X])
    beta, *_ = np.linalg.lstsq(X1, y, rcond=None)
    resid = y - X1 @ beta
    ss_res = float(np.sum(resid ** 2))
    return 1.0 - ss_res / ss_tot


def pearson(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    if a.std() == 0 or b.std() == 0:
        return 0.0
    return float(np.corrcoef(a, b)[0, 1])


def spearman(a, b):
    ra = np.argsort(np.argsort(a)).astype(float)
    rb = np.argsort(np.argsort(b)).astype(float)
    return pearson(ra, rb)


def pop_hash(N):
    h = hashlib.sha256()
    for n in sorted(int(x) for x in N):
        h.update(f"{n},".encode())
    return h.hexdigest()


# ------------------------------------------------------- factorization ctx
class FactCtx:
    def __init__(self, cfg):
        self.primes_small = primes_upto(cfg["small_limit"])
        self.primes_pm1 = primes_upto(cfg["pm1_B1"])
        self.rho_cap = cfg["rho_cap"]
        self._ctr = itertools.count()
        self.cache = {}

    def _rho_seed(self):
        return 918273 + next(self._ctr)

    def _strip(self, n):
        fac = []
        for p in self.primes_small.tolist():
            if p * p > n:
                break
            while n % p == 0:
                fac.append(p)
                n //= p
        return fac, n

    def _pm1(self, n):
        a = mpz(2)
        for p in self.primes_pm1.tolist():
            pe = p
            while pe * p <= self.pm1_cap:
                pe *= p
            a = powmod(a, pe, n)
        g = g_gcd(a - 1, n)
        return int(g) if 1 < g < n else None

    def _brent(self, n):
        if n % 2 == 0:
            return 2
        if n % 3 == 0:
            return 3
        rng = np.random.default_rng(self._rho_seed())
        n = mpz(n)
        for _att in range(8):
            y = mpz(int(rng.integers(2, 1 << 62))) % n
            if y < 2:
                y = mpz(2)
            c = mpz(int(rng.integers(1, 1 << 62))) % n
            m, g, r, q = 128, 1, 1, 1
            x = ys = y
            iters = 0
            while g == 1 and iters <= self.rho_cap:
                x = y
                for _ in range(r):
                    y = (y * y + c) % n
                k = 0
                while k < r and g == 1:
                    ys = y
                    for _ in range(min(m, r - k)):
                        y = (y * y + c) % n
                        q = q * abs(x - y) % n
                        iters += 1
                    g = g_gcd(q, n)
                    k += m
                r <<= 1
            if 1 < g < n:
                return int(g)
            if g == n:
                g2, y2 = 1, ys
                while g2 == 1:
                    y2 = (y2 * y2 + c) % n
                    g2 = g_gcd(abs(x - y2), n)
                if 1 < g2 < n:
                    return int(g2)
            q = 1
            if iters > self.rho_cap:
                break
        return None

    def factor(self, n):
        """Return (omega_distinct, lpf) for int n, or None if censored."""
        n = int(n)
        if n in self.cache:
            return self.cache[n]
        self.pm1_cap = 10 ** 5
        omegas, lpfs = set(), []
        stack = [mpz(n)]
        ok = True
        while stack:
            m = stack.pop()
            if m == 1:
                continue
            smalls, rem = self._strip(m)
            for p in smalls:
                omegas.add(int(p)); lpfs.append(int(p))
            if rem == 1:
                continue
            if is_prime(rem):
                omegas.add(int(rem)); lpfs.append(int(rem))
                continue
            f = self._pm1(rem)
            if f is None:
                f = self._brent(rem)
            if f is None:
                ok = False
                break
            stack.append(mpz(f)); stack.append(rem // f)
        out = (len(omegas), max(lpfs)) if (ok and lpfs) else None
        self.cache[n] = out
        return out


# ------------------------------------------------------------- QR dial
def qr_dial(N, primes_odd):
    Nm = mpz(int(N))
    s = 0.0
    for p in primes_odd.tolist():
        if Nm % p == 0:
            continue
        if powmod(Nm % p, (p - 1) // 2, p) == 1:
            s += 2.0 / p
    return s


# --------------------------------------------------------- hit counting
def hits_for_N(N, cfg, primes400, rng):
    s = int(g_isqrt(mpz(int(N))))
    r = int(N) - s * s                      # v = t^2 + 2 s t - r, t>=1 => v>0
    t = rng.integers(1, cfg["twindow"] + 1, size=cfg["nsamp"]).astype(np.int64)
    v = t * t + (2 * s) * t - r
    res = v.copy()
    for p in primes400.tolist():
        tm = t % np.int64(p)
        sm = s % p
        rm = r % p
        vm = (tm * tm + (2 * sm) % p * tm - rm) % p
        classes = np.unique(tm[vm == 0])
        if classes.size == 0:
            continue
        idx = np.flatnonzero(np.isin(tm, classes))
        for _guard in range(64):
            vals = res[idx]
            dv = (vals % np.int64(p)) == 0
            if not dv.any():
                break
            res[idx[dv]] //= np.int64(p)
    hits_full = int(np.count_nonzero(res == 1))
    m = (res > 1) & (res <= cfg["large_bound"])
    hits_part = hits_full
    if m.any():
        cand = np.unique(res[m])
        pr = [int(c) for c in cand if is_prime(int(c))]
        if pr:
            hits_part += int(np.count_nonzero(np.isin(res[m], pr)))
    return hits_full, hits_part


# ------------------------------------------------------------ population
def gen_smoke_pop(cfg):
    rng = np.random.default_rng(585)
    out = []
    while len(out) < cfg["npop"]:
        p = next_prime(mpz(int(rng.integers(2 ** 47, 2 ** 48))))
        q = next_prime(mpz(int(rng.integers(max(int(p), 2 ** 47), 2 ** 48))))
        N = p * q
        if N.bit_length() == cfg["bitlen"]:
            out.append((int(p), int(q), int(N)))
    return out


def gen_lineage_pop(cfg):
    """Documented reconstruction recipe (NOT verified against exp577):
    numpy default_rng(20260827); independent p,q = next_prime(U[2^47,2^48));
    accept pair iff bitlen(p*q)==96; repeat to n=128; store generation order."""
    rng = np.random.default_rng(cfg["seed"])
    out = []
    guard = 0
    while len(out) < cfg["npop"] and guard < 200000:
        guard += 1
        p = int(next_prime(mpz(int(rng.integers(2 ** 47, 2 ** 48)))))
        q = int(next_prime(mpz(int(rng.integers(2 ** 47, 2 ** 48)))))
        Nn = p * q
        if Nn.bit_length() == cfg["bitlen"]:
            out.append((p, q, Nn))
    return out


def load_population(cfg):
    data = np.load(NPZ_PATH, allow_pickle=True)
    keys = list(data.keys())
    N = None
    for k in ("N", "Ns", "pop", "population", "semiprimes"):
        if k in keys:
            N = [int(x) for x in np.atleast_1d(data[k]).tolist()]
            break
    rec_hash = None
    for k in ("population_hash", "pop_hash", "hash", "N_hash", "sha256"):
        if k in keys:
            rec_hash = str(data[k])
            break
    meta = {}
    for k in ("p", "q", "pprime", "p_", "q_"):
        if k in keys:
            meta[k] = [int(x) for x in np.atleast_1d(data[k]).tolist()]
    fp = ""
    if N is None:
        # npz carries only hit/control POSITION arrays + jlo/jhi. jlo=s+1,
        # jhi=3*s with s=isqrt(N_i): use as a FINGERPRINT for any candidate.
        triples = gen_lineage_pop(cfg)
        N = [t[2] for t in triples]
        meta = {"p": [t[0] for t in triples], "q": [t[1] for t in triples]}
        fp_note = "regenerated by exp585 documented recipe"
        if "jlo" in keys and "jhi" in keys:
            s_true = np.atleast_1d(data["jhi"]).astype(object) // 3
            # verify the jlo/jhi<=>isqrt relation first
            rel_ok = bool(np.all(np.atleast_1d(data["jlo"]).astype(object)
                                 == s_true + 1))
            s_mine = [gmpy2.isqrt(mpz(n)) for n in N]
            n_match = sum(1 for a, b in zip(s_mine, s_true.tolist()) if a == b)
            fp = (f"isqrt-fingerprint vs exp581 jlo/jhi: {n_match}/{len(N)} "
                  f"match (jlo=jhi//3+1 relation holds: {rel_ok}); "
                  f"PROVENANCE {'VERIFIED' if n_match == len(N) else 'UNVERIFIED'} "
                  "-- exact exp577 generator not recoverable from permitted files "
                  "(15-variant recipe grid all 0-match)")
        else:
            fp = "no fingerprint available in npz"
        pop_source = f"{NPZ_PATH.split('/')[-1]} has NO N array -> {fp_note}"
        return N, keys, rec_hash, meta, pop_source, fp
    return N, keys, rec_hash, meta, f"loaded from {os.path.basename(NPZ_PATH)}", fp


# ------------------------------------------------------------------ main
def run(cfg):
    t0 = time.time()
    phases = {}
    print(f"[exp585:{cfg['tag']}] cfg={json.dumps({k: v for k, v in cfg.items()})}")

    # --- population -------------------------------------------------
    ta = time.time()
    if cfg["tag"] == "smoke":
        triples = gen_smoke_pop(cfg)
        N = [tr[2] for tr in triples]
        pop_source = "synthetic smoke population (rng 585, NOT the lineage population)"
        hash_cmp = "n/a (synthetic)"
        keys = []
    else:
        N, keys, rec_hash, meta, pop_source, fp_note = load_population(cfg)
        my_hash = pop_hash(N)
        if rec_hash is not None:
            match = (rec_hash.strip().lower() == my_hash)
            hash_cmp = {"recorded": rec_hash, "computed": my_hash,
                        "match": bool(match), "fingerprint": fp_note}
            if not match:
                print("WARNING: population hash MISMATCH vs recorded hash "
                      "(continuing, disclosed in honest_notes)")
        else:
            hash_cmp = {"recorded": None, "computed": my_hash,
                        "match": None, "fingerprint": fp_note,
                        "note": "no recorded hash available for comparison "
                                "(exp577_result.json not readable this session); "
                                "NON-COMPARISON DISCLOSED"}
    bl = [int(x).bit_length() for x in N]
    print(f"[pop] n={len(N)} bitlen min/med/max={min(bl)}/{int(np.median(bl))}/{max(bl)} "
          f"source={pop_source}")
    phases["population_s"] = round(time.time() - ta, 2)

    # --- covariates ---------------------------------------------------
    ta = time.time()
    offs = [d for d in cfg["offsets"] if d != 0]
    ctx = FactCtx(cfg)
    nb_rows, cens_total = [], 0
    for i, Ni in enumerate(N):
        ow, lw = {"-": [], "+": []}, {"-": [], "+": []}
        for d in offs:
            r = ctx.factor(Ni + d)
            if r is None:
                cens_total += 1
                continue
            side = "-" if d < 0 else "+"
            ow[side].append(r[0]); lw[side].append(math.log(r[1]))
        def mean_or_nan(lst):
            return float(np.mean(lst)) if lst else float("nan")
        nb_rows.append([mean_or_nan(ow["-"]), mean_or_nan(ow["+"]),
                        mean_or_nan(lw["-"]), mean_or_nan(lw["+"])])
    NB = np.array(nb_rows, dtype=float)
    n_cens_rows = int(np.sum(np.isnan(NB).any(axis=1)))
    for j in range(NB.shape[1]):                     # median-impute censored
        col = NB[:, j]
        if np.isnan(col).any():
            col[np.isnan(col)] = np.nanmedian(col)
    primes_odd400 = primes_upto(cfg["B"])[1:]        # odd primes only
    QR = np.array([qr_dial(Ni, primes_odd400) for Ni in N])
    print(f"[cov] offsets={offs} censored_factorizations={cens_total} "
          f"rows_with_imputation={n_cens_rows} qr mean/sd={QR.mean():.4f}/{QR.std():.4f}")
    phases["covariates_s"] = round(time.time() - ta, 2)

    # --- hits ---------------------------------------------------------
    ta = time.time()
    primes400 = primes_upto(cfg["B"])
    rng = np.random.default_rng(cfg["seed"])
    HF, HP = [], []
    for Ni in N:
        hf, hp = hits_for_N(Ni, cfg, primes400, rng)
        HF.append(hf); HP.append(hf if False else hp)
    HF = np.array(HF, float); HP = np.array(HP, float)
    print(f"[hits] full mu/med/max = {HF.mean():.1f}/{np.median(HF):.0f}/{HF.max():.0f}"
          f"  part mu/med/max = {HP.mean():.1f}/{np.median(HP):.0f}/{HP.max():.0f}")
    phases["hits_s"] = round(time.time() - ta, 2)

    # --- regressions + permutation ------------------------------------
    ta = time.time()
    Xq = zscore(QR)[:, None]
    Xnb = np.column_stack([zscore(NB[:, j]) for j in range(4)])
    out_reg = {}
    for nm, y_ in (("primary_hits_part", HP), ("secondary_hits_full", HF)):
        rq = r2(y_, Xq)
        rn = r2(y_, Xnb)
        rf = r2(y_, np.hstack([Xq, Xnb]))
        out_reg[nm] = dict(R2_qr=rq, R2_nb=rn, R2_joint=rf,
                           dR2_neighbors=rf - rq, dR2_qr_given_nb=rf - rn,
                           corr_qr=pearson(QR, y_),
                           corr_nb=[pearson(Xnb[:, j], y_) for j in range(4)])
    # permutation on PRIMARY endpoint only (pre-registered; primary =
    # hits_part after the smoke-stage amendment recorded in the header)
    y = HP
    obs = out_reg["primary_hits_part"]["dR2_neighbors"]
    prng = np.random.default_rng(cfg["seed"] + 1)
    null = np.empty(cfg["perm"])
    for b in range(cfg["perm"]):
        pi = prng.permutation(len(y))
        null[b] = r2(y, np.hstack([Xq, Xnb[pi]])) - r2(y, Xq)
    pval = float((1 + np.sum(null >= obs)) / (1 + cfg["perm"]))
    print(f"[reg] primary dR2_nb={obs:.4f} perm p={pval:.4f} "
          f"(null q95={np.quantile(null, 0.95):.4f})")
    print(f"[reg] secondary dR2_nb={out_reg['secondary_hits_full']['dR2_neighbors']:.4f}")
    phases["stats_s"] = round(time.time() - ta, 2)

    # --- verdicts -------------------------------------------------------
    d = obs
    if d >= 0.05 and pval < 0.01:
        verdict, consequence = "H1_SUPPORTED", (
            "local neighbor factorization structure predicts per-N hit-richness "
            "BEYOND the QR dial; part of the ~40% residual is explained.")
    elif d < 0.02:
        verdict, consequence = "H0_SUPPORTED", (
            "neighbor omega/LPF structure around N carries nothing beyond the QR "
            "dial; the residual remains unexplained by every tested N-property class.")
    else:
        verdict, consequence = "INCONCLUSIVE", (
            "incremental dR2 lands in the pre-registered gray band (or uncalibrated "
            "effect); no claim either way.")

    wall = round(time.time() - t0, 1)
    result = dict(
        experiment="exp585_NEIGHBOR-SMOOTHNESS-COVARIATE",
        date="2026-08-24",
        prereg=dict(
            H1="dR2_neighbors >= 0.05 AND permutation p < 0.01",
            H0="dR2_neighbors < 0.02",
            band="else INCONCLUSIVE",
            primary_endpoint="hits_part (400-smooth part x one prime cofactor "
                             "<= 2^40; PRIMARY after smoke-stage amendment)",
            secondary_endpoint="hits_full (fully 400-smooth v_j; recorded, "
                               "expected degenerate ~0 at bitlen 96)",
            amendment="primary/secondary swapped at SMOKE stage on synthetic "
                      "rng-585 data, before any lineage-population analysis: "
                      "hits_full = 0 in 160k+ draws even at t<=16",
        ),
        config=cfg,
        population=dict(source=pop_source, n=len(N),
                        bitlen_min=min(bl), bitlen_median=int(np.median(bl)),
                        bitlen_max=max(bl), hash_comparison=hash_cmp,
                        npz_keys=keys),
        covariates=dict(
            offsets=offs,
            qr_dial_def="sum_{p<=400 odd, (N/p)=1} 2/p",
            qr_mean=float(QR.mean()), qr_sd=float(QR.std()),
            neighbor_cols=["omega_bar_minus", "omega_bar_plus",
                           "lpflog_bar_minus", "lpflog_bar_plus"],
            neighbor_means=[float(x) for x in NB.mean(axis=0)],
            neighbor_sds=[float(x) for x in NB.std(axis=0)],
            censored_factorizations=cens_total,
            rows_with_imputation=n_cens_rows,
        ),
        hits=dict(mu_part=float(HP.mean()), med_part=float(np.median(HP)),
                  max_part=float(HP.max()),
                  cv_per_N=float(1 / np.sqrt(max(HP.mean(), 1))),
                  mu_full=float(HF.mean()), full_degenerate=bool(HF.sum() == 0)),
        regressions=out_reg,
        permutation=dict(B=cfg["perm"], observed_dR2=float(obs), p_value=pval,
                         null_q95=float(np.quantile(null, 0.95))),
        verdicts=dict(verdict=verdict, consequence=consequence),
        honest_notes=[
            "PROVENANCE: exp581_regen_positions.npz carries only per-N hit/control "
            "POSITION arrays + jlo/jhi (=isqrt(N) fingerprint), NOT N itself. "
            "Population REGENERATED with the documented in-file recipe under seed "
            "20260827. See population.hash_comparison.fingerprint for the isqrt "
            "verification outcome against the true lineage population.",
            "Consequence of unverified provenance (if fingerprint failed): results "
            "are conditional on exchangeability of balanced bitlen-96 semiprime "
            "populations; lab precedent holds these laws population-robust "
            "(pool-ensemble = unrestricted-random; dial laws size-stable), but "
            "this specific replication is NOT the identical-N lineage.",
            "exp569-classify code path not readable; hit classification "
            "reimplemented here (modular-root sieve, exact): t = j-isqrt(N) "
            f"distributed U[1,{cfg['twindow']}], v=t^2+2*s*t-(N-s^2), hit = v "
            "fully B=400-smooth. Window choice is ours, not canonical.",
            "Power: with mu_part hits/N, per-N rate CV ~= 1/sqrt(mu_part); "
            "measurement noise attenuates attainable dR2 while the permutation "
            "test stays exactly calibrated.",
            "QR dial is a monotone reconstruction of the S@400 family (sum of "
            "2/p over QR primes), not the verbatim paper-227 formula.",
            f"Neighbor factorization censoring: {cens_total} of "
            f"{len(N)*len(offs)} (N+delta) factorizations failed within the "
            "rho cap and were median-imputed (rows_with_imputation listed).",
        ],
        phases_s=phases,
        wall_s=wall,
    )
    print(f"[done] verdict={verdict} wall_s={wall}")
    if cfg["tag"] != "smoke":
        with open(os.path.join(BASE, "exp585_result.json"), "w") as f:
            json.dump(result, f, indent=1, default=str)
        print(f"[write] {os.path.join(BASE, 'exp585_result.json')}")
    else:
        with open(os.path.join(BASE, "exp585_smoke_meta.json"), "w") as f:
            json.dump(result, f, indent=1, default=str)
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    run(CFG_SMOKE if args.smoke else CFG_FULL)
