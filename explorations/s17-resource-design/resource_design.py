#!/usr/bin/env python3
"""S17: can a better-verified offline resource bring the teleportation round's second-order silent coefficient down?  (a small, exact family search)

S15 found that the S14 teleportation round has a second-order silent coefficient of at least 19.68 even with a perfect resource and 43 to 54 with the resources tried (T0..T3), against
2.32 (J flag) and 9.90 (J cat).  Is the resource part (23 to 34 of it) intrinsic to a distance-2 resource, or does a better-verified resource remove it?  Here more resource designs are
evaluated, and the second-order coefficient is split by the stage (Bell pairs, pair checks, projection of the blocks, online round) of the two faults of a pair.

Method.  S15's state-vector runs give, for every single fault of a circuit, its syndrome (the detector parities) and its Pauli error on the output block modulo the stabilizers; the
effects of two faults at distinct locations compose by XOR (a Pauli-frame statement for a Clifford circuit with Pauli faults), and a pair is silent iff its syndrome is 0 and the composite
error commutes with ZZZZ and XXXX without being a stabilizer.  This is exactly V0.9's pair definition, evaluated in seconds instead of minutes; U0 validates it against S15's state-vector
pair enumeration (recorded totals) and against fresh state-vector runs of sampled pairs.

Designs (all with S15's online round; resource of two [[4,2,2]] blocks A and N holding the encoded Bell pair; checks flagged where the weight is 4)
  T1  Bell pairs, flagged checks of A                   T3  flagged checks of A and N
  T4  Bell pairs, each pair verified by its own ZZ and XX checks, then flagged checks of A
  T5  as T4, then flagged checks of A and N             T6  as T5 with the block checks done twice
  (T0 and T2 are the unflagged versions of T1 and T3, kept to validate the method against S15)
Claims
  U0  The method reproduces S15's recorded totals (ideal 19.680, T1 43.200, T3 50.960, T0 45.058, T2 54.009) to 3 decimals and agrees with state-vector classification on sampled pairs.  DERIVED
  U1  The table of first-order and second-order coefficients and the stage split for T1, T3, T4, T5, T6.                                                                           DERIVED
  U2  No design here brings the total below the online floor 492/25 (the resource only adds).                                                                         DERIVED
  U3  Even with perfect readout (r = 0) every design here keeps a gate-gate term above V0.9's whole J flag coefficient (2.320, which bounds J flag's c2(r) for every r <= 1),
      so the readout ratio of S16 cannot rescue these resources against J flag.                                                                                            DERIVED
Not claimed: that no better resource exists (the family is small and chosen by me); anything about cost in photons or time; any combination with the heralded metric.  Author-side;
not an independent reproduction.  Requires numpy.  Run with python3 -I.
"""
import importlib.util, itertools, os, random, re, sys, time
from fractions import Fraction as Fr
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
def _load(name, rel):
    sp = importlib.util.spec_from_file_location(name, os.path.join(ROOT, *rel)); m = importlib.util.module_from_spec(sp)
    sys.modules[name] = m; sp.loader.exec_module(m); return m
s15 = _load("s15", ["explorations", "s15-teleportation-silent-faults", "teleport_silent.py"])
A, N, DATA, ANC, FLAG = s15.A, s15.N, s15.DATA, s15.ANC, s15.FLAG
par = s15.par

OK = True
def check(name, ok):
    global OK
    OK = OK and bool(ok); print(("PASS  " if ok else "FAIL  ") + name, flush=True)

def build17(code, on="A", flagged=False, pairverify=False, reps=1):
    """S15's circuit family, extended with per-pair checks and repeated block checks; ancilla qubits are re-used after each measurement; records the stage of every operation.
    With pairverify=False and reps=1 it produces exactly S15's operation list (U0b checks the totals)."""
    assert code == "J"
    ops = []; rec = [0]; stage = []
    def add(st, *t): ops.append(t); stage.append(st)
    def bit(): rec[0] += 1; return rec[0] - 1
    a, f = ANC, FLAG
    for i in range(4):
        add("bell", "P+", A[i]); add("bell", "P0", N[i]); add("bell", "CNOT", A[i], N[i])
    if pairverify:
        for i in range(4):
            add("pairchk", "P0", a); add("pairchk", "CNOT", A[i], a); add("pairchk", "CNOT", N[i], a); add("pairchk", "MZ", a, bit())
            add("pairchk", "P+", a); add("pairchk", "CNOT", a, A[i]); add("pairchk", "CNOT", a, N[i]); add("pairchk", "MX", a, bit())
    for _ in range(reps):
        for blk in ([A] + ([N] if on == "AN" else [])):
            for typ in "ZX":
                qs = list(blk)
                if not flagged:
                    if typ == "Z":
                        add("proj", "P0", a)
                        for q in qs: add("proj", "CNOT", q, a)
                        add("proj", "MZ", a, bit())
                    else:
                        add("proj", "P+", a)
                        for q in qs: add("proj", "CNOT", a, q)
                        add("proj", "MX", a, bit())
                elif typ == "Z":
                    add("proj", "P0", a); add("proj", "P+", f); add("proj", "CNOT", qs[0], a); add("proj", "CNOT", f, a)
                    for q in qs[1:-1]: add("proj", "CNOT", q, a)
                    add("proj", "CNOT", f, a); add("proj", "CNOT", qs[-1], a); add("proj", "MZ", a, bit()); add("proj", "MX", f, bit())
                else:
                    add("proj", "P+", a); add("proj", "P0", f); add("proj", "CNOT", a, qs[0]); add("proj", "CNOT", a, f)
                    for q in qs[1:-1]: add("proj", "CNOT", a, q)
                    add("proj", "CNOT", a, f); add("proj", "CNOT", a, qs[-1]); add("proj", "MX", a, bit()); add("proj", "MZ", f, bit())
    prep_end = len(ops); md = []; ma = []
    for i in range(4):
        add("online", "CNOT", DATA[i], A[i]); b1 = bit(); add("online", "MX", DATA[i], b1); b2 = bit(); add("online", "MZ", A[i], b2); md.append(b1); ma.append(b2)
    return ops, dict(prep_end=prep_end, md=md, ma=ma, nrec=rec[0], stage=stage)
def null_space_fast(recs, nrec):
    """a basis of all parities that vanish on every fault-free record, by Gauss-Jordan elimination over GF(2) (S15's brute-force version is fine for 16 record bits, not for 32)"""
    piv = {}
    for r in set(recs):
        for c, pr in piv.items():
            if r >> c & 1: r ^= pr
        if r:
            c = r.bit_length() - 1
            for c2 in list(piv):
                if piv[c2] >> c & 1: piv[c2] ^= r
            piv[c] = r
    gens = []
    for fcol in (c for c in range(nrec) if c not in piv):
        m = 1 << fcol
        for c, pr in piv.items():
            if pr >> fcol & 1: m |= 1 << c
        gens.append(m)
    return gens
s15.build = build17            # S15's Round() looks `build` and `null_space` up in its module globals when it is constructed
s15.null_space = null_space_fast

def effects(R, branches=(0, 5, 77)):
    """per location: list of (syndrome as an int, canonical output error (x, z)) for each of its faults; consistent over the branches"""
    paulis = list(itertools.product("IXYZ", repeat=4)); PS = np.zeros((256, 16), dtype=complex)
    for k, pa in enumerate(paulis):
        w = R.psi
        for q, c in enumerate(pa):
            if c != "I": w = R.sim4.one(w, s15.PAULI[c], q)
        PS[k] = w
    stab = [(0, 0), (15, 0), (0, 15), (15, 15)]
    canon = lambda x, z: min((x ^ sx, z ^ sz) for sx, sz in stab)
    xz_of = []
    for pa in paulis:
        x = z = 0
        for q, c in enumerate(pa):
            if c in "XY": x |= 1 << q
            if c in "ZY": z |= 1 << q
        xz_of.append((x, z))
    out = []; consistent = True
    for loc in R.locs:
        row = []
        for fl in loc:
            es = []
            for b in branches:
                n, rec = R.state([fl], b); ov = np.abs(PS.conj() @ n); k = int(np.argmax(ov)); assert ov[k] > 1 - 1e-9, "output must be a Pauli-error state"
                syn = 0
                for j, m in enumerate(R.dets): syn |= par(rec & m) << j
                es.append((syn, canon(*xz_of[k])))
            consistent &= len(set(es)) == 1; row.append(es[0])
        out.append(row)
    return out, consistent, canon

def cat_of(syn, xz, canon):
    if syn: return "det"
    x, z = xz
    if par(x) or par(z): return "pass_damaged"
    return "pass_clean" if xz in {canon(*s) for s in [(0, 0), (15, 0), (0, 15), (15, 15)]} else "silent"

def analyse(R):
    eff, consistent, canon = effects(R)
    stage = R.meta.get("stage"); L = len(R.locs)
    st = (lambda i: stage[R.locs[i][0][0]]) if stage else (lambda i: "res" if R.locs[i][0][0] < R.meta["prep_end"] else "online")
    kind = lambda i: "m" if R.ops[R.locs[i][0][0]][0] in ("MZ", "MX") else "g"
    first = {"silent": Fr(0), "pass_damaged": Fr(0), "det": Fr(0), "pass_clean": Fr(0)}
    single = []
    for i in range(L):
        row = []
        for e in eff[i]:
            c = cat_of(e[0], e[1], canon); first[c] += Fr(1, len(eff[i])); row.append(c)
        single.append(row)
    tot = Fr(0); bystage = {}; bykind = {"gg": Fr(0), "gm": Fr(0), "mm": Fr(0)}
    STABC = {canon(*sg) for sg in [(0, 0), (15, 0), (0, 15), (15, 15)]}; PAR = [bin(v).count("1") & 1 for v in range(16)]
    for a in range(L):
        for b in range(a + 1, L):
            cnt = 0
            for ia, (sa, xa) in enumerate(eff[a]):
                if single[a][ia] == "silent": continue
                for ib, (sb, xb) in enumerate(eff[b]):
                    if single[b][ib] == "silent": continue
                    if sa == sb:
                        x = xa[0] ^ xb[0]; z = xa[1] ^ xb[1]
                        if not (PAR[x] or PAR[z]) and canon(x, z) not in STABC: cnt += 1
            if cnt:
                w = Fr(cnt, len(eff[a]) * len(eff[b])); tot += w
                key = "-".join(sorted((st(a), st(b)))); bystage[key] = bystage.get(key, Fr(0)) + w
                kk = "".join(sorted(kind(a) + kind(b))); bykind[kk] += w
    return dict(first=first, second=tot, stage=bystage, kinds=bykind, consistent=consistent, eff=eff, canon=canon, single=single)

def main():
    t00 = time.time(); variants = [
        ("ideal", dict(ideal=True)), ("T0", dict(on="A")), ("T1", dict(on="A", flagged=True)), ("T2", dict(on="AN")), ("T3", dict(on="AN", flagged=True)),
        ("T4", dict(on="A", flagged=True, pairverify=True)), ("T5", dict(on="AN", flagged=True, pairverify=True)), ("T6", dict(on="AN", flagged=True, pairverify=True, reps=2))]
    res = {}; Rs = {}
    # S15's recorded totals (3 decimals), read from its execution record
    rec = open(os.path.join(ROOT, "explorations", "s15-teleportation-silent-faults", "execution-record.txt"), encoding="utf-8").read()
    ref = {k: float(v) for k, v in re.findall(r"^\s+(T\d|L)\s+second-order silent ([\d.]+)", rec, re.M)}; ref["ideal"] = 19.68
    for nm, kw in variants:
        t0 = time.time(); R = s15.Round("J", **kw); Rs[nm] = R; res[nm] = analyse(R)
        fo = res[nm]["first"]
        print("      %-6s locs %3d | first order: silent %.3f damaged %.3f detected %.3f | second order %.3f | by kind gg %.3f gm %.3f mm %.3f | %s  [%.0f s]" % (
            nm, len(R.locs), float(fo["silent"]), float(fo["pass_damaged"]), float(fo["det"]), float(res[nm]["second"]), float(res[nm]["kinds"]["gg"]), float(res[nm]["kinds"]["gm"]), float(res[nm]["kinds"]["mm"]),
            "consistent over 3 branches" if res[nm]["consistent"] else "NOT consistent", time.time() - t0), flush=True)
    check("U0a single-fault effects are identical on 3 measurement branches in every circuit (so Pauli-frame composition applies)", all(res[nm]["consistent"] for nm in res))
    check("U0b the method reproduces S15's recorded second-order totals to 3 decimals: " + ", ".join("%s %.3f" % (k, ref[k]) for k in ("ideal", "T0", "T1", "T2", "T3")),
          all(abs(float(res[k]["second"]) - ref[k]) < 5.1e-4 for k in ("ideal", "T0", "T1", "T2", "T3")))
    # sampled pairs against the state-vector classifier
    rr = random.Random(21); bad = 0; nb = 0
    for nm in ("T0", "T4", "T5"):
        R = Rs[nm]; r = res[nm]; eff = r["eff"]; canon = r["canon"]
        flat = [(i, j) for i, row in enumerate(R.locs) for j in range(len(row)) if r["single"][i][j] != "silent"]
        for _ in range(400):
            (i1, j1), (i2, j2) = rr.sample(flat, 2)
            if i1 == i2: continue
            sa, xa = eff[i1][j1]; sb, xb = eff[i2][j2]; pred = cat_of(sa ^ sb, canon(xa[0] ^ xb[0], xa[1] ^ xb[1]), canon)
            got = R.classify([R.locs[i1][j1], R.locs[i2][j2]]); got = "det" if got in ("false_reject", "caught_damage") else got
            nb += 1; bad += (pred != got)
    check("U0c the composed category equals the state-vector category on %d sampled pairs (T0, T4, T5)" % nb, bad == 0)
    print("== second-order silent coefficient by stage pair (resource variants; online-online is 492/25 = 19.68 throughout) ==")
    for nm in ("T1", "T3", "T4", "T5", "T6"):
        print("      %-3s total %.2f   %s" % (nm, float(res[nm]["second"]), "   ".join("%s %.2f" % (k, float(v)) for k, v in sorted(res[nm]["stage"].items()))))
    print("== first order: pass-damaged and silent weights ==")
    for nm in ("T1", "T3", "T4", "T5", "T6"):
        print("      %-3s silent %.3f   pass-damaged %.3f   detected %.3f   locations %d" % (nm, float(res[nm]["first"]["silent"]), float(res[nm]["first"]["pass_damaged"]), float(res[nm]["first"]["det"]), len(Rs[nm].locs)))
    best = min(("T1", "T3", "T4", "T5", "T6"), key=lambda k: res[k]["second"])
    check("U1  first order of T3, T5 and T6 equals J flag's (silent 0, pass-damaged 1.867); T1 and T4 keep unchecked block N: damaged weights %.3f and %.3f" % (float(res["T1"]["first"]["pass_damaged"]), float(res["T4"]["first"]["pass_damaged"])),
          all(res[k]["first"]["silent"] == 0 for k in ("T1", "T3", "T4", "T5", "T6")) and all(abs(float(res[k]["first"]["pass_damaged"]) - 1.867) < 5.1e-4 for k in ("T3", "T5", "T6")))
    print("      lowest second-order total in this family: %s = %.2f (online floor 19.68; J flag 2.32, J cat 9.90, local 1.24)" % (best, float(res[best]["second"])))
    check("U2  no design in this family brings the second-order coefficient below the online floor 492/25 = 19.68 (the lowest is %s with %.2f)" % (best, float(res[best]["second"])),
          min(res[k]["second"] for k in ("T1", "T3", "T4", "T5", "T6")) > Fr(492, 25))
    gg = {k: res[k]["kinds"]["gg"] for k in ("T1", "T3", "T4", "T5", "T6")}
    check("U3  with perfect readout (r = 0) the gate-gate terms are %s, all above 2.320 (V0.9's whole J flag coefficient, an upper bound on J flag's c2(r) for r <= 1)" % ", ".join("%s %.2f" % (k, float(v)) for k, v in gg.items()),
          all(v > Fr(2320, 1000) for v in gg.values()))
    print("NOTE  A family of five resource designs of my choosing; it does not show no better resource exists.  Per-pair verification removes the Bell-stage pair terms (10.88 to 0) but adds its own")
    print("      and leaves the projection-stage terms (online-proj 5.89 in every design: a projection fault paired with an online fault); repeating the block checks makes it worse.")
    print("      Total wall-clock %.0f s" % (time.time() - t00))
    print("ALL PASS" if OK else "FAILED")
    return 0 if OK else 1

if __name__ == "__main__": sys.exit(main())
