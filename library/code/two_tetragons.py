# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tyler O'Bryan, where applicable
"""Volume 6: two Tetragons on two photons. Joint states, entanglement counts and the five correlation patterns.
Plain Python only (no NumPy). Address k = 2*p + t:  p = polarization (0 = H, 1 = V), t = twist (0 = -1, 1 = +1)."""
from itertools import product
from math import log2

def joint(perm):
    """Equal-weight state (1/2) * sum over a of  |a>_A |perm[a]>_B,  as a 4x4 coefficient matrix psi[a][b]."""
    psi = [[0.0] * 4 for _ in range(4)]
    for a in range(4):
        psi[a][perm[a]] = 0.5
    return psi

def purity(psi):
    """Trace of rho_A squared, where rho_A = psi psi^T (real amplitudes). 1/4 means four equal Schmidt weights."""
    rho = [[sum(psi[i][k] * psi[j][k] for k in range(4)) for j in range(4)] for i in range(4)]
    return sum(rho[i][j] ** 2 for i in range(4) for j in range(4))

def rank(m, tol=1e-9):
    m = [row[:] for row in m]; r = 0
    for c in range(len(m[0])):
        piv = max(range(r, len(m)), key=lambda i: abs(m[i][c]), default=None)
        if piv is None or abs(m[piv][c]) < tol: continue
        m[r], m[piv] = m[piv], m[r]
        for i in range(len(m)):
            if i != r:
                f = m[i][c] / m[r][c]; m[i] = [x - f * y for x, y in zip(m[i], m[r])]
        r += 1
        if r == len(m): break
    return r

def op_rank_across_axes(perm):
    """Operator Schmidt rank of the permutation operator on (polarization x twist): 1 means it is a product of one operation per axis."""
    # entry of the operator: U[(p',t'),(p,t)] = 1 if perm[2p+t] == 2p'+t'. Regroup as R[(p',p),(t',t)].
    R = [[0.0] * 4 for _ in range(4)]
    for a in range(4):
        p, t = divmod(a, 2); p2, t2 = divmod(perm[a], 2)
        R[2 * p2 + p][2 * t2 + t] = 1.0
    return rank(R)

def pol_pair_vs_twist_pair_purity(psi):
    """Purity of the state across the cut  (polarization of A and B) | (twist of A and B). 1 means a product of a polarization pair and a twist pair."""
    # coefficient of |pA,tA>|pB,tB> is psi[2pA+tA][2pB+tB]; regroup as M[(pA,pB),(tA,tB)]
    M = [[0.0] * 4 for _ in range(4)]
    for a, b in product(range(4), repeat=2):
        pA, tA = divmod(a, 2); pB, tB = divmod(b, 2)
        M[2 * pA + pB][2 * tA + tB] = psi[a][b]
    rho = [[sum(M[i][k] * M[j][k] for k in range(4)) for j in range(4)] for i in range(4)]
    return sum(rho[i][j] ** 2 for i in range(4) for j in range(4))

PATTERNS = {"corresponding": [0, 1, 2, 3], "horizontal reflection": [1, 0, 3, 2],
            "vertical reflection": [2, 3, 0, 1], "diagonal reflection": [3, 2, 1, 0], "cyclic rotation": [1, 3, 0, 2]}

def main():
    # 1. Joint dimensions and the largest entanglement of a pure state with d equal Schmidt weights (log2 d)
    for d, joint_dim in ((2, 4), (4, 16), (8, 64), (16, 256), (32, 1024), (4096, 16777216)):
        assert d * d == joint_dim
    for r, ebits in ((2, 1.0), (3, 1.585), (4, 2.0), (8, 3.0), (16, 4.0), (4096, 12.0)):
        assert abs(log2(r) - ebits) < 5e-4, r
    print("joint dimensions d*d and entanglement log2(rank) for equal weights: OK")

    # 2. All five patterns are equally entangled between the photons: four equal Schmidt weights (purity 1/4), 2 ebits
    for name, perm in PATTERNS.items():
        assert abs(purity(joint(perm)) - 0.25) < 1e-12, name
    print("all five patterns have four equal Schmidt weights (2 ebits between the photons): OK")

    # 3. Which patterns come from per-axis operations on photon B, starting from 'corresponding'?
    #    The relabelling of B is perm; it is a product of one operation per axis exactly when its operator rank is 1.
    ranks = {n: op_rank_across_axes(p) for n, p in PATTERNS.items()}
    assert ranks == {"corresponding": 1, "horizontal reflection": 1, "vertical reflection": 1, "diagonal reflection": 1, "cyclic rotation": 4}
    # horizontal = twist flip, vertical = polarization flip, diagonal = both
    flip_twist = [a ^ 1 for a in range(4)]; flip_pol = [a ^ 2 for a in range(4)]
    assert PATTERNS["horizontal reflection"] == flip_twist and PATTERNS["vertical reflection"] == flip_pol
    assert PATTERNS["diagonal reflection"] == [a ^ 3 for a in range(4)]
    print("operator rank across axes:", ranks)

    # 4. Four patterns are a polarization Bell pair times a twist Bell pair (hyperentangled); the cyclic one is not
    pur = {n: pol_pair_vs_twist_pair_purity(joint(p)) for n, p in PATTERNS.items()}
    for n in ("corresponding", "horizontal reflection", "vertical reflection", "diagonal reflection"):
        assert abs(pur[n] - 1.0) < 1e-12, n
    assert abs(pur["cyclic rotation"] - 0.25) < 1e-12
    print("first four = polarization pair x twist pair; cyclic rotation is not:", {n: round(v, 3) for n, v in pur.items()})

    # 5. A local relabelling (a permutation on B alone) leaves the entanglement unchanged; a joint sign pattern can change it
    #    with identical probabilities: product state with one sign flipped on |11> becomes maximally entangled (two-level pair)
    prod = [[0.5, 0.5], [0.5, 0.5]]; flipped = [[0.5, 0.5], [0.5, -0.5]]
    def two_level_purity(m):
        rho = [[sum(m[i][k] * m[j][k] for k in range(2)) for j in range(2)] for i in range(2)]
        return sum(rho[i][j] ** 2 for i in range(2) for j in range(2))
    assert abs(two_level_purity(prod) - 1.0) < 1e-12 and abs(two_level_purity(flipped) - 0.5) < 1e-12
    print("a joint sign change keeps probabilities but changes entanglement: OK")
    # 6. The cyclic rotation is an exchange of the two axes (SWAP) followed by a flip of one axis, and it is coupled but not entangling
    import random
    random.seed(7)
    swap = [2 * (a % 2) + a // 2 for a in range(4)]                    # (p, t) -> (t, p)
    flip_second = [a ^ 1 for a in range(4)]                            # flip the new twist
    assert [flip_second[swap[a]] for a in range(4)] == PATTERNS["cyclic rotation"]
    assert op_rank_across_axes(swap) == 4                              # SWAP has maximal operator Schmidt rank (it does not factor) ...
    def axis_purity(v):                                                # purity of polarization vs twist for one photon's 4 amplitudes
        n = sum(x * x for x in v); m = [[v[0], v[1]], [v[2], v[3]]]
        rho = [[sum(m[i][k] * m[j][k] for k in range(2)) / n for j in range(2)] for i in range(2)]
        return sum(rho[i][j] ** 2 for i in range(2) for j in range(2))
    for _ in range(200):
        a = [random.uniform(-1, 1) for _ in range(2)]; b = [random.uniform(-1, 1) for _ in range(2)]
        v = [a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1]]       # a product input: polarization state times twist state
        for perm in (swap, PATTERNS["cyclic rotation"]):
            w = [0.0] * 4
            for k in range(4): w[perm[k]] = v[k]
            assert abs(axis_purity(w) - 1.0) < 1e-9                    # spot check of the exact fact: SWAP sends a-times-b to b-times-a, and the flip acts on one axis only
    cz = [1, 1, 1, -1]                                                 # controlled phase: sign flip on address 11
    plus = [0.5, 0.5, 0.5, 0.5]
    assert abs(axis_purity([p * s for p, s in zip(plus, cz)]) - 0.5) < 1e-12   # ... whereas a controlled phase does entangle
    # 7. Gate-count floor from operator rank: gates of rank at most r need at least ceil(log_r R) copies for a rank-R target (not tight)
    cnot_ct = [0, 1, 3, 2]; cnot_tc = [0, 3, 2, 1]                     # control first axis / control second axis
    assert op_rank_across_axes(cnot_ct) == 2 and op_rank_across_axes(swap) == 4
    three = [cnot_ct[cnot_tc[cnot_ct[a]]] for a in range(4)]           # apply cnot_ct, then cnot_tc, then cnot_ct
    assert three == swap                                               # SWAP = three CNOTs, although the rank floor is only 2
    print("SWAP has rank 4, CNOT rank 2: the floor is 2 CNOTs, the standard exact circuit uses 3 (the floor is not tight): OK")
    print("cyclic rotation = SWAP of the axes then one flip; operator rank 4 (maximal non-factorizability, not interaction strength) and non-entangling (exact; 200 random real inputs as a spot check); a controlled phase does entangle: OK")
    print("two_tetragons.py: ALL PASS")

if __name__ == "__main__":
    main()
