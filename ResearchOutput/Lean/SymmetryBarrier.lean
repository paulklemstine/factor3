import Mathlib

/-! # The Symmetry Barrier Theorem (formalized)

Paper: `ResearchOutput/NewMathematics/02_Structural_Barrier_Theorems.md`,
Theorem 2.

Any quantity computed from N = p*q alone is symmetric in (p, q): if
f(p,q) = g(p*q) for some g, then f(p,q) = f(q,p).  Hence any quantity that
DISTINGUISHES p from q (i.e. is not symmetric) cannot be a function of N
alone — factor-revealing antisymmetry is uncomputable from the symmetric
product N.

We also formalize the CRT-split divisibility fact underlying paper 11's
Fact 1: for coprime p, q, divisibility by p*q is equivalent to divisibility
by both p and q.
-/

namespace BarrierFormalization

/-- Any function of N = p*q alone is symmetric in (p, q). -/
theorem n_computable_is_symmetric {X : Type*} (g : ℕ → X) (p q : ℕ) :
    g (p * q) = g (q * p) := by
  rw [Nat.mul_comm]

/-- Contrapositive: a quantity h(p,q) that distinguishes p from q (not
  symmetric) is not a function of N = p*q alone. -/
theorem antisymmetric_not_n_computable {X : Type*} (h : ℕ → ℕ → X)
    (p q : ℕ) (hasymm : h p q ≠ h q p) :
    ¬ ∃ g : ℕ → X, ∀ a b : ℕ, h a b = g (a * b) := by
  rintro ⟨g, hg⟩
  exact hasymm (by
    calc
      h p q = g (p * q) := hg p q
      _ = g (q * p) := by rw [Nat.mul_comm]
      _ = h q p := (hg q p).symm)

/-- The EML commutator example from the paper: (p,q) ↦ p² - q² is
  antisymmetric (when p > q), hence cannot be computed from N = p*q alone. -/
theorem commutator_not_n_computable (p q : ℕ) (h : p * p - q * q ≠ q * q - p * p) :
    ¬ ∃ g : ℕ → ℕ, ∀ a b : ℕ, a * a - b * b = g (a * b) :=
  antisymmetric_not_n_computable (fun a b : ℕ => a * a - b * b) p q h

/-- CRT-split (paper 11, Fact 1 core): for coprime p, q, divisibility by p*q
  is equivalent to divisibility by both p and q. -/
theorem crt_mul_dvd_iff {p q d : ℤ} (hcop : IsCoprime p q) :
    p * q ∣ d ↔ p ∣ d ∧ q ∣ d := by
  constructor
  · intro hd
    exact ⟨dvd_trans (dvd_mul_right p q) hd, dvd_trans (dvd_mul_left q p) hd⟩
  · rintro ⟨hp, hq⟩
    exact hcop.mul_dvd hp hq

end BarrierFormalization
