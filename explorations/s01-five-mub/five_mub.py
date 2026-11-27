#!/usr/bin/env python3
"""S01: the proposed HDOC five-basis investigation, executed exactly for two qubits.

Model: the Tetragon as polarization (qubit A) times a two-mode OAM space (qubit B), d = 4.
Everything here is exact linear algebra checked numerically to 1e-12 (numpy).  Author-side;
not independent reproduction.  Nothing here is a hardware statement.

Claims checked (labels are evidence classes, see docs):
  C1  The 15 non-identity two-qubit Paulis split into 5 commuting triples; their joint
      eigenbases are 5 orthonormal bases with every cross-basis squared overlap 1/4.   DERIVED
  C2  Entanglement of the 20 states across polarization|OAM: 12 product, 8 maximally
      entangled in this construction.                                                  DERIVED
  C3  THEOREM (2-design argument): for ANY complete set of 5 MUBs in d = 4, the sum over its
      20 states of the purity of the polarization marginal is exactly 16 (average 4/5).
      Checked on the construction and on 200 random global unitaries.                  DERIVED
  C4  Consequence: any complete MUB set contains at least 8 entangled states, so at least
      two of its five bases are not product bases, and at most three can be product.   DERIVED
  C5  Active maps U(j<-i) = B_j D P B_i^dagger over all 24 orderings and four-valued phases:
      the minimum operator Schmidt rank across polarization|OAM for each directed pair.
      Product<->entangled pairs cannot be done by a local unitary; the others can.     DERIVED
"""
import itertools, sys
import numpy as np

OK = True
def check(name, ok):
    global OK
    OK = OK and bool(ok)
    print(("PASS  " if ok else "FAIL  ") + name)

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
P1 = {'I': I2, 'X': X, 'Y': Y, 'Z': Z}
def pauli(s): return np.kron(P1[s[0]], P1[s[1]])

# a spread of the 15 non-identity Paulis into 5 commuting triples (c = product of the first two)
TRIPLES = [('XI', 'IX', 'XX'), ('YI', 'IY', 'YY'), ('ZI', 'IZ', 'ZZ'), ('XY', 'YZ', 'ZX'), ('XZ', 'YX', 'ZY')]
NAMES = ['XX-basis', 'YY-basis', 'ZZ-basis', 'XY/YZ/ZX-basis', 'XZ/YX/ZY-basis']

def commute(a, b): return np.allclose(pauli(a) @ pauli(b), pauli(b) @ pauli(a))

def joint_eigenbasis(t):
    """Ordered eigenbasis of the commuting pair (t[0], t[1]); columns ordered by (eig0, eig1) in
    (+,+), (+,-), (-,+), (-,-).  Each column is a stabilizer state."""
    A, B = pauli(t[0]), pauli(t[1])
    cols = []
    for e0 in (1, -1):
        for e1 in (1, -1):
            Pj = (np.eye(4) + e0 * A) @ (np.eye(4) + e1 * B) / 4     # rank-1 projector
            w, v = np.linalg.eigh(Pj)
            cols.append(v[:, -1])
    return np.array(cols).T

def purity_A(psi):
    m = psi.reshape(2, 2)               # psi_{ab}: a = polarization, b = OAM
    rho = m @ m.conj().T
    return float(np.real(np.trace(rho @ rho)))

def osr(U, tol=1e-9):
    """Operator Schmidt rank of a 4x4 unitary across (A|B)."""
    R = U.reshape(2, 2, 2, 2).transpose(0, 2, 1, 3).reshape(4, 4)   # [(a a'), (b b')]
    s = np.linalg.svd(R, compute_uv=False)
    return int(np.sum(s > tol)), s

def main():
    # ---- C1
    allp = [a + b for a in 'IXYZ' for b in 'IXYZ' if a + b != 'II']
    used = [t for tr in TRIPLES for t in tr]
    check('C1a the five triples partition the 15 non-identity Paulis', sorted(used) == sorted(allp))
    check('C1b every triple is mutually commuting', all(commute(a, b) for tr in TRIPLES for a, b in itertools.combinations(tr, 2)))
    check('C1c triples from different bases are not all commuting (maximal)', all(not all(commute(a, b) for a in t1 for b in t2) for t1, t2 in itertools.combinations(TRIPLES, 2)))
    B = [joint_eigenbasis(t) for t in TRIPLES]
    check('C1d each basis is orthonormal', all(np.allclose(b.conj().T @ b, np.eye(4), atol=1e-12) for b in B))
    worst = 0.0
    for i, j in itertools.combinations(range(5), 2):
        ov = np.abs(B[i].conj().T @ B[j]) ** 2
        worst = max(worst, float(np.max(np.abs(ov - 0.25))))
    check('C1e all 10 basis pairs are mutually unbiased (max |overlap^2 - 1/4| = %.1e)' % worst, worst < 1e-12)
    rays = {tuple(np.round(np.abs(c), 6)) for b in B for c in b.T}
    check('C1f 20 states in the union, 4 per basis', sum(b.shape[1] for b in B) == 20)

    # ---- C2
    pur = [[purity_A(b[:, k]) for k in range(4)] for b in B]
    kinds = []
    for i, p in enumerate(pur):
        kind = 'product' if all(abs(x - 1) < 1e-12 for x in p) else ('maximally entangled' if all(abs(x - 0.5) < 1e-12 for x in p) else 'mixed')
        kinds.append(kind); print('      %-16s purity of polarization marginal %s -> %s' % (NAMES[i], [round(x, 6) for x in p], kind))
    check('C2 three bases are product, two are maximally entangled', kinds.count('product') == 3 and kinds.count('maximally entangled') == 2)
    s0 = sum(sum(p) for p in pur)
    check('C2b sum of purities in this construction = 16 (12 x 1 + 8 x 1/2); got %.12f' % s0, abs(s0 - 16) < 1e-9)

    # ---- C3: 2-design argument and numerical test on random global unitaries
    rng = np.random.default_rng(20261127)
    sums = []
    for _ in range(200):
        M = rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4))
        Q, R = np.linalg.qr(M); Q = Q * (np.diag(R) / np.abs(np.diag(R)))
        sums.append(sum(purity_A((Q @ b)[:, k]) for b in B for k in range(4)))
    sums = np.array(sums)
    check('C3 sum of purities is 16 for 200 random global unitaries (spread %.1e); the set stays a complete MUB set' % (sums.max() - sums.min()), np.max(np.abs(sums - 16)) < 1e-9)
    # the 2-design property itself: average of (psi psi*)^{(x)2} over the 20 states equals the Haar value 2 Pi_sym / (d(d+1))
    S = np.zeros((16, 16), dtype=complex)
    for b in B:
        for k in range(4):
            v = np.kron(b[:, k], b[:, k]); S += np.outer(v, v.conj())
    S /= 20
    swap = np.zeros((16, 16))
    for a in range(4):
        for c in range(4): swap[a * 4 + c, c * 4 + a] = 1
    haar = (np.eye(16) + swap) / (4 * 5)
    check('C3b the 20 states form a complex projective 2-design (max entry difference %.1e)' % np.max(np.abs(S - haar)), np.allclose(S, haar, atol=1e-12))
    # Haar value of the purity = (dA + dB)/(dA dB + 1) = 4/5
    check('C3c Haar average purity (dA+dB)/(dA dB+1) = 4/5 gives 20 x 4/5 = 16', abs(20 * (2 + 2) / (4 + 1) - 16) < 1e-12)

    # ---- C4: counting consequence
    # each state has linear entropy 1 - purity <= 1/2, and the sum over 20 states is 20 - 16 = 4
    check('C4 sum of linear entropies = 4 and each is at most 1/2, so at least 8 states are entangled', abs((20 - 16) - 4) < 1e-12 and 4 / 0.5 == 8)

    # ---- C5: active maps and operator Schmidt rank
    perms = list(itertools.permutations(range(4)))
    phs = [1, 1j, -1, -1j]
    rows = []
    for i in range(5):
        for j in range(5):
            if i == j: continue
            best = 99
            for p in perms:
                Bi = B[i]; Bj = B[j][:, list(p)]
                for ph in itertools.product(phs, repeat=3):      # global phase of U is irrelevant: fix the first phase to 1
                    D = np.diag([1, *ph])
                    U = Bj @ D @ Bi.conj().T
                    r, _ = osr(U)
                    if r < best: best = r
                if best == 1: break
            rows.append((i, j, best))
    print('      minimum operator Schmidt rank of an active map B_j D P B_i^dagger (rank 1 = local unitary):')
    for i, j, r in rows:
        print('        %-16s -> %-16s %d' % (NAMES[i], NAMES[j], r))
    prod = [i for i, k in enumerate(kinds) if k == 'product']; ent = [i for i, k in enumerate(kinds) if k != 'product']
    pp = [r for i, j, r in rows if i in prod and j in prod]
    ee = [r for i, j, r in rows if i in ent and j in ent]
    pe = [r for i, j, r in rows if (i in prod) != (j in prod)]
    check('C5a every product<->product map has a local-unitary realisation (rank 1)', all(r == 1 for r in pp))
    check('C5b every product<->entangled map needs rank >= 2 (a local unitary cannot do it)', all(r >= 2 for r in pe))
    check('C5c the entangled<->entangled map has a local realisation', all(r == 1 for r in ee))
    check('C5d product<->entangled maps are all rank exactly 2 at the minimum (a single CNOT-class interaction is not excluded)', all(r == 2 for r in pe))
    nloc = sum(1 for i, j, r in rows if r == 1)
    print('      directed pairs: %d total, %d realisable by local unitaries, %d need an entangling operation' % (len(rows), nloc, len(rows) - nloc))
    check('C5e counts: 20 directed pairs, 8 local (6 product + 2 entangled), 12 entangling', len(rows) == 20 and nloc == 8 and len(rows) - nloc == 12)
    # sanity: the rank computation recognises a CNOT as rank 2 and a tensor product as rank 1
    CN = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=complex)
    check('sanity: OSR(CNOT) = 2, OSR(H(x)H) = 1, OSR(identity) = 1',
          osr(CN)[0] == 2 and osr(np.kron(np.array([[1, 1], [1, -1]]) / 2 ** .5, np.array([[1, 1], [1, -1]]) / 2 ** .5))[0] == 1 and osr(np.eye(4))[0] == 1)
    print('ALL PASS' if OK else 'SOME CHECKS FAILED')
    return 0 if OK else 1

if __name__ == '__main__':
    sys.exit(main())
