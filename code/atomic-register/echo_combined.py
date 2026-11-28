"""Combined-error echo tests E1-E4 on the two-ring model (64-dim, ratio J_A/J_B = 1.5, D=2, peak v=0.1).
Errors on ring A: bond (3,0) strength +10%, optional site-0 detuning 3% of J_B.
Interaction: off / uniform (mean only) / uneven (1/d^6). Two sin^2 segments, ideal instantaneous A+B flips.
Target = INTENDED gate: same sequence, no errors, uniform interaction (= clean internal controlled phase).
Metrics on the 16-dim code: leakage-aware F_avg via W = C^dag U_target^dag U C, and worst-case leakage."""
import numpy as np, sys, os
sys.argv = ["x"]
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "two_ring.py")).read().split("import sys\nif len")[0])

def ring_hop(J, bond_err=0.0):
    H = J*hop.astype(complex)
    H[3, 0] *= 1 + bond_err; H[0, 3] *= 1 + bond_err
    return H

def build(bond_err, det, interaction, v=0.1, D=2.0, r=1.5):
    HA = ring_hop(r, bond_err); HA[0, 0] += det
    H0 = np.kron(np.kron(HA, I2), np.eye(8)) + np.kron(np.eye(8), np.kron(ring_hop(1.0), I2))
    d = np.array([[np.linalg.norm(pos[j] - (pos[k] + [D, 0])) for k in range(N)] for j in range(N)])
    W = d**-6; W *= v/W.mean()
    if interaction == "off": W = 0*W
    if interaction == "uniform": W = v*np.ones((N, N))
    V = sum(W[j, k]*np.kron(np.kron(np.diag(I4[j]), P2), np.kron(np.diag(I4[k]), P2)) for j in range(N) for k in range(N))
    S = np.kron(np.diag([(-1.)**j for j in range(N)]), I2); FAB = np.kron(S, np.eye(8)) @ np.kron(np.eye(8), S)
    T1 = np.kron(F, I2); T = np.kron(T1, T1); tr = lambda M: T.conj().T @ M @ T
    one = [2*l + s for l in (0, 2) for s in (0, 1)]; code = [8*a + b for a in one for b in one]
    return tr(H0), tr(V), tr(FAB), code

def run(H0, V, FAB, tg, steps=600):
    U = np.eye(64, dtype=complex); m = steps//2; dt = (tg/2)/m
    for _ in range(2):
        for n in range(m):
            U = expmh(H0 + np.sin(np.pi*(n+0.5)/m)**2*V, dt) @ U
        U = FAB @ U
    return U

tg = 2*np.pi/0.1
H0t, Vt, FABt, code = build(0.0, 0.0, "uniform")
Ut = run(H0t, Vt, FABt, tg)
C = np.eye(64)[:, code]
print("target check: target is exactly diagonal phase on code?", np.allclose(np.abs(C.T@Ut@C), np.diag(np.abs(np.diag(C.T@Ut@C))), atol=1e-9))
cases = [("E0 no errors, uniform V      ", 0.0, 0.00, "uniform"),
         ("E1 bond 10%, V off           ", 0.1, 0.00, "off"),
         ("E1b bond 10%, uniform V      ", 0.1, 0.00, "uniform"),
         ("E2 bond 10% + det 3%, V off  ", 0.1, 0.03, "off"),
         ("E3 bond 10% + det 3%, uniform", 0.1, 0.03, "uniform"),
         ("E4 bond 10% + det 3%, uneven ", 0.1, 0.03, "uneven"),
         ("ref: no errors, uneven V     ", 0.0, 0.00, "uneven")]
for name, be, de, it in cases:
    H0, V, FAB, _ = build(be, de, it)
    U = run(H0, V, FAB, tg)
    Utar = Ut if it != "off" else run(H0t, 0*Vt, FABt, tg)
    K = C.T @ U @ C; Wm = C.T @ Utar.conj().T @ U @ C
    Fa = (abs(np.trace(Wm))**2 + np.real(np.trace(Wm.conj().T @ Wm)))/(16*17)
    print(f"{name}: 1-F_avg = {1-Fa:.2e}   worst leakage = {np.linalg.norm(np.eye(16)-K.conj().T@K, 2):.2e}")
