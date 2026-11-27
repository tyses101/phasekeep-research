#!/usr/bin/env python3
"""S08: geometry conversion (local [[4,2,1]] <-> joint [[4,2,2]]) under heralded two-photon gate failure.

V0.8 found the conversion circuits; V1.0 / the V1.1 roadmap (priority 3) say that their behaviour under realistic interaction failure
is not computed ("the conversion has two inter-photon gates, completion probability s^2").  This script adds the missing piece under
the same ASSUMED erasure semantics as S07 (a failed gate heralds itself and erases the qubits it acts on, "EraseAxis", or their whole
photons, "ErasePhoton"; intra-photon gates are ideal).  There is no ancilla in the conversion, so the test is the stabilizer-code
erasure criterion on the transported code: erasing a set E is harmless iff no nontrivial logical operator is supported on E.

Claims
  K1  Group-graph cross-check of V0.8: 5355 unsigned two-check groups reachable from the local code, 4-gate minimum, 24 minimum circuits,
      each with 2 inter-photon gates.                                                                       DERIVED (reproduces V0.8)
  K2  In all 24 minimum circuits BOTH inter-photon gate failures are fatal (the logical information is lost), forward and in reverse,
      under both erasure semantics.  Loss probability is 1 - s^2 and the completion probability s^2 is also the information-preservation
      probability: the conversion has no graceful degradation.                                              DERIVED on ASSUMED semantics
  K3  Over ALL circuits in the gate set {H, S, CNOT, CZ} (any length; exact shortest-path search over the 5355 groups): under EraseAxis the
      minimum number of fatal inter-photon failure points is 1, not 2 (the first version of this script claimed 2; its own check failed and
      the search found the counterexample, see run-history.txt).  It is reached by a 7-gate circuit that decodes each photon locally, makes a
      Bell pair on the two information-free axes with the FIRST inter-photon gate, and re-encodes; only the second inter-photon gate touches
      data.  Under ErasePhoton the minimum stays 2.  No circuit has 0.                                          DERIVED on ASSUMED semantics
  K4  The state-vector Knill-Laflamme test of S07 agrees with the stabilizer criterion on every inter-photon gate of every minimum circuit and
      of the 7-gate circuit (independent methods).                                                              DERIVED (cross-check)
  K5  The 7-gate circuit is a valid conversion: state vectors show it maps the four local logical basis states to four orthonormal states in the
      joint code space up to a Pauli frame, and it induces a logical Clifford that may differ from the one of the 4-gate circuits (reported).  DERIVED
  K6  Consequence, ASSUMED semantics: with retry of the harmless failure, the probability that the conversion eventually completes before the
      information is lost is s for the 7-gate circuit and s^2 for the 4-gate circuits.  It needs two degrees of freedom of one photon to fail
      independently (open problem 4); under whole-photon erasure there is no gain.                              DERIVED on ASSUMED semantics
Signs are ignored (a Pauli frame fixes them); S is not its own inverse so the reverse of a circuit containing S is not in the same gate set
and is evaluated only for circuits without S.  Author-side; not an independent reproduction.  Requires numpy for K4 only.
"""
import heapq, importlib.util, itertools, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
def _load(name, rel):
    sp = importlib.util.spec_from_file_location(name, os.path.join(ROOT, *rel)); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
s07 = _load("s07", ["explorations", "s07-failure-semantics", "failure_semantics.py"])
sv = s07.sv

OK = True
def check(name, ok):
    global OK
    OK = OK and bool(ok); print(("PASS  " if ok else "FAIL  ") + name)

def pz(s):
    x = z = 0
    for q, c in enumerate(s):
        if c in "XY": x |= 1 << q
        if c in "ZY": z |= 1 << q
    return (x, z)
def mul(a, b): return (a[0] ^ b[0], a[1] ^ b[1])
def sp(a, b): return (bin(a[0] & b[1]).count("1") + bin(a[1] & b[0]).count("1")) & 1
def grp(gens):
    G = {(0, 0)}
    for g in gens: G |= {mul(h, g) for h in G}
    return frozenset(G)
def gate(g, p):
    k = g[0]; x, z = p
    if k == "H":
        q = g[1]
        if ((x >> q) & 1) != ((z >> q) & 1): x ^= 1 << q; z ^= 1 << q
    elif k == "S":
        if (x >> g[1]) & 1: z ^= 1 << g[1]
    elif k == "CNOT":
        c, t = g[1], g[2]
        if (x >> c) & 1: x ^= 1 << t
        if (z >> t) & 1: z ^= 1 << c
    elif k == "CZ":
        a, b = g[1], g[2]
        if (x >> b) & 1: z ^= 1 << a
        if (x >> a) & 1: z ^= 1 << b
    return (x, z)
GATES = [("H", q) for q in range(4)] + [("S", q) for q in range(4)] + [("CNOT", c, t) for c in range(4) for t in range(4) if c != t] + [("CZ", a, b) for a in range(4) for b in range(a + 1, 4)]
def qubits(g): return g[1:]
def photon(q): return q // 2                       # photon 0 = axes 0,1 ; photon 1 = axes 2,3
def inter(g): return len(g) == 3 and photon(g[1]) != photon(g[2])
def gname(g): return g[0] + "(" + ",".join(str(q) for q in g[1:]) + ")"
L = grp([pz("ZZII"), pz("IIZZ")]); J = grp([pz("ZZZZ"), pz("XXXX")])
PAULIS = [(x, z) for x in range(16) for z in range(16)]
def supp(p): return p[0] | p[1]
def correctable(G, E):
    mask = sum(1 << q for q in E); gens = [p for p in G if p != (0, 0)]
    for p in PAULIS:
        if supp(p) & ~mask: continue
        if all(sp(p, g) == 0 for g in gens) and p not in G: return False
    return True
def lost_set(g, sem):
    E = set(qubits(g))
    if sem == "ErasePhoton": E = {q for q in range(4) if photon(q) in {photon(x) for x in E}}
    return E
def weights(G): return sorted(bin(p[0] | p[1]).count("1") for p in G if p != (0, 0))

def main():
    # graph ----------------------------------------------------------------------------------------------------------------
    order = [L]; seen = {L}; adj = {}; i = 0
    while i < len(order):
        n = order[i]; i += 1; adj[n] = []
        for g in GATES:
            m = frozenset(gate(g, p) for p in n); adj[n].append((g, m))
            if m not in seen: seen.add(m); order.append(m)
    dist = {L: 0}; fr = [L]; cnt = {L: 1}
    while fr and J not in dist:
        nx = []
        for n in fr:
            for g, m in adj[n]:
                if m not in dist: dist[m] = dist[n] + 1; cnt[m] = 0; nx.append(m)
                if dist[m] == dist[n] + 1: cnt[m] += cnt[n]
        fr = nx
    check("K1a %d unsigned two-check groups reachable from the local code (V0.8: at most 21,420 signed = 4 x 5355)" % len(order), len(order) == 5355)
    check("K1b shortest conversion has %d gates and there are %d such circuits (V0.8: 4 gates, 24 circuits)" % (dist[J], cnt[J]), dist[J] == 4 and cnt[J] == 24)
    # enumerate the minimum circuits
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
    paths = []
    def dfs(n, acc, nodes):
        if n == J and len(acc) == dist[J]: paths.append((list(acc), list(nodes))); return
        if len(acc) >= dist[J]: return
        for g, m in adj[n]:
            if rdist.get(m, 99) == dist[J] - len(acc) - 1: acc.append(g); nodes.append(m); dfs(m, acc, nodes); acc.pop(); nodes.pop()
    dfs(L, [], [L])
    check("K1c enumerated %d minimum circuits, every one with exactly 2 inter-photon gates" % len(paths), len(paths) == 24 and all(sum(inter(g) for g in p) == 2 for p, _ in paths))
    ex = next(p for p in paths if all(g[0] in ("H", "CNOT") for g in p[0]) and p[0][0] == ("H", 0))
    print("      example circuit:", [gname(g) for g in ex[0]])
    for k, n in enumerate(ex[1]): print("        after %d gates: check weights %s" % (k, weights(n)))
    # K2 -------------------------------------------------------------------------------------------------------------------
    pats = {}
    for p, nodes in paths:
        for sem in ("EraseAxis", "ErasePhoton"):
            fwd = tuple(int(correctable(nodes[k], lost_set(g, sem))) for k, g in enumerate(p) if inter(g))
            rev = tuple(int(correctable(nodes[k + 1], lost_set(g, sem))) for k, g in enumerate(p) if inter(g))    # inverse circuit: gate k undone on the code AFTER it
            pats[(sem, "forward")] = pats.get((sem, "forward"), set()) | {fwd}
            if not any(g[0] == "S" for g in p): pats[(sem, "reverse")] = pats.get((sem, "reverse"), set()) | {rev}
    print("== K2 recoverability pattern r of the 2 inter-photon gates over the 24 minimum circuits (distinct patterns) ==")
    for k, v in sorted(pats.items()): print("      %-12s %-8s %s" % (k[0], k[1], sorted(v)))
    check("K2 every inter-photon failure is fatal (r = 00) for every minimum circuit, both directions, both semantics", all(v == {(0, 0)} for v in pats.values()))
    for s in (0.95, 0.75, 0.5): print("      s = %-5g completion = information preserved = s^2 = %.4f ; loss probability = %.4f" % (s, s * s, 1 - s * s))
    # K3: lexicographic shortest path: minimise (fatal inter-photon points, inter-photon gates, total gates) ---------------------------
    import heapq
    def search(sem):
        best = {L: (0, 0, 0)}; prev = {}; heap = [((0, 0, 0), 0, L)]; t = 0
        while heap:
            d, _, n = heapq.heappop(heap)
            if d > best[n]: continue
            for g, m in adj[n]:
                if m == n: continue
                f = 1 if (inter(g) and not correctable(n, lost_set(g, sem))) else 0
                nd = (d[0] + f, d[1] + (1 if inter(g) else 0), d[2] + 1)
                if m not in best or nd < best[m]: best[m] = nd; prev[m] = (n, g); t += 1; heapq.heappush(heap, (nd, t, m))
        gs = []; nodes = [J]; n = J
        while n != L: pn, g = prev[n]; gs.append(g); nodes.append(pn); n = pn
        return best[J], list(reversed(gs)), list(reversed(nodes))
    found = {}
    for sem in ("EraseAxis", "ErasePhoton"):
        found[sem] = search(sem); b_, gs_, nd_ = found[sem]
        print("      %-12s best over all circuits (fatal inter-photon points, inter-photon gates, total gates) = %s" % (sem, b_))
    b7, g7, n7 = found["EraseAxis"]
    print("      EraseAxis optimum circuit:", [gname(g) for g in g7])
    for k, g in enumerate(g7):
        tag = ""
        if inter(g): tag = "   INTER-PHOTON, lost axes %s, recoverable = %s" % (sorted(lost_set(g, "EraseAxis")), correctable(n7[k], lost_set(g, "EraseAxis")))
        print("        %-12s check weights after: %s%s" % (gname(g), weights(n7[k + 1]), tag))
    clean = [q for q in range(4) if any(pp != (0, 0) and bin(pp[0] | pp[1]).count("1") == 1 and ((pp[0] | pp[1]) >> q) & 1 for pp in n7[3])]
    print("      the information-free (clean) axes before the first inter-photon gate: %s (single-axis stabilizers present)" % clean)
    check("K3a EraseAxis: minimum fatal inter-photon points over all circuits is 1 (not 0, not 2), with 2 inter-photon gates in 7 gates", b7 == (1, 2, 7))
    check("K3b ErasePhoton: minimum fatal points is 2 = the minimum number of inter-photon gates (a failed gate erases both photons, i.e. everything)", found["ErasePhoton"][0][0] == 2 and found["ErasePhoton"][0][1] == 2)
    check("K3c in the optimum circuit the first inter-photon gate acts only on the two clean axes (recoverable) and the second is fatal",
          [int(correctable(n7[k], lost_set(g, "EraseAxis"))) for k, g in enumerate(g7) if inter(g)] == [1, 0] and set(lost_set(g7[3], "EraseAxis")) <= set(clean))
    # K4: cross-check with state vectors ----------------------------------------------------------------------------------
    basis = s07.code_basis("L"); sim = sv.Sim(4); agree = True; n_t = 0
    for p, nodes in paths + [(g7, n7)]:
        for sem in ("EraseAxis", "ErasePhoton"):
            for k, g in enumerate(p):
                if not inter(g): continue
                phis = []
                for j in range(4):
                    v = basis[:, j].astype(complex)
                    for gg in p[:k]:
                        if gg[0] == "H": v = sim.one(v, sv.HAD, gg[1])
                        elif gg[0] == "S": v = sim.one(v, np.diag([1, 1j]), gg[1])
                        elif gg[0] == "CNOT": v = sim.cnot(v, gg[1], gg[2])
                        else: v = sim.cz(v, gg[1], gg[2])
                    phis.append(v)
                lost, E = s07.lost_blocks(sim, phis, lost_set(g, sem)); rho = E[(0, 0)]
                kl = all(np.allclose(E[(a, a)], rho, atol=1e-9) for a in range(4)) and all(np.allclose(E[(a, b)], 0, atol=1e-9) for a in range(4) for b in range(4) if a != b)
                agree &= (kl == correctable(nodes[k], lost_set(g, sem))); n_t += 1
    check("K4 state-vector Knill-Laflamme test and stabilizer criterion agree on all %d (circuit, gate, semantics) cases, including the 7-gate circuit" % n_t, agree)
    # K5: is the 7-gate circuit a valid conversion?
    ZZZZ = {q: "Z" for q in range(4)}; XXXX = {q: "X" for q in range(4)}
    outs = []
    for j in range(4):
        v = basis[:, j].astype(complex)
        for gg in g7:
            if gg[0] == "H": v = sim.one(v, sv.HAD, gg[1])
            elif gg[0] == "S": v = sim.one(v, np.diag([1, 1j]), gg[1])
            elif gg[0] == "CNOT": v = sim.cnot(v, gg[1], gg[2])
            else: v = sim.cz(v, gg[1], gg[2])
        outs.append(v)
    ev = [(np.vdot(o, sim.pauli(o, ZZZZ)).real, np.vdot(o, sim.pauli(o, XXXX)).real) for o in outs]
    gram = np.array([[np.vdot(a, b) for b in outs] for a in outs])
    sup = sum(c * o for c, o in zip([0.5, 0.5j, -0.5, 0.5], outs)); evs = (np.vdot(sup, sim.pauli(sup, ZZZZ)).real, np.vdot(sup, sim.pauli(sup, XXXX)).real)
    check("K5a the 7-gate circuit maps the four local logical basis states to orthonormal states with deterministic joint-check values (ZZZZ, XXXX) = %s, the same for a superposition (a sign is a Pauli frame)" % [tuple(int(round(x)) for x in e) for e in ev][:1],
          np.allclose(gram, np.eye(4), atol=1e-9) and all(abs(abs(e[0]) - 1) < 1e-9 and abs(abs(e[1]) - 1) < 1e-9 for e in ev) and all(np.allclose(ev[0], e) for e in ev) and np.allclose(ev[0], evs))
    def lmap(gs):
        img = []
        for lg in ("XXII", "ZIII", "IIXX", "IIIZ"):
            pp = pz(lg)
            for gg in gs: pp = gate(gg, pp)
            img.append(pp)
        return img
    def same_mod_J(m1, m2): return all(mul(a, b) in J for a, b in zip(m1, m2))
    ref = lmap(paths[0][0]); classes = []
    for p, _ in paths:
        mp = lmap(p)
        if not any(same_mod_J(mp, c) for c in classes): classes.append(mp)
    m7 = lmap(g7); same = any(same_mod_J(m7, c) for c in classes)
    def pstr_(pp): return "".join("I" if not ((pp[0] >> q) & 1 or (pp[1] >> q) & 1) else ("Y" if (pp[0] >> q) & 1 and (pp[1] >> q) & 1 else ("X" if (pp[0] >> q) & 1 else "Z")) for q in range(4))
    def rep(pp): return pstr_(min((mul(pp, g) for g in J), key=lambda r: (bin(r[0] | r[1]).count("1"), pstr_(r))))
    for ci, c in enumerate(classes): print("        class %d (X1,Z1,X2,Z2 of the local code -> joint-code operators, lowest weight): %s" % (ci, [rep(x) for x in c]))
    print("        7-gate circuit:                                                                         %s" % [rep(x) for x in m7])
    print("      logical maps of the 24 minimum circuits fall into %d distinct class(es) modulo the joint stabilizers; the 7-gate circuit's map %s one of them" % (len(classes), "equals" if same else "differs from every"))
    check("K5b every logical operator of the local code is carried to a joint-code logical operator by the 7-gate circuit (a possibly different logical Clifford, to be tracked)", all(all(sp(img, g) == 0 for g in [pz("ZZZZ"), pz("XXXX")]) and img not in J for img in m7))
    # K6: consequence
    print("== K6 retry-on-harmless-failure consequence (ASSUMED semantics; harmless failure = the two clean axes are erased and re-prepared) ==")
    print("      %-6s %-26s %-34s" % ("s", "4-gate: eventually completes", "7-gate: eventually completes (P_loss per attempt s(1-s))"))
    for s_ in (0.95, 0.75, 0.5):
        print("      %-6g %-26.4f %-34.4f" % (s_, s_ * s_, (s_ * s_) / (s_ * s_ + s_ * (1 - s_))))
    check("K6 P(complete before loss) = s^2 / (s^2 + s(1-s)) = s for the 7-gate circuit (equals s) versus s^2 for the 4-gate circuits", all(abs((s_ * s_) / (s_ * s_ + s_ * (1 - s_)) - s_) < 1e-12 for s_ in (0.3, 0.5, 0.75, 0.95)))
    # controls for the criterion itself
    check("C1 control: erasing one axis of the joint code is recoverable, two axes on different photons are not; erasing one axis of the local code is not",
          correctable(J, {0}) and not correctable(J, {0, 2}) and not correctable(L, {0}))
    print("== reading ==")
    print("      4-gate circuits: both inter-photon gates act on data-carrying axes, so under erasure-type failure the conversion has no graceful degradation (loss 1 - s^2).")
    print("      The 7-gate circuit moves one inter-photon gate onto two information-free axes, which halves the number of fatal points, but only if the two degrees of freedom of a")
    print("      photon can fail independently (EraseAxis).  With whole-photon erasure the minimum is 2 again.  This is a design lever and a falsifiable dependency, not a hardware claim.")
    print("ALL PASS" if OK else "SOME CHECKS FAILED")
    return 0 if OK else 1

if __name__ == "__main__":
    sys.exit(main())
