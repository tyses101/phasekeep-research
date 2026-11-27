#!/usr/bin/env python3
"""S11: what does S08's one-fatal-point conversion cost in ordinary Pauli faults?

S08 found a 7-gate conversion with one fatal heralded failure point (under per-axis erasure) against 4 gates with two.  More gates are more places for
ordinary faults.  Using V0.8's own conversion fault model (an X and a Z flip, each with probability r, on every axis a gate touches, after the gate),
this script counts, to first order in r, the single-fault events of each circuit that end as an UNDETECTED logical error when the joint checks are applied at
the end (V0.8's "accepted-wrong"), the detected ones, and the harmless ones.  First order: Y and multi-fault events are O(r^2) and are not counted.

Claims
  P1  The propagation engine reproduces V0.8's stated numbers for its example circuit (single-axis faults inserted before the gates, 12 faults: 8 detected /
      4 logical before the first CNOT, 10 / 2 between the CNOTs, 12 / 0 after).                                        DERIVED (cross-check)
  P2  First-order counts for all 24 minimum circuits, for the S08 optimum (7 gates), and over every circuit of at most 7 gates with exactly one fatal point
      under EraseAxis.                                                                                              DERIVED on the V0.8 fault model (ASSUMED)
Author-side; not an independent reproduction.  Standard library plus the S08 module.
"""
import importlib.util, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
def _load(name, rel):
    sp = importlib.util.spec_from_file_location(name, os.path.join(ROOT, *rel)); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
s08 = _load("s08", ["explorations", "s08-conversion-failure", "conversion_failure.py"])
gate, grp, mul, sp, inter, pz, L, J, GATES, correctable, lost_set, qubits, gname = (getattr(s08, k) for k in ("gate", "grp", "mul", "sp", "inter", "pz", "L", "J", "GATES", "correctable", "lost_set", "qubits", "gname"))

OK = True
def check(name, ok):
    global OK
    OK = OK and bool(ok); print(("PASS  " if ok else "FAIL  ") + name)

JG = [pz("ZZZZ"), pz("XXXX")]
def classify(p):
    if any(sp(p, g) for g in JG): return "detected"
    return "harmless" if p in J else "logical"
def run_path(p, path):
    for g in path: p = gate(g, p)
    return p
def events(path, only_two_qubit=False):
    """first-order events: after gate i, an X or a Z flip on each touched axis"""
    cnt = {"detected": 0, "logical": 0, "harmless": 0}; n = 0
    for i, g in enumerate(path):
        if only_two_qubit and len(g) < 3: continue
        for q in qubits(g):
            for pa in ((1 << q, 0), (0, 1 << q)):
                cnt[classify(run_path(pa, path[i + 1:]))] += 1; n += 1
    return cnt, n

def main():
    # graph and distances ---------------------------------------------------------------------------------------------
    order = [L]; seen = {L}; adj = {}; i = 0
    while i < len(order):
        n = order[i]; i += 1; adj[n] = []
        for g in GATES:
            m = frozenset(gate(g, p) for p in n); adj[n].append((g, m))
            if m not in seen: seen.add(m); order.append(m)
    rdist = {J: 0}; radj = {n: [] for n in order}
    for n in order:
        for g, m in adj[n]: radj[m].append(n)
    fr = [J]
    while fr:
        nx = []
        for m in fr:
            for n in radj[m]:
                if n not in rdist: rdist[n] = rdist[m] + 1; nx.append(n)
        fr = nx
    def circuits(maxlen):
        out = []
        def dfs(n, acc, nodes):
            if n == J and acc: out.append((list(acc), list(nodes)))
            if len(acc) >= maxlen: return
            for g, m in adj[n]:
                if m == n: continue
                if rdist.get(m, 99) <= maxlen - len(acc) - 1: acc.append(g); nodes.append(m); dfs(m, acc, nodes); acc.pop(); nodes.pop()
        dfs(L, [], [L]); return out
    # P1: V0.8 example circuit --------------------------------------------------------------------------------------------
    ex = [("H", 0), ("H", 1), ("CNOT", 0, 2), ("CNOT", 1, 3)]
    rows = []
    for k in range(5):
        c = {"detected": 0, "logical": 0, "harmless": 0}
        for q in range(4):
            for pa in ((1 << q, 0), (0, 1 << q), (1 << q, 1 << q)): c[classify(run_path(pa, ex[k:]))] += 1
        rows.append((c["detected"], c["logical"], c["harmless"]))
    print("      V0.8 example circuit H(0) H(1) CNOT(0,2) CNOT(1,3): single-axis faults (12) inserted before gate k: (detected, logical, harmless) per k = 0..4:", rows)
    check("P1 reproduces V0.8's stated numbers: 8 detected / 4 logical before the CNOTs (k = 0, 1, 2), 10 / 2 between them (k = 3), 12 / 0 after (k = 4)",
          all(r[:2] == (8, 4) for r in rows[:3]) and rows[3][:2] == (10, 2) and rows[4][:2] == (12, 0))
    # P2 ----------------------------------------------------------------------------------------------------------------
    c4 = circuits(4); check("P2a 24 minimum circuits enumerated", len([c for c in c4 if len(c[0]) == 4]) == 24)
    min4 = [c for c in c4 if len(c[0]) == 4]
    ev4 = sorted({(events(p)[0]["logical"], events(p)[1]) for p, _ in min4})
    print("== P2 first-order events (X and Z flip on every axis touched by every gate); logical = undetected wrong output ==")
    print("      24 minimum circuits (4 gates): distinct (logical, total events) pairs: %s" % ev4)
    c7 = circuits(7); print("      circuits of at most 7 gates from the local to the joint group (no null gates): %d" % len(c7))
    one = []
    for p, nodes in c7:
        inter_fatal = sum(1 for k, g in enumerate(p) if inter(g) and not correctable(nodes[k], lost_set(g, "EraseAxis")))
        if inter_fatal == 1: one.append((p, nodes))
    check("P2b at least one circuit of at most 7 gates has exactly one fatal point under EraseAxis (S08's optimum is one of them: %d such circuits)" % len(one), len(one) >= 1)
    s8 = [("H", 0), ("CNOT", 2, 3), ("CZ", 0, 1), ("CNOT", 0, 3), ("CNOT", 0, 1), ("CNOT", 2, 3), ("CNOT", 1, 2)]
    check("P2c S08's 7-gate optimum is among them", any(p == s8 for p, _ in one))
    res = []
    for p, nodes in one:
        e, n = events(p); e2, n2 = events(p, only_two_qubit=True); res.append((e["logical"], n, e2["logical"], n2, p))
    best_all = min(res, key=lambda r: (r[0], r[1])); best_two = min(res, key=lambda r: (r[2], r[3]))
    e4 = [events(p) for p, _ in min4]; l4 = sorted({e[0]["logical"] for e in e4}); n4 = sorted({e[1] for e in e4})
    e4b = [events(p, True) for p, _ in min4]; l4b = sorted({e[0]["logical"] for e in e4b})
    e_s8, n_s8 = events(s8); e_s8b, n_s8b = events(s8, True)
    print("      all gates as fault locations (X and Z flip on each touched axis):")
    print("        4-gate circuits:            events %s, undetected-logical events per circuit %s" % (n4, l4))
    print("        S08 7-gate optimum:         events %d, undetected-logical %d, detected %d, harmless %d" % (n_s8, e_s8["logical"], e_s8["detected"], e_s8["harmless"]))
    print("        best 1-fatal circuit <= 7:  events %d, undetected-logical %d : %s" % (best_all[1], best_all[0], [gname(g) for g in best_all[4]]))
    print("      only two-qubit gates as fault locations:")
    print("        4-gate circuits:            undetected-logical events per circuit %s (of 8 events: 2 gates x 2 axes x 2)" % l4b)
    print("        S08 7-gate optimum:         undetected-logical %d of %d" % (e_s8b["logical"], n_s8b))
    print("        best 1-fatal circuit <= 7:  undetected-logical %d of %d : %s" % (best_two[2], best_two[3], [gname(g) for g in best_two[4]]))
    print("      distribution over the %d one-fatal-point circuits (undetected-logical events, all gates): min %d, max %d" % (len(res), min(r[0] for r in res), max(r[0] for r in res)))
    check("P2d every one of the %d one-fatal-point circuits has more first-order undetected-wrong events than any 4-gate circuit (min %d versus max %d with all gates as locations; min %d versus max %d with two-qubit gates only)" %
          (len(res), min(r[0] for r in res), max(l4), min(r[2] for r in res), max(l4b)), min(r[0] for r in res) > max(l4) and min(r[2] for r in res) > max(l4b))
    ratio = best_all[0] / max(1, max(l4)) if l4 else None
    print("      reading: price of one fewer fatal heralded point, in first-order undetected-wrong events per circuit, is %+d (best 1-fatal %d versus 4-gate %s); at conversion fault probability r that is %+d r.  Heralded-loss benefit and silent-fault price are different quantities and are not combined." %
          (best_all[0] - max(l4), best_all[0], l4, best_all[0] - max(l4)))
    print("ALL PASS" if OK else "SOME CHECKS FAILED")
    return 0 if OK else 1

if __name__ == "__main__":
    sys.exit(main())
