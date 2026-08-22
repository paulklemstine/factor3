#!/usr/bin/env python3
"""EXP 509 MA1-EFFECTIVE lean v2 (round-48). Exact computation via sympy.
Quantify equidistribution deviations for paper 132's MA-1.
H1: max per-class deviation < 0.001 relative at x=2^30 for m <= 31.
H2: dominated by a single class.
H3: deviation shrinks from smaller to larger x.
"""
import json, time, math
import numpy as np
from sympy import primerange

T0 = time.time()
OUT = {"meta": {"exp": 509, "codename": "MA1-EFFECTIVE-v2"}}
def checkpoint():
    json.dump(OUT, open("/tmp/exp47_ma1/result_v2.json", "w"), indent=1)

results = []
for x_exp in (28, 30):
    x = 2 ** x_exp
    primes = np.array(list(primerange(2, x)), dtype=np.int64)
    total = len(primes)
    print(f"x=2^{x_exp}: {total} primes", flush=True)
    from sympy import li
    li_x = float(li(x))
    for m in (3, 4, 5, 7, 8, 11, 31):
        phi_m = sum(1 for a in range(1, m) if math.gcd(a, m) == 1)
        classes = sorted(set(a for a in range(1, m+1) if math.gcd(a, m) == 1))
        phi = len(classes)
        res = primes % m
        counts = np.array([int((res == a).sum()) for a in classes])
        exp_per_class = total / phi  # empirical mean
        # also theoretical: li(x)/phi(m)
        exp_theory = li_x / phi
        devs = np.abs(counts - exp_per_class) / exp_per_class
        max_dev = float(devs.max())
        worst = int(np.argmax(devs))
        # chi-squared
        chi2 = float(((counts - exp_per_class)**2 / exp_per_class).sum())
        r = dict(m=m, x_exp=x_exp, x=x, phi=phi, total_primes=total,
                 max_dev_rel_empirical=round(max_dev, 6),
                 worst_class=classes[worst],
                 counts=[int(c) for c in counts],
                 expected_per_class=int(exp_per_class),
                 chi2=round(chi2, 2))
        results.append(r)
        OUT.setdefault("cells", []).append(r)
    checkpoint()
    print(f"x_exp={x_exp} done", round(time.time()-T0,1), "s", flush=True)

# H1: max dev < 0.001 at x=2^30
h130 = [r for r in results if r["x_exp"] == 30]
max_dev_30 = max(r["max_dev_rel_empirical"] for r in h130)
# H2: worst class stability across x values
from collections import defaultdict
by_m = defaultdict(list)
for r in results:
    by_m[r["m"]].append((r["x_exp"], r["worst_class"]))
h2_stable = {}
for m, vals in by_m.items():
    wcs = set(wc for _, wc in vals)
    h2_stable[m] = len(wcs) == 1
# H3: deviation shrinks from x_exp=28 to 30
shrink = {}
for m in (3, 4, 5, 7, 8, 11, 31):
    v28 = next(r["max_dev_rel_empirical"] for r in results if r["m"]==m and r["x_exp"]==28)
    v30 = next(r["max_dev_rel_empirical"] for r in results if r["m"]==m and r["x_exp"]==30)
    shrink[m] = v30 < v28
OUT["summary"] = {
    "H1_max_dev_at_30": round(max_dev_30, 6),
    "H1_pass_lt_0.001": max_dev_30 < 0.001,
    "H2_worst_stable": h2_stable,
    "H3_shrinking": shrink}
checkpoint()
print(json.dumps(OUT["summary"]))
print("DONE", round(time.time()-T0,1), "s")
