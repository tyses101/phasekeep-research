# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tyler O'Bryan, where applicable
"""Buddy verification, version 1.0: which of the version 0.9 results survive photonic reality? Plain Python, no packages.

Evidence: [[DERIVED]] means exact within the stated model (ideal Clifford circuits plus Pauli, erasure and loss-like faults; exact Pauli-frame
propagation; exact convolution of independent location faults; small state-vector simulations). Rates, success probabilities, hosting rules and
noise biases are [[ASSUMED]] parameters, not measurements. Literature on photonic gates is [[UNVERIFIED]] (abstract level). Nothing here is a
hardware result, a cost, or a comparison with a conventional architecture. Structural counts are proxies; no combined score is formed.

Every new mechanism has a switch that reduces to the version 0.9 assumptions (no loss, deterministic gates, uniform Pauli noise, one round,
ideal references), and part A checks that the switched-off program reproduces version 0.9's numbers, so differences are attributable.

Parts
  A. Regression to version 0.9 (switches off) and the erratum list
  B. Feasibility structure: destructive detection, hosting of ancillas on photons, inter-photon gate counts
  C. Probabilistic inter-photon gates: completion probability and attempt counts
  D. Photon loss: heralded and unheralded
  E. Biased noise across axes and verification resources, and basis-dependent readout
  F. Repeated rounds and accumulated damage, against no verification
  G. Coherent error amplification with reference preparations
  H. One measurement mechanism, several purposes: what the observable must satisfy
  I. Capability report version 2 and selection under physical profiles
  J. Result checks (written after reading the output of A to I)
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


# =============================================================== B. circuit-level engine
print("== circuit-level engine (copied from version 0.9) ==")
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


# ---- small state-vector helpers (copied from version 0.9)
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

# =============================================================== generalized enumerator and exact engine (new in 1.0)
# Location types: g (gate, preparation, one-qubit gate), mz / mx (measurement flip in Z / X basis), in (incoming data fault),
# idle (idle live qubit), ld (loss of a data photon at a gate, unheralded variant: its two axes are randomised),
# la_h (loss of an ancilla photon at a gate, HERALDED: the round is flagged), la_u (same loss, UNHERALDED: the ancilla qubit is randomised).
P1 = [(1, 0), (1, 1), (0, 1)]
def pauli_w(q, u, bias):
    """weight of single-qubit Pauli u=(x,z) on qubit q. bias = {'data': (kind, b), 'anc': (kind, b)} or None; kind 'Z' or 'X' multiplies that Pauli's weight."""
    if bias is None or u == (0, 0): return 1.0
    kind, b = bias['data' if q < 4 else 'anc']
    if kind == 'Z' and u == (0, 1): return b
    if kind == 'X' and u == (1, 0): return b
    return 1.0
def enum_w(ops, bias=None, loss=False):
    locs = []; alive = set(range(4))
    def mk(typ, plist, i0):
        opts = []
        for xm, zm, w in plist:
            rec, x, z = run_from(ops, i0, xm, zm); opts.append((rec, x & 15, z & 15, w, 0))
        locs.append((typ, opts))
    for q in range(4): mk('in', [(p[0] << q, p[1] << q, pauli_w(q, p, bias)) for p in P1], 0)
    for i, op in enumerate(ops):
        tq = touched(op)
        if op[0] in ('MZ', 'MX'): alive.discard(op[1])
        elif op[0] in ('P0', 'P+'): alive.add(op[1])
        if op[0] == 'MZ': locs.append(('mz', [(1 << op[2], 0, 0, 1.0, 0)]))
        elif op[0] == 'MX': locs.append(('mx', [(1 << op[2], 0, 0, 1.0, 0)]))
        elif len(tq) == 2:
            a, b = tq; pl = []
            for u in [(0, 0)] + P1:
                for v in [(0, 0)] + P1:
                    if u == (0, 0) and v == (0, 0): continue
                    pl.append(((u[0] << a) | (v[0] << b), (u[1] << a) | (v[1] << b), pauli_w(a, u, bias) * pauli_w(b, v, bias)))
            mk('g', pl, i + 1)
        else: mk('g', [(p[0] << tq[0], p[1] << tq[0], pauli_w(tq[0], p, bias)) for p in P1], i + 1)
        for q in sorted(alive):
            if q not in tq: mk('idle', [(p[0] << q, p[1] << q, pauli_w(q, p, bias)) for p in P1], i + 1)
        if loss and len(tq) == 2:
            for q in tq:
                if q < 4:      # data photon q//2 loses (unheralded variant): both its axes become a uniformly random Pauli (identity included)
                    ax = (2 * (q // 2), 2 * (q // 2) + 1); pl = []
                    for u in [(0, 0)] + P1:
                        for v in [(0, 0)] + P1:
                            pl.append(((u[0] << ax[0]) | (v[0] << ax[1]), (u[1] << ax[0]) | (v[1] << ax[1]), 1.0))
                    mk('ld', pl, i + 1)
                else:
                    locs.append(('la_h', [(0, 0, 0, 1.0, 1)]))
                    mk('la_u', [(0, 0, 1.0)] + [(p[0] << q, p[1] << q, 1.0) for p in P1], i + 1)
    return locs
class Exact2:
    """Exact distribution of one extraction round: independent location faults, XOR-convolved by a Walsh-Hadamard transform."""
    def __init__(s, B, code, bias=None, loss=False):
        s.B = B; s.code = code; s.dets = B.dets; s.nd = len(B.dets) + 1; s.nb = s.nd + 8; s.N = 1 << s.nb
        locs = enum_w(B.ops, bias, loss); grp_ = defaultdict(int)
        for typ, opts in locs:
            tot = sum(o[3] for o in opts); pk = []
            for rec, ex, ez, w, hr in opts:
                dv = 0
                for j, m in enumerate(B.dets):
                    if pop(rec & m) & 1: dv |= 1 << j
                pk.append((dv | (hr << (s.nd - 1)) | (ex << s.nd) | (ez << (s.nd + 4)), w / tot))
            grp_[(typ, tuple(sorted(pk)))] += 1
        PCt = [pop(i) & 1 for i in range(s.N)]; s.groups = []
        for (typ, pk), mult in grp_.items():
            C = [sum(w * (1 - 2 * PCt[sv & f]) for f, w in pk) for sv in range(s.N)]
            s.groups.append((typ, C, mult))
        s.cls = []
        for f in range(s.N):
            dv = f & ((1 << (s.nd - 1)) - 1); hr = (f >> (s.nd - 1)) & 1; ex = (f >> s.nd) & 15; ez = (f >> (s.nd + 4)) & 15
            s.cls.append((dv, hr, CT[code][(ex, ez)], (ex, ez)))
    def dist(s, rates):
        W = [1.0] * s.N
        for typ, C, mult in s.groups:
            r = rates.get(typ, 0.0)
            if r == 0.0: continue
            for sv in range(s.N): W[sv] *= (1 - r + r * C[sv]) ** mult
        P = wht(W); inv = 1.0 / s.N
        return [(x * inv if abs(x * inv) > 1e-18 else 0.0) for x in P]
    def at(s, rates):
        P = s.dist(rates); r = defaultdict(float)
        for f in range(s.N):
            pr = P[f]
            if pr == 0.0: continue
            dv, hr, cl, _ = s.cls[f]
            if hr: r['herald'] += pr
            elif dv == 0: r['silent' if cl == 'logical' else ('accept_damaged' if cl == 'detected' else 'accept_clean')] += pr
            else: r['reject_damaged' if cl in ('detected', 'logical') else 'reject_clean'] += pr
        r['reject'] = r['reject_damaged'] + r['reject_clean']
        return dict(r)
def wht(a):
    h = 1; n = len(a)
    while h < n:
        for i in range(0, n, 2 * h):
            for j in range(i, i + h):
                u, v = a[j], a[j + h]; a[j], a[j + h] = u + v, u - v
        h *= 2
    return a
def RT(p, **kw):
    """version 0.9 rates (M3-like when idle/in are on): gate, measurement, idle and incoming locations all fail with probability p."""
    d = {'g': p, 'mz': p, 'mx': p}; d.update(kw); return d
V09 = dict(**{})
# =============================================================== A. regression to version 0.9, erratum list
print("== A. regression to version 0.9 (all new mechanisms switched off) ==")
ZZZZ_G = ((0, 0b1111, 1),); JZF = {(0, 0), (0, 0b1111)}; CT['Jz'] = classtable(ZZZZ_G, JZF)
ROUNDS['J ZZZZ only (partial)'] = (lambda: build_round([(z_conv, AX)]), 'Jz')
NAMES = ['L conv (baseline)', 'J conv', 'J flag', 'J cat (verified)', 'J cat (unverified)', 'J coop (Bell, verified)', 'J coop (Bell, unverified)', 'J ZZZZ only (partial)']
E2 = {}
for nm in NAMES:
    mk, code = ROUNDS[nm]; B = mk(); E2[nm] = Exact2(B, code); R_ = {'B': B, 'code': code}
BR = {nm: ROUNDS[nm][0]() for nm in NAMES}
# version 0.9 published values (page section 4), M2 meaning gate/preparation/measurement faults only (no incoming, no idle)
V09_M2_SILENT_1E3 = {'L conv (baseline)': 5.31e-4, 'J conv': 2.66e-4, 'J flag': 2.29e-6, 'J cat (verified)': 9.66e-6}
V09_M2_REJECT_1E3 = {'L conv (baseline)': 5.45e-3, 'J conv': 8.62e-3, 'J flag': 1.61e-2, 'J cat (verified)': 3.13e-2}
ok_reg = True
for nm in V09_M2_SILENT_1E3:
    e = E2[nm].at(RT(1e-3))
    ok_reg &= abs(e['silent'] / V09_M2_SILENT_1E3[nm] - 1) < 0.01 and abs(e['reject'] / V09_M2_REJECT_1E3[nm] - 1) < 0.01
check("REGRESSION: with loss, bias and incoming faults off, the generalized exact engine reproduces the version 0.9 silent and rejection probabilities at p=1e-3 (M2) for the local, joint, flagged and verified-cat rounds, within 1% of the published values", ok_reg)
e_in = E2['J flag'].at(RT(1e-3, idle=1e-3, **{'in': 1e-3}))
check("REGRESSION: switching idle and incoming faults on (version 0.9 model M3) reproduces its flagged-round silent probability 3.93e-4 at p=1e-3 within 1%", abs(e_in['silent'] / 3.93e-4 - 1) < 0.01)
print("  erratum list for version 0.9: none required by this version's checks; see page section 1 for the one clarification (the model's qubits are generic, and photonic readout is destructive).")

# =============================================================== B. feasibility structure: destructive detection and hosting
print("== B. feasibility structure: ancillas as photons, and inter-photon gate counts ==")
def comps(B):
    """connected components of ancilla qubits (edges: ancilla-ancilla two-qubit gates); also the data-ancilla gates per component"""
    anc = list(range(4, B.nq)); par = {q: q for q in anc}
    def f(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    for o in B.ops:
        if o[0] in ('CNOT', 'CZ') and o[1] >= 4 and o[2] >= 4: par[f(o[1])] = f(o[2])
    cs = defaultdict(list)
    for q in anc: cs[f(q)].append(q)
    return [sorted(v) for v in cs.values()]
def partitions(items, K):
    if not items: yield []; return
    first, rest = items[0], items[1:]
    for p in partitions(rest, K):
        for i in range(len(p)):
            if len(p[i]) < K: yield p[:i] + [[first] + p[i]] + p[i + 1:]
        yield [[first]] + p
def inter_count(B, K):
    """Destructive readout: ancillas live on their own photons, at most K ancilla qubits per photon; data photons never host ancillas.
    Returns (inter-photon two-qubit gates, ancilla photons consumed), minimised over groupings."""
    n_da = sum(1 for o in B.ops if o[0] in ('CNOT', 'CZ') and ((o[1] < 4) != (o[2] < 4)))
    tot_I = n_da; tot_ph = 0
    for c in comps(B):
        best = None
        for p in partitions(c, K):
            where = {q: gi for gi, g in enumerate(p) for q in g}
            ni = sum(1 for o in B.ops if o[0] in ('CNOT', 'CZ') and o[1] in where and o[2] in where and where[o[1]] != where[o[2]])
            cand = (ni, len(p))
            if best is None or cand < best: best = cand
        tot_I += best[0]; tot_ph += best[1]
    return tot_I, tot_ph
def inter_count_qnd(B):
    """Optimistic alternative (UNVERIFIED feasibility): a nondestructive readout exists, so an ancilla may be an extra degree of freedom of a DATA photon.
    Lower bound on inter-photon gates (host in {photon A, photon B, own photon}); QND readout itself is not costed."""
    tot = 0; extra = 0
    for c in comps(B):
        best = None
        for hosts in product(('A', 'B', None), repeat=len(c)):
            ph = {}
            for q, h in zip(c, hosts): ph[q] = h if h else ('own', q)
            def photon(q): return ('A' if q < 2 else 'B') if q < 4 else ph[q]
            ni = sum(1 for o in B.ops if o[0] in ('CNOT', 'CZ') and (o[1] in c or o[2] in c) and photon(o[1]) != photon(o[2]))
            ne = len({ph[q] for q in c if isinstance(ph[q], tuple)})
            cand = (ni, ne)
            if best is None or cand < best: best = cand
        tot += best[0]; extra += best[1]
    return tot, extra
NI = {}
print("  inter-photon two-qubit gates per round (and ancilla photons consumed), destructive readout, K ancilla qubits per ancilla photon; last column: nondestructive-readout lower bound")
print("      method                       total 2q   K=1          K=2          K=5          QND lower bound")
for nm in NAMES:
    B = BR[nm]; row = {K: inter_count(B, K) for K in (1, 2, 5)}; q_ = inter_count_qnd(B); NI[nm] = (row, q_)
    print(f"      {nm:27s} {resources(B)['n2q']:8d}   " + "   ".join(f"{row[K][0]:3d} ({row[K][1]:2d} ph)" for K in (1, 2, 5)) + f"   {q_[0]:3d} ({q_[1]} ph)")

# =============================================================== C. probabilistic inter-photon gates
print("== C. probabilistic inter-photon gates ==")
SS = [1.0, 0.75, 0.5, 0.25, 1 / 9]
def abort_attempts(n, s):   # expected number of gate attempts per COMPLETED round when a failure aborts the round and everything restarts
    if s == 1.0: return float(n)
    return (1 - s ** n) / ((1 - s) * s ** n)
print("  completion probability s^n of one round when ANY failed inter-photon gate aborts it (K=1 hosting):")
print("      method                          n_I  " + "".join(f"s={s:<7.3g}" for s in SS))
for nm in NAMES:
    n = NI[nm][0][1][0]; print(f"      {nm:27s} {n:6d}  " + "".join(f"{s ** n:<9.2e}" for s in SS))
print("  expected inter-photon gate ATTEMPTS per completed round: abort-and-restart | benign-retry (each failed gate simply repeated, data undisturbed):")
for nm in ('L conv (baseline)', 'J conv', 'J flag', 'J cat (verified)'):
    n = NI[nm][0][1][0]
    print(f"      {nm:27s} " + "  ".join(f"s={s:.3g}: {abort_attempts(n, s):9.1f} | {n / s:6.1f}" for s in SS[1:]))

# =============================================================== D. photon loss
print("== D. photon loss: heralded and unheralded ==")
LM = ['L conv (baseline)', 'J conv', 'J flag', 'J cat (verified)']
EL = {nm: Exact2(BR[nm], ROUNDS[nm][1], loss=True) for nm in LM}
NDA = {nm: sum(1 for o in BR[nm].ops if o[0] in ('CNOT', 'CZ') and ((o[1] < 4) != (o[2] < 4))) for nm in LM}
print("  data-photon participations per round (loss opportunities for data):", NDA)
P_GATE = 1e-3
LOSSQ = [1e-3, 1e-2, 5e-2]
DL = {}
print(f"  gate faults at p={P_GATE:g}; loss probability q per photon per two-qubit gate; data loss LATENT (found at final readout) unless stated; ancilla loss HERALDED by a missing click (h=1) or not (h=0)")
print("      method                    q      survival(data,latent)  heralded-ancilla-loss | silent(h=1)  rejected(h=1)  usable(h=1)  | silent(h=0)  rejected(h=0)  usable(h=0)")
for nm in LM:
    for q in LOSSQ:
        S = (1 - q) ** NDA[nm]; row = {}
        for h in (1.0, 0.0):
            e = EL[nm].at(RT(P_GATE, la_h=q * h, la_u=q * (1 - h)))
            acc = e.get('silent', 0) + e.get('accept_damaged', 0) + e.get('accept_clean', 0)
            row[h] = (e.get('silent', 0), e['reject'] + e.get('herald', 0), acc * S, e.get('herald', 0))
        DL[(nm, q)] = row
        print(f"      {nm:24s} {q:<7g} {S:12.4f}           {row[1.0][3]:11.4f}        | {row[1.0][0]:10.2e}  {row[1.0][1]:12.4f}  {row[1.0][2]:10.4f}   | {row[0.0][0]:10.2e}  {row[0.0][1]:12.4f}  {row[0.0][2]:10.4f}")
WL = {}
print("  worst case: data loss UNHERALDED (the lost photon's two axes become a random Pauli, nothing flags it), ancilla loss heralded")
for nm in LM:
    WL[nm] = [EL[nm].at(RT(P_GATE, ld=q, la_h=q))['silent'] for q in LOSSQ]
    print(f"      {nm:24s} silent at q={LOSSQ}: " + ", ".join(f"{x:.2e}" for x in WL[nm]))

# =============================================================== E. biased noise and basis-dependent readout
print("== E. biased noise across axes and verification resources; basis-dependent readout ==")
BM = ['L conv (baseline)', 'J conv', 'J flag', 'J cat (verified)', 'J ZZZZ only (partial)']
BS = {}
print("  silent-logical probability per round at p=1e-3, version 0.9 model M3 (gate, measurement, idle and incoming faults); the weight b multiplies the Z (or X) Pauli at faulted locations; b=1 is version 0.9")
print("      kind  scope        b     " + "".join(f"{nm[:18]:>20s}" for nm in BM) + "   lowest")
for kind in ('Z', 'X'):
    for scope in ('all', 'data', 'anc'):
        for b in (1, 10, 100):
            if b == 1 and (kind, scope) != ('Z', 'all'): continue
            bias = {'data': (kind, b if scope in ('all', 'data') else 1), 'anc': (kind, b if scope in ('all', 'anc') else 1)}
            row = {}
            for nm in BM:
                ex_ = Exact2(BR[nm], ROUNDS[nm][1], bias=bias)
                row[nm] = ex_.at(RT(1e-3, idle=1e-3, **{'in': 1e-3}))['silent']
            BS[(kind, scope, b)] = row
            low = min(row, key=row.get)
            print(f"      {kind}     {scope:5s}   {b:>4d}  " + "".join(f"{row[nm]:20.2e}" for nm in BM) + f"   {low}")
print("  basis-dependent readout (gate faults p=1e-3, Z-basis readout flip 1e-3, X-basis readout flip m):")
RD = {}
for nm in ('L conv (baseline)', 'J conv', 'J flag', 'J ZZZZ only (partial)'):
    for m in (1e-3, 1e-2, 3e-2):
        e = E2[nm].at({'g': 1e-3, 'mz': 1e-3, 'mx': m}); RD[(nm, m)] = e
    print(f"      {nm:24s} " + "  ".join(f"mx={m:g}: silent {RD[(nm, m)]['silent']:.2e}, reject {RD[(nm, m)]['reject']:.4f}" for m in (1e-3, 1e-2, 3e-2)))

# =============================================================== F. repeated rounds and accumulated damage
print("== F. repeated rounds: accumulated damage against no verification ==")
def build_T(nm, p):
    ex_ = E2[nm]; P = ex_.dist({'g': p, 'mz': p, 'mx': p}); T = defaultdict(lambda: [0.0] * 256); mask = (1 << (ex_.nd - 1)) - 1
    for f, pr in enumerate(P):
        if pr == 0.0: continue
        dv = f & mask; ef = ((f >> ex_.nd) & 15) | (((f >> (ex_.nd + 4)) & 15) << 4); T[dv][ef] += pr
    return T
def syn_table(nm):
    B = BR[nm]; t = []
    for e in range(256):
        rec, _, _ = run_from(B.ops, 0, e & 15, e >> 4); dv = 0
        for j, m in enumerate(B.dets):
            if pop(rec & m) & 1: dv |= 1 << j
        t.append(dv)
    return t
def incoming(dist, p):
    for q in range(4):
        fs = [(0, 1 - p)] + [((u[0] << q) | ((u[1] << q) << 4), p / 3) for u in P1]; new = [0.0] * 256
        for e, pe in enumerate(dist):
            if pe:
                for f, pf in fs: new[e ^ f] += pe * pf
        dist = new
    return dist
def summarize(dist, code):
    r = {'clean': 0.0, 'pending': 0.0, 'silent': 0.0}
    for e, m in enumerate(dist):
        if m: r[{'none': 'clean', 'harmless': 'clean', 'detected': 'pending', 'logical': 'silent'}[CT[code][(e & 15, e >> 4)]]] += m
    return r
RM = ['L conv (baseline)', 'J conv', 'J flag', 'J cat (verified)']
SYN = {nm: syn_table(nm) for nm in RM}
RND = {}
RLIST = (1, 5, 20); PR = (1e-4, 1e-3, 1e-2)
for p in PR:
    for nm in RM:
        T = build_T(nm, p); dist = [0.0] * 256; dist[0] = 1.0; code = ROUNDS[nm][1]
        for r in range(1, max(RLIST) + 1):
            dist = incoming(dist, p); new = [0.0] * 256; syn = SYN[nm]
            for e0, m in enumerate(dist):
                if m:
                    row = T.get(syn[e0])
                    if row:
                        for ef, t in enumerate(row):
                            if t: new[e0 ^ ef] += m * t
            dist = new
            if r in RLIST: RND[(nm, p, r)] = (sum(dist), summarize(dist, code))
    for code, key in (('L', 'none-L'), ('J', 'none-J')):
        dist = [0.0] * 256; dist[0] = 1.0
        for r in range(1, max(RLIST) + 1):
            dist = incoming(dist, p)
            if r in RLIST:
                sm = summarize(dist, code); RND[(key, p, r)] = (1.0, sm)
print("  incoming data faults (probability p per axis per round, uniform Pauli) plus the round's own gate and measurement faults (model M2); a rejected round ends the run")
print("  columns: P(run still accepted) | accepted AND damaged = silent + pending (pending damage would show in the next round) | accepted and silent-wrong")
for p in PR:
    print(f"  p = {p:g}")
    print("      method                         " + "".join(f"R={r:<3d} accepted  damaged   silent    " for r in RLIST))
    for nm in RM:
        print(f"      {nm:27s} " + "".join(f"{RND[(nm, p, r)][0]:>13.4f}  {RND[(nm, p, r)][1]['pending'] + RND[(nm, p, r)][1]['silent']:8.4f}  {RND[(nm, p, r)][1]['silent']:8.2e}  " for r in RLIST))
    for code in ('L', 'J'):
        k = 'none-' + code
        print(f"      {'no verification (stabilizers of ' + code + ')':27s} " + "".join(f"{1.0:>13.4f}  {RND[(k, p, r)][1]['pending'] + RND[(k, p, r)][1]['silent']:8.4f}  {RND[(k, p, r)][1]['silent']:8.2e}  " for r in RLIST))

# consistency check of the repeated-round DP against the exact single-round engine
_e1 = E2['J flag'].at({'g': 1e-3, 'mz': 1e-3, 'mx': 1e-3, 'in': 1e-3})
_acc = _e1['silent'] + _e1['accept_damaged'] + _e1['accept_clean']
check("CONSISTENCY: the repeated-round recursion at R=1 equals the exact single-round engine with incoming faults switched on (flagged joint, p=1e-3): accepted mass and silent probability agree to 1e-9",
      abs(RND[('J flag', 1e-3, 1)][0] - _acc) < 1e-9 and abs(RND[('J flag', 1e-3, 1)][1]['silent'] - _e1['silent']) < 1e-9)

# =============================================================== G. coherent error amplification with reference preparations
print("== G. coherent error amplification ==")
def sv_cphase(v, a, b, phi): return [x * complex(math.cos(phi), math.sin(phi)) if ((i >> a) & 1 and (i >> b) & 1) else x for i, x in enumerate(v)]
amp_ok = True
for d in (0.01, 0.1, 0.4):
    for N in (1, 5, 50):
        v = [0j] * 4; v[2] = v[3] = 1 / math.sqrt(2)
        a_ = list(v); i_ = list(v)
        for _ in range(N): a_ = sv_cphase(a_, 0, 1, math.pi + d); i_ = sv_cphase(i_, 0, 1, math.pi)
        click = 1 - abs(sum(x.conjugate() * y for x, y in zip(i_, a_))) ** 2
        amp_ok &= abs(click - math.sin(N * d / 2) ** 2) < 1e-12
check("N consecutive applications of the same gate with a constant angle error d turn the reference click probability into exactly sin^2(N d/2) (state-vector check, d in 0.01, 0.1, 0.4 and N in 1, 5, 50)", amp_ok)
def _pmf_cdf_lt(R, P, c):
    """P(Bin(R,P) < c), by recurrence on the pmf (exact; c is small whenever this is used)"""
    if P <= 0: return 1.0 if c > 0 else 0.0
    if P >= 1: return 0.0 if c <= R else 1.0
    lq = math.log1p(-P); lp = math.log(P); s = 0.0
    for k in range(0, min(c, R + 1)):
        s += math.exp(math.lgamma(R + 1) - math.lgamma(k + 1) - math.lgamma(R - k + 1) + k * lp + (R - k) * lq)
    return min(s, 1.0)
def detect_ok(R, P0, P1, alpha=0.05, power=0.95):
    """Is there a click-count threshold c with P(>=c clicks | no error) <= alpha and P(>=c clicks | error) >= power?"""
    if R * min(P0, 1 - P0) >= 60 and R * min(P1, 1 - P1) >= 60:       # normal approximation, mean large
        za, zb = 1.645, 1.645
        return (za * math.sqrt(P0 * (1 - P0)) + zb * math.sqrt(P1 * (1 - P1))) * math.sqrt(R) <= (P1 - P0) * R
    for c in range(0, 4000):
        if 1 - _pmf_cdf_lt(R, P0, c) <= alpha:
            return 1 - _pmf_cdf_lt(R, P1, c) >= power
        if c > R: return False
    return False
def runs_needed(P0, P1):
    R = 1
    while not detect_ok(R, P0, P1): R = max(R + 1, int(R * 1.02))
    lo, hi = max(1, int(R / 1.02) - 1), R            # refine inside the last 2% step (assumes local monotonicity)
    while lo < hi:
        mid = (lo + hi) // 2
        if detect_ok(mid, P0, P1): hi = mid
        else: lo = mid + 1
    return hi
def click_probs(d, N, eps):
    b = (1 - (1 - eps) ** N) / 2; s = math.sin(N * d / 2) ** 2
    return b, b + s - 2 * b * s
AMP = {}
print("  detecting a constant angle error d against stochastic noise: each gate use adds an independent error with probability eps, which flips the reference outcome with probability 1/2 (ASSUMED);")
print("  decision rule: report an error when the click count reaches a threshold with at most 5% false alarms; runs needed for 95% detection (at eps=0 this is exactly the version 0.9 criterion);")
print("  N = consecutive applications of the gate per run, taken from powers of two up to pi/d; runs are searched in 2% steps (normal approximation only when both means exceed 60)")
print("      d       eps        N=1 runs   best N    runs   total gate uses   saving in gate uses over N=1")
for d in (0.01, 0.03, 0.1):
    for eps in (0.0, 1e-4, 1e-3, 1e-2):
        b0, p0 = click_probs(d, 1, eps); r1 = runs_needed(b0, p0); best = None; N = 1
        while N <= math.pi / d:
            Q0, Q1 = click_probs(d, N, eps)
            if Q1 > Q0 + 1e-12:
                rr = runs_needed(Q0, Q1)
                if best is None or rr * N < best[2]: best = (N, rr, rr * N)
            N *= 2
        AMP[(d, eps)] = (r1, best)
        print(f"      {d:<6g}  {eps:<8g} {r1:>11d}  {best[0]:7d}  {best[1]:8d}  {best[2]:14d}   {r1 / best[2]:10.1f}x")
b1, c1_ = click_probs(0.03, 4, 0.0); b2, c2_ = click_probs(0.03, 8, 0.0); b3, c3_ = click_probs(0.0, 4, 1e-3); b4, c4_ = click_probs(0.0, 8, 1e-3)
print(f"  signature of a COHERENT error: doubling N multiplies the click probability by about 4 ({c2_ / c1_:.2f} here) whereas stochastic noise multiplies it by about 2 ({c4_ / c3_:.2f} here)")


alt = [0j] * 4; alt[2] = alt[3] = 1 / math.sqrt(2); ide = list(alt)
for k in range(50): alt = sv_cphase(alt, 0, 1, math.pi + (0.01 if k % 2 == 0 else -0.01)); ide = sv_cphase(ide, 0, 1, math.pi)
click_alt = 1 - abs(sum(x.conjugate() * y for x, y in zip(ide, alt))) ** 2
R50 = runs_needed(*click_probs(0.01, 50, 0.0))
print(f"  user's example (d=0.01, 50 consecutive gates, no stochastic noise): {R50} runs, {R50 * 50} gate uses; an error that ALTERNATES in sign on successive uses gives click probability {click_alt:.1e} after 50 uses (nothing accumulates)")

# =============================================================== H. one measurement mechanism, several purposes
print("== H. one measurement mechanism, several purposes ==")
def pauli_class(P, code):
    gens = LG if code == 'L' else JG; gf = LF if code == 'L' else JF
    if anti(P, gens): return 'disturbs checks'
    return 'stabilizer' if P in gf else 'logical'
HC = {}
for code in ('L', 'J'):
    cnt = defaultdict(int); mw = {}
    for P in ALL:
        if P == (0, 0): continue
        c = pauli_class(P, code); cnt[c] += 1; mw[c] = min(mw.get(c, 9), weight(P))
    HC[code] = (dict(cnt), mw)
    print(f"  code {code}: non-identity Pauli products by what measuring them does to code-space states: {dict(cnt)}; minimum weight per class: {mw}")
def logical_state(code):
    gens = LG if code == 'L' else JG
    v = sv_norm(project_code([rc() for _ in range(16)], [(e[0], e[1], e[2]) for e in gens])); return v
def measure_effect(v, P):
    pv = sv_pauli(v, P[0], P[1]); ev = sum((a.conjugate() * b) for a, b in zip(v, pv)).real
    fid = 0.0
    for sgn in (1, -1):
        pr = (1 + sgn * ev) / 2
        if pr > 1e-12:
            post = [(a + sgn * b) / 2 for a, b in zip(v, pv)]; post = [x / math.sqrt(pr) for x in post]
            fid += pr * abs(sum(a.conjugate() * b for a, b in zip(v, post))) ** 2
    return ev, fid
SH = {}
for code in ('L', 'J'):
    for cls in ('stabilizer', 'logical', 'disturbs checks'):
        Ps = [P for P in ALL if P != (0, 0) and pauli_class(P, code) == cls]; evs = []; fids = []; keep = []
        for _ in range(60):
            v = logical_state(code); P = random.choice(Ps); ev, fid = measure_effect(v, P)
            gens = LG if code == 'L' else JG
            pv = sv_pauli(v, P[0], P[1]); post = [(a + b) / 2 for a, b in zip(v, pv)]; nrm = math.sqrt(sum(abs(x) ** 2 for x in post))
            evs.append(abs(ev)); fids.append(fid)
            if nrm > 1e-6:
                post = [x / nrm for x in post]; keep.append(min(sum((a.conjugate() * b) for a, b in zip(post, sv_pauli(post, e[0], e[1]))).real * e[2] for e in gens))
        SH[(code, cls)] = (sum(evs) / len(evs), sum(fids) / len(fids), (min(keep) if keep else None))
        print(f"      {code} {cls:16s}: mean |<P>| {SH[(code, cls)][0]:.3f}; mean fidelity of the post-measurement state with the pre-measurement state {SH[(code, cls)][1]:.3f}; lowest check value afterwards {SH[(code, cls)][2]}")
check("DERIVED: a measurement leaves unknown code-space information undisturbed exactly when the measured Pauli is a stabilizer element (outcome certain, fidelity 1); a logical-operator measurement has random outcomes and disturbs the state (fidelity below 1); a Pauli that anticommutes with a check also takes the state out of the code (check value below +1)",
      all(abs(SH[(c, 'stabilizer')][1] - 1) < 1e-9 and abs(SH[(c, 'stabilizer')][0] - 1) < 1e-9 and SH[(c, 'logical')][1] < 0.97 and SH[(c, 'disturbs checks')][2] < 1 - 1e-6 for c in ('L', 'J')))
check("counts: 3 stabilizer, 60 logical and 192 check-disturbing non-identity Pauli products for both the local and joint code; cheapest stabilizer weight 2 (local) versus 4 (joint); cheapest logical weight 1 versus 2",
      all(HC[c][0] == {'stabilizer': 3, 'logical': 60, 'disturbs checks': 192} for c in ('L', 'J')) and HC['L'][1]['stabilizer'] == 2 and HC['J'][1]['stabilizer'] == 4 and HC['L'][1]['logical'] == 1 and HC['J'][1]['logical'] == 2)

# =============================================================== I. capability report version 2 and selection under physical profiles
print("== I. capability report v2 and selection under physical profiles ==")
def single_axis_detected(code): return sum(1 for q in range(4) for pz in ((1, 0), (0, 1), (1, 1)) if CT[code][(pz[0] << q, pz[1] << q)] == 'detected')
CM = ['L conv (baseline)', 'J conv', 'J flag', 'J cat (verified)', 'J ZZZZ only (partial)']
ELC = {nm: (EL[nm] if nm in EL else Exact2(BR[nm], ROUNDS[nm][1], loss=True)) for nm in CM}
PROF = {
  'P0 ideal (version 0.9)':                  dict(p=1e-3, q=0.0,  s=1.0,  mode='none'),
  'P1 loss only (q=1e-2, ancilla heralded)':  dict(p=1e-3, q=1e-2, s=1.0,  mode='none'),
  'P2 s=0.5, failures benign, retried':       dict(p=1e-3, q=1e-2, s=0.5,  mode='retry'),
  'P3 s=0.75, any failure aborts the round':  dict(p=1e-3, q=1e-2, s=0.75, mode='abort'),
}
def cap_row(nm, pf):
    n_I, ph = NI[nm][0][1]; nda = sum(1 for o in BR[nm].ops if o[0] in ('CNOT', 'CZ') and ((o[1] < 4) != (o[2] < 4)))
    e = ELC[nm].at(RT(pf['p'], la_h=pf['q'])); acc = e.get('silent', 0) + e.get('accept_damaged', 0) + e.get('accept_clean', 0)
    comp = pf['s'] ** n_I if pf['mode'] == 'abort' else 1.0
    usable = acc * (1 - pf['q']) ** nda * comp
    attempts = abort_attempts(n_I, pf['s']) if pf['mode'] == 'abort' else (n_I / pf['s'] if pf['mode'] == 'retry' else float(n_I))
    return dict(config=nm, silent=e.get('silent', 0.0), unusable=1 - usable, attempts=attempts, photons=ph,
                coverage=single_axis_detected(ROUNDS[nm][1]), completion=comp, inter_photon_gates=n_I, physical_cost=None)
def dom(a, b, keys, mx=('coverage',)):
    better = False
    for k in keys:
        x, y = a[k], b[k]
        if k in mx: x, y = -x, -y
        if y > x + 1e-300: return False
        if y < x: better = True
    return better
def pick(rows, req, keys):
    feas = [r for r in rows if all((op == '<=' and r[k] <= lim) or (op == '>=' and r[k] >= lim) for k, (op, lim) in req.items())]
    par = [a for a in feas if not any(dom(a, b, keys) for b in feas if b is not a)]
    return [f['config'] for f in feas], [q_['config'] for q_ in par]
KEYS2 = ['silent', 'unusable', 'attempts', 'photons', 'coverage']
REQ2 = {'A: silent <= 1e-4, unusable <= 20%': {'silent': ('<=', 1e-4), 'unusable': ('<=', 0.2)},
        'B: silent <= 1e-3, attempts <= 12': {'silent': ('<=', 1e-3), 'attempts': ('<=', 12)}}
SEL2 = {}
print("  silent is per round that runs to completion; 'unusable' = rejected, heralded or lost; 'attempts' = inter-photon gate attempts per completed round (retry or abort mode as stated); photons = ancilla photons (K=1); coverage = single-axis faults detected of 12")
for pn, pf in PROF.items():
    rows = [cap_row(nm, pf) for nm in CM]; SEL2[pn] = {}
    print(f"  profile {pn}")
    for r in rows: print(f"      {r['config']:24s} silent {r['silent']:.2e}  unusable {r['unusable']:.3f}  attempts {r['attempts']:11.1f}  photons {r['photons']:2d}  completion {r['completion']:.3g}  coverage {r['coverage']}")
    for rn, rq in REQ2.items():
        f, par = pick(rows, rq, KEYS2); SEL2[pn][rn] = (f, par); print(f"      requirement {rn}: feasible {f} -> Pareto {par}")
print("  provisional capability report v2 row (flagged joint, profile P1); the cost fields stay empty (A02):")
print("     ", {k: (round(v, 6) if isinstance(v, float) else v) for k, v in cap_row('J flag', PROF['P1 loss only (q=1e-2, ancilla heralded)']).items()})

# =============================================================== J. result checks (written after reading the output of A to I)
print("== J. result checks ==")
def mc2(nm, bias, rates, n):
    B = BR[nm]; ex_ = Exact2(B, ROUNDS[nm][1], bias=bias, loss=True); locs = enum_w(B.ops, bias, True); nd = ex_.nd; packed = []
    for typ, opts in locs:
        r = rates.get(typ, 0.0)
        if r == 0.0: continue
        tot = sum(o[3] for o in opts); pk = []; cum = 0.0
        for rec, ex2, ez2, w, hr in opts:
            dv = 0
            for j, m in enumerate(B.dets):
                if pop(rec & m) & 1: dv |= 1 << j
            cum += w / tot; pk.append((cum, dv | (hr << (nd - 1)) | (ex2 << nd) | (ez2 << (nd + 4))))
        packed.append((r, pk))
    cnt = defaultdict(int)
    for _ in range(n):
        f = 0
        for r, pk in packed:
            if random.random() < r:
                u = random.random()
                for cum, sg in pk:
                    if u <= cum: f ^= sg; break
                else: f ^= pk[-1][1]
        dv, hr, cl, _ = ex_.cls[f]
        cnt['herald' if hr else ('silent' if (dv == 0 and cl == 'logical') else ('acc_dam' if (dv == 0 and cl == 'detected') else ('rej' if dv else 'clean')))] += 1
    return ex_, {k: v / n for k, v in cnt.items()}
bias_t = {'data': ('Z', 8.0), 'anc': ('X', 5.0)}; rates_t = RT(0.03, la_h=0.04, la_u=0.02, ld=0.03, idle=0.01, **{'in': 0.02})
ex_t, m_t = mc2('J flag', bias_t, rates_t, 40000); e_t = ex_t.at(rates_t); okmc = True
for k, kk in (('silent', 'silent'), ('acc_dam', 'accept_damaged'), ('herald', 'herald'), ('rej', 'reject')):
    sd = math.sqrt(max(e_t[kk] * (1 - e_t[kk]), 1e-12) / 40000); okmc &= abs(m_t.get(k, 0.0) - e_t[kk]) < 5 * sd + 1e-9
check("VALIDATION of the generalized exact engine (bias weights, heralded and unheralded loss locations, idle and incoming faults): 40,000 Monte Carlo rounds of the flagged joint circuit with Z-biased data, X-biased ancillas and all mechanisms on agree with the exact distribution within 5 standard errors for silent, accepted-damaged, heralded and rejected", okmc)

def inv(nm, K): return NI[nm][0][K][0]
check("FEASIBILITY (DERIVED, on the assumption that photon detection destroys the photon): every data-ancilla gate is then an inter-photon gate, so one round needs at least 4 inter-photon gates (local) or 8 (joint); the local geometry's advantage is only 2x in inter-photon gates, not 'no inter-photon gates'",
      inv('L conv (baseline)', 1) == 4 and inv('J conv', 1) == 8 and all(inv(n, 5) >= 4 for n in NAMES))
check("a flag that shares its ancilla's photon (K=2) costs nothing extra in inter-photon gates (8, as conventional joint) but needs a second axis on that photon; with one qubit per ancilla photon it costs 12; the verified cat needs 18 (K=1), 14 (K=2) or 8 (K=5)",
      inv('J flag', 2) == 8 and inv('J flag', 1) == 12 and inv('J cat (verified)', 1) == 18 and inv('J cat (verified)', 2) == 14 and inv('J cat (verified)', 5) == 8)
check("LOWER BOUND (UNVERIFIED feasibility): if a nondestructive readout existed so that an ancilla could be an extra degree of freedom of a data photon, the inter-photon gates would fall to 0 (local) and 4 (joint, conventional or flagged); the nondestructive readout itself is not costed",
      NI['L conv (baseline)'][1][0] == 0 and NI['J conv'][1][0] == 4 and NI['J flag'][1][0] == 4)
check("PROBABILISTIC GATES: completion probability s^n_I at s=0.5 is 1/16 (local), 1/256 (joint), 2^-12 (flagged), 2^-18 (verified cat); expected attempts per completed round when a failure aborts the round: 30, 510, 8190, 524286; if failures were benign and retried: 8, 16, 24, 36",
      near(0.5 ** inv('L conv (baseline)', 1), 1 / 16) and near(0.5 ** inv('J conv', 1), 1 / 256) and near(0.5 ** inv('J flag', 1), 2.0 ** -12) and near(0.5 ** inv('J cat (verified)', 1), 2.0 ** -18)
      and [round(abort_attempts(inv(n, 1), 0.5)) for n in ('L conv (baseline)', 'J conv', 'J flag', 'J cat (verified)')] == [30, 510, 8190, 524286]
      and [inv(n, 1) / 0.5 for n in ('L conv (baseline)', 'J conv', 'J flag', 'J cat (verified)')] == [8, 16, 24, 36])
check("NEGATIVE RESULT: if a failed inter-photon gate disturbs the data photon, a joint round completes with probability 0.100 at s=0.75 and 0.0039 at s=0.5, the flagged round 0.032 and 0.00024, so verification of unknown data is only usable with gates whose failure is heralded AND benign; whether such gates exist at useful success probability is open",
      near(0.75 ** 8, 0.1001, 1e-4) and near(0.5 ** 8, 0.00390625) and near(0.75 ** 12, 0.0317, 1e-4) and near(0.5 ** 12, 2.0 ** -12))
check("LOSS, data photons latent: survival through one round is 0.9606 (local) and 0.9227 (joint, flagged and verified cat alike) at q=1e-2: data loss exposure follows the number of data-ancilla gates, not the number of ancilla resources",
      near((1 - 1e-2) ** NDA['L conv (baseline)'], 0.9606, 1e-4) and all(near((1 - 1e-2) ** NDA[n], 0.9227, 1e-4) for n in ('J conv', 'J flag', 'J cat (verified)')))
check("LOSS, ancilla photons heralded by a missing click: the round-rejection share caused by loss grows with ancilla resources: at q=1e-2 it is 0.0388 (local), 0.0746 (joint), 0.1381 (flagged), 0.2160 (verified cat); usable rounds (accepted and no data loss) fall to 0.918, 0.847, 0.783, 0.701",
      all(near(DL[(n, 1e-2)][1.0][3], v, 6e-4) for n, v in zip(LM, (0.0388, 0.0746, 0.1381, 0.2160))) and all(near(DL[(n, 1e-2)][1.0][2], v, 6e-4) for n, v in zip(LM, (0.9183, 0.8465, 0.7825, 0.7008))))
check("NEGATIVE RESULT: if ancilla loss is NOT heralded (the lost ancilla is replaced by a random qubit), silent damage rises about 10 times for the local round and about 60 times for the flagged round at q=1e-2 (5.44e-3 versus 5.11e-4; 1.20e-4 versus 1.98e-6): heralding the ancilla is worth more than the flag",
      DL[('L conv (baseline)', 1e-2)][0.0][0] > 8 * DL[('L conv (baseline)', 1e-2)][1.0][0] and DL[('J flag', 1e-2)][0.0][0] > 40 * DL[('J flag', 1e-2)][1.0][0])
check("NEGATIVE RESULT: if data-photon loss is unheralded (random Pauli on the lost photon's axes), the flagged round's silent probability at q=1e-3 is about 420 times its loss-free value (9.7e-4 versus 2.3e-6) and only 10 to 30% below the conventional joint round's (ratio between 0.7 and 0.95 at every q tested); the loss floor, not the extraction design, sets the silent rate",
      WL['J flag'][0] > 100 * E2['J flag'].at(RT(1e-3))['silent'] and all(0.7 < WL['J flag'][i] / WL['J conv'][i] < 0.95 for i in range(3)) and WL['J flag'][0] > 5e-4)
check("BIAS (Z-biased noise, all qubits, b=100, M3 at p=1e-3): the flagged joint round is the best of the five, and the local round has about 20 times its silent probability; the local code is blind to Z",
      min(BS[('Z', 'all', 100)], key=BS[('Z', 'all', 100)].get) == 'J flag' and BS[('Z', 'all', 100)]['L conv (baseline)'] > 20 * BS[('Z', 'all', 100)]['J flag'])
check("BIAS REVERSAL: with X-biased noise on all qubits (b=100) the local round (and the ZZZZ-only partial round) have lower silent probability than every joint round (3.98e-4 and 3.77e-4 versus 1.25e-3 flagged and 1.36e-3 conventional): the version 0.9 ranking is not robust to the noise bias, and a configuration choice that follows the bias is justified",
      BS[('X', 'all', 100)]['L conv (baseline)'] < BS[('X', 'all', 100)]['J flag'] and BS[('X', 'all', 100)]['L conv (baseline)'] < BS[('X', 'all', 100)]['J conv'] and BS[('X', 'all', 100)]['J ZZZZ only (partial)'] < BS[('X', 'all', 100)]['J flag'])
check("BIAS ON THE VERIFICATION RESOURCES ALONE: with X- or Z-biased ancillas and unbiased data, the flagged round is the best of the five at b=10 and b=100 (its flag catches the hook that bias makes common); with Z-biased DATA the conventional joint round beats the flagged one (7.5e-4 versus 1.3e-3 at b=100) because the longer flagged round exposes the data to more idle Z faults",
      all(min(BS[(k, 'anc', b)], key=BS[(k, 'anc', b)].get) == 'J flag' for k in ('Z', 'X') for b in (10, 100)) and BS[('Z', 'data', 100)]['J conv'] < BS[('Z', 'data', 100)]['J flag'])
check("READOUT ASYMMETRY (illustrative, the factor is ASSUMED): if X-basis readout flips 30 times as often as Z-basis readout (3e-2 against 1e-3), the flagged joint round's rejection rises from 0.0161 to 0.0723 and its silent probability about 2.6 times, the conventional joint round's rejection from 0.0086 to 0.0373, while the local round and the ZZZZ-only partial round, which use only Z-basis readout, do not change at all",
      near(RD[('J flag', 1e-3)]['reject'], 0.0161, 2e-4) and near(RD[('J flag', 3e-2)]['reject'], 0.0723, 3e-4) and 2.2 < RD[('J flag', 3e-2)]['silent'] / RD[('J flag', 1e-3)]['silent'] < 3.0
      and RD[('L conv (baseline)', 3e-2)]['reject'] == RD[('L conv (baseline)', 1e-3)]['reject'] and RD[('J ZZZZ only (partial)', 3e-2)]['silent'] == RD[('J ZZZZ only (partial)', 1e-3)]['silent'])
def cond_damaged(key, p, r): m, s = RND[(key, p, r)]; return (s['pending'] + s['silent']) / m
check("REPEATED ROUNDS (p=1e-3, 20 rounds, incoming faults plus the round's own faults): of the runs still accepted, 0.20% of flagged-joint runs are damaged against 3.7% for the local round and 7.7% with no verification; the price is that only 64% (flagged) or 46% (verified cat) of runs are still accepted",
      cond_damaged('J flag', 1e-3, 20) < 0.0025 and cond_damaged('L conv (baseline)', 1e-3, 20) > 0.03 and near(RND[('none-J', 1e-3, 20)][1]['pending'] + RND[('none-J', 1e-3, 20)][1]['silent'], 0.0767, 2e-4)
      and near(RND[('J flag', 1e-3, 20)][0], 0.6436, 5e-4) and near(RND[('J cat (verified)', 1e-3, 20)][0], 0.4644, 5e-4))
check("silent damage accumulates almost linearly in the number of rounds (20 rounds give 15 to 20 times the one-round value) for the joint rounds at p=1e-3: flagged 6.09e-6 to 1.12e-4, conventional joint 2.70e-4 to 4.10e-3; verification does not stop accumulation, it slows it",
      all(15 < RND[(n, 1e-3, 20)][1]['silent'] / RND[(n, 1e-3, 1)][1]['silent'] < 20 for n in ('J conv', 'J flag')))
check("NEGATIVE RESULT: at p=1e-2 over 20 rounds only 1.2% of flagged and 0.05% of verified-cat runs are still accepted (16% for the local round): detect-and-reject verification is unusable for long computations at this fault rate",
      RND[('J flag', 1e-2, 20)][0] < 0.015 and RND[('J cat (verified)', 1e-2, 20)][0] < 0.001 and 0.15 < RND[('L conv (baseline)', 1e-2, 20)][0] < 0.17)
check("COHERENT AMPLIFICATION: the user's example is reproduced (d=0.01: 119,829 single-gate runs at 95% detection; 50 consecutive gates need 48 runs and 2,400 gate uses), and larger N does better still: N=256 needs 2 runs and 512 gate uses (a factor 234 in gate uses and 59,900 in runs) in the absence of stochastic noise",
      AMP[(0.01, 0.0)][0] == 119829 and R50 == 48 and AMP[(0.01, 0.0)][1] == (256, 2, 512) and AMP[(0.03, 0.0)][0] == 13314 and AMP[(0.1, 0.0)][0] == 1198)
check("amplification survives stochastic noise in this model: with eps=1e-3 per gate use and d=0.01 the best N is 256 with 5 runs (1,280 gate uses) against 8.9 million single-gate runs; with eps=1e-2 the best N falls to 128 and the gain to about 2,600 in gate uses",
      AMP[(0.01, 1e-3)][1] == (256, 5, 1280) and AMP[(0.01, 1e-2)][1][0] == 128 and 2000 < AMP[(0.01, 1e-2)][0] / AMP[(0.01, 1e-2)][1][2] < 3000)
check("LIMIT: the signature of a coherent error is a click probability that grows about 4 times when N doubles (stochastic: 2 times), and an error that alternates in sign on successive uses never accumulates (click probability about 0 after 50 uses): amplification measures only what accumulates coherently",
      3.9 < c2_ / c1_ < 4.1 and 1.9 < c4_ / c3_ < 2.1 and click_alt < 1e-12)
check("SELECTION UNDER PHYSICAL PROFILES: requirement A (silent at most 1e-4, at most 20% unusable) has the single Pareto choice 'flagged joint' under the version 0.9 assumptions (P0) and NOTHING feasible once ancilla loss of 1e-2 is added (P1, flagged unusable 0.218, verified cat 0.299); requirement B (silent at most 1e-3, at most 12 attempts) loses the joint rounds when s=0.5 (P2) or when failures abort (P3), leaving the local round and the ZZZZ-only partial round",
      SEL2['P0 ideal (version 0.9)']['A: silent <= 1e-4, unusable <= 20%'][1] == ['J flag'] and SEL2['P1 loss only (q=1e-2, ancilla heralded)']['A: silent <= 1e-4, unusable <= 20%'][0] == []
      and sorted(SEL2['P2 s=0.5, failures benign, retried']['B: silent <= 1e-3, attempts <= 12'][1]) == sorted(['L conv (baseline)', 'J ZZZZ only (partial)'])
      and sorted(SEL2['P3 s=0.75, any failure aborts the round']['B: silent <= 1e-3, attempts <= 12'][1]) == sorted(['L conv (baseline)', 'J ZZZZ only (partial)']))
check("P3 completion probabilities: local 0.316, conventional joint 0.100, flagged 0.0317, verified cat 0.0056, partial 0.316",
      all(near(cap_row(n, PROF['P3 s=0.75, any failure aborts the round'])['completion'], v, 2e-4) for n, v in zip(CM, (0.3164, 0.1001, 0.0317, 0.0056, 0.3164))))
check("every selection set is a subset of its feasible set, and there is no combined score anywhere in the capability report (physical cost fields are None)", all(set(par) <= set(f) for d_ in SEL2.values() for f, par in d_.values()) and cap_row('J flag', PROF['P1 loss only (q=1e-2, ancilla heralded)'])['physical_cost'] is None)
print(); print("ALL PASS" if all(ok for _, ok in results) else "FAILURES")
