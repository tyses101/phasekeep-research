#!/usr/bin/env python3
"""S26: how much worse than a gate may idling be before flagging stops paying?  (the idle-to-gate fault-rate ratio rho)

V0.9 and V1.0 give every idle location the same fault probability p as every gate (rho = 1) and find that the flagged joint round beats the conventional joint round only below p of about
1.05e-3.  S23 and S24 varied how idle time is COUNTED; here the idle fault RATE is varied: every idle location faults with probability rho x p (rho = 0 is model M2 plus incoming faults, rho = 1
is V0.9's M3), under V0.9's serial counting and under S23's layered counting (a layer holding a measurement lasts m gate times).  For each p the exact smallest rho at which the conventional joint
round's silent probability falls to the flagged round's is found; it is compared with the first-order estimate that follows from the exact second-order coefficient,
    c2(rho) = A + rho x B + rho^2 x C   (A: pairs of gate and incoming-fault locations, B: one idle location, C: two idle locations),   flagged better while  (c1_conv - c1_flag) / p  >  c2_flag(rho) - c2_conv(rho),
with c1_conv - c1_flag = 4/15 (the first-order silent coefficients do not depend on rho in either counting).  Incoming faults on the data axes are not scaled by rho.

Claims
  R0  The weighted second-order coefficient reproduces S23's values at rho = 1 (158.249 and 426.942 serially; 51.360 and 78.276 layered with m = 1), and the exact silent probabilities at small p
      equal c1 p + c2(rho) p^2 within 2 % for rho = 0.1, 1 and 3.                                                                                                                           DERIVED
  R1  The exact critical ratio rho*(p) (flagged round better below it) is tabulated for p = 1e-4, 3e-4, 1e-3, 3e-3, 1e-2 under four counting conventions; at rho = 1 it reproduces the exact
      crossing p = 1.0496e-3 of S19 and S23 (serial).  Under serial counting it is 3.30, 1.89, 1.025, 0.59, 0.34; under layered counting with m = 1 it is 11.2, 6.4, 3.55, 2.1, 1.36.    DERIVED
  R2  The first-order estimate (second-order coefficients only) is within 10 % of the exact rho* for p up to 1e-3 in every convention (it is worse at 1e-2, where it is not claimed); rho* falls as 1 / sqrt(p) between 1e-4 and 1e-3 to within 10 %.   DERIVED
Not claimed: any idle rate of a platform; that idle faults and gate faults are Pauli and independent (as in V0.9); the other rounds' ratios.  Author-side; not an independent reproduction.  Requires numpy.  Run with python3 -I.
"""
import importlib.util, math, os, sys, time
from fractions import Fraction as Fr
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
def _load(name, rel):
    sp = importlib.util.spec_from_file_location(name, os.path.join(ROOT, *rel)); m = importlib.util.module_from_spec(sp)
    sys.modules[name] = m; sp.loader.exec_module(m); return m
s23 = _load("s23", ["explorations", "s23-flag-design-search", "flag_design_search.py"])

OK = True
def check(name, ok):
    global OK
    OK = OK and bool(ok); print(("PASS  " if ok else "FAIL  ") + name, flush=True)

class Round:
    """one round under one counting convention: exact distribution engine (idle rates scalable) and second-order pair counts"""
    def __init__(self, nm, conv, m):
        r = s23.v10.load()[nm]
        if conv == "serial": locs, ops = s23.serial_locations(r["ops"], "M3")
        else: locs, ops, _ = s23.layered_locations(r["ops"], m)
        self.locs = locs; self.coef = s23.Coef(locs, ops, r["dets"], r["code"]); self.P = s23.Prob(locs, ops, r["dets"], r["code"]); self.base = [mu for _, _, mu in self.P.locs]
        self.c1 = self.coef.c1["silent"]
        # pair counts per pair of locations (integers in units of 1/(2*225)), kept for the polynomial in rho
        per = self.coef.per; self.pairs = []
        for i in range(len(per)):
            for j in range(i + 1, len(per)):
                cnt = 0
                for a in per[i][1]:
                    if a[3] == "silent": continue
                    for b in per[j][1]:
                        if b[3] != "silent" and s23.cat(a[0] ^ b[0], a[1] ^ b[1], a[2] ^ b[2], "J") == "silent": cnt += 2 * a[4] * b[4]
                if cnt: self.pairs.append((i, j, cnt))
        self.idle = [t == "idle" for t, _, _ in locs]
    def c2(self, rho):
        f = [self.base[k] * (rho if self.idle[k] else 1.0) for k in range(len(self.base))]
        return sum(c * f[i] * f[j] for i, j, c in self.pairs) / (2 * 225)
    def silent(self, p, rho):
        self.P.locs = [(t, row, (mu * rho if t == "idle" else mu)) for (t, row, _), mu in zip(self.P.locs, self.base)]
        return self.P.at(p)["silent"]

def first_rho(F, C, p, lo=1e-3, hi=1e2, n=100):
    """smallest rho at which the flagged round's silent probability reaches the conventional one's (None if never in [lo, hi])"""
    f = lambda rho: F.silent(p, rho) - C.silent(p, rho); prev = None
    for k in range(n + 1):
        r = lo * (hi / lo) ** (k / n); g = f(r)
        if prev is not None and prev[1] < 0 <= g:
            a, b = math.log(prev[0]), math.log(r)
            for _ in range(45):
                mid = (a + b) / 2
                if f(math.exp(mid)) < 0: a = mid
                else: b = mid
            return math.exp((a + b) / 2)
        prev = (r, g)
    return None

def est_rho(F, C, p, lo=1e-3, hi=1e2, n=200):
    """first-order estimate: smallest rho at which c2_flag(rho) - c2_conv(rho) reaches (c1_conv - c1_flag) / p"""
    target = float(C.c1 - F.c1) / p; g = lambda rho: F.c2(rho) - C.c2(rho) - target; prev = None
    for k in range(n + 1):
        r = lo * (hi / lo) ** (k / n); v = g(r)
        if prev is not None and prev[1] < 0 <= v:
            a, b = math.log(prev[0]), math.log(r)
            for _ in range(45):
                mid = (a + b) / 2
                if g(math.exp(mid)) < 0: a = mid
                else: b = mid
            return math.exp((a + b) / 2)
        prev = (r, v)
    return None

def main():
    t00 = time.time(); CONV = [("serial", "serial", 1), ("m=1", "layered", 1), ("m=3", "layered", 3), ("m=6", "layered", 6)]
    RD = {cn: {nm: Round(nm, cv, m) for nm in ("J conv", "J flag")} for cn, cv, m in CONV}
    # ---- R0
    c = {cn: (float(RD[cn]["J conv"].c2(1.0)), float(RD[cn]["J flag"].c2(1.0))) for cn, _, _ in CONV}
    check("R0a at rho = 1 the weighted second-order coefficients are %.3f / %.3f serially and %.3f / %.3f layered with m = 1 (S23: 158.249 / 426.942 and 51.360 / 78.276); with rho = 0 they are %.3f / %.3f serially (M2 plus incoming faults)" % (
        *c["serial"], *c["m=1"], float(RD["serial"]["J conv"].c2(0.0)), float(RD["serial"]["J flag"].c2(0.0))),
          abs(c["serial"][0] - 158.249) < 5.1e-4 and abs(c["serial"][1] - 426.942) < 5.1e-4 and abs(c["m=1"][0] - 51.360) < 5.1e-4 and abs(c["m=1"][1] - 78.276) < 5.1e-4)
    ok = True; p0 = 1e-5
    for cn, _, _ in CONV:
        for nm in ("J conv", "J flag"):
            for rho in (0.1, 1.0, 3.0):
                R = RD[cn][nm]; ex = R.silent(p0, rho); ap = float(R.c1) * p0 + R.c2(rho) * p0 ** 2; ok &= abs(ex / ap - 1) < 0.02
    check("R0b at p = 1e-5 the exact silent probabilities equal c1 p + c2(rho) p^2 within 2 % for both rounds, rho = 0.1, 1, 3 and all four conventions", ok)
    # ---- R1 / R2
    PS = [1e-4, 3e-4, 1e-3, 3e-3, 1e-2]; EX = {}; ES = {}
    print("      critical idle-to-gate ratio rho* (flagged joint round better than conventional joint round for idle rate below rho* x p); exact (first-order estimate):")
    print("      %-8s " % "" + "  ".join("p=%-14.0e" % p for p in PS))
    for cn, _, _ in CONV:
        for p in PS: EX[(cn, p)] = first_rho(RD[cn]["J flag"], RD[cn]["J conv"], p); ES[(cn, p)] = est_rho(RD[cn]["J flag"], RD[cn]["J conv"], p)
        print("      %-8s " % cn + "  ".join("%-16s" % ("%.3f (%.3f)" % (EX[(cn, p)], ES[(cn, p)])) for p in PS), flush=True)
    xs = EX[("serial", 1.0496e-3)] if ("serial", 1.0496e-3) in EX else first_rho(RD["serial"]["J flag"], RD["serial"]["J conv"], 1.0496e-3)
    check("R1a at p = 1.0496e-3 (the exact crossing of S19 and S23 at rho = 1) the serial critical ratio is %.4f, i.e. 1 to 3 figures" % xs, abs(xs - 1.0) < 1.5e-3)
    check("R1b serial: rho* = %.3f, %.3f, %.3f, %.3f, %.3f for p = 1e-4 .. 1e-2 (at p = 1e-3 the idle rate may be at most %.1f %% above the gate rate)" % (*[EX[("serial", p)] for p in PS], 100 * (EX[("serial", 1e-3)] - 1)),
          abs(EX[("serial", 1e-4)] - 3.30) < 0.02 and abs(EX[("serial", 1e-3)] - 1.025) < 0.01 and abs(EX[("serial", 1e-2)] - 0.336) < 0.01)
    check("R1c layered with m = 1: rho* = %.2f, %.2f, %.3f, %.2f, %.2f; with m = 3: %.2f at p = 1e-4 and %.3f at 1e-3; with m = 6: %.3f at 1e-3 (close to the serial value, as in S23)" % (
        *[EX[("m=1", p)] for p in PS], EX[("m=3", 1e-4)], EX[("m=3", 1e-3)], EX[("m=6", 1e-3)]),
          abs(EX[("m=1", 1e-4)] - 11.2) < 0.1 and abs(EX[("m=1", 1e-3)] - 3.55) < 0.05 and abs(EX[("m=3", 1e-3)] - 1.86) < 0.05 and abs(EX[("m=6", 1e-3)] - 1.03) < 0.02
          and all(EX[(cn, a)] > EX[(cn, b)] for cn, _, _ in CONV for a, b in zip(PS, PS[1:])))
    rel = max(abs(ES[(cn, p)] / EX[(cn, p)] - 1) for cn, _, _ in CONV for p in PS if p <= 1e-3)
    sl = max(abs(EX[(cn, 1e-4)] / EX[(cn, 1e-3)] / math.sqrt(10) - 1) for cn, _, _ in CONV)
    check("R2 the first-order estimate from the exact second-order coefficients is within %.1f %% of the exact rho* for every convention and p up to 1e-3 (but %.0f %% off at p = 1e-2, convention m = 1, where the estimate leaves out all terms beyond second order); rho*(1e-4) / rho*(1e-3) differs from sqrt(10) by at most %.1f %%" % (100 * rel, 100 * max(abs(ES[(cn, 1e-2)] / EX[(cn, 1e-2)] - 1) for cn, _, _ in CONV), 100 * sl), rel < 0.10 and sl < 0.10)
    print("NOTE  rho is a free parameter (V0.9 and V1.0 fix it at 1).  A statement like 'flagging pays while idle faults are no more than rho* times as likely as gate faults' is exact for V0.9's Pauli model and counting conventions, and says nothing about any platform.  Total wall-clock %.0f s" % (time.time() - t00))
    print("ALL PASS" if OK else "FAILED")
    return 0 if OK else 1

if __name__ == "__main__": sys.exit(main())
