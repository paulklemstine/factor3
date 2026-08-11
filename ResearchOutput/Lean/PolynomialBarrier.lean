import Mathlib

open Polynomial

/-! # The Polynomial Barrier Theorem (formalized)

This file formalizes Theorem 1 of the lab paper
`ResearchOutput/NewMathematics/02_Structural_Barrier_Theorems.md`:

  For any integer polynomial f and any p dividing N = pq:
      p | f(N)  <=>  p | f(0)

so `gcd(f(N), N)` contains only primes dividing `f(0)`.  Hence **no polynomial
invariant of N alone is a universal factoring witness** — the polynomial
barrier (LLL).

Note: primality of `p` is not actually needed; the theorem holds for any
modulus `p`.  The hypothesis is kept to match the paper's statement and to
serve the corollary below.

The proof works by reduction modulo `p`: since `N ≡ 0 (mod p)`, evaluation of
`f` at `N` and at `0` coincide modulo `p` (evaluation commutes with the ring
hom `ℤ → ZMod p` via `Polynomial.eval₂_hom`).
-/

namespace BarrierFormalization

/-- Evaluation commutes with reduction modulo p: `(g.map φ).eval (φ a) = φ (g.eval a)`.
  This is `Polynomial.eval₂_hom` composed with `eval₂_eq_eval_map`. -/
lemma eval_mod (g : Polynomial ℤ) (φ : ℤ →+* ZMod p) (a : ℤ) :
    (g.map φ).eval (φ a) = φ (g.eval a) := by
  exact (Polynomial.eval₂_eq_eval_map (p := g) (f := φ) (x := φ a)).symm.trans
    (Polynomial.eval₂_hom φ a)

/-- The polynomial barrier: if `p | N` then `p | f(N) ⟺ p | f(0)`.
  Equivalently, `f(N) ≡ f(0) (mod p)`. -/
theorem congruent_eval (f : Polynomial ℤ) {p N : ℕ} (_hp : Nat.Prime p) (hpN : p ∣ N) :
    (p : ℤ) ∣ f.eval (N : ℤ) ↔ (p : ℤ) ∣ f.eval (0 : ℤ) := by
  rw [← ZMod.intCast_zmod_eq_zero_iff_dvd (a := f.eval (N : ℤ))]
  rw [← ZMod.intCast_zmod_eq_zero_iff_dvd (a := f.eval (0 : ℤ))]
  let φ : ℤ →+* ZMod p := Int.castRingHom (ZMod p)
  let z0 : ℤ := 0
  have hN0 : ((N : ℤ) : ZMod p) = 0 := by
    rw [ZMod.intCast_zmod_eq_zero_iff_dvd]
    exact_mod_cast hpN
  have hφN : φ (N : ℤ) = φ z0 := by
    change ((N : ℤ) : ZMod p) = ((z0 : ℤ) : ZMod p)
    exact hN0.trans (by simp [z0])
  have heval : φ (f.eval (N : ℤ)) = φ (f.eval z0) := by
    calc
      φ (f.eval (N : ℤ)) = (f.map φ).eval (φ (N : ℤ)) := (eval_mod f φ (N : ℤ)).symm
      _ = (f.map φ).eval (φ z0) := by rw [hφN]
      _ = φ (f.eval z0) := eval_mod f φ z0
  -- φ x is definitionally (x : ZMod p) (Int.castRingHom has toFun := Int.cast)
  have h : ((f.eval (N : ℤ) : ℤ) : ZMod p) = ((f.eval z0 : ℤ) : ZMod p) := by
    rw [show ((f.eval (N : ℤ) : ℤ) : ZMod p) = φ (f.eval (N : ℤ)) by rfl]
    rw [show ((f.eval z0 : ℤ) : ZMod p) = φ (f.eval z0) by rfl]
    exact heval
  rw [h]

/-- Corollary: any prime dividing both `f(N)` and `N` also divides `f(0)`.
  Hence `gcd(f(N), N)` is composed only of prime divisors of `f(0)`. -/
theorem factor_divides_f0 {f : Polynomial ℤ} {p N : ℕ} (hp : Nat.Prime p)
    (hpN : p ∣ N) (hpf : (p : ℤ) ∣ f.eval (N : ℤ)) : (p : ℤ) ∣ f.eval (0 : ℤ) :=
  (congruent_eval f hp hpN).mp hpf

end BarrierFormalization
