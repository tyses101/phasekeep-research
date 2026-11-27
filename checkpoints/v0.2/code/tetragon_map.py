# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tyler O'Bryan, where applicable
"""Ideal-model checks on one Tetragon (polarization x OAM, two binary Encoding Axies). Plain Python, no packages.

Index convention: state index = 2*pol + oam, so |00>=(H,-1) |01>=(H,+1) |10>=(V,-1) |11>=(V,+1).
Evidence: every result here is [[DERIVED]] for IDEAL, noise-free operations. Nothing is measured, and nothing says what a
physical device costs. Limits are listed in docs/tetragon-map-v0.md.

Parts
  1. Bell family: four maximally nonseparable states, which local operations permute them, the one-axis transpose property
  2. Time as a quantum control versus a classical schedule
  3. Complete mutually unbiased bases (MUBs) from Pauli stabilizers
  4. Map of the 15 stabilizer bases: which operation class links which pair
  5. Persistence: operations inside a maximally entangled class collapse to one 2x2 unitary
  6. Restricted input subspaces: when does an operation on one axis equal an operation on the other?
  7. Adaptive representation: what class of operation switches one two-vertex encoding of a logical qubit into another?
  8. Logical gates and geometry: does being free to choose the output encoding lower the cost of a logical gate? (U E1 = E2 G)
  9. Targeted verification of the diagonal encoding: which local settings give the logical state and the leakage?
"""
from itertools import product, combinations
from math import sqrt
from collections import Counter

S = 1 / sqrt(2)
I2 = [[1, 0], [0, 1]]; X = [[0, 1], [1, 0]]; Y = [[0, -1j], [1j, 0]]; Z = [[1, 0], [0, -1]]
H = [[S, S], [S, -S]]; PH = [[1, 0], [0, 1j]]

# ---------- small linear algebra ----------
def kron(M, N): return [[M[i // 2][j // 2] * N[i % 2][j % 2] for j in range(4)] for i in range(4)]
def mm4(M, N): return [[sum(M[i][k] * N[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
def mm2(M, N): return [[sum(M[i][k] * N[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def ap(M, x): return [sum(M[i][j] * x[j] for j in range(len(x))) for i in range(len(M))]
def ip(x, y): return sum(a.conjugate() * b for a, b in zip(x, y))
def close(M, N, t=1e-9): return all(abs(a - b) < t for r, s in zip(M, N) for a, b in zip(r, s))
def vclose(x, y, t=1e-9): return all(abs(a - b) < t for a, b in zip(x, y))
def same_ray(x, y): return abs(abs(ip(x, y)) - 1) < 1e-9
def vec(*pairs):
    x = [0j] * 4
    for i, a in pairs: x[i] = a
    return x
def schmidt(v):
    """(rank, ebits) of a normalised two-qubit vector across axis0 | axis1."""
    from math import log2
    a, b, c, d = v
    p = abs(a) ** 2 + abs(b) ** 2; q = abs(c) ** 2 + abs(d) ** 2; r = a * c.conjugate() + b * d.conjugate()
    disc = sqrt(max(0.0, (p - q) ** 2 + 4 * abs(r) ** 2)); ls = [(p + q + disc) / 2, (p + q - disc) / 2]
    rk = sum(1 for l in ls if l > 1e-10)
    return rk, -sum(l * log2(l) for l in ls if l > 1e-10)

def clifford_group():
    def canon(M):
        for r in M:
            for e in r:
                if abs(e) > 1e-9:
                    ph = e / abs(e)
                    return tuple(tuple((round((x / ph).real, 6), round((x / ph).imag, 6)) for x in rr) for rr in M)
    g = {canon(I2): I2}; fr = [I2]
    while fr:
        nf = []
        for M in fr:
            for gen in (H, PH):
                N = mm2(gen, M); c = canon(N)
                if c not in g: g[c] = N; nf.append(N)
        fr = nf
    return list(g.values())
CL = clifford_group()
ONE_AXIS = [kron(P, I2) for P in CL] + [kron(I2, P) for P in CL]
LOCAL = [kron(P, Q) for P in CL for Q in CL]
CZ = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]]
SWAP = [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]

# ---------- Part 1: Bell family ----------
A = vec((0, S), (3, S)); B = vec((0, S), (3, -S)); C = vec((1, S), (2, S)); D = vec((1, S), (2, -S))
BELL = {'A': A, 'B': B, 'C': C, 'D': D}

def part1():
    rows = {"flip pol": (kron(X, I2), 'C'), "flip OAM": (kron(I2, X), 'C'), "phase on pol": (kron(Z, I2), 'B'),
            "phase on OAM": (kron(I2, Z), 'B'), "flip+phase on pol (Z.X)": (kron(mm2(Z, X), I2), 'D'),
            "flip both": (kron(X, X), 'A')}
    for name, (M, tgt) in rows.items():
        assert vclose(ap(M, A), BELL[tgt]), name
    for n, v in BELL.items():
        assert schmidt(v)[0] == 2 and abs(schmidt(v)[1] - 1.0) < 1e-9
    for (n1, v1), (n2, v2) in combinations(BELL.items(), 2): assert abs(ip(v1, v2)) < 1e-9
    prod_basis = [vec((i, 1)) for i in range(4)]
    mags = sorted({round(abs(ip(p, v)), 4) for p in prod_basis for v in BELL.values()})
    assert mags == [0.0, 0.7071], mags
    def perm_of(U):
        out = []
        for n in 'ABCD':
            r = ap(U, BELL[n]); m = [i for i, k in enumerate('ABCD') if same_ray(r, BELL[k])]
            if len(m) != 1: return None
            out.append(m[0])
        return tuple(out)
    one = {p for U in ONE_AXIS if (p := perm_of(U)) is not None}
    both = {p for U in LOCAL if (p := perm_of(U)) is not None}
    nm = lambda p: ''.join('ABCD'[i] for i in p)
    assert sorted(nm(p) for p in one) == ['ABCD', 'BADC', 'CDAB', 'DCBA']
    assert len(both) == 24
    assert nm(perm_of(CZ)) == 'BACD'                      # CZ swaps A and B; a local S(x)S gives the same relabelling
    assert nm(perm_of(kron(PH, PH))) == 'BACD'
    assert nm(perm_of(SWAP)) == 'ABCD' and vclose(ap(SWAP, D), [-x for x in D])   # axis SWAP: labels fixed, one sign
    import math
    t = 0.7; R = [[math.cos(t), -math.sin(t)], [math.sin(t), math.cos(t)]]; RT = [[R[j][i] for j in range(2)] for i in range(2)]
    assert vclose(ap(kron(R, I2), A), ap(kron(I2, RT), A))                        # transpose property, state A only
    return len(one), len(both)

# ---------- Part 2: time as control ----------
def part2():
    """State = time(2) x pol(2). Controlled operation sum_k |k><k| (x) U_k."""
    def ctrl(U0, U1):
        M = [[0] * 4 for _ in range(4)]
        for i, j in product(range(2), repeat=2): M[i][j] = U0[i][j]; M[2 + i][2 + j] = U1[i][j]
        return M
    res = {}
    for uname, (U0, U1) in {"same op in both slots": (I2, I2), "none then flip": (I2, X)}.items():
        for sname, st in (("superposed time bins", [S, 0, S, 0]), ("one definite slot", [1, 0, 0, 0])):
            res[(uname, sname)] = schmidt(ap(ctrl(U0, U1), [complex(x) for x in st]))[1]
    assert abs(res[("same op in both slots", "superposed time bins")]) < 1e-9
    assert abs(res[("none then flip", "superposed time bins")] - 1.0) < 1e-9
    assert abs(res[("none then flip", "one definite slot")]) < 1e-9
    assert abs(0.99 ** 100 - 0.366) < 1e-3
    return res

# ---------- Part 3 and 4: stabilizer bases ----------
P1 = {'I': I2, 'X': X, 'Y': Y, 'Z': Z}
NAMES = [a + b for a in 'IXYZ' for b in 'IXYZ' if a + b != 'II']
PAULI = {n: kron(P1[n[0]], P1[n[1]]) for n in NAMES}
def commute(a, b): return close(mm4(PAULI[a], PAULI[b]), mm4(PAULI[b], PAULI[a]))
def proportional(M, N): return any(close(M, [[c * x for x in r] for r in N]) for c in (1, -1, 1j, -1j))
def find_lines():
    lines = []
    for a, b in combinations(NAMES, 2):
        if commute(a, b):
            c = [n for n in NAMES if n not in (a, b) and proportional(PAULI[n], mm4(PAULI[a], PAULI[b]))]
            if c and frozenset((a, b, c[0])) not in lines: lines.append(frozenset((a, b, c[0])))
    return lines
def basis_of(line):
    a, b, _ = sorted(line); out = []
    for s1, s2 in product((1, -1), repeat=2):
        P = mm4([[(i == j) + s1 * PAULI[a][i][j] for j in range(4)] for i in range(4)],
                [[(i == j) + s2 * PAULI[b][i][j] for j in range(4)] for i in range(4)])
        col = max(range(4), key=lambda c: sum(abs(P[r][c]) ** 2 for r in range(4)))
        v = [P[r][col] for r in range(4)]; n = sqrt(sum(abs(x) ** 2 for x in v)); out.append([x / n for x in v])
    return out
def kind(b): return 'product' if all(schmidt(v)[0] == 1 for v in b) else 'entangled'

def part3_4():
    lines = find_lines(); assert len(lines) == 15
    spreads = []
    def bt(ch, used):
        if len(ch) == 5: spreads.append(list(ch)); return
        for L in lines:
            if not (L & used) and (not ch or lines.index(L) > lines.index(ch[-1])): bt(ch + [L], used | L)
    bt([], frozenset()); assert len(spreads) == 6
    bases = [basis_of(L) for L in lines]; kinds = [kind(b) for b in bases]
    assert Counter(kinds) == {'product': 9, 'entangled': 6}
    for sp in spreads:
        Bs = [basis_of(L) for L in sp]
        assert all(abs(ip(u, w)) < 1e-9 for b in Bs for u, w in combinations(b, 2))
        assert all(abs(abs(ip(u, w)) ** 2 - 0.25) < 1e-9 for i, j in combinations(range(5), 2) for u in Bs[i] for w in Bs[j])
        assert Counter(kind(b) for b in Bs) == {'product': 3, 'entangled': 2}
    assert {sum(1 for sp in spreads if L in sp) for L in lines} == {2}
    enc, bell = frozenset(('IZ', 'ZI', 'ZZ')), frozenset(('XX', 'YY', 'ZZ'))
    assert not any(enc in sp and bell in sp for sp in spreads)
    assert Counter(round(abs(ip(u, w)), 4) for u in basis_of(enc) for w in basis_of(bell)) == {0.0: 8, 0.7071: 8}
    # --- Part 4: map
    def image(U, i):
        out = [ap(U, v) for v in bases[i]]
        for j, b in enumerate(bases):
            if all(any(same_ray(o, w) for w in b) for o in out): return j
    reach = lambda ops, i: {image(U, i) for U in ops} - {None}
    cls = {}
    for i in range(15):
        r1, r2 = reach(ONE_AXIS, i), reach(LOCAL, i); r3 = set()
        for b in r2:
            c = image(CZ, b)
            if c is not None: r3 |= reach(LOCAL, c)
        for j in range(15):
            cls[(i, j)] = 'single-axis' if j in r1 else 'local, both axes' if j in r2 else 'one entangling gate + local' if j in r3 else 'unreached'
    tot = Counter(cls.values())
    assert tot == {'single-axis': 81, 'local, both axes': 36, 'one entangling gate + local': 108} and sum(tot.values()) == 225
    by = {(a, b): Counter(cls[(i, j)] for i in range(15) for j in range(15) if kinds[i] == a and kinds[j] == b)
          for a in ('product', 'entangled') for b in ('product', 'entangled')}
    assert by[('entangled', 'entangled')] == {'single-axis': 36}
    assert by[('product', 'product')] == {'single-axis': 45, 'local, both axes': 36}
    assert by[('product', 'entangled')] == {'one entangling gate + local': 54} == by[('entangled', 'product')]
    return tot, by


# ---------- Part 5: persistence inside an entangled class ----------
def part5():
    import random, math, cmath
    random.seed(5)
    def rand_u():
        a, b, c = [random.uniform(0, 2 * math.pi) for _ in range(3)]
        return [[cmath.exp(1j * a) * math.cos(b), cmath.exp(1j * c) * math.sin(b)],
                [-cmath.exp(-1j * c) * math.sin(b), cmath.exp(-1j * a) * math.cos(b)]]
    T = lambda M: [[M[j][i] for j in range(2)] for i in range(2)]
    phi = vec((0, S), (3, S)); v = phi[:]; M = I2
    for _ in range(200):
        U = rand_u()
        if random.random() < 0.5: v = ap(kron(U, I2), v); M = mm2(U, M)      # on polarization: left-multiply
        else: v = ap(kron(I2, U), v); M = mm2(M, T(U))                      # on OAM: right-multiply by transpose
    assert vclose(v, ap(kron(M, I2), phi))
    rk, eb = schmidt(v); assert rk == 2 and abs(eb - 1.0) < 1e-9
    return True

# ---------- Part 6: restricted-subspace substitution ----------
def part6():
    import random, cmath, math
    random.seed(9)
    SDG = [[1, 0], [0, -1j]]
    GATES = {'Z': Z, 'S': PH, 'S-dagger': SDG, 'X': X, 'H': H, 'I': I2}
    def basis_vec(i): v = [0j] * 4; v[i] = 1; return v
    def equal_up_to_phase(M1, M2, sub):
        c = None
        for i in sub:
            a, b = ap(M1, basis_vec(i)), ap(M2, basis_vec(i))
            k = max(range(4), key=lambda r: abs(b[r]))
            if abs(b[k]) < 1e-9: return False
            ci = a[k] / b[k]
            if abs(abs(ci) - 1) > 1e-9: return False
            if c is None: c = ci
            elif abs(c - ci) > 1e-9: return False
            if not vclose(a, [c * x for x in b]): return False
        return True
    def trivial_on(M, sub):      # acts as a single scalar on the subspace
        return equal_up_to_phase(M, [[1 if i == j else 0 for j in range(4)] for i in range(4)], sub)
    found = {}
    for k in (2, 3, 4):
        for sub in combinations(range(4), k):
            pairs = [(u, v) for u, U in GATES.items() for v, V in GATES.items()
                     if not trivial_on(kron(U, I2), sub) and equal_up_to_phase(kron(U, I2), kron(I2, V), sub)]
            found[sub] = pairs
    assert sorted(found[(0, 3)]) == sorted([('Z', 'Z'), ('S', 'S'), ('S-dagger', 'S-dagger')]), found[(0, 3)]   # span{00,11}: same phase gate on either axis
    assert sorted(found[(1, 2)]) == sorted([('Z', 'Z'), ('S', 'S-dagger'), ('S-dagger', 'S')]), found[(1, 2)]  # span{01,10}
    assert all(not pr for sub, pr in found.items() if sub not in ((0, 3), (1, 2)))
    assert not any(u in ('X', 'H') for pr in found.values() for u, v in pr)
    # the diagonal example with unknown amplitudes
    for _ in range(50):
        a = complex(random.gauss(0, 1), random.gauss(0, 1)); b = complex(random.gauss(0, 1), random.gauss(0, 1))
        n = sqrt(abs(a) ** 2 + abs(b) ** 2); psi = vec((0, a / n), (3, b / n))
        phi_ = random.uniform(0, 2 * math.pi); G = [[1, 0], [0, cmath.exp(1j * phi_)]]
        assert vclose(ap(kron(G, I2), psi), ap(kron(I2, G), psi))        # any phase gate: same on either axis
        ZZ = kron(Z, Z)
        assert abs(ip(psi, ap(ZZ, psi)) - 1) < 1e-9                       # inside the subspace, parity = +1
        assert abs(ip(ap(kron(X, I2), psi), ap(ZZ, ap(kron(X, I2), psi))) + 1) < 1e-9     # one flip: parity -1, whatever a, b are
        assert abs(ip(ap(kron(Z, I2), psi), ap(ZZ, ap(kron(Z, I2), psi))) - 1) < 1e-9     # one phase error: parity still +1 (not detected)
        assert vclose(ap(kron(X, X), psi), vec((0, b / n), (3, a / n)))   # logical flip needs both axes
    return found

# ---------- Parts 7 and 8: encodings, switching and logical gates ----------
ENC = [(a, b) for a in range(4) for b in range(4) if a != b]     # ordered pairs of vertices = logical 0, logical 1
def _kind(a, b): return 'edge' if bin(a ^ b).count('1') == 1 else 'diagonal'
def _mat(a, b):
    ea = [0j] * 4; eb = [0j] * 4; ea[a] = 1; eb[b] = 1; return (ea, eb)
def _key(E):
    flat = [x for col in E for x in col]
    for x in flat:
        if abs(x) > 1e-9: ph = x / abs(x); break
    return tuple((round((x / ph).real, 5) + 0.0, round((x / ph).imag, 5) + 0.0) for x in flat)
def _app(U, E): return tuple(ap(U, col) for col in E)
def _orbit(ops, starts):
    out = {}
    for E in starts:
        for U in ops:
            F = _app(U, E); out.setdefault(_key(F), F)
    return out
_STAGES = {}
def stages():
    """For every ordered two-vertex encoding E1: the sets of encodings (as keys) reachable by, cheapest first,
    a single-axis Clifford; local Cliffords on both axes; local-SWAP-local; local-CZ-local. About half a minute."""
    if not _STAGES:
        for (a, b) in ENC:
            E = _mat(a, b); L = _orbit(LOCAL, [E])
            _STAGES[(a, b)] = (set(_orbit(ONE_AXIS, [E])), set(L),
                               set(_orbit(LOCAL, _orbit([SWAP], L.values()).values())),
                               set(_orbit(LOCAL, _orbit([CZ], L.values()).values())))
    return _STAGES
CLASS_NAMES = ['frame update only', 'single-axis', 'local, both axes', 'axis SWAP + local', 'one entangling gate + local']
def _cost(E1, target):
    if _key(target) == _key(_mat(*E1)): return 0
    for i, st in enumerate(stages()[E1]):
        if _key(target) in st: return i + 1
    return 99

def part7():
    """Switching with the logical operation equal to the identity: U E1 = E2 up to one global phase."""
    res = {(E1, E2): CLASS_NAMES[max(1, _cost(E1, _mat(*E2)))] if E1 != E2 else 'single-axis' for E1 in ENC for E2 in ENC}
    by = {(t1, t2): Counter(v for ((a, b), (c, d)), v in res.items() if _kind(a, b) == t1 and _kind(c, d) == t2)
          for t1 in ('edge', 'diagonal') for t2 in ('edge', 'diagonal')}
    assert by[('edge', 'edge')] == {'single-axis': 24, 'axis SWAP + local': 32, 'local, both axes': 8}, by[('edge', 'edge')]
    assert by[('edge', 'diagonal')] == {'one entangling gate + local': 32} == by[('diagonal', 'edge')]
    assert by[('diagonal', 'diagonal')] == {'single-axis': 12, 'local, both axes': 4}
    assert sum(sum(c.values()) for c in by.values()) == 144
    return by

def part8():
    """Logical gate G with output encoding free: U E1 = E2 G. Compare E2 = E1 (fixed geometry) with the best of the 12 encodings."""
    def lg(E, G): return tuple([sum(E[k][r] * G[k][j] for k in range(2)) for r in range(4)] for j in range(2))
    gates = {'X': X, 'Z': Z, 'S': PH, 'H': H}
    out = {}
    for gname, G in gates.items():
        for t in ('edge', 'diagonal'):
            fixed = Counter(); free = Counter()
            for E1 in ENC:
                if _kind(*E1) != t: continue
                fixed[CLASS_NAMES[_cost(E1, lg(_mat(*E1), G))]] += 1
                free[CLASS_NAMES[min(_cost(E1, lg(_mat(*E2), G)) for E2 in ENC)]] += 1
            out[(gname, t)] = (dict(fixed), dict(free))
    assert out[('X', 'edge')] == ({'single-axis': 8}, {'frame update only': 8})
    assert out[('X', 'diagonal')] == ({'local, both axes': 4}, {'frame update only': 4})
    for g in ('Z', 'S'):
        for t, n in (('edge', 8), ('diagonal', 4)): assert out[(g, t)] == ({'single-axis': n}, {'single-axis': n})
    assert out[('H', 'edge')] == ({'single-axis': 8}, {'single-axis': 8})
    assert out[('H', 'diagonal')] == ({'one entangling gate + local': 4}, {'one entangling gate + local': 4})
    return out

# ---------- Part 9: targeted verification of the diagonal encoding ----------
def part9():
    import random
    random.seed(21)
    for _ in range(100):
        a = complex(random.gauss(0, 1), random.gauss(0, 1)); b = complex(random.gauss(0, 1), random.gauss(0, 1))
        n = sqrt(abs(a) ** 2 + abs(b) ** 2); a, b = a / n, b / n; psi = vec((0, a), (3, b))
        ex = lambda M: ip(psi, ap(M, psi))
        assert abs(ex(kron(Z, Z)) - 1) < 1e-9                                  # parity setting: ZZ = +1 inside the subspace
        bloch = (2 * (a.conjugate() * b).real, 2 * (a.conjugate() * b).imag, abs(a) ** 2 - abs(b) ** 2)
        assert abs(ex(kron(X, X)) - bloch[0]) < 1e-9                           # logical X from the XX setting
        assert abs(ex(kron(Y, X)) - bloch[1]) < 1e-9                           # logical Y from the YX setting
        assert abs(ex(kron(Z, I2)) - bloch[2]) < 1e-9                          # logical Z from the ZZ setting (either axis)
    assert round(3 / 0.01) == 300 and round(3 / 0.001) == 3000                  # rule of three, 95% upper bound with zero events
    return True


def main():
    n1, n2 = part1()
    print("1. Bell family OK: six operation rows, Gram = identity, encoding-vs-Bell overlaps {0, 0.7071}, CZ and S(x)S both relabel A<->B,")
    print(f"   axis SWAP fixes all four labels (one sign), transpose property. Permutations of {{A,B,C,D}}: single-axis {n1} of 24, both axes {n2} of 24.")
    r = part2()
    print("2. Time as control OK (ebits between time and polarization):")
    for (u, s), e in r.items(): print(f"   {u:22s} {s:22s} {abs(e):.3f}")
    print("   0.99^100 = %.3f" % (0.99 ** 100))
    tot, by = part3_4()
    print("3. MUBs OK: 15 commuting Pauli triples, 6 complete sets, each = 3 product + 2 entangled bases, pairwise unbiased;")
    print("   every basis is in exactly 2 sets; encoding and Bell bases are in no common set.")
    print("4. Basis map OK, 225 ordered pairs:", dict(tot))
    for k, c in by.items(): print(f"   {k[0]:9s} -> {k[1]:9s}", dict(c))
    part5()
    print("5. Persistence OK: 200 random single-axis operations on either axis equal one 2x2 unitary on one axis; Schmidt weights stay 0.5, 0.5.")
    f = part6()
    print("6. Restricted subspaces OK (operation pairs, one axis vs the other, equal up to a global phase on the subspace):")
    for sub in ((0, 3), (1, 2)): print("   span of vertices", [format(i, '02b') for i in sub], "->", f[sub])
    print("   no pair for any other coordinate subspace; X and H are never substitutable; single X leaves the subspace (parity -1, detectable");
    print("   without knowing the amplitudes); a single phase error keeps parity +1 (not detected); logical X needs both axes.")
    print("   loss: -ln(0.99) = %.5f per interaction; 100 interactions leave %.1f%%" % (-__import__('math').log(0.99), 100 * 0.99 ** 100))
    by = part7()
    print("7. Switching encodings OK (144 ordered pairs of two-vertex encodings; edge = one bit differs, diagonal = both differ):")
    for k, c in by.items(): print(f"   {k[0]:8s} -> {k[1]:8s}", dict(c))
    o = part8()
    print("8. Logical gates, fixed versus free output encoding (count of the 8 edge or 4 diagonal starting encodings):")
    for (g, t), (fx, fr) in o.items(): print(f"   G={g} from {t:8s} fixed {fx} | free {fr}")
    part9()
    print("9. Diagonal encoding, targeted verification OK: settings ZZ, XX, YX give parity and the three logical components (3 of the 9 local")
    print("   Pauli settings of full two-qubit tomography); zero leakage events in n shots bounds leakage below about 3/n at 95% (300 shots for 1%).")
    print("tetragon_map.py: ALL PASS")

if __name__ == "__main__":
    main()
