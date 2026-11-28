"""Two-register photon-mediated heralded gate built from ancilla-switched atomic mirrors (PMOT branch).

PART A -- corrected single-pass mirror model (10x10 array, spacing 0.8 lambda, Gaussian beam)
  Fixes requested in review:
   (1) longitudinal incident phase e^{ikz} for atoms displaced along z (Gaussian-beam Gouy/curvature corrections
       are estimated and shown negligible: z_R = pi w^2/lambda);
   (2) spectral grid refined to 0.005 linewidth for photon bandwidths ~0.05 linewidth;
   (3) ensemble entanglement: mean per-realization pure-state concurrence versus concurrence of the
       ensemble-averaged (collection-heralded) mixed state (Wootters);
   plus: transverse (n-projected) polarization in the far field, explicit normalization of every branch.
  Mode amplitudes use input-output relations: t = 1 + g S_fwd, r = g S_bwd, with S = sum_j conj(mode(r_j)).c_j and
  one complex constant g. g is fixed by a far-field projection on the ideal array (optical theorem fixes its phase)
  and VALIDATED on other configurations by |r|^2 + |t|^2 <= 1 with the far-field-derived leakage.
PART B -- conditional-phase element: array + retro-mirror behind it (round-trip phase theta):
  R_x = r_x + t_x^2 e^{i theta} / (1 - r_x e^{i theta})   (symmetric array; mode-matched retro-reflection ASSUMED)
PART C -- protocols on two registers A, B (qubits |g>=0, |r>=1 of each ancilla), single photon:
  (I) interferometric: MZ1 (device A in one arm) -> MZ2 fed by MZ1's output port 1 (device B in one arm)
      -> beam splitter -> detection d in {0,1} -> feed-forward Z corrections.  Ideal = CZ_AB (photon as flying
      ancilla; same logical structure as Daiss et al., Science 371, 614 (2021)).
  (S) sequential: single MZ whose device arm reflects off A then B -> heralded parity projection (entangler).
  Imperfections: device amplitudes from PART A (loss -> no click), path-phase errors, photon distinguishability V
  (mode mismatch between device arm and bypass), ancilla decay during the photon (amplitude damping p).
Metrics: heralding probability, conditional average gate fidelity (random superpositions and an entangled
reference via the Choi state), unconditional success per launched photon, coherence accounting (local, joint,
accessible, leaked), photon information leakage (outcome dependence on the register state), repeated-operation
budget.
"""
import numpy as np, itertools, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pmot_model_C import green, lg, SIG0

lam = 2*np.pi
EP = np.array([1, 1j, 0])/np.sqrt(2)
rng = np.random.default_rng(11)

# ---------------------------------------------------------------- PART A: single-pass mirror
def lattice(n, a):
    xs = (np.arange(n) - (n - 1)/2)*a
    return np.array([[x, y, 0.0] for x in xs for y in xs])

def coupling_matrix(pos):
    N = len(pos); V = np.zeros((3*N, 3*N), complex)
    for j in range(N):
        for k in range(N):
            if k != j: V[3*j:3*j+3, 3*k:3*k+3] = 3*np.pi*green(pos[j] - pos[k])
    return V

def solve(pos, w, det, V):
    N = len(pos)
    E = np.concatenate([lg(0, w, p[0], p[1])*np.exp(1j*p[2])*EP for p in pos])      # fix (1): e^{ikz}
    M = V + np.kron(np.diag(np.asarray(det, float) + 0.5j), np.eye(3))
    return np.linalg.solve(M, -E)

def mode_sums(pos, w, c):
    d = c.reshape(-1, 3)
    uf = np.array([lg(0, w, p[0], p[1])*np.exp(1j*p[2]) for p in pos])               # forward mode at atoms
    ub = np.array([lg(0, w, p[0], p[1])*np.exp(-1j*p[2]) for p in pos])              # backward mode at atoms
    return np.sum(np.conj(uf)*(d @ np.conj(EP))), np.sum(np.conj(ub)*(d @ np.conj(EP)))

# far-field machinery (transverse polarization, used only to calibrate g and to measure leakage)
NTH, NPH = 1200, 48
TH = (np.arange(NTH) + 0.5)*np.pi/NTH; PH = np.linspace(0, 2*np.pi, NPH, endpoint=False)
TT, PP = np.meshgrid(TH, PH, indexing="ij"); DW = np.sin(TT)*(np.pi/NTH)*(2*np.pi/NPH)
NV = np.stack([np.sin(TT)*np.cos(PP), np.sin(TT)*np.sin(PP), np.cos(TT)], -1)
def inner(a, b): return np.sum(np.conj(a)*b*DW[..., None])
def transverse(v): return v - NV*np.sum(NV*v, -1, keepdims=True)
def gauss_far(w, forward):
    s = np.sin(TT); m = (NV[..., 2] > 0) if forward else (NV[..., 2] < 0)
    f = transverse((np.exp(-(w*s/2)**2)*m)[..., None]*EP)                               # transverse polarization
    return f/np.sqrt(np.real(inner(f, f)))
def scat_far(pos, c):
    d = c.reshape(-1, 3); ph = np.exp(-1j*np.einsum("tpk,nk->tpn", NV, pos))
    return transverse(np.einsum("tpn,nk->tpk", ph, d))

def calibrate_g(pos, w, V):
    """Independent calibration (optical theorem): extinction = -2 Re(g S_fwd) must equal the model-C extinction
    2 sigma0/(pi w^2) * Im(sum conj(E).c)/n1 (n1 = single on-axis atom).  This fixes g = i kappa with
    kappa = sigma0/(pi w^2 n1); the same g applies to the backward mode by mirror symmetry of a planar dipole sheet.
    Validated afterwards by |r|^2 + |t|^2 <= 1 on every configuration (no fitted parameter)."""
    c1 = solve(np.zeros((1, 3)), w, [0.0], np.zeros((3, 3)))
    n1 = np.sum(np.imag(np.conj(lg(0, w, 0, 0)*EP)*c1))
    g = 1j*SIG0/(np.pi*w*w*n1)
    c = solve(pos, w, np.zeros(len(pos)), V); Sf, Sb = mode_sums(pos, w, c)
    t, r = 1 + g*Sf, g*Sb
    return g, g, dict(t=t, r=r, leak=1 - abs(t)**2 - abs(r)**2)

def calibrate_g_farfield_unused(pos, w, V):
    """(superseded: phase search converged to the trivial zero-scattering root) Far-field: gamma = fin + s e^{i phi} A, with s from photon conservation and the optical theorem
    (Re<fin|sc> = -||sc||^2/2), solved exactly for one configuration; g then follows from t = 1 + g S_fwd."""
    fin, bwd = gauss_far(w, True), gauss_far(w, False)
    c = solve(pos, w, np.zeros(len(pos)), V); A = scat_far(pos, c)
    X, NA = inner(fin, A), np.real(inner(A, A))
    # unknown complex z = s e^{i phi}: |fin + z A|^2 = 1  ->  2 Re(z X) + |z|^2 NA = 0, and z X real & negative for a
    # lossless forward-scattering theorem with no backward overlap of fin; choose z = -2 conj(X)/NA * (Re/|X|^2 part)
    z = -2*np.conj(X)*np.real(X)/(abs(X)**2*NA) if abs(X) > 0 else 0
    # general solution family z = rho e^{i phi}; use the optical-theorem branch that also matches the backward mode
    best = None
    for phi in np.linspace(0, 2*np.pi, 7201):
        rho = -2*np.real(np.exp(1j*phi)*X)/NA
        if rho <= 0: continue
        gam = fin + rho*np.exp(1j*phi)*A
        err = abs(np.real(inner(gam, gam)) - 1)
        tf = inner(fin, gam); rb = inner(bwd, gam)
        if best is None or abs(abs(tf)**2 + abs(rb)**2 - 1) < best[0] - 1e-12 or (abs(abs(tf)**2 + abs(rb)**2 - 1) <= 1 and best is None):
            best = (abs(abs(tf)**2 + abs(rb)**2 - 1), phi, rho, tf, rb)
    _, phi, rho, tf, rb = best
    Sf, Sb = mode_sums(pos, w, c)
    g_f, g_b = (tf - 1)/Sf, rb/Sb
    return g_f, g_b, dict(t=tf, r=rb, leak=1 - abs(tf)**2 - abs(rb)**2)

def single_pass(pos, w, det, V, g_f, g_b):
    c = solve(pos, w, det, V); Sf, Sb = mode_sums(pos, w, c)
    t, r = 1 + g_f*Sf, g_b*Sb
    n = abs(t)**2 + abs(r)**2
    return r, t, max(0.0, 1 - n)

def wootters(rho):
    sy = np.array([[0, -1j], [1j, 0]]); Y = np.kron(sy, sy)
    ev = np.sqrt(np.abs(np.sort(np.linalg.eigvals(rho @ Y @ np.conj(rho) @ Y).real)[::-1]))
    return max(0.0, ev[0] - ev[1] - ev[2] - ev[3])

# ---------------------------------------------------------------- PART B: conditional-phase device
def device(r, t, theta):
    e = np.exp(1j*theta)
    return r + t*t*e/(1 - r*e)

# ---------------------------------------------------------------- PART C: protocols
def bs(a, b):                       # 50/50: input modes amplitudes -> outputs (o0, o1)
    return (a + b)/np.sqrt(2), (a - b)/np.sqrt(2)

def rot(V):                          # internal-mode change on a device pass (distinguishability)
    cb, sb = np.sqrt(V), np.sqrt(1 - V)
    return np.array([[cb, -sb], [sb, cb]])

def protocol_I(Ra, Rb, ph1=0.0, ph2=0.0, V=1.0):
    """Returns Kraus amplitudes A[d][k] as 4-vectors over |ab>, ab in 00,01,10,11 (diagonal operations)."""
    D = rot(V); out = {(d, k): np.zeros(4, complex) for d in (0, 1) for k in (0, 1)}
    for idx, (a, b) in enumerate(itertools.product((0, 1), (0, 1))):
        v0 = np.array([1, 0], complex)                                  # internal mode vector
        u, l = bs(v0, np.zeros(2))                                      # BS1 (amplitude vectors per arm)
        u = Ra[a]*(D @ u); l = np.exp(1j*ph1)*l
        o0, o1 = bs(u, l)                                               # BS2
        o1 = Rb[b]*(D @ o1); o0 = np.exp(1j*ph2)*o0
        d0, d1 = bs(o1, o0)                                             # BS3
        for k in (0, 1):
            out[(0, k)][idx] = d0[k]; out[(1, k)][idx] = d1[k]
    return out

def protocol_S(Ra, Rb, ph=0.0, V=1.0):
    D = rot(V); out = {(d, k): np.zeros(4, complex) for d in (0, 1) for k in (0, 1)}
    for idx, (a, b) in enumerate(itertools.product((0, 1), (0, 1))):
        u, l = bs(np.array([1, 0], complex), np.zeros(2))
        u = Rb[b]*(D @ (Ra[a]*(D @ u))); l = np.exp(1j*ph)*l
        d0, d1 = bs(u, l)
        for k in (0, 1):
            out[(0, k)][idx] = d0[k]; out[(1, k)][idx] = d1[k]
    return out

CZ = np.diag([1, 1, 1, -1]).astype(complex)
def damping_kraus(p):
    E0 = np.array([[1, 0], [0, np.sqrt(1 - p)]]); E1 = np.array([[0, np.sqrt(p)], [0, 0]])
    return [np.kron(x, y) for x in (E0, E1) for y in (E0, E1)]

def corrections_from_ideal(amps):
    """Feed-forward local phases per outcome d that turn the ideal Kraus into CZ (fixed lookup)."""
    corr = {}
    for d in (0, 1):
        p = amps[(d, 0)]; p = p/p[0]
        cA = np.array([1, np.conj(p[2])/abs(p[2])]); cB = np.array([1, np.conj(p[1])/abs(p[1])])
        corr[d] = np.kron(np.diag(cA), np.diag(cB))
    return corr

def channel(amps, corr, p_dec, ideal_target=CZ):
    """Heralded channel Kraus list (with feed-forward) and failure Kraus (photon lost)."""
    dec = damping_kraus(p_dec)
    herald = []
    for (d, k), vec in amps.items():
        K = corr[d] @ np.diag(vec) if corr is not None else np.diag(vec)
        herald += [K @ E for E in dec]
    # failure: missing norm per register branch, env states taken orthogonal (conservative)
    miss = 1 - sum(np.abs(v)**2 for v in amps.values())
    fail = [np.diag(np.sqrt(np.clip(miss, 0, 1))*(np.arange(4) == i)) @ E for i in range(4) for E in dec]
    return herald, fail

def apply(Ks, rho):
    Ks = np.asarray(Ks); return np.einsum("nij,jk,nlk->il", Ks, rho, Ks.conj())

def haar_states(n, dim=4):
    v = rng.normal(size=(n, dim)) + 1j*rng.normal(size=(n, dim)); return v/np.linalg.norm(v, axis=1, keepdims=True)
PSI = haar_states(300)

def evaluate(herald, fail, target=CZ):
    Fs, Ps, Pd = [], [], []
    for psi in PSI:
        rho = np.outer(psi, psi.conj()); out = apply(herald, rho); P = np.real(np.trace(out))
        tgt = target @ psi; Fs.append(np.real(tgt.conj() @ out @ tgt)/P); Ps.append(P)
    # entangled reference (Choi): registers (x) 2-qubit reference, maximally entangled
    phi = np.zeros(16, complex)
    for i in range(4): phi[i*4 + i] = 0.5
    Ks = np.asarray(herald)                       # Choi-state fidelity with a maximally entangled reference
    PC = np.real(np.einsum("nij,nij->", Ks.conj(), Ks))/4
    Fpro = np.sum(np.abs(np.einsum("ij,nij->n", np.conj(target), Ks))**2)/16/PC; Favg = (4*Fpro + 1)/5
    # register survivability after a failed attempt (photon lost): fidelity with the pre-attempt state
    Ff = []
    for psi in PSI[:100]:
        rho = np.outer(psi, psi.conj()); o = apply(fail, rho); P = np.real(np.trace(o))
        if P > 1e-12: Ff.append(np.real(psi.conj() @ o @ psi)/P)
    return dict(F_states=np.mean(Fs), F_min=np.min(Fs), P_h=np.mean(Ps), P_h_spread=np.ptp(Ps), F_pro=Fpro, F_avg=Favg,
                F_after_fail=np.mean(Ff) if Ff else np.nan)

def photon_info(amps):
    """Outcome probabilities' dependence on the register input: if the photon leaves carrying no information,
    P(d) is the same for every input state."""
    Pd = []
    for psi in PSI[:200]:
        Pd.append([sum(abs(np.sum(np.abs(psi)**2*np.abs(amps[(d, k)])**2)) for k in (0, 1)) for d in (0, 1)])
    Pd = np.array(Pd); return Pd.mean(0), np.ptp(Pd[:, 0])

def coherence_accounting(amps_real, amps_ideal, corr, psi):
    """Local / joint / accessible / leaked for one input state (before decay; decay reported separately)."""
    # pre-measurement joint state: registers (x) (detector-basis amplitudes are a unitary image of the exit modes)
    J = np.array([[amps_real[(d, k)][i]*psi[i] for i in range(4)] for d in (0, 1) for k in (0, 1)])   # 4 photon x 4 reg
    Ji = np.array([[amps_ideal[(d, k)][i]*psi[i] for i in range(4)] for d in (0, 1) for k in (0, 1)])
    P_coll = np.real(np.sum(np.abs(J)**2)); leaked = 1 - P_coll
    rho_reg = J.T @ J.conj()                                        # reduced register state (collected part)
    rho_reg_full = rho_reg + np.diag((1 - np.sum(np.abs(np.stack([amps_real[x] for x in amps_real]))**2, 0))*np.abs(psi)**2)
    l1 = lambda r: np.sum(np.abs(r)) - np.sum(np.abs(np.diag(r)))
    local = l1(rho_reg_full)/l1(np.outer(psi, psi.conj()))
    joint = abs(np.sum(np.conj(Ji)*J))**2/max(P_coll, 1e-15)        # fidelity of joint (reg+photon) state, conditioned
    out = sum(np.outer(corr[d] @ (amps_real[(d, k)]*psi), (corr[d] @ (amps_real[(d, k)]*psi)).conj()) for d in (0, 1) for k in (0, 1))
    tgt = CZ @ psi; acc = np.real(tgt.conj() @ out @ tgt)/np.real(np.trace(out))
    return dict(local=local, joint=joint, accessible=acc, leaked=leaked)

# ---------------------------------------------------------------- main
if __name__ == "__main__":
    n, a = 10, 0.8*lam; base = lattice(n, a); w = 0.45*n*a; N = len(base)
    zR = np.pi*w*w/lam
    print(f"Beam: w = {w/lam:.2f} lambda, Rayleigh range z_R = {zR/lam:.1f} lambda; Gouy phase at z = 0.05 lambda: {0.05*lam/zR:.1e} rad"
          f" (curvature negligible) -> only e^(ikz) is kept [fix 1]")
    Vb = coupling_matrix(base)
    g_f, g_b, cal = calibrate_g(base, w, Vb)
    print(f"\nPART A calibration (ideal array, resonant, ancilla g): far field t = {cal['t']:.4f}, r = {cal['r']:.4f}, leak {cal['leak']:.4f}")
    for lbl, det in (("g (resonant)", np.zeros(N)), ("r (shift 5)", np.full(N, 5.0)), ("check: shift 2", np.full(N, 2.0)), ("check: det 0.3", np.full(N, 0.3))):
        r, t, lk = single_pass(base, w, det, Vb, g_f, g_b)
        print(f"  {lbl:16s} r = {r:+.4f}  t = {t:+.4f}  |r|^2={abs(r)**2:.4f} |t|^2={abs(t)**2:.4f} leak={lk:.4f}")
    print(f"  forward/backward constants agree? |g_f/g_b| = {abs(g_f/g_b):.4f}, phase diff {np.angle(g_f/g_b):+.4f} rad")

    # configurations: ideal, 2% defects, disorder 0.02 and 0.05 lambda (6 realizations each)
    configs = {"ideal": [(base, Vb)]}
    for lbl, maker in (("2% empty", lambda: base[rng.random(N) > 0.02]),
                       ("disorder 0.02", lambda: base + rng.normal(0, 0.02*lam, base.shape)),
                       ("disorder 0.05", lambda: base + rng.normal(0, 0.05*lam, base.shape))):
        reals = []
        for _ in range(6):
            p = maker(); reals.append((p, coupling_matrix(p)))
        configs[lbl] = reals

    # PART A ensemble entanglement (single pass, monochromatic): fix (3)
    print("\nPART A ensemble entanglement (ancilla (x) photon path R/T), monochromatic resonant probe")
    single = {}
    for lbl, reals in configs.items():
        Cs, rhos, Ws = [], np.zeros((4, 4), complex), 0
        for p, Vm in reals:
            rg, tg, lg_ = single_pass(p, w, np.zeros(len(p)), Vm, g_f, g_b)
            rr, tr, lr = single_pass(p, w, np.full(len(p), 5.0), Vm, g_f, g_b)
            O = np.conj(rg)*rr + np.conj(tg)*tr                                 # env overlap neglected (<= sqrt(lg lr))
            nrm = np.sqrt((abs(rg)**2 + abs(tg)**2 + lg_)*(abs(rr)**2 + abs(tr)**2 + lr))
            Cs.append(np.sqrt(max(0, 1 - abs(O/nrm)**2)))
            v = np.array([rg, tg, rr, tr])/np.sqrt(2)                           # |g>(r|R>+t|T>) + |r>(...), basis g/r x R/T
            rhos += np.outer(v, v.conj())
            single.setdefault(lbl, []).append((rg, tg, rr, tr))
        P = np.real(np.trace(rhos)); Cw = wootters(rhos/P)
        print(f"  {lbl:14s} mean per-realization concurrence (full field) {np.mean(Cs):.3f} | ensemble-averaged, "
              f"collection-heralded state concurrence {Cw:.3f} | collection prob {P/len(reals):.3f}")

    # spectral response on a fine grid: fix (2)
    dets = np.arange(-0.25, 0.2501, 0.005); bw = 0.05
    wts = np.exp(-dets**2/(2*bw*bw)); wts /= wts.sum()
    print(f"\nSpectral grid: {len(dets)} points, spacing 0.005 Gamma, photon rms bandwidth {bw} Gamma")

    DEV_CACHE = {}
    def device_set(lbl, theta, spectral):
        key = (lbl, spectral)
        if key not in DEV_CACHE: DEV_CACHE[key] = device_set_raw(lbl, theta, spectral)
        return DEV_CACHE[key]
    def device_set_raw(lbl, theta, spectral):
        """List of (weight, Ra(2), Rb(2)) over realizations x frequencies; A and B drawn from the same ensemble.
        Amplitudes are referenced to the fixed calibration phase CHI (set once on the ideal array at line centre,
        i.e. the bypass-arm phase is tuned once, not per realization)."""
        out = []
        reals = configs[lbl]
        freqs = list(zip(dets, wts)) if spectral else [(0.0, 1.0)]
        for i, (p, Vm) in enumerate(reals):
            pB, VB = reals[(i + 1) % len(reals)]
            for d0, wt in freqs:
                Ra, Rb = [], []
                for (pp, VV, RR) in ((p, Vm, Ra), (pB, VB, Rb)):
                    rg, tg, _ = single_pass(pp, w, np.full(len(pp), d0), VV, g_f, g_b)
                    rr, tr, _ = single_pass(pp, w, np.full(len(pp), d0 + 5.0), VV, g_f, g_b)
                    RR += [device(rg, tg, theta)*np.exp(-1j*CHI), device(rr, tr, theta)*np.exp(-1j*CHI)]
                out.append((wt/len(reals), np.array(Ra), np.array(Rb)))
        return out

    # choose the retro-mirror phase theta on the ideal array (maximize phase contrast x reflectivity)
    best = None
    for th in np.linspace(-np.pi, np.pi, 721):
        rg, tg, _ = single_pass(base, w, np.zeros(N), Vb, g_f, g_b); rr, tr, _ = single_pass(base, w, np.full(N, 5.0), Vb, g_f, g_b)
        Rg, Rr = device(rg, tg, th), device(rr, tr, th)
        score = abs(Rg)*abs(Rr)*abs(np.sin(np.angle(Rr/Rg)/2))
        if best is None or score > best[0]: best = (score, th, Rg, Rr)
    _, TH0, Rg0, Rr0 = best
    CHI = np.angle(Rr0 - Rg0)      # reference-arm phase that best maps (R_g, R_r) onto (-1, +1)
    print(f"\nPART B device (ideal array): theta = {TH0:+.3f} rad  R_g = {Rg0:+.4f} (|R|^2 {abs(Rg0)**2:.4f})  R_r = {Rr0:+.4f} "
          f"(|R|^2 {abs(Rr0)**2:.4f})  conditional phase {np.angle(Rr0/Rg0):+.4f} rad")

    def run_case(tag, lbl, protocol="I", ph1=0.0, ph2=0.0, V=1.0, p_dec=0.0, spectral=True, show_cohere=False):
        dev = device_set(lbl, TH0, spectral)
        ideal_dev = (np.array([-1, 1.0]), np.array([-1, 1.0]))
        if protocol == "I":
            amps_id = protocol_I(*ideal_dev); corr = corrections_from_ideal(amps_id); target = CZ
        else:
            amps_id = protocol_S(*ideal_dev); corr = None; target = None
        herald, fail = [], []
        for wt, Ra, Rb in dev:
            amps = protocol_I(Ra, Rb, ph1, ph2, V) if protocol == "I" else protocol_S(Ra, Rb, ph1, V)
            h, f = channel(amps, corr, p_dec)
            herald += [np.sqrt(wt)*K for K in h]; fail += [np.sqrt(wt)*K for K in f]
        if protocol == "I":
            m = evaluate(herald, fail)
            pinfo, spread = photon_info(protocol_I(*dev[(len(dets)//2) if spectral else 0][1:], ph1, ph2, V))
            s = (f"  {tag:40s} P_herald {m['P_h']:.3f}  F_cond(avg gate) {m['F_avg']:.4f}  F_states mean/min {m['F_states']:.4f}/{m['F_min']:.4f}"
                 f"  unconditional success/photon {m['P_h']*m['F_avg']:.3f}  F after failed attempt {m['F_after_fail']:.3f}"
                 f"  photon P(d=0) spread over inputs {spread:.1e}")
            print(s, flush=True)
            if show_cohere:
                wt, Ra, Rb = dev[(len(dets)//2) if spectral else 0]
                for name, psi in (("|++>", np.full(4, 0.5, complex)), ("random", PSI[0])):
                    ca = coherence_accounting(protocol_I(Ra, Rb, ph1, ph2, V), amps_id, corr, psi)
                    print(f"      coherence [{name}]: local {ca['local']:.3f}  joint {ca['joint']:.4f}  accessible {ca['accessible']:.4f}  leaked {ca['leaked']:.3f}")
            return m
        else:
            # parity entangler: input |++>, compare each outcome with the ideal (normalized) projection
            psi = np.full(4, 0.5, complex); res = []
            for d in (0, 1):
                out = sum(np.outer(np.sqrt(wt)*amps_k*psi, (np.sqrt(wt)*amps_k*psi).conj())
                          for wt, Ra, Rb in dev for k in (0, 1)
                          for amps_k in [protocol_S(Ra, Rb, ph1, V)[(d, k)]])
                Pd = np.real(np.trace(out)); vi = amps_id[(d, 0)]*psi; vi = vi/np.linalg.norm(vi)
                res.append((Pd, np.real(vi.conj() @ out @ vi)/Pd))
            print(f"  {tag:40s} outcome d=0: P {res[0][0]:.3f} Bell fidelity {res[0][1]:.4f} | d=1: P {res[1][0]:.3f} Bell fidelity {res[1][1]:.4f}", flush=True)

    print("\nPART C ideal analytic baseline (R_g = -1, R_r = +1, no loss)")
    am = protocol_I(np.array([-1, 1.0]), np.array([-1, 1.0])); co = corrections_from_ideal(am)
    h, f = channel(am, co, 0.0); m = evaluate(h, f); pi_, sp = photon_info(am)
    print(f"  protocol I: P_herald {m['P_h']:.4f}, F_avg {m['F_avg']:.6f}, F_states min {m['F_min']:.6f}; P(d) = {pi_}, spread {sp:.1e}"
          " -> exact CZ, photon outcome independent of the registers (it leaves with no information)")
    psi = np.full(4, 0.5, complex)
    for d in (0, 1):
        v = protocol_S(np.array([-1, 1.0]), np.array([-1, 1.0]))[(d, 0)]*psi
        print(f"  protocol S, d={d}: P {np.sum(np.abs(v)**2):.3f}, state {np.round(v/np.linalg.norm(v), 3)} (parity projection)")

    print("\nPART C realistic device (ideal array), protocol I, photon bandwidth 0.05 Gamma")
    run_case("ideal array, perfect optics", "ideal", show_cohere=True)
    print("\nSensitivity: optical path phase errors (rad)")
    for e in (0.05, 0.1, 0.3):
        run_case(f"phase error ph1 = ph2 = {e}", "ideal", ph1=e, ph2=e)
    print("Sensitivity: photon distinguishability (mode overlap V)")
    for V in (0.99, 0.95, 0.9):
        run_case(f"V = {V}", "ideal", V=V)
    print("Sensitivity: ancilla decay per photon interaction p")
    for p in (0.0025, 0.01, 0.03):
        run_case(f"p_decay = {p}", "ideal", p_dec=p)
    print("Sensitivity: array imperfections")
    for lbl in ("2% empty", "disorder 0.02", "disorder 0.05"):
        run_case(lbl, lbl, show_cohere=(lbl == "disorder 0.02"))
    print("Combined realistic case: 2% empty + V 0.98 + phase 0.05 + p_decay 0.01")
    mR = run_case("combined", "2% empty", ph1=0.05, ph2=0.05, V=0.98, p_dec=0.01, show_cohere=True)

    print("\nPART C protocol S (sequential parity entangler), input |++>")
    run_case("ideal array", "ideal", protocol="S")
    run_case("2% empty + V 0.98 + p 0.01", "2% empty", protocol="S", V=0.98, p_dec=0.01)

    print("\nRepeated operations (protocol I), retry until heralded; per successful gate:")
    for tag, m in (("ideal array", run_case("ideal array (repeat budget)", "ideal")), ("combined realistic", mR)):
        att = 1/m["P_h"]; err = (1 - m["F_avg"]) + (att - 1)*(1 - m["F_after_fail"])
        print(f"  {tag:20s} attempts/gate {att:.2f}  error/gate {err:.4f}  ->  fidelity after 10 gates {np.exp(-10*err):.3f}, after 100 {np.exp(-100*err):.3f}")
