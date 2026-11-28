"""REF-01 negative controls. Same one-hot 8-qubit ring as ref01_onehot.py.
Cases: (a) baseline uniform hopping; (b) internal-state-dependent hopping J0 != J1 (prediction: STILL exact,
    because each internal sector keeps commuting layers); (c) local detuning on site 0 (prediction: Trotter
    error appears and converges as steps increase).
Exact reference: independent eigendecomposition of the full Hamiltonian. Circuit: symmetric Trotter B/2 . (A + D) . B/2.
Metrics on the 8-dim single-excitation sector S and the 4-dim code C:
  F_proc(S) = |Tr(U_ex^dag U)|^2/64, F_avg(C) leakage-aware, worst-case code leakage, unitarity error ||U_S^dag U_S - I||."""
import numpy as np
DIM = 256; q = lambda j, r: 2*(j % 4) + r

def xy_ham(a, b):
    H = np.zeros((DIM, DIM))
    for s in range(DIM):
        if (s >> a) & 1 and not (s >> b) & 1:
            t = s ^ (1 << a) ^ (1 << b); H[t, s] = H[s, t] = 1
    return H
def num(a): return np.diag([(s >> a) & 1 for s in range(DIM)]).astype(float)
def expmh(H, t):
    w, V = np.linalg.eigh(H); return (V*np.exp(-1j*w*t)) @ V.conj().T

T = 0.7
S = [1 << q(j, r) for j in range(4) for r in (0, 1)]
def mode(l, r):
    v = np.zeros(DIM, complex)
    for j in range(4): v[1 << q(j, r)] = np.exp(1j*np.pi*l*j/2)/2
    return v
C = np.array([mode(l, r) for l in (0, 2) for r in (0, 1)]).T

def case(J0, J1, delta):
    A = sum(Jr*xy_ham(q(j, r), q(j+1, r)) for j in (0, 2) for r, Jr in ((0, J0), (1, J1)))
    B = sum(Jr*xy_ham(q(j, r), q(j+1, r)) for j in (1, 3) for r, Jr in ((0, J0), (1, J1)))
    D = delta*(num(q(0, 0)) + num(q(0, 1)))
    PS = np.zeros((DIM, 8)); PS[S, range(8)] = 1
    cA, cB = PS.T@A@PS, PS.T@B@PS
    Uex = expmh(A + B + D, T)
    rows = []
    for n in (1, 2, 4, 8, 16, 32):
        step = expmh(B, T/(2*n)) @ expmh(A + D, T/n) @ expmh(B, T/(2*n))
        U = np.linalg.matrix_power(step, n)
        US, UeS = U[np.ix_(S, S)], Uex[np.ix_(S, S)]
        Fp = abs(np.trace(UeS.conj().T @ US))**2/64
        K, Ke = C.conj().T @ U @ C, C.conj().T @ Uex @ C
        Fc = (abs(np.trace(Ke.conj().T @ K))**2 + np.real(np.trace(K.conj().T @ K)))/20
        leak = np.linalg.norm(np.eye(4) - K.conj().T @ K, 2)
        unit = np.linalg.norm(US.conj().T @ US - np.eye(8), 2)
        rows.append((n, Fp, Fc, leak, unit, 4*n + 8*n + 4*n))      # XY gates: B/2, A, B/2 layers (4 each) per step
    return np.linalg.norm(cA@cB - cB@cA), rows

for name, args in (("(a) baseline J0=J1=1", (1, 1, 0)), ("(b) J0=1, J1=1.6", (1, 1.6, 0)), ("(c) site-0 detuning 0.8", (1, 1, 0.8))):
    comm, rows = case(*args)
    print(f"{name}: ||[A,B]|| in single-excitation sector = {comm:.2e}")
    print("   steps | 1-F_proc(S) | 1-F_avg(code) | code leakage | unitarity err | XY gates")
    for n, Fp, Fc, lk, un, g in rows:
        print(f"   {n:5d} | {1-Fp:11.2e} | {1-Fc:13.2e} | {lk:12.2e} | {un:13.1e} | {g}")
