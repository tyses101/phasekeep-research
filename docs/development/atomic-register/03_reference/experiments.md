# Experiments index

[← Start here](../README.md)

Each row gives the question, the script, the data, the headline result and the evidence class. Scripts live in [simulation source](https://github.com/tyses101/phasekeep-research/tree/main/code/atomic-register). Run logs are written to `code/results/logs/` by `run_all.py`.

| ID | Question | Script | Data | Headline result | Evidence |
|---|---|---|---|---|---|
| L1 | Is microwave + Raman control complete on the Tetragon? | `lie_check.py` | log | No: 10/15. A pure OAM flip gives 15/15. A four-site staggered phase is an exact flip | SIMULATED |
| L2 | Energetic-confinement robustness | `confine_robust.py` | log | Leakage = 1/(1+16Δ²) envelope; spectator phase ≈ (π/2)/(8Δ) | SIMULATED |
| L3 | Ring controllability | `ring_lie.py` | log | 7 / 9 / 63: needs hopping | SIMULATED |
| L4 | Chiral hopping and code closure | `ring_chiral.py` | log | 15/15; closure ~1e-16; N = 8 not closed | SIMULATED |
| L5 | Gauge and physical current | `ring_gauge.py` | log | Flux 2π: no current; flux π: current and splitting | SIMULATED |
| T1 | Two-ring hopping ratio | `two_ring.py` | log | Ratios 1 and 2 leak fully; ~1.5 works | SIMULATED |
| T2 | Ring spacing (mean interaction held fixed) | `two_ring.py D` | log | Leakage ≈ c(D)·(v/J)², c from 12 down to 0.5. **Not a speed result** | SIMULATED |
| T3 | Abrupt versus sin² pulse | `two_ring_shaped.py` | log | ~10⁴ lower final leakage at equal time | SIMULATED |
| T4 | Ring-mode echo | `two_ring_echo.py` | log | 98.22% → 99.989% (2-segment) | SIMULATED |
| REF-01 | One-hot single ring | `ref01_onehot.py` | log | Exact in 1 Trotter step; sanity controls pass | SIMULATED |
| REF-01d | Negative controls | `ref01_diagnostics.py` | log | Detuning gives n⁻⁴ Trotter convergence. Note the code-fidelity metric caveat (ch. 4) | SIMULATED |
| P2 | Single-ring tolerance | `ref_tolerance.py` | log | Leakage ≈ 0.1x², bounded; bond error grows into logical phase | SIMULATED |
| E1–E4 | Echo with combined errors | `echo_combined.py` | log | Exact under uniform V; bond + uneven V ≈ 4e-3 | SIMULATED |
| E3-SD | State-dependent hopping | `echo_statedep.py` | log | Still exact under uniform V | SIMULATED |
| P2-CIM | Coupled imperfection map | `p2cim.py`, `p2cim_analyze.py` | `p2cim_*.csv` | Sixth-order isolated; 0.43(εα)² cross term | SIMULATED |
| E5 | Dynamic drift | `e5_drift.py` | `e5_drift.csv` | Linear 0.39, step 0.88; balance condition | SIMULATED |
| E6 | Finite flips | `e6_flips.py` | `e6_flips.csv` | Composite exact if V off or uniform; 0.7% / 6.9% if uneven V on | SIMULATED |
| E7 | Echo timing | `e7_timing.py` | `e7_timing.csv` | E7-B best compromise; blind spots; continuous fails | SIMULATED |
| E7-D | Notches; balance | `e7d_notch.py`, `e7d_followup.py` | `e7d_*.csv` | Notches ~1e-3; factorization 6.7e-13; p ≈ 4; ∫g² balance | SIMULATED |
| A-1 | Hypercube equivalence | *(separate AI re-run (REPORTED))* | — | Residuals ≤ 2.5e-15 up to 5-cube | REPORTED |
| A-2 | Compact Gray REF-01 | *(audit)* | — | 0 entangling gates; residual 7.6e-16 | REPORTED |
| A-3 | REF-05 parity circuit | *(audit)* | — | 2 CNOT + 4 H; detection table (ch. 6) | REPORTED |
| A-4 | REF-03-P compilation | *(audit)* | — | 32 terms; 130 → 36 CNOT/slice; 64-slice 99.99759% | REPORTED |
| A-5 | Synchronized composite flips (first version) | *(independent run)* | — | 99.98868% recovered; amplitude/hopping error tables | REPORTED |
| A-6 | Excitation-count noise checks | *(audit)* | — | Uniform damping flagged; phase error passes | REPORTED |

**A-series scripts were run independently and are not included.** Codex should either obtain them or re-implement and re-verify them (see handoff).
