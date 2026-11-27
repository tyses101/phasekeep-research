#!/usr/bin/env python3
"""S29: relational structure of four continuity arrangements for two logical qubits, and what each one buys: universal protection, noise-specific protection, photon-loss exposure, and transformation cost.

Arrangements (two logical qubits each; stabilizer generators in brackets):
   U2   two unencoded qubits                                  []
   X3   three qubits, one stabilizer XXX                      [XXX]       detects single Y and Z faults (X commutes with XXX)
   Z3   three qubits, one stabilizer ZZZ                      [ZZZ]       detects single X and Y faults
   C4   four qubits, V1.0's joint code [[4,2,2]]              [XXXX, ZZZZ]
The question is not which is best.  It is which property each one has, exactly, and under which noise each property matters.  Four things are kept SEPARATE and no score is formed:
   (a) universal protection: distance, and the share of single-qubit Pauli faults detected;
   (b) noise-specific protection: silent logical-error probability of a parked register under a Z- or X-biased Pauli noise (memory only: w idle layers, then a perfect syndrome readout; no intermediate checks);
   (c) photon-loss exposure: axes (qubits) are not photons.  For every way of hosting the axes on photons of at most two axes, which single-photon heralded losses are unrecoverable;
   (d) relational structure and transformation cost: entanglement entropies of the encoded state (with an entangled reference) across qubit and photon cuts, and what they bound.
Claims
  Z0  The four arrangements have distance 1, 1, 1, 2; detect 0, 6, 6, 12 of the 6, 9, 9, 12 single-qubit Pauli faults; the classification of every Pauli error (harmless / detected / silent) by group theory equals the classification by explicit state vectors of the
      encoded state entangled with a reference (all 16, 64, 64, 256 errors).                                                                                                                                DERIVED
  Z1  Heralded erasure: the recoverability criterion 'no logical operator inside the erased set' equals the information criterion 'the erased set is uncorrelated with the reference' (two independent methods) for every subset of qubits in all four arrangements; then, for
      every hosting of the axes on photons of at most two axes, the number of single photons whose loss is unrecoverable and of unrecoverable photon pairs.                                                       DERIVED
  Z2  Memory-only silent probability (exact): first order in the fault rate for U2, X3, Z3 (with the Z / X bias weight in front), second order for C4; the exact crossover bias b* between X3 (or Z3, mirror) and C4 as a function of q w.  Exact on the stated noise only.  DERIVED
  Z3  Entanglement entropies of each arrangement's state with its reference across photon cuts; consequences as exact lower bounds on the number of two-qubit gates (each can add at most one ebit across a cut) needed to disentangle a photon (decode in place) or to move the logical
      information to a new register.                                                                                                                                                                             DERIVED
  Z4  Negative controls: identical pairwise (here all three-body) reduced states with orthogonal global states (GHZ and its phase partner); stabilizer-preserving errors that fool a structure test (a logical Pauli, a coherent logical phase rotation) and are caught only by a
      logical-state test against the entangled reference.  Five checks (structural validity, syndrome, logical-state fidelity, external entanglement, intended operation) are tabulated against each control.      DERIVED
Not claimed: any noise bias or loss rate of a platform; that any arrangement can be hosted or controlled as assumed; syndrome-extraction cost, repeated checks or readout faults (memory only); unheralded loss.  Author-side; not an independent reproduction.  Requires numpy.  Run with python3 -I.
"""
import itertools, math, os, sys, time
from fractions import Fraction as Fr
import numpy as np

OK = True
def check(name, ok):
    global OK
    OK = OK and bool(ok); print(("PASS  " if ok else "FAIL  ") + name, flush=True)

pc = lambda v: bin(v).count("1")
def comm(a, b): return (pc(a[0] & b[1]) + pc(a[1] & b[0])) % 2 == 0
def mul(a, b): return (a[0] ^ b[0], a[1] ^ b[1])
def wt(a): return pc(a[0] | a[1])
def span(gens):
    S = {(0, 0)}
    for g in gens: S |= {mul(s, g) for s in S}
    return S
XM = lambda qs: (sum(1 << q for q in qs), 0); ZM = lambda qs: (0, sum(1 << q for q in qs))
ARR = {"U2": (2, []), "X3": (3, [XM([0, 1, 2])]), "Z3": (3, [ZM([0, 1, 2])]), "C4": (4, [XM([0, 1, 2, 3]), ZM([0, 1, 2, 3])])}

class Code:
    def __init__(self, name):
        self.name = name; self.n, self.gens = ARR[name]; n = self.n; self.k = n - len(self.gens)
        allp = [(x, z) for x in range(1 << n) for z in range(1 << n)]; self.allp = allp
        self.S = span(self.gens); self.N = {P for P in allp if all(comm(P, g) for g in self.gens)}; self.L = self.N - self.S
        self.d = min(wt(P) for P in self.L)
        singles = [(1 << q if u else 0, 1 << q if v else 0) for q in range(n) for u, v in ((1, 0), (1, 1), (0, 1))]
        self.single = singles; self.det1 = sum(1 for P in singles if P not in self.N)
        # symplectic logical basis (lightest first)
        Ls = sorted(self.L, key=lambda P: (wt(P), P)); self.lx = []; self.lz = []
        for _ in range(self.k):
            for X in Ls:
                if all(comm(X, a) and comm(X, b) for a, b in zip(self.lx, self.lz)) and all(comm(X, a) for a in self.lx):
                    Z = next((Z for Z in Ls if not comm(X, Z) and all(comm(Z, a) and comm(Z, b) for a, b in zip(self.lx, self.lz))), None)
                    if Z: self.lx.append(X); self.lz.append(Z); break
        assert len(self.lx) == self.k, name
    def classify(self, E):
        if not all(comm(E, g) for g in self.gens): return "detected"
        return "harmless" if E in self.S else "silent"
    def choi_gens(self):
        """stabilizer generators of the encoded state entangled with a reference (qubits n .. n+k-1)"""
        n = self.n; out = [(g[0], g[1]) for g in self.gens]
        for i in range(self.k):
            out.append((self.lx[i][0] | (1 << (n + i)), self.lx[i][1])); out.append((self.lz[i][0], self.lz[i][1] | (1 << (n + i))))
        return out

def rank2(rows):
    rows = list(rows); r = 0
    while rows:
        piv = rows.pop()
        if piv == 0: continue
        r += 1; hb = piv & -piv
        rows = [x ^ piv if x & hb else x for x in rows]
    return r
def entropy(gens, N, A):
    """entropy (in bits) of the qubit subset A (iterable) of the N-qubit stabilizer state with generators gens (list of (x, z))"""
    A = set(A); Bm = sum(1 << q for q in range(N) if q not in A)
    return len(A) - N + rank2([(x & Bm) | ((z & Bm) << N) for x, z in gens])

# ---------------------------------------------------------------- state vectors
def apply_pauli(v, N, P):
    x, z = P; idx = np.arange(1 << N); sign = np.array([(-1) ** pc(i & z) for i in idx]); out = np.zeros_like(v); out[idx ^ x] = sign * v
    # Y = i X Z conventions: P = X^x Z^z (phase ignored; only expectations of products of commuting generators and fidelities matter)
    return out
def stab_state(gens, N, seed=1):
    rng = np.random.default_rng(seed); v = rng.normal(size=1 << N) + 1j * rng.normal(size=1 << N)
    for g in gens:
        phase = 1j ** pc(g[0] & g[1]); w = phase * apply_pauli(v, N, g)            # Hermitian Pauli i^{x.z} X^x Z^z
        v = (v + w) / 2
    return v / np.linalg.norm(v)
def herm(v, N, g): return (1j ** pc(g[0] & g[1])) * apply_pauli(v, N, g)

def main():
    t00 = time.time(); C = {nm: Code(nm) for nm in ARR}
    # ---- Z0
    print("      %-4s %3s %3s %3s %-26s %-12s %s" % ("", "n", "k", "d", "min weight of logical ops", "detected", "silent single-qubit Paulis"))
    for nm, c in C.items():
        print("      %-4s %3d %3d %3d %-26s %2d of %2d      %s" % (nm, c.n, c.k, c.d, "X-like %s Z-like %s" % ([wt(P) for P in c.lx], [wt(P) for P in c.lz]), c.det1, 3 * c.n, 3 * c.n - c.det1 - sum(1 for P in c.single if P in c.S)))
    check("Z0a distance 1, 1, 1, 2 and detected single-qubit Paulis 0 of 6, 6 of 9, 6 of 9, 12 of 12 for U2, X3, Z3, C4 (X3 detects exactly the Y and Z faults, Z3 the X and Y faults)",
          [c.d for c in C.values()] == [1, 1, 1, 2] and [c.det1 for c in C.values()] == [0, 6, 6, 12]
          and {P for P in C["X3"].single if P not in C["X3"].N} == {P for P in C["X3"].single if (P[1] & 7) != 0} and {P for P in C["Z3"].single if P not in C["Z3"].N} == {P for P in C["Z3"].single if (P[0] & 7) != 0})
    ok = True; cnt = {}
    for nm, c in C.items():
        N = c.n + c.k; psi = stab_state(c.choi_gens(), N); ok &= all(abs(np.vdot(psi, herm(psi, N, g)) - 1) < 1e-9 for g in c.choi_gens()); tab = {"harmless": 0, "detected": 0, "silent": 0}
        for E in c.allp:
            Ev = apply_pauli(psi, N, E)
            syn = [np.vdot(psi, herm(Ev, N, g)).real for g in c.gens]                      # <psi|E^+ g E|psi> = +-1 on the encoded state
            fid = abs(np.vdot(psi, Ev)) ** 2
            kind = "detected" if any(s < 0 for s in [np.vdot(Ev, herm(Ev, N, g)).real for g in c.gens]) else ("harmless" if fid > 1 - 1e-9 else "silent")
            ok &= kind == c.classify(E); tab[kind] += 1
        cnt[nm] = tab
    print("      all Pauli errors on the code qubits by explicit state vectors (harmless / detected / silent): " + "; ".join("%s %d / %d / %d" % (nm, t["harmless"], t["detected"], t["silent"]) for nm, t in cnt.items()))
    check("Z0b the group-theoretic classification of every Pauli error equals the state-vector classification (syndrome from the generators' expectation on the errored state; harmless iff the Choi state is unchanged) for all 16, 64, 64, 256 errors", ok)
    # ---- Z1
    ok = True; hostings = {}
    for nm, c in C.items():
        n = c.n; N = n + c.k; gens = c.choi_gens(); R = list(range(n, N))
        for r in range(1, n + 1):
            for E in itertools.combinations(range(n), r):
                m = sum(1 << q for q in E); by_logic = not any((P[0] | P[1]) & ~m == 0 for P in c.L)
                info = entropy(gens, N, R) + entropy(gens, N, E) - entropy(gens, N, R + list(E))
                ok &= by_logic == (abs(info) < 1e-9)
    check("Z1a for every nonempty set of erased qubits, in all four arrangements: 'no logical operator supported inside the set' <=> 'zero mutual information between the set and the reference' (stabilizer entropies): two independent criteria agree", ok)
    def partitions(items):
        if not items: yield []; return
        a, rest = items[0], items[1:]
        for p in partitions(rest):
            yield [[a]] + p
            for i in range(len(p)):
                if len(p[i]) < 2: yield p[:i] + [[a] + p[i]] + p[i + 1:]
    def recoverable(c, E):
        m = sum(1 << q for q in E); return not any((P[0] | P[1]) & ~m == 0 for P in c.L)
    print("      photon-loss exposure by hosting (axes per photon <= 2); heralded loss, recoverable in principle (no recovery cost charged); 'fatal' = loss of that photon (or pair) cannot be undone")
    best = {}
    for nm, c in C.items():
        seen = {}
        for part in partitions(list(range(c.n))):
            key = tuple(sorted(len(b) for b in part)); fat1 = sum(1 for b in part if not recoverable(c, b))
            pairs = list(itertools.combinations(part, 2)); fat2 = sum(1 for a, b in pairs if recoverable(c, a) and recoverable(c, b) and not recoverable(c, a + b)); nonrec_pairs = sum(1 for a, b in pairs if not recoverable(c, a + b))
            seen.setdefault(key, set()).add((len(part), fat1, nonrec_pairs, len(pairs)))
        hostings[nm] = seen
        for key, vals in sorted(seen.items(), reverse=True):
            print("      %-4s photons with axes %-14s -> (photons, fatal single photons, unrecoverable photon pairs, photon pairs): %s" % (nm, key, sorted(vals)))
    h = lambda nm, key: sorted(hostings[nm][key])
    ok1b = (h("U2", (2,)) == [(1, 1, 0, 0)] and h("U2", (1, 1)) == [(2, 2, 1, 1)]
            and all(f == p_ for k in hostings["X3"] for (p_, f, _, _) in hostings["X3"][k]) and all(f == p_ for k in hostings["Z3"] for (p_, f, _, _) in hostings["Z3"][k])
            and h("C4", (2, 2)) == [(2, 2, 1, 1)] and h("C4", (1, 1, 2)) == [(3, 1, 3, 3)] and h("C4", (1, 1, 1, 1)) == [(4, 0, 6, 6)])
    check("Z1b hostings: U2 on one photon has 1 photon and its loss is fatal (on two photons both are); X3 and Z3 lose everything to ANY single-photon loss in every hosting (distance 1, also for erasure); C4 on two two-axis photons (V1.0's hosting) has 2 photons and BOTH single losses are fatal; "
          "C4 with one two-axis and two one-axis photons has 3 photons, 1 fatal; C4 on four one-axis photons survives every single-photon loss and fails on 6 of 6 photon pairs: distance-2 protection against loss exists only if every photon carries at most one axis, at the price of twice the photons", ok1b)
    # ---- Z2 : memory-only exact silent probability
    def per_qubit(q, b, dom, w):
        wx, wy, wz = (1.0, 1.0, b) if dom == "Z" else (b, 1.0, 1.0); s = wx + wy + wz   # group Z2^2 indexed x | z << 1: I = 0, X = 1, Z = 2, Y = 3
        
        v = np.zeros(4); v[0] = 1 - q; v[1] = q * wx / s; v[3] = q * wy / s; v[2] = q * wz / s
        T = np.zeros((4, 4))
        for a in range(4):
            for c2 in range(4): T[a ^ c2, a] += v[c2]
        out = np.zeros(4); out[0] = 1.0
        for _ in range(w): out = T @ out
        return out
    def silent_mem(c, q, b, dom, w):
        pq = per_qubit(q, b, dom, w); tot = 0.0
        for P in c.L:
            pr = 1.0
            for qb in range(c.n): pr *= pq[((P[0] >> qb) & 1) | (((P[1] >> qb) & 1) << 1)]
            tot += pr
        return tot
    # sanity: first-order
    q = 1e-4; ok = True
    for nm, c in C.items():
        for dom in ("Z", "X"):
            for b in (1.0, 10.0, 100.0):
                s = sum(per_qubit(q, b, dom, 1)[1:]); ok &= abs(sum(per_qubit(q, b, dom, 1)) - 1) < 1e-12 and abs(s - q) < 1e-12
    check("Z2a the per-qubit Pauli distribution is normalised and its non-identity mass is q (bias weights X : Y : Z = 1 : 1 : b for Z-dominant noise, b : 1 : 1 for X-dominant)", ok)
    print("      memory-only silent probability after w idle layers (rate q per qubit per layer; perfect final syndrome readout; no intermediate checks); q = 1e-3")
    q = 1e-3; tab = {}
    for dom in ("Z", "X"):
        for b in (1.0, 10.0, 100.0, 1000.0):
            for w in (1, 10):
                tab[(dom, b, w)] = {nm: silent_mem(c, q, b, dom, w) for nm, c in C.items()}
                print("      %s-dominant b = %-6g w = %-2d  U2 %.3e   X3 %.3e   Z3 %.3e   C4 %.3e" % (dom, b, w, *[tab[(dom, b, w)][nm] for nm in ARR]))
    # first-order exactness: U2 = 1 - (1-q)^(2w)-like; X3 ~ 3 w q wx/s ; check at q small
    ok = True
    for nm, k1 in (("U2", lambda q, b, d: 2 * q), ("X3", lambda q, b, d: 3 * q * (1.0 if d == "Z" else b) / (2 + b)), ("Z3", lambda q, b, d: 3 * q * (b if d == "Z" else 1.0) / (2 + b))):
        for dom in ("Z", "X"):
            for b in (1.0, 10.0, 100.0):
                qq = 1e-7; ok &= abs(silent_mem(C[nm], qq, b, dom, 1) / k1(qq, b, dom) - 1) < 1e-3
    check("Z2b first-order silent probabilities: U2 2q, X3 3 q w_X / (2 + b) and Z3 3 q w_Z / (2 + b) with w_X = 1 (Z-dominant) or b (X-dominant), at q = 1e-7 to within 0.1 % (C4 has no first-order term)", ok)
    c4 = [silent_mem(C["C4"], qq, 1.0, "Z", 1) / qq ** 2 for qq in (1e-5, 1e-6)]
    check("Z2c C4's silent probability is second order: silent / q^2 = %.3f and %.3f at q = 1e-5 and 1e-6 for one idle layer, unbiased (it is %.3f at b = 1000, Z-dominant)" % (*c4, silent_mem(C["C4"], 1e-6, 1000.0, "Z", 1) / 1e-12), abs(c4[0] - c4[1]) < 1e-3 * c4[1] and 1 < c4[1] < 100)
    # crossover bias b*: X3 silent (Z-dominant) = C4 silent
    def bstar(q, w):
        f = lambda b: silent_mem(C["X3"], q, b, "Z", w) - silent_mem(C["C4"], q, b, "Z", w)
        lo, hi = 1.0, 1e7
        if f(lo) < 0: return None
        if f(hi) > 0: return float("inf")
        a, bb = math.log(lo), math.log(hi)
        for _ in range(60):
            mid = (a + bb) / 2
            if f(math.exp(mid)) > 0: a = mid
            else: bb = mid
        return math.exp((a + bb) / 2)
    BS = {(qq, w): bstar(qq, w) for qq in (1e-4, 1e-3, 1e-2) for w in (1, 10)}
    print("      crossover bias b* (Z-dominant): X3 has the lower memory-only silent probability than C4 for b above b*; mirror image for Z3 with X-dominant noise")
    for qq in (1e-4, 1e-3, 1e-2): print("        q = %.0e: " % qq + "   ".join("w = %2d: b* = %s" % (w, ("%.1f" % BS[(qq, w)]) if BS[(qq, w)] and BS[(qq, w)] != float("inf") else str(BS[(qq, w)])) for w in (1, 10)))
    rel = max(abs(BS[(qq, w)] / (1 / (qq * w) - 2) - 1) for (qq, w) in BS if qq * w <= 1e-2)
    check("Z2d crossover bias b*: it rises as q w falls, from %.0f (q = 1e-3, w = 1) to %.0f (w = 10); the leading-order relation b* + 2 = 1 / (q w) holds within %.0f %% for every q w <= 1e-2 tested (values 1 / (q w) - 2 for comparison: %.0f, %.0f); X3 (Z-dominant) and Z3 (X-dominant) mirror each other exactly" % (
          BS[(1e-3, 1)], BS[(1e-3, 10)], 100 * rel, 1 / 1e-3 - 2, 1 / 1e-2 - 2),
          all(v and v != float("inf") for v in BS.values()) and BS[(1e-4, 1)] > BS[(1e-3, 1)] > BS[(1e-2, 1)] and BS[(1e-3, 1)] > BS[(1e-3, 10)] and rel < 0.10
          and abs(silent_mem(C["X3"], 1e-3, 50.0, "Z", 3) - silent_mem(C["Z3"], 1e-3, 50.0, "X", 3)) < 1e-15)
    qq = 1e-4; fx = silent_mem(C["X3"], qq, 1e6, "Z", 1) / qq ** 2; fc = silent_mem(C["C4"], qq, 1e6, "Z", 1) / qq ** 2
    check("Z2e why b* is where it is (leading order): at very large Z bias the second-order floor of X3 is 3 q^2 (the three undetected ZZ pairs) and C4's is 6 q^2 (six ZZ pairs; here %.3f and %.3f in units of q^2), so X3 = 3 q w / (b + 2) + 3 (q w)^2 against 6 (q w)^2 gives b + 2 = 1 / (q w)" % (fx, fc),
          abs(fx - 3) < 0.05 and abs(fc - 6) < 0.03)
    # ---- Z3 entropies
    print("      entanglement entropy (ebits) of each hosting block with everything else (reference included), in the encoded state entangled with a 2-qubit reference")
    ENT = {}
    for nm, c in C.items():
        N = c.n + c.k; gens = c.choi_gens()
        for key in sorted({tuple(sorted(len(b) for b in p)) for p in partitions(list(range(c.n)))}, reverse=True):
            part = next(p for p in partitions(list(range(c.n))) if tuple(sorted(len(b) for b in p)) == key)
            ENT[(nm, key)] = sorted([entropy(gens, N, b) for b in part])
            print("      %-4s blocks %-12s block entropies %s" % (nm, key, ENT[(nm, key)]))
    check("Z3a entropies: for C4 hosted on two two-axis photons each photon shares %s ebits with the rest; hosted on four one-axis photons each shares %s; total entropy of all code qubits is 2 for every arrangement (the reference's)" % (ENT[("C4", (2, 2))], ENT[("C4", (1, 1, 1, 1))]),
          all(abs(entropy(c.choi_gens(), c.n + c.k, range(c.n)) - 2) < 1e-9 for c in C.values()) and ENT[("C4", (2, 2))] == [2, 2] and ENT[("C4", (1, 1, 1, 1))] == [1, 1, 1, 1])
    lb = ENT[("C4", (2, 2))][0]
    check("Z3b consequence (exact): each two-qubit gate (operator Schmidt rank 2) raises the Schmidt rank across a cut by at most 2, so at least %d inter-photon two-qubit gates are needed to disentangle one two-axis photon of a hosted C4 (decode in place), and at least k = 2 two-qubit gates across any cut to move two logical qubits into a register that starts unentangled "
          "(the reference is entangled with 2 ebits to the destination at the end, 0 at the start)" % lb, lb == 2)
    # ---- Z4 negative controls
    def red(v, N, keep):
        t = v.reshape([2] * N); other = [q for q in range(N) if q not in keep]; t = np.moveaxis(t, [N - 1 - q for q in other] + [N - 1 - q for q in keep], list(range(N)))
        m = t.reshape(2 ** len(other), 2 ** len(keep)); return m.T @ m.conj()
    N4 = 4; g0 = np.zeros(16, complex); g0[0] = 1; g1 = np.zeros(16, complex); g1[15] = 1; ghz_p = (g0 + g1) / math.sqrt(2); ghz_m = (g0 - g1) / math.sqrt(2)
    same3 = all(np.allclose(red(ghz_p, N4, list(k)), red(ghz_m, N4, list(k))) for r in (1, 2, 3) for k in itertools.combinations(range(4), r))
    check("Z4a GHZ4 and its phase partner have identical reduced states on every one-, two- and three-qubit subset (all pairwise and triple relations) but are orthogonal as global states (overlap %.1e): pairwise or triple structure does not determine the state" % abs(np.vdot(ghz_p, ghz_m)),
          same3 and abs(np.vdot(ghz_p, ghz_m)) < 1e-12)
    c = C["C4"]; N = 6; gens = c.choi_gens(); psi = stab_state(gens, N); L1z = c.lz[0]
    def entropy_state(v, N, keep):
        rho = red(v, N, keep); ev = np.linalg.eigvalsh(rho); ev = ev[ev > 1e-12]; return float(-(ev * np.log2(ev)).sum())
    def battery(v, intended):
        stab = all(abs(np.vdot(v, herm(v, N, g)).real - 1) < 1e-6 for g in c.gens)                 # structural validity = clean syndrome of the code's stabilizers
        fid = abs(np.vdot(intended, v)) ** 2                                                         # logical-state integrity / correctness of the intended operation: overlap with the intended state
        ent = abs(entropy_state(v, N, [4, 5]) - 2) < 1e-6                                             # external entanglement: reference still maximally mixed
        return stab, fid, ent
    def apply_phase(v, P, th):
        w = herm(v, N, P); return math.cos(th) * v + 1j * math.sin(th) * w                           # exp(i th P) for a Hermitian involution P
    Zb = (c.lz[0][0], c.lz[0][1]); psi_Z = apply_pauli(psi, N, Zb)
    cases = [("intact, intended: identity", psi, psi), ("logical Pauli Zbar_1 appears, intended: identity", psi_Z, psi), ("coherent logical phase exp(i 0.3 Zbar_1), intended: identity", apply_phase(psi, Zb, 0.3), psi),
             ("single-qubit Z error on axis 0, intended: identity", apply_pauli(psi, N, (0, 1)), psi), ("Zbar_1 applied as intended", psi_Z, psi_Z), ("Zbar_1 intended but skipped", psi, psi_Z)]
    print("      verification battery on C4 with a reference: stabilizers hold (structure / syndrome) | fidelity with the intended state | reference still maximally entangled with the code space")
    res = {}
    for nm2, v, want in cases:
        res[nm2] = battery(v, want); print("        %-62s %-5s %.4f   %s" % (nm2, *res[nm2]))
    keys = [k for k, _, _ in cases]
    check("Z4b a logical Pauli and a coherent logical phase error keep the stabilizers satisfied and the reference maximally entangled, yet their fidelity with the intended state is %.3f and %.3f; a skipped intended operation has fidelity %.3f with the structure fully intact; the same operation applied as intended has fidelity %.3f; "
          "only the physical single-qubit error is caught by the structure test: verifying the geometry does not establish the information" % (res[keys[1]][1], res[keys[2]][1], res[keys[5]][1], res[keys[4]][1]),
          res[keys[0]] == (True, res[keys[0]][1], True) and res[keys[0]][1] > 0.999999 and all(res[k][0] and res[k][2] and res[k][1] < 0.999 for k in (keys[1], keys[2], keys[5])) and res[keys[4]][0] and res[keys[4]][1] > 0.999999 and res[keys[4]][2] and not res[keys[3]][0])
    print("NOTE  everything above is exact on stated models: stabilizer algebra, state vectors of at most 6 qubits, and Pauli idle noise with a per-layer fault probability q and a bias weight b.  It does not include syndrome extraction, repeated checks, readout faults or unheralded loss, so it is a comparison of MEMORY properties, not of complete protocols.  Total wall-clock %.0f s" % (time.time() - t00))
    print("ALL PASS" if OK else "FAILED")
    return 0 if OK else 1

if __name__ == "__main__": sys.exit(main())
