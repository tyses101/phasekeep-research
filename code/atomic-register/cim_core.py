"""Shared two-ring model for P2-CIM / E5 / E6 (NumPy only).
Two four-site rings, one excitation each, internal {R1,R2}; 64-dim; zero flux; code = ring modes {0,2} x internal.
Hopping J_A = r (default 1.5), J_B = 1. Inter-ring interaction acts only on R2-R2 pairs:
    V(alpha) = Vbar + alpha*(V_phys - Vbar),   V_phys ~ 1/d^6 (side-by-side squares, centre spacing D), mean = v.
Imperfections: bond (3,0) strength error eps on ring A or B; site-0 detuning delta on ring A.
Gate: two sin^2 segments (total area pi for the mean interaction), ideal or finite staggered flips on both rings.
Target: intended gate = same sequence, no errors, alpha = 0 (pure internal controlled phase on the code).
All operators are returned in the (mode, internal) x (mode, internal) basis."""
import numpy as np

N = 4
I2, I4 = np.eye(2), np.eye(4)
P2 = np.diag([0., 1.])
HOP = np.zeros((N, N))
for j in range(N): HOP[j, (j+1) % N] = HOP[(j+1) % N, j] = 1
POS = [np.array([np.cos(np.pi/4+j*np.pi/2), np.sin(np.pi/4+j*np.pi/2)])/np.sqrt(2) for j in range(N)]
F = np.array([[np.exp(2j*np.pi*l*j/N)/2 for l in range(N)] for j in range(N)])
T1 = np.kron(F, I2); T = np.kron(T1, T1)
ONE = [2*l + s for l in (0, 2) for s in (0, 1)]
CODE = [8*a + b for a in ONE for b in ONE]
C = np.eye(64)[:, CODE]
tr = lambda M: T.conj().T @ M @ T
RA = lambda M: np.kron(np.kron(M, I2), np.eye(8))      # site operator on ring A
RB = lambda M: np.kron(np.eye(8), np.kron(M, I2))      # site operator on ring B

def expmh(H, t):
    w, V = np.linalg.eigh(H); return (V*np.exp(-1j*w*t)) @ V.conj().T

BOND = np.zeros((N, N)); BOND[3, 0] = BOND[0, 3] = 1          # bond (3,0) perturbation (unit)
SITE0 = np.diag(I4[0])
ODD = np.diag([j % 2 for j in range(N)]).astype(float)
S = np.diag([(-1.)**j for j in range(N)])

def operators(r=1.5, v=0.1, D=2.0):
    d = np.array([[np.linalg.norm(POS[j] - (POS[k] + [D, 0])) for k in range(N)] for j in range(N)])
    W = d**-6; W *= v/W.mean()
    Vop = lambda Wm: sum(Wm[j, k]*np.kron(np.kron(np.diag(I4[j]), P2), np.kron(np.diag(I4[k]), P2)) for j in range(N) for k in range(N))
    ops = dict(
        H0=tr(RA(r*HOP) + RB(HOP)),
        bondA=tr(RA(r*BOND)), bondB=tr(RB(BOND)),          # relative bond error eps multiplies the bond's own J
        siteA=tr(RA(SITE0)),
        Vbar=tr(Vop(v*np.ones((N, N)))), Vdev=tr(Vop(W - v)),
        oddA=tr(RA(ODD)), oddB=tr(RB(ODD)),
        FAB=tr(RA(S) @ RB(S)))
    return ops

def gate(ops, alpha=0., epsA=0., epsB=0., delta=0., steps=600, v=0.1,
         eps_fn=None, flip=None, r_on=0.0):
    """eps_fn(t, tg) -> (epsA, epsB) for time-dependent drift (overrides static eps).
    flip: None (ideal) or callable(ops, H_static_fn, r_on, alpha) -> (U_flip, tau, extra_area).
    r_on: fraction of the interaction left on during finite flips (its area is compensated in the segments)."""
    V = ops["Vbar"] + alpha*ops["Vdev"]
    Hs = lambda t, tg: ops["H0"] + delta*ops["siteA"] + \
        (lambda e: e[0]*ops["bondA"] + e[1]*ops["bondB"])(eps_fn(t, tg) if eps_fn else (epsA, epsB))
    tg = 2*np.pi/v
    tau, extra = 0.0, 0.0
    Uf = ops["FAB"]
    if flip is not None:
        Uf, tau, extra = flip(ops, Hs, r_on, alpha, tg)
    peak = (np.pi - extra)*2/tg                                  # sin^2 area per unit peak = tg/2
    U = np.eye(64, dtype=complex); m = steps//2; dt = (tg/2)/m; t = 0.0
    for seg in range(2):
        for n in range(m):
            U = expmh(Hs(t + dt/2, tg) + (peak/v)*np.sin(np.pi*(n+0.5)/m)**2*V, dt) @ U
            t += dt
        U = Uf @ U
    return U, tg + 2*tau

def metrics(U, Ut):
    K = C.T @ U @ C; W = C.T @ Ut.conj().T @ U @ C
    F = (abs(np.trace(W))**2 + np.real(np.trace(W.conj().T @ W)))/(16*17)
    return 1 - F, np.linalg.norm(np.eye(16) - K.conj().T @ K, 2)
