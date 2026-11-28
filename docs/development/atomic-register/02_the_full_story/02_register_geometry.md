# 2. Register geometry

[← Architecture](01_architecture.md) · [Next: physical development →](03_physical_development.md)

> **In plain words:** four sites in a ring, with one excitation hopping among them, behave exactly like **two qubits sitting on the corners of a square**. The two "standing wave" patterns we use to store information form a standard error-detecting code. The natural way to grow the register is a **cube** or hypercube, not a bigger ring. All of this is established maths, so the register is **not** a new kind of qubit.

[ASSUMED] Scope: numerical statements apply only to the stated model, sequence and sampled parameters. They are not hardware guarantees.

## The ring register
- **Space:** 4 sites × 2 internal levels {R1, R2} = 8 states per ring, holding one excitation.
- **Ring modes:** |ℓ⟩ = Σⱼ e^{iπℓj/2}|j⟩/2, for ℓ = 0…3.
- **Uniform hopping energies:** E_ℓ = 2J cos(πℓ/2), giving +2J, 0, −2J, 0. [DERIVED]
- **Code:** standing-wave modes {0, 2} × internal = 4 states (a Tetragon, signature [2,2]).
- **Staggered flip:** a π phase on odd sites, S = (−1)ʲ, which swaps 0 ↔ 2 exactly. [DERIVED, SIMULATED `lie_check.py`, `ring_chiral.py`]

## Two equivalent representations
| | One-hot (physical) | Compact (Gray code) |
|---|---|---|
| Qubits per ring | 8 (site × internal) | 3 (two site bits + one internal bit) |
| Uniform hopping | 8 XY gates, exact in one step | **J(X₁ + X₂)**: single-qubit rotations, **no entangling gates** |
| Staggered flip | Z on odd-site qubits | Z₁Z₂ |
| Free error check | Excitation count | X₁X₂ parity |

**Sources:**
- REF-01 one-hot: [SIMULATED `ref01_onehot.py`, `ref01_diagnostics.py`]
- Gray-code equivalence, residual 7.6e-16: [REPORTED, separate AI re-run (REPORTED)]

## Why this works: it's a square
Gray order 00, 01, 11, 10 makes every ring bond flip exactly one bit. Hopping is then J(X₁ + X₂). Consequences:
- **The code** {0, 2} = {|++⟩, |−−⟩} is the **X₁X₂ = +1 stabilizer code**.
- **Logical operations:** the flip Z₁Z₂ is logical X, and hopping is logical Z. [DERIVED]
- **Why the four-site case is special:** the two "dimer" hopping layers commute on the square. That's why one Trotter step is exact, and why alternating bond strengths and 2π flux stay exact. A 6- or 8-site cycle isn't a hypercube, so exactness fails there. [SIMULATED `ref01_diagnostics.py`; REPORTED audit]

## Hypercube generalization [REPORTED, separate AI re-run (REPORTED)]
| Spatial dimension | Compact qubits | Matrix residual vs. independent rotations |
|---:|---:|---:|
| 4 | 2 | 3.96e-16 |
| 8 | 3 | 9.55e-16 |
| 16 | 4 | 1.22e-15 |
| 32 | 5 | 2.51e-15 |

Hopping on an n-cube is J·ΣXᵢ. **It does not generate entanglement between the compact site bits under this separable hopping Hamiltonian.** Entanglement and protection have to come from the internal axis and from interactions between registers.

## Keep these four things separate
| Concept | Meaning here |
|---|---|
| Capacity | Dimension of the state space (Tetragon: 4 = two qubits). Not readable classical bits (Holevo bound) |
| Controllability | Which unitaries are reachable (Lie dimension; ch. 5) |
| Entanglement | Which correlations the controls can create (requires internal axis / interaction) |
| Protection | Which errors are detected, suppressed or cancelled (ch. 5–11) |

## Larger rings
- **Eight sites (corrected 2026-11-28; see [errata](../../errata.md)).**
  - **Original statement, kept for the record:** "the staggered shift maps ℓ = +1 to +3. Phase-pattern flips stop being closed."
  - **Correction:** two phase patterns coincide on four sites and differ on eight.
  - **The twice-winding pattern** e^{2iφⱼ} shifts modes by 2, mapping ℓ = +1 to +3, outside a {+1, −1} code. [SIMULATED `ring_chiral.py`]
  - **The alternating pattern** (−1)ʲ shifts modes by N/2 = 4, mapping +1 to 5 ≡ −3. Codes such as {0, 4} stay closed under it. [DERIVED]
  - **Closure depends on ring size and the chosen modes.** An operation that preserves the four-site code needn't preserve the equivalent code on a larger ring.
- **Scaling:** use **coupled four-site rings or hypercubes**, not larger cycles.
