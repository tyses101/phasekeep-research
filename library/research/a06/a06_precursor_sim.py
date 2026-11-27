#!/usr/bin/env python3
"""A06 precursor: does ONE shared optical element keep its advantage over INDIVIDUAL addressing
as the encoded mode family grows, once preparation / access costs and imperfections are counted?

Operation under test (the same for both implementations): polarization exchange H<->V applied
coherently to every one of N OAM modes, leaving each mode in place (a half-wave plate at 45 deg).
Mode family: l in {-(N-1), -(N-3), ..., +(N-1)} (odd values, mirror closed; N=2 is the Tetragon pair +-1).

  SHARED       one half-wave plate acts on all N modes at once.
  INDIVIDUAL   OAM sorter (binary tree of N-1 interferometers) -> one plate per mode -> inverse sorter.

Run:  python3 -I a06_precursor_sim.py [outdir]      (numpy only; deterministic; exit 0 only if all checks pass)

EVIDENCE CLASSES. Operation counts and the closed-form checks are DERIVED. EVERY error and loss number below is
ASSUMED (a sensitivity input), not a measurement. The sorter error model is an illustrative node-error model, not a
specific sorter design. State preparation fidelity and detection are NOT simulated (only counted). Nothing here
demonstrates efficiency; it asks where an advantage would erode under stated assumptions.
"""
import csv, json, math, sys
from pathlib import Path
import numpy as np

SEED = 20261126
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "a06_results")
OUT.mkdir(parents=True, exist_ok=True)
NS = [2, 4, 8, 16, 32]
REPS = 400
ELEMENTS_PER_INTERFEROMETER = 3          # 2 beam splitters + 1 Dove prism (counting convention, ASSUMED)
DEFAULT = dict(sigma_cal=0.01,           # residual plate calibration error (rad), retardance and axis, per calibrated plate
               kappa=5e-4,               # shared plate: retardance drift per unit |l| (rad), mode dependence of ONE plate
               sigma_rot=2e-3,           # Dove-prism rotation error (rad); node phase error scales with |l|
               eps_el=2e-3,              # insertion loss per optical element
               clip=1e-3)                # aperture sized so the largest mode loses this fraction per element
checks = []


def check(name, ok, detail=""):
    checks.append((name, bool(ok), detail))
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))


# ---------------- derived helpers ----------------
def modes(N):
    return np.array([2 * i - (N - 1) for i in range(N)])


def enclosed_power(l, x):
    """Fraction of LG(p=0,l) power inside radius R, x = 2R^2/w^2: regularized lower gamma P(|l|+1, x)."""
    k = abs(int(l))
    return 1.0 - math.exp(-x) * sum(x ** j / math.factorial(j) for j in range(k + 1))


def aperture_x(lmax, loss):
    lo, hi = 0.0, 400.0
    for _ in range(200):
        mid = (lo + hi) / 2
        (lo, hi) = (mid, hi) if 1 - enclosed_power(lmax, mid) > loss else (lo, mid)
    return hi


def counts(N):
    """Optical element counts by stage for three tasks. DERIVED from the stated conventions (illustrative)."""
    lv = int(math.log2(N))
    sorter = (N - 1) * ELEMENTS_PER_INTERFEROMETER
    prep_slm = 1                                  # option (a): one hologram/SLM-type device (fidelity not simulated)
    prep_sorter = sorter                          # option (b): inverse sorter from N input ports
    c = {}
    # C: transform in place; state continues to the next operation (no readout)
    c["C_in_place"] = {"shared": {"operation": 1, "after": 0},
                       "individual": {"operation": 2 * sorter + N, "after": 0}}
    # A: transform, then read polarization only
    c["A_read_pol_only"] = {"shared": {"operation": 1, "after": 1},
                            "individual": {"operation": 2 * sorter + N, "after": 1}}
    # B: transform, then resolve OAM and polarization (individual design reads at the sorted ports; no second sorter)
    c["B_full_readout"] = {"shared": {"operation": 1, "after": sorter + N},
                           "individual": {"operation": sorter + N, "after": N}}
    cal = {"shared": 2, "individual": N * 2 + 2 * (N - 1) * 2}
    return c, cal, dict(prep_slm=prep_slm, prep_sorter=prep_sorter, levels=lv)


# ---------------- simulation ----------------
def plate(eps, beta):
    """Half-wave plate, retardance pi+eps, fast axis at 45deg+beta, Jones matrix in the H/V basis."""
    G = math.pi + eps
    nz, nx = -math.sin(2 * beta), math.cos(2 * beta)         # (cos 2theta, sin 2theta) at theta = 45deg+beta
    sz = np.array([[1, 0], [0, -1]], complex)
    sx = np.array([[0, 1], [1, 0]], complex)
    return math.cos(G / 2) * np.eye(2) - 1j * math.sin(G / 2) * (nz * sz + nx * sx)


TARGET = -1j * np.array([[0, 1], [1, 0]], complex)          # ideal plate (eps=beta=0)


def sorter_matrix(N, sigma_rot, rng):
    """Binary-butterfly of random Givens rotations on mode pairs (i, i xor 2^k); angle sd ~ sigma_rot*max|l|/2.
    Acts identically on both polarizations. Ideal sorter = identity after relabeling ports."""
    ls = modes(N)
    S = np.eye(N)
    for k in range(int(math.log2(N))):
        G = np.eye(N)
        for i in range(N):
            j = i ^ (1 << k)
            if i < j:
                th = rng.normal(0, sigma_rot * max(abs(ls[i]), abs(ls[j])) / 2)
                c, s = math.cos(th), math.sin(th)
                G[i, i], G[j, j], G[i, j], G[j, i] = c, c, -s, s
        S = G @ S
    return np.kron(S, np.eye(2))                              # index = 2*mode + pol


def build(N, impl, p, rng, with_loss=True):
    ls = modes(N)
    if impl == "shared":
        eps0, beta0 = rng.normal(0, p["sigma_cal"], 2)
        eps = eps0 + p["kappa"] * np.abs(ls)
        beta = np.full(N, beta0)
    else:
        eps = rng.normal(0, p["sigma_cal"], N)
        beta = rng.normal(0, p["sigma_cal"], N)
    P = np.zeros((2 * N, 2 * N), complex)
    for m in range(N):
        P[2 * m:2 * m + 2, 2 * m:2 * m + 2] = plate(eps[m], beta[m])
    if impl == "individual":
        U = sorter_matrix(N, p["sigma_rot"], rng) @ P @ sorter_matrix(N, p["sigma_rot"], rng)
        n_el = 2 * int(math.log2(N)) * ELEMENTS_PER_INTERFEROMETER + 1
    else:
        U, n_el = P, 1
    amp = np.ones(2 * N)
    if with_loss:
        x = aperture_x(N - 1, p["clip"])
        T = np.array([(1 - p["eps_el"]) ** n_el * enclosed_power(l, x) ** n_el for l in ls])
        # clip applies per element; enclosed_power is the per-element transmission of mode l
        amp = np.sqrt(np.repeat(T, 2))
    return U * amp[None, :], TARGET


def metrics(K, N):
    V = np.kron(np.eye(N), TARGET)
    tr = np.trace(V.conj().T @ K)
    f_unc = abs(tr) ** 2 / (2 * N) ** 2
    tt = np.trace(K.conj().T @ K).real
    f_cond = abs(tr) ** 2 / (2 * N * tt)
    out = K @ np.eye(2 * N)
    s = np.array([abs(np.vdot(V[:, i], out[:, i])) ** 2 / max(np.vdot(out[:, i], out[:, i]).real, 1e-300) for i in range(2 * N)])
    return f_unc, f_cond, tt / (2 * N), s.min()


def run_point(N, impl, p, reps=REPS, seed=SEED):
    rng = np.random.default_rng([seed, N, 0 if impl == "shared" else 1])
    r = np.array([metrics(build(N, impl, p, rng)[0], N) for _ in range(reps)])
    m, se = r.mean(0), r.std(0, ddof=1) / math.sqrt(reps)
    return dict(F_cond=m[1], F_cond_hw95=1.96 * se[1], F_uncond=m[0], transmission=m[2], worst_input=m[3])


# ---------------- self-checks ----------------
def self_checks():
    zero = dict(sigma_cal=0, kappa=0, sigma_rot=0, eps_el=0, clip=1e-3)
    for N in NS:
        for impl in ("shared", "individual"):
            K, _ = build(N, impl, zero, np.random.default_rng(1), with_loss=False)
            fu, fc, tr, w = metrics(K, N)
            check(f"zero-error limit, N={N}, {impl}: fidelity 1, transmission 1", abs(fc - 1) < 1e-12 and abs(tr - 1) < 1e-12 and abs(w - 1) < 1e-12)
    # closed form for the shared plate with mode dependence only: F = |mean_l cos(eps_l/2)|^2
    p = dict(zero, kappa=2e-3)
    for N in (4, 16):
        K, _ = build(N, "shared", p, np.random.default_rng(1), with_loss=False)
        want = np.mean(np.cos(p["kappa"] * np.abs(modes(N)) / 2)) ** 2
        check(f"closed form F=|mean cos(eps_l/2)|^2, shared, N={N}", abs(metrics(K, N)[1] - want) < 1e-12, f"{want:.8f}")
    # sorter unitarity (orthogonality) with errors
    S = sorter_matrix(32, 5e-3, np.random.default_rng(2))
    check("sorter error matrix is orthogonal (no hidden gain or loss)", np.max(abs(S.T @ S - np.eye(64))) < 1e-12)
    # aperture formula: P(1,x)=1-e^-x ; monotone in l
    check("enclosed-power formula: l=0 gives 1-e^-x", abs(enclosed_power(0, 2.0) - (1 - math.exp(-2.0))) < 1e-15)
    check("enclosed power decreases with |l| at fixed aperture", all(enclosed_power(l, 20) > enclosed_power(l + 2, 20) for l in range(0, 20, 2)))
    x = aperture_x(31, 1e-3)
    check("aperture solver: largest mode loses 0.1% per element", abs((1 - enclosed_power(31, x)) - 1e-3) < 1e-9, f"R/w = {math.sqrt(x / 2):.3f}")
    # counts
    c, cal, _ = counts(8)
    check("count formulas N=8: individual in-place = 2*(N-1)*3 + N = 50, shared = 1", c["C_in_place"]["individual"]["operation"] == 50 and c["C_in_place"]["shared"]["operation"] == 1)
    check("calibration parameters N=8: shared 2, individual 2N + 4(N-1) = 44", cal["shared"] == 2 and cal["individual"] == 44)
    # determinism
    a = run_point(8, "individual", DEFAULT, reps=20)
    b = run_point(8, "individual", DEFAULT, reps=20)
    check("deterministic for a fixed seed", a == b)


# ---------------- sweeps ----------------
def sweeps():
    rows = []
    # 1. headline: default assumptions, scaling in N
    for N in NS:
        for impl in ("shared", "individual"):
            rows.append(dict(sweep="default", N=N, impl=impl, **{k: DEFAULT[k] for k in DEFAULT}, **run_point(N, impl, DEFAULT)))
    # 2. shared-plate mode dependence kappa (individual unaffected)
    for kappa in (0, 1e-4, 5e-4, 1e-3, 2e-3, 5e-3, 1e-2, 2e-2, 5e-2):
        for N in NS:
            rows.append(dict(sweep="kappa", N=N, impl="shared", **dict(DEFAULT, kappa=kappa), **run_point(N, "shared", dict(DEFAULT, kappa=kappa))))
    # 3. sorter rotation error and element loss (individual only)
    for sr in (5e-4, 1e-3, 2e-3, 5e-3, 1e-2):
        for N in NS:
            rows.append(dict(sweep="sigma_rot", N=N, impl="individual", **dict(DEFAULT, sigma_rot=sr), **run_point(N, "individual", dict(DEFAULT, sigma_rot=sr))))
    for el in (1e-3, 2e-3, 5e-3, 1e-2):
        for N in NS:
            for impl in ("shared", "individual"):
                rows.append(dict(sweep="eps_el", N=N, impl=impl, **dict(DEFAULT, eps_el=el), **run_point(N, impl, dict(DEFAULT, eps_el=el))))
    return rows


def main():
    print("== self-checks ==")
    self_checks()
    print("\n== sweeps (all error parameters ASSUMED) ==")
    rows = sweeps()
    with open(OUT / "a06_precursor_results.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    d = {(r["N"], r["impl"]): r for r in rows if r["sweep"] == "default"}
    print("\nDefault assumptions: conditional process fidelity (mean +- 95% half-width), transmission, worst-input fidelity")
    print(f"{'N':>3} | {'shared F':>16} {'T':>7} {'worst':>7} | {'individual F':>16} {'T':>7} {'worst':>7}")
    for N in NS:
        s, i = d[(N, "shared")], d[(N, "individual")]
        print(f"{N:>3} | {s['F_cond']:.5f}+-{s['F_cond_hw95']:.5f} {s['transmission']:.4f} {s['worst_input']:.4f} | {i['F_cond']:.5f}+-{i['F_cond_hw95']:.5f} {i['transmission']:.4f} {i['worst_input']:.4f}")
    # crossover in kappa by bisection (log scale; common random numbers because the seed is fixed per N/impl)
    print("\nShared-plate mode dependence kappa* (rad per unit |l|) at which shared conditional fidelity falls to the individual design's (default sorter error):")
    cross = {}
    for N in NS:
        ind = d[(N, "individual")]["F_cond"]
        f = lambda k: run_point(N, "shared", dict(DEFAULT, kappa=k))["F_cond"] - ind
        lo, hi = 1e-4, 1.0
        if f(lo) < 0:
            cross[N] = None
        else:
            for _ in range(30):
                mid = math.sqrt(lo * hi)
                (lo, hi) = (mid, hi) if f(mid) > 0 else (lo, mid)
            cross[N] = math.sqrt(lo * hi)
        edge = (cross[N] * (N - 1)) if cross[N] else None
        print(f"  N={N:>2}: individual F={ind:.5f}; kappa* = {cross[N]:.2e} rad per unit |l|  (retardance error at |l|max = {edge:.3f} rad)")
    print("\nIndividual design sensitivity to Dove-prism rotation error sigma_rot (conditional F), default other parameters:")
    for N in (8, 32):
        print(f"  N={N:>2}: " + ", ".join(f"{r['sigma_rot']:.1e}: {r['F_cond']:.4f}" for r in rows if r["sweep"] == "sigma_rot" and r["N"] == N))
    print("Transmission vs per-element loss (shared / individual), N=8 and N=32:")
    for N in (8, 32):
        print(f"  N={N:>2}: " + ", ".join(f"{r['eps_el']:.0e}: {next(x for x in rows if x['sweep']=='eps_el' and x['N']==N and x['impl']=='shared' and x['eps_el']==r['eps_el'])['transmission']:.3f}/{r['transmission']:.3f}" for r in rows if r["sweep"] == "eps_el" and r["N"] == N and r["impl"] == "individual"))
    c8 = {N: counts(N) for N in NS}
    print("\nOptical elements by stage and task (illustrative counting convention):")
    print(f"{'N':>3} | {'in-place':>17} | {'read pol only':>17} | {'full readout':>17} | cal params | prep (SLM-type / sorter-based)")
    for N in NS:
        c, cal, pr = c8[N]
        f = lambda t: f"{c[t]['shared']['operation'] + c[t]['shared']['after']:>3} vs {c[t]['individual']['operation'] + c[t]['individual']['after']:>3}"
        print(f"{N:>3} | {f('C_in_place'):>17} | {f('A_read_pol_only'):>17} | {f('B_full_readout'):>17} | {cal['shared']} vs {cal['individual']:>3} | {pr['prep_slm']} / {pr['prep_sorter']} (same for both)")
    summary = dict(seed=SEED, reps=REPS, defaults=DEFAULT, evidence="counts DERIVED; all error and loss parameters ASSUMED; preparation and detection fidelity not simulated",
                   default_results={f"{k[0]}_{k[1]}": {m: v[m] for m in ("F_cond", "F_cond_hw95", "F_uncond", "transmission", "worst_input")} for k, v in d.items()},
                   kappa_crossover=cross, aperture_R_over_w={N: math.sqrt(aperture_x(N - 1, DEFAULT["clip"]) / 2) for N in NS},
                   counts={N: dict(by_task=c8[N][0], calibration_parameters=c8[N][1], preparation=c8[N][2]) for N in NS},
                   checks=[dict(name=n, passed=ok, detail=dt) for n, ok, dt in checks])
    (OUT / "a06_precursor_summary.json").write_text(json.dumps(summary, indent=2))
    bad = [n for n, ok, _ in checks if not ok]
    print("\nALL CHECKS PASS" if not bad else f"\n{len(bad)} CHECKS FAILED: {bad}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
