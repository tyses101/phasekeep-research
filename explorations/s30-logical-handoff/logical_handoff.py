#!/usr/bin/env python3
"""S30: logical handoff of the two [[4,2,2]] logical qubits to a physically separate register: six mechanisms verified against an entangled reference, exact single-fault (and, for one mechanism, double-fault) classification, round trips and break-even against staying.

Setting.  The source register holds V1.0's joint code [[4,2,2]] (axes 0, 1 on photon A and axes 2, 3 on photon B).  A two-qubit reference R is entangled with the two logical qubits (a Choi state), so a handoff that preserves arbitrary logical states, relative phases AND entanglement
with the outside is exactly one whose output, restricted to (R, destination), equals the intended Choi state.  Mechanisms (destination qubits start in |0>):
   M1  decode, then move each data qubit with two CNOTs into an UNENCODED destination (U2: two qubits on one photon)                  M2  decode, then SWAP (three CNOTs per qubit)
   M3  decode, then teleport each data qubit through an offline Bell pair (two measurements and two classically controlled Paulis per qubit)
   M4  decode so that both data qubits sit on ONE photon (A), then route that photon (coherent routing; the move itself contains no gate)  M5  direct encoded-state transfer: move all four code qubits with two CNOTs each (destination holds the same [[4,2,2]])
   M6  decode, move, then ENCODE into a three-qubit continuity code with two CNOTs: X3 (stabilizer XXX, detects Y and Z) or Z3 (ZZZ, detects X and Y)
Decoding is the inverse of a standard encoder (CNOT, CNOT, CNOT, CNOT, CNOT, H); its two syndrome qubits are its only detection.  Fault model M2 as in V0.9: after every gate every non-identity Pauli on its qubits with equal weight; a flip after a preparation; a flip of a measured record; a
Pauli after a classically controlled Pauli; every location faults with probability p.  A single fault is HARMLESS, DETECTED (a perfect final check of the stabilizers of the code that then holds the information, plus the decode syndrome, is nonzero) or SILENT (clean checks, wrong output).
Claims
  H0  Each mechanism's output equals the intended state: M1-M4 against two independently built Bell pairs (R1-D1, R2-D2); M5 against the source state relabelled onto the destination; M6 by five stabilizer expectation values; the input is in the code space with a maximally mixed reference.     DERIVED
      Computational handoff: after M1, G in {logical Pauli, H, controlled-Z, T} at the destination gives the target with G applied (fidelity 1) and the plain handoff is not that target.                                                                                     DERIVED
  H1  Separate cost metrics per mechanism (no combined score) and exact lower bounds on gates across a cut from Schmidt ranks (each CNOT or CZ raises or lowers the Schmidt rank across a cut by at most a factor of 2).                                                          DERIVED
  H2  Exact first-order classification of every single fault: silent, detected, harmless coefficients.  M5 has no first-order silent fault; the decode-based mechanisms have.                                                                                         DERIVED
  H3  Negative controls: faulty handoffs that keep the apparent structure (omitted CNOT, unintended CZ, wrong destination assignment, stabilizer-preserving logical Pauli, coherent logical phase error) pass structure tests and fail only the reference-fidelity test.            DERIVED
  H4  Round trips (out, w parked layers, back) and break-even against staying in the source register: first-order terms exact; for M5 also the exact second-order gate coefficient and the gate-park cross coefficient (exhaustive double faults).  Idle rates are ASSUMED.         DERIVED, ASSUMED rates
  H6  Loss exposure of the parked register by hosting (fatal single and pair losses) and of the transfer circuits (photons touched).                                                                                                               DERIVED
  H5  A computational handoff adds no inter-photon gate; it adds one fault location per non-Pauli G (all options silent) and none for a logical Pauli (a frame update).                                                                                                    DERIVED
Not claimed: that any mechanism is physically realisable; that a heralded photonic two-qubit gate acts as the CNOT used here (success probability, loss and failure modes are NOT in the fault model: V1.0 and S08-S14); any rate or latency; unheralded loss; the comparison with a logical gate
inside the code (not synthesised); that the gate counts are minimal; second-order terms of M1-M4, M6; the continuity code under a measured-syndrome protocol (only a perfect final check).  Author-side; not an independent reproduction.  Requires numpy.  Run with python3 -I.
"""
import importlib.util, math, os, sys, time
from fractions import Fraction as Fr
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
def _load(name, rel):
    sp = importlib.util.spec_from_file_location(name, os.path.join(ROOT, *rel)); m = importlib.util.module_from_spec(sp)
    sys.modules[name] = m; sp.loader.exec_module(m); return m
s29 = _load("s29", ["explorations", "s29-relational-structure-continuity", "relational_structure_continuity.py"])

OK = True
def check(name, ok):
    global OK
    OK = OK and bool(ok); print(("PASS  " if ok else "FAIL  ") + name, flush=True)

# ---------------------------------------------------------------- state-vector primitives (qubit q is bit q of the basis index)
N = 10; DIM = 1 << N; IDX = np.arange(DIM); BITS = [(IDX >> q) & 1 for q in range(N)]
def h_(v, q):
    t = v.reshape(-1, 2, 1 << q); a, b = t[:, 0, :].copy(), t[:, 1, :].copy(); t[:, 0, :] = (a + b) / math.sqrt(2); t[:, 1, :] = (a - b) / math.sqrt(2); return t.reshape(-1)
def x_(v, q): return v[IDX ^ (1 << q)]
def z_(v, q): return v * (1 - 2 * BITS[q])
def y_(v, q): return 1j * x_(z_(v, q), q)
def t_(v, q): return v * np.where(BITS[q], np.exp(1j * math.pi / 4), 1.0)
def cnot_(v, c, t): return np.where(BITS[c], v[IDX ^ (1 << t)], v)
def cz_(v, a, b): return v * (1 - 2 * (BITS[a] & BITS[b]))
PAULI = {"X": x_, "Y": y_, "Z": z_}
def pauli_str(v, P):
    for q, c in P.items():
        if c != "I": v = PAULI[c](v, q)
    return v

# ---------------------------------------------------------------- circuits.  op = (kind, qubits...); kinds ending in _off are offline resource preparation
def kind(op): return op[0].split("_")[0]
def is_off(op): return op[0].endswith("_off")
def run(ops, v, faults=()):
    fd = {}
    for i, f in faults: fd.setdefault(i, []).append(f)
    for i, op in enumerate(ops):
        k = kind(op)
        if k == "H": v = h_(v, op[1])
        elif k == "T": v = t_(v, op[1])
        elif k in ("CNOT", "FFX"): v = cnot_(v, op[1], op[2])
        elif k in ("CZ", "FFZ"): v = cz_(v, op[1], op[2])
        elif k == "X": v = x_(v, op[1])
        elif k == "Z": v = z_(v, op[1])
        for f in fd.get(i, ()): v = pauli_str(v, f)
    return v
P2 = [(u, w) for u in "IXYZ" for w in "IXYZ" if (u, w) != ("I", "I")]
def locations(ops):
    """(op index, list of fault dicts, kind): one-qubit gates and PARK 3 Paulis; two-qubit gates 15; P0 and MFLIP one flip; FFX/FFZ 3 Paulis on the corrected qubit"""
    out = []
    for i, op in enumerate(ops):
        k = kind(op); qs = op[1:]
        if k in ("H", "T", "PARK"): out.append((i, [{qs[0]: c} for c in "XYZ"], k))
        elif k in ("CNOT", "CZ"): out.append((i, [{qs[0]: u, qs[1]: w} for u, w in P2], k))
        elif k in ("FFX", "FFZ"): out.append((i, [{qs[1]: c} for c in "XYZ"], k))
        elif k in ("P0", "MFLIP"): out.append((i, [{qs[0]: "X"}], k))
    return out

R1, R2 = 4, 5; DST = (6, 7); TEL = (8, 9); DST4 = (6, 7, 8, 9)
PHOTON = {0: "A", 1: "A", 2: "B", 3: "B", 4: "R", 5: "R", 6: "C", 7: "C", 8: "D", 9: "D"}
ROLES_SPLIT = (0, 3, 1, 2); ROLES_ONE = (2, 3, 0, 1)         # (s, pq, da, db): data on qubit 1 (photon A) and 2 (photon B) / data on qubits 0, 1 (both on photon A, syndromes on photon B)
def decode(s, pq, da, db): return [("CNOT", s, pq), ("CNOT", s, db), ("CNOT", s, da), ("CNOT", db, pq), ("CNOT", da, pq), ("H", s)]
def encode(s, pq, da, db): return list(reversed(decode(s, pq, da, db)))
def move2(a, d): return [("P0", d), ("CNOT", a, d), ("CNOT", d, a)]
def swap3(a, d): return [("P0", d), ("CNOT", a, d), ("CNOT", d, a), ("CNOT", a, d)]
def tele(a, t, d): return [("P0_off", t), ("P0_off", d), ("H_off", t), ("CNOT_off", t, d), ("CNOT", a, t), ("H", a), ("MFLIP", a), ("MFLIP", t), ("FFX", t, d), ("FFZ", a, d)]
def enter_x3(d1, d2, da): return [("P0", da), ("H", da), ("CNOT", da, d1), ("CNOT", da, d2)]
def enter_z3(d1, d2, da): return [("P0", da), ("CNOT", d1, da), ("CNOT", d2, da)]
def unrev(ops): return [o for o in reversed(ops) if kind(o) != "P0"]          # inverse of a Clifford segment without its preparations

def bell_target(pairs):
    v = np.zeros(DIM, complex); v[0] = 1.0
    for a, b in pairs: v = cnot_(h_(v, a), a, b)
    return v
def choi(roles):
    v = bell_target([(R1, roles[2]), (R2, roles[3])]); return run(encode(*roles), v)
def split(w, K):
    t = w.reshape([2] * N); ax = [N - 1 - q for q in K]; rest = [a for a in range(N) if a not in ax]; return np.transpose(t, rest + ax).reshape(-1, 1 << len(K))
def reduced_fid(v, target_v, K):
    """fidelity of v's reduced state on the qubits K with the pure state target_v restricted to K (target_v must be a product of its K part and the rest)"""
    tv = split(target_v, K); row = tv[np.argmax((np.abs(tv) ** 2).sum(1))]; phi = row / np.linalg.norm(row); return float((np.abs(split(v, K) @ phi.conj()) ** 2).sum())
def expect(v, P): return float(np.vdot(v, pauli_str(v, P)).real)
def prob_zero(v, qs):
    m = np.ones(DIM, bool)
    for q in qs: m &= (BITS[q] == 0)
    return float((np.abs(v[m]) ** 2).sum())
def ebits(v, A):
    s = np.linalg.svd(split(v, list(A)), compute_uv=False); s = s[s > 1e-9]; return len(s), float(-(s ** 2 * np.log2(s ** 2)).sum())
def inter(ops): return sum(1 for o in ops if kind(o) in ("CNOT", "CZ") and PHOTON[o[1]] != PHOTON[o[2]])
def cross(ops, dest): return sum(1 for o in ops if kind(o) in ("CNOT", "CZ") and (PHOTON[o[1]] in dest) != (PHOTON[o[2]] in dest))
def depth(ops):
    t = {}; d = 0
    for o in ops:
        if kind(o) in ("MFLIP", "PARK"): continue
        lv = 1 + max(t.get(q, 0) for q in o[1:]); [t.__setitem__(q, lv) for q in o[1:]]; d = max(d, lv)
    return d
def photons(ops): return len({PHOTON[q] for o in ops for q in o[1:]} - {"R"})

def classify(ops, v0, vid, K, clean_fn, soft=False, only=None):
    """exact first-order classification.  Returns ({silent, detected, harmless} as Fractions summed over locations (soft: silent uses 1 - fidelity), {kind: ...})"""
    c = {"silent": Fr(0), "detected": Fr(0), "harmless": Fr(0)}; det = {}
    for i, opts, kd in locations(ops):
        if only is not None and kd not in only: continue
        n = len(opts); loc = {"silent": Fr(0), "detected": Fr(0), "harmless": Fr(0)}
        for f in opts:
            v = run(ops, v0, [(i, f)])
            if not clean_fn(v): loc["detected"] += 1; continue
            F = reduced_fid(v, vid, K)
            if soft: loc["silent"] += Fr(round((1 - F) * 4096), 4096); loc["harmless"] += Fr(round(F * 4096), 4096)
            else:
                assert F < 1e-6 or F > 1 - 1e-6, (ops[i], f, F)
                loc["harmless" if F > 0.5 else "silent"] += 1
        d = det.setdefault(kd, {"silent": Fr(0), "detected": Fr(0), "harmless": Fr(0)})
        for k2 in c: c[k2] += loc[k2] / n; d[k2] += loc[k2] / n
    return c, det

# per-qubit Pauli channel after w layers (closed form by the Walsh-Hadamard transform on the group Z2^2 with index x | z << 1); weights (wx, wy, wz)
def pq_dist(q, wts, w):
    wx, wy, wz = wts; s = wx + wy + wz; v = np.array([1 - q, q * wx / s, q * wz / s, q * wy / s]); w = np.asarray(w, float)
    lam = [sum(v[g] * (-1) ** bin(a & g).count("1") for g in range(4)) for a in range(4)]
    return np.array([sum(lam[a] ** w * (-1) ** bin(a & g).count("1") for a in range(4)) / 4 for g in range(4)])
def mem_prob(c, pq, subset):
    tot = 0.0
    for P in subset:
        pr = 1.0
        for qb in range(c.n): pr = pr * pq[((P[0] >> qb) & 1) | (((P[1] >> qb) & 1) << 1)]
        tot = tot + pr
    return tot
def mem_silent(c, q, wts, w): return mem_prob(c, pq_dist(q, wts, w), c.L)
def mem_reject(c, q, wts, w): return 1 - mem_prob(c, pq_dist(q, wts, w), c.N)

def main():
    t00 = time.time(); H = ROLES_SPLIT; da, db = H[2], H[3]; dec = decode(*H); dec1 = decode(*ROLES_ONE)
    v_in = choi(H); v_in1 = choi(ROLES_ONE)
    # ------------------------------------------------------------ H0
    stab = all(abs(expect(v_in, {q: c for q in range(4)}) - 1) < 1e-9 for c in "XZ") and all(abs(expect(v_in1, {q: c for q in range(4)}) - 1) < 1e-9 for c in "XZ")
    sR = ebits(v_in, [R1, R2]); check("H0a the Choi inputs (both role assignments) are stabilized by XXXX and ZZZZ and the reference is maximally mixed (Schmidt rank %d, entropy %.3f ebits): they are code states carrying two logical qubits entangled with R" % (sR[0], sR[1]), stab and sR[0] == 4 and abs(sR[1] - 2) < 1e-9)
    mech = {"M1": dec + move2(da, DST[0]) + move2(db, DST[1]), "M2": dec + swap3(da, DST[0]) + swap3(db, DST[1]), "M3": dec + tele(da, TEL[0], DST[0]) + tele(db, TEL[1], DST[1]), "M4": dec1,
            "M5": [o for q, e in zip(range(4), DST4) for o in move2(q, e)]}
    mech["M6x"] = mech["M1"] + enter_x3(DST[0], DST[1], 8); mech["M6z"] = mech["M1"] + enter_z3(DST[0], DST[1], 8)
    FID = {}
    for k in ("M1", "M2", "M3"): FID[k] = reduced_fid(run(mech[k], v_in), bell_target([(R1, DST[0]), (R2, DST[1])]), list(DST) + [R1, R2])
    FID["M4"] = reduced_fid(run(mech["M4"], v_in1), bell_target([(R1, ROLES_ONE[2]), (R2, ROLES_ONE[3])]), [ROLES_ONE[2], ROLES_ONE[3], R1, R2])
    relab = bell_target([(R1, DST4[H[2]]), (R2, DST4[H[3]])]); relab = run(encode(*[DST4[r] for r in H]), relab)
    FID["M5"] = reduced_fid(run(mech["M5"], v_in), relab, list(DST4) + [R1, R2])
    # M6: five stabilizer expectation values uniquely fix the five-qubit state on (R1, R2, D1, D2, Da)
    D1, D2, Da = DST[0], DST[1], 8; vx = run(mech["M6x"], v_in); vz = run(mech["M6z"], v_in)
    sx = [{D1: "X", D2: "X", Da: "X"}, {D1: "X", R1: "X"}, {D2: "X", R2: "X"}, {D1: "Z", Da: "Z", R1: "Z"}, {D2: "Z", Da: "Z", R2: "Z"}]
    sz = [{D1: "Z", D2: "Z", Da: "Z"}, {D1: "Z", R1: "Z"}, {D2: "Z", R2: "Z"}, {D1: "X", Da: "X", R1: "X"}, {D2: "X", Da: "X", R2: "X"}]
    ex = [expect(vx, g) for g in sx]; ez = [expect(vz, g) for g in sz]
    def rank_gf2(gs, n=N):
        rows = [sum((1 << q if c in "XY" else 0) | (1 << (q + n) if c in "ZY" else 0) for q, c in g.items()) for g in gs]; r = 0
        for b in range(2 * n):
            piv = next((i for i in range(r, len(rows)) if rows[i] >> b & 1), None)
            if piv is None: continue
            rows[r], rows[piv] = rows[piv], rows[r]
            for i in range(len(rows)):
                if i != r and rows[i] >> b & 1: rows[i] ^= rows[r]
            r += 1
        return r
    def anti(g, h): return sum(1 for q in g if q in h and g[q] != h[q]) % 2
    ind = rank_gf2(sx) == 5 and rank_gf2(sz) == 5 and all(anti(a, b) == 0 for a in sx for b in sx) and all(anti(a, b) == 0 for a in sz for b in sz)
    FID["M6x"] = min(ex); FID["M6z"] = min(ez)
    check("H0b output equals the intended state: fidelity %s for M1, M2, M3, M4, M5 (targets: two independent Bell pairs, or the source state relabelled onto the destination for M5); M6: the five commuting independent generators of the Choi state of X3 / Z3 all have expectation +1 (min %.6f / %.6f) which fixes the state uniquely. "
          "So arbitrary logical states, their relative phases and their entanglement with the reference are preserved in every mechanism (a faultless, gate-count-level statement)" % (", ".join("%.6f" % FID[k] for k in ("M1", "M2", "M3", "M4", "M5")), FID["M6x"], FID["M6z"]),
          all(abs(FID[k] - 1) < 1e-9 for k in FID) and ind)
    Gs = {"logical Z (Pauli)": [("Z", DST[0])], "logical H": [("H", DST[0])], "logical CZ(1,2)": [("CZ", DST[0], DST[1])], "logical T (non-Clifford)": [("T", DST[0])]}
    ok = True; gf = []
    for nm, gops in Gs.items():
        vt = run(gops, bell_target([(R1, DST[0]), (R2, DST[1])])); F = reduced_fid(run(mech["M1"] + gops, v_in), vt, list(DST) + [R1, R2]); Fw = reduced_fid(run(mech["M1"], v_in), vt, list(DST) + [R1, R2]); gf.append((F, Fw)); ok &= abs(F - 1) < 1e-9 and Fw < 1 - 1e-6
    check("H0c computational handoff (M1 then G at the destination) reproduces the target with G applied: fidelity %s for %s; the plain handoff output has fidelity %s with those targets (so the check can tell them apart)" % (
          ", ".join("%.6f" % f for f, _ in gf), ", ".join(Gs), ", ".join("%.3f" % w for _, w in gf)), ok)
    # ------------------------------------------------------------ H1
    sides = {"M1": {"C"}, "M2": {"C"}, "M3": {"C"}, "M5": {"C", "D"}, "M6x": {"C"}, "M6z": {"C"}}
    print("      cost metrics per mechanism (hosting: source A = axes 0,1, B = axes 2,3; destination C = axes 6,7 (+ D = axes 8,9: teleport resource halves for M3, destination photon 2 for M5, the extra axis of X3/Z3 for M6)).  'cut' = two-qubit gates with one end in the destination photons.  Offline = resource preparation outside the information path")
    print("      %-4s %5s %5s %6s %5s %5s %6s %5s %5s %6s %5s %6s" % ("", "ops", "2q", "inter", "cut", "data", "offl", "meas", "ff", "prep0", "phot", "depth"))
    MET = {}
    for k in ("M1", "M2", "M3", "M4", "M5", "M6x", "M6z"):
        o = mech[k]; MET[k] = dict(ops=len(o), q2=sum(1 for x in o if kind(x) in ("CNOT", "CZ")), inter=inter(o), cut=cross(o, sides[k]) if k in sides else 0, data=sum(1 for x in o if kind(x) in ("CNOT", "CZ", "H", "T") and not is_off(x)),
                                   off=sum(1 for x in o if is_off(x)), meas=sum(1 for x in o if kind(x) == "MFLIP"), ff=sum(1 for x in o if kind(x) in ("FFX", "FFZ")), prep=sum(1 for x in o if kind(x) == "P0"), phot=photons(o), dep=depth(o))
        m = MET[k]; print("      %-4s %5d %5d %6d %5s %5d %6d %5d %5d %6d %5d %6d" % (k, m["ops"], m["q2"], m["inter"], m["cut"] if k in sides else "n/a", m["data"], m["off"], m["meas"], m["ff"], m["prep"], m["phot"], m["dep"]))
    print("      reading: M3 has 0 data-touching gates across the cut (only its 2 offline Bell-pair gates cross) but 2 Bell pairs, 4 measurements and 4 feed-forward Paulis; M4 has 0 across the cut because the photon itself moves; M2's third CNOT per qubit acts with control |0> on a |0> destination, so it changes nothing and only adds fault locations")
    third = all(abs(np.vdot(run(mech["M1"], v_in), run(mech["M2"], v_in)) - 1) < 1e-9 for _ in [0])
    # lower bounds from Schmidt ranks
    rk = lambda v, A: ebits(v, A)[0]
    rB0, rB1 = rk(v_in1, [2, 3]), rk(run(dec1, v_in1), [2, 3]); rB0s, rB1s = rk(v_in, [2, 3]), rk(run(dec, v_in), [2, 3])
    rC = rk(run(mech["M1"], v_in), list(DST)); rCD = rk(run(mech["M5"], v_in), list(DST4)); lb = lambda a, b: math.ceil(math.log2(max(a, b) / min(a, b)) - 1e-9)
    lbs = {"decode with the data on photon A: photon B must end disentangled (rank %d -> %d)" % (rB0, rB1): lb(rB0, rB1), "decode with the data split over A and B: photon B keeps one data qubit (rank %d -> %d)" % (rB0s, rB1s): lb(rB0s, rB1s), "move into U2 (photon C: rank 1 -> %d)" % rC: lb(1, rC), "move into C4 (photons C, D: rank 1 -> %d)" % rCD: lb(1, rCD)}
    print("      exact lower bounds on two-qubit gates across the stated cut (rank ratio, rounded up in log2; one CNOT or CZ changes the Schmidt rank by at most a factor 2): " + "; ".join("%s: %d" % (a, b) for a, b in lbs.items()))
    check("H1 lower bounds %s are below the gate counts used (decode with the data on photon A: 4 inter-photon gates against bound %d; split data: 3 against %d; move into U2: 4 across the cut against %d; direct move of the code: 8 against %d), so none of the circuits is shown minimal; "
          "M2's third CNOT is idle on a |0> destination (the M1 and M2 outputs coincide: %s)" % (list(lbs.values()), list(lbs.values())[0], list(lbs.values())[1], list(lbs.values())[2], list(lbs.values())[3], third),
          third and list(lbs.values()) == [2, 1, 2, 2] and MET["M4"]["inter"] == 4 and inter(dec) == 3 and MET["M1"]["cut"] == 4 and MET["M5"]["cut"] == 8)
    # ------------------------------------------------------------ H2
    def clean_dec(roles): return lambda v: prob_zero(v, (roles[0], roles[1])) > 0.5
    def clean_stab(qs): return lambda v: all(abs(expect(v, {q: c for q in qs}) - 1) < 1e-9 for c in "XZ")
    def clean_c(code, qs, roles):
        f = clean_dec(roles)
        if code == "x3": return lambda v: f(v) and abs(expect(v, {q: "X" for q in qs}) - 1) < 1e-9
        if code == "z3": return lambda v: f(v) and abs(expect(v, {q: "Z" for q in qs}) - 1) < 1e-9
        return f
    C1 = {}; t0 = time.time()
    for k, code, K, vin_, roles in (("M1", None, list(DST) + [R1, R2], v_in, H), ("M2", None, list(DST) + [R1, R2], v_in, H), ("M3", None, list(DST) + [R1, R2], v_in, H), ("M4", None, [ROLES_ONE[2], ROLES_ONE[3], R1, R2], v_in1, ROLES_ONE),
                                    ("M6x", "x3", list(DST) + [8, R1, R2], v_in, H), ("M6z", "z3", list(DST) + [8, R1, R2], v_in, H)):
        vid = run(mech[k], vin_); C1[k] = classify(mech[k], vin_, vid, K, clean_c(code, (6, 7, 8), roles))
    vid5 = run(mech["M5"], v_in); C1["M5"] = classify(mech["M5"], v_in, vid5, list(DST4) + [R1, R2], clean_stab(DST4))
    print("      first-order coefficients c (silent probability = c p to first order), by mechanism; locations / single faults; silent coefficient by location kind  [%.0f s]" % (time.time() - t0))
    for k in ("M1", "M2", "M3", "M4", "M5", "M6x", "M6z"):
        c, d = C1[k]; lo = locations(mech[k]); print("      %-4s silent %-8s (%6.3f)  detected %-9s (%6.3f)  harmless %-7s (%5.3f)   %2d locations, %3d faults   silent by kind: %s" % (k, c["silent"], float(c["silent"]), c["detected"], float(c["detected"]), c["harmless"], float(c["harmless"]), len(lo), sum(len(o) for _, o, _ in lo),
              {kk: float(vv["silent"]) for kk, vv in d.items() if vv["silent"]}))
    check("H2a every single fault is classified: the three coefficients sum to the number of locations for all seven circuits", all(sum(C1[k][0].values()) == len(locations(mech[k])) for k in C1))
    check("H2b first-order silent coefficients: M1 %s, M2 %s, M3 %s, M4 %s, M6x %s, M6z %s are all positive (the decode window and the move leave data unprotected), M5 has %s: with its destination checked perfectly every single fault in a direct encoded transfer is detected or harmless (a first-order statement; double faults in H4)" % (
          *[C1[k][0]["silent"] for k in ("M1", "M2", "M3", "M4", "M6x", "M6z")], C1["M5"][0]["silent"]), C1["M5"][0]["silent"] == 0 and all(C1[k][0]["silent"] > 0 for k in ("M1", "M2", "M3", "M4", "M6x", "M6z")))
    print("      note: M3 reports detected only when the decode syndrome fires; its faults after the decode (teleport CNOTs, measurements, corrections) are silent or harmless (see by kind).  The silent coefficients are NOT comparable across mechanisms without also comparing which register each leaves the information in (M4 leaves it on a photon that still has to be routed; M5 in a code)")
    # ------------------------------------------------------------ H3
    vt_bell = bell_target([(R1, DST[0]), (R2, DST[1])]); KD = list(DST) + [R1, R2]
    ctrl = []
    miss = mech["M1"][:-3] + [("P0", DST[1]), ("CNOT", db, DST[1])]                                       # second qubit's second CNOT omitted
    ctrl.append(("omitted second CNOT of the second move", miss, v_in, vt_bell, KD, clean_dec(H)))
    ctrl.append(("unintended CZ between the two data qubits after the decode", dec + [("CZ", da, db)] + move2(da, DST[0]) + move2(db, DST[1]), v_in, vt_bell, KD, clean_dec(H)))
    swap_assign = dec + move2(da, DST[1]) + move2(db, DST[0]); ctrl.append(("logical qubits delivered to each other's slot", swap_assign, v_in, vt_bell, KD, clean_dec(H)))
    ctrl.append(("M5 plus a logical Pauli (Z0 Z2) on the destination", mech["M5"] + [("Z", DST4[0]), ("Z", DST4[2])], v_in, relab, list(DST4) + [R1, R2], clean_stab(DST4)))
    th = 0.3
    v5 = run(mech["M5"], v_in); v5c = math.cos(th / 2) * v5 - 1j * math.sin(th / 2) * pauli_str(v5, {DST4[0]: "Z", DST4[2]: "Z"})
    rows = []
    for nm, ops, vin_, tgt, K, cf in ctrl:
        vo = run(ops, vin_); rows.append((nm, cf(vo), reduced_fid(vo, tgt, K))); 
    rows.append(("M5 plus a coherent logical phase exp(-i 0.3/2 Z0Z2)", clean_stab(DST4)(v5c), reduced_fid(v5c, relab, list(DST4) + [R1, R2])))
    for nm, cl, F in rows: print("      %-62s structure test passes: %-5s  fidelity with the intended state %.4f" % (nm, cl, F))
    sR5 = ebits(run(mech["M5"] + [("Z", DST4[0]), ("Z", DST4[2])], v_in), list(DST4)); 
    check("H3 negative controls: every faulty handoff passes its structure test (decode syndrome clean or destination stabilizers satisfied: %s), the Z0Z2 case also keeps the destination maximally entangled with the reference (entropy %.3f ebits), and every one has fidelity below 1 with the intended state (%s); "
          "only the reference-fidelity test separates them" % (all(r[1] for r in rows), sR5[1], ", ".join("%.3f" % r[2] for r in rows)), all(r[1] for r in rows) and all(r[2] < 0.99 for r in rows) and abs(sR5[1] - 2) < 1e-9 and abs(rows[3][2]) < 1e-9)
    # ------------------------------------------------------------ H4: round trips
    C4, U2, X3, Z3 = s29.Code("C4"), s29.Code("U2"), s29.Code("X3"), s29.Code("Z3")
    wcheck = np.array([0, 1, 3, 10, 50]); q0 = 2.3e-3; pw = pq_dist(q0, (1.0, 1.0, 5.0), wcheck); T = np.zeros((4, 4)); v_ = np.array([1 - q0, q0 / 7, 5 * q0 / 7, q0 / 7])
    for a in range(4):
        for c2 in range(4): T[a ^ c2, a] += v_[c2]
    mm = np.array([np.linalg.matrix_power(T, int(w))[:, 0] for w in wcheck]).T
    check("H4a the closed-form per-qubit Pauli distribution after w layers (Walsh-Hadamard on Z2^2) equals the explicit w-fold convolution (max difference %.1e over w = 0, 1, 3, 10, 50, biased weights 1 : 1 : 5), and for one unbiased C4 layer the silent probability over q^2 is %.3f, equal to S29's recorded Z2c value 2.000 (an independent implementation of the same memory model)" % (np.abs(pw - mm).max(), float(mem_silent(C4, 1e-6, (1.0, 1.0, 1.0), 1)) / 1e-12),
          np.abs(pw - mm).max() < 1e-12 and abs(float(mem_silent(C4, 1e-6, (1.0, 1.0, 1.0), 1)) / 1e-12 - 2.0) < 1e-3)
    chk_c4 = lambda v: clean_stab((0, 1, 2, 3))(v)
    def rt_ops(fwd, park, back): return fwd + [("PARK", q) for q in park] + back
    def rt_clean(extra_zero=()):
        def f(v):
            if not chk_c4(v): return False
            if extra_zero and prob_zero(v, extra_zero) < 0.5: return False
            return True
        return f
    RT = {}
    RT["M1"] = (rt_ops(mech["M1"], DST, unrev(mech["M1"])), rt_clean(), DST)
    RT["M5"] = (rt_ops(mech["M5"], DST4, unrev(mech["M5"])), rt_clean(), DST4)
    RT["M6x"] = (rt_ops(mech["M6x"], (6, 7, 8), unrev(mech["M6x"])), rt_clean(extra_zero=(8,)), (6, 7, 8))
    RT["M6z"] = (rt_ops(mech["M6z"], (6, 7, 8), unrev(mech["M6z"])), rt_clean(extra_zero=(8,)), (6, 7, 8))
    RC = {}
    for k, (ops, cf, pk) in RT.items():
        vid = run(ops, v_in); assert reduced_fid(vid, v_in, [0, 1, 2, 3, R1, R2]) > 1 - 1e-9, k
        g, _ = classify(ops, v_in, vid, [0, 1, 2, 3, R1, R2], cf, only={"H", "CNOT", "CZ", "P0", "T"}); p_, _ = classify(ops, v_in, vid, [0, 1, 2, 3, R1, R2], cf, only={"PARK"}); RC[k] = (g, p_)
    print("      round trip (out, parked, back to the source code; perfect final check of the source stabilizers, and of the continuity code's residual ancilla for M6): first-order coefficients of the GATES, and of ONE parked layer (all parked qubits)")
    for k in RC: g, p_ = RC[k]; print("      %-4s gates: silent %-7s (%6.3f) detected %-8s (%6.3f)   parked layer: silent %s detected %s harmless %s" % (k, g["silent"], float(g["silent"]), g["detected"], float(g["detected"]), p_["silent"], p_["detected"], p_["harmless"]))
    check("H4b parked unencoded qubits (M1) are silently hit by every single fault (silent %s per layer), parked code qubits of M5 never silently at first order (silent %s, all %s detected per layer); the first-order gate coefficients of the round trip are M1 %s, M5 %s, M6x %s, M6z %s" % (
          RC["M1"][1]["silent"], RC["M5"][1]["silent"], RC["M5"][1]["detected"], *[RC[k][0]["silent"] for k in ("M1", "M5", "M6x", "M6z")]),
          RC["M1"][1]["silent"] == 2 and RC["M1"][1]["detected"] == 0 and RC["M5"][1]["silent"] == 0 and RC["M5"][1]["detected"] == 4 and RC["M5"][0]["silent"] == 0)
    print("      parked layer for the three-qubit codes (first order, single Pauli per qubit; silent fraction by which Paulis are weight-1 logicals): X3 silent %s detected %s; Z3 silent %s detected %s" % (RC["M6x"][1]["silent"], RC["M6x"][1]["detected"], RC["M6z"][1]["silent"], RC["M6z"][1]["detected"]))
    # second-order exact coefficients of the M5 round trip: gate pairs and gate-park cross terms
    t0 = time.time(); ops5 = RT["M5"][0]; vid5 = run(ops5, v_in); K0 = [0, 1, 2, 3, R1, R2]; cf5 = RT["M5"][1]
    loc5 = locations(ops5); G5 = [l for l in loc5 if l[2] != "PARK"]; P5 = [l for l in loc5 if l[2] == "PARK"]
    def pairs(A, B, same):
        tot = Fr(0)
        for ia in range(len(A)):
            for ib in range(ia + 1 if same else 0, len(B)):
                (i, oa, _), (j, ob, _) = A[ia], B[ib]; s = 0
                for fa in oa:
                    for fb in ob:
                        v = run(ops5, v_in, [(i, fa), (j, fb)])
                        if cf5(v) and reduced_fid(v, vid5, K0) < 0.5: s += 1
                tot += Fr(s, len(oa) * len(ob))
        return tot
    cgg = pairs(G5, G5, True); cgp = pairs(G5, P5, False)
    print("      M5 round trip exact second-order coefficients: gate-gate %s (%.3f), gate-park %s (%.3f per parked layer; exhaustive over %d + %d locations)  [%.0f s]" % (cgg, float(cgg), cgp, float(cgp), len(G5), len(P5), time.time() - t0))
    c2C4 = float(mem_silent(C4, 1e-6, (1.0, 1.0, 1.0), 1)) / 1e-12
    check("H4c the M5 round trip has second-order silent coefficient %.3f p^2 from its gates plus %.3f p q_m per parked layer from gate-park pairs, against the memory-only %.3f (rho p w)^2 of staying in C4 (V1.0 unbiased)" % (float(cgg), float(cgp), c2C4), cgg > 0 and c2C4 > 0)
    # break-even
    pp = 1e-3; W = np.arange(1, 3001)
    def stay_silent(rho_p, wts): return mem_silent(C4, rho_p * pp, wts, W)
    def stay_reject(rho_p, wts): return mem_reject(C4, rho_p * pp, wts, W)
    def hand(k, rho_m, wts):
        q = rho_m * pp; g, p_ = RC[k]
        if k == "M1": S = float(g["silent"]) * pp + mem_silent(U2, q, wts, W); R = float(g["detected"]) * pp + 0 * W
        elif k == "M5": S = float(cgg) * pp ** 2 + float(cgp) * pp * q * W + mem_silent(C4, q, wts, W); R = float(g["detected"]) * pp + mem_reject(C4, q, wts, W)
        else:
            c = X3 if k == "M6x" else Z3; S = float(g["silent"]) * pp + mem_silent(c, q, wts, W); R = float(g["detected"]) * pp + mem_reject(c, q, wts, W)
        return S, R
    def windows(better):
        idx = np.nonzero(better)[0]
        if len(idx) == 0: return None
        brk = np.nonzero(np.diff(idx) > 1)[0]; starts = [idx[0]] + [idx[b + 1] for b in brk]; ends = [idx[b] for b in brk] + [idx[-1]]; return [(int(W[s]), int(W[e])) for s, e in zip(starts, ends)]
    BE = {}
    print("      break-even windows (p = 1e-3; unbiased; w = parked layers; the window lists the w for which the handoff round trip has the SMALLER silent probability than idling in C4 for the same w; None = no such w up to 3000; a window ending at 3000 is cut by the scan range; second-order and cross terms only, so values at large rho_m w are extrapolations)")
    print("      rows: continuity register; columns: rho_m (continuity idle ratio) for rho_p (source idle ratio) = 0.3 | 1 | 3")
    for k in ("M1", "M5", "M6x"):
        for rho_m in (0.0, 0.1, 1.0):
            row = []
            for rho_p in (0.3, 1.0, 3.0):
                Ss, Rs = hand(k, rho_m, (1.0, 1.0, 1.0)); Sy = stay_silent(rho_p, (1.0, 1.0, 1.0)); BE[(k, rho_m, rho_p)] = windows(Ss < Sy); row.append(str(BE[(k, rho_m, rho_p)]))
            print("      %-4s rho_m = %-4g  %s" % (k, rho_m, "  |  ".join(row)))
    # analytic leading order for M1 with a perfect continuity memory: the window starts where C4's idle silent probability (c2 (rho p w)^2) reaches c1 p
    c1 = float(RC["M1"][0]["silent"]); dev = []
    for pe in (1e-3, 1e-4, 1e-5, 1e-6):
        Wl = np.arange(1, 40001); Sy = mem_silent(C4, pe, (1.0, 1.0, 1.0), Wl); wn = int(Wl[np.argmax(Sy > c1 * pe)]); wa = math.sqrt(c1 / (c2C4 * pe)); dev.append((pe, wn, wa, wn / wa - 1))
    print("      M1 with a perfect continuity memory (rho_m = 0, rho_p = 1): window start w* against the leading-order estimate sqrt(c1 / (c2 p)) (c1 = %s, c2 = %.2f): " % (RC["M1"][0]["silent"], c2C4) + "; ".join("p = %g: w* %d vs %.1f (%+.1f %%)" % (a, b, c, 100 * d) for a, b, c, d in dev))
    check("H4d the leading-order window start for M1 with a perfect continuity memory, w* = sqrt(c1 / (c2 rho_p^2 p)), is an asymptote: the exact first crossing deviates from it by %s at p = 1e-3, 1e-4, 1e-5, 1e-6 (decreasing towards 0 as p falls); the deviation is the neglected next order in rho_p p w" % ", ".join("%+.1f %%" % (100 * d[3]) for d in dev),
          all(dev[i][3] > dev[i + 1][3] > 0 for i in range(3)) and dev[-1][3] < 0.02)
    ok5 = all(BE[("M5", 0.1, rp)] is not None for rp in (0.3, 1.0, 3.0)) and BE[("M5", 1.0, 1.0)] is None
    wl = {rp: BE[("M5", 0.0, rp)][0][0] for rp in (0.3, 1.0, 3.0)}
    check("H4e M5 (direct encoded transfer): with a continuity memory of the same idle rate (rho_m = rho_p = 1) the round trip never beats staying (window %s) because it adds gates to the same code; with a quieter memory (rho_m = 0) it first wins at w = %s layers for rho_p = 0.3, 1, 3, with rho_m = 0.1 %s; "
          "the window start scales as sqrt(c_gg / (c2 (rho_p^2 - rho_m^2))): %s from that formula (cross term neglected)" % (BE[("M5", 1.0, 1.0)], ", ".join(str(wl[r]) for r in wl), BE[("M5", 0.1, 1.0)][0][0] if BE[("M5", 0.1, 1.0)] else None,
          ", ".join("%.1f" % math.sqrt(float(cgg) / (c2C4 * rp ** 2)) for rp in (0.3, 1.0, 3.0))), ok5)
    # separate metrics at chosen w: silent, rejection, silent | accepted
    print("      separate metrics at p = 1e-3, rho_p = 1 (unbiased): stay in C4 against round trip through M1 (U2), M5 (C4) and M6x (X3), continuity idle ratio rho_m = 0.1; per w: silent (unconditional) / rejected / silent | accepted")
    print("      %-5s %-30s %-30s %-30s %-30s" % ("w", "stay (C4)", "M1 round trip (U2)", "M5 round trip (C4)", "M6x round trip (X3)"))
    for w in (1, 10, 30, 100, 300, 1000):
        i = w - 1; cells = []
        for k in (None, "M1", "M5", "M6x"):
            if k is None: S, Rj = stay_silent(1.0, (1.0, 1.0, 1.0))[i], stay_reject(1.0, (1.0, 1.0, 1.0))[i]
            else: Ss, Rr = hand(k, 0.1, (1.0, 1.0, 1.0)); S, Rj = Ss[i], Rr[i] if not np.isscalar(Rr) else Rr
            cells.append("%.1e / %.3f / %.1e" % (S, Rj, S / (1 - Rj))); 
        print("      %-5d %-30s %-30s %-30s %-30s" % (w, *cells))
    # bias: Z-dominant continuity X3 against C4
    print("      Z-dominant noise (weights 1 : 1 : b, same b for the source's idling and the continuity memory), X3 against C4, rho_p = rho_m = 1: windows in w where the X3 round trip has the smaller silent probability")
    for b in (1.0, 10.0, 100.0, 1000.0):
        Ss, _ = hand("M6x", 1.0, (1.0, 1.0, b)); Sy = stay_silent(1.0, (1.0, 1.0, b)); BE[("M6x", "bias", b)] = windows(Ss < Sy); print("      b = %-6g X3 window %s" % (b, BE[("M6x", "bias", b)]))
    check("H4f entering a three-qubit continuity code pays a first-order silent cost (M6x gates %s p) that C4's second-order idling only reaches after tens of layers; X3 under Z-dominant bias has a window of w values where it beats idling in C4, and under unbiased noise (b = 1) the window is %s; the existence and position of the windows depend on the ASSUMED idle ratios and bias" % (RC["M6x"][0]["silent"], BE[("M6x", "bias", 1.0)]),
          BE[("M6x", "bias", 100.0)] is not None)
    # ------------------------------------------------------------ H5
    base = C1["M1"][0]["silent"]; extra = {}; ok = True
    for nm, gops in Gs.items():
        ops = mech["M1"] + gops; vid = run(ops, v_in); soft = "T" in nm
        c, _ = classify(ops, v_in, vid, KD, clean_dec(H), soft=soft); extra[nm] = c["silent"] - base; ok &= inter(ops) == inter(mech["M1"]) and cross(ops, {"C"}) == 4
    ex_vals = list(extra.values())
    print("      computational handoff: change of the first-order silent coefficient after adding G to M1: " + ", ".join("%s %s (%.4f)" % (k, v, float(v)) for k, v in extra.items()))
    check("H5 G at the destination adds no inter-photon or cross-cut gate; its first-order silent change is %s for the logical Pauli (a frame update has no fault location), %s for H and %s for CZ (one location each, all options silent), and %s for T (the same location; a Pauli error before T becomes a non-Pauli operator, but the fidelity with the maximally entangled Choi target depends only on its trace, so earlier faults score exactly as without T: this is an entanglement-fidelity statement, not a statement about every input state)" % (
          ex_vals[0], ex_vals[1], ex_vals[2], ex_vals[3]), ok and ex_vals == [0, 1, 1, 1])
    # ------------------------------------------------------------ H6: unheralded-loss exposure of the parked register (erasure of whole photons)
    def fatal(c, hosting, k):
        """number of subsets of k photons whose joint loss erases a set that contains a logical operator (unrecoverable)"""
        import itertools
        n = 0
        for combo in itertools.combinations(range(len(hosting)), k):
            E = {q for i in combo for q in hosting[i]}; n += any(all(((P[0] | P[1]) >> q) & 1 == 0 or q in E for q in range(c.n)) for P in c.L)
        return n
    HOST = [("C4 on A, B (source, V1.0)", C4, [(0, 1), (2, 3)]), ("C4 on four one-axis photons", C4, [(0,), (1,), (2,), (3,)]), ("U2 on one photon (M1, M2, M3)", U2, [(0, 1)]), ("U2 on two one-axis photons", U2, [(0,), (1,)]),
            ("X3 on a two-axis and a one-axis photon (M6x)", X3, [(0, 1), (2,)]), ("Z3 on a two-axis and a one-axis photon (M6z)", Z3, [(0, 1), (2,)])]
    LOSS = {}
    print("      loss exposure of the PARKED register (a lost photon is an erasure at a known place; fatal = the erased qubits contain a logical operator; unheralded loss is not modelled): photons, fatal single losses, fatal pairs of losses")
    for nm, c, hs in HOST:
        LOSS[nm] = (len(hs), fatal(c, hs, 1), fatal(c, hs, 2) if len(hs) > 1 else None); print("      %-48s %d photon(s)   fatal singles %d   fatal pairs %s" % (nm, *LOSS[nm]))
    peak = {k: MET[k]["phot"] for k in ("M1", "M3", "M4", "M5", "M6x")}
    check("H6 loss exposure while parked: C4 on two two-axis photons has 2 photons and both single losses are fatal; on four one-axis photons no single loss is fatal but all 6 pairs are; U2 on ONE photon has 1 photon with its loss fatal (half the fatal single-photon exposure of the source); X3 and Z3 hosted on two photons have 2 fatal single losses (distance 1 for erasure too, S29). "
          "During the transfer itself the circuits touch %s photons (M1, M3, M4, M5, M6x): a smaller parked register lowers the exposure only after the transfer, and the transfer's own exposure is larger than the source's 2 photons" % ", ".join(str(peak[k]) for k in peak),
          LOSS[HOST[0][0]] == (2, 2, 1) and LOSS[HOST[1][0]] == (4, 0, 6) and LOSS[HOST[2][0]] == (1, 1, None) and LOSS[HOST[3][0]][1] == 2 and LOSS[HOST[4][0]][:2] == (2, 2) and LOSS[HOST[5][0]][:2] == (2, 2)
          and all(peak[k] > 2 for k in ("M1", "M3", "M5", "M6x")))
    print("NOTE  every inter-photon gate here is an ideal CNOT or CZ with no success probability, loss or failure modes (V1.0 section C); the teleportation Bell pairs are assumed available; idle ratios are assumed, not measured and any bias applies to idling only (gate faults stay unbiased); the lower bounds apply to gate-based transfer without extra resources.  Total wall-clock %.0f s" % (time.time() - t00))
    print("ALL PASS" if OK else "FAILED")
    return 0 if OK else 1

if __name__ == "__main__": sys.exit(main())
