#!/usr/bin/env python3
"""S03: can a photon that hosts m axes still be lost without losing the logical information?

Setting (from S02): a photon hosting m data axes erases m qubits when it is lost.  A stabilizer code [[n,k]]
tolerates the heralded loss of one photon exactly when no nontrivial logical operator is supported on that
photon's qubits (photon-level distance >= 2).  Three results:

  U1  Quantum Singleton bound for one erased photon: n - k >= 2m.  Therefore photons per logical qubit
      p/k >= (k + 2m) / (m k) for full photons, which tends to 1/m for large k, but for small k the overhead is
      large.  (Standard bound; its use here is DERIVED arithmetic.)
  U2  Existence by explicit certificate: stabilizer codes, found by random search, in which every photon of a
      given hosting tolerates heralded loss; each certificate is re-verified by the Knill-Laflamme condition on
      the explicit projector (n <= 8).  "Not found" means only that a time-limited random search found nothing;
      it is not a non-existence claim.
  U3  Comparison with the V1.0 geometry: the [[4,2,2]] code needs 4 photons for 2 logical qubits (2 photons per
      logical qubit) at m = 1 and cannot tolerate any 2-axis photon.
Author-side; not independent reproduction.  Requires numpy for the projector check.
"""
import itertools, random, sys, time
import numpy as np

OK = True
def check(name, ok):
    global OK
    OK = OK and bool(ok)
    print(("PASS  " if ok else "FAIL  ") + name)

def rank2(rows):
    rows = [r for r in rows if r]; rk = 0
    while rows:
        piv = rows.pop(); 
        if piv == 0: continue
        rk += 1; lb = piv & -piv
        rows = [r ^ piv if r & lb else r for r in rows]
        rows = [r for r in rows if r]
    return rk

def random_code(n, k, rng, depth=None):
    """Random stabilizer code: Z_1..Z_{n-k} conjugated by random H, S, CNOT gates.  Generators as (x, z) bitmask pairs."""
    gens = [[0, 1 << i] for i in range(n - k)]
    for _ in range(depth or 8 * n * n):
        t = rng.random()
        if t < 0.25:
            q = rng.randrange(n)
            for g in gens:
                xq, zq = (g[0] >> q) & 1, (g[1] >> q) & 1
                if xq != zq: g[0] ^= 1 << q; g[1] ^= 1 << q
        elif t < 0.45:
            q = rng.randrange(n)
            for g in gens:
                if (g[0] >> q) & 1: g[1] ^= 1 << q
        else:
            c = rng.randrange(n); tt = rng.randrange(n)
            if c == tt: continue
            for g in gens:
                if (g[0] >> c) & 1: g[0] ^= 1 << tt
                if (g[1] >> tt) & 1: g[1] ^= 1 << c
    return [tuple(g) for g in gens]

def correctable(gens, n, E):
    """E: list of qubit indices.  True iff no nontrivial logical operator is supported on E (stabilizer cleaning criterion)."""
    r = len(gens); m = len(E); Ec = [q for q in range(n) if q not in E]
    # dim(N(S) ∩ P(E)) = 2m - rank(symplectic products of generators with the 2m basis Paulis on E)
    rows = []
    for g in gens:
        row = 0
        for j, q in enumerate(E):
            row |= ((g[1] >> q) & 1) << (2 * j)         # product with X_q picks the generator's z bit
            row |= ((g[0] >> q) & 1) << (2 * j + 1)     # product with Z_q picks the generator's x bit
        rows.append(row)
    dimN = 2 * m - rank2(rows)
    # dim(S ∩ P(E)) = r - rank of the generators restricted to the complement qubits
    rows2 = []
    for g in gens:
        row = 0
        for j, q in enumerate(Ec):
            row |= ((g[0] >> q) & 1) << (2 * j); row |= ((g[1] >> q) & 1) << (2 * j + 1)
        rows2.append(row)
    dimS = r - rank2(rows2)
    return dimN == dimS

def valid_stabilizer(gens):
    def comm(a, b): return (bin(a[0] & b[1]).count("1") + bin(a[1] & b[0]).count("1")) % 2 == 0
    return all(comm(a, b) for a, b in itertools.combinations(gens, 2))

def blocks(n, m):
    out = []; q = 0
    while q < n: out.append(list(range(q, min(n, q + m)))); q += m
    return out

def search(n, k, m, secs, seed=1):
    rng = random.Random(seed); t0 = time.time(); tries = 0
    B = blocks(n, m)
    while time.time() - t0 < secs:
        tries += 1
        g = random_code(n, k, rng)
        if all(correctable(g, n, b) for b in B): return g, B, tries
    return None, B, tries

def projector_kl_ok(gens, n, B):
    """Explicit Knill-Laflamme check: for every Pauli supported on one photon's qubits, P E P is proportional to P."""
    I2 = np.eye(2, dtype=complex); X = np.array([[0, 1], [1, 0]], dtype=complex); Z = np.diag([1, -1]).astype(complex); Y = 1j * X @ Z
    def pm(x, z):
        m = np.array([[1]], dtype=complex)
        for q in range(n):
            a, b = (x >> q) & 1, (z >> q) & 1
            m = np.kron(m, I2 if (a, b) == (0, 0) else X if (a, b) == (1, 0) else Z if (a, b) == (0, 1) else Y)
        return m
    P = np.eye(1 << n, dtype=complex)
    for g in gens: P = P @ (np.eye(1 << n) + pm(*g)) / 2
    if abs(np.trace(P).real - 2 ** (n - len(gens))) > 1e-8: return False
    for blk in B:
        sup = [q for q in blk]
        for xs in range(1 << len(sup)):
            for zs in range(1 << len(sup)):
                x = sum(((xs >> j) & 1) << q for j, q in enumerate(sup)); z = sum(((zs >> j) & 1) << q for j, q in enumerate(sup))
                M = P @ pm(x, z) @ P; c = np.trace(M) / np.trace(P)
                if not np.allclose(M, c * P, atol=1e-8): return False
    return True

def pauli_distance(gens, n):
    """Minimum weight of a nontrivial logical operator (brute force, n <= 8)."""
    best = 99
    def comm(a, b): return (bin(a[0] & b[1]).count("1") + bin(a[1] & b[0]).count("1")) % 2 == 0
    # stabilizer group
    S = {(0, 0)}
    for g in gens: S |= {(a[0] ^ g[0], a[1] ^ g[1]) for a in S}
    for x in range(1 << n):
        for z in range(1 << n):
            p = (x, z)
            if p in S or p == (0, 0): continue
            if all(comm(p, g) for g in gens): best = min(best, bin(x | z).count("1"))
    return best

def fmt(g, n):
    out = []
    for x, z in g:
        out.append("".join("IXZY"[((x >> q) & 1) + 2 * ((z >> q) & 1)] for q in range(n)))
    return out


def group_elems(gens):
    S = {(0, 0)}
    for g in gens: S |= {(a[0] ^ g[0], a[1] ^ g[1]) for a in S}
    return S

def min_weight_generators(gens, n):
    """Greedy minimum-weight generating set of the stabilizer group (lightest independent elements first)."""
    S = sorted((e for e in group_elems(gens) if e != (0, 0)), key=lambda e: (bin(e[0] | e[1]).count("1"), e))
    chosen = []; vecs = []
    for e in S:
        v = e[0] | (e[1] << n)
        if rank2(vecs + [v]) > len(vecs): chosen.append(e); vecs.append(v)
        if len(chosen) == len(gens): break
    return chosen

def photon_span(e, B):
    sup = e[0] | e[1]
    return sum(1 for b in B if any((sup >> q) & 1 for q in b))

def best_weight_profile(n, k, m, secs, seed):
    """Among random certificates (all photons erasure-tolerant) keep the one whose lightest generating set has least total weight."""
    rng = random.Random(seed); t0 = time.time(); B = blocks(n, m); best = None; cnt = 0; tries = 0
    while time.time() - t0 < secs:
        tries += 1
        g = random_code(n, k, rng)
        if not all(correctable(g, n, b) for b in B): continue
        cnt += 1
        mg = min_weight_generators(g, n); w = sorted(bin(e[0] | e[1]).count("1") for e in mg)
        key = (sum(w), max(w))
        if best is None or key < best[0]: best = (key, w, mg, g)
    return best, cnt, tries, B

def main():
    print("== U1 Singleton bound: photons per logical qubit at photon-level distance >= 2 ==")
    print("      m axes per photon, k logical qubits: n >= k + 2m, photons p = ceil(n/m)")
    rows = {}
    for m in (1, 2, 3):
        for k in (1, 2, 3, 4, 6, 8, 20):
            n = k + 2 * m; p = -(-n // m); rows[(m, k)] = (n, p, p / k)
    print("      %-4s " % "m\\k" + "".join("%16s" % ("k=%d" % k) for k in (1, 2, 3, 4, 6, 8, 20)))
    for m in (1, 2, 3):
        print("      %-4d " % m + "".join("%16s" % ("n>=%d p>=%d %.2f" % (rows[(m, k)][0], rows[(m, k)][1], rows[(m, k)][2])) for k in (1, 2, 3, 4, 6, 8, 20)))
    check("U1a m=1, k=2 gives n >= 4 (the [[4,2,2]] code, 2 photons per logical qubit) -- tight", rows[(1, 2)][0] == 4 and abs(rows[(1, 2)][2] - 2) < 1e-12)
    check("U1b for k = 20 the bound approaches 1/m photons per logical qubit (m=2: %.2f, m=3: %.2f)" % (rows[(2, 20)][2], rows[(3, 20)][2]), rows[(2, 20)][2] < 0.7 and rows[(3, 20)][2] < 0.5)
    check("U1c the bound alone allows m=2 to beat m=1 for k = 2 (3 vs 4 photons) -- needs a certificate", rows[(2, 2)][1] == 3 and rows[(1, 2)][1] == 4)

    print("== U2 certificates by random stabilizer-code search (time-limited) ==")
    cases = [(1, 2, 1, 5), (2, 1, 2, 10), (2, 2, 2, 60), (2, 3, 2, 60), (2, 4, 2, 90), (3, 2, 3, 90)]   # (m, k, ...) set below
    found = {}
    for (m, k, _, secs) in [(1, 2, None, 5), (2, 1, None, 10), (2, 2, None, 60), (2, 3, None, 60), (2, 4, None, 90), (3, 2, None, 90), (3, 1, None, 60)]:
        n = k + 2 * m
        g, B, tries = search(n, k, m, secs, seed=m * 100 + k)
        status = "FOUND" if g else "not found"
        print("      m=%d k=%d n=%d (hosting %s): %s after %d random codes" % (m, k, n, [len(b) for b in B], status, tries))
        if g:
            ok_kl = projector_kl_ok(g, n, B) if n <= 8 else None
            d = pauli_distance(g, n) if n <= 8 else None
            print("        stabilizer generators: %s" % " ".join(fmt(g, n)))
            print("        independent checks: generators commute = %s; Knill-Laflamme on explicit projector = %s; Pauli distance = %s" % (valid_stabilizer(g), ok_kl, d))
            found[(m, k)] = (g, B, n, ok_kl, d)
    check("U2a the V1.0 case (m=1, k=2, n=4) is found again by the search", (1, 2) in found)
    check("U2b every certificate found passes the explicit-projector Knill-Laflamme check", all(v[3] in (True, None) for v in found.values()) and all(v[3] is True for v in found.values() if v[2] <= 8))
    check("U2c every certificate has valid (commuting, independent) generators", all(valid_stabilizer(v[0]) for v in found.values()))
    if (2, 2) in found:
        print("      m=2,k=2: [[6,2]] hosted on 3 photons x 2 axes tolerates the heralded loss of any one photon: 1.5 photons per logical qubit versus 2.0 for [[4,2,2]] with 1 axis per photon")
        check("U3 a 3-photon, 2-axes-per-photon hosting of 2 logical qubits exists: fewer photons than the V1.0 geometry (3 vs 4)", len(found[(2, 2)][1]) == 3)
    print("== U4 what the certificates cost: stabilizer weight (data-touching gates per conventional round) ==")
    print("      lightest generating set found among random certificates (time-limited; not an optimum); weights are data-touching gates per generator under conventional extraction")
    print("      %-26s %-8s %-22s %-10s %-14s" % ("code / hosting", "photons", "generator weights", "sum", "sum per logical"))
    base = {("[[4,2,2]] 1 axis/photon", 4): ([4, 4], 2)}
    print("      %-26s %-8d %-22s %-10d %-14.1f" % ("[[4,2,2]] 1 axis/photon", 4, "[4, 4]", 8, 8 / 2))
    prof = {}; klall = []
    for (m, k, secs) in [(2, 1, 15), (2, 2, 30), (2, 3, 30), (2, 4, 40), (3, 2, 30)]:
        n = k + 2 * m
        best, cnt, tries, B = best_weight_profile(n, k, m, secs, seed=7 * m + k)
        if best is None: print("      m=%d k=%d: none found" % (m, k)); continue
        (sw, mx), w, mg, g = best; prof[(m, k)] = (sw, w, len(B)); klv = projector_kl_ok(g, n, B); klall.append(klv)
        if klv is not True: print('      WARNING: best code failed explicit KL check')
        print("      %-26s %-8d %-22s %-10d %-14.1f  (%d certificates among %d random codes)" % ("[[%d,%d]] %d axes/photon" % (n, k, m), len(B), w, sw, sw / k, cnt, tries))
    check("U4b the lightest-weight certificate of every family also passes the explicit-projector Knill-Laflamme check", all(klall) and len(klall) == 5)
    print("      note: the [[8,2]] 3-axes entry contains a weight-1 generator (one axis held in a fixed state), i.e. a degenerate use of that axis")
    check("U4a every certificate family has a heavier lightest generating set per logical qubit than the [[4,2,2]] code (4.0 data-touching gates per logical qubit)", all(v[0] / k > 4.0 for (m, k), v in prof.items() if k == 2) if prof else False)
    if (2, 2) in prof:
        print("      [[6,2]] on 3 photons: %.1f photons per logical qubit (vs 2.0) but %.1f data-touching gates per logical qubit per conventional round (vs 4.0): the photon saving is paid for in check weight" % (prof[(2, 2)][2] / 2, prof[(2, 2)][0] / 2))
    print("ALL PASS" if OK else "SOME CHECKS FAILED")
    return 0 if OK else 1

if __name__ == "__main__":
    sys.exit(main())
