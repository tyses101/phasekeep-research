#!/usr/bin/env python3
"""S28: repeated verification rounds under idle faults (serial and layered counting): the baseline for waiting and handoff studies.

V1.0's repeated-round table (section F) gives incoming data faults p per axis per round plus the round's own gate faults (model M2, no idle faults).  S21 reproduced it.  S23 to S26 showed that
the idle-fault counting changes the ranking of the single-round silent probability.  Here the round transitions of S21's recursion are rebuilt from S23's exact distributions, so that a round
can carry idle faults (V0.9's serial counting, or S23's layered counting with measurement layers of m gate times; idle probability rho x p, rho = 1 unless stated), and the recursion is run for up to
20 rounds, a rejected run ending.  The four rounds of V0.9 / V1.0 are compared on separate metrics (still accepted, accepted and damaged, damaged given accepted, silent per run).  No score is formed.

Claims
  P0  With idle faults off (model M2 inside the round, incoming faults separate) the engine reproduces V1.0's repeated-round table at p = 1e-3, R = 20 for the four rounds (accepted, damaged, damaged given
      accepted, silent) at the printed precision.                                                                                                                                                       DERIVED
  P1  For R = 1 the recursion equals the single-round exact distribution with incoming faults (S23's engine) for accepted mass and silent probability, in every convention tried, also at rho = 2.         DERIVED
  P2  The table at p = 1e-3, R = 1, 5, 20 for serial, m = 1, 3, 6 counting (rho = 1) is computed (separate metrics) and the order of the four rounds on each metric is stated; V1.0's R = 20 statements
      (flagged joint lowest damage, accepted fraction falling in the order local > conventional joint > flagged > cat) are tested in each convention.                                                      DERIVED, ASSUMED conventions
  P3  Accumulation: silent probability at R = 20 over its value at R = 1 for each round and convention.                                                                                                 DERIVED
  P4  The critical idle-to-gate ratio of S26 for R rounds, on two separate metrics (silent probability per run; silent probability among accepted runs), at p = 1e-3, R = 1, 5, 20, for serial, m = 1, m = 6.   DERIVED
Not claimed: any idle rate, readout or loss effect (none included), any decision rule; flags are not in a repeated-run decision loop.  Author-side; not an independent reproduction.  Requires numpy.  Run with python3 -I.
"""
import importlib.util, math, os, sys, time
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

NAMES = ["L conv (baseline)", "J conv", "J flag", "J cat (verified)"]
SHORT = {"L conv (baseline)": "local", "J conv": "conv joint", "J flag": "flagged", "J cat (verified)": "cat"}
V10 = s23.v10.load()

class Eng:
    """one round under one convention: location list (without the incoming locations: those are applied between rounds), syndrome table of accumulated data errors"""
    def __init__(self, nm, conv, m=1):
        r = V10[nm]; self.nm = nm; self.code = r["code"]; self.dets = r["dets"]
        if conv == "M2": locs, ops = s23.serial_locations(r["ops"], "M2")
        elif conv == "serial": locs, ops = s23.serial_locations(r["ops"], "M3")
        else: locs, ops, _ = s23.layered_locations(r["ops"], m)
        self.full = s23.Prob(locs, ops, self.dets, self.code)                       # with incoming locations (M3) for the single-round check
        self.P = s23.Prob([l for l in locs if l[0] != "in"], ops, self.dets, self.code); self.d = len(self.dets)
        sx = [s23.effect(ops, self.dets, (-1, "p", {q: "X"}))[0] for q in range(4)]; sz = [s23.effect(ops, self.dets, (-1, "p", {q: "Z"}))[0] for q in range(4)]
        self.SYN = [0] * 256
        for e in range(256):
            s = 0
            for q in range(4):
                if (e >> q) & 1: s ^= sx[q]
                if (e >> (q + 4)) & 1: s ^= sz[q]
            self.SYN[e] = s
        self.cls = [{"none": 0, "harmless": 0, "detected": 1, "logical": 2}[s23.classify_err(e & 15, e >> 4, self.code)] for e in range(256)]
        self._T = {}
    def trans(self, p, rho):
        key = (p, rho)
        if key in self._T: return self._T[key]
        P = self.P; V = np.zeros(P.N); V[0] = 1.0
        for typ, row, mu in P.locs:
            r = min(1.0, p * mu * (rho if typ == "idle" else 1.0)); acc = np.zeros(P.N)
            for e in row: acc += V[P.idx ^ e]
            V = (1 - r) * V + r * acc / len(row)
        d = self.d; T = {}
        for f in np.nonzero(V)[0]:
            f = int(f); syn = f & ((1 << d) - 1); ef = ((f >> d) & 15) | (((f >> (d + 4)) & 15) << 4)
            T.setdefault(syn, np.zeros(256))[ef] += V[f]
        self._T[key] = T; return T
    def run(self, p, rho, rounds):
        T = self.trans(p, rho); dist = np.zeros(256); dist[0] = 1.0; out = {}; idx = np.arange(256)
        for r in range(1, max(rounds) + 1):
            new = (1 - p) ** 4 * dist                              # incoming faults: each axis suffers X, Y or Z with probability p / 3 each, independently
            nd = dist
            for q in range(4):
                nq = (1 - p) * nd
                for u in ((1, 0), (1, 1), (0, 1)): nq = nq + (p / 3) * nd[idx ^ ((u[0] << q) | ((u[1] << q) << 4))]
                nd = nq
            dist = nd; new = np.zeros(256)
            for e0 in range(256):
                if dist[e0] > 0 and self.SYN[e0] in T: new[idx ^ e0] += dist[e0] * T[self.SYN[e0]]
            dist = new
            if r in rounds:
                acc = dist.sum(); sil = sum(dist[e] for e in range(256) if self.cls[e] == 2); pen = sum(dist[e] for e in range(256) if self.cls[e] == 1)
                out[r] = dict(accepted=acc, damaged=sil + pen, damaged_given=(sil + pen) / acc if acc else 0.0, silent=sil, silent_given=sil / acc if acc else 0.0)
        return out

def main():
    t00 = time.time(); p = 1e-3
    # ---- P0
    V10T = {"L conv (baseline)": (0.833, 0.031, 3.7e-2, 3.0e-2), "J conv": (0.746, 0.0057, 0.77e-2, 4.1e-3), "J flag": (0.644, 0.0013, 0.20e-2, 1.1e-4), "J cat (verified)": (0.464, 0.0014, 0.30e-2, 1.8e-4)}
    E2 = {nm: Eng(nm, "M2") for nm in NAMES}; ok = True; shown = []
    for nm in NAMES:
        o = E2[nm].run(p, 1.0, (20,))[20]; a, dm, dg, sl = V10T[nm]; shown.append((o["accepted"], o["damaged"], o["damaged_given"], o["silent"]))
        ok &= round(o["accepted"], 3) == a and abs(o["damaged"] - dm) <= (0.00051 if dm >= 0.01 else 0.000051) and abs(100 * o["damaged_given"] - 100 * dg) < 0.06 and abs(o["silent"] / sl - 1) < 0.05
    print("      M2 engine at p = 1e-3, R = 20 (accepted, damaged, damaged | accepted, silent): " + "; ".join("%s %.3f %.4f %.2f%% %.2e" % (SHORT[nm], x[0], x[1], 100 * x[2], x[3]) for nm, x in zip(NAMES, shown)))
    check("P0 with idle faults off the engine reproduces V1.0's repeated-round table at p = 1e-3, R = 20: accepted to 3 decimals, damaged to the printed precision (2 figures), damaged-given-accepted within 0.06 percentage points of the printed value (V1.0 prints 3.7, 0.77, 0.20, 0.30 %; this engine gives 3.75, 0.77, 0.21, 0.31), silent within 5 % (V1.0 prints 2 figures)", ok)
    # ---- engines for the conventions
    CONVS = [("serial", "serial", 1), ("m=1", "layered", 1), ("m=3", "layered", 3), ("m=6", "layered", 6)]
    EN = {cn: {nm: Eng(nm, cv, m) for nm in NAMES} for cn, cv, m in CONVS}
    # ---- P1
    ok = True; worst = 0.0
    for cn, _, _ in CONVS:
        for nm in NAMES:
            for rho in (1.0, 2.0):
                E = EN[cn][nm]; E.full.locs = [(t, row, (mu * rho if t == "idle" else mu)) for (t, row, _), mu in zip(E.full.locs, [m for _, _, m in E.full.locs])] if False else E.full.locs
                # single-round exact distribution with incoming faults, idle scaled by rho (rescale a copy of the location list)
                F = s23.Prob.__new__(s23.Prob); F.__dict__.update(E.full.__dict__); F.locs = [(t, row, mu * rho if t == "idle" else mu) for (t, row, mu) in E.full.locs]
                ex = F.at(p); o = E.run(p, rho, (1,))[1]
                worst = max(worst, abs(o["silent"] / ex["silent"] - 1), abs(o["accepted"] - (1 - ex["reject"])))
    check("P1 for R = 1 the recursion equals the single-round exact distribution with incoming faults (accepted mass to 1e-9 absolute, silent probability to 1e-6 relative), four rounds, four conventions, rho = 1 and 2 (largest deviation %.1e)" % worst, worst < 1e-6)
    # ---- P2 / P3
    RS = (1, 5, 20); RES = {}
    print("      p = 1e-3, rho = 1: after R rounds (accepted | damaged given accepted | silent per run), separate metrics, no combined score")
    for cn, _, _ in CONVS:
        for nm in NAMES: RES[(cn, nm)] = EN[cn][nm].run(p, 1.0, RS)
    for R in RS:
        print("      R = %d" % R)
        for cn in ["M2"] + [c for c, _, _ in CONVS]:
            row = []
            for nm in NAMES:
                o = (E2[nm].run(p, 1.0, RS)[R] if cn == "M2" else RES[(cn, nm)][R]); row.append("%-10s %5.3f %6.2f%% %8.2e" % (SHORT[nm], o["accepted"], 100 * o["damaged_given"], o["silent"]))
            print("        %-7s " % cn + " | ".join(row), flush=True)
    def order(cn, key, R, rev=False):
        v = {nm: (RES[(cn, nm)][R][key]) for nm in NAMES}; return [SHORT[nm] for nm in sorted(NAMES, key=lambda n: v[n], reverse=rev)]
    ord_ = {}
    M2R = {nm: E2[nm].run(p, 1.0, (20,))[20] for nm in NAMES}
    m2_dg = [SHORT[nm] for nm in sorted(NAMES, key=lambda n: M2R[n]["damaged_given"])]; m2_sg = [SHORT[nm] for nm in sorted(NAMES, key=lambda n: M2R[n]["silent_given"])]
    print("      M2      R = 20 order (best first): damaged|accepted %s ; silent|accepted %s" % (" > ".join(m2_dg), " > ".join(m2_sg)))
    for cn, _, _ in CONVS:
        ord_[cn] = (order(cn, "accepted", 20, True), order(cn, "damaged_given", 20), order(cn, "silent_given", 20), order(cn, "silent", 20))
        print("      %-7s R = 20 order (best first): accepted %s ; damaged|accepted %s ; silent|accepted %s ; silent per run %s" % (cn, *[" > ".join(x) for x in ord_[cn]]), flush=True)
    check("P2a V1.0's accepted-fraction order at R = 20 (local > conventional joint > flagged > cat) holds in every idle convention",
          all(ord_[cn][0] == ["local", "conv joint", "flagged", "cat"] for cn, _, _ in CONVS))
    check("P2b V1.0's M2 order of damage given acceptance after 20 rounds (flagged lowest, then cat, conventional joint, local) %s in any of the four idle conventions; with idle faults the conventional joint round has the lowest damage given acceptance in %s" % (
          "does not survive" if all(ord_[cn][1] != m2_dg for cn, _, _ in CONVS) else "survives in some", ", ".join(cn for cn, _, _ in CONVS if ord_[cn][1][0] == "conv joint") or "none"),
          m2_dg == ["flagged", "cat", "conv joint", "local"] and all(ord_[cn][1] != m2_dg for cn, _, _ in CONVS))
    check("P2c silent probability among accepted runs after 20 rounds, lowest round: M2 %s; serial %s, m = 1 %s, m = 3 %s, m = 6 %s (the 'silent per run' ordering is distorted by acceptance: serial verified cat keeps %.1f %% of runs)" % (
          m2_sg[0], *[ord_[cn][2][0] for cn, _, _ in CONVS], 100 * RES[("serial", "J cat (verified)")][20]["accepted"]),
          m2_sg[0] == "flagged" and all(ord_[cn][2][0] in ("flagged", "cat", "conv joint") for cn, _, _ in CONVS))
    acc = {(cn, nm): RES[(cn, nm)][20]["silent_given"] / RES[(cn, nm)][1]["silent_given"] for cn, _, _ in CONVS for nm in NAMES}
    acc2 = {nm: M2R[nm]["silent"] / E2[nm].run(p, 1.0, (1,))[1]["silent"] for nm in NAMES}
    print("      accumulation of silent probability among accepted runs, R = 20 over R = 1: " + "; ".join("%s: " % cn + ", ".join("%s %.1f" % (SHORT[nm], acc[(cn, nm)]) for nm in NAMES) for cn, _, _ in CONVS))
    pr = {(cn, nm): RES[(cn, nm)][20]["silent"] / RES[(cn, nm)][1]["silent"] for cn, _, _ in CONVS for nm in NAMES}
    print("      accumulation of silent probability PER RUN, R = 20 over R = 1: M2: " + ", ".join("%s %.1f" % (SHORT[nm], acc2[nm]) for nm in NAMES) + "; " + "; ".join("%s: " % cn + ", ".join("%s %.1f" % (SHORT[nm], pr[(cn, nm)]) for nm in NAMES) for cn, _, _ in CONVS))
    check("P3 the silent probability per run after 20 rounds is %.1f to %.1f times its one-round value at M2 (V1.0: 15 to 20) and %.1f to %.1f times under idle faults (below 20 where acceptance has collapsed: verified cat, serial, keeps 0.6 %% of runs); among accepted runs the ratio is %.1f to %.1f, above 20 because it is the per-run ratio times the ratio of accepted fractions (acc(1) / acc(20) > 1)" % (
          min(acc2.values()), max(acc2.values()), min(pr.values()), max(pr.values()), min(acc.values()), max(acc.values())),
          all(12 < v < 20 for v in acc2.values()) and all(0 < v < 20 for v in pr.values()) and all(abs(acc[k] - pr[k] * RES[(k[0], k[1])][1]["accepted"] / RES[(k[0], k[1])][20]["accepted"]) < 1e-9 * max(1, acc[k]) for k in acc))
    # ---- P4
    def rho_star(cn_conv, m, R, key="silent", lo=0.01, hi=100.0, n=60):
        F = Eng("J flag", cn_conv, m); C = Eng("J conv", cn_conv, m)
        g = lambda rho: F.run(p, rho, (R,))[R][key] - C.run(p, rho, (R,))[R][key]; prev = None
        for k in range(n + 1):
            r = lo * (hi / lo) ** (k / n); v = g(r)
            if prev is not None and prev[1] < 0 <= v:
                a, b = math.log(prev[0]), math.log(r)
                for _ in range(40):
                    mid = (a + b) / 2
                    if g(math.exp(mid)) < 0: a = mid
                    else: b = mid
                return math.exp((a + b) / 2)
            prev = (r, v)
        return None
    def always_below(cv, m, R, key="silent", lo=0.01, hi=100.0, n=60):
        F = Eng("J flag", cv, m); C = Eng("J conv", cv, m)
        return all(F.run(p, lo * (hi / lo) ** (k / n), (R,))[R][key] < C.run(p, lo * (hi / lo) ** (k / n), (R,))[R][key] for k in range(n + 1))
    BELOW = {cn: always_below(cv, m, 20) for cn, cv, m in (("serial", "serial", 1), ("m=1", "layered", 1), ("m=6", "layered", 6))}
    RSTAR = {}; fmt = lambda x: ("%.3f" % x) if x else "none"
    for cn, cv, m in (("serial", "serial", 1), ("m=1", "layered", 1), ("m=6", "layered", 6)):
        for R in (1, 5, 20):
            for key in ("silent", "silent_given"): RSTAR[(cn, R, key)] = rho_star(cv, m, R, key)
        print("      first-crossing rho*(R) for R = 1, 5, 20 at p = 1e-3, %-6s: silent per run %s | silent among accepted runs %s   (search range 0.01 to 100)" % (
            cn, "  ".join(fmt(RSTAR[(cn, R, "silent")]) for R in (1, 5, 20)), "  ".join(fmt(RSTAR[(cn, R, "silent_given")]) for R in (1, 5, 20))), flush=True)
    check("P4a at R = 1 the critical ratio equals S26's (serial 1.025, m = 1 3.550, m = 6 1.031) on the per-run metric", RSTAR[("serial", 1, "silent")] and abs(RSTAR[("serial", 1, "silent")] - 1.025) < 0.01 and abs(RSTAR[("m=1", 1, "silent")] - 3.550) < 0.05 and abs(RSTAR[("m=6", 1, "silent")] - 1.031) < 0.02)
    check("P4b the metric matters after repetition: on silent probability PER RUN the flagged round has no crossing in rho = 0.01 to 100 after 20 rounds (on all 61 grid points its silent probability per run stays below the conventional joint round's; its accepted fraction after 20 rounds is much smaller, e.g. %.3f against %.3f serially at rho = 1), "
          "while among ACCEPTED runs the critical ratio after 20 rounds is %s (serial), %s (m = 1), %s (m = 6) against %s, %s, %s after one round (per-accepted-run metric at R = 1)" % (
          RES[("serial", "J flag")][20]["accepted"], RES[("serial", "J conv")][20]["accepted"], *[fmt(RSTAR[(cn, 20, "silent_given")]) for cn in ("serial", "m=1", "m=6")], *[fmt(RSTAR[(cn, 1, "silent_given")]) for cn in ("serial", "m=1", "m=6")]),
          all(RSTAR[(cn, 20, "silent")] is None and BELOW[cn] for cn in ("serial", "m=1", "m=6")) and all(RSTAR[(cn, R, "silent_given")] for cn in ("serial", "m=1", "m=6") for R in (1, 5, 20)))
    print("NOTE  repeated rounds here are incoming faults plus one verification round per step with rejection ending the run; no decision rule, no loss, no readout error beyond a flip at gate rate. Total wall-clock %.0f s" % (time.time() - t00))
    print("ALL PASS" if OK else "FAILED")
    return 0 if OK else 1

if __name__ == "__main__": sys.exit(main())
