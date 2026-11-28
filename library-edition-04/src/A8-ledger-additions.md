# Ledger Additions

Every number used in Volumes 15–17, with its evidence tag and where it came from. Numbering continues the idea of Edition 03's ledger (Appendix 2) with a new prefix, **E4-**, so no Edition 03 identifier is reused.

| ID | Number | Meaning | Tag | Source |
|---|---|---|---|---|
| E4-01 | 50/50, +1, +1/−1/0, 1/1/½ | Bell-state comparison table (15.3) | [[DERIVED]] | Standard two-qubit algebra |
| E4-02 | 16, 6, 4, 30 | Two-Tetragon dimension, pairs, triples, real parameters (15.8) | [[DERIVED]] | Counting; 2·16 − 2 = 30 |
| E4-03 | ≥ 3 levels | Minimum dimension for contextuality (15.6) | [[REPORTED]] | Kochen–Specker; Mermin 1990 (abstract) |
| E4-04 | 1.02, 1.25, 1.47 × 10⁻²⁷ kg·m/s | Photon momentum at 650, 532, 450 nm (16.1) | [[DERIVED]] | p = h/λ |
| E4-05 | 461, 564, 666 THz; 1.91, 2.33, 2.76 eV | Frequency and energy at the same wavelengths (16.1) | [[DERIVED]] | f = c/λ, E = hc/λ |
| E4-06 | 2p + \|ℓ\| + 1 | Gouy phase dependence (16.4) | [[DERIVED]] | Standard Laguerre–Gauss beam formula |
| E4-07 | 2θ, 4θ, θ, 2θ | Rotation phases for ±1, ±2, 0/+1 and circular polarization (16.5) | [[DERIVED]] | Phase ℓθ (and sθ for spin) |
| E4-08 | about 1,000 atoms; 60S, 59P, 59S | Experiment setup (17.3) | [[REPORTED]] | Jiao et al. 2025, full text §III |
| E4-09 | 18.51 GHz, 18.23 GHz | Microwave transition frequencies (17.3) | [[REPORTED]] | Jiao et al. 2025 |
| E4-10 | < 1.8 µs | Complete sequence time (17.3) | [[REPORTED]] | Jiao et al. 2025 |
| E4-11 | 0.45 ± 0.05 | g⁽²⁾(0) single-excitation measure (17.3) | [[REPORTED]] | Jiao et al. 2025 |
| E4-12 | 47.1%, 38.6%, 14.2% | Measured level populations (17.3) | [[REPORTED]] | Jiao et al. 2025 |
| E4-13 | 10–100 µs, ~123 µs, 406 µs | Rydberg lifetimes: typical alkali; 55P at room temperature; 55P at 4 K (17.2) | [[REPORTED]] | Jiao et al. 2025 (typical range); arXiv:2602.05959 (55P), summary level |
| E4-14 | 1/√(1 + x²) and the table values | Concurrence of the middle states versus field ratio x = b/A (17.5) | [[DERIVED]] | Two-spin hyperfine model |
| E4-15 | +2J, 0, −2J, 0 | Ring-mode energies (18.2) | [[DERIVED]] | 2J cos(πℓ/2) |
| E4-16 | ±0.5 | Currents of modes 1 and 3 at zero flux, model units (18.2) | [[SIMULATED]] | `code/atomic-register/ring_gauge.py` |
| E4-17 | 0 | Leakage of the staggered flip on the code (18.4) | [[SIMULATED]] | `lie_check.py`, `ring_chiral.py` |
| E4-18 | 7, 9, 63 of 63 | Control directions reached with/without hopping (18.5) | [[SIMULATED]] | `ring_lie.py` |
| E4-19 | ±1.41J, ±0.35 | Flux-π energies and currents (18.6) | [[SIMULATED]] | `ring_gauge.py` |
| E4-20 | ≲ 2.5 × 10⁻¹⁵ | Ring/hypercube ↔ independent-rotation equivalence residuals (18.7) | [[REPORTED]] | Independent re-run by a separate AI assistant; script not in the repository |
| E4-21 | 1, 2, ½; 1.5 | Forbidden and best hopping ratios (19.2) | [[DERIVED]] | Energy-coincidence analysis |
| E4-22 | 100%, 3.9%, 3.0%, 2.4%, 100% | Worst leakage at ratios 1, 1.425, 1.5, 1.575, 2 (v/J_B = 0.05, D = 2) (19.2) | [[SIMULATED]] | `two_ring.py` |
| E4-23 | 2.2 × 10⁻², 2.3 × 10⁻⁶ | Final leakage, abrupt vs sin² at equal time (19.3) | [[SIMULATED]] | `two_ring_shaped.py` |
| E4-24 | 98.22% → 99.989% | Gate fidelity without/with echo (19.4) | [[SIMULATED]] | `two_ring_echo.py` |
| E4-25 | ~10⁻¹⁴ | Echo cancellation with 10% bond error, uniform interaction, incl. state-dependent hopping (19.4) | [[SIMULATED]] | `echo_combined.py`, `echo_statedep.py` |
| E4-26 | 8 / 3 qubits; 16 / 6; 8 gates; 0 gates; 1 CZ | Encodings and costs (19.6) | [[DERIVED]] | Volume 18 mapping; `ref01_onehot.py` |
| E4-27 | 130 → 36 CNOT per slice; 2,304 total | Physical-interaction emulation cost (19.6) | [[REPORTED]] | Independent re-run; script not in the repository |
| E4-28 | 0.1 x²; 2 × 10⁻³ | Single-flaw leakage; 1% bond error over T = 10/J (20.2) | [[SIMULATED]] | `ref_tolerance.py` |
| E4-29 | sixth power; 0.43(εα)²; 0.15, 0.05, 0.015, 0.005 | Coupled-imperfection fit and budget (20.3) | [[SIMULATED]] | `p2cim.py`, `p2cim_analyze.py` |
| E4-30 | ~0, 39%, 81–88%, 94%, 10⁻⁹–10⁻⁸ | Drift results (20.4) | [[SIMULATED]] | `e5_drift.py` |
| E4-31 | ~90 rad | Hopping phase per echo half in the gate (20.4) | [[DERIVED]] | 2J·T_seg with T_seg ≈ 31/J |
| E4-32 | 53%, 40%, exact, 0.7% / 6.9%, 5 × 10⁻⁵ | Finite-flip results (20.5) | [[SIMULATED]] | `e6_flips.py` |
| E4-33 | 1.4 × 10⁻⁵ vs 1.7 × 10⁻⁶; ~1,000× | Symmetric vs original echo (20.6) | [[SIMULATED]] | `e7_timing.py` |
| E4-34 | 1.2–2.8 × 10⁻³; 4th power; table values | Notch results and balance comparison (20.7) | [[SIMULATED]] | `e7d_notch.py`, `e7d_followup.py` (follow-up confirmation pending at publication of the atomic-register checkpoint) |
| E4-35 | 25% fidelity, count passes | Phase error invisible to excitation counting (21.3) | [[REPORTED]] | Independent re-run; script not in the repository |
| E4-36 | 2 two-qubit + 4 single-qubit gates; 100%, 0%, 0%, 50% | Parity-check circuit and detection table (21.4) | [[REPORTED]] | Independent re-run; script not in the repository |
| E4-37 | up to 94% infidelity, tiny leakage | Hidden drift error (21.5) | [[SIMULATED]] | `e5_drift.py` |
| E4-38 | fewer than 4 qubits | No universal single-error detection for two logical qubits (21.6) | [[DERIVED]] | Exploration S29 (repository `explorations/`) |
| E4-39 | e^(−t ΣΓ); 𝓑 = 1/(t ΣΓ) | Survival and loss budget (22.2) | [[DERIVED]] | Exponential decay |
| E4-40 | 8 | Fragile atoms in a two-ring S/P exchange gate (22.2) | [[DERIVED]] | Model of Volume 18 |
| E4-41 | ~10 µs | Gate time at 1 MHz hopping, v = 0.1 J (22.3) | [[DERIVED]] from [[ASSUMED]] 1 MHz | 2π/v × 159 ns |
| E4-42 | 20%, 52%, 82% | Survival per gate at lifetimes 50, 123, 406 µs (22.3) | [[DERIVED]] from [[REPORTED]] lifetimes | arXiv:2602.05959 (123 and 406 µs, summary); 50 µs illustrative |
| E4-43 | ~7.5 MHz; ~1.3 µs; ~92%, ~97% | Faster-hopping illustration (22.3) | [[DERIVED]] from **mixed** [[REPORTED]] inputs | C₃ from arXiv:1705.03293 (summary) with lifetimes above. Illustrative only |
| E4-44 | 74%, 4.8%; 99.9%, 99.0% | Compounding over 10 and 100 gates (22.3) | [[DERIVED]] | Powers of 0.97 and 0.9999 |
| E4-45 | 2.55 ms, 3.7 ms | Circular Rydberg lifetimes (22.4) | [[REPORTED]] | PRX 14, 021024 (2024); arXiv:2510.27471 (summaries) |
| E4-46 | few–tens of kHz | Predicted circular-state exchange (22.4) | [[REPORTED]] (theory) | Nguyen et al. 2018; arXiv:2411.14854 (summaries) |
| E4-47 | ~13 kHz | Rydberg-dressed interaction (22.4) | [[REPORTED]] | Zeiher et al. 2017 (summary) |
| E4-48 | 126; 8.49 × 10⁻²⁸; √3 | Workbook answers (Volume 23) | [[DERIVED]] | Arithmetic shown in Volume 23 |
