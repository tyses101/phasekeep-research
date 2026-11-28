"""PMOT quantum version, scaled up: larger sub-wavelength rings and 2D square arrays (atomic mirrors).
Same physics, conventions and calibration as pmot_model_Q.py (single photon, ancilla in (|g>+|r>)/sqrt2 shifting
chosen atoms by 5 linewidths when in |r>). Adds:
  - a global probe detuning scan (probe relative to the bare atomic line) to find collective resonances,
  - backward (reflected) Gaussian-mode detection in addition to forward modes,
  - a converter pattern with angular harmonic 2 for rings (shift_j = 5 (1 + cos 2 phi_j)/2), which couples l -> l +- 2.
Reported per case: ancilla coherence |O|, concurrence, forward input-mode probabilities and branch phase, backward
Gaussian probabilities, and (converter) probability in the target mode l' = -1.
"""
import numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pmot_model_Q as Q
from pmot_model_C import solve, ring, SIG0, ext_fraction

lam = 2*np.pi

def lg_far_dir(l, w, forward=True):
    s = np.sin(Q.TT)
    mask = (Q.NZ > 0) if forward else (Q.NZ < 0)
    u = (w*s/np.sqrt(2))**abs(l)*np.exp(-(w*s/2)**2)*np.exp(1j*l*Q.PP)*mask
    pol = Q.EPSP   # the reflected field keeps the same LAB-frame polarization vector as the driven dipoles
                   # (an earlier version used its conjugate, which is orthogonal and gave R = 0: fixed)
    f = u[..., None]*pol
    return f/np.sqrt(np.real(Q.inner(f, f)))

def lattice(n, a):
    xs = (np.arange(n) - (n - 1)/2)*a
    return np.array([[x, y, 0.0] for x in xs for y in xs])

def case(pos, w, l_in, det_g, det_r, det_chk, target=None):
    fin = Q.lg_far(l_in, w)
    sols = {k: solve(pos, l_in, w, d) for k, d in (("g", det_g), ("r", det_r), ("chk", det_chk))}
    A = {k: Q.scat_far(pos, c) for k, (E, c) in sols.items()}
    E1, c1 = solve(np.array([[0, 0, 0.0]]), 0, w, [0.0]); n1 = ext_fraction(E1, c1)
    ext = {k: SIG0*2/(np.pi*w*w)*ext_fraction(*sols[k])/n1 for k in sols}
    sk, phi0, ok = Q.calibrate(fin, A["g"], A["r"], ext["g"])
    gam = {k: fin + sk*np.exp(1j*phi0)*A[k] for k in A}
    norm_err = max(abs(np.real(Q.inner(gam[k], gam[k])) - 1) for k in gam)
    O = Q.inner(gam["g"], gam["r"])
    fwd, bwd = Q.lg_far(l_in, w), lg_far_dir(0, w, forward=False)
    ag, ar = Q.inner(fwd, gam["g"]), Q.inner(fwd, gam["r"])
    bg, br = Q.inner(bwd, gam["g"]), Q.inner(bwd, gam["r"])
    out = dict(coh=abs(O), conc=np.sqrt(max(0, 1 - abs(O)**2)), Pg=abs(ag)**2, Pr=abs(ar)**2,
               ph=np.angle(ar/ag) if abs(ag) > 1e-6 else np.nan, Rg=abs(bg)**2, Rr=abs(br)**2,
               bph=np.angle(br/bg) if abs(bg) > 1e-6 and abs(br) > 1e-6 else np.nan, ext_g=ext["g"], err=norm_err)
    if target is not None:
        tm = Q.lg_far(target, w)
        out["Tg"], out["Tr"] = abs(Q.inner(tm, gam["g"]))**2, abs(Q.inner(tm, gam["r"]))**2
    return out

def line(tag, o):
    s = (f"  {tag:34s} coh {o['coh']:.3f} conc {o['conc']:.3f} | fwd P g/r {o['Pg']:.3f}/{o['Pr']:.3f} ph {o['ph']:+.2f}"
         f" | back R g/r {o['Rg']:.3f}/{o['Rr']:.3f} | ext_g {o['ext_g']:.3f} | norm err {o['err']:.1e}")
    if "Tg" in o: s += f" | target g/r {o['Tg']:.2e}/{o['Tr']:.2e}"
    print(s, flush=True)

if __name__ == "__main__" and "mirror" in sys.argv:
    print("MIRROR re-run with corrected reflected-mode polarization; Gaussian input; ancilla shifts ALL atoms by +5")
    for n, a in ((4, 0.6), (8, 0.6), (8, 0.8), (10, 0.8)):
        pos = lattice(n, a*lam); w = max(1.5*lam, 0.45*n*a*lam)
        for d0 in (-0.5, 0.0, 0.5):
            g = np.full(len(pos), d0); line(f"{n}x{n} a={a}lam w={w/lam:.1f}lam det={d0:+.1f}", case(pos, w, 0, g, g + 5, g + 2))
    sys.exit()

if __name__ == "__main__":
    print("SWITCH / MIRROR: Gaussian input (w = 1.5 lambda unless stated); ancilla shifts ALL atoms by +5 linewidths")
    for n, a in ((4, 0.6), (6, 0.6), (8, 0.6), (8, 0.8)):
        pos = lattice(n, a*lam); w = max(1.5*lam, 0.45*n*a*lam)
        best = None
        for d0 in (-1.5, -1.0, -0.5, 0.0, 0.5, 1.0):
            g = np.full(len(pos), d0); o = case(pos, w, 0, g, g + 5, g + 2)
            if best is None or o["Rg"] > best[1]["Rg"]: best = (d0, o)
        line(f"{n}x{n} array a={a}lam w={w/lam:.1f}lam det={best[0]:+.1f}", best[1])
    print("\nOAM SWITCH on rings (input l=+1, w = sqrt2 R or >= 1.5 lambda); ancilla shifts all atoms")
    for N, d in ((12, 0.4), (16, 0.4), (24, 0.4), (36, 0.4), (24, 0.3)):
        R = d*lam/(2*np.sin(np.pi/N)); pos = ring(N, R); w = max(1.5*lam, np.sqrt(2)*R)
        best = None
        for d0 in (-1.0, -0.5, 0.0, 0.5, 1.0):
            g = np.full(N, d0); o = case(pos, w, 1, g, g + 5, g + 2)
            if best is None or o["conc"] > best[1]["conc"]: best = (d0, o)
        line(f"ring N={N} d={d}lam R={R/lam:.2f}lam det={best[0]:+.1f}", best[1])
    print("\nCONVERTER on rings (input l=+1, target l'=-1); ancilla applies shift 5(1+cos 2phi_j)/2")
    for N, d in ((12, 0.4), (24, 0.4), (36, 0.4)):
        R = d*lam/(2*np.sin(np.pi/N)); pos = ring(N, R); w = max(1.5*lam, np.sqrt(2)*R)
        phis = 2*np.pi*np.arange(N)/N; pat = 5*(1 + np.cos(2*phis))/2
        best = None
        for d0 in (-1.0, -0.5, 0.0, 0.5, 1.0):
            g = np.full(N, d0); o = case(pos, w, 1, g, g + pat, g + 0.4*pat, target=-1)
            if best is None or o["Tr"] > best[1]["Tr"]: best = (d0, o)
        line(f"ring N={N} d={d}lam det={best[0]:+.1f}", best[1])
