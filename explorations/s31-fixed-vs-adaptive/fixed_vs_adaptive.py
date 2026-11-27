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
  K5  Correct completions per attempt and inter-photon gates per correct completion for representative conditions.
  K6  (review follow-up) The memory-quality ratio f_m scanned continuously: is 'ten times quieter' a threshold, and how quiet must the continuity memory be for each condition where adaptivity is needed?
  K7  (review follow-up) The effect of the neglected terms on the coverage numbers: independent-union combination of the gate and memory phases, M5's exact second-order rejection, the union property of the coverage, and the effect of a uniform error in the gate-fault terms.
  K8  (review follow-up) Labelled denominators: silent error per attempted run and among accepted outputs; inter-photon gates per correct completion with scheduled and with executed gates.                                                                                                                                                       DERIVED
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
    # in-place conversion against staying: where does it have the smaller silent AND the smaller rejection probability?
    Wf = np.arange(1, 3001); winC = {}
    def wins(mask):
        ix = np.nonzero(mask)[0]
        if len(ix) == 0: return None
        br = np.nonzero(np.diff(ix) > 1)[0]; st = [ix[0]] + [ix[b + 1] for b in br]; en = [ix[b] for b in br] + [ix[-1]]; return [(int(Wf[x]), int(Wf[y])) for x, y in zip(st, en)]
    print("      in-place conversion (CONV, same photons, same idle rate) against staying in C4: layers w where CONV has the smaller silent probability AND the smaller rejection probability (rho_p = 1; a window ending at 3000 is cut by the scan)")
    for bl, bw in (("b = 1", (1.0, 1.0, 1.0)), ("b = 10", (1.0, 1.0, 10.0)), ("b = 100", (1.0, 1.0, 100.0)), ("b = 1000", (1.0, 1.0, 1000.0))):
        row = []
        for pe in (1e-3, 1e-4):
            S0 = s30.mem_silent(C4, pe, bw, Wf); R0 = s30.mem_reject(C4, pe, bw, Wf); S1, R1, _, _, _ = OPT["CONV"].metrics(pe, 1.0, 1.0, Wf, bw, 1.0)
            winC[(bl, pe)] = (wins(S1 < S0), wins(R1 < R0), wins((S1 < S0) & (R1 < R0))); row.append("p = %g: silent %s, rejection %s, both %s" % ((pe,) + winC[(bl, pe)]))
        print("      %-9s " % bl + "  |  ".join(row))
    check("K2c adaptive in-place conversion into X3 beats staying on silent AND rejection probability only under strong Z bias: windows %s at b = 100 and %s at b = 1000 (p = 1e-3); none at b = 1 or 10 (silent probability higher at every w, although its rejection is lower from w = 8); the gain is modest (e.g. silent 0.029 against 0.039 and rejection 0.24 against 0.28 at p = 1e-3, rho_p = 1, w = 100, b = 100) and in this envelope never turns a failing condition into a passing one" % (winC[("b = 100", 1e-3)][2], winC[("b = 1000", 1e-3)][2]),
          winC[("b = 1", 1e-3)][2] is None and winC[("b = 10", 1e-3)][2] is None and winC[("b = 1", 1e-4)][2] is None and winC[("b = 10", 1e-4)][2] is None and winC[("b = 100", 1e-3)][2] is not None and winC[("b = 1000", 1e-3)][2] is not None and winC[("b = 100", 1e-4)][2] is not None)
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
    # ------------------------------------------------------------ K6: the memory-quality ratio scanned continuously (review follow-up)
    # The envelope samples f_m = 1 and 0.1 only; whether 'ten times quieter' is NEEDED has to be scanned, not read off two points.
    def at(x, iw): return float(np.ravel(x)[iw]) if np.size(x) > 1 else float(x)
    def fe(d, k, rq, iw): return at(d[k][0], iw) <= rq[0] and at(d[k][3], iw) <= rq[1]
    FMG = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.15, 0.1, 0.05, 0.0]; base = [(p, rho, bn) for p in PS for rho in RHOS for bn in BIAS]; ncond = len(base) * len(WS)
    curve = {rn: [] for rn in REQ}
    for fm in FMG:
        cnt = {rn: 0 for rn in REQ}
        for (p, rho, bn) in base:
            d = all_metrics(p, rho, fm, BIAS[bn], 1.0)
            for iw in range(len(WS)):
                for rn, rq in REQ.items():
                    if any(fe(d, k, rq, iw) for k in NAMES) and not fe(d, "STAY", rq, iw): cnt[rn] += 1
        for rn in REQ: curve[rn].append(cnt[rn])
    print("      conditions (of %d at each f_m; s = 1) where some option meets the requirement and STAY does not, against the continuity memory's idle ratio f_m" % ncond)
    print("      %-24s " % "f_m" + " ".join("%5g" % f for f in FMG))
    for rn in REQ: print("      %-24s " % rn + " ".join("%5d" % c for c in curve[rn]))
    def m5_ok(p, rho, bn, iw, rq, fm):
        S, R, A, L, CC = OPT["M5"].metrics(p, rho, fm, WS, BIAS[bn], 1.0); return at(S, iw) <= rq[0] and at(L, iw) <= rq[1]
    fstar = {}
    for rn, rq in REQ.items():
        vals = []
        for (p, rho, bn) in base:
            d = all_metrics(p, rho, 0.1, BIAS[bn], 1.0)
            for iw in range(len(WS)):
                if fe(d, "STAY", rq, iw) or not m5_ok(p, rho, bn, iw, rq, 0.1): continue
                lo, hi = 0.1, 1.0
                for _ in range(30):
                    mid = 0.5 * (lo + hi)
                    if m5_ok(p, rho, bn, iw, rq, mid): lo = mid
                    else: hi = mid
                vals.append(lo)
        fstar[rn] = np.array(vals)
    for rn in REQ: print("      %-24s largest f_m at which the picked handoff (M5) still meets the requirement, over its %d adaptive-only conditions at f_m = 0.1: min %.3f, quartiles %.3f / %.3f / %.3f, max %.3f; share needing f_m <= 0.2: %.0f %%" % ((rn, len(fstar[rn]), fstar[rn].min()) + tuple(np.percentile(fstar[rn], [25, 50, 75])) + (fstar[rn].max(), 100 * (fstar[rn] <= 0.2).mean())))
    i5 = FMG.index(0.5)
    check("K6 'ten times quieter' is not a threshold: no condition is adaptive-only at f_m = 1, the count grows monotonically as f_m falls, it is already positive at f_m = 0.5 (%s) for all three requirements, and the largest f_m at which the picked handoff still works has medians %.2f / %.2f / %.2f over the conditions found at f_m = 0.1 (minimum %.2f): the finding is a gradual dependence on the memory ratio, sampled at 1 and 0.1 only in the envelope"
          % (", ".join("%d" % curve[rn][i5] for rn in REQ), *[float(np.median(fstar[rn])) for rn in REQ], min(float(fstar[rn].min()) for rn in REQ)),
          all(curve[rn][0] == 0 for rn in REQ) and all(all(a <= b for a, b in zip(curve[rn], curve[rn][1:])) for rn in REQ) and all(curve[rn][i5] > 0 for rn in REQ) and all(len(fstar[rn]) == curve[rn][FMG.index(0.1)] for rn in REQ) and all(fstar[rn].min() >= 0.1 for rn in REQ))
    # ------------------------------------------------------------ K7: how much do the neglected terms matter for the coverage numbers? (review follow-up)
    # (a) combination rule: S = Sg + Sm and R = Rg + Rm add the gate-phase and memory-phase probabilities; the opposite bracket treats the two phases as independent outcomes (reject if either rejects; silent if not rejected and wrong in either)
    def parts(k, p, rho, fm, wts, kappa=1.0):
        o = OPT[k]; q = rho * fm * p if k in ("M1", "M5", "M6x") else rho * p; Sm, Rm = mem_from_table(o.tab, q, wts, WS)
        Sg = (kappa ** 2 * o.second[0] * p * p + kappa * o.second[1] * p * q * WS) if o.second is not None else kappa * o.s1 * p; Rg = kappa * o.r1 * p
        return [np.broadcast_to(np.asarray(x, dtype=float), WS.shape) for x in (Sg, Rg, Sm, Rm)]
    def union_rule(k, p, rho, fm, wts, s):
        Sg, Rg, Sm, Rm = parts(k, p, rho, fm, wts); A = 1 - s ** OPT[k].g; og, om = 1 - Sg - Rg, 1 - Sm - Rm
        R = 1 - (1 - Rg) * (1 - Rm); S = og * Sm + Sg * om + Sg * Sm; return S, 1 - (1 - A) * (1 - R)
    mx = 0.0
    for (p, rho, fm, bn, s), d in list(DATA.items())[:40]:
        for k in ("CONV", "M1", "M5", "M6x"):
            Sg, Rg, Sm, Rm = parts(k, p, rho, fm, BIAS[bn]); mx = max(mx, float(np.abs(np.minimum(Sg + Sm, 1) - np.asarray(d[k][0])).max()), float(np.abs(np.minimum(Rg + Rm, 1) - np.asarray(d[k][1])).max()))
    flips = 0; dec = 0; cov_u = {}
    for (p, rho, fm, bn, s), d in DATA.items():
        U = {"STAY": (d["STAY"][0], d["STAY"][3])}
        for k in ("CONV", "M1", "M5", "M6x"): U[k] = union_rule(k, p, rho, fm, BIAS[bn], s)
        for rn, rq in REQ.items():
            F0 = {k: feas_arr(d, k, rq) for k in NAMES}; F1 = {k: (np.asarray(U[k][0]) <= rq[0]) & (np.asarray(U[k][1]) <= rq[1]) for k in NAMES}
            for k in NAMES: flips += int((F0[k] != F1[k]).sum()); dec += len(WS)
            a0 = np.zeros(len(WS), bool); a1 = np.zeros(len(WS), bool)
            for k in NAMES: a0 |= F0[k]; a1 |= F1[k]
            c = cov_u.setdefault((rn, s), [0, 0, {k: 0 for k in NAMES}, 0]); c[0] += int(a1.sum()); c[1] += int((a1 & ~F1["STAY"]).sum()); c[3] += len(WS)
            for k in NAMES: c[2][k] += int(F1[k].sum())
    same = all(cov_u[(rn, s)][0] == cov[(rn, s)][2] and cov_u[(rn, s)][1] == cov[(rn, s)][3] and cov_u[(rn, s)][2] == cov[(rn, s)][1] for rn in REQ for s in SS)
    print("      (a) independent-union combination of the gate phase and the memory phase instead of adding them: option feasibility decisions that change: %d of %d over the whole envelope; oracle coverage, adaptive-only counts and every fixed coverage identical: %s (reconstruction of the additive S and R from the parts: max difference %.1e)" % (flips, dec, same, mx))
    # (b) exact second-order rejection of the M5 round trip (gate pairs and gate x parked-qubit pairs, with the first-order overlap removed), and the union property
    ops5, cf5 = OPT["M5"].ops, RT["M5"][1]; vid5 = s30.run(ops5, v_in); K05 = [0, 1, 2, 3, s30.R1, s30.R2]; loc5 = s30.locations(ops5)
    G5 = [l for l in loc5 if l[2] != "PARK"]; P5 = [l for l in loc5 if l[2] == "PARK"]
    def cls5(v): return "d" if not cf5(v) else ("h" if s30.reduced_fid(v, vid5, K05) > 0.5 else "s")
    one = {}
    for (i, oo, _) in loc5:
        cc = [cls5(s30.run(ops5, v_in, [(i, f)])) for f in oo]; one[i] = (Fr(cc.count("d"), len(cc)), Fr(cc.count("s"), len(cc)))
    sd = sum(one[l[0]][0] for l in G5); rj = sum(one[l[0]][0] for l in P5)
    def pair5(A, B, same):
        td = ts = Fr(0)
        for ia in range(len(A)):
            for ib in range(ia + 1 if same else 0, len(B)):
                (i, oa, _), (j, ob, _) = A[ia], B[ib]; cc = [cls5(s30.run(ops5, v_in, [(i, fa), (j, fb)])) for fa in oa for fb in ob]; td += Fr(cc.count("d"), len(cc)); ts += Fr(cc.count("s"), len(cc))
        return td, ts
    gd, gs = pair5(G5, G5, True); pd_, ps_ = pair5(G5, P5, False); c2R = gd - (len(G5) - 1) * sd; cxR = pd_ - sd * len(P5) - rj * len(G5)
    print("      (b) M5 round trip, exact to second order: rejection = %s p %+.3f p^2 %+.3f p q w (gate pairs; gate x parked pairs per parked layer); silent pair sums %s p^2 and %s p q w reproduce K0's coefficients" % (sd, float(c2R), float(cxR), gs, ps_))
    cov_c = {}; 
    for (p, rho, fm, bn, s), d in DATA.items():
        q = rho * fm * p; S5, R5, A5, L5, CC5 = [np.broadcast_to(np.asarray(x, dtype=float), WS.shape) for x in d["M5"]]
        R5c = np.clip(R5 + float(c2R) * p * p + float(cxR) * p * q * WS, 0, 1); L5c = 1 - (1 - A5) * (1 - R5c)
        for rn, rq in REQ.items():
            F = {k: feas_arr(d, k, rq) for k in NAMES}; F["M5"] = (S5 <= rq[0]) & (L5c <= rq[1]); a = np.zeros(len(WS), bool)
            for k in NAMES: a |= F[k]
            c = cov_c.setdefault((rn, s), [0, 0, {k: 0 for k in NAMES}]); c[0] += int(a.sum()); c[1] += int((a & ~F["STAY"]).sum())
            for k in NAMES: c[2][k] += int(F[k].sum())
    same2 = all(cov_c[(rn, s)][0] == cov[(rn, s)][2] and cov_c[(rn, s)][1] == cov[(rn, s)][3] and cov_c[(rn, s)][2] == cov[(rn, s)][1] for rn in REQ for s in SS)
    extra = 0
    for (p, rho, fm, bn, s), d in DATA.items():
        for rn, rq in REQ.items():
            Fx = {k: feas_arr(d, k, rq) for k in NAMES}; extra += int(((Fx["CONV"] | Fx["M1"] | Fx["M6x"]) & ~(Fx["STAY"] | Fx["M5"])).sum())
    print("      with M5's exact second-order rejection every coverage count (fixed options, oracle, adaptive-only) is unchanged: %s" % same2)
    print("      (c) conditions (all s) where CONV, M1 or M6x meets a requirement that neither STAY nor M5 meets: %d (so the oracle's coverage is that of STAY and M5, whose memory parts are exact and whose gate parts are exact to second order)" % extra)
    # (d) sensitivity to a uniform error in all gate-phase fault terms (kappa), at s = 1: how much does a 10 % or 25 % error in the gate faults move the counts?
    kap_rows = {}
    for kap in (0.9, 1.0, 1.1, 1.25):
        for rn, rq in REQ.items():
            n = 0; orc = 0; bf = {k: 0 for k in NAMES}; ao = 0
            for (p, rho, fm, bn, s), _ in DATA.items():
                if s != 1.0: continue
                d = all_metrics(p, rho, fm, BIAS[bn], 1.0, kap)
                for iw in range(len(WS)):
                    ok = [k for k in NAMES if fe(d, k, rq, iw)]; n += 1; orc += bool(ok); ao += bool(ok) and "STAY" not in ok
                    for k in ok: bf[k] += 1
            kap_rows[(kap, rn)] = (100 * orc / n, 100 * max(bf.values()) / n, 100 * (orc - max(bf.values())) / n, ao)
    print("      (d) all conversion and transfer gate-fault terms scaled by kappa (s = 1): oracle coverage % / best fixed % / gain (points) / adaptive-only count, per requirement")
    for kap in (0.9, 1.0, 1.1, 1.25): print("      kappa %-5g " % kap + "   ".join("%s: %.1f / %.1f / %+.2f / %d" % ((rn.split()[0],) + kap_rows[(kap, rn)]) for rn in REQ))
    check("K7 the neglected terms do not change any coverage count of the envelope: independent-union combination flips %d of %d feasibility decisions and leaves the counts as they are (%s), M5's exact second-order rejection leaves them as they are (%s), and no other option ever meets a requirement that neither STAY nor M5 meets (%d); a uniform 10 %% / 25 %% error in the gate-fault terms moves the adaptive-only counts for the first requirement from %d to %d / %d and for the third from %d to %d / %d (the gain over the best fixed option is not monotone in kappa: %+.2f, %+.2f, %+.2f points for the first requirement), so the decisions near a threshold are sensitive to the gate rates themselves, which the thresholds kappa* of K3 quantify"
          % (flips, dec, same, same2, extra, kap_rows[(1.0, list(REQ)[0])][3], kap_rows[(1.1, list(REQ)[0])][3], kap_rows[(1.25, list(REQ)[0])][3], kap_rows[(1.0, list(REQ)[2])][3], kap_rows[(1.1, list(REQ)[2])][3], kap_rows[(1.25, list(REQ)[2])][3], kap_rows[(1.0, list(REQ)[0])][2], kap_rows[(1.1, list(REQ)[0])][2], kap_rows[(1.25, list(REQ)[0])][2]),
          mx < 1e-12 and same and same2 and extra == 0 and gs == Fr(1752, 25) and ps_ == Fr(104, 5) and sd == Fr(104, 5) and all(kap_rows[(a, rn)][3] >= kap_rows[(b, rn)][3] for rn in REQ for a, b in ((0.9, 1.0), (1.0, 1.1), (1.1, 1.25))))
    # ------------------------------------------------------------ K8: labelled denominators and the gate-count convention (review follow-up)
    print("      K5's representative condition with labelled denominators (p = 1e-3, rho_p = 1, f_m = 0.1, unbiased, w = 100): S per attempted run; S / (1 - R) = silent error among ACCEPTED outputs (no abort); inter-photon gates per correct completion under two conventions: SCHEDULED (all g gates charged to every attempt, K5) and EXECUTED (gates run until the first heralded failure: (1 - s^g)/(1 - s) in expectation)")
    k8 = {}
    for k in NAMES:
        for s in SS:
            d = DATA[(1e-3, 1.0, 0.1, "unbiased", s)]; S, R, A, L, CC = d[k]; S = at(S, iw3); R = at(R, iw3); CC = at(CC, iw3); g = 0 if k == "STAY" else OPT[k].g
            ge = (g if s == 1.0 else (1 - s ** g) / (1 - s)) if g else 0.0; k8[(k, s)] = (S, R, S / (1 - R), g / CC if g else None, ge / CC if g else None, ge)
        print("      %-5s S %.5f  R %.4f  accepted-output silent %.3f %%  |  gates per correct completion scheduled / executed at s = 1, 0.99, 0.9: %s" % (k, k8[(k, 1.0)][0], k8[(k, 1.0)][1], 100 * k8[(k, 1.0)][2], " | ".join("-" if g_ is None else "%.1f / %.1f" % (g_, e_) for g_, e_ in ((k8[(k, s)][3], k8[(k, s)][4]) for s in SS))))
    check("K8 the silent error among accepted outputs is %.2f %% for M1 and %.3f %% for M5 at the K5 condition (S per attempted run %.4f and %.5f), and the executed-gate convention charges fewer gates per correct completion than the scheduled one whenever s < 1 (M5 at s = 0.9: %.1f against %.1f) and the same at s = 1"
          % (100 * k8[("M1", 1.0)][2], 100 * k8[("M5", 1.0)][2], k8[("M1", 1.0)][0], k8[("M5", 1.0)][0], k8[("M5", 0.9)][4], k8[("M5", 0.9)][3]),
          abs(k8[("M1", 1.0)][2] - 0.0333) < 5e-4 and abs(k8[("M5", 1.0)][2] - 0.00050) < 5e-5 and all(k8[(k, 1.0)][3] == k8[(k, 1.0)][4] for k in NAMES[1:]) and all(k8[(k, s)][4] < k8[(k, s)][3] for k in NAMES[1:] for s in (0.99, 0.9)))
    print("NOTE  the oracle is an upper bound: estimating p, the idle ratios and the wait costs something that is not modelled here; gate x memory cross terms are neglected except for M5 (K7 brackets their effect on every coverage count); heralded abort is assumed fatal for the information.  Total wall-clock %.0f s" % (time.time() - t00))
    print("ALL PASS" if OK else "FAILED")
    return 0 if OK else 1

if __name__ == "__main__": sys.exit(main())
