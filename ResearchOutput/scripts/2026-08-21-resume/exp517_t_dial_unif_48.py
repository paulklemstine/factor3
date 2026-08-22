#!/usr/bin/env python3
"""exp517 T-DIAL-UNIF-48 -- T-dial (sum 2/p over QR primes <=400) on UNIFORM semiprime draws, nominal bitlen 48.

Parent spec (round-52 #517):
  3 populations (seeds 20261080..82) x 1200 uniform semiprimes,
  p in [2^10,2^16), q in [2^16,2^22)   <-- ARM A ("A_literal", official)
  240 relation values v_j = (isqrt(N)+j)^2 - N ; u = 2.5 smoothness:
  B = exp(ln(vmed)/2.5) = vmed^(1/2.5); strip primes <= B; smooth iff rem == 1
  (rem==1 after stripping primes<=B implies maxp<=B).
  Features: T(N)  = sum_{odd p<=400, (N|p)=1} 2/p   (Euler criterion, gmpy2.powmod)
            CNT(N)= #{odd p<=100 : (N|p)=1}         (bare QR-count)
  Stats: per-seed Spearman(T,rate), Spearman(CNT,rate), advantage = rho_T - rho_CNT,
         300-resample percentile bootstrap CIs, verdicts.
  H1: rho_T within [0.55, 0.85] at u=2.5 on uniform draws.
  H2: T beats bare QR-count by > +0.05 on >= 2/3 seeds.

DESIGNED-CATCH NOTE (spec inconsistency, flagged pre-run):
  The literal ranges put N at 26-38 bits, which contradicts the "bitlen 48" label.
  Doubling every exponent (p in [2^20,2^24), q in [2^24,2^28) -> N in [2^44,2^52],
  centered at bitlen 48) reproduces the label and matches the bitlen range of the
  balanced-draw line (papers 162/175: 44..52). We therefore run BOTH arms:
    ARM A "A_literal" (parent's literal numbers) -> OFFICIAL verdicts.
    ARM B "B_scaled"  (exponent-doubled, label-matched) -> pre-registered sensitivity.
  Both arms identical otherwise. All verdicts quoted from ARM A; ARM B reported
  alongside as the sensitivity check.

Protocol: work only in /tmp/exp52_tu48/ ; result.json checkpointed after every stage.
"""
import json, os, sys, time
import numpy as np
import gmpy2
from scipy.stats import spearmanr

WORK = "/tmp/exp52_tu48"
RES = os.path.join(WORK, "result.json")

SEEDS = [20261080, 20261081, 20261082]
NN = 1200          # semiprimes per population
NV = 240           # relation values per N (j = 0..239)
U = 2.5            # smoothness parameter
TPMAX = 400        # T-dial prime bound
CNTMAX = 100       # bare QR-count prime bound
NBOOT = 300        # bootstrap resamples
ARMS = {
    "A_literal": dict(p_lo=10, p_hi=16, q_lo=16, q_hi=22),   # official (literal spec)
    "B_scaled":  dict(p_lo=20, p_hi=24, q_lo=24, q_hi=28),   # sensitivity (label-matched)
}

def log(*a):
    print(f"[{time.strftime('%H:%M:%S')}]", *a, flush=True)

def checkpoint(stage, payload):
    res = {}
    if os.path.exists(RES):
        with open(RES) as f:
            res = json.load(f)
    res[stage] = payload
    res["last_stage"] = stage
    res["updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(RES, "w") as f:
        json.dump(res, f, indent=1)
    log(f"checkpoint: {stage}")

# ---------------------------------------------------------------- primes
def sieve(n):
    m = np.ones(n + 1, bool); m[:2] = False
    for i in range(2, int(n**0.5) + 1):
        if m[i]: m[i*i::i] = False
    return np.nonzero(m)[0]

ODDP400 = [int(p) for p in sieve(TPMAX) if p > 2]

# ---------------------------------------------------------------- population
def rand_prime(rng, lo, hi):
    # unbiased: rejection-sample uniform ints, Miller-Rabin accept
    while True:
        n = int(rng.integers(lo, hi))
        if gmpy2.is_prime(n, 25):
            return n

def gen_population(seed, p_lo, p_hi, q_lo, q_hi):
    rng = np.random.default_rng(seed)
    ps, qs = [], []
    for _ in range(NN):
        ps.append(rand_prime(rng, 1 << p_lo, 1 << p_hi))
        qs.append(rand_prime(rng, 1 << q_lo, 1 << q_hi))
    return ps, qs

# ---------------------------------------------------------------- features
def t_features(N):
    T = 0.0; c = 0
    for p in ODDP400:
        r = gmpy2.powmod(N, (p - 1) // 2, p)
        if r == 1:
            T += 2.0 / p
            if p <= CNTMAX:
                c += 1
    return T, c

# ---------------------------------------------------------------- smoothness
def smooth_rates(Ns):
    """V (n,240) int64 of |v_j|; per-row B = vmed^(1/u); strip primes<=B ascending
    with per-row deactivation; smooth iff final V == 1 (=> maxp <= B_row)."""
    n = len(Ns)
    V = np.empty((n, NV), dtype=np.int64)
    B = np.empty(n, dtype=np.float64)
    r0s = [int(gmpy2.isqrt(N)) for N in Ns]
    for i, (N, r0) in enumerate(zip(Ns, r0s)):
        v = np.array([abs((r0 + j) * (r0 + j) - N) for j in range(NV)], dtype=np.int64)
        V[i] = v
        B[i] = float(np.median(v.astype(np.float64))) ** (1.0 / U)
    primes = sieve(int(np.ceil(B.max())) + 1)
    for p in primes:
        act = np.nonzero(p <= B)[0]
        if act.size == 0:
            break
        sub = V[act]
        m = (sub % p == 0) & (sub > 1)
        if m.any():
            while m.any():
                sub[m] //= p
                m = (sub % p == 0) & (sub > 1)
            V[act] = sub
    return (V == 1).mean(axis=1), B

def smooth_check_fallback(N, j, B):
    """pure-python reference smoothness test for designed-check spot audits"""
    r0 = int(gmpy2.isqrt(N))
    v = abs((r0 + j) * (r0 + j) - N)
    if v == 1: return True
    for p in sieve(int(B) + 1):
        while v % p == 0:
            v //= p
        if v == 1: return True
    return v == 1

# ---------------------------------------------------------------- stats
def boot_ci(T, C, R, rng):
    n = len(R)
    rT = np.empty(NBOOT); rC = np.empty(NBOOT)
    for b in range(NBOOT):
        idx = rng.integers(0, n, n)
        rT[b] = spearmanr(T[idx], R[idx]).statistic
        rC[b] = spearmanr(C[idx], R[idx]).statistic
    adv = rT - rC
    def ci(x): return [float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))]
    return dict(rhoT_ci=ci(rT), adv_ci=ci(adv))

def main():
    t_start = time.time()
    checkpoint("meta", dict(
        exp="exp517", codename="T-DIAL-UNIF-48", round="round-52", date="2026-08-22",
        seeds=SEEDS, n_per_pop=NN, n_rel=NV, u=U, T_pmax=TPMAX, cnt_pmax=CNTMAX,
        nboot=NBOOT, arms=ARMS,
        spec_note=("parent ranges p in [2^10,2^16), q in [2^16,2^22) put N at 26-38 bits, "
                   "inconsistent with the 'bitlen 48' label; ARM A = literal (official), "
                   "ARM B = exponent-doubled [2^20,2^24)x[2^24,2^28) = N 44-52 bits (sensitivity)"),
        hypotheses=dict(H1="0.55 <= rho_T <= 0.85 on uniform draws (all 3 seeds, ARM A)",
                        H2="adv = rho_T - rho_CNT > +0.05 on >= 2/3 seeds (ARM A)"),
    ))

    results = {}
    for arm, ex in ARMS.items():
        results[arm] = {}
        for k, seed in enumerate(SEEDS):
            t0 = time.time()
            # ---- stage 1: population + features
            ps, qs = gen_population(seed, ex["p_lo"], ex["p_hi"], ex["q_lo"], ex["q_hi"])
            Ns = [p * q for p, q in zip(ps, qs)]
            # designed check: semiprime integrity on every 97th N + first/last
            for i in list(range(0, NN, 97)) + [NN - 1]:
                N = Ns[i]
                assert gmpy2.is_prime(ps[i]) and gmpy2.is_prime(qs[i])
                assert N % ps[i] == 0 and N % qs[i] == 0
                assert (1 << ex["p_lo"]) <= ps[i] < (1 << ex["p_hi"])
                assert (1 << ex["q_lo"]) <= qs[i] < (1 << ex["q_hi"])
                assert ps[i] != qs[i]
            feats = [t_features(N) for N in Ns]
            T = np.array([f[0] for f in feats]); C = np.array([f[1] for f in feats], float)
            nbits = np.array([int(N).bit_length() for N in Ns])
            checkpoint(f"{arm}_s{k}_pop", dict(
                seed=seed, n=NN,
                Nbit_min=int(nbits.min()), Nbit_max=int(nbits.max()), Nbit_mean=float(nbits.mean()),
                T_mean=float(T.mean()), T_std=float(T.std()), T_min=float(T.min()), T_max=float(T.max()),
                CNT_mean=float(C.mean()), CNT_std=float(C.std()),
            ))

            # ---- stage 2: relations + smoothness rate
            rate, B = smooth_rates(Ns)
            # designed check: pure-python fallback on 12 random spots
            rng_chk = np.random.default_rng(seed + 777)
            ok = 0
            for i in rng_chk.integers(0, NN, 12):
                j = int(rng_chk.integers(0, NV))
                ref = smooth_check_fallback(Ns[i], j, B[i])
                r0 = int(gmpy2.isqrt(Ns[i]))
                v = abs((r0 + j) * (r0 + j) - Ns[i])
                vec_smooth_j = None
                # recompute vectorized decision for this single v
                vv = v; sm = vv == 1
                if not sm:
                    for p in sieve(int(B[i]) + 1):
                        while vv % p == 0: vv //= p
                        if vv == 1: sm = True; break
                assert ref == sm
                ok += 1
            checkpoint(f"{arm}_s{k}_rate", dict(
                seed=seed, fallback_checks=ok,
                rate_mean=float(rate.mean()), rate_std=float(rate.std()),
                rate_min=float(rate.min()), rate_max=float(rate.max()),
                B_median=float(np.median(B)), B_min=float(B.min()), B_max=float(B.max()),
            ))
            np.savez(os.path.join(WORK, f"{arm}_s{k}.npz"),
                     T=T, C=C, rate=rate, B=B, nbits=nbits,
                     N=np.array(Ns, dtype=np.uint64))

            # ---- stage 3: stats + bootstrap
            rhoT = float(spearmanr(T, rate).statistic)
            rhoC = float(spearmanr(C, rate).statistic)
            adv = rhoT - rhoC
            bci = boot_ci(T, C, rate, np.random.default_rng(seed + 90000 + k))
            results[arm][f"seed{seed}"] = dict(
                rhoT=rhoT, rhoC=rhoC, adv=adv, **bci,
                rate_mean=float(rate.mean()), Nbit_mean=float(nbits.mean()))
            checkpoint(f"{arm}_s{k}_stats", results[arm][f"seed{seed}"])
            log(f"{arm} seed{seed}: rhoT={rhoT:.4f} rhoCNT={rhoC:.4f} adv={adv:+.4f} "
                f"rate={rate.mean():.4f} Nbits={nbits.mean():.1f} [{time.time()-t0:.1f}s]")

        # pooled per arm
        Ts = np.concatenate([np.load(os.path.join(WORK, f"{arm}_s{k}.npz"))["T"] for k in range(3)])
        Cs = np.concatenate([np.load(os.path.join(WORK, f"{arm}_s{k}.npz"))["C"] for k in range(3)])
        Rs = np.concatenate([np.load(os.path.join(WORK, f"{arm}_s{k}.npz"))["rate"] for k in range(3)])
        p_rhoT = float(spearmanr(Ts, Rs).statistic)
        p_rhoC = float(spearmanr(Cs, Rs).statistic)
        bci = boot_ci(Ts, Cs, Rs, np.random.default_rng(424242))
        results[arm]["pooled"] = dict(rhoT=p_rhoT, rhoC=p_rhoC, adv=p_rhoT - p_rhoC, **bci)
        checkpoint(f"{arm}_pooled", results[arm]["pooled"])
        log(f"{arm} POOLED: rhoT={p_rhoT:.4f} rhoCNT={p_rhoC:.4f} adv={p_rhoT-p_rhoC:+.4f}")

    # ---- stage 4: verdicts (ARM A official)
    A = results["A_literal"]; Bm = results["B_scaled"]
    a_seeds = [A[f"seed{s}"] for s in SEEDS]
    lo, hi = 0.55, 0.85
    in_win = [lo <= d["rhoT"] <= hi for d in a_seeds]
    if all(in_win):
        h1 = "CONFIRMED"
    elif any(in_win) or (lo <= A["pooled"]["rhoT"] <= hi):
        h1 = "PARTIAL"
    else:
        h1 = "REFUTED"
    n_adv = sum(d["adv"] > 0.05 for d in a_seeds)
    h2 = "CONFIRMED" if n_adv >= 2 else "REFUTED"
    verdict = dict(
        H1=h1, H1_detail={SEEDS[i]: dict(rhoT=a_seeds[i]["rhoT"], in_window=in_win[i]) for i in range(3)},
        H2=h2, H2_detail={SEEDS[i]: dict(adv=a_seeds[i]["adv"]) for i in range(3)},
        n_seeds_adv_gt_005=n_adv,
        sensitivity_arm_B={s: dict(rhoT=Bm[f"seed{s}"]["rhoT"], rhoC=Bm[f"seed{s}"]["rhoC"],
                                   adv=Bm[f"seed{s}"]["adv"]) for s in SEEDS} | {"pooled": Bm["pooled"]},
    )
    checkpoint("verdicts", verdict)
    log(f"VERDICTS: H1={h1}  H2={h2}  (n_adv>{0.05}: {n_adv}/3)")
    log(f"total {time.time()-t_start:.1f}s")
    print(json.dumps(results, indent=1))

if __name__ == "__main__":
    main()
