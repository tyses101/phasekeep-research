# 8. Drift (E5)

[← Combined imperfections](07_imperfections_P2CIM.md) · [Next: finite control pulses →](09_finite_control_E6.md)

> **In plain words:** the echo cancels hopping that is *wrong but steady*. If hopping strength *changes during* the operation, the two halves of the echo no longer match, and the leftover error can be huge. Worse, that error stays *inside* the allowed states, so our integrity checks don't notice it.

**Script:** `code/e5_drift.py`. **Data:** `code/results/e5_drift.csv`. **Evidence:** SIMULATED. Drift amplitude 0.05 on bond 3–0, standard model.

| Drift (α = 0) | Infidelity | Leakage |
|---|---|---|
| Static (both rings, or one ring) | ~1e-13 (exact) | ~1e-13 |
| Linear ramp over the gate | **0.39** | 3e-4 |
| Abrupt change between segments | **0.81–0.88** | ~1e-7 |
| Sinusoid, ½ cycle per segment | **0.94** | ~1e-5 |
| Sinusoid, ¼ cycle, rings out of phase | **0.67** | 6e-4 |
| Sinusoid, integer cycles per segment | 1e-9 to 3e-8 | — |

[ASSUMED] Scope: numerical statements apply only to the stated model, sequence and sampled parameters. They are not hardware guarantees.

## Why: the balance condition [DERIVED]
- **For mutually commuting time-dependent hopping Hamiltonians, equal segment integrals cancel hopping.** For changing noncommuting bond patterns, equal integrals alone do not ensure cancellation; time ordering matters.
- **The phase at stake is large.** During a COUPLE gate, each segment accumulates about 2J·T_seg ≈ 90 rad of hopping phase, so a between-segment mismatch Δε leaves about 90·Δε rad of logical error.
- **Zero-average drift can cancel in the commuting model; it is not generally harmless for noncommuting controls.**
- **This is the classic Hahn-echo limit:** static errors cancel, linear drift does not.

## Consequences
- **Stability requirement:** roughly **Δε ≲ 1e-4** between segments for 1e-4-level gates. This applies to **this gate duration and error model only**.
- **Correlated beats independent:** drift common to both rings is much milder than drift on one ring. At α = 0.25 static, 2.6e-7 versus 6.3e-5.
- **Detection:** this is the clearest case of an error **invisible to IQA levels 1–2** (chapter 6).
- **Timing as the fix:** better echo timing partly addresses it (chapter 10).
