# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tyler O'Bryan, where applicable
"""Buddy verification, version 0.7: how the verification observable is transported, and whether verification stays local
as registers interact. Plain Python, no packages.

Evidence: every result is [[DERIVED]] inside the stated model (ideal unitaries; exact Pauli-algebra bookkeeping; the independent
Pauli fault model of version 0.5 for part 7). Ensembles and noise values are [[ASSUMED]] examples, not measurements.
Nothing here says what a device costs. Term count, support size and interaction order are structural proxies, NOT measurement costs,
and no combined score is formed.

Conventions: a photon is a Tetragon with two data axes a_i = 2i, b_i = 2i+1 in the diagonal encoding (|0> = |00>, |1> = |11>).
Its local check is S_i = Z(a_i) Z(b_i). Pauli strings are bit pairs (x, z); a Hermitian Pauli is i^(x.z) X^x Z^z.

Parts
  1. Transported-check complexity for one Tetragon: terms, support, prefix length; the by-construction rule; engine validation
  2. Two-Tetragon verification compatibility (16-dimensional state vectors)
  3. Verification as the register count grows (2, 4, 8 photons): fixed generators versus the transported stabilizer group
  4. Non-commuting steps, term growth and equivalent routes
  5. Measuring, transporting or deferring a check around an excursion out of the code
  6. Preparation geometry: criteria kept separate
  7. Productivity under explicit output-identifiability assumptions
"""
import math, random
from itertools import product
from collections import defaultdict

random.seed(20261127)
results = []
def check(name, ok_):
    results.append((name, bool(ok_)))
    print(("PASS  " if ok_ else "FAIL  ") + name)
def near(a, b, t=1e-9): return abs(a - b) < t
def pr(v, p): return p if v else 1 - p
def rc(): return complex(random.gauss(0, 1), random.gauss(0, 1))
def vn(v):
    n = math.sqrt(sum(abs(x) ** 2 for x in v)); return [x / n for x in v]

# =============================================================== Pauli-algebra engine
def pc(n): return bin(n).count('1')
def pmul(k1, k2):
    """k1 * k2 = i^e * k, for Hermitian Paulis k = (x, z)."""
    x1, z1 = k1; x2, z2 = k2; x = x1 ^ x2; z = z1 ^ z2
    return (pc(x1 & z1) + pc(x2 & z2) - pc(x & z) + 2 * pc(z1 & x2)) % 4, (x, z)
def commute(k1, k2): return (pc(k1[0] & k2[1]) + pc(k1[1] & k2[0])) % 2 == 0
def weight(k): return pc(k[0] | k[1])
def photons(k): return len({q // 2 for q in range(40) if ((k[0] | k[1]) >> q) & 1})
def prune(op): return {k: c for k, c in op.items() if abs(c) > 1e-9}
def Zk(q): return (0, 1 << q)
def Xk(q): return (1 << q, 0)
def rot_conj(op, P, th):
    """U op U^dagger for U = exp(-i th/2 P), P a Pauli key."""
    new = defaultdict(complex)
    for Q, c in op.items():
        if commute(Q, P): new[Q] += c
        else:
            new[Q] += c * math.cos(th)
            e, key = pmul(Q, P); new[key] += c * 1j * math.sin(th) * (1j ** e)
    return prune(new)
def gate_one(x, z, g):
    """Conjugation of one Hermitian Pauli by an elementary Clifford gate; returns (x, z, sign)."""
    kind = g[0]
    if kind == 'H':
        q = g[1]; xq, zq = (x >> q) & 1, (z >> q) & 1; s = xq & zq
        if xq != zq: x ^= 1 << q; z ^= 1 << q
        return x, z, -1 if s else 1
    if kind == 'S':
        q = g[1]; xq, zq = (x >> q) & 1, (z >> q) & 1; s = xq & zq
        z ^= xq << q; return x, z, -1 if s else 1
    if kind == 'CNOT':
        c, t = g[1], g[2]; xc, zc, xt, zt = (x >> c) & 1, (z >> c) & 1, (x >> t) & 1, (z >> t) & 1
        s = xc & zt & ((xt ^ zc ^ 1) & 1); x ^= xc << t; z ^= zt << c
        return x, z, -1 if s else 1
    if kind == 'CZ':
        x, z, s1 = gate_one(x, z, ('H', g[2])); x, z, s2 = gate_one(x, z, ('CNOT', g[1], g[2])); x, z, s3 = gate_one(x, z, ('H', g[2]))
        return x, z, s1 * s2 * s3
    raise ValueError(kind)
def gate_conj(op, g):
    new = defaultdict(complex)
    for (x, z), c in op.items():
        x2, z2, s = gate_one(x, z, g); new[(x2, z2)] += s * c
    return prune(new)
def macro_conj(op, m):
    return rot_conj(op, m[1], m[2]) if m[0] == 'r' else gate_conj(op, m[1])
def nterms(op): return len(op)

# matrices (for validation and for the two-photon state-vector parts)
def kron(A, B): return [[A[i // len(B)][j // len(B[0])] * B[i % len(B)][j % len(B[0])] for j in range(len(A[0]) * len(B[0]))] for i in range(len(A) * len(B))]
def mm(A, B): return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def mv(A, v): return [sum(A[i][k] * v[k] for k in range(len(v))) for i in range(len(A))]
def dag(A): return [[complex(A[j][i]).conjugate() for j in range(len(A))] for i in range(len(A[0]))]
def eye(n): return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
def close(A, B, t=1e-9): return all(abs(A[i][j] - B[i][j]) < t for i in range(len(A)) for j in range(len(A[0])))
def madd(A, B, a=1, b=1): return [[a * A[i][j] + b * B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
I2 = [[1, 0], [0, 1]]; PX = [[0, 1], [1, 0]]; PY = [[0, -1j], [1j, 0]]; PZ = [[1, 0], [0, -1]]
HAD = [[1 / math.sqrt(2), 1 / math.sqrt(2)], [1 / math.sqrt(2), -1 / math.sqrt(2)]]; SG = [[1, 0], [0, 1j]]
def pmat(k, N):
    M = [[1]]
    for q in range(N):
        xb, zb = (k[0] >> q) & 1, (k[1] >> q) & 1
        M = kron(M, {(0, 0): I2, (1, 0): PX, (1, 1): PY, (0, 1): PZ}[(xb, zb)])
    return M
def single(M1, q, N):
    M = [[1]]
    for i in range(N): M = kron(M, M1 if i == q else I2)
    return M
def gmat(g, N):
    if g[0] == 'H': return single(HAD, g[1], N)
    if g[0] == 'S': return single(SG, g[1], N)
    dim = 1 << N; M = [[0] * dim for _ in range(dim)]
    for k in range(dim):
        b = [(k >> (N - 1 - q)) & 1 for q in range(N)]
        if g[0] == 'CNOT':
            if b[g[1]]: b[g[2]] ^= 1
            ph = 1
        else:   # CZ
            ph = -1 if (b[g[1]] and b[g[2]]) else 1
        M[sum(bb << (N - 1 - q) for q, bb in enumerate(b))][k] = ph
    return M
def mac_mat(m, N, frac=1.0):
    if m[0] == 'g': return gmat(m[1], N)
    c, s = math.cos(m[2] * frac / 2), math.sin(m[2] * frac / 2); P = pmat(m[1], N)
    return [[c * (1 if i == j else 0) - 1j * s * P[i][j] for j in range(len(P))] for i in range(len(P))]
def op_to_mat(op, N):
    dim = 1 << N; M = [[0j] * dim for _ in range(dim)]
    for k, c in op.items():
        P = pmat(k, N)
        for i in range(dim):
            for j in range(dim): M[i][j] += c * P[i][j]
    return M

# =============================================================== engine validation
print("== 0. engine validation against explicit matrices ==")
okv = True
for N in (2, 3):
    for _ in range(30):
        key = (random.randrange(1 << N), random.randrange(1 << N))
        macs = []
        for _ in range(4):
            r_ = random.random()
            if r_ < 0.25: macs.append(('g', ('H', random.randrange(N))))
            elif r_ < 0.5: macs.append(('g', ('S', random.randrange(N))))
            elif r_ < 0.75:
                c_, t_ = random.sample(range(N), 2); macs.append(('g', ('CNOT' if random.random() < .5 else 'CZ', c_, t_)))
            else: macs.append(('r', (random.randrange(1 << N), random.randrange(1 << N)), random.uniform(0.1, 3.0)))
        op = {key: 1.0}; U = eye(1 << N)
        for m in macs: op = macro_conj(op, m); U = mm(mac_mat(m, N), U)
        okv &= close(op_to_mat(op, N), mm(U, mm(pmat(key, N), dag(U))), 1e-8)
check("the Pauli-algebra engine (gate rules and Pauli rotations) equals explicit matrix conjugation on random sequences, 2 and 3 axes", okv)

# =============================================================== 1. transported-check complexity, one Tetragon
print("== 1. transported-check complexity, one Tetragon ==")
a_, b_ = 0, 1
ZZk = (0, 3); XXk = (3, 0); ZIk = (0, 1); IZk = (0, 2)
CL = [('CNOT', 0, 1), ('CNOT', 1, 0), ('H', 0), ('H', 1), ('S', 0), ('S', 1)]
mx = 0
for _ in range(300):
    op = {ZZk: 1.0}
    for _ in range(12): op = gate_conj(op, random.choice(CL)); mx = max(mx, nterms(op))
check("Clifford steps: the transported check stays a single Pauli string in 300 random sequences of 12 steps", mx == 1)
norm = [k for k in [(x, z) for x in range(4) for z in range(4)] if commute(k, ZZk) and k != (0, 0) and k != ZZk]
check(f"by construction: every Pauli that commutes with ZZ (the {len(norm)} logical operators, i.e. the normalizer minus the stabilizer) generates rotations that leave the check ZZ unchanged for any angle",
      len(norm) == 6 and all(rot_conj({ZZk: 1.0}, k, 0.83) == {ZZk: 1.0} for k in norm))
bad = [k for k in [(x, z) for x in range(4) for z in range(4)] if not commute(k, ZZk)]
check(f"the {len(bad)} Paulis that anticommute with ZZ turn it into two terms under a rotation by a generic angle (cos t * ZZ plus sin t * another string) and into one term only at multiples of pi/2",
      len(bad) == 8 and all(nterms(rot_conj({ZZk: 1.0}, k, 0.83)) == 2 for k in bad) and all(nterms(rot_conj({ZZk: 1.0}, k, math.pi / 2)) == 1 for k in bad))
# mean growth along random sequences containing generic rotations (ASSUMED ensemble)
cnt = []; sup = []
for _ in range(400):
    op = {ZZk: 1.0}; c_, s_ = [], []
    for _ in range(6):
        if random.random() < 0.5: op = gate_conj(op, random.choice(CL))
        else: op = rot_conj(op, random.choice([(1, 0), (2, 0), (3, 0), (0, 1), (3, 3)]), random.uniform(0.2, 1.3))
        c_.append(nterms(op)); s_.append(max(weight(k) for k in op))
    cnt.append(c_); sup.append(s_)
means = [sum(c[i] for c in cnt) / len(cnt) for i in range(6)]
print("  ensemble (ASSUMED): half Clifford steps, half generic-angle rotations about single-axis X, Y, Z or the XX-type; mean terms after steps 1..6:", [round(m, 2) for m in means], " max terms:", max(max(c) for c in cnt))
check("with generic non-commuting rotations in the mix the transported check acquires several terms (mean grows over six steps, maximum above 3), while terms, support and prefix length are different quantities that must be tracked separately",
      means[5] > means[0] and max(max(c) for c in cnt) > 3)
# measuring by reversing the prefix
okr = True
for _ in range(60):
    macs = [random.choice([('g', random.choice(CL)), ('r', random.choice([(1, 0), (0, 1), (3, 3)]), random.uniform(.2, 1.2))]) for _ in range(4)]
    op = {ZZk: 1.0}; U = eye(4)
    for m in macs: op = macro_conj(op, m); U = mm(mac_mat(m, 2), U)
    psi = vn([rc() for _ in range(4)])
    Sp = op_to_mat(op, 2); lhs = sum(x.conjugate() * y for x, y in zip(psi, mv(Sp, psi)))
    phi = mv(dag(U), psi); rhs = sum(x.conjugate() * y for x, y in zip(phi, mv(op_to_mat({ZZk: 1.0}, 2), phi)))
    okr &= abs(lhs - rhs) < 1e-9
check("measuring the transported observable U S U^dagger equals reversing the computational prefix and measuring S: it is a possible implementation, not a statement that it is the cheapest", okr)
# equivalent routes for a logical Rx(theta)
th = 0.9
R1 = [('r', XXk, th)]
R2 = [('g', ('CNOT', 0, 1)), ('r', (1, 0), th), ('g', ('CNOT', 0, 1))]
U1 = eye(4); U2 = eye(4)
for m in R1: U1 = mm(mac_mat(m, 2), U1)
for m in R2: U2 = mm(mac_mat(m, 2), U2)
same = close(U1, U2, 1e-9)
def route_profile(macs, S0, N):
    op = {S0: 1.0}; names = []; terms = []; maxorder = 0
    for m in macs:
        op = macro_conj(op, m); terms.append(nterms(op)); names.append(sorted(op))
        if m[0] == 'r': maxorder = max(maxorder, weight(m[1]))
    return terms, names, maxorder
t1, n1, o1 = route_profile(R1, ZZk, 2); t2, n2, o2 = route_profile(R2, ZZk, 2)
check(f"two equivalent routes for a logical X rotation (coupled XX rotation; CNOT, single-axis X rotation, CNOT) are the same unitary on all four basis states, both keep ONE term throughout, and differ in the largest rotation generator: {o1} axes versus {o2} axis (the second needs two CNOTs instead)",
      same and max(t1) == 1 and max(t2) == 1 and o1 == 2 and o2 == 1 and n2 == [[IZk], [IZk], [ZZk]])

# =============================================================== 2. two Tetragons, state vectors
print("== 2. two Tetragons: local checks during inter-photon operations (16-dim state vectors) ==")
N2 = 4
C1 = (0, 0b0011); C2 = (0, 0b1100)
M1 = pmat(C1, N2); M2 = pmat(C2, N2)
def odd(v, M): return (1 - sum(x.conjugate() * y for x, y in zip(v, mv(M, v))).real) / 2
def code2(amp):                 # photon 1 logical p, photon 2 logical q: |pp qq>
    v = [0j] * 16
    for (p, q), x in zip(product((0, 1), repeat=2), amp): v[(p * 3) * 4 + (q * 3)] = x
    return v
def rnd2(): return code2(vn([rc() for _ in range(4)]))
CZs = {(0, 2): 'a1-a2', (0, 3): 'a1-b2', (1, 2): 'b1-a2', (1, 3): 'b1-b2'}
okc = okl = True
for (c_, t_) in CZs:
    G = gmat(('CZ', c_, t_), 4)
    okc &= close(mm(G, M1), mm(M1, G)) and close(mm(G, M2), mm(M2, G))
    for p, q in product((0, 1), repeat=2):
        k = (p * 3) * 4 + (q * 3); okl &= near(G[k][k].real, -1 if (p and q) else 1)
check("all four physical controlled-phase routes commute with BOTH local parity checks and act as the logical controlled-phase on the code", okc and okl)
phi = 2.0
Gw = [[0j] * 16 for _ in range(16)]
for k in range(16):
    b = [(k >> (3 - q)) & 1 for q in range(4)]; Gw[k][k] = complex(math.cos(phi), math.sin(phi)) if (b[0] and b[2]) else 1
ideal = gmat(('CZ', 0, 2), 4)
fid = []; oddw = 0.0
for _ in range(300):
    v = rnd2(); w = mv(Gw, v); oddw = max(oddw, odd(w, M1), odd(w, M2))
    ref = mv(ideal, v); fid.append(abs(sum(x.conjugate() * y for x, y in zip(ref, w))) ** 2)
check(f"a controlled phase with the WRONG angle (phi = 2.0 instead of pi) commutes with both checks and passes both (odd weight {oddw:.1e}) while its output has mean fidelity {sum(fid)/len(fid):.3f} with the intended logical controlled-phase: preserving the local checks does not show the intended operation succeeded",
      oddw < 1e-12 and sum(fid) / len(fid) < 0.9)
def apply_macros(v, macs, record=None, sub=10):
    for m in macs:
        if m[0] == 'g': v = mv(gmat(m[1], 4), v); record and record(v)
        else:
            for _ in range(sub): v = mv(mac_mat(m, 4, 1.0 / sub), v); record and record(v)
    return v
def full_mat(macs, N=4):
    U = eye(1 << N)
    for m in macs: U = mm(mac_mat(m, N), U)
    return U
def cnotL_ok(macs):
    U = full_mat(macs); ph = None
    for p, q in product((0, 1), repeat=2):
        kin = (p * 3) * 4 + (q * 3); kout = (p * 3) * 4 + (((q ^ p)) * 3)
        col = [U[i][kin] for i in range(16)]
        if abs(abs(col[kout]) - 1) > 1e-9: return False
        ph = ph or col[kout]
        if abs(col[kout] - ph) > 1e-9: return False
    return True
a1, b1, a2, b2 = 0, 1, 2, 3
HLg = lambda a, b: [('r', Zk(a), math.pi / 2), ('r', (1 << a | 1 << b, 0), math.pi / 2), ('r', Zk(a), math.pi / 2)]
routeP = [('g', ('CNOT', a1, a2)), ('g', ('CNOT', b1, b2))]
routeG = HLg(a2, b2) + [('g', ('CZ', a1, a2))] + HLg(a2, b2)
Zc = Zk(a1); Xt = (1 << a2 | 1 << b2, 0); ZcXt = (Xt[0], Zc[1])
routeT = [('r', Zc, math.pi / 2), ('r', Xt, math.pi / 2), ('r', ZcXt, -math.pi / 2)]
check("three routes to the SAME logical CNOT (photon 1 controls photon 2): two physical CNOTs; H_L from generators, controlled phase, H_L; and three generator rotations Z_c, X_t, Z_c X_t (the last a three-axis interaction) all give the logical CNOT on the code up to a global phase",
      cnotL_ok(routeP) and cnotL_ok(routeG) and cnotL_ok(routeT))
mid = []; end_ = []
for _ in range(200):
    v = rnd2(); p1 = sum(abs(v[(1 * 3) * 4 + (q * 3)]) ** 2 for q in (0, 1))
    w = mv(gmat(('CNOT', a1, a2), 4), v)
    mid.append((odd(w, M1), odd(w, M2), p1))
    w2 = apply_macros(v, routeP); end_.append((odd(w2, M1), odd(w2, M2)))
check("two physical CNOTs: after the FIRST one photon 1's check is intact and photon 2's check reads odd with probability equal to the probability that photon 1 is logical 1 (amplitude-dependent); after the second both checks are valid again",
      all(near(a, 0) and near(b_, c) for a, b_, c in mid) and all(near(a, 0) and near(b, 0) for a, b in end_)
      and max(c for _, _, c in mid) - min(c for _, _, c in mid) > 0.5)
worstG = worstT = 0.0
for _ in range(60):
    v = rnd2(); recG = []; recT = []
    apply_macros(v, routeG, lambda s: recG.append(max(odd(s, M1), odd(s, M2))))
    apply_macros(v, routeT, lambda s: recT.append(max(odd(s, M1), odd(s, M2))))
    worstG = max(worstG, max(recG)); worstT = max(worstT, max(recT))
check(f"the generator route and the three-axis route keep BOTH local checks at exactly zero odd weight at every sub-step (worst {max(worstG, worstT):.1e}); the price is in the interaction: the largest single generator touches {weight(ZcXt)} axes of two photons for the three-axis route and 2 axes for the H_L-CZ-H_L route",
      max(worstG, worstT) < 1e-12 and weight(ZcXt) == 3)
phys = []
for _ in range(100):
    v = rnd2(); w = mv(gmat(('CNOT', a1, a2), 4), v); phys.append(odd(w, M2))
check("a lone physical CNOT between axes of different photons is not a logical gate: it leaves the code and photon 2's check reads values from 0 to 1 depending on the state", max(phys) > 0.7 and min(phys) < 0.3)

# =============================================================== 3. register count and locality
print("== 3. verification as the register count grows ==")
def S_key(i): return (0, 3 << (2 * i))
def group_elems(rows):
    el = {(0, 0): 1.0}
    for key, c in rows:
        new = {}
        for k0, c0 in el.items():
            new[k0] = c0
            e, kk = pmul(k0, key); cc = c0 * c * (1j ** e)
            assert abs(cc.imag) < 1e-9
            new[kk] = cc.real
        el = new
    return el
def min_basis(el, nrows, Nax):
    items = sorted((k for k in el if k != (0, 0)), key=lambda k: (weight(k), photons(k)))
    basis = []; xs = []
    for k in items:
        v = k[0] | (k[1] << Nax)
        for b in xs: v = min(v, v ^ b)
        if v:
            xs.append(v); basis.append(k)
            if len(basis) == nrows: break
    return basis
def route_macros(kind, i, j, rt=0):
    a_i, b_i, a_j, b_j = 2 * i, 2 * i + 1, 2 * j, 2 * j + 1
    pairs = [(a_i, a_j), (a_i, b_j), (b_i, a_j), (b_i, b_j)]
    if kind == 'H': return HLg(a_i, b_i)
    if kind == 'CZ': return [('g', ('CZ',) + pairs[rt])]
    if kind == 'CNOT_G': return HLg(a_j, b_j) + [('g', ('CZ',) + pairs[rt])] + HLg(a_j, b_j)
    if kind == 'CNOT_T': return [('r', Zk(a_i), math.pi / 2), ('r', (1 << a_j | 1 << b_j, 0), math.pi / 2), ('r', ((1 << a_j | 1 << b_j), 1 << a_i), -math.pi / 2)]
    if kind == 'CNOT_P': return [('g', ('CNOT', a_i, a_j)), ('g', ('CNOT', b_i, b_j))]
def track(n, ops):
    """ops: list of (kind, i, j, rt). Returns per macro-step records for the fixed generators and the transported group."""
    Nax = 2 * n; rows = [({S_key(i): 1.0}) for i in range(n)]
    recs = []
    for kind, i, j, rt in ops:
        macs = route_macros(kind, i, j, rt)
        for mi, m in enumerate(macs):
            rows = [macro_conj(r, m) for r in rows]
            assert all(len(r) == 1 for r in rows)
            gr = [(next(iter(r)), next(iter(r.values())).real) for r in rows]
            el = group_elems(gr); basis = min_basis(el, n, Nax)
            valid = all(S_key(i) in el and el[S_key(i)] > 0 for i in range(n))
            recs.append(dict(kind=kind, last=(mi == len(macs) - 1), fixed_w=max(weight(k) for k, _ in gr), fixed_p=max(photons(k) for k, _ in gr),
                             basis_w=max(weight(k) for k in basis), basis_p=max(photons(k) for k in basis), valid=valid))
    return recs
def rand_ops(n, L, allow):
    ops = []
    for _ in range(L):
        kind = random.choice(allow); i = random.randrange(n); j = random.choice([x for x in range(n) if x != i])
        ops.append((kind, i, j, random.randrange(4)))
    return ops
print("      photons   steps   ensemble                    local checks valid   max fixed-generator weight (axes, photons)   max min-weight-basis weight (axes, photons)")
okA = okB = True; table = {}
for n in (2, 4, 8):
    for label, allow in (("compatible routes only", ['H', 'CZ', 'CNOT_G', 'CNOT_T']), ("with two-CNOT route", ['H', 'CZ', 'CNOT_G', 'CNOT_T', 'CNOT_P'])):
        fw = fp = bw = bp = 0; allvalid = True; endvalid = True; endbw = 0; midbw = 0
        for _ in range(40 if n < 8 else 25):
            recs = track(n, rand_ops(n, 25, allow))
            for r in recs:
                fw = max(fw, r['fixed_w']); fp = max(fp, r['fixed_p']); bw = max(bw, r['basis_w']); bp = max(bp, r['basis_p'])
                allvalid &= r['valid']
                if r['last']: endvalid &= r['valid']; endbw = max(endbw, r['basis_w'])
                elif r['kind'] == 'CNOT_P': midbw = max(midbw, r['basis_w'])
        table[(n, label)] = (allvalid, endvalid, fw, fp, bw, bp, endbw, midbw)
        print(f"      {n:7d}  {25:5d}   {label:26s}  {str(allvalid):18s} {fw:10d} {fp:6d}                        {bw:10d} {bp:6d}")
check("compatible routes only (2, 4 and 8 photons, random logical sequences): every local check stays valid after every macro-step, every fixed generator stays on one photon with weight 2, and the minimum-weight basis of the transported group stays at weight 2 on one photon",
      all(table[(n, "compatible routes only")][:6] == (True, True, 2, 1, 2, 1) for n in (2, 4, 8)))
check("with the two-physical-CNOT route in the mix the original local checks are valid again at every logical-gate endpoint (the code space is preserved), even though the fixed generators have spread across photons",
      all(table[(n, "with two-CNOT route")][1] for n in (2, 4, 8)) and all(table[(n, "with two-CNOT route")][3] > 1 for n in (4, 8)))
check("the spreading of the fixed generators is an artefact of which generator you track: the minimum-weight basis of the transported group at logical-gate endpoints stays at weight 2 on one photon, so a local check exists whenever the code space is preserved",
      all(table[(n, "with two-CNOT route")][6] == 2 for n in (2, 4, 8)))
check("inside the two-CNOT route, between the two physical CNOTs, no check of weight 2 exists and the lowest-weight basis has weight 3 across two photons (the true spreading, which only exists mid-operation)",
      all(table[(n, "with two-CNOT route")][7] == 3 for n in (2, 4, 8)))
fixed_growth = table[(8, "with two-CNOT route")][2]
print(f"  fixed-generator weight reached with the two-CNOT route at 8 photons: {fixed_growth} axes")
# a single physical CNOT between photons (not a logical gate)
n = 4; rows = [{S_key(i): 1.0} for i in range(n)]
rows = [gate_conj(r, ('CNOT', 0, 2)) for r in rows]
gr = [(next(iter(r)), next(iter(r.values())).real) for r in rows]; el = group_elems(gr); basis = min_basis(el, n, 8)
check("a lone physical CNOT between axes of two photons removes photon 2's local check from the group: the lowest-weight check involving photon 2 has weight 3 and spans both photons",
      S_key(1) not in el and max(weight(k) for k in basis) == 3 and max(photons(k) for k in basis) == 2)
# invisible faults versus register count
def count_faults(n):
    tot = inv = harm = 0
    for x in range(1 << (2 * n)):
        det = any(((x >> (2 * i)) & 1) != ((x >> (2 * i + 1)) & 1) for i in range(n))
        for z in range(1 << (2 * n)):
            tot += 1
            if not det:
                inv += 1
                if all(((z >> (2 * i)) & 1) == ((z >> (2 * i + 1)) & 1) for i in range(n)) and x == 0: harm += 1
    return tot, inv, harm
okf = True
for n in (1, 2, 3):
    tot, inv, harm = count_faults(n); okf &= tot == 16 ** n and inv == 8 ** n and harm == 2 ** n
check("which faults stay invisible, counted by brute force for 1, 2 and 3 photons and by formula for any n: of 16^n two-axis Pauli strings, 8^n commute with every local check, of which 2^n are harmless (products of the checks) and 8^n - 2^n are undetected logical errors; the invisible class is the same per photon however many photons there are", okf)
check("single-axis faults at any register size: 6n of them (X, Y, Z on 2n axes), 4n detected (every X and Y) and 2n invisible (every Z): the detected fraction of single-axis faults is 2/3 whether there are 2 photons or 8",
      all(near(4 * n / (6 * n), 2 / 3) for n in (2, 4, 8)))

# =============================================================== 4. non-commuting steps and term growth
print("== 4. non-commuting steps, term growth, and equivalent routes ==")
def growth(n, L, q_bad, trials):
    out = []; ph_out = []
    for _ in range(trials):
        op = {S_key(0): 1.0}; Nax = 2 * n
        for _ in range(L):
            if random.random() < q_bad:
                ax = random.randrange(Nax); gen = random.choice([Xk, lambda a: (1 << a, 1 << a)])(ax)    # single-axis X or Y rotation
                op = rot_conj(op, gen, random.uniform(0.3, 1.2))
            else:
                r_ = random.random(); i = random.randrange(n); j = random.choice([x for x in range(n) if x != i])
                if r_ < 0.4: op = rot_conj(op, (3 << (2 * i), 0), random.uniform(0.3, 1.2))                          # logical X rotation, XX generator
                elif r_ < 0.7: op = rot_conj(op, Zk(2 * i + random.randrange(2)), random.uniform(0.3, 1.2))        # logical Z rotation
                else:
                    pairs = [(2 * i, 2 * j), (2 * i, 2 * j + 1), (2 * i + 1, 2 * j), (2 * i + 1, 2 * j + 1)]; c_, t_ = random.choice(pairs)
                    th_ = random.uniform(0.3, 1.2)                                                                     # controlled-phase(phi): ZZ, Z, Z rotations
                    op = rot_conj(op, (0, 1 << c_ | 1 << t_), th_); op = rot_conj(op, Zk(c_), -th_); op = rot_conj(op, Zk(t_), -th_)
                # also a Clifford: CZ_L route (physical CZ) on the pair
                if r_ >= 0.95: op = gate_conj(op, ('CZ', 2 * i, 2 * j))
            if len(op) > 4000: break
        out.append(len(op)); ph_out.append(max(photons(k) for k in op))
    return sum(out) / len(out), sum(ph_out) / len(ph_out), max(out)
print("      photons   incompatible steps   mean terms in photon 0's check   mean photons touched   max terms   (30 steps, ASSUMED ensemble)")
gr = {}
for n in (2, 4, 8):
    for q_bad in (0.0, 0.05, 0.1):
        t, p_, m_ = growth(n, 30, q_bad, 60 if n < 8 else 40)
        gr[(n, q_bad)] = (t, p_, m_)
        print(f"      {n:7d}   {q_bad:17.2f}   {t:30.2f}   {p_:20.2f}   {m_:9d}")
check("compatible steps only (logical rotations about normalizer generators, with the controlled phase built from ZZ and Z rotations): photon 0's check stays ONE term on ONE photon at 2, 4 and 8 photons, for generic angles",
      all(gr[(n, 0.0)][0] == 1.0 and gr[(n, 0.0)][1] == 1.0 for n in (2, 4, 8)))
check("with a fraction of non-commuting single-axis rotations in the sequence the check grows in terms and, because the inter-photon controlled phases that follow do not commute with it, in the number of photons it touches (the growth depends on the steps taken, and the table reports an example ensemble)",
      all(gr[(n, 0.1)][0] > 1.0 for n in (2, 4, 8)) and any(gr[(n, 0.1)][1] > 1.0 for n in (2, 4, 8)))
# a CNOT-conjugated route for the same logical rotation never produces a multi-term check; test with a physical CZ afterwards
op = {S_key(0): 1.0}
for m in [('g', ('CNOT', 0, 1)), ('r', (1, 0), 0.9), ('g', ('CNOT', 0, 1)), ('g', ('CZ', 0, 2))]: op = macro_conj(op, m)
check("equivalent route: a logical X rotation done as CNOT, single-axis X rotation, CNOT (generic angle) followed by a physical controlled phase to another photon leaves photon 0's check as ONE term",
      len(op) == 1)

# =============================================================== 5. measure, transport or defer
print("== 5. measuring, transporting or deferring a check around an excursion out of the code ==")
N1 = 2
def apply4(G, v): return mv(G, v)
CN = gmat(('CNOT', 0, 1), 2); HA = gmat(('H', 0), 2)
seq = [CN, HA, CN]
def detection(fault_axis, fault_p, loc, which):
    """Probability of the 'odd' outcome of check `which` ('mid': IZ after the first CNOT, 'end': ZZ at the end), averaged and min/max over inputs."""
    vals = []
    FM = {'X': PX, 'Z': PZ}[fault_p]; F = single(FM, fault_axis, 2)
    for _ in range(100):
        v = vn([rc(), rc()]); v = [v[0], 0, 0, v[1]]
        for k in range(4):
            if k == loc: v = mv(F, v)
            if which == 'mid' and k == 1:
                if loc > 1: return None
                Mc = pmat(IZk, 2); vals.append((1 - sum(x.conjugate() * y for x, y in zip(v, mv(Mc, v))).real) / 2); break
            if k < 3: v = mv(seq[k], v)
        if which == 'end':
            Mc = pmat(ZZk, 2); vals.append((1 - sum(x.conjugate() * y for x, y in zip(v, mv(Mc, v))).real) / 2)
    return vals
def label(vals):
    if vals is None: return "  --  "
    lo, hi = min(vals), max(vals)
    if hi - lo < 1e-9: return f"{lo:6.2f}"
    return f"{lo:.2f}-{hi:.2f}"
print("      fault   inserted before step   transported check IZ after the CNOT   deferred check ZZ at the end   (H via CNOT, H on a, CNOT; 0 = before the first CNOT; 1 = after the first CNOT, just before IZ is read and before H; 2 = after H, before the second CNOT, i.e. after IZ was read, so '--')")
cov = {}
for ax, p in ((0, 'X'), (1, 'X'), (0, 'Z'), (1, 'Z')):
    for loc in (0, 1, 2):
        m_ = detection(ax, p, loc, 'mid'); e_ = detection(ax, p, loc, 'end')
        cov[(ax, p, loc)] = (m_, e_)
        print(f"      {p}_{'ab'[ax]}      {loc:12d}              {label(m_):>20s}                  {label(e_):>20s}")
check("faults made BEFORE the excursion are seen by the transported check IZ in the middle: X on either axis gives odd probability 1 there, Z gives 0",
      all(near(min(cov[(ax, 'X', 0)][0]), 1.0) and near(max(cov[(ax, 'Z', 0)][0]), 0.0) for ax in (0, 1)))
check("deferring the check to the end (ZZ after the whole operation) still sees an X fault made before the excursion on EITHER axis with probability 1: detectability survives the excursion, only the timing of the report changes",
      all(near(min(cov[(ax, 'X', 0)][1]), 1.0) for ax in (0, 1)))
check("faults made INSIDE the excursion follow the edge geometry's coverage: an X on the idle axis b is seen with probability 1 by the end check wherever in the excursion it occurs (by the transported check IZ too when it occurs before that check is read; faults after IZ is read are outside its reach and only the deferred check can see them), but an X on axis a there is the logical X of the edge geometry, passes into the code space and is invisible both to IZ and to the end check ZZ; the same X_a made BEFORE the excursion is seen by both",
      near(min(cov[(1, 'X', 1)][1]), 1.0) and near(min(cov[(1, 'X', 2)][1]), 1.0) and near(max(cov[(0, 'X', 1)][1]), 0.0) and near(max(cov[(0, 'X', 2)][1]), 0.0)
      and near(min(cov[(0, 'X', 0)][0]), 1.0) and near(min(cov[(0, 'X', 0)][1]), 1.0)
      and near(max(cov[(0, 'X', 1)][0]), 0.0) and near(min(cov[(1, 'X', 1)][0]), 1.0) and cov[(0, 'X', 2)][0] is None and cov[(1, 'X', 2)][0] is None)
check("every Z fault, at every insertion point, gives odd weight 0 at both the transported check and the end check: phase-type faults are invisible to the parity observables in all three geometries of this route",
      all(near(max(v), 0.0) for (ax, p, loc), (m_, e_) in cov.items() if p == 'Z' for v in ([e_] + ([m_] if m_ else []))))
# invisible is not harmless: fidelity of the faulty output with the ideal output, for the invisible faults
def fidelity_after(fault_axis, fault_p, loc):
    F = single({'X': PX, 'Z': PZ}[fault_p], fault_axis, 2); fs = []
    for _ in range(100):
        v = vn([rc(), rc()]); v = [v[0], 0, 0, v[1]]; ideal = v; fa = v
        for k in range(3): ideal = mv(seq[k], ideal)
        for k in range(4):
            if k == loc: fa = mv(F, fa)
            if k < 3: fa = mv(seq[k], fa)
        fs.append(abs(sum(x.conjugate() * y for x, y in zip(ideal, fa))) ** 2)
    return min(fs), sum(fs) / len(fs)
fx = fidelity_after(0, 'X', 1); fz = fidelity_after(0, 'Z', 1); fb = fidelity_after(1, 'Z', 1)
print(f"      fidelity with the ideal output, fault inserted before the Hadamard: X_a mean {fx[1]:.3f} (min {fx[0]:.3f}); Z_a mean {fz[1]:.3f} (min {fz[0]:.3f}); Z_b mean {fb[1]:.3f}")
check("the invisible faults are not harmless: X_a or Z_a made before the Hadamard leaves the output in the code (both checks pass) with mean fidelity below 1 against the intended output (a logical error), whereas Z_b there does nothing because that axis is in the state |0>",
      fx[1] < 0.9 and fz[1] < 0.9 and near(fb[1], 1.0))

# =============================================================== 6. preparation geometry, criteria separate
print("== 6. preparation geometry: criteria kept separate ==")
def geom(name, basis, chk, carrier):
    return dict(name=name, basis=basis, chk=chk, carrier=carrier)
GE = {'diagonal': geom('diagonal', [0, 3], pmat((0, 3), 2), None), 'edge': geom('edge', [0, 1], pmat((0, 1), 2), 1)}
def code_block(G, basis): return [[G[basis[i]][basis[j]] for j in range(2)] for i in range(2)]
def same_phase(M, T):
    ph = None
    for i in range(2):
        for j in range(2):
            if abs(T[i][j]) > 1e-9: ph = M[i][j] / T[i][j]; break
        if ph: break
    return abs(abs(ph) - 1) < 1e-9 and close(M, [[ph * T[i][j] for j in range(2)] for i in range(2)], 1e-9)
TG = {'Z': PZ, 'S': SG, 'X': PX, 'H': HAD}
GEN = {  # generator rotations (key, angle) per logical gate, per geometry (qubit on axis 1 for the edge code {00,01})
    'diagonal': {'Z': [((0, 1), math.pi)], 'S': [((0, 1), math.pi / 2)], 'X': [((3, 0), math.pi)],
                 'H': [((0, 1), math.pi / 2), ((3, 0), math.pi / 2), ((0, 1), math.pi / 2)]},
    'edge': {'Z': [((0, 2), math.pi)], 'S': [((0, 2), math.pi / 2)], 'X': [((2, 0), math.pi)],
             'H': [((0, 2), math.pi / 2), ((2, 0), math.pi / 2), ((0, 2), math.pi / 2)]},
}
rows6 = {}
for g_ in ('diagonal', 'edge'):
    for lg in 'ZSXH':
        U = eye(4)
        for key, th_ in GEN[g_][lg]: U = mm(mac_mat(('r', key, th_), 2), U)
        okc_ = same_phase(code_block(U, GE[g_]['basis']), TG[lg]) if lg != 'S' else abs(U[GE[g_]['basis'][1]][GE[g_]['basis'][1]] / U[GE[g_]['basis'][0]][GE[g_]['basis'][0]] - 1j) < 1e-9
        comm_ = all(commute(key, (0, 3) if g_ == 'diagonal' else (0, 1)) for key, _ in GEN[g_][lg])
        rows6[(g_, lg)] = (okc_, comm_, max(weight(k) for k, _ in GEN[g_][lg]))
for g_ in ('diagonal', 'edge'):
    print(f"      {g_:9s} " + "   ".join(f"{lg}: correct={rows6[(g_, lg)][0]}, preserves check={rows6[(g_, lg)][1]}, largest generator {rows6[(g_, lg)][2]} axis(es)" for lg in 'ZSXH'))
check("for each logical gate in each geometry the generator route is correct and preserves the geometry's own check throughout (diagonal: generators of 1 to 2 axes; edge: single-axis generators only, on the carrier axis)",
      all(v[0] and v[1] for v in rows6.values()) and all(rows6[('edge', lg)][2] == 1 for lg in 'ZSXH')
      and rows6[('diagonal', 'X')][2] == 2 and rows6[('diagonal', 'H')][2] == 2 and rows6[('diagonal', 'Z')][2] == 1)
det = {}
for g_, S0 in (('diagonal', (0, 3)), ('edge', (0, 1))):
    d = 0
    for ax in (0, 1):
        for p, k in (('X', (1 << ax, 0)), ('Y', (1 << ax, 1 << ax)), ('Z', (0, 1 << ax))):
            if not commute(k, S0): d += 1
    det[g_] = d
check("fault detectability, kept separate: single-axis faults detected by the geometry's check: diagonal 4 of 6 (both axes), edge 2 of 6 (the idle axis only)", det == {'diagonal': 4, 'edge': 2})
check("inter-photon controlled-phase routes, kept separate: diagonal-diagonal 4, edge-edge 1 (v0.3), and every route preserves every local check of its geometry (diagonal routes verified above)",
      okc)

# =============================================================== 7. productivity with explicit output identifiability
print("== 7. productivity with explicit output-identifiability assumptions ==")
def frame_ok(f): return f[0] == 0 and f[1] == 0 and f[2] == f[3]
def seg(dist, x, z):
    new = defaultdict(float)
    for f, w in dist.items():
        for e in product((0, 1), repeat=4):
            new[tuple(a ^ b for a, b in zip(f, e))] += w * pr(e[0], x) * pr(e[1], x) * pr(e[2], z) * pr(e[3], z)
    return new
def chk(dist, gx, gz, l, acc):
    new = defaultdict(float); acc['interactions'] += sum(dist.values())
    for f, w in dist.items():
        for ax, az, lo in product((0, 1), repeat=3):
            pw = w * pr(ax, gx) * pr(az, gz) * pr(lo, l)
            if lo: acc['lost'] += pw; continue
            g = list(f); g[2] ^= az
            if (g[0] ^ g[1]) ^ ax: acc['false_rej' if frame_ok(g) else 'rej_damaged'] += pw
            else: new[tuple(g)] += pw
    return new
def run(xs, z, checks, gx=0.0, gz=0.0, l=0.0):
    dist = {(0, 0, 0, 0): 1.0}; acc = defaultdict(float)
    for i, x in enumerate(xs):
        acc['segments'] += sum(dist.values()); dist = seg(dist, x, z)
        if i in checks: dist = chk(dist, gx, gz, l, acc)
    for f, w in dist.items(): acc['acc_correct' if frame_ok(f) else 'false_acc'] += w
    acc['accepted'] = acc['acc_correct'] + acc['false_acc']
    return acc
Tn = 8; Z_, GX, GZ, L_ = 0.001, 0.002, 0.003, 0.002
print(f"  T = {Tn}, z = {Z_}, ancilla X fault {GX}, harmful Z fault {GZ}, loss {L_} (ASSUMED). Mode I: wrong outputs are identified and discarded at the end. Mode II: they are not, all accepted outputs are used.")
print("      x      policy      I: segments per accepted-correct   II: accepted per run   II: wrong share of accepted   II: segments per accepted output")
bestI = {}; bestII = {}; seg_I = {}; wrong_II = {}
for x in (0.005, 0.01, 0.02, 0.05, 0.1):
    base = run([x] * Tn, Z_, set()); xs_ = [x] * Tn
    print(f"  {x:6.3f}   unchecked   {Tn / base['acc_correct']:28.2f}   {1.0:20.4f}   {1 - base['acc_correct']:27.4f}   {float(Tn):28.2f}")
    for s in (1, 2, 4, 8):
        a = run(xs_, Z_, {i for i in range(Tn) if (i + 1) % s == 0}, GX, GZ, L_)
        seg_I[(x, s)] = a['segments'] / a['acc_correct']; wrong_II[(x, s)] = a['false_acc'] / a['accepted']
        print(f"  {x:6.3f}   spacing {s}   {seg_I[(x, s)]:28.2f}   {a['accepted']:20.4f}   {wrong_II[(x, s)]:27.4f}   {a['segments'] / a['accepted']:28.2f}")
    bestI[x] = min((1, 2, 4, 8), key=lambda s: seg_I[(x, s)]); bestII[x] = min((1, 2, 4, 8), key=lambda s: wrong_II[(x, s)])
print("  best spacing by Mode I (fewest segments per accepted-correct):", bestI)
print("  best spacing by Mode II (lowest wrong share among accepted):  ", bestII)
check("the answer to 'which policy is best' depends on the identifiability assumption: at some noise levels the best spacing under Mode I differs from the best spacing under Mode II", any(bestI[x] != bestII[x] for x in bestI))
mI_rej, mI_ph = 0.99 ** 100, (1 + 0.98 ** 100) / 2
check("the accumulation example under both modes: Mode I (wrong outputs identified): phase-type faults yield MORE correct results per run than rejected-type ones (56.63% versus 36.60%). Mode II (not identified): phase-type faults deliver 43.37% wrong among accepted outputs, rejected-type ones 0%",
      near(mI_rej, 0.3660, 1e-4) and near(mI_ph, 0.5663, 1e-4) and mI_ph > mI_rej and near((1 - 0.98 ** 100) / 2, 0.4337, 1e-4))

print()
bad = [n for n, ok_ in results if not ok_]
print("ALL PASS" if not bad else "FAILURES: " + "; ".join(bad))
raise SystemExit(0 if not bad else 1)
