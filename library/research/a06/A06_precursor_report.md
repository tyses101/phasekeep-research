# A06 precursor: shared versus individually addressed transformation

Prepared 2026-11-26. Modeled results only. **Every error and loss number is an assumed sensitivity input, not a measurement.** Counts are derived from stated conventions. Not independently reviewed. No claim of demonstrated efficiency.

## What was simulated
Operation: H↔V polarization exchange applied coherently to all N OAM modes, each mode left in place. Mode family ℓ ∈ {−(N−1), …, +(N−1)} in steps of 2 (mirror closed; N = 2 is the Tetragon pair ±1). N = 2, 4, 8, 16, 32.

- **Shared:** one half-wave plate acts on all modes.
- **Individual:** sorter (binary tree of N−1 interferometers, 3 elements each) → one plate per mode → inverse sorter.

Metrics: conditional and unconditional process fidelity against the ideal operation, worst-input fidelity, transmission, element counts by stage, calibration parameters. 400 Monte Carlo draws per point, fixed seed, 95% half-widths ≤ 1e-4 on fidelity at default settings.

Self-checks (19, all pass): zero-error limit gives fidelity 1 and transmission 1 for both designs at every N; closed form F = |mean cos(ε_ℓ/2)|² for the shared plate; sorter error matrix is orthogonal; aperture formula; count formulas; determinism.

Default assumed inputs: plate calibration residual 0.01 rad; shared-plate retardance drift κ = 5e-4 rad per unit |ℓ|; Dove-prism rotation error 2e-3 rad (node phase error scales with |ℓ|); 0.2% loss per element; aperture sized so the largest mode loses 0.1% per element (R/w = 5.12 at N = 32).

## Your five questions

**1. How much equipment can be eliminated?** (illustrative element counts)

| N | in place (operation) | read polarization only | full OAM + polarization readout | calibration parameters |
|---|---|---|---|---|
| 2 | 1 vs 8 | 2 vs 9 | 6 vs 7 | 2 vs 8 |
| 4 | 1 vs 22 | 2 vs 23 | 14 vs 17 | 2 vs 20 |
| 8 | 1 vs 50 | 2 vs 51 | 30 vs 37 | 2 vs 44 |
| 16 | 1 vs 106 | 2 vs 107 | 62 vs 77 | 2 vs 92 |
| 32 | 1 vs 218 | 2 vs 219 | 126 vs 157 | 2 vs 188 |

(shared vs individual). The naive "16 plates versus 1" undercounts the individual design, because separating modes needs a sorter and recombining needs a second one. The saving is large when the state stays in place, and falls to the N−1 plates (14% at N = 2, about 20% at N = 32) when every mode must be resolved at the end.

**2. When do imperfections matter?** Default assumptions, conditional fidelity (transmission):

| N | shared | individual |
|---|---|---|
| 2 | 0.99961 (0.997) | 0.99959 (0.979) |
| 8 | 0.99956 (0.998) | 0.99935 (0.958) |
| 16 | 0.99962 (0.998) | 0.99852 (0.948) |
| 32 | 0.99954 (0.998) | 0.99471 (0.937) |

The individual design degrades with N through sorter error (which grows with |ℓ|) and element loss. With Dove-prism error 5e-3 it falls to 0.970 at N = 32, and to 0.886 at 1e-2. The shared design loses to the individual one only if the single plate's retardance varies across the mode family by roughly 0.01 rad (N = 2) to 0.23 rad (N = 32) over the full range, i.e. κ* ≈ 6e-3 to 1e-2 rad per unit |ℓ|, about 13 to 20 times the default. Whether a real plate behaves like that is unknown and is the first thing to measure.

**3. Does preparation and decoding cancel the savings?** Preparation is the same for both designs, so it does not change the comparison (counted: SLM-type 1 element, sorter-based 3 to 93; fidelity not simulated). Decoding is what matters: if the OAM label must be resolved at the end, the saving drops to about 20%. If the information stays in the mode family and only polarization (or only the final result) is read, the saving is nearly the whole sorter and recombiner. This is a property of the architecture, not of the waveplate.

**4. Which transformations stay simple as N grows?** Simulated: only the polarization exchange. Reasoned, not simulated: operations on a property that is independent of the mode (waveplates) stay one element; a rotation phase proportional to ℓ (Dove prism, image rotation) is also one element but its sensitivity grows with Δℓ; ℓ-selective operations such as flipping one OAM bit need either sorting or a conversion element such as a q-plate, which has leakage and closure issues. These are the next things to simulate.

**5. Which encodings are most practical?** This run does not rank encodings. It supports one narrow point: a polarization operation shared across an OAM family is cheap and scales well under these assumptions, so polarization × OAM remains a good first build, with N = 2 (Tetragon) first and N = 4 to 8 as scaling studies.

## Limits
- The sorter model is an illustrative interferometric tree with assumed node errors, not a specific device. Published OAM sorters are different devices with different efficiencies, so the individual design here may be optimistic, which would understate the shared design's advantage in transmission.
- Radial modes, wavelength dependence, polarization-dependent sorter errors, preparation fidelity, detection and any inter-photon operation are not modeled.
- The shared plate's only mode dependence is the single parameter κ; the mechanism behind it (retardance non-uniformity across a larger beam) is a hypothesis.
- Three sorter measurements must stay separate in any engineering calculation: modes tested, discrimination accuracy, optical transmission. From the source abstracts checked in this session: Berkhout et al. (PRL 105, 153601) report sorting eleven OAM states, with no efficiency figure in the abstract; Mirhosseini et al. (Nat. Commun. 4, 2781) report a separation efficiency above 92% against about 77% for earlier methods, with no mode count in the abstract. The 25-mode and 92.1% figures were not rechecked, and whether "separation efficiency" there includes optical transmission needs the full text.

## Suggested first bench measurements (classical light; single-photon linear operations are equivalent)
1. Retardance, axis and transmission of one half-wave plate versus ℓ for LG modes up to the largest N, to estimate κ.
2. Crosstalk matrix and transmission of the chosen sorter, reported separately.
3. Repeat at N = 2, 4, 8.

## Files
`a06_precursor_sim.py` (numpy only; `python3 -I a06_precursor_sim.py <outdir>`; exit 0 only if all checks pass), `results/a06_precursor_results.csv` (120 rows), `results/a06_precursor_summary.json`, `run_log.txt`.
