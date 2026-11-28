# Evidence, failures and audit findings

[← Start here](../README.md)

## 1. Evidence classification of headline claims
| Claim | Class |
|---|---|
| Four-site ring = 2-qubit square; code = X₁X₂ = +1; hypercube generalization | DERIVED; REPORTED numerics |
| Static bipartite hopping cancels exactly under the staggered echo | DERIVED; SIMULATED |
| Uniform internally selective interaction commutes and survives the echo | DERIVED; SIMULATED |
| Intended two-ring gate = one CZ on internal qubits | DERIVED; SIMULATED |
| Isolated imperfections suppressed ~sixth order (this sequence) | SIMULATED (empirical) |
| Coupled term 0.43(εα)² | SIMULATED (fit) |
| Drift-balance condition | DERIVED; SIMULATED |
| ∫g² envelope-balance mechanism | PROPOSED mechanism; SIMULATED support |
| Decay dominates the atomic error budget | DERIVED from literature values (REPORTED (mixed-source assumptions), partly UNVERIFIED) |
| Platform parameters | REPORTED by others; combinations REPORTED (mixed-source assumptions) |
| Any hardware performance | **None** |

## 2. Negative results (kept on purpose)
| # | Result | Where |
|---|---|---|
| N1 | Microwave + Raman can't control the ensemble Tetragon (10/15) and leaks | ch. 3 |
| N2 | Energetic confinement: phase error ∝ 1/Δ; still not universal; no physical source in a frozen ensemble | ch. 3 |
| N3 | Ring controls without hopping reach only 7/63 | ch. 3 |
| N4 | Flux-2π "chirality" is a gauge relabelling | ch. 3 |
| N5 | Equal hopping (ratio 1) and ratio 2 leak completely | ch. 3 |
| N6 | Symmetric 3-segment echo (first test) worse than 2-segment at fixed peak | ch. 10 |
| N7 | Flat-top pulses lose the leakage benefit (ramps too short) | ch. 5 |
| N8 | Simple square and sin² flips fail at realistic strength | ch. 9 |
| N9 | Composite flips fail with uneven interaction on (0.7%, 6.9% leakage) | ch. 9 |
| N10 | Quadratic error models A and B fail on held-out data | ch. 7 |
| N11 | Echo fails under drift (0.39–0.94) | ch. 8 |
| N12 | Continuous envelope and continuous CPMG-4 leak with uneven V | ch. 10 |
| N13 | Interaction notches don't recover segmented performance; p ≈ 4 | ch. 11 |
| N14 | Parity misses ZZ, X and half of the one-hot phase errors; counting misses phase errors | ch. 6 |
| N15 | Earlier mixed-source estimate ranked circular Rydberg worse (weak assumed exchange); not an established platform ranking | ch. 12 |
| N16 | Rydberg dressing doesn't improve interaction / decay (β² scaling); collective decay | ch. 12 |

## 3. Superseded assumptions
| Earlier assumption | Replaced by |
|---|---|
| A single Rydberg excitation hops among ground-state atoms | Resonant exchange needs an all-Rydberg background (8 fragile atoms per 2-ring gate) |
| Decay estimate 66% survival (10 µs, 50 µs) | ≈19% with 8 atoms |
| "Chiral splitting" at flux 2π | Relabelling; standing-wave code |
| Code-fidelity formula with projected target (REF-01d) | Exact-output W formula |
| "Overlap" \|Tr\|/16 used as fidelity | Leakage-aware F_avg (lower values) |
| Gate count 12 for the REF-01 script | 16 as written; 12 after merging layers |
| Ensemble spin-wave OAM as the register's spatial axis | Discrete four-site ring |
| Envelope slew ≈ 0.8 MHz/µs | 0.126 MHz/µs (2π conversion error corrected) |
| Parity "catches" one-hot phase errors | Only partially (50%) |
| Spacing sweep results were read as speed improvements | Mean was held fixed, so they show evenness only |

## 4. Separate AI re-run (REPORTED) findings
- **Scripts:** all 10 v3 scripts were re-executed independently with exit code 0. Separately uploaded files byte-matched the archive.
- **Checks passed:** Lie-rank stability under tolerance 1e-7 to 1e-10; shaped-pulse time-step convergence (≤ 0.34% change from 600 to 2400 steps); leakage-aware fidelity reproduced (98.2213%).
- **Corrections raised:**
  - gate count (16 versus 12)
  - REF-01d code-fidelity metric conflating leakage with approximation error
  - exactness limited to specific symmetric cases (unequal bonds, π flux, 6/8 sites break it)
- **Additional checks:** compact Gray equivalence; hypercube residuals; parity circuit; REF-03 split-step convergence; noise-channel checks.
- **Not done in any audit:** literature verification, hardware execution, full open-system modelling.

## Audit attribution

[REPORTED] The earlier re-run was performed by a separate AI assistant (ChatGPT), at the project owner's request on 27–28 November 2026. The A-series scripts are not included in the archive. This is not an external human review or independent experimental validation.
