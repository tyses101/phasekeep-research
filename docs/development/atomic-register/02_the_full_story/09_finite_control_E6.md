# 9. Finite control pulses (E6)

[← Drift](08_drift_E5.md) · [Next: echo timing →](10_echo_timing_E7.md)

> **In plain words:** real flips take time, and the register keeps hopping while they happen. Simple pulses fail badly at a realistic strength. Cleverly timed **composite** pulses work perfectly, but only if the uneven interaction is switched off, or made uniform, during the flip.

**Script:** `code/e6_flips.py`. **Data:** `code/results/e6_flips.csv`. **Evidence:** SIMULATED.

[ASSUMED] Scope: numerical statements apply only to the stated model, sequence and sampled parameters. They are not hardware guarantees.

## The key reduction [DERIVED]
- **During a flip each ring is a two-level system.** The interaction is off, and in the code subspace {0, 2}: **H = −a·τ_x + 2J·τ_z**.
- **That's an off-resonant π pulse,** where the hopping acts as the detuning.
- **So composite pulses and optimal control apply,** and an exact flip exists for any J at bounded control strength.

## Composite flips [SIMULATED]
- **Design:** 4 signed constant segments (+, −, +, −) at a = 4 J_B, optimized per ring to give exactly τ_x up to global phase.
- **Synchronization:** both rings are forced to the same total duration (1.18/J_B), so neither waits.
- **Accuracy:** isolated flip infidelity is about 2e-15.
- **Durations:**
  - ring B: [0.305, 0.570, 0.133, 0.172]
  - ring A: [0.343, 0.493, 0.135, 0.208]

## Results inside the full gate
| Flip | α = 0 | α = 0, bond 5% | α = 0.5, V off during flip | α = 0.5, **V on** |
|---|---|---|---|---|
| Ideal instantaneous | exact | exact | 1.7e-6 | — |
| Square (τ = π/8) | 0.53 | 0.93 | 0.54 | 0.54 |
| sin², same area | 0.40 | 0.54 | 0.40 | 0.41 |
| **Composite** | **exact** | 5.1e-5 | **1.7e-6** | **7.0e-3, leakage 6.9%** |

## Lessons
1. **Composite flips recover ideal performance** when the interaction is uniform or off during the flip.
2. **They reintroduce a small bond-calibration sensitivity** (5e-5 at 5%), because they're tuned to the nominal J.
3. **An uneven interaction left on during a composite flip breaks it.** The best *isolated* flip is not the best flip *during COUPLE*.

So isolated control optimization is not enough. Interaction-aware optimization (E8) is pending.

**Hardware scale** [DERIVED from ASSUMED J_B/h = 1 MHz]:
- control coefficient about 4 MHz
- flip about 0.19 µs
- earlier fast-square estimate: about 78.5 MHz for 3.2 ns
