"""Diagnose P2-CIM fits: slice structure, and models A, B, C (C adds eps^2 delta^2 and alpha^2 delta^2 terms).
Fit in log space via relative-weighted least squares; 5-fold CV; coefficients printed in scientific notation."""
import numpy as np, os
R = np.loadtxt(os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "p2cim_grid.csv"), delimiter=",", skiprows=1)
e, d, a, y = R.T[:4]
def show(title, m):
    print(title); [print(f"   eps={r[0]:.2f} delta={r[1]:.2f} alpha={r[2]:.2f}: {r[3]:.3e}") for r in R[m]]
show("alpha=0 slice (no unevenness), delta=0.03:", (a == 0) & (d == .03))
show("alpha=0, eps=0:", (a == 0) & (e == 0))
show("eps=0, delta=0 (unevenness only):", (e == 0) & (d == 0))
show("eps=0.1, delta=0:", (e == .1) & (d == 0))
mask = y > 1e-11
e, d, a, y = e[mask], d[mask], a[mask], y[mask]
F = {"A": [a**2, d**2, e**2*a**2],
     "B": [a**2, d**2, e*a**2, e**2*a**2, a*d],
     "C": [a**2, d**2, e**2*a**2, e**2*d**2, a**2*d**2],
     "D": [a**2, d**2, e*a**2, e**2*a**2, e**2*d**2, a**2*d**2, e*d**2],
     "E (sixth-order + cross)": [a**6, d**6, e**2*a**2],
     "E+ (adds eps^2 delta^2, alpha^2 delta^2)": [a**6, d**6, e**2*a**2, e**2*d**2, a**2*d**2]}
idx = np.random.default_rng(0).permutation(len(y)); folds = np.array_split(idx, 5)
for name, cols in F.items():
    X = np.stack(cols, 1); errs = []
    for k in range(5):
        te = folds[k]; trn = np.setdiff1d(idx, te)
        coef, *_ = np.linalg.lstsq(X[trn]/y[trn, None], np.ones(len(trn)), rcond=None)
        errs.append(np.abs(np.log10(np.clip(X[te] @ coef, 1e-14, None)/y[te])))
    errs = np.concatenate(errs)
    coef, *_ = np.linalg.lstsq(X/y[:, None], np.ones_like(y), rcond=None)
    print(f"model {name}: coef = " + ", ".join(f"{c:.3e}" for c in coef) +
          f"\n   held-out |log10 err| median {np.median(errs):.3f}  90% {np.percentile(errs, 90):.3f}  max {errs.max():.3f}")
    if name.startswith("E+"):
        out = np.column_stack([e, d, a, y, X @ coef, np.log10(np.clip(X @ coef, 1e-14, None)/y)])
        np.savetxt(os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "p2cim_fit_residuals_modelEplus.csv"), out,
                   delimiter=",", header="eps,delta,alpha,infidelity,predicted,log10_pred_over_actual", comments="")
