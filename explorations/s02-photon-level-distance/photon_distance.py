#!/usr/bin/env python3
"""S02: photon-level distance. How the number of axes hosted on one photon changes what a photon loss can do.

Model (all from the checkpoints): four data axes a1,b1,a2,b2 (qubits 0..3).  Local code checks ZZII, IIZZ;
joint code checks ZZZZ, XXXX ([[4,2,2]]).  A photon hosts one or more axes; losing a photon takes all of them.
  heralded loss   = the hosting photon's axes are erased at a known place;
  unheralded loss = its axes are replaced by a uniformly random Pauli (V1.0's 'ld' rule, identity included).
Standard facts used (checked numerically below, not assumed): a set E of qubits is erasure-correctable iff the
Knill-Laflamme condition P E' P = c(E') P holds for every Pauli E' supported on E.

Claims
  T1 Photon-level distance d_ph (fewest photons whose axes contain a nontrivial logical operator):
     the joint code hosted 2+2 has d_ph = 1 for EVERY pairing; hosted 1+1+1+1 it has d_ph = 2; the local
     code has d_ph = 1 in every hosting.                                                         DERIVED
  T2 Knill-Laflamme check by explicit projector: single-photon loss is correctable exactly when d_ph >= 2. DERIVED
  T3 For an unheralded loss with a random Pauli on the lost photon's axes, the share that is an undetected
     logical error: local pair 6/16, joint pair 3/16, joint single axis 0.                      DERIVED
  T4 Circuit level, exact: the first-order (linear in q) silent probability of unheralded data loss in each V1.0
     round, for 2+2 and 1+1+1+1 hosting; 1+1+1+1 has first-order coefficient exactly 0 for the joint rounds.
     The 2+2 values agree with the slope implied by V1.0's own table.                          DERIVED (own propagation)
  T5 Second-order coefficient and the loss rate q* below which 1+1+1+1 hosting beats 2+2.        DERIVED
Author-side; not independent reproduction.  Requires numpy (only for the T2 projector).
"""
import importlib.util, itertools, os, re, sys
from fractions import Fraction
from collections import defaultdict
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
spec = importlib.util.spec_from_file_location("v10_rounds", os.path.join(ROOT, "explorations", "common", "v10_rounds.py"))
v10 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v10)

OK = True
def check(name, ok):
    global OK
    OK = OK and bool(ok)
    print(("PASS  " if ok else "FAIL  ") + name)

# ---------------------------------------------------------------- Pauli algebra on 4 qubits, (x, z) bitmasks
def pc(n): return bin(n).count("1")
def commute(a, b): return (pc(a[0] & b[1]) + pc(a[1] & b[0])) % 2 == 0
def mul(a, b): return (a[0] ^ b[0], a[1] ^ b[1])
def support(a): return a[0] | a[1]
CHECKS = {"L": [(0, 0b0011), (0, 0b1100)], "J": [(0, 0b1111), (0b1111, 0)]}
def group(gens):
    g = {(0, 0)}
    for h in gens: g |= {mul(h, e) for e in g}
    return g
STAB = {k: group(v) for k, v in CHECKS.items()}
ALLP = [(x, z) for x in range(16) for z in range(16)]
def is_logical(k, p): return all(commute(p, g) for g in CHECKS[k]) and p not in STAB[k]
LOGICALS = {k: [p for p in ALLP if is_logical(k, p)] for k in "LJ"}

def set_partitions(items):
    if not items: yield []; return
    first, rest = items[0], items[1:]
    for part in set_partitions(rest):
        yield [[first]] + part
        for i in range(len(part)): yield part[:i] + [[first] + part[i]] + part[i + 1:]

def dph(k, hosting):
    best = 99
    for p in LOGICALS[k]:
        s = support(p); n = sum(1 for ph in hosting if any((s >> q) & 1 for q in ph))
        best = min(best, n)
    return best

def main():
    # ---------- T1
    print("== T1 photon-level distance over every hosting of the four axes ==")
    check("T1a code facts: 60 logical Paulis (256 - 64 - ... : commuting with both checks and not in the group) and weights", len(LOGICALS["J"]) == 60 and len(LOGICALS["L"]) == 60)
    allparts = list(set_partitions([0, 1, 2, 3])); res = {"L": {}, "J": {}}
    for k in "LJ":
        for part in allparts:
            key = tuple(sorted(tuple(sorted(b)) for b in part)); res[k][key] = dph(k, part)
    for k in "LJ":
        print("      code %s:" % ("local (ZZII,IIZZ)" if k == "L" else "joint ([[4,2,2]])"))
        for key, v in sorted(res[k].items(), key=lambda t: (len(t[0]), t[0])):
            print("        hosting %-34s d_ph = %d" % (key, v))
    pairs22 = [k for k in res["J"] if sorted(len(b) for b in k) == [2, 2]]
    check("T1b joint code, every 2+2 pairing (3 of them): d_ph = 1", len(pairs22) == 3 and all(res["J"][k] == 1 for k in pairs22))
    check("T1c joint code hosted 1+1+1+1: d_ph = 2", res["J"][((0,), (1,), (2,), (3,))] == 2)
    check("T1d local code: d_ph = 1 in all 15 hostings (a weight-1 Z is a logical operator)", all(v == 1 for v in res["L"].values()))
    nonone = [k for k, v in res["J"].items() if v >= 2]
    print("      joint-code hostings with d_ph >= 2:", nonone)
    check("T1f the only joint-code hosting with d_ph >= 2 is 1+1+1+1", nonone == [((0,), (1,), (2,), (3,))])

    # ---------- T2 explicit Knill-Laflamme check with the code projector
    print("== T2 Knill-Laflamme check with explicit projectors ==")
    I2 = np.eye(2, dtype=complex); X = np.array([[0, 1], [1, 0]], dtype=complex); Z = np.diag([1, -1]).astype(complex); Yp = 1j * X @ Z
    def pmat(p):
        m = np.array([[1]], dtype=complex)
        for q in range(4):  # qubit 0 is the most significant factor
            x, z = (p[0] >> q) & 1, (p[1] >> q) & 1
            m = np.kron(m, [[I2, Z], [X, Yp]][x][z] if False else (I2 if (x, z) == (0, 0) else X if (x, z) == (1, 0) else Z if (x, z) == (0, 1) else Yp))
        return m
    def projector(k):
        P = np.eye(16, dtype=complex)
        for g in CHECKS[k]: P = P @ (np.eye(16) + pmat(g)) / 2
        return P
    def kl_fails(k, qubits):
        P = projector(k); bad = 0
        sup = sum(1 << q for q in qubits)
        for p in ALLP:
            if support(p) & ~sup: continue
            M = P @ pmat(p) @ P
            c = np.trace(M) / np.trace(P)
            if not np.allclose(M, c * P, atol=1e-10): bad += 1
        return bad
    check("T2a projectors are rank 4 (two logical qubits)", all(abs(np.trace(projector(k)).real - 4) < 1e-9 for k in "LJ"))
    jp = kl_fails("J", [0, 1]); js = max(kl_fails("J", [q]) for q in range(4)); lp = kl_fails("L", [0, 1]); ls = kl_fails("L", [0])
    print("      Paulis violating KL on the erased set: joint pair %d, joint single axis %d, local pair %d, local single axis %d" % (jp, js, lp, ls))
    check("T2b joint code: loss of a 2-axis photon is NOT correctable (KL violated), loss of a 1-axis photon IS", jp > 0 and js == 0)
    check("T2c local code: not correctable even for one axis (KL violated by Z)", ls > 0 and lp > 0)
    check("T2d the KL verdict equals the d_ph >= 2 criterion in every case above", (jp > 0) == (res["J"][((0, 1), (2, 3))] == 1) and (js == 0) == (res["J"][((0,), (1,), (2,), (3,))] >= 2) and (ls > 0) == (res["L"][((0,), (1,), (2,), (3,))] == 1))

    # ---------- T3 random-Pauli share
    print("== T3 share of random-Pauli replacements that are undetected logical errors ==")
    def share(k, qubits):
        sup = sum(1 << q for q in qubits); P = [p for p in ALLP if not (support(p) & ~sup)]
        return Fraction(sum(1 for p in P if is_logical(k, p)), len(P))
    sL2, sJ2, sJ1, sL1 = share("L", [0, 1]), share("J", [0, 1]), share("J", [0]), share("L", [0])
    print("      local pair %s, joint pair %s, joint single %s, local single %s" % (sL2, sJ2, sJ1, sL1))
    check("T3 shares are 6/16, 3/16, 0 and 1/4 (weight-1 Z is silent in the local code)", (sL2, sJ2, sJ1, sL1) == (Fraction(6, 16), Fraction(3, 16), 0, Fraction(1, 4)))

    # ---------- T4/T5 circuit-level exact expansion in q
    print("== T4/T5 circuit-level expansion of unheralded data loss (own Pauli-frame propagation) ==")
    rounds = v10.load()
    def prop(ops, i0, frame):
        fr = {q: list(v) for q, v in frame.items()}; rec = 0
        for op in ops[i0:]:
            k = op[0]
            if k == "H":
                if op[1] in fr: fr[op[1]] = [fr[op[1]][1], fr[op[1]][0]]
            elif k == "CNOT":
                c, t = op[1], op[2]
                xc, zc = fr.get(c, [0, 0]); xt, zt = fr.get(t, [0, 0])
                xt ^= xc; zc ^= zt; fr[c] = [xc, zc]; fr[t] = [xt, zt]
            elif k == "CZ":
                a, b = op[1], op[2]
                xa, za = fr.get(a, [0, 0]); xb, zb = fr.get(b, [0, 0])
                za ^= xb; zb ^= xa; fr[a] = [xa, za]; fr[b] = [xb, zb]
            elif k == "MZ":
                x, z = fr.pop(op[1], [0, 0])
                if x: rec |= 1 << op[2]
            elif k == "MX":
                x, z = fr.pop(op[1], [0, 0])
                if z: rec |= 1 << op[2]
            else:   # P0 / P+ reset
                fr.pop(op[1], None)
        ex = sum((fr.get(q, [0, 0])[0] & 1) << q for q in range(4)); ez = sum((fr.get(q, [0, 0])[1] & 1) << q for q in range(4))
        return rec, (ex, ez)
    ONE = [(0, 0), (1, 0), (1, 1), (0, 1)]       # I, X, Y, Z as (x,z)
    def loss_locations(R, hosting):
        locs = []
        for i, op in enumerate(R["ops"]):
            if op[0] in ("CNOT", "CZ"):
                a, b = op[1], op[2]
                for q in (a, b):
                    if q < 4:
                        ph = next(h for h in hosting if q in h)
                        outs = []
                        for combo in itertools.product(ONE, repeat=len(ph)):
                            frame = {qq: list(c) for qq, c in zip(ph, combo) if c != (0, 0)}
                            outs.append(prop(R["ops"], i + 1, frame))
                        locs.append(outs)
        return locs
    def expand(R, hosting, order=8):
        code = R["code"]; dets = R["dets"]
        locs = loss_locations(R, hosting)
        def dv_of(rec): return sum(((pc(rec & m) & 1) << j) for j, m in enumerate(dets))
        dist = {(0, 0, 0): [Fraction(1)] + [Fraction(0)] * order}
        for outs in locs:
            n = len(outs); new = defaultdict(lambda: [Fraction(0)] * (order + 1))
            eff = [(dv_of(rec), fr[0], fr[1]) for rec, fr in outs]
            for key, poly in dist.items():
                t = new[key]
                for d in range(order + 1):
                    t[d] += poly[d] - (poly[d - 1] if d else 0)           # no loss: (1 - q)
                for dv, ex, ez in eff:
                    k2 = (key[0] ^ dv, key[1] ^ ex, key[2] ^ ez); t2 = new[k2]
                    for d in range(1, order + 1): t2[d] += poly[d - 1] / n
            dist = dict(new)
        sil = [Fraction(0)] * (order + 1); acc_dam = [Fraction(0)] * (order + 1); rej = [Fraction(0)] * (order + 1)
        for (dv, ex, ez), poly in dist.items():
            fr = (ex, ez)
            if dv:
                tgt = rej
            elif fr == (0, 0) or fr in STAB[code if code in "LJ" else "J"]:
                continue
            elif is_logical(code if code in "LJ" else "J", fr):
                tgt = sil
            else:
                tgt = acc_dam
            for d in range(order + 1): tgt[d] += poly[d]
        return sil, acc_dam, rej, len(locs)
    HOST = {"2+2": [(0, 1), (2, 3)], "1+1+1+1": [(0,), (1,), (2,), (3,)]}
    names = ["L conv (baseline)", "J conv", "J flag", "J cat (verified)"]
    table = {}
    print("      silent probability = c1 q + c2 q^2 + ...  (exact; only unheralded data-loss events, no gate faults)")
    print("      %-20s %-9s %5s  %12s %12s   %s" % ("round", "hosting", "locs", "c1", "c2", "q* = c1(2+2)/c2(1+1+1+1)"))
    for nm in names:
        for hn, h in HOST.items():
            sil, ad, rej, nloc = expand(rounds[nm], h)
            table[(nm, hn)] = (sil, nloc)
            print("      %-20s %-9s %5d  %12.6f %12.6f" % (nm, hn, nloc, float(sil[1]), float(sil[2])))
    for nm in names:
        c1_22 = table[(nm, "2+2")][0][1]; c2_41 = table[(nm, "1+1+1+1")][0][2]
        if nm.startswith("J"):
            print("      %-20s q* = %.4f  (below it, 1+1+1+1 hosting has the lower silent probability)" % (nm, float(c1_22 / c2_41)))
    check("T4a every round has 8 data-photon participations (4 local) under both hostings, as V1.0 states", all(table[(n, h)][1] == (4 if n.startswith("L") else 8) for n in names for h in HOST))
    check("T4b joint rounds, 1+1+1+1 hosting: first-order silent coefficient c1 is exactly 0", all(table[(n, "1+1+1+1")][0][1] == 0 for n in names if n.startswith("J")))
    check("T4c joint rounds, 2+2 hosting: c1 > 0 (linear in q)", all(table[(n, "2+2")][0][1] > 0 for n in names if n.startswith("J")))
    check("T4d local code: c1 > 0 under both hostings (weight-1 Z is logical)", all(table[("L conv (baseline)", h)][0][1] > 0 for h in HOST))
    check("T4e c1 never exceeds the crude bound (participations x share): local 4 x 6/16, joint 8 x 3/16", float(table[("L conv (baseline)", "2+2")][0][1]) <= 4 * 6 / 16 + 1e-12 and all(float(table[(n, "2+2")][0][1]) <= 8 * 3 / 16 + 1e-12 for n in names if n.startswith("J")))
    check("T4g the first-order silent coefficient is EXACTLY 1 for the local code under both hostings and for all three joint rounds under 2+2 hosting (exact rational arithmetic)",
          all(table[("L conv (baseline)", h)][0][1] == 1 for h in HOST) and all(table[(n, "2+2")][0][1] == 1 for n in names if n.startswith("J")))
    check("T4h the second-order silent coefficient of the three joint rounds under 1+1+1+1 hosting is EXACTLY 3", all(table[(n, "1+1+1+1")][0][2] == 3 for n in names if n.startswith("J")))
    # compare with V1.0's own numbers.  V1.0's unheralded-data-loss column is conditioned on NO heralded ancilla loss, so its
    # silent probability carries a factor (1-q)^(ancilla gate participations); the loss-free baseline is conditioned the same way.
    log = open(os.path.join(ROOT, "reproduction", "execution-logs", "v1.0.stdout.txt"), encoding="utf-8").read()
    wl = {}
    for m in re.finditer(r"^\s+(L conv \(baseline\)|J conv|J flag|J cat \(verified\))\s+silent at q=\[0.001, 0.01, 0.05\]: ([\d.e+-]+), ([\d.e+-]+), ([\d.e+-]+)", log, re.M):
        wl[m.group(1)] = float(m.group(2))
    base = {}
    for m in re.finditer(r"^\s+(L conv \(baseline\)|J conv|J flag|J cat \(verified\))\s+0\.001\s+[\d.]+\s+[\d.]+\s+\|\s+([\d.e+-]+)", log, re.M):
        base[m.group(1)] = float(m.group(2))
    def n_anc_part(R): return sum(1 for op in R["ops"] if op[0] in ("CNOT", "CZ") for q in op[1:3] if q >= 4)
    print("      comparison with V1.0's printed tables at q = 1e-3 (unheralded data loss, ancilla loss heralded, gate faults p = 1e-3):")
    print("      V1.0 slope = (silent_unheralded - silent_baseline) / (q (1-q)^n_anc);  mine = c1 + c2 q + ... (exact polynomial at q = 1e-3)")
    ok_all = True; worst = 0.0
    for nm in names:
        sil = table[(nm, "2+2")][0]; q = 1e-3
        mine_slope = sum(float(c) * q ** (d - 1) for d, c in enumerate(sil) if d >= 1)
        v10_slope = (wl[nm] - base[nm]) / (q * (1 - q) ** n_anc_part(rounds[nm]))
        rel = abs(mine_slope - v10_slope) / v10_slope; worst = max(worst, rel); ok_all &= rel < 0.03
        print("        %-20s V1.0 %.4f   mine %.4f   difference %.1f%%   (n_anc = %d)" % (nm, v10_slope, mine_slope, 100 * rel, n_anc_part(rounds[nm])))
    check("T4f my exact expansion agrees with the slope implied by V1.0's printed tables within 3%% for all four rounds (worst %.1f%%; the residual, which grows with the number of ancilla locations, is attributed to loss x gate-fault cross terms and was not computed separately)" % (100 * worst), ok_all)
    # T5
    print("== T5 exact polynomials: 2+2 versus 1+1+1+1 hosting (loss events only) ==")
    def S(poly, q): return sum(float(c) * q ** d for d, c in enumerate(poly))
    def root(f, lo, hi):
        flo = f(lo)
        for _ in range(200):
            mid = (lo + hi) / 2
            if (f(mid) > 0) == (flo > 0): lo = mid
            else: hi = mid
        return (lo + hi) / 2
    for nm in names[1:]:
        a = table[(nm, "2+2")][0]; b = table[(nm, "1+1+1+1")][0]
        ratios = ["q=%g: %.0fx" % (q, S(a, q) / S(b, q)) for q in (1e-3, 1e-2, 5e-2)]
        qs = root(lambda q: S(a, q) - S(b, q), 1e-4, 0.9)
        print("      %-18s silent(2+2)/silent(1+1+1+1): %s ; exact crossover q* = %.3f" % (nm, ", ".join(ratios), qs))
    nm = "J conv"; a = table[(nm, "2+2")][0]; b = table[(nm, "1+1+1+1")][0]
    check("T5a 1+1+1+1 hosting has the lower silent probability at q = 1e-3, 1e-2 and 5e-2 for all three joint rounds", all(S(table[(n, "2+2")][0], q) > S(table[(n, "1+1+1+1")][0], q) for n in names[1:] for q in (1e-3, 1e-2, 5e-2)))
    check("T5b the three joint rounds have identical loss-only silent polynomials (the floor does not depend on the extraction design)", all(table[(n, "2+2")][0] == table[("J conv", "2+2")][0] and table[(n, "1+1+1+1")][0] == table[("J conv", "1+1+1+1")][0] for n in names[1:]))
    print("ALL PASS" if OK else "SOME CHECKS FAILED")
    return 0 if OK else 1

if __name__ == "__main__":
    sys.exit(main())
