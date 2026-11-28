"""E5: time-dependent bond drift during the echo gate (ratio 1.5, D=2, v=0.1, ideal flips, delta=0).
Drift amplitude eps0 = 0.05 on bond (3,0). Operating points chosen from P2-CIM: alpha = 0 (uniform control),
0.25 (robust), 0.75 (high-tier boundary), 1.0 (original geometry).
'corr' = same eps(t) on both rings; 'indep' = ring B opposite sign (linear/abrupt) or +pi/2 phase (sinusoid).
Segment length Ts = tg/2; sinusoid frequency given as f*Ts (cycles per echo segment). Output: results/e5_drift.csv"""
import numpy as np, csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cim_core import operators, gate, metrics
ops = operators(); Ut, _ = gate(ops); e0 = 0.05
def drifts():
    yield "static", "corr", lambda t, tg: (e0, e0)
    yield "static", "A only", lambda t, tg: (e0, 0.0)
    yield "linear", "corr", lambda t, tg: (e0*t/tg, e0*t/tg)
    yield "linear", "indep", lambda t, tg: (e0*t/tg, -e0*t/tg)
    yield "abrupt (seg 1 only)", "corr", lambda t, tg: ((e0, e0) if t < tg/2 else (0.0, 0.0))
    yield "abrupt (seg 1 only)", "A only", lambda t, tg: ((e0, 0.0) if t < tg/2 else (0.0, 0.0))
    for fT in (0.25, 0.5, 1, 2, 4):
        yield f"sin f*Ts={fT}", "corr", (lambda fT: lambda t, tg: (e0*np.sin(2*np.pi*fT*t/(tg/2)),)*2)(fT)
        yield f"sin f*Ts={fT}", "indep", (lambda fT: lambda t, tg: (e0*np.sin(2*np.pi*fT*t/(tg/2)), e0*np.cos(2*np.pi*fT*t/(tg/2))))(fT)
rows = []
for alpha in (0.0, 0.25, 0.75, 1.0):
    print(f"--- alpha = {alpha}")
    for kind, corr, fn in drifts():
        inf, lk = metrics(gate(ops, alpha=alpha, eps_fn=fn)[0], Ut)
        rows.append((alpha, kind, corr, inf, lk)); print(f"   {kind:22s} {corr:7s} infidelity {inf:.3e}  leakage {lk:.3e}")
os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "results"), exist_ok=True)
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "e5_drift.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["alpha", "drift", "correlation", "infidelity", "worst_leakage"]); w.writerows(rows)
