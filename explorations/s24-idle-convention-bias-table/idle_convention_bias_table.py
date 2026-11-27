#!/usr/bin/env python3
"""S24: which statements of V1.0's bias table depend on how idle time is counted?

V1.0's bias table (13 settings x 5 rounds, silent probability at p = 1e-3 in model M3) and V0.9's crossing both use M3, which puts one idle location after EVERY OPERATION on every live untouched
qubit (as if operations ran one after another).  S23 showed that this convention carries most of the second-order silent coefficient and that counting idle time per parallel layer removes the
unbiased flagged / conventional crossing.  Here the same question is asked of V1.0's biased-noise statements.  S23's Pauli-frame engine is given V1.0's bias weights (a bias weight b on the Z or X
Pauli of a faulted qubit, identity components weigh 1; idle and incoming faults weighted the same way), it is checked against all 65 printed table entries, and the table is then recomputed under a
family of idle conventions: serial (V0.9/V1.0), and the layered convention of S23 with a measurement layer lasting m = 1, 2, 3, 6 and 10 gate times.  The conventions are a PROPOSED sensitivity
(the idle RATE per layer equals the gate rate; the durations are assumed), not hardware timings.

Claims
  C0  With V1.0's rule the frame engine reproduces all 65 entries of V1.0's printed bias table (13 rows x 5 rounds) and all 13 'lowest' labels (a third engine after S19's).                         DERIVED
  C1  Under the layered convention (m = 1) five of the 13 'lowest' labels change: with the bias on the data alone (Z b = 10 and 100, X b = 10) the flagged round replaces the conventional joint
      round, and with X bias b = 100 on all qubits or on the data alone the local round replaces the ZZZZ-only round.  The number that change at m = 2, 3, 6, 10 is printed.               DERIVED on PROPOSED
  C2  V1.0's four statements about the table (E2a flagged lowest and the local round about 20 times higher under Z bias b = 100; E2b under X bias b = 100 the local and ZZZZ-only rounds are below the
      flagged and conventional joint rounds; E2c with bias on the ancillas alone the flagged round is lowest; E2d with Z-biased data alone the conventional joint round is below the flagged round) are
      tested under each convention.  All four hold serially.  At m = 1 E2a and E2c hold, E2d fails and E2b holds only for the local round.  E2a holds only at m = 1, E2c only up to m = 2,
      and the 20 x ratio falls to 14.6 x at m = 10; the local-round half of E2b holds in every convention.                                                                                    DERIVED on PROPOSED
  C3  The X-bias value b* at which the local round's silent probability equals each joint round's (S19: 26.0, 28.0, 6.9 for conventional, flagged, cat) is recomputed under each convention.     DERIVED on PROPOSED
Not claimed: that any convention is right; hardware timing; the loss table and the readout lines of V1.0 (they use model M2 and do not depend on idle counting); independence from V1.0's fault
definition.  Author-side; not an independent reproduction.  Requires numpy.  Run with python3 -I.
"""
import importlib.util, math, os, re, sys, time
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

class BProb(s23.Prob):
    """S23's exact convolution with V1.0's bias weights on gate, preparation, idle and incoming locations"""
    def __init__(self, locs, ops, dets, code="J"):
        super().__init__(locs, ops, dets, code); self.pds = [[f[2] for f in fl] for _, fl, _ in locs]
    def at(self, p, bias=None):
        P = np.zeros(self.N); P[0] = 1.0
        for (typ, row, mu), pds in zip(self.locs, self.pds):
            r = min(1.0, p * mu); ws = np.array([s23.bias_w(pd, bias) if typ in ("g", "idle", "in") else 1.0 for pd in pds]); ws = ws / ws.sum(); acc = np.zeros(self.N)
            for e, w in zip(row, ws): acc += w * P[self.idx ^ e]
            P = (1 - r) * P + r * acc
        return dict(silent=P[self.sil].sum(), reject=P[self.rj].sum(), total=P.sum())

NAMES = ["L conv (baseline)", "J conv", "J flag", "J cat (verified)", "J ZZZZ only (partial)"]
SHORT = {"L conv (baseline)": "local", "J conv": "conv", "J flag": "flag", "J cat (verified)": "cat", "J ZZZZ only (partial)": "ZZZZ-only"}
CONVS = [("serial", None), ("m=1", 1), ("m=2", 2), ("m=3", 3), ("m=6", 6), ("m=10", 10)]

def fmt_ok(computed, tok):
    v = float(tok); ulp = 10 ** (math.floor(math.log10(abs(v))) - 2) if v != 0 else 1e-18
    return abs(computed - v) <= 0.5 * ulp * (1 + 1e-6)

def main():
    t00 = time.time(); R10 = s23.v10.load()
    LOG = open(os.path.join(ROOT, "reproduction", "execution-logs", "v1.0.stdout.txt"), encoding="utf-8").read(); rows = {}
    for m in re.finditer(r"^\s+([ZX])\s+(all|data|anc)\s+(\d+)((?:\s+[0-9.]+e[-+]\d+){5})\s+(.+?)\s*$", LOG, re.M): rows[(m.group(1), m.group(2), int(m.group(3)))] = (m.group(4).split(), m.group(5))
    ORDER = sorted(rows, key=lambda k: (k[0] != "Z", k[1] != "all", k[2]))
    E = {}
    for cn, m in CONVS:
        E[cn] = {}
        for nm in NAMES:
            r = R10[nm]
            if m is None: locs, ops = s23.serial_locations(r["ops"], "M3")
            else: locs, ops, _ = s23.layered_locations(r["ops"], m)
            E[cn][nm] = BProb(locs, ops, r["dets"], r["code"])
    def bias_of(key):
        kind, scope, b = key; return {"data": (kind, b if scope in ("all", "data") else 1), "anc": (kind, b if scope in ("all", "anc") else 1)}
    T = {cn: {key: {nm: E[cn][nm].at(1e-3, bias_of(key))["silent"] for nm in NAMES} for key in ORDER} for cn, _ in CONVS}
    low = lambda row: min(row, key=row.get)
    # ---- C0
    nexact = sum(fmt_ok(T["serial"][key][nm], tok) for key in ORDER for nm, tok in zip(NAMES, rows[key][0])); nlab = sum(low(T["serial"][key]) == rows[key][1] for key in ORDER)
    check("C0 with V1.0's bias rule the frame engine equals V1.0's printed bias table at the printed three figures (%d of 65) and all 13 'lowest' labels agree (%d of 13)" % (nexact, nlab), len(rows) == 13 and nexact == 65 and nlab == 13)
    # ---- C1 labels
    print("      V1.0 bias table, silent probability at p = 1e-3 (model M3), lowest round per setting, by idle convention:")
    print("      %-12s " % "setting" + "  ".join("%-10s" % cn for cn, _ in CONVS))
    for key in ORDER: print("      %-12s " % ("%s %s b=%d" % key) + "  ".join("%-10s" % SHORT[low(T[cn][key])] for cn, _ in CONVS))
    chg = {cn: [key for key in ORDER if low(T[cn][key]) != low(T["serial"][key])] for cn, _ in CONVS}
    print("      labels that differ from the serial table: " + ", ".join("%s %d" % (cn, len(chg[cn])) for cn, _ in CONVS))
    want = {("Z", "data", 10): ("J conv", "J flag"), ("Z", "data", 100): ("J conv", "J flag"), ("X", "data", 10): ("J conv", "J flag"), ("X", "all", 100): ("J ZZZZ only (partial)", "L conv (baseline)"), ("X", "data", 100): ("J ZZZZ only (partial)", "L conv (baseline)")}
    check("C1 layered (m = 1): five of the 13 'lowest' labels change, exactly %s; at m = 2, 3, 6, 10 the numbers that change are %d, %d, %d, %d" % (
        ["%s %s b=%d" % k for k in sorted(want)], len(chg["m=2"]), len(chg["m=3"]), len(chg["m=6"]), len(chg["m=10"])),
        set(chg["m=1"]) == set(want) and all((low(T["serial"][k]), low(T["m=1"][k])) == v for k, v in want.items()))
    # ---- C2 statements
    def stm(cn):
        t = T[cn]; zb = t[("Z", "all", 100)]; xb = t[("X", "all", 100)]
        return {"E2a flagged lowest, Z all b=100": low(zb) == "J flag", "E2a' local > 20 x flagged, Z all b=100": zb["L conv (baseline)"] > 20 * zb["J flag"],
                "E2b X all b=100: local and ZZZZ-only below flagged and conv": xb["L conv (baseline)"] < min(xb["J flag"], xb["J conv"]) and xb["J ZZZZ only (partial)"] < min(xb["J flag"], xb["J conv"]),
                "E2b' X all b=100: local below flagged and conv": xb["L conv (baseline)"] < min(xb["J flag"], xb["J conv"]),
                "E2c anc-only bias (4 settings): flagged lowest": all(low(t[(k, "anc", b)]) == "J flag" for k in "ZX" for b in (10, 100)),
                "E2d Z data b=100: conv below flagged": t[("Z", "data", 100)]["J conv"] < t[("Z", "data", 100)]["J flag"]}
    S = {cn: stm(cn) for cn, _ in CONVS}; names = list(S["serial"])
    print("      V1.0's statements about the table (True = holds):")
    print("      %-62s " % "" + "  ".join("%-7s" % cn for cn, _ in CONVS))
    for nm in names: print("      %-62s " % nm + "  ".join("%-7s" % S[cn][nm] for cn, _ in CONVS))
    check("C2a under V1.0's serial convention all four statements (E2a, E2b, E2c, E2d) hold, as S19 found", all(S["serial"][n] for n in names if n not in ("E2a' local > 20 x flagged, Z all b=100", "E2b' X all b=100: local below flagged and conv")) and S["serial"]["E2a' local > 20 x flagged, Z all b=100"])
    check("C2b under the layered convention with m = 1: E2a, E2a' and E2c hold; E2d (Z-biased data alone: conventional below flagged) and the ZZZZ-only half of E2b FAIL (the local half of E2b holds)",
          S["m=1"]["E2a flagged lowest, Z all b=100"] and S["m=1"]["E2a' local > 20 x flagged, Z all b=100"] and S["m=1"]["E2c anc-only bias (4 settings): flagged lowest"] and not S["m=1"]["E2d Z data b=100: conv below flagged"]
          and not S["m=1"]["E2b X all b=100: local and ZZZZ-only below flagged and conv"] and S["m=1"]["E2b' X all b=100: local below flagged and conv"])
    ratio = {cn: T[cn][("Z", "all", 100)]["L conv (baseline)"] / T[cn][("Z", "all", 100)]["J flag"] for cn, _ in CONVS}
    print("      local / flagged silent ratio at Z bias b = 100 on every qubit: " + ", ".join("%s %.1f" % (cn, ratio[cn]) for cn, _ in CONVS))
    check("C2c the flagged round's advantage over the local round under Z bias b = 100 (V1.0: about 20 x) is %.1f x serial, %.1f x to %.1f x for m = 1, 2, 3, 6 (all above 20) and %.1f x at m = 10 (below 20): it needs a measurement layer shorter than about 10 gate times" % (
        ratio["serial"], min(ratio[c] for c in ("m=1", "m=2", "m=3", "m=6")), max(ratio[c] for c in ("m=1", "m=2", "m=3", "m=6")), ratio["m=10"]),
          ratio["serial"] > 20 and all(ratio[c] > 20 for c in ("m=1", "m=2", "m=3", "m=6")) and ratio["m=10"] < 20)
    chk = {cn: (S[cn]["E2a flagged lowest, Z all b=100"], S[cn]["E2c anc-only bias (4 settings): flagged lowest"]) for cn, _ in CONVS}
    check("C2d 'flagged lowest under Z bias on every qubit' (E2a) holds serially and at m = 1 only (the verified cat is lowest for m = 2, 3, 6 and the conventional joint round at m = 10); E2c (ancilla-only bias) holds serially and for m = 1, 2 only; the other tests are printed above",
          [chk[cn][0] for cn, _ in CONVS] == [True, True, False, False, False, False] and [chk[cn][1] for cn, _ in CONVS] == [True, True, True, False, False, False])
    # ---- C3 X-bias crossing
    def silent_X(cn, nm, b): return E[cn][nm].at(1e-3, {"data": ("X", b), "anc": ("X", b)})["silent"]
    bstar = {}
    for cn, _ in CONVS:
        for nm in ("J conv", "J flag", "J cat (verified)"):
            f = lambda b: silent_X(cn, "L conv (baseline)", b) - silent_X(cn, nm, b); lo, hi = 1.0, 1000.0
            assert f(lo) > 0 > f(hi), (cn, nm, f(lo), f(hi))
            for _ in range(55):
                mid = math.sqrt(lo * hi)
                if f(mid) > 0: lo = mid
                else: hi = mid
            bstar[(cn, nm)] = math.sqrt(lo * hi)
    grid = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]; mono = True
    for cn, _ in CONVS:
        for nm in NAMES:
            vals = [silent_X(cn, nm, b) for b in grid]
            mono &= all(a >= c * (1 - 1e-12) for a, c in zip(vals, vals[1:])) if nm in ("L conv (baseline)", "J ZZZZ only (partial)") else all(a <= c * (1 + 1e-12) for a, c in zip(vals, vals[1:]))
    print("      X-bias crossing b* (local equals the joint round's silent probability), p = 1e-3, M3, same bias on every qubit:")
    print("      %-18s " % "" + "  ".join("%-9s" % cn for cn, _ in CONVS))
    for nm in ("J conv", "J flag", "J cat (verified)"): print("      %-18s " % nm + "  ".join("%-9.1f" % bstar[(cn, nm)] for cn, _ in CONVS))
    check("C3a serial b* are 26.0, 28.0 and 6.9 (S19); on the grid b = 1..1000 the local and ZZZZ-only rounds' silent probability is non-increasing in b and every joint round's non-decreasing in every convention (so each crossing is unique)",
          abs(bstar[("serial", "J conv")] - 26.0) < 0.05 and abs(bstar[("serial", "J flag")] - 28.0) < 0.05 and abs(bstar[("serial", "J cat (verified)")] - 6.9) < 0.05 and mono)
    lm1 = {nm: bstar[("m=1", nm)] for nm in ("J conv", "J flag", "J cat (verified)")}
    check("C3b layered (m = 1): b* = %.1f (conventional), %.1f (flagged), %.1f (cat): the flagged round's crossing moves from 28.0 to %.1f and the cat's from 6.9 to %.1f, so S19's and V1.0's ordering of the three crossings is convention-dependent" % (lm1["J conv"], lm1["J flag"], lm1["J cat (verified)"], lm1["J flag"], lm1["J cat (verified)"]),
          lm1["J flag"] > 2 * bstar[("serial", "J flag")] and lm1["J cat (verified)"] > 5 * bstar[("serial", "J cat (verified)")] and lm1["J conv"] < bstar[("serial", "J conv")])
    print("NOTE  Everything is conditional on V1.0's location model and bias rule, the equal rate p = 1e-3 for gate, idle and incoming locations, and the idle conventions above (the layered ones are a PROPOSED sensitivity).  Total wall-clock %.0f s" % (time.time() - t00))
    print("ALL PASS" if OK else "FAILED")
    return 0 if OK else 1

if __name__ == "__main__": sys.exit(main())
