#!/usr/bin/env python3
"""S06: how often can one stabilizer basis be turned into another with local operations only, and what does it cost
in entangling gates when not?  Exact for n = 1..4 qubits (n = 5 for the counting part).

Objects: a stabilizer basis of n qubits is a maximal commuting Pauli group (a Lagrangian subspace of F_2^{2n}); there
are prod_{i=1}^{n} (2^i + 1) of them (3, 15, 135, 2295, 75735).  Two bases are "locally related" when a product of
single-qubit Cliffords maps one to the other as a set.  The cost of a pair is the fewest CNOTs in a Clifford circuit
that maps one basis to the other as a set, with single-qubit Cliffords free (and, in a second count, qubit swaps free).
Generalises V0's two-qubit count (225 ordered pairs, 108 needing an entangling gate).

Claims
  B1  n = 1, 2, 3, 4: number of bases, local orbits, ordered pairs that need an entangling gate.  n = 2 reproduces
      V0's 225 and 108.                                                                              DERIVED
  B2  Provable bound: the fraction of ordered pairs related by local Cliffords is at most 6^n / prod (2^i+1), which tends
      to 0; the exact fractions for n <= 5 are listed.                                                 DERIVED
  B3  Exact distribution of the minimum CNOT cost over all ordered pairs (n = 2, 3, 4; n = 5 with --n5, about 20 minutes),
      its mean and maximum.  The pattern max = n - 1 seen for n <= 4 is FALSE at n = 5 (max 5).  DERIVED
Scope: stabilizer bases and Clifford circuits only.  It says nothing about non-stabilizer bases, continuous-variable
or high-dimensional photonic encodings, or the cost of a CNOT in any hardware.  Author-side.  Standard library only.
"""
import sys, time
from collections import defaultdict, deque

OK = True
def check(name, ok):
    global OK
    OK = OK and bool(ok)
    print(("PASS  " if ok else "FAIL  ") + name)

def rref(vs):
    rows = []
    for v in vs:
        for r in rows:
            if v ^ r < v: v ^= r
        if v:
            rows = [r ^ v if r ^ v < r else r for r in rows]
            rows.append(v)
    rows.sort(reverse=True)
    return tuple(rows)

def mkgates(n):
    mx = (1 << n) - 1
    def H(i):
        def f(v):
            x, z = v & mx, v >> n
            xi, zi = (x >> i) & 1, (z >> i) & 1
            if xi != zi: x ^= 1 << i; z ^= 1 << i
            return x | (z << n)
        return f
    def S(i):
        def f(v):
            x, z = v & mx, v >> n
            if (x >> i) & 1: z ^= 1 << i
            return x | (z << n)
        return f
    def CN(c, t):
        def f(v):
            x, z = v & mx, v >> n
            if (x >> c) & 1: x ^= 1 << t
            if (z >> t) & 1: z ^= 1 << c
            return x | (z << n)
        return f
    def SW(i, j):
        def f(v):
            x, z = v & mx, v >> n
            xi, xj, zi, zj = (x >> i) & 1, (x >> j) & 1, (z >> i) & 1, (z >> j) & 1
            if xi != xj: x ^= (1 << i) | (1 << j)
            if zi != zj: z ^= (1 << i) | (1 << j)
            return x | (z << n)
        return f
    local = [H(i) for i in range(n)] + [S(i) for i in range(n)]
    cnots = [CN(c, t) for c in range(n) for t in range(n) if c != t]
    swaps = [SW(i, j) for i in range(n) for j in range(i + 1, n)]
    return local, cnots, swaps

def act(g, B): return rref([g(v) for v in B])

def all_bases(n, local, cnots):
    start = rref([1 << (n + i) for i in range(n)])            # computational (Z) basis: generators Z_i
    seen = {start: 0}; order = [start]; dq = deque([start])
    gens = local + cnots
    while dq:
        B = dq.popleft()
        for g in gens:
            C = act(g, B)
            if C not in seen: seen[C] = len(order); order.append(C); dq.append(C)
    return order, seen

def orbits(order, seen, gens):
    comp = [-1] * len(order); sizes = []
    for i in range(len(order)):
        if comp[i] >= 0: continue
        c = len(sizes); comp[i] = c; st = [i]; cnt = 0
        while st:
            j = st.pop(); cnt += 1
            for g in gens:
                k = seen[act(g, order[j])]
                if comp[k] < 0: comp[k] = c; st.append(k)
        sizes.append(cnt)
    return comp, sizes

def zero_one_bfs(src, order, seen, local, cnots):
    """min number of CNOTs from basis index src to every basis (local gates cost 0, CNOT cost 1)."""
    INF = 10 ** 9; dist = [INF] * len(order); dist[src] = 0; dq = deque([src])
    while dq:
        j = dq.popleft(); d = dist[j]
        for g in local:
            k = seen[act(g, order[j])]
            if dist[k] > d: dist[k] = d; dq.appendleft(k)
        for g in cnots:
            k = seen[act(g, order[j])]
            if dist[k] > d + 1: dist[k] = d + 1; dq.append(k)
    return dist

def main():
    prod = lambda n: 1
    expected_N = {1: 3, 2: 15, 3: 135, 4: 2295, 5: 75735}
    results = {}
    for n in ((1, 2, 3, 4, 5) if '--n5' in sys.argv else (1, 2, 3, 4)):
        t0 = time.time()
        local, cnots, swaps = mkgates(n)
        order, seen = all_bases(n, local, cnots)
        N = len(order)
        check("n=%d the number of stabilizer bases is prod (2^i+1) = %d" % (n, expected_N[n]), N == expected_N[n])
        comp, sizes = orbits(order, seen, local)
        comp2, sizes2 = orbits(order, seen, local + swaps) if swaps else (comp, sizes)
        pairs_local = sum(s * s for s in sizes); pairs_local2 = sum(s * s for s in sizes2)
        need = N * N - pairs_local; need2 = N * N - pairs_local2
        results[n] = dict(N=N, orbits=len(sizes), sizes=sorted(sizes, reverse=True), need=need, orbits2=len(sizes2), need2=need2)
        print("      n=%d  bases %d | local-Clifford orbits %d sizes %s | ordered pairs %d, need >=1 entangling gate: %d (%.1f%%) | with free swaps: %d orbits, %d (%.1f%%)   [%.1f s]" % (
            n, N, len(sizes), sorted(sizes, reverse=True)[:8], N * N, need, 100 * need / N ** 2, len(sizes2), need2, 100 * need2 / N ** 2, time.time() - t0))
        # B3: min-CNOT cost distribution over all ordered pairs, using one representative per local orbit
        if n >= 2:
            hist = defaultdict(int); rep = {}
            for i, c in enumerate(comp): rep.setdefault(c, i)
            for c, i in rep.items():
                dist = zero_one_bfs(i, order, seen, local, cnots)
                for d in dist: hist[d] += sizes[c]
            tot = sum(hist.values()); mean = sum(d * v for d, v in hist.items()) / tot; mx = max(hist)
            results[n].update(hist=dict(sorted(hist.items())), mean=mean, maxcost=mx)
            print("        minimum CNOT cost over all %d ordered pairs: %s   mean %.3f  maximum %d" % (tot, dict(sorted(hist.items())), mean, mx))
            check("n=%d every pair is reachable (cost finite) and the cost-0 pairs equal the locally related pairs" % n, tot == N * N and hist[0] == pairs_local)
    check("B1 n=2 reproduces V0: 15 bases, 225 ordered pairs, 108 needing an entangling gate (2 x 9 x 6)", results[2]["N"] == 15 and results[2]["need"] == 108 and results[2]["sizes"] == [9, 6])
    check("B1b n=2: the maximum cost is 1 CNOT (every product<->entangled pair is one CNOT-class move)", results[2]["maxcost"] == 1 and results[2]["hist"] == {0: 117, 1: 108})
    # B2 provable bound
    print("== B2 bound: fraction of ordered pairs related by local Cliffords <= 6^n / N_n ==")
    exact_frac = {n: 1 - results[n]["need"] / results[n]["N"] ** 2 for n in results}
    Nn = {1: 3, 2: 15, 3: 135, 4: 2295, 5: 75735, 6: 75735 * 65, 7: 75735 * 65 * 129, 8: 75735 * 65 * 129 * 257}
    for n in range(1, 9):
        b = 6 ** n / Nn[n]
        print("      n=%d  N=%-12d bound 6^n/N = %-10.4g exact locally-related fraction %s" % (n, Nn[n], b, ("%.4f" % exact_frac[n]) if n in exact_frac else "(not computed)"))
    check("B2a the exact local fractions respect the bound for n = 1..4 (6^n/N >= fraction)", all(6 ** n / Nn[n] + 1e-12 >= exact_frac[n] for n in exact_frac))
    check("B2b the bound is below 1 from n = 4 and below 1% from n = 6, and tends to 0 (6^n grows like e^{1.8 n}, N like 2^{n(n+1)/2})", 6 ** 4 / Nn[4] < 1 and 6 ** 6 / Nn[6] < 0.01 and 6 ** 8 / Nn[8] < 1e-4)
    mc = {n: results[n]["maxcost"] for n in results if n >= 2}
    print("      maximum minimum-CNOT cost found:", mc)
    check("B3a for n = 2, 3, 4 the maximum minimum-CNOT cost is n - 1 (1, 2, 3), exact over all ordered pairs", all(mc[n] == n - 1 for n in (2, 3, 4) if n in mc))
    if 5 in mc:
        check("B3b the pattern 'maximum = n - 1' is FALSE at n = 5: the maximum is %d (not 4); the conjecture formed from n <= 4 is retracted and no formula is claimed" % mc[5], mc[5] == 5)
    print("ALL PASS" if OK else "SOME CHECKS FAILED")
    return 0 if OK else 1

if __name__ == "__main__":
    sys.exit(main())
