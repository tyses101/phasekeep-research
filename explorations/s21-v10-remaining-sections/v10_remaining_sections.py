#!/usr/bin/env python3
"""S21: independent re-derivation of the rest of V1.0's numbers: repeated rounds (section F), the amplification run counts (section G), the Pauli-class counts (section H) and the
capability-report selection (section I).

S19 reproduced V1.0's sections D and E and the V0.9 M3 scan with a different engine.  This script does the same for the sections S19 did not touch:

  F  Repeated rounds.  V1.0 propagates the accumulated data error through 20 rounds with a table of round transitions and a table of syndromes.  Here the round transitions come from
     S19's convolution engine, the syndrome of an accumulated data error from explicit state-vector runs (one run per error, 256 per round), and the recursion is re-written.
  G  Amplification.  V1.0's run counts use exact binomial tails when the means are small and a normal approximation when both means exceed 60.  Here every tail is computed exactly
     (regularized incomplete beta by continued fraction, which V1.0 does not use), with V1.0's own search procedure for the smallest run count, so the rows where V1.0 used the
     approximation can be compared with the exact answer.
  H  Pauli classes of the two codes by brute force with a symplectic representation written here.
  I  Capability rows and Pareto selections for V1.0's four profiles from S19's exact distributions, with the selection rule re-written from its description.

Claims
  F1  The repeated-round recursion at one round equals the single-round exact distribution with incoming faults on (accepted mass and silent probability, flagged joint round, p = 1e-3).   DERIVED
  F2  All 162 printed numbers of V1.0's repeated-round table (3 values of p x 4 rounds x 3 round counts x 3 columns, plus the two no-verification baselines) equal this engine's values at
      the printed precision, and V1.0's statement about 20 rounds at p = 1e-3 holds (0.20 % damaged among accepted flagged-joint runs against 3.7 % local and 7.7 % unverified; 64 % and 46 %
      still accepted).                                                                                                                                                                          DERIVED
  G1  119829, 48 and 2 runs (d = 0.01 at N = 1, 50, 256, no stochastic noise) follow from the closed form ceil(ln 0.05 / ln(1 - sin^2(N d / 2))).                                              DERIVED
  G2  All 12 rows of V1.0's amplification table are compared with the true minimum run count under exact binomial tails (the predicate is a sawtooth in the run count, so V1.0's 2 %
      step search need not land on the minimum): whether each printed count is valid, and how far above the minimum it lies.                                                                                                                                 DERIVED
  H1  Both codes have 3 stabilizer, 60 logical and 192 check-disturbing non-identity Pauli products; minimum weights stabilizer 2 / 4 and logical 1 / 2 (local / joint).                          DERIVED
  I1  Every row of V1.0's capability report for profiles P0 to P3 (silent, unusable, attempts, photons, completion, coverage) and every feasible and Pareto set equal this engine's.            DERIVED
Not claimed: V1.0's sections A to E (S19), B and C (inter-photon counts and completion probabilities, closed forms already checked in S07 to S09), the Monte Carlo validation of V1.0's own engine,
or any value of the assumed rates.  Author-side; not an independent reproduction.  Requires numpy.  Run with python3 -I.
"""
import ast, importlib.util, itertools, math, os, re, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
def _load(name, rel):
    sp = importlib.util.spec_from_file_location(name, os.path.join(ROOT, *rel)); m = importlib.util.module_from_spec(sp)
    sys.modules[name] = m; sp.loader.exec_module(m); return m
s19 = _load("s19", ["explorations", "s19-v10-exact-reproduction", "v10_exact_reproduction.py"])
s18 = s19.s18
LOG = open(os.path.join(ROOT, "reproduction", "execution-logs", "v1.0.stdout.txt"), encoding="utf-8").read()
fmt_ok = s19.fmt_ok

OK = True
def check(name, ok):
    global OK
    OK = OK and bool(ok); print(("PASS  " if ok else "FAIL  ") + name, flush=True)

# ------------------------------------------------------------------ F. repeated rounds
def syndrome_table(E):
    """syndrome of every accumulated data error (x | z << 4) before a round, from explicit state-vector runs"""
    R = E.R; tab = []
    for e in range(256):
        x, z = e & 15, e >> 4; d = {}
        for q in range(4):
            c = "".join(ch for ch, on in (("X", (x >> q) & 1), ("Z", (z >> q) & 1)) if on)
            if c: d[q] = {"X": "X", "Z": "Z", "XZ": "Y"}[c]
        tab.append(0 if not d else R.effect([(-1, "p", d)])[0])
    return tab

def transitions(E, p):
    """T[round syndrome][error pattern x | z << 4] = probability, model M2 with every location at p (V1.0's setting for this table)"""
    P = E.dist({"g": p, "mz": p, "mx": p}); d = E.d; T = {}
    for f in np.nonzero(P)[0]:
        syn = int(f) & ((1 << d) - 1); ef = ((int(f) >> (d + 1)) & 15) | (((int(f) >> (d + 5)) & 15) << 4)
        T.setdefault(syn, np.zeros(256))[ef] += P[f]
    return T

def incoming(dist, p):
    for q in range(4):
        new = (1 - p) * dist
        for u in ((1, 0), (1, 1), (0, 1)):
            f = (u[0] << q) | ((u[1] << q) << 4); idx = np.arange(256) ^ f; new = new + (p / 3) * dist[idx]
        dist = new
    return dist

def summarize(dist, code):
    r = {"clean": 0.0, "pending": 0.0, "silent": 0.0}
    for e in range(256):
        if dist[e] > 0: r[{"none": "clean", "harmless": "clean", "detected": "pending", "logical": "silent"}[s18.classify_err(e & 15, e >> 4, code)]] += dist[e]
    return r

def repeated(E, SYN, p, rounds):
    dist = np.zeros(256); dist[0] = 1.0; T = transitions(E, p); out = {}; idx = np.arange(256)
    for r in range(1, max(rounds) + 1):
        dist = incoming(dist, p); new = np.zeros(256)
        for e0 in range(256):
            if dist[e0] > 0 and SYN[e0] in T:
                row = T[SYN[e0]]; new[idx ^ e0] += dist[e0] * row                     # new error = e0 xor the round's own error pattern
        dist = new
        if r in rounds: out[r] = (dist.sum(), summarize(dist, E.code))
    return out

def unverified(code, p, rounds):
    dist = np.zeros(256); dist[0] = 1.0; out = {}
    for r in range(1, max(rounds) + 1):
        dist = incoming(dist, p)
        if r in rounds: out[r] = summarize(dist, code)
    return out

# ------------------------------------------------------------------ G. exact binomial tails
def _betacf(a, b, x):
    FPMIN = 1e-300; qab = a + b; qap = a + 1.0; qam = a - 1.0; c = 1.0; d = 1.0 - qab * x / qap
    d = 1.0 / (d if abs(d) > FPMIN else FPMIN); h = d
    for m in range(1, 200000):
        m2 = 2 * m; aa = m * (b - m) * x / ((qam + m2) * (a + m2)); d = 1.0 + aa * d; d = d if abs(d) > FPMIN else FPMIN
        c = 1.0 + aa / c; c = c if abs(c) > FPMIN else FPMIN; d = 1.0 / d; h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2)); d = 1.0 + aa * d; d = d if abs(d) > FPMIN else FPMIN
        c = 1.0 + aa / c; c = c if abs(c) > FPMIN else FPMIN; d = 1.0 / d; de = d * c; h *= de
        if abs(de - 1.0) < 1e-15: break
    return h

def betai(a, b, x):
    if x <= 0.0: return 0.0
    if x >= 1.0: return 1.0
    bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log1p(-x))
    return bt * _betacf(a, b, x) / a if x < (a + 1.0) / (a + b + 2.0) else 1.0 - bt * _betacf(b, a, 1.0 - x) / b

def sf(c, R, P):
    """P(Bin(R, P) >= c)"""
    if c <= 0: return 1.0
    if c > R: return 0.0
    if P <= 0.0: return 0.0
    if P >= 1.0: return 1.0
    return betai(c, R - c + 1, P)

def detect_exact(R, P0, P1, alpha=0.05, power=0.95):
    """smallest threshold c with P(X >= c | no error) <= alpha, then is P(X >= c | error) >= power (exact binomial tails)"""
    if P0 <= 0.0: c = 1
    else:
        lo, hi = 1, R + 1
        while lo < hi:
            mid = (lo + hi) // 2
            if sf(mid, R, P0) <= alpha: hi = mid
            else: lo = mid + 1
        c = lo
    if c > R: return False
    return sf(c, R, P1) >= power

def feasible_scan(Rlo, Rhi, P0, P1, alpha=0.05, power=0.95):
    """brute force: every R in [Rlo, Rhi] for which the exact criterion is met (the smallest threshold c with P(X >= c | no error) <= alpha is non-decreasing in R, so one pointer is enough)"""
    lo, hi = 1, Rlo + 1
    while lo < hi:
        mid = (lo + hi) // 2
        if sf(mid, Rlo, P0) <= alpha: hi = mid
        else: lo = mid + 1
    c = lo; out = []
    for R in range(Rlo, Rhi + 1):
        while sf(c, R, P0) > alpha: c += 1
        if c <= R and sf(c, R, P1) >= power: out.append(R)
    return out

def min_runs_exact(P0, P1, alpha=0.05, power=0.95):
    """the true minimum number of runs R for which SOME threshold c gives P(X >= c | no error) <= alpha and P(X >= c | error) >= power, with exact binomial tails.
    For a fixed threshold c both tails grow with R, so the feasible R form an interval [R1(c), R2(c)]; R1 and R2 both grow with c and R2 - R1 grows too, so the smallest feasible c gives the minimum R1."""
    if P0 <= 0.0: return 1 if P1 >= 1.0 else math.ceil(math.log(1 - power) / math.log1p(-P1))
    def R1(c):
        hi = max(2 * c, 8)
        while sf(c, hi, P1) < power: hi *= 2
        lo = c
        while lo < hi:
            mid = (lo + hi) // 2
            if sf(c, mid, P1) >= power: hi = mid
            else: lo = mid + 1
        return lo
    def R2(c):                                               # largest R with sf(c, R, P0) <= alpha
        lo = c - 1; hi = max(2 * c, 8)
        while sf(c, hi, P0) <= alpha: lo = hi; hi *= 2
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if sf(c, mid, P0) <= alpha: lo = mid
            else: hi = mid
        return lo
    feas = lambda c: R1(c) <= R2(c)
    hi = 1
    while not feas(hi): hi *= 2
    lo = hi // 2 + 1 if hi > 1 else 1
    while lo < hi:
        mid = (lo + hi) // 2
        if feas(mid): hi = mid
        else: lo = mid + 1
    return R1(lo)

def click_probs(d, N, eps):
    b = (1 - (1 - eps) ** N) / 2; s = math.sin(N * d / 2) ** 2
    return b, b + s - 2 * b * s

# ------------------------------------------------------------------ H. Pauli classes, written independently (symplectic bits)
def pauli_classes(code):
    gens = {"L": [(0, 0b0011), (0, 0b1100)], "J": [(0, 0b1111), (0b1111, 0)]}[code]       # (x mask, z mask)
    par = lambda v: bin(v).count("1") & 1
    anti = lambda a, b: par(a[0] & b[1]) ^ par(a[1] & b[0])
    stab = {(0, 0)}
    for r in range(1, 3):
        for sub in itertools.combinations(gens, r):
            x = z = 0
            for g in sub: x ^= g[0]; z ^= g[1]
            stab.add((x, z))
    cnt = {}; mw = {}
    for x in range(16):
        for z in range(16):
            if (x, z) == (0, 0): continue
            c = "disturbs checks" if any(anti((x, z), g) for g in gens) else ("stabilizer" if (x, z) in stab else "logical")
            cnt[c] = cnt.get(c, 0) + 1; w = bin(x | z).count("1"); mw[c] = min(mw.get(c, 9), w)
    return cnt, mw

def main():
    t00 = time.time(); names = ["L conv (baseline)", "J conv", "J flag", "J cat (verified)"]
    E = {nm: s19.Engine(nm) for nm in names + ["J ZZZZ only (partial)"]}
    # ---- F
    SYN = {nm: syndrome_table(E[nm]) for nm in names}
    print("      syndrome tables built (256 state-vector runs per round) in %.0f s" % (time.time() - t00), flush=True)
    rows = {}; PR = [1e-4, 1e-3, 1e-2]; cur = None
    seg = LOG[LOG.index("== F. repeated rounds"):LOG.index("CONSISTENCY: the repeated-round recursion")]
    for line in seg.splitlines():
        m = re.match(r"\s+p = ([\d.e+-]+)\s*$", line)
        if m: cur = float(m.group(1)); continue
        m = re.match(r"\s+(L conv \(baseline\)|J conv|J flag|J cat \(verified\)|no verification \(stabilizers of [LJ]\))\s+(.*?)\s*$", line)
        if m and cur is not None and len(m.group(2).split()) == 9: rows[(m.group(1), cur)] = m.group(2).split()
    check("F0 V1.0's printed repeated-round table has 18 rows (6 methods x 3 values of p)", len(rows) == 18)
    RND = {}; nok = 0; ntot = 0; bad = []
    for p in PR:
        for nm in names:
            out = repeated(E[nm], SYN[nm], p, (1, 5, 20))
            for i, r in enumerate((1, 5, 20)):
                acc, sm = out[r]; RND[(nm, p, r)] = (acc, sm); toks = rows[(nm, p)][3 * i:3 * i + 3]
                for val, tok in ((acc, toks[0]), (sm["pending"] + sm["silent"], toks[1]), (sm["silent"], toks[2])):
                    ntot += 1; good = fmt_ok(val, tok); nok += good
                    if not good: bad.append((nm, p, r, val, tok))
        for code in ("L", "J"):
            key = "no verification (stabilizers of %s)" % code; out = unverified(code, p, (1, 5, 20))
            for i, r in enumerate((1, 5, 20)):
                sm = out[r]; RND[("none-" + code, p, r)] = (1.0, sm); toks = rows[(key, p)][3 * i:3 * i + 3]
                for val, tok in ((1.0, toks[0]), (sm["pending"] + sm["silent"], toks[1]), (sm["silent"], toks[2])):
                    ntot += 1; good = fmt_ok(val, tok); nok += good
                    if not good: bad.append((key, p, r, val, tok))
    check("F2a all %d printed numbers of V1.0's repeated-round table equal this engine's values at the printed precision (%d of %d; mismatches: %s)" % (ntot, nok, ntot, bad[:3] or "none"), nok == ntot == 162)
    e1 = E["J flag"].at({"g": 1e-3, "mz": 1e-3, "mx": 1e-3, "in": 1e-3}); acc1 = e1["silent"] + e1["accept_damaged"] + e1["accept_clean"]
    check("F1 the repeated-round recursion at R = 1 equals the single-round exact distribution with incoming faults on (flagged joint, p = 1e-3): accepted mass %.9f vs %.9f, silent %.6e vs %.6e" % (
          RND[("J flag", 1e-3, 1)][0], acc1, RND[("J flag", 1e-3, 1)][1]["silent"], e1["silent"]), abs(RND[("J flag", 1e-3, 1)][0] - acc1) < 1e-9 and abs(RND[("J flag", 1e-3, 1)][1]["silent"] - e1["silent"]) < 1e-9)
    cd = lambda k, p, r: (RND[(k, p, r)][1]["pending"] + RND[(k, p, r)][1]["silent"]) / RND[(k, p, r)][0]
    check("F2b 20 rounds at p = 1e-3: among accepted runs %.3f %% of flagged-joint runs are damaged against %.1f %% local and %.1f %% unverified (joint code); %.1f %% (flagged) and %.1f %% (verified cat) of runs are still accepted"
          % (100 * cd("J flag", 1e-3, 20), 100 * cd("L conv (baseline)", 1e-3, 20), 100 * cd("none-J", 1e-3, 20), 100 * RND[("J flag", 1e-3, 20)][0], 100 * RND[("J cat (verified)", 1e-3, 20)][0]),
          cd("J flag", 1e-3, 20) < 0.0025 and cd("L conv (baseline)", 1e-3, 20) > 0.03 and abs(cd("none-J", 1e-3, 20) - 0.0767) < 2e-4
          and abs(RND[("J flag", 1e-3, 20)][0] - 0.6436) < 5e-4 and abs(RND[("J cat (verified)", 1e-3, 20)][0] - 0.4644) < 5e-4)
    # ---- G
    d = 0.01; closed = {N: math.ceil(math.log(0.05) / math.log1p(-math.sin(N * d / 2) ** 2)) for N in (1, 50, 256)}
    check("G1 closed form ceil(ln 0.05 / ln(1 - sin^2(N d / 2))) at d = 0.01 gives %s for N = 1, 50, 256 (V1.0: 119829, 48, 2)" % [closed[N] for N in (1, 50, 256)], [closed[N] for N in (1, 50, 256)] == [119829, 48, 2])
    gt = {}
    for m in re.finditer(r"^\s+(0\.01|0\.03|0\.1)\s+(0|0\.0001|0\.001|0\.01)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([\d.]+)x\s*$", LOG, re.M):
        gt[(float(m.group(1)), float(m.group(2)))] = tuple(int(m.group(i)) for i in (3, 4, 5, 6)) + (float(m.group(7)),)
    check("G0 V1.0's printed amplification table has 12 rows", len(gt) == 12)
    # exact amplification table: true minimum run counts, and whether V1.0's printed counts are valid under exact tails
    mine = {}; t1 = time.time(); valid1 = {}; validb = {}
    for (dd, eps) in gt:
        b0, p0 = click_probs(dd, 1, eps); r1 = min_runs_exact(b0, p0); best = None; N = 1
        while N <= math.pi / dd:
            Q0, Q1 = click_probs(dd, N, eps)
            if Q1 > Q0 + 1e-12:
                rr = min_runs_exact(Q0, Q1)
                if best is None or rr * N < best[2]: best = (N, rr, rr * N)
            N *= 2
        mine[(dd, eps)] = (r1, best[0], best[1], best[2], r1 / best[2])
        r1v, Nv, rv = gt[(dd, eps)][:3]; Q0, Q1 = click_probs(dd, Nv, eps)
        valid1[(dd, eps)] = detect_exact(r1v, b0, p0); validb[(dd, eps)] = detect_exact(rv, Q0, Q1)
    print("      amplification table with exact binomial tails computed in %.0f s" % (time.time() - t1))
    print("      d       eps      N=1 runs: V1.0 | exact minimum (valid under exact tails?)    best N: V1.0 | exact   runs at best N: V1.0 | exact   branch V1.0 used at N=1")
    devs = []
    for key in sorted(gt, key=lambda k: (k[0], k[1])):
        (r1v, Nv, rv, totv, sv), (r1, N, rr, tot, sv2) = gt[key], mine[key]; b0, p0 = click_probs(key[0], 1, key[1])
        approx = r1v * min(b0, 1 - b0) >= 60 and r1v * min(p0, 1 - p0) >= 60
        print("      %-6g  %-8g %11d | %-11d (%-5s, %+.2f %%)      %5d | %-5d              %5d | %-5d       %s" % (key[0], key[1], r1v, r1, "valid" if valid1[key] else "NOT valid", 100 * (r1v / r1 - 1), Nv, N, rv, rr, "normal approximation" if approx else "exact binomial"))
        devs.append((r1v / r1 - 1, key, approx))
    exact_rows = [k for k in gt if not (gt[k][0] * min(click_probs(k[0], 1, k[1])[0], 1 - click_probs(k[0], 1, k[1])[0]) >= 60 and gt[k][0] * min(click_probs(k[0], 1, k[1])[1], 1 - click_probs(k[0], 1, k[1])[1]) >= 60)]
    appr_rows = [k for k in gt if k not in exact_rows]
    dv = lambda k: gt[k][0] / mine[k][0] - 1
    check("G2a the %d rows where V1.0's N = 1 count came from its exact binomial branch: each printed count meets the exact criterion and lies %.2f %% to %.2f %% above the true minimum (its 2 %% step search stops at or above the minimum)" % (
          len(exact_rows), 100 * min(dv(k) for k in exact_rows), 100 * max(dv(k) for k in exact_rows)), len(exact_rows) == 8 and all(valid1[k] and -1e-12 <= dv(k) < 0.02 for k in exact_rows))
    check("G2b the %d rows where V1.0 used its normal approximation (both means >= 60): the printed N = 1 count differs from the true exact minimum by %+.2f %% to %+.2f %%; the exact criterion is met at the printed count in %d of them (the feasible run counts form a sawtooth, so a count a few hundred above the minimum can be infeasible)" % (
          len(appr_rows), 100 * min(dv(k) for k in appr_rows), 100 * max(dv(k) for k in appr_rows), sum(valid1[k] for k in appr_rows)), len(appr_rows) == 4 and max(abs(dv(k)) for k in appr_rows) < 0.002)
    badb = [k for k in gt if not validb[k]]
    sv_d = {k: (gt[k][0] / gt[k][3]) / (mine[k][0] / mine[k][3]) - 1 for k in gt}
    check("G2c best N equals the exact best N in %d of 12 rows; V1.0's best-N run count meets the exact criterion in %d of 12 rows%s; V1.0's printed saving factor (N = 1 runs / best-N runs) differs from the exact factor by %+.1f %% to %+.1f %%" % (
          sum(gt[k][1] == mine[k][1] for k in gt), 12 - len(badb),
          "" if not badb else " (the exception%s: %s)" % ("s" if len(badb) > 1 else "", ", ".join("d=%g eps=%g at N=%d: V1.0 %d runs, exact minimum %d" % (k[0], k[1], gt[k][1], gt[k][2], min_runs_exact(*click_probs(k[0], gt[k][1], k[1]))) for k in badb)),
          100 * min(sv_d.values()), 100 * max(sv_d.values())),
          all(gt[k][1] == mine[k][1] for k in gt) and badb == [(0.01, 0.01)] and abs(gt[(0.01, 0.01)][2] / min_runs_exact(*click_probs(0.01, gt[(0.01, 0.01)][1], 0.01)) - 1) < 0.03 and max(abs(v) for v in sv_d.values()) < 0.03)
    # G3: the minimum above is a search result; confirm it by brute force where that is affordable
    small = [k for k in sorted(gt) if k[1] > 0 and mine[k][0] <= 20000]
    ok3 = True; first = []
    for k in small:
        b0, p0 = click_probs(k[0], 1, k[1]); f = feasible_scan(1, mine[k][0], b0, p0); first.append((k, f[0] if f else None)); ok3 = ok3 and bool(f) and f[0] == mine[k][0]
    wins = []
    for k in sorted(gt):
        if k[1] == 0: continue
        b0, p0 = click_probs(k[0], 1, k[1]); m = mine[k][0]; top = max(gt[k][0], m)
        f = feasible_scan(m - 300, top, b0, p0); inside = [R for R in f if m <= R <= gt[k][0]]
        wins.append((k, m, gt[k][0], len(inside), gt[k][0] - m + 1, f[0] if f else None)); ok3 = ok3 and bool(f) and f[0] == m
    print("      brute-force first feasible N = 1 run count from R = 1: " + "; ".join("d=%g eps=%g: %s" % (k[0], k[1], v) for k, v in first))
    print("      feasible run counts between the exact minimum and V1.0's printed count (window scan from 300 below the minimum):")
    for (k, m, v, nin, ntot, f0) in wins: print("        d=%-5g eps=%-7g exact minimum %-9d V1.0 %-9d: %d of the %d run counts in [minimum, V1.0] meet the criterion%s" % (k[0], k[1], m, v, nin, ntot, "" if v == m else ("; at V1.0's count: %s" % ("met" if detect_exact(v, *click_probs(k[0], 1, k[1])) else "not met"))))
    check("G3 brute force confirms the exact minimum of the N = 1 run count: first feasible count from R = 1 equals the search result in %d rows (all those with a minimum up to 20000 and eps > 0), and in all 9 rows with eps > 0 no run count in the 300 below the minimum is feasible and the minimum is" % len(small), ok3 and len(small) == 3)
    # ---- H
    HCl = {c: pauli_classes(c) for c in ("L", "J")}
    check("H1 both codes have 3 stabilizer, 60 logical and 192 check-disturbing non-identity Pauli products; minimum weights: stabilizer %d / %d and logical %d / %d (local / joint)" % (
          HCl["L"][1]["stabilizer"], HCl["J"][1]["stabilizer"], HCl["L"][1]["logical"], HCl["J"][1]["logical"]),
          all(HCl[c][0] == {"stabilizer": 3, "logical": 60, "disturbs checks": 192} for c in HCl) and (HCl["L"][1]["stabilizer"], HCl["J"][1]["stabilizer"], HCl["L"][1]["logical"], HCl["J"][1]["logical"]) == (2, 4, 1, 2))
    # ---- I
    CM = names + ["J ZZZZ only (partial)"]
    EL = {nm: s19.Engine(nm, loss=True) for nm in CM}
    def nI(nm): return sum(1 for o in EL[nm].R.ops if o[0] in ("CNOT", "CZ"))
    def photons(nm):
        qs = set()
        for o in EL[nm].R.ops:
            qs.add(o[1])
            if o[0] in ("CNOT", "CZ"): qs.add(o[2])
        return len({q for q in qs if q >= 4})
    def attempts_abort(n, s): return (1 - s ** n) / ((1 - s) * s ** n)
    def coverage(nm):
        code = EL[nm].code; return sum(1 for q in range(4) for c in ("X", "Z", "Y") if s18.classify_err((1 << q) if c in "XY" else 0, (1 << q) if c in "ZY" else 0, code) == "detected")
    PROF = {"P0": dict(p=1e-3, q=0.0, s=1.0, mode="none"), "P1": dict(p=1e-3, q=1e-2, s=1.0, mode="none"), "P2": dict(p=1e-3, q=1e-2, s=0.5, mode="retry"), "P3": dict(p=1e-3, q=1e-2, s=0.75, mode="abort")}
    def cap_row(nm, pf):
        e = EL[nm].at({"g": pf["p"], "mz": pf["p"], "mx": pf["p"], "la_h": pf["q"]}); acc = e["silent"] + e["accept_damaged"] + e["accept_clean"]
        nda = sum(1 for o in EL[nm].R.ops if o[0] in ("CNOT", "CZ") and ((o[1] < 4) != (o[2] < 4))); n = nI(nm)
        comp = pf["s"] ** n if pf["mode"] == "abort" else 1.0
        att = attempts_abort(n, pf["s"]) if pf["mode"] == "abort" else (n / pf["s"] if pf["mode"] == "retry" else float(n))
        return dict(config=nm, silent=e["silent"], unusable=1 - acc * (1 - pf["q"]) ** nda * comp, attempts=att, photons=photons(nm), coverage=coverage(nm), completion=comp)
    KEYS = ["silent", "unusable", "attempts", "photons", "coverage"]
    def dominated(a, b):
        """b dominates a: no worse in every key (coverage: higher is better) and strictly better in one"""
        better = False
        for k in KEYS:
            x, y = a[k], b[k]
            if k == "coverage": x, y = -x, -y
            if y > x + 1e-300: return False
            if y < x: better = True
        return better
    REQ = {"A": lambda r: r["silent"] <= 1e-4 and r["unusable"] <= 0.2, "B": lambda r: r["silent"] <= 1e-3 and r["attempts"] <= 12}
    seg = LOG[LOG.index("== I. capability report"):LOG.index("provisional capability report v2 row")]
    prof_txt = re.split(r"^\s+profile (P\d) ", seg, flags=re.M); printed = {}
    for i in range(1, len(prof_txt), 2): printed[prof_txt[i]] = prof_txt[i + 1]
    nok = ntot = 0; badrows = []; selok = True
    for pn, pf in PROF.items():
        rows_ = [cap_row(nm, pf) for nm in CM]; txt = printed[pn]
        for r in rows_:
            m = re.search(r"^\s+" + re.escape(r["config"]) + r"\s+silent ([\d.e+-]+)\s+unusable ([\d.]+)\s+attempts\s+([\d.]+)\s+photons\s+(\d+)\s+completion ([\d.e+-]+)\s+coverage (\d+)", txt, re.M)
            for ok_, lab in ((fmt_ok(r["silent"], m.group(1)), "silent"), (fmt_ok(r["unusable"], m.group(2)), "unusable"), (fmt_ok(r["attempts"], m.group(3)), "attempts"), (r["photons"] == int(m.group(4)), "photons"),
                             (("%.3g" % r["completion"]) == m.group(5), "completion"), (r["coverage"] == int(m.group(6)), "coverage")):
                ntot += 1; nok += ok_
                if not ok_: badrows.append((pn, r["config"], lab))
        for rn, req in REQ.items():
            feas = [r for r in rows_ if req(r)]; par = [a for a in feas if not any(dominated(a, b) for b in feas if b is not a)]
            m = re.search(r"requirement %s: [^\n]*feasible (\[.*?\]) -> Pareto (\[.*?\])" % rn, txt)
            selok &= [r["config"] for r in feas] == ast.literal_eval(m.group(1)) and [r["config"] for r in par] == ast.literal_eval(m.group(2))
    check("I1a all %d numbers of V1.0's capability rows (4 profiles x 5 rounds x 6 fields) equal this engine's values at the printed precision (%d of %d; mismatches: %s)" % (ntot, nok, ntot, badrows[:3] or "none"), nok == ntot == 120)
    check("I1b all eight feasible-and-Pareto selections (4 profiles x 2 requirements) equal V1.0's printed lists", selok)
    print("NOTE  Section F's table-driven recursion is re-written but has the same structure as V1.0's (the transition tables come from S19's engine and the syndromes from state vectors).  Section G's printed run counts for means above 60 use a normal approximation in V1.0; the exact comparison above says how far that matters.  Total wall-clock %.0f s" % (time.time() - t00))
    print("ALL PASS" if OK else "FAILED")
    return 0 if OK else 1

if __name__ == "__main__": sys.exit(main())
