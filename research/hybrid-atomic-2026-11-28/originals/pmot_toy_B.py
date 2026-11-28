"""PMOT toy model B (scalar, NOT a vector-dipole or scattering model).
Four identical point emitters at r_j = R(cos(j pi/2), sin(j pi/2), 0), collective amplitudes c_j = e^{i q j pi/2}/2.
Far field A(theta, phi) ~ sum_j c_j exp(-i k r_j . khat). Decompose each polar ring into azimuthal harmonics m.
Reports, per q and R/lambda:
  - fraction of total emitted power (whole sphere) inside a collection cone of numerical aperture NA about +z
  - inside the cone: the share of the strongest m, and the top three m with their shares
Analytic expectation (DERIVED, Jacobi-Anger): only m = q (mod 4) appear, weighted by J_m(k R sin theta)."""
import numpy as np

def harmonics(q, R_over_lam, theta):
    phi = np.linspace(0, 2*np.pi, 256, endpoint=False)
    kR = 2*np.pi*R_over_lam
    A = sum(np.exp(1j*q*j*np.pi/2)/2*np.exp(-1j*kR*np.sin(theta)*np.cos(phi - j*np.pi/2)) for j in range(4))
    a = np.fft.fft(A)/len(phi)                 # coefficient of e^{i m phi}, m = index (wrapped)
    m = np.fft.fftfreq(len(phi), 1/len(phi)).astype(int)
    return m, np.abs(a)**2

def run(q, R_over_lam, NA, nth=2000):
    th = (np.arange(nth) + 0.5)*np.pi/nth
    w = np.sin(th)*np.pi/nth
    tot = 0; coll = {}
    for t, wt in zip(th, w):
        m, p = harmonics(q, R_over_lam, t)
        tot += wt*p.sum()
        if t <= np.arcsin(NA):
            for mm, pp in zip(m, p):
                if pp > 1e-15: coll[mm] = coll.get(mm, 0) + wt*pp
    c = sum(coll.values())
    top = sorted(coll.items(), key=lambda x: -x[1])[:3]
    return c/tot, [(mm, v/c) for mm, v in top]

print("q  R/lambda  NA   collected   top azimuthal modes in the cone (m: share)")
for q in (0, 1, 2, 3):
    for R in (0.1, 0.25, 0.5, 1.0, 2.5):
        for NA in (0.5,):
            f, top = run(q, R, NA)
            print(f"{q}  {R:5.2f}    {NA:.1f}  {f:8.3f}    " + ", ".join(f"m={mm:+d}: {s:.3f}" for mm, s in top))
