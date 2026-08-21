# Paper 98 — BATTERY-UTILITY: The Labels Are Not Filters

**Verdict name: THE-LABELS-ARE-NOT-FILTERS.**
Round-28 #4 · exp 433 · assessment v208 · script `/tmp/exp_batteryutility.py` · log `/tmp/r28n4b.log`.

## 1. The closing question

Papers 91–94 measured the 6-dial battery's capacity (12.7235 bits, 99.6% of ceiling, factor-blind). The natural closing question: what does that capacity BUY? Concretely: does observing the six-dial label vector narrow the trial-division candidate set for p beyond the unconditional scan?

## 2. What broke, and why it matters

The planned measurement needed, per dial, a map **residue r mod m\* → type of a prime ≡ r mod m\*** — so that observed labels could filter candidate residues. Building that map by evaluating the defining polynomial at r (does f(r) ≡ 0?) produced tables that were conceptually wrong: they tested whether *r itself* is a root of f mod m\*, not which *splitting type* primes ≡ r carry.

And the deeper fact surfaced by the failure: **that map does not exist**. Primes in the same residue class mod m\* carry different splitting types — that is precisely why every measured channel sits below its label-entropy ceiling (I₁ = 1.0012 against H(T) = 2.2982 for S₃a; the gap IS the within-class variation). The battery's labels are statistics of the JOINT (p mod m\*, q mod m\*) draw; they are not functions of any single residue, and therefore **cannot be compiled into per-candidate residue filters**. The candidate-set framing of battery utility is category-error, not an implementation bug.

Consistency data from the broken build confirms the diagnosis indirectly: the cubic dials' union-of-types filter excluded the true p in 0/150 cases — but only because their (wrong) admissible unions covered nearly all residues; the quartic dials' buggy pattern enumeration excluded 6/150. Neither implements a true constraint.

## 3. The corrected understanding

The battery's utility must be stated Bayesianly: observing the label vector re-weights the posterior over the joint residue vector (p mod M, q mod M) — a 12.7-bit update on a ~20-bit joint space, exactly as the capacity law says. Converting that posterior into individual-candidate narrowing requires the per-prime type determination that the abelianization gap denies. In no-pinning terms: the battery's information is about the JOINT residue draw, factors through the trace-and-character content, and **cannot be compiled into a candidate filter without already knowing the factorization** (which type a prime carries is decided by the Frobenius at that prime — computing it is the factoring problem).

## 4. Barriers

**(a)** clean — the utility horns were pre-stated; the refutation of the framing is the result, with the diagnosis (which dial, which mechanism) traced before recording. **(b)** clean. **(c)** confronted — 150 fresh semiprimes through the broken filter (6 exclusions found and diagnosed), 150-case cubic consistency check (0 exclusions, explained). **(d)** clean. **(e)** the substance — the category error identified, named, and elevated to the corrected Bayesian statement. **(f)** controlled — the inconsistency assert stopped the run before any claim. **(g)** fair — marginals and walls from papers 91–93 untouched. **(h)** relevance — closes the battery arc with the utility question answered in its honest form: the battery buys posterior mass on joint residue vectors, not candidate filters; its constant-boundedness follows from the fixed CRT modulus, consistent with no-pinning.

Now 433 experiments. Assessment v208 (the round consumed one experiment slot; the recorded count includes the diagnostic runs). Paper 98, issue #190.
