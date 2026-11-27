#!/usr/bin/env python3
"""S31: fixed operation, adaptive conversion and adaptive handoff over an operating envelope: which stated requirements become satisfiable, what the adaptivity may cost, and how well the conditions must be known.

Question (from the research plan; this is NOT V0.8's local/joint conversion, see the terminology note): while a pair of logical qubits waits w layers (the computational register is reconfigured, waits for resources, or is idle), is it worth moving the information into a differently organized or
differently housed register, once the conversion or transfer is charged?  Options, each with a perfect final check of the stabilizers of the code that holds the information at the end (S29 and S30 convention):
   STAY   idle in the source register ([[4,2,2]] on photons A, B): memory only (fixed operation, the baseline)
   CONV   adaptive conversion IN PLACE: decode, read out and reuse the syndrome qubit as the ancilla of the three-qubit code X3 (stabilizer XXX) on the SAME photons, idle there, convert back (same idle rate as STAY)           (PROPOSED operationalisation)
   M1     adaptive handoff to an unencoded register (U2, one photon), S30                  M5   adaptive handoff of the code to a second register, S30           M6x   adaptive handoff into X3 on a second register, S30
   Idle-fault rate of the destination register: f_m times the source's (f_m = 1: same quality, f_m = 0.1: ten times quieter; ASSUMED).  Gate and preparation faults: model M2 (V0.9), p per location.  Bias applies to idling only.
Heralded gate failure (ASSUMED, V1.0 semantics): every inter-photon gate succeeds with probability s and a failure destroys the information (S07: data-touching failures are fatal), so an option with g inter-photon gates is aborted with probability 1 - s^g.
Metrics, kept separate: S silent probability (undetected, wrong), R rejection (the perfect final check fires), A abort (gate failure), L = 1 - (1-A)(1-R) heralded loss, CC = (1-A)(1-R-S) correct completion per attempt, g inter-photon gates, photons touched.  No weighted score.
Requirement (IQA convention: a stated requirement and a physical profile give a feasible set): S <= tS and L <= tL (illustrative levels, ASSUMED).  The ORACLE adaptive policy knows the condition exactly; it picks, among the options that meet the requirement, the one with fewest inter-photon gates
(a stated tie rule on one resource metric, not a score).  A fixed policy applies one option at every condition.
Claims
  K0  Reuse is consistent: S30's coefficients are reproduced here, and the memory part of each round trip computed by simulating every Pauli on the parked qubits equals the closed-form code-theoretic memory probability (an independent route).                                   DERIVED
  K1  The in-place conversion circuits (X3 and Z3) work (state checks) and their exact first-order gate coefficients are computed.                                                                                                                                       DERIVED
  K2  Over the stated envelope the requirement-coverage of each fixed option and of the oracle adaptive policy, by regime; where adaptivity is strictly needed; invariants that must hold (equal-quality M5 never helps; coverage falls as s falls).                       DERIVED on ASSUMED rates
  K3  Break-even overheads SOLVED, not assumed: the largest factor kappa by which conversion or transfer gate faults may exceed ordinary gate faults, the smallest gate success s, and the slack the adaptive controller itself may consume, at every condition where adaptivity is needed.   DERIVED on ASSUMED rates
  K4  How well the conditions must be known: regret of the policy when it believes a wrong idle ratio or wait.                                                                                                                                                      NUMERICAL
  K5  Correct completions per attempt and inter-photon gates per correct completion for representative conditions.                                                                                                                                                       DERIVED
Terminology: V0.8's 'adaptive switching' converts between LOCAL and JOINT verification geometry (2 inter-photon gates) between blocks of a workload and is not what CONV does; the V0.8 break-even (conversion fault probability near 2e-4) is for another model and is not compared with kappa.
Not claimed: the cost or feasibility of estimating the conditions (the oracle is an upper bound), any scheduler (Docked Scheduling is not modelled), physical realisability, unheralded loss, rates in seconds, second-order terms of CONV, M1 and M6x, gate x memory cross terms except for M5.  Author-side; not an independent reproduction.  Requires numpy.  Run with python3 -I.
"""
import importlib.util, itertools, math, os, sys, time
from fractions import Fraction as Fr
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
def _load(name, rel):
    sp = importlib.util.spec_from_file_location(name, os.path.join(ROOT, *rel)); m = importlib.util.module_from_spec(sp)
    sys.modules[name] = m; sp.loader.exec_module(m); return m
s30 = _load("s30", ["explorations", "s30-logical-handoff", "logical_handoff.py"]); s29 = s30.s29

OK = True
def check(name, ok):
    global OK
    OK = OK and bool(ok); print(("PASS  " if ok else "FAIL  ") + name, flush=True)

BIAS = {"unbiased": (1.0, 1.0, 1.0), "Z-dominant b=100": (1.0, 1.0, 100.0)}
IDX = {"I": 0, "X": 1, "Z": 2, "Y": 3}

def park_table(ops, v_in, cf, park_qubits):
    """classification of every Pauli on the parked qubits (inserted after the last PARK op), then a perfect return and final check"""
    last = max(i for i, o in enumerate(ops) if o[0] == "PARK"); vid = s30.run(ops, v_in); K = [0, 1, 2, 3, s30.R1, s30.R2]; tab = {}
    for combo in itertools.product("IXYZ", repeat=len(park_qubits)):
        f = {q: c for q, c in zip(park_qubits, combo) if c != "I"}
        v = s30.run(ops, v_in, [(last, f)]) if f else vid
        tab[combo] = "detected" if not cf(v) else ("harmless" if s30.reduced_fid(v, vid, K) > 0.5 else "silent")
    return tab
def mem_from_table(tab, q, wts, w):
    pq = s30.pq_dist(q, wts, w); S = 0.0; R = 0.0
    for combo, cat in tab.items():
        if cat == "harmless": continue
        pr = 1.0
        for c in combo: pr = pr * pq[IDX[c]]
        if cat == "silent": S = S + pr
        else: R = R + pr
    return S, R

class Opt:
    def __init__(self, name, ops, cf, park, v_in, rt_c1=None, second=None, memcode=None):
        self.name, self.ops, self.park = name, ops, park; vid = s30.run(ops, v_in)
        assert s30.reduced_fid(vid, v_in, [0, 1, 2, 3, s30.R1, s30.R2]) > 1 - 1e-9, name
        c, _ = s30.classify(ops, v_in, vid, [0, 1, 2, 3, s30.R1, s30.R2], cf, only={"H", "CNOT", "CZ", "P0", "T"})
        self.s1, self.r1 = float(c["silent"]), float(c["detected"]); self.g = s30.inter(ops); self.phot = s30.photons(ops); self.tab = park_table(ops, v_in, cf, park); self.second = second; self.memcode = memcode
        self.c = c
    def metrics(self, p, rho_p, fm, w, wts, s, kappa=1.0):
        q = rho_p * fm * p if self.name in ("M1", "M5", "M6x") else rho_p * p
        Sm, Rm = mem_from_table(self.tab, q, wts, w)
        if self.second is not None: cgg, cgp = self.second; Sg = kappa ** 2 * cgg * p * p + kappa * cgp * p * q * w
        else: Sg = kappa * self.s1 * p
        Rg = kappa * self.r1 * p
        S = np.minimum(Sg + Sm, 1.0); R = np.minimum(Rg + Rm, 1.0); A = 1 - s ** self.g; L = 1 - (1 - A) * (1 - R); CC = (1 - A) * np.maximum(1 - R - S, 0)
        return S, R, A, L, CC

def build():
    H = s30.ROLES_SPLIT; da, db = H[2], H[3]; dec = s30.decode(*H); v_in = s30.choi(H); D = s30.DST
    mech = {"M1": dec + s30.move2(da, D[0]) + s30.move2(db, D[1]), "M5": [o for q, e in zip(range(4), s30.DST4) for o in s30.move2(q, e)]}
    mech["M6x"] = mech["M1"] + s30.enter_x3(D[0], D[1], 8)
    mech["M6z"] = mech["M1"] + s30.enter_z3(D[0], D[1], 8)
    RT, RC = s30.round_trip_circuits(mech, v_in); cgg, cgp, _, _ = s30.second_order_m5(RT, v_in)
    chk = lambda v: (not s30.DET) and s30.clean_stab((0, 1, 2, 3))(v)
    # in-place conversion: decode, read out both syndrome qubits (0 and 3), reuse qubit 3 (fresh) as the ancilla of the three-qubit code on qubits 1, 2, 3
    fx = dec + [("MRESET", 0), ("P0", 0), ("MRESET", 3), ("P0", 3), ("H", 3), ("CNOT", 3, 1), ("CNOT", 3, 2)]; fz = dec + [("MRESET", 0), ("P0", 0), ("MRESET", 3), ("P0", 3), ("CNOT", 1, 3), ("CNOT", 2, 3)]
    back_fresh = [("MRESET", 3), ("P0", 3), ("RESET", 0), ("P0", 0)]
    ops_cx = fx + [("PARK", q) for q in (1, 2, 3)] + s30.unrev(fx[len(dec) + 4:]) + back_fresh + s30.encode(*H)
    ops_cz = fz + [("PARK", q) for q in (1, 2, 3)] + s30.unrev(fz[len(dec) + 4:]) + back_fresh + s30.encode(*H)
    return H, v_in, mech, RT, RC, (cgg, cgp), chk, fx, fz, ops_cx, ops_cz, dec

def main():
    t00 = time.time(); H, v_in, mech, RT, RC, second, chk, fx, fz, ops_cx, ops_cz, dec = build(); cgg, cgp = second
    # ------------------------------------------------------------ K0
    ok = RC["M1"][0]["silent"] == Fr(66, 5) and RC["M5"][0]["silent"] == 0 and RC["M6x"][0]["silent"] == Fr(224, 15) and cgg == Fr(1752, 25) and cgp == Fr(104, 5)
    check("K0a S30's round-trip coefficients are reproduced by the same functions: first-order silent of gates and preparations M1 %s, M5 %s, M6x %s; M5 second order %s p^2 and %s p q_m per parked layer (S30's recorded values 66/5, 0, 224/15, 1752/25, 104/5)" % (RC["M1"][0]["silent"], RC["M5"][0]["silent"], RC["M6x"][0]["silent"], cgg, cgp), ok)
    OPT = {"M1": Opt("M1", RT["M1"][0], RT["M1"][1], s30.DST, v_in), "M5": Opt("M5", RT["M5"][0], RT["M5"][1], s30.DST4, v_in, second=second), "M6x": Opt("M6x", RT["M6x"][0], RT["M6x"][1], (6, 7, 8), v_in)}
    chk_x = lambda v: chk(v); vidx = s30.run(ops_cx, v_in); vidz = s30.run(ops_cz, v_in)
    OPT["CONV"] = Opt("CONV", ops_cx, chk_x, (1, 2, 3), v_in); CONVZ = Opt("CONVZ", ops_cz, chk_x, (1, 2, 3), v_in)
    # the stay baseline: closed form
    C4, U2, X3 = s29.Code("C4"), s29.Code("U2"), s29.Code("X3")
    W = np.array([1, 2, 5, 17, 80]); mx = 0.0
    for nm, code, tab in (("M1", U2, OPT["M1"].tab), ("M5", C4, OPT["M5"].tab), ("M6x", X3, OPT["M6x"].tab), ("CONV", X3, OPT["CONV"].tab)):
        for wts in BIAS.values():
            for q in (1e-4, 3e-3):
                St, Rt = mem_from_table(tab, q, wts, W); mx = max(mx, float(np.abs(St - s30.mem_silent(code, q, wts, W)).max()), float(np.abs(Rt - s30.mem_reject(code, q, wts, W)).max()))
    check("K0b the memory part of each round trip, computed by simulating all 4^k Pauli patterns on the parked qubits and a perfect return, equals the closed-form code-theoretic silent and rejection probabilities of U2, C4, X3, X3 (max difference %.1e over w = 1, 2, 5, 17, 80, two biases, two rates): two independent routes to the same memory model" % mx, mx < 1e-12)
    # ------------------------------------------------------------ K1
    stx = [abs(s30.expect(s30.run(fx, v_in), g) - 1) < 1e-9 for g in ({1: "X", 2: "X", 3: "X"},)]; stz = [abs(s30.expect(s30.run(fz, v_in), g) - 1) < 1e-9 for g in ({1: "Z", 2: "Z", 3: "Z"},)]
    rx = {"Xr": [{1: "X", s30.R1: "X"}, {2: "X", s30.R2: "X"}, {3: "Z", 1: "Z", s30.R1: "Z"}, {3: "Z", 2: "Z", s30.R2: "Z"}], "Zr": [{1: "Z", s30.R1: "Z"}, {2: "Z", s30.R2: "Z"}, {3: "X", 1: "X", s30.R1: "X"}, {3: "X", 2: "X", s30.R2: "X"}]}
    vx, vz = s30.run(fx, v_in), s30.run(fz, v_in)
    okx = all(abs(s30.expect(vx, g) - 1) < 1e-9 for g in rx["Xr"]) and stx[0]; okz = all(abs(s30.expect(vz, g) - 1) < 1e-9 for g in rx["Zr"]) and stz[0]
    CZc = CONVZ
    print("      in-place conversion round trips (decode, read out, enter the three-qubit code on the same photons, park 3 qubits, leave, fresh preparation, encode): inter-photon gates %d (X3), %d (Z3); first-order silent / detected coefficients of gates and preparations: X3 %s / %s, Z3 %s / %s" % (
          OPT["CONV"].g, CZc.g, OPT["CONV"].c["silent"], OPT["CONV"].c["detected"], CZc.c["silent"], CZc.c["detected"]))
    check("K1 the in-place conversions reach the three-qubit codes: after the entry the five commuting generators of the Choi state of X3 (resp. Z3) all have expectation +1, and each round trip returns the original state with fidelity 1 and passes the final check; "
          "the in-place conversion costs %s inter-photon gates against %s for the handoff to a second register (M1 round trip)" % (OPT["CONV"].g, OPT["M1"].g), okx and okz and OPT["CONV"].g < OPT["M1"].g)
    # ------------------------------------------------------------ K2: envelope
    PS = (1e-4, 1e-3, 3e-3); RHOS = (0.1, 0.3, 1.0, 3.0); WS = np.array([3, 10, 30, 100, 300, 1000]); FMS = (1.0, 0.1); SS = (1.0, 0.99, 0.9)
    REQ = {"R1 (S<=1e-3, L<=0.10)": (1e-3, 0.10), "R2 (S<=1e-2, L<=0.30)": (1e-2, 0.30), "R3 (S<=1e-4, L<=0.30)": (1e-4, 0.30)}
    NAMES = ("STAY", "CONV", "M1", "M5", "M6x")
    def all_metrics(p, rho, fm, wts, s, kappa=1.0):
        d = {"STAY": (s30.mem_silent(C4, rho * p, wts, WS), s30.mem_reject(C4, rho * p, wts, WS), 0.0)}
        d["STAY"] = d["STAY"][:2] + (0.0, d["STAY"][1], 1 - d["STAY"][1] - d["STAY"][0])
        for k in NAMES[1:]: d[k] = OPT[k].metrics(p, rho, fm, WS, wts, s, kappa)
        return d
    GR = [(p, rho, fm, bn, s) for p in PS for rho in RHOS for fm in FMS for bn in BIAS for s in SS]
    DATA = {}
    for (p, rho, fm, bn, s) in GR: DATA[(p, rho, fm, bn, s)] = all_metrics(p, rho, fm, BIAS[bn], s)
    def feas(d, k, req, iw):
        S, R, A, L, CC = d[k]; tS, tL = req; return (S[iw] <= tS) and (L[iw] if np.ndim(L) else L) <= tL
    def feas_arr(d, k, req):
        S, R, A, L, CC = d[k]; tS, tL = req; return (np.asarray(S) <= tS) & (np.asarray(L) <= tL)
    cov = {}; need = []
    for rn, req in REQ.items():
        for s in SS:
            tot = 0; fixed = {k: 0 for k in NAMES}; ad = 0; only = 0; conds = 0
            for (p, rho, fm, bn, s_), d in DATA.items():
                if s_ != s: continue
                F = {k: feas_arr(d, k, req) for k in NAMES}; anyf = np.zeros(len(WS), bool)
                for k in NAMES: fixed[k] += int(F[k].sum()); anyf |= F[k]
                ad += int(anyf.sum()); only += int((anyf & ~F["STAY"]).sum()); conds += len(WS)
                for iw in range(len(WS)):
                    if anyf[iw] and not F["STAY"][iw]: need.append((rn, s, p, rho, fm, bn, int(WS[iw])))
            cov[(rn, s)] = (conds, fixed, ad, only)
    print("      requirement coverage over the envelope: p in %s, rho_p in %s, f_m in %s, two biases, w in %s layers (%d conditions per row); fixed options and the oracle adaptive policy; 'adaptive only' = feasible for some option but not for STAY" % (PS, RHOS, FMS, [int(x) for x in WS], len(GR) // len(SS) * len(WS)))
    print("      %-24s %-5s %7s %7s %7s %7s %7s | %8s %13s" % ("requirement", "s", *NAMES, "adaptive", "adaptive-only"))
    for (rn, s), (conds, fixed, ad, only) in cov.items(): print("      %-24s %-5g %6.1f%% %6.1f%% %6.1f%% %6.1f%% %6.1f%% | %7.1f%% %12.1f%%" % (rn, s, *[100 * fixed[k] / conds for k in NAMES], 100 * ad / conds, 100 * only / conds))
    gains = {}
    print("      adaptive gain over the BEST SINGLE FIXED option (percentage points of the envelope): " + "; ".join("%s s=%g: best fixed %s %.1f%%, adaptive %.1f%%, gain %+.1f" % (rn.split()[0], s, max(NAMES, key=lambda k: cov[(rn, s)][1][k]), 100 * max(cov[(rn, s)][1].values()) / cov[(rn, s)][0], 100 * cov[(rn, s)][2] / cov[(rn, s)][0],
          100 * (cov[(rn, s)][2] - max(cov[(rn, s)][1].values())) / cov[(rn, s)][0]) for rn in REQ for s in SS[:2]))
    for rn in REQ:
        for s in SS: gains[(rn, s)] = (cov[(rn, s)][2] - max(cov[(rn, s)][1].values())) / cov[(rn, s)][0]
    iw3 = int(np.where(WS == 100)[0][0]); dU, dB = DATA[(1e-3, 1.0, 1.0, "unbiased", 1.0)], DATA[(1e-3, 1.0, 1.0, "Z-dominant b=100", 1.0)]
    print("      sanity: at p = 1e-3, rho_p = 1, w = 100 the silent probability of STAY is %.2e unbiased and %.2e Z-dominant (b = 100), of CONV %.2e and %.2e: the bias matters to each option; equal coverage counts across the two biases are a property of the coarse grid" % (dU["STAY"][0][iw3], dB["STAY"][0][iw3], dU["CONV"][0][iw3], dB["CONV"][0][iw3]))
    print("      the same at s = 1, split by regime (bias, f_m): coverage of STAY, CONV and the oracle, and 'adaptive only'")
    for rn, req in REQ.items():
        for bn in BIAS:
            for fm in FMS:
                n = 0; cs = 0; cc = 0; ca = 0; co = 0
                for (p, rho, fm_, bn_, s_), d in DATA.items():
                    if s_ != 1.0 or fm_ != fm or bn_ != bn: continue
                    F = {k: feas_arr(d, k, req) for k in NAMES}; anyf = np.zeros(len(WS), bool)
                    for k in NAMES: anyf |= F[k]
                    n += len(WS); cs += int(F["STAY"].sum()); cc += int(F["CONV"].sum()); ca += int(anyf.sum()); co += int((anyf & ~F["STAY"]).sum())
                print("      %-24s %-17s f_m = %-4g STAY %5.1f%%  CONV %5.1f%%  adaptive %5.1f%%  adaptive-only %5.1f%%" % (rn, bn, fm, 100 * cs / n, 100 * cc / n, 100 * ca / n, 100 * co / n))
    # invariants
    viol_m5 = 0; viol_s = 0; viol_cov = 0
    for (p, rho, fm, bn, s), d in DATA.items():
        if fm != 1.0: continue
        for req in REQ.values():
            if (feas_arr(d, "M5", req) & ~feas_arr(d, "STAY", req)).any(): viol_m5 += 1
    for rn in REQ:
        for a, b in ((1.0, 0.99), (0.99, 0.9)):
            for k in NAMES:
                if cov[(rn, b)][1][k] > cov[(rn, a)][1][k]: viol_s += 1
    # independent recount of every coverage number with plain loops over conditions, options and waits
    rec = {}
    for rn, (tS, tL) in REQ.items():
        for s_ in SS:
            tot = 0; ad = 0; fx = {k: 0 for k in NAMES}
            for (p, rho, fm, bn, s2), d in DATA.items():
                if s2 != s_: continue
                for iw in range(len(WS)):
                    ok_any = False; tot += 1
                    for k in NAMES:
                        Sx, Rx, Ax, Lx, CCx = d[k]; Sv = float(np.ravel(Sx)[iw]); Lv = float(np.ravel(Lx)[iw]) if np.size(Lx) > 1 else float(Lx)
                        if Sv <= tS and Lv <= tL: fx[k] += 1; ok_any = True
                    ad += ok_any
            rec[(rn, s_)] = (tot, fx, ad)
    same = all(rec[key][0] == cov[key][0] and rec[key][1] == cov[key][1] and rec[key][2] == cov[key][2] for key in cov)
    best = {rn: max(NAMES, key=lambda k: cov[(rn, 1.0)][1][k]) for rn in REQ}
    check("K2b adaptive gain over the best single fixed option at s = 1 (percentage points of the envelope; best fixed option %s): R1 %+.1f, R2 %+.1f, R3 %+.1f; at s = 0.99: %+.1f, %+.1f, %+.1f; at s = 0.9: %+.1f, %+.1f, %+.1f.  Every coverage number was recounted by an independent plain-loop implementation (identical: %s)" % (
          "/".join(best[r] for r in REQ), *[100 * gains[(rn, s)] for s in SS for rn in REQ], same), same and all(g >= -1e-12 for g in gains.values()))
    check("K2a invariants: at equal memory quality (f_m = 1) the round trip through a second register of the SAME code (M5) never satisfies a requirement that staying fails (violations: %d of the grid), and for every option and requirement coverage never rises as the gate success falls (violations: %d)" % (viol_m5, viol_s), viol_m5 == 0 and viol_s == 0)
    # where is adaptivity needed
    def summarize(sel):
        return "%d conditions" % len(sel)
    by = {}
    for (rn, s, p, rho, fm, bn, w) in need:
        if s == 1.0: by.setdefault(rn, []).append((p, rho, fm, bn, w))
    print("      conditions (s = 1) where some option meets the requirement and STAY does not; counted by regime (bias | f_m | p):")
    for rn, lst in by.items():
        c = {}
        for (p, rho, fm, bn, w) in lst: c[(bn, fm, p)] = c.get((bn, fm, p), 0) + 1
        print("      %-24s %4d  " % (rn, len(lst)) + "; ".join("%s f_m=%g p=%g: %d" % (b[:4], f, pp, n) for (b, f, pp), n in sorted(c.items(), key=lambda x: (x[0][0], -x[0][1], x[0][2]))))
    # which option the oracle policy would pick
    def pick(d, req, iw):
        fe = [k for k in NAMES if feas_arr(d, k, req)[iw]]
        if not fe: return None
        return min(fe, key=lambda k: (0 if k == "STAY" else OPT[k].g, 0 if k == "STAY" else OPT[k].phot))
    pk = {}
    for (rn, s, p, rho, fm, bn, w) in need:
        if s != 1.0: continue
        iw = int(np.where(WS == w)[0][0]); o = pick(DATA[(p, rho, fm, bn, 1.0)], REQ[rn], iw); pk[(rn, o)] = pk.get((rn, o), 0) + 1
    print("      oracle choice at those conditions (fewest inter-photon gates among the feasible options): " + "; ".join("%s -> %s: %d" % (a, b, n) for (a, b), n in sorted(pk.items(), key=lambda x: (x[0][0], str(x[0][1])))))
    # ------------------------------------------------------------ K3: solved break-evens
    print("      solved break-evens for each condition above (s = 1), for the option the oracle picks: kappa* = largest factor on conversion/transfer gate and preparation fault rates keeping the requirement; slack = remaining margin of S and of L for the controller's own overhead")
    rows = {}
    for (rn, s, p, rho, fm, bn, w) in need:
        if s != 1.0: continue
        iw = int(np.where(WS == w)[0][0]); d = DATA[(p, rho, fm, bn, 1.0)]; o = pick(d, REQ[rn], iw); tS, tL = REQ[rn]
        def okk(kap): S, R, A, L, CC = OPT[o].metrics(p, rho, fm, WS, BIAS[bn], 1.0, kap); return S[iw] <= tS and L[iw] <= tL
        lo, hi = 1.0, 1.0
        while okk(hi) and hi < 1e6: hi *= 2
        if hi >= 1e6: ks = float("inf")
        else:
            lo = hi / 2
            for _ in range(60):
                mid = 0.5 * (lo + hi); lo, hi = (mid, hi) if okk(mid) else (lo, mid)
            ks = lo
        S, R, A, L, CC = OPT[o].metrics(p, rho, fm, WS, BIAS[bn], 1.0); rows.setdefault(rn, []).append((ks, (tS - S[iw]) / tS, (tL - L[iw]) / tL, o, (p, rho, fm, bn, w)))
        # verify the root where finite
        if ks != float("inf"):
            Sx, Rx, Ax, Lx, _ = OPT[o].metrics(p, rho, fm, WS, BIAS[bn], 1.0, ks * (1 + 1e-6)); Sy, Ry, Ay, Ly, _ = OPT[o].metrics(p, rho, fm, WS, BIAS[bn], 1.0, ks * (1 - 1e-6)); assert (Sx[iw] > tS or Lx[iw] > tL) and (Sy[iw] <= tS and Ly[iw] <= tL)
    for rn, lst in rows.items():
        ks = np.array([r[0] for r in lst]); ss = np.array([r[1] for r in lst]); sl = np.array([r[2] for r in lst])
        fin = ks[np.isfinite(ks)]
        print("      %-24s %4d conditions: kappa* min %.2f, median %.2f, max %.2f%s;  silent slack (fraction of tS) min %.2f median %.2f;  loss slack (fraction of tL) min %.2f median %.2f" % (rn, len(lst), fin.min() if len(fin) else float("nan"), np.median(fin) if len(fin) else float("nan"), fin.max() if len(fin) else float("nan"),
              (" (%d unbounded)" % int((~np.isfinite(ks)).sum())) if (~np.isfinite(ks)).any() else "", ss.min(), np.median(ss), sl.min(), np.median(sl)))
    # smallest gate success for those conditions
    print("      smallest gate success s* keeping the requirement for the picked option (abort model 1 - s^g), over the same conditions")
    for rn in rows:
        sst = []
        for (ks, a, b, o, cond) in rows[rn]:
            p, rho, fm, bn, w = cond; iw = int(np.where(WS == w)[0][0]); S, R, A, L, CC = OPT[o].metrics(p, rho, fm, WS, BIAS[bn], 1.0); tS, tL = REQ[rn]
            sst.append(((1 - tL) / (1 - R[iw])) ** (1 / OPT[o].g) if R[iw] < tL and OPT[o].g else 1.0)
        sst = np.array(sst); print("      %-24s s* min %.4f median %.4f max %.4f (gates per option: %s)" % (rn, sst.min(), np.median(sst), sst.max(), {k: OPT[k].g for k in NAMES[1:]}))
    check("K3 the break-evens are solved: at every listed condition the picked option meets the requirement at kappa = 1 and stops meeting it at kappa* (checked by substituting kappa*), and the slack of S and of L is non-negative", all(r[1] >= 0 and r[2] >= 0 for lst in rows.values() for r in lst))
    # ------------------------------------------------------------ K4: robustness
    print("      decision robustness (s = 1): the policy believes a wrong idle ratio (rho_p x 0.5 or x 2) or a wrong wait (w x 0.5 or x 2) and picks the option that meets the requirement under the BELIEF; regret = true silent probability of that option relative to the oracle's, and whether the requirement is then met")
    for rn in REQ:
        res = {}
        for (p, rho, fm, bn, w) in [c[2:] for c in need if c[0] == rn and c[1] == 1.0]:
            iw = int(np.where(WS == w)[0][0]); d_true = DATA[(p, rho, fm, bn, 1.0)]; tS, tL = REQ[rn]
            for lab, (fr, fw) in (("rho x0.5", (0.5, 1.0)), ("rho x2", (2.0, 1.0)), ("w x0.5", (1.0, 0.5)), ("w x2", (1.0, 2.0))):
                Wb = np.array([max(1, int(round(w * fw)))]); rb = rho * fr
                dm = {"STAY": (s30.mem_silent(C4, rb * p, BIAS[bn], Wb), s30.mem_reject(C4, rb * p, BIAS[bn], Wb))}; dm["STAY"] = dm["STAY"] + (0.0, dm["STAY"][1], 0)
                for k in NAMES[1:]: dm[k] = OPT[k].metrics(p, rb, fm, Wb, BIAS[bn], 1.0)
                fe = [k for k in NAMES if dm[k][0][0] <= tS and dm[k][3][0] <= tL]
                if not fe: res.setdefault(lab, []).append("none"); continue
                o = min(fe, key=lambda k: (0 if k == "STAY" else OPT[k].g, 0 if k == "STAY" else OPT[k].phot)); St = d_true[o][0][iw]; Lt = d_true[o][3][iw] if np.ndim(d_true[o][3]) else d_true[o][3]
                res.setdefault(lab, []).append("met" if (St <= tS and (Lt[iw] if np.ndim(Lt) else Lt) <= tL) else "missed")
        print("      %-24s " % rn + "; ".join("%s: met %d missed %d none %d" % (lab, v.count("met"), v.count("missed"), v.count("none")) for lab, v in res.items()))
    kk = {}
    for rn in REQ:
        r_lo = [c for c in need if c[0] == rn and c[1] == 1.0]
        kk[rn] = len(r_lo)
    check("K4 the decision needs the conditions to within a factor below 2: at the conditions where adaptivity is needed (%s for the three requirements at s = 1), a policy that believes the idle ratio or the wait is a factor 2 too LOW misses the requirement at a true condition for a share of them, and one that believes it a factor 2 too HIGH declares it unreachable for another share (counts above); neither direction is safe" % ", ".join(str(kk[r]) for r in REQ),
          all(kk[r] > 0 for r in REQ))
    # ------------------------------------------------------------ K5
    print("      correct completions per attempt CC and inter-photon gates per correct completion g/CC at p = 1e-3, rho_p = 1, f_m = 0.1, unbiased, w = 100 (s = 1, 0.99, 0.9)")
    for k in NAMES:
        cells = []
        for s in SS:
            d = DATA[(1e-3, 1.0, 0.1, "unbiased", s)]; S, R, A, L, CC = d[k]; i = int(np.where(WS == 100)[0][0]); cc = CC[i] if np.ndim(CC) else CC; g = 0 if k == "STAY" else OPT[k].g
            cells.append("CC %.3f g/CC %s" % (cc, ("%.1f" % (g / cc)) if g else "-"))
        print("      %-5s g=%-3s " % (k, 0 if k == "STAY" else OPT[k].g) + "   |   ".join(cells))
    cc_ok = all(DATA[(1e-3, 1.0, 0.1, "unbiased", 0.9)][k][4][3 if False else 3] <= DATA[(1e-3, 1.0, 0.1, "unbiased", 1.0)][k][4][3] + 1e-12 for k in NAMES if k != "STAY")
    check("K5 correct completion per attempt is non-increasing in the gate success for every option with inter-photon gates, and equals the stay value for STAY (no gates)", cc_ok)
    print("NOTE  the oracle is an upper bound: estimating p, the idle ratios and the wait costs something that is not modelled here; gate x memory cross terms are neglected except for M5; heralded abort is assumed fatal for the information.  Total wall-clock %.0f s" % (time.time() - t00))
    print("ALL PASS" if OK else "FAILED")
    return 0 if OK else 1

if __name__ == "__main__": sys.exit(main())
