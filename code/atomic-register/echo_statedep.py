"""E3-SD: echo with internal-state-dependent hopping (J_R2 = 1.3 J_R1 in both rings), plus ring-A bond +10%.
Uniform vs uneven interaction; same sequence and intended-gate target as echo_combined.py."""
import numpy as np, sys, os
sys.argv = ["x"]
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "echo_combined.py")).read().split("tg = 2*np.pi/0.1")[0])

def build_sd(ratio_R2, bond_err, det, interaction, v=0.1, D=2.0, r=1.5):
    Pint = np.diag([1.0, ratio_R2])                                  # hopping scale per internal state
    HA = ring_hop(r, bond_err); HA[0, 0] += 0                         # detuning added separately below
    HAfull = np.kron(HA, Pint) + det*np.kron(np.diag(I4[0]), I2)
    H0 = np.kron(HAfull, np.eye(8)) + np.kron(np.eye(8), np.kron(ring_hop(1.0), Pint))
    d = np.array([[np.linalg.norm(pos[j] - (pos[k] + [D, 0])) for k in range(N)] for j in range(N)])
    W = d**-6; W *= v/W.mean()
    if interaction == "uniform": W = v*np.ones((N, N))
    V = sum(W[j, k]*np.kron(np.kron(np.diag(I4[j]), P2), np.kron(np.diag(I4[k]), P2)) for j in range(N) for k in range(N))
    S = np.kron(np.diag([(-1.)**j for j in range(N)]), I2); FAB = np.kron(S, np.eye(8)) @ np.kron(np.eye(8), S)
    T1 = np.kron(F, I2); T = np.kron(T1, T1); tr = lambda M: T.conj().T @ M @ T
    one = [2*l + s for l in (0, 2) for s in (0, 1)]; code = [8*a + b for a in one for b in one]
    return tr(H0), tr(V), tr(FAB), code

tg = 2*np.pi/0.1
H0t, Vt, FABt, code = build(0.0, 0.0, "uniform"); Ut = run(H0t, Vt, FABt, tg); C = np.eye(64)[:, code]
for name, args in (("E3-SD uniform V, J_R2=1.3, bond 10%        ", (1.3, 0.1, 0.0, "uniform")),
                   ("E3-SD uniform V, J_R2=1.3, bond 10%, det 3%", (1.3, 0.1, 0.03, "uniform")),
                   ("E4-SD uneven V,  J_R2=1.3, bond 10%        ", (1.3, 0.1, 0.0, "uneven"))):
    H0, V, FAB, _ = build_sd(*args); U = run(H0, V, FAB, tg)
    K = C.T @ U @ C; Wm = C.T @ Ut.conj().T @ U @ C
    Fa = (abs(np.trace(Wm))**2 + np.real(np.trace(Wm.conj().T @ Wm)))/(16*17)
    print(f"{name}: 1-F_avg = {1-Fa:.2e}   worst leakage = {np.linalg.norm(np.eye(16)-K.conj().T@K, 2):.2e}")
