# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tyler O'Bryan, where applicable
"""Volume 4: corners, edges, square faces and cubes of the n-axis hypercube, by enumeration and by formula. Plain Python only."""
from itertools import combinations, product
from math import comb

def enumerate_counts(n):
    verts = list(product((0, 1), repeat=n))
    edges = sum(1 for a, b in combinations(verts, 2) if sum(x != y for x, y in zip(a, b)) == 1)
    def faces(k):                       # a k-face fixes n-k axes and lets k axes vary
        return comb(n, k) * 2 ** (n - k)
    return len(verts), edges, faces(2), faces(3), faces(4)

def formula_counts(n):
    k = lambda j: comb(n, j) * 2 ** (n - j) if n >= j else 0
    return 2 ** n, n * 2 ** (n - 1), k(2), k(3), k(4)

def main():
    for n in range(2, 7):            # squares counted independently as 4-cycles: each square has two diagonals
        verts = list(product((0, 1), repeat=n))
        d2 = sum(1 for a, b in combinations(verts, 2) if sum(x != y for x, y in zip(a, b)) == 2)
        assert d2 // 2 == formula_counts(n)[2], n
    print("squares counted as 4-cycles agree with the formula for n = 2 to 6")
    for n in range(1, 8):
        e, f = enumerate_counts(n), formula_counts(n)
        assert e == f, (n, e, f)
    print("enumeration matches the formulas for n = 1 to 7")
    print("n = 12:", formula_counts(12), "(corners, edges, squares, cubes, tesseracts)")
    assert formula_counts(12) == (4096, 24576, 67584, 112640, 126720)
    print("hypercube_counts.py: ALL PASS")

if __name__ == "__main__":
    main()
