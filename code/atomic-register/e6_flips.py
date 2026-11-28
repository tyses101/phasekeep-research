"""E6: finite-duration staggered flips inside the two-ring echo gate (ratio 1.5, D=2, v=0.1, hopping always on).
Flip control: potential g(t) on odd sites of both rings (g*tau = pi gives the ideal flip). Control magnitude
a = g/2 = 4 J_B for square and composite flips.
  inst      : ideal instantaneous flip (reference)
  square    : g = 8 for tau = pi/8
  sin2      : g(t) = 16 sin^2(pi t/tau), same tau and area (twice the peak)
  composite : 4 signed constant-|g| segments per ring (+,-,+,-), durations optimised in the two-level code
              model (H = -s a tau_x + 2J tau_z) to give exactly tau_x up to global phase; both rings forced to the
              same total duration (no waiting). Optimiser: Nelder-Mead implemented here (NumPy only).
Interaction during flips: r_on = 0 (off) or 1 (left on at full mean strength v, with alpha unevenness);
its conditional-phase area is subtracted from the sin^2 segments so the intended phase stays pi.
Cases: alpha in {0, 0.5}; bond error eps_A in {0, 0.05}. Target = intended gate (ideal flips, no errors, alpha=0).
Output: results/e6_flips.csv"""
import numpy as np, csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cim_core import operators, gate, metrics, expmh
X2 = np.array([[0, 1], [1, 0]], complex); Z2 = np.diag([1., -1]).astype(complex)
def u2(durs, signs, a, J):
    U = np.eye(2, dtype=complex)
    for t, s in zip(durs, signs): U = expmh(-s*a*X2 + 2*J*Z2, t) @ U
    return U
def nelder_mead(f, x0, step=0.1, iters=3000, tol=1e-14):
    n = len(x0); P = [np.array(x0, float)] + [np.array(x0, float) + step*np.eye(n)[i] for i in range(n)]
    V = [f(p) for p in P]
    for _ in range(iters):
        o = np.argsort(V); P = [P[i] for i in o]; V = [V[i] for i in o]
        if V[-1] - V[0] < tol: break
        c = np.mean(P[:-1], 0); xr = c + (c - P[-1]); fr = f(xr)
        if fr < V[0]:
            xe = c + 2*(c - P[-1]); fe = f(xe); P[-1], V[-1] = (xe, fe) if fe < fr else (xr, fr)
        elif fr < V[-2]: P[-1], V[-1] = xr, fr
        else:
            xc = c + 0.5*(P[-1] - c); fc = f(xc)
            if fc < V[-1]: P[-1], V[-1] = xc, fc
            else:
                P = [P[0]] + [P[0] + 0.5*(p - P[0]) for p in P[1:]]; V = [f(p) for p in P]
    return P[int(np.argmin(V))], min(V)
a, signs = 4.0, (1, -1, 1, -1)
infid = lambda U: 1 - abs(np.trace(X2.conj().T @ U))**2/4
def solve_ring(J, total=None, seeds=40):
    rng = np.random.default_rng(1); best = (None, 1)
    for _ in range(seeds):
        if total is None:
            f = lambda x: infid(u2(np.abs(x), signs, a, J)); x, v = nelder_mead(f, rng.uniform(0.05, 0.5, 4))
            d = np.abs(x)
        else:
            f = lambda x: infid(u2(np.append(np.abs(x), max(total - np.abs(x).sum(), 0)), signs, a, J)) + 10*max(np.abs(x).sum() - total, 0)
            x, v = nelder_mead(f, rng.uniform(0.02, total/3, 3)); d = np.append(np.abs(x), total - np.abs(x).sum())
        if v < best[1]: best = (d, v)
    return best
dB, vB = solve_ring(1.0); TC = dB.sum()
dA, vA = solve_ring(1.5, total=TC)
print(f"composite: ring B durations {np.round(dB, 4)} (infid {vB:.1e}); ring A durations {np.round(dA, 4)} (infid {vA:.1e}); total {TC:.4f}/J_B")

def flip_factory(kind, tau=np.pi/8, steps=200):
    def make(ops, Hs, r_on, alpha, tg):
        V = r_on*(ops["Vbar"] + alpha*ops["Vdev"]); Hb = Hs(0.0, tg) + V
        if kind in ("square", "sin2"):
            U = np.eye(64, dtype=complex); dt = tau/steps
            for n in range(steps):
                g = 8.0 if kind == "square" else 16*np.sin(np.pi*(n+0.5)/steps)**2
                U = expmh(Hb + g*(ops["oddA"] + ops["oddB"]), dt) @ U
            return U, tau, 2*r_on*0.1*tau
        # composite: merge the two rings' piecewise-constant schedules
        edges = sorted(set(np.concatenate([[0], np.cumsum(dA), np.cumsum(dB)]).round(12)))
        seg = lambda d, t: int(np.searchsorted(np.cumsum(d), t, side="right"))
        U = np.eye(64, dtype=complex)
        for t0, t1 in zip(edges[:-1], edges[1:]):
            tm = (t0 + t1)/2; sA, sB = signs[min(seg(dA, tm), 3)], signs[min(seg(dB, tm), 3)]
            U = expmh(Hb + 8.0*(sA*ops["oddA"] + sB*ops["oddB"]), t1 - t0) @ U
        return U, TC, 2*r_on*0.1*TC
    return make

ops = operators(); Ut, tg0 = gate(ops); rows = []
for alpha in (0.0, 0.5):
    for eps in (0.0, 0.05):
        print(f"--- alpha={alpha}, eps_A={eps}")
        for kind in ("inst", "square", "sin2", "composite"):
            for r_on in ((0.0,) if kind == "inst" else (0.0, 1.0)):
                U, tgt = gate(ops, alpha=alpha, epsA=eps, flip=None if kind == "inst" else flip_factory(kind), r_on=r_on)
                inf, lk = metrics(U, Ut); rows.append((alpha, eps, kind, r_on, tgt, inf, lk))
                print(f"   {kind:9s} interaction-during-flip={'on ' if r_on else 'off'}  gate time {tgt:7.3f}/J_B  infidelity {inf:.3e}  leakage {lk:.3e}")
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "e6_flips.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["alpha", "eps_A", "flip", "interaction_on_during_flip", "gate_time", "infidelity", "worst_leakage"]); w.writerows(rows)
