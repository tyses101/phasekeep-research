"""Ring-mode echo: split the sin^2 inter-ring pulse into segments separated by ideal, instantaneous
staggered-phase flips (local, exact ring-mode flips 0<->2 on ring A and/or B).
Target = the identical sequence with the interaction replaced by its uniform mean.
Reports final leakage and leakage-aware average gate fidelity (d=16)."""
import numpy as np, sys, os
sys.argv = ["x"]
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "two_ring.py")).read().split("import sys\nif len")[0])

def build(r, v, D):
    d = np.array([[np.linalg.norm(pos[j] - (pos[k] + [D, 0])) for k in range(N)] for j in range(N)])
    W = d**-6; W *= v/W.mean()
    H0 = np.kron(np.kron(r*hop, I2), np.eye(8)) + np.kron(np.eye(8), np.kron(hop, I2))
    Vf = sum(W[j, k]*np.kron(np.kron(np.diag(I4[j]), P2), np.kron(np.diag(I4[k]), P2)) for j in range(N) for k in range(N))
    Vm = v*np.kron(np.kron(I4, P2), np.kron(I4, P2))
    S = np.kron(np.diag([(-1.)**j for j in range(N)]), I2)              # staggered phase on one ring
    FA, FB = np.kron(S, np.eye(8)), np.kron(np.eye(8), S)
    T1 = np.kron(F, I2); T = np.kron(T1, T1); tr = lambda M: T.conj().T @ M @ T
    one = [2*l + s for l in (0, 2) for s in (0, 1)]; code = [8*a + b for a in one for b in one]
    return tr(H0), tr(Vf), tr(Vm), tr(FA), tr(FB), code

def run(H0, V, flips, tg, steps=600):
    """flips: list of flip operators applied after each segment (len = number of segments)."""
    U = np.eye(64, dtype=complex); nseg = len(flips); ts = tg/nseg; dt = ts/(steps//nseg)
    for f in flips:
        for n in range(steps//nseg):
            s = (n + 0.5)/(steps//nseg)
            U = expmh(H0 + np.sin(np.pi*s)**2*V, dt) @ U
        U = f @ U
    return U

def favg(K, Kt, d=16):
    return (abs(np.trace(Kt.conj().T @ K))**2 + np.real(np.trace(K.conj().T @ K)))/(d*(d+1))

for D, v in ((2, 0.1), (2, 0.05), (4, 0.1)):
    H0, Vf, Vm, FA, FB, code = build(1.5, v, D)
    I = np.eye(64); AB = FA @ FB
    seqs = {"single sin^2      ": [I],
            "2-seg, flip A+B   ": [AB, AB],
            "4-seg, A,B,A,B    ": [FA, FB, FA, FB]}
    for name, fl in seqs.items():
        tg = 2*np.pi/v                                                 # same total area as single sin^2 (area 1/2)
        K = run(H0, Vf, fl, tg)[np.ix_(code, code)]; Kt = run(H0, Vm, fl, tg)[np.ix_(code, code)]
        leak = np.linalg.norm(np.eye(16) - K.conj().T @ K, 2)
        print(f"D={D} v={v}  {name} final leak={leak:.2e}  F_avg={100*favg(K, Kt):.5f}%")
