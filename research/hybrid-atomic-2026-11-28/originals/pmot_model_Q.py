"""PMOT quantum version: one photon scattered by an atomic array whose configuration is CONDITIONED on an ancilla
atom held in a superposition (|g> + |r>)/sqrt2  (e.g. a Rydberg ancilla shifting some array atoms, Srakaew-type).

Why this is exact enough to be useful: for ONE photon and array atoms starting in their ground state, single-excitation
scattering equals the linear coupled-dipole response (model C). With the ancilla static during the photon, the joint
output is
        |Psi> = ( |g>|gamma_g> + |r>|gamma_r> ) / sqrt2 ,
where |gamma_x> = incident field + scattered field for configuration x. All atom-light quantities follow from the
overlap O = <gamma_g|gamma_r>:
  - ancilla coherence after the photon leaves (traced out):   |O|         (1 = untouched, 0 = fully measured)
  - ancilla-photon entanglement (concurrence):                 sqrt(1 - |O|^2)
  - conditional mode operation: amplitudes of each branch in detected modes (LG l' = -1, 0, +1, sigma+).
Normalization: the scattered field's real scale kappa and phase phi0 relative to the incident far field are fixed by
photon-number conservation <gamma_x|gamma_x> = 1 for two configurations, and CHECKED on a third configuration and
against the independent extinction formula of model C.
Not included: ancilla decay/blockade errors during the photon, recoil, saturation, real Rb level structure.
"""
import numpy as np, sys, os
from math import factorial
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pmot_model_C import solve, ring, SIG0, ext_fraction   # reuse the validated coupled-dipole solver

lam = 2*np.pi
NTH, NPH = 1600, 64
TH = (np.arange(NTH) + 0.5)*np.pi/NTH; PH = np.linspace(0, 2*np.pi, NPH, endpoint=False)
TT, PP = np.meshgrid(TH, PH, indexing="ij"); DW = (np.sin(TT)*(np.pi/NTH)*(2*np.pi/NPH))
NX, NY, NZ = np.sin(TT)*np.cos(PP), np.sin(TT)*np.sin(PP), np.cos(TT)
EPSP = np.array([1, 1j, 0])/np.sqrt(2)

def inner(a, b):                                   # <a|b> over the sphere, vector fields (..., 3)
    return np.sum(np.conj(a)*b*DW[..., None])

def lg_far(l, w):
    """Paraxial angular spectrum of LG_{0,l} (sigma+), forward hemisphere, unit norm on the sphere grid."""
    s = np.sin(TT); u = (w*s/np.sqrt(2))**abs(l)*np.exp(-(w*s/2)**2)*np.exp(1j*l*PP)*(NZ > 0)
    f = u[..., None]*EPSP
    return f/np.sqrt(np.real(inner(f, f)))

def scat_far(pos, c):
    d = c.reshape(-1, 3)
    ph = np.exp(-1j*(NX[..., None]*pos[:, 0] + NY[..., None]*pos[:, 1] + NZ[..., None]*pos[:, 2]))   # th,ph,N
    D = np.einsum("tpn,nk->tpk", ph, d)
    n = np.stack([NX, NY, NZ], -1)
    return D - n*np.sum(n*D, -1, keepdims=True)

def calibrate(fin, A1, A2, ext1):
    """Scale from the independent model-C extinction of config 1 (sqrt(kappa) = sqrt(ext1 / ||A1||^2)); phase phi0 from
    photon-number conservation of config 1 (two roots), choosing the root that also conserves config 2."""
    X1, X2 = inner(fin, A1), inner(fin, A2); N1, N2 = np.real(inner(A1, A1)), np.real(inner(A2, A2))
    sk = np.sqrt(ext1/N1)
    # need 2 sk Re(e^{i phi} X1) = -ext1  ->  cos(phi + arg X1) = -ext1 / (2 sk |X1|)
    cval = np.clip(-ext1/(2*sk*abs(X1)), -1, 1); base = np.arccos(cval)
    roots = [base - np.angle(X1), -base - np.angle(X1)]
    err = [abs(2*sk*np.real(np.exp(1j*p)*X2) + sk*sk*N2) for p in roots]
    return sk, roots[int(np.argmin(err))], abs(cval) <= 1

def run(name, pos, w, l_in, det_g, det_r, det_check):
    fin = lg_far(l_in, w)
    sols = {k: solve(pos, l_in, w, d) for k, d in (("g", det_g), ("r", det_r), ("chk", det_check))}
    A = {k: scat_far(pos, c) for k, (E, c) in sols.items()}
    E1, c1 = solve(np.array([[0, 0, 0.0]]), 0, w, [0.0]); n1 = ext_fraction(E1, c1)
    ext = {k: SIG0*2/(np.pi*w*w)*ext_fraction(*sols[k])/n1 for k in sols}
    sk, phi0, ok = calibrate(fin, A["g"], A["r"], ext["g"])
    gam = {k: fin + sk*np.exp(1j*phi0)*A[k] for k in A}
    norms = {k: np.real(inner(gam[k], gam[k])) for k in gam}
    scp = {k: sk**2*np.real(inner(A[k], A[k])) for k in A}
    O = inner(gam["g"], gam["r"])
    modes = {lp: lg_far(lp, w) for lp in (-1, 0, 1)}
    amp = {(k, lp): inner(modes[lp], gam[k]) for k in ("g", "r") for lp in modes}
    print(f"\n=== {name}: input LG l={l_in:+d}")
    print(f"  checks: <gamma|gamma> g={norms['g']:.4f} r={norms['r']:.4f} check-config={norms['chk']:.4f} (must be 1);"
          f" scattered power vs model-C extinction: g {scp['g']:.4f}/{ext['g']:.4f}, r {scp['r']:.4f}/{ext['r']:.4f}, chk {scp['chk']:.4f}/{ext['chk']:.4f}")
    print(f"  overlap O = {abs(O):.4f} (phase {np.angle(O):+.3f} rad) -> ancilla coherence {abs(O):.4f}, "
          f"ancilla-photon concurrence {np.sqrt(max(0, 1-abs(O)**2)):.4f}")
    for lp in (-1, 0, 1):
        ag, ar = amp[("g", lp)], amp[("r", lp)]
        print(f"  detected mode LG{lp:+d}: P(g-branch) {abs(ag)**2:.4f}  P(r-branch) {abs(ar)**2:.4f}  "
              f"relative phase r/g {np.angle(ar/ag) if abs(ag) > 1e-9 else float('nan'):+.3f} rad")

if __name__ == "__main__":
    sq = ring(4, 0.35*lam); r8 = ring(8, 0.4*lam/(2*np.sin(np.pi/8))); w = 1.5*lam
    z4, z8 = np.zeros(4), np.zeros(8)
    run("SWITCH, sub-wavelength square, ancilla shifts all atoms by 5 linewidths", sq, w, 0, z4, np.full(4, 5.0), np.full(4, 2.0))
    run("SWITCH, 8-atom ring, ancilla shifts all atoms", r8, w, 0, z8, np.full(8, 5.0), np.full(8, 2.0))
    run("CONVERTER, sub-wavelength square, ancilla shifts atoms 2 and 4", sq, w, 1, z4, np.array([0, 5, 0, 5.0]), np.array([0, 2, 0, 2.0]))
    run("CONVERTER, 8-atom ring, ancilla shifts atoms 2,4,6,8 (alternate)", r8, w, 1, z8, np.array([0, 5]*4, float), np.array([0, 2]*4, float))
