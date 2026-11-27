#!/usr/bin/env python3
"""S05: state-vector re-implementation of the V0.9/V1.0 Pauli-frame engine (model M2), first and second order.

The checkpoints classify circuit faults by propagating Pauli frames through Clifford circuits.  Here the same
circuits (read-only, from V1.0's builders) are executed as explicit complex state vectors with real measurements,
a random logical input state, and every single fault (and every fault pair) injected, and the result is
classified from the actual data state and the actual measurement record -- no frame propagation, no class
tables.  The location-weighted coefficients are compared with what V0.9 printed.

Fault model M2 (as in the checkpoints): after each non-measurement operation, each non-identity Pauli on the
operation's qubits (3 for a one-qubit operation or preparation, 15 for a two-qubit gate); each measurement may flip
its record.  A location with n faults gives each fault weight 1/n.
Categories (from the simulation): detected = some detector parity odd; pass_clean = no detection, data state
equals the ideal (fidelity 1); silent = no detection, data still in the code space but a different state;
pass_damaged = no detection, data outside the code space (caught by the next round); false_reject = detection with
undamaged data; caught_damage = detection with damaged data.

Claims
  W1  Per round, the number of locations and faults and the four first-order coefficients agree with V0.9's
      printed table to its 3 printed decimals.                                           DERIVED (independent method)
  W2  The second-order silent coefficient (pairs of faults at distinct locations, neither silent alone) agrees with
      V0.9's printed 1.244, 2.427, 2.320 (and 9.902 for the verified cat when run).    DERIVED (independent method)
Author-side: same author, different method; this is not independent reproduction by someone else.
Requires numpy.  Run with python3 -I.
"""
import importlib.util, itertools, os, re, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
spec = importlib.util.spec_from_file_location("v10_rounds", os.path.join(ROOT, "explorations", "common", "v10_rounds.py"))
v10 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v10)

OK = True
def check(name, ok):
    global OK
    OK = OK and bool(ok)
    print(("PASS  " if ok else "FAIL  ") + name)

def run_cat():   # the verified cat has 14 qubits and ~50k fault pairs; opt in with --cat
    return "--cat" in sys.argv

PAULI = {"I": np.eye(2, dtype=complex), "X": np.array([[0, 1], [1, 0]], dtype=complex), "Z": np.diag([1, -1]).astype(complex)}
PAULI["Y"] = 1j * PAULI["X"] @ PAULI["Z"]
HAD = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)

class Sim:
    def __init__(self, nq):
        self.nq = nq; self.N = 1 << nq
        idx = np.arange(self.N); self.idx = idx
        self.bit = [(idx >> q) & 1 for q in range(nq)]
    def one(self, v, U, q):
        v = v.reshape(-1, 2, 1 << q)                      # axes: high bits, qubit q, low bits
        return np.einsum("ab,hbl->hal", U, v).reshape(-1)
    def cnot(self, v, c, t):
        out = v.copy(); m = self.bit[c] == 1
        out[m] = v[self.idx[m] ^ (1 << t)]; return out
    def cz(self, v, a, b):
        return np.where((self.bit[a] == 1) & (self.bit[b] == 1), -v, v)
    def pauli(self, v, p):          # p: {qubit: 'X'|'Y'|'Z'}
        for q, s in p.items(): v = self.one(v, PAULI[s], q)
        return v
    def measure_z(self, v, q, branch=None):
        """Projective Z measurement.  Deterministic outcomes are taken as they are.  A random outcome (p1 = 1/2, which happens
        for the individual X measurements of a cat state) is resolved by `branch` (0 or 1); returns (state, outcome, was_random)."""
        p1 = float(np.sum(np.abs(v[self.bit[q] == 1]) ** 2))
        rnd = False
        if p1 > 1 - 1e-9: out = 1
        elif p1 < 1e-9: out = 0
        else:
            if branch is None: raise RuntimeError("random measurement outcome (p1=%.6f) and no branch given" % p1)
            out = branch; rnd = True
        v = np.where(self.bit[q] == out, v, 0)
        v = v / np.linalg.norm(v)
        if out: v = self.one(v, PAULI["X"], q)             # reset to |0>
        return v, out, rnd

def run(sim, ops, psi, faults=(), choice=0, count=None):
    """faults: list of (op_index, kind, payload); kind 'p' = Pauli dict after op_index, 'm' = flip record of a measurement op."""
    v = np.zeros(sim.N, dtype=complex); v[:16] = psi          # data qubits 0..3 are the 4 least significant bits
    rec = 0; ri = 0
    after = {}; flips = set()
    for i, kind, pl in faults:
        if kind == "p": after.setdefault(i, []).append(pl)
        else: flips.add(i)
    for i, op in enumerate(ops):
        k = op[0]
        if k == "P0": pass
        elif k == "P+": v = sim.one(v, HAD, op[1])
        elif k == "H": v = sim.one(v, HAD, op[1])
        elif k == "CNOT": v = sim.cnot(v, op[1], op[2])
        elif k == "CZ": v = sim.cz(v, op[1], op[2])
        elif k in ("MZ", "MX"):
            if k == "MX": v = sim.one(v, HAD, op[1])
            v, out, rnd = sim.measure_z(v, op[1], branch=(choice >> ri) & 1)
            if rnd:
                ri += 1
            if i in flips: out ^= 1
            if out: rec |= 1 << op[2]
        for pl in after.get(i, []): v = sim.pauli(v, pl)
    if count is not None: count.append(ri)
    return v[:16], rec

def enumerate_locations(ops):
    locs = []
    for i, op in enumerate(ops):
        if op[0] in ("MZ", "MX"): locs.append([(i, "m", None)]); continue
        qs = [op[1], op[2]] if op[0] in ("CNOT", "CZ") else [op[1]]
        opts = []
        for combo in itertools.product("IXYZ", repeat=len(qs)):
            if all(c == "I" for c in combo): continue
            opts.append((i, "p", {q: c for q, c in zip(qs, combo) if c != "I"}))
        locs.append(opts)
    return locs

CODES = {"L": [("ZZII",), ("IIZZ",)], "J": [("ZZZZ",), ("XXXX",)]}
def data_pauli_apply(sim4, v, s):      # s string over 4 data qubits, qubit 0 = least significant
    for q, c in enumerate(s):
        if c != "I": v = sim4.one(v, PAULI[c], q)
    return v

def main():
    rounds = v10.load()
    log = open(os.path.join(ROOT, "reproduction", "execution-logs", "v0.9.stdout.txt"), encoding="utf-8").read()
    ref = {}
    for m in re.finditer(r"^\s+(L conv \(baseline\)|J conv|J flag|J cat \(verified\))\s+(\d+)\s+(\d+) \|\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+) \|", log, re.M):
        if m.group(1) in ref: continue          # the log prints the M2 table first and the M3 table later; use the first (M2)
        ref[m.group(1)] = (int(m.group(2)), int(m.group(3)), float(m.group(4)), float(m.group(5)), float(m.group(6)), float(m.group(7)))
    m2 = re.search(r"second-order silent coefficient from fault PAIRS \(M2\) is ([\d.]+) local, ([\d.]+) joint conventional, ([\d.]+) flagged, ([\d.]+) verified cat", log)
    ref2 = dict(zip(["L conv (baseline)", "J conv", "J flag", "J cat (verified)"], [float(x) for x in m2.groups()]))
    names = ["L conv (baseline)", "J conv", "J flag"] + (["J cat (verified)"] if run_cat() else [])
    rng = np.random.default_rng(20261127)
    sim4 = Sim(4)
    for nm in names:
        R = rounds[nm]; ops = R["ops"]; dets = R["dets"]; code = R["code"]
        sim = Sim(R["nq"])
        # random logical state in the code space: project a random vector, normalise
        Pc = None
        def proj(v):
            for (g,) in CODES[code]:
                v = (v + data_pauli_apply(sim4, v, g)) / 2
            return v
        psi = proj(rng.normal(size=16) + 1j * rng.normal(size=16)); psi /= np.linalg.norm(psi)
        cnt0 = []; base, rec0 = run(sim, ops, psi, count=cnt0); nrand = cnt0[0]
        print('      %s: %d random-outcome measurements in the fault-free circuit (individual X readouts of a cat state are random; only their parity is deterministic)' % (nm, nrand))
        check("%s: fault-free run returns the input state and an all-zero record" % nm, abs(abs(np.vdot(psi, base)) - 1) < 1e-9 and rec0 == 0)
        locs = enumerate_locations(ops)
        nfault = sum(len(l) for l in locs)
        def classify(faults, choice=0):
            v, rec = run(sim, ops, psi, faults, choice)
            det = any(bin(rec & m).count("1") & 1 for m in dets)
            f = abs(np.vdot(psi, v)) ** 2
            incode = float(np.real(np.vdot(v, proj(v))))
            if not det:
                if f > 1 - 1e-9: return "pass_clean"
                return "silent" if incode > 1 - 1e-9 else "pass_damaged"
            return "false_reject" if f > 1 - 1e-9 else "caught_damage"
        t0 = time.time(); c1 = {"silent": 0.0, "pass_damaged": 0.0, "false_reject": 0.0, "caught_damage": 0.0, "pass_clean": 0.0}
        cls = []      # per location: list of (category, fault)
        for loc in locs:
            row = []
            for fl in loc:
                cat = classify([fl]); c1[cat] += 1 / len(loc); row.append((cat, fl))
            cls.append(row)
        if nrand:
            allb = list(range(1 << nrand)); dep = 0
            for row in cls:
                for cat0, fl in row:
                    if any(classify([fl], b) != cat0 for b in allb): dep += 1
            print("      %s: single faults whose category depends on the random branch: %d of %d" % (nm, dep, nfault))
            check("%s: every single-fault category is the same on all %d measurement branches (branch 0 may be used for pairs)" % (nm, 1 << nrand), dep == 0)
            import random as _r
            rr = _r.Random(5); flat = [(i, f) for i, row in enumerate(cls) for c, f in row if c != "silent"]
            bad = 0; samp = 300
            for _ in range(samp):
                (ia, fa), (ib, fb) = rr.sample(flat, 2)
                if ia == ib: continue
                c0 = classify([fa, fb], 0)
                if any(classify([fa, fb], b) != c0 for b in allb[:: max(1, len(allb) // 32)]): bad += 1
            print("      %s: %d random fault pairs checked on 32 branches each: %d branch-dependent" % (nm, samp, bad))
            check("%s: pair categories were branch independent in the sample (so branch 0 is used for all pairs)" % nm, bad == 0)
        if nm in ref:
            rl, rf, rs, rp, rfr, rcd = ref[nm]
            print("      %-18s locations %d faults %d | silent %.3f damaged-pass %.3f false-reject %.3f caught-damage %.3f   (V0.9 printed: %d %d | %.3f %.3f %.3f %.3f)" % (nm, len(locs), nfault, c1["silent"], c1["pass_damaged"], c1["false_reject"], c1["caught_damage"], rl, rf, rs, rp, rfr, rcd))
            check("W1 %s: locations, faults and the four first-order coefficients match V0.9 to its printed decimals" % nm,
                  (len(locs), nfault) == (rl, rf) and all(abs(a - b) < 5.1e-4 for a, b in zip((c1["silent"], c1["pass_damaged"], c1["false_reject"], c1["caught_damage"]), (rs, rp, rfr, rcd))))
        # second order: unordered pairs of distinct locations, neither single fault silent
        S2 = 0.0
        for a in range(len(locs)):
            for b in range(a + 1, len(locs)):
                for ca, fa in cls[a]:
                    if ca == "silent": continue
                    for cb, fb in cls[b]:
                        if cb == "silent": continue
                        if classify([fa, fb]) == "silent": S2 += 1 / (len(locs[a]) * len(locs[b]))
        print("      %-18s second-order silent coefficient %.3f  (V0.9 printed %.3f)   [%.0f s]" % (nm, S2, ref2[nm], time.time() - t0))
        check("W2 %s: second-order silent coefficient matches V0.9 to its printed decimals" % nm, abs(S2 - ref2[nm]) < 5.1e-4)
    print("ALL PASS" if OK else "SOME CHECKS FAILED")
    return 0 if OK else 1

if __name__ == "__main__":
    sys.exit(main())
