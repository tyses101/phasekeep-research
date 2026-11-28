"""REF-01 (local, noiseless): one four-site ring x internal {R1,R2} in DIRECT ONE-HOT encoding on 8 qubits.
Qubit q = 2*j + r  (site j = 0..3, internal r = 0,1); one excitation = one qubit in |1>.
Gate set (all excitation-number conserving, native to XY/iSWAP-type hardware):
  - hopping Trotter step: XY rotations on ring bonds, split into two commuting layers {(0,1),(2,3)} and {(1,2),(3,0)}
  - staggered flip: Z gate on the qubits of odd sites (exact)
  - microwave rotation on the internal axis: XY rotation between qubits (j,0),(j,1) on every site (exact)
Test: random superpositions of the 4 code states {l=0,2} x {R1,R2}; sequence = MW_x(theta) . Flip . exp(-i H_hop T).
Compared with the exact 8-dim model. Reports mean/min state fidelity, code leakage (to l=1,3), excitation-number leakage."""
import numpy as np
rng = np.random.default_rng(1)
NQ, DIM = 8, 256
q = lambda j, r: 2*(j % 4) + r

def xy_ham(a, b):
    """sigma+_a sigma-_b + h.c. on the full 256-dim space."""
    H = np.zeros((DIM, DIM))
    for s in range(DIM):
        if (s >> a) & 1 and not (s >> b) & 1:
            t = s ^ (1 << a) ^ (1 << b); H[t, s] = H[s, t] = 1
    return H

def expmh(H, t):
    w, V = np.linalg.eigh(H); return (V*np.exp(-1j*w*t)) @ V.conj().T

J, T, theta = 1.0, 0.7, 0.9
layerA = sum(xy_ham(q(j, r), q(j+1, r)) for j in (0, 2) for r in (0, 1))
layerB = sum(xy_ham(q(j, r), q(j+1, r)) for j in (1, 3) for r in (0, 1))
Hhop = J*(layerA + layerB)
Hmw = sum(xy_ham(q(j, 0), q(j, 1)) for j in range(4))
Zodd = np.diag([(-1)**sum((s >> q(j, r)) & 1 for j in (1, 3) for r in (0, 1)) for s in range(DIM)]).astype(complex)
MW = expmh(Hmw, theta)

onehot = lambda j, r: 1 << q(j, r)
def mode_state(l, r):                         # ring mode l (code uses 0, 2) with internal r
    v = np.zeros(DIM, complex)
    for j in range(4): v[onehot(j, r)] = np.exp(1j*np.pi*l*j/2)/2
    return v
code = np.array([mode_state(l, r) for l in (0, 2) for r in (0, 1)]).T      # 256 x 4
single = [onehot(j, r) for j in range(4) for r in (0, 1)]

U_exact = MW @ Zodd @ expmh(Hhop, T)
# sanity: the two hopping layers commute on the 4-site ring (Klein-group dimer coverings) -> Trotter is exact
print("||[layerA, layerB]|| =", np.linalg.norm(layerA @ layerB - layerB @ layerA))
c0 = np.ones(4)/2; p0 = code @ c0
print("sanity (test is not vacuous): F(exact, no-hopping) =", round(abs(np.vdot(U_exact @ p0, MW @ Zodd @ p0))**2, 4),
      " F(exact, no-flip) =", round(abs(np.vdot(U_exact @ p0, MW @ expmh(Hhop, T) @ p0))**2, 4))
print("Trotter steps | mean F   | min F    | mean code leakage | number leakage | 2-qubit XY gates")
for n in (1, 2, 4, 8, 16, 32):
    step = expmh(J*layerB, T/(2*n)) @ expmh(J*layerA, T/n) @ expmh(J*layerB, T/(2*n))   # symmetric (2nd-order) Trotter
    U = MW @ Zodd @ np.linalg.matrix_power(step, n)
    Fs, Ls, Ns = [], [], []
    for _ in range(200):
        c = rng.normal(size=4) + 1j*rng.normal(size=4); c /= np.linalg.norm(c)
        psi0 = code @ c; out, ideal = U @ psi0, U_exact @ psi0
        Fs.append(abs(np.vdot(ideal, out))**2)
        Ls.append(1 - np.linalg.norm(code.conj().T @ out)**2)
        Ns.append(1 - sum(abs(out[s])**2 for s in single))
    gates = n*12 + 4                           # per step: 4 (B/2) + 4 (A) + 4 (B/2) bonds; + 4 MW XY gates
    print(f"{n:13d} | {np.mean(Fs):.6f} | {min(Fs):.6f} | {np.mean(Ls):.2e}          | {max(Ns):.1e}        | {gates}")
