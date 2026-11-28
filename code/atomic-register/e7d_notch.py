"""E7-D: interaction notches around ideal flips (ratio 1.5, D=2, v=0.1, alpha=0.5 unless stated).
Base envelope: one continuous sin^2 over T. Around each flip time t_f the envelope is multiplied by
  n(t) = 1 - (1 - r) * p(x),  x = (t - t_f)/(w*T/2)
with p a notch profile (1 at x=0, 0 for |x|>=1 or decaying): raised cosine, Gaussian (sigma = 1/2.5, truncated),
quartic polynomial (1-x^2)^2. r = residual interaction at the flip, w = full notch width / T.
The envelope is rescaled so the mean-interaction area stays pi (intended conditional phase); the required peak
scaling is reported. 'uneven-only' variant notches only the uneven part: V = g(t) Vbar + g(t) n(t) alpha Vdev.
Phase 1: grid r x w x profile, symmetric timing, no drift. Phase 2: best settings vs drift, CPMG-4, other alpha.
Output: results/e7d_grid.csv, results/e7d_followup.csv"""
import numpy as np, csv, os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cim_core import operators, metrics, expmh
ops = operators(); v = 0.1; T = 2*np.pi/v; e0 = 0.05; STEPS = 2400
PROF = {"raised-cos": lambda x: np.where(np.abs(x) < 1, 0.5*(1 + np.cos(np.pi*x)), 0.0),
        "gaussian": lambda x: np.where(np.abs(x) < 1.5, np.exp(-x**2/(2*0.4**2)), 0.0),
        "quartic": lambda x: np.where(np.abs(x) < 1, (1 - x**2)**2, 0.0)}
FLIPS = {"sym": [0.25, 0.75], "cpmg4": [0.125, 0.375, 0.625, 0.875]}

def envelope(flips, r, w, prof):
    t = (np.arange(STEPS) + 0.5)/STEPS*T
    g = np.sin(np.pi*t/T)**2; n = np.ones_like(t)
    for tf in flips:
        n *= 1 - (1 - r)*PROF[prof]((t - tf*T)/(w*T/2))
    return t, g, n

def run(flips, r, w, prof, alpha=0.5, drift=lambda t: (0, 0), uneven_only=False):
    t, g, n = envelope(flips, r, w, prof); dt = T/STEPS
    gu = g if uneven_only else g*n                                   # envelope on the uniform part
    scale = np.pi/(v*np.sum(gu)*dt)                                  # keep mean-interaction area = pi
    U = np.eye(64, dtype=complex); k = 0
    for i, tm in enumerate(t):
        eA, eB = drift(tm)
        H = ops["H0"] + eA*ops["bondA"] + eB*ops["bondB"] + scale*(gu[i]*ops["Vbar"] + g[i]*n[i]*alpha*ops["Vdev"])
        U = expmh(H, dt) @ U
        while k < len(flips) and (i + 1)*dt >= flips[k]*T - 1e-9: U = ops["FAB"] @ U; k += 1
    return U, scale*np.max(gu)/1.0

Ut = run(FLIPS["sym"], 0, 0.1, "raised-cos", alpha=0.0)[0]           # intended gate (uniform V) - pure controlled phase
rows = []
print("phase 1: alpha=0.5, symmetric timing, no drift   (infidelity / leakage, peak factor)")
for prof, w, r in itertools.product(PROF, (0.01, 0.025, 0.05, 0.1, 0.2), (0, .01, .05, .1, .25, .5)):
    U, pk = run(FLIPS["sym"], r, w, prof); inf, lk = metrics(U, Ut); rows.append((prof, w, r, inf, lk, pk))
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "e7d_grid.csv"), "w", newline="") as f:
    wr = csv.writer(f); wr.writerow(["profile", "width_frac_T", "residual", "infidelity", "worst_leakage", "peak_factor"]); wr.writerows(rows)
for prof in PROF:
    print(f"  {prof}: rows = width, cols = residual {[0, .01, .05, .1, .25, .5]}")
    for w in (0.01, 0.025, 0.05, 0.1, 0.2):
        print(f"    w={w:5.3f} " + " ".join(f"{x[3]:8.1e}" for x in rows if x[0] == prof and x[1] == w) +
              f"   peak x{[x[5] for x in rows if x[0] == prof and x[1] == w][0]:.2f}")
best = min(rows, key=lambda x: x[3]); print("best:", best)

fu = []; prof, w = best[0], best[1]
DR = {"none": lambda t: (0, 0), "linear corr": lambda t: (e0*t/T,)*2, "step corr": lambda t: (e0, e0) if t < T/2 else (0, 0),
      "sin fT=0.5": lambda t: (e0*np.sin(np.pi*t/T),)*2, "sin fT=1": lambda t: (e0*np.sin(2*np.pi*t/T),)*2}
print(f"phase 2: best profile {prof}, width {w}")
for seq, alpha, r, uo in itertools.product(("sym", "cpmg4"), (0.25, 0.5, 1.0), (0.0, 0.05), (False, True)):
    for dname, dfn in DR.items():
        inf, lk = metrics(run(FLIPS[seq], r, w, prof, alpha=alpha, drift=dfn, uneven_only=uo)[0], Ut)
        fu.append((seq, alpha, r, "uneven-only" if uo else "full", dname, inf, lk))
    print(f"  {seq:5s} alpha={alpha:4} r={r:4} notch={'uneven-only' if uo else 'full':11s} " +
          "  ".join(f"{x[4]}:{x[5]:.1e}" for x in fu[-len(DR):]))
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "e7d_followup.csv"), "w", newline="") as f:
    wr = csv.writer(f); wr.writerow(["timing", "alpha", "residual", "notch", "drift", "infidelity", "worst_leakage"]); wr.writerows(fu)
