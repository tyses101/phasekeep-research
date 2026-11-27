#!/usr/bin/env python3
"""S13: what does it cost, in inter-photon gates, to rebuild one erased axis of the joint [[4,2,2]] code?

S12 left the number m of data-touching gates of the recovery as a free parameter and showed that the verdict (does the joint round beat the local one?) turns on it.
This script constructs recoveries, verifies them on full state vectors, and proves what it can about the minimum.

Setting (ASSUMED, as S07/S12): one data axis per photon, axis 3 is erased (heralded), axes 0, 1, 2 survive; a reference system R holds the other half of a maximally
entangled input, so "recovered" means the reference and the four code qubits end in exactly the original state (identity logical map, up to a known Pauli).
Free operations: single-qubit Cliffords, single-qubit Pauli-basis measurement and reset, classical feed-forward of Pauli corrections, any operation that touches
no live data (so ancilla-only gates, offline).  Counted: every two-qubit gate that touches a live data qubit (these can fail and then destroy that qubit).

Claims
  W0  A two-qubit Clifford gate changes the Pauli weight of any Pauli operator by at most 1 (all 720 symplectic classes of two-qubit Cliffords, every Pauli).     DERIVED
  W1  In the gauge picture the 4 qubits are 2 logical + 2 gauge qubits.  Initially the stabilized gauge element is Z3 (weight 1); a SECOND independent commuting element
      has to be created by a measurement, and the lightest such element has weight 3 (X0X1X2, Y0Y1Y2, Z0Z1Z2).  The two code stabilizers all have weight 4.   DERIVED
  W2  Consequence (a proof, given the family below): an IN-PLACE recovery (gates only among the four data qubits and fresh product-state ancillas; single-qubit
      measurements and resets; Pauli feed-forward) needs at least 2 gates before the measurement that creates the new element (weight 3 -> 1) and at least
      3 after it (weight 1 -> 4), so at least 5 data-touching gates.  Whether 5 is attained is NOT determined here.                                               DERIVED on the stated family
  W3  No single-qubit Pauli measurement on any surviving axis commutes with all four logical operators, so a surviving axis cannot just be measured out.          DERIVED
  R6  An in-place recovery with 6 data-touching gates exists (measure X0X1X2 with one ancilla, then fan the three axes onto the replacement); verified on state vectors
      (both measurement outcomes).                                                                                                                              DERIVED
  T3  A teleportation-based recovery with exactly 3 data-touching gates exists: an offline-prepared resource (10 ancilla-only gates, none touching live data) implements the
      whole recovery channel, and 3 inter-photon gates (Bell measurements of axes 0, 1, 2 with resource qubits) move the information into a fresh block.  Verified on all 64
      Bell-outcome branches (a Pauli correction exists for each; fidelity 1).  Two negative controls fail as they must (no junk-cancelling correction: 0.5; no recovery
      at all: < 1).                                                                                                                                             DERIVED
  C3  With the recovery cost m, the joint cat (or flagged, free ancilla failures) round beats the local round only above a crossover s (S12): m = 3, 5, 6 given with exact
      rational sign certificates.  The best recovery here (m = 3) still needs s > 0.86.                                                                            DERIVED on S12's ASSUMED process
Not claimed: that fewer than 3 data-touching gates is impossible for protocols with arbitrary offline resources (not proved); that 5 is attained in place; that the
resource can be prepared and held without loss or waiting-time cost (it takes 8 extra photons and its own verification, unmodelled); anything about a device.
Author-side; not an independent reproduction.  Requires numpy.
"""
import importlib.util, itertools, os, sys
from fractions import Fraction as Fr
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
def _load(name, rel):
    sp = importlib.util.spec_from_file_location(name, os.path.join(ROOT, *rel)); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
s07 = _load("s07", ["explorations", "s07-failure-semantics", "failure_semantics.py"]); sv = s07.sv
s12 = _load("s12", ["explorations", "s12-recovery-charged-completion", "recovery_completion.py"])

OK = True
def check(name, ok):
    global OK
    OK = OK and bool(ok); print(("PASS  " if ok else "FAIL  ") + name)

# ---------------------------------------------------------------------------------------------------------------------------------
# Pauli bookkeeping on 4 data qubits: (x bits, z bits) as 8-bit ints, bit q = qubit q
def pauli(s):
    x = z = 0
    for q, c in enumerate(s):
        if c in "XY": x |= 1 << q
        if c in "ZY": z |= 1 << q
    return x, z
def commute(a, b): return (bin(a[0] & b[1]).count("1") + bin(a[1] & b[0]).count("1")) % 2 == 0
def weight(a): return bin(a[0] | a[1]).count("1")
def name(a): return "".join("IXZY"[((a[0] >> q) & 1) + 2 * ((a[1] >> q) & 1)] for q in range(4))
def mul(a, b): return (a[0] ^ b[0], a[1] ^ b[1])
ALL4 = [(x, z) for x in range(16) for z in range(16)]

def weight_lemma():
    """closure of the 2-qubit Clifford group acting on Pauli vectors (x0 x1 z0 z1) over F_2: 720 symplectic matrices"""
    def mat(f):                                    # image of the 4 basis vectors
        return tuple(f(v) for v in (1, 2, 4, 8))
    def apply(m, v):
        out = 0
        for k in range(4):
            if (v >> k) & 1: out ^= m[k]
        return out
    # bits: 0 = x0, 1 = x1, 2 = z0, 3 = z1
    def H0(v): x0, x1, z0, z1 = [(v >> k) & 1 for k in range(4)]; return z0 | (x1 << 1) | (x0 << 2) | (z1 << 3)
    def H1(v): x0, x1, z0, z1 = [(v >> k) & 1 for k in range(4)]; return x0 | (z1 << 1) | (z0 << 2) | (x1 << 3)
    def S0(v): x0, x1, z0, z1 = [(v >> k) & 1 for k in range(4)]; return x0 | (x1 << 1) | ((z0 ^ x0) << 2) | (z1 << 3)
    def S1(v): x0, x1, z0, z1 = [(v >> k) & 1 for k in range(4)]; return x0 | (x1 << 1) | (z0 << 2) | ((z1 ^ x1) << 3)
    def CN(v): x0, x1, z0, z1 = [(v >> k) & 1 for k in range(4)]; return x0 | ((x1 ^ x0) << 1) | ((z0 ^ z1) << 2) | (z1 << 3)
    def NC(v): x0, x1, z0, z1 = [(v >> k) & 1 for k in range(4)]; return (x0 ^ x1) | (x1 << 1) | (z0 << 2) | ((z1 ^ z0) << 3)
    gens = [mat(f) for f in (H0, H1, S0, S1, CN, NC)]
    ident = mat(lambda v: v); seen = {ident}; frontier = [ident]
    while frontier:
        nxt = []
        for m in frontier:
            for g in gens:
                comp = tuple(apply(g, m[k]) for k in range(4))        # apply m, then g
                if comp not in seen: seen.add(comp); nxt.append(comp)
        frontier = nxt
    wt = lambda v: ((v | (v >> 2)) & 1) + (((v >> 1) | (v >> 3)) & 1)  # number of qubits (0,1) with non-identity
    worst_up = max(wt(apply(m, v)) - wt(v) for m in seen for v in range(1, 16)); worst_dn = max(wt(v) - wt(apply(m, v)) for m in seen for v in range(1, 16))
    return len(seen), worst_up, worst_dn

# ---------------------------------------------------------------------------------------------------------------------------------
# state-vector side
NQ = 14; sim = sv.Sim(NQ); H = sv.HAD
DATA = [0, 1, 2]; ERASED = 3; NEW = [4, 5, 6, 7]; JUNK = 8; AN = [9, 10, 11]; REF = [12, 13]
BASIS = s07.code_basis("J")

def initial():
    v = np.zeros(sim.N, dtype=complex)
    for l in range(4): v[(l << 12):(l << 12) + 16] += 0.5 * BASIS[:, l]
    return v

class Rec:
    """applies gates to a state vector and records every two-qubit gate"""
    def __init__(self, v): self.v = v; self.gates = []
    def h(self, q): self.v = sim.one(self.v, H, q)
    def cnot(self, c, t): self.v = sim.cnot(self.v, c, t); self.gates.append(("CNOT", c, t))
    def cz(self, a, b): self.v = sim.cz(self.v, a, b); self.gates.append(("CZ", a, b))
    def pauli(self, q, c): self.v = sim.pauli(self.v, {q: c})
    def measure(self, q, branch): self.v, o, _ = sim.measure_z(self.v, q, branch=branch); return o

TARGET = np.zeros(64, dtype=complex)
for l in range(4): TARGET[(l << 4):(l << 4) + 16] = 0.5 * BASIS[:, l]
PM = {"I": np.eye(2), "X": np.array([[0, 1], [1, 0]]), "Z": np.diag([1., -1.]), "Y": np.array([[0, -1j], [1j, 0]])}

def block_matrix(v, block):
    """rows: (ref, block) basis states in the order of TARGET; columns: everything else"""
    keep = [13, 12, block[3], block[2], block[1], block[0]]
    T = v.reshape([2] * NQ); ka = [NQ - 1 - q for q in keep]; ra = [a for a in range(NQ) if a not in ka]
    return np.transpose(T, ka + ra).reshape(64, -1)

def fidelity(v, block, corr="IIII"):
    """overlap of the reduced state of (reference, block) with the target code state, after applying the Pauli string `corr` to the block"""
    tt = TARGET.copy().reshape([2] * 6)
    for k, c in enumerate(corr):
        if c != "I": tt = np.moveaxis(np.tensordot(PM[c], tt, axes=([1], [5 - k])), 0, 5 - k)
    return float(np.sum(np.abs(tt.reshape(-1).conj() @ block_matrix(v, block)) ** 2))

def best_pauli(v, block):
    return max((fidelity(v, block, "".join(p)), "".join(p)) for p in itertools.product("IXYZ", repeat=4))

def recover_in_place(v0, branch):
    """R6: measure X0X1X2 with ancilla JUNK (6 data-touching gates in all), then fan the three axes onto the replacement qubit 7"""
    r = Rec(v0.copy()); A = JUNK; q3 = NEW[3]
    r.h(A)
    for i in DATA: r.cnot(A, i)                       # controlled-X on axis i, control A: kicks back X0X1X2 onto A's phase
    r.h(A); m = r.measure(A, branch)
    for i in DATA: r.cnot(i, q3)                      # Z3 -> Z0Z1Z2Z3 (restores ZZZZ); X0X1X2 -> X0X1X2X3 (restores XXXX up to the sign m)
    if m: r.pauli(q3, "Z")
    return r, m

def resource(variant="cz"):
    """offline: Bell pairs (NEW[i], AN[i]), then the recovery unitary W on (NEW[0..2], NEW[3] = replacement, JUNK = parity qubit); no live data is touched"""
    r = Rec(np.zeros(sim.N, dtype=complex)); r.v[0] = 1.0
    for i in range(3): r.h(NEW[i]); r.cnot(NEW[i], AN[i])
    r.h(JUNK)
    for i in range(3): r.cnot(JUNK, NEW[i])
    r.h(JUNK)
    for i in range(3): r.cnot(NEW[i], NEW[3])
    if variant == "cz": r.cz(JUNK, NEW[3])
    return r

def main():
    # ------------------------------------------------------------------ W0
    n, up, dn = weight_lemma()
    check("W0 the 2-qubit Clifford group has %d symplectic classes; no gate raises or lowers the weight of any Pauli by more than 1 (max rise %d, max fall %d)" % (n, up, dn), n == 720 and up == 1 and dn == 1)
    # ------------------------------------------------------------------ W1
    LOG = [pauli("XXII"), pauli("ZIZI"), pauli("XIXI"), pauli("ZZII")]       # data parts of the four logical operators (X1, Z1, X2, Z2)
    STAB = [pauli("ZZZZ"), pauli("XXXX")]
    ok_log = all(commute(a, s) for a in LOG for s in STAB) and not commute(LOG[0], LOG[1]) and not commute(LOG[2], LOG[3]) and commute(LOG[0], LOG[3]) and commute(LOG[1], LOG[2]) \
        and commute(LOG[0], LOG[2]) and commute(LOG[1], LOG[3])
    check("W1a the four logical operators commute with both stabilizers and have the Heisenberg algebra of two logical qubits", ok_log)
    cent = [p for p in ALL4 if all(commute(p, l) for l in LOG)]                    # the gauge group: 2 gauge qubits = 16 Paulis
    z3 = pauli("IIIZ"); D0 = {(0, 0), z3}
    add = [p for p in cent if commute(p, z3) and p not in D0]
    lightest = min(weight(p) for p in add)
    print("      gauge group has %d elements; elements that commute with Z3 and are not in <Z3>: %s" % (len(cent), sorted(name(p) for p in add)))
    check("W1b the centralizer of the logical operators has 16 elements (two gauge qubits) and exactly 6 candidate new elements; the lightest has weight 3", len(cent) == 16 and len(add) == 6 and lightest == 3)
    sing = [p for p in cent if weight(p) == 1]
    check("W1c the weight-1 elements of the gauge group are X3, Y3, Z3 only; none of them is a new element commuting with Z3 (a new abelian pair needs weight >= 3 now)",
          sorted(name(p) for p in sing) == ["IIIX", "IIIY", "IIIZ"] and all((not commute(p, z3)) or p in D0 for p in sing))
    S_all = [mul(STAB[0], STAB[1]), STAB[0], STAB[1]]
    check("W1d every nonidentity element of the final stabilizer group {I, ZZZZ, XXXX, YYYY} has weight 4", all(weight(p) == 4 for p in S_all))
    check("W2  in-place recovery needs >= 2 (weight 3 -> 1 before the measurement) + 3 (weight 1 -> 4 after it) = 5 data-touching gates by W0, W1b and W1d: %d + %d = %d" % (lightest - 1, 4 - 1, (lightest - 1) + 3), (lightest - 1) + 3 == 5)
    # ------------------------------------------------------------------ W3
    bad = {i: all(any(not commute(((1 << i) if c in "XY" else 0, (1 << i) if c in "ZY" else 0), l) for l in LOG) for c in "XYZ") for i in DATA}
    check("W3 every single-qubit Pauli (X, Y, Z) on each surviving axis anticommutes with some logical operator: no surviving axis can simply be measured out", all(bad.values()))
    # ------------------------------------------------------------------ R6 in-place, 6 gates
    v0 = initial(); base = fidelity(v0, [0, 1, 2, 3]); print("      sanity: fidelity of the untouched original block (ref + axes 0..3) with the target: %.6f" % base)
    check("T0a the target and the initial state agree (fidelity 1 before anything is erased)", abs(base - 1) < 1e-9)
    fids = []
    for br in (0, 1):
        r, m = recover_in_place(v0, br); fids.append(fidelity(r.v, [0, 1, 2, 7]))
    gates6 = len(recover_in_place(v0, 0)[0].gates)
    check("R6 in-place recovery (ancilla parity measurement, then fan-in) has fidelity 1 for both measurement outcomes; data-touching gates = %d" % gates6, all(abs(f - 1) < 1e-9 for f in fids) and gates6 == 6)
    # control: skip the recovery -> the erased axis is simply replaced by a fresh |0>: not the code state
    ctrl = fidelity(v0, [0, 1, 2, 7])                     # qubit 7 is a fresh |0> (never touched)
    check("T0b control: replacing the erased axis by a fresh qubit and doing nothing gives fidelity %.4f < 1" % ctrl, ctrl < 0.99)
    # ------------------------------------------------------------------ T3 teleportation-based recovery
    res = resource("cz"); res_nocz = resource("nocz")
    nres = len(res.gates); live = {0, 1, 2, 3}
    check("T3a the resource preparation has %d two-qubit gates and none of them touches a live data qubit (axes 0..3)" % nres, nres == 10 and all(not (set(g[1:]) & live) for g in res.gates))
    def online(res_v, bits):
        """combine data-side state with the resource (disjoint qubits) and run the Bell measurements"""
        v = initial()                                      # reference + data + erased qubit on qubits 0..3, 12, 13
        # the resource state lives on qubits 4..11 with all other qubits in |0>; the data state has qubits 4..11 in |0>: take the tensor product by index arithmetic
        A = v.reshape(4, 2 ** 8, 2 ** 4)                   # (ref, middle 4..11, data 0..3)
        Bv = res_v.reshape(4, 2 ** 8, 2 ** 4)
        out = np.zeros((4, 2 ** 8, 2 ** 4), dtype=complex)
        out[:, :, :] = np.einsum("rd,m->rmd", A[:, 0, :], Bv[0, :, 0])
        r = Rec(out.reshape(-1)); k = 0
        for i in range(3):
            r.cnot(DATA[i], AN[i]); r.h(DATA[i])
            r.measure(DATA[i], bits[k]); k += 1
            r.measure(AN[i], bits[k]); k += 1
        return r
    worst = 1.0; tab = {}; ngate = set()
    for bits in itertools.product((0, 1), repeat=6):
        r = online(res.v, bits); f, p = best_pauli(r.v, NEW); worst = min(worst, f); tab[bits] = p; ngate.add(len(r.gates))
    check("T3b teleportation recovery: for each of the 64 Bell-outcome branches a Pauli correction on the new block gives fidelity 1 (worst branch %.9f); data-touching gates = %s" % (worst, sorted(ngate)), abs(worst - 1) < 1e-9 and ngate == {3})
    worst0 = 1.0
    for bits in itertools.product((0, 1), repeat=6):
        r = online(res_nocz.v, bits); worst0 = min(worst0, best_pauli(r.v, NEW)[0])
    check("T3c negative control: without the junk-cancelling CZ in the resource no outcome-only Pauli correction exists for some branch (worst fidelity %.4f)" % worst0, worst0 < 0.9)
    # the correction should be an affine function of the six outcome bits over GF(2), modulo the stabilizer group of the block (frame propagation through a Clifford network)
    Sg = {(0, 0), pauli("ZZZZ"), pauli("XXXX"), pauli("YYYY")}
    c0 = pauli(tab[(0,) * 6]); ci = []
    for k in range(6):
        e = tuple(1 if j == k else 0 for j in range(6)); a = pauli(tab[e]); ci.append((a[0] ^ c0[0], a[1] ^ c0[1]))
    affine = True
    for bits, p in tab.items():
        x, z = c0
        for b, c in zip(bits, ci):
            if b: x ^= c[0]; z ^= c[1]
        a = pauli(p); affine &= (a[0] ^ x, a[1] ^ z) in Sg
    check("T3d the Pauli correction is an affine function of the six Bell-outcome bits over GF(2), modulo the block's stabilizers, in all 64 branches (so it is ordinary Pauli-frame propagation, not a per-branch oracle)", affine)
    # ------------------------------------------------------------------ summary and C3
    def margin(mm): return lambda s: s12.chain(tuple([1] * 8), s, s ** mm) - s ** 4
    X = {m: s12.crossing(margin(m)) for m in (3, 5, 6)}
    cert = all(X[m] is not None and margin(m)(X[m][0]) <= 0 < margin(m)(X[m][1]) for m in X)
    check("C3 crossover per-gate success s (joint cat / flagged-free beats local only above it): m = 3: %.4f, m = 5: %.4f, m = 6: %.4f; exact sign certificates at the brackets"
          % tuple(float(X[m][1]) for m in (3, 5, 6)), cert and float(X[3][1]) < float(X[5][1]) < float(X[6][1]))
    print("== summary of data-touching gates needed to rebuild one erased axis of [[4,2,2]] (one axis per photon) ==")
    print("      teleportation with an offline resource : 3   (constructed, verified)   resource: 10 ancilla-only gates, 8 extra photons")
    print("      in place, ancilla parity + fan-in       : 6   (constructed, verified)")
    print("      in place, any circuit of the stated family: >= 5 (proved); whether 5 is attained is open")
    print("      fewer than 3 with arbitrary offline resources: not proved impossible here")
    print("NOTE  Every verdict above is on the assumed erasure semantics and S12's process; 'free' offline preparation ignores the waiting time of the data photons and the loss of the")
    print("      resource photons themselves (S04), and the resource needs 8 photons against 4 for the data block.")
    print("ALL PASS" if OK else "FAILED")
    return 0 if OK else 1

if __name__ == "__main__": sys.exit(main())
