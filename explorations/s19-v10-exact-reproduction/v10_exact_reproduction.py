#!/usr/bin/env python3
"""S19: independent exact re-derivation of V1.0's biased-noise table, basis-dependent readout lines and photon-loss table.

V1.0 computes these with a Pauli-propagation fault enumerator and a Walsh-Hadamard XOR convolution (floating point, with a 1e-18 truncation).  Here the single-fault effects come from
explicit state-vector runs (S18's engine, extended to the loss locations), the weights are re-derived from V1.0's stated rule (a bias weight b on the Z or the X Pauli of a faulted
qubit; a location faults with probability r and then picks an option in proportion to its weight), and the distribution of the XOR of independent location faults is accumulated by
plain non-negative convolution on a table of 2^13 states (syndrome, herald, data X mask, data Z mask) -- no transform, no cancellation.  An exact rational version of the same
convolution is run on three rounds to show that the floating-point version loses nothing visible.  Every printed number of V1.0's section E (bias table, readout lines) and
section D (loss table, worst-case lines) is then compared with this engine, digit for digit at the printed precision.

Claims
  E0  The engine reproduces V0.9's published probabilities at p = 1e-3: silent and reject (model M2, three figures) for four rounds, and the flagged round's M3 silent probability 3.93e-4.         DERIVED
  E1  All 65 entries of V1.0's bias table (13 rows x 5 rounds) equal this engine's values at the printed precision; the 13 'lowest' labels agree.                                 DERIVED
  E2  The six V1.0 statements about that table (flagged best under Z bias, ~20x local; X-bias reversal; ancilla-only bias; Z-biased data) hold on this engine.                      DERIVED
  E3  V1.0's basis-dependent readout lines (12 silent and 12 reject values) equal this engine's values at the printed precision, and its readout-asymmetry statement holds.        DERIVED
  D1  All 12 rows of V1.0's loss table (survival, heralded-ancilla-loss probability, silent / rejected / usable for h = 1 and h = 0) and the 12 worst-case unheralded-data-loss
      silent values equal this engine's values at the printed precision; V1.0's four loss statements (10x, 60x, 420x, 10 to 30 %) hold.                                              DERIVED
  X1  (new) The X-bias value b* at which the local round's silent probability crosses each joint round's, at p = 1e-3 in model M3, with the same bias on every qubit: b* is found
      by bisection on the exact value; V1.0 printed only b = 10 and b = 100.                                                                                                       DERIVED
  X2  (new) V0.9's exact-probability scan is re-done: its printed crossover 1.12e-3 is the first point of its own 12 % grid past the exact crossing (1.05e-3, new), and the exact crossing
      is computed again under six of V1.0's bias settings.                                                                                                                              DERIVED
Not claimed: V1.0's section F (repeated rounds, Monte Carlo), G, H, I; the bias and loss RATES are V1.0's ASSUMED parameters, not measurements; the location model (M3, loss
locations) is V1.0's definition, re-implemented from its description, not independently chosen.  Author-side; not an independent reproduction.  Requires numpy.  Run with python3 -I.
"""
import importlib.util, itertools, math, os, re, sys, time
from fractions import Fraction as Fr
from collections import defaultdict
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
def _load(name, rel):
    sp = importlib.util.spec_from_file_location(name, os.path.join(ROOT, *rel)); m = importlib.util.module_from_spec(sp)
    sys.modules[name] = m; sp.loader.exec_module(m); return m
s18 = _load("s18", ["explorations", "s18-m3-reproduction", "m3_reproduction.py"])
LOG = open(os.path.join(ROOT, "reproduction", "execution-logs", "v1.0.stdout.txt"), encoding="utf-8").read()

OK = True
def check(name, ok):
    global OK
    OK = OK and bool(ok); print(("PASS  " if ok else "FAIL  ") + name, flush=True)

def locations(ops, loss):
    """V1.0's location kinds.  Each location is (type, options); an option is (fault, weight-pauli dict, herald, unit weight or None)
    types: in (incoming Pauli on a data axis), g (every non-identity Pauli after a gate, preparation or one-qubit operation), mz / mx (record flip), idle (live qubit not touched),
    ld (data photon lost at a two-qubit gate, unheralded: both axes of its photon get a uniformly random Pauli, identity included),
    la_h (ancilla photon lost at a two-qubit gate, HERALDED: the round is flagged), la_u (same loss, UNHERALDED: the ancilla gets a random Pauli, identity included)"""
    alive = set(range(4)); locs = []
    def one(q, i): return [((i, "p", {q: c}), {q: c}, 0) for c in "XYZ"]
    for q in range(4): locs.append(("in", [((-1, "p", {q: c}), {q: c}, 0) for c in "XYZ"]))
    for i, op in enumerate(ops):
        tq = [op[1], op[2]] if op[0] in ("CNOT", "CZ") else [op[1]]
        if op[0] in ("MZ", "MX"): alive.discard(op[1])
        elif op[0] in ("P0", "P+"): alive.add(op[1])
        if op[0] == "MZ": locs.append(("mz", [((i, "m", None), {}, 0)]))
        elif op[0] == "MX": locs.append(("mx", [((i, "m", None), {}, 0)]))
        elif len(tq) == 2:
            a, b = tq; fl = []
            for u in "IXYZ":
                for v in "IXYZ":
                    if u == "I" and v == "I": continue
                    d = {q: c for q, c in ((a, u), (b, v)) if c != "I"}
                    fl.append(((i, "p", d), d, 0))
            locs.append(("g", fl))
        else: locs.append(("g", one(tq[0], i)))
        for q in sorted(alive):
            if q not in tq: locs.append(("idle", one(q, i)))
        if loss and len(tq) == 2:
            for q in tq:
                if q < 4:
                    ax = (2 * (q // 2), 2 * (q // 2) + 1); fl = []
                    for u in "IXYZ":
                        for v in "IXYZ":
                            d = {k: c for k, c in ((ax[0], u), (ax[1], v)) if c != "I"}
                            fl.append(((i, "p", d), None, 0))                     # None: this location's weights are all 1
                    locs.append(("ld", fl))
                else:
                    locs.append(("la_h", [(None, None, 1)]))
                    locs.append(("la_u", [(None, None, 0)] + [((i, "p", {q: c}), None, 0) for c in "XYZ"]))
    return locs

def bias_weight(pd, bias):
    """V1.0's rule: the Z (or X) Pauli of a faulted qubit carries weight b; data qubits are 0..3, ancillas 4 and above; identity components weigh 1"""
    if bias is None or pd is None: return 1.0
    w = 1.0
    for q, c in pd.items():
        kind, b = bias["data" if q < 4 else "anc"]
        if c == kind: w *= b
    return w

class Engine:
    def __init__(self, name, loss=False):
        self.name = name; self.R = R = s18.Rnd(name); self.code = R.code; self.d = d = len(R.dets); self.nb = d + 1 + 8; self.N = 1 << self.nb
        self.locs = locations(R.ops, loss); self.eff = []; consistent = True; self.nfault = 0; self.rate_types = ("g", "mz", "mx", "idle", "in")
        branches = (0,) if not R.nrand else (0, (1 << R.nrand) - 1, 5 % (1 << R.nrand))
        for typ, opts in self.locs:
            row = []
            for f, pd, hr in opts:
                self.nfault += 1
                if f is None or (f[1] == "p" and not f[2]): syn, x, z = 0, 0, 0
                else:
                    es = [R.effect([f], b) for b in branches]
                    consistent &= len({(e[0], s18.classify_err(*e[1], self.code)) for e in es}) == 1 and all(
                        s18.classify_err(es[0][1][0] ^ e[1][0], es[0][1][1] ^ e[1][1], self.code) in ("none", "harmless") for e in es)
                    syn, (x, z) = es[0]
                row.append(syn | (hr << d) | (x << (d + 1)) | (z << (d + 5)))
            self.eff.append(row)
        self.consistent = consistent; idx = np.arange(self.N)
        syn = idx & ((1 << d) - 1); her = (idx >> d) & 1; x = (idx >> (d + 1)) & 15; z = (idx >> (d + 5)) & 15
        cl = np.array([{"none": 0, "harmless": 0, "detected": 1, "logical": 2}[s18.classify_err(int(a), int(b), self.code)] for a, b in zip(x, z)])
        self.m_sil = (her == 0) & (syn == 0) & (cl == 2); self.m_ad = (her == 0) & (syn == 0) & (cl == 1); self.m_ac = (her == 0) & (syn == 0) & (cl == 0)
        self.m_rd = (her == 0) & (syn != 0) & (cl >= 1); self.m_rc = (her == 0) & (syn != 0) & (cl == 0); self.m_h = her == 1; self.idx = idx
    def weights(self, bias):
        out = []
        for (typ, opts) in self.locs:
            w = [bias_weight(pd, bias) if typ in ("in", "g", "idle") else 1.0 for _, pd, _ in opts]; s = sum(w); out.append([a / s for a in w])
        return out
    def dist(self, rates, bias=None):
        P = np.zeros(self.N); P[0] = 1.0; W = self.weights(bias)
        for (typ, _), row, ws in zip(self.locs, self.eff, W):
            r = rates.get(typ, 0.0)
            if r == 0.0: continue
            acc = np.zeros(self.N)
            for e, w in zip(row, ws): acc += w * P[self.idx ^ e]
            P = (1.0 - r) * P + r * acc
        return P
    def at(self, rates, bias=None):
        P = self.dist(rates, bias)
        s = dict(silent=P[self.m_sil].sum(), accept_damaged=P[self.m_ad].sum(), accept_clean=P[self.m_ac].sum(), reject_damaged=P[self.m_rd].sum(), reject_clean=P[self.m_rc].sum(), herald=P[self.m_h].sum())
        s["reject"] = s["reject_damaged"] + s["reject_clean"]; s["total"] = P.sum(); return s
    def at_exact(self, p):
        """the same convolution in exact integer arithmetic (unbiased weights, every location type with the same rate p = Fraction), as a dictionary over reachable states.
        Every location multiplies the scaled state by 15 * den: staying with probability (den - num)/den is (den - num) * 15 units, each of its n options num * (15 / n) units (n is 1, 3 or 15)"""
        num, den = p.numerator, p.denominator; P = {0: 1}; L = 0
        for (typ, _), row in zip(self.locs, self.eff):
            if typ not in self.rate_types: continue
            n = len(row); assert n in (1, 3, 15), n; new = {}
            for k, v in P.items(): new[k] = new.get(k, 0) + (den - num) * 15 * v
            for k, v in P.items():
                for e in row: new[k ^ e] = new.get(k ^ e, 0) + num * (15 // n) * v
            P = new; L += 1
        scale = (15 * den) ** L; out = defaultdict(Fr)
        for k, v in P.items():
            for name, m in (("silent", self.m_sil), ("accept_damaged", self.m_ad), ("accept_clean", self.m_ac), ("reject_damaged", self.m_rd), ("reject_clean", self.m_rc), ("herald", self.m_h)):
                if m[k]: out[name] += Fr(v, scale)
        out["reject"] = out["reject_damaged"] + out["reject_clean"]; return out

def RT(p, **kw):
    d = {"g": p, "mz": p, "mx": p}; d.update(kw); return d

def fmt_ok(computed, printed_str):
    """True if computed rounds to the printed token (scientific with 3 significant figures, or fixed with 4 decimals); a tie at the rounding boundary is accepted to 1e-6 relative"""
    v = float(printed_str)
    if "e" in printed_str: ulp = 10 ** (math.floor(math.log10(abs(v))) - 2) if v != 0 else 1e-18
    else: ulp = 10.0 ** (-len(printed_str.split(".")[1]))
    return abs(computed - v) <= 0.5 * ulp * (1 + 1e-6)

NAMES = ["L conv (baseline)", "J conv", "J flag", "J cat (verified)", "J ZZZZ only (partial)"]

def main():
    t00 = time.time()
    t0 = time.time(); E = {nm: Engine(nm) for nm in NAMES}
    print("      engines built (single-fault state-vector effects for model M3, no loss) in %.0f s: " % (time.time() - t0) + ", ".join("%s %d locations / %d faults, %d detector bits" % (nm, len(e.locs), e.nfault, e.d) for nm, e in E.items()), flush=True)
    check("E0a every single-fault effect is the same, up to stabilizers, on 3 sampled measurement branches in all five rounds", all(e.consistent for e in E.values()))
    check("E0b the convolution conserves probability (total 1 to 1e-12) for every round and a sample of rates", all(abs(e.at(RT(1e-3, idle=1e-3, **{"in": 1e-3}), {"data": ("Z", 7.0), "anc": ("X", 3.0)})["total"] - 1) < 1e-12 for e in E.values()))
    # --- E0: V0.9's published numbers
    v09_sil = {"L conv (baseline)": "5.31e-04", "J conv": "2.66e-04", "J flag": "2.29e-06", "J cat (verified)": "9.66e-06"}
    v09_rej = {"L conv (baseline)": "5.45e-03", "J conv": "8.62e-03", "J flag": "1.61e-02", "J cat (verified)": "3.13e-02"}
    bad = []
    for nm in v09_sil:
        a = E[nm].at(RT(1e-3)); print("      M2 p=1e-3 %-18s silent %.3e (V0.9 %s)  reject %.3e (V0.9 %s)" % (nm, a["silent"], v09_sil[nm], a["reject"], v09_rej[nm]))
        if not (fmt_ok(a["silent"], v09_sil[nm]) and fmt_ok(a["reject"], v09_rej[nm])): bad.append(nm)
    m3 = E["J flag"].at(RT(1e-3, idle=1e-3, **{"in": 1e-3}))["silent"]
    check("E0 at p = 1e-3 model M2 the engine reproduces V0.9's printed silent probabilities (5.31e-4, 2.66e-4, 2.29e-6, 9.66e-6; 3 figures) and rejection probabilities (5.45e-3, 8.62e-3, 1.61e-2, 3.13e-2; all matching except %s), and model M3's flagged silent %.3e = 3.93e-4" % (bad or "none", m3),
          not bad and fmt_ok(m3, "3.93e-04"))
    # --- exact rational cross-check
    ok_x = True
    for nm in ("L conv (baseline)", "J conv", "J flag"):
        t1 = time.time(); ex = E[nm].at_exact(Fr(1, 1000)); fl = E[nm].at(RT(1e-3, idle=1e-3, **{"in": 1e-3}))
        dev = max(abs(float(ex[k]) / fl[k] - 1) for k in ("silent", "reject", "accept_damaged", "accept_clean"))
        print("      exact rational vs float, %-18s silent %.6e  max relative difference %.1e  [%.0f s]" % (nm, float(ex["silent"]), dev, time.time() - t1))
        ok_x &= dev < 1e-9
    check("E0c the exact rational convolution (Fractions, no rounding) and the floating-point one agree to 1e-9 relative on silent, reject, accepted-damaged and accepted-clean for L conv, J conv and J flag at M3 and p = 1e-3", ok_x)

    # --- E1: bias table
    rows = {}
    for m in re.finditer(r"^\s+([ZX])\s+(all|data|anc)\s+(\d+)((?:\s+[0-9.]+e[-+]\d+){5})\s+(.+?)\s*$", LOG, re.M):
        rows[(m.group(1), m.group(2), int(m.group(3)))] = (m.group(4).split(), m.group(5))
    check("E1a V1.0's printed bias table has 13 rows", len(rows) == 13)
    BS = {}; mism = []; nexact = 0; nlow = 0
    for key, (toks, low) in sorted(rows.items(), key=lambda kv: (kv[0][0] != "Z", kv[0][1] != "all", kv[0][2])):
        kind, scope, b = key
        bias = {"data": (kind, b if scope in ("all", "data") else 1), "anc": (kind, b if scope in ("all", "anc") else 1)}
        row = {nm: E[nm].at(RT(1e-3, idle=1e-3, **{"in": 1e-3}), bias)["silent"] for nm in NAMES}; BS[key] = row
        for nm, tok in zip(NAMES, toks):
            if fmt_ok(row[nm], tok): nexact += 1
            else: mism.append((key, nm, row[nm], tok))
        nlow += min(row, key=row.get) == low
        print("      %s %-5s b=%-4d " % (kind, scope, b) + "  ".join("%.2e" % row[nm] for nm in NAMES) + "   lowest: %s (V1.0: %s)" % (min(row, key=row.get), low))
    check("E1b all 65 bias-table entries equal this engine's values at the printed three figures (%d of 65; mismatches: %s)" % (nexact, mism[:4] or "none"), nexact == 65)
    check("E1c the 'lowest' label of every one of the 13 rows agrees (%d of 13)" % nlow, nlow == 13)
    # --- E2: V1.0's statements about the table
    zb = BS[("Z", "all", 100)]; xb = BS[("X", "all", 100)]
    check("E2a Z bias on all qubits, b = 100: the flagged joint round is the lowest of the five and the local round is about 20 times higher (%.1f x)" % (zb["L conv (baseline)"] / zb["J flag"]),
          min(zb, key=zb.get) == "J flag" and zb["L conv (baseline)"] > 20 * zb["J flag"])
    check("E2b X bias on all qubits, b = 100: the local round (%.2e) and the ZZZZ-only round (%.2e) are below both the flagged (%.2e) and the conventional joint (%.2e) round"
          % (xb["L conv (baseline)"], xb["J ZZZZ only (partial)"], xb["J flag"], xb["J conv"]),
          xb["L conv (baseline)"] < xb["J flag"] and xb["L conv (baseline)"] < xb["J conv"] and xb["J ZZZZ only (partial)"] < xb["J flag"])
    check("E2c bias on the ancillas alone (X or Z, b = 10 and 100): the flagged round is the lowest of the five", all(min(BS[(k, "anc", b)], key=BS[(k, "anc", b)].get) == "J flag" for k in ("Z", "X") for b in (10, 100)))
    check("E2d Z-biased data alone, b = 100: the conventional joint round (%.2e) is below the flagged one (%.2e)" % (BS[("Z", "data", 100)]["J conv"], BS[("Z", "data", 100)]["J flag"]), BS[("Z", "data", 100)]["J conv"] < BS[("Z", "data", 100)]["J flag"])

    # --- E3: readout lines
    ok_r = True; cnt = 0; RD = {}
    for nm in NAMES[:3] + NAMES[4:]:
        mm = re.search(r"^\s+" + re.escape(nm) + r"\s+(mx=.*)$", LOG, re.M)
        trip = re.findall(r"mx=([\d.]+): silent ([\d.e+-]+), reject ([\d.]+)", mm.group(1)); assert len(trip) == 3
        for mx, sil, rej in trip:
            a = E[nm].at({"g": 1e-3, "mz": 1e-3, "mx": float(mx)}); RD[(nm, float(mx))] = a
            good = fmt_ok(a["silent"], sil) and fmt_ok(a["reject"], rej); cnt += 2 * good; ok_r &= good
            if not good: print("      MISMATCH readout %s mx=%s: silent %.3e vs %s, reject %.4f vs %s" % (nm, mx, a["silent"], sil, a["reject"], rej))
    check("E3a all 12 (silent, reject) pairs of V1.0's basis-dependent readout lines equal this engine's values at the printed precision (%d of 24 numbers)" % cnt, ok_r and cnt == 24)
    f1, f3 = RD[("J flag", 1e-3)], RD[("J flag", 3e-2)]
    check("E3b readout asymmetry: flagged rejection %.4f -> %.4f, silent x%.2f; the local and the ZZZZ-only round are exactly unchanged (they read out only in the Z basis)" % (f1["reject"], f3["reject"], f3["silent"] / f1["silent"]),
          2.2 < f3["silent"] / f1["silent"] < 3.0 and RD[("L conv (baseline)", 3e-2)]["silent"] == RD[("L conv (baseline)", 1e-3)]["silent"] and RD[("J ZZZZ only (partial)", 3e-2)]["silent"] == RD[("J ZZZZ only (partial)", 1e-3)]["silent"])

    # --- D1: loss
    t0 = time.time(); EL = {nm: Engine(nm, loss=True) for nm in NAMES[:4]}
    print("      loss engines built in %.0f s: " % (time.time() - t0) + ", ".join("%s %d locations / %d faults" % (nm, len(e.locs), e.nfault) for nm, e in EL.items()), flush=True)
    check("D0 every single-fault effect, including the loss locations, is the same up to stabilizers on 3 sampled measurement branches", all(e.consistent for e in EL.values()))
    NDA = {nm: sum(1 for o in EL[nm].R.ops if o[0] in ("CNOT", "CZ") and ((o[1] < 4) != (o[2] < 4))) for nm in EL}
    rows = []
    for m in re.finditer(r"^\s+(L conv \(baseline\)|J conv|J flag|J cat \(verified\))\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+\|\s+([\d.e+-]+)\s+([\d.]+)\s+([\d.]+)\s+\|\s+([\d.e+-]+)\s+([\d.]+)\s+([\d.]+)\s*$", LOG, re.M):
        rows.append(m.groups())
    check("D1a V1.0's printed loss table has 12 rows", len(rows) == 12)
    DL = {}; nok = 0; ntot = 0; bad = []
    for nm, q, S_, hp, s1, r1, u1, s0, r0, u0 in rows:
        qf = float(q); S = (1 - qf) ** NDA[nm]; row = {}
        for h in (1.0, 0.0):
            e = EL[nm].at(RT(1e-3, la_h=qf * h, la_u=qf * (1 - h))); acc = e["silent"] + e["accept_damaged"] + e["accept_clean"]
            row[h] = (e["silent"], e["reject"] + e["herald"], acc * S, e["herald"])
        DL[(nm, qf)] = row
        for val, tok in ((S, S_), (row[1.0][3], hp), (row[1.0][0], s1), (row[1.0][1], r1), (row[1.0][2], u1), (row[0.0][0], s0), (row[0.0][1], r0), (row[0.0][2], u0)):
            ntot += 1; good = fmt_ok(val, tok); nok += good
            if not good: bad.append((nm, qf, val, tok))
    check("D1b all 96 numbers of the 12 loss-table rows equal this engine's values at the printed precision (%d of %d; mismatches: %s)" % (nok, ntot, bad[:3] or "none"), nok == ntot == 96)
    WLr = {}
    for nm in EL:
        mm = re.search(r"^\s+" + re.escape(nm) + r"\s+silent at q=\[[^\]]*\]: (.+)$", LOG, re.M); toks = [t.strip() for t in mm.group(1).split(",")]
        WLr[nm] = [EL[nm].at(RT(1e-3, ld=q, la_h=q))["silent"] for q in (1e-3, 1e-2, 5e-2)]
        WLr[nm + "_tok"] = toks
    check("D1c the 12 worst-case (unheralded data loss) silent values equal V1.0's printed ones at three figures", all(fmt_ok(v, t) for nm in EL for v, t in zip(WLr[nm], WLr[nm + "_tok"])))
    r10 = DL[("L conv (baseline)", 1e-2)][0.0][0] / DL[("L conv (baseline)", 1e-2)][1.0][0]; r60 = DL[("J flag", 1e-2)][0.0][0] / DL[("J flag", 1e-2)][1.0][0]
    base = E["J flag"].at(RT(1e-3))["silent"]; r420 = WLr["J flag"][0] / base; rat = [WLr["J flag"][i] / WLr["J conv"][i] for i in range(3)]
    check("D2a unheralded ancilla loss raises the silent probability at q = 1e-2 by %.1f x for the local round and %.1f x for the flagged round (V1.0: 'about 10' and 'about 60')" % (r10, r60), 8 < r10 < 12 and 50 < r60 < 70)
    check("D2b unheralded data loss at q = 1e-3 puts the flagged round at %.2e, %.0f x its loss-free value %.2e (V1.0: about 420 x), and %.2f to %.2f of the conventional joint round's across q" % (WLr["J flag"][0], r420, base, min(rat), max(rat)), 400 < r420 < 440 and all(0.7 < x < 0.95 for x in rat))
    check("D2c the data survival exponents are the data-ancilla gate counts %s: %.4f (local) and %.4f (joint, all three) at q = 1e-2" % (NDA, 0.99 ** NDA["L conv (baseline)"], 0.99 ** NDA["J conv"]),
          NDA == {"L conv (baseline)": 4, "J conv": 8, "J flag": 8, "J cat (verified)": 8})

    # --- X1: X-bias crossover (new)
    def silent_X(nm, b): return E[nm].at(RT(1e-3, idle=1e-3, **{"in": 1e-3}), {"data": ("X", b), "anc": ("X", b)})["silent"]
    def crossing(nm):
        lo, hi = 1.0, 1000.0
        f = lambda b: silent_X("L conv (baseline)", b) - silent_X(nm, b)
        assert f(lo) > 0 > f(hi), (nm, f(lo), f(hi))
        for _ in range(60):
            mid = math.sqrt(lo * hi)
            if f(mid) > 0: lo = mid
            else: hi = mid
        return math.sqrt(lo * hi)
    bst = {nm: crossing(nm) for nm in ("J conv", "J flag", "J cat (verified)")}
    # monotonic check on a grid: the local round's silent probability falls and the joint rounds' rises, so each crossing is unique
    grid = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]; mono = True
    for nm in NAMES:
        vals = [silent_X(nm, b) for b in grid]
        if nm.startswith("L") or "ZZZZ" in nm: mono &= all(a >= b_ * (1 - 1e-12) for a, b_ in zip(vals, vals[1:]))
        else: mono &= all(a <= b_ * (1 + 1e-12) for a, b_ in zip(vals, vals[1:]))
    print("      X bias on every qubit, M3, p = 1e-3: local silent equals J conv at b = %.1f, J flag at b = %.1f, J cat at b = %.1f" % (bst["J conv"], bst["J flag"], bst["J cat (verified)"]))
    check("X1a on the grid b = 1..1000 the local and ZZZZ-only rounds' silent probability is non-increasing in the X bias and every joint round's non-decreasing (so each crossing on the grid is unique)", mono)
    brk = {}
    for nm in bst:
        pts = [(1, BS[("Z", "all", 1)]), (10, BS[("X", "all", 10)]), (100, BS[("X", "all", 100)])]
        above = [b for b, r in pts if r["L conv (baseline)"] > r[nm]]; below = [b for b, r in pts if r["L conv (baseline)"] < r[nm]]
        brk[nm] = (max(above), min(below))
    check("X1b the crossings lie inside the brackets given by V1.0's printed rows b = 1, 10, 100: " + "; ".join("%s %.1f in (%d, %d)" % (nm, bst[nm], *brk[nm]) for nm in bst), all(brk[nm][0] < bst[nm] < brk[nm][1] for nm in bst))
    # --- X2: the flagged-versus-conventional crossing in p (V0.9's M3 scan) and how a noise bias moves it (new)
    def sil_p(nm, p, bias=None): return E[nm].at(RT(p, idle=p, **{"in": p}), bias)["silent"]
    def p_star(bias, lo=1e-5, hi=1e-1):
        f = lambda p: sil_p("J conv", p, bias) - sil_p("J flag", p, bias)          # positive while the flagged round is better
        grid = [lo * (hi / lo) ** (i / 60) for i in range(61)]; signs = [f(g) > 0 for g in grid]
        ch = [i for i in range(60) if signs[i] != signs[i + 1]]
        out = []
        for i in ch:
            a, b = grid[i], grid[i + 1]
            for _ in range(60):
                m = math.sqrt(a * b)
                if (f(m) > 0) == signs[i]: a = m
                else: b = m
            out.append(math.sqrt(a * b))
        return out, signs[0]
    ps0, flag_better_at_low = p_star(None)
    grid9 = [10 ** (-5 + 0.05 * i) for i in range(71)]                                  # V0.9's scan grid, 1e-5 .. 10^-1.5, 12 % steps
    first = next(g for g in grid9 if sil_p("J conv", g) < sil_p("J flag", g))             # V0.9's "crossover": the first grid point where the conventional round is lower
    below = max(g for g in grid9 if g < first)
    print("      unbiased M3: flagged round better at low p: %s; exact crossings of the silent probabilities (p per location): %s" % (flag_better_at_low, ["%.4e" % x for x in ps0]))
    print("      V0.9's grid: the last point with the flagged round better is %.4e, the first with the conventional round better is %.4e (V0.9 printed 1.12e-03)" % (below, first))
    check("X2a V0.9's printed 'crossover' 1.12e-03 is reproduced as the first point of its own 71-point grid (12 %% steps) at which the conventional joint round is lower (%.2e); the exact crossing is p* = %.4e, inside the grid cell (%.4e, %.4e]; the order flips back at a second crossing %.3e where silent probabilities are %.3f (flagged) and %.3f (conventional)" % (first, ps0[0], below, first, ps0[1], sil_p("J flag", ps0[1]), sil_p("J conv", ps0[1])),
          len(ps0) == 2 and flag_better_at_low and fmt_ok(first, "1.12e-03") and below < ps0[0] <= first and ps0[1] > 1e-2)
    res = {}; tab = {"Z all b=10": ("Z", "all", 10), "Z all b=100": ("Z", "all", 100), "X all b=10": ("X", "all", 10), "X all b=100": ("X", "all", 100), "Z anc b=100": ("Z", "anc", 100), "Z data b=100": ("Z", "data", 100)}
    bsp = {k: {"data": (k[0], k[2] if k[1] in ("all", "data") else 1), "anc": (k[0], k[2] if k[1] in ("all", "anc") else 1)} for k in tab.values()}
    for label, key in tab.items():
        res[label] = p_star(bsp[key])
        print("      %-13s flagged better at low p: %-5s  crossings: %s" % (label, res[label][1], ["%.3e" % x for x in res[label][0]] or "none in 1e-5..1e-1"))
    ok = True
    for label, key in tab.items():
        xs, low = res[label]; better_at_1e3 = low ^ (sum(x < 1e-3 for x in xs) % 2 == 1)
        ok &= better_at_1e3 == (BS[key]["J flag"] < BS[key]["J conv"])
    check("X2b the crossings found by the scan (one per bias setting listed above, possibly none) are consistent with the order of J flag and J conv at p = 1e-3 in V1.0's printed table for all six settings", ok)
    print("NOTE  Everything here is conditional on V1.0's location model and its ASSUMED rates and bias weights (all qubits at the same bias, p = 1e-3 per location, the rule that a faulted location picks a Pauli in proportion to its weight).  The b* values are exact for that model, not predictions for a device.  Total wall-clock %.0f s" % (time.time() - t00))
    print("ALL PASS" if OK else "FAILED")
    return 0 if OK else 1

if __name__ == "__main__": sys.exit(main())
