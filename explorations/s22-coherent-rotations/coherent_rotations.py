#!/usr/bin/env python3
"""S22: coherent (non-Pauli) rotation noise on V1.0's five rounds, and how much of the ranking survives it.

V0.9 and V1.0 use independent Pauli faults.  Open problem 18 asks whether non-Pauli noise changes the rankings.  Here every location gets a small COHERENT rotation of the same angle theta and the
same sign, exp(-i theta M / 2) with M a Hermitian involution, simulated as an explicit state vector with all measurements deferred (no qubit is reused after its measurement), then compared with
the Pauli-twirled channel of the very same rotations (each location applies its Pauli with probability sin^2(theta/2); exact dense convolution on the S19-style state table).

Models (ASSUMED; each is a stylised systematic error, not a device model)
  Z  a Z rotation on every qubit an operation touches, after every non-measurement operation (preparations and one-qubit operations included)
  X  the same with X
  G  a gate over-rotation: exp(-i theta Z_c X_t / 2) after each CNOT, exp(-i theta Z_a Z_b / 2) after each CZ; nothing else
  U  a rotation about the axis (X+Y+Z)/sqrt(3) on every touched qubit (a generic single-qubit coherent error; its twirl is X, Y, Z each with probability sin^2(theta/2)/3)

How "silent" is defined for a superposition (ASSUMED definition; it reduces to V0.9's definition for a Pauli fault)
  For each measurement record with all detector parities even, V_m is the operator the circuit applies to the data given that record.  Restricted to the code space it is a d x d matrix K_m
  (d = 4, or 8 for the ZZZZ-only round).  Its trace part is the identity logical operation; the rest, K_m - (Tr K_m / d) I, is the logical-error part; silent weight = sum over accepted
  records of ||K_m - (Tr K_m / d) I||_F^2 / d (average over code-space inputs, so a logical Pauli twirl of the code space would find exactly this weight).  The weight outside the code
  space is accepted-damaged and the weight on records with an odd detector parity is the rejection probability.

Claims
  K0  the engine's ideal run (theta = 0) is the ideal round: nothing silent, nothing damaged, nothing rejected, accepted weight 1, for every round and model.                          DERIVED
  K1  one location at a time: for a Pauli-axis rotation the coherent silent, damaged and rejected probabilities equal sin^2(theta/2) times the Pauli fault's class, for every location of every
      round (Z, X and G models).                                                                                                                                              DERIVED
  K2  the Pauli-twirled value used here (XOR of single-fault effects) equals what an explicit state-vector run of every PAIR of faults gives, in class, for every round and model.          DERIVED
  K3  the amplitude polynomial in t = tan(theta/2) (orders <= 4, exact) agrees with the direct simulation at a small angle, and its leading coefficient agrees with a second code path
      (explicit Pauli-fault state vectors from S05, summed coherently over fault sets) on every round with deterministic records.                                                       DERIVED
  K4  the leading coefficients of the coherent silent probability are exact integers (rationals for model U) and are compared with the twirled leading coefficients.                   DERIVED
  K5  averaged over ALL 2^L sign patterns of the L rotation angles, the leading coherent coefficient equals the twirled one exactly (rounds with L <= 12): the amplification below is a
      property of the same-sign (systematic) assumption.                                                                                                                       DERIVED
  K6  exact silent probabilities at the same per-location infidelity s = sin^2(theta/2) = 1e-4, 1e-3, 1e-2, with the exact crossings between rounds.                                  DERIVED
Not claimed: that real devices have same-sign rotations of equal angle on every location, or any rotation at all; rates are not measured.  Readout flips are absent (they are not rotations).
Idle faults and the incoming data faults of V0.9's M3 are absent; the locations are those of model M2 without correlated two-qubit Paulis.  Author-side; not independent reproduction.
Requires numpy.  Run with python3 -I.
"""
import functools, importlib.util, itertools, math, os, sys, time
from fractions import Fraction as Fr
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
def _load(name, rel):
    sp = importlib.util.spec_from_file_location(name, os.path.join(ROOT, *rel)); m = importlib.util.module_from_spec(sp)
    sys.modules[name] = m; sp.loader.exec_module(m); return m
s18 = _load("s18", ["explorations", "s18-m3-reproduction", "m3_reproduction.py"])
v10 = s18.v10; s05 = s18.s05; PAULIM = s18.PAULI
ROUNDS = ["L conv (baseline)", "J conv", "J flag", "J cat (verified)", "J ZZZZ only (partial)"]
MODELS = ["Z", "X", "G", "U"]

OK = True
def check(name, ok):
    global OK
    OK = OK and bool(ok); print(("PASS  " if ok else "FAIL  ") + name, flush=True)

def code_basis(code):
    gens = {"L": ["ZZII", "IIZZ"], "J": ["ZZZZ", "XXXX"], "Z": ["ZZZZ"]}[code]
    P = np.eye(16, dtype=complex)
    for g in gens:
        G = functools.reduce(np.kron, [PAULIM[g[q]] for q in (3, 2, 1, 0)])
        P = P @ ((np.eye(16) + G) / 2)
    u, s, vh = np.linalg.svd(P); r = int(round(s.sum())); assert np.allclose(s[:r], 1) and np.allclose(s[r:], 0)
    return u[:, :r]

UAX = (PAULIM["X"] + PAULIM["Y"] + PAULIM["Z"]) / math.sqrt(3)
def rot_locations(ops, model):
    """list of (op index, kind, payload): kind 'P' = Pauli string {qubit: 'X'|'Y'|'Z'}, kind 'U' = the (X+Y+Z)/sqrt(3) axis on one qubit"""
    locs = []
    for i, op in enumerate(ops):
        if op[0] in ("MZ", "MX"): continue
        qs = [op[1], op[2]] if op[0] in ("CNOT", "CZ") else [op[1]]
        if model in ("Z", "X"):
            for q in qs: locs.append((i, "P", {q: model}))
        elif model == "U":
            for q in qs: locs.append((i, "U", q))
        elif model == "G":
            if op[0] == "CNOT": locs.append((i, "P", {op[1]: "Z", op[2]: "X"}))
            elif op[0] == "CZ": locs.append((i, "P", {op[1]: "Z", op[2]: "Z"}))
    return locs

def options(loc):
    """the Pauli options of the twirl of a location: list of (fault dict, weight as Fraction)"""
    i, kind, pl = loc
    if kind == "P": return [(pl, Fr(1))]
    return [({pl: c}, Fr(1, 3)) for c in "XYZ"]

class SV:
    def __init__(self, nq):
        self.nq = nq; self.N = 1 << nq; self.idx = np.arange(self.N)
        self.bit = [(self.idx >> q) & 1 for q in range(nq)]; self.pc = np.array([bin(n).count("1") & 1 for n in range(self.N)])
    def one(self, v, U, q):
        B = v.shape[0]; return np.einsum("ab,xhbl->xhal", U, v.reshape(B, -1, 2, 1 << q)).reshape(B, -1)
    def cnot(self, v, c, t):
        return v[:, np.where(self.bit[c] == 1, self.idx ^ (1 << t), self.idx)]
    def cz(self, v, a, b):
        return v * np.where((self.bit[a] == 1) & (self.bit[b] == 1), -1.0, 1.0)
    def pauli_arrays(self, pd):
        xm = zm = ny = 0
        for q, c in pd.items():
            if c in "XY": xm |= 1 << q
            if c in "ZY": zm |= 1 << q
            if c == "Y": ny += 1
        src = self.idx ^ xm; return src, (1j ** ny) * np.where(self.pc[src & zm] == 1, -1.0, 1.0)

HAD = s05.HAD
class Coh:
    """coherent-rotation engine for one round and one model"""
    def __init__(self, name, model):
        R = v10.load()[name]; self.name = name; self.model = model; self.ops = R["ops"]; self.dets = R["dets"]; self.code = R["code"]; self.nq = R["nq"]
        self.sv = SV(self.nq); self.B = code_basis(self.code); self.d = self.B.shape[1]
        self.locs = rot_locations(self.ops, model); self.arr = [self.sv.pauli_arrays(l[2]) if l[1] == "P" else None for l in self.locs]
        meas = [(o[1], o[2]) for o in self.ops if o[0] in ("MZ", "MX")]; assert len(meas) == self.nq - 4       # every ancilla is measured, none is reused afterwards (checked in K0)
        n_anc = 1 << (self.nq - 4); self.rec = np.zeros(n_anc, dtype=int)
        for a in range(n_anc): self.rec[a] = sum(1 << b for q, b in meas if (a >> (q - 4)) & 1)
        self.nrec = 1 << len(meas); assert len(set(self.rec.tolist())) == n_anc == self.nrec
        self.syn = np.array([[bin(m & mk).count("1") & 1 for mk in self.dets] for m in range(self.nrec)]); self.acc = self.syn.sum(1) == 0
        self.order = np.zeros(n_anc, dtype=int); self.order[self.rec] = np.arange(n_anc); self._cache = {}
        self.locof = {}
        for j, l in enumerate(self.locs): self.locof.setdefault(l[0], []).append(j)
    def apply_loc(self, w, j):                       # w: (batch, N)
        l = self.locs[j]
        if l[1] == "P": src, coef = self.arr[j]; return w[:, src] * coef
        return self.sv.one(w, UAX, l[2])
    def run(self, K, theta=None, sg=None):
        """K >= 1: truncated amplitude polynomial, array (K+1, nin, N) whose k-th slice is the coefficient of t^k of the product of (I - i t M); K = 0 with theta: the actual rotation"""
        nin = self.d; v = np.zeros((K + 1, nin, self.sv.N), dtype=complex)
        for i in range(nin): v[0, i, :16] = self.B[:, i]
        for i, op in enumerate(self.ops):
            k = op[0]; sh = v.shape; w = v.reshape(-1, self.sv.N)
            if k in ("P+", "H", "MX"): w = self.sv.one(w, HAD, op[1])
            elif k == "CNOT": w = self.sv.cnot(w, op[1], op[2])
            elif k == "CZ": w = self.sv.cz(w, op[1], op[2])
            v = w.reshape(sh)
            for j in self.locof.get(i, []):
                sj = 1.0 if sg is None else sg[j]
                if K == 0:
                    v = math.cos(theta / 2) * v - 1j * math.sin(theta / 2) * sj * self.apply_loc(v.reshape(-1, self.sv.N), j).reshape(v.shape)
                else:
                    nv = v.copy()
                    for k_ in range(1, K + 1): nv[k_] = v[k_] - 1j * sj * self.apply_loc(v[k_ - 1], j)
                    v = nv
        return v
    def blocks(self, F):
        K1, nin, N = F.shape; G = F.reshape(K1, nin, N >> 4, 16)[:, :, self.order, :]            # (k, input, record, data)
        Km = np.einsum("jd,kimj->kmdi", self.B.conj(), G); W = G - np.einsum("jd,kmdi->kimj", self.B, Km); return Km, W, G
    def direct(self, theta):
        key = round(theta, 15)
        if key in self._cache: return self._cache[key]
        Km, W, G = self.blocks(self.run(0, theta=theta)); Km, W, G = Km[0], W[0], G[0]; d = self.d
        tr = np.einsum("mdd->m", Km); Kni = Km - (tr / d)[:, None, None] * np.eye(d)[None]
        a = self.acc; out = dict(silent=float((np.abs(Kni[a]) ** 2).sum() / d), damaged=float((np.abs(W[:, a, :]) ** 2).sum() / d),
                                 reject=float((np.abs(G[:, ~a, :]) ** 2).sum() / d), accepted=float((np.abs(G[:, a, :]) ** 2).sum() / d))
        self._cache[key] = out; return out
    def poly(self, K, sg=None):
        F = self.run(K, sg=sg); Km, W, G = self.blocks(F); d = self.d
        tr = np.einsum("kmdd->km", Km); Kni = Km - (tr / d)[:, :, None, None] * np.eye(d)[None, None]; Ka = Kni[:, self.acc]
        s = np.zeros(2 * K + 1)
        for j in range(K + 1):
            for k in range(K + 1): s[j + k] += float(np.real(np.vdot(Ka[j], Ka[k]))) / d
        return s
    def lead(self, s, tol=1e-9):
        for n, x in enumerate(s):
            if abs(x) > tol: return n, x
        return None, 0.0

class Tw:
    """Pauli twirl of the same rotations: independent locations, each with its options (Pauli, weight), taken from state-vector effects"""
    def __init__(self, name, model):
        self.R = R = s18.Rnd(name); self.name = name; self.code = R.code; self.d = len(R.dets); self.locs = rot_locations(R.ops, model); self.opts = []
        branches = (0,) if not R.nrand else (0, (1 << R.nrand) - 1, 5 % (1 << R.nrand)); self.consistent = True
        for loc in self.locs:
            row = []
            for pd, w in options(loc):
                es = [R.effect([(loc[0], "p", pd)], b) for b in branches]
                self.consistent &= len({(e[0], s18.classify_err(*e[1], self.code)) for e in es}) == 1
                syn, (x, z) = es[0]; row.append((syn, x, z, w))
            self.opts.append(row)
        nb = self.d + 8; self.N = 1 << nb; idx = np.arange(self.N); self.idx = idx
        syn = idx & ((1 << self.d) - 1); x = (idx >> self.d) & 15; z = (idx >> (self.d + 4)) & 15
        cl = np.array([{"none": 0, "harmless": 0, "detected": 1, "logical": 2}[s18.classify_err(int(a), int(b), self.code)] for a, b in zip(x, z)])
        self.m_sil = (syn == 0) & (cl == 2); self.m_dam = (syn == 0) & (cl == 1); self.m_rej = syn != 0
    def cat(self, e): return s18.category(e[0], e[1], e[2], self.code)
    def code_of(self, row): return [(syn | (x << self.d) | (z << (self.d + 4)), w) for syn, x, z, w in row]
    def counts(self):
        """exact first-order coefficient d1 and second-order coefficient d2 of the silent probability in s, as Fractions"""
        L = len(self.opts); d1 = Fr(0)
        for row in self.opts: d1 += sum(w for syn, x, z, w in row if self.cat((syn, x, z)) == "silent")
        pairs = Fr(0)
        for a in range(L):
            for b in range(a + 1, L):
                for sa, xa, za, wa in self.opts[a]:
                    for sb, xb, zb, wb in self.opts[b]:
                        if self.cat((sa ^ sb, xa ^ xb, za ^ zb)) == "silent": pairs += wa * wb
        return L, d1, pairs, pairs - (L - 1) * d1
    def dist(self, s):
        P = np.zeros(self.N); P[0] = 1.0
        for row in self.opts:
            acc = np.zeros(self.N)
            for e, w in self.code_of(row): acc += float(w) * P[self.idx ^ e]
            P = (1 - s) * P + s * acc
        return dict(silent=P[self.m_sil].sum(), damaged=P[self.m_dam].sum(), reject=P[self.m_rej].sum())

def ratio(a, b): return a / b if b else float("nan")

def main():
    t00 = time.time(); S = {}; T = {}
    t0 = time.time()
    for md in MODELS:
        for nm in ROUNDS: S[(md, nm)] = Coh(nm, md); T[(md, nm)] = Tw(nm, md)
    print("      engines built in %.0f s; rotation locations per round (Z/X, G, U): %s" % (time.time() - t0, "; ".join("%s %d/%d/%d" % (nm, len(S[("Z", nm)].locs), len(S[("G", nm)].locs), len(S[("U", nm)].locs)) for nm in ROUNDS)))
    # K0
    bad = []
    for key, c in S.items():
        r = c.direct(0.0)
        if not (abs(r["silent"]) < 1e-12 and abs(r["damaged"]) < 1e-12 and abs(r["reject"]) < 1e-12 and abs(r["accepted"] - 1) < 1e-12): bad.append(key)
    nrand = {nm: T[("Z", nm)].R.nrand for nm in ROUNDS}
    check("K0 at theta = 0 every round and model gives silent = damaged = rejected = 0 and accepted weight 1 (%d engines); every ancilla is measured exactly once (nq - 4 = number of measurements)" % len(S), not bad)
    check("K0b the twirl effects of every location are consistent across sampled measurement branches (random outcomes of the cat rounds: %s)" % {nm: nrand[nm] for nm in ROUNDS if nrand[nm]}, all(t.consistent for t in T.values()))
    # K1: one location at a time (Pauli-axis models)
    th = 0.37; s_ = math.sin(th / 2) ** 2; nloc = 0; bad = []
    for md in ("Z", "X", "G"):
        for nm in ROUNDS:
            c, t = S[(md, nm)], T[(md, nm)]; L = len(c.locs)
            for j in range(L):
                sub = Coh(nm, md); sub.locs = [c.locs[j]]; sub.arr = [c.arr[j]]; sub.locof = {c.locs[j][0]: [0]}; sub._cache = {}
                r = sub.direct(th); syn, x, z, w = t.opts[j][0]; cat = t.cat((syn, x, z))
                exp = dict(silent=s_ * (cat == "silent"), damaged=s_ * (cat == "pass_damaged"), reject=s_ * (cat in ("false_reject", "caught_damage")))
                nloc += 1
                if any(abs(r[k] - exp[k]) > 1e-12 for k in exp): bad.append((md, nm, j))
    check("K1 one rotation at a time: coherent silent, accepted-damaged and rejected probabilities equal sin^2(theta/2) x [the Pauli fault's class] for all %d single locations of the Z, X and G models (theta = %.2f)%s" % (nloc, th, "" if not bad else "; failures: %s" % bad[:5]), not bad)
    # K2: XOR composition of single-fault effects vs explicit two-fault state vectors
    npair = 0; bad = []; t0 = time.time()
    for md in ("Z", "X", "G", "U"):
        for nm in ROUNDS:
            t = T[(md, nm)]; R = t.R; L = len(t.opts)
            for a in range(L):
                for b in range(a + 1, L):
                    oa = t.opts[a][0]; ob = t.opts[b][-1]; la, lb = t.locs[a], t.locs[b]
                    pa = options(la)[0][0]; pb = options(lb)[-1][0]
                    e = R.effect([(la[0], "p", pa), (lb[0], "p", pb)], 0); x_ = (oa[0] ^ ob[0], oa[1] ^ ob[1], oa[2] ^ ob[2])
                    npair += 1
                    if t.cat((e[0], e[1][0], e[1][1])) != t.cat(x_): bad.append((md, nm, a, b))
    check("K2 the class of the XOR of two single-fault effects equals the class of the explicit two-fault state-vector run for %d fault pairs (every pair of locations, first option of the first, last of the second; Z, X, G, U; five rounds) in %.0f s%s" % (npair, time.time() - t0, "" if not bad else "; failures: %s" % bad[:5]), not bad)
    # K3a: polynomial vs direct at a small angle; K3b: second code path
    tsm = 2e-4; thsm = 2 * math.atan(tsm); bad = []; worst = 0.0; polys = {}
    for key, c in S.items():
        s = c.poly(4); polys[key] = s; a, x = c.lead(s)
        if a is None: continue
        pred = (1 + tsm ** 2) ** (-len(c.locs)) * sum(s[n] * tsm ** n for n in range(0, 9)); dv = c.direct(thsm)["silent"]
        worst = max(worst, abs(dv / pred - 1))
    check("K3a for every round and model with a nonzero silent coefficient the exact amplitude polynomial (orders <= 4, i.e. the silent probability to t^8) reproduces the direct rotation simulation at theta = %.1e to a relative difference of at most %.1e" % (thsm, worst), worst < 5e-4)
    # K3b: independent path: explicit Pauli-fault state vectors from S05 summed coherently over fault sets (rounds with deterministic records)
    t0 = time.time(); diffs = []; npaths = 0
    for md in MODELS:
        for nm in ROUNDS:
            if nrand[nm]: continue
            c, t = S[(md, nm)], T[(md, nm)]; R = t.R; d = c.d; B = c.B; a, x = c.lead(polys[(md, nm)])
            if a is None: continue
            order = a // 2                                                     # silent amplitude order (= 1 for a = 2, 2 for a = 4)
            Km = {}
            for S_ in itertools.combinations(range(len(c.locs)), order):
                for assign in itertools.product(*[options(c.locs[j]) for j in S_]):
                    faults = [(c.locs[j][0], "p", o[0]) for j, o in zip(S_, assign)]; wgt = 1.0
                    for o in assign: wgt *= math.sqrt(float(o[1]))
                    for i in range(d):
                        v, rec = s05.run(R.sim, R.ops, B[:, i], faults, 0)
                        Km.setdefault(rec, np.zeros((d, d), dtype=complex))[:, i] += wgt * ((-1j) ** order) * (B.conj().T @ v)
            tot = 0.0
            for rec, K in Km.items():
                if not any(bin(rec & mk).count("1") & 1 for mk in c.dets):
                    Kn = K - np.trace(K) / d * np.eye(d); tot += np.linalg.norm(Kn) ** 2 / d
            diffs.append((md, nm, x, tot)); npaths += 1
    ok = all(abs(x - tot) < 1e-8 * max(1, abs(x)) for md, nm, x, tot in diffs)
    check("K3b the leading coefficient from explicit Pauli-fault state vectors (S05's runner, summed coherently over all fault sets of the leading order) equals the polynomial's in all %d cases with deterministic records (Z, X, G, U; L conv, J conv, J flag, ZZZZ-only) in %.0f s; largest absolute difference %.1e" % (npaths, time.time() - t0, max(abs(x - tot) for md, nm, x, tot in diffs)), ok)
    # K4: leading coefficients
    print("      leading coefficients (silent probability ~ coefficient x s^a, s = sin^2(theta/2)): coherent = amplitude-level, twirled = Pauli-twirled channel of the same rotations")
    print("      model  round                       L   order  coherent    twirled    coherent / twirled")
    rows = {}; tol_ok = True; ord_ok = True
    for md in MODELS:
        for nm in ROUNDS:
            c, t = S[(md, nm)], T[(md, nm)]; L, d1, p2, d2 = t.counts(); a, x = c.lead(polys[(md, nm)])
            ta = 1 if d1 > 0 else (2 if p2 > 0 else None); tw = d1 if ta == 1 else (p2 if ta == 2 else Fr(0))
            fr = Fr(x).limit_denominator(2000) if a else Fr(0); tol_ok &= abs(float(fr) - x) < 1e-9
            ord_ok &= (ta is None and a is None) or (ta is not None and a == 2 * ta)
            rows[(md, nm)] = (a, fr, ta, tw)
            print("      %-5s  %-26s %3d   %-5s  %-10s  %-10s  %s" % (md, nm, L, "-" if a is None else "t^%d" % a, "-" if a is None else str(fr), "-" if ta is None else str(tw), "-" if (a is None or ta is None) else "%.3f" % float(fr / tw)))
    check("K4a the lowest nonzero order of the coherent silent probability (in t) is twice the lowest order of the twirled one (in s) for all 20 round x model cases, so the two have the same leading power of the error rate", ord_ok)
    check("K4b every leading coherent coefficient is a rational number with denominator at most 2000 to 1e-9 (the Z, X and G models give integers)", tol_ok and all(rows[(md, nm)][1].denominator == 1 for md in ("Z", "X", "G") for nm in ROUNDS))
    # K5: sign average
    t0 = time.time(); okavg = True; summary = []
    for md in ("Z", "X", "G"):
        for nm in ROUNDS:
            c = S[(md, nm)]; L = len(c.locs); a, fr, ta, tw = rows[(md, nm)]
            if L > 12 or a is None: continue
            vals = []
            for bits in range(1 << L):
                sg = [1.0 - 2.0 * ((bits >> j) & 1) for j in range(L)]
                s = c.poly(a // 2, sg=sg); vals.append(s[a])
            mean = float(np.mean(vals)); okavg &= abs(mean - float(tw)) < 1e-9 * max(1, float(tw)); summary.append((md, nm, L, min(vals), mean, max(vals), float(fr)))
    print("      sign patterns (all 2^L, L <= 12): model round, L, min / mean / max of the leading coefficient, and the same-sign value")
    for r in summary: print("        %-2s %-26s L=%-2d  min %8.3f  mean %8.3f  max %8.3f  same-sign %8.3f" % r)
    check("K5 averaged over all 2^L sign patterns the leading coherent coefficient equals the twirled one exactly in all %d cases with L <= 12 (%.0f s); the same-sign value is the maximum in %d of them" % (len(summary), time.time() - t0, sum(1 for r in summary if abs(r[6] - r[5]) < 1e-9)), okavg and len(summary) == 7)
    # twirled leading coefficient vs dense convolution
    bad = []
    for key, t in T.items():
        a, fr, ta, tw = rows[key]
        if ta is None: continue
        sv = 1e-6; got = t.dist(sv)["silent"]; bad += [] if abs(got / (float(tw) * sv ** ta) - 1) < 5e-3 else [key]
    check("K4c the twirled leading coefficients (exact counts) agree with the dense convolution at s = 1e-6 to 5e-3 relative in all cases", not bad)
    # K6: exact values
    svals = (1e-4, 1e-3, 1e-2); print("      exact silent probability / rejection probability at the same per-location infidelity s (coherent: direct simulation; twirled: dense convolution)")
    RES = {}
    for md in MODELS:
        print("      model %s" % md)
        for nm in ROUNDS:
            c, t = S[(md, nm)], T[(md, nm)]; line = []
            for sv in svals:
                th = 2 * math.asin(math.sqrt(sv)); a = c.direct(th); b = t.dist(sv); RES[(md, nm, sv)] = (a, b)
                line.append("s=%g: coh %.3e (rej %.3f) | tw %.3e (rej %.3f) | x%.2f" % (sv, a["silent"], a["reject"], b["silent"], b["reject"], ratio(a["silent"], b["silent"])))
            print("        %-24s " % nm + "  ".join(line))
    def order_at(md, kind, sv):
        return sorted(ROUNDS, key=lambda nm: RES[(md, nm, sv)][0 if kind == "coh" else 1]["silent"])
    short = {"L conv (baseline)": "local", "J conv": "conv", "J flag": "flag", "J cat (verified)": "cat", "J ZZZZ only (partial)": "Zonly"}
    for md in MODELS:
        print("      %s at s = 1e-3, lowest to highest silent: coherent %s | twirled %s" % (md, " < ".join(short[n] for n in order_at(md, "coh", 1e-3)), " < ".join(short[n] for n in order_at(md, "tw", 1e-3))))
    # amplification factors of the leading coefficient
    amp = {k: float(v[1] / v[3]) for k, v in rows.items() if v[0] is not None}
    check("K4d the same-sign (systematic) leading coefficient is at least the twirled one in all %d round x model cases with a silent term (largest factors: %s)" % (len(amp), ", ".join("%s %s x%.2f" % (md, short[nm], amp[(md, nm)]) for md, nm in sorted(amp, key=lambda k: -amp[k])[:4])), all(v >= 1 - 1e-12 for v in amp.values()))
    adv = lambda md, kind, a, b, sv: RES[(md, b, sv)][0 if kind == "coh" else 1]["silent"] / RES[(md, a, sv)][0 if kind == "coh" else 1]["silent"]
    shr = {md: adv(md, "tw", "J flag", "J conv", 1e-3) / adv(md, "coh", "J flag", "J conv", 1e-3) for md in ("Z", "X", "U")}
    check("K6a the flagged joint round's silent advantage over the conventional joint round at s = 1e-3 (conventional / flagged), twirled -> coherent: %s; the advantage shrinks by a factor %.1f to %.1f and stays above 2 under all three single-qubit models" % (
          "; ".join("%s %.1f -> %.1f" % (md, adv(md, "tw", "J flag", "J conv", 1e-3), adv(md, "coh", "J flag", "J conv", 1e-3)) for md in ("Z", "X", "U")), min(shr.values()), max(shr.values())),
          all(7 < v < 10 for v in shr.values()) and all(adv(md, "coh", "J flag", "J conv", 1e-3) > 2 for md in ("Z", "X", "U")))
    g = lambda md, nm, kind: RES[(md, nm, 1e-3)][0 if kind == "coh" else 1]["silent"]
    check("K6b at s = 1e-3 the flagged and verified-cat rounds swap order between the twirled and the coherent value under X (flagged %.2e < cat %.2e twirled; cat %.2e < flagged %.2e coherent) and under U (%.2e < %.2e twirled; %.2e < %.2e coherent); under Z the cat round is lower in both (%.2e < %.2e coherent) and under G the flagged round is lower in both" % (
          g("X", "J flag", "tw"), g("X", "J cat (verified)", "tw"), g("X", "J cat (verified)", "coh"), g("X", "J flag", "coh"), g("U", "J flag", "tw"), g("U", "J cat (verified)", "tw"), g("U", "J cat (verified)", "coh"), g("U", "J flag", "coh"), g("Z", "J cat (verified)", "coh"), g("Z", "J flag", "coh")),
          all(g(md, "J flag", "tw") < g(md, "J cat (verified)", "tw") and g(md, "J cat (verified)", "coh") < g(md, "J flag", "coh") for md in ("X", "U"))
          and g("Z", "J cat (verified)", "coh") < g("Z", "J flag", "coh") and g("Z", "J cat (verified)", "tw") < g("Z", "J flag", "tw") and g("G", "J flag", "coh") < g("G", "J cat (verified)", "coh") and g("G", "J flag", "tw") < g("G", "J cat (verified)", "tw"))
    # exact crossings in s between rounds
    def crossings(f, lo=1e-5, hi=0.1, n=60):
        xs = [lo * (hi / lo) ** (i / n) for i in range(n + 1)]; out = []; v = [math.log(f(x)) for x in xs]
        for i in range(n):
            if v[i] * v[i + 1] < 0:
                a, b = xs[i], xs[i + 1]
                for _ in range(50):
                    m = math.sqrt(a * b)
                    if math.log(f(m)) * v[i] > 0: a = m
                    else: b = m
                out.append(math.sqrt(a * b))
        return out
    def silent(md, nm, s, kind):
        if kind == "coh": return S[(md, nm)].direct(2 * math.asin(math.sqrt(s)))["silent"]
        return T[(md, nm)].dist(s)["silent"]
    print("      exact crossings in s (silent probability of the first round equals that of the second), s from 1e-5 to 0.1:")
    CR = {}
    for md in ("Z", "X", "U"):
        for a, b in (("J flag", "J conv"), ("J cat (verified)", "J flag"), ("J conv", "L conv (baseline)")):
            for kind in ("coh", "tw"):
                CR[(md, a, b, kind)] = crossings(lambda s: silent(md, a, s, kind) / silent(md, b, s, kind))
            print("        %s  %-5s vs %-5s  coherent %s | twirled %s" % (md, short[a], short[b], ["%.3g" % x for x in CR[(md, a, b, "coh")]] or "none", ["%.3g" % x for x in CR[(md, a, b, "tw")]] or "none"))
    fx = lambda md, a, b, kind: CR[(md, a, b, kind)]
    check("K6c exact crossings (s from 1e-5 to 0.1): the flagged round stays below the conventional joint round over the whole range under Z and U in both treatments and in the twirled X model, but under coherent X noise the two cross at s = %.4f (the flagged round is the lower one only below it); cat versus flagged: coherent crossings Z %s, X %s, U %s against twirled Z %s, X %s, U %s" % (
          fx("X", "J flag", "J conv", "coh")[0], ["%.3g" % x for x in fx("Z", "J cat (verified)", "J flag", "coh")], ["%.3g" % x for x in fx("X", "J cat (verified)", "J flag", "coh")], ["%.3g" % x for x in fx("U", "J cat (verified)", "J flag", "coh")],
          ["%.3g" % x for x in fx("Z", "J cat (verified)", "J flag", "tw")] or "none", ["%.3g" % x for x in fx("X", "J cat (verified)", "J flag", "tw")], ["%.3g" % x for x in fx("U", "J cat (verified)", "J flag", "tw")]),
          fx("Z", "J flag", "J conv", "coh") == [] and fx("U", "J flag", "J conv", "coh") == [] and fx("Z", "J flag", "J conv", "tw") == [] and fx("U", "J flag", "J conv", "tw") == [] and fx("X", "J flag", "J conv", "tw") == []
          and len(fx("X", "J flag", "J conv", "coh")) == 1 and abs(fx("X", "J flag", "J conv", "coh")[0] - 0.0642) < 2e-4 and len(fx("X", "J cat (verified)", "J flag", "coh")) == 1 and abs(fx("X", "J cat (verified)", "J flag", "coh")[0] - 0.00347) < 2e-5
          and len(fx("Z", "J cat (verified)", "J flag", "coh")) == 2 and fx("Z", "J cat (verified)", "J flag", "tw") == [] and len(fx("U", "J cat (verified)", "J flag", "coh")) == 1 and len(fx("U", "J cat (verified)", "J flag", "tw")) == 1)
    return RES, rows, S, T, polys, t00

if __name__ == "__main__":
    RES, rows, S, T, polys, t00 = main()
    print("NOTE  Everything is conditional on the stated rotation models (same angle and sign on every location) and on this definition of silent for superpositions.  Total wall-clock %.0f s" % (time.time() - t00))
    print("ALL PASS" if OK else "FAILED"); sys.exit(0 if OK else 1)
