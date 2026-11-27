#!/usr/bin/env python3
"""S15: the silent-fault metric of V0.8 to V1.0 applied to the S14 teleportation round (resource faults included).

S14 showed that verifying the [[4,2,2]] block by teleportation (4 data-touching gates, like the local round) wins on the heralded completion metric.  It said in plain words that the
silent-fault metric of V0.9/V1.0 was not computed and that this could overturn the lead.  Here it is computed, with the same fault model (M2), the same four categories and the same
second-order coefficient definition as V0.9 and S05, on the explicit circuit: the offline resource preparation (4 Bell pairs and the checks of the resource) plus the online round
(CNOT data -> A_i, X-measure the data axis, Z-measure A_i, for i = 0..3), with the Pauli-frame correction X^(Z-outcome of A_i) Z^(X-outcome of data_i) applied to the new block.
Detectors are not typed in: they are every parity of the measurement record that is deterministic over all branches of the fault-free circuit (a GF(2) null space).

Circuits compared (all with the same online round)
  ideal   faults only in the online round (the offline resource is assumed perfect)
  T0      the resource of S14 as written: Bell pairs, then the two weight-4 checks (ZZZZ, XXXX) of block A with conventional ancillas
  T1      T0 with flagged checks (V1.0's z_flag/x_flag pattern)
  T2      checks of both blocks A and N, conventional
  T3      checks of both blocks A and N, flagged
  L       the local code <ZZII, IIZZ> with the T0 pattern (control)

Claims
  F0  The fault-free circuits are clean on every branch, the detector sets are found from the circuit, and the runner agrees with S05's on V1.0's rounds.               DERIVED
  F1  Ideal resource, first order: every single online fault is either harmless (4/5 of a fault per round) or detected (56/5); no silent and no pass-damaged fault.    DERIVED
  F2  Ideal resource, second order: the silent coefficient is exactly 492/25 = 19.68 = 12 + 32/25 + 32/5 by simulation and by a separate count over the record-flip
      classes; it is larger than V0.9/V1.0's 2.320 (J flag) and 9.902 (J cat).  The cause is that the 8 Bell-outcome bits carry the data frame, so two flips of the same
      type form a logical error that no parity sees.                                                                                                                   DERIVED
  F3  Resource as in S14 (T0), first order: 4/15 silent, from exactly four hook faults inside the two weight-4 checks; 10.667 pass-damaged (N is never checked).        DERIVED
  F4  Flagging the checks (T1) removes the silent faults; checking both blocks (T2, T3) removes most of the pass-damaged ones; T3 reproduces J flag's printed silent (0) and
      pass-damaged (1.867) coefficients.                                                                                                                              DERIVED
  F5  Second order (with --pairs): the online-online part is 492/25 in every variant; the resource adds more than 23 to it in every variant tried, and flagging helps only a little.  DERIVED
  F6  Per-fault categories are the same on every sampled measurement branch, for single faults and for sampled pairs.                                                 DERIVED
Not claimed: the heralded-completion metric (S14) combined with this one into any score; that a better design cannot exist (only the variants above were tried); anything about
waiting time, idle faults (model M3), or two axes per photon; that the offline resource is cheap (T3 uses 28 ancilla-only gates and 8 resource photons per round, no yield loss
counted); that V0.9's model is physical.  A detected round's follow-up (retry, recovery) is not modelled, as in V0.9.  Author-side; not an independent reproduction.  Requires numpy.
Run with python3 -I; --pairs adds the second-order coefficients of T0..T3 and L (about 15 minutes on two cores).
"""
import concurrent.futures as cf, importlib.util, itertools, os, random, re, sys, time
from fractions import Fraction as Fr
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
def _load(name, rel):
    sp = importlib.util.spec_from_file_location(name, os.path.join(ROOT, *rel)); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
s05 = _load("s05", ["explorations", "s05-statevector-crosscheck", "statevector_crosscheck.py"])
v10 = _load("v10_rounds", ["explorations", "common", "v10_rounds.py"])
s12 = _load("s12", ["explorations", "s12-recovery-charged-completion", "recovery_completion.py"])
Sim, HAD, PAULI = s05.Sim, s05.HAD, s05.PAULI

OK = True
def check(name, ok):
    global OK
    OK = OK and bool(ok); print(("PASS  " if ok else "FAIL  ") + name, flush=True)

DATA = [0, 1, 2, 3]; A = [4, 5, 6, 7]; N = [8, 9, 10, 11]; ANC, FLAG = 12, 13; NQ = 14
GENS = {"J": [("Z", [0, 1, 2, 3]), ("X", [0, 1, 2, 3])], "L": [("Z", [0, 1]), ("Z", [2, 3])]}
PROJ = {"L": ["ZZII", "IIZZ"], "J": ["ZZZZ", "XXXX"]}
CATS = ["pass_clean", "silent", "pass_damaged", "false_reject", "caught_damage"]

def build(code, on="A", flagged=False):
    """operation list (V1.0 op tuples).  Resource: P+ A_i, P0 N_i, CNOT A_i -> N_i; then the checks of block A (and of N when on == 'AN'); ancilla qubits are re-used after
    each measurement (the simulator resets a measured qubit to |0>).  Online round: CNOT data_i -> A_i, MX data_i, MZ A_i."""
    ops = []; rec = [0]
    def add(*t): ops.append(t)
    def bit():
        rec[0] += 1; return rec[0] - 1
    for i in range(4):
        add("P+", A[i]); add("P0", N[i]); add("CNOT", A[i], N[i])
    a, f = ANC, FLAG
    for blk in ([A] + ([N] if on == "AN" else [])):
        for typ, supp in GENS[code]:
            qs = [blk[i] for i in supp]
            if not flagged or len(qs) < 3:
                if typ == "Z":
                    add("P0", a)
                    for q in qs: add("CNOT", q, a)
                    add("MZ", a, bit())
                else:
                    add("P+", a)
                    for q in qs: add("CNOT", a, q)
                    add("MX", a, bit())
            elif typ == "Z":      # V1.0 z_flag pattern
                add("P0", a); add("P+", f); add("CNOT", qs[0], a); add("CNOT", f, a)
                for q in qs[1:-1]: add("CNOT", q, a)
                add("CNOT", f, a); add("CNOT", qs[-1], a); add("MZ", a, bit()); add("MX", f, bit())
            else:                 # V1.0 x_flag pattern
                add("P+", a); add("P0", f); add("CNOT", a, qs[0]); add("CNOT", a, f)
                for q in qs[1:-1]: add("CNOT", a, q)
                add("CNOT", a, f); add("CNOT", a, qs[-1]); add("MX", a, bit()); add("MZ", f, bit())
    prep_end = len(ops); md = []; ma = []
    for i in range(4):
        add("CNOT", DATA[i], A[i]); b1 = bit(); add("MX", DATA[i], b1); b2 = bit(); add("MZ", A[i], b2); md.append(b1); ma.append(b2)
    return ops, dict(prep_end=prep_end, md=md, ma=ma, nrec=rec[0])

def run2(sim, ops, psi, faults=(), choice=0, count=None):
    """as S05's run(), but returns the whole state vector (the output block is not the input block)"""
    v = np.zeros(sim.N, dtype=complex); v[:16] = psi
    rec = 0; ri = 0; after = {}; flips = set()
    for i, kind, pl in faults:
        if kind == "p": after.setdefault(i, []).append(pl)
        else: flips.add(i)
    for i, op in enumerate(ops):
        k = op[0]
        if k == "P0": pass
        elif k in ("P+", "H"): v = sim.one(v, HAD, op[1])
        elif k == "CNOT": v = sim.cnot(v, op[1], op[2])
        elif k == "CZ": v = sim.cz(v, op[1], op[2])
        elif k in ("MZ", "MX"):
            if k == "MX": v = sim.one(v, HAD, op[1])
            v, out, rnd = sim.measure_z(v, op[1], branch=(choice >> ri) & 1)
            if rnd: ri += 1
            if i in flips: out ^= 1
            if out: rec |= 1 << op[2]
        for pl in after.get(i, []): v = sim.pauli(v, pl)
    if count is not None: count.append(ri)
    return v, rec

def par(x): return bin(x).count("1") & 1

def null_space(recs, nrec):
    """a basis (over GF(2)) of all record parities that are 0 on every fault-free record"""
    rows = set(recs); dets = []
    for m in range(1, 1 << nrec):
        if all(par(r & m) == 0 for r in rows): dets.append(m)
    gen = []; span = {0}
    for m in sorted(dets, key=lambda x: (bin(x).count("1"), x)):
        if m not in span: gen.append(m); span |= {s ^ m for s in span}
    return gen

class Round:
    def __init__(self, code, ideal=False, seed=20261128, **kw):
        self.code = code; self.ideal = ideal; self.ops, self.meta = build(code, **kw)
        self.sim = Sim(NQ); self.sim4 = Sim(4); rng = np.random.default_rng(seed)
        psi = self.proj(rng.normal(size=16) + 1j * rng.normal(size=16)); self.psi = psi / np.linalg.norm(psi)
        self.NIDX = np.arange(16) << 8
        cnt = []; run2(self.sim, self.ops, self.psi, count=cnt); self.nrand = cnt[0]
        recs = [run2(self.sim, self.ops, self.psi, choice=b)[1] for b in range(1 << self.nrand)]
        self.nideal = len(set(recs)); self.dets = null_space(recs, self.meta["nrec"])
        locs = s05.enumerate_locations(self.ops)
        self.locs = [l for l in locs if l[0][0] >= self.meta["prep_end"]] if ideal else locs
    def proj(self, v):
        for g in PROJ[self.code]:
            w = v
            for q, c in enumerate(g):
                if c != "I": w = self.sim4.one(w, PAULI[c], q)
            v = (v + w) / 2
        return v
    def state(self, faults, choice=0):
        v, rec = run2(self.sim, self.ops, self.psi, faults, choice)
        n = v[self.NIDX]
        assert abs(1 - np.sum(np.abs(n) ** 2)) < 1e-9, "measured and reset qubits must be back in |0>"
        for i in range(4):
            if rec >> self.meta["ma"][i] & 1: n = self.sim4.one(n, PAULI["X"], i)
            if rec >> self.meta["md"][i] & 1: n = self.sim4.one(n, PAULI["Z"], i)
        return n, rec
    def classify(self, faults, choice=0):
        n, rec = self.state(faults, choice)
        det = any(par(rec & m) for m in self.dets)
        f = abs(np.vdot(self.psi, n)) ** 2; incode = float(np.real(np.vdot(n, self.proj(n))))
        if not det:
            if f > 1 - 1e-9: return "pass_clean"
            return "silent" if incode > 1 - 1e-9 else "pass_damaged"
        return "false_reject" if f > 1 - 1e-9 else "caught_damage"

def first_order(R, branch=0):
    """per-category sums with weight 1/n per fault at a location of n faults (exact fractions), the per-location classification, and the group split (resource / online)"""
    tot = {c: Fr(0) for c in CATS}; grp = {"res": {c: Fr(0) for c in CATS}, "on": {c: Fr(0) for c in CATS}}; cls = []
    for loc in R.locs:
        g = "res" if loc[0][0] < R.meta["prep_end"] else "on"; row = []
        for fl in loc:
            c = R.classify([fl], branch); tot[c] += Fr(1, len(loc)); grp[g][c] += Fr(1, len(loc)); row.append((c, fl))
        cls.append(row)
    return tot, grp, cls

_W = {}
def _init(code, kw, cls):
    _W["R"] = Round(code, **kw); _W["cls"] = cls
def _work(pairs):
    R = _W["R"]; cls = _W["cls"]; out = []
    for a, b in pairs:
        cnt = 0
        for ca, fa in cls[a]:
            if ca == "silent": continue
            for cb, fb in cls[b]:
                if cb == "silent": continue
                if R.classify([fa, fb]) == "silent": cnt += 1
        out.append((a, b, cnt))
    return out

def second_order(R, code, kw, cls):
    """V0.9's definition: unordered pairs of distinct locations, neither single fault silent, weight 1/(n_a n_b); returns the exact total and its split by group"""
    L = len(R.locs); pairs = [(a, b) for a in range(L) for b in range(a + 1, L)]
    chunks = [pairs[i::64] for i in range(64)]; tot = Fr(0); split = {}
    grp = lambda i: "res" if R.locs[i][0][0] < R.meta["prep_end"] else "on"
    kind = lambda i: "m" if R.ops[R.locs[i][0][0]][0] in ("MZ", "MX") else "g"      # m = readout flip, g = fault after a preparation or gate
    with cf.ProcessPoolExecutor(max_workers=os.cpu_count() or 1, initializer=_init, initargs=(code, kw, cls)) as ex:
        for res in ex.map(_work, chunks):
            for a, b, cnt in res:
                w = Fr(cnt, len(R.locs[a]) * len(R.locs[b])); tot += w
                key = grp(a) + "-" + grp(b); split[key] = split.get(key, Fr(0)) + w
                kk = "".join(sorted(kind(a) + kind(b))); split[kk] = split.get(kk, Fr(0)) + w
    return tot, split

def main():
    do_pairs = "--pairs" in sys.argv; t00 = time.time()
    # ---- reference values printed by V0.9 (first order from the M2 table, second order from its summary line), as S05 reads them
    log = open(os.path.join(ROOT, "reproduction", "execution-logs", "v0.9.stdout.txt"), encoding="utf-8").read(); ref = {}
    for m in re.finditer(r"^\s+(L conv \(baseline\)|J conv|J flag|J cat \(verified\))\s+(\d+)\s+(\d+) \|\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+) \|", log, re.M):
        if m.group(1) in ref: continue
        ref[m.group(1)] = (int(m.group(2)), int(m.group(3)), float(m.group(4)), float(m.group(5)), float(m.group(6)), float(m.group(7)))
    m2 = re.search(r"second-order silent coefficient from fault PAIRS \(M2\) is ([\d.]+) local, ([\d.]+) joint conventional, ([\d.]+) flagged, ([\d.]+) verified cat", log)
    ref2 = dict(zip(["L conv (baseline)", "J conv", "J flag", "J cat (verified)"], [float(x) for x in m2.groups()]))
    variants = [("ideal", "J", dict(ideal=True)), ("T0", "J", dict(on="A")), ("T1", "J", dict(on="A", flagged=True)), ("T2", "J", dict(on="AN")), ("T3", "J", dict(on="AN", flagged=True)), ("L", "L", dict(on="A"))]
    # ---- F0
    rounds = v10.load(); rr = random.Random(11); same = True; nt = 0
    for nm in ("L conv (baseline)", "J conv"):
        Rd = rounds[nm]; sim = Sim(Rd["nq"]); psi = np.random.default_rng(3).normal(size=16) + 1j * np.random.default_rng(4).normal(size=16); psi /= np.linalg.norm(psi)
        locs = s05.enumerate_locations(Rd["ops"]); flat = [fl for l in locs for fl in l]
        for fl in rr.sample(flat, 40):
            v1, r1 = s05.run(sim, Rd["ops"], psi, [fl]); v2, r2 = run2(sim, Rd["ops"], psi, [fl])
            same &= (r1 == r2 and np.allclose(v1, v2[:16])); nt += 1
    check("F0a the full-state runner used here returns the same data state and record as S05's runner on V1.0's L conv and J conv rounds (%d single faults)" % nt, same)
    R = {}
    for nm, code, kw in variants:
        t0 = time.time(); R[nm] = Round(code, **kw); r = R[nm]
        clean = all(r.classify([], b) == "pass_clean" for b in range(1 << r.nrand))
        print("      %-5s qubits %d, %d random outcomes in the fault-free run, %d distinct fault-free records, %d detectors, offline ancilla-only CNOTs %d, online data-touching CNOTs 4  [%.1f s]"
              % (nm, NQ, r.nrand, r.nideal, len(r.dets), sum(1 for o in r.ops[:r.meta["prep_end"]] if o[0] == "CNOT"), time.time() - t0))
        check("F0b %s: the fault-free circuit returns the input state with no detection on all %d branches, and %d records + %d detectors account for all %d record bits"
              % (nm, 1 << r.nrand, r.nideal, len(r.dets), r.meta["nrec"]), clean and r.nideal * (1 << len(r.dets)) == 1 << r.meta["nrec"])
    # ---- first order, all variants
    FO = {}
    print("== first order (V0.9 model M2, weight 1/n per fault of a location): fault weights per round ==")
    print("      %-18s %5s %6s | %-8s %-12s %-11s %-13s | %s" % ("round", "locs", "faults", "silent", "pass_damaged", "false_rej", "caught_dmg", "(pass_clean)"))
    for nm, code, kw in variants:
        tot, grp, cls = first_order(R[nm]); FO[nm] = (tot, grp, cls); nf = sum(len(l) for l in R[nm].locs)
        print("      %-18s %5d %6d | %-8.3f %-12.3f %-11.3f %-13.3f | %.3f" % ("teleport " + nm, len(R[nm].locs), nf, float(tot["silent"]), float(tot["pass_damaged"]), float(tot["false_reject"]), float(tot["caught_damage"]), float(tot["pass_clean"])))
    for k in ("L conv (baseline)", "J conv", "J flag", "J cat (verified)"):
        rl, rf, a, b, c, d = ref[k]; print("      %-18s %5d %6d | %-8.3f %-12.3f %-11.3f %-13.3f |   (V0.9 printed, M2)" % (k, rl, rf, a, b, c, d))
    # ---- F1
    tI = FO["ideal"][0]
    check("F1  ideal resource: %d locations, no silent and no pass-damaged single fault; harmless weight %s = 4 x 3/15, detected weight %s (all %s of it in caught_damage: the record also steers the correction)"
          % (len(R["ideal"].locs), tI["pass_clean"], tI["false_reject"] + tI["caught_damage"], tI["caught_damage"]),
          tI["silent"] == 0 and tI["pass_damaged"] == 0 and tI["pass_clean"] == Fr(4, 5) and tI["false_reject"] + tI["caught_damage"] == Fr(56, 5) and tI["false_reject"] == 0)
    # ---- F3
    t0_, g0, c0 = FO["T0"]
    sil = [(R["T0"].ops[l[0][0]], l[0][0], fl) for l, row in zip(R["T0"].locs, c0) for c, fl in row if c == "silent"]
    inchk = all(R["T0"].meta["prep_end"] > i >= 12 and o[0] == "CNOT" for o, i, fl in sil)
    for o, i, fl in sil: print("      silent fault: after op %d %s : %s" % (i, o[:3], fl[2]))
    check("F3  T0 (S14's resource): silent weight %s = 4/15, from exactly %d faults, all after CNOTs inside the two weight-4 checks (hooks); pass_damaged %.3f of which %.3f from the resource, none from the online round"
          % (t0_["silent"], len(sil), float(t0_["pass_damaged"]), float(g0["res"]["pass_damaged"])),
          t0_["silent"] == Fr(4, 15) and len(sil) == 4 and inchk and g0["on"]["pass_damaged"] == 0 and g0["on"]["silent"] == 0)
    # ---- F4
    t1, t2, t3 = FO["T1"][0], FO["T2"][0], FO["T3"][0]
    check("F4a T1 (flagged checks of A): silent weight 0; pass-damaged %.3f is almost unchanged from T0's %.3f because N is not checked" % (float(t1["pass_damaged"]), float(t0_["pass_damaged"])), t1["silent"] == 0 and abs(float(t1["pass_damaged"]) - float(t0_["pass_damaged"])) < 0.5)
    check("F4b T2 (conventional checks of A and N): pass-damaged falls to %.3f but the hooks return (silent %.3f)" % (float(t2["pass_damaged"]), float(t2["silent"])), t2["silent"] > 0 and t2["pass_damaged"] < t0_["pass_damaged"] / 4)
    rj = ref["J flag"]
    check("F4c T3 (flagged checks of A and N): silent %.3f and pass-damaged %.3f equal V0.9's printed J flag values (%.3f, %.3f); its false-reject and caught-damage weights are larger (more locations)"
          % (float(t3["silent"]), float(t3["pass_damaged"]), rj[2], rj[3]), abs(float(t3["silent"]) - rj[2]) < 5.1e-4 and abs(float(t3["pass_damaged"]) - rj[3]) < 5.1e-4)
    tl = FO["L"][0]
    check("F4d local-code control (T0 pattern, Z-blind code): silent weight %.3f against V0.9's local round %.3f: with the resource included the local code's Z exposure grows by an order of magnitude"
          % (float(tl["silent"]), ref["L conv (baseline)"][2]), float(tl["silent"]) > 10 * ref["L conv (baseline)"][2])
    # ---- F6 branch independence
    bad = 0; nb = 0; rr = random.Random(5); branches = [0, (1 << 8) - 1] + [rr.randrange(1 << 8) for _ in range(2)]
    for nm, code, kw in variants:
        for loc, row in zip(R[nm].locs, FO[nm][2]):
            for c0_, fl in row:
                for b in branches[1:]:
                    nb += 1; bad += R[nm].classify([fl], b) != c0_
    check("F6a single-fault categories are identical on %d sampled branch choices (branch 0, all ones, two random ones; all variants; %d extra fault-branch runs)" % (len(branches), nb), bad == 0)
    bad = 0; nb = 0
    for nm in ("T0", "T3"):
        r = R[nm]; flat = [fl for row in FO[nm][2] for c, fl in row if c != "silent"]
        for _ in range(120):
            fa, fb = rr.sample(flat, 2)
            if fa[0] == fb[0]: continue
            c0_ = r.classify([fa, fb], 0)
            for b in branches[1:]: nb += 1; bad += r.classify([fa, fb], b) != c0_
    check("F6b sampled fault pairs (T0 and T3, %d pair-branch runs): the pair category is the same on every sampled branch, so branch 0 is used for all pairs" % nb, bad == 0)
    # ---- F2 second order, ideal resource: simulation and an independent count over record-flip classes
    t0 = time.time(); S2, sp = second_order(R["ideal"], "J", dict(ideal=True), FO["ideal"][2]); S = {"ideal": (S2, sp)}
    # separate count by Pauli-frame algebra on the single-fault effects: every single online fault is reduced to (its syndrome over the detectors, its Pauli error on the output
    # block modulo the stabilizers), taken from one state-vector run; effects of two faults compose by XOR (on three branches the effect is checked to be the same), so a pair is
    # silent iff its syndrome is 0 and its composite error commutes with ZZZZ and XXXX without being a stabilizer
    r = R["ideal"]; paulis = list(itertools.product("IXYZ", repeat=4)); PS = np.zeros((256, 16), dtype=complex)
    for k, pa in enumerate(paulis):
        w = r.psi
        for q, c in enumerate(pa):
            if c != "I": w = r.sim4.one(w, PAULI[c], q)
        PS[k] = w
    stab = [(0, 0), (15, 0), (0, 15), (15, 15)]
    def canon(x, z): return min((x ^ sx, z ^ sz) for sx, sz in stab)
    def effect(fl, b):
        n, rec = r.state([fl], b); ov = np.abs(PS.conj() @ n); k = int(np.argmax(ov)); assert ov[k] > 1 - 1e-9, "the output must be a Pauli-error state"
        x = z = 0
        for q, c in enumerate(paulis[k]):
            if c in "XY": x |= 1 << q
            if c in "ZY": z |= 1 << q
        return tuple(par(rec & m) for m in r.dets), canon(x, z)
    def acat(syn, xz):
        if any(syn): return "det"
        x, z = xz
        if par(x) or par(z): return "pass_damaged"
        return "pass_clean" if xz in [canon(*sg) for sg in stab] else "silent"
    eff = []; consistent = True; agree = True
    for loc, row in zip(r.locs, FO["ideal"][2]):
        er = []
        for (c, fl) in row:
            es = [effect(fl, b) for b in (0, 5, 77)]; consistent &= len(set(es)) == 1; e = es[0]; er.append(e)
            agree &= acat(*e) == ("det" if c in ("false_reject", "caught_damage") else c)
        eff.append(er)
    alg = Fr(0)
    for a_ in range(len(r.locs)):
        for b_ in range(a_ + 1, len(r.locs)):
            cnt = 0
            for (sa, xa) in eff[a_]:
                for (sb, xb) in eff[b_]:
                    syn = tuple(u ^ v for u, v in zip(sa, sb)); xz = canon(xa[0] ^ xb[0], xa[1] ^ xb[1])
                    if acat(syn, xz) == "silent": cnt += 1
            alg += Fr(cnt, len(r.locs[a_]) * len(r.locs[b_]))
    closed = 12 + 6 * 3 * Fr(4, 15) ** 2 + 24 * Fr(4, 15)
    print("      ideal-resource second order: simulation %s = %.4f, Pauli-frame count %s, closed form 12 + 6*3*(4/15)^2 + 24*(4/15) = %s   [%.0f s]" % (S2, float(S2), alg, closed, time.time() - t0))
    check("F2  ideal resource: second-order silent coefficient = 492/25 = 19.68 by state-vector simulation of all %d location pairs, by a Pauli-frame count over the single-fault effects (consistent on 3 branches: %s; reproduces all %d single-fault categories: %s) and by the closed form (12 readout-flip pairs of the same type + 18 gate-gate class pairs of weight (4/15)^2 + 24 readout-gate pairs of weight 4/15)"
          % (len(r.locs) * (len(r.locs) - 1) // 2, consistent, sum(len(l) for l in r.locs), agree),
          S2 == alg == closed == Fr(492, 25) and consistent and agree)
    sk = sp
    check("F2c ideal resource, split by location kind: readout-readout %s, readout-gate %s, gate-gate %s (gg = both faults after preparations or gates, gm = one readout flip, mm = two readout flips), so c2 = 12 r^2 + 32/5 r p + 32/25 p^2 if readouts flip with probability r and gates fault with probability p"
          % (sk["mm"], sk["gm"], sk["gg"]), (sk["mm"], sk["gm"], sk["gg"]) == (Fr(12), Fr(32, 5), Fr(32, 25)))
    check("F2b 19.68 exceeds V0.9/V1.0's second-order coefficients for J flag (%.3f), J conv (%.3f), J cat (%.3f) and the local round (%.3f): by 8.5, 8.1, 2.0 and 15.8 times" % (ref2["J flag"], ref2["J conv"], ref2["J cat (verified)"], ref2["L conv (baseline)"]),
          float(S2) > max(ref2.values()))
    # ---- F5
    if do_pairs:
        for nm, code, kw in variants[1:]:
            t0 = time.time(); S[nm] = second_order(R[nm], code, kw, FO[nm][2])
            print("      %-5s second-order silent %.3f   (resource-resource %.3f, resource-online %.3f, online-online %.3f; by kind: gg %.3f, gm %.3f, mm %.3f)   [%.0f s]" % (nm, float(S[nm][0]), float(S[nm][1].get("res-res", 0)), float(S[nm][1].get("res-on", 0)), float(S[nm][1].get("on-on", 0)),
                  float(S[nm][1].get("gg", 0)), float(S[nm][1].get("gm", 0)), float(S[nm][1].get("mm", 0)), time.time() - t0), flush=True)
        check("F5a in every variant the online-online part of the second-order coefficient is 492/25 (the resource does not change it)", all(S[nm][1].get("on-on", 0) == Fr(492, 25) for nm in ("T0", "T1", "T2", "T3")))
        tt = {nm: S[nm][0] for nm in ("T0", "T1", "T2", "T3")}
        check("F5b the resource adds at least 23 to the second-order coefficient in every variant, and the order is T1 < T0 < T3 < T2 (%s): flagging the checks lowers it a little, checking block N as well raises it"
              % ", ".join("%s %.2f" % (k, float(v)) for k, v in sorted(tt.items(), key=lambda kv: kv[1])), all(v - Fr(492, 25) > 23 for v in tt.values()) and tt["T1"] < tt["T0"] < tt["T3"] < tt["T2"])
    print("== second-order silent coefficient (pairs of faults at distinct locations, neither silent alone) ==")
    for k in ("L conv (baseline)", "J conv", "J flag", "J cat (verified)"): print("      %-24s %8.3f   (V0.9 printed)" % (k, ref2[k]))
    for nm in ("ideal", "T0", "T1", "T2", "T3", "L"):
        if nm in S: print("      %-24s %8.3f" % ("teleport " + nm, float(S[nm][0])))
    print("== two axes, side by side, NOT combined (V0.9 model; p = per-location fault probability) ==")
    s_ = Fr(9, 10); Pl = s_ ** 4; Pc = s12.chain(tuple([1] * 8), s_, s_ ** 3); Pk = s_ ** 4 / (1 - 4 * (1 - s_) * s_ ** 6)
    print("      silent logical per round ~ c1 p + c2 p^2 (c1, c2 above).  Heralded completion at s = 0.9 (S12/S14, recovery charged): local %.4f, cat joint (m = 3) %.4f, teleportation joint %.4f." % (float(Pl), float(Pc), float(Pk)))
    print("      The ideal-resource teleportation round has c1 = 0 and c2 = 19.68; J flag has c1 = 0 and c2 = 2.32; J cat has c1 = 0 and c2 = 9.90.")
    print("NOTE  This evaluates the S14 design only on the V0.9 silent-fault metric and does not combine it with S14's heralded metric.  The two metrics disagree for this round: heralded completion")
    print("      favours it (S14), the second-order silent coefficient does not (19.68 at best against 2.32 and 9.90), and S14's own resource, as written, also adds first-order silent faults.")
    print("      Every variant here is a distance-2 resource built from many fault locations; repairing the first order (T1, T3) does not repair the second.  The model gives every location the same p,")
    print("      so a readout much better than a gate would shrink the readout terms of the online floor (12 r^2 + 6.4 r p + 1.28 p^2 for readout error r); that is not computed for the other rounds.")
    print("      Total wall-clock %.0f s" % (time.time() - t00))
    print("ALL PASS" if OK else "FAILED")
    return 0 if OK else 1

if __name__ == "__main__": sys.exit(main())
