"""Abrupt vs sin^2-shaped inter-ring interaction, same pulse area (same mean conditional phase pi).
Reuses the two-ring model (ratio 1.5). Reports final leakage, worst transient leakage, overlap with target."""
import numpy as np, sys, os
sys.argv = ["x"]
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "two_ring.py")).read().split("import sys\nif len")[0]
exec(src)

def build(r, v, D):
    JA, JB = r, 1.0
    d = np.array([[np.linalg.norm(pos[j] - (pos[k] + [D, 0])) for k in range(N)] for j in range(N)])
    W = d**-6; W *= v/W.mean()
    H0 = np.kron(np.kron(JA*hop, I2), np.eye(8)) + np.kron(np.eye(8), np.kron(JB*hop, I2))
    Vf = sum(W[j, k]*np.kron(np.kron(np.diag(I4[j]), P2), np.kron(np.diag(I4[k]), P2)) for j in range(N) for k in range(N))
    Vm = v*np.kron(np.kron(I4, P2), np.kron(I4, P2))
    T1 = np.kron(F, I2); T = np.kron(T1, T1)
    one = [2*l + s for l in (0, 2) for s in (0, 1)]; code = [8*a + b for a in one for b in one]
    tr = lambda M: T.conj().T @ M @ T
    return tr(H0), tr(Vf), tr(Vm), code

def evolve(H0, V, env, tg, steps, code):
    U = np.eye(64, dtype=complex); dt = tg/steps; worst = 0
    for n in range(steps):
        U = expmh(H0 + env((n+0.5)/steps)*V, dt) @ U
        K = U[np.ix_(code, code)]; worst = max(worst, np.linalg.norm(np.eye(16) - K.conj().T @ K, 2))
    return U, worst

for D, v in ((2, 0.1), (2, 0.05), (4, 0.1)):
    H0, Vf, Vm, code = build(1.5, v, D)
    for name, env, area in (("abrupt", lambda s: 1.0, 1.0), ("sin^2 ", lambda s: np.sin(np.pi*s)**2, 0.5)):
        tg = np.pi/(v*area)
        U, worst = evolve(H0, Vf, env, tg, 600, code); Ut, _ = evolve(H0, Vm, env, tg, 600, code)
        K, Kt = U[np.ix_(code, code)], Ut[np.ix_(code, code)]
        fin = np.linalg.norm(np.eye(16) - K.conj().T @ K, 2)
        print(f"D={D} v/J_B={v} {name}  t={tg:6.1f}/J_B  final leak={fin:.2e}  worst transient={worst:.2e}  overlap={abs(np.trace(Kt.conj().T@K))/16:.5f}")
