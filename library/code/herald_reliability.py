# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tyler O'Bryan, where applicable
"""Volume 7: herald probability, reliability and a simple random simulation. Plain Python only.
The three probabilities are the R30 reconstruction results for inputs (3, j), j < 3 (ideal detectors, a model, not a measurement)."""
import random

P_VALID, P_FALSE = 0.125, 0.25
P_HERALD = P_VALID + P_FALSE

def main():
    print("herald probability :", P_HERALD)
    print("valid  probability :", P_VALID)
    print("false-herald prob. :", P_FALSE)
    print("reliability        :", round(P_VALID / P_HERALD, 6), "(= 1/3)")
    assert P_HERALD == 0.375 and abs(P_VALID / P_HERALD - 1 / 3) < 1e-12
    rng = random.Random(2026)
    n = 100000
    herald = valid = 0
    for _ in range(n):
        r = rng.random()
        if r < P_VALID: herald += 1; valid += 1
        elif r < P_HERALD: herald += 1
    print(f"\n{n} simulated attempts: {herald} heralds, {valid} valid -> reliability {valid/herald:.4f}, herald rate {herald/n:.4f}")
    assert abs(valid / herald - 1 / 3) < 0.01
    print("1000 attempts with 375 heralds and 125 valid -> reliability", round(125 / 375, 4), "not 0.375")
    s = 0.95
    print("\nreuse: expected successful reuses", round(s / (1 - s), 6), "; survival after 10 cycles", round(s ** 10, 4))
    assert abs(s / (1 - s) - 19) < 1e-9 and abs(s ** 10 - 0.5987) < 5e-5
    print("herald_reliability.py: ALL PASS")

if __name__ == "__main__":
    main()
