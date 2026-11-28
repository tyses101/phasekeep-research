# How to reproduce everything

[← Start here](../README.md)

## Requirements
- **Python:** 3.9 or newer, with **NumPy** (`code/requirements.txt`). No SciPy is needed. Nelder–Mead is implemented inline in `e6_flips.py`.
- **Platform:** tested on Windows with Python 3.12 + NumPy. Results are deterministic (fixed random seeds).

## One command
```
cd code
python -I run_all.py            # everything; P2-CIM and E7-D take several minutes
python -I run_all.py --quick    # skips the four slow scripts
```
**Output:** `code/results/logs/<script>.log` for each script, plus `SUMMARY.txt` with exit codes and run times. CSVs are written to `code/results/`.

## Individual scripts
Run from inside `code/` with `python -I <script>.py`. `p2cim_analyze.py` needs `p2cim.py` run first. `two_ring_shaped.py`, `two_ring_echo.py`, `echo_combined.py` and `echo_statedep.py` import `two_ring.py` from the same folder. `two_ring.py D` runs the spacing sweep.

## What to compare against
| Script | Expected (key lines) |
|---|---|
| `lie_check.py` | 10 / 10 / 15; ring flip block [[0,1],[1,0]] |
| `ring_lie.py` | 7 / 9 / 63 |
| `ring_gauge.py` | Lie dimension 7 / 15 / 15; current 0 at flux 2π |
| `two_ring_echo.py` | single 98.22130%, 2-segment 99.98869% (D = 2, v = 0.1) |
| `echo_combined.py` | E1 ~1e-13; E4 ≈ 4.0e-3 |
| `p2cim.py` | 180 configurations; convergence identical across 600 / 1200 / 2400 steps |
| `e5_drift.py` | linear 0.394, step 0.878, ½-cycle 0.940 (α = 0) |
| `e6_flips.py` | composite exact at α = 0; 7.0e-3 with uneven V on |
| `e7_timing.py` | E7-B linear 3.2e-4; E7-C 1.2e-3 at α = 0.5 |
| `e7d_followup.py` | matched-envelope 6.7e-13; sym-seg 1.43e-5 |

## Conventions
- **Units:** ħ = 1, J_B = 1. Physical conversions assume J_B/h = 1 MHz, so one time unit = 159 ns.
- **Basis order:** (ring mode, internal) ⊗ (ring mode, internal). Code = modes {0, 2} × {R1, R2}.
- **Fidelity:** leakage-aware F_avg = (|Tr W|² + Tr W†W)/(d(d+1)), with W = C†U_target†U C and d = 16.
- **Leakage:** worst case = spectral norm of I − K†K, with K = C†UC.
