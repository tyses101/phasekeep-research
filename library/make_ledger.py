#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tyler O'Bryan, where applicable
"""Generates src/A2-ledger.md and ledger.csv. Every DERIVED number is recomputed here and asserted against the stated value.
Run before build.py:  python3 make_ledger.py   (needs NumPy)"""
import csv
from math import comb
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
n = 0.25
fid = lambda e, v=0.0, nb=n: (1 + v + nb * (1 - np.sqrt(e)) ** 2) ** -4
B = ((1 + n) / (1 + 2 * n)) ** 4
thr = lambda nb: (1 - 1 / np.sqrt(1 + nb)) ** 2
def close(a, b, t): assert abs(a - b) <= t, (a, b)
close(B, 0.482253, 5e-7); close(fid(0), 0.4096, 1e-9); close(2 / 5, 0.40, 1e-12)
close(thr(0.25), 0.011146, 1e-6); close(thr(1), 0.085786, 1e-6)
close(fid(0.04, 0.04), B, 1e-3); close(fid(0.02, 1e-4), 0.508185, 5e-7)
close(0.507107 - B, 0.024854, 1e-6); close(0.04 * 0.49 * 0.23, 0.004508, 1e-9)
for i, c, t in ((0.04, .49, 56.9), (0.04, .81, 34.4), (0.126, .49, 18.1), (0.126, .81, 10.9)):
    close(round(100 * thr(0.25) / (i * c), 1), t, 0.051)
close(0.95 ** 10, 0.5987, 5e-5); close(0.95 / 0.05, 19, 1e-9)
close(0.375 - 0.125, 0.25, 1e-12); close(0.125 / 0.375, 1 / 3, 1e-12)
close(0.7 * 0.04 * 0.7, 0.0196, 1e-12); close(0.22 ** 2, 0.0484, 1e-12)
assert (2**12, 12 * 2**11, comb(12, 2) * 2**10, comb(12, 3) * 2**9) == (4096, 24576, 67584, 112640)
close(0.125 * 0.04 * 0.49 * 0.23, 0.0005635, 1e-9); close(0.125 * 0.126 * 0.49 * 0.9, 0.00694575, 1e-9); close(1 - 6 / 7, 0.14, 0.005); close(1 - 126 / 157, 0.20, 0.005)

def _sw(psi): return np.linalg.svd(np.asarray(psi).reshape(2, 2), compute_uv=False) ** 2
_edge = np.array([1, 1, 0, 0]) / np.sqrt(2); _diag = np.array([1, 0, 0, 1]) / np.sqrt(2)
assert comb(12, 4) * 2 ** 8 == 126720 and comb(6, 4) * 2 ** 2 == 60
assert np.allclose(_sw([.5, .5, .5, .5]), [1, 0]) and np.allclose(_sw([.5, .5, .5, -.5]), [.5, .5])
_mix = np.zeros(4); _mix[0] = np.cos(np.pi / 4); _mix[3] = np.sin(np.pi / 4)
assert np.allclose(_sw(_mix), [.5, .5]) and np.allclose(_sw([0, 0, 0, 1]), [1, 0])
assert np.allclose(_sw(_edge), [1, 0]) and np.allclose(_sw(_diag), [.5, .5])
_rng = np.random.default_rng(1)
def _U():
    q, _ = np.linalg.qr(_rng.normal(size=(2, 2)) + 1j * _rng.normal(size=(2, 2))); return q
for _ in range(20): assert np.allclose(_sw(np.kron(_U(), _U()) @ _diag), [.5, .5])
R = []  # id, quantity, value, tag, volume, source
def add(*a): R.append(a)
add("L01", "Joint classical bound, coherent states, n̄ = 0.25, four modes", "0.482253", "DERIVED", "8", "verify_r25.py; proof awaiting independent review (B03)")
add("L02", "Fidelity of an empty memory (η = 0, no noise)", "0.4096", "DERIVED", "8", "verify_r25.py")
add("L03", "Single-photon benchmark 2/(d+1), d = 4, hidden Haar-random inputs", "0.40", "DERIVED", "2, 8", "verify_r25.py (section B); standard result")
add("L04", "Entangled-target overlap benchmark", "0.25", "DERIVED", "8", "verify_r25.py (section B)")
add("L05", "Noiseless efficiency threshold, n̄ = 0.25", "1.1146 %", "DERIVED", "8", "verify_r25.py")
add("L06", "Noiseless efficiency threshold, n̄ = 1", "8.5786 %", "DERIVED", "8", "verify_r25.py")
add("L07", "Noise v at which 4 % efficiency sits on the bound", "0.04", "DERIVED", "8", "verify_r25.py")
add("L08", "Fidelity at 2 % efficiency, v = 1e-4", "0.508185", "DERIVED", "8", "verify_r25.py")
add("L09", "Analytic-anchored combined fidelity / margin over bound", "0.507107 / 0.024854", "SIMULATED", "8", "verify_r25.py; Monte Carlo error only")
add("L10", "Detector-efficiency crossover (ideal, infinite statistics)", "85.73 %", "DERIVED", "8", "verify_r25.py")
add("L11", "Chain 4 % × 0.49 × 23 %", "0.451 %", "DERIVED", "8", "verify_r25.py; inputs ASSUMED or supplied")
add("L12", "Required filter transmission, zero margin (4 %, 0.49 / 4 %, 0.81 / 12.6 %, 0.49 / 12.6 %, 0.81)", "56.9 / 34.4 / 18.1 / 10.9 %", "DERIVED", "8", "verify_r25.py")
add("L13", "Margins over the bound for filter rows (0.451 % / 1.764 % / 1.420 % / 5.557 %)", "−0.0272 / +0.0198 / +0.0098 / +0.0975", "DERIVED", "8", "verify_r25.py")
add("L14", "Earlier time-mode chain 0.70 × 0.04 × 0.70", "1.96 %", "ASSUMED", "8", "historical modelling")
add("L15", "Herald / occupancy-valid / false-herald probability for inputs (3, j), j < 3", "0.375 / 0.125 / 0.25", "SIMULATED", "7", "outcome_resolved_herald_r30.py (ideal PNR detectors, reconstruction-specific)")
add("L16", "Herald reliability, worst case studied", "1/3 (33.3 %)", "SIMULATED", "7", "outcome_resolved_herald_r30.py")
add("L17", "Probability all heralds fire, 2 stages / 16 stages", "0.01953125 / 1.4725e-14", "SIMULATED", "7", "SIM-06; audit_bundle_r25.py")
add("L18", "Fidelity given heralds, 2/4/8/16 reactions (ideal)", "80.0 / 67.0 / 48.0 / 24.3 %", "SIMULATED", "7", "SIM-06")
add("L19", "Same with correlated phase drift σ = 0.05 rad", "78.7 / 62.8 / 37.2 / 9.1 %", "SIMULATED", "7", "SIM-06")
add("L20", "Fidelity given occupancy-valid, 2 stages", "98.5 %", "SIMULATED", "7", "SIM-06")
add("L21", "Reuse: expected successful reuses s/(1−s) at s = 0.95; survival after 10 cycles", "19; 59.87 %", "DERIVED", "7", "arithmetic")
add("L22", "Hypercube counts, n = 12: corners / edges / squares / cubes", "4,096 / 24,576 / 67,584 / 112,640", "DERIVED", "4", "enumeration check")
add("L23", "Operator Schmidt rank: CP on Z4×Z4 / one CPF", "4 / 2", "DERIVED", "6", "numerical check")
add("L24", "Minimum number of CPF gates for CP", "at least 2 (true count undefined)", "DERIVED", "6", "rank bound")
add("L25", "Heralded gate theoretical success", "1/4 × 1/2 = 1/8", "REPORTED", "6", "Liu et al. arXiv 2407.16356, read")
add("L26", "Process fidelity of the heralded gate", "0.64 to 0.82", "REPORTED", "6", "Liu et al., read")
add("L27", "Atom–cavity gate: fidelity / two-photon transmission / bandwidth", "76.2 ± 3.6 % (abstract) / 4.8 % and 0.7 MHz (project notes)", "REPORTED", "6", "Hacker et al. arXiv:1605.05261; fidelity checked in the abstract, the other two unconfirmed")
add("L28", "Bandwidth ratio, ~1 GHz memory band to 0.7 MHz", "about 1,400×", "DERIVED", "6", "arithmetic on supplied values")
add("L29", "A06 parts saved, full readout: N = 2 / N = 32", "14 % / 20 %", "SIMULATED", "4, 9", "a06_precursor_sim.py (counts; error inputs ASSUMED)")
add("L30", "A06 conditional fidelity, shared vs individual, N = 2 / N = 32", "0.99961 vs 0.99959 / 0.99954 vs 0.99471", "SIMULATED", "4, 9", "a06_precursor_sim.py (ASSUMED errors)")
add("L31", "Parameters of a pure d-level state", "2d − 2", "DERIVED", "2, 4", "standard")
add("L32", "Check counts: verify_r25 / spec / A06 self-checks / R30 independent rerun", "71 / 12 / 19 / 20", "REPORTED", "9", "script output; R30 rerun by second party")
add("L35", "Illustrative joint yield, supplied chain: 0.125 × 0.00451", "0.056 % (about 1 in 1,800)", "DERIVED", "12", "arithmetic on SIMULATED and ASSUMED inputs; independence assumed")
add("L36", "Illustrative joint yield, better chain (5.557 %)", "0.69 % (about 1 in 144)", "DERIVED", "12", "arithmetic on SIMULATED and ASSUMED inputs; independence assumed")
add("L37", "Fusion-based scheme: tolerated photon loss per fusion (ballistic scheme)", "10.4 %", "REPORTED", "13", "Bartolucci et al. arXiv:2101.09310, abstract only; not comparable to other numbers here")
add("L38", "Tesseracts (4-cubes) in a 12-axis register, subspace dimension 16", "126,720", "DERIVED", "4", "hypercube_counts.py; make_ledger.py")
add("L39", "Schmidt weights: (00+01+10+11)/2 / (00+01+10−11)/2 (same probabilities, 0.25 each)", "1, 0 / 0.5, 0.5", "DERIVED", "10", "tetragon.py; make_ledger.py")
add("L40", "Schmidt weights after rotating 00 toward 11 by 45° / after X⊗X on 00", "0.5, 0.5 / 1, 0", "DERIVED", "4", "tetragon.py; make_ledger.py")
# two Tetragons (Volume 6, section 6.7)
def _sw(perm):
    m = np.zeros((4, 4))
    for a in range(4): m[a, perm[a]] = 0.5
    return m
for _p in ([0,1,2,3], [1,0,3,2], [2,3,0,1], [3,2,1,0], [1,3,0,2]):
    assert np.allclose(np.linalg.svd(_sw(_p), compute_uv=False) ** 2, 0.25)
close(np.log2(3), 1.585, 5e-4); close(np.log2(4096), 12, 1e-12); assert 4096 * 4096 == 16777216
_pairs = lambda perm: _sw(perm).reshape(2, 2, 2, 2).transpose(0, 2, 1, 3).reshape(4, 4)
for _p in ([0,1,2,3], [1,0,3,2], [2,3,0,1], [3,2,1,0]): assert np.allclose(np.linalg.svd(_pairs(_p), compute_uv=False) ** 2, [1, 0, 0, 0])
assert np.allclose(np.linalg.svd(_pairs([1,3,0,2]), compute_uv=False) ** 2, 0.25)
add("L41", "Two Tetragons: joint basis states; two 12-axis registers", "16; 16,777,216", "DERIVED", "6", "two_tetragons.py; make_ledger.py")
add("L42", "Entanglement of equal-weight pure states with Schmidt rank 2 / 3 / 4 / 8 / 16 / 4,096", "1 / 1.585 / 2 / 3 / 4 / 12 ebits", "DERIVED", "6", "two_tetragons.py; make_ledger.py")
add("L43", "Five correlation patterns of two Tetragons: Schmidt weights between the photons", "0.25 each (2 ebits) for all five", "DERIVED", "6", "two_tetragons.py; make_ledger.py")
add("L44", "Operator rank across polarization and twist of the relabelling of photon B: corresponding, horizontal, vertical, diagonal / cyclic", "1 (per-axis operations) / 4 (coupled operation)", "DERIVED", "6", "two_tetragons.py")
add("L45", "First four patterns are a polarization pair times a twist pair; cyclic rotation is not", "yes / no (weights 0.25 across the cut)", "DERIVED", "6", "two_tetragons.py; make_ledger.py")
add("L46", "Cyclic rotation = axis SWAP then one flip; operator Schmidt rank 4 (does not factor); non-entangling by construction (SWAP sends a-times-b to b-times-a; 200 random real inputs spot-checked); a controlled phase does entangle", "yes; yes; yes", "DERIVED", "6", "two_tetragons.py")
add("L33", "Schmidt weights: edge blend (00+01)/√2 / diagonal blend (00+11)/√2", "1, 0 / 0.5, 0.5", "DERIVED", "4", "make_ledger.py (numerical check)")
add("L34", "Schmidt weights after independent unitaries on each axis (20 random trials)", "unchanged", "DERIVED", "4", "make_ledger.py (numerical check)")

R.sort(key=lambda r: r[0])
with open(HERE / "ledger.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["id", "quantity", "value", "evidence_tag", "volume", "source_or_script"]); w.writerows(R)
md = ["# The Ledger of Numbers", "",
      "Every number used in the series, with its evidence tag and where it comes from. Derived values were recomputed by `make_ledger.py` when this page was built. The same table is in `ledger.csv`, which opens in any spreadsheet.", "",
      "::: watch", "A **DERIVED** tag means the arithmetic checks out under the stated assumptions. It does not mean the assumptions hold in a laboratory.", ":::", "",
      "| ID | Quantity | Value | Tag | Vol. | Source |", "|---|---|---|---|---|---|"]
for r in R:
    md.append(f"| {r[0]} | {r[1]} | {r[2]} | [[{r[3]}]] | {r[4]} | {r[5]} |")
md += ["", "## Not in the ledger", "", "No [[MEASURED]] number exists. A ledger line with that tag will appear only after a PhaseKeep bench measurement."]
(HERE / "src" / "A2-ledger.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print("ledger ok,", len(R), "rows")
