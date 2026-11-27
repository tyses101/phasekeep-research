# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tyler O'Bryan, where applicable
"""Entanglement quantity versus entanglement organization, for two photons that each carry a Tetragon.

Four subsystems, in this order: 0 = A-polarization, 1 = A-OAM, 2 = B-polarization, 3 = B-OAM  (each two-level).
A state is a list of 16 real amplitudes; the index is 8*pA + 4*tA + 2*pB + tB.
Plain Python only (no NumPy), so that it can be checked independently of any numerical library.

What it checks (all [[DERIVED]]):
  1. Matching (SEE-type) and cross (NEE-type) pairings both give four equal Schmidt weights between the photons: 2 ebits, a 16-dimensional joint Hilbert space.
  2. Single-axis local unitary transformations preserve the relevant pairing structure and bipartite entanglement; an ideal axis SWAP on photon B reorganizes existing pairings. It does not generate entanglement between the swapped axes from their product states.
  3. Having four levels per photon does not make the entanglement high-dimensional: a state can have Schmidt rank 2.
  4. A four-subsystem GHZ-type state is genuinely multipartite and is NOT a product of entangled pairs.
"""
from itertools import product
from math import log2, cos, sin, sqrt
import random

NAMES = ["A-pol", "A-OAM", "B-pol", "B-OAM"]
SPLITS = {"photon partition (A | B)": (0, 1),   # subsystems on the left side of the cut
          "matched pairs (pol-pol | OAM-OAM)": (0, 2),
          "cross pairs (A-pol,B-OAM | A-OAM,B-pol)": (0, 3)}

def idx(bits):                         # bits = (pA, tA, pB, tB)
    return 8 * bits[0] + 4 * bits[1] + 2 * bits[2] + bits[3]

def bits(i):
    return (i >> 3 & 1, i >> 2 & 1, i >> 1 & 1, i & 1)

def normalize(v):
    n = sqrt(sum(x * x for x in v)); return [x / n for x in v]

def pair_state(pairing):
    """Equal blend over the four address values a = (p, t) of A, with B holding pairing(a). pairing maps (p,t) -> (p',t')."""
    v = [0.0] * 16
    for p, t in product((0, 1), repeat=2):
        pb, tb = pairing(p, t); v[idx((p, t, pb, tb))] = 1.0
    return normalize(v)

matching = pair_state(lambda p, t: (p, t))          # polarization with polarization, OAM with OAM
cross = pair_state(lambda p, t: (t, p))             # polarization with OAM, OAM with polarization

def matrix_for_cut(v, left):
    """Rows indexed by the subsystems in `left` (in increasing order), columns by the rest."""
    right = [k for k in range(4) if k not in left]
    M = [[0.0] * 4 for _ in range(4)]
    for i, a in enumerate(v):
        b = bits(i)
        r = 2 * b[left[0]] + b[left[1]]; c = 2 * b[right[0]] + b[right[1]]
        M[r][c] += a
    return M

def rank(M, tol=1e-9):
    m = [row[:] for row in M]; r = 0
    for c in range(len(m[0])):
        piv = max(range(r, len(m)), key=lambda i: abs(m[i][c]))
        if abs(m[piv][c]) < tol: continue
        m[r], m[piv] = m[piv], m[r]
        for i in range(len(m)):
            if i != r:
                f = m[i][c] / m[r][c]; m[i] = [x - f * y for x, y in zip(m[i], m[r])]
        r += 1
        if r == len(m): break
    return r

def purity(M):
    rho = [[sum(M[i][k] * M[j][k] for k in range(4)) for j in range(4)] for i in range(4)]
    return sum(rho[i][j] ** 2 for i in range(4) for j in range(4))

def cut_report(v, left):
    M = matrix_for_cut(v, left); r = rank(M); p = purity(M)
    equal = abs(p * r - 1.0) < 1e-9          # equal Schmidt weights  <=>  purity = 1/rank
    return r, (log2(r) if equal else None)

def apply_single(v, k, U):
    """Apply the 2x2 matrix U to subsystem k."""
    out = [0.0] * 16
    for i, a in enumerate(v):
        if a == 0.0: continue
        b = list(bits(i))
        for new in (0, 1):
            bb = b[:]; bb[k] = new; out[idx(tuple(bb))] += U[new][b[k]] * a
    return out

def swap_axes_on_B(v):
    out = [0.0] * 16
    for i, a in enumerate(v):
        pA, tA, pB, tB = bits(i); out[idx((pA, tA, tB, pB))] += a
    return out

def product_of_two_pairs(v, left):
    """True if the state factors across the split `left | rest`, and each factor is itself entangled."""
    M = matrix_for_cut(v, left)
    if rank(M) != 1: return False
    right = [k for k in range(4) if k not in left]
    col = max(range(4), key=lambda c: sum(M[r][c] ** 2 for r in range(4)))
    f = [M[r][col] for r in range(4)]                                   # left factor as 2x2 over `left`
    row = max(range(4), key=lambda r: sum(M[r][c] ** 2 for c in range(4)))
    g = [M[row][c] for c in range(4)]                                   # right factor
    return rank([[f[0], f[1], 0, 0], [f[2], f[3], 0, 0], [0] * 4, [0] * 4]) == 2 and \
           rank([[g[0], g[1], 0, 0], [g[2], g[3], 0, 0], [0] * 4, [0] * 4]) == 2

def genuinely_multipartite(v):
    """Check all seven unique bipartitions, with redundant complementary checks.
    Return early on a rank-1 cut; the printed table displays only three bipartitions.
    A pure state is genuinely multipartite entangled if no bipartition gives rank 1.
    """
    seen = set()
    for r_ in range(1, 3):
        for left in product(range(4), repeat=r_):
            if len(set(left)) != r_ or tuple(sorted(left)) != left: continue
            right = tuple(k for k in range(4) if k not in left)
            M = [[0.0] * 16 for _ in range(16)]                          # general rectangular cut
            rows = {}; cols = {}
            for i, a in enumerate(v):
                b = bits(i)
                rr = tuple(b[k] for k in left); cc = tuple(b[k] for k in right)
                rows.setdefault(rr, len(rows)); cols.setdefault(cc, len(cols))
                M[rows[rr]][cols[cc]] += a
            small = [row[:len(cols)] for row in M[:len(rows)]]
            # pad to square for the rank routine
            n = max(len(small), len(small[0]))
            sq = [r + [0.0] * (n - len(r)) for r in small] + [[0.0] * n for _ in range(n - len(small))]
            if rank(sq) == 1: return False
    return True

def main():
    random.seed(11)
    print("Subsystems:", NAMES)
    # 1. Matching and cross pairings: same amount of entanglement between the photons
    for label, v in (("matching (SEE-type)", matching), ("cross (NEE-type)", cross)):
        r, e = cut_report(v, SPLITS["photon partition (A | B)"])
        assert r == 4 and abs(e - 2.0) < 1e-9, label
    print("1. matching and cross pairings: Schmidt rank 4 and 2 ebits between the photons, a 16-dimensional joint Hilbert space: OK")

    # which pair-splits is each a product of two entangled pairs?
    pm = {k: product_of_two_pairs(matching, s) for k, s in SPLITS.items()}
    pc = {k: product_of_two_pairs(cross, s) for k, s in SPLITS.items()}
    assert pm["matched pairs (pol-pol | OAM-OAM)"] and not pm["cross pairs (A-pol,B-OAM | A-OAM,B-pol)"]
    assert pc["cross pairs (A-pol,B-OAM | A-OAM,B-pol)"] and not pc["matched pairs (pol-pol | OAM-OAM)"]
    print("   matching state is a product of two entangled pairs under the matched split only; cross state under the cross split only: OK")

    # 2. Single-axis local unitary transformations keep the pairing; the axis SWAP on B changes it
    def rot(a): return [[cos(a), -sin(a)], [sin(a), cos(a)]]
    v = matching[:]
    for k in range(4): v = apply_single(v, k, rot(random.uniform(0, 3.1)))
    assert product_of_two_pairs(v, SPLITS["matched pairs (pol-pol | OAM-OAM)"])
    assert abs(cut_report(v, SPLITS["photon partition (A | B)"])[1] - 2.0) < 1e-9
    print("2a. random single-axis rotations on all four subsystems: still matched pairs, still 2 ebits: OK")
    sw = swap_axes_on_B(matching)
    assert all(abs(x - y) < 1e-9 for x, y in zip(sw, cross))
    assert product_of_two_pairs(sw, SPLITS["cross pairs (A-pol,B-OAM | A-OAM,B-pol)"])
    assert abs(cut_report(sw, SPLITS["photon partition (A | B)"])[1] - 2.0) < 1e-9
    print("2b. axis SWAP on photon B turns the matching state into the cross state, still 2 ebits: OK")

    # 3. Four levels per photon is not enough for high-dimensional entanglement
    v = [0.0] * 16
    for pt in ((0, 0), (1, 1)): v[idx((pt[0], pt[1], pt[0], pt[1]))] = 1.0
    v = normalize(v)
    r, e = cut_report(v, SPLITS["photon partition (A | B)"])
    assert r == 2 and abs(e - 1.0) < 1e-9
    print("3. a state of two four-level photons with Schmidt rank 2 (1 ebit): not high-dimensional: OK")

    # 4. GHZ-type state across all four subsystems
    ghz = [0.0] * 16; ghz[idx((0, 0, 0, 0))] = ghz[idx((1, 1, 1, 1))] = 1 / sqrt(2)
    assert genuinely_multipartite(ghz)
    for k, s in SPLITS.items():
        assert not product_of_two_pairs(ghz, s), k
    r, e = cut_report(ghz, SPLITS["photon partition (A | B)"])
    assert r == 2 and abs(e - 1.0) < 1e-9
    assert not genuinely_multipartite(matching) and not genuinely_multipartite(cross)
    print("4. GHZ-type state: genuinely multipartite, not a product of entangled pairs under any split, 1 ebit between the photons: OK")

    print("\nTable (rank across each split; ebits where weights are equal):")
    for label, v in (("matching", matching), ("cross", cross), ("GHZ-type", ghz)):
        row = [f"{k}: rank {cut_report(v, s)[0]}" for k, s in SPLITS.items()]
        print(f"  {label:9s}", " | ".join(row), "| genuinely multipartite:", genuinely_multipartite(v))
    print("entanglement_organization.py: ALL PASS")

if __name__ == "__main__":
    main()
