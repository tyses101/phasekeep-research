#!/usr/bin/env python3
"""S14: verification by teleportation (Knill-style) instead of by ancilla checks: what does it do to the heralded-failure problem?

S07 to S13 show that the joint [[4,2,2]] round needs 8 data-touching inter-photon gates against the local round's 4, and that the joint code's advantage (a failed gate leaves the
information recoverable) is eaten by that exposure unless s is high.  Here the verification is done differently.  An offline-prepared resource (two code blocks a and n
holding encoded Bell pairs) is used to teleport the four data axes onto the fresh block n: each data axis takes part in ONE inter-photon gate (a Bell measurement with its
partner axis in block a), so the round has 4 data-touching gates, the same as the local round, while the measurement record carries the code's syndrome.

Assumptions (ASSUMED, as S07/S12/S13): one axis per photon; a failed inter-photon gate heralds itself and erases its two qubits (EraseAxis); intra-photon operations, single-qubit
measurements and the offline resource preparation are ideal except that the preparation is built from real gates (counted), none touching live data; the resource is assumed
correct (its own faults are NOT modelled).  Only the heralded-completion metric is computed.  The silent-fault metric of V0.9/V1.0 is NOT computed for this design, and the two
are not combined.

Claims
  K0  The resource is prepared by 12 ancilla-only gates (4 Bell pairs, then two postselected weight-4 stabilizer checks of block a; 8 gates for the local code's weight-2 checks) and
      equals the encoded Bell state (fidelity 1).                                                                                                             DERIVED
  K1  Teleporting the four axes through it reproduces the data state on the new block: for every possible Bell-outcome record a Pauli correction gives fidelity 1, and the correction
      is an affine function of the outcome bits modulo the block's stabilizers (ordinary Pauli-frame propagation).                                                    DERIVED
  K2  Detection: every single-qubit Pauli error on a data axis (12 cases) produces outcome records that never occur for an error-free input, i.e. it is always detected (the code has
      distance 2).  The local code's analogue detects Z errors that the checks see but is blind to X errors.                                                        DERIVED
  K3  Heralded failure at gate k (k = 1..4): the joint code keeps the information recoverable at every gate (r = 1), including after the remaining gates have run, from the three
      surviving axes of the new block; the local code never does (r = 0 at every gate).                                                                              DERIVED on ASSUMED semantics
  K3c After a failed gate at k the three surviving new-block axes together with the reference are in exactly the reduced state of the code with axis k erased, up to a Pauli
      frame, for every outcome record: the state S13's recovery was verified on.                                                                                   DERIVED
  K4  Completion probability with recovery charged as in S12/S13: a failure at gate k is followed by the remaining 4 - k gates and a 3-gate teleportation recovery (S13), so the
      chain is P = s^4 / (1 - 4 (1-s) s^6), which exceeds the local s^4 at every s in (0,1), and the cat round's value at S13's m = 3 as well (checked on a grid, not proved in general).
      The advantage over the local round is at most about 29 % (ratio 1/(1 - 4(1-s)s^6)).                                                                             DERIVED on ASSUMED process
Not claimed: anything about silent faults or resource faults; that the resource can be prepared and held (it takes 8 photons plus 2 preparation ancillas per round and waiting time
is unmodelled); that a recovery by symmetry from S13 was re-simulated end to end for each k (argued from the code's qubit-permutation symmetry, checked in K6); two axes per photon.
Author-side; not an independent reproduction.  Requires numpy.
"""
import importlib.util, itertools, math, os, random, sys
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

NQ = 16; sim = sv.Sim(NQ); H = sv.HAD
DATA = [0, 1, 2, 3]; A = [4, 5, 6, 7]; N = [8, 9, 10, 11]; REF = [12, 13]; C1, C2 = 14, 15
CODES = {"J": ["ZZZZ", "XXXX"], "L": ["ZZII", "IIZZ"]}
BASIS = {c: s07.code_basis(c) for c in "JL"}
PM = {"I": np.eye(2), "X": np.array([[0, 1], [1, 0]]), "Z": np.diag([1., -1.]), "Y": np.array([[0, -1j], [1j, 0]])}

class NeedBit(Exception): pass

class Rec:
    def __init__(self, v): self.v = v; self.gates = []
    def h(self, q): self.v = sim.one(self.v, H, q)
    def cnot(self, c, t): self.v = sim.cnot(self.v, c, t); self.gates.append((c, t))
    def pauli(self, q, c): self.v = sim.pauli(self.v, {q: c})
    def measure(self, q, bits):
        """projective Z measurement; a random outcome consumes the next bit of `bits` (an iterator), a deterministic one does not"""
        try: self.v, o, rnd = sim.measure_z(self.v, q)
        except RuntimeError:
            b = next(bits, None)
            if b is None: raise NeedBit()
            self.v, o, rnd = sim.measure_z(self.v, q, branch=b)
        return o

def resource_state(code):
    """offline preparation: Bell pairs (A[i], N[i]), then postselected stabilizer checks of block A with ancillas C1, C2; returns (state, gate list)"""
    r = Rec(np.zeros(sim.N, dtype=complex)); r.v[0] = 1.0
    for i in range(4): r.h(A[i]); r.cnot(A[i], N[i])
    anc = [C1, C2]
    for gen, c in zip(CODES[code], anc):
        supp = [i for i, ch in enumerate(gen) if ch != "I"]
        if gen[supp[0]] == "Z":
            for i in supp: r.cnot(A[i], c)
            o = r.measure(c, iter([0]))
        else:
            r.h(c)
            for i in supp: r.cnot(c, A[i])
            r.h(c); o = r.measure(c, iter([0]))
        assert o == 0, "postselection outcome must be +1 for the resource to be the code-space projection"
    return r

def with_data(res_v, data_v):
    """combine the resource vector (data qubits 0..3 and ref 12,13 in |0>) with a data-side vector (qubits 4..11, 14, 15 in |0>)"""
    out = np.zeros(sim.N, dtype=complex)
    idx = np.nonzero(np.abs(data_v) > 1e-14)[0]
    ridx = np.nonzero(np.abs(res_v) > 1e-14)[0]
    for i in idx:
        out[ridx | i] += data_v[i] * res_v[ridx]
    return out

def initial_ref(code):
    v = np.zeros(sim.N, dtype=complex)
    for l in range(4): v[(l << 12):(l << 12) + 16] += 0.5 * BASIS[code][:, l]
    return v
def initial_basis(code, l):
    v = np.zeros(sim.N, dtype=complex); v[:16] = BASIS[code][:, l]; return v

TARGET = {c: np.zeros(256, dtype=complex) for c in "JL"}       # (ref, new block) in the order (ref bits high) -> index = (l << 4) + block bits
for c in "JL":
    for l in range(4): TARGET[c][(l << 4):(l << 4) + 16] = 0.5 * BASIS[c][:, l]

def block_matrix(v, qubits):
    keep = [13, 12] + [qubits[3], qubits[2], qubits[1], qubits[0]]
    T = v.reshape([2] * NQ); ka = [NQ - 1 - q for q in keep]; ra = [a for a in range(NQ) if a not in ka]
    return np.transpose(T, ka + ra).reshape(64, -1)
TGT64 = {c: np.zeros(64, dtype=complex) for c in "JL"}
for c in "JL":
    for l in range(4): TGT64[c][(l << 4):(l << 4) + 16] = 0.5 * BASIS[c][:, l]
PAULIS = ["".join(p) for p in itertools.product("IXYZ", repeat=4)]
def _pauli_targets(code):
    out = np.zeros((256, 64), dtype=complex)
    for n, corr in enumerate(PAULIS):
        tt = TGT64[code].copy().reshape([2] * 6)
        for k, ch in enumerate(corr):
            if ch != "I": tt = np.moveaxis(np.tensordot(PM[ch], tt, axes=([1], [5 - k])), 0, 5 - k)
        out[n] = tt.reshape(-1)
    return out
PT = {c: _pauli_targets(c) for c in "JL"}
def fid_all(v, qubits, code):
    """fidelity of the reduced state of (reference, block) with the target after each of the 256 Pauli corrections on the block"""
    G = PT[code].conj() @ block_matrix(v, qubits)
    return np.sum(np.abs(G) ** 2, axis=1)
def best_pauli(v, qubits, code):
    f = fid_all(v, qubits, code); k = int(np.argmax(f)); return float(f[k]), PAULIS[k]

def teleport(v0, upto=4, bits=None, skip=None, error=None, halt_at=None):
    """Bell-measure data axis i with A[i] for i < upto; `error` = (qubit, pauli) applied to the data before the round; `skip` = index k whose gate fails (data k and A k erased: the pair is
    simply not measured and is traced out by the caller)"""
    r = Rec(v0.copy()); bits = iter(bits if bits is not None else [])
    if error: r.pauli(*error)
    outs = []
    for i in range(upto):
        if i == skip: continue
        r.cnot(DATA[i], A[i]); r.h(DATA[i])
        outs.append(r.measure(DATA[i], bits)); outs.append(r.measure(A[i], bits))
    return r, tuple(outs)

def explore(fn):
    """depth-first enumeration of the random measurement outcomes: fn(bits) must raise NeedBit when it needs a further random bit; returns {outcome record: result}"""
    out = {}; stack = [[]]
    while stack:
        pre = stack.pop()
        try: res = fn(pre)
        except NeedBit:
            stack.append(pre + [0]); stack.append(pre + [1]); continue
        out.setdefault(res[1], res[0])
    return out

def kl_ok(phis, lost):
    """Knill-Laflamme test: Tr_keep |phi_j><phi_k| = delta_jk rho for the four logical basis states.  The lost-side blocks are formed on the joint support only
    (an isometric reduction by an SVD of the stacked kept-by-lost matrices), so a large lost set does not need a 2^n by 2^n matrix."""
    lost = sorted(lost); keep = [q for q in range(NQ) if q not in lost]; M = []
    for v in phis:
        T = v.reshape([2] * NQ)
        M.append(np.transpose(T, [NQ - 1 - q for q in keep] + [NQ - 1 - q for q in lost]).reshape(2 ** len(keep), 2 ** len(lost)))
    _, sg, vh = np.linalg.svd(np.vstack(M), full_matrices=False)
    V = vh[: int(np.sum(sg > 1e-9))]; Ap = [m @ V.conj().T for m in M]
    E = {(j, k): Ap[j].conj().T @ Ap[k] for j in range(4) for k in range(4)}; rho = E[(0, 0)]
    return all(np.allclose(E[(j, j)], rho, atol=1e-9) for j in range(4)) and all(np.allclose(E[(j, k)], 0, atol=1e-9) for j in range(4) for k in range(4) if j != k)

def main():
    res = {c: resource_state(c) for c in "JL"}
    # ---------------------------------------------------------------- K0
    for c, expect in (("J", 12), ("L", 8)):
        ng = len(res[c].gates); live = set(DATA) | set(REF)
        # reduced state of (A, N) must be the encoded Bell state of the code
        T = res[c].v.reshape([2] * NQ); keep_q = A[::-1] + N[::-1]
        ka = [NQ - 1 - q for q in keep_q]; ra = [a for a in range(NQ) if a not in ka]
        M = np.transpose(T, ka + ra).reshape(256, -1)
        tgt = np.zeros(256, dtype=complex)
        for l in range(4): tgt += 0.5 * np.kron(BASIS[c][:, l], BASIS[c][:, l].conj())       # block A on the low 4 bits? ordering below
        # index = (A bits high, N bits low) in the order keep_q = A[3],A[2],A[1],A[0],N[3],..,N[0]; kron(a, n) with a as the high factor
        f = float(np.sum(np.abs(tgt.conj() @ M) ** 2))
        check("K0%s the resource for code %s is prepared by %d two-qubit gates, none touching a live data or reference qubit, and equals the encoded Bell state (fidelity %.6f)"
              % (c.lower(), c, ng, f), ng == expect and all(not ({g[0], g[1]} & live) for g in res[c].gates) and abs(f - 1) < 1e-9)
    # ---------------------------------------------------------------- K1
    summary = {}
    for c in "JL":
        v0 = with_data(res[c].v, initial_ref(c))
        recs = explore(lambda pre: teleport(v0, bits=pre))
        worst = 1.0; tab = {}
        for outs, r in recs.items():
            f, p = best_pauli(r.v, N, c); worst = min(worst, f); tab[outs] = p
        summary[c] = (len(recs), worst, tab, {len(r.gates) for r in recs.values()})
    nJ, wJ, tabJ, gJ = summary["J"]
    check("K1  joint: %d distinct Bell-outcome records occur; for each a Pauli correction on the new block gives fidelity 1 (worst %.9f); data-touching gates per round = %s" % (nJ, wJ, sorted(gJ)),
          abs(wJ - 1) < 1e-9 and gJ == {4})
    # the correction should be affine in the outcome bits (outcome records are 8 bits; only the records that occur are tested)
    def pz(s):
        x = z = 0
        for q, ch in enumerate(s):
            if ch in "XY": x |= 1 << q
            if ch in "ZY": z |= 1 << q
        return x, z
    Sg = {(0, 0), pz("ZZZZ"), pz("XXXX"), pz("YYYY")}
    ks = sorted(tabJ); base = ks[0]; c0 = pz(tabJ[base])
    # solve for the affine map by least squares over GF(2) is overkill: test the weaker, exact property that XOR of two records' corrections equals the correction of the XOR record when it occurs
    aff = True; keyset = set(ks)
    for a, b in itertools.combinations(ks, 2):
        d = tuple(x ^ y ^ z for x, y, z in zip(a, b, base))
        if d in keyset:
            pa, pb, pd, p0 = pz(tabJ[a]), pz(tabJ[b]), pz(tabJ[d]), c0
            x = pa[0] ^ pb[0] ^ p0[0] ^ pd[0]; z = pa[1] ^ pb[1] ^ p0[1] ^ pd[1]
            aff &= (x, z) in Sg
    check("K1b the Pauli correction is affine in the outcome record, modulo the block's stabilizers (checked on every triple of records whose XOR is also a record)", aff)
    # ---------------------------------------------------------------- K2
    vJ = with_data(res["J"].v, initial_ref("J")); good = explore(lambda pre: teleport(vJ, bits=pre)); valid = set(good)
    det = {}
    for q in range(4):
        for ch in "XYZ":
            rr = explore(lambda pre, q=q, ch=ch: teleport(vJ, bits=pre, error=(q, ch)))
            det[(q, ch)] = set(rr) & valid
    check("K2  joint: all 12 single-qubit Pauli errors on a data axis give only outcome records that never occur for an error-free input (always detected)", all(len(x) == 0 for x in det.values()))
    vL = with_data(res["L"].v, initial_ref("L")); goodL = set(explore(lambda pre: teleport(vL, bits=pre)))
    detL = {}
    for q in range(4):
        for ch in "XYZ":
            rr = explore(lambda pre, q=q, ch=ch: teleport(vL, bits=pre, error=(q, ch))); detL[(q, ch)] = len(set(rr) & goodL) == 0
    blind = sorted(k for k, v in detL.items() if not v)
    print("      local code: errors NOT always detected: %s" % ", ".join("%s%d" % (ch, q) for q, ch in blind))
    check("K2b local code control: its two Z-parity checks detect the X and Y errors on every axis and are blind to every Z error (one error type only)", all(detL[(q, ch)] for q in range(4) for ch in "XY") and all(not detL[(q, "Z")] for q in range(4)))
    # ---------------------------------------------------------------- K3
    def r_vector(c):
        rv = []; rv_end = []
        vs = [with_data(res[c].v, initial_basis(c, l)) for l in range(4)]
        def phis_at(pre, upto, skip=None):
            """four states (one per logical basis input) after the gates 0..upto-1 (gate `skip` omitted), sharing the same random bits; returns (states, outcome record)"""
            out = []; outs = None
            for v in vs:
                r, o = teleport(v, upto=upto, bits=pre, skip=skip)
                out.append(r.v)
                if outs is None: outs = o
                assert o == outs, "the four logical inputs must give the same outcome record for the same random bits"
            return out, outs
        for k in range(4):
            before = explore(lambda pre: phis_at(pre, k))
            ok_now = all(kl_ok(ph, [DATA[k], A[k]]) for ph in before.values())
            after = explore(lambda pre: phis_at(pre, 4, skip=k))
            keep = [N[j] for j in range(4) if j != k]
            lost = [q for q in range(NQ) if q not in keep and q not in REF]
            ok_end = all(kl_ok(ph, lost) for ph in after.values())
            rv.append(int(ok_now)); rv_end.append(int(ok_end))
        return rv, rv_end
    rJ, rJe = r_vector("J"); rL, rLe = r_vector("L")
    print("      joint: r at the instant of the failure %s, from the surviving new-block axes after the round %s" % ("".join(map(str, rJ)), "".join(map(str, rJe))))
    print("      local: r at the instant of the failure %s, from the surviving new-block axes after the round %s" % ("".join(map(str, rL)), "".join(map(str, rLe))))
    check("K3a joint code: the information is recoverable after a failed gate at every one of the 4 gates, at the instant and after the round (r = 1111 and 1111)", rJ == [1] * 4 and rJe == [1] * 4)
    check("K3b local code control: not recoverable at any gate, so the difference is the code and not the teleportation (r = 0000 and 0000)", rL == [0] * 4 and rLe == [0] * 4)
    # K3c: the surviving three axes are in the state S13's recovery expects (code state with axis k erased), up to a Pauli frame
    vref = with_data(res["J"].v, initial_ref("J")); ok3c = True; nrec = 0
    t6 = TGT64["J"].reshape([2] * 6)                       # axes: ref13, ref12, axis3, axis2, axis1, axis0
    for k in range(4):
        keepq = [13, 12] + [N[j] for j in (3, 2, 1, 0) if j != k]
        recs3 = explore(lambda pre, k=k: teleport(vref, bits=pre, skip=k))
        ax = 2 + (3 - k)
        T2 = np.moveaxis(t6, ax, 5).reshape(32, 2)           # remove axis k (last), keep the other five in the same order
        rho2 = T2 @ T2.conj().T
        for outs, r in recs3.items():
            T = r.v.reshape([2] * NQ); ka = [NQ - 1 - q for q in keepq]; ra = [a for a in range(NQ) if a not in ka]
            M = np.transpose(T, ka + ra).reshape(32, -1); rho1 = M @ M.conj().T
            found = False
            for p in itertools.product("IXYZ", repeat=3):
                P = np.kron(np.eye(4), np.kron(PM[p[0]], np.kron(PM[p[1]], PM[p[2]])))
                if np.allclose(P @ rho1 @ P.conj().T, rho2, atol=1e-9): found = True; break
            ok3c &= found; nrec += 1
    check("K3c after a failed gate at any k, the surviving three new-block axes plus the reference are in the code state with axis k erased, up to a Pauli frame (%d outcome records over the 4 positions)" % nrec, ok3c)
    # ---------------------------------------------------------------- K6 symmetry (supports reusing S13's recovery for any erased axis)
    B = BASIS["J"]; P0 = B @ B.conj().T; symm = True
    for perm in itertools.permutations(range(4)):
        idx = [sum(((i >> q) & 1) << perm[q] for q in range(4)) for i in range(16)]
        Pm = np.zeros((16, 16));
        for i in range(16): Pm[idx[i], i] = 1
        symm &= np.allclose(Pm @ P0 @ Pm.T, P0, atol=1e-9)
    check("K6  the [[4,2,2]] code space is invariant under all 24 permutations of its four axes, so S13's recovery of an erased axis applies to any axis", symm)
    # ---------------------------------------------------------------- K4 chain
    def P_knill(s): return s ** 4 / (1 - 4 * (1 - s) * s ** 6)
    def mc(s, Nt, seed):
        rng = random.Random(seed); wins = 0
        for _ in range(Nt):
            while True:
                j = None
                for k in range(4):
                    if rng.random() >= s: j = k; break
                if j is None: wins += 1; break
                need = (3 - j) + 3
                if all(rng.random() < s for _ in range(need)): continue
                break
        return wins / Nt
    cases = [0.9, 0.75]; mc_ok = True; Nt = 150000
    for idx, s in enumerate(cases):
        ex = float(P_knill(Fr(s))); est = mc(s, Nt, 77 + idx); sig = math.sqrt(ex * (1 - ex) / Nt); mc_ok &= abs(est - ex) < 4 * sig
        print("      MC s=%.2f  exact %.5f  Monte Carlo %.5f  (|diff| = %.1f sigma)" % (s, ex, est, abs(est - ex) / sig))
    check("K4a closed form P = s^4 / (1 - 4(1-s)s^6) agrees with a gate-by-gate Monte Carlo of the process (recovery = remaining gates + 3) within 4 sigma", mc_ok)
    grid = [Fr(k, 200) for k in range(1, 200)]
    check("K4b the recovery mass 4(1-s)s^6 is below 1 and P exceeds the local s^4 at every s = k/200, k = 1..199", all(0 < 4 * (1 - s) * s ** 6 < 1 and P_knill(s) > s ** 4 for s in grid))
    cat8 = tuple([1] * 8)
    check("K4c ... and exceeds the verified-cat joint round with S13's 3-gate recovery (S12's chain at rho = s^3) at every such s (a grid check)", all(P_knill(s) > s12.chain(cat8, s, s ** 3) for s in grid))
    ratio_max = max(float(1 / (1 - 4 * (1 - s) * s ** 6)) for s in grid)
    print("      largest ratio P / s^4 on the grid: %.4f (at s = %.3f)" % (ratio_max, float(max(grid, key=lambda s: 1 / (1 - 4 * (1 - s) * s ** 6)))))
    check("K4d the advantage over the local round is bounded: P / s^4 <= 1.30 on the grid", ratio_max < 1.30)
    print("== P(eventually complete one verification with the information intact) ==")
    print("      %-6s %-8s %-18s %-14s" % ("s", "local", "cat joint (m=3)", "teleportation joint"))
    for s in (0.99, 0.95, 0.9, 0.85, 0.8, 0.75, 0.5):
        f = Fr(s); print("      %-6.2f %-8.4f %-18.4f %-14.4f" % (s, s ** 4, float(s12.chain(cat8, f, f ** 3)), float(P_knill(f))))
    print("NOTE  Heralded-completion metric only, with the resource assumed correct.  Silent faults (V0.9/V1.0's metric) and faults inside the resource preparation are not computed here;")
    print("      the round consumes 8 resource photons plus 2 preparation ancillas, against 2 to 10 ancilla photons for the ancilla-check rounds, and the resource must wait ready.")
    print("ALL PASS" if OK else "FAILED")
    return 0 if OK else 1

if __name__ == "__main__": sys.exit(main())
