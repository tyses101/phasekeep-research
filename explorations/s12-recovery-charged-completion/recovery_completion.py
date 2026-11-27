#!/usr/bin/env python3
"""S12: what is left of S07's "harmless failure" result once the recovery of the erased axis is charged for?

S07 Model A says: in the joint flagged and cat rounds, a failed data-touching gate (one erased axis) leaves the logical information intact
(r_i = 1 at every gate), so P_A = 1.  S07 also says what this is NOT: the erased axis must be re-created, and that takes inter-photon gates of its
own, each of which can fail.  This script puts a price on that and compares the result with the local round (distance 1, every failure fatal).

Process (ASSUMED; each line is a modelling choice, not a measurement)
  - a "data-affecting gate" is an inter-photon gate that touches a data axis (D), or (strict policy only) an ancilla-only gate with an ancilla that has
    already interacted with data (T).  Ancilla-only gates on untouched ancillas (F) fail harmlessly and are retried at no cost to the data (this ignores
    the time they take; time-dependent loss is open problem 6).
  - every data-affecting gate succeeds with probability s, independently; the first failure aborts the attempt and erases the axes of that gate
    (EraseAxis, one axis per photon, exactly S07's r_i).
  - r_i = 0: the information has leaked, fatal.  r_i = 1: one axis is erased and must be recovered.
  - recovery restores the code space and succeeds with probability rho; a failed recovery is fatal (two erased axes of [[4,2,2]] are never correctable, checked
    below as R5).  After a successful recovery the verification round is repeated from the start, because restoring the erased axis uses up the syndrome
    (the replacement axis is set from the others, which absorbs any error on them; argued, not simulated).
  - P(rho) = P(eventually complete one verification round with the information intact).  Local round: no failure is recoverable, P = s^4.
  - rho = s^m models a recovery that needs m inter-photon gates that all must succeed.  The MINIMUM m is not known here; it is a parameter.

Claims
  R0  The gate classification (D, T, F) and the r_i vectors are recomputed from V1.0's op lists with S07's full-state test.  Conventional r = 10011001,
      flagged and cat r = 1 at every gate; flagged has 8 D and 4 T gates, cat has 8 D, 0 T and 10 F gates.                                DERIVED
  R5  Erasing any one axis of [[4,2,2]] is recoverable and erasing any two is not (all 4 and all 6 cases).                               DERIVED
  R1  Closed form P = s^n / (1 - h rho), with h = sum over recoverable first-failure positions of s^(j-1)(1-s), equals the exact value from enumerating all gate outcomes
      the exact enumeration of all gate outcomes, and a gate-by-gate Monte Carlo (4 sigma).  rho = 1 gives 1 (S07's ceiling); rho = 0 gives s^n (plain completion).        DERIVED
  R2  Conventional joint round: P(rho) < s^4 for EVERY rho <= 1 and every s in (0,1), because s + s^2 > s^4 + s^7.  Even free recovery does not rescue it.  DERIVED
  R3  Flagged and cat joint rounds, ancilla failures free: P(rho) > s^4 iff rho > 1/(1+s^4).  With rho = s^m this is s^m (1 + s^4) > 1.  Crossover s for
      m = 3 and m = 8 given with exact sign certificates; above it the joint round wins, below it the local round does.                      DERIVED on ASSUMED process
  R4  Strict policy (flagged ancilla failures also need recovery): flagged needs rho > (1+s^4)/(1+s^4+s^8), cat is unchanged, so under this price the cat
      design keeps an advantage over the flagged one that Model B and the free policy could not show.                                       DERIVED on ASSUMED process
Not claimed: that any recovery circuit has m gates for any particular m; that P(rho) predicts a device; anything about time, leakage, correlated loss.
Author-side; not an independent reproduction.  Requires numpy (through S07).
"""
import importlib.util, itertools, math, os, random, sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
def _load(name, rel):
    sp = importlib.util.spec_from_file_location(name, os.path.join(ROOT, *rel)); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
s07 = _load("s07", ["explorations", "s07-failure-semantics", "failure_semantics.py"]); v10 = s07.v10

OK = True
def check(name, ok):
    global OK
    OK = OK and bool(ok); print(("PASS  " if ok else "FAIL  ") + name)

def classify(ops):
    """kind of every two-qubit gate: D = touches a data axis (qubits 0..3); T = ancilla-only but an ancilla has already (transitively) interacted with data;
    F = ancilla-only, both ancillas untouched by data so far"""
    tainted = set(range(4)); kinds = []
    for op in ops:
        if op[0] not in ("CNOT", "CZ"): continue
        a, b = op[1], op[2]
        kinds.append("D" if (a < 4 or b < 4) else ("T" if (a in tainted or b in tainted) else "F"))
        if a in tainted or b in tainted: tainted |= {a, b}
    return kinds

def r_vector(R, basis, name):
    """S07's full-state test at every two-qubit gate: lose the qubits of the gate (EraseAxis, one axis per photon)"""
    ops = R[name]["ops"]; out = []
    for i, op in enumerate(ops):
        if op[0] in ("CNOT", "CZ"): out.append(1 if s07.recoverable(R[name], basis, i, {op[1], op[2]}) else 0)
    return out

def sequence(kinds, r, policy):
    """r_j of the data-affecting gates in order; policy 'free' keeps D only, 'strict' keeps D and T"""
    keep = ("D",) if policy == "free" else ("D", "T")
    return tuple(ri for k, ri in zip(kinds, r) if k in keep)

def chain(seq, s, rho):
    """P(eventually complete with the information intact); exact for Fraction s, rho"""
    n = len(seq); p = s ** n
    h = sum(s ** j * (1 - s) for j, ri in enumerate(seq) if ri)
    return p / (1 - h * rho)

def enum_masses(seq, s):
    """probabilities of 'complete' and 'first failure at a recoverable gate', by enumerating all 2^n success/failure vectors of the data-affecting gates
    (each vector has probability prod s or (1-s) over all n gates; it belongs to the first failure in it) -- no use of the s^j (1-s) formula"""
    n = len(seq); pc = Fr(0); to_E = Fr(0)
    for v in itertools.product((1, 0), repeat=n):
        pr = Fr(1)
        for x in v: pr *= s if x else 1 - s
        if all(v): pc += pr
        elif seq[v.index(0)]: to_E += pr
    return pc, to_E

def mc(seq, s, m, N, seed):
    """gate-by-gate Monte Carlo of the process; recovery = m gates that must all succeed"""
    rng = random.Random(seed); wins = 0
    for _ in range(N):
        while True:
            j = None
            for k in range(len(seq)):
                if rng.random() >= s: j = k; break
            if j is None: wins += 1; break
            if not seq[j]: break
            if all(rng.random() < s for _ in range(m)): continue
            break
    return wins / N

def crossing(fun, lo=Fr(3, 10), hi=Fr(9995, 10000)):
    """sample the sign of fun(s) on 2001 rational points; require exactly one change (joint loses below, wins above); bisect with exact rationals"""
    grid = [lo + (hi - lo) * k / 2000 for k in range(2001)]; sg = [fun(x) > 0 for x in grid]
    changes = [k for k in range(2000) if sg[k] != sg[k + 1]]
    if len(changes) != 1 or sg[0] or not sg[-1]: return None
    a, b = grid[changes[0]], grid[changes[0] + 1]
    for _ in range(40):
        mid = (a + b) / 2
        if fun(mid) > 0: b = mid
        else: a = mid
    return a, b

def main():
    R = v10.load()
    check("G0 the V1.0 op lists pass S07's guard (known ops, ancillas start with a preparation, no qubit prepared twice)", s07.guard_ops(R))
    B = s07.code_basis("J")
    names = {"conv": "J conv", "flag": "J flag", "cat": "J cat (verified)"}
    kinds = {k: classify(R[v]["ops"]) for k, v in names.items()}; rv = {k: r_vector(R, B, v) for k, v in names.items()}
    print("== R0 gate classes and S07's r vectors (EraseAxis, 1 axis/photon) ==")
    for k in names: print("      %-5s kinds %-20s r %s   D=%d T=%d F=%d" % (k, "".join(kinds[k]), "".join(map(str, rv[k])), kinds[k].count("D"), kinds[k].count("T"), kinds[k].count("F")))
    check("R0a conventional: 8 data-touching gates, r = 10011001", kinds["conv"] == ["D"] * 8 and rv["conv"] == [1, 0, 0, 1, 1, 0, 0, 1])
    check("R0b flagged: 8 D and 4 T gates, no F gate; r = 1 at every gate", (kinds["flag"].count("D"), kinds["flag"].count("T"), kinds["flag"].count("F")) == (8, 4, 0) and all(rv["flag"]))
    check("R0c cat: 8 D, 0 T, 10 F gates (cat preparation and its verification never touch data); r = 1 at every gate", (kinds["cat"].count("D"), kinds["cat"].count("T"), kinds["cat"].count("F")) == (8, 0, 10) and all(rv["cat"]))
    check("R0d every ancilla-only gate has r = 1 (an F or T failure leaks nothing) in the flagged and cat rounds", all(r == 1 for k in ("flag", "cat") for kd, r in zip(kinds[k], rv[k]) if kd != "D"))
    # --- R5: second failure is fatal -------------------------------------------------------------------------------------
    one = [s07.has_logical_on("J", {q}) for q in range(4)]; two = [s07.has_logical_on("J", set(p)) for p in itertools.combinations(range(4), 2)]
    check("R5 no single axis of [[4,2,2]] supports a nontrivial logical operator (recoverable) and every one of the 6 pairs does (not recoverable)", not any(one) and all(two) and len(two) == 6)
    # sequences
    seq = {"conv": sequence(kinds["conv"], rv["conv"], "free"), "cat": sequence(kinds["cat"], rv["cat"], "free"), "flag_free": sequence(kinds["flag"], rv["flag"], "free"),
           "flag_strict": sequence(kinds["flag"], rv["flag"], "strict"), "cat_strict": sequence(kinds["cat"], rv["cat"], "strict")}
    check("R1a the sequences: conventional 8 gates, flagged free 8, flagged strict 12, cat free = cat strict = 8", [len(seq[k]) for k in ("conv", "flag_free", "flag_strict", "cat", "cat_strict")] == [8, 8, 12, 8, 8] and seq["cat"] == seq["cat_strict"])
    # --- R1 exactness ----------------------------------------------------------------------------------------------------
    probe_s = [Fr(1, 2), Fr(3, 4), Fr(9, 10), Fr(19, 20), Fr(99, 100)]; probe_r = [Fr(0), Fr(1, 3), Fr(3, 4), Fr(1)]
    exact = True
    for k in seq:
        for s in probe_s:
            pc, to_E = enum_masses(seq[k], s)
            for r in probe_r: exact &= chain(seq[k], s, r) == pc / (1 - to_E * r)
    check("R1b closed form equals the value computed from an exhaustive enumeration of all 2^n gate outcomes, exactly, for every sequence at 5 values of s and 4 values of rho", exact)
    ends = all(chain(seq[k], s, Fr(0)) == s ** len(seq[k]) for k in seq for s in probe_s) and all(chain(seq[k], s, Fr(1)) == 1 for k in ("cat", "flag_free", "flag_strict") for s in probe_s)
    check("R1c brackets: rho = 0 gives s^n (plain completion); rho = 1 gives 1 for the all-recoverable sequences (S07's P_A = 1 is the free-recovery limit)", ends)
    mono = all(chain(seq[k], s, a) < chain(seq[k], s, b) for k in seq for s in probe_s for a, b in zip(probe_r, probe_r[1:]))
    check("R1d P is strictly increasing in rho", mono)
    cases = [("conv", Fr(9, 10), 3), ("flag_free", Fr(19, 20), 8), ("flag_strict", Fr(19, 20), 3), ("cat", Fr(9, 10), 3)]; mc_ok = True; N = 120000
    for idx, (k, s, m) in enumerate(cases):
        ex = float(chain(seq[k], s, s ** m)); est = mc(seq[k], float(s), m, N, 1000 + idx); sig = math.sqrt(ex * (1 - ex) / N)
        good = abs(est - ex) < 4 * sig; mc_ok &= good
        print("      MC %-12s s=%-5s m=%d  exact %.5f  Monte Carlo %.5f  (|diff| = %.1f sigma)" % (k, float(s), m, ex, est, abs(est - ex) / sig))
    check("R1e gate-by-gate Monte Carlo agrees with the closed form within 4 sigma in 4 cases (N = %d each)" % N, mc_ok)
    # --- R2: conventional never beats local --------------------------------------------------------------------------------
    grid = [Fr(k, 200) for k in range(1, 200)]
    check("R2a conventional joint with FREE recovery (rho = 1) is strictly below the local s^4 at every s = k/200, k = 1..199", all(chain(seq["conv"], s, Fr(1)) < s ** 4 for s in grid))
    poly_ok = all(((1 + s + s ** 2 + s ** 3) - (1 + s ** 3 + s ** 4 + s ** 7)) == (s + s ** 2 - s ** 4 - s ** 7) == s * (1 - s ** 3) + s ** 2 * (1 - s ** 5) and s * (1 - s ** 3) + s ** 2 * (1 - s ** 5) > 0 for s in grid)
    check("R2b the algebra: P_conv(1) < s^4 iff (1-s^4) > q with q = (1-s)(1+s^3+s^4+s^7); (1+s+s^2+s^3) - (1+s^3+s^4+s^7) = s(1-s^3) + s^2(1-s^5) > 0", poly_ok)
    q_ok = all(sum(s ** j * (1 - s) for j, ri in enumerate(seq["conv"]) if ri) == (1 - s) * (1 + s ** 3 + s ** 4 + s ** 7) for s in grid)
    check("R2c the recoverable failure mass of the conventional round is (1-s)(1+s^3+s^4+s^7) (gates 1, 4, 5, 8)", q_ok)
    # --- R3: flagged / cat, free ancilla failures --------------------------------------------------------------------------
    thr = all((chain(seq["cat"], s, Fr(1) / (1 + s ** 4)) == s ** 4) for s in grid)
    check("R3a at rho = 1/(1+s^4) the cat/flagged-free joint round equals s^4 exactly, at every s = k/200", thr)
    side = all(chain(seq["cat"], s, min(Fr(1), Fr(1) / (1 + s ** 4) + Fr(1, 1000))) > s ** 4 and chain(seq["cat"], s, Fr(1) / (1 + s ** 4) - Fr(1, 1000)) < s ** 4 for s in grid)
    check("R3b slightly more recovery success than 1/(1+s^4) (capped at 1) wins, slightly less loses (strict inequalities at every s = k/200)", side)
    def f_free(m): return lambda s: chain(seq["cat"], s, s ** m) - s ** 4
    def f_strict(m): return lambda s: chain(seq["flag_strict"], s, s ** m) - s ** 4
    X = {}
    for m in (1, 3, 8, 12):
        X[("free", m)] = crossing(f_free(m)); X[("strict", m)] = crossing(f_strict(m))
    check("R3c a single sign change (joint loses below, wins above) is found on the grid for m = 1, 3, 8, 12, free policy and strict flagged", all(v is not None for v in X.values()))
    cert = all(f_free(m)(X[("free", m)][0]) <= 0 < f_free(m)(X[("free", m)][1]) and f_strict(m)(X[("strict", m)][0]) <= 0 < f_strict(m)(X[("strict", m)][1]) for m in (1, 3, 8, 12))
    check("R3d exact sign certificates at the bracket ends of every crossover (rational arithmetic)", cert)
    print("== crossover s: the joint round (flagged/cat free, or flagged strict) beats the local s^4 only ABOVE this s, when recovery needs m gates that must all succeed ==")
    print("      %-4s %-26s %-26s" % ("m", "cat / flagged, ancilla free", "flagged, strict (12 gates)"))
    for m in (1, 3, 8, 12):
        print("      %-4d %-26s %-26s" % (m, "%.6f" % float(X[("free", m)][1]), "%.6f" % float(X[("strict", m)][1])))
    print("      (cat: strict = free, because no cat gate touches data except the 8 D gates)")
    ms = lambda s: math.log(1 + s ** 4) / -math.log(s)
    print("== largest recovery gate count m*(s) = ln(1+s^4) / (-ln s) for which the joint round still beats local (free policy) ==")
    print("      " + "   ".join("s=%.2f: %.2f" % (s, ms(s)) for s in (0.99, 0.97, 0.95, 0.9, 0.85, 0.8, 0.75, 0.5)))
    check("R3e m*(s) from the formula agrees with the numerical crossover: s^m(1+s^4) = 1 at the bracket (m = 3, 8), to 1e-6",
          all(abs(float(X[("free", m)][1]) ** m * (1 + float(X[("free", m)][1]) ** 4) - 1) < 1e-6 for m in (3, 8)))
    # --- R4: strict policy ------------------------------------------------------------------------------------------------
    thr4 = all(chain(seq["flag_strict"], s, (1 + s ** 4) / (1 + s ** 4 + s ** 8)) == s ** 4 for s in grid)
    check("R4a flagged, strict policy: at rho = (1+s^4)/(1+s^4+s^8) the flagged joint round equals s^4 exactly, at every s = k/200", thr4)
    check("R4b the flagged threshold is above the cat threshold at every s (flagged needs strictly better recovery to win)", all((1 + s ** 4) / (1 + s ** 4 + s ** 8) > Fr(1) / (1 + s ** 4) for s in grid))
    check("R4c at every s = k/200 and every m in {1, 3, 8} the cat round is at least as good as the flagged-strict round, strictly better when s < 1 (checked, not claimed in general)",
          all(chain(seq["cat"], s, s ** m) > chain(seq["flag_strict"], s, s ** m) for s in grid for m in (1, 3, 8)))
    # --- table -------------------------------------------------------------------------------------------------------------
    print("== P(eventually complete one verification round with the information intact) ==")
    print("      %-6s %-8s %-9s | %-26s | %-26s | %-9s" % ("s", "local", "conv rho=1", "cat/flag-free  m=3  m=8 ", "flag-strict  m=3  m=8", "S07 P_A"))
    for s in (0.99, 0.97, 0.95, 0.93, 0.9, 0.85, 0.8, 0.75, 0.5):
        f = Fr(s)
        print("      %-6.2f %-8.4f %-9.4f | %-8.4f %-8.4f           | %-8.4f %-8.4f           | 1.0000" % (s, s ** 4, float(chain(seq["conv"], f, Fr(1))), float(chain(seq["cat"], f, f ** 3)), float(chain(seq["cat"], f, f ** 8)),
              float(chain(seq["flag_strict"], f, f ** 3)), float(chain(seq["flag_strict"], f, f ** 8))))
    print("NOTE  Every number here is conditional on the process above.  The minimum number m of inter-photon gates of an erased-axis recovery is NOT established; m = 3 is only an")
    print("      illustrative low value (one gate per remaining data axis; NOT a derived lower bound), m = 8 stands for a full verification round used as the recovery.  Waiting-time loss, the")
    print("      unheralded-loss floor (S02) and silent faults are outside this model.  The comparison with the local round gives the local round no recovery option at all.")
    print("ALL PASS" if OK else "FAILED")
    return 0 if OK else 1

if __name__ == "__main__": sys.exit(main())
