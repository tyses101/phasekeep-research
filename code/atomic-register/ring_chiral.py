"""Chiral hopping on an N-site ring, single excitation x internal {R1,R2}.
Checks: (1) chiral energies vs 2J cos(pi l/2 - phi) for N=4; (2) whether every generator leaves the
code {l=-1,+1} x {R1,R2} invariant; (3) Lie dimension on the code (su(4)=15); (4) N=8 closure of the staggered flip."""
import numpy as np, itertools
I2 = np.eye(2); X = np.array([[0, 1], [1, 0]], complex); Y = np.array([[0, -1j], [1j, 0]]); Z = np.diag([1., -1]).astype(complex)
sp = np.array([[0, 0], [1, 0]], complex)

def lie_dim(gens, n):
    basis, vecs = [], []
    def add(m):
        m = m - np.trace(m)/n*np.eye(n)
        v = np.concatenate([m.real.ravel(), m.imag.ravel()])
        if np.linalg.matrix_rank(np.array(vecs + [v]), tol=1e-8) > len(vecs):
            basis.append(m); vecs.append(v); return True
        return False
    for g in gens: add(1j*g)
    grew = True
    while grew:
        grew = False
        for a, b in itertools.combinations(list(basis), 2):
            if add(a@b - b@a): grew = True
    return len(basis)

def ring(N, phi=np.pi/2, J=1.0):
    F = np.array([[np.exp(2j*np.pi*l*j/N)/np.sqrt(N) for l in range(N)] for j in range(N)])  # site j, mode l (mod N)
    H = np.zeros((N, N), complex)
    for j in range(N): H[(j+1) % N, j] = J*np.exp(1j*phi); H[j, (j+1) % N] = J*np.exp(-1j*phi)
    stag = np.diag([np.exp(2j*2*np.pi*j/N) for j in range(N)])  # e^{2 i phi_j}: shift l by +2
    return F, H, stag

N = 4; F, Hc, stag = ring(N)
E = np.real(np.diag(F.conj().T @ Hc @ F))
print("N=4 chiral energies (l=0..3):", np.round(E, 6), " formula:", np.round([2*np.cos(np.pi*l/2 - np.pi/2) for l in range(4)], 6))
gens = [np.kron(np.eye(N), P) for P in (X, Y, Z)]                       # microwave
gens += [np.kron(Hc, I2)]                                                # chiral hopping
gens += [np.kron(stag, I2)]                                              # staggered phase  (Hermitian here: (-1)^j)
Rm = np.kron(stag, sp); gens += [Rm + Rm.conj().T, 1j*(Rm - Rm.conj().T)]  # ring Raman R1->R2 with l+2
T = np.kron(F, I2)                                                       # to (mode, internal) basis
code = [2*3, 2*3+1, 2*1, 2*1+1]                                          # l=-1(=3) and l=+1, both internal
out = [i for i in range(2*N) if i not in code]
gm = [T.conj().T @ g @ T for g in gens]
print("max code->outside coupling over generators:", max(np.abs(g[np.ix_(out, code)]).max() for g in gm))
print("Lie dimension on code (su(4)=15):", lie_dim([g[np.ix_(code, code)] for g in gm], 4))

N = 8; F, Hc, stag = ring(N)
S = F.conj().T @ stag @ F
print("N=8: staggered/Raman shift maps l=+1 to l =", int(np.argmax(np.abs(S[:, 1]))), "(code is l=1 and l=7)")
