#!/usr/bin/env python3
"""S25: does the teleportation round's place in the ranking survive idle faults (V0.9's model M3)?

S15 to S20 compared S14's teleportation round with V1.0's four rounds under model M2 and said in plain words that idle and waiting faults were not covered.  Here M3 is extended to the teleportation
round (PROPOSED extension; V0.9 defined M3 only for the V1.0 rounds): incoming Paulis on the four data axes, and one idle location (three Paulis) for every live qubit not touched by an operation,
counted either serially (after every operation, V0.9's convention) or per parallel layer (S23's PROPOSED convention, with a layer that holds a measurement lasting m gate times).  The data qubits
join at the online round, so only the resource qubits (and, in the full circuits, the resource's own check ancilla and flag) idle while the resource is prepared; the resource may also wait w
layers before the data arrive.  A multiplier rho on every idle location of the resource phase and the hold (rho = 1: the same rate p as everywhere else) says how much better than a gate the
resource's memory has to be.  The single-fault effects come from a Pauli-frame engine (S23's propagation, plus the teleportation's correction rule) that is checked against S15's state-vector
classification; S23's exact coefficient and convolution code then gives second-order coefficients and exact silent probabilities.

Claims
  U0  The frame engine equals S15's explicit state-vector classification on every single fault of the M2 location sets of the ideal-resource round, T0 and T3 (892 faults) and on sampled faults
      of the M3 location sets (incoming, idle) under both conventions.                                                                                                                    DERIVED
  U1  The engine reproduces S15's and S20's M2 second-order coefficients: ideal 492/25 = 19.68, T0 45.06 (first-order silent 4/15), T3 50.960.                                        DERIVED
  U2  Ideal resource, no waiting: the teleportation round's silent probability at p = 1e-3 in M3 is above the flagged and conventional joint rounds under V0.9's serial convention, and below all
      four V1.0 rounds under the layered convention for m = 1, 3 and 6 (M2: above flagged and cat, S20); under the serial convention it is also below the local round and the verified cat.                                                                                   DERIVED on PROPOSED
  U3  If the resource waits w layers at the ordinary idle rate, the round is above the flagged round from w = 2, 4 and 7 layers (m = 1, 3, 6).                                           DERIVED on PROPOSED
  U4  S14's resource as written (T0) and with flagged checks on both blocks (T3), with the resource idling at the ordinary rate (rho = 1): T3 is 35, 25 and 17 times above the flagged round,
      T0 is 3.5, 4.6 and 5.4 times above the conventional joint round.  Almost all of T3's silent probability comes from idle faults in the resource phase.                                   DERIVED on PROPOSED
  U5  T3 equals the flagged round at a resource idle multiplier rho* of about 0.002 (m = 1), 0.06 (m = 3) and 0.12 (m = 6): the resource's memory has to be that much better than a gate.    DERIVED on PROPOSED
Not claimed: that T3 is the best resource design (S17 tried five designs under M2 only); the heralded metric; any timing, memory or hold time of a platform (m, w and rho are free parameters);
the teleportation round's rejection or yield; faults inside the corrections.  Author-side; not an independent reproduction.  Requires numpy.  Run with python3 -I.
"""
import copy, importlib.util, math, os, random, sys, time
from fractions import Fraction as Fr
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
def _load(name, rel):
    sp = importlib.util.spec_from_file_location(name, os.path.join(ROOT, *rel)); m = importlib.util.module_from_spec(sp)
    sys.modules[name] = m; sp.loader.exec_module(m); return m
s23 = _load("s23", ["explorations", "s23-flag-design-search", "flag_design_search.py"])
s15 = _load("s15", ["explorations", "s15-teleportation-silent-faults", "teleport_silent.py"])

OK = True
def check(name, ok):
    global OK
    OK = OK and bool(ok); print(("PASS  " if ok else "FAIL  ") + name, flush=True)

def tele_eff(meta):
    """single-fault effect on the teleportation circuits: (syndrome over the detector masks, X mask, Z mask of the OUTPUT block N after the protocol's corrections X^(A outcome) Z^(data outcome))"""
    def eff(ops, dets, f):
        i, kind, pd = f; x = z = 0
        if kind == "m": rec = 1 << ops[i][2]
        else:
            for q, c in pd.items():
                if c in "XY": x |= 1 << q
                if c in "ZY": z |= 1 << q
            x, z, rec = s23.propagate(ops, i + 1, x, z, 0)
        syn = sum((bin(rec & m).count("1") & 1) << j for j, m in enumerate(dets)); xN = (x >> 8) & 15; zN = (z >> 8) & 15
        for k in range(4):
            if (rec >> meta["ma"][k]) & 1: xN ^= 1 << k
            if (rec >> meta["md"][k]) & 1: zN ^= 1 << k
        return syn, xN, zN
    return eff

def tele_locations(R, conv, w=0, m=1, rho=1.0, m2_only=False):
    """locations of a teleportation round.  Gate, preparation and readout faults (M2) of the faulty part (the whole circuit, or only the online round for the ideal resource); then incoming faults on the
    data axes and idle faults.  The resource part (operations before prep_end) and the online part are scheduled separately with a barrier between them; w empty hold layers sit between them.
    conv 'serial': every operation is its own layer.  'layered': ASAP layers (S23's schedule).  A layer holding a measurement gives its idle locations a rate multiplier m; idle locations in the
    resource phase and the hold get rho as well.  Returns (locations, operation list in layer order)"""
    ops = R.ops; pe = R.meta["prep_end"]; ideal = R.ideal; res = ops[:pe]; onl = ops[pe:]
    if conv == "serial": lr = list(range(len(res))); lo = list(range(len(onl)))
    else: lr = s23.schedule(res); lo = s23.schedule(onl)
    ordr = sorted(range(len(res)), key=lambda i: (lr[i], i)); ordo = sorted(range(len(onl)), key=lambda i: (lo[i], i))
    nops = [res[i] for i in ordr] + [onl[i] for i in ordo]; nres = max(lr) + 1
    layer = [lr[i] for i in ordr] + [nres + w + lo[i] for i in ordo]; locs = []
    for i, op in enumerate(nops):
        if ideal and i < pe: continue
        ty, fl = s23.gate_locations(nops, i, op); locs.append((ty, fl, 1))
    if m2_only: return locs, nops
    for q in range(4): locs.append(("in", [(pe - 1, "p", {q: c}) for c in "XYZ"], 1))
    alive = set(range(4, 12)) if ideal else set(); bylayer = {}
    for i, l in enumerate(layer): bylayer.setdefault(l, []).append(i)
    for k in range(max(layer) + 1):
        idx = bylayer.get(k, [])
        if idx: at = idx[-1]; touched = {q for i in idx for q in s23.qs(nops[i])}; mult = m if any(nops[i][0] in ("MZ", "MX") for i in idx) else 1
        else: at = pe - 1; touched = set(); mult = 1
        if k == nres + w: alive |= set(range(4))
        if (not ideal) or k >= nres:
            for q in sorted(alive):
                if q not in touched: locs.append(("idle", [(at, "p", {q: c}) for c in "XYZ"], mult * (rho if k < nres + w else 1.0)))
        for i in idx:
            if nops[i][0] in ("P0", "P+"): alive.add(nops[i][1])
            elif nops[i][0] in ("MZ", "MX"): alive.discard(nops[i][1])
    return locs, nops

def main():
    t00 = time.time(); R10 = s23.v10.load(); rr = random.Random(20261127)
    RS = {"ideal": s15.Round("J", ideal=True), "T0": s15.Round("J", on="A"), "T3": s15.Round("J", on="AN", flagged=True)}
    EFF = {k: tele_eff(R.meta) for k, R in RS.items()}
    # ---- U0
    def compare(R, k, locs, nops, sample=None):
        R2 = copy.copy(R); R2.ops = nops; fl = [f for _, o, _ in locs for f in o]
        if sample: fl = rr.sample(fl, min(sample, len(fl)))
        bad = 0
        for f in fl:
            syn, x, z = EFF[k](nops, R.dets, f); bad += s23.cat(syn, x, z, "J") != R2.classify([f], 0)
        return len(fl), bad
    n0 = b0 = 0
    for k, R in RS.items():
        locs, nops = tele_locations(R, "serial", m2_only=True); n_, b_ = compare(R, k, locs, nops); n0 += n_; b_0 = b_; b0 += b_0
    check("U0 the frame engine equals S15's state-vector classification on every single fault of the M2 location sets of the ideal-resource round, T0 and T3: %d faults, %d differ" % (n0, b0), b0 == 0 and n0 == 892)
    n1 = b1 = 0
    for k in ("ideal", "T3"):
        for conv, w, m in (("serial", 0, 1), ("layered", 3, 3)):
            locs, nops = tele_locations(RS[k], conv, w, m); n_, b_ = compare(RS[k], k, locs, nops, 300); n1 += n_; b1 += b_
    check("U0 the same on %d sampled faults of the M3 location sets (incoming, idle, gate and readout) of the ideal and T3 rounds under both conventions (serial; layered with w = 3, m = 3): %d differ" % (n1, b1), b1 == 0)
    # ---- U1
    C2 = {}
    for k, R in RS.items():
        locs, nops = tele_locations(R, "serial", m2_only=True); C2[k] = s23.Coef(locs, nops, R.dets, "J", eff=EFF[k])
        print("      M2 %-6s locations %3d faults %3d | first-order silent %s damaged %.3f | second-order %s = %.3f" % (k, C2[k].nloc, C2[k].nfault, C2[k].c1["silent"], float(C2[k].c1["pass_damaged"]), C2[k].c2, float(C2[k].c2)))
    check("U1 M2 second-order coefficients through the frame engine: ideal %s (S15: 492/25), T0 %.2f (S20: 45.06, first-order silent %s), T3 %.3f (S20: 50.960, first-order silent %s)" % (C2["ideal"].c2, float(C2["T0"].c2), C2["T0"].c1["silent"], float(C2["T3"].c2), C2["T3"].c1["silent"]),
          C2["ideal"].c2 == Fr(492, 25) and abs(float(C2["T0"].c2) - 45.06) < 5e-3 and C2["T0"].c1["silent"] == Fr(4, 15) and abs(float(C2["T3"].c2) - 50.960) < 5e-4 and C2["T3"].c1["silent"] == 0 and C2["ideal"].c1["silent"] == 0)
    # ---- reference rounds
    def ref_silent(nm, conv, m):
        r = R10[nm]
        if conv == "serial": locs, ops = s23.serial_locations(r["ops"], "M3")
        else: locs, ops, _ = s23.layered_locations(r["ops"], m)
        return s23.Prob(locs, ops, r["dets"], r["code"]).at(1e-3)["silent"]
    def tele_silent(k, conv, w=0, m=1, rho=1.0):
        locs, nops = tele_locations(RS[k], conv, w, m, rho); return s23.Prob(locs, nops, RS[k].dets, "J", eff=EFF[k]).at(1e-3)["silent"]
    V = ["L conv (baseline)", "J conv", "J flag", "J cat (verified)"]; CONV = [("serial", "serial", 1), ("m=1", "layered", 1), ("m=3", "layered", 3), ("m=6", "layered", 6)]
    REF = {cn: {nm: ref_silent(nm, cv, m) for nm in V} for cn, cv, m in CONV}
    # ---- U2
    ID = {cn: tele_silent("ideal", cv, 0, m) for cn, cv, m in CONV}
    cs = {cn: s23.Coef(*tele_locations(RS["ideal"], cv, 0, m), RS["ideal"].dets, "J", eff=EFF["ideal"]) for cn, cv, m in CONV[:2]}
    print("      M3, silent probability at p = 1e-3 (idle rate = gate rate; ideal resource, no waiting):")
    print("      %-30s " % "" + "  ".join("%-9s" % cn for cn, _, _ in CONV))
    for nm in V: print("      %-30s " % nm + "  ".join("%-9.2e" % REF[cn][nm] for cn, _, _ in CONV))
    print("      %-30s " % "teleportation, ideal resource" + "  ".join("%-9.2e" % ID[cn] for cn, _, _ in CONV))
    print("      ideal-resource second-order coefficient: serial %.3f, layered m = 1 %.3f (flagged: 426.942 and 78.276)" % (float(cs["serial"].c2), float(cs["m=1"].c2)))
    check("U2a serial: the ideal-resource teleportation round (%.2e) is above the flagged (%.2e) and conventional joint (%.2e) rounds and below the local round and the verified cat" % (ID["serial"], REF["serial"]["J flag"], REF["serial"]["J conv"]),
          ID["serial"] > REF["serial"]["J flag"] and ID["serial"] > REF["serial"]["J conv"] and ID["serial"] < REF["serial"]["L conv (baseline)"] and ID["serial"] < REF["serial"]["J cat (verified)"])
    fac = {cn: REF[cn]["J flag"] / ID[cn] for cn, _, _ in CONV[1:]}
    check("U2b layered (m = 1, 3, 6): the ideal-resource teleportation round is below all four V1.0 rounds, %.1f, %.1f and %.1f times below the flagged round" % (fac["m=1"], fac["m=3"], fac["m=6"]),
          all(ID[cn] < min(REF[cn].values()) for cn, _, _ in CONV[1:]))
    # ---- U3 hold
    first = {}
    for cn, cv, m in CONV[1:]:
        vals = [tele_silent("ideal", "layered", w, m) for w in range(0, 13)]; first[cn] = next(w for w, v in enumerate(vals) if v > REF[cn]["J flag"])
        assert all(a < b for a, b in zip(vals, vals[1:]))
    print("      hold layers w after which the ideal-resource round is above the flagged round: " + ", ".join("%s %d" % (cn, first[cn]) for cn in first))
    check("U3 the silent probability of the ideal-resource round grows with the hold time w (strictly, w = 0..12) and is above the flagged round's from w = %d, %d and %d layers for m = 1, 3, 6 (a resource that waits that long at the ordinary idle rate has no lead)" % (first["m=1"], first["m=3"], first["m=6"]),
          (first["m=1"], first["m=3"], first["m=6"]) == (2, 4, 7))
    # ---- U4 / U5
    T3 = {cn: tele_silent("T3", cv, 0, m, 1.0) for cn, cv, m in CONV}; T0 = {cn: tele_silent("T0", cv, 0, m, 1.0) for cn, cv, m in CONV}; T3z = {cn: tele_silent("T3", cv, 0, m, 0.0) for cn, cv, m in CONV}
    print("      resources of S14, silent probability at p = 1e-3, M3, no waiting:")
    print("      %-30s " % "" + "  ".join("%-9s" % cn for cn, _, _ in CONV))
    print("      %-30s " % "T0 (as written), rho = 1" + "  ".join("%-9.2e" % T0[cn] for cn, _, _ in CONV)); print("      %-30s " % "T3 (flagged checks), rho = 1" + "  ".join("%-9.2e" % T3[cn] for cn, _, _ in CONV)); print("      %-30s " % "T3, rho = 0 (idle-free resource)" + "  ".join("%-9.2e" % T3z[cn] for cn, _, _ in CONV))
    f3 = {cn: T3[cn] / REF[cn]["J flag"] for cn, _, _ in CONV[1:]}; f0 = {cn: T0[cn] / REF[cn]["J conv"] for cn, _, _ in CONV[1:]}; share = {cn: 1 - T3z[cn] / T3[cn] for cn, _, _ in CONV[1:]}
    check("U4 with the resource idling at the ordinary rate, T3 is %.1f, %.1f, %.1f times above the flagged round and T0 %.1f, %.1f, %.1f times above the conventional joint round (m = 1, 3, 6); %.1f %%, %.1f %%, %.1f %% of T3's silent probability is idle faults of the resource phase" % (
        f3["m=1"], f3["m=3"], f3["m=6"], f0["m=1"], f0["m=3"], f0["m=6"], 100 * share["m=1"], 100 * share["m=3"], 100 * share["m=6"]),
          all(f3[c] > 15 for c in f3) and all(f0[c] > 3 for c in f0) and all(share[c] > 0.9 for c in share))
    rstar = {}
    for cn, cv, m in CONV[1:]:
        f = lambda rho: tele_silent("T3", "layered", 0, m, rho) - REF[cn]["J flag"]; lo, hi = 0.0, 1.0; assert f(0.0) < 0 < f(1.0), (cn, f(0.0), f(1.0))
        for _ in range(40):
            mid = (lo + hi) / 2
            if f(mid) < 0: lo = mid
            else: hi = mid
        rstar[cn] = (lo + hi) / 2
    print("      resource idle multiplier rho* at which T3 equals the flagged round: " + ", ".join("%s %.4f" % (cn, rstar[cn]) for cn in rstar))
    check("U5 T3 (no waiting) equals the flagged round at rho* = %.4f (m = 1), %.4f (m = 3), %.4f (m = 6): the resource's idle fault rate has to be below these fractions of the gate fault rate; with an idle-free resource T3 is %.2e against %.2e (m = 1)" % (
        rstar["m=1"], rstar["m=3"], rstar["m=6"], T3z["m=1"], REF["m=1"]["J flag"]),
          0.001 < rstar["m=1"] < 0.004 and rstar["m=1"] < rstar["m=3"] < rstar["m=6"] < 0.2 and all(T3z[cn] < REF[cn]["J flag"] for cn in rstar))
    print("NOTE  M3 is extended to the teleportation round here by a PROPOSED rule (data qubits join at the online round; the resource qubits idle while it is prepared and held); the layered conventions, m, w and rho are free parameters, not hardware.  Total wall-clock %.0f s" % (time.time() - t00))
    print("ALL PASS" if OK else "FAILED")
    return 0 if OK else 1

if __name__ == "__main__": sys.exit(main())
