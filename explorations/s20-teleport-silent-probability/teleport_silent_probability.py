#!/usr/bin/env python3
"""S20: exact silent-logical PROBABILITIES of the teleportation rounds against the V1.0 rounds, as a function of p and of the readout ratio r (a correction to how S15 and S16 were read).

S15 and S16 compare second-order silent COEFFICIENTS c2 (silent probability = c1 p + c2 p^2 + ...).  That is the right comparison between rounds whose first-order coefficient c1 is the same,
which holds for the flagged and verified-cat rounds (c1 = 0) and for teleportation rounds whose resource checks are flagged (T1/T3-type designs, c1 = 0).  It is NOT a fair comparison against
rounds with c1 > 0: the local round (c1 = 8/15) and the conventional joint round (c1 = 4/15), whose first-order term dominates at every realistic p.  Here the exact distribution of each
round (independent location faults, model M2: every gate or preparation location faults with probability p, every readout flip with probability r p) is accumulated by non-negative convolution
(S19's engine for the V1.0 rounds; S17's single-fault effects for the teleportation rounds), the silent probability is compared at each p, and the exact crossings in p are found.

Claims
  Y0  The exact distributions are probability distributions, and at small p the silent probability equals c1 p + c2 p^2 of S15, S16 and V0.9 (within 2 % at p = 1e-5, for r = 1 and r = 0.1).  DERIVED
  Y1  (the correction) With a PERFECT resource and r = 1, the teleportation round's silent probability is BELOW the local round's and the conventional joint round's for every p below a crossing
      (exact crossings are printed; the first-order estimates c1 / (c2_t - c2_o) are 2.9 % and 1.5 %), and ABOVE the flagged and verified-cat joint rounds' at every p in 1e-5 .. 3e-2.  The c2
      ratios of S15 (8.5x, 2.0x versus flagged, cat) are therefore the relevant ones only for those two rounds.                                                                             DERIVED
  Y2  S14's resource with flagged checks on both blocks (T3, c1 = 0) at r = 1 and r = 0.1: lower than the local round everywhere in 1e-5 .. 1e-1 and than the conventional joint round at small p
      (crossing printed), above the flagged and cat rounds at every p up to 3e-2.                                                                                                             DERIVED
  Y3  S14's resource exactly as written (T0, c1 = 4/15 like the conventional joint round) is above the conventional joint round at every p in the range (its c2 is 45 against 2.4 and its c1 is the same).  DERIVED
Not claimed: anything about the heralded metric (not combined), about faults in the preparation of the resource beyond the S15/S17 circuits, about idle or incoming faults (M3), or about any platform's
readout-to-gate ratio.  Author-side; not an independent reproduction.  Requires numpy.  Run with python3 -I.
"""
import importlib.util, math, os, sys, time
from fractions import Fraction as Fr
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
def _load(name, rel):
    sp = importlib.util.spec_from_file_location(name, os.path.join(ROOT, *rel)); m = importlib.util.module_from_spec(sp)
    sys.modules[name] = m; sp.loader.exec_module(m); return m
s19 = _load("s19", ["explorations", "s19-v10-exact-reproduction", "v10_exact_reproduction.py"])
s17 = _load("s17", ["explorations", "s17-resource-design", "resource_design.py"])
s15 = s17.s15

OK = True
def check(name, ok):
    global OK
    OK = OK and bool(ok); print(("PASS  " if ok else "FAIL  ") + name, flush=True)

PAR4 = np.array([bin(v).count("1") & 1 for v in range(16)])
STABSET = {(0, 0), (15, 0), (0, 15), (15, 15)}

class Tele:
    """exact distribution of a teleportation round under model M2 (gate/preparation faults at rate p, readout flips at rate r p), from S17's single-fault effects"""
    def __init__(self, nm, kw):
        t0 = time.time(); self.nm = nm; R = s15.Round("J", **kw); self.R = R; eff, cons, canon = s17.effects(R); self.consistent = cons
        self.d = len(R.dets); self.nloc = len(R.locs)
        self.kind = ["m" if R.ops[R.locs[i][0][0]][0] in ("MZ", "MX") else "g" for i in range(self.nloc)]
        self.eff = [[syn | (x << self.d) | (z << (self.d + 4)) for syn, (x, z) in row] for row in eff]
        self.N = 1 << (self.d + 8); idx = np.arange(self.N); self.idx = idx
        syn = idx & ((1 << self.d) - 1); x = (idx >> self.d) & 15; z = (idx >> (self.d + 4)) & 15
        instab = np.array([(int(a), int(b)) in STABSET for a, b in zip(x, z)])
        clean_pass = (syn == 0) & (PAR4[x] == 0) & (PAR4[z] == 0)
        self.m_sil = clean_pass & ~instab; self.m_dam = (syn == 0) & ((PAR4[x] == 1) | (PAR4[z] == 1)); self.m_rej = syn != 0
        self.build_s = time.time() - t0
    def at(self, p, r):
        P = np.zeros(self.N); P[0] = 1.0
        for row, kd in zip(self.eff, self.kind):
            rate = p if kd == "g" else r * p
            if rate == 0.0: continue
            acc = np.zeros(self.N)
            for f in row: acc += P[self.idx ^ f]
            P = (1.0 - rate) * P + rate * acc / len(row)
        return dict(silent=P[self.m_sil].sum(), damaged=P[self.m_dam].sum(), reject=P[self.m_rej].sum(), total=P.sum())

CACHE = {}
def silent_of(E, T, nm, p, r, field="silent"):
    """exact probability of one category for a V1.0 round (nm in E) or a teleportation round (nm in T), cached"""
    k = (nm, p, r)
    if k not in CACHE: CACHE[k] = T[nm].at(p, r) if nm in T else E[nm].at({"g": p, "mz": r * p, "mx": r * p})
    return CACHE[k][field]

def crossing(f, lo=1e-5, hi=1e-1, n=60):
    """all sign changes of f(p) on a log grid, refined by bisection; also whether f > 0 at the lowest p"""
    grid = [lo * (hi / lo) ** (i / n) for i in range(n + 1)]; vals = [f(g) for g in grid]; out = []
    for i in range(n):
        if (vals[i] > 0) != (vals[i + 1] > 0):
            a, b = grid[i], grid[i + 1]; sa = vals[i] > 0
            for _ in range(40):
                m = math.sqrt(a * b)
                if (f(m) > 0) == sa: a = m
                else: b = m
            out.append(math.sqrt(a * b))
    return out, vals[0] > 0, grid

def main():
    t00 = time.time()
    names = ["L conv (baseline)", "J conv", "J flag", "J cat (verified)"]
    E = {nm: s19.Engine(nm) for nm in names}
    T = {}
    for nm, kw in (("ideal", dict(ideal=True)), ("T0", dict(on="A")), ("T3", dict(on="AN", flagged=True))):
        T[nm] = Tele(nm, kw)
        print("      %-6s %3d locations, %d detector bits, built in %.0f s" % (nm, T[nm].nloc, T[nm].d, T[nm].build_s), flush=True)
    S = lambda nm, p, r: silent_of(E, T, nm, p, r)
    check("Y0a single-fault effects are the same on 3 measurement branches in every teleportation circuit", all(t.consistent for t in T.values()))
    check("Y0b every exact distribution sums to 1 (to 1e-12)", all(abs(silent_of(E, T, nm, 3e-3, 0.5, "total") - 1) < 1e-12 for nm in list(T) + names))
    c1 = {"L conv (baseline)": 8 / 15, "J conv": 4 / 15, "J flag": 0.0, "J cat (verified)": 0.0}
    c2_r1 = {"L conv (baseline)": 1.244, "J conv": 2.427, "J flag": 2.320, "J cat (verified)": 9.902}
    p0 = 1e-5; ok0 = all(abs(S(nm, p0, 1.0) / (c1[nm] * p0 + c2_r1[nm] * p0 ** 2) - 1) < 0.02 for nm in names)
    ok0 &= abs(S("ideal", p0, 1.0) / (492 / 25 * p0 ** 2) - 1) < 0.02 and abs(S("T3", p0, 1.0) / (50.960 * p0 ** 2) - 1) < 0.02
    ok0 &= abs(S("ideal", p0, 0.1) / ((32 / 25 + 32 / 5 * 0.1 + 12 * 0.01) * p0 ** 2) - 1) < 0.02
    check("Y0c at p = 1e-5 and r = 1 the exact silent probabilities equal c1 p + c2 p^2 within 2 % (four V1.0 rounds, ideal and T3 teleportation), and the ideal round at r = 0.1 equals (32/25 + 32/5 r + 12 r^2) p^2", ok0)
    PS = [1e-4, 1e-3, 3e-3, 1e-2, 3e-2]
    for r in (1.0, 0.1):
        print("== exact silent-logical probability per round, model M2, readout flip = r x gate fault, r = %g ==" % r)
        print("      round                " + "".join("p=%-10g" % p for p in PS))
        for nm in names: print("      %-20s " % nm + "".join("%-12.3e" % S(nm, p, r) for p in PS))
        for nm in ("ideal", "T0", "T3"): print("      teleport %-11s " % nm + "".join("%-12.3e" % S(nm, p, r) for p in PS))
    print("== probability that the round is REJECTED at p = 1e-3, r = 1 (for information; NOT combined with the silent probability) ==")
    print("      " + "   ".join("%s %.4f" % (nm, silent_of(E, T, nm, 1e-3, 1.0, "reject")) for nm in names + ["ideal", "T0", "T3"]))
    cr = {}
    for r in (1.0, 0.1):
        for tn in ("ideal", "T0", "T3"):
            for on in names:
                cr[(tn, on, r)] = crossing(lambda p, tn=tn, on=on, r=r: S(tn, p, r) - S(on, p, r))
            print("      r=%-4g teleport %-5s " % (r, tn) + "; ".join("vs %s: %s at p = 1e-5, crossings %s" % (on, "above" if cr[(tn, on, r)][1] else "below", ["%.2e" % x for x in cr[(tn, on, r)][0]] or "none") for on in names), flush=True)
    grid = cr[("ideal", "J flag", 1.0)][2]; gridp = [g for g in grid if g <= 3e-2 * 1.0000001]
    loc = cr[("ideal", "L conv (baseline)", 1.0)]; cv = cr[("ideal", "J conv", 1.0)]
    est_loc = (8 / 15) / (492 / 25 - 1.244); est_cv = (4 / 15) / (492 / 25 - 2.427)
    check("Y1a perfect resource, r = 1: the teleportation round is lower than the local round for p below %.3e and lower than the conventional joint round for p below %.3e (first-order estimates c1 / (c2_t - c2_o): %.3e and %.3e)"
          % (loc[0][0], cv[0][0], est_loc, est_cv), not loc[1] and not cv[1] and 0.5 < loc[0][0] / est_loc < 1.5 and 0.5 < cv[0][0] / est_cv < 1.5)
    check("Y1b perfect resource, r = 1: the teleportation round is above BOTH the flagged and the verified-cat joint rounds at every one of %d log-spaced p from 1e-5 to 3e-2 (so the c2 comparison of S15 is the right one against those two)" % len(gridp),
          all(S("ideal", p, 1.0) > S(nm, p, 1.0) for p in gridp for nm in ("J flag", "J cat (verified)")))
    at1 = {nm: S(nm, 1e-3, 1.0) for nm in names + ["ideal", "T0", "T3"]}
    print("      at p = 1e-3, r = 1: " + ", ".join("%s %.2e" % (k, v) for k, v in at1.items()))
    check("Y1c at p = 1e-3, r = 1 the perfect-resource teleportation round (%.2e) is %.0f x below the local round (%.2e) and %.0f x below the conventional joint round (%.2e), %.1f x above the verified cat (%.2e) and %.1f x above the flagged round (%.2e)"
          % (at1["ideal"], at1["L conv (baseline)"] / at1["ideal"], at1["L conv (baseline)"], at1["J conv"] / at1["ideal"], at1["J conv"], at1["ideal"] / at1["J cat (verified)"], at1["J cat (verified)"],
             at1["ideal"] / at1["J flag"], at1["J flag"]),
          at1["ideal"] < at1["L conv (baseline)"] and at1["ideal"] < at1["J conv"] and at1["ideal"] > at1["J cat (verified)"] and at1["ideal"] > at1["J flag"])
    t3 = {on: cr[("T3", on, 1.0)] for on in names}; lc = t3["L conv (baseline)"][0]; cc = t3["J conv"][0]
    check("Y2a S14's resource with flagged checks on both blocks (T3), r = 1: lower than the local round at every p from 1e-5 to 1e-1 (crossings: %s), lower than the conventional joint round for p below %.2e (crossings %s), and above the flagged and verified-cat rounds at every one of the %d p up to 3e-2"
          % (["%.2e" % x for x in lc] or "none", cc[0], ["%.2e" % x for x in cc], len(gridp)),
          (not t3["L conv (baseline)"][1]) and not lc and (not t3["J conv"][1]) and len(cc) >= 1 and all(S("T3", p, 1.0) > S(nm, p, 1.0) for p in gridp for nm in ("J flag", "J cat (verified)")))
    check("Y2b at r = 0.1 T3 is still above the flagged and cat rounds at every one of the %d p up to 3e-2 (its gate-gate term alone, 27.6, exceeds their whole c2)" % len(gridp),
          all(S("T3", p, 0.1) > S(nm, p, 0.1) for p in gridp for nm in ("J flag", "J cat (verified)")))
    check("Y3 S14's resource as written (T0) is above the conventional joint round at every one of the %d p from 1e-5 to 3e-2 at r = 1 (same c1 = 4/15, c2 45.06 against 2.43)" % len(gridp),
          all(S("T0", p, 1.0) > S("J conv", p, 1.0) for p in gridp))
    print("NOTE  Conditional on model M2 (equal fault probability p for every gate and preparation location, r p for every readout flip) and on S15's and S17's circuits.  The first-order coefficients decide the comparison against the local")
    print("      and conventional joint rounds at any realistic p; the second-order coefficients decide it against the flagged and cat rounds.  This corrects how S15's F2b line and S16's crossover table can be read: the ratios")
    print("      15.8 and 8.1 compare c2 only and say nothing about the silent probability against rounds whose c1 is not 0.  Total wall-clock %.0f s" % (time.time() - t00))
    print("ALL PASS" if OK else "FAILED")
    return 0 if OK else 1

if __name__ == "__main__": sys.exit(main())
