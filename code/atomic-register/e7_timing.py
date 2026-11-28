"""E7: drift-resistant echo timing (ideal instantaneous flips; ratio 1.5, D=2, v=0.1; total interaction area pi).
Sequences (flip times as fractions of total T; even flip count so labels are restored):
  orig-seg   : two sin^2 segments, flips at 1/2 and 1        (the baseline used so far)
  orig-cont  : one continuous sin^2 envelope, flips at 1/2 and 1
  sym-seg    : three sin^2 segments T/4, T/2, T/4, flips at 1/4 and 3/4
  sym-cont   : continuous envelope, flips at 1/4 and 3/4      (cancels constant and linear drift)
  cpmg4-cont : continuous envelope, flips at 1/8, 3/8, 5/8, 7/8
Drift on bond (3,0), amplitude 0.05, both rings ('corr') or ring A only: static, linear, step at T/2,
sinusoid with f*T in {0.5, 1, 2}. alpha in {0, 0.5}. Output: results/e7_timing.csv"""
import numpy as np, csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cim_core import operators, metrics, expmh
ops = operators(); v = 0.1; T = 2*np.pi/v; e0 = 0.05
SEQ = {"orig-seg": ("seg", [0.5, 1.0]), "orig-cont": ("cont", [0.5, 1.0]),
       "sym-seg": ("seg", [0.25, 0.75]), "sym-cont": ("cont", [0.25, 0.75]),
       "cpmg4-cont": ("cont", [0.125, 0.375, 0.625, 0.875])}

def run(seq, alpha, drift, steps=1600):
    mode, flips = SEQ[seq]
    V = ops["Vbar"] + alpha*ops["Vdev"]
    bounds = [0.0] + flips + ([1.0] if flips[-1] < 1.0 else [])
    U = np.eye(64, dtype=complex); dt = T/steps; nflip = 0
    for k in range(steps):
        t0, t1 = k*dt, (k+1)*dt; tm = (t0 + t1)/2
        if mode == "cont":
            env = 2*np.sin(np.pi*tm/T)**2                             # area v*T (x2 => same as segmented total)
        else:
            i = int(np.searchsorted(bounds, tm/T) - 1); a, b = bounds[i]*T, bounds[i+1]*T
            env = 2*np.sin(np.pi*(tm - a)/(b - a))**2
        eA, eB = drift(tm)
        H = ops["H0"] + eA*ops["bondA"] + eB*ops["bondB"] + 0.5*env*V   # 0.5*2 sin^2 averages to 1/2 -> area pi
        U = expmh(H, dt) @ U
        while nflip < len(flips) and t1 >= flips[nflip]*T - 1e-9:
            U = ops["FAB"] @ U; nflip += 1
    return U

DRIFT = {"none": lambda t: (0, 0), "static corr": lambda t: (e0, e0), "static A": lambda t: (e0, 0),
         "linear corr": lambda t: (e0*t/T,)*2, "linear A": lambda t: (e0*t/T, 0),
         "step corr": lambda t: (e0, e0) if t < T/2 else (0, 0),
         **{f"sin fT={f} corr": (lambda f: lambda t: (e0*np.sin(2*np.pi*f*t/T),)*2)(f) for f in (0.5, 1, 2)}}
Ut = run("orig-seg", 0.0, DRIFT["none"])
rows = []
for alpha in (0.0, 0.5):
    print(f"--- alpha = {alpha}   (infidelity / leakage)")
    print("   drift          " + "".join(f"{s:>22s}" for s in SEQ))
    for dname, dfn in DRIFT.items():
        cells = []
        for s in SEQ:
            inf, lk = metrics(run(s, alpha, dfn), Ut); rows.append((alpha, dname, s, inf, lk)); cells.append(f"{inf:9.1e}/{lk:8.1e}   ")
        print(f"   {dname:14s} " + "".join(f"{c:>22s}" for c in cells))
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "e7_timing.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["alpha", "drift", "sequence", "infidelity", "worst_leakage"]); w.writerows(rows)
