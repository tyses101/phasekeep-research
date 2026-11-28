"""Four-site ring, single excitation. Space = site j (4) x internal r (2) = 8 dims.
Ring modes |l> = sum_j e^{i l pi j/2}|j>/2, code = {l=-1,+1} x {R1,R2}.
Checks Lie-algebra dimension of available controls (su(8) = 63; code su(4) = 15)."""
import numpy as np, itertools
I2, I4 = np.eye(2), np.eye(4)
X = np.array([[0, 1], [1, 0]], complex); Y = np.array([[0, -1j], [1j, 0]]); Z = np.diag([1., -1]).astype(complex)
sp = np.array([[0, 0], [1, 0]], complex)
k = np.kron  # site (x) internal

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

mw = [k(I4, X), k(I4, Y), k(I4, Z)]
stag = np.diag([(-1)**j for j in range(4)]).astype(complex)          # e^{2i phi_j}
raman = [k(stag, sp) + k(stag, sp).conj().T, 1j*(k(stag, sp) - k(stag, sp).conj().T)]  # R1->R2 with e^{2i phi}
stag_phase = [k(stag, I2)]
site_diag = [k(np.diag(np.eye(4)[j]).astype(complex), I2) for j in range(4)]           # arbitrary site light shifts
hop = np.zeros((4, 4), complex)
for j in range(4): hop[j, (j+1) % 4] = hop[(j+1) % 4, j] = 1
hop = [k(hop, I2)]

print("A  MW + ring Raman + staggered phase      :", lie_dim(mw + raman + stag_phase, 8))
print("B  A + arbitrary site light shifts        :", lie_dim(mw + raman + site_diag, 8))
print("C  B + nearest-neighbour hopping (exchange):", lie_dim(mw + raman + site_diag + hop, 8), "(su(8)=63)")
