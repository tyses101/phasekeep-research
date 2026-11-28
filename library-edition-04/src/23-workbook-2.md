# Workbook II and Code

::: plain
This workbook lets you check Edition 04 for yourself. Part 1 has exercises for Volumes 15–22, with answers, from easy arithmetic to short derivations. Part 2 explains how to run the actual simulation programs behind Volumes 18–20, and what each one should print. You don't need to trust our numbers. Recompute them.
:::

## Part 1: Exercises

### Relationships (Volume 15)

1. Two qubits have correlation +1 in the standard basis and +1 in the diagonal basis. Which state from Volume 15's table is it? *Answer: Entangled A, (|00⟩ + |11⟩)/√2.*
2. A pure state of three Tetragons (six two-level parts): how many real numbers describe it, after removing normalization and overall phase? *Answer: dimension 2⁶ = 64, so 2·64 − 2 = 126.*
3. True or false: if every part of a system looks random on its own, the whole system must be random. *Answer: false. Entangled A and B are counter-examples.*

### Light (Volume 16)

4. What is the momentum of a 780 nm photon? Use h = 6.626 × 10⁻³⁴ J·s. *Answer: h/λ ≈ 8.49 × 10⁻²⁸ kg·m/s.*
5. A beam with twists ±2 is rotated by 10°. What relative phase appears? *Answer: 4 × 10° = 40°.*
6. Does a superposition of twist 0 and twist +2 share its Gouy phase (same radial index)? *Answer: no; |ℓ| differs (0 versus 2).*

### Atoms (Volume 17)

7. At what field ratio b/A is the middle-state concurrence exactly 0.5? *Answer: 1/√(1 + x²) = 0.5 gives x = √3 ≈ 1.73.*
8. The 2025 experiment measured populations 47.1%, 38.6% and 14.2%. Do they add to 100%? What does the remainder mean? *Answer: they add to 99.9%; the 0.1% is rounding in the reported values.*

### The ring (Volume 18)

9. Write the four ring-mode energies for J = 2. *Answer: +4, 0, −4, 0.*
10. On a six-site ring, the alternating phase shifts modes by how much? Which pairs are swapped? *Answer: by N/2 = 3; pairs {0, 3}, {1, 4}, {2, 5}.*
11. Why does the alternating phase on eight sites not preserve a code made of modes ±1? *Answer: it maps +1 to 5 ≡ −3, which is outside {+1, −1}.*

### Registers talking (Volume 19)

12. Ring A has hopping 3 MHz. Name a hopping for ring B that avoids every resonant ratio in Volume 19's model, other than the 1.5 ratio. *Answer: for example 4 MHz (ratio 1.33) or 2.5 MHz (ratio 1.2). Avoid 1.5, 3 and 6 MHz, which are ratios ½, 1 and 2. Note: 1.33 and 1.2 have smaller gaps than 1.5 in this model.*
13. In the compact encoding, how many qubits and entangling gates does the intended gate between four rings, in pairs, need? *Answer: 12 qubits; one CZ per coupled pair.*

### When things go wrong (Volume 20)

14. Bond error 2%, unevenness 0.3. Does the combined term stay below 1 in 10,000? *Answer: εα = 0.006 < 0.015, so yes: 0.43 × 0.006² ≈ 1.5 × 10⁻⁵.*
15. The echo's halves each accumulate 90 radians of hopping phase. Hopping drifts by 0.1% between halves. Roughly what phase error remains? *Answer: about 0.09 radians.*

### Checking (Volume 21)

16. Which errors pass both excitation counting and parity? Give one. *Answer: for example, a logical phase error caused by hopping drift, or a phase flip on both compact qubits.*
17. Why does [[4,2,2]] need location information to correct an error? *Answer: it can tell that an error occurred, but not which carrier, unless the location is flagged.*

### Machines (Volume 22)

18. Eight atoms with lifetime 400 µs; gate 5 µs. Survival per gate? *Answer: e^(−8 × 5/400) = e^(−0.1) ≈ 90.5%.*
19. What gate time gives 99% survival with eight atoms of lifetime 400 µs? *Answer: 8t/400 = 0.01, so t = 0.5 µs.*

## Part 2: Run the models

Every simulation behind Volumes 18–20 is in the repository under `code/atomic-register/`. Each is a short Python file using only Python 3 and NumPy. From that folder, run any file with `python -I <name>.py`, or run them all with `python -I run_all.py`, which writes logs to `results/logs/`.

| Program | What it checks | Key output to compare | Volume |
|---|---|---|---|
| `lie_check.py` | Control directions in the cloud model; the four-site flip | 10, 10, 15; flip block [[0,1],[1,0]] | 17, 18 |
| `ring_lie.py` | Why hopping is needed | 7, 9, 63 | 18 |
| `ring_gauge.py` | Flux 0, π, 2π: energies, currents, control | Currents ±0.5 at zero flux; 0 at 2π; dimensions 7, 15, 15 | 18 |
| `ring_chiral.py` | Code closure; eight-site twice-winding pattern | Closure ~10⁻¹⁶; 8-site maps 1 → 3 | 18 |
| `two_ring.py` | Hopping ratios | Ratios 1 and 2: leakage 1.0; 1.5: about 0.03 | 19 |
| `two_ring_shaped.py` | Abrupt versus smooth pulses | Final leakage 2.2 × 10⁻² versus 2.3 × 10⁻⁶ at equal time | 19 |
| `two_ring_echo.py` | The echo | 98.22% → 99.989% | 19 |
| `echo_combined.py`, `echo_statedep.py` | Echo with combined errors | Exact (~10⁻¹³) with uniform interaction; about 4 × 10⁻³ with uneven | 19, 20 |
| `ref01_onehot.py`, `ref01_diagnostics.py` | The 8-qubit digital version | Fidelity 1 in one step; a site detuning gives converging Trotter error | 19 |
| `ref_tolerance.py` | Single imperfections | Leakage ≈ 0.1 x²; growing bond-error phase | 20 |
| `p2cim.py`, `p2cim_analyze.py` | Coupled imperfections | 180 configurations; model E+ fit | 20 |
| `e5_drift.py` | Drift | Linear 0.394; jump 0.878; half-cycle 0.940 | 20 |
| `e6_flips.py` | Finite flips | Composite exact at α = 0; 7.0 × 10⁻³ with uneven interaction on | 20 |
| `e7_timing.py` | Echo timing | Symmetric echo: linear drift 3.2 × 10⁻⁴ | 20 |
| `e7d_notch.py`, `e7d_followup.py` | Notches and balance | 1.2–2.8 × 10⁻³; matched envelope 6.7 × 10⁻¹³; 1.43 × 10⁻⁵ | 20 |

::: try
Change one number and predict the result before running. Examples:
- Set the hopping ratio in `two_ring.py` to 1.2. Volume 19's gap argument predicts more leakage than at 1.5, but far less than at 1 or 2.
- Double the drift amplitude in `e5_drift.py`. The linear-drift infidelity should grow roughly fourfold while it is small, then saturate.
:::

::: watch
These programs are idealized models: no decoherence, normalized parameters, idealized pulses unless stated. A program agreeing with a printed value shows the arithmetic is right. It says nothing about whether real hardware behaves this way.
:::
