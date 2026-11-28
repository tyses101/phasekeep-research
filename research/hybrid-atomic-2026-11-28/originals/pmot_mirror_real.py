"""Realism for the ancilla-switched atomic mirror (10x10, spacing 0.8 lambda, Gaussian input, single photon).
Baseline = the ideal case of pmot_model_Q2.py. One imperfection is added at a time:
  1. Atom-position disorder: Gaussian displacement sigma (all 3 axes), averaged over random realizations.
  2. Filling defects: each site empty with probability p, averaged over realizations.
  3. Ancilla shift profile: shift_j = D0 / (1 + (rho_j / Rc)^6) (rho = distance from array centre), several D0 and Rc;
     plus uniform shifts of different strength.
  4. Real-atom transition model: sigma+-only dipoles (a cycling transition, e.g. Rb F=2,mF=2 -> F'=3,mF'=3),
     instead of the isotropic J=0 -> 1 model.
  5. Finite photon bandwidth: Gaussian spectrum of rms width b (units of Gamma0), frequency-resolved overlap.
Metrics (per photon): reflection R and transmission T into the Gaussian modes for each ancilla branch, the ancilla
coherence |O| and concurrence after the photon, routing fidelity (R_g + T_r)/2, and collected fraction.
Ancilla decay during the photon is estimated analytically in the report (not simulated here).
"""
import numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pmot_model_Q as Q
from pmot_model_C import green, lg, SIG0
from pmot_model_Q2 import lattice, lg_far_dir

lam = 2*np.pi
EP = np.array([1, 1j, 0])/np.sqrt(2)

def solve_any(pos, w, det, sigma_only=False):
    N = len(pos)
    if sigma_only:
        M = np.zeros((N, N), complex)
        for j in range(N):
            M[j, j] = det[j] + 0.5j
            for k in range(N):
                if k != j: M[j, k] = np.conj(EP) @ (3*np.pi*green(pos[j] - pos[k])) @ EP
        E = np.array([lg(0, w, p[0], p[1]) for p in pos])          # sigma+ projection of a sigma+ beam
        c = np.linalg.solve(M, -E)
        return np.concatenate([[lg(0, w, p[0], p[1])*EP for p in pos]]).ravel(), np.kron(c, EP)
    M = np.zeros((3*N, 3*N), complex)
    for j in range(N):
        M[3*j:3*j+3, 3*j:3*j+3] = (det[j] + 0.5j)*np.eye(3)
        for k in range(N):
            if k != j: M[3*j:3*j+3, 3*k:3*k+3] = 3*np.pi*green(pos[j] - pos[k])
    E = np.concatenate([lg(0, w, p[0], p[1])*EP for p in pos])
    return E, np.linalg.solve(M, -E)

FIN_CACHE = {}
def metrics(pos, w, det_g, det_r, sigma_only=False):
    key = round(w, 6)
    if key not in FIN_CACHE:
        FIN_CACHE[key] = (Q.lg_far(0, w), lg_far_dir(0, w, forward=False))
        E1, c1 = solve_any(np.array([[0, 0, 0.0]]), w, [0.0], sigma_only=False)
        FIN_CACHE[(key, "n1")] = np.sum(np.imag(np.conj(E1)*c1))
    fin, bwd = FIN_CACHE[key]; n1 = FIN_CACHE[(key, "n1")]
    out = {}
    for k, d in (("g", det_g), ("r", det_r)):
        E, c = solve_any(pos, w, d, sigma_only)
        ext = SIG0*2/(np.pi*w*w)*np.sum(np.imag(np.conj(E)*c))/n1
        A = Q.scat_far(pos, c)
        out[k] = (A, ext)
    sk, phi0, _ = Q.calibrate(fin, out["g"][0], out["r"][0], out["g"][1])
    gam = {k: fin + sk*np.exp(1j*phi0)*out[k][0] for k in out}
    err = max(abs(np.real(Q.inner(gam[k], gam[k])) - 1) for k in gam)
    R = {k: abs(Q.inner(bwd, gam[k]))**2 for k in gam}; T = {k: abs(Q.inner(fin, gam[k]))**2 for k in gam}
    O = Q.inner(gam["g"], gam["r"])
    return dict(Rg=R["g"], Rr=R["r"], Tg=T["g"], Tr=T["r"], O=O, err=err, gam=gam)

def summarize(tag, ms):
    Rg, Rr, Tg, Tr = (np.mean([m[k] for m in ms]) for k in ("Rg", "Rr", "Tg", "Tr"))
    coh = abs(np.mean([m["O"] for m in ms])) if len(ms) == 1 else np.mean([abs(m["O"]) for m in ms])
    conc = np.sqrt(max(0, 1 - coh**2)); route = (Rg + Tr)/2; coll = (Rg + Tg + Rr + Tr)/2
    err = max(m["err"] for m in ms)
    print(f"  {tag:44s} R g/r {Rg:.3f}/{Rr:.3f}  T g/r {Tg:.3f}/{Tr:.3f}  coherence {coh:.3f} conc {conc:.3f}"
          f"  routing {route:.3f}  collected {coll:.3f}  (norm err {err:.1e}, n={len(ms)})", flush=True)

if __name__ == "__main__":
    n, a = 10, 0.8*lam; base = lattice(n, a); w = 0.45*n*a; N = len(base); rng = np.random.default_rng(7)
    z = np.zeros(N); five = np.full(N, 5.0)
    print("BASELINE (ideal, isotropic atoms, uniform shift 5, monochromatic)")
    summarize("ideal", [metrics(base, w, z, five)])
    print("\n1. POSITION DISORDER (sigma in lambda, 3D), 6 realizations each")
    for s in (0.02, 0.05, 0.1):
        summarize(f"sigma = {s} lambda", [metrics(base + rng.normal(0, s*lam, base.shape), w, z, five) for _ in range(6)])
    print("\n2. FILLING DEFECTS (empty-site probability), 6 realizations each")
    for p in (0.02, 0.05, 0.1, 0.2):
        ms = []
        for _ in range(6):
            keep = rng.random(N) > p; pos = base[keep]; ms.append(metrics(pos, w, np.zeros(len(pos)), np.full(len(pos), 5.0)))
        summarize(f"empty fraction = {p}", ms)
    print("\n3. ANCILLA SHIFT: strength and spatial profile")
    rho = np.linalg.norm(base[:, :2], axis=1)
    for D0 in (2.0, 5.0, 20.0):
        summarize(f"uniform shift D0 = {D0}", [metrics(base, w, z, np.full(N, D0))])
    for Rc in (6.0, 4.0, 3.0):
        summarize(f"profile D0=20, Rc = {Rc} lambda", [metrics(base, w, z, 20/(1 + (rho/(Rc*lam))**6))])
    print("\n4. CYCLING-TRANSITION ATOMS (sigma+ only) instead of isotropic")
    for d0 in (-0.5, 0.0, 0.5):
        summarize(f"sigma+ only, probe detuning {d0:+.1f}", [metrics(base, w, np.full(N, d0), np.full(N, d0 + 5), sigma_only=True)])
    print("\n5. PHOTON BANDWIDTH (Gaussian spectrum, rms b in units of Gamma0), isotropic, uniform shift 5")
    dets = np.linspace(-3, 3, 25); per = {d: metrics(base, w, np.full(N, d), np.full(N, d + 5)) for d in dets}
    for b in (0.05, 0.2, 0.5, 1.0):
        wts = np.exp(-dets**2/(2*b*b)); wts /= wts.sum()
        R_g = sum(wt*per[d]["Rg"] for d, wt in zip(dets, wts)); T_r = sum(wt*per[d]["Tr"] for d, wt in zip(dets, wts))
        Rr = sum(wt*per[d]["Rr"] for d, wt in zip(dets, wts)); Tg = sum(wt*per[d]["Tg"] for d, wt in zip(dets, wts))
        Oav = sum(wt*per[d]["O"] for d, wt in zip(dets, wts))
        coh = abs(Oav); print(f"  bandwidth b = {b:4.2f} Gamma0                         R g/r {R_g:.3f}/{Rr:.3f}  T g/r {Tg:.3f}/{T_r:.3f}"
                              f"  coherence {coh:.3f} conc {np.sqrt(max(0, 1-coh**2)):.3f}  routing {(R_g + T_r)/2:.3f}", flush=True)
