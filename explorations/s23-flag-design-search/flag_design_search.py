#!/usr/bin/env python3
"""S23: a search over a family of flagged joint-extraction rounds for the [[4,2,2]] (J) code, and a sensitivity of V0.9's idle-fault negative result to how idle time is counted.

V1.0 places each check's flag so that it brackets the two middle data couplings (windows (1,3)).  That is one point of a larger family: each of the two checks may carry no flag or one
flag whose two couplings sit at any two of the five slots 0..4 (before data coupling 0, ..., after data coupling 3), the second check may use any order of the four data qubits, and
either check may come first: 2 x 11 x 11 x 24 = 5,808 rounds, V1.0's J conv and J flag among them.  Every round is evaluated exactly (rational arithmetic) under V0.9's model M2 and model M3
by Pauli-frame propagation, which is first validated against explicit state-vector runs.  V0.9's coefficients (first-order silent, rejected, damaged; second-order silent) are reproduced
for the four rounds, then used to find which family members have no first-order silent error, how low their second-order coefficient can go, and which are Pareto-optimal in
(second-order silent coefficient, rejection coefficient).

M3 counts one idle location per live qubit after EVERY OPERATION, as if all operations were executed one after another.  A second, PROPOSED convention is also evaluated: the same operation list
scheduled as soon as possible on parallel layers (preparations as late as possible), one idle location per live untouched qubit per LAYER; optionally a layer that holds a measurement lasts m gate
times.  This is a sensitivity analysis of V0.9's conclusion, not a replacement for V0.9's definition and not a hardware timing model.

Claims
  A0  The builder reproduces V1.0's J conv and J flag operation lists and detector masks exactly (windows None and (1,3), Z check first, identity data order).                          DERIVED
  A1  The Pauli-frame engine equals explicit state-vector runs: every single-fault effect (M3 locations) of J conv, J flag, the two optimum rounds and sampled faults of 14 random family
      members, J cat and L conv has the same syndrome and the same V0.9 class; the layered operation lists give the same agreement.                                                   DERIVED
  A2  For the four rounds the engine's M2 and M3 first-order coefficients and second-order silent coefficients equal V0.9's printed values to 3 decimals.                          DERIVED
  A3  Within the 5,808 rounds exactly 768 have a zero first-order silent coefficient, all with a flag on both checks; with one flag the smallest first-order silent value is 2/15, with none 4/15.   DERIVED
  A4  Model M2: among those 768 the smallest second-order coefficient is 352/225 (windows (0,4) and (0,4)), 33 % below V1.0's 58/25; V1.0's round is Pareto-dominated.                  DERIVED
  A5  Model M3: the smallest second-order coefficient is lower by under 5 % than V1.0's; V1.0's round is again Pareto-dominated; the best design changes by the model.                  DERIVED
  A6  Exact probabilities at p = 1e-3, and the exact flagged / conventional crossing in model M3, for V1.0's flagged round and for the two optimum rounds.                            DERIVED
  A7  In M3 the pairs of two idle faults carry 67 % (J conv) and 81 % (J flag) of the second-order coefficient; the gate-only part equals the M2 coefficient.                       DERIVED
  B1  Idle counted per layer on the same operation lists: exact second-order coefficients and probabilities for the four rounds; the flagged / conventional crossing disappears below p = 0.1.   DERIVED on PROPOSED
  B2  If a layer with a measurement lasts m gate times, the crossing returns; V0.9's 1.05e-3 corresponds to m of about 6.                                                          DERIVED on ASSUMED
  B3  In the layered view V1.0's flag windows are Pareto-optimal in the family; the choice of flag windows moves the second-order coefficient by far less than the idle convention.       DERIVED
Not claimed: any hardware timing, any measured rate, any independence from V0.9's fault definition (re-implemented here from V0.9's text), or that the layered convention is the right one.
Author-side; not an independent reproduction.  Requires numpy.  Run with python3 -I.
"""
import importlib.util, itertools, math, os, random, re, sys, time
from collections import Counter, defaultdict
from fractions import Fraction as Fr
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
def _load(name, rel):
    sp = importlib.util.spec_from_file_location(name, os.path.join(ROOT, *rel)); m = importlib.util.module_from_spec(sp)
    sys.modules[name] = m; sp.loader.exec_module(m); return m
s18 = _load("s18", ["explorations", "s18-m3-reproduction", "m3_reproduction.py"])
s05 = s18.s05; v10 = s18.v10; classify_err = s18.classify_err; PAULI = s05.PAULI; Sim = s05.Sim

OK = True
def check(name, ok):
    global OK
    OK = OK and bool(ok); print(("PASS  " if ok else "FAIL  ") + name, flush=True)

# ---------------------------------------------------------------- Pauli-frame engine
CATS = {}
def cat(syn, x, z, code="J"):
    """V0.9's category of (syndrome, data X mask, data Z mask), memoised"""
    k = (syn, x, z, code)
    if k not in CATS:
        c = classify_err(x, z, code)
        CATS[k] = ({"none": "pass_clean", "harmless": "pass_clean", "detected": "pass_damaged", "logical": "silent"}[c] if syn == 0 else ("false_reject" if c in ("none", "harmless") else "caught_damage"))
    return CATS[k]

def qs(op): return [op[1], op[2]] if op[0] in ("CNOT", "CZ") else [op[1]]

def propagate(ops, start, x, z, rec):
    """push a Pauli frame (x, z bit masks over all qubits) and a record-flip mask through ops[start:]"""
    for op in ops[start:]:
        k = op[0]
        if k in ("P0", "P+"): m = ~(1 << op[1]); x &= m; z &= m
        elif k == "CNOT":
            c, t = op[1], op[2]
            if (x >> c) & 1: x ^= 1 << t
            if (z >> t) & 1: z ^= 1 << c
        elif k == "CZ":
            a, b = op[1], op[2]
            if (x >> a) & 1: z ^= 1 << b
            if (x >> b) & 1: z ^= 1 << a
        elif k == "H":
            q = op[1]
            if ((x >> q) & 1) != ((z >> q) & 1): x ^= 1 << q; z ^= 1 << q
        elif k == "MZ":
            if (x >> op[1]) & 1: rec ^= 1 << op[2]
            m = ~(1 << op[1]); x &= m; z &= m
        elif k == "MX":
            if (z >> op[1]) & 1: rec ^= 1 << op[2]
            m = ~(1 << op[1]); x &= m; z &= m
        else: raise ValueError(k)
    return x, z, rec

def effect(ops, dets, f):
    """(syndrome, data X mask, data Z mask) of one fault f = (index, 'p' or 'm', Pauli dict); index -1 is an incoming fault"""
    i, kind, pd = f
    if kind == "m": x = z = 0; rec = 1 << ops[i][2]
    else:
        x = z = 0
        for q, c in pd.items():
            if c in "XY": x |= 1 << q
            if c in "ZY": z |= 1 << q
        x, z, rec = propagate(ops, i + 1, x, z, 0)
    return sum((bin(rec & m).count("1") & 1) << j for j, m in enumerate(dets)), x & 15, z & 15

def gate_locations(ops, i, op):
    t = qs(op)
    if op[0] in ("MZ", "MX"): return ("m", [(i, "m", None)])
    if len(t) == 2:
        a, b = t; fl = []
        for u in "IXYZ":
            for v in "IXYZ":
                if u != "I" or v != "I": fl.append((i, "p", {q: c for q, c in ((a, u), (b, v)) if c != "I"}))
        return ("g", fl)
    return ("g", [(i, "p", {t[0]: c}) for c in "XYZ"])

def serial_locations(ops, model):
    """V0.9's locations.  M2: every gate, preparation, one-qubit operation (non-identity Paulis) and measurement (record flip).  M3 adds an idle location (3 Paulis) for every live qubit not touched by an operation,
    after every operation, and one incoming location (3 Paulis) on each of the four data axes.  Each location is (type, options, rate multiplier)"""
    locs = []
    if model == "M3":
        for q in range(4): locs.append(("in", [(-1, "p", {q: c}) for c in "XYZ"], 1))
    alive = set(range(4))
    for i, op in enumerate(ops):
        t = qs(op)
        if op[0] in ("MZ", "MX"): alive.discard(op[1])
        elif op[0] in ("P0", "P+"): alive.add(op[1])
        ty, fl = gate_locations(ops, i, op); locs.append((ty, fl, 1))
        if model == "M3":
            for q in sorted(alive):
                if q not in t: locs.append(("idle", [(i, "p", {q: c}) for c in "XYZ"], 1))
    return locs, ops

def schedule(ops):
    """as-soon-as-possible layers (a qubit does one operation per layer; each qubit's own operation order is kept); preparations moved to the layer just before their first use"""
    last = {}; lay = []
    for op in ops:
        l = 1 + max([last.get(q, -1) for q in qs(op)] + [-1]); lay.append(l)
        for q in qs(op): last[q] = l
    for i, op in enumerate(ops):
        if op[0] in ("P0", "P+"): lay[i] = min(lay[j] for j in range(i + 1, len(ops)) if op[1] in qs(ops[j])) - 1
    return lay

def layered_locations(ops, m=1):
    """the same operation list in layer order (operations of one layer touch disjoint qubits, so the circuit is unchanged); gate locations as in M3; one idle location per live untouched qubit per
    layer, whose rate multiplier is m if the layer holds a measurement and 1 otherwise.  Returns (locations, reordered operations, number of layers)"""
    lay = schedule(ops); order = sorted(range(len(ops)), key=lambda i: (lay[i], i)); nops = [ops[i] for i in order]; nl = [lay[i] for i in order]
    for q in range(max(max(qs(o)) for o in ops) + 1):
        assert [o for o in ops if q in qs(o)] == [o for o in nops if q in qs(o)], "per-qubit order must be unchanged"
    locs = [("in", [(-1, "p", {q: c}) for c in "XYZ"], 1) for q in range(4)]
    for i, op in enumerate(nops):
        ty, fl = gate_locations(nops, i, op); locs.append((ty, fl, 1))
    first = {}; lastl = {}
    for i, op in enumerate(nops):
        for q in qs(op): first.setdefault(q, nl[i]); lastl[q] = nl[i]
    nq = max(max(qs(o)) for o in nops) + 1
    for k in range(max(nl) + 1):
        idx = [i for i in range(len(nops)) if nl[i] == k]
        if not idx: continue
        touched = {q for i in idx for q in qs(nops[i])}; mult = m if any(nops[i][0] in ("MZ", "MX") for i in idx) else 1
        for q in range(nq):
            if q in touched: continue
            if q < 4 or (q in first and first[q] < k < lastl[q]): locs.append(("idle", [(idx[-1], "p", {q: c}) for c in "XYZ"], mult))
    return locs, nops, max(nl) + 1

class Coef:
    """exact first-order coefficients (sum over locations of the fraction of its options in each category) and V0.9's second-order silent coefficient (pairs of distinct locations,
    neither fault silent alone, signatures aggregated; weights 15 // n so that all arithmetic is integer), plus the split of the second-order coefficient by location-type pair"""
    def __init__(self, locs, ops, dets, code="J", eff=None):
        self.c1 = {k: Fr(0) for k in ("pass_clean", "pass_damaged", "silent", "false_reject", "caught_damage")}; self.per = []; eff = eff or effect
        for typ, fl, _ in locs:
            n = len(fl); row = []
            for f in fl:
                syn, x, z = eff(ops, dets, f); c = cat(syn, x, z, code); self.c1[c] += Fr(1, n); row.append((syn, x, z, c, 15 // n))
            self.per.append((typ, row))
        tot = defaultdict(int)
        for _, row in self.per:
            for syn, x, z, c, w in row:
                if c != "silent": tot[(syn, x, z)] += w
        S = 0; keys = list(tot)
        for a in keys:
            for b in keys:
                if cat(a[0] ^ b[0], a[1] ^ b[1], a[2] ^ b[2], code) == "silent": S += tot[a] * tot[b]
        SL = 0
        for _, row in self.per:
            ns = [r for r in row if r[3] != "silent"]
            for a in ns:
                for b in ns:
                    if cat(a[0] ^ b[0], a[1] ^ b[1], a[2] ^ b[2], code) == "silent": SL += a[4] * b[4]
        self.c2 = Fr(S - SL, 2 * 225); self.code = code; self.nloc = len(locs); self.nfault = sum(len(r) for _, r in self.per)
    @property
    def rej(self): return self.c1["false_reject"] + self.c1["caught_damage"]
    def split(self):
        out = defaultdict(int); P = self.per
        for i in range(len(P)):
            for j in range(i + 1, len(P)):
                for a in P[i][1]:
                    if a[3] == "silent": continue
                    for b in P[j][1]:
                        if b[3] != "silent" and cat(a[0] ^ b[0], a[1] ^ b[1], a[2] ^ b[2], self.code) == "silent": out[tuple(sorted((P[i][0], P[j][0])))] += 2 * a[4] * b[4]
        return {k: Fr(v, 2 * 225) for k, v in out.items()}

def bias_w(pd, bias):
    if bias is None or pd is None: return 1.0
    w = 1.0
    for q, c in pd.items():
        kind, b = bias["data" if q < 4 else "anc"]
        if c == kind: w *= b
    return w

class Prob:
    """exact distribution of the XOR of independent location faults (floating-point convolution on 2^(d+8) states: syndrome, data X mask, data Z mask); a location faults with probability min(1, p * multiplier)"""
    def __init__(self, locs, ops, dets, code="J", eff=None):
        self.d = d = len(dets); self.N = N = 1 << (d + 8); self.locs = []; eff = eff or effect
        for typ, fl, mu in locs:
            row = []
            for f in fl:
                syn, x, z = eff(ops, dets, f); row.append(syn | (x << d) | (z << (d + 4)))
            self.locs.append((typ, row, mu))
        idx = np.arange(N); self.idx = idx; syn = idx & ((1 << d) - 1); x = (idx >> d) & 15; z = (idx >> (d + 4)) & 15
        cl = np.array([{"none": 0, "harmless": 0, "detected": 1, "logical": 2}[classify_err(int(a), int(b), code)] for a, b in zip(x, z)])
        self.sil = (syn == 0) & (cl == 2); self.rj = syn != 0
    def at(self, p):
        P = np.zeros(self.N); P[0] = 1.0
        for typ, row, mu in self.locs:
            r = min(1.0, p * mu); acc = np.zeros(self.N)
            for e in row: acc += P[self.idx ^ e]
            P = (1 - r) * P + r * acc / len(row)
        return dict(silent=P[self.sil].sum(), reject=P[self.rj].sum(), total=P.sum())

def first_crossing(A, B, lo=1e-5, hi=1e-1, n=80):
    """smallest p on a log grid (and then by bisection) at which the silent probabilities of A and B swap order; None if they never swap on the grid"""
    prev = None
    for k in range(n + 1):
        p = lo * (hi / lo) ** (k / n); g = A.at(p)["silent"] - B.at(p)["silent"]
        if prev is not None and prev[1] * g < 0:
            a, b, ga = math.log(prev[0]), math.log(p), prev[1]
            for _ in range(45):
                mm = (a + b) / 2; gm = A.at(math.exp(mm))["silent"] - B.at(math.exp(mm))["silent"]
                if ga * gm <= 0: b = mm
                else: a, ga = mm, gm
            return math.exp((a + b) / 2)
        prev = (p, g)
    return None

# ---------------------------------------------------------------- the design family
def check_ops(kind, perm, win, anc, flg, rec):
    """one check.  Z check: ancilla |0> is the target of CNOT(data, ancilla), flag |+> is the control of CNOT(flag, ancilla) and is measured in X.  X check: ancilla |+> controls CNOT(ancilla, data), flag |0> is the target and
    is measured in Z.  win = (a, b): the flag couples to the ancilla before data coupling a and before data coupling b (slot 4 is after the last); None: no flag"""
    Zk = kind == "Z"; ops = [("P0", anc) if Zk else ("P+", anc)]
    if win: ops.append(("P+", flg) if Zk else ("P0", flg))
    fc = ("CNOT", flg, anc) if Zk else ("CNOT", anc, flg)
    for j, q in enumerate(perm):
        if win and j in win: ops.append(fc)
        ops.append(("CNOT", q, anc) if Zk else ("CNOT", anc, q))
    if win and 4 in win: ops.append(fc)
    ops.append(("MZ", anc, rec) if Zk else ("MX", anc, rec))
    if win: ops.append(("MX", flg, rec + 1) if Zk else ("MZ", flg, rec + 1))
    return ops

def build(first, perm2, w1, w2):
    """first check of kind `first` with data order 0123 and window w1; second check of the other kind with data order perm2 and window w2; qubits and records numbered in order of use"""
    second = "X" if first == "Z" else "Z"; q = 4; r = 0
    a1 = q; q += 1; f1 = None
    if w1: f1 = q; q += 1
    ops = check_ops(first, (0, 1, 2, 3), w1, a1, f1, r); r += 2 if w1 else 1
    a2 = q; q += 1; f2 = None
    if w2: f2 = q; q += 1
    ops += check_ops(second, perm2, w2, a2, f2, r); r += 2 if w2 else 1
    return ops, [1 << i for i in range(r)], q

WINS = [None] + [(a, b) for a in range(5) for b in range(a + 1, 5)]
ID = (0, 1, 2, 3)

# ---------------------------------------------------------------- state-vector validation
class RndOps(s18.Rnd):
    """S18's state-vector engine on an arbitrary operation list (J code state)"""
    def __init__(self, ops, dets, nq, seed=20261127):
        self.name = "custom"; self.ops = ops; self.dets = dets; self.code = "J"; self.sim = Sim(nq); self.sim4 = Sim(4)
        rng = np.random.default_rng(seed); psi = rng.normal(size=16) + 1j * rng.normal(size=16)
        for g in ("ZZZZ", "XXXX"):
            w = psi
            for q, c in enumerate(g): w = self.sim4.one(w, PAULI[c], q)
            psi = (psi + w) / 2
        self.psi = psi / np.linalg.norm(psi); cnt = []; s05.run(self.sim, self.ops, self.psi, count=cnt); self.nrand = cnt[0]
        paulis = list(itertools.product("IXYZ", repeat=4)); self.PS = np.zeros((256, 16), dtype=complex); self.xz = []
        for k, pa in enumerate(paulis):
            w = self.psi; x = z = 0
            for q, c in enumerate(pa):
                if c != "I": w = self.sim4.one(w, PAULI[c], q)
                if c in "XY": x |= 1 << q
                if c in "ZY": z |= 1 << q
            self.PS[k] = w; self.xz.append((x, z))

def compare_with_statevector(R, ops, dets, code, locs, sample=None, rr=None):
    """number of single faults compared and number whose (syndrome, category) differ between the frame engine and the state-vector run"""
    fl = [f for _, o, _ in locs for f in o]
    if sample: fl = rr.sample(fl, min(sample, len(fl)))
    bad = 0
    for f in fl:
        syn, x, z = effect(ops, dets, f); syn2, (x2, z2) = R.effect([f], 0)
        bad += syn != syn2 or cat(syn, x, z, code) != cat(syn2, x2, z2, code)
    return len(fl), bad

def main():
    t00 = time.time(); R10 = v10.load()
    # ---- A0
    o, d, n = build("Z", ID, None, None); a0a = o == R10["J conv"]["ops"] and d == R10["J conv"]["dets"]
    o, d, n = build("Z", ID, (1, 3), (1, 3)); a0b = o == R10["J flag"]["ops"] and d == R10["J flag"]["dets"]
    check("A0 the builder reproduces V1.0's J conv operation list and detector masks (no flags) exactly", a0a)
    check("A0 the builder reproduces V1.0's J flag operation list and detector masks (windows (1,3) and (1,3), Z check first, identity order) exactly", a0b)

    # ---- A2 first (coefficients of the four rounds), then A1
    log = open(os.path.join(ROOT, "reproduction", "execution-logs", "v0.9.stdout.txt"), encoding="utf-8").read(); ref = {}
    for m in re.finditer(r"^\s+(L conv \(baseline\)|J conv|J flag|J cat \(verified\))\s+(\d+)\s+(\d+) \|\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+) \|.*\| ([\d.]+)\s*$", log, re.M):
        ref.setdefault(m.group(1), []).append((int(m.group(2)), int(m.group(3)), float(m.group(4)), float(m.group(5)), float(m.group(6)), float(m.group(7)), float(m.group(8))))
    NAMES = ["L conv (baseline)", "J conv", "J flag", "J cat (verified)"]; C = {}; okc = {"M2": True, "M3": True}
    for model, k in (("M2", 0), ("M3", 1)):
        for nm in NAMES:
            r = R10[nm]; locs, ops = serial_locations(r["ops"], model); c = C[(model, nm)] = Coef(locs, ops, r["dets"], r["code"]); p = ref[nm][k]
            ok = (c.nloc, c.nfault) == (p[0], p[1]) and all(abs(float(c.c1[kk]) - v) < 5.1e-4 for kk, v in (("silent", p[2]), ("pass_damaged", p[3]), ("false_reject", p[4]), ("caught_damage", p[5]))) and abs(float(c.c2) - p[6]) < 5.1e-4
            okc[model] &= ok
            print("      %s %-18s locs %3d faults %4d | silent %.3f damaged %.3f false_rej %.3f caught %.3f | second-order %.3f   (V0.9: %d %d | %.3f %.3f %.3f %.3f | %.3f)" % (
                model, nm, c.nloc, c.nfault, float(c.c1["silent"]), float(c.c1["pass_damaged"]), float(c.c1["false_reject"]), float(c.c1["caught_damage"]), float(c.c2), *p), flush=True)
    check("A2 model M2: location and fault counts, the four first-order coefficients and the second-order silent coefficient of the four rounds equal V0.9's printed values to 3 decimals", okc["M2"])
    check("A2 model M3: the same for model M3 (second-order 60.000, 158.249, 426.942, 2314.169)", okc["M3"])

    # ---- the whole family
    t0 = time.time(); FAM = []
    for first in "ZX":
        for w1 in WINS:
            for w2 in WINS:
                for perm in itertools.permutations(range(4)):
                    ops, dets, nq = build(first, perm, w1, w2); row = dict(first=first, w1=w1, w2=w2, perm=perm, ops=ops, dets=dets, nq=nq)
                    for key, loc in (("m2", serial_locations(ops, "M2")[0]), ("m3", serial_locations(ops, "M3")[0])):
                        c = Coef(loc, ops, dets); row[key] = (c.c1["silent"], c.c2, c.rej, c.c1["pass_damaged"])
                    ll, nops, depth = layered_locations(ops); c = Coef(ll, nops, dets); row["ly"] = (c.c1["silent"], c.c2, c.rej, c.c1["pass_damaged"]); row["depth"] = depth
                    FAM.append(row)
        print("      family: check order %s done, %d rounds so far [%.0f s]" % (first, len(FAM), time.time() - t0), flush=True)
    def find(first, perm, w1, w2): return next(r for r in FAM if (r["first"], r["perm"], r["w1"], r["w2"]) == (first, perm, w1, w2))
    VC = find("Z", ID, None, None); VF = find("Z", ID, (1, 3), (1, 3))
    check("A2 (family) the family members J conv and J flag give the same M2, M3 coefficients as the V0.9-checked rounds above (second-order %.3f / %.3f in M2, %.3f / %.3f in M3)" % (float(VC["m2"][1]), float(VF["m2"][1]), float(VC["m3"][1]), float(VF["m3"][1])),
          VC["m2"][1] == C[("M2", "J conv")].c2 and VF["m2"][1] == C[("M2", "J flag")].c2 and VC["m3"][1] == C[("M3", "J conv")].c2 and VF["m3"][1] == C[("M3", "J flag")].c2)

    # ---- A1 state-vector validation
    rr = random.Random(20261127); tot = bad = 0
    best2 = min((r for r in FAM if r["m2"][0] == 0), key=lambda r: (r["m2"][1], r["m2"][2])); best3 = min((r for r in FAM if r["m3"][0] == 0), key=lambda r: (r["m3"][1], r["m3"][2]))
    for r in (VC, VF, best2, best3):
        RS = RndOps(r["ops"], r["dets"], r["nq"]); locs = serial_locations(r["ops"], "M3")[0]; n_, b_ = compare_with_statevector(RS, r["ops"], r["dets"], "J", locs); tot += n_; bad += b_
        ll, nops, _ = layered_locations(r["ops"]); RS = RndOps(nops, r["dets"], r["nq"]); n_, b_ = compare_with_statevector(RS, nops, r["dets"], "J", ll); tot += n_; bad += b_
    check("A1 frame engine = state vector on every single fault (M3 locations and layered locations) of J conv, J flag and the two optimum rounds: %d faults, %d differ" % (tot, bad), bad == 0)
    tot2 = bad2 = 0
    for _ in range(14):
        r = rr.choice(FAM); RS = RndOps(r["ops"], r["dets"], r["nq"]); locs = serial_locations(r["ops"], "M3")[0]; n_, b_ = compare_with_statevector(RS, r["ops"], r["dets"], "J", locs, 250, rr); tot2 += n_; bad2 += b_
    check("A1 frame engine = state vector on %d sampled faults of 14 random family members: %d differ" % (tot2, bad2), bad2 == 0)
    tot3 = bad3 = 0
    for nm, ns in (("J cat (verified)", 250), ("L conv (baseline)", 250)):
        r = R10[nm]; RS = s18.Rnd(nm); locs = serial_locations(r["ops"], "M3")[0]; n_, b_ = compare_with_statevector(RS, r["ops"], r["dets"], r["code"], locs, ns, rr); tot3 += n_; bad3 += b_
    check("A1 frame engine = state vector on %d sampled faults of V1.0's J cat (H, CZ operations) and L conv: %d differ" % (tot3, bad3), bad3 == 0)

    # ---- A3
    z = [r for r in FAM if r["m2"][0] == 0]; z3 = [r for r in FAM if r["m3"][0] == 0]
    def kind(r): return (r["w1"] is not None) + (r["w2"] is not None)
    one = [r for r in FAM if kind(r) == 1]; none = [r for r in FAM if kind(r) == 0]
    print("      family %d rounds; zero first-order silent: %d (M2), %d (M3); by number of flags: %s" % (len(FAM), len(z), len(z3), dict(Counter(kind(r) for r in z))))
    check("A3 %d rounds in all (2 x 11 x 11 x 24); %d have zero first-order silent in M2 and the same %d in M3, every one with a flag on both checks; smallest first-order silent with one flag %s, with none %s" % (
        len(FAM), len(z), len(z3), min(r["m2"][0] for r in one), min(r["m2"][0] for r in none)),
        len(FAM) == 5808 and len(z) == 768 and {id(r) for r in z} == {id(r) for r in z3} and all(kind(r) == 2 for r in z) and min(r["m2"][0] for r in one) == Fr(2, 15) and min(r["m2"][0] for r in none) == Fr(4, 15) and min(r["m3"][0] for r in one) == Fr(2, 15))

    # ---- A4 / A5
    def front(rs, key):
        pts = sorted(set((r[key][1], r[key][2]) for r in rs)); out = []; best = None
        for c2, rj in pts:
            if best is None or rj < best: out.append((c2, rj)); best = rj
        return out
    def dominated(r, rs, key): return any(s[key][1] <= r[key][1] and s[key][2] <= r[key][2] and (s[key][1], s[key][2]) != (r[key][1], r[key][2]) for s in rs)
    f2 = front(z, "m2"); f3 = front(z3, "m3")
    w2 = sorted({(r["w1"], r["w2"]) for r in z if r["m2"][1] == best2["m2"][1]}); perms2 = {r["perm"] for r in z if r["w1"] == (0, 4) and r["w2"] == (0, 4) and r["first"] == "Z"}
    print("      M2: smallest second-order %s = %.4f at windows %s (rejection %.4f); V1.0's J flag %s = %.4f (rejection %.4f); Pareto front %s" % (best2["m2"][1], float(best2["m2"][1]), w2, float(best2["m2"][2]), VF["m2"][1], float(VF["m2"][1]), float(VF["m2"][2]), [(str(c), float(rj)) for c, rj in f2]))
    check("A4 model M2: the smallest second-order silent coefficient among the 768 is 352/225 = %.4f at windows (0,4),(0,4) only; V1.0's is 58/25 = %.4f, so %.1f %% higher; the best round rejects %.3f against %.3f" % (
        float(best2["m2"][1]), float(VF["m2"][1]), 100 * float(VF["m2"][1] / best2["m2"][1] - 1), float(best2["m2"][2]), float(VF["m2"][2])),
        best2["m2"][1] == Fr(352, 225) and VF["m2"][1] == Fr(58, 25) and w2 == [((0, 4), (0, 4))] and len(perms2) == 24 and len({r["m2"][1] for r in z if r["w1"] == (0, 4) and r["w2"] == (0, 4)}) == 1)
    check("A4 model M2: V1.0's J flag is Pareto-dominated in (second-order, rejection): the round with the same rejection %s has second-order %.3f against V1.0's %.3f; the front has %d points" % (
        VF["m2"][2], float(min(r["m2"][1] for r in z if r["m2"][2] == VF["m2"][2])), float(VF["m2"][1]), len(f2)), dominated(VF, z, "m2") and (VF["m2"][1], VF["m2"][2]) not in f2)
    print("      M3: smallest second-order %s = %.4f at %s %s %s %s (rejection %.4f); V1.0 %.4f (rejection %.4f); Pareto front %s" % (best3["m3"][1], float(best3["m3"][1]), best3["first"], best3["w1"], best3["w2"], best3["perm"], float(best3["m3"][2]), float(VF["m3"][1]), float(VF["m3"][2]), [(float(c), float(rj)) for c, rj in f3]))
    gain3 = 1 - best3["m3"][1] / VF["m3"][1]
    check("A5 model M3: the smallest second-order coefficient among the 768 is %.3f (%s, %s, order %s), %.1f %% below V1.0's %.3f (under 5 %%); V1.0's round is Pareto-dominated; the M2-optimal round has %.3f" % (
        float(best3["m3"][1]), best3["w1"], best3["w2"], best3["perm"], 100 * float(gain3), float(VF["m3"][1]), float(best2["m3"][1])),
        0 < gain3 < Fr(5, 100) and dominated(VF, z3, "m3") and best3["w1"] != best3["w2"] and best2["m3"][1] > best3["m3"][1])

    # ---- A6 exact probabilities and crossings
    PRC = Prob(*(lambda r: (serial_locations(r["ops"], "M3")[0], r["ops"], r["dets"]))(VC)); PRF = Prob(*(lambda r: (serial_locations(r["ops"], "M3")[0], r["ops"], r["dets"]))(VF))
    P2 = Prob(*(lambda r: (serial_locations(r["ops"], "M3")[0], r["ops"], r["dets"]))(best2)); P3 = Prob(*(lambda r: (serial_locations(r["ops"], "M3")[0], r["ops"], r["dets"]))(best3))
    M2P = {nm: Prob(*(lambda r: (serial_locations(r["ops"], "M2")[0], r["ops"], r["dets"]))(r)) for nm, r in (("conv", VC), ("flag", VF), ("best2", best2))}
    rows = []
    for nm, E in (("J conv", PRC), ("J flag (V1.0)", PRF), ("M2-optimal (0,4),(0,4)", P2), ("M3-optimal", P3)):
        a = E.at(1e-3); rows.append((nm, a["silent"], a["reject"])); print("      M3 p=1e-3 %-26s silent %.4e  reject %.4e" % (nm, a["silent"], a["reject"]))
    m2a = {nm: E.at(1e-3) for nm, E in M2P.items()}
    for nm in M2P: print("      M2 p=1e-3 %-26s silent %.4e  reject %.4e" % (nm, m2a[nm]["silent"], m2a[nm]["reject"]))
    pstar = {nm: first_crossing(E, PRC, 1e-4, 1e-2, 40) for nm, E in (("J flag (V1.0)", PRF), ("M2-optimal", P2), ("M3-optimal", P3))}
    print("      M3 exact flagged-versus-conventional crossing: " + ", ".join("%s %.4e" % (k, v) for k, v in pstar.items()))
    check("A6 at p = 1e-3 in model M2 the M2-optimal round's silent probability is %.3e against V1.0's %.3e (%.1f %% lower) at a rejection %.3e against %.3e" % (m2a["best2"]["silent"], m2a["flag"]["silent"], 100 * (1 - m2a["best2"]["silent"] / m2a["flag"]["silent"]), m2a["best2"]["reject"], m2a["flag"]["reject"]),
          m2a["best2"]["silent"] < m2a["flag"]["silent"] and abs(m2a["flag"]["silent"] - 2.29e-6) < 0.005e-6 and abs(m2a["conv"]["silent"] - 2.66e-4) < 0.005e-4)
    check("A6 in model M3 V1.0's crossing with J conv is %.4e (S19: 1.0496e-3); the M2-optimal round's is %.3e and the M3-optimal round's %.3e: the crossing moves by less than 15 %%, so V0.9's negative result stands in the family" % (pstar["J flag (V1.0)"], pstar["M2-optimal"], pstar["M3-optimal"]),
          abs(pstar["J flag (V1.0)"] - 1.0496e-3) < 5e-8 and all(abs(v / pstar["J flag (V1.0)"] - 1) < 0.15 for v in pstar.values()))

    # ---- A7 decomposition
    dc = {nm: C[("M3", nm)].split() for nm in ("J conv", "J flag")}; shares = {}
    for nm in dc:
        tot_ = sum(dc[nm].values()); shares[nm] = dc[nm].get(("idle", "idle"), 0) / tot_
        print("      M3 second-order split, %-7s total %.3f: " % (nm, float(tot_)) + ", ".join("%s %.1f %%" % ("-".join(k), 100 * float(v / tot_)) for k, v in sorted(dc[nm].items(), key=lambda kv: -kv[1])))
    gates_only = {nm: dc[nm].get(("g", "g"), 0) + dc[nm].get(("g", "m"), 0) + dc[nm].get(("m", "m"), 0) for nm in dc}
    check("A7 the split sums to the second-order coefficient; its gate-and-measurement part equals the M2 coefficient (%.3f, %.3f); idle-idle pairs carry %.1f %% (J conv) and %.1f %% (J flag)" % (float(gates_only["J conv"]), float(gates_only["J flag"]), 100 * float(shares["J conv"]), 100 * float(shares["J flag"])),
          all(sum(dc[nm].values()) == C[("M3", nm)].c2 for nm in dc) and all(gates_only[nm] == C[("M2", nm)].c2 for nm in dc) and 0.66 < shares["J conv"] < 0.69 and 0.80 < shares["J flag"] < 0.83)

    # ---- B1 layered idle model
    L = {}; E_s = {}; E_l = {}
    for nm in NAMES:
        r = R10[nm]; ll, nops, depth = layered_locations(r["ops"]); c = Coef(ll, nops, r["dets"], r["code"]); L[nm] = (c, depth, len(ll))
        E_s[nm] = Prob(serial_locations(r["ops"], "M3")[0], r["ops"], r["dets"], r["code"]); E_l[nm] = Prob(ll, nops, r["dets"], r["code"])
        cs = C[("M3", nm)]; a = E_s[nm].at(1e-3); b = E_l[nm].at(1e-3)
        print("      %-18s serial: %3d locations, second-order %8.3f, silent(1e-3) %.3e reject %.3e | layered: %2d layers, %3d locations, second-order %8.3f, silent(1e-3) %.3e reject %.3e" % (nm, cs.nloc, float(cs.c2), a["silent"], a["reject"], depth, len(ll), float(c.c2), b["silent"], b["reject"]))
    rank_s = sorted(NAMES, key=lambda n: E_s[n].at(1e-3)["silent"]); rank_l = sorted(NAMES, key=lambda n: E_l[n].at(1e-3)["silent"])
    print("      order of silent probability at p = 1e-3: serial %s ; layered %s" % (rank_s, rank_l))
    cr_s = first_crossing(E_s["J flag"], E_s["J conv"], 1e-5, 1e-1, 80); cr_l = first_crossing(E_l["J flag"], E_l["J conv"], 1e-5, 1e-1, 80)
    grid = [1e-5 * (1e4) ** (k / 160) for k in range(161)]; below = all(E_l["J flag"].at(p)["silent"] < E_l["J conv"].at(p)["silent"] for p in grid)
    idle_s = {nm: sum(1 for t, _, _ in serial_locations(R10[nm]["ops"], "M3")[0] if t == "idle") for nm in NAMES}
    idle_l = {nm: sum(1 for t, _, _ in layered_locations(R10[nm]["ops"])[0] if t == "idle") for nm in NAMES}
    print("      idle locations serial / layered: " + ", ".join("%s %d / %d" % (nm, idle_s[nm], idle_l[nm]) for nm in NAMES))
    check("B1 layered: depth 7 (J conv) and 9 (J flag); idle locations %d and %d against %d and %d serial (J cat %d against %d)" % (idle_l["J conv"], idle_l["J flag"], idle_s["J conv"], idle_s["J flag"], idle_l["J cat (verified)"], idle_s["J cat (verified)"]),
          (L["J conv"][1], L["J flag"][1]) == (7, 9) and (idle_l["J conv"], idle_l["J flag"], idle_s["J conv"], idle_s["J flag"]) == (20, 32, 40, 84) and all(idle_l[n] < idle_s[n] for n in NAMES))
    check("B1 layered: first-order silent coefficients are unchanged (0.267 and 0); second-order are 51.360 and 78.276 (serial 158.249 and 426.942)", L["J conv"][0].c1["silent"] == C[("M3", "J conv")].c1["silent"] and L["J flag"][0].c1["silent"] == 0
          and abs(float(L["J conv"][0].c2) - 51.360) < 5.1e-4 and abs(float(L["J flag"][0].c2) - 78.276) < 5.1e-4)
    check("B1 serial: the flagged and conventional silent probabilities cross at %.4e (S19: 1.0496e-3) and again higher up; layered: no crossing on a 161-point log grid from 1e-5 to 1e-1, J flag lower throughout (%s); crossing found: %s" % (cr_s, below, cr_l),
          abs(cr_s - 1.0496e-3) < 5e-8 and below and cr_l is None)
    check("B1 the order at p = 1e-3 is %s serial and %s layered (J cat overtakes J conv under the layered count)" % (rank_s, rank_l), rank_s == ["J flag", "J conv", "J cat (verified)", "L conv (baseline)"] and rank_l == ["J flag", "J cat (verified)", "J conv", "L conv (baseline)"])

    # ---- B2 measurement-layer duration
    cross = {}
    for m in (1, 2, 3, 4, 5, 6, 8, 10, 20):
        pr = {nm: (lambda r: (lambda ll, nops, dep: Prob(ll, nops, r["dets"], "J"))(*layered_locations(r["ops"], m)))(R10[nm]) for nm in ("J conv", "J flag")}
        cross[m] = first_crossing(pr["J flag"], pr["J conv"], 1e-5, 1e-1, 80); print("      measurement layer = %2d gate times: crossing %s" % (m, "%.4e" % cross[m] if cross[m] else "none up to 0.1"), flush=True)
    mono = all(cross[a] > cross[b] for a, b in ((2, 3), (3, 4), (4, 5), (5, 6), (6, 8), (8, 10), (10, 20))) and cross[1] is None
    lo, hi = 5.0, 8.0
    def pc(m):
        pr = {nm: (lambda r: (lambda ll, nops, dep: Prob(ll, nops, r["dets"], "J"))(*layered_locations(r["ops"], m)))(R10[nm]) for nm in ("J conv", "J flag")}
        return first_crossing(pr["J flag"], pr["J conv"], 1e-4, 1e-1, 60)
    for _ in range(14):
        mid = (lo + hi) / 2
        if pc(mid) > 1.0496e-3: lo = mid
        else: hi = mid
    mstar = (lo + hi) / 2; print("      m* with crossing 1.0496e-3: %.3f gate times" % mstar)
    check("B2 the crossing decreases strictly as m grows (none at m = 1; %.2e at m = 2, %.2e at 6, %.2e at 20); the m that reproduces V0.9's 1.0496e-3 is %.2f gate times" % (cross[2], cross[6], cross[20], mstar), mono and 6.0 < mstar < 6.1)

    # ---- B3 family under the layered count
    zl = [r for r in FAM if r["ly"][0] == 0]; fl_ = front(zl, "ly"); bestl = min(zl, key=lambda r: (r["ly"][1], r["ly"][2]))
    print("      layered: %d rounds with zero first-order silent; smallest second-order %.3f at %s %s %s %s (depth %d, rejection %.3f); V1.0 %.3f (rejection %.3f); Pareto front %s" % (
        len(zl), float(bestl["ly"][1]), bestl["first"], bestl["w1"], bestl["w2"], bestl["perm"], bestl["depth"], float(bestl["ly"][2]), float(VF["ly"][1]), float(VF["ly"][2]), [(round(float(c), 3), round(float(rj), 3)) for c, rj in fl_]))
    lever_design_m3 = float(VF["m3"][1] / best3["m3"][1]); lever_conv = float(VF["m3"][1] / VF["ly"][1]); lever_design_ly = float(VF["ly"][1] / bestl["ly"][1])
    check("B3 layered: %d rounds have zero first-order silent; V1.0's J flag has the smallest rejection among them (%.3f) and is on the Pareto front; the smallest second-order is %.3f (%.1f %% below V1.0's %.3f); minimum depth in the family is %d, V1.0's is %d" % (
        len(zl), float(VF["ly"][2]), float(bestl["ly"][1]), 100 * (1 - float(bestl["ly"][1] / VF["ly"][1])), float(VF["ly"][1]), min(r["depth"] for r in zl), VF["depth"]),
        len(zl) == 768 and VF["ly"][2] == min(r["ly"][2] for r in zl) and (VF["ly"][1], VF["ly"][2]) in fl_ and VF["depth"] == min(r["depth"] for r in zl))
    check("B3 for the flagged round, changing the flag windows moves the M3 second-order coefficient by a factor %.2f (serial) and %.2f (layered) at most; changing from serial to layered idle counting moves it by %.2f" % (lever_design_m3, lever_design_ly, lever_conv),
          lever_design_m3 < 1.06 and lever_design_ly < 1.07 and lever_conv > 5)
    print("NOTE  total wall-clock %.0f s" % (time.time() - t00))
    print("ALL PASS" if OK else "FAILED")
    return 0 if OK else 1

if __name__ == "__main__": sys.exit(main())
