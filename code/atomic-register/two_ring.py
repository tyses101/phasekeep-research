"""Two four-site rings, one excitation each, internal {R1,R2}. Joint dim (4*2)^2 = 64.
Zero flux (standing-wave code: ring modes l in {0,2}) x internal -> 4 per ring, 16 joint code states.
H = J_A hop_A + J_B hop_B + sum_jk V_jk n_j^A n_k^B (x) |R2R2><R2R2|   (only R2-R2 pairs interact).
Geometry: unit-side squares, centres separated by D along x, V_jk ~ 1/d^6 scaled so mean V = v.
Target gate: same H with V replaced by its mean v (clean internal-axis controlled phase), at t = pi/v.
Reports: worst-case code leakage (max over 200 times in [0,t]), worst code->code ring-mode exchange
amplitude^2 not present in target, and overlap |Tr(U_t^dag K)|/16 at t."""
import numpy as np

def expmh(H, t):
    w, V = np.linalg.eigh(H); return (V*np.exp(-1j*w*t)) @ V.conj().T

N = 4
hop = np.zeros((N, N))
for j in range(N): hop[j, (j+1) % N] = hop[(j+1) % N, j] = 1
pos = [np.array([np.cos(np.pi/4+j*np.pi/2), np.sin(np.pi/4+j*np.pi/2)])/np.sqrt(2) for j in range(N)]
F = np.array([[np.exp(2j*np.pi*l*j/N)/2 for l in range(N)] for j in range(N)])
I2, I4 = np.eye(2), np.eye(4); P2 = np.diag([0., 1.])

def run(r, v, D=2.0):
    JA, JB = r, 1.0
    d = np.array([[np.linalg.norm(pos[j] - (pos[k] + [D, 0])) for k in range(N)] for j in range(N)])
    W = d**-6; W *= v/W.mean()
    HA = np.kron(np.kron(JA*hop, I2), np.eye(8)); HB = np.kron(np.eye(8), np.kron(JB*hop, I2))
    Vfull = sum(W[j, k]*np.kron(np.kron(np.diag(I4[j]), P2), np.kron(np.diag(I4[k]), P2)) for j in range(N) for k in range(N))
    Vmean = v*np.kron(np.kron(I4, P2), np.kron(I4, P2))
    T1 = np.kron(F, I2); T = np.kron(T1, T1)                      # to (mode,int)x(mode,int) basis
    one = [2*l + s for l in (0, 2) for s in (0, 1)]
    code = [8*a + b for a in one for b in one]
    H = T.conj().T @ (HA + HB + Vfull) @ T; Ht = T.conj().T @ (HA + HB + Vmean) @ T
    tg = np.pi/v; leak = 0
    for t in np.linspace(0, tg, 200):
        K = expmh(H, t)[np.ix_(code, code)]
        leak = max(leak, np.linalg.norm(np.eye(16) - K.conj().T @ K, 2))
    K = expmh(H, tg)[np.ix_(code, code)]; Kt = expmh(Ht, tg)[np.ix_(code, code)]
    exch = np.max(np.abs(K)**2 * (np.abs(Kt)**2 < 1e-9))           # code->code amplitude absent in target
    return leak, exch, abs(np.trace(Kt.conj().T @ K))/16

import sys
if len(sys.argv) > 1:
    for D in (2, 3, 4, 6):
        for v in (0.05, 0.1):
            L, E, O = run(1.5, v, D); print(f"D={D}  v/J_B={v}  leak={L:.2e}  overlap={O:.5f}")
    sys.exit()
print("ratio  v/J_B   leak_max   exchange   overlap")
for r in (1.0, 1.425, 1.5, 1.575, 2.0):
    for v in (0.05, 0.1, 0.2):
        L, E, O = run(r, v)
        print(f"{r:5.3f}  {v:5.2f}   {L:.2e}   {E:.2e}   {O:.5f}")
