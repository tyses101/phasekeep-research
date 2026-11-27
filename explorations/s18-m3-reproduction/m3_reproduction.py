#!/usr/bin/env python3
"""S18: independent state-vector reproduction of V0.9's idle-fault model M3 (first and second order) for the local, joint conventional, flagged and verified-cat rounds.

S05 reproduced V0.9's model M2 (gate, preparation and measurement faults).  V0.9's headline negative result, that flagged extraction stops beating conventional joint extraction at about
p = 1e-3 per location, rests on model M3 (M2 plus a single-qubit Pauli location on every idle live qubit after every operation and one incoming fault on each data axis), which S05 did
not cover.  Here M3 is rebuilt from V0.9's own definition (the enumerator is re-written, not imported), every single fault is run as an explicit state vector, its syndrome and its Pauli
error on the data are read off the final state, and pairs are composed by XOR with V0.9's exact pair definition (distinct locations, neither single fault silent, signatures aggregated).
The composition step is validated against explicit two-fault state-vector runs on sampled pairs.

Claims
  M0  Location and fault counts of model M3 equal V0.9's printed table for the four rounds (40/164, 56/260, 108/460, 290/1066).                                              DERIVED
  M1  The four first-order coefficients per round equal V0.9's printed M3 values to their 3 decimals (e.g. local silent 11.200, joint conventional 0.267, flagged and cat 0).   DERIVED
  M2  The second-order silent coefficient per round equals V0.9's printed M3 value (60.000, 158.249, 426.942, 2314.169) to 3 decimals.                                        DERIVED
  M3  The analytic crossover estimate p* = (4/15) / (S2_flag - S2_conv) from these coefficients lies in the interval V0.9's scan reports (5e-4 .. 3e-3) and rounds to its stated
      "about 1e-3".  (V0.9's scan itself, with exact probabilities, is not redone.)                                                                                           DERIVED
Not claimed: the exact-probability scan of V0.9; the X-bias and loss results of V1.0; independence from V0.9's idle-fault DEFINITION (the definition is taken from V0.9 as stated).
Author-side; not an independent reproduction.  Requires numpy.  Run with python3 -I.
"""
import importlib.util, itertools, os, random, re, sys, time
from fractions import Fraction as Fr
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
def _load(name, rel):
    sp = importlib.util.spec_from_file_location(name, os.path.join(ROOT, *rel)); m = importlib.util.module_from_spec(sp)
    sys.modules[name] = m; sp.loader.exec_module(m); return m
s05 = _load("s05", ["explorations", "s05-statevector-crosscheck", "statevector_crosscheck.py"])
v10 = _load("v10_rounds", ["explorations", "common", "v10_rounds.py"])
Sim = s05.Sim; PAULI = s05.PAULI
par = lambda x: bin(x).count("1") & 1

OK = True
def check(name, ok):
    global OK
    OK = OK and bool(ok); print(("PASS  " if ok else "FAIL  ") + name, flush=True)

STAB = {"L": [(0, 0b0011), (0, 0b1100), (0, 0b1111)], "J": [(15, 0), (0, 15), (15, 15)], "Z": [(0, 0b1111)]}       # non-identity stabilizer elements as (x mask, z mask)
GENS = {"L": ([], [0b0011, 0b1100]), "J": ([0b1111], [0b1111]), "Z": ([], [0b1111])}                                  # (X-type generator masks, Z-type generator masks)

def classify_err(x, z, code):
    """V0.9's four classes of a data Pauli: none, harmless (stabilizer element), detected (leaves the code space), logical"""
    if (x, z) == (0, 0): return "none"
    xg, zg = GENS[code]
    if any(par(z & g) for g in xg) or any(par(x & g) for g in zg): return "detected"
    return "harmless" if (x, z) in STAB[code] else "logical"

def locations(ops, nq):
    """V0.9's model M3 re-written from its definition: incoming Paulis on the four data axes; after every operation its own faults (15 for a two-qubit gate, 3 for a one-qubit
    operation or preparation, one record flip for a measurement) and a location of 3 Paulis on every idle live qubit"""
    alive = set(range(4)); locs = []
    def one(q, i): return [(i, "p", {q: c}) for c in "XYZ"]
    for q in range(4): locs.append(("in", [(-1, "p", {q: c}) for c in "XYZ"]))
    for i, op in enumerate(ops):
        tq = [op[1], op[2]] if op[0] in ("CNOT", "CZ") else [op[1]]
        if op[0] in ("MZ", "MX"): alive.discard(op[1])
        elif op[0] in ("P0", "P+"): alive.add(op[1])
        if op[0] in ("MZ", "MX"): locs.append(("m", [(i, "m", None)]))
        elif len(tq) == 2:
            a, b = tq; fl = []
            for u in "IXYZ":
                for v in "IXYZ":
                    if u == "I" and v == "I": continue
                    fl.append((i, "p", {q: c for q, c in ((a, u), (b, v)) if c != "I"}))
            locs.append(("g", fl))
        else: locs.append(("g", one(tq[0], i)))
        for q in sorted(alive):
            if q not in tq: locs.append(("idle", one(q, i)))
    return locs

class Rnd:
    def __init__(self, name, seed=20261127):
        R = v10.load()[name]; self.name = name; self.ops = R["ops"]; self.dets = R["dets"]; self.code = R["code"]; self.sim = Sim(R["nq"]); self.sim4 = Sim(4)
        rng = np.random.default_rng(seed); psi = rng.normal(size=16) + 1j * rng.normal(size=16)
        for g in ({"L": ["ZZII", "IIZZ"], "J": ["ZZZZ", "XXXX"], "Z": ["ZZZZ"]}[self.code]):
            w = psi
            for q, c in enumerate(g):
                if c != "I": w = self.sim4.one(w, PAULI[c], q)
            psi = (psi + w) / 2
        self.psi = psi / np.linalg.norm(psi)
        cnt = []; s05.run(self.sim, self.ops, self.psi, count=cnt); self.nrand = cnt[0]
        self.locs = locations(self.ops, R["nq"])
        paulis = list(itertools.product("IXYZ", repeat=4)); self.PS = np.zeros((256, 16), dtype=complex); self.xz = []
        for k, pa in enumerate(paulis):
            w = self.psi; x = z = 0
            for q, c in enumerate(pa):
                if c != "I": w = self.sim4.one(w, PAULI[c], q)
                if c in "XY": x |= 1 << q
                if c in "ZY": z |= 1 << q
            self.PS[k] = w; self.xz.append((x, z))
    def run(self, faults, choice=0):
        psi = self.psi; rest = []
        for f in faults:
            if f[0] == -1:
                for q, c in f[2].items(): psi = self.sim4.one(psi, PAULI[c], q)
            else: rest.append(f)
        return s05.run(self.sim, self.ops, psi, rest, choice)
    def effect(self, faults, choice=0):
        """(syndrome as an int, data error (x, z) as a Pauli reproducing the final state from the input)"""
        v, rec = self.run(faults, choice); ov = np.abs(self.PS.conj() @ v); k = int(np.argmax(ov)); assert ov[k] > 1 - 1e-9, "the data must end in a Pauli-error state"
        syn = 0
        for j, m in enumerate(self.dets): syn |= par(rec & m) << j
        return syn, self.xz[k]

def category(syn, x, z, code):
    c = classify_err(x, z, code)
    if syn == 0: return {"none": "pass_clean", "harmless": "pass_clean", "detected": "pass_damaged", "logical": "silent"}[c]
    return "false_reject" if c in ("none", "harmless") else "caught_damage"

def analyse(R):
    """first-order coefficients (exact), and V0.9's second-order silent coefficient, from single-fault effects"""
    code = R.code; eff = []; consistent = True
    for kind, fl in R.locs:
        row = []
        for f in fl:
            es = [R.effect([f], b) for b in ((0,) if not R.nrand else (0, (1 << R.nrand) - 1, 5 % (1 << R.nrand)))]
            # effects may differ by a stabilizer element between branches: compare classes through the syndrome and the error's class relative to the stabilizers
            consistent &= len({(e[0], classify_err(*e[1], code)) for e in es}) == 1 and all(
                classify_err(es[0][1][0] ^ e[1][0], es[0][1][1] ^ e[1][1], code) in ("none", "harmless") for e in es)
            row.append(es[0])
        eff.append(row)
    c1 = {k: Fr(0) for k in ("pass_clean", "pass_damaged", "silent", "false_reject", "caught_damage")}; nfault = 0; per_loc = []
    for (kind, fl), row in zip(R.locs, eff):
        n = len(row); nfault += n; sig = []
        for syn, (x, z) in row:
            cat = category(syn, x, z, code); c1[cat] += Fr(1, n); sig.append((syn, x, z, cat, 15 // n))        # weights in units of 1/15 (n is 1, 3 or 15)
        per_loc.append(sig)
    tot = {}
    for sig in per_loc:
        for syn, x, z, cat, w in sig:
            if cat != "silent": tot[(syn, x, z)] = tot.get((syn, x, z), 0) + w
    keys = list(tot); S = 0
    for a in keys:
        wa = tot[a]
        for b in keys:
            if category(a[0] ^ b[0], a[1] ^ b[1], a[2] ^ b[2], code) == "silent": S += wa * tot[b]
    SL = 0
    for sig in per_loc:
        ns = [(syn, x, z, w) for syn, x, z, cat, w in sig if cat != "silent"]
        for a in ns:
            for b in ns:
                if category(a[0] ^ b[0], a[1] ^ b[1], a[2] ^ b[2], code) == "silent": SL += a[3] * b[3]
    return dict(nloc=len(R.locs), nfault=nfault, c1=c1, S2=Fr(S - SL, 2 * 225), eff=eff, consistent=consistent, per_loc=per_loc)

def main():
    t00 = time.time()
    log = open(os.path.join(ROOT, "reproduction", "execution-logs", "v0.9.stdout.txt"), encoding="utf-8").read()
    names = ["L conv (baseline)", "J conv", "J flag", "J cat (verified)"]
    # V0.9's printed M3 table is the second occurrence of each row in the log
    ref = {}
    for m in re.finditer(r"^\s+(L conv \(baseline\)|J conv|J flag|J cat \(verified\))\s+(\d+)\s+(\d+) \|\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+) \|.*\| ([\d.]+)\s*$", log, re.M):
        ref.setdefault(m.group(1), []).append((int(m.group(2)), int(m.group(3)), float(m.group(4)), float(m.group(5)), float(m.group(6)), float(m.group(7)), float(m.group(8))))
    ref3 = {k: v[1] for k, v in ref.items()}
    res = {}
    for nm in names:
        t0 = time.time(); R = Rnd(nm); res[nm] = a = analyse(R); r = ref3[nm]; c = a["c1"]
        print("      %-18s locs %3d faults %4d | silent %.3f damaged %.3f false_rej %.3f caught %.3f | second-order silent %.3f   (V0.9 printed: %d %d | %.3f %.3f %.3f %.3f | %.3f)   [%.0f s]" % (
            nm, a["nloc"], a["nfault"], float(c["silent"]), float(c["pass_damaged"]), float(c["false_reject"]), float(c["caught_damage"]), float(a["S2"]), r[0], r[1], r[2], r[3], r[4], r[5], r[6], time.time() - t0), flush=True)
        check("M0 %s: the effects of every single fault are the same on 3 sampled measurement branches (so composition is exact)" % nm, a["consistent"])
        check("M0 %s: %d locations and %d faults equal V0.9's printed M3 counts" % (nm, a["nloc"], a["nfault"]), (a["nloc"], a["nfault"]) == (r[0], r[1]))
        check("M1 %s: the four first-order coefficients equal V0.9's printed M3 values to 3 decimals" % nm,
              all(abs(float(c[k]) - v) < 5.1e-4 for k, v in (("silent", r[2]), ("pass_damaged", r[3]), ("false_reject", r[4]), ("caught_damage", r[5]))))
        check("M2 %s: the second-order silent coefficient %.4f equals V0.9's printed %.3f to 3 decimals" % (nm, float(a["S2"]), r[6]), abs(float(a["S2"]) - r[6]) < 5.1e-4)
    # validation of the composition on sampled pairs against explicit two-fault state-vector runs
    rr = random.Random(33); bad = 0; nb = 0
    for nm in names:
        R = Rnd(nm); a = res[nm]; flat = [(i, j) for i, row in enumerate(a["eff"]) for j in range(len(row)) if a["per_loc"][i][j][3] != "silent"]
        for _ in range(150 if nm != "J cat (verified)" else 60):
            (i1, j1), (i2, j2) = rr.sample(flat, 2)
            if i1 == i2: continue
            f1 = R.locs[i1][1][j1]; f2 = R.locs[i2][1][j2]; sa, (xa, za) = a["eff"][i1][j1]; sb, (xb, zb) = a["eff"][i2][j2]
            pred = category(sa ^ sb, xa ^ xb, za ^ zb, R.code)
            syn, (x, z) = R.effect([f1, f2]); got = category(syn, x, z, R.code); nb += 1; bad += pred != got
    check("M-v the composed category equals the explicit two-fault state-vector category on %d sampled pairs across the four rounds" % nb, bad == 0)
    s2c = float(res["J conv"]["S2"]); s2f = float(res["J flag"]["S2"]); pstar = (4 / 15) / (s2f - s2c)
    print("      analytic crossover estimate p* = (4/15) / (S2_flag - S2_conv) = %.3e   (V0.9's scan: between 5e-4 and 3e-3, \"about 1e-3\")" % pstar)
    check("M3 the crossover estimate %.2e lies between 5e-4 and 3e-3 and rounds to about 1e-3" % pstar, 5e-4 < pstar < 3e-3 and abs(pstar - 1e-3) < 3e-4)
    print("NOTE  Reproduces V0.9's M3 numbers with a different engine (state vectors, XOR composition); the M3 location definition is V0.9's.  Total wall-clock %.0f s" % (time.time() - t00))
    print("ALL PASS" if OK else "FAILED")
    return 0 if OK else 1

if __name__ == "__main__": sys.exit(main())
