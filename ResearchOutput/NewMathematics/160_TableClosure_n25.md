# Paper 160 — TABLE-CLOSURE: The g/Is/A/X Tables Shut at n = 25

**Verdict name: TABLES-SHUT (H1/H2 confirmed; H3's guessed asymptotic refuted — ratios measured instead).**
Round-42 #6 (cron iteration) · exp 491 · assessment v269 · script `ResearchOutput/scripts/2026-08-21-resume/exp491_table_closure.py` (+ `exp491_result.json`).

## 1. Closing the fork-channel tables

The lab's exact closed forms (papers 72–74) computed for n = 2..25, all four channels
(g/OR, Is/split-count, A/AND, X/XOR), with the inequality structure verified exactly.

## 2. Results

- **H1 CONFIRMED**: Is(n) ≥ max(g, A, X)(n) at every n ∈ [2, 25] (no violations);
  A(n) ≥ g(n) everywhere; **A overtakes X exactly at n = 8** — re-deriving paper 74's
  crossover to the integer.
- **H2 CONFIRMED**: every channel → 0 (n=25: g 0.00073, Is 0.01200, A 0.00748, X 0.00471).
- **H3 REFUTED**: the pre-stated asymptotic X/g → 2 is wrong in direction and magnitude —
  X/g rises through 5.93 (n=5), 6.27 (10), 6.43 (25), still climbing; the measured ratio
  table replaces the guess.

## 3. What this decides

The fork-channel tables are shut: dominance structure exact (Is universal; A ≥ g; A/X
crossover pinned at n = 8), decay to zero verified, and the asymptotics corrected by
measurement. Barriers: (5)/(8) unchanged.

Method ledger: two-stage silent-garbage hunt — an unnormalized entropy function followed by
non-summing distributions (Is's middle element written 1/n instead of ((n−1)/n)²); both
produced plausible-looking wrong numbers until the exact complement forms were imposed.
Both disclosed.

Now 492 experiments. Assessment v269.
