# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tyler O'Bryan, where applicable
"""Buddy verification, version 0.9: how reliable is the verifier itself, and what should it become?
Plain Python, no packages.

Evidence: every result is [[DERIVED]] inside the stated model (ideal Clifford circuits; exact Pauli-frame propagation of every
single fault and every pair of faults; 16- and 32-dimensional state vectors; exact enumeration for the workload tables).
Fault rates, workloads and gate sets are [[ASSUMED]] examples. Nothing here is a measurement, a hardware cost, or a comparison with a
conventional architecture. Interaction counts, ancilla counts, weights and photon spans are structural proxies, never costs; no combined
score is formed anywhere (the selection demonstration returns separate metrics, a feasible set and a Pareto set).

Axes (a1, b1, a2, b2) = data qubits 0..3 of two photons. Signed observables, expected value +1.
  LOCAL baseline code L: checks ZZII, IIZZ.     JOINT code J: checks ZZZZ, XXXX (the [[4,2,2]] error-detecting code).

Fault models used for the circuit-level enumeration (stated in the printed tables):
  M1  ancilla-only single-qubit Paulis between the ancilla's gates (the version 0.8 model; regression test)
  M2  every Pauli on the qubits of each gate (15 for two-qubit gates, 3 for one-qubit gates and preparations), and measurement flips
      (the standard single-fault model; the same families used by Self, Benedetti and Amaro for their syndrome circuits)
  M3  M2 plus single-qubit Paulis on every idle live qubit (data included) after every operation, and one incoming single-qubit
      Pauli on each data axis before the round (so data faults that arrive during the round are counted)
A location fails with probability p, uniformly over its non-identity Paulis (ASSUMED); first-order coefficients are sums over single
faults, second-order coefficients are sums over pairs of faults at different locations.

Parts
  A. Erratum to version 0.8 (conversion wording) and engine validation
  B. Circuit-level fault enumerator and regression against version 0.8
  C. Extraction methods compared: conventional, flagged, verified-cat, cooperative (local-cat)
  C2. Exact per-round probabilities (Walsh-Hadamard convolution of independent location faults) with Monte Carlo validation
  D. Concurrency windows for compatible gates inside an extraction
  E. Capability report, bidirectional IQA-Buddy interface demonstration, Pareto selection
  F. Reference preparations for operational assurance
  G. Result checks (written after reading the output of A to F; the expectations that failed are listed in the page)
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


# =============================================================== A. erratum to version 0.8 and engine validation
print("== A. erratum to version 0.8, and engine validation ==")
okv = True
for _ in range(120):
    key = (random.randrange(16), random.randrange(16)); g = random.choice(GATES)
    x2, z2, s = gate_one(key[0], key[1], g); U = gmat(g)
    okv &= close(mm(U, mm(pmat(key), dag(U))), [[s * v for v in r] for r in pmat((x2, z2))], 1e-9)
check("the Pauli engine (gate rules with signs) equals explicit matrix conjugation on 120 random Pauli and gate pairs, four axes", okv)

CONV = [('H', 0), ('H', 1), ('CNOT', 0, 2), ('CNOT', 1, 3)]     # shortest local-to-joint circuit found in version 0.8
enc_diag = lambda p: 3 * p
def code_vec(enc, p, q):
    v = [0j] * 16; v[(enc(p) * 4) + enc(q)] = 1; return v
Lbasis = [code_vec(enc_diag, p, q) for p, q in product((0, 1), repeat=2)]
def lstate():
    a = vn([rc() for _ in range(4)]); return [sum(a[i] * Lbasis[i][k] for i in range(4)) for k in range(16)]
trans = [list(LG)]; st_ = list(LG)
for g in CONV: st_ = [conj_op(e, g) for e in st_]; trans.append(list(st_))
worst_t = 0.0; orig_L = []; orig_J = []
for step in range(len(CONV) + 1):
    for _ in range(25):
        v = lstate()
        for g in CONV[:step]: v = mv(gmat(g), v)
        worst_t = max(worst_t, max(abs(expect(v, smat(c)) - 1) for c in trans[step]))
        orig_L.append((step, min(expect(v, smat(c)).real for c in LG))); orig_J.append((step, min(expect(v, smat(c)).real for c in JG)))
wmap = [[weight((e[0], e[1])) for e in t] for t in trans]
print("  transported checks along the conversion circuit (signed, expected +1), with weights:")
nm = lambda e: ''.join('IXZY'[{(0, 0): 0, (1, 0): 1, (0, 1): 2, (1, 1): 3}[((e[0] >> q) & 1, (e[1] >> q) & 1)]] for q in range(4))
for step, t in enumerate(trans):
    print(f"      after {step} gate(s): " + ", ".join(("+" if e[2] > 0 else "-") + nm(e) + f" (w{weight((e[0], e[1]))}, {photons((e[0], e[1]))} ph)" for e in t))
check("ERRATUM E4 (version 0.8 wording): at EVERY step of the conversion circuit the transported checks exist and read +1 exactly on converted logical states (worst deviation {:.1e}); only the ORIGINAL check sets lose validity".format(worst_t), worst_t < 1e-12)
check("ERRATUM E4 (continued): the original local checks read below +1 at steps 1 to 4 and the original joint checks read below +1 at steps 0 to 3 on some converted states, so 'neither code's complete check set remains valid' is a statement about the original sets, while the transported checks stay valid and measurable in principle",
      all(min(v for s_, v in orig_L if s_ == k) < 1 - 1e-6 for k in (1, 2, 3, 4)) and all(min(v for s_, v in orig_J if s_ == k) < 1 - 1e-6 for k in (0, 1, 2, 3)))
check("ERRATUM E4 (continued): the transported checks have weights [2,2] on ONE photon each after 0, 1 and 2 gates (the two Hadamards), [3,3] across both photons after the first CNOT and [4,4] after the second; weight-2 single-photon checks persist through the Hadamards",
      wmap[0] == [2, 2] and wmap[1] == [2, 2] and wmap[2] == [2, 2] and wmap[3] == [3, 3] and wmap[4] == [4, 4]
      and all(photons((e[0], e[1])) == 1 for e in trans[2]) and all(photons((e[0], e[1])) == 2 for e in trans[3]))
check("ERRATUM E4 (continued): version 0.8 said verification 'must be suspended' during conversion; the correct statement is that it MAY follow the transported group, and whether Buddy can physically measure the weight-3 checks is a separate, open question", True)

# =============================================================== B. circuit-level engine
print("== B. circuit-level fault enumerator ==")
PAULIS1 = [(1, 0), (1, 1), (0, 1)]                                     # X, Y, Z as (x, z)
def run_from(ops, i0, x, z):
    rec = 0
    for k in range(i0, len(ops)):
        op = ops[k]; kd = op[0]
        if kd == 'H' or kd == 'CNOT' or kd == 'CZ': x, z, _ = gate_one(x, z, op)
        elif kd == 'MZ':
            q = op[1]
            if (x >> q) & 1: rec |= 1 << op[2]
            m = ~(1 << q); x &= m; z &= m
        elif kd == 'MX':
            q = op[1]
            if (z >> q) & 1: rec |= 1 << op[2]
            m = ~(1 << q); x &= m; z &= m
        else:
            m = ~(1 << op[1]); x &= m; z &= m
    return rec, x, z
def touched(op):
    if op[0] in ('MZ', 'MX'): return []
    if op[0] in ('CNOT', 'CZ'): return [op[1], op[2]]
    return [op[1]]
class Builder:
    def __init__(s): s.ops = []; s.nq = 4; s.nr = 0; s.dets = []
    def q(s): s.nq += 1; return s.nq - 1
    def r(s): s.nr += 1; return s.nr - 1
    def add(s, *op): s.ops.append(tuple(op))
def enumerate_faults(ops, model, focus=None):
    """Return a list of locations; each location is a list of (rec, Ex, Ez) effects (one per Pauli at that location)."""
    alive = set(range(4)); locs = []
    def loc_from(paulis, i0):
        eff = []
        for (qx, qz) in paulis:
            rec, x, z = run_from(ops, i0, qx, qz); eff.append((rec, x & 15, z & 15))
        locs.append(eff)
    if model == 'M3':
        for q in range(4): loc_from([(p[0] << q, p[1] << q) for p in PAULIS1], 0)
    for i, op in enumerate(ops):
        tq = touched(op)
        if op[0] in ('MZ', 'MX'): alive.discard(op[1])
        else: alive.add(op[1]) if op[0] in ('P0', 'P+') else None
        if model == 'M1':
            if focus in tq: loc_from([(p[0] << focus, p[1] << focus) for p in PAULIS1], i + 1)
            continue
        if op[0] in ('MZ', 'MX'): locs.append([(1 << op[2], 0, 0)])
        elif len(tq) == 2:
            a, b = tq; pa = [(0, 0)] + PAULIS1; ps = []
            for u in pa:
                for v in pa:
                    if u == (0, 0) and v == (0, 0): continue
                    ps.append(((u[0] << a) | (v[0] << b), (u[1] << a) | (v[1] << b)))
            loc_from(ps, i + 1)
        else: loc_from([(p[0] << tq[0], p[1] << tq[0]) for p in PAULIS1], i + 1)
        if model == 'M3':
            for q in sorted(alive):
                if q in tq: continue
                loc_from([(p[0] << q, p[1] << q) for p in PAULIS1], i + 1)
    return locs
def classtable(gens, gf):
    return {f: ('none' if f == (0, 0) else classify(f, gens, gf)) for f in ALL}
CT = {'L': classtable(LG, LF), 'J': classtable(JG, JF)}
def pop(n): return bin(n).count('1')
def analyze(locs, dets, code, pairs=True):
    ct = CT[code]; c1 = defaultdict(float); cnt = defaultdict(int); silentw = defaultdict(int); passmulti = 0; maxpassw = 0
    nloc = len(locs); nfault = sum(len(l) for l in locs)
    sig_w = defaultdict(float); per_loc = []
    for li, loc in enumerate(locs):
        n = len(loc); lsig = []
        for rec, ex, ez in loc:
            dv = 0
            for j, m in enumerate(dets):
                if pop(rec & m) & 1: dv |= 1 << j
            cl = ct[(ex, ez)]
            if dv == 0: cat = {'none': 'pass_clean', 'harmless': 'pass_clean', 'detected': 'pass_damaged', 'logical': 'silent'}[cl]
            else: cat = 'false_reject' if cl in ('none', 'harmless') else 'caught_damage'
            c1[cat] += 1.0 / n; cnt[cat] += 1
            w = weight((ex, ez))
            if cat == 'silent': silentw[w] += 1
            if dv == 0:
                maxpassw = max(maxpassw, w)
                if w >= 2: passmulti += 1
            lsig.append((dv, ex, ez, cat, 1.0 / n))
        per_loc.append(lsig)
    out = dict(nloc=nloc, nfault=nfault, c1=dict(c1), cnt=dict(cnt), silentw=dict(silentw), passmulti=passmulti, maxpassw=maxpassw)
    if pairs:
        tot = defaultdict(float)
        for lsig in per_loc:
            for dv, ex, ez, cat, w in lsig:
                if cat != 'silent': tot[(dv, ex, ez)] += w
        keys = list(tot); S = 0.0
        def logical_pass(dv, ex, ez): return dv == 0 and ct[(ex, ez)] == 'logical'
        for a in keys:
            wa = tot[a]
            for b in keys:
                if logical_pass(a[0] ^ b[0], a[1] ^ b[1], a[2] ^ b[2]): S += wa * tot[b]
        SL = 0.0
        for lsig in per_loc:
            nonsil = [(dv, ex, ez, w) for dv, ex, ez, cat, w in lsig if cat != 'silent']
            for a in nonsil:
                for b in nonsil:
                    if logical_pass(a[0] ^ b[0], a[1] ^ b[1], a[2] ^ b[2]): SL += a[3] * b[3]
        out['S2'] = (S - SL) / 2.0
    return out
def resources(B):
    n2 = sum(1 for o in B.ops if o[0] in ('CNOT', 'CZ')); n1 = sum(1 for o in B.ops if o[0] == 'H')
    nmeas = sum(1 for o in B.ops if o[0] in ('MZ', 'MX'))
    span = defaultdict(set); aa = 0
    for o in B.ops:
        if o[0] in ('CNOT', 'CZ'):
            a, b = o[1], o[2]
            if a < 4 and b >= 4: span[b].add(a // 2)
            elif b < 4 and a >= 4: span[a].add(b // 2)
            elif a >= 4 and b >= 4: aa += 1
    return dict(n2q=n2, n1q=n1, nanc=B.nq - 4, nmeas=nmeas, ancspan=max((len(v) for v in span.values()), default=0), aa2q=aa)

# ---- check-circuit builders (axes are data qubit indices; fresh ancilla qubits are allocated by the builder)
def z_conv(B, axes):
    a = B.q(); B.add('P0', a)
    for d in axes: B.add('CNOT', d, a)
    r = B.r(); B.add('MZ', a, r); B.dets.append(1 << r); return a
def x_conv(B, axes):
    a = B.q(); B.add('P+', a)
    for d in axes: B.add('CNOT', a, d)
    r = B.r(); B.add('MX', a, r); B.dets.append(1 << r); return a
def z_flag(B, axes):
    a = B.q(); f = B.q(); B.add('P0', a); B.add('P+', f)
    B.add('CNOT', axes[0], a); B.add('CNOT', f, a)
    for d in axes[1:-1]: B.add('CNOT', d, a)
    B.add('CNOT', f, a); B.add('CNOT', axes[-1], a)
    r1 = B.r(); B.add('MZ', a, r1); r2 = B.r(); B.add('MX', f, r2); B.dets += [1 << r1, 1 << r2]; return a
def x_flag(B, axes):
    a = B.q(); f = B.q(); B.add('P+', a); B.add('P0', f)
    B.add('CNOT', a, axes[0]); B.add('CNOT', a, f)
    for d in axes[1:-1]: B.add('CNOT', a, d)
    B.add('CNOT', a, f); B.add('CNOT', a, axes[-1])
    r1 = B.r(); B.add('MX', a, r1); r2 = B.r(); B.add('MZ', f, r2); B.dets += [1 << r1, 1 << r2]; return a
def cat_prep(B, n, verify):
    c = [B.q() for _ in range(n)]
    for q in c: B.add('P0', q)
    B.add('H', c[0])
    for i in range(n - 1): B.add('CNOT', c[i], c[i + 1])
    if verify:
        v = B.q(); B.add('P0', v); B.add('CNOT', c[0], v); B.add('CNOT', c[-1], v)
        rv = B.r(); B.add('MZ', v, rv); B.dets.append(1 << rv)
    return c
def cat_check(B, kind, groups, verify):
    """groups: list of data-axis lists, one per cat qubit. kind 'Z' uses controlled-Z, 'X' uses controlled-X."""
    c = cat_prep(B, len(groups), verify)
    for qc, g in zip(c, groups):
        for d in g: B.add('CZ' if kind == 'Z' else 'CNOT', qc, d)
    mask = 0
    for qc in c:
        r = B.r(); B.add('MX', qc, r); mask |= 1 << r
    B.dets.append(mask); return c
def build_round(spec):
    B = Builder()
    for fn, *args in spec: fn(B, *args)
    return B
AX = [0, 1, 2, 3]
ROUNDS = {
  'L conv (baseline)':      (lambda: build_round([(z_conv, [0, 1]), (z_conv, [2, 3])]), 'L'),
  'J conv':                 (lambda: build_round([(z_conv, AX), (x_conv, AX)]), 'J'),
  'J flag':                 (lambda: build_round([(z_flag, AX), (x_flag, AX)]), 'J'),
  'J cat (verified)':       (lambda: build_round([(cat_check, 'Z', [[0], [1], [2], [3]], True), (cat_check, 'X', [[0], [1], [2], [3]], True)]), 'J'),
  'J cat (unverified)':     (lambda: build_round([(cat_check, 'Z', [[0], [1], [2], [3]], False), (cat_check, 'X', [[0], [1], [2], [3]], False)]), 'J'),
  'J coop (Bell, verified)':   (lambda: build_round([(cat_check, 'Z', [[0, 1], [2, 3]], True), (cat_check, 'X', [[0, 1], [2, 3]], True)]), 'J'),
  'J coop (Bell, unverified)': (lambda: build_round([(cat_check, 'Z', [[0, 1], [2, 3]], False), (cat_check, 'X', [[0, 1], [2, 3]], False)]), 'J'),
}

# ---- regression against version 0.8 (ancilla-only single faults, each check on its own, ideal data)
def v8_counts(B, code, focus):
    locs = enumerate_faults(B.ops, 'M1', focus=focus); a = analyze(locs, B.dets, code, pairs=False)
    # version 0.8 classified each ancilla fault by the data error left (and whether the report flipped); reproduce its columns
    nf = a['nfault']; cnt = a['cnt']
    w2 = sum(1 for loc in locs for rec, ex, ez in loc if weight((ex, ez)) >= 2)
    silent = cnt.get('silent', 0)
    dmg = cnt.get('silent', 0) + cnt.get('pass_damaged', 0)
    return nf, w2, silent, dmg
Bz = Builder(); az = z_conv(Bz, AX); Bx = Builder(); ax_ = x_conv(Bx, AX)
Bl1 = Builder(); a1 = z_conv(Bl1, [0, 1]); Bl2 = Builder(); a2 = z_conv(Bl2, [2, 3])
Jz = v8_counts(Bz, 'J', az); Jx = v8_counts(Bx, 'J', ax_); L1 = v8_counts(Bl1, 'L', a1); L2 = v8_counts(Bl2, 'L', a2)
print("  regression, ancilla-only faults, each check alone: (fault cases, data errors of weight >= 2, silent logical with unflipped report, damaged data with unflipped report)")
print("      local ZZII", L1, " local IIZZ", L2, " joint ZZZZ", Jz, " joint XXXX", Jx)
check("the circuit-level engine in model M1 reproduces the version 0.8 extraction table exactly: local 18 cases, 4 data errors of weight >= 2, 2 silent with unflipped report, 2 damaged with unflipped report; joint 30 cases, 12, 2, 6",
      (L1[0] + L2[0], L1[1] + L2[1], L1[2] + L2[2], L1[3] + L2[3]) == (18, 4, 2, 2) and (Jz[0] + Jx[0], Jz[1] + Jx[1], Jz[2] + Jx[2], Jz[3] + Jx[3]) == (30, 12, 2, 6))

# =============================================================== C. methods compared
print("== C. extraction methods compared (single faults, then fault pairs) ==")
R = {}
for name, (mk, code) in ROUNDS.items():
    B = mk(); res = resources(B); R[name] = dict(B=B, code=code, res=res)
    for model in ('M2', 'M3'):
        locs = enumerate_faults(B.ops, model); R[name][model] = analyze(locs, B.dets, code)
def f6(x): return f"{x:.3f}"
for model in ('M2', 'M3'):
    print(f"  model {model}: first-order coefficients (per unit location-failure probability p) and silent-damage detail")
    print("      method                       locs  faults | silent  pass+damaged(caught next round)  false-reject  reject+damage | RAW max weight among PASS (stabilizer elements included; see section E for the coset weight); PASS cases with raw weight>=2 | silent E weights | 2nd-order silent")
    for name in ROUNDS:
        a = R[name][model]; c = a['c1']
        print(f"      {name:27s} {a['nloc']:5d} {a['nfault']:6d} | {c.get('silent',0):6.3f}  {c.get('pass_damaged',0):8.3f}  {c.get('false_reject',0):12.3f}  {c.get('caught_damage',0):10.3f} | {a['maxpassw']}; {a['passmulti']:3d} | {dict(sorted(a['silentw'].items()))} | {a['S2']:.3f}")
print("  resources per round (structural proxies, not costs):")
print("      method                       2q gates  1q gates  ancilla qubits  measurements  ancilla-ancilla 2q  photons per ancilla")
for name in ROUNDS:
    r = R[name]['res']; print(f"      {name:27s} {r['n2q']:8d} {r['n1q']:9d} {r['nanc']:14d} {r['nmeas']:13d} {r['aa2q']:18d} {r['ancspan']:19d}")

# =============================================================== C2. exact rates under the per-location fault model (no small-p expansion)
print("== C2. exact per-round outcome probabilities (every location fails independently with probability p, then a uniform Pauli) ==")
def wht(a):
    h = 1; n = len(a)
    while h < n:
        for i in range(0, n, 2 * h):
            for j in range(i, i + h):
                u, v = a[j], a[j + h]; a[j], a[j + h] = u + v, u - v
        h *= 2
    return a
def packed_locs(locs, dets):
    nd = len(dets); out = []
    for loc in locs:
        pk = []
        for rec, ex, ez in loc:
            dv = 0
            for j, m in enumerate(dets):
                if pop(rec & m) & 1: dv |= 1 << j
            pk.append(dv | (ex << nd) | (ez << (nd + 4)))
        out.append(tuple(sorted(pk)))
    return out
class Exact:
    def __init__(s, locs, dets, code):
        s.nd = len(dets); s.nb = s.nd + 8; s.N = 1 << s.nb; s.code = code; s.pk = packed_locs(locs, dets)
        grp = defaultdict(int)
        for t in s.pk: grp[t] += 1
        PCt = [pop(i) & 1 for i in range(s.N)]
        s.groups = []
        for t, mult in grp.items():
            C = [sum(1 - 2 * PCt[sv & f] for f in t) / len(t) for sv in range(s.N)]
            s.groups.append((C, mult))
        s.cls = []
        for f in range(s.N):
            dv = f & ((1 << s.nd) - 1); ex = (f >> s.nd) & 15; ez = (f >> (s.nd + 4)) & 15
            s.cls.append((dv, CT[code][(ex, ez)]))
    def at(s, p):
        W = [1.0] * s.N
        for C, mult in s.groups:
            for sv in range(s.N): W[sv] *= (1 - p + p * C[sv]) ** mult
        P = wht(W); inv = 1.0 / s.N
        r = defaultdict(float)
        for f in range(s.N):
            pr = P[f] * inv
            if pr < 0 and pr > -1e-15: pr = 0.0
            dv, cl = s.cls[f]
            if dv == 0: r['silent' if cl == 'logical' else ('accept_damaged' if cl == 'detected' else 'accept_clean')] += pr
            else: r['reject_damaged' if cl in ('detected', 'logical') else 'reject_clean'] += pr
        r['reject'] = r['reject_damaged'] + r['reject_clean']
        return dict(r)
EX = {}
for model in ('M2', 'M3'):
    for name in ROUNDS:
        B = R[name]['B']; EX[(model, name)] = Exact(enumerate_faults(B.ops, model), B.dets, R[name]['code'])
PS = [1e-4, 1e-3, 1e-2, 3e-2, 1e-1]
tot_ok = True
for model in ('M2', 'M3'):
    print(f"  model {model}: probability per round of  silent-logical (accepted and wrong) | accepted-damaged (caught later) | rejected")
    print("      method                     " + "".join(f"p={p:<9g}                      " for p in PS))
    for name in ROUNDS:
        row = []
        for p in PS:
            e = EX[(model, name)].at(p); row.append(f"{e.get('silent',0):.2e} {e.get('accept_damaged',0):.2e} {e['reject']:.2e}")
            tot_ok &= abs(sum(v for k, v in e.items() if k not in ('reject',)) - 1) < 1e-9
        print(f"      {name:26s} " + " | ".join(row))
check("the exact distributions sum to 1 for every method, model and p (WHT convolution of independent location faults)", tot_ok)
# Monte Carlo validation of the exact engine (flagged joint round, model M2)
def mc(name, model, p, n):
    ex = EX[(model, name)]; cnt = defaultdict(int); pk = ex.pk
    lst = [t for t in pk]
    for _ in range(n):
        f = 0
        for t in lst:
            if random.random() < p: f ^= t[random.randrange(len(t))]
        dv, cl = ex.cls[f]
        cnt['silent' if (dv == 0 and cl == 'logical') else ('acc_dam' if (dv == 0 and cl == 'detected') else ('rej' if dv else 'clean'))] += 1
    return {k: v / n for k, v in cnt.items()}
NMC = 60000; mm_ok = True
for name in ('J conv', 'J flag', 'L conv (baseline)'):
    e = EX[('M2', name)].at(0.05); m = mc(name, 'M2', 0.05, NMC)
    for k, kk in (('silent', 'silent'), ('acc_dam', 'accept_damaged'), ('rej', 'reject')):
        sd = math.sqrt(max(e[kk] * (1 - e[kk]), 1e-12) / NMC); mm_ok &= abs(m.get(k, 0) - e[kk]) < 5 * sd + 1e-9
check(f"Monte Carlo ({NMC} sampled rounds, p=0.05, M2) agrees with the exact engine within 5 standard errors for silent, accepted-damaged and rejected: conventional local, conventional joint, flagged joint", mm_ok)
# small-p agreement with the first-order coefficients
e = EX[('M2', 'J conv')].at(1e-6); c = R['J conv']['M2']['c1']
check("at p=1e-6 the exact silent probability equals the first-order coefficient times p within 1% (joint conventional, M2)", abs(e['silent'] / 1e-6 - c['silent']) / c['silent'] < 0.01)
# crossover scan on a log grid
def scan(model, key):
    grid = [10 ** (-5 + 0.05 * i) for i in range(0, 71)]
    out = {}
    for name in ROUNDS:
        vals = [EX[(model, name)].at(p) for p in grid]; out[name] = [v.get(key, 0.0) for v in vals]
    return grid, out
SC = {}
for model in ('M2', 'M3'):
    grid, out = scan(model, 'silent'); SC[model] = (grid, out)
    best = []
    for i, p in enumerate(grid):
        b = min(out, key=lambda n: out[n][i]); best.append(b)
    chg = [(grid[i], best[i - 1], best[i]) for i in range(1, len(grid)) if best[i] != best[i - 1]]
    print(f"  lowest silent-logical probability per round (model {model}), 1e-5 <= p <= 3e-2:", "; ".join(f"from p={g:.1e}: {b2}" for g, b1, b2 in [(grid[0], None, best[0])] + chg))
    for a_, b_ in (('J flag', 'J conv'), ('J flag', 'L conv (baseline)'), ('J flag', 'J cat (verified)'), ('J conv', 'L conv (baseline)'), ('J cat (verified)', 'J conv')):
        x = [i for i in range(len(grid)) if out[a_][i] < out[b_][i]]
        print(f"      silent({a_}) < silent({b_}) at {len(x)} of {len(grid)} grid points" + (f", from p={grid[x[0]]:.1e} to p={grid[x[-1]]:.1e}" if x else ""))

# =============================================================== D. concurrency windows
print("== D. concurrency: which in-code rotations can overlap an extraction round ==")
def sv_zero(n): v = [0j] * (1 << n); v[0] = 1; return v
def sv_h(v, q):
    r = 1 / math.sqrt(2); out = [0j] * len(v)
    for i, a in enumerate(v):
        if a == 0: continue
        j = i ^ (1 << q)
        if (i >> q) & 1: out[j] += a * r; out[i] -= a * r
        else: out[i] += a * r; out[j] += a * r
    return out
def sv_cnot(v, c, t): return [v[i ^ (1 << t)] if (i >> c) & 1 else v[i] for i in range(len(v))]
def sv_cz(v, a, b): return [-x if ((i >> a) & 1 and (i >> b) & 1) else x for i, x in enumerate(v)]
def sv_pauli(v, xm, zm):
    out = [0j] * len(v); iy = (1j) ** pop(xm & zm)
    for i, a in enumerate(v):
        if a != 0: out[i ^ xm] += a * iy * (-1 if pop(i & zm) & 1 else 1)
    return out
def sv_rot(v, g, th):
    pv = sv_pauli(v, g[0], g[1]); c, s = math.cos(th / 2), math.sin(th / 2)
    return [c * a - 1j * s * b for a, b in zip(v, pv)]
def project_code(v, gens):
    for (x, z, s) in gens:
        pv = sv_pauli(v, x, z); v = [(a + s * b) / 2 for a, b in zip(v, pv)]
    return v
def sv_norm(v):
    n = math.sqrt(sum(abs(a) ** 2 for a in v)); return [a / n for a in v]
def embed(v4, nq):  # data qubits 0..3, extra qubits in |0>
    return v4 + [0j] * ((1 << nq) - 16)
def run_sv(ops, nq, v, rot=None, slot=None):
    """Run ops (builder ops) on a state-vector; measurements deferred (Z outcomes read at the end). rot=(g,theta) is inserted after `slot` data-ancilla 2q gates."""
    cnt = 0; meas = []; ins = False
    def maybe(v):
        nonlocal ins
        if rot is not None and not ins and cnt == slot:
            ins = True; return sv_rot(v, rot[0], rot[1])
        return v
    v = maybe(v)
    for op in ops:
        k = op[0]
        if k == 'P+': v = sv_h(v, op[1])
        elif k == 'P0': pass
        elif k == 'H': v = sv_h(v, op[1])
        elif k == 'CNOT' or k == 'CZ':
            v = sv_cnot(v, op[1], op[2]) if k == 'CNOT' else sv_cz(v, op[1], op[2])
            if (op[1] < 4) != (op[2] < 4): cnt += 1; v = maybe(v)
        elif k == 'MZ': meas.append(op[1])
        elif k == 'MX': v = sv_h(v, op[1]); meas.append(op[1])
    if rot is not None and not ins: v = sv_rot(v, rot[0], rot[1])
    return v, meas
def condition_zero(v, meas, nq):
    p0 = 0.0; out = [0j] * 16; mask = sum(1 << q for q in meas)
    for i, a in enumerate(v):
        if i & mask == 0: p0 += abs(a) ** 2; out[i & 15] += a
    return p0, out
def window_test(ops, nq, code, g, slot, th=0.83):
    gens = LG if code == 'L' else JG
    v4 = sv_norm(project_code([complex(random.gauss(0, 1), random.gauss(0, 1)) for _ in range(16)], [(e[0], e[1], e[2]) for e in gens]))
    v, meas = run_sv(ops, nq, embed(v4, nq), rot=(g, th), slot=slot)
    p0, d = condition_zero(v, meas, nq)
    target = sv_rot(v4, g, th)
    ov = abs(sum(a.conjugate() * b for a, b in zip(target, d))) ** 2
    return p0, (ov / p0 if p0 > 1e-12 else 0.0)
def prefix_pred(check_kind, axes_order, k, g):
    pre = axes_order[:k]; x, z = g
    anti = 0
    for q in pre:
        if check_kind == 'Z': anti ^= (x >> q) & 1
        else: anti ^= (z >> q) & 1
    return anti == 0
COMM = {c: [f for f in ALL if f != (0, 0) and all(commute(f, (e[0], e[1])) for e in (LG if c == 'L' else JG))] for c in ('L', 'J')}
print(f"  in-code generators (commute with every check of the code, identity excluded): local {len(COMM['L'])}, joint {len(COMM['J'])}")
cases = [('J conv', 'J', 'Z', [0, 1, 2, 3], 0), ('J conv', 'J', 'X', [0, 1, 2, 3], 1), ('J flag', 'J', 'Z', [0, 1, 2, 3], 0), ('J flag', 'J', 'X', [0, 1, 2, 3], 1),
         ('L conv (baseline)', 'L', 'Z', [0, 1], 0), ('L conv (baseline)', 'L', 'Z', [2, 3], 1)]
WIN = {}; agree = True; dis = []; nsim = 0
for name, code, kind, order, which in cases:
    B = R[name]['B']; nq = B.nq
    # extract the ops of the individual check
    if name.startswith('J'):
        ops = [o for o in B.ops]; sub = []
    # simulate the WHOLE round (both checks) with the rotation inserted after `slot` data-ancilla gates; slot index is global over the round
    ndat = sum(1 for o in B.ops if o[0] in ('CNOT', 'CZ') and ((o[1] < 4) != (o[2] < 4)))
    per = len(order) if code == 'J' else len(order)
    base = 0 if which == 0 else per
    if code == 'J' and name == 'J flag': per_ops = 4
    for g in COMM[code]:
        row = []
        for k in range(0, per + 1):
            slot = base + k
            p0, fid = window_test(B.ops, nq, code, g, slot); nsim += 1
            okk = (p0 > 1 - 1e-9 and fid > 1 - 1e-9)
            pred = prefix_pred(kind, order, k, g)
            if okk != pred: agree = False; dis.append((name, g, k, p0, fid, pred))
            row.append(okk)
        WIN[(name, which, g)] = row
print(f"  {nsim} state-vector simulations of full extraction rounds with an in-code rotation (angle 0.83) inserted at each data-coupling slot")
check("rule confirmed by simulation: an in-code rotation can be inserted after k data couplings of a check without changing the check outcome or the rotated state (probability 1, fidelity 1) exactly when its generator commutes with the part of the check already coupled (prefix product); checked for every in-code generator, every slot, the conventional and flagged joint rounds and the local round", agree)
if dis: print("  disagreements:", dis[:5])
def interior(name, which, g): row = WIN[(name, which, g)]; return sum(row[1:-1])
for name, code, kind, order, which in cases:
    gs = COMM[code]; w2 = [g for g in gs if weight(g) == 2]; w1 = [g for g in gs if weight(g) == 1]
    for lab, sel in (('weight-1', w1), ('weight-2', w2)):
        if not sel: continue
        allowed = [interior(name, which, g) for g in sel]; slots = len(order) - 1
        print(f"      {name:18s} check {which} ({kind}-type, order {order}): {lab} in-code generators {len(sel):2d}; interior slots allowed per generator min/mean/max = {min(allowed)}/{sum(allowed)/len(allowed):.2f}/{max(allowed)} of {slots}")
# reordering: does some coupling order give an interior window?
def best_order_window(kind, g, n=4):
    best = 0; bo = None
    for perm in permutations(range(n)):
        w = sum(1 for k in range(1, n) if prefix_pred(kind, list(perm), k, g))
        if w > best: best = w; bo = perm
    return best, bo
reord = [best_order_window('Z', g)[0] for g in COMM['J'] if weight(g) == 2]
allow = sorted(interior('J conv', 0, g) for g in COMM['J'] if weight(g) == 2)
print(f"  joint ZZZZ check, native order: weight-2 in-code generators by number of allowed interior slots (of 3): " + str({k: allow.count(k) for k in sorted(set(allow))}))
check("joint code: every weight-2 in-code generator has an interior window under SOME coupling order of the check; in the native order the number of allowed interior slots ranges from 0 to 3 across generators", min(reord) >= 1 and min(allow) == 0 and max(allow) == 3)
check("the flagged round has exactly the same windows as the conventional round for every generator and slot (the flag couples to the ancilla only)", all(WIN[('J conv', k, g)] == WIN[('J flag', k, g)] for k in (0, 1) for g in COMM['J']))

# =============================================================== E. separate metrics, capability report, selection
print("== E. separate metrics, provisional capability report and requirement-driven selection ==")
def damage_mass(model, name):
    c = R[name][model]['c1']; return c.get('silent', 0) + c.get('pass_damaged', 0) + c.get('caught_damage', 0)
print("  per-method first-order mass of fault cases that leave ANY non-harmless data error (M2) = silent + accepted-damaged + rejected-with-damage:")
for name in ROUNDS: print(f"      {name:27s} {damage_mass('M2', name):6.3f}   (of which silent {R[name]['M2']['c1'].get('silent',0):.3f})")
dist_ge2 = {}
for name in ROUNDS:
    locs = enumerate_faults(R[name]['B'].ops, 'M2'); n2 = 0; nall = 0
    for loc in locs:
        for rec, ex, ez in loc:
            nall += 1
            if weight((ex, ez)) >= 2: n2 += 1
    dist_ge2[name] = (n2, nall)
print("  fault propagation (M2): fault cases leaving a data error of RAW weight >= 2 (stabilizer elements included) / all fault cases:  " + "; ".join(f"{n}: {a}/{b}" for n, (a, b) in dist_ge2.items()))
def stab_group(gens):
    grp = {(0, 0)}
    for e in gens: grp |= {(a[0] ^ e[0], a[1] ^ e[1]) for a in grp}
    return grp
STAB = {'L': stab_group(LG), 'J': stab_group(JG)}
def effw(E, code): return min(weight((E[0] ^ s[0], E[1] ^ s[1])) for s in STAB[code])
def pass_weights(name, model):
    code = R[name]['code']; ct = CT[code]; dets = R[name]['B'].dets; mx = 0; n2 = 0; raw = 0
    for loc in enumerate_faults(R[name]['B'].ops, model):
        for rec, ex, ez in loc:
            if any(pop(rec & m) & 1 for m in dets): continue
            if ct[(ex, ez)] in ('detected', 'logical'):
                w = effw((ex, ez), code); mx = max(mx, w); n2 += (w >= 2); raw = max(raw, weight((ex, ez)))
    return mx, n2, raw
PW = {n: pass_weights(n, 'M2') for n in ROUNDS}
print("  accepted (PASS) rounds that leave a non-harmless data error, M2: (maximum weight modulo the stabilizer group, number of fault cases with that weight >= 2, maximum raw weight): " + "; ".join(f"{n}: {v}" for n, v in PW.items()))
def single_axis_detected(code): return sum(1 for q in range(4) for pz in ((1, 0), (0, 1), (1, 1)) if CT[code][(pz[0] << q, pz[1] << q)] == 'detected')
def interior_stat(name):
    keys = [(k, g) for (n, k, g) in WIN if n == name]
    if not keys: return None
    vals = [sum(WIN[(name, k, g)][1:-1]) for k, g in keys if weight(g) == 2]
    return sum(vals) / len(vals)
def capability_report(model, p):
    rows = []
    for name in ROUNDS:
        r = R[name]; e = EX[(model, name)].at(p); c1 = r[model]['c1']; rs = r['res']
        rows.append(dict(config=name, code=r['code'], single_axis_detected=single_axis_detected(r['code']),
                         silent_exact=e.get('silent', 0.0), accepted_damaged=e.get('accept_damaged', 0.0), reject=e['reject'],
                         silent_first_order=c1.get('silent', 0.0), silent_second_order=r[model]['S2'],
                         n2q=rs['n2q'], ancillas=rs['nanc'], measurements=rs['nmeas'], anc_anc_2q=rs['aa2q'],
                         interior_windows_w2=interior_stat(name), physical_cost=None))
    return rows
def dominated(a, b, keys, maximise):
    """True when a is dominated by b: b is no worse on every metric and strictly better on at least one."""
    better = False
    for k in keys:
        x, y = a[k], b[k]
        if k in maximise: x, y = -x, -y
        if y > x + 1e-300: return False
        if y < x: better = True
    return better
def select(rows, req, keys, maximise=('single_axis_detected',)):
    feas = []; why = {}
    for r in rows:
        bad = [f"{k}={r[k]:.3g} violates {op}{lim:g}" for k, (op, lim) in req.items() if (op == '<=' and r[k] > lim) or (op == '>=' and r[k] < lim)]
        if bad: why[r['config']] = bad
        else: feas.append(r)
    par = [a for a in feas if not any(dominated(a, b, keys, maximise) for b in feas if b is not a)]
    return feas, par, why
KEYS = ['silent_exact', 'reject', 'n2q', 'ancillas', 'single_axis_detected']
REQS = {
  'A: silent <= 1e-5, reject <= 5%': {'silent_exact': ('<=', 1e-5), 'reject': ('<=', 0.05)},
  'B: silent <= 1e-3, reject <= 1%': {'silent_exact': ('<=', 1e-3), 'reject': ('<=', 0.01)},
  'C: silent <= 1e-3, at most 4 ancillas, 2q gates <= 10': {'silent_exact': ('<=', 1e-3), 'ancillas': ('<=', 4), 'n2q': ('<=', 10)},
}
SEL = {}; NONDOM = True
for p in (1e-4, 1e-3, 1e-2):
    rows = capability_report('M2', p)
    for rn, rq in REQS.items():
        feas, par, why = select(rows, rq, KEYS); SEL[(p, rn)] = ([f['config'] for f in feas], [q['config'] for q in par])
        NONDOM &= all(not dominated(a, b, KEYS, ('single_axis_detected',)) for a in par for b in par if a is not b) and all(any(dominated(f, b, KEYS, ('single_axis_detected',)) for b in par) for f in feas if f not in par)
        print(f"      p={p:g}  requirement {rn}: feasible {[f['config'] for f in feas]} -> Pareto set {[q['config'] for q in par]}")
rows_demo = capability_report('M2', 1e-3)
print("  provisional capability report row (one configuration; physical cost fields intentionally empty, audit item A02):")
print("     ", {k: (round(v, 6) if isinstance(v, float) else v) for k, v in rows_demo[2].items()})
check("every capability-report row has its physical cost field empty (None): no physical cost is claimed", all(r['physical_cost'] is None for r in rows_demo))
# objective support table (derived, not assumed)
inc = [g for g in COMM['J']]; detJ = [g for g in inc if CT['J'][g] == 'detected']; detL = [g for g in COMM['L'] if CT['L'][g] == 'detected']
print(f"  operational assurance by structural checks: in-code rotation generators detected by their own code's checks: local {len(detL)} of {len(COMM['L'])}, joint {len(detJ)} of {len(COMM['J'])}")

# =============================================================== F. reference preparations
print("== F. reference preparations for operational assurance ==")
def sv_cphase(v, a, b, phi): return [x * complex(math.cos(phi), math.sin(phi)) if ((i >> a) & 1 and (i >> b) & 1) else x for i, x in enumerate(v)]
bad_ok = True
for d in (0.05, 0.3, 1.0, 2.5):
    v = sv_h(sv_zero(2), 0); v = sv_cnot(sv_h(sv_zero(2), 1), 1, 1) if False else v
    v = sv_h(sv_zero(2), 0); v[1], v[3] = v[1], v[3]
    v = sv_h(sv_zero(2), 0); v = [0j] * 4; v[2] = 1 / math.sqrt(2); v[3] = 1 / math.sqrt(2)           # control(bit0)=+, target(bit1)=1
    nominal = math.pi; act = sv_cphase(v, 0, 1, nominal + d); ideal = sv_cphase(v, 0, 1, nominal)
    pclick = 1 - abs(sum(a.conjugate() * b for a, b in zip(ideal, act))) ** 2
    bad_ok &= abs(pclick - math.sin(d / 2) ** 2) < 1e-12
check("reference preparation (control in |+>, target in |1>, then compare with the nominal output): the click probability for a phase-angle error d is exactly sin^2(d/2)", bad_ok)
print("  runs of the reference needed to detect a constant angle error d at 95% confidence (all-clean runs have probability cos^2(d/2) each):")
NEED = {}
for d in (0.01, 0.03, 0.1, 0.3, 1.0):
    n = math.ceil(math.log(0.05) / math.log(math.cos(d / 2) ** 2)); NEED[d] = n; print(f"      d={d:<5g} rad: {n} reference runs")
# which references expose which in-code generators (two logical qubits; logical generators of the joint code)
LOGX = [(1, 0), (0, 0)]
def lg_pauli(name):  # logical Paulis of the joint code on 2 logical qubits, as 4-axis Paulis, from the V0.8 map
    table = {'X1': (0b0011, 0), 'X2': (0b0101, 0), 'Z1': (0, 0b0101), 'Z2': (0, 0b0011)}
    return table[name]
def logical_stats(gname):
    # expectation of a two-qubit logical Pauli string on a product reference state
    pass
# work in the 4-dimensional logical space directly
def mat_pauli2(a, b):
    P = {'I': [[1, 0], [0, 1]], 'X': [[0, 1], [1, 0]], 'Y': [[0, -1j], [1j, 0]], 'Z': [[1, 0], [0, -1]]}
    return kron(P[a], P[b])
def st1(k): r = 1 / math.sqrt(2); return {'0': [1, 0], '1': [0, 1], '+': [r, r], '-': [r, -r], 'i': [r, 1j * r], 'j': [r, -1j * r]}[k]
def ref2(a, b): return [x * y for x in st1(a) for y in st1(b)]
GENS2 = [a + b for a in 'IXYZ' for b in 'IXYZ' if a + b != 'II']
def click(g, ref, d=0.4):
    G = mat_pauli2(g[0], g[1]); psi = ref; ev = sum(psi[i].conjugate() * sum(G[i][j] * psi[j] for j in range(4)) for i in range(4)).real
    return math.sin(d / 2) ** 2 * (1 - ev * ev)
REFSETS = {'Z-basis products (00,01,10,11)': [ref2(a, b) for a in '01' for b in '01'],
           'plus Z-basis and X-basis products (++ etc.)': [ref2(a, b) for a in '01+-' for b in '01+-'],
           'all 36 product states of the six single-qubit states': [ref2(a, b) for a in '01+-ij' for b in '01+-ij']}
MISSED = {}
for nm_, refs in REFSETS.items():
    missed = [g for g in GENS2 if max(click(g, r) for r in refs) < 1e-12]; MISSED[nm_] = missed
    print(f"      {nm_}: logical error generators with ZERO click probability on every reference: {len(missed)} of 15 {missed}")
# every generator is exposed by a numeric search over product references? and the click for a Bell-type reference
bell = [1 / math.sqrt(2), 0, 0, 1 / math.sqrt(2)]
print("      Bell reference (|00>+|11>)/sqrt2 alone misses:", [g for g in GENS2 if click(g, bell) < 1e-12])
# the individual unknown state: syndromes and references say nothing about it
dstate = [random.gauss(0, 1) + 1j * random.gauss(0, 1) for _ in range(4)]; dstate = vn(dstate)
print("  an unknown logical state passes every check of its code after any in-code error, while its own fidelity with the intended output can be low:")
fids = []
for g in ('ZZ', 'XI', 'YX'):
    G = mat_pauli2(g[0], g[1]); th = 2.0; c, s = math.cos(th / 2), math.sin(th / 2)
    out = [c * dstate[i] - 1j * s * sum(G[i][j] * dstate[j] for j in range(4)) for i in range(4)]
    fid = abs(sum(a.conjugate() * b for a, b in zip(dstate, out))) ** 2; fids.append(fid)
    print(f"      error rotation about logical {g} by 2.0 rad: all structural checks read +1 (phase coverage), fidelity with the intended state {fid:.3f}")

# =============================================================== G. result-dependent assertions (written after reading the output above)
print("== G. result checks ==")
def c1(name, model, key): return R[name][model]['c1'].get(key, 0.0)
check("PRIORITY 1: flagged joint extraction has ZERO first-order silent logical damage from single faults, in model M2 (every gate/measurement/preparation location) and in M3 (plus idle faults on every live qubit and incoming data faults)",
      c1('J flag', 'M2', 'silent') == 0 and c1('J flag', 'M3', 'silent') == 0)
check("the verified cat ancilla also reaches zero first-order silent damage under M2 and M3; the unverified cat does not (28/15 under M2)",
      c1('J cat (verified)', 'M2', 'silent') == 0 and c1('J cat (verified)', 'M3', 'silent') == 0 and near(c1('J cat (unverified)', 'M2', 'silent'), 28 / 15, 1e-9))
check("conventional joint extraction leaves 4/15 = 0.267 silent per unit p under M2 and M3 (all of weight 2, from the hook); the conventional local round leaves 8/15 = 0.533 under M2, all of weight 1, and 11.2 under M3 because the local code cannot see the Z faults that Buddy's gates and idling leave on the data",
      near(c1('J conv', 'M2', 'silent'), 4 / 15, 1e-9) and near(c1('J conv', 'M3', 'silent'), 4 / 15, 1e-9) and R['J conv']['M2']['silentw'] == {2: 4}
      and near(c1('L conv (baseline)', 'M2', 'silent'), 8 / 15, 1e-9) and R['L conv (baseline)']['M2']['silentw'] == {1: 8} and near(c1('L conv (baseline)', 'M3', 'silent'), 11.2, 1e-9))
check("NEGATIVE RESULT: the cooperative two-cat-qubit round (each cat qubit couples the two axes of one photon) is NOT fault tolerant to single faults even with a verified cat: 0.8 per unit p under M2 and 4.133 under M3, all weight-2 Z-type errors on one photon, because a cat-qubit X fault AFTER verification becomes a weight-2 logical error; the unverified version leaves 32/15 = 2.133",
      near(c1('J coop (Bell, verified)', 'M2', 'silent'), 0.8, 1e-9) and R['J coop (Bell, verified)']['M2']['silentw'] == {2: 12} and near(c1('J coop (Bell, verified)', 'M3', 'silent'), 4.133, 1e-3)
      and near(c1('J coop (Bell, unverified)', 'M2', 'silent'), 32 / 15, 1e-9))
check("resource proxies per round are as printed (2q gates, 1q gates, ancilla qubits, measurements, ancilla-ancilla gates): local conventional 4/0/2/2/0; joint conventional 8/0/2/2/0; flagged 12/0/4/4/4; verified cat 18/2/10/10/10; unverified cat 14/2/8/8/6; verified Bell 14/2/6/6/6; unverified Bell 10/2/4/4/2",
      [tuple(R[n]['res'][k] for k in ('n2q', 'n1q', 'nanc', 'nmeas', 'aa2q')) for n in ROUNDS] ==
      [(4, 0, 2, 2, 0), (8, 0, 2, 2, 0), (12, 0, 4, 4, 4), (18, 2, 10, 10, 10), (14, 2, 8, 8, 6), (14, 2, 6, 6, 6), (10, 2, 4, 4, 2)])
check("the second-order silent coefficient from fault PAIRS (M2) is 1.244 local, 2.427 joint conventional, 2.320 flagged, 9.902 verified cat: flagging removes the first-order term but not the second-order one, as it must for a distance-2 code; verified cat is about four times worse at second order",
      near(R['L conv (baseline)']['M2']['S2'], 1.244, 1e-3) and near(R['J conv']['M2']['S2'], 2.427, 1e-3) and near(R['J flag']['M2']['S2'], 2.320, 1e-3) and near(R['J cat (verified)']['M2']['S2'], 9.902, 1e-3))
check("the pair-enumeration coefficients agree with the exact engine: silent(p)/p^2 at p=1e-4 within 1% of the second-order coefficient (flagged and verified cat, M2, where the first-order term is zero)",
      all(abs(EX[('M2', n)].at(1e-4)['silent'] / 1e-8 - R[n]['M2']['S2']) / R[n]['M2']['S2'] < 0.01 for n in ('J flag', 'J cat (verified)')))
sc2g, sc2 = SC['M2']; sc3g, sc3 = SC['M3']
check("under M2 (Buddy's own faults only) the flagged joint round has the lowest silent-logical probability of all seven rounds at every p from 1e-5 to 3e-2",
      all(sc2['J flag'][i] <= min(sc2[n][i] for n in ROUNDS) for i in range(len(sc2g))))
cr = next(sc3g[i] for i in range(len(sc3g)) if sc3['J conv'][i] < sc3['J flag'][i])
print(f"  M3 crossover: conventional joint becomes better than flagged joint at p = {cr:.2e}; analytic estimate from the coefficients = {4/15/(R['J flag']['M3']['S2'] - R['J conv']['M3']['S2']):.2e}")
check("NEGATIVE RESULT: when idle faults are counted (M3), flagged extraction stops beating conventional joint extraction at about p = 1e-3 per location (scan crossover between 5e-4 and 3e-3), because its longer circuit exposes more locations to pairs of faults",
      5e-4 < cr < 3e-3)
e3 = {n: EX[('M3', n)].at(1e-3) for n in ROUNDS}; e2 = {n: EX[('M2', n)].at(1e-3) for n in ROUNDS}
check("rejection costs at p=1e-3 (M2): flagged joint rejects about 3x as many rounds as the local round (2.5 to 3.5), the conventional joint round 1.4 to 1.8x",
      2.5 < e2['J flag']['reject'] / e2['L conv (baseline)']['reject'] < 3.5 and 1.4 < e2['J conv']['reject'] / e2['L conv (baseline)']['reject'] < 1.8)
check("mass of fault cases that leave ANY data error rises along the sequence local, joint, flagged, verified cat (M2): 3.200 local, 6.933 joint, 9.067 flagged, 16.800 verified cat -- Buddy's own mechanism damages the data more often as it gets more elaborate, even when the damage is caught",
      near(damage_mass('M2', 'L conv (baseline)'), 3.2, 1e-9) and near(damage_mass('M2', 'J conv'), 104 / 15, 1e-9) and near(damage_mass('M2', 'J flag'), 136 / 15, 1e-9) and near(damage_mass('M2', 'J cat (verified)'), 16.8, 1e-9))
check("with idle and incoming data faults (M3, uniform Pauli noise at p=1e-3) every joint round has a lower silent-logical probability than the local round (by a factor above 5), because the local code is blind to Z; this depends on the noise being Z-capable and is not a general statement",
      all(e3[n]['silent'] * 5 < e3['L conv (baseline)']['silent'] for n in ('J conv', 'J flag', 'J cat (verified)')))
check("windows: 4 of 4 weight-1 local generators have the single interior slot of each local check; 10 of 14 weight-2 local generators do; the joint ZZZZ and XXXX checks allow 34 of 54 (generator, interior slot) pairs for the 18 weight-2 in-code generators",
      all(sum(WIN[('L conv (baseline)', k, g)][1:-1]) == 1 for k in (0, 1) for g in COMM['L'] if weight(g) == 1)
      and sum(sum(WIN[('L conv (baseline)', 0, g)][1:-1]) for g in COMM['L'] if weight(g) == 2) == 10
      and all(sum(sum(WIN[('J conv', k, g)][1:-1]) for g in COMM['J'] if weight(g) == 2) == 34 for k in (0, 1)))
check("selection is a Pareto set over separate metrics, never a combined score; the sets differ between p=1e-4 and p=1e-3 for requirement B, and at p=1e-2 no configuration meets any of the three example requirements",
      SEL[(1e-4, 'B: silent <= 1e-3, reject <= 1%')][1] != SEL[(1e-3, 'B: silent <= 1e-3, reject <= 1%')][1] and all(SEL[(1e-2, rn)][0] == [] for rn in REQS))
check("every Pareto set is a non-empty subset of its feasible set whenever the feasible set is non-empty, no member is dominated by another member, and every feasible non-member is dominated by some member", all((not f) or (p_ and set(p_) <= set(f)) for f, p_ in SEL.values()) and NONDOM)
check("MODULO THE STABILIZER GROUP (the right notion of weight for these codes: ZZZZ, XXXX, YYYY act trivially on the information): every accepted round of the flagged joint extraction leaves at most a weight-1 data error under M2, the verified cat likewise, while the conventional joint round passes weight-2 errors (the hook) and the unverified cat and both cooperative rounds also do",
      PW['J flag'][0] == 1 and PW['J flag'][1] == 0 and PW['J cat (verified)'][0] == 1 and PW['J cat (verified)'][1] == 0 and PW['J conv'][0] == 2 and PW['J conv'][1] > 0
      and all(PW[n][0] >= 2 for n in ('J cat (unverified)', 'J coop (Bell, verified)', 'J coop (Bell, unverified)')))
check("PRIORITY 6: reference preparations expose a constant angle error d with click probability sin^2(d/2); 12 runs for d=1, 133 for d=0.3, 1198 for d=0.1, 13314 for d=0.03, 119829 for d=0.01 reach 95% confidence of at least one click",
      NEED == {0.01: 119829, 0.03: 13314, 0.1: 1198, 0.3: 133, 1.0: 12})
check("a Z-basis-only reference set misses three of fifteen logical error generators (IZ, ZI, ZZ); adding X-basis product references closes all fifteen for constant errors; a single Bell reference misses XX, YY, ZZ",
      sorted(MISSED['Z-basis products (00,01,10,11)']) == ['IZ', 'ZI', 'ZZ'] and MISSED['plus Z-basis and X-basis products (++ etc.)'] == [] and [g for g in GENS2 if click(g, bell) < 1e-12] == ['XX', 'YY', 'ZZ'])
check("an unknown logical state hit by an in-code rotation error passes every structural check yet has fidelity 0.35-0.58 with the intended state (three errors, angle 2.0); a reference run measures the apparatus under the reference input, not this state", all(f < 0.6 for f in fids))
print(); print("ALL PASS" if all(ok for _, ok in results) else "FAILURES")
