"""P2 tolerance envelope for one four-site ring (single excitation x internal, 8-dim exact model).
Ideal: uniform hopping J=1, evolve time T. Imperfections (applied to both internal states):
  site  : detuning delta on site 0
  bond  : bond (3,0) strength 1+eps
  phase : Peierls phase phi on bond (3,0)  (net flux phi)
Metrics vs the ideal evolution, on code C = {l=0,2} x {R1,R2}:
  worst-case code leakage (spectral norm of I - K^dag K), and leakage-aware logical F_avg against the ideal
  code unitary: W = C^dag U_ideal^dag U C, F = (|Tr W|^2 + Tr W^dag W)/(4*5)."""
import numpy as np
def expmh(H, t):
    w, V = np.linalg.eigh(H); return (V*np.exp(-1j*w*t)) @ V.conj().T
def ring(delta=0., eps=0., phi=0.):
    H = np.zeros((4, 4), complex)
    for j in range(4):
        a, b = j, (j+1) % 4
        g = (1+eps)*np.exp(1j*phi) if (a, b) == (3, 0) else 1.0
        H[b, a] += g; H[a, b] += np.conj(g)
    H[0, 0] += delta
    return np.kron(H, np.eye(2))
F4 = np.array([[np.exp(1j*np.pi*l*j/2)/2 for l in range(4)] for j in range(4)])
C = np.kron(F4[:, [0, 2]], np.eye(2))                       # 8 x 4 code basis
def metrics(Hp, T):
    U, U0 = expmh(Hp, T), expmh(ring(), T)
    K = C.conj().T @ U @ C
    W = C.conj().T @ U0.conj().T @ U @ C
    return np.linalg.norm(np.eye(4) - K.conj().T @ K, 2), 1 - (abs(np.trace(W))**2 + np.real(np.trace(W.conj().T @ W)))/20

levels = (0.001, 0.01, 0.05, 0.1, 0.2, 0.8)
for T in (0.7, 10.0):
    print(f"=== evolution time T = {T}/J ===")
    print("  size   | site: leak / 1-F      | bond: leak / 1-F      | phase: leak / 1-F")
    for x in levels:
        r = [metrics(ring(**{k: x}), T) for k in ("delta", "eps", "phi")]
        print(f"  {x:6.3f} | " + " | ".join(f"{l:.2e} / {f:.2e}" for l, f in r))
