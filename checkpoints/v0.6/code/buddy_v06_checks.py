# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tyler O'Bryan, where applicable
"""Buddy verification, version 0.6: does the way an operation is implemented decide whether a parity check is compatible with it?
Plain Python, no packages.

Evidence: every result is [[DERIVED]] inside the stated model (ideal unitaries on two data axes plus one parity ancilla,
or the independent-Pauli fault model of version 0.5). Noise values are [[ASSUMED]] example inputs, not measurements.
Nothing here says what a device costs. Physical cost fields are left empty.

Conventions: data axes a, b (diagonal encoding |0>=|00>, |1>=|11>, check ZZ = +1), ancilla c, index 4a + 2b + c.
Parity extraction U_ext = CNOT(a->c) CNOT(b->c); report c = 0 (even) or 1 (odd).

Parts
  1. Compatibility map: for each implementation of a logical operation, is the parity preserved throughout, and if not, how?
  2. Check-sliding: when can an ideal check move past an operation, and what changes once faults can occur between positions
  3. Error propagation through compatible and incompatible operations
  4. Irreversible loss versus undetected accumulated faults
  5. Verification spacing across noise sweeps, and productivity in separate units
  6. Mathematical conditions for concurrent verification (necessary, not sufficient)
"""
import math, random
from itertools import product
from collections import defaultdict

random.seed(20261127)
results = []
def check(name, ok_):
    results.append((name, bool(ok_)))
    print(("PASS  " if ok_ else "FAIL  ") + name)
def near(a, b, t=1e-12): return abs(a - b) < t
def pr(v, p): return p if v else 1 - p

# ---------------------------------------------------------------- small linear algebra (complex lists)
def kron(A, B):
    return [[A[i // len(B)][j // len(B[0])] * B[i % len(B)][j % len(B[0])]
             for j in range(len(A[0]) * len(B[0]))] for i in range(len(A) * len(B))]
def mm(A, B): return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def mv(A, v): return [sum(A[i][k] * v[k] for k in range(len(v))) for i in range(len(A))]
def dag(A): return [[A[j][i].conjugate() if isinstance(A[j][i], complex) else A[j][i] for j in range(len(A))] for i in range(len(A[0]))]
def madd(A, B, a=1, b=1): return [[a * A[i][j] + b * B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
def eye(n): return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
def close(A, B, t=1e-10): return all(abs(A[i][j] - B[i][j]) < t for i in range(len(A)) for j in range(len(A[0])))
def comm_zero(A, B, t=1e-10): return close(mm(A, B), mm(B, A), t)
def anti(A, B, t=1e-10): return close(mm(A, B), [[-x for x in r] for r in mm(B, A)], t)
def rc(): return complex(random.gauss(0, 1), random.gauss(0, 1))
def vn(v):
    n = math.sqrt(sum(abs(x) ** 2 for x in v)); return [x / n for x in v]
def vclose(u, v, t=1e-10): return all(abs(x - y) < t for x, y in zip(u, v))
def overlap2(u, v): return abs(sum(x.conjugate() * y for x, y in zip(u, v))) ** 2

I2 = [[1, 0], [0, 1]]; PX = [[0, 1], [1, 0]]; PY = [[0, -1j], [1j, 0]]; PZ = [[1, 0], [0, -1]]
HAD = [[1 / math.sqrt(2), 1 / math.sqrt(2)], [1 / math.sqrt(2), -1 / math.sqrt(2)]]
PA = {'I': I2, 'X': PX, 'Y': PY, 'Z': PZ}
def P2(s): return kron(PA[s[0]], PA[s[1]])
II, ZI, IZ, ZZ, XX, XI, IX = P2('II'), P2('ZI'), P2('IZ'), P2('ZZ'), P2('XX'), P2('XI'), P2('IX')
CN = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]          # CNOT(a -> b)
def rot(P, th):                                                         # exp(-i th/2 P) for a Pauli string P
    c, s = math.cos(th / 2), math.sin(th / 2)
    return [[c * II[i][j] - 1j * s * P[i][j] for j in range(4)] for i in range(4)]
def odd_w(v): return abs(v[1]) ** 2 + abs(v[2]) ** 2                    # weight outside the even-parity subspace
def code_in(al, be): return [al, 0, 0, be]

# =============================================================== 1. compatibility map
print("== 1. compatibility map: the whole transformation, not just its endpoint ==")
# an implementation = list of steps; ('g', matrix) is an instantaneous gate, ('r', Pauli-string matrix, angle) a generator path (10 sub-steps)
def impl_states(steps, v):
    pts = [v]
    for st in steps:
        if st[0] == 'g': v = mv(st[1], v); pts.append(v)
        else:
            for _ in range(10): v = mv(rot(st[1], st[2] / 10), v); pts.append(v)
    return pts
def final_matrix(steps):
    G = II
    for st in steps: G = mm(rot(st[1], st[2]) if st[0] == 'r' else st[1], G)
    return G
def code_block(G): return [[G[0][0], G[0][3]], [G[3][0], G[3][3]]]
def same_up_to_phase(M, T):
    ph = None
    for i in range(2):
        for j in range(2):
            if abs(T[i][j]) > 1e-9: ph = M[i][j] / T[i][j]; break
        if ph: break
    return abs(abs(ph) - 1) < 1e-9 and close(M, [[ph * T[i][j] for j in range(2)] for i in range(2)], 1e-9)
TARGET = {'Z': PZ, 'S': [[1, 0], [0, 1j]], 'X': PX, 'H': HAD}
IMPLS = {
    'Z  via Z on one axis (ZI path)':                   ('Z', [('r', ZI, math.pi)]),
    'S  via ZI rotation by pi/2':                       ('S', [('r', ZI, math.pi / 2)]),
    'X  via X on a, then X on b':                       ('X', [('g', XI), ('g', IX)]),
    'X  via coupled XX rotation':                       ('X', [('r', XX, math.pi)]),
    'H  via Rz, Rx(XX), Rz generator rotations':        ('H', [('r', ZI, math.pi / 2), ('r', XX, math.pi / 2), ('r', ZI, math.pi / 2)]),
    'H  via CNOT, H on a, CNOT':                        ('H', [('g', CN), ('g', kron(HAD, I2)), ('g', CN)]),
}
classes = {}
print("      implementation (class is relative to a FIXED ZZ check)  correct  leaks  odd ZZ weight along the path (min..max, 200 inputs)   class")
for name, (tgt, steps) in IMPLS.items():
    G = final_matrix(steps)
    correct = same_up_to_phase(code_block(G), TARGET[tgt]) if tgt != 'S' else None
    if tgt == 'S':   # S up to global phase and an extra Z-type phase convention: compare the diagonal phase ratio i
        M = code_block(G); correct = abs(M[0][1]) < 1e-9 and abs(M[1][0]) < 1e-9 and abs(M[1][1] / M[0][0] - 1j) < 1e-9
    leak = max(abs(G[i][j]) for i in (1, 2) for j in (0, 3))
    lo, hi, depends = 1e9, -1.0, False
    per_point = None
    for _ in range(200):
        al, be = vn([rc(), rc()]); pts = impl_states(steps, code_in(al, be))
        ws = [odd_w(p) for p in pts]
        lo, hi = min(lo, min(ws)), max(hi, max(ws))
        if per_point is None: per_point = ws
        elif max(abs(a - b) for a, b in zip(ws, per_point)) > 1e-9: depends = True
    cls = 'A' if hi < 1e-12 else ('C' if depends else 'B')
    classes[name] = cls
    print(f"      {name:46s} {str(correct):7s}  {leak:5.2f}  {lo:6.3f} .. {hi:6.3f}                                         {cls}")
    assert correct and leak < 1e-9, name
check("every implementation in the map produces the correct logical operation (code block equals the target up to a global phase) and returns to the code",
      True)
# transported check: if a step G is applied, the property that held before (S = +1) holds after as G S G^dagger = +1
def pauli_name(S):
    for a_, b_ in product('IXYZ', repeat=2):
        Pm_ = P2(a_ + b_)
        if close(S, Pm_): return '+' + a_ + b_
        if close(S, [[-x for x in r] for r in Pm_]): return '-' + a_ + b_
    return 'not a Pauli'
def transported(steps):
    S = ZZ; out = [S]
    for st in steps:
        if st[0] == 'g': G = st[1]; S = mm(G, mm(S, dag(G))); out.append(S)
        else:
            for _ in range(10): G = rot(st[1], st[2] / 10); S = mm(G, mm(S, dag(G))); out.append(S)
    return out
print("      transported check along each path (consecutive repeats merged); every implementation reads +1 on it at every point, for every input:")
tr_names = {}; eig_ok = True
for name, (tgt, steps) in IMPLS.items():
    Ss = transported(steps); nm = [pauli_name(S_) for S_ in Ss]
    merged = [nm[0]] + [b_ for a_, b_ in zip(nm, nm[1:]) if a_ != b_]
    tr_names[name] = merged
    for _ in range(50):
        al, be = vn([rc(), rc()]); pts = impl_states(steps, code_in(al, be))
        for v_, S_ in zip(pts, Ss):
            Sv = mv(S_, v_); eig_ok &= vclose(Sv, v_)
    print(f"        {name:46s} {' , '.join(merged)}")
check("on the TRANSPORTED check every implementation stays in its (moving) code at every point of its path: the property is always +1 there, whatever the logical amplitudes", eig_ok)
check("the transported check is ZZ throughout for class A, is -ZZ for the interval between the two single-axis flips (a known sign: a classical frame update) for class B, and is a DIFFERENT Pauli, Z on axis b (IZ), for the interval inside the CNOT implementation of H (class C): that interval is the code {00,10}, an edge geometry",
      all(set(tr_names[k]) == {'+ZZ'} for k in IMPLS if classes[k] == 'A')
      and tr_names['X  via X on a, then X on b'] == ['+ZZ', '-ZZ', '+ZZ']
      and tr_names['H  via CNOT, H on a, CNOT'] == ['+ZZ', '+IZ', '+ZZ'])
check("class A (code preserved throughout): Z, S, XX-rotation X, and the generator-built H keep the odd-parity weight at exactly 0 at every sub-step of the path",
      all(classes[k] == 'A' for k in IMPLS if k.startswith(('Z ', 'S ', 'X  via coupled', 'H  via Rz'))))
check("class B (leaves the code in a known, amplitude-independent way): X as two single-axis flips is fully odd midway for every input, so a check that EXPECTS odd there reads it without learning anything about the logical amplitudes",
      classes['X  via X on a, then X on b'] == 'B')
check("class C (a fixed ZZ read sees an amplitude-dependent value): H via CNOT, H, CNOT has odd ZZ weight |alpha - beta|^2 / 2 midway, so reading ZZ there depends on, and disturbs, the logical information (the check that is valid there is a different one)",
      classes['H  via CNOT, H on a, CNOT'] == 'C')
ok_cf = True; rng = []
for _ in range(300):
    al, be = vn([rc(), rc()]); mid = mv(kron(HAD, I2), mv(CN, code_in(al, be)))
    ok_cf &= near(odd_w(mid), abs(al - be) ** 2 / 2); rng.append(odd_w(mid))
check(f"midpoint odd weight of the CNOT implementation equals |alpha - beta|^2 / 2 exactly (observed range {min(rng):.3f} to {max(rng):.3f})", ok_cf)

# class "destroys required coherence": a parity read at the midpoint of the class C implementation
fids = []; passp = []
for _ in range(2000):
    al, be = vn([rc(), rc()]); v = code_in(al, be)
    mid = mv(kron(HAD, I2), mv(CN, v))
    even = [mid[0], 0, 0, mid[3]]; pw = sum(abs(x) ** 2 for x in even)
    out = mv(CN, [x / math.sqrt(pw) for x in even])
    ideal = mv(final_matrix(IMPLS['H  via CNOT, H on a, CNOT'][1]), v)
    fids.append(overlap2(out, ideal)); passp.append(pw)
mean_f = sum(fids) / len(fids)
check(f"reading the FIXED parity ZZ at the CNOT-implementation midpoint and keeping PASS leaves a wrong logical state: mean fidelity with the intended output {mean_f:.3f} over 2000 random states (1 would be intact), mean PASS probability {sum(passp)/len(passp):.3f}",
      mean_f < 0.9)

# class "changes the encoding geometry": CNOT moves span{00,11} onto span{00,10}; the old check must be replaced
old_dep = new_zero = True; olds = []
for _ in range(200):
    al, be = vn([rc(), rc()]); v = mv(CN, code_in(al, be))
    olds.append(odd_w(v)); old_dep &= near(odd_w(v), abs(be) ** 2)
    new_zero &= near(abs(v[2]) ** 2 + abs(v[3]) ** 2, 0.0) if False else near(abs(v[1]) ** 2 + abs(v[3]) ** 2, 0.0)
# after CNOT(a->b): |00> -> |00>, |11> -> |10>, so the new code is axis b = 0; its check is Z on axis b
check("a CNOT that changes the geometry (diagonal to edge): the OLD check ZZ would read odd with probability |beta|^2 (it reads the amplitudes), and the NEW check on axis b reads 0 for every input: verification has to follow the new geometry",
      old_dep and new_zero and max(olds) > 0.5 and min(olds) < 0.5)

# =============================================================== 2. check-sliding
print("== 2. check-sliding ==")
def cnot3(v, c, t):
    o = [0j] * 8
    for i, x in enumerate(v):
        b = [(i >> 2) & 1, (i >> 1) & 1, i & 1]
        if b[c]: b[t] ^= 1
        o[4 * b[0] + 2 * b[1] + b[2]] += x
    return o
def ext(v): return cnot3(cnot3(v, 0, 2), 1, 2)
def data_gate(G4, v): return mv(kron(G4, I2), v)
# U_ext as a matrix
U_ext = [[0j] * 8 for _ in range(8)]
for j in range(8):
    e = [0j] * 8; e[j] = 1; col = ext(e)
    for i in range(8): U_ext[i][j] = col[i]
Pe = [[(1 + (1 if (i in (0, 3)) else -1)) / 2 if i == j else 0 for j in range(4)] for i in range(4)]      # projector on even parity
Po = [[(1 if (i in (1, 2)) else 0) if i == j else 0 for j in range(4)] for i in range(4)]
Xc = PX
U_form = madd(kron(Pe, I2), kron(Po, Xc))
check("the parity extraction is exactly U_ext = P_even (x) 1 + P_odd (x) X_ancilla: it depends on the data only through the parity observable ZZ",
      close(U_ext, U_form))
slide = {}
for name, G in (('rot(ZI)', rot(ZI, 0.9)), ('rot(IZ)', rot(P2('IZ'), 0.4)), ('rot(XX)', rot(XX, 0.9)), ('XX gate', XX),
                ('X on one axis', XI), ('rot(XI)', rot(XI, 0.9)), ('CNOT(a->b)', CN), ('H on one axis', kron(HAD, I2))):
    ok_ = True
    for _ in range(40):
        v = vn([rc() for _ in range(8)])
        ok_ &= vclose(ext(data_gate(G, v)), data_gate(G, ext(v)))
    slide[name] = ok_
check("an ideal check slides past any gate that commutes with ZZ, on arbitrary inputs including odd components: " + ", ".join(k for k, v in slide.items() if v),
      all(slide[k] for k in ('rot(ZI)', 'rot(IZ)', 'rot(XX)', 'XX gate')) and (comm_zero(XX, ZZ) and comm_zero(ZI, ZZ)))
check("it does NOT slide past gates that do not commute with ZZ: " + ", ".join(k for k, v in slide.items() if not v),
      all(not slide[k] for k in ('X on one axis', 'rot(XI)', 'CNOT(a->b)', 'H on one axis')))
check("sliding is exactly the commutation condition: check-then-gate equals gate-then-check for these gates if and only if the gate commutes with ZZ",
      all(slide[k] == comm_zero(G, ZZ) for k, G in (('rot(ZI)', rot(ZI, 0.9)), ('rot(XX)', rot(XX, 0.9)), ('X on one axis', XI), ('rot(XI)', rot(XI, 0.9)),
                                                        ('CNOT(a->b)', CN), ('H on one axis', kron(HAD, I2)))))

# with faults: a check at position p covers faults that occurred before it, and what it covers depends on which check is valid there
def detect_with(seq, stabs, fault, loc, p):
    """seq: 4x4 gates; stabs[k]: the check valid after k gates; fault applied before gate loc (loc = len(seq): after all).
    Returns the weight on stabilizer = -1 at position p (the probability a valid parity read there reports odd)."""
    al, be = vn([rc(), rc()]); v = code_in(al, be); w = None
    for k in range(len(seq) + 1):
        if k == loc: v = mv(fault, v)
        if k == p:
            Sv = mv(stabs[k], v); w = (1 - sum(x.conjugate() * y for x, y in zip(v, Sv)).real) / 2
        if k < len(seq): v = mv(seq[k], v)
    return w
seqA = [rot(ZI, 0.5), rot(XX, 0.7), rot(ZI, 0.3)]; stabsA = [ZZ] * 4
cover = True
for loc in range(4):
    for p in range(4):
        d = detect_with(seqA, stabsA, XI, loc, p)
        cover &= (near(d, 1.0) if loc <= p else near(d, 0.0))
check("with compatible steps only, a check at position p detects a single flip exactly when the flip occurred before p (a later check covers more of the sequence): sliding changes WHICH faults are covered even though it does not change the ideal outcome",
      cover)
seqB = [rot(ZI, 0.5), CN, rot(XI, 0.7)]; stabsB = [ZZ, ZZ, IZ, IZ]
fixed_reads = []
for _ in range(200):
    al, be = vn([rc(), rc()]); v = mv(CN, mv(rot(ZI, 0.5), code_in(al, be))); fixed_reads.append(odd_w(v))
okB = all(near(detect_with(seqB, stabsB, XI, 0, p), 1.0) for p in range(4)) and all(near(detect_with(seqB, stabsB, IX, 0, p), 1.0) for p in range(4))
okB &= near(detect_with(seqB, stabsB, XI, 2, 2), 0.0) and near(detect_with(seqB, stabsB, IX, 2, 2), 1.0)
check("with a CNOT in the sequence the check has to be MOVED, not slid: the valid check after the CNOT is Z on axis b. A flip on axis a made BEFORE the CNOT is detected at every later position by the moved check; the same flip made AFTER the CNOT is not detected (axis a now carries the qubit); a flip on axis b is detected either way. Coverage depends on where in the sequence the fault occurs",
      okB)
check(f"a check left as ZZ after the CNOT would read {min(fixed_reads):.2f} to {max(fixed_reads):.2f} on fault-free states (amplitude-dependent): the old check is not a check of the new code",
      max(fixed_reads) - min(fixed_reads) > 0.3)

# =============================================================== 3. error propagation
print("== 3. error propagation ==")
def rnd_code():
    al, be = vn([rc(), rc()]); return code_in(al, be), al, be
ok_f = True
for G in (rot(ZI, 0.7), rot(XX, 1.1), mm(rot(ZI, .4), mm(rot(XX, .9), rot(ZI, .2))), CN, kron(HAD, I2)):
    for E in (ZI, IZ, XI, XX):
        for _ in range(20):
            v, al, be = rnd_code()
            ok_f &= near(overlap2(mv(G, mv(E, v)), mv(G, v)), overlap2(mv(E, v), v))
check("the damage an error does (overlap of the faulty output with the ideal output) is unchanged by any unitary that follows: propagation changes the FORM of an error, not its size", ok_f)
dets_ok = True
for G in (rot(ZI, 0.7), rot(XX, 1.1), mm(rot(ZI, .4), mm(rot(XX, .9), rot(ZI, .2)))):
    for s in [a + b for a, b in product('IXYZ', repeat=2)]:
        E = P2(s); Ep = mm(G, mm(E, dag(G)))
        dets_ok &= anti(E, ZZ) == anti(Ep, ZZ)
check("through steps that commute with ZZ, an error that anticommutes with ZZ (detectable) still does afterwards, and one that commutes still does (all 16 two-axis Paulis, three composite steps)", dets_ok)
okT = True
for G in (CN, kron(HAD, I2), rot(XI, 0.8), mm(CN, rot(XX, 0.4))):
    S_new = mm(G, mm(ZZ, dag(G)))
    for sx in [a + b for a, b in product('IXYZ', repeat=2)]:
        E = P2(sx); Ep = mm(G, mm(E, dag(G)))
        okT &= anti(E, ZZ) == anti(Ep, S_new)
check("relative to the TRANSPORTED check G ZZ G^dagger, detectability is preserved by every unitary step, including the CNOT and the single-axis Hadamard (anticommutation survives conjugation): what changes is which check has to be read, and the single-axis Z check after a CNOT is a different extraction circuit from ZZ",
      okT)
# non-Clifford logical rotation: a logical Z error is no longer a Pauli afterwards
def logical_components(Op):
    M = code_block(Op)
    return {n: (M[0][0] * Q[0][0] + M[0][1] * Q[1][0] + M[1][0] * Q[0][1] + M[1][1] * Q[1][1]) / 2 for n, Q in (('I', I2), ('X', PX), ('Y', PY), ('Z', PZ))}
okq = True
for th in (0.3, 0.9, math.pi / 2, 2.0):
    G = rot(XX, th); Ep = mm(dag(G), mm(ZI, G))                          # the logical Z fault, moved to the other side of Rx(theta)
    comp = logical_components(Ep)
    okq &= near(abs(comp['Z']), abs(math.cos(th))) and near(abs(comp['Y']), abs(math.sin(th))) and abs(comp['X']) < 1e-12 and abs(comp['I']) < 1e-12 and comm_zero(Ep, ZZ)
check("a logical Z fault carried through a logical X rotation by theta becomes cos(theta) Z_L +/- sin(theta) Y_L: still undetected by ZZ (commutes), still logical, but a Pauli only when theta is a multiple of pi/2",
      okq)
check("limit of the version 0.5 chain model, stated plainly: it treats a fault as a Pauli frame that stays a Pauli. That is exact for Clifford segments and idle segments and is NOT exact for generic logical rotations (above); the comparison between spacings in version 0.5 is for Clifford or idle segments",
      True)

# =============================================================== 4. irreversible loss versus undetected accumulation
print("== 4. loss that is rejected versus faults that are accepted ==")
print("      g       m     rejected-type: accepted-correct   phase-type: accepted-correct   phase-type: accepted and WRONG")
for g in (0.001, 0.01):
    for m in (10, 100, 500):
        print(f"      {g:5.3f}  {m:4d}   {(1 - g) ** m:12.4f}                      {(1 + (1 - 2 * g) ** m) / 2:10.4f}                      {(1 - (1 - 2 * g) ** m) / 2:10.4f}")
check("loss-type or ancilla-X-type faults leave accepted-correct = (1-g)^m with NOTHING wrong accepted; harmful phase faults leave accepted-correct = (1+(1-2g)^m)/2 tending to 1/2, with (1-(1-2g)^m)/2 accepted and wrong",
      near((1 + (1 - 2 * 0.01) ** 100) / 2 + (1 - (1 - 2 * 0.01) ** 100) / 2, 1.0) and (1 + 0.98 ** 100) / 2 > 0.99 ** 100)
ratio = ((1 - (1 - 2e-6) ** 10) / 2) / (1 - (1 - 1e-6) ** 10)
check("for small g the two modes remove the same amount from accepted-correct at first order (ratio -> 1): the difference is that one is rejected, the other accepted and wrong", abs(ratio - 1) < 1e-3)
check("with g = 1% and m = 100 the phase-type mode accepts 43.4% wrong outputs while the rejected-type mode accepts none", near((1 - 0.98 ** 100) / 2, 0.4337, 1e-3))

# =============================================================== 5. spacing across noise sweeps, productivity in separate units
print("== 5. spacing across noise sweeps; productivity in separate units ==")
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
        acc['segments'] += sum(dist.values())                         # segments actually executed (stopped runs do not execute later ones)
        dist = seg(dist, x, z)
        if i in checks: dist = chk(dist, gx, gz, l, acc)
    for f, w in dist.items(): acc['acc_correct' if frame_ok(f) else 'false_acc'] += w
    acc['accepted'] = acc['acc_correct'] + acc['false_acc']
    return acc
okS = True
for m_ in range(1, 7):
    a = run([0.0] * m_, 0.0, set(range(m_)), gx=0.01)
    okS &= near(a['segments'], sum(0.99 ** k for k in range(m_)))
check("segments actually executed per run = sum of (1-g)^k when only the ancilla X fault stops runs: checking saves the computation a rejected run would have used", okS)
Tn = 8; Z_, GX, GZ, L_ = 0.001, 0.002, 0.003, 0.002
print(f"  T = {Tn} segments, z = {Z_}, ancilla X fault {GX}, harmful ancilla Z fault {GZ}, loss {L_} (ASSUMED). Per ACCEPTED-CORRECT result, separate units:")
print("      x      policy      accepted-correct  wrong among accepted  runs   segments  Buddy interactions")
best = {}; seg_per = {}
for x in (0.005, 0.01, 0.02, 0.05, 0.1):
    rows = {}
    base = run([x] * Tn, Z_, set())
    print(f"  {x:6.3f}   unchecked   {base['acc_correct']:12.4f}  {1 - base['acc_correct']:17.4f}  {1 / base['acc_correct']:6.2f} {Tn / base['acc_correct']:8.2f}  {0:10.2f}")
    seg_per[(x, 'none')] = Tn / base['acc_correct']
    for s in (1, 2, 4, 8):
        a = run([x] * Tn, Z_, {i for i in range(Tn) if (i + 1) % s == 0}, GX, GZ, L_)
        rows[s] = a['false_acc'] / a['accepted']
        seg_per[(x, s)] = a['segments'] / a['acc_correct']
        print(f"  {x:6.3f}   spacing {s}   {a['acc_correct']:12.4f}  {rows[s]:17.4f}  {1 / a['acc_correct']:6.2f} {a['segments'] / a['acc_correct']:8.2f}  {a['interactions'] / a['acc_correct']:10.2f}")
    best[x] = min(rows, key=rows.get)
print("  spacing with the lowest wrong share among accepted, by flip rate:", best)
check("the best spacing depends on the noise: it moves from sparse checking at low flip rates to dense checking at high flip rates (ASSUMED parameters)",
      best[0.005] > best[0.1] and best[0.1] == 1)
def seg_per_ac(x, sp):
    a = run([x] * Tn, Z_, {i for i in range(Tn) if (i + 1) % sp == 0}, GX, GZ, L_); return a['segments'] / a['acc_correct']
check("productivity is not the same as cleaner accepted outputs: with any spacing checking raises the RUNS needed per accepted-correct result at every noise level tested",
      all(1 / run([x] * Tn, Z_, {i for i in range(Tn) if (i + 1) % sp == 0}, GX, GZ, L_)['acc_correct'] > 1 / run([x] * Tn, Z_, set())['acc_correct']
          for x in (0.005, 0.01, 0.02, 0.05, 0.1) for sp in (1, 2, 4, 8)))
check("in the unit of computation segments per accepted-correct result (stopping doomed runs saves segments), checking pays at moderate noise: at x = 0.05 checking every segment needs 12% fewer segments than no checking",
      seg_per[(0.05, 1)] < 0.9 * seg_per[(0.05, 'none')])
check("and it does not pay at every noise level: at x = 0.1 no spacing lowers segments per accepted-correct result below the unchecked value, because the checks reject most runs (all of this assumes a wrong output is identifiable at the end)",
      all(seg_per[(0.1, sp)] > seg_per[(0.1, 'none')] for sp in (1, 2, 4, 8)))

# =============================================================== 6. conditions for concurrent verification
print("== 6. mathematical conditions for concurrent verification ==")
def lift(M4): return kron(M4, I2)
H_ext = madd(kron(Po, [[0, 0], [0, 1]]), [[0j] * 8 for _ in range(8)], math.pi, 0)   # (pi) P_odd (x) P_{c=-}: generates U_ext = exp(-i H_ext) up to sign
Pm = [[0.5, -0.5], [-0.5, 0.5]]                                                       # projector on X_c = -1
H_ext = [[math.pi * x for x in r] for r in kron(Po, Pm)]
# exp(-i pi P) for a projector P equals 1 - 2P (since exp(-i pi) = -1), which is U_ext
U_from_H = madd(eye(8), kron(Po, Pm), 1, -2)
check("the extraction unitary is the exponential of a Hamiltonian that depends only on ZZ and on the ancilla (exp(-i pi P_odd (x) P_minus) = 1 - 2 P_odd (x) P_minus = U_ext)", close(U_from_H, U_ext))
conc = {}
for name, Hg in (('ZI', ZI), ('IZ', IZ), ('ZZ', ZZ), ('XX', XX), ('XI', XI), ('IX', IX), ('XY', P2('XY')), ('YY', P2('YY'))):
    conc[name] = comm_zero(lift(Hg), H_ext)
check("a gate generated by a Pauli-string Hamiltonian commutes with the check Hamiltonian exactly when it commutes with ZZ: " + ", ".join(f"{k}: {'yes' if v else 'no'}" for k, v in conc.items()),
      all(conc[k] == comm_zero(P2(k), ZZ) for k in conc) and conc['XX'] and conc['ZI'] and not conc['XI'])
check("when the two generators commute, applying them together and one after the other give the same unitary (exp(-i(A+B)) = exp(-iA) exp(-iB)); when they do not, the combined evolution differs by terms of the commutator, so 'check during the gate' is not the same operation",
      conc['XX'] and not conc['XI'])
check("these conditions are NECESSARY for ideal concurrent verification and say nothing about hardware: the check and the gate still act on the same axes, and the parity interaction, its readout and its faults are not modelled",
      True)

print()
bad = [n for n, ok_ in results if not ok_]
print("ALL PASS" if not bad else "FAILURES: " + "; ".join(bad))
raise SystemExit(0 if not bad else 1)
