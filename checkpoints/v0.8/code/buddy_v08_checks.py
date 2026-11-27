# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tyler O'Bryan, where applicable
"""Buddy verification, version 0.8: local versus joint verification geometries, and what it takes to move between them.
Plain Python, no packages.

Evidence: every result is [[DERIVED]] inside the stated model (ideal unitaries; exact Pauli algebra; 16-dimensional state vectors;
exact enumeration or exact Pauli-frame propagation for the probability tables). Noise values and workloads are [[ASSUMED]] examples.
Nothing here is a measurement, a hardware cost or a comparison with a conventional architecture. Gate counts, weights, photon spans and
interaction orders are structural proxies, never costs, and no combined score is formed anywhere.

Four axes (a1, b1, a2, b2) = qubits 0..3 of two photons (Tetragons). Pauli keys are (x, z) bit masks, bit q = axis q.
Signed observables are used throughout: a check is a signed Pauli whose expected value for valid information is +1.
  LOCAL  code L: checks ZZII, IIZZ   (the diagonal Tetragon encoding, one check per photon)
  JOINT  code J: checks ZZZZ, XXXX   (the standard [[4,2,2]] error-detecting code on the same four axes)

Parts
  A. Erratum to version 0.7 (three corrections) and engine validation
  1. The two verification geometries compared
  2. Conversion between them (unitary), its coverage profile, and fault propagation through it
  3. Gate compatibility
  4. Phase-fault coverage
  5. Extraction resources and correlated errors created by the verifier
  6. Adaptive selection: single-checkpoint enumeration and a two-phase workload model
"""
import math, random
from itertools import product, permutations
from collections import defaultdict, deque

random.seed(20261127)
results = []
def check(name, ok_):
    results.append((name, bool(ok_)))
    print(("PASS  " if ok_ else "FAIL  ") + name)
def near(a, b, t=1e-9): return abs(a - b) < t
def rc(): return complex(random.gauss(0, 1), random.gauss(0, 1))
def vn(v):
    n = math.sqrt(sum(abs(x) ** 2 for x in v)); return [x / n for x in v]

# =============================================================== Pauli engine (same conventions as version 0.7)
def pc(n): return bin(n).count('1')
def pmul(k1, k2):
    x1, z1 = k1; x2, z2 = k2; x = x1 ^ x2; z = z1 ^ z2
    return (pc(x1 & z1) + pc(x2 & z2) - pc(x & z) + 2 * pc(z1 & x2)) % 4, (x, z)
def commute(k1, k2): return (pc(k1[0] & k2[1]) + pc(k1[1] & k2[0])) % 2 == 0
def weight(k): return pc(k[0] | k[1])
def photons(k): return len({q // 2 for q in range(8) if ((k[0] | k[1]) >> q) & 1})
def gate_one(x, z, g):
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
def conj_op(op, g):
    x, z, s = op; x2, z2, sg = gate_one(x, z, g); return (x2, z2, s * sg)
def gmul(a, b):
    e, key = pmul((a[0], a[1]), (b[0], b[1])); assert e % 2 == 0
    return (key[0], key[1], a[2] * b[2] * (1 if e % 4 == 0 else -1))
def grp(gens):
    g1, g2 = gens; return frozenset([g1, g2, gmul(g1, g2)])
def gkey(elems): return tuple(sorted(elems))

# matrices
def kron(A, B): return [[A[i // len(B)][j // len(B[0])] * B[i % len(B)][j % len(B[0])] for j in range(len(A[0]) * len(B[0]))] for i in range(len(A) * len(B))]
def mm(A, B): return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def mv(A, v): return [sum(A[i][k] * v[k] for k in range(len(v))) for i in range(len(A))]
def dag(A): return [[complex(A[j][i]).conjugate() for j in range(len(A))] for i in range(len(A[0]))]
def eye(n): return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
def close(A, B, t=1e-9): return all(abs(A[i][j] - B[i][j]) < t for i in range(len(A)) for j in range(len(A[0])))
I2 = [[1, 0], [0, 1]]; PX = [[0, 1], [1, 0]]; PY = [[0, -1j], [1j, 0]]; PZ = [[1, 0], [0, -1]]
HAD = [[1 / math.sqrt(2), 1 / math.sqrt(2)], [1 / math.sqrt(2), -1 / math.sqrt(2)]]; SG = [[1, 0], [0, 1j]]
def pmat(k, N=4):
    M = [[1]]
    for q in range(N):
        xb, zb = (k[0] >> q) & 1, (k[1] >> q) & 1
        M = kron(M, {(0, 0): I2, (1, 0): PX, (1, 1): PY, (0, 1): PZ}[(xb, zb)])
    return M
def smat(op, N=4):
    M = pmat((op[0], op[1]), N); return [[op[2] * v for v in r] for r in M]
def single(M1, q, N):
    M = [[1]]
    for i in range(N): M = kron(M, M1 if i == q else I2)
    return M
def gmat(g, N=4):
    if g[0] == 'H': return single(HAD, g[1], N)
    if g[0] == 'S': return single(SG, g[1], N)
    dim = 1 << N; M = [[0] * dim for _ in range(dim)]
    for k in range(dim):
        b = [(k >> (N - 1 - q)) & 1 for q in range(N)]
        if g[0] == 'CNOT':
            if b[g[1]]: b[g[2]] ^= 1
            ph = 1
        else: ph = -1 if (b[g[1]] and b[g[2]]) else 1
        M[sum(bb << (N - 1 - q) for q, bb in enumerate(b))][k] = ph
    return M
def rotmat(key, th, N=4):
    c, s = math.cos(th / 2), math.sin(th / 2); P = pmat(key, N)
    return [[c * (1 if i == j else 0) - 1j * s * P[i][j] for j in range(len(P))] for i in range(len(P))]
def expect(v, M): return sum(x.conjugate() * y for x, y in zip(v, mv(M, v)))
def overlap(a, b): return sum(x.conjugate() * y for x, y in zip(a, b))

LG = ((0, 0b0011, 1), (0, 0b1100, 1))          # ZZII, IIZZ
JG = ((0, 0b1111, 1), (0b1111, 0, 1))          # ZZZZ, XXXX
LGRP, JGRP = grp(LG), grp(JG)
def gframes(G): return {(e[0], e[1]) for e in G} | {(0, 0)}
LF, JF = gframes(LGRP), gframes(JGRP)
def anti(frame, gens): return any(not commute(frame, (g[0], g[1])) for g in gens)
def classify(frame, gens, gf):
    if anti(frame, gens): return 'detected'
    return 'harmless' if frame in gf else 'logical'
ALL = [(x, z) for x in range(16) for z in range(16)]
SINGLE = [k for q in range(4) for k in ((1 << q, 0), (1 << q, 1 << q), (0, 1 << q))]
GATES = [('H', q) for q in range(4)] + [('S', q) for q in range(4)] + [('CNOT', c, t) for c in range(4) for t in range(4) if c != t] + [('CZ', i, j) for i in range(4) for j in range(i + 1, 4)]
def inter(g): return len({q // 2 for q in g[1:]}) == 2

# =============================================================== A. erratum and engine validation
print("== A. erratum to version 0.7, and engine validation ==")
okv = True
for _ in range(120):
    key = (random.randrange(16), random.randrange(16)); g = random.choice(GATES)
    x2, z2, s = gate_one(key[0], key[1], g); U = gmat(g)
    okv &= close(mm(U, mm(pmat(key), dag(U))), [[s * v for v in r] for r in pmat((x2, z2))], 1e-9)
check("the Pauli engine (gate rules with signs) equals explicit matrix conjugation on 120 random Pauli and gate pairs, four axes", okv)
mprod = mm(smat(JG[1]), smat(JG[0]))
okg = close(mprod, smat(gmul(JG[1], JG[0])), 1e-9) and gmul(JG[1], JG[0]) == (15, 15, 1)
check("signed group multiplication is right: XXXX times ZZZZ = +YYYY (the signs are tracked, not assumed)", okg and len(LGRP) == 3 and len(JGRP) == 3)

# --- E1: insertion points of the faults in the CNOT, H_a, CNOT route
CN = gmat(('CNOT', 0, 1), 2); HA = gmat(('H', 0), 2); seq = [CN, HA, CN]
ZZ2 = pmat((0, 3), 2)
def fault_row(axis, p, loc, ns=300):
    F = single({'X': PX, 'Z': PZ}[p], axis, 2); det = []; fid = []
    for _ in range(ns):
        v = vn([rc(), rc()]); v = [v[0], 0, 0, v[1]]; ideal = v; fa = v
        for k in range(3): ideal = mv(seq[k], ideal)
        for k in range(3):
            if k == loc: fa = mv(F, fa)
            fa = mv(seq[k], fa)
        det.append((1 - expect(fa, ZZ2).real) / 2); fid.append(abs(overlap(ideal, fa)) ** 2)
    return sum(det) / ns, sum(fid) / ns
print("  E1. single faults in CNOT(a,b), H on a, CNOT(a,b); position 0 = before the first CNOT, 1 = after the first CNOT and before H, 2 = after H and before the second CNOT")
print("      fault  position   P(final ZZ reads odd)   mean fidelity with the ideal output")
E1 = {}
for ax, p in ((0, 'X'), (0, 'Z'), (1, 'X'), (1, 'Z')):
    for loc in (0, 1, 2):
        E1[(ax, p, loc)] = fault_row(ax, p, loc); print(f"      {p}_{'ab'[ax]}      {loc}          {E1[(ax, p, loc)][0]:8.3f}                {E1[(ax, p, loc)][1]:8.3f}")
check("ERRATUM E1: version 0.7 said an X_a 'before the Hadamard' is invisible. That is true only AFTER the first CNOT (position 1: odd probability 0, logical error, mean fidelity well below 1). BEFORE the first CNOT (position 0) the same X_a is detected with probability 1",
      near(E1[(0, 'X', 0)][0], 1.0) and near(E1[(0, 'X', 1)][0], 0.0) and E1[(0, 'X', 1)][1] < 0.9 and near(E1[(0, 'X', 2)][0], 0.0))
check("ERRATUM E1 (continued): Z_a is invisible at positions 0, 1 and 2 and changes the output (fidelity below 1) at each; Z_b at position 1 or 2 does nothing because that axis is in |0>; X_b is detected at all positions",
      all(near(E1[(0, 'Z', l)][0], 0.0) and E1[(0, 'Z', l)][1] < 0.9 for l in (0, 1, 2)) and near(E1[(1, 'Z', 1)][1], 1.0) and near(E1[(1, 'Z', 2)][1], 1.0)
      and all(near(E1[(1, 'X', l)][0], 1.0) for l in (0, 1, 2)))

check("ERRATUM E1 (numbers): a logical Pauli error leaves a Haar-random logical input with mean fidelity exactly 1/3 against the intended output; the 0.29 and 0.32 printed in version 0.7 were 100-sample estimates of this, and the sampled values here (300 samples) are 0.32 to 0.35",
      all(abs(E1[k][1] - 1 / 3) < 0.05 for k in ((0, 'X', 1), (0, 'X', 2), (0, 'Z', 0), (0, 'Z', 1), (0, 'Z', 2), (1, 'Z', 0))))

# --- E2: physical controlled-phase routes, diagonal versus edge, computed here (version 0.7 carried 4 versus 1 from version 0.3)
def code_vec(enc, p, q):
    v = [0j] * 16
    v[(enc(p) * 4) + enc(q)] = 1; return v
enc_diag = lambda p: 3 * p                    # photon value (a, b) = (p, p)
enc_edge = lambda p: 2 * p                    # photon value (a, b) = (p, 0): data on axis a, axis b idle
CHK_D = [pmat((0, 0b0011)), pmat((0, 0b1100))]; CHK_E = [pmat((0, 0b0010)), pmat((0, 0b1000))]    # Z(b1), Z(b2) for the edge code
def route_stats(enc, chks):
    pres = lgl = 0
    for (i, j) in ((0, 2), (0, 3), (1, 2), (1, 3)):
        G = gmat(('CZ', i, j)); okp = all(close(mm(G, C), mm(C, G)) for C in chks); okl = True
        for p, q in product((0, 1), repeat=2):
            k = enc(p) * 4 + enc(q); okl &= near(G[k][k].real, -1 if (p and q) else 1) and all(abs(G[r][k]) < 1e-12 for r in range(16) if r != k)
        pres += okp; lgl += okp and okl
    return pres, lgl
rd, re = route_stats(enc_diag, CHK_D), route_stats(enc_edge, CHK_E)
print(f"  E2. physical CZ axis pairs (of 4): preserve both local checks / act as the logical controlled phase:  diagonal {rd},  edge {re}")
check("ERRATUM E2: computed here rather than carried from version 0.3: of the four physical controlled-phase axis pairs, ALL four preserve both local checks in both geometries (a diagonal gate commutes with Z-type checks), and the number that implement the logical controlled phase is 4 for diagonal-diagonal and 1 for edge-edge (the other three edge routes touch an idle axis and act as the identity on the code)",
      rd == (4, 4) and re == (4, 1))

# --- E3: exact mean fidelity of a wrong-angle controlled phase
def Fmean(d): return 1 - 0.3 * (1 - math.cos(d))
tot = 0.0; NS = 40000
for _ in range(NS):
    v = vn([rc() for _ in range(4)]); p_ = abs(v[3]) ** 2; d = math.pi - 2.0
    tot += abs(1 - p_ + p_ * complex(math.cos(d), math.sin(d))) ** 2
check(f"ERRATUM E3: the mean fidelity of a controlled phase with angle error d on Haar-random logical inputs is 1 - 0.3 (1 - cos d) (E[p(1-p)] = 3/20 for p = |amplitude of |11>|^2); at phi = 2.0 this is {Fmean(math.pi-2):.4f} (the 0.826 in version 0.7 was a 300-sample estimate); sampled {tot/NS:.4f}",
      abs(Fmean(math.pi - 2) - 0.8248) < 5e-4 and abs(tot / NS - Fmean(math.pi - 2)) < 3e-3)

# =============================================================== 1. the two geometries
print("== 1. the two verification geometries compared ==")
def stats(gens, gf):
    nor = [k for k in ALL if not anti(k, gens)]; lg = [k for k in nor if k not in gf]
    det1 = sum(1 for k in SINGLE if anti(k, gens))
    w2 = [k for k in ALL if weight(k) == 2]; det2 = sum(1 for k in w2 if anti(k, gens))
    byw = {w: sum(1 for k in nor if weight(k) == w) for w in (1, 2, 3, 4)}
    return dict(nor=len(nor), harmless=len(nor) - len(lg), logical=len(lg), det1=det1, det2=det2, n2=len(w2), dist=min(weight(k) for k in lg), invw=byw,
                wts=sorted(weight(e) for e in (LGRP if gens is LG else JGRP)), phot=sorted(photons(e) for e in (LGRP if gens is LG else JGRP)))
SL, SJ = stats(LG, LF), stats(JG, JF)
print("      property                                   local ZZII, IIZZ                joint ZZZZ, XXXX")
print(f"      single-axis faults detected (of 12)        {SL['det1']:<30d}  {SJ['det1']}")
print(f"      weight-2 Pauli faults detected (of {SL['n2']})      {SL['det2']:<30d}  {SJ['det2']}")
print(f"      Paulis commuting with both checks (of 256) {SL['nor']:<30d}  {SJ['nor']}")
print(f"        of which harmless (check products)       {SL['harmless']:<30d}  {SJ['harmless']}")
print(f"        of which undetected logical errors       {SL['logical']:<30d}  {SJ['logical']}")
print(f"      invisible Paulis by weight 1,2,3,4         {[SL['invw'][w] for w in (1,2,3,4)]!s:<30}  {[SJ['invw'][w] for w in (1,2,3,4)]}")
print(f"      check weights (axes) / photons per check   {SL['wts']} / {SL['phot']}                 {SJ['wts']} / {SJ['phot']}")
print(f"      code distance (min weight of a logical op) {SL['dist']:<30d}  {SJ['dist']}")
check("same axes, same number of independent checks, same logical capacity: both codes have 2 independent commuting checks on 4 axes (2 logical qubits) and exactly 64 of 256 Paulis commuting with both checks, 4 of them harmless (identity and check products) and 60 undetected logical errors",
      SL['nor'] == 64 and SJ['nor'] == 64 and SL['harmless'] == 4 and SJ['harmless'] == 4 and SL['logical'] == 60 and SJ['logical'] == 60)
check("what differs is WHICH faults are detected: single-axis 8 of 12 versus 12 of 12 (local misses every Z; joint misses none); code distance 1 versus 2",
      SL['det1'] == 8 and SJ['det1'] == 12 and SL['dist'] == 1 and SJ['dist'] == 2
      and all(not anti((0, 1 << q), LG) for q in range(4)) and all(anti(k, JG) for k in SINGLE))
check("at weight 2 the picture reverses in part: invisible weight-2 faults number 14 for the local code and 18 for the joint code (the joint code has MORE undetected two-axis faults: XX, YY and ZZ on each of the 6 axis pairs; the local code's 14 are the 6 Z-type pairs plus the 8 X/Y-type pairs that sit inside one photon)",
      SL['invw'][2] == 14 and SJ['invw'][2] == 18)
check("check structure: local checks have weight 2 on one photon each; joint checks (and their product) have weight 4 across both photons",
      SL['wts'] == [2, 2, 4] and SL['phot'] == [1, 1, 2] and SJ['wts'] == [4, 4, 4] and SJ['phot'] == [2, 2, 2])
xl = (0b1111, 0)
check("the joint check XXXX is a LOGICAL operator of the local code (it commutes with both local checks and is not a product of them; it is X-bar of photon 1 times X-bar of photon 2): measuring it on locally encoded data would read logical information, so the joint geometry cannot be reached by adding a measurement",
      not anti(xl, LG) and xl not in LF and (0b1111, 0b1111) not in LF)
check("conversely the joint check ZZZZ is already a PRODUCT of the local checks (it is in the local group): the joint geometry keeps ZZZZ and replaces IIZZ's separate role by XXXX",
      (0, 0b1111) in LF)

# =============================================================== 2. conversion
print("== 2. conversion between local and joint geometries ==")
start, target = gkey(LGRP), gkey(JGRP)
dist = {start: 0}; preds = defaultdict(list); frontier = [start]
while frontier and target not in dist:
    nxt = []
    for st in frontier:
        for g in GATES:
            ns = gkey(conj_op(e, g) for e in st)
            if ns not in dist: dist[ns] = dist[st] + 1; nxt.append(ns); preds[ns].append((st, g))
            elif dist[ns] == dist[st] + 1: preds[ns].append((st, g))
    frontier = nxt
dmin = dist[target]
paths = []
def back(st, acc):
    if st == start: paths.append(list(reversed(acc))); return
    for p_, g in preds[st]: back(p_, acc + [g])
back(target, [])
LOGL = [(0b0011, 0, 1), (0, 0b0001, 1), (0b1100, 0, 1), (0, 0b0100, 1)]       # X1 = XXII, Z1 = ZIII, X2 = IIXX, Z2 = IIIZ (local logical operators)
def image(path, ops):
    for g in path: ops = [conj_op(o, g) for o in ops]
    return ops
def wt_mod(op, gf): return min(weight((op[0] ^ f[0], op[1] ^ f[1])) for f in gf)
def path_info(p):
    img = image(p, LOGL)
    return dict(n=len(p), inter=sum(1 for g in p if inter(g)), kinds=sorted(g[0] for g in p), maxw=max(wt_mod(o, JF) for o in img), maxph=max(min(photons((o[0] ^ f[0], o[1] ^ f[1])) for f in JF) for o in img))
infos = [path_info(p) for p in paths]
print(f"  minimum number of elementary gates from the local group to the joint group (gate set H, S, CNOT, CZ on the 4 axes, ASSUMED ideal): {dmin}; number of distinct minimum-length circuits: {len(paths)}")
print(f"  across those circuits: inter-photon gates {min(i['inter'] for i in infos)} to {max(i['inter'] for i in infos)}; largest weight of a logical operator after conversion {min(i['maxw'] for i in infos)} to {max(i['maxw'] for i in infos)}")
rep = min(range(len(paths)), key=lambda i: (infos[i]['inter'], infos[i]['maxw'], i)); P = paths[rep]
print("  example circuit with the fewest inter-photon gates (ties: lowest logical weight):", P, "; gate kinds", infos[rep]['kinds'], "; inter-photon gates", infos[rep]['inter'])
check(f"a unitary conversion exists: the local group maps to the joint group (all signs +1) in {dmin} elementary gates, found by breadth-first search over the signed two-check stabilizer groups on four axes (at most 21,420 exist; the search stops at the first depth that reaches the joint group, so this is the minimum for the gate set)",
      dmin >= 2 and dmin <= 8 and gkey(grp(tuple(image(P, list(LG))))) == target and len(dist) <= 21420)
U = eye(16)
for g in P: U = mm(gmat(g), U)
PJ = mm([[ (1 if i == j else 0) + smat((0, 15, 1))[i][j] for j in range(16)] for i in range(16)], [[ (1 if i == j else 0) + smat((15, 0, 1))[i][j] for j in range(16)] for i in range(16)])
PJ = [[v / 4 for v in r] for r in PJ]
def jbasis(b):
    v = [0j] * 16; v[b] = 1; w = mv(PJ, v); n = math.sqrt(sum(abs(x) ** 2 for x in w)); return [x / n for x in w]
JB = {(0, 0): jbasis(0b0000), (1, 0): jbasis(0b0011), (0, 1): jbasis(0b0101), (1, 1): jbasis(0b0110)}      # joint-code logical basis: Z-bar1 = ZIZI, Z-bar2 = ZZII eigenstates
okc = True; Lbasis = [code_vec(enc_diag, p, q) for p, q in product((0, 1), repeat=2)]
images = [mv(U, b) for b in Lbasis]
for im in images: okc &= all(abs(a - b) < 1e-9 for a, b in zip(mv(PJ, im), im))
gram_ok = all(abs(overlap(images[i], images[j]) - (1 if i == j else 0)) < 1e-9 for i in range(4) for j in range(4))
for _ in range(40):
    a = vn([rc() for _ in range(4)]); psi = [sum(a[i] * Lbasis[i][k] for i in range(4)) for k in range(16)]
    out = mv(U, psi); okc &= abs(expect(out, smat(JG[0])) - 1) < 1e-9 and abs(expect(out, smat(JG[1])) - 1) < 1e-9
    back_ = mv(dag(U), out); okc &= abs(overlap(psi, back_)) > 1 - 1e-9
check("on explicit 16-dimensional state vectors: the conversion maps the four local logical basis states to four orthonormal states inside the joint code space (both joint checks read +1 for any superposition), and the inverse circuit returns arbitrary logical superpositions exactly (amplitudes and relative phases preserved)", okc and gram_ok)
img = image(P, LOGL); okm = True
for o, o2 in zip(LOGL, img): okm &= close(mm(U, mm(smat(o), dag(U))), smat(o2), 1e-9)
print("  logical operators after conversion (X1, Z1, X2, Z2 of the local code), as signed Paulis (x mask, z mask, sign):", img)
check("the induced map on logical operators is a Pauli-to-Pauli map computed by the engine and confirmed by the matrices; each local logical operator becomes a joint-code logical operator of weight >= 2 (the joint code has no weight-1 logical operator)",
      okm and all(wt_mod(o, JF) >= 2 and not anti((o[0], o[1]), JG) for o in img))
# coverage profile along the circuit
print("  coverage profile along the circuit (stabilizer group after each gate): single-axis detected of 12 / check weights / local checks valid / joint checks valid")
prof = []
st = [e for e in LGRP]
def prof_row(st):
    G = set(st); gens = sorted(G); w = sorted(weight((e[0], e[1])) for e in G)
    det = sum(1 for k in SINGLE if any(not commute(k, (e[0], e[1])) for e in G))
    return det, w, all(e in G for e in LGRP), all(e in G for e in JGRP)
prof.append(prof_row(st)); print(f"      step 0  (start)             {prof[-1]}")
for i, g in enumerate(P):
    st = [conj_op(e, g) for e in st]; prof.append(prof_row(st)); print(f"      step {i+1}  after {str(g):18s} {prof[-1]}")
check("the profile is monotone only at its ends: the first state is the local code (8 of 12 single-axis faults detected, local checks valid) and the last is the joint code (12 of 12, joint checks valid); in between the register is in neither code and its coverage is whatever the transported group gives",
      prof[0][0] == 8 and prof[0][2] and prof[-1][0] == 12 and prof[-1][3] and (not prof[0][3]) and (not prof[-1][2]))
# detectability of already-made faults is invariant under conversion
inv_ok = True
for k in ALL:
    if k == (0, 0): continue
    kk = (k[0], k[1], 1)
    for g in P: kk = conj_op(kk, g)
    inv_ok &= anti(k, LG) == anti((kk[0], kk[1]), JG)
check("a fault made BEFORE conversion keeps its detectability: for all 255 nonidentity Paulis, 'detected by a local check' before equals 'detected by a joint check' after (conversion is a unitary, so it changes coverage of FUTURE faults only; the Z faults already made stay invisible)", inv_ok)
# fault propagation through the circuit
print("  single-axis fault inserted before gate k of the circuit and classified by the JOINT checks at the end: detected / logical / harmless; widest final fault (axes, photons)")
fp = []
for k in range(len(P) + 1):
    cnt = defaultdict(int); mw = mp = 0; spread = 0; multi = 0
    for f in SINGLE:
        x, z = f
        for g in P[k:]: x, z, _ = gate_one(x, z, g)
        c = classify((x, z), JG, JF); cnt[c] += 1; mw = max(mw, weight((x, z))); mp = max(mp, photons((x, z)))
        if weight((x, z)) > 1: multi += 1
        if photons((x, z)) == 2 and photons(f) == 1: spread += 1
    fp.append((cnt, mw, mp, multi, spread)); print(f"      k={k}  detected {cnt['detected']:2d}  logical {cnt['logical']:2d}  harmless {cnt['harmless']:2d}   widest ({mw} axes, {mp} photons); single faults that became multi-axis: {multi}; that crossed photons: {spread}")
check("faults made during the conversion circuit can be CORRELATED by it: at least one single-axis fault inserted mid-circuit reaches the end as a multi-axis fault, and at least one crosses from one photon to the other (the propagation is structural: no ancilla is used in the conversion itself)",
      any(f[3] > 0 for f in fp[1:-1]) and any(f[4] > 0 for f in fp[1:-1]))
check("faults made after the conversion are fully covered at single-axis level (12 of 12 detected) and faults made before it keep the local code's coverage (8 detected, 4 invisible Z faults): the coverage a fault gets depends on where in the circuit it occurs",
      fp[-1][0]['detected'] == 12 and fp[0][0]['detected'] == 8 and fp[0][0]['logical'] == 4)

# =============================================================== 3. gate compatibility
print("== 3. gate compatibility ==")
def gens_by(gens, gf):
    out = {}
    for w in (1, 2, 3, 4):
        ks = [k for k in ALL if weight(k) == w and not anti(k, gens)]
        lg = [k for k in ks if k not in gf]
        out[w] = (len(ks), len(lg), sum(1 for k in lg if photons(k) == 1), sum(1 for k in lg if photons(k) == 2))
    return out
GL, GJ = gens_by(LG, LF), gens_by(JG, JF)
print("      rotation generators that leave the checks unchanged, by weight: (all commuting, nontrivial logical, of those on one photon, on two photons)")
for w in (1, 2, 3, 4): print(f"      weight {w}:  local {GL[w]}   joint {GJ[w]}")
check("rotation generators that preserve the checks for any angle: the local code allows 4 single-axis generators (every Z) and the joint code allows NONE of weight 1; the joint code's logical generators start at weight 2 and most of them span both photons",
      GL[1][0] == 4 and GJ[1][0] == 0 and GJ[2][1] > 0 and GJ[2][3] > 0)
def classes(gens, gf):
    nor = [k for k in ALL if not anti(k, gens)]; cl = defaultdict(list)
    for k in nor: cl[min(((k[0] ^ f[0], k[1] ^ f[1]) for f in gf))].append(k)
    return [(wmin, pmin) for cls in cl.values() if (0, 0) not in cls for wmin, pmin in [(min(weight(k) for k in cls), min(photons(k) for k in cls))]]
CLL, CLJ = classes(LG, LF), classes(JG, JF)
print("      the 15 nontrivial logical Pauli operators, cheapest representative of each: (weight, photons) counts")
hl = defaultdict(int); hj = defaultdict(int)
for c in CLL: hl[c] += 1
for c in CLJ: hj[c] += 1
print("      local:", dict(sorted(hl.items())), "  joint:", dict(sorted(hj.items())))
check("the 15 nontrivial logical Pauli operators: the local code has cheapest representatives of weight 1 for 2 operators (Z-bar of each photon) and joint-code representatives all have weight >= 2, with 3 of them inside one photon and 12 spanning both; a joint-code logical rotation therefore needs an interaction among at least 2 axes, where the local code can use 1 axis for the two single-photon logical Z rotations",
      len(CLL) == 15 and len(CLJ) == 15 and min(c[0] for c in CLL) == 1 and min(c[0] for c in CLJ) == 2 and sum(1 for c in CLL if c[0] == 1) == 2 and sum(1 for c in CLJ if c[1] == 1) == 3 and sum(1 for c in CLJ if c[1] == 2) == 12)
# physical routes of the local code applied to joint-encoded data
print("      the four local-code controlled-phase routes applied to jointly encoded data: is the joint group preserved?")
okr = True
for (i, j) in ((0, 2), (0, 3), (1, 2), (1, 3)):
    g = ('CZ', i, j); new = {conj_op(e, g) for e in JGRP}; pres = new == set(JGRP)
    okr &= not pres; print(f"      CZ({i},{j}): joint group preserved = {pres}; transported checks have weights {sorted(weight((e[0], e[1])) for e in new)}")
check("the local code's four physical controlled-phase routes do NOT preserve the joint code: applying them to jointly encoded data changes the joint group (the routes verified in versions 0.3 and 0.7 are specific to the local geometry)", okr)
# gates (<= 4 elementary) that return the joint group to itself
OPS0 = (JG[0], JG[1], (0b0011, 0, 1), (0, 0b0101, 1), (0b0101, 0, 1), (0, 0b0011, 1))      # joint checks and logical X1 = XXII, Z1 = ZIZI, X2 = XIXI, Z2 = ZZII
JSET = set(JGRP); IDMAP = OPS0[2:]
maps = {}; counts = defaultdict(int); total_nodes = [0]; two_seqs = []
def dfs(ops, sq, depth):
    for g in GATES:
        if sq and g == sq[-1] and g[0] in ('H', 'CNOT', 'CZ'): continue
        nops = tuple(conj_op(o, g) for o in ops); total_nodes[0] += 1; nsq = sq + [g]
        if nops[0] in JSET and nops[1] in JSET:
            counts[len(nsq)] += 1; m = nops[2:]
            if len(nsq) == 2: two_seqs.append((nsq, m))
            if m not in maps or len(maps[m]) > len(nsq): maps[m] = nsq
        if depth < 4: dfs(nops, nsq, depth + 1)
dfs(OPS0, [], 1)
single_pres = [g for g in GATES if gkey(conj_op(e, g) for e in JGRP) == gkey(JGRP)]
nonid = {m: s for m, s in maps.items() if m != IDMAP}
print(f"  sequences of up to 4 elementary gates that return the joint group to itself: by length {dict(sorted(counts.items()))}; distinct logical maps reached {len(maps)} (non-identity {len(nonid)}); nodes explored {total_nodes[0]}")
ex = sorted(nonid.values(), key=lambda s: (len(s), str(s)))[:3]
print("   shortest examples:", ex)
LBASIS = [(0b0011, 0), (0, 0b0101), (0b0101, 0), (0, 0b0011)]; LNAMES = ['X1', 'Z1', 'X2', 'Z2']
def lname(op):
    f = (op[0], op[1])
    for combo in product((0, 1), repeat=4):
        fr = (0, 0)
        for c_, b_ in zip(combo, LBASIS):
            if c_: fr = (fr[0] ^ b_[0], fr[1] ^ b_[1])
        if (f[0] ^ fr[0], f[1] ^ fr[1]) in JF:
            nm = [LNAMES[i] for i in range(4) if combo[i]]
            if 'X1' in nm and 'Z1' in nm: nm = ['Y1'] + [n for n in nm if n not in ('X1', 'Z1')]
            if 'X2' in nm and 'Z2' in nm: nm = ['Y2'] + [n for n in nm if n not in ('X2', 'Z2')]
            return ''.join(nm) or 'I'
    return '?'
two = two_seqs
names2 = set()
for sq, m in sorted(two, key=lambda t: str(t[0])):
    nm = tuple(lname(o) for o in m); names2.add(nm)
    print(f"   2-gate sequence {sq}: X1->{nm[0]}, Z1->{nm[1]}, X2->{nm[2]}, Z2->{nm[3]}   (signs {[o[2] for o in m]})")
okcz = True
for sq, m in two:
    Uq = eye(16)
    for g in sq: Uq = mm(gmat(g), Uq)
    pp = [overlap(JB[b], mv(Uq, JB[b])) for b in ((0, 0), (1, 0), (0, 1), (1, 1))]
    leak = max(abs(overlap(JB[b2], mv(Uq, JB[b1]))) for b1 in JB for b2 in JB if b1 != b2)
    okcz &= leak < 1e-9 and all(abs(abs(v) - 1) < 1e-9 and abs(v.imag) < 1e-9 for v in pp) and abs(pp[0] * pp[3] + pp[1] * pp[2]) < 1e-9
check("the shortest code-preserving physical operations on the joint code are PAIRS of physical controlled-phase gates (6 sequences: the three ways to split the four axes into two pairs, in both orders). Every one induces the SAME unsigned logical action X1->X1Z2, Z1->Z1, X2->Z1X2, Z2->Z2, i.e. a logical controlled phase between the two logical qubits (all four signs +1, so exactly the controlled phase, no Pauli frame), confirmed on the state vectors (diagonal phases +-1 with the controlled-phase signature p00 p11 = - p10 p01, no leakage inside the code). In the local code ONE physical controlled phase on one axis pair did that",
      counts[2] == 6 and len(two) == 6 and all(sq[0][0] == 'CZ' and sq[1][0] == 'CZ' for sq, _ in two)
      and names2 == {('X1Z2', 'Z1', 'Z1X2', 'Z2')} and all(o[2] == 1 for _, m in two for o in m) and okcz)
check("no single elementary gate preserves the joint group, so every code-preserving physical operation on the joint code is a sequence (found by exhaustive search up to length 4: the shortest non-identity ones are listed above); the number of distinct logical Cliffords reached within 4 gates is recorded and the identity map is trivially reached",
      len(single_pres) == 0 and len(nonid) > 0 and IDMAP in maps)
# logical controlled phase in the joint code: generators, correctness, zero odd weight at every sub-step
Zb1, Zb2 = (0, 0b0101), (0, 0b0011); Zb12 = (0, 0b0110)
PJ_ = PJ
def jbasis(b):
    v = [0j] * 16; v[b] = 1; w = mv(PJ_, v); n = math.sqrt(sum(abs(x) ** 2 for x in w)); return [x / n for x in w]
JB = {(0, 0): jbasis(0b0000), (1, 0): jbasis(0b0011), (0, 1): jbasis(0b0101), (1, 1): jbasis(0b0110)}
phi = 1.7
macs = [(Zb1, phi / 2), (Zb2, phi / 2), (Zb12, -phi / 2)]
Ucp = eye(16)
for k, th in macs: Ucp = mm(rotmat(k, th), Ucp)
ph = [overlap(JB[b], mv(Ucp, JB[b])) for b in ((0, 0), (1, 0), (0, 1), (1, 1))]
rel = [p_ / ph[0] for p_ in ph]
okcp = abs(abs(ph[0]) - 1) < 1e-9 and near(rel[1].real, 1) and near(rel[2].real, 1) and abs(rel[3] - complex(math.cos(phi), math.sin(phi))) < 1e-9
worst = 0.0
for _ in range(30):
    a = vn([rc() for _ in range(4)]); v = [sum(a[i] * JB[b][k] for i, b in enumerate(((0, 0), (1, 0), (0, 1), (1, 1)))) for k in range(16)]
    for k, th in macs:
        for s in range(1, 6):
            w = mv(rotmat(k, th * s / 5), v)
            worst = max(worst, (1 - expect(w, smat(JG[0])).real) / 2, (1 - expect(w, smat(JG[1])).real) / 2)
check(f"a logical controlled phase of any angle exists in the joint code using only generators that preserve both joint checks (Z-bar1 = ZIZI, Z-bar2 = ZZII, Z-bar1 Z-bar2 = IZZI: weight 2 each; two of the three span both photons): correct on all four logical basis states, and both joint checks stay at odd weight 0 at every sub-step (worst {worst:.1e})",
      okcp and worst < 1e-12 and weight(Zb1) == 2 and photons(Zb1) == 2 and photons(Zb12) == 2)

# =============================================================== 4. phase-fault coverage
print("== 4. phase-fault coverage ==")
def code_states(code):
    if code == 'L': return [code_vec(enc_diag, p, q) for p, q in product((0, 1), repeat=2)]
    return [JB[b] for b in ((0, 0), (1, 0), (0, 1), (1, 1))]
def rnd_code_state(code):
    B = code_states(code); a = vn([rc() for _ in range(4)]); return [sum(a[i] * B[i][k] for i in range(4)) for k in range(16)]
def odd_w(v, gens): return max((1 - expect(v, smat(g)).real) / 2 for g in gens)
# (a) in-code unitaries are invisible, whichever code
worst = {'L': 0.0, 'J': 0.0}
for code, gens, gf in (('L', LG, LF), ('J', JG, JF)):
    nor = [k for k in ALL if k != (0, 0) and not anti(k, gens)]
    for _ in range(25):
        v = rnd_code_state(code)
        for _ in range(6):
            k = random.choice(nor); v = mv(rotmat(k, random.uniform(0.1, 3.0)), v); worst[code] = max(worst[code], odd_w(v, gens))
check(f"THEOREM, tested: any product of rotations about generators that commute with a code's checks leaves the code space invariant, so every check of THAT code passes with probability 1, whatever the angles (worst odd weight over 25 random logical states x 6 random rotations: local {worst['L']:.1e}, joint {worst['J']:.1e}); a wrong angle in such a rotation is therefore a logical error that no stabilizer measurement of that code can see",
      worst['L'] < 1e-12 and worst['J'] < 1e-12)
# (b) wrong-angle controlled phase in the joint code
phi_w = 2.0; fid = []; oddm = 0.0
Uw = eye(16)
for k, th in [(Zb1, phi_w / 2), (Zb2, phi_w / 2), (Zb12, -phi_w / 2)]: Uw = mm(rotmat(k, th), Uw)
Ui = eye(16)
for k, th in [(Zb1, math.pi / 2), (Zb2, math.pi / 2), (Zb12, -math.pi / 2)]: Ui = mm(rotmat(k, th), Ui)
for _ in range(400):
    v = rnd_code_state('J'); w = mv(Uw, v); r = mv(Ui, v); oddm = max(oddm, odd_w(w, JG)); fid.append(abs(overlap(r, w)) ** 2)
check(f"the wrong-angle controlled phase (phi = 2.0 instead of pi) built in the JOINT code passes both joint checks (odd weight {oddm:.1e}) with the same mean fidelity as the local version (sampled {sum(fid)/len(fid):.3f}; exact {Fmean(math.pi-2):.4f}): the joint geometry does not close the relative-phase gap for gates implemented by in-code generators",
      oddm < 1e-12 and abs(sum(fid) / len(fid) - Fmean(math.pi - 2)) < 0.02)
# (c) coherent rotation errors about off-code generators: detection probability and post-selected fidelity
def error_stats(code, gens, key, eps, ns=60):
    pd = []; pf = []; fr = []
    for _ in range(ns):
        v = rnd_code_state(code); w = mv(rotmat(key, eps), v)
        Pm = [[1 if i == j else 0 for j in range(16)] for i in range(16)]
        for g in gens:
            S = smat(g); Pm = mm(Pm, [[(1 if i == j else 0) + S[i][j] for j in range(16)] for i in range(16)]); Pm = [[x / 2 for x in r] for r in Pm]
        wp = mv(Pm, w); pw = sum(abs(x) ** 2 for x in wp); pd.append(1 - pw); fr.append(abs(overlap(v, w)) ** 2)
        pf.append(abs(overlap(v, wp)) ** 2 / pw if pw > 1e-14 else 1.0)
    return sum(pd) / ns, min(pd), max(pd), min(pf), min(fr), sum(fr) / ns
eps = 0.3; kz = (0, 0b0001)
sL = error_stats('L', LG, kz, eps); sJ = error_stats('J', JG, kz, eps)
print(f"  coherent single-axis Z rotation, angle {eps}: local code: P(detected) {sL[0]:.4f} (min {sL[1]:.4f}, max {sL[2]:.4f}), mean fidelity of the unchecked output {sL[5]:.4f}; joint code: P(detected) {sJ[0]:.4f} (min {sJ[1]:.4f}, max {sJ[2]:.4f}), fidelity of the accepted output {sJ[3]:.6f} (sin^2(eps/2) = {math.sin(eps/2)**2:.4f})")
check("a small coherent Z rotation on one axis: the local code never sees it (detection probability 0 for every input state, output fidelity below 1: a logical phase error); the joint code detects it with probability sin^2(eps/2) independent of the state and, given PASS, the accepted output is unchanged (post-selected fidelity 1): the error is projected out",
      sL[2] < 1e-12 and sL[5] < 1 - 1e-4 and abs(sJ[1] - math.sin(eps / 2) ** 2) < 1e-9 and abs(sJ[2] - math.sin(eps / 2) ** 2) < 1e-9 and sJ[3] > 1 - 1e-9)
kx = (0b0001, 0); sLx = error_stats('L', LG, kx, eps); sJx = error_stats('J', JG, kx, eps)
check("a small coherent X rotation on one axis is detected the same way by both codes (probability sin^2(eps/2), state-independent, accepted output unchanged): the joint code adds coverage of Z-type noise and does not change X-type coverage",
      abs(sLx[1] - math.sin(eps / 2) ** 2) < 1e-9 and abs(sJx[1] - math.sin(eps / 2) ** 2) < 1e-9 and sLx[3] > 1 - 1e-9 and sJx[3] > 1 - 1e-9)
# (d) classification of all weight-1 and weight-2 rotation generators
gen = [k for k in ALL if weight(k) in (1, 2)]
cls = defaultdict(int)
for k in gen: cls[(not anti(k, LG), not anti(k, JG))] += 1
print(f"  coherent-rotation generators of weight 1 or 2 ({len(gen)}): visible to both {cls[(False, False)]}, visible only to the joint code {cls[(True, False)]}, visible only to the local code {cls[(False, True)]}, invisible to both {cls[(True, True)]}")
check("classification of the 66 generators of weight 1 or 2 as coherent error sources: some are visible only to the joint code (the Z-type ones), some only to the local code, some to both, some to neither; the joint code is not a superset of the local code's coverage",
      cls[(True, False)] > 0 and cls[(False, True)] > 0 and cls[(False, False)] > 0 and cls[(True, True)] > 0 and sum(cls.values()) == 66)
lonly = {k for k in gen if anti(k, LG) and not anti(k, JG)}
jonly = {k for k in gen if anti(k, JG) and not anti(k, LG)}
bothinv = {k for k in gen if not anti(k, LG) and not anti(k, JG)}
cross = [(i, j) for i in (0, 1) for j in (2, 3)]; within = [(0, 1), (2, 3)]; allp = [(i, j) for i in range(4) for j in range(i + 1, 4)]
m_ = lambda i, j: (1 << i) | (1 << j)
exp_l = {(m_(i, j), 0) for i, j in cross} | {(m_(i, j), m_(i, j)) for i, j in cross}
exp_j = {(0, 1 << q) for q in range(4)} | {(m_(i, j), 1 << i) for i, j in within} | {(m_(i, j), 1 << j) for i, j in within}
exp_b = {(0, m_(i, j)) for i, j in allp} | {(m_(i, j), 0) for i, j in within} | {(m_(i, j), m_(i, j)) for i, j in within}
check("which generators only one code sees, identified exactly: visible only to the LOCAL code are the 8 cross-photon XX and YY couplings; visible only to the JOINT code are the 4 single-axis Z rotations and the 4 same-photon XY and YX couplings; invisible to both are the 6 ZZ couplings on any axis pair and the 4 same-photon XX and YY couplings",
      lonly == exp_l and jonly == exp_j and bothinv == exp_b)
xt = (0, 0b0101)
check("crosstalk-type error: a ZZ rotation between one axis of each photon (Z_a1 Z_a2) commutes with all checks of both codes, so it is invisible to both (in the local code it is a logical ZZ-type rotation, in the joint code it is Z-bar1)",
      not anti(xt, LG) and not anti(xt, JG) and xt not in LF and xt not in JF)
print("  summary: errors that leave the code are exposed by that code's checks (with state-independent probability for a single rotation); errors that stay inside the code, including a wrong ANGLE of an intended in-code rotation, are invisible to every stabilizer measurement of that code")

# =============================================================== 5. extraction resources and correlated errors
print("== 5. extraction resources and errors created by the verifier ==")
def extract_faults(kind, axes):
    """Single ancilla Pauli faults during ancilla-based extraction of a weight-n check (ancilla = qubit 4, no flags, ideal data).
    kind 'Z': ancilla |0>, CNOT(d -> anc) in order, measured in Z. kind 'X': ancilla |+>, CNOT(anc -> d), measured in X.
    Returns a list of (slot, fault, data error frame, report flipped)."""
    out = []; n = len(axes)
    gates = [('CNOT', d, 4) if kind == 'Z' else ('CNOT', 4, d) for d in axes]
    for slot in range(n + 1):
        for name, (fx, fz) in (('X', (1, 0)), ('Y', (1, 1)), ('Z', (0, 1))):
            x, z = fx << 4, fz << 4
            for g in gates[slot:]: x, z, _ = gate_one(x, z, g)
            flip = bool((x >> 4) & 1) if kind == 'Z' else bool((z >> 4) & 1)
            out.append((slot, name, (x & 15, z & 15), flip))
    return out
def hook_stats(gens, gf, kind, axes):
    rows = extract_faults(kind, axes); c = defaultdict(int)
    for slot, name, E, flip in rows:
        if E == (0, 0): c['no data error'] += 1; continue
        cl = classify(E, gens, gf)
        c[cl] += 1
        if cl == 'logical': c['silent logical, report ' + ('flipped' if flip else 'NOT flipped')] += 1
        if cl in ('logical', 'detected') and not flip: c['damaged data, report NOT flipped'] += 1
        if weight(E) >= 2: c['weight>=2 data error'] += 1
    return len(rows), dict(c)
L1 = hook_stats(LG, LF, 'Z', [0, 1]); L2 = hook_stats(LG, LF, 'Z', [2, 3])
J1 = hook_stats(JG, JF, 'Z', [0, 1, 2, 3]); J2 = hook_stats(JG, JF, 'X', [0, 1, 2, 3])
print("  fault locations x Pauli types for single ancilla faults, with the data error each leaves (classified by the code's own checks):")
print("      local ZZII (2 CNOTs):", L1); print("      local IIZZ (2 CNOTs):", L2)
print("      joint ZZZZ (4 CNOTs):", J1); print("      joint XXXX (4 CNOTs):", J2)
silent = lambda s: s[1].get('silent logical, report NOT flipped', 0)
check("resources per round, kept separate: local extraction uses 2 CNOTs per check and 4 in total, each check engaging one photon; joint extraction uses 4 CNOTs per check and 8 in total, each check engaging both photons at once (a structural statement, not a cost)",
      len(extract_faults('Z', [0, 1])) == 9 and len(extract_faults('Z', [0, 1, 2, 3])) == 15)
dmg = lambda s_: s_[1].get('damaged data, report NOT flipped', 0)
w2 = lambda s_: s_[1].get('weight>=2 data error', 0)
print(f"  totals over each code's two checks: fault locations x types {L1[0]+L2[0]} versus {J1[0]+J2[0]}; data errors of weight >= 2: {w2(L1)+w2(L2)} versus {w2(J1)+w2(J2)}; silent logical (undetected by the code): {L1[1].get('logical',0)+L2[1].get('logical',0)} versus {J1[1].get('logical',0)+J2[1].get('logical',0)}; of those with an unflipped report {silent(L1)+silent(L2)} versus {silent(J1)+silent(J2)}; damaged data (silent or caught later) with an unflipped report {dmg(L1)+dmg(L2)} versus {dmg(J1)+dmg(J2)}")
check("single ancilla faults in the joint extraction create more multi-axis data errors (12 versus 4) over more fault locations (30 versus 18), but the number that stay SILENT is the same (4 logical cases in each code, 2 of them with an unflipped report); the extra damage of the joint extraction is of the kind the joint checks catch in a later round. Correlation rises; undetected damage per fault location does not",
      w2(L1) + w2(L2) == 4 and w2(J1) + w2(J2) == 12 and L1[0] + L2[0] == 18 and J1[0] + J2[0] == 30
      and L1[1].get('logical', 0) + L2[1].get('logical', 0) == 4 and J1[1].get('logical', 0) + J2[1].get('logical', 0) == 4 and silent(L1) + silent(L2) == 2 and silent(J1) + silent(J2) == 2)
check("damaged data that the report does NOT flag is more common in the joint extraction (counted above): the joint round can say PASS while leaving a data error that the next joint round will flag",
      dmg(J1) + dmg(J2) > dmg(L1) + dmg(L2))
mins = []
for kind in ('Z', 'X'):
    best = min(permutations(range(4)), key=lambda o: silent(hook_stats(JG, JF, kind, list(o))))
    vals = [silent(hook_stats(JG, JF, kind, list(o))) for o in permutations(range(4))]; mins.append((min(vals), max(vals)))
print(f"  silent logical damage with unflipped report, over all 24 CNOT orders of each joint check: ZZZZ {mins[0]}, XXXX {mins[1]} (min, max)")
check("reordering the four CNOTs does not remove the joint extraction's silent logical damage (the minimum over all 24 orders is still above zero for both checks): a weight-2 hook error is a logical operator of the joint code whatever the order. No flag or verified-ancilla protocol is studied here",
      mins[0][0] > 0 and mins[1][0] > 0)

# =============================================================== 6. adaptive selection
print("== 6. adaptive selection ==")
def wht(a):
    a = list(a); n = len(a); h = 1
    while h < n:
        for i in range(0, n, 2 * h):
            for j in range(i, i + h): u, v = a[j], a[j + h]; a[j], a[j + h] = u + v, u - v
        h *= 2
    return a
def iwht(a): return [v / len(a) for v in wht(a)]
def noise1(x, z, axes=(0, 1, 2, 3)):
    d = [0.0] * 256; msk = sum(1 << q for q in axes)
    for xp in range(16):
        if xp & ~msk: continue
        px = 1.0
        for q in axes: px *= x if (xp >> q) & 1 else 1 - x
        for zp in range(16):
            if zp & ~msk: continue
            pz = 1.0
            for q in axes: pz *= z if (zp >> q) & 1 else 1 - z
            d[xp | (zp << 4)] = px * pz
    return d
def power(d, m): return iwht([v ** m for v in wht(d)])
def conv(a, b): return iwht([u * v for u, v in zip(wht(a), wht(b))])
def evaluate(dist, gens, gf):
    c = w = r = 0.0
    for idx, p_ in enumerate(dist):
        f = (idx & 15, idx >> 4)
        if anti(f, gens): r += p_
        elif f in gf: c += p_
        else: w += p_
    return c, w, r
def reject(dist, gens):
    new = [0.0] * 256; rej = 0.0
    for idx, p_ in enumerate(dist):
        if anti((idx & 15, idx >> 4), gens): rej += p_
        else: new[idx] = p_
    return new, rej
def cmap(dist, g):
    new = [0.0] * 256
    for idx, p_ in enumerate(dist):
        if p_ == 0.0: continue
        x, z, _ = gate_one(idx & 15, idx >> 4, g); new[x | (z << 4)] += p_
    return new
d0 = [0.0] * 256; d0[0] = 1.0
# single-checkpoint exact enumeration
print("  one checkpoint after one block, independent X and Z faults with probabilities x, z on each of the four axes (ASSUMED), ideal check")
print("      x          z         local: accepted-correct  accepted-wrong  rejected     joint: accepted-correct  accepted-wrong  rejected")
rows6 = {}
for x, z in ((1e-3, 0.0), (1e-3, 1e-5), (1e-3, 1e-4), (1e-3, 1e-3), (1e-3, 1e-2), (1e-2, 1e-3), (0.0, 1e-3)):
    dn = noise1(x, z); a = evaluate(dn, LG, LF); b = evaluate(dn, JG, JF); rows6[(x, z)] = (a, b)
    print(f"      {x:8.0e}  {z:8.0e}        {a[0]:.6f}          {a[1]:.2e}       {a[2]:.2e}         {b[0]:.6f}          {b[1]:.2e}       {b[2]:.2e}")
check("exact enumeration sums to 1 for both codes at every setting", all(near(sum(a), 1.0, 1e-12) and near(sum(b), 1.0, 1e-12) for a, b in rows6.values()))
dn = noise1(1e-4, 0.0); a = evaluate(dn, LG, LF); b = evaluate(dn, JG, JF)
check("X-type noise only: the joint code accepts about 3 times as many wrong outputs as the local code (6 invisible pair faults versus 2, at leading order x^2) and rejects the same share to first order (4x); with no Z noise the local code has the lower accepted-wrong at equal rejection",
      abs(b[1] / a[1] - 3.0) < 0.05 and abs(b[2] / a[2] - 1.0) < 2e-3)
dn = noise1(0.0, 1e-4); a = evaluate(dn, LG, LF); b = evaluate(dn, JG, JF)
check("Z-type noise only: to first order the local code's accepted-wrong share equals 4z (every single Z fault is silent) and the joint code converts exactly that into rejection: its rejected share is 4z and its accepted-wrong share is O(z^2). Silent damage becomes identifiable discard, one for one at first order",
      abs(a[1] / 4e-4 - 1) < 0.01 and abs(b[2] / 4e-4 - 1) < 0.01 and b[1] < 1e-6 and a[2] < 1e-12)
def breakeven(x):
    lo, hi = 1e-12, 0.1
    for _ in range(200):
        mid = math.sqrt(lo * hi); dn = noise1(x, mid)
        if evaluate(dn, LG, LF)[1] > evaluate(dn, JG, JF)[1]: hi = mid
        else: lo = mid
    return hi
be = {x: breakeven(x) for x in (1e-4, 1e-3, 1e-2)}
print("  Z-noise level z* above which the joint code accepts fewer wrong outputs than the local code, for X noise x:", {k: f"{v:.2e}" for k, v in be.items()}, "(compare x^2:", {k: f"{k*k:.2e}" for k in be}, ")")
check("the break-even Z-noise level on accepted-wrong is of order x^2 (z* / x^2 within a factor of 2 of 1 at x = 1e-4, 1e-3, 1e-2): above it the joint code accepts fewer wrong outputs, but it rejects more; both numbers are reported, none is combined",
      all(0.5 < be[x] / (x * x) < 2.0 for x in be))
# two-phase workload with conversion
Pd = P; Prev = list(reversed(P))
def policy(codeA, codeB, conv_path, r, m1, ph1, m2, ph2):
    dist = conv(d0, power(noise1(*ph1), m1))
    gA = (LG, LF) if codeA == 'L' else (JG, JF); gB = (LG, LF) if codeB == 'L' else (JG, JF)
    dist, rej1 = reject(dist, gA[0])
    for g in conv_path:
        dist = cmap(dist, g)
        if r > 0: dist = conv(dist, noise1(r, r, tuple(sorted(set(g[1:])))))
    dist = conv(dist, power(noise1(*ph2), m2))
    c, w, rj = evaluate(dist, gB[0], gB[1]); return c, w, rj + rej1
m1 = m2 = 50
PROFILES = {"X-dominated, then Z-heavy": ((5e-4, 1e-5), (1e-4, 5e-4), 'LJ'), "Z-heavy, then X-dominated": ((1e-4, 5e-4), (5e-4, 1e-5), 'JL'), "strongly X-dominated, then Z-heavy": ((2e-3, 0.0), (1e-4, 5e-4), 'LJ')}
print(f"  two blocks of {m1} segments each (ASSUMED noise per axis per segment, X and Z flip probabilities); a check at the end of each block (ideal extraction); conversion circuit faults: X and Z flips with probability r on each axis a gate touches")
tab = {}
for pname, (p1, p2, direction) in PROFILES.items():
    print(f"   profile: {pname}   block 1 (x, z) = {p1}, block 2 (x, z) = {p2}")
    print("      policy                      r        accepted-correct  accepted-wrong  rejected")
    for pol in ('fixed local', 'fixed joint', 'adaptive'):
        for r in ((0.0,) if pol != 'adaptive' else (0.0, 2e-4, 1e-3, 3e-3)):
            if pol == 'fixed local': res = policy('L', 'L', [], 0, m1, p1, m2, p2)
            elif pol == 'fixed joint': res = policy('J', 'J', [], 0, m1, p1, m2, p2)
            elif direction == 'LJ': res = policy('L', 'J', Pd, r, m1, p1, m2, p2)
            else: res = policy('J', 'L', Prev, r, m1, p1, m2, p2)
            tab[(pname, pol, r)] = res
            print(f"      {pol:26s}  {r:7.0e}   {res[0]:.6f}         {res[1]:.2e}       {res[2]:.4f}")
okp = all(near(sum(v), 1.0, 1e-9) for v in tab.values())
check("every policy's three outcome probabilities (accepted-correct, accepted-wrong, rejected) sum to 1 in all workload profiles", okp)
def adaptive_at(pname, r):
    p1, p2, direction = PROFILES[pname]
    return policy('L', 'J', Pd, r, m1, p1, m2, p2) if direction == 'LJ' else policy('J', 'L', Prev, r, m1, p1, m2, p2)
def bisect_r(pname, key):
    ref = tab[(pname, 'fixed joint', 0.0)]
    if adaptive_at(pname, 0.0)[key] >= ref[key]: return None
    lo, hi = 0.0, 0.1
    if adaptive_at(pname, hi)[key] < ref[key]: return None
    for _ in range(60):
        mid = (lo + hi) / 2
        if adaptive_at(pname, mid)[key] < ref[key]: lo = mid
        else: hi = mid
    return lo
for pname in PROFILES:
    fl, fj, a0 = tab[(pname, 'fixed local', 0.0)], tab[(pname, 'fixed joint', 0.0)], tab[(pname, 'adaptive', 0.0)]
    rw = bisect_r(pname, 1)
    print(f"  {pname}: ideal conversion: accepted-wrong adaptive {a0[1]:.2e} / fixed local {fl[1]:.2e} / fixed joint {fj[1]:.2e}; rejected {a0[2]:.4f} / {fl[2]:.4f} / {fj[2]:.4f}; conversion fault probability at which adaptive's accepted-wrong equals the fixed joint policy's: {('%.1e' % rw) if rw else 'none in range'}")
pn1, pn2, pn3 = list(PROFILES)
for pn in (pn1, pn3):
    a0, fl, fj = tab[(pn, 'adaptive', 0.0)], tab[(pn, 'fixed local', 0.0)], tab[(pn, 'fixed joint', 0.0)]
    check(f"profile '{pn}', ideal conversion: the adaptive policy accepts fewer wrong outputs than both fixed policies; compared with the fixed joint policy the gain in accepted-wrong is {100*(1-a0[1]/fj[1]):.1f}% and the change in rejected share is {a0[2]-fj[2]:+.4f} (printed, not combined)",
          a0[1] < fl[1] and a0[1] < fj[1])
check("the benefit over simply staying in the joint code is small in the base profile and is lost at a conversion-circuit fault probability of order 1e-4 to 1e-3 per gate axis (printed break-even), while the benefit over staying local comes from the joint code itself (silent Z damage turned into rejection), not from switching",
      bisect_r(pn1, 1) is not None and 5e-5 < bisect_r(pn1, 1) < 2e-3 and tab[(pn1, 'adaptive', 1e-3)][1] > tab[(pn1, 'fixed joint', 0.0)][1])
check("the benefit of switching depends on the workload: in the strongly X-dominated profile the adaptive policy's accepted-wrong is far below the fixed joint policy's and the conversion-fault probability at which that advantage disappears is above 5e-3 (versus about 2e-4 and 8e-5 in the other two profiles); its rejected share stays higher than the fixed joint policy's throughout, so this is a trade of silent damage for discard and not a free gain",
      bisect_r(pn3, 1) is not None and bisect_r(pn3, 1) > 5e-3 and all(tab[(pn3, 'adaptive', r_)][2] > tab[(pn3, 'fixed joint', 0.0)][2] for r_ in (0.0, 2e-4, 1e-3, 3e-3)))
check("conversion has a price in every profile: raising the conversion-circuit fault probability r never lowers the adaptive policy's total of rejected plus accepted-wrong in the printed range",
      all(all(tab[(pn, 'adaptive', r2)][2] + tab[(pn, 'adaptive', r2)][1] >= tab[(pn, 'adaptive', r1)][2] + tab[(pn, 'adaptive', r1)][1] - 1e-15 for r1, r2 in ((0.0, 2e-4), (2e-4, 1e-3), (1e-3, 3e-3))) for pn in PROFILES))
a0b, flb, fjb = tab[(pn2, 'adaptive', 0.0)], tab[(pn2, 'fixed local', 0.0)], tab[(pn2, 'fixed joint', 0.0)]
check("profile 2 (Z-heavy, then X-dominated), ideal conversion back to the local code: the adaptive policy accepts fewer wrong outputs than the fixed local policy; the comparison with the fixed joint policy is printed and not used to claim a win",
      a0b[1] < flb[1])

print()
bad = [n for n, ok_ in results if not ok_]
print("ALL PASS" if not bad else "FAILURES: " + "; ".join(bad))
raise SystemExit(0 if not bad else 1)
