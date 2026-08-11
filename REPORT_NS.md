# REPORT NS — Navier–Stokes / Turbulence Factoring Exploration

**Date:** 2026-08-11
**Full report:** `~/lean/Catalog/ResearchOutput/Exp_NavierStokes.md`
**Code:** `~/factor3/ns_factoring.py`
**Verdict:** **REFUTED** — new instance of the structural orthogonality barrier.

## TL;DR

Fluid dynamics does not yield a new factoring method. The natural observables of
Navier–Stokes — energy spectrum, dissipation rate, mode transfer, cascade, and
the ε-regularity singular set — are all **additive/Fourier invariants** on the
mode index set. Factoring `N = pq` is encoded in the **multiplicative/CRT**
structure. Additive characters do not see the CRT decomposition without knowing
the factors. The factors appear, at best, as *periods* of additive invariants —
but (1) constructing the data that exposes those periods requires knowing the
factors (circularity), and (2) reading a period on `ℤ/Nℤ` is the period-finding
problem, classically `Θ(√N)` (free-witness aggregation). This is the same
structural orthogonality that defeated the Berggren tree and the dyadic
solenoid, now expressed via spectral PDE theory.

## The six hypotheses

| # | Hypothesis | Result | Barrier |
|---|-----------|--------|---------|
| H1 | Energy spectrum of factor-independent fields encodes a factor | REFUTED (E1: signal/random = 0.73, i.e. no signal) | Structural orthogonality |
| H2 | Galerkin ODE attractor / energy landscape encodes a factor | REFUTED (E3: energy is monotone Lyapunov, single minimum) | Structural orthogonality |
| H3 | Dissipation rate / mode transfer encodes a factor | REFUTED (E3, E4b: tautology, no N-info) | Structural orthogonality |
| H4 | Singular-set measure encodes a factor | REFUTED (E4c: empty for smooth fields; needs oracle) | Circularity |
| H5 | Cascade direction / inertial range encodes a factor | REFUTED (E3: cascade is scale-additive, orthogonal) | Structural orthogonality |
| H6 | Fourier/transcendental structure evades polynomial barrier | REFUTED (E5 poly barrier; E6 reduces to period-finding) | Poly barrier + free-witness |

## Key experiments

**E1 (20,111 tests):** Spectral features of 9 factor-independent field types
vs N. Actual features hit factors 6.88% of the time; a random-integer baseline
hits 9.46%. **Signal/random = 0.73** — the structured features do *worse* than
random. No genuine signal; the "hits" are pure multiple-testing artifact.

**E2 (oracle test):** With known factors, a separable product field
`u_{a,b} = α_a β_b` has an energy spectrum that factors exactly
(max error 3×10⁻²⁹), and the autocorrelation peak lands on `p`. The factors ARE
present as periods — but building the product field needs the CRT decomposition
(circularity), and reading the period from `ℤ/Nℤ` samples is period-finding
(`Θ(√N)` classically — free-witness aggregation).

**E3 (Galerkin simulation):** 2D vorticity Galerkin system (80 modes) evolved
with factor-independent ICs. 73/6720 spurious gcds (1.09%) — pure artifact.
Energy is monotone decreasing (dissipation identity), cannot develop factor
structure.

**E4 (structural):** (a) `E(u)=‖u‖²` is convex, one minimum — no "strange
landscape" of minima. (b) Mode transfer identity verified (sum = 2.87e-14) but
is a universal bookkeeping tautology. (c) Singular set empty for smooth fields.

**E5 (polynomial barrier):** For `u_i = i²`, dissipation proxy is a degree-5
polynomial in N; sporadic gcds are the finitely-many-prime phenomenon.

**E6 (period-finding):** Exponential fields `u_i = a^i mod N` reduce to reading
`ord_N(a)` from the spectrum = period-finding = Shor's classical bottleneck.

## The structural obstruction (in one sentence)

> Turbulence's natural coordinates (energy spectrum over additive wavenumbers)
> are orthogonal to factoring's natural coordinates (CRT / multiplicative
> order); additive Fourier observables can only encode the factors as periods,
> but constructing period-exposing data needs the factors (circularity) and
> reading a period on `ℤ/Nℤ` needs Θ(√N) time (free-witness aggregation).

## Conclusion

Navier–Stokes sharpens the portrait of the structural orthogonality barrier —
showing it governs even sophisticated PDE observables — but does not overcome
it. No classical factoring method here. Experiment **NS**, lab count now 90.
