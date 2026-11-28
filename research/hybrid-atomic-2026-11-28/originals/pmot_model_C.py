"""PMOT model C: coupled-dipole (vector) scattering of structured light by small atomic arrays.

Physics (linear, weak-drive regime; this is CLASSICAL coherent scattering, equivalent to a phased array of
coupled dipoles -- single-photon, saturation and atom-light entanglement effects are outside this model):
  - Atoms: isotropic J=0 -> J=1 transitions (3 dipole components), linewidth Gamma0 = 1, units k = 1 (lambda = 2 pi).
  - Dipole-dipole coupling (Asenjo-Garcia et al., PRX 2017 form):  V_jl = -(3 pi) p.G0(r_jl).p  with
      G0(r) = e^{ir}/(4 pi r^3) [ (r^2 + i r - 1) I + (3 - 3 i r - r^2) rr ]          (k = 1, Gamma0 = 1)
  - Steady state:  [ (delta_j + i/2) 1 - V ] c = -E_in(r_j)   (per-atom detuning delta_j, in units of Gamma0)
  - Incident field at the waist plane: circular sigma+ polarization, Laguerre-Gauss mode LG_{0,l}, unit power.
  - Extinguished fraction  f_ext = sigma0 * sum_j Im(E_in*(r_j) . c_j) / norm, calibrated so that ONE isolated
    resonant atom on the axis of a Gaussian beam gives sigma0 * I_peak (sigma0 = 3 lambda^2 / 2 pi).
  - Scattered far field  E_sc(n) ~ (1 - n n) . sum_j c_j e^{-i n.r_j}; inside a forward cone of numerical aperture NA it
    is split into circular components s = +-1 (relative to z) and azimuthal harmonics m; J_z = s + m is reported.
Geometry symmetry rule (DERIVED): with N-fold rotational symmetry, J_z is conserved modulo N.
"""
import numpy as np
from math import factorial

def green(r):
    d = np.linalg.norm(r); n = r/d
    return np.exp(1j*d)/(4*np.pi*d**3)*((d*d + 1j*d - 1)*np.eye(3) + (3 - 3j*d - d*d)*np.outer(n, n))

def lg(l, w, x, y):
    rr2 = x*x + y*y; phi = np.arctan2(y, x)
    C = np.sqrt(2/(np.pi*w*w*factorial(abs(l))))
    return C*(np.sqrt(2*rr2)/w)**abs(l)*np.exp(-rr2/(w*w))*np.exp(1j*l*phi)

EPS = np.array([1, 1j, 0])/np.sqrt(2)          # sigma+ (relative to +z)
SIG0 = 3*(2*np.pi)**2/(2*np.pi)                 # 3 lambda^2 / 2pi in units k = 1

def solve(pos, l, w, det):
    N = len(pos); M = np.zeros((3*N, 3*N), complex)
    for j in range(N):
        M[3*j:3*j+3, 3*j:3*j+3] = (det[j] + 0.5j)*np.eye(3)
        for k in range(N):
            if k != j: M[3*j:3*j+3, 3*k:3*k+3] = -(-(3*np.pi)*green(pos[j] - pos[k]))
    E = np.concatenate([lg(l, w, p[0], p[1])*EPS for p in pos])
    c = np.linalg.solve(M, -E)
    return E, c

def ext_fraction(E, c):
    return np.sum(np.imag(np.conj(E)*c))

def far_field_modes(pos, c, NA, nth=120, nph=128):
    th = (np.arange(nth) + 0.5)*np.pi/nth; ph = np.linspace(0, 2*np.pi, nph, endpoint=False)
    d = c.reshape(-1, 3); tot = 0; cone = {}
    for t in th:
        wt = np.sin(t)*np.pi/nth
        n = np.stack([np.sin(t)*np.cos(ph), np.sin(t)*np.sin(ph), np.cos(t)*np.ones_like(ph)], 1)
        phase = np.exp(-1j*(n @ pos.T))                      # nph x N
        D = phase @ d                                        # nph x 3
        Et = D - n*np.sum(n*D, 1, keepdims=True)             # transverse part
        tot += wt*np.sum(np.abs(Et)**2)/nph
        if t <= np.arcsin(NA):
            for s, e in ((+1, np.array([1, -1j, 0])/np.sqrt(2)), (-1, np.array([1, 1j, 0])/np.sqrt(2))):
                comp = Et @ e                                # projection onto sigma_s (paraxial approx.)
                a = np.fft.fft(comp)/nph; m = np.fft.fftfreq(nph, 1/nph).astype(int)
                for mm, aa in zip(m, a):
                    cone[(s, mm)] = cone.get((s, mm), 0) + wt*abs(aa)**2
    c_tot = sum(cone.values())
    if tot < 1e-30 or c_tot < 1e-30:
        return 0.0, []
    top = sorted(cone.items(), key=lambda x: -x[1])[:3]
    return c_tot/tot, [(s, m, s + m, v/c_tot) for (s, m), v in top]

def ring(N, R):
    return np.array([[R*np.cos(2*np.pi*j/N), R*np.sin(2*np.pi*j/N), 0.0] for j in range(N)])

lam = 2*np.pi
def report(name, pos, w, NA=0.5, configs=None):
    configs = configs or {"all resonant": np.zeros(len(pos))}
    # single-atom calibration: one resonant atom at the centre of a Gaussian of the same waist
    E1, c1 = solve(np.array([[0, 0, 0.0]]), 0, w, [0.0]); norm1 = ext_fraction(E1, c1)
    I_peak = 2/(np.pi*w*w)
    print(f"\n=== {name}: {len(pos)} atoms, beam waist {w/lam:.2f} lambda; single atom on Gaussian axis extinguishes {SIG0*I_peak:.3f}")
    for cname, det in configs.items():
        for l in (-1, 0, 1):
            E, c = solve(pos, l, w, det)
            f = SIG0*I_peak*ext_fraction(E, c)/norm1
            frac, top = far_field_modes(pos, c, NA)
            tops = ", ".join(f"(s{s:+d},m{m:+d}; Jz{jz:+d}) {sh:.2f}" for s, m, jz, sh in top)
            print(f"  {cname:22s} input l={l:+d} (Jz={l+1:+d}): extinguished {f:6.3f} | scattered into NA{NA} cone {frac:5.3f} | top: {tops}")

if __name__ == "__main__":
    # validation: single isolated atom, sigma+ Gaussian -> scattered light must be pure s=+1, m=0 near axis
    report("VALIDATION single atom", np.array([[0, 0, 0.0]]), 2.0*lam)
    R_tw = 2.5*lam                                      # tweezer-scale square (side ~3.5 lambda ~ 2.8 um at 780 nm)
    report("Tweezer-scale square (R = 2.5 lambda)", ring(4, R_tw), np.sqrt(2)*R_tw,
           configs={"all resonant": np.zeros(4), "atoms 2,4 shifted +5": np.array([0, 5, 0, 5.0])})
    # Paraxial validity: beam waists are kept >= 1.5 lambda (an OAM beam cannot be focused onto a sub-wavelength ring).
    R_sw = 0.35*lam                                     # sub-wavelength square
    report("Sub-wavelength square (R = 0.35 lambda), paraxial beam w = 1.5 lambda", ring(4, R_sw), 1.5*lam,
           configs={"all resonant": np.zeros(4), "atoms 2,4 shifted +5": np.array([0, 5, 0, 5.0]),
                    "all shifted +5": np.full(4, 5.0)})
    R8 = 0.4*lam/(2*np.sin(np.pi/8))                    # 8-atom ring, nearest spacing 0.4 lambda
    report("Sub-wavelength 8-atom ring (spacing 0.4 lambda), w = 1.5 lambda", ring(8, R8), 1.5*lam,
           configs={"all resonant": np.zeros(8), "alternate atoms shifted +5": np.array([0, 5]*4, float)})
    # Convergence of the far-field integration (one case, doubled grids)
    pos = ring(4, R_sw); E, c = solve(pos, 1, 1.5*lam, np.array([0, 5, 0, 5.0]))
    print("\nconvergence (sub-wavelength square, atoms 2,4 shifted, l=+1):",
          far_field_modes(pos, c, 0.5)[1][:2], "vs doubled grid:", far_field_modes(pos, c, 0.5, nth=240, nph=256)[1][:2])
