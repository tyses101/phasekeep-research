"""Robustness of quadratic confinement for the Raman A<->D pulse.
Basis: internal r in {0,1} x odd l in [-L..L]. Raman couples (0,l)<->(1,l+2), magnitude 1. H_conf = Delta*l^2.
Reports, over pulse durations t in [0.9,1.1]*pi/2: worst-case leakage (spectral norm of I-K^dag K),
A->D transfer, and spectator phase of B and C relative to the ideal (identity) action."""
import numpy as np

def expmh(H, t):
    w, V = np.linalg.eigh(H); return (V * np.exp(-1j*w*t)) @ V.conj().T

def model(L, delta):
    ells = list(range(-L, L+1, 2))
    basis = [(r, l) for r in (0, 1) for l in ells]; idx = {s: i for i, s in enumerate(basis)}
    H = np.diag([delta*l*l for r, l in basis]).astype(complex)
    for l in ells:
        if l+2 in ells: a, b = idx[0, l], idx[1, l+2]; H[a, b] = H[b, a] = 1
    code = [idx[s] for s in [(0, -1), (1, -1), (0, 1), (1, 1)]]
    return H, code

for L in (3, 7):
    print(f"--- truncation |l| <= {L}")
    for delta in (5, 20, 100):
        H, code = model(L, delta)
        worst, phB, phC, tr = 0, 0, 0, 1
        for t in np.linspace(0.9, 1.1, 401)*np.pi/2:
            U = expmh(H, t); K = U[np.ix_(code, code)]
            worst = max(worst, np.linalg.norm(np.eye(4)-K.conj().T@K, 2))
        U = expmh(H, np.pi/2); K = U[np.ix_(code, code)]
        ref = np.exp(-1j*delta*1*np.pi/2)          # common Delta*l^2 phase for |l|=1
        phB = np.angle(K[1, 1]/ref); phC = np.angle(K[2, 2]/ref)
        print(f"Delta={delta:4d}  worst leakage over t+-10%: {worst:.2e}  envelope 1/(1+16D^2): {1/(1+16*delta**2):.2e}"
              f"  A->D: {abs(K[3,0])**2:.6f}  spectator phase B,C: {phB:+.4f},{phC:+.4f} rad  (est (pi/2)/(8D)={np.pi/2/(8*delta):.4f})")
