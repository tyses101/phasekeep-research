#!/usr/bin/env python3
"""S07: what a heralded failure of a two-qubit gate could do to the logical information, tested on the real V1.0 circuits.

V1.0 left "what does a failed gate do to the data?" open (open problem 1).  Here the failure is given an explicit, testable meaning
and evaluated exactly (state vectors) on the circuits V1.0 defines, which are read, not modified.  TWO models are kept side by side
because they disagree on a question that matters (does the ancilla-extraction design matter at all?).

MODEL A  "abort at the failing gate, track what the lost ancilla knew"   (full-state Knill-Laflamme test)
  A failed two-qubit gate heralds itself and ERASES the qubits it acts on ("EraseAxis"), or the whole photons hosting them
  ("ErasePhoton", with the hosting given).  The round stops there; all earlier gates succeeded.  With |Phi_j> (j = 1..4) the full state
  just before the failing gate for an orthonormal basis of the code space, the logical information survives the loss of the qubits L
  if and only if   Tr_{not L} |Phi_j><Phi_k|  =  delta_jk rho_L   (the lost qubits learn nothing about the logical state).
  r_i = 1 if that holds for the i-th two-qubit gate, else 0.   P_A(s) = s^n + sum_i s^(i-1) (1-s) r_i.
MODEL B  "the round continues, erasures accumulate, ancillas are ignored" (code-only criterion; this was the first model written)
  Each data-touching gate fails independently with probability 1-s and erases its data axis (or photon); the final erased set must
  support no nontrivial logical operator of the data code.  The state of the failed gate's ancilla is NOT considered.
Both give an UPPER bound on usable outcomes (the recovery circuit and its own gate failures are not modelled).

Claims (DERIVED means: exact on the stated assumptions; the failure semantics themselves are ASSUMED, replaceable by a measurement)
  F1  Per-gate recoverability pattern r_i of Model A for every V1.0 round, both hostings and both erasure semantics.
  F2  Model A, 1 axis/photon: local r = 0000; joint conventional r = 10011001 (the middle gates of each check fail because the lost
      ancilla holds a weight-2 parity, which is a logical operator); joint flagged and joint cat: r = 1 at every gate.
  F3  Model B: P_B is s^4 for local and 4 s^6 - 3 s^8 for every joint design (flagged, cat, conventional alike); joint beats local
      only for s > 1/sqrt(3) = 0.577350... ; with 2 axes/photon under ErasePhoton the joint rounds give s^8 (any failure erases a photon).
  F4  Model A, 2 axes/photon, ErasePhoton: every DATA-TOUCHING failure is non-recoverable in every joint round (a whole photon is erased and
      the photon-level distance is 1, S02); only the data-free ancilla-ancilla failures remain recoverable.   [the first version of
      this script claimed "no failure at all is recoverable"; that was over-stated and its own check caught it, see run-history.txt]
  F5  Therefore "P_keep is independent of the extraction design" holds in Model B and is FALSE in Model A: the verdict on the design depends
      on whether the state of the failed gate's ancilla is tracked.  Which model is closer to a real gate is open problem 1; this
      script does not decide it.
Author-side; not an independent reproduction.  Requires numpy.
"""
import importlib.util, itertools, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
def _load(name, rel):
    sp = importlib.util.spec_from_file_location(name, os.path.join(ROOT, *rel)); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
v10 = _load("v10_rounds", ["explorations", "common", "v10_rounds.py"])
sv = _load("sv", ["explorations", "s05-statevector-crosscheck", "statevector_crosscheck.py"])

OK = True
def check(name, ok):
    global OK
    OK = OK and bool(ok); print(("PASS  " if ok else "FAIL  ") + name)

CODES = {"L": ["ZZII", "IIZZ"], "J": ["ZZZZ", "XXXX"]}
KNOWN_OPS = {"P0", "P+", "H", "CNOT", "CZ", "MZ", "MX"}

def code_basis(code):
    sim = sv.Sim(4); cols = []
    for k in range(16):
        e = np.zeros(16, dtype=complex); e[k] = 1
        for g in CODES[code]: e = (e + sim.pauli(e, {q: c for q, c in enumerate(g) if c != "I"})) / 2
        cols.append(e)
    u, s, vh = np.linalg.svd(np.array(cols).T, full_matrices=False)
    assert np.sum(s > 1e-9) == 4
    return u[:, :4]

def guard_ops(R):
    """True only if (i) every op kind is one the replay handles, (ii) every ancilla qubit's first op is a preparation (P0 or P+), and (iii) no qubit is
    prepared a second time (no qubit reuse after measurement), so replaying 'P0' as a no-op on a fresh |0> register is exact"""
    ok = True
    for nm, r in R.items():
        first = {}; preps = {}
        for op in r["ops"]:
            if op[0] not in KNOWN_OPS: ok = False
            qs = [op[1], op[2]] if op[0] in ("CNOT", "CZ") else [op[1]]
            for q in qs:
                first.setdefault(q, op[0])
                if op[0] in ("P0", "P+"): preps[q] = preps.get(q, 0) + 1
        ok &= all(first[q] in ("P0", "P+") for q in first if q >= 4)
        ok &= all(c == 1 for c in preps.values()) and all(q >= 4 for q in preps)
    return ok

def states_before(R, basis, i_stop, branch=0):
    """full states after executing ops[0:i_stop] on each code basis state (ancillas start in |0>; data are qubits 0..3 = low bits)"""
    sim = sv.Sim(R["nq"]); out = []; nrand = 0
    for j in range(4):
        v = np.zeros(sim.N, dtype=complex); v[:16] = basis[:, j]; ri = 0
        for op in R["ops"][:i_stop]:
            k = op[0]
            if k == "P0": pass
            elif k in ("P+", "H"): v = sim.one(v, sv.HAD, op[1])
            elif k == "CNOT": v = sim.cnot(v, op[1], op[2])
            elif k == "CZ": v = sim.cz(v, op[1], op[2])
            else:
                if k == "MX": v = sim.one(v, sv.HAD, op[1])
                v, o, rnd = sim.measure_z(v, op[1], branch=(branch >> ri) & 1)
                if rnd: ri += 1
        out.append(v); nrand = ri
    return sim, out, nrand

def lost_blocks(sim, phis, lost):
    lost = sorted(lost); keep = [q for q in range(sim.nq) if q not in lost]
    A = []
    for v in phis:
        T = v.reshape([2] * sim.nq)
        A.append(np.transpose(T, [sim.nq - 1 - q for q in keep] + [sim.nq - 1 - q for q in lost]).reshape(2 ** len(keep), 2 ** len(lost)))
    return lost, {(j, k): A[j].conj().T @ A[k] for j in range(4) for k in range(4)}

def recoverable(R, basis, i, lost, branch=0):
    sim, phis, _ = states_before(R, basis, i, branch)
    lost, E = lost_blocks(sim, phis, lost); rho = E[(0, 0)]
    return all(np.allclose(E[(j, j)], rho, atol=1e-9) for j in range(4)) and all(np.allclose(E[(j, k)], 0, atol=1e-9) for j in range(4) for k in range(4) if j != k)

PM = {"I": np.eye(2), "X": np.array([[0, 1], [1, 0]]), "Z": np.diag([1., -1.]), "Y": np.array([[0, -1j], [1j, 0]])}
def witness(R, basis, i, lost):
    """lowest-weight Pauli on the lost qubits whose expectation depends on the logical state (explains r = 0); None if none exists"""
    sim, phis, _ = states_before(R, basis, i); lost, E = lost_blocks(sim, phis, lost)
    cands = sorted(itertools.product("IXYZ", repeat=len(lost)), key=lambda p: sum(c != "I" for c in p))
    for p in cands:
        P = np.array([[1.0]])
        for c in p: P = np.kron(P, PM[c])
        diag = [np.sum(P * E[(j, j)]) for j in range(4)]
        off = [np.sum(P * E[(k, j)]) for j in range(4) for k in range(4) if j != k]
        dd = max(abs(d - diag[0]) for d in diag); oo = max(abs(o) for o in off)
        if dd > 1e-9 or oo > 1e-9:
            return lost, "".join(p), [complex(np.round(d, 6)) for d in diag], ("diagonal (separates logical basis states)" if dd > 1e-9 else "off-diagonal (reveals coherence between logical basis states)")
    return None

def pkeep_poly(r):
    n = len(r); poly = {n: 1}
    for i, ri in enumerate(r, start=1):
        if ri: poly[i - 1] = poly.get(i - 1, 0) + 1; poly[i] = poly.get(i, 0) - 1
    return {k: v for k, v in poly.items() if v}
def peval(p, s): return sum(v * s ** k for k, v in p.items())
def pstr(p): return " ".join(("%+d" % v if k == 0 else ("%+d s^%d" % (v, k) if k > 1 else "%+d s" % v)) for k, v in sorted(p.items()))

# ---- Model B (code-only criterion) --------------------------------------------------------------------------------------
def xz(s): return tuple(int(c in "XY") for c in s), tuple(int(c in "ZY") for c in s)
def sp(a, b): return (sum(a[0][i] * b[1][i] + a[1][i] * b[0][i] for i in range(4))) % 2
def stab_group(code):
    g = [xz(s) for s in CODES[code]]; G = set()
    for m in itertools.product((0, 1), repeat=len(g)):
        x = [0] * 4; z = [0] * 4
        for mi, gi in zip(m, g):
            if mi: x = [(a + b) % 2 for a, b in zip(x, gi[0])]; z = [(a + b) % 2 for a, b in zip(z, gi[1])]
        G.add((tuple(x), tuple(z)))
    return G
def has_logical_on(code, E):
    gens = [xz(s) for s in CODES[code]]; G = stab_group(code)
    for p in itertools.product("IXYZ", repeat=4):
        if any(c != "I" and q not in E for q, c in enumerate(p)): continue
        pp = xz("".join(p))
        if all(sp(pp, g) == 0 for g in gens) and pp not in G: return True
    return False
def pmul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): out[i + j] += x * y
    return out
def model_b(R, code, host):
    gates = [op for op in R["ops"] if op[0] in ("CNOT", "CZ") and (op[1] < 4) != (op[2] < 4)]
    axes = [min(op[1], op[2]) for op in gates]; n = len(gates); total = [0] * (n + 1)
    for fail in itertools.product((0, 1), repeat=n):
        E = set()
        for f, ax in zip(fail, axes):
            if f: E |= set(next(h for h in host if ax in h))
        if has_logical_on(code, E): continue
        term = [1]
        for f in fail: term = pmul(term, [1, -1] if f else [0, 1])      # failure: (1 - s); success: s
        for k, c in enumerate(term): total[k] += c
    return {k: v for k, v in enumerate(total) if v}

def main():
    R = v10.load()
    check("G0 every op kind in the V1.0 rounds is handled by the replay (no silent skips), every ancilla starts with a preparation, and no qubit is prepared twice", guard_ops(R))
    bases = {c: code_basis(c) for c in "LJ"}
    # --- controls: the test must be able to say both yes and no ---------------------------------------------------
    sim6 = sv.Sim(R["J conv"]["nq"]); ok_emb = True
    for code in "LJ":
        for j in range(4):
            v = np.zeros(sim6.N, dtype=complex); v[:16] = bases[code][:, j]
            for g in CODES[code]: ok_emb &= np.allclose(sim6.pauli(v, {q: c for q, c in enumerate(g) if c != "I"}), v)
    check("C0 embedded code states are +1 eigenstates of their stabilizers in the larger register (qubit ordering consistent)", ok_emb)
    Jc = R["J conv"]; Lc = R["L conv (baseline)"]
    check("C1 control: erasing one data axis of the joint code is recoverable; erasing two or three is not", recoverable(Jc, bases["J"], 0, [0]) and not recoverable(Jc, bases["J"], 0, [0, 1]) and not recoverable(Jc, bases["J"], 0, [0, 1, 2]))
    check("C2 control: erasing a data axis of the local code (distance 1) is not recoverable", not recoverable(Lc, bases["L"], 0, [0]))
    check("C3 control: after all four CNOTs the ancilla of ZZZZ holds only the stabilizer value (erasing it is harmless), after two CNOTs it holds a logical parity (erasing it is not)",
          recoverable(Jc, bases["J"], 5, [4]) and not recoverable(Jc, bases["J"], 3, [4]))
    # --- F1: tables --------------------------------------------------------------------------------------------------------
    cfg = [("L conv (baseline)", "L"), ("J conv", "J"), ("J flag", "J"), ("J cat (verified)", "J")]
    H1 = [(0,), (1,), (2,), (3,)]; H2 = [(0, 1), (2, 3)]; res = {}; kinds = {}
    for nm, code in cfg:
        ops = R[nm]["ops"]; gates = [(i, op) for i, op in enumerate(ops) if op[0] in ("CNOT", "CZ")]
        kinds[nm] = "".join("D" if (op[1] < 4) != (op[2] < 4) else "a" for _, op in gates)
        for hn, host in (("1 axis/photon", H1), ("2 axes/photon", H2)):
            for sem in ("EraseAxis", "ErasePhoton"):
                r = []
                for i, op in gates:
                    lost = {op[1], op[2]}
                    if sem == "ErasePhoton":
                        for q in list(lost):
                            if q < 4: lost |= set(next(h for h in host if q in h))
                    r.append(1 if recoverable(R[nm], bases[code], i, lost) else 0)
                res[(nm, hn, sem)] = r
    print("== F1 Model A: r_i per two-qubit gate (1 = logical information survives the erasure at that gate; D = data-touching gate, a = ancilla-only) ==")
    for nm, code in cfg:
        print("      %-18s gate kinds %s" % (nm, kinds[nm]))
        for hn in ("1 axis/photon", "2 axes/photon"):
            for sem in ("EraseAxis", "ErasePhoton"):
                print("          %-14s %-12s r = %s" % (hn, sem, "".join(map(str, res[(nm, hn, sem)]))))
    # branch independence for the cat round (random individual X outcomes must not matter)
    cat = R["J cat (verified)"]; gates = [(i, op) for i, op in enumerate(cat["ops"]) if op[0] in ("CNOT", "CZ")]
    bri = True; nr_seen = set()
    for br in (0, 0b10101010, 0b11111111, 0b01010101, 0b00110011):
        for (i, op), r0 in zip(gates, res[("J cat (verified)", "1 axis/photon", "EraseAxis")]):
            bri &= (recoverable(cat, bases["J"], i, {op[1], op[2]}, branch=br) == bool(r0))
        nr_seen.add(states_before(cat, bases["J"], len(cat["ops"]), br)[2])
    check("C4 cat round: r_i is the same for 5 different resolutions of the random individual cat-qubit X outcomes (%s random outcomes seen)" % sorted(nr_seen), bri)
    check("F2a local geometry: no failure is recoverable (r all 0) for either hosting or erasure semantics", all(sum(res[("L conv (baseline)", h, s)]) == 0 for h in ("1 axis/photon", "2 axes/photon") for s in ("EraseAxis", "ErasePhoton")))
    Jr = "".join(map(str, res[("J conv", "1 axis/photon", "EraseAxis")]))
    check("F2b joint conventional, 1 axis/photon, EraseAxis: r = 10011001 (first and last gate of each check recoverable)", Jr == "10011001")
    check("F2c joint flagged and joint cat, 1 axis/photon: r = 1 at every gate under EraseAxis and ErasePhoton", all(all(res[(nm, "1 axis/photon", s)]) for nm in ("J flag", "J cat (verified)") for s in ("EraseAxis", "ErasePhoton")))
    check("F4  2 axes/photon + ErasePhoton: every data-touching gate failure is non-recoverable in every joint round",
          all(r == 0 for nm in ("J conv", "J flag", "J cat (verified)") for r, k in zip(res[(nm, "2 axes/photon", "ErasePhoton")], kinds[nm]) if k == "D"))
    check("F4b the only recoverable failures there are data-free ancilla-ancilla gates (flag: gates 2,5,8,11; cat: all 'a' gates; conventional: none)",
          all((r == 1) == (k == "a") for nm in ("J conv", "J flag", "J cat (verified)") for r, k in zip(res[(nm, "2 axes/photon", "ErasePhoton")], kinds[nm])))
    check("F4c under EraseAxis the hosting changes nothing by construction (r identical for 1 and 2 axes/photon)", all(res[(nm, "1 axis/photon", "EraseAxis")] == res[(nm, "2 axes/photon", "EraseAxis")] for nm, _ in cfg))
    # --- leak witnesses --------------------------------------------------------------------------------------------------
    print("== leak witnesses (why r = 0): lowest-weight Pauli on the lost qubits whose expectation depends on the logical state; values for the 4 logical basis states ==")
    gl = [(i, op) for i, op in enumerate(Jc["ops"]) if op[0] in ("CNOT", "CZ")]
    wit_ok = True
    for g, ((i, op), r) in enumerate(zip(gl, res[("J conv", "1 axis/photon", "EraseAxis")]), start=1):
        if r == 0:
            w = witness(Jc, bases["J"], i, {op[1], op[2]}); wit_ok &= (w is not None)
            print("      J conv gate %d (qubits %d,%d lost): witness %s on qubits %s, %s; diagonal values %s" % (g, op[1], op[2], w[1], w[0], w[3], [("%+.0f" % x.real) for x in w[2]]))
    gl2 = [(i, op) for i, op in enumerate(Lc["ops"]) if op[0] in ("CNOT", "CZ")]
    for g, (i, op) in enumerate(gl2[:1], start=1):
        w = witness(Lc, bases["L"], i, {op[1], op[2]}); wit_ok &= (w is not None)
        print("      L conv gate %d (qubits %d,%d lost): witness %s on qubits %s, %s; diagonal values %s" % (g, op[1], op[2], w[1], w[0], w[3], [("%+.0f" % x.real) for x in w[2]]))
    check("W1 every non-recoverable case shown has an explicit witness operator", wit_ok)
    # --- F3: Model A and Model B -----------------------------------------------------------------------------------------
    L = res[("L conv (baseline)", "1 axis/photon", "EraseAxis")]
    PA = {"local": pkeep_poly(L), "joint conventional": pkeep_poly(res[("J conv", "1 axis/photon", "EraseAxis")]),
          "joint flagged": pkeep_poly(res[("J flag", "1 axis/photon", "EraseAxis")]), "joint cat": pkeep_poly(res[("J cat (verified)", "1 axis/photon", "EraseAxis")])}
    print("== Model A  P_A(s) (1 axis/photon, EraseAxis; ceiling only: recovery not modelled) ==")
    for k, p in PA.items(): print("      %-20s %s" % (k, pstr(p)))
    check("A1 P_A(local) = s^4;  P_A(joint conv) = 1 - s + s^3 - s^5 + s^7;  P_A(flagged) = P_A(cat) = 1", PA["local"] == {4: 1} and PA["joint conventional"] == {0: 1, 1: -1, 3: 1, 5: -1, 7: 1} and PA["joint flagged"] == {0: 1} and PA["joint cat"] == {0: 1})
    H1m = H1; B = {}
    for nm, code in cfg:
        for hn, host in (("1 axis/photon", H1), ("2 axes/photon", H2)):
            B[(nm, hn)] = model_b(R[nm], code, host)
    print("== Model B  P_B(s) (accumulate erasures, ancillas ignored) ==")
    for nm, code in cfg:
        for hn in ("1 axis/photon", "2 axes/photon"): print("      %-18s %-14s %s" % (nm, hn, pstr(B[(nm, hn)])))
    check("B0 P_B(local) = s^4 for either hosting", B[("L conv (baseline)", "1 axis/photon")] == {4: 1} and B[("L conv (baseline)", "2 axes/photon")] == {4: 1})
    check("B1 P_B(joint, 1 axis/photon) = 4 s^6 - 3 s^8 for conventional, flagged AND cat (extraction design does not matter in Model B)",
          all(B[(nm, "1 axis/photon")] == {6: 4, 8: -3} for nm in ("J conv", "J flag", "J cat (verified)")))
    check("B2 P_B(joint, 2 axes/photon) = s^8 (a failure erases a whole photon, which supports a logical operator)", all(B[(nm, "2 axes/photon")] == {8: 1} for nm in ("J conv", "J flag", "J cat (verified)")))
    s0 = 1 / math.sqrt(3); f = lambda s: peval({6: 4, 8: -3}, s) - s ** 4
    check("B3 crossover joint(1 axis/photon) = local at s = 1/sqrt(3) = %.6f; local better below, joint better above (exact root of 3u^2 - 4u + 1 with u = s^2)" % s0,
          abs(f(s0)) < 1e-12 and f(0.5) < 0 < f(0.7))
    print("      %-6s %-9s %-14s %-12s %-12s %-12s" % ("s", "local", "A joint conv", "A flag/cat", "B joint 1ax", "B joint 2ax"))
    for s in (0.95, 0.9, 0.75, 0.577, 0.5, 0.25):
        print("      %-6g %-9.4f %-14.4f %-12.4f %-12.4f %-12.4f" % (s, s ** 4, peval(PA["joint conventional"], s), 1.0, peval({6: 4, 8: -3}, s), s ** 8))
    check("F5 the two models disagree on design dependence: B says all joint designs identical, A says conventional < flagged = cat", PA["joint conventional"] != PA["joint flagged"] and B[("J conv", "1 axis/photon")] == B[("J flag", "1 axis/photon")])
    print("      NOTE  A flagged/cat P = 1 means only that the logical information has not leaked into what the failure erased at that instant.")
    print("            The erased data axis must still be re-created, which needs inter-photon gates of its own, and the unheralded loss floor (S02) is untouched.")
    print("            Erasure is the conservative end: a failure that merely MEASURES the two qubits in a known basis is a post-processing of an erasure, so r = 1 under erasure implies r = 1 there too (data-processing argument; not tested here).")
    print("ALL PASS" if OK else "SOME CHECKS FAILED")
    return 0 if OK else 1

if __name__ == "__main__":
    sys.exit(main())
