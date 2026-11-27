# The Ledger of Numbers

*Every number used in the library, its evidence tag and where it came from*


Every number used in the series, with its evidence tag and where it comes from. Derived values were recomputed by `make_ledger.py` when this page was built. The same table is in `ledger.csv`, which opens in any spreadsheet.

>
> **Common mistake**
> A **DERIVED** tag means the arithmetic checks out under the stated assumptions. It does not mean the assumptions hold in a laboratory.


| ID | Quantity | Value | Tag | Vol. | Source |
|---|---|---|---|---|---|
| L01 | Joint classical bound, coherent states, n̄ = 0.25, four modes | 0.482253 | [DERIVED] | 8 | verify_r25.py; proof awaiting independent review (B03) |
| L02 | Fidelity of an empty memory (η = 0, no noise) | 0.4096 | [DERIVED] | 8 | verify_r25.py |
| L03 | Single-photon benchmark 2/(d+1), d = 4, hidden Haar-random inputs | 0.40 | [DERIVED] | 2, 8 | verify_r25.py (section B); standard result |
| L04 | Entangled-target overlap benchmark | 0.25 | [DERIVED] | 8 | verify_r25.py (section B) |
| L05 | Noiseless efficiency threshold, n̄ = 0.25 | 1.1146 % | [DERIVED] | 8 | verify_r25.py |
| L06 | Noiseless efficiency threshold, n̄ = 1 | 8.5786 % | [DERIVED] | 8 | verify_r25.py |
| L07 | Noise v at which 4 % efficiency sits on the bound | 0.04 | [DERIVED] | 8 | verify_r25.py |
| L08 | Fidelity at 2 % efficiency, v = 1e-4 | 0.508185 | [DERIVED] | 8 | verify_r25.py |
| L09 | Analytic-anchored combined fidelity / margin over bound | 0.507107 / 0.024854 | [SIMULATED] | 8 | verify_r25.py; Monte Carlo error only |
| L10 | Detector-efficiency crossover (ideal, infinite statistics) | 85.73 % | [DERIVED] | 8 | verify_r25.py |
| L11 | Chain 4 % × 0.49 × 23 % | 0.451 % | [DERIVED] | 8 | verify_r25.py; inputs ASSUMED or supplied |
| L12 | Required filter transmission, zero margin (4 %, 0.49 / 4 %, 0.81 / 12.6 %, 0.49 / 12.6 %, 0.81) | 56.9 / 34.4 / 18.1 / 10.9 % | [DERIVED] | 8 | verify_r25.py |
| L13 | Margins over the bound for filter rows (0.451 % / 1.764 % / 1.420 % / 5.557 %) | −0.0272 / +0.0198 / +0.0098 / +0.0975 | [DERIVED] | 8 | verify_r25.py |
| L14 | Earlier time-mode chain 0.70 × 0.04 × 0.70 | 1.96 % | [ASSUMED] | 8 | historical modelling |
| L15 | Herald / occupancy-valid / false-herald probability for inputs (3, j), j < 3 | 0.375 / 0.125 / 0.25 | [SIMULATED] | 7 | outcome_resolved_herald_r30.py (ideal PNR detectors, reconstruction-specific) |
| L16 | Herald reliability, worst case studied | 1/3 (33.3 %) | [SIMULATED] | 7 | outcome_resolved_herald_r30.py |
| L17 | Probability all heralds fire, 2 stages / 16 stages | 0.01953125 / 1.4725e-14 | [SIMULATED] | 7 | SIM-06; audit_bundle_r25.py |
| L18 | Fidelity given heralds, 2/4/8/16 reactions (ideal) | 80.0 / 67.0 / 48.0 / 24.3 % | [SIMULATED] | 7 | SIM-06 |
| L19 | Same with correlated phase drift σ = 0.05 rad | 78.7 / 62.8 / 37.2 / 9.1 % | [SIMULATED] | 7 | SIM-06 |
| L20 | Fidelity given occupancy-valid, 2 stages | 98.5 % | [SIMULATED] | 7 | SIM-06 |
| L21 | Reuse: expected successful reuses s/(1−s) at s = 0.95; survival after 10 cycles | 19; 59.87 % | [DERIVED] | 7 | arithmetic |
| L22 | Hypercube counts, n = 12: corners / edges / squares / cubes | 4,096 / 24,576 / 67,584 / 112,640 | [DERIVED] | 4 | enumeration check |
| L23 | Operator Schmidt rank: CP on Z4×Z4 / one CPF | 4 / 2 | [DERIVED] | 6 | numerical check |
| L24 | Minimum number of CPF gates for CP | at least 2 (true count undefined) | [DERIVED] | 6 | rank bound |
| L25 | Heralded gate theoretical success | 1/4 × 1/2 = 1/8 | [REPORTED] | 6 | Liu et al. arXiv 2407.16356, read |
| L26 | Process fidelity of the heralded gate | 0.64 to 0.82 | [REPORTED] | 6 | Liu et al., read |
| L27 | Atom–cavity gate: fidelity / two-photon transmission / bandwidth | 76.2 ± 3.6 % (abstract) / 4.8 % and 0.7 MHz (project notes) | [REPORTED] | 6 | Hacker et al. arXiv:1605.05261; fidelity checked in the abstract, the other two unconfirmed |
| L28 | Bandwidth ratio, ~1 GHz memory band to 0.7 MHz | about 1,400× | [DERIVED] | 6 | arithmetic on supplied values |
| L29 | A06 parts saved, full readout: N = 2 / N = 32 | 14 % / 20 % | [SIMULATED] | 4, 9 | a06_precursor_sim.py (counts; error inputs ASSUMED) |
| L30 | A06 conditional fidelity, shared vs individual, N = 2 / N = 32 | 0.99961 vs 0.99959 / 0.99954 vs 0.99471 | [SIMULATED] | 4, 9 | a06_precursor_sim.py (ASSUMED errors) |
| L31 | Parameters of a pure d-level state | 2d − 2 | [DERIVED] | 2, 4 | standard |
| L32 | Check counts: verify_r25 / spec / A06 self-checks / R30 independent rerun | 71 / 12 / 19 / 20 | [REPORTED] | 9 | script output; R30 rerun by second party |
| L33 | Schmidt weights: edge blend (00+01)/√2 / diagonal blend (00+11)/√2 | 1, 0 / 0.5, 0.5 | [DERIVED] | 4 | make_ledger.py (numerical check) |
| L34 | Schmidt weights after independent unitaries on each axis (20 random trials) | unchanged | [DERIVED] | 4 | make_ledger.py (numerical check) |
| L35 | Illustrative joint yield, supplied chain: 0.125 × 0.00451 | 0.056 % (about 1 in 1,800) | [DERIVED] | 12 | arithmetic on SIMULATED and ASSUMED inputs; independence assumed |
| L36 | Illustrative joint yield, better chain (5.557 %) | 0.69 % (about 1 in 144) | [DERIVED] | 12 | arithmetic on SIMULATED and ASSUMED inputs; independence assumed |
| L37 | Fusion-based scheme: tolerated photon loss per fusion (ballistic scheme) | 10.4 % | [REPORTED] | 13 | Bartolucci et al. arXiv:2101.09310, abstract only; not comparable to other numbers here |
| L38 | Tesseracts (4-cubes) in a 12-axis register, subspace dimension 16 | 126,720 | [DERIVED] | 4 | hypercube_counts.py; make_ledger.py |
| L39 | Schmidt weights: (00+01+10+11)/2 / (00+01+10−11)/2 (same probabilities, 0.25 each) | 1, 0 / 0.5, 0.5 | [DERIVED] | 10 | tetragon.py; make_ledger.py |
| L40 | Schmidt weights after rotating 00 toward 11 by 45° / after X⊗X on 00 | 0.5, 0.5 / 1, 0 | [DERIVED] | 4 | tetragon.py; make_ledger.py |
| L41 | Two Tetragons: joint basis states; two 12-axis registers | 16; 16,777,216 | [DERIVED] | 6 | two_tetragons.py; make_ledger.py |
| L42 | Entanglement of equal-weight pure states with Schmidt rank 2 / 3 / 4 / 8 / 16 / 4,096 | 1 / 1.585 / 2 / 3 / 4 / 12 ebits | [DERIVED] | 6 | two_tetragons.py; make_ledger.py |
| L43 | Five correlation patterns of two Tetragons: Schmidt weights between the photons | 0.25 each (2 ebits) for all five | [DERIVED] | 6 | two_tetragons.py; make_ledger.py |
| L44 | Operator rank across polarization and twist of the relabelling of photon B: corresponding, horizontal, vertical, diagonal / cyclic | 1 (per-axis operations) / 4 (coupled operation) | [DERIVED] | 6 | two_tetragons.py |
| L45 | First four patterns are a polarization pair times a twist pair; cyclic rotation is not | yes / no (weights 0.25 across the cut) | [DERIVED] | 6 | two_tetragons.py; make_ledger.py |
| L46 | Cyclic rotation = axis SWAP then one flip; operator Schmidt rank 4 (does not factor); non-entangling by construction (SWAP sends a-times-b to b-times-a; 200 random real inputs spot-checked); a controlled phase does entangle | yes; yes; yes | [DERIVED] | 6 | two_tetragons.py |

## Not in the ledger

No [MEASURED] number exists. A ledger line with that tag will appear only after a PhaseKeep bench measurement.


---
*(c) 2026 Tyler O'Bryan, where applicable. PhaseKeep Research. Text CC BY 4.0, code MIT. AI-assisted research, documentation and numerical analysis. Draft for technical review.*
