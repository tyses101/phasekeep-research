"""Gauge check for the 4-site ring with bond phase phi (total flux 4*phi).
For code modes l=+1,-1: energy (2J cos(pi l/2 - phi)), physical ring current <I> (gauge-invariant),
and Lie dimension of the code control set (MW, hopping, staggered phase, ring Raman)."""
import numpy as np, itertools
I2 = np.eye(2); X = np.array([[0, 1], [1, 0]], complex); Y = np.array([[0, -1j], [1j, 0]]); Z = np.diag([1., -1]).astype(complex)
sp = np.array([[0, 0], [1, 0]], complex); N = 4

def lie_dim(gens, n):
    basis, vecs = [], []
    def add(m):
        m = m - np.trace(m)/n*np.eye(n); v = np.concatenate([m.real.ravel(), m.imag.ravel()])
        if np.linalg.matrix_rank(np.array(vecs + [v]), tol=1e-8) > len(vecs): basis.append(m); vecs.append(v); return True
        return False
    for g in gens: add(1j*g)
    grew = True
    while grew:
        grew = False
        for a, b in itertools.combinations(list(basis), 2):
            if add(a@b - b@a): grew = True
    return len(basis)

F = np.array([[np.exp(2j*np.pi*l*j/N)/2 for l in range(N)] for j in range(N)])
stag = np.diag([(-1.)**j for j in range(N)]).astype(complex)
for phi in (0, np.pi/4, np.pi/2):
    H = np.zeros((N, N), complex); Cur = np.zeros((N, N), complex)
    for j in range(N):
        H[(j+1) % N, j] = np.exp(1j*phi); H[j, (j+1) % N] = np.exp(-1j*phi)
        Cur[(j+1) % N, j] += 1j*np.exp(1j*phi)/N; Cur[j, (j+1) % N] += -1j*np.exp(-1j*phi)/N   # mean bond current
    E = [np.real(F[:, l].conj() @ H @ F[:, l]) for l in (1, 3)]
    I = [np.real(F[:, l].conj() @ Cur @ F[:, l]) for l in (1, 3)]
    gens = [np.kron(np.eye(N), P) for P in (X, Y, Z)] + [np.kron(H, I2), np.kron(stag, I2)]
    Rm = np.kron(stag, sp); gens += [Rm + Rm.conj().T, 1j*(Rm - Rm.conj().T)]
    T = np.kron(F, I2); code = [2, 3, 6, 7]
    dim = lie_dim([(T.conj().T @ g @ T)[np.ix_(code, code)] for g in gens], 4)
    print(f"phi={phi:.4f} (flux {4*phi/np.pi:.0f}pi): E(+1),E(-1)={E[0]:+.3f},{E[1]:+.3f}  current(+1),(-1)={I[0]:+.3f},{I[1]:+.3f}  code Lie dim={dim}")
