# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tyler O'Bryan, where applicable
"""Volume 8: the memory certification numbers. Plain Python only."""
import math

def bound(nbar=0.25):               # joint classical bound for four independent coherent-state modes
    return ((1 + nbar) / (1 + 2 * nbar)) ** 4

def fidelity(eta, v=0.0, nbar=0.25):   # pure loss eta plus added thermal noise v per mode
    return (1 + v + nbar * (1 - math.sqrt(eta)) ** 2) ** -4

def threshold(nbar):                 # noiseless minimum efficiency
    return (1 - 1 / math.sqrt(1 + nbar)) ** 2

def main():
    B = bound()
    print("joint bound at nbar = 0.25      :", round(B, 6))
    print("empty memory fidelity           :", round(fidelity(0.0), 4))
    print("threshold nbar = 0.25 / nbar = 1:", f"{100*threshold(0.25):.4f} %", f"{100*threshold(1):.4f} %")
    assert abs(B - 0.482253) < 5e-7 and abs(fidelity(0.0) - 0.4096) < 1e-9
    assert abs(100 * threshold(0.25) - 1.1146) < 5e-5 and abs(100 * threshold(1) - 8.5786) < 5e-5
    assert abs(fidelity(0.04, 0.04) - B) < 1e-3             # 4 % efficiency with v = 0.04 sits on the bound
    print("fidelity at 2 %, v = 1e-4       :", round(fidelity(0.02, 1e-4), 6))
    assert abs(fidelity(0.02, 1e-4) - 0.508185) < 5e-7
    print("\nchain: internal x converters x filter")
    for internal, conv, filt in ((0.04, 0.49, 0.23), (0.04, 0.49, 0.90), (0.126, 0.49, 0.23), (0.126, 0.49, 0.90)):
        eta = internal * conv * filt
        print(f"  {internal:6.3f} x {conv:4.2f} x {filt:4.2f} = {100*eta:6.3f} %   margin over bound {fidelity(eta) - B:+.4f}")
    print("\nrequired filter transmission (zero margin, no noise):")
    for internal, conv, expect in ((0.04, 0.49, 56.9), (0.04, 0.81, 34.4), (0.126, 0.49, 18.1), (0.126, 0.81, 10.9)):
        t = 100 * threshold(0.25) / (internal * conv)
        print(f"  internal {100*internal:4.1f} %, converters {conv:4.2f}: {t:5.1f} %")
        assert round(t, 1) == expect
    print("memory_thresholds.py: ALL PASS")

if __name__ == "__main__":
    main()
