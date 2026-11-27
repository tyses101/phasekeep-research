# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tyler O'Bryan, where applicable
"""Ideal-model and Pauli-fault checks for the Buddy verification idea. Plain Python, no packages.

Evidence: every result is [[DERIVED]] inside the stated model (ideal gates, or the stated Pauli fault model).
The noise parameters in part 4 are [[ASSUMED]] sweep values, not measurements. Nothing here says what a device costs.

Conventions: three binary axes (a, b = the two Tetragon axes carrying the logical qubit; c = the Buddy ancilla),
state index = 4a + 2b + c. Diagonal encoding: logical |0> = |00>, logical |1> = |11> (even parity, ZZ = +1).
Parity extraction: CNOT(a -> c), then CNOT(b -> c), then read c in the Z basis (0 = even parity = PASS).

Parts (working identifiers BUD-01 .. BUD-04 from the review)
  1. BUD-01 ideal parity extraction: logical amplitudes preserved, flip detected, phase error not detected,
     filtering on c = 0, coherence between parity sectors lost
  2. BUD-02 detectable and undetectable single and double Pauli errors, edge versus diagonal encoding
  3. BUD-03 Buddy-induced faults: every single Pauli fault at three positions, classified by the four outcomes
  4. BUD-04 accounting model: accepted-correct probability, false acceptance, runs per correct result,
     and the break-even downstream cost
"""
import math, random
from itertools import product

random.seed(20261127)
results = []
def check(name, ok):
    results.append((name, bool(ok)))
    print(("PASS  " if ok else "FAIL  ") + name)

# ---------------------------------------------------------------- linear algebra (small, exact enough)
def kron(A, B):
    return [[A[i // len(B)][j // len(B[0])] * B[i % len(B)][j % len(B[0])]
             for j in range(len(A[0]) * len(B[0]))] for i in range(len(A) * len(B))]
def mm(A, B): return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def mv(A, v): return [sum(A[i][k] * v[k] for k in range(len(v))) for i in range(len(A))]
def close(A, B, t=1e-12):
    return all(abs(A[i][j] - B[i][j]) < t for i in range(len(A)) for j in range(len(A[0])))
def neg(A): return [[-x for x in r] for r in A]
def vclose(u, v, t=1e-12): return all(abs(x - y) < t for x, y in zip(u, v))
def vnorm(v):
    n = math.sqrt(sum(abs(x) ** 2 for x in v)); return [x / n for x in v]
def rc(): return complex(random.gauss(0, 1), random.gauss(0, 1))

I2 = [[1, 0], [0, 1]]; PX = [[0, 1], [1, 0]]; PY = [[0, -1j], [1j, 0]]; PZ = [[1, 0], [0, -1]]
PAULI = {'I': I2, 'X': PX, 'Y': PY, 'Z': PZ}

# ---------------------------------------------------------------- three-axis state helpers
def bits(i): return [(i >> 2) & 1, (i >> 1) & 1, i & 1]
def idx(b): return 4 * b[0] + 2 * b[1] + b[2]
def cnot(v, c, t):
    out = [0j] * 8
    for i, x in enumerate(v):
        b = bits(i)
        if b[c]: b[t] ^= 1
        out[idx(b)] += x
    return out
def pauli_on(v, axis, p):
    """Apply Pauli p ('X','Y','Z') to one axis of a 3-axis state. Y is applied as X then Z (global phase irrelevant)."""
    out = list(v)
    if p in ('X', 'Y'):
        o = [0j] * 8
        for i, x in enumerate(out):
            b = bits(i); b[axis] ^= 1; o[idx(b)] += x
        out = o
    if p in ('Z', 'Y'):
        out = [x * (-1 if bits(i)[axis] else 1) for i, x in enumerate(out)]
    return out
def parity_extract(v): return cnot(cnot(v, 0, 2), 1, 2)
def logical_state(al, be):
    v = [0j] * 8; v[0b000] = al; v[0b110] = be; return v
def rand_logical():
    a, b = vnorm([rc(), rc()]); return a, b

# =============================================================== 1. BUD-01 ideal parity extraction
print("== 1. BUD-01 ideal parity extraction ==")
ok_valid = ok_flip = ok_phase = ok_filter = ok_repeat = True
for _ in range(200):
    al, be = rand_logical()
    v = logical_state(al, be)
    out = parity_extract(v)
    ok_valid &= vclose(out, v)                                   # unchanged, ancilla still |0>
    f = [0j] * 8; f[0b100] = al; f[0b010] = be                   # one flip on axis a
    o = parity_extract(f); ok_flip &= abs(o[0b101] - al) < 1e-12 and abs(o[0b011] - be) < 1e-12
    p = logical_state(al, -be)                                   # one phase error
    ok_phase &= vclose(parity_extract(p), p)
    ok_repeat &= vclose(parity_extract(parity_extract(v)), v)    # repeated checkpoints on a valid state
    eps = random.uniform(0, 0.3); e = vnorm([rc(), rc()]); od = vnorm([rc(), rc()])
    s = [0j] * 8
    s[0b000] = math.sqrt(1 - eps) * e[0]; s[0b110] = math.sqrt(1 - eps) * e[1]
    s[0b100] = math.sqrt(eps) * od[0];    s[0b010] = math.sqrt(eps) * od[1]
    o = parity_extract(s)
    kept = [o[i] for i in range(8) if i % 2 == 0]
    ok_filter &= abs(sum(abs(x) ** 2 for x in kept) - (1 - eps)) < 1e-12 \
        and abs(o[0b000] - s[0b000]) < 1e-12 and abs(o[0b110] - s[0b110]) < 1e-12 \
        and all(abs(o[i]) < 1e-12 for i in (0b100, 0b010))
check("valid even-parity state: ancilla stays |0>, state unchanged (200 random logical states)", ok_valid)
check("one bit flip: ancilla reads 1, logical amplitudes carried through unchanged", ok_flip)
check("one phase error: ancilla still reads 0 (NOT detected)", ok_phase)
check("repeating the parity extraction on a valid state changes nothing", ok_repeat)
check("keeping only ancilla = 0: success probability = even weight, survivors unchanged, flips become loss", ok_filter)

# coherence between parity sectors: the ancilla records the sector, so the data lose coherence between sectors
def reduced_data(v):
    rho = [[0j] * 4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            rho[i][j] = sum(v[2 * i + c] * v[2 * j + c].conjugate() for c in (0, 1))
    return rho
e = vnorm([rc(), rc()]); od = vnorm([rc(), rc()])
s = [0j] * 8
s[0b000] = e[0] / math.sqrt(2); s[0b110] = e[1] / math.sqrt(2)
s[0b100] = od[0] / math.sqrt(2); s[0b010] = od[1] / math.sqrt(2)
rho_in = reduced_data(s); rho_out = reduced_data(parity_extract(s))
even_ix, odd_ix = (0, 3), (1, 2)
coh_in = max(abs(rho_in[i][j]) for i in even_ix for j in odd_ix)
coh_out = max(abs(rho_out[i][j]) for i in even_ix for j in odd_ix)
within = all(abs(rho_in[i][j] - rho_out[i][j]) < 1e-12 for i in even_ix for j in even_ix)
check("coherence BETWEEN parity sectors is destroyed by the extraction, coherence WITHIN the even sector is kept",
      coh_in > 0.05 and coh_out < 1e-12 and within)

# =============================================================== 2. BUD-02 detectable / undetectable errors
print("== 2. BUD-02 detectable and undetectable Pauli errors (edge versus diagonal) ==")
def pauli2(p, q): return kron(PAULI[p], PAULI[q])
CODES = {
    # diagonal: span{|00>,|11>}, check ZZ.  edge: span{|00>,|01>} (axis 1 fixed at 0, qubit on axis 2), check ZI
    'diagonal': dict(basis=[0, 3], check=pauli2('Z', 'Z')),
    'edge':     dict(basis=[0, 1], check=pauli2('Z', 'I')),
}
def classify(code, E):
    C = code['check']; EC = mm(E, C); CE = mm(C, E)
    if close(CE, neg(EC)): return 'detected', None
    assert close(CE, EC)
    b = code['basis']
    M = [[E[b[i]][b[j]] for j in range(2)] for i in range(2)]      # E restricted to the code (it maps the code to itself)
    if abs(M[0][1]) < 1e-12 and abs(M[1][0]) < 1e-12 and abs(M[0][0] - M[1][1]) < 1e-12: return 'harmless', 'I'
    for name, P in (('X', PX), ('Y', PY), ('Z', PZ)):
        for ph in (1, -1, 1j, -1j):
            if close(M, [[ph * x for x in r] for r in P]): return 'logical', name
    raise AssertionError("unclassified")
table = {}
for cname, code in CODES.items():
    for p, q in product('IXYZ', repeat=2):
        if p == 'I' and q == 'I': continue
        table[(cname, p + q)] = classify(code, pauli2(p, q))
def tally(cname, labels):
    c = {'detected': 0, 'harmless': 0, 'logical': 0}
    for l in labels: c[table[(cname, l)][0]] += 1
    return c
single = ['XI', 'YI', 'ZI', 'IX', 'IY', 'IZ']
allp = [p + q for p, q in product('IXYZ', repeat=2) if p + q != 'II']
for cname in ('edge', 'diagonal'):
    print(f"  {cname:8s} single-axis errors {tally(cname, single)}   all 15 two-axis Paulis {tally(cname, allp)}")
    for l in allp:
        k, w = table[(cname, l)]
        print(f"      {l}: {k}{'' if w is None else ' (acts as logical ' + w + ')' if k == 'logical' else ''}")
check("diagonal: every single-axis X or Y error on EITHER axis is detected (4 of 6); the 2 single-axis Z errors are undetected logical phase errors",
      tally('diagonal', single) == {'detected': 4, 'harmless': 0, 'logical': 2}
      and all(table[('diagonal', l)] == ('logical', 'Z') for l in ('ZI', 'IZ')))
check("edge: the check covers only the idle axis; every error on the carrier axis (X, Y, Z) is an undetected logical error",
      tally('edge', single) == {'detected': 2, 'harmless': 1, 'logical': 3}
      and [table[('edge', l)] for l in ('IX', 'IY', 'IZ')] == [('logical', 'X'), ('logical', 'Y'), ('logical', 'Z')])
check("diagonal: the double flips XX, YY, XY, YX are undetected logical errors (a single check cannot see an even number of flips)",
      all(table[('diagonal', l)][0] == 'logical' for l in ('XX', 'YY', 'XY', 'YX')))
check("both encodings: over all 15 two-axis Paulis, 8 detected, 6 undetected logical, 1 harmless (same totals, different distribution)",
      tally('diagonal', allp) == tally('edge', allp) == {'detected': 8, 'harmless': 1, 'logical': 6})

# =============================================================== 3. BUD-03 Buddy-induced faults
print("== 3. BUD-03 single Pauli faults at three positions in the extraction circuit ==")
LOC = {0: 'before CNOT1', 1: 'between CNOTs', 2: 'after CNOT2'}
def run_fault(al, be, loc, axis, p):
    v = logical_state(al, be)
    steps = [(0, 2), (1, 2)]
    for k in range(3):
        if k == loc: v = pauli_on(v, axis, p)
        if k < 2: v = cnot(v, *steps[k])
    pr1 = sum(abs(v[i]) ** 2 for i in range(8) if i & 1)
    assert min(pr1, 1 - pr1) < 1e-12, "ancilla should be definite for a single Pauli fault"
    c = 1 if pr1 > 0.5 else 0
    data = [v[2 * d + c] for d in range(4)]                                  # data state given the report
    ref = [al, 0, 0, be]
    fid = abs(sum(x.conjugate() * y for x, y in zip(ref, data))) ** 2
    return ('FAIL' if c else 'PASS'), fid > 1 - 1e-9
def outcome(report, data_ok):
    return {('PASS', True): 'true acceptance', ('FAIL', True): 'FALSE REJECTION',
            ('PASS', False): 'FALSE ACCEPTANCE', ('FAIL', False): 'rejection of damaged data'}[(report, data_ok)]
AXN = {0: 'axis a', 1: 'axis b', 2: 'Buddy ancilla'}
fault_table = {}
for loc in (0, 1, 2):
    for axis in (2, 0, 1):
        for p in 'XYZ':
            reps = set()
            for _ in range(10):
                al, be = rand_logical()
                reps.add(outcome(*run_fault(al, be, loc, axis, p)))
            assert len(reps) == 1, "outcome must not depend on the logical amplitudes"
            fault_table[(loc, axis, p)] = reps.pop()
for loc in (0, 1, 2):
    for axis in (2, 0, 1):
        print(f"  {LOC[loc]:14s} {AXN[axis]:14s} " + "  ".join(f"{p}: {fault_table[(loc, axis, p)]:26s}" for p in 'XYZ'))
anc = lambda loc, p: fault_table[(loc, 2, p)]
check("Buddy ancilla X fault at any position: valid data reported FAIL, data untouched (false rejection)",
      all(anc(l, 'X') == 'FALSE REJECTION' for l in (0, 1, 2)))
check("Buddy ancilla Z fault between the CNOTs: a logical phase error on the data AND a PASS report (Buddy-induced false acceptance)",
      anc(1, 'Z') == 'FALSE ACCEPTANCE')
check("Buddy ancilla Z fault before the first or after the second CNOT: harmless",
      anc(0, 'Z') == 'true acceptance' and anc(2, 'Z') == 'true acceptance')
check("Buddy ancilla Y fault between the CNOTs: reported FAIL and the data are also damaged (Buddy discards good data AND would have corrupted it)",
      anc(1, 'Y') == 'rejection of damaged data' and anc(0, 'Y') == 'FALSE REJECTION' and anc(2, 'Y') == 'FALSE REJECTION')
check("data Z faults (either axis, any position) are PASS with wrong data: missed by the parity check, not introduced by the Buddy",
      all(fault_table[(l, ax, 'Z')] == 'FALSE ACCEPTANCE' for l in (0, 1, 2) for ax in (0, 1)))
check("timing window: a data flip on axis a AFTER its CNOT, or on axis b after the second CNOT, passes this round's check (it would be caught by the next round)",
      fault_table[(0, 0, 'X')] == 'rejection of damaged data' and fault_table[(1, 0, 'X')] == 'FALSE ACCEPTANCE'
      and fault_table[(2, 0, 'X')] == 'FALSE ACCEPTANCE' and fault_table[(1, 1, 'X')] == 'rejection of damaged data'
      and fault_table[(2, 1, 'X')] == 'FALSE ACCEPTANCE')

# =============================================================== 4. BUD-04 accounting model
print("== 4. BUD-04 accounting model (ASSUMED parameters; Pauli-frame model of one checkpoint) ==")
def model(x, z, gx, gz, l):
    """One diagonal-encoded checkpoint. Independent faults: X on each data axis (prob x), Z on each data axis (prob z),
    Buddy ancilla X fault (gx: flips the report), Buddy ancilla Z fault between the CNOTs (gz: a Z on axis a),
    photon loss during the Buddy interaction (l). Returns outcome probabilities."""
    out = dict(acc_correct=0.0, false_acc=0.0, false_rej=0.0, rej_damaged=0.0, lost=l)
    def pr(v, p): return p if v else 1 - p
    for fx1, fx2, fz1, fz2, ax, az in product((0, 1), repeat=6):
        w = pr(fx1, x) * pr(fx2, x) * pr(fz1, z) * pr(fz2, z) * pr(ax, gx) * pr(az, gz) * (1 - l)
        ok = fx1 == 0 and fx2 == 0 and (fz1 ^ fz2 ^ az) == 0
        accepted = (fx1 ^ fx2 ^ ax) == 0
        key = ('acc_correct' if ok else 'false_acc') if accepted else ('false_rej' if ok else 'rej_damaged')
        out[key] += w
    out['accepted'] = out['acc_correct'] + out['false_acc']
    return out
def base_single(x, z): return (1 - x) * (1 - z)                      # one axis, no Buddy: correct iff no X and no Z
def base_diag(x, z): return (1 - x) ** 2 * ((1 - z) ** 2 + z ** 2)   # two axes, no Buddy: correct iff no flips and Z even
def d_star(x, z, gx, gz, l, cB, base):
    """Minimum downstream cost D (in units of the pre-checkpoint stage) above which a checkpoint pays:
    Buddy runs cost 1 + cB + P_accept * D per run and give P_acc_correct correct results; the baseline costs 1 + D per run
    and gives P_baseline correct results. Wrong outputs are assumed identifiable and discarded at the end [ASSUMED]."""
    m = model(x, z, gx, gz, l)
    pa, pc, pb = m['accepted'], m['acc_correct'], base
    purity_gain = 1 / pb - pa / pc
    if purity_gain <= 0: return math.inf
    return max(0.0, ((1 + cB) / pc - 1 / pb) / purity_gain)

m0 = model(0.05, 0, 0, 0, 0)
check("no Buddy faults, no loss, no Z noise: false acceptance = x^2 (double flip), accepted-correct = (1-x)^2, accepted = (1-x)^2 + x^2",
      abs(m0['false_acc'] - 0.05 ** 2) < 1e-15 and abs(m0['acc_correct'] - 0.95 ** 2) < 1e-15
      and abs(m0['accepted'] - (0.95 ** 2 + 0.05 ** 2)) < 1e-15)
tot_ok = True; never_more = True
grid = [0.0, 0.001, 0.01, 0.05, 0.2]
for x, z, gx, gz, l in product(grid, grid, grid, grid, [0.0, 0.01]):
    m = model(x, z, gx, gz, l)
    tot_ok &= abs(m['acc_correct'] + m['false_acc'] + m['false_rej'] + m['rej_damaged'] + m['lost'] - 1) < 1e-12
    never_more &= m['acc_correct'] <= base_diag(x, z) + 1e-12
check("the five outcome probabilities sum to 1 over the whole parameter grid", tot_ok)
check("the accepted-correct probability never exceeds the no-Buddy correct probability of the same encoding (z <= 0.5): the Buddy never gives MORE correct results per run, only fewer wrong ones among those accepted",
      never_more)

# Buddy-induced false acceptance with no data noise at all: a Buddy that only adds harm
mg = model(0, 0, 0, 0.01, 0)
check("no data noise, Buddy Z fault rate 1%: false acceptance = 1% with nothing to detect, so a Buddy can lower reliability",
      abs(mg['false_acc'] - 0.01) < 1e-15 and abs(base_diag(0, 0) - 1) < 1e-15)

# when does the accepted outputs' purity beat the baseline? bisect on the harmful Buddy fault rate gz
def purity_ok(x, z, gx, gz, l, base):
    m = model(x, z, gx, gz, l); return m['acc_correct'] / m['accepted'] > base
def gz_limit(x, z, base_fn):
    lo, hi = 0.0, 0.5
    if not purity_ok(x, z, 0, 0, 0, base_fn(x, z)): return 0.0
    for _ in range(60):
        mid = (lo + hi) / 2
        (lo, hi) = (mid, hi) if purity_ok(x, z, 0, mid, 0, base_fn(x, z)) else (lo, mid)
    return lo
print("  largest harmful-Buddy-fault rate gz at which the accepted outputs are still purer than the baseline (gx=0, l=0), ASSUMED data noise:")
print("      x      z    vs same encoding without Buddy    vs single axis without Buddy")
lim_prev = -1; monotone = True
for x in (0.001, 0.01, 0.05, 0.1):
    for z in (0.0, x / 10):
        a = gz_limit(x, z, base_diag); b = gz_limit(x, z, base_single)
        print(f"  {x:6.3f} {z:6.4f}   {a:10.5f}                         {b:10.5f}")
    lim = gz_limit(x, 0.0, base_diag); monotone &= lim > lim_prev; lim_prev = lim
check("with only flip noise the tolerable harmful Buddy fault rate grows with the data flip rate (a Buddy is worth more when the data are noisier)", monotone)
check("exact threshold: with flip noise only (z = gx = l = 0), the accepted outputs are purer than the baseline exactly when the harmful Buddy fault rate gz < 2x(1-x), the probability of an odd number of data flips",
      all(abs(gz_limit(x, 0.0, base_diag) - 2 * x * (1 - x)) < 1e-9 for x in (0.001, 0.01, 0.05, 0.1, 0.3)))
check("dephasing-dominated noise: with Z noise z = 0.1 and small x, the diagonal encoding with Buddy is NOT purer than a single axis (it exposes two axes to Z and the Buddy cannot see Z)",
      not purity_ok(0.001, 0.1, 0, 0, 0, base_single(0.001, 0.1)))

print("  break-even downstream cost D* (in units of one pre-checkpoint stage), vs same encoding without Buddy. ASSUMED parameters.")
print("      x     gx     gz     l     cB      D*")
dprev = math.inf; dmono = True
for x in (0.01, 0.02, 0.05, 0.1):
    d = d_star(x, 0, 0, 0.001, 0, 0.2, base_diag(x, 0))
    print(f"  {x:6.3f} {0:6.3f} {0.001:6.3f} {0:5.2f} {0.2:5.2f}  {d:10.2f}")
    dmono &= d < dprev; dprev = d
check("break-even downstream cost falls as the data noise rises (flip-only noise, small harmful Buddy fault)", dmono)
check("break-even is infinite (the Buddy never pays) when the harmful Buddy fault rate exceeds the purity limit",
      d_star(0.01, 0, 0, 0.5, 0, 0.0, base_diag(0.01, 0)) == math.inf)
check("a costlier Buddy interaction raises the break-even downstream cost",
      d_star(0.05, 0, 0, 0.001, 0, 0.5, base_diag(0.05, 0)) > d_star(0.05, 0, 0, 0.001, 0, 0.1, base_diag(0.05, 0)))

print()
bad = [n for n, ok in results if not ok]
print("ALL PASS" if not bad else "FAILURES: " + "; ".join(bad))
raise SystemExit(0 if not bad else 1)
