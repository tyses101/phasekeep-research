#!/usr/bin/env python3
"""S16: how much does the second-order silent comparison depend on giving readout flips the same fault probability as gates?

V0.8 to V1.0 (model M2) give every location the same probability p: each preparation or gate gets one of its non-identity Paulis, each measurement gets a record flip.  A photonic
platform need not have equal readout and gate error.  Here the second-order silent coefficient of each round is split by the KIND of the two locations in a pair (g = fault after a
preparation or gate, m = readout flip), so that with readout probability r p and gate probability p

      c2(r) = gg + gm r + mm r^2          (silent logical probability per round = c1 p + c2(r) p^2)

with gg, gm, mm exact fractions from the same state-vector pair enumeration as S05 and S15.  The first-order coefficient has no readout part (checked), so it does not depend on r.

Claims
  R0  gg + gm + mm reproduces V0.9's printed second-order silent coefficient for the local, joint conventional and joint flagged rounds (and the verified cat with --full),
      and the split of the ideal-resource teleportation round is 12 r^2 + 32/5 r + 32/25.                                                                      DERIVED
  R1  A single readout flip is never silent in any of these rounds (so c1 does not depend on r).                                                               DERIVED
  R2  Crossover ratios r* where the ideal-resource teleportation round's c2 equals each other round's: exact roots of a quadratic, with exact sign checks either side.  They show
      how much better readout must be than gates before the teleportation floor drops below the other rounds'; they say nothing about whether any real platform is there.   DERIVED
Not claimed: that readouts are or are not better than gates in any platform; the same r for every measurement kind (a measurement of a flag, of an ancilla, of a data axis); anything
about the heralded metric; or a combined score.  Author-side; not an independent reproduction.  Requires numpy.  Run with python3 -I.  --full adds the verified cat (about 5 minutes)
and the T3 teleportation resource of S15 (about 10 minutes).
"""
import concurrent.futures as cf, importlib.util, math, os, random, re, sys, time
from fractions import Fraction as Fr
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
def _load(name, rel):
    sp = importlib.util.spec_from_file_location(name, os.path.join(ROOT, *rel)); m = importlib.util.module_from_spec(sp)
    sys.modules[name] = m; sp.loader.exec_module(m); return m          # registered so that the worker processes of S15's pair enumeration can unpickle its functions
s05 = _load("s05", ["explorations", "s05-statevector-crosscheck", "statevector_crosscheck.py"])
v10 = _load("v10_rounds", ["explorations", "common", "v10_rounds.py"])
s15 = _load("s15", ["explorations", "s15-teleportation-silent-faults", "teleport_silent.py"])
Sim, PAULI = s05.Sim, s05.PAULI

OK = True
def check(name, ok):
    global OK
    OK = OK and bool(ok); print(("PASS  " if ok else "FAIL  ") + name, flush=True)

def par(x): return bin(x).count("1") & 1

class RoundV:
    """one of V1.0's rounds, classified exactly as S05 does (random code-space input, full state vector, detectors from V1.0)"""
    def __init__(self, name, seed=20261127):
        R = v10.load()[name]; self.name = name; self.ops = R["ops"]; self.dets = R["dets"]; self.code = R["code"]
        self.sim = Sim(R["nq"]); self.sim4 = Sim(4); rng = np.random.default_rng(seed)
        psi = self.proj(rng.normal(size=16) + 1j * rng.normal(size=16)); self.psi = psi / np.linalg.norm(psi)
        cnt = []; s05.run(self.sim, self.ops, self.psi, count=cnt); self.nrand = cnt[0]
        self.locs = s05.enumerate_locations(self.ops)
    def proj(self, v):
        for (g,) in s05.CODES[self.code]: v = (v + s05.data_pauli_apply(self.sim4, v, g)) / 2
        return v
    def classify(self, faults, choice=0):
        v, rec = s05.run(self.sim, self.ops, self.psi, faults, choice)
        det = any(par(rec & m) for m in self.dets); f = abs(np.vdot(self.psi, v)) ** 2; incode = float(np.real(np.vdot(v, self.proj(v))))
        if not det:
            if f > 1 - 1e-9: return "pass_clean"
            return "silent" if incode > 1 - 1e-9 else "pass_damaged"
        return "false_reject" if f > 1 - 1e-9 else "caught_damage"
    def kind(self, i): return "m" if self.ops[self.locs[i][0][0]][0] in ("MZ", "MX") else "g"

_W = {}
def _init(name, cls): _W["R"] = RoundV(name); _W["cls"] = cls
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

def kinds_v(name):
    R0 = RoundV(name); cls = [[(R0.classify([fl]), fl) for fl in loc] for loc in R0.locs]
    L = len(R0.locs); pairs = [(a, b) for a in range(L) for b in range(a + 1, L)]; chunks = [pairs[i::32] for i in range(32)]; split = {"gg": Fr(0), "gm": Fr(0), "mm": Fr(0)}
    with cf.ProcessPoolExecutor(max_workers=os.cpu_count() or 1, initializer=_init, initargs=(name, cls)) as ex:
        for res in ex.map(_work, chunks):
            for a, b, cnt in res: split["".join(sorted(R0.kind(a) + R0.kind(b)))] += Fr(cnt, len(R0.locs[a]) * len(R0.locs[b]))
    return R0, cls, split

def c2(split, r): return split["gg"] + split["gm"] * r + split["mm"] * r * r

def crossing(t, o):
    """smallest r > 0 at which c2_t(r) = c2_o(r): roots of a quadratic; returns (r*, True if the exact difference changes sign across a 1e-6 bracket) or (None, True)"""
    A = t["mm"] - o["mm"]; B = t["gm"] - o["gm"]; C = t["gg"] - o["gg"]
    roots = []
    if A == 0:
        if B != 0: roots = [-float(C) / float(B)]
    else:
        D = float(B) ** 2 - 4 * float(A) * float(C)
        if D >= 0: roots = [(-float(B) + sg * math.sqrt(D)) / (2 * float(A)) for sg in (1, -1)]
    roots = sorted(x for x in roots if x > 0)
    if not roots: return None, True
    x = roots[0]; lo = Fr(int(x * 10 ** 6) - 1, 10 ** 6); hi = Fr(int(x * 10 ** 6) + 2, 10 ** 6)
    f = lambda r: (A * r * r + B * r + C)
    return x, f(lo) * f(hi) < 0

def main():
    full = "--full" in sys.argv; t00 = time.time()
    log = open(os.path.join(ROOT, "reproduction", "execution-logs", "v0.9.stdout.txt"), encoding="utf-8").read()
    m2 = re.search(r"second-order silent coefficient from fault PAIRS \(M2\) is ([\d.]+) local, ([\d.]+) joint conventional, ([\d.]+) flagged, ([\d.]+) verified cat", log)
    names = ["L conv (baseline)", "J conv", "J flag", "J cat (verified)"]; ref2 = dict(zip(names, [float(x) for x in m2.groups()]))
    use = names if full else names[:3]; K = {}; first_m = {}
    for nm in use:
        t0 = time.time(); R0, cls, K[nm] = kinds_v(nm)
        tot = sum(K[nm].values()); first_m[nm] = [c for i, row in enumerate(cls) if R0.kind(i) == "m" for c, fl in row]
        if R0.nrand:
            rr = random.Random(9); flat = [(i, fl) for i, row in enumerate(cls) for c, fl in row if c != "silent"]; bad = 0; nb = 0
            for _ in range(100):
                (ia, fa), (ib, fb) = rr.sample(flat, 2)
                if ia == ib: continue
                c0 = R0.classify([fa, fb], 0)
                for b in (1, (1 << R0.nrand) - 1, rr.randrange(1 << R0.nrand)): nb += 1; bad += R0.classify([fa, fb], b) != c0
            check("R3 %s: %d sampled fault pairs on 3 further measurement branches give the same category (branch 0 is used for all pairs)" % (nm, nb), bad == 0)
        print("      %-18s gg %-14s gm %-14s mm %-10s  total %.3f  (V0.9 printed %.3f)   [%.0f s]" % (nm, K[nm]["gg"], K[nm]["gm"], K[nm]["mm"], float(tot), ref2[nm], time.time() - t0), flush=True)
        check("R0 %s: gg + gm + mm = %.4f reproduces V0.9's printed second-order silent coefficient %.3f to its printed decimals" % (nm, float(tot), ref2[nm]), abs(float(tot) - ref2[nm]) < 5.1e-4)
    check("R1  no single readout flip is silent in any of the rounds (%d readout faults checked), so the first-order silent coefficient does not depend on r" % sum(len(v) for v in first_m.values()), all(c != "silent" for v in first_m.values() for c in v))
    # teleportation, ideal resource (and T3 with --full), via S15's own machinery
    t0 = time.time(); Ri = s15.Round("J", ideal=True); tot, grp, cls = s15.first_order(Ri); S2, sp = s15.second_order(Ri, "J", dict(ideal=True), cls)
    K["teleport ideal"] = {k: sp[k] for k in ("gg", "gm", "mm")}
    check("R0b ideal-resource teleportation round: gg = 32/25, gm = 32/5, mm = 12 (total 492/25), so c2(r) = 32/25 + 32/5 r + 12 r^2   [%.0f s]" % (time.time() - t0), (K["teleport ideal"]["gg"], K["teleport ideal"]["gm"], K["teleport ideal"]["mm"]) == (Fr(32, 25), Fr(32, 5), Fr(12)))
    if full:
        t0 = time.time(); R3 = s15.Round("J", on="AN", flagged=True); tot, grp, cls = s15.first_order(R3); S3, sp3 = s15.second_order(R3, "J", dict(on="AN", flagged=True), cls)
        K["teleport T3"] = {k: sp3[k] for k in ("gg", "gm", "mm")}
        print("      teleport T3        gg %-14s gm %-14s mm %-10s  total %.3f   [%.0f s]" % (K["teleport T3"]["gg"], K["teleport T3"]["gm"], K["teleport T3"]["mm"], float(S3), time.time() - t0), flush=True)
    rs = [Fr(0), Fr(1, 20), Fr(1, 10), Fr(1, 4), Fr(1, 2), Fr(1)]
    print("== c2(r), r = readout flip probability / gate fault probability (V0.9's model is r = 1) ==")
    print("      %-18s " % "round" + "  ".join("r=%-6s" % (str(float(r))) for r in rs))
    for nm in list(K):
        print("      %-18s " % nm + "  ".join("%-8.3f" % float(c2(K[nm], r)) for r in rs))
    print("== crossover r* (teleportation, ideal resource, is BELOW the other round for r < r*; c1 = 0 for teleportation, 0.267 / 0 / 0 / 0.533 for J conv / J flag / J cat / local) ==")
    cross = {}
    for nm in K:
        if nm.startswith("teleport"): continue
        x, cert = crossing(K["teleport ideal"], K[nm]); cross[nm] = (x, cert)
        print("      vs %-18s r* = %s" % (nm, "none (the difference keeps one sign for r > 0)" if x is None else "%.4f" % x))
    check("R2a every crossover found is an exact sign change of the difference of the two quadratics (rational points 1e-6 either side)", all(cert for x, cert in cross.values()))
    check("R2b at r = 1 (V0.9's model) the ideal-resource teleportation round has the highest c2 of all rounds listed", all(c2(K["teleport ideal"], Fr(1)) > c2(K[nm], Fr(1)) for nm in K if nm != "teleport ideal" and not nm.startswith("teleport T")))
    print("      at r = 0 (perfect readout): ideal-resource teleportation c2 = %.3f; " % float(K["teleport ideal"]["gg"]) + ", ".join("%s %.3f" % (nm, float(K[nm]["gg"])) for nm in K if not nm.startswith("teleport")))
    print("NOTE  This is a sensitivity of the second axis only.  The ideal-resource row ignores the resource's own faults; T3 (with --full) includes them and keeps its pair terms from the many offline gates.")
    print("      The first-order coefficients c1 and the heralded metric are untouched by r.  Nothing here combines the axes.  Total wall-clock %.0f s" % (time.time() - t00))
    print("ALL PASS" if OK else "FAILED")
    return 0 if OK else 1

if __name__ == "__main__": sys.exit(main())
