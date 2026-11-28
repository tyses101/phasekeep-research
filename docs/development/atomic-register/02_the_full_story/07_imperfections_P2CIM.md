# 7. Combined imperfections (P2-CIM)

[← Integrity checks](06_iqa.md) · [Next: drift →](08_drift_E5.md)

> **In plain words:** each imperfection on its own is suppressed enormously: error grows only as the *sixth* power of its size. Two imperfections *together* are much worse. A wrong hopping strength combined with an uneven interaction produces error that grows only as the *square*. That gives one practical rule: **hopping error × interaction unevenness ≲ 0.015** for 1-in-10,000 accuracy.

**Script:** `code/p2cim.py`, `code/p2cim_analyze.py`. **Data:** `code/results/p2cim_*.csv`. **Evidence:** SIMULATED, standard model, ideal flips.

[ASSUMED] Scope: numerical statements apply only to the stated model, sequence and sampled parameters. They are not hardware guarantees.

## Definitions
- **ε:** fractional bond-strength error (bond 3–0, ring A).
- **δ:** site-0 detuning, in J_B units.
- **α:** interaction unevenness, defined by V(α) = V̄ + α(V_phys − V̄). α is the fraction of the originally modelled variation, not a percentage of the physical coupling.

## Grid
ε ∈ {0, .01, .03, .05, .1, .2} × δ ∈ {0, .01, .03, .05, .1} × α ∈ {0, .1, .25, .5, .75, 1} = **180 configurations**.

## Fits: the proposed models failed [negative result, kept]
| Model | Terms | Held-out \|log₁₀ error\|, median / 90% / max |
|---|---|---|
| A | α², δ², ε²α² | 0.21 / 4.1 / 5.3 |
| B | + εα², αδ | 0.18 / 3.9 / 10.1 |
| C, D | other quadratic combinations | ~0.11 / 1.6 / 8.2 |
| E | **α⁶, δ⁶, ε²α²** | 0.07 / 0.90 / 5.2 |
| **E+** | E + ε²δ², α²δ² | **0.045 / 0.47 / 1.04** |

**Empirical model (E+):**

  **1 − F ≈ 1.3e-4·α⁶ + 58·δ⁶ + 0.43·ε²α² + 2.7·ε²δ² + 4.2e-5·α²δ²**

**Evidence of sixth order:**
- α = 0.25 → 0.5 → 1 gives 2.7e-8 → 1.7e-6 → 1.1e-4 (×64 per doubling)
- detuning shows the same pattern

**What the model misses:** at α = 0 the bond × detuning interaction oscillates with ε. That's coherent interference, which no polynomial captures.

**Sixth-order suppression is an empirical property of this pulse sequence and parameter range,** not a general architectural law. Its derivation is open.

## Design rule (dominant coupled term only)
| Infidelity contribution | Maximum εα |
|---:|---:|
| 1e-2 | 0.15 |
| 1e-3 | 0.048 |
| 1e-4 | 0.015 |
| 1e-5 | 0.005 |

These are **individual error-budget terms**, not guarantees of total fidelity.

## Other results
- **Sign and location** (ε = ±0.2, δ = 0.1, α = 1):

  | Ring | +20% | −20% |
  |---|---|---|
  | A, infidelity / leakage | 1.61e-2 / 6.7e-3 | 1.49e-2 / 6.2e-3 |
  | B, infidelity / leakage | 1.39e-2 / 1.2e-3 | 1.53e-2 / 1.0e-3 |

  Sign matters about 10%. Errors on ring A leak about **6×** more.
- **Operating boundaries** for four tiers (99%, 99.9%, 99.99%, 99.999%, each with matching leakage limits) are in `p2cim_boundaries.csv`.
- **Convergence:** 600, 1200 and 2400 steps agree to 5 significant figures at three test points (`p2cim_convergence.csv`).
