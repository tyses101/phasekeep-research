"""Lie-closure checks for the atomic Tetragon (internal sigma x OAM tau), basis A,B,C,D =
(R1,-1),(R2,-1),(R1,+1),(R2,+1) -> internal index i (R1=0,R2=1), oam index o (-1=0,+1=1), state = 2*o + i? use kron(tau, sigma)."""
import numpy as np, itertools

I2 = np.eye(2); X = np.array([[0,1],[1,0]],complex); Y = np.array([[0,-1j],[1j,0]]); Z = np.diag([1.,-1]).astype(complex)
sp = np.array([[0,0],[1,0]],complex)  # |1><0| : R1->R2 (sigma) or -1->+1 (tau)
k = lambda t, s: np.kron(t, s)          # tau (OAM) (x) sigma (internal)

def lie_dim(gens):
    basis = []
    def add(m):
        m = m - np.trace(m)/4*np.eye(4)
        v = np.concatenate([m.real.ravel(), m.imag.ravel()])
        M = np.array([np.concatenate([b.real.ravel(), b.imag.ravel()]) for b in basis] + [v])
        if np.linalg.matrix_rank(M, tol=1e-9) > len(basis):
            basis.append(m); return True
        return False
    for g in gens: add(1j*g)
    grew = True
    while grew:
        grew = False
        for a, b in itertools.combinations(list(basis), 2):
            if add(a@b - b@a): grew = True
    return len(basis)

mw = [k(I2, X), k(I2, Y), k(I2, Z)]
# confined Raman (continuous ensemble): couples only A=(R1,-1) <-> D=(R2,+1): sigma+ (x) tau+ + h.c., both quadratures
R = k(sp, sp); raman = [R + R.conj().T, 1j*(R - R.conj().T)]
print("MW + confined Raman (A<->D):", lie_dim(mw + raman))
R2 = k(sp, sp.T)  # B<->C diagonal (other pairing)
print("MW + both diagonals:        ", lie_dim(mw + raman + [R2 + R2.conj().T, 1j*(R2 - R2.conj().T)]))
print("MW + Raman + pure OAM flip: ", lie_dim(mw + raman + [k(X, I2)]))

# 4-site ring: site phases phi_j = j*pi/2, OAM basis |l> = sum_j e^{i l phi_j}|j>/2, l mod 4
F = np.array([[np.exp(1j*l*j*np.pi/2)/2 for l in range(4)] for j in range(4)])  # columns l=0..3 (3 == -1)
D = np.diag([(-1)**j for j in range(4)]).astype(complex)                          # staggered pi phase = e^{2i phi_j}
Dl = F.conj().T @ D @ F
code = [3, 1]  # l=-1, l=+1
print("ring: staggered phase in OAM basis, code block:\n", np.round(Dl[np.ix_(code, code)], 6).real)
print("ring: leakage from code to l in {0,2}:", np.round(np.abs(Dl[np.ix_([0, 2], code)]).max(), 9))
