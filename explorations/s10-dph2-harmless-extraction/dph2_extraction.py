#!/usr/bin/env python3
"""S10: can a code that survives the loss of a whole 2-axis photon (S03) ALSO have harmless gate failures (S07) under whole-photon erasure?

S07: with the V1.0 geometry hosted two axes per photon and a failure that erases the photons of the gate, every data-touching failure of
the [[4,2,2]] joint round is fatal (photon-level distance 1).  S03: [[6,2]] hosted 3 photons x 2 axes has photon-level distance >= 2 (any one photon
may be lost).  Question: with explicit extraction circuits (conventional, and a verified cat in V1.0's pattern) does the full-state erasure test (S07 Model A)
say that a failed gate leaves the logical information intact at every gate?  A generic circuit builder is used and validated first against V1.0's own
op lists and against S07's patterns, so the new engine is not trusted on its own.

Assumptions (ASSUMED, as in S07): a failed inter-photon gate heralds itself, erases the photons of both qubits (data photon = its 2 axes; each ancilla
qubit is its own photon, K = 1), the round stops there, earlier gates succeeded; intra-photon gates are ideal.  Each check of a round is analysed from the
code state (earlier checks have finished and their ancillas are measured).  "Harmless" is an upper bound on usable outcomes (recovery is not modelled).

Claims
  E1  The generic builder reproduces V1.0's cat-check op list for ZZZZ and XXXX gate by gate, and reproduces S07's recoverability patterns for [[4,2,2]]
      (conventional 10011001 with 1 axis/photon; all-fatal data gates with 2 axes/photon).                                           DERIVED (cross-check)
  E2  [[6,2]] hosted [2,2,2] under whole-photon erasure: exact patterns for conventional and verified-cat extraction of its lightest generating set,
      with the number of fatal points, the inter-photon gate count (completion exponent) and the data-touching gates per logical qubit.  DERIVED on ASSUMED semantics
  E4  The same holds, certificate by certificate, for 9 further certificates of [[5,1]], [[7,3]] and [[8,4]] (hosted in blocks of 2 axes): verified-cat extraction has 0
      fatal points, conventional extraction 2 to 12.  An observation across 19 certificates in 4 families, NOT a proof and no mechanism is tested.  DERIVED per certificate
  E3  The result is compared with [[4,2,2]] 1+1+1+1 verified cat (S07/S09): photons per logical qubit, completion exponent, fatal points.          DERIVED
Author-side; not an independent reproduction.  Requires numpy.
"""
import importlib.util, itertools, os, random, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
def _load(name, rel):
    sp = importlib.util.spec_from_file_location(name, os.path.join(ROOT, *rel)); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
s07 = _load("s07", ["explorations", "s07-failure-semantics", "failure_semantics.py"]); sv = s07.sv; v10 = s07.v10
s03 = _load("s03", ["explorations", "s03-hosted-codes", "hosted_codes.py"])

OK = True
def check(name, ok):
    global OK
    OK = OK and bool(ok); print(("PASS  " if ok else "FAIL  ") + name)

SGATE = np.diag([1, 1j]); SDAG = np.diag([1, -1j])
def pauli_dict(g, n): return {q: ("Y" if (g[0] >> q) & 1 and (g[1] >> q) & 1 else "X" if (g[0] >> q) & 1 else "Z") for q in range(n) if (g[0] | g[1]) >> q & 1}
def pstr(g, n): return "".join(pauli_dict(g, n).get(q, "I") for q in range(n))

def code_basis(gens, n, k):
    sim = sv.Sim(n); cols = []
    for idx in range(2 ** n):
        e = np.zeros(2 ** n, dtype=complex); e[idx] = 1
        for g in gens: e = (e + sim.pauli(e, pauli_dict(g, n))) / 2
        cols.append(e)
    u, s_, vh = np.linalg.svd(np.array(cols).T, full_matrices=False)
    assert np.sum(s_ > 1e-9) == 2 ** k, (np.sum(s_ > 1e-9), 2 ** k)
    return u[:, :2 ** k]

# ---------- generic extraction-circuit builders (ops as in the V1.0 loader, plus ('S',q) and ('Sd',q)) ----------
def build_conv(g, n, first_anc, ycorr):
    """one ancilla in |+> controlling the generator on the data qubits, read out in the X basis"""
    a = first_anc; ops = [("P+", a)]; supp = [q for q in range(n) if (g[0] | g[1]) >> q & 1]
    for q in supp:
        x, z = (g[0] >> q) & 1, (g[1] >> q) & 1
        ops += ([("CZ", a, q), ("CNOT", a, q)] if x and z else [("CNOT", a, q)] if x else [("CZ", a, q)])
    ops += [("S", a)] * ycorr
    ops.append(("MX", a, 0)); return ops, 1
def build_cat(g, n, first_anc, ycorr):
    """verified cat in V1.0's pattern: GHZ on w qubits, parity-check of its end qubits, each cat qubit controls one factor, X readout"""
    supp = [q for q in range(n) if (g[0] | g[1]) >> q & 1]; w = len(supp); cat = list(range(first_anc, first_anc + w)); ver = first_anc + w
    ops = [("P0", c) for c in cat] + [("H", cat[0])] + [("CNOT", cat[i], cat[i + 1]) for i in range(w - 1)]
    ops += [("P0", ver), ("CNOT", cat[0], ver), ("CNOT", cat[-1], ver), ("MZ", ver, 0)]
    for c, q in zip(cat, supp):
        x, z = (g[0] >> q) & 1, (g[1] >> q) & 1
        if x and z: ops += [("CZ", c, q), ("CNOT", c, q)] + [("S", c)] * ycorr
        elif x: ops.append(("CNOT", c, q))
        else: ops.append(("CZ", c, q))
    ops += [("MX", c, 1 + i) for i, c in enumerate(cat)]
    return ops, w + 1

def replay(sim, ops, v, branch=0, upto=None):
    out = []; ri = 0
    for op in ops[:upto]:
        k = op[0]
        if k == "P0": pass
        elif k in ("P+", "H"): v = sim.one(v, sv.HAD, op[1])
        elif k == "S": v = sim.one(v, SGATE, op[1])
        elif k == "Sd": v = sim.one(v, SDAG, op[1])
        elif k == "CNOT": v = sim.cnot(v, op[1], op[2])
        elif k == "CZ": v = sim.cz(v, op[1], op[2])
        else:
            if k == "MX": v = sim.one(v, sv.HAD, op[1])
            v, o, rnd = sim.measure_z(v, op[1], branch=(branch >> ri) & 1)
            if rnd: ri += 1
            out.append((k, op[1], o))
    return v, out

def make_check(builder, g, n, basis, first_anc):
    """choose the phase correction for Y factors so that the fault-free check returns +1 deterministically and leaves the data unchanged"""
    for yc in (0, 1, 2, 3):
        ops, nanc = builder(g, n, first_anc, yc); nq = first_anc + nanc; sim = sv.Sim(nq); good = True
        for j in range(basis.shape[1]):
            for br in (0, 0b1010, 0b0101, 0b1111):
                v = np.zeros(sim.N, dtype=complex); v[:2 ** n] = basis[:, j]
                try: v, out = replay(sim, ops, v, br)
                except RuntimeError: good = False; break
                mx = [o for k, q, o in out if k == "MX"]; mz = [o for k, q, o in out if k == "MZ"]
                par = sum(mx) % 2 if len(mx) > 1 else (mx[0] if mx else 0)
                good &= (par == 0 and all(o == 0 for o in mz) and abs(abs(np.vdot(v[:2 ** n], basis[:, j])) - 1) < 1e-9)
            if not good: break
        if good: return ops, nq, yc
    return None

def failable(ops, n, host, K1=True):
    """(op index, lost set under ErasePhoton, kind) for every inter-photon two-qubit gate; every ancilla qubit is its own photon"""
    of = {q: tuple(b) for b in host for q in b}; out = []
    for i, op in enumerate(ops):
        if op[0] not in ("CNOT", "CZ"): continue
        a, b = op[1], op[2]
        if a < n or b < n:
            d, an = (a, b) if a < n else (b, a); out.append((i, set(of[d]) | {an}, "D"))
        else: out.append((i, {a, b}, "a"))
    return out

def recover_pattern(ops, nq, n, basis, host, sem, detail=None):
    sim = sv.Sim(nq); res = []; kinds = ""
    for i, lost, kind in failable(ops, n, host):
        if sem == "EraseAxis":
            lost = {q for q in lost if q >= n or q in set(sum([list(b) for b in host if any(q2 in b for q2 in [x for x in lost if x < n][:1])], []))}
            ops_i = ops[i]; lost = {ops_i[1], ops_i[2]}
        phis = []
        for j in range(basis.shape[1]):
            v = np.zeros(sim.N, dtype=complex); v[:2 ** n] = basis[:, j]; v, _ = replay(sim, ops, v, 0, upto=i); phis.append(v)
        lostl, E = lost_blocks_generic(sim, phis, lost)
        d = basis.shape[1]; rho = E[(0, 0)]
        ok = all(np.allclose(E[(j, j)], rho, atol=1e-9) for j in range(d)) and all(np.allclose(E[(j, k)], 0, atol=1e-9) for j in range(d) for k in range(d) if j != k)
        res.append(1 if ok else 0); kinds += kind
        if detail is not None: detail.append((ok, kind, tuple(sorted(q for q in lost if q < n))))
    return res, kinds

def lost_blocks_generic(sim, phis, lost):
    lost = sorted(lost); keep = [q for q in range(sim.nq) if q not in lost]; A = []
    for v in phis:
        T = v.reshape([2] * sim.nq)
        A.append(np.transpose(T, [sim.nq - 1 - q for q in keep] + [sim.nq - 1 - q for q in lost]).reshape(2 ** len(keep), 2 ** len(lost)))
    d = len(phis); return lost, {(j, k): A[j].conj().T @ A[k] for j in range(d) for k in range(d)}

def round_pattern(gens, n, k, host, builder, sem, detail=None):
    basis = code_basis(gens, n, k); allr = []; allk = ""; gates = 0
    for g in gens:
        made = make_check(builder, g, n, basis, n)
        if made is None: raise RuntimeError("no phase correction makes the fault-free check deterministic for generator " + pstr(g, n))
        ops, nq, yc = made
        r, kinds = recover_pattern(ops, nq, n, basis, host, sem, detail); allr += r; allk += kinds
    return allr, allk

def main():
    # ---- E1: validation against V1.0 and S07 -----------------------------------------------------------------------------
    R = v10.load(); Z4 = (0, 0b1111); X4 = (0b1111, 0)
    ops_z, nq_z, _ = make_check(build_cat, Z4, 4, s07.code_basis("J"), 4)
    v1 = [op for op in R["J cat (verified)"]["ops"][:20] if op[0] != "MX"]
    mine = [op for op in ops_z if op[0] != "MX"]
    norm = lambda ops: [tuple(o[:3]) if o[0] in ("CNOT", "CZ") else (o[0],) + tuple(o[1:2]) for o in ops]
    check("E1a generic cat builder for ZZZZ reproduces V1.0's cat-check gate sequence (CNOT/CZ list, same qubit labels)", [o for o in norm(mine) if o[0] in ("CNOT", "CZ")] == [o for o in norm(v1) if o[0] in ("CNOT", "CZ")])
    ops_x, _, _ = make_check(build_cat, X4, 4, s07.code_basis("J"), 4)
    seq_x = [tuple(o[:3]) for o in ops_x if o[0] in ("CNOT", "CZ")]
    shift = lambda q: q - 5 if q >= 4 else q
    v1b = [(o[0], shift(o[1]), shift(o[2])) for o in R["J cat (verified)"]["ops"] if o[0] in ("CNOT", "CZ")][-9:]
    check("E1b generic cat builder for XXXX reproduces V1.0's second cat-check gate sequence (9 gates, labels shifted by the 5 ancilla qubits of the first check)", seq_x == v1b)
    J = [X4, Z4]; host1 = [(0,), (1,), (2,), (3,)]; host2 = [(0, 1), (2, 3)]
    rconv1, kc1 = round_pattern([Z4, X4], 4, 2, host1, build_conv, "EraseAxis")
    rconv2, kc2 = round_pattern([Z4, X4], 4, 2, host2, build_conv, "ErasePhoton")
    rcat2, kk2 = round_pattern([Z4, X4], 4, 2, host2, build_cat, "ErasePhoton")
    rcat1, kk1 = round_pattern([Z4, X4], 4, 2, host1, build_cat, "EraseAxis")
    check("E1c generic conventional extraction of [[4,2,2]], 1 axis/photon, EraseAxis: r = 10011001 (S07)", "".join(map(str, rconv1)) == "10011001")
    check("E1d generic conventional extraction of [[4,2,2]], 2 axes/photon, ErasePhoton: all fatal (S07)", sum(rconv2) == 0 and len(rconv2) == 8)
    check("E1e generic verified-cat extraction of [[4,2,2]], 2 axes/photon, ErasePhoton: 111110000 pattern twice (S07: 111110000111110000)", "".join(map(str, rcat2)) == "111110000111110000")
    check("E1f generic verified-cat extraction of [[4,2,2]], 1 axis/photon: every failure harmless (S07/S09)", all(rcat1))
    # ---- E2: the [[6,2]] code --------------------------------------------------------------------------------------------
    n, k, m = 6, 2, 2; rng = random.Random(202); cands = []
    for t in range(6000):
        g = s03.random_code(n, k, rng)
        if all(s03.correctable(g, n, b) for b in s03.blocks(n, m)):
            mg = s03.min_weight_generators(g, n); w = sorted(bin(e[0] | e[1]).count("1") for e in mg); cands.append(((sum(w), max(w)), mg, g))
    cands.sort(key=lambda c: c[0]); best = cands[0]; gens = [tuple(e) for e in best[1]]
    host = [tuple(b) for b in s03.blocks(n, m)]
    print("== E2 [[6,2]] hosted %s, d_ph >= 2 (%d certificates in 6000 random codes); lightest generating set found: %s  weights %s ==" % (host, len(cands), [pstr(g, n) for g in gens], sorted(bin(g[0] | g[1]).count("1") for g in gens)))
    check("E2a the code is a certificate of S03 (every photon erasable) and its generators are independent and commuting", all(s03.correctable(list(gens), n, b) for b in s03.blocks(n, m)) and s03.valid_stabilizer(gens))
    out = {}
    for nm, bld in (("conventional", build_conv), ("verified cat", build_cat)):
        for sem in ("ErasePhoton", "EraseAxis"):
            r, kinds = round_pattern(gens, n, k, host, bld, sem); out[(nm, sem)] = (r, kinds)
            print("      %-13s %-12s inter-photon gates %-3d kinds %s" % (nm, sem, len(r), kinds))
            print("                    r = %s   fatal points %d" % ("".join(map(str, r)), r.count(0)))
    cv0 = out[("conventional", "ErasePhoton")][0]; cat_r = out[("verified cat", "ErasePhoton")][0]
    check("E2b [[6,2]] with conventional extraction, ErasePhoton: has fatal points (%d of %d inter-photon gates)" % (cv0.count(0), len(cv0)), cv0.count(0) > 0)
    check("E2c [[6,2]] with verified-cat extraction, ErasePhoton: EVERY failure is harmless (0 fatal points of %d)" % len(cat_r), all(cat_r))
    # E2d: negative control -- same code, a hosting in which one photon DOES support a nontrivial logical operator (d_ph = 1): fatal points must appear
    bad = None
    for pair in itertools.combinations(range(n), 2):
        if not s03.correctable(list(gens), n, list(pair)):
            rest = [q for q in range(n) if q not in pair]
            for p2 in itertools.combinations(rest, 2):
                bad = [tuple(pair), tuple(p2), tuple(q for q in rest if q not in p2)]; break
            break
    det = []; rbad, kbad = round_pattern(gens, n, k, bad, build_cat, "ErasePhoton", det)
    fatal = [d for d in det if not d[0]]; nonerasable = {tuple(b_) for b_ in bad if not s03.correctable(list(gens), n, list(b_))}
    fatal_photons = {d[2] for d in fatal}
    check("E2d negative control: hosting %s has non-erasable photons %s; the verified-cat round then has %d fatal points, all data-touching, exactly at those photons (%s), none at the erasable photon(s)" %
          (bad, sorted(nonerasable), len(fatal), sorted(fatal_photons)), len(fatal) > 0 and all(d[1] == "D" for d in fatal) and fatal_photons == nonerasable)
    # E2e: robustness over the 10 lightest certificates
    print("== E2e robustness: fatal points over the 10 lightest certificates found (ErasePhoton) ==")
    stats = []
    for c in cands[:10]:
        gg = [tuple(e) for e in c[1]]
        rc, _ = round_pattern(gg, n, k, host, build_conv, "ErasePhoton"); rk, kk = round_pattern(gg, n, k, host, build_cat, "ErasePhoton")
        stats.append((c[0], rc.count(0), len(rc), rk.count(0), len(rk)))
        print("      weights-sum/max %-8s conventional: %d fatal of %d    verified cat: %d fatal of %d" % (c[0], rc.count(0), len(rc), rk.count(0), len(rk)))
    check("E2e verified-cat extraction has 0 fatal points for all 10 certificates; conventional extraction has fatal points for each of them", all(st[3] == 0 for st in stats) and all(st[1] > 0 for st in stats))
    # E4: other S03 families -- does "d_ph >= 2 plus verified-cat extraction => every failure harmless" hold beyond [[6,2]]?
    print("== E4 other certificate families (3 lightest certificates of each; ErasePhoton; data hosting by blocks of m axes) ==")
    fam_ok = True; fam_rows = []
    for (n_, k_, m_, tries_) in ((5, 1, 2, 3000), (7, 3, 2, 4000), (8, 4, 2, 6000)):
        rng_ = random.Random(1000 * n_ + k_); cc = []
        for t_ in range(tries_):
            g_ = s03.random_code(n_, k_, rng_)
            if all(s03.correctable(g_, n_, b_) for b_ in s03.blocks(n_, m_)):
                mg_ = s03.min_weight_generators(g_, n_); w_ = sorted(bin(e[0] | e[1]).count("1") for e in mg_); cc.append(((sum(w_), max(w_)), mg_))
        cc.sort(key=lambda c_: c_[0]); host_ = [tuple(b_) for b_ in s03.blocks(n_, m_)]
        for key_, mg_ in cc[:3]:
            gg_ = [tuple(e) for e in mg_]
            rc_, _ = round_pattern(gg_, n_, k_, host_, build_conv, "ErasePhoton"); rk_, _ = round_pattern(gg_, n_, k_, host_, build_cat, "ErasePhoton")
            fam_rows.append((n_, k_, host_, key_, rc_.count(0), len(rc_), rk_.count(0), len(rk_)))
            print("      [[%d,%d]] hosting %-30s weights sum/max %-8s conventional: %2d fatal of %2d   verified cat: %2d fatal of %2d" % (n_, k_, host_, key_, rc_.count(0), len(rc_), rk_.count(0), len(rk_)))
        if not cc: print("      [[%d,%d]] no certificate found in %d random codes" % (n_, k_, tries_)); fam_ok = False
    check("E4 verified-cat extraction has 0 fatal points for every certificate tested in the extra families (%d certificates)" % len(fam_rows), fam_ok and len(fam_rows) > 0 and all(r[6] == 0 for r in fam_rows))
    print("== E3 comparison (assumed semantics; ceilings, recovery not modelled; K = 1: every ancilla qubit its own photon) ==")
    wt = sorted(bin(g[0] | g[1]).count("1") for g in gens); dg = sum(wt)
    cv = out[("conventional", "ErasePhoton")][0]; anc_cv = len(gens); anc_cat = sum(w_ + 1 for w_ in wt)
    print("      %-40s %-9s %-10s %-10s %-9s %-9s %-7s" % ("design", "data ph.", "per logical", "data gates", "inter n", "anc ph.", "fatal"))
    print("      %-40s %-9d %-10.2f %-10d %-9d %-9d %-7d" % ("[[4,2,2]] 1+1+1+1, verified cat (EraseAxis)", 4, 2.0, 8, 18, 10, 0))
    print("      %-40s %-9d %-10.2f %-10d %-9d %-9d %-7d" % ("[[6,2]] 3x2, conventional (ErasePhoton)", 3, 1.5, dg, len(cv), anc_cv, cv.count(0)))
    print("      %-40s %-9d %-10.2f %-10d %-9d %-9d %-7d" % ("[[6,2]] 3x2, verified cat (ErasePhoton)", 3, 1.5, dg, len(cat_r), anc_cat, cat_r.count(0)))
    print("      data photons per logical qubit fall from 2.0 to 1.5, but data-touching gates per logical qubit rise from 4 to %.1f and the completion exponent for a cat round" % (dg / k))
    print("      rises from 18 to %d (s^%d: at s = 0.9, %.4f versus %.4f).  The harmless failures also erase 2 axes at a time, which the recovery must rebuild." % (len(cat_r), len(cat_r), 0.9 ** len(cat_r), 0.9 ** 18))
    check("E3 the numbers above are computed: [[6,2]] cat round has %d inter-photon gates (V1.0 [[4,2,2]] cat: 18)" % len(cat_r), len(cat_r) > 18)
    print("ALL PASS" if OK else "SOME CHECKS FAILED")
    return 0 if OK else 1

if __name__ == "__main__":
    sys.exit(main())
