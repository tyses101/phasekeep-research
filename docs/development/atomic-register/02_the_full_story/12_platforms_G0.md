# 12. Platforms (G0)

[← Envelope balance](11_envelope_balance_E7D.md) · [Next: pending research →](13_pending.md)

> **In plain words:** which real hardware could build this? The design itself doesn't care: it's a target Hamiltonian that several platforms can realize. Superconducting circuits have already built a three-site ring with the right kind of control. Atoms are the original target, but **atomic decay is a major unresolved obstacle** under the illustrative parameters; a consistent platform comparison remains open. **No platform has demonstrated the full PhaseKeep register.**

Detailed table with sources: [source verification record](../03_reference/sources.md). Values are abstract-level and need full-text checking.

[ASSUMED] Scope: numerical statements apply only to the stated model, sequence and sampled parameters. They are not hardware guarantees.

## Candidates (identifiers preserved)
| Branch | Platform | Key evidence | Classification |
|---|---|---|---|
| G0-A1 | Conventional Rydberg | Resonant exchange chains demonstrated. C₃ ≈ 7456 MHz·µm³ (1–10 MHz at ~10 µm). 55P lifetime 406 µs at 4 K (about 123 µs at room temperature) | REPORTED external measurements; combination REPORTED (mixed-source assumptions) |
| G0-A2 | Circular Rydberg | Package reports lifetimes 2.55 ms (Sr) and 3.7 ms (Rb, n = 52), detailed values UNVERIFIED in this integration. Exchange **predicted** at only a few to tens of kHz | REPORTED lifetimes / theory exchange |
| G0-B | Rydberg dressing | ~13 kHz interactions. **Collective decay hazard** | REPORTED external measurements |
| G0-C1 | Trapped ions | XY hopping of spin excitations demonstrated. J and T₂ not retrieved | Partly UNVERIFIED |
| G0-C2 | Mediated neutral atoms | Not searched | UNVERIFIED |
| G0-D | Superconducting circuits | **3-site ring with synthetic flux and measured chiral currents.** 12-qubit hopping chain. J, T₁, T₂ not retrieved | REPORTED external measurements; numbers UNVERIFIED |

## Figures of merit
- **J·T / N_fragile:** a screening metric.
- **𝓑 = 1/(t_gate·ΣΓ):** survival per gate = exp(−1/𝓑).
- **A1 estimates (REPORTED (mixed-source assumptions) sources):** about 92–97% survival per gate, with all 8 Rydberg atoms counted.
- **Illustrative A2 estimate (not one demonstrated setup):** about 15 exchange periods per lifetime, which is insufficient under the assumed gate requirements; this is not a platform-wide impossibility result.

## Qualification requirements from this update (priority order)
1. **Interaction uniformity:** εα ≤ 0.015 for a 1e-4 budget (ch. 7).
2. **Coherent lifetime:** decay dominates every budget (ch. 3).
3. **Hopping stability during execution:** ~1e-4 between echo segments for the tested gate (ch. 8).
4. **Bond calibration under uneven interactions** (ch. 5, 7).
5. **Accurate staggered control:** composite flips at ~4 J_B (ch. 9).
6. **Interaction-envelope programmability:** segmented, balanced, switchable or uniform during flips (ch. 9–11).
7. **Phase-preserving storage and transfer** (PK-LMI, ch. 3).
8. **Operation-dependent calibration** (ch. 5).

**Two development paths:** a *reference* implementation on established hardware (REF-03-I), and the *target* atomic implementation.

## Integration qualification

[ASSUMED] The 92–97% survival estimate combines rubidium D/P exchange parameters with a cesium 55P lifetime from another experiment. It is only an order-of-magnitude illustration, not a feasible operating point. Circular-Rydberg values are also source-specific: the current abstract of arXiv:2510.27471 reports lifetimes over 10 ms with Purcell suppression; the supplied 3.7 ms at n = 52 has not been confirmed here. These numbers cannot establish a platform ranking. Detailed coefficients, decay budgets and device-specific conclusions remain UNVERIFIED pending a consistent setup.
