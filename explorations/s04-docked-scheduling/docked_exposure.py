#!/usr/bin/env python3
"""S04: how much of each V1.0 round can a classical scheduler move off the active path?

Annotation A01 split the V1.0 two-qubit gates into data-touching and ancilla-only gates and noted that offline
preparation could change the ancilla-only ones.  This analysis checks that statement gate by gate, using the
circuits V1.0 itself defines (read-only), and then works out the consequences under the V1.0 abort model.

Definitions (ours, stated so they can be checked):
  contaminated qubit  = a data qubit, or an ancilla qubit that has interacted (directly or through earlier
                        ancilla-ancilla gates) with a data qubit
  pre-interaction gate = a two-qubit gate whose two qubits are both uncontaminated when it runs; it can in
                        principle be run before the data is present (offline, verified, buffered)
  interleaved gate     = an ancilla-ancilla gate with at least one contaminated qubit: it is part of the
                        data-coupled protocol and cannot be prepared ahead without changing the circuit

Claims
  D1  Per round, the counts of data-touching / pre-interaction / interleaved gates.   DERIVED (circuit analysis)
  D2  Offline preparation helps only designs whose ancilla-only gates are all pre-interaction (verified cat);
      the flagged round's four ancilla-only gates are all interleaved.                  DERIVED
  D3  Active-path completion probability s^(data-touching + interleaved) at s = 0.75, 0.5, 0.25 under the abort
      rule, compared with V1.0's all-on-the-active-path value.                          DERIVED on ASSUMED s
  D4  The scheduling does not remove the cost: factory attempts per completed round and the number of parallel
      preparation units needed for a buffered resource to be ready with probability 0.99.   DERIVED on ASSUMED s
Author-side; not independent reproduction.  Standard library only.
"""
import importlib.util, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
spec = importlib.util.spec_from_file_location("v10_rounds", os.path.join(ROOT, "explorations", "common", "v10_rounds.py"))
v10 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v10)

OK = True
def check(name, ok):
    global OK
    OK = OK and bool(ok)
    print(("PASS  " if ok else "FAIL  ") + name)

def classify(ops):
    cont = set(range(4)); data_t = pre = inter = 0; detail = []
    for i, op in enumerate(ops):
        if op[0] in ("CNOT", "CZ"):
            a, b = op[1], op[2]
            ca, cb = a in cont, b in cont
            if a < 4 or b < 4:
                data_t += 1; cont |= {a, b}; detail.append((i, "data"))
            elif not ca and not cb:
                pre += 1; detail.append((i, "pre"))
            else:
                inter += 1; cont |= {a, b}; detail.append((i, "interleaved"))
    return data_t, pre, inter, detail

def main():
    R = v10.load()
    names = ["L conv (baseline)", "J conv", "J ZZZZ only (partial)", "J flag", "J cat (verified)"]
    print("== D1 gate classes per round (V1.0 circuits, K = 1) ==")
    print("      %-24s %7s %14s %12s %12s" % ("round", "total", "data-touching", "pre-interaction", "interleaved"))
    tab = {}
    for nm in names:
        d, p, i, det = classify(R[nm]["ops"]); tab[nm] = (d, p, i, det)
        print("      %-24s %7d %14d %12d %12d" % (nm, d + p + i, d, p, i))
    check("D1a data-touching counts match annotation A01 / V1.0 (4, 8, 4, 8, 8)", [tab[n][0] for n in names] == [4, 8, 4, 8, 8])
    check("D1b totals match V1.0's K = 1 column (4, 8, 4, 12, 18)", [sum(tab[n][:3]) for n in names] == [4, 8, 4, 12, 18])
    check("D2a flagged round: all 4 ancilla-only gates are interleaved, none can be prepared offline", tab["J flag"][1] == 0 and tab["J flag"][2] == 4)
    check("D2b verified-cat round: all 10 ancilla-only gates are pre-interaction (offline-preparable)", tab["J cat (verified)"][1] == 10 and tab["J cat (verified)"][2] == 0)
    check("D2c local, joint conventional and ZZZZ-only rounds have no ancilla-only gates", all(tab[n][1] == tab[n][2] == 0 for n in ("L conv (baseline)", "J conv", "J ZZZZ only (partial)")))
    # show where the flagged round's ancilla-only gates sit
    det = tab["J flag"][3]
    seq = "".join({"data": "D", "pre": "p", "interleaved": "i"}[k] for _, k in det)
    print("      flagged round, gate order (D data-touching, i interleaved ancilla-only):  " + seq)
    seq2 = "".join({"data": "D", "pre": "p", "interleaved": "i"}[k] for _, k in tab["J cat (verified)"][3])
    print("      verified-cat round, gate order (p pre-interaction, D data-touching):     " + seq2)

    print("== D3 active-path completion probability (abort rule: any failure on the active path aborts) ==")
    S = [0.75, 0.5, 0.25]
    print("      %-24s exponent: all-on-path / after offline preparation" % "round")
    for nm in names:
        d, p, i, _ = tab[nm]
        cells = []
        for s in S:
            cells.append("s=%g: %.3g -> %.3g (x%.3g)" % (s, s ** (d + p + i), s ** (d + i), s ** (d + i) / s ** (d + p + i)))
        print("      %-24s %d / %d              %s" % (nm, d + p + i, d + i, "   ".join(cells)))
    check("D3a under offline preparation the verified-cat round has the same active-path completion probability as conventional joint (exponent 8)", tab["J cat (verified)"][0] + tab["J cat (verified)"][2] == tab["J conv"][0] + tab["J conv"][2] == 8)
    check("D3b the flagged round gains nothing from offline preparation (exponent stays 12)", tab["J flag"][0] + tab["J flag"][1] + tab["J flag"][2] == tab["J flag"][0] + tab["J flag"][2] == 12)
    check("D3c at s = 0.75 the cat round's active-path completion rises from 0.0056 to 0.100 (about 18 times)", abs(0.75 ** 18 - 0.0056) < 5e-5 and abs(0.75 ** 8 - 0.1001) < 5e-4 and abs(0.75 ** 8 / 0.75 ** 18 - 0.75 ** -10) < 1e-9)

    print("== D4 the cost moves, it does not vanish (verified cat) ==")
    print("      one verified cat resource needs 5 pre-interaction gates if the 4-qubit cat chain plus its verifier succeed (3 chain + 2 verify); a round consumes one Z cat and one X cat")
    print("      %-8s %-26s %-30s %-32s %s" % ("s", "P(resource prepared)=s^5", "factory gate attempts per resource", "units for P(ready)>=0.99 per window", "active attempts per completed round"))
    for s in (0.75, 0.5, 0.25):
        ps = s ** 5
        att = (1 - ps) / (ps * (1 - s)) if s < 1 else 5       # expected gate attempts to get one prepared resource when a failure restarts it (same formula as V1.0)
        units = math.ceil(math.log(0.01) / math.log(1 - ps)) if ps < 1 else 1
        act = (1 - s ** 8) / (s ** 8 * (1 - s))
        print("      %-8g %-26.4g %-30.4g %-32d %.4g" % (s, ps, att, units, act))
    def units_for(ps, target=0.99):
        u = math.ceil(math.log(1 - target) / math.log(1 - ps))
        return u
    ok4 = True
    for sv in (0.75, 0.5, 0.25):
        ps = sv ** 5; u = units_for(ps)
        ok4 &= (1 - (1 - ps) ** u >= 0.99) and (1 - (1 - ps) ** (u - 1) < 0.99)
    check("D4a the unit counts are the least M with 1 - (1 - s^5)^M >= 0.99 (verified by evaluating M and M - 1)", ok4)
    check("D4b the factory work scales as s^-5 per resource: 32 times more attempts at s = 0.5 than at s = 1 (1/ps = 32)", abs(1 / 0.5 ** 5 - 32) < 1e-12)
    print("      note: one round needs two cats, and the verifier itself can reject; the unit counts above are therefore lower bounds for the same availability on both cats (roughly double).")
    print("      This is classical probability over assumed s; it says nothing about whether such a factory, its buffering loss or its synchronisation exist (open problems 6 and 10).")
    print("== D5 where the saving comes from: retry granularity, not offline-ness ==")
    print("      expected TOTAL gate attempts per completed round, abort-and-restart rule; DS = prepare each cat until it succeeds (restarting only its 5 gates), then run the 8 active gates (two cats consumed per round attempt)")
    print("      %-6s %-26s %-26s %s" % ("s", "all on one restart loop (18)", "DS: factory + active", "ratio"))
    def A(n, sv): return (1 - sv ** n) / (sv ** n * (1 - sv))
    ok5 = True
    for sv in (0.75, 0.5, 0.25):
        allp = A(18, sv); rounds_ = 1 / sv ** 8; ds = rounds_ * 2 * A(5, sv) + A(8, sv)
        ok5 &= ds < allp
        print("      %-6g %-26.5g %-26.5g %.3gx" % (sv, allp, ds, allp / ds))
    check("D5a V1.0's 524,286 attempts at s = 0.5 for the verified cat is reproduced by the formula (1 - s^n) / (s^n (1 - s))", abs(A(18, 0.5) - 524286) < 1e-6)
    check("D5b the modular (DS) total is below the single-restart-loop total at s = 0.75, 0.5, 0.25", ok5)
    print("      Caution on reading D5: a protocol that prepares and verifies the cat BEFORE coupling it to data and retries only that preparation gets the same gate-attempt total with no scheduler at all, provided the data photon can wait.")
    print("      The scheduling question is therefore the waiting time of the data photon: without a ready resource the data waits about A(5,s) gate times (%.0f at s = 0.5); with a buffered resource it waits ~0. The value of that depends on a storage-loss rate per gate time, which no checkpoint models." % A(5, 0.5))
    print("ALL PASS" if OK else "SOME CHECKS FAILED")
    return 0 if OK else 1

if __name__ == "__main__":
    sys.exit(main())
