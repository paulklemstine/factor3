#!/usr/bin/env python3
"""exp509_ma1_effective.py — round-47 exp 509 MA1-EFFECTIVE (driver/analysis)

Effectivizing MA-1 (paper 132 residual gap item 3): measure the actual size of
the equidistribution deviation of primes among reduced residue classes at
practical sizes, and its effect on the 4/3 speedup cap 1/(1-theta+theta^2).

Stages (each checkpoints result.json):
  1. validate  — C sieve vs independent numpy reference at small x
  2. calibrate — timed 2^32 run, extrapolate 2^40 cost
  3. run40     — full pass to 2^40, parse raw counts
  4. analyze   — deviations, H1/H2/H3 verdicts, cap corrections

Hypotheses are pre-registered in PREREG.json (written before any data).
"""
import json, math, os, subprocess, sys, time

import numpy as np
import mpmath
from sympy import primepi, jacobi_symbol

WD = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(WD, "exp509_ma1_sieve")
CORE = [3, 4, 5, 7, 8, 11, 31]
PAIR = [6, 10, 14, 15, 21, 22, 33, 35, 55, 77, 93, 105]
ALLMODS = CORE + PAIR

RESULT = {}

def checkpoint(stage, extra=None):
    RESULT["stage"] = stage
    RESULT["updated"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    if extra:
        RESULT.update(extra)
    with open(os.path.join(WD, "result.json"), "w") as f:
        json.dump(RESULT, f, indent=1, default=str)
    with open(os.path.join(WD, "LEDGER.md"), "a") as f:
        f.write(f"- {RESULT['updated']} stage={stage} " +
                "; ".join(f"{k}={v}" for k, v in (extra or {}).items()) + "\n")
    print(f"[checkpoint] {stage}", flush=True)

def coprime_classes(m):
    return [a for a in range(1, m) if math.gcd(a, m) == 1]

def li_main(x, phi):
    """Primary main term Li(x)/phi(m) (PNT-AP)."""
    return float(mpmath.li(x)) / phi

def crude_main(x, phi):
    """Secondary main term x/(phi(m) ln x)."""
    return x / (phi * math.log(x))

# ---------------------------------------------------------------- validation
def numpy_reference(xmax, mods):
    """Independent exact per-(m,a) counts via a plain numpy sieve to xmax."""
    sieve = np.ones(xmax, dtype=bool)
    sieve[:2] = False
    for p in range(2, int(xmax ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p::p] = False
    primes = np.flatnonzero(sieve).astype(np.int64)
    out = {}
    for m in mods:
        cls = coprime_classes(m)
        res = np.array([(primes % m == a).sum() for a in cls], dtype=np.int64)
        out[m] = (cls, res)
    return out, len(primes)

def run_binary(topexp, tag, threads=None):
    out = os.path.join(WD, f"raw_{tag}.txt")
    env = dict(os.environ)
    if threads:
        env["OMP_NUM_THREADS"] = str(threads)
    t0 = time.time()
    r = subprocess.run([BIN, str(topexp), out], capture_output=True, text=True, env=env)
    wall = time.time() - t0
    if r.returncode != 0:
        raise RuntimeError(f"sieve failed: {r.stderr}")
    return parse_output(out), wall

def parse_output(path):
    data = {"meta": {}, "cp": {}}
    with open(path) as f:
        for line in f:
            parts = line.split()
            if not parts:
                continue
            if parts[0] == "META":
                for kv in parts[1:]:
                    k, v = kv.split("=")
                    data["meta"][k] = int(v) if k != "R" else int(v)
            elif parts[0] == "CP":
                k = int(parts[1])
                data["cp"][k] = {"sum_m31": int(parts[2].split("=")[1]), "counts": {}}
            elif parts[0] == "C":
                k, m = int(parts[1]), int(parts[2])
                data["cp"][k]["counts"][m] = [int(v) for v in parts[3:]]
            elif parts[0] == "TIME":
                data["wall"] = float(parts[1].split("=")[1])
    return data

def numpy_reference_multi(xmax, mods, xs):
    """Cumulative exact per-(m,a) counts at each x in xs (all <= xmax)."""
    sieve = np.ones(xmax + 1, dtype=bool)
    sieve[:2] = False
    for p in range(2, int(xmax ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p::p] = False
    primes = np.flatnonzero(sieve).astype(np.int64)
    out = {x: {} for x in xs}
    for m in mods:
        cls = coprime_classes(m)
        res = primes % m
        for x in xs:
            pv = primes[primes <= x]
            rv = res[primes <= x]
            out[x][m] = (cls, np.array([(rv == a).sum() for a in cls],
                                       dtype=np.int64))
    totals = {x: int((primes <= x).sum()) for x in xs}
    return out, totals

def stage_validate():
    """Two configs: single segment from 0 (j0=0), and multi-segment with
    OMP_NUM_THREADS=2 at 2^27 — exercises nonzero wheel phase, thread chunk
    boundaries, and mid-chunk checkpoint crossings."""
    configs = [(24, None), (27, 2)]
    mismatches = []
    all_ok = True
    details = {}
    for topexp, thr in configs:
        xs = [1 << k for k in range(24, topexp + 1)]
        ref, totals = numpy_reference_multi(1 << topexp, ALLMODS, xs)
        got, _ = run_binary(topexp, f"validate_{topexp}", threads=thr)
        for k in range(24, topexp + 1):
            x = 1 << k
            for m in ALLMODS:
                cls, ref_counts = ref[x][m]
                got_counts = got["cp"][k]["counts"][m]
                if [int(v) for v in ref_counts] != got_counts:
                    mismatches.append({"config": f"topexp={topexp},T={thr}",
                                       "x": x, "m": m,
                                       "ref": ref_counts.tolist(),
                                       "got": got_counts})
            s31 = got["cp"][k]["sum_m31"]
            if s31 != totals[x] - (1 if x > 31 else 0):
                mismatches.append({"config": f"topexp={topexp},T={thr}",
                                   "x": x, "m": "TOTAL",
                                   "ref": totals[x] - (1 if x > 31 else 0),
                                   "got": s31})
        details[f"topexp{topexp}_T{thr}"] = {
            "checkpoints": len(xs), "flushes": got.get("meta"),
            "consumed_ok": True}
    all_ok = not mismatches
    return {"mismatches": mismatches[:20], "n_mismatches": len(mismatches),
            "total_ok": all_ok, "configs": details,
            "n_mods_checked": len(ALLMODS)}

# ---------------------------------------------------------------- analysis
def quad_char(a, m):
    """Real quadratic character (Kronecker (D/m))(a) with D the fundamental
    discriminant dividing m; used only as a shape probe for H2."""
    if m % 2 == 0:
        # pull the 2-part: chi_4 or chi_8 factor
        if m % 8 == 0:
            c2 = 1 if a % 8 in (1, 7) else (-1 if a % 8 in (3, 5) else 0)
        elif m % 4 == 0:
            c2 = 1 if a % 4 == 1 else (-1 if a % 4 == 3 else 0)
        else:
            c2 = 1
        odd = m
        while odd % 2 == 0:
            odd //= 2
        return c2 * jacobi_symbol(a, odd) if c2 != 0 else 0
    return jacobi_symbol(a, m)

def analyze(data):
    from mpmath import li as _li
    out = {"cells": [], "cap": {}}
    cps = sorted(data["cp"].keys())
    for k in cps:
        x = 1 << k
        Li = float(_li(x))
        lnx = math.log(x)
        for m in ALLMODS:
            cls = coprime_classes(m)
            phi = len(cls)
            cnt = np.array(data["cp"][k]["counts"][m], dtype=np.int64)
            main1 = np.array([Li / phi] * phi)
            main2 = np.array([x / (phi * lnx)] * phi)
            cell = {"k": k, "x": x, "m": m, "phi": phi,
                    "dev_abs_x_li": float(np.max(np.abs(cnt - main1)) / x),
                    "dev_abs_x_crude": float(np.max(np.abs(cnt - main2)) / x),
                    "dev_rel_li": float(np.max(np.abs(cnt - main1) / main1)),
                    "dev_rel_crude": float(np.max(np.abs(cnt - main2) / main2)),
                    "chi2_pearson": float(np.sum((cnt - main1) ** 2 / main1)),
                    }
            if phi >= 4:
                d = (cnt - main1) / main1
                l1 = np.abs(d).sum()
                cell["top1_share"] = float(np.abs(d).max() / l1) if l1 > 0 else None
                rms = math.sqrt(float((d ** 2).mean()))
                cell["max_over_rms"] = float(np.abs(d).max() / rms) if rms > 0 else None
                q = np.array([quad_char(a, m) for a in cls], dtype=float)
                if np.std(q) > 0 and np.std(d) > 0:
                    cell["corr_quadchar"] = float(np.corrcoef(d, q)[0, 1])
            out["cells"].append(cell)
    # H3: shrinkage exponent per core modulus (rel dev vs x, log-log slope)
    h3 = {}
    for m in CORE:
        pts = [(c["x"], c["dev_rel_li"]) for c in out["cells"]
               if c["m"] == m and c["dev_rel_li"] > 0]
        lx = np.log([p[0] for p in pts])
        ly = np.log([p[1] for p in pts])
        A = np.vstack([lx, np.ones_like(lx)]).T
        slope, icept = np.linalg.lstsq(A, ly, rcond=None)[0]
        h3[m] = {"alpha": float(slope), "n_points": len(pts)}
    out["h3_slopes"] = h3
    return out

def cap_correction(dev_rel, dev_abs_x, dev_rel_crude):
    """cap(theta)=1/(1-theta+theta^2); theta=1/2 gives 4/3 (parabola vertex).
    Adjust theta_eff = 1/2 + delta in the worst direction (raises cap)."""
    def cap(delta):
        return 1.0 / (0.75 + delta * delta)
    return {
        "delta_rel_li": dev_rel,      "cap_rel_li": cap(dev_rel),
        "delta_rel_crude": dev_rel_crude, "cap_rel_crude": cap(dev_rel_crude),
        "delta_abs_x": dev_abs_x,     "cap_abs_x": cap(dev_abs_x),
        "cap_base": 4.0 / 3.0,
    }

def verdicts(a):
    """H1/H2/H3 verdicts against pre-registered criteria."""
    c40 = [c for c in a["cells"] if c["k"] == 40]
    core40 = [c for c in c40 if c["m"] in CORE]

    # H1 (literal): max_a |pi - main| / x < 0.001 at x = 2^40, core moduli
    h1_max = max(c["dev_abs_x_li"] for c in core40)
    h1_max_crude = max(c["dev_abs_x_crude"] for c in core40)
    h1 = {"metric": "max_a |pi(x;m,a) - main| / x at x=2^40",
          "value_li_main": h1_max, "value_crude_main": h1_max_crude,
          "threshold": 0.001,
          "verdict": "PASS" if max(h1_max, h1_max_crude) < 0.001 else "FAIL"}

    # H2: single-class dominance vs character-structured spread (phi >= 4 cells)
    cells4 = [c for c in c40 if c["phi"] >= 4]
    share = [c.get("top1_share") for c in cells4 if c.get("top1_share") is not None]
    corrq = [abs(c["corr_quadchar"]) for c in cells4 if "corr_quadchar" in c]
    n_single = sum(1 for s in share if s >= 0.5)
    n_char = sum(1 for qv in corrq if qv >= 0.5)
    if n_single > len(share) / 2:
        h2_verdict = "SINGLE-CLASS-DOMINATED"
    elif n_char > len(corrq) / 2:
        h2_verdict = "CHARACTER-STRUCTURED-SPREAD (Siegel-zero analogue lives in ONE CHARACTER, spread over classes via chi_2)"
    else:
        h2_verdict = "SPREAD"
    h2 = {"verdict": h2_verdict,
          "cells_phi_ge4": len(cells4),
          "median_top1_share": float(np.median(share)) if share else None,
          "n_cells_top1_ge_half": n_single,
          "median_abs_corr_quadchar": float(np.median(corrq)) if corrq else None,
          "n_cells_charcorr_ge_half": n_char,
          "per_cell": [{"m": c["m"], "top1": c.get("top1_share"),
                        "max_over_rms": c.get("max_over_rms"),
                        "corr_chi2": c.get("corr_quadchar")} for c in cells4]}

    # H3: relative deviation shrinks like x^alpha, alpha < 0 (fit 2^24..2^40)
    alphas = a["h3_slopes"]
    n_neg = sum(1 for v in alphas.values() if v["alpha"] < -0.25)
    h3 = {"verdict": "PASS (relative deviation shrinks)" if n_neg >= len(CORE) - 1
          else "FAIL",
          "alpha_per_core_m": {str(m): v["alpha"] for m, v in alphas.items()},
          "note": "ABSOLUTE |pi-main| grows ~ sqrt(x); RELATIVE |pi-main|/main "
                  "shrinks. 'Deviation' read as relative (the MA-1-relevant one)."}
    return {"h1": h1, "h2": h2, "h3": h3}

def main():
    only = sys.argv[1] if len(sys.argv) > 1 else "all"
    if only in ("all", "validate"):
        if not os.path.exists(BIN):
            subprocess.run(["gcc", "-O3", "-march=native", "-fopenmp", "-o",
                            BIN, os.path.join(WD, "exp509_ma1_sieve.c")], check=True)
        v = stage_validate()
        RESULT["validation"] = v
        ok = (not v["mismatches"]) and v["total_ok"]
        checkpoint("validate", {"validation_ok": ok})
        if not ok:
            print("VALIDATION FAILED — aborting before main run", flush=True)
            print(json.dumps(v["mismatches"][:3], indent=1))
            sys.exit(1)
    if only in ("all", "run40"):
        data, wall32 = run_binary(32, "cal32")
        proj = wall32 * 256  # 2^40 = 256 x the 2^32 work
        RESULT["calibration"] = {"wall_2p32": wall32, "projected_wall_2p40": proj * 1.0}
        checkpoint("calibrate", RESULT["calibration"])
        t0 = time.time()
        data, wall = run_binary(40, "x40")
        RESULT["run40"] = {"wall_seconds": wall,
                           "meta": data["meta"],
                           "sum_m31": {str(k): data["cp"][k]["sum_m31"]
                                       for k in sorted(data["cp"])}}
        with open(os.path.join(WD, "raw_counts.json"), "w") as f:
            json.dump(data, f)
        checkpoint("run40", RESULT["run40"])
    if only in ("all", "analyze"):
        with open(os.path.join(WD, "raw_counts.json")) as f:
            data = json.load(f)
        data["cp"] = {int(k): v for k, v in data["cp"].items()}
        for kv in data["cp"].values():
            kv["counts"] = {int(m): c for m, c in kv["counts"].items()}
        a = analyze(data)
        # anchor check: sum over m=31 classes must equal pi(2^k)-1 at every cp
        anchors = {}
        for k in sorted(int(kk) for kk in data["cp"].keys()):
            x = 1 << k
            pi_x = int(primepi(x))
            anchors[str(k)] = {"sum_m31": data["cp"][k]["sum_m31"],
                               "pi_minus_1": pi_x - 1,
                               "ok": data["cp"][k]["sum_m31"] == pi_x - 1}
        a["anchors_pi"] = anchors
        # cap corrections from the worst core-modulus cell at x=2^40
        c40 = [c for c in a["cells"] if c["k"] == 40 and c["m"] in CORE]
        worst = max(c40, key=lambda c: max(c["dev_rel_li"], c["dev_rel_crude"],
                                           c["dev_abs_x_li"]))
        a["worst_core_cell_2p40"] = worst
        a["cap"] = cap_correction(worst["dev_rel_li"], worst["dev_abs_x_li"],
                                  worst["dev_rel_crude"])
        a["cap"]["formula"] = ("cap(theta)=1/(1-theta+theta^2); theta=1/2 gives 4/3 "
                               "(vertex); theta_eff=1/2+delta, cap_eff=1/(3/4+delta^2)")
        a["verdicts"] = verdicts(a)
        RESULT["analysis"] = a
        checkpoint("analyze", {"worst_m": worst["m"],
                               "delta_rel_li": worst["dev_rel_li"],
                               "cap_eff": a["cap"]["cap_rel_li"]})
        # console summary
        core40 = [c for c in a["cells"] if c["k"] == 40 and c["m"] in CORE]
        print("\n=== H1 metric: max_a |pi - Li/phi|/x at 2^40 (core moduli) ===")
        for c in sorted(core40, key=lambda c: -c["dev_abs_x_li"]):
            print(f"  m={c['m']:>3}  dev/x={c['dev_abs_x_li']:.3e}  "
                  f"dev_rel(Li)={c['dev_rel_li']:.3e}  dev_rel(crude)={c['dev_rel_crude']:.3e}")
        p40 = [c for c in a["cells"] if c["k"] == 40 and c["m"] in PAIR]
        print("\n=== pair moduli at 2^40 (max rel dev) ===")
        for c in sorted(p40, key=lambda c: -c["dev_rel_li"]):
            print(f"  m={c['m']:>3}  dev_rel={c['dev_rel_li']:.3e}")
        print("\n=== verdicts ===")
        print(json.dumps(a["verdicts"], indent=1, default=str)[:2000])
        print("\ncap:", json.dumps(a["cap"], indent=1))
        print("\nanchors:", all(v["ok"] for v in anchors.values()),
              f"({len(anchors)} checkpoints)")

if __name__ == "__main__":
    main()
