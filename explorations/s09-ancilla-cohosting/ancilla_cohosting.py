#!/usr/bin/env python3
"""S09: what hosting several ancilla qubits on one photon (V1.0's "K") does to the recoverability found in S07.

V1.0 reports that a flag sharing its ancilla's photon (K = 2) costs no extra inter-photon gates (8 instead of 12) and that the verified cat needs
18 / 14 / 8 inter-photon gates at K = 1 / 2 / 5.  S07 found that, if a failed inter-photon gate erases the qubits it acts on, the flag and the cat make
every failure harmless because the other ancilla qubits survive.  If the ancilla qubits share a photon, a failed gate erases the WHOLE ancilla photon,
so the surviving partner qubits vanish with it.  This script tests exactly that, with the same exact full-state test as S07 (Model A), same ASSUMED
erasure semantics, data hosted one axis per photon (so the data side is EraseAxis), and the packing rule of V1.0 (K consecutive ancilla qubits of one
check per photon).  Intra-photon gates (both qubits on one photon) are ideal and cannot fail.

Claims
  H1  The inter-photon gate counts obtained from this packing reproduce V1.0's table (conventional 8/8/8, flagged 12/8/8, verified cat 18/14/8 for K = 1/2/5).  DERIVED (cross-check)
  H2  At K = 1 the recoverability patterns equal S07's (flagged and cat: every failure harmless).                                                         DERIVED (cross-check)
  H3  At K >= 2 the flagged round loses the harmless-failure property and has EXACTLY the conventional round's failure profile (r = 10011001: the flag
      is erased together with its ancilla and its masking vanishes); the verified cat at K = 5 does the same; the verified cat at K = 2 keeps zero
      fatal points at 14 inter-photon gates (mechanism, not tested here: the relative phase that records a partial parity lives in the cat's GHZ coherence and survives while some cat qubit survives).  [the first version of this script
      claimed the cat also acquires fatal points at K = 2; its own check failed, see run-history.txt]                                              DERIVED on ASSUMED semantics
  H4  Whether the saving pays depends on s: the table prints, per round and K, the completion probability s^n and the lower bound on the probability that a
      round attempt loses the logical information (recovery of the erased axis after a harmless failure is not modelled, so the loss is a lower bound).        DERIVED
Author-side; not an independent reproduction.  Requires numpy.
"""
import importlib.util, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
def _load(name, rel):
    sp = importlib.util.spec_from_file_location(name, os.path.join(ROOT, *rel)); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
s07 = _load("s07", ["explorations", "s07-failure-semantics", "failure_semantics.py"]); v10 = s07.v10

OK = True
def check(name, ok):
    global OK
    OK = OK and bool(ok); print(("PASS  " if ok else "FAIL  ") + name)

CHECKS = {"J conv": [[4], [5]], "J flag": [[4, 5], [6, 7]], "J cat (verified)": [[4, 5, 6, 7, 8], [9, 10, 11, 12, 13]]}
V10_COUNT = {"J conv": {1: 8, 2: 8, 5: 8}, "J flag": {1: 12, 2: 8, 5: 8}, "J cat (verified)": {1: 18, 2: 14, 5: 8}}
V10_PHOTONS = {"J conv": {1: 2, 2: 2, 5: 2}, "J flag": {1: 4, 2: 2, 5: 2}, "J cat (verified)": {1: 10, 2: 6, 5: 2}}

def groups(nm, K):
    g = []
    for chk in CHECKS[nm]:
        for i in range(0, len(chk), K): g.append(tuple(chk[i:i + K]))
    return g

def analyse(R, nm, K, basis):
    G = groups(nm, K); of = {q: gr for gr in G for q in gr}
    ops = R["ops"]; rec = []; kinds = []; order = []
    for i, op in enumerate(ops):
        if op[0] not in ("CNOT", "CZ"): continue
        a, b = op[1], op[2]
        if a < 4 or b < 4:                               # data-touching (always inter-photon: the data photon is not an ancilla photon)
            d, an = (a, b) if a < 4 else (b, a)
            lost = {d} | set(of[an]); kind = "D"
        else:
            if of[a] == of[b]: continue                  # intra-photon, ideal
            lost = set(of[a]) | set(of[b]); kind = "a"
        rec.append(1 if s07.recoverable(R, basis, i, lost) else 0); kinds.append(kind)
    return G, rec, "".join(kinds)

def main():
    R = v10.load(); bases = {c: s07.code_basis(c) for c in "LJ"}
    print("== H1/H2/H3 exact recoverability r_i over the FAILABLE (inter-photon) gates; D = data-touching, a = ancilla-ancilla ==")
    res = {}; ok1 = True; ok2 = True
    for nm in ("J conv", "J flag", "J cat (verified)"):
        for K in (1, 2, 5):
            G, r, kinds = analyse(R[nm], nm, K, bases["J"]); res[(nm, K)] = (r, kinds)
            ok1 &= (len(r) == V10_COUNT[nm][K]) and (len(G) == V10_PHOTONS[nm][K])
            print("      %-18s K=%d  photons %-2d inter-photon gates %-2d  kinds %-20s r = %s   (fatal points: %d)" % (nm, K, len(G), len(r), kinds, "".join(map(str, r)), r.count(0)))
    check("H1 inter-photon gate counts and ancilla photon counts reproduce V1.0's table for all 9 (round, K) cases", ok1)
    s07flag = s07_pattern(R, bases, "J flag"); s07cat = s07_pattern(R, bases, "J cat (verified)"); s07conv = s07_pattern(R, bases, "J conv")
    check("H2 K=1 patterns equal S07's (flagged all 1; cat all 1; conventional 10011001)", all(res[("J flag", 1)][0]) and all(res[("J cat (verified)", 1)][0]) and "".join(map(str, res[("J conv", 1)][0])) == "10011001")
    check("H2b K=1 patterns of all three joint rounds are identical, gate by gate, to the lists S07's own code produces", res[("J flag", 1)][0] == s07flag and res[("J cat (verified)", 1)][0] == s07cat and res[("J conv", 1)][0] == s07conv)
    check("H3a conventional joint: one ancilla per check, so K changes nothing (same pattern at K = 1, 2, 5)", res[("J conv", 1)][0] == res[("J conv", 2)][0] == res[("J conv", 5)][0])
    check("H3b flagged round at K = 2 has fatal failure points (the flag is erased together with its ancilla)", res[("J flag", 2)][0].count(0) > 0)
    conv = res[("J conv", 1)][0]
    check("H3c flagged round at K = 2 and K = 5 has exactly the conventional pattern (r = 10011001), so its failure profile equals the conventional round's", res[("J flag", 2)][0] == conv and res[("J flag", 5)][0] == conv)
    check("H3d verified cat at K = 5 has exactly the conventional pattern", res[("J cat (verified)", 5)][0] == conv)
    check("H3e verified cat at K = 2 keeps ZERO fatal failure points at 14 inter-photon gates (18 at K = 1, 8 at K = 5)", res[("J cat (verified)", 2)][0].count(0) == 0 and len(res[("J cat (verified)", 2)][0]) == 14)
    # table with s
    def pk(r):
        n = len(r); poly = {n: 1}
        for i, ri in enumerate(r, start=1):
            if ri: poly[i - 1] = poly.get(i - 1, 0) + 1; poly[i] = poly.get(i, 0) - 1
        return poly
    def pe(p, s): return sum(v * s ** k for k, v in p.items())
    print("== H4  per round attempt: completion = s^n ; P(information lost) >= sum over fatal failable gates of s^(i-1)(1-s) ; harmless aborts = the rest ==")
    print("      %-18s %-3s %-4s | %s" % ("round", "K", "n", "   ".join("s=%-4g completion / lost / harmless-abort" % s for s in (0.95, 0.75, 0.5))))
    for nm in ("J conv", "J flag", "J cat (verified)"):
        for K in (1, 2, 5):
            r, kinds = res[(nm, K)]; n = len(r); cells = []
            for s in (0.95, 0.75, 0.5):
                comp = s ** n; lost = sum(s ** (i) * (1 - s) for i, ri in enumerate(r) if not ri); harm = 1 - comp - lost
                cells.append("%.4f / %.4f / %.4f" % (comp, lost, harm))
            print("      %-18s %-3d %-4d | %s" % (nm, K, n, "   ".join(cells)))
    loss = lambda nm, K, s: sum(s ** i * (1 - s) for i, ri in enumerate(res[(nm, K)][0]) if not ri)
    check("H4a flagged: P(loss) is exactly 0 at K = 1 and strictly positive at K = 2 for every s in (0, 1)", all(loss("J flag", 1, s) == 0 and loss("J flag", 2, s) > 0 for s in (0.3, 0.5, 0.75, 0.95)))
    print("      NOTE  the K = 2 flagged round has the conventional round's inter-photon gate count (8) AND its exact loss profile (%.4f at s = 0.75): the flag then adds first-order silent-damage protection (V0.9/V1.0) but nothing against heralded failure." % loss("J flag", 2, 0.75))
    print("      Harmless aborts are not free: the erased data axis must be rebuilt (not modelled).  Loss probabilities here are lower bounds; the completion exponents are V1.0's.")
    print("ALL PASS" if OK else "SOME CHECKS FAILED")
    return 0 if OK else 1

def s07_pattern(R, bases, nm):
    """S07's r_i for the failable gates at K = 1 (all ancilla qubits on their own photon), computed through S07's own function path"""
    ops = R[nm]["ops"]; out = []
    for i, op in enumerate(ops):
        if op[0] in ("CNOT", "CZ"): out.append(1 if s07.recoverable(R[nm], bases["J"], i, {op[1], op[2]}) else 0)
    return out

if __name__ == "__main__":
    sys.exit(main())
