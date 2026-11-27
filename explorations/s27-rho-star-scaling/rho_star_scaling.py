#!/usr/bin/env python3
"""S27: can S26's approximate 1/sqrt(p) scaling of the critical idle-to-gate ratio be derived, and where does it hold?

S26 found numerically that the idle-to-gate ratio rho* below which the flagged joint round beats the conventional joint round falls roughly as 1/sqrt(p).  With the idle fault probability written
rho x p, the silent probability of a round is  c1 p + (A + B rho + C rho^2) p^2 + O(p^3),  where c1 is the first-order silent coefficient and A, B, C are the pair counts of V0.9's second-order
coefficient split by how many of the two locations are idle (none, one, both; incoming-fault locations count as non-idle).  The flagged round is better to second order exactly when
        (c1_conv - c1_flag) / p  >  dA + dB rho + dC rho^2           (d = flagged minus conventional),
so everything follows from six exact rational numbers and one first-order difference T = c1_conv - c1_flag = 4/15.  This script derives the consequences and tests them against the exact
distributions of S23 / S26.

Claims
  Q0  A, B, C are exact rationals for each round and convention; A + B rho + C rho^2 equals S26's weighted coefficient; no idle location carries a single silent fault, so c1 does not depend on rho.     DERIVED
  Q1  Closed form:  rho*(p) = [ -dB + sqrt( dB^2 + 4 dC (T/p - dA) ) ] / (2 dC)  (the positive root; second-order theory), and p*(rho) = T / (dA + dB rho + dC rho^2).  At rho = 1 serially,
      p* = 9.92e-4, the 'analytic crossover estimate' of S18 (the exact crossing is 1.0496e-3).                                                                                                                    DERIVED
  Q2  The local scaling exponent n = -d ln rho* / d ln p equals (dC rho*^2 + dB rho* + dA) / (2 dC rho*^2 + dB rho*), so that n - 1/2 = (dB rho* + 2 dA) / (2 (2 dC rho*^2 + dB rho*)): it tends
      to 1/2 where the idle-idle term dominates (rho* >> dB / dC) and is below 1 always, so 1/sqrt(p) is the large-rho* asymptote of a quadratic, not a law.  dA, dB, dC, dB / dC and n are tabulated.   DERIVED
  Q3  Validity against the exact distributions (NUMERICAL OBSERVATION): the closed form lies below the exact rho* in every case tested and is within 5 % and 10 % of it for p up to the values tabulated;
      beyond them terms of third order matter (not derived).                                                                                                                                                    NUMERICAL
Not claimed: that the scaling holds for other pairs of rounds, other codes or non-Pauli noise; a bound on the third-order term; any platform value.  Author-side; not an independent reproduction.  Requires numpy.  Run with python3 -I.
"""
import importlib.util, math, os, sys, time
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
def _load(name, rel):
    sp = importlib.util.spec_from_file_location(name, os.path.join(ROOT, *rel)); m = importlib.util.module_from_spec(sp)
    sys.modules[name] = m; sp.loader.exec_module(m); return m
s23 = _load("s23", ["explorations", "s23-flag-design-search", "flag_design_search.py"])
s26 = _load("s26", ["explorations", "s26-idle-to-gate-ratio", "idle_to_gate_ratio.py"])

OK = True
def check(name, ok):
    global OK
    OK = OK and bool(ok); print(("PASS  " if ok else "FAIL  ") + name, flush=True)

CONV = [("serial", "serial", 1), ("m=1", "layered", 1), ("m=3", "layered", 3), ("m=6", "layered", 6)]
def abc(R):
    """exact (A, B, C) of a Round: weighted second-order silent coefficient = A + B rho + C rho^2, where a pair of locations counts mu_i mu_j (mu = the layer-duration multiplier of an idle location, 1 for all
    other locations) times the number of silent two-fault combinations, in units of 1/450"""
    A = B = C = Fr(0)
    for i, j, cnt in R.pairs:
        w = Fr(cnt * R.base[i] * R.base[j], 450); k = R.idle[i] + R.idle[j]
        if k == 0: A += w
        elif k == 1: B += w
        else: C += w
    return A, B, C

def root(dA, dB, dC, T, p):
    disc = dB * dB + 4 * dC * (T / p - dA)
    return (-dB + math.sqrt(disc)) / (2 * dC)

def main():
    t00 = time.time(); RD = {cn: {nm: s26.Round(nm, cv, m) for nm in ("J conv", "J flag")} for cn, cv, m in CONV}
    ABC = {cn: {nm: abc(RD[cn][nm]) for nm in RD[cn]} for cn, _, _ in CONV}
    # ---- Q0
    ok = True
    for cn, _, _ in CONV:
        for nm in RD[cn]:
            R = RD[cn][nm]; A, B, C = ABC[cn][nm]
            if cn in ("serial", "m=1"):
                sp = R.coef.split(); ok &= A + B + C == R.coef.c2 and C == sum(v for (t1, t2), v in sp.items() if t1 == t2 == "idle") and A == sum(v for (t1, t2), v in sp.items() if "idle" not in (t1, t2))
            for rho in (0.0, 0.5, 1.0, 2.0, 3.0): ok &= abs(float(A) + float(B) * rho + float(C) * rho * rho - R.c2(rho)) < 1e-9
    check("Q0a with all multipliers 1 (serial, m = 1) A + B + C equals S23's second-order silent coefficient exactly (as fractions) and A, C equal the sums of S23's split by location-type pair; in all four conventions A + B rho + C rho^2 equals S26's weighted coefficient at rho = 0, 0.5, 1, 2, 3, for both rounds", ok)
    idle_silent = any(a[3] == "silent" for cn, _, _ in CONV for nm in RD[cn] for t, row in RD[cn][nm].coef.per if t == "idle" for a in row)
    check("Q0b no single fault at an idle location is silent in either round and any convention, so the first-order silent coefficient (4/15 and 0) does not depend on rho", (not idle_silent) and all(
        RD[cn]["J conv"].coef.c1["silent"] == Fr(4, 15) and RD[cn]["J flag"].coef.c1["silent"] == 0 for cn, _, _ in CONV))
    T = Fr(4, 15); D = {}
    print("      exact second-order polynomial  c2 = A + B rho + C rho^2   (fractions in units of 1/450; decimals shown)")
    for cn, _, _ in CONV:
        for nm in ("J conv", "J flag"):
            A, B, C = ABC[cn][nm]; print("      %-7s %-7s A = %s (%.3f)   B = %s (%.3f)   C = %s (%.3f)" % (cn, nm, A, float(A), B, float(B), C, float(C)))
        a = [ABC[cn]["J flag"][k] - ABC[cn]["J conv"][k] for k in range(3)]; D[cn] = a
        print("      %-7s difference (flagged - conventional): dA = %s (%.3f)  dB = %s (%.3f)  dC = %s (%.3f);  dB / dC = %.3f" % (cn, a[0], float(a[0]), a[1], float(a[1]), a[2], float(a[2]), float(a[1] / a[2])), flush=True)
    check("Q0c in every convention dA < 0 < dB and dC > 0 (at rho = 0 the flagged round has the smaller second-order coefficient; the idle terms are what the flagged round loses on)", all(D[cn][0] < 0 < D[cn][1] and D[cn][2] > 0 for cn, _, _ in CONV))
    # ---- Q1
    PS = [1e-4, 3e-4, 1e-3, 3e-3, 1e-2]; ok = True; EXA = {}
    for cn, _, _ in CONV:
        dA, dB, dC = (float(x) for x in D[cn])
        for p in PS: ok &= abs(root(dA, dB, dC, 4 / 15, p) - s26.est_rho(RD[cn]["J flag"], RD[cn]["J conv"], p)) < 1e-6
    check("Q1a the closed-form root equals the numerical root of S26's first-order estimate to 1e-6 for four conventions and five values of p", ok)
    dA, dB, dC = (float(x) for x in D["serial"]); pstar = (4 / 15) / (dA + dB + dC)
    check("Q1b p*(rho = 1) = (4/15) / (dA + dB + dC) = %.4e serially: S18's 'analytic crossover estimate 9.92e-4'; the exact crossing (S19, S23) is 1.0496e-3, %.1f %% higher" % (pstar, 100 * (1.0496e-3 / pstar - 1)),
          abs(pstar - 9.92e-4) < 0.006e-4)
    # ---- Q2
    print("      local scaling exponent n = -d ln rho* / d ln p  (1/2 would be exact 1/sqrt(p)), from the closed form at its own rho*, for p = 1e-4, 3e-4, 1e-3, 3e-3, 1e-2:")
    NN = {}
    for cn, _, _ in CONV:
        dA, dB, dC = (float(x) for x in D[cn]); row = []
        for p in PS:
            r = root(dA, dB, dC, 4 / 15, p); n = (dC * r * r + dB * r + dA) / (2 * dC * r * r + dB * r); NN[(cn, p)] = n; row.append("%.3f" % n)
        print("      %-7s " % cn + "  ".join(row) + "     asymptote sqrt(T / (p dC)) / closed form at p = 1e-4: %.3f" % (math.sqrt((4 / 15) / (1e-4 * dC)) / root(dA, dB, dC, 4 / 15, 1e-4)), flush=True)
    ok = True
    for cn, _, _ in CONV:
        dA, dB, dC = (float(x) for x in D[cn])
        for p in (3e-4, 1e-3, 3e-3):
            h = 1e-4; fd = -(math.log(root(dA, dB, dC, 4 / 15, p * (1 + h))) - math.log(root(dA, dB, dC, 4 / 15, p * (1 - h)))) / (math.log(1 + h) - math.log(1 - h))
            r = root(dA, dB, dC, 4 / 15, p); ok &= abs(fd - (dC * r * r + dB * r + dA) / (2 * dC * r * r + dB * r)) < 1e-6
    check("Q2a the exponent formula equals a finite-difference derivative of the closed form (three p, four conventions)", ok)
    check("Q2b the exponent lies between 1/2 and 1 for every case (the idle-idle term alone would give 1/2, the one-idle term alone 1); serially it is %.2f at p = 1e-4 and %.2f at 1e-2, and under layered counting with m = 1 %.2f and %.2f: "
          "'approximately 1/sqrt(p)' is accurate to the extent that rho* >> dB / dC" % (NN[("serial", 1e-4)], NN[("serial", 1e-2)], NN[("m=1", 1e-4)], NN[("m=1", 1e-2)]),
          all(0.5 < v < 1.0 for v in NN.values()) and NN[("serial", 1e-4)] < NN[("serial", 1e-2)] and NN[("m=1", 1e-4)] < NN[("m=1", 1e-2)])
    ok = True
    for cn, _, _ in CONV:
        dA, dB, dC = (float(x) for x in D[cn])
        for p in PS:
            r = root(dA, dB, dC, 4 / 15, p); ok &= abs((dC * r * r + dB * r + dA) / (2 * dC * r * r + dB * r) - 0.5 - (dB * r + 2 * dA) / (2 * (2 * dC * r * r + dB * r))) < 1e-12
    check("Q2d the identity n - 1/2 = (dB rho* + 2 dA) / (2 (2 dC rho*^2 + dB rho*)) holds (so n > 1/2 exactly when rho* > 2 |dA| / dB: %s for the four conventions)" % ", ".join("%.3f" % (2 * abs(float(D[cn][0])) / float(D[cn][1])) for cn, _, _ in CONV), ok)
    ok = True
    for cn, _, _ in CONV:
        dA, dB, dC = (float(x) for x in D[cn]); lim = (-dB + math.sqrt(dB * dB - 4 * dC * dA)) / (2 * dC)
        ok &= lim > 0 and all(root(dA, dB, dC, 4 / 15, p) > lim for p in PS)
    check("Q2c as p grows the closed form tends not to 0 but to the positive root rho0 of dA + dB rho + dC rho^2 = 0 (second-order theory: a flagged round with idle faults rarer than rho0 x gate faults is better at every p); rho0 = %s" % (
        ", ".join("%.3f (%s)" % ((-float(D[cn][1]) + math.sqrt(float(D[cn][1]) ** 2 - 4 * float(D[cn][2]) * float(D[cn][0]))) / (2 * float(D[cn][2])), cn) for cn, _, _ in CONV)), ok)
    # ---- Q3
    print("      validity: closed-form rho* against the exact rho* (S26's exact engine), by p; largest p of the tested grid within 5 % / 10 %:")
    GRID = [1e-4, 2e-4, 5e-4, 1e-3, 2e-3, 3e-3, 5e-3, 1e-2, 2e-2]; below = True; lim = {}
    for cn, _, _ in CONV:
        dA, dB, dC = (float(x) for x in D[cn]); errs = []
        for p in GRID:
            ex = s26.first_rho(RD[cn]["J flag"], RD[cn]["J conv"], p, hi=1e3); es = root(dA, dB, dC, 4 / 15, p)
            errs.append(es / ex - 1 if ex else float("nan"))
            if ex: below &= es <= ex * (1 + 1e-9)
        l5 = max([p for p, e in zip(GRID, errs) if abs(e) < 0.05 and all(abs(x) < 0.05 for x, q in zip(errs, GRID) if q <= p)] or [0]); l10 = max([p for p, e in zip(GRID, errs) if abs(e) < 0.10 and all(abs(x) < 0.10 for x, q in zip(errs, GRID) if q <= p)] or [0])
        lim[cn] = (l5, l10); print("      %-7s " % cn + "  ".join(("%+5.1f%%" % (100 * e)) if e == e else "  n/a " for e in errs) + "     within 5 %% up to p = %.0e, within 10 %% up to p = %.0e" % (l5, l10), flush=True)
    print("              p =     " + "  ".join("%-6.0e" % p for p in GRID))
    check("Q3a the closed form is at or below the exact rho* at every tested p and convention (the neglected terms raise the conventional round's silent probability more than the flagged round's)", below)
    check("Q3b the closed form is within 5 %% of the exact rho* for p up to %.0e (serial), %.0e (m = 1), %.0e (m = 3), %.0e (m = 6) and within 10 %% up to %.0e, %.0e, %.0e, %.0e; the range is shorter under layered counting with m = 1, where rho* is large and a few idle locations carry the rate" % (
        lim["serial"][0], lim["m=1"][0], lim["m=3"][0], lim["m=6"][0], lim["serial"][1], lim["m=1"][1], lim["m=3"][1], lim["m=6"][1]), lim["serial"][0] >= 1e-3 and lim["m=1"][0] < lim["serial"][0] and all(v[1] >= 1e-3 for v in lim.values()))
    ex_n = {}
    for cn, _, _ in CONV:
        dA, dB, dC = (float(x) for x in D[cn]); r = {p: s26.first_rho(RD[cn]["J flag"], RD[cn]["J conv"], p, hi=1e3) for p in (1e-4, 1e-3, 1e-2)}; c = {p: root(dA, dB, dC, 4 / 15, p) for p in (1e-4, 1e-3, 1e-2)}
        ex_n[cn] = (math.log(r[1e-4] / r[1e-3]) / math.log(10), math.log(r[1e-3] / r[1e-2]) / math.log(10), math.log(c[1e-4] / c[1e-3]) / math.log(10), math.log(c[1e-3] / c[1e-2]) / math.log(10))
    print("      decade exponents  exact (1e-4 to 1e-3, 1e-3 to 1e-2) | closed form (same):  " + "   ".join("%s: %.3f %.3f | %.3f %.3f" % (cn, *ex_n[cn]) for cn, _, _ in CONV))
    check("Q3c over the decade 1e-4 to 1e-3 the exact exponent is within 0.02 of the closed form's and within 0.02 of 1/2 in every convention (%.3f to %.3f); over 1e-3 to 1e-2 the exact exponent is below 1/2 (%.3f to %.3f) while the closed form says above (%.3f to %.3f): the "
          "second-order theory over-states the steepening at p of order 1e-2" % (min(v[0] for v in ex_n.values()), max(v[0] for v in ex_n.values()), min(v[1] for v in ex_n.values()), max(v[1] for v in ex_n.values()), min(v[3] for v in ex_n.values()), max(v[3] for v in ex_n.values())),
          all(abs(v[0] - v[2]) < 0.02 and abs(v[0] - 0.5) < 0.02 for v in ex_n.values()) and all(v[1] < 0.5 < v[3] for v in ex_n.values()))
    print("NOTE  the 1/sqrt(p) law is an intermediate asymptote of a quadratic, derived here from six exact fractions; its range of validity is set by (i) rho* >> dB / dC (n -> 1/2) and (ii) the neglect of third-order terms (numerical, above). Total wall-clock %.0f s" % (time.time() - t00))
    print("ALL PASS" if OK else "FAILED")
    return 0 if OK else 1

if __name__ == "__main__": sys.exit(main())
