"""P2-CIM-01: coupled imperfection mapping (ratio 1.5, 2 echo segments, D=2, v=0.1, ideal flips).
Grid: eps (ring-A bond, +) x delta (ring-A site 0) x alpha (interaction unevenness) = 6 x 5 x 6 = 180.
Outputs: results/p2cim_grid.csv, results/p2cim_variants.csv, results/p2cim_convergence.csv,
results/p2cim_boundaries.csv; prints model fits (A vs B, 5-fold CV in log space) and summaries."""
import numpy as np, csv, os, itertools, time, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cim_core import operators, gate, metrics

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "results"); os.makedirs(OUT, exist_ok=True)
ops = operators()
Ut, _ = gate(ops)                                              # intended gate (alpha=0, no errors)
EPS = [0, .01, .03, .05, .1, .2]; DEL = [0, .01, .03, .05, .1]; ALP = [0, .1, .25, .5, .75, 1.0]

t0 = time.time(); rows = []
for e, dl, a in itertools.product(EPS, DEL, ALP):
    inf, lk = metrics(gate(ops, alpha=a, epsA=e, delta=dl)[0], Ut)
    rows.append((e, dl, a, inf, lk))
with open(os.path.join(OUT, "p2cim_grid.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["eps_bondA", "delta_siteA", "alpha", "infidelity", "worst_leakage"]); w.writerows(rows)
print(f"grid: {len(rows)} configs in {time.time()-t0:.0f}s")

R = np.array(rows)
# ---------- model fits on log(infidelity), excluding numerically-zero points ----------
mask = R[:, 3] > 1e-11
e, dl, a, y = R[mask, 0], R[mask, 1], R[mask, 2], R[mask, 3]
feats = {"A": lambda e, d, a: np.stack([a**2, d**2, e**2*a**2], 1),
         "B": lambda e, d, a: np.stack([a**2, d**2, e*a**2, e**2*a**2, a*d], 1)}
rng = np.random.default_rng(0); idx = rng.permutation(len(y)); folds = np.array_split(idx, 5)
for name, fx in feats.items():
    X = fx(e, dl, a); errs = []
    for k in range(5):
        te = folds[k]; trn = np.setdiff1d(idx, te)
        wgt = 1/y[trn]                                          # relative-error weighted least squares
        coef, *_ = np.linalg.lstsq(X[trn]*wgt[:, None], y[trn]*wgt, rcond=None)
        pred = np.clip(X[te] @ coef, 1e-14, None)
        errs.append(np.abs(np.log10(pred/y[te])))
    errs = np.concatenate(errs)
    coef, *_ = np.linalg.lstsq(X/y[:, None], np.ones_like(y), rcond=None)
    print(f"model {name}: coef = {np.round(coef, 5)}   held-out |log10 error|: median {np.median(errs):.3f}, 90% {np.percentile(errs, 90):.3f}, max {errs.max():.3f}")

# ---------- sign / location variants at the worst grid point ----------
var = []
for loc, sgn in (("A", 1), ("A", -1), ("B", 1), ("B", -1)):
    kw = dict(epsA=sgn*.2) if loc == "A" else dict(epsB=sgn*.2)
    inf, lk = metrics(gate(ops, alpha=1.0, delta=.1, **kw)[0], Ut); var.append((loc, sgn*.2, inf, lk))
    print(f"variant bond error {sgn*20:+d}% on ring {loc} (alpha=1, delta=.1): infidelity {inf:.3e}, leakage {lk:.3e}")
with open(os.path.join(OUT, "p2cim_variants.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["ring", "eps", "infidelity", "worst_leakage"]); w.writerows(var)

# ---------- operating boundaries (max alpha on grid meeting both thresholds) ----------
tiers = [("exploratory", 1e-2, 1e-2), ("precision", 1e-3, 1e-3), ("high", 1e-4, 1e-4), ("extended", 1e-5, 1e-5)]
bnd = []
for e_, d_ in itertools.product(EPS, DEL):
    sub = R[(R[:, 0] == e_) & (R[:, 1] == d_)]
    for tname, fi, lk in tiers:
        okF = [r[2] for r in sub if r[3] <= fi]; okL = [r[2] for r in sub if r[4] <= lk]
        both = [r[2] for r in sub if r[3] <= fi and r[4] <= lk]
        mx = lambda L: max(L) if L else -1
        bnd.append((e_, d_, tname, mx(okF), mx(okL), mx(both)))
with open(os.path.join(OUT, "p2cim_boundaries.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["eps", "delta", "tier", "max_alpha_fidelity", "max_alpha_leakage", "max_alpha_both"]); w.writerows(bnd)
print("max alpha meeting BOTH thresholds (-1 = none), rows eps, cols delta:")
for tname, *_ in tiers:
    print(f"  {tname}:")
    for e_ in EPS:
        print("   eps=%.2f  " % e_ + "  ".join("%5.2f" % [b[5] for b in bnd if b[0] == e_ and b[1] == d_ and b[2] == tname][0] for d_ in DEL))

# ---------- convergence ----------
conv = []
for (e_, d_, a_) in ((.2, .1, 1.0), (.05, .03, .5), (.1, .01, .25)):
    vals = [metrics(gate(ops, alpha=a_, epsA=e_, delta=d_, steps=s)[0], gate(ops, steps=s)[0]) for s in (600, 1200, 2400)]
    conv.append((e_, d_, a_, *[x for p in vals for x in p]))
    print(f"convergence eps={e_} delta={d_} alpha={a_}: infidelity " + " -> ".join(f"{p[0]:.4e}" for p in vals))
with open(os.path.join(OUT, "p2cim_convergence.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["eps", "delta", "alpha", "inf600", "leak600", "inf1200", "leak1200", "inf2400", "leak2400"]); w.writerows(conv)
