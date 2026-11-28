"""Quick checks of claims made in the #phasekeep-research group (msgs 93-101)."""
import numpy as np
def null_space(A, tol=1e-12):
    u, sv, vh = np.linalg.svd(A); r = int((sv > tol).sum()); return vh[r:].conj().T
rng = np.random.default_rng(1)
N = 4
F = np.array([[np.exp(2j*np.pi*m*j/N)/2 for j in range(N)] for m in range(N)])  # rows = k_m
k = [F[m] for m in range(N)]

def kl_res(Ks, V):
    d = V.shape[1]; r = 0
    for A in Ks:
        for B in Ks:
            X = V.conj().T @ A.conj().T @ B @ V
            r = max(r, np.linalg.norm(X - np.trace(X)/d*np.eye(d)))
    return r

# 1. Ideal ring: J = sum sigma_j on single-excitation manifold -> row vector <vac| = (1,1,1,1)
J = np.ones((1, N), complex)
Vd = np.array(k[1:]).T
print("1. ideal  J V_dark norm:", np.linalg.norm(J @ Vd))

# 2. Amplitude/phase disorder eps on couplings: uncalibrated Fourier code vs calibrated ker(J')
for eps in [1e-3, 1e-2, 1e-1]:
    Jp = (1 + eps*rng.standard_normal(N)) * np.exp(1j*eps*rng.standard_normal(N))
    Jp = Jp[None, :]
    leak = np.linalg.norm(Jp @ Vd)**2 / np.linalg.norm(Jp)**2   # fraction of Gamma seen by dark code
    Vcal = null_space(Jp)
    print(f"2. eps={eps:g}: uncalibrated dark-code max rate/Gamma ~ {leak:.2e};"
          f"  calibrated ker(J') dim={Vcal.shape[1]}, |J'V|={np.linalg.norm(Jp@Vcal):.1e}")

# 3. Any rank-1 collective channel on 4 random positions has a 3-dim exact dark space (no geometry needed)
Jr = (rng.standard_normal(N) + 1j*rng.standard_normal(N))[None, :]
print("3. random-coupling rank-1 channel: dark dim =", null_space(Jr).shape[1])

# 4. Dual rail under COLLECTIVE decay: no-jump branch is non-scalar on the code
dt, G = 1e-3, 1.0
Vdr = np.eye(2)                       # code = {|10>,|01>} inside single-excitation sector
Jdr = np.array([[1, 1]], complex) * np.sqrt(G*dt)
K0 = np.eye(2) - 0.5*Jdr.conj().T @ Jdr
M0 = K0.conj().T @ K0
ev = np.linalg.eigvalsh(M0)
print(f"4. dual rail, collective decay: Delta p_nojump = {ev[-1]-ev[0]:.2e} (= Gamma dt -> not scalar)")

# 5. HOLD on a free-space-like ring: circulant dipole-dipole H splits the dark modes
#    any circulant H (symmetric hopping J1 nn, J2 diag) has k-mode eigenvalues
J1, J2 = 1.0, 0.35
H = np.zeros((N, N))
for j in range(N):
    H[j, (j+1) % N] = H[(j+1) % N, j] = J1
    H[j, (j+2) % N] = J2
Hd = Vd.conj().T @ H @ Vd
print("5. dark-space energies under circulant H_dd:", np.round(np.linalg.eigvalsh(Hd), 3),
      "(not proportional to identity -> HOLD is a known unitary, not identity)")

# 6. Dynamic bright-vector steering = Zeno dragging (no Hamiltonian gap)
#    H_eff = -i Gamma/2 |B(t)><B(t)| - i gamma'/2 I ; B rotates k0 -> k1 over angle pi/2 in time T
def drag(T, Gam, gp, steps=4000):
    psi = k[1].astype(complex).copy()          # dark at t=0, must end as -k0 (dark at t=T)
    dtt = T/steps
    for s in range(steps):
        th = (s+0.5)/steps*np.pi/2
        B = np.cos(th)*k[0] + np.sin(th)*k[1]
        P = np.outer(B, B.conj())
        psi = np.exp(-0.5*gp*dtt) * (np.eye(N) + (np.exp(-0.5*Gam*dtt) - 1)*P) @ psi
    surv = np.vdot(psi, psi).real
    fid = abs(np.vdot(-k[0], psi))**2/surv
    return 1-surv, fid
print("6. Zeno dragging (Gamma=1, gamma'=0): T, loss, 4*theta^2/(Gamma T), cond. fidelity")
for T in [10, 30, 100, 300]:
    loss, fid = drag(T, 1.0, 0.0)
    print(f"   T={T:4d}  loss={loss:.4f}  pred={4*(np.pi/2)**2/T:.4f}  F={fid:.6f}")
print("   with gamma'/Gamma = 1e-3: optimum T* = 2theta/sqrt(G g'), loss_min = 4 theta sqrt(g'/G)")
gp = 1e-3; th = np.pi/2; Ts = 2*th/np.sqrt(gp)
for T in [Ts/3, Ts, 3*Ts]:
    loss, fid = drag(T, 1.0, gp)
    print(f"   T={T:7.1f}  loss={loss:.4f}   (predicted min {4*th*np.sqrt(gp):.4f} at T*={Ts:.1f})")
