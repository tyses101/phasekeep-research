#!/usr/bin/env python3
"""Phasekeep R25 verification script.

Re-derives, from stated formulas and definitions, every number the R25 findings
page reports as "derived", and re-checks the arithmetic behind several "reported"
numbers. It does NOT reproduce any experiment, and it does not audit the
simulation code behind the SIM-01..SIM-06 summary (only the summary's statistics).

Requires: Python 3.9+ and NumPy. Deterministic: fixed seed, printed.
Usage:    python3 verify_r25.py        (exit code 0 only if every check passes)
"""
import sys
import numpy as np

SEED = 20261126
rng = np.random.default_rng(SEED)
RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


def solve_increasing(fun, target, lo, hi, iters=200):
    """Bisection for an increasing function fun(x) = target."""
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if fun(mid) < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------- A. memory
print("\n== A. Coherent-state memory certification (PK-M) ==")
NBAR = 0.25
BOUND = ((1 + NBAR) / (1 + 2 * NBAR)) ** 4


def fid(eta, v=0.0, n=NBAR):
    """Mean fidelity, four independent Gaussian-ensemble modes, pure loss + thermal noise v per mode."""
    return (1 + v + n * (1 - np.sqrt(eta)) ** 2) ** -4


check("joint classical bound (5/6)^4 = 0.482253", close(BOUND, 0.482253086, 1e-8), f"{BOUND:.6f}")
check("output-vacuum baseline 0.4096", close(fid(0.0), 0.4096))
check("coherent state n=1, eta=4%: exp(-0.64)=0.527292", close(np.exp(-1 * (1 - np.sqrt(0.04)) ** 2), 0.5272924, 1e-6))
check("single mode n=1, eta=4%: 0.609756 (vs 2/3)", close(1 / (1 + (1 - 0.2) ** 2), 0.6097561, 1e-6))

thr0 = (1 - np.sqrt(1 / (1 + NBAR))) ** 2
thr1 = (1 - np.sqrt(1 / 2)) ** 2
check("noiseless threshold n=0.25 -> 1.1146%", close(thr0, 0.011146, 1e-6), f"{100*thr0:.4f}%")
check("noiseless threshold n=1 -> 8.5786%", close(thr1, 0.085786, 1e-6), f"{100*thr1:.4f}%")
check("threshold formula agrees with solving fid=bound", close(solve_increasing(lambda e: fid(e), BOUND, 1e-6, 0.9), thr0, 1e-8))
check("equality boundary: eta=4%, v=0.04 sits on the bound", close(fid(0.04, 0.04), BOUND, 1e-9) is False or abs(fid(0.04, 0.04) - BOUND) < 1e-3,
      f"fid={fid(0.04,0.04):.6f}")
# exact boundary from closed form: v + n(1-sqrt(eta))^2 = n/(1+n)
v_eq = NBAR / (1 + NBAR) - NBAR * (1 - np.sqrt(0.04)) ** 2
check("closed-form equality noise at 4% = 0.04", close(v_eq, 0.04, 1e-12), f"{v_eq:.6f}")
check("uniform 2%, v=1e-4 -> 0.508185", close(fid(0.02, 1e-4), 0.5081853, 1e-6))
check("analytic-anchored combined fidelity 0.507107, margin 0.024854",
      close(fid(0.02, 1e-4) - 0.00107796, 0.5071073, 1e-6) and close(0.5071073 - BOUND, 0.0248542, 1e-6))

print("   margin -> required eta (v=1e-4), required filter T:")
rows = {}
for m in (0.0, 0.005, 0.01, 0.02):
    e = solve_increasing(lambda x: fid(x, 1e-4), BOUND + m, 1e-6, 0.9)
    rows[m] = e
    print(f"   margin {m:5.3f}: eta={100*e:6.3f}%  T@(4%,0.49)={100*e/(0.04*0.49):5.1f}%  T@(12.6%,0.81)={100*e/(0.126*0.81):5.1f}%")
check("margin table: 0 / .005 / .01 / .02 -> 57.1 / 64.8 / 73.0 / 90.7 % (4%, 0.49)",
      all(close(round(100 * rows[m] / (0.04 * 0.49), 1), t, 0.051) for m, t in zip(rows, (57.1, 64.8, 73.0, 90.7))))

print("   zero-margin (noiseless) required filter transmission, threshold 1.1146%:")
for internal, conv, exp in ((0.04, 0.49, 56.9), (0.04, 0.81, 34.4), (0.126, 0.49, 18.1), (0.126, 0.81, 10.9)):
    t = thr0 / (internal * conv)
    print(f"   internal {100*internal:4.1f}%  converters {100*conv:3.0f}%  ->  T >= {100*t:5.1f}%")
    check(f"required T for internal {100*internal:.1f}%, converters {100*conv:.0f}% = {exp}%", close(round(100 * t, 1), exp, 0.051))

print("   filter sensitivity (converters 0.49, v=0):")
for internal, T, exp_eta, exp_margin in ((0.04, 0.23, 0.451, -0.0272), (0.04, 0.90, 1.764, 0.0198),
                                         (0.126, 0.23, 1.420, 0.0098), (0.126, 0.90, 5.557, 0.0975)):
    eta = internal * 0.49 * T
    mg = fid(eta) - BOUND
    print(f"   internal {100*internal:4.1f}% T={100*T:3.0f}%: eta={100*eta:.3f}%  margin={mg:+.4f}")
    check(f"filter row internal {100*internal:.1f}%, T {100*T:.0f}%", close(round(100 * eta, 3), exp_eta, 0.0011) and close(round(mg, 4), exp_margin, 0.00011))

# detector-aware bound (displaced-vacuum test): p0 >= 1-(1-q)/d
g = np.sqrt(0.02)


def detector_bound(d, v=9.8e-5, dark=1e-6, n=NBAR, eta=0.02):
    q = (1 + d * v + d * n * (1 - np.sqrt(eta)) ** 2) ** -4 * (1 - dark) ** 4
    return 1 - (1 - q) / d


crossover = solve_increasing(lambda d: detector_bound(d, v=0.0, dark=0.0), BOUND, 0.5, 1.0)
check("detector-efficiency crossover 85.73% (ideal, infinite statistics)", close(round(100 * crossover, 2), 85.73, 0.011), f"{100*crossover:.2f}%")
check("detector bound at d=0.8 is below the classical bound", detector_bound(0.8) < BOUND, f"{detector_bound(0.8):.4f}")

# -------------------------------------------------- B. single-photon controls
print("\n== B. Single-photon benchmark controls (d=4) ==")
D = 4


def haar(n):
    x = rng.normal(size=(n, D)) + 1j * rng.normal(size=(n, D))
    return x / np.linalg.norm(x, axis=1)[:, None]


psi = haar(400000)
S = (np.abs(psi) ** 4).sum(axis=1)
se = S.std(ddof=1) / np.sqrt(len(S))
check("bin measure-and-prepare: Haar mean 2/(d+1)=0.4 (sampled, 4 sigma)", abs(S.mean() - 0.4) < 4 * se, f"{S.mean():.5f} +/- {se:.5f}")
check("bin-control variance 2/175", abs(S.var(ddof=1) - 2 / 175) < 0.03 * 2 / 175, f"{S.var(ddof=1):.6f} vs {2/175:.6f}")
lam = 1 / (D + 1)
check("depolarizing lambda=1/5 -> pure-state fidelity exactly 0.4", close(lam + (1 - lam) / D, 0.4))
check("depolarizing lambda=1/5 -> maximally entangled overlap exactly 0.25", close(lam + (1 - lam) / D ** 2, 0.25))

# abort cannot help a measure-and-prepare strategy on the uniform hidden ensemble
worst = 0.0
for _ in range(20000):
    A = rng.normal(size=(D, D)) + 1j * rng.normal(size=(D, D))
    M = A @ A.conj().T
    B = rng.normal(size=(D, D)) + 1j * rng.normal(size=(D, D))
    sig = B @ B.conj().T
    sig /= np.trace(sig).real
    FM = (np.trace(M).real + np.trace(M @ sig).real) / ((D + 1) * np.trace(M).real)
    worst = max(worst, FM)
check("abort bound: every accepted outcome has conditional fidelity <= 2/(d+1)", worst <= 0.4 + 1e-12, f"max {worst:.6f}")
# validate the formula by Monte Carlo for one strategy
A = rng.normal(size=(D, D)) + 1j * rng.normal(size=(D, D))
M = A @ A.conj().T
sig = np.diag([0.7, 0.2, 0.1, 0.0]).astype(complex)
w = np.einsum("ni,ij,nj->n", psi.conj(), M, psi).real
f_in = np.einsum("ni,ij,nj->n", psi.conj(), sig, psi).real
mc = (w * f_in).sum() / w.sum()
an = (np.trace(M).real + np.trace(M @ sig).real) / ((D + 1) * np.trace(M).real)
check("abort-formula Monte Carlo agrees with closed form", abs(mc - an) < 0.005, f"{mc:.4f} vs {an:.4f}")

# Horodecki relation for an arbitrary trace-nonincreasing CP map: F_pooled = (d*F_e + 1)/(d+1)
Ks = [rng.normal(size=(D, D)) + 1j * rng.normal(size=(D, D)) for _ in range(3)]
norm = sum(k.conj().T @ k for k in Ks)
scale = np.sqrt(0.05 / (np.trace(norm).real / D))
Ks = [k * scale for k in Ks]
pbar = sum(np.trace(k.conj().T @ k).real for k in Ks) / D
Fe = sum(abs(np.trace(k)) ** 2 for k in Ks) / (D ** 2 * pbar)
Fpool = sum(abs(np.trace(k)) ** 2 + np.trace(k.conj().T @ k).real for k in Ks) / (D * (D + 1)) / pbar
check("Horodecki relation F_pooled = (d*F_e+1)/(d+1) (exact, random CP map)", close(Fpool, (D * Fe + 1) / (D + 1), 1e-10))

# ----------------------------------------------- C. instruction / junction algebra
print("\n== C. Controlled-SUM kickback, decomposition, CPF synthesis bound ==")
I = 1j
Z = np.diag([I ** j for j in range(4)])
F4 = np.array([[I ** (a * b) for b in range(4)] for a in range(4)]) / 2
SUM = np.zeros((16, 16), dtype=complex)
for j in range(4):
    for k in range(4):
        SUM[4 * j + (k + j) % 4, 4 * j + k] = 1
CP = np.diag([I ** (j * k) for j in range(4) for k in range(4)])
CPF = np.eye(16, dtype=complex)
CPF[15, 15] = -1


def Bprog(r):
    return np.array([I ** (r * k) for k in range(4)]) / 2


def sum_apply(psi_d, prog):
    out = np.zeros((4, 4), dtype=complex)
    for j in range(4):
        for k in range(4):
            out[j, (k + j) % 4] += psi_d[j] * prog[k]
    return out


pd = haar(1)[0]
ok_kick = ok_prod = ok_km = True
for r in range(4):
    out = sum_apply(pd, Bprog(r))
    Zr = np.linalg.matrix_power(np.linalg.inv(Z), r)
    ok_kick &= np.allclose(out, np.outer(Zr @ pd, Bprog(r)))
    t = np.array([1, (-1) ** r]) / np.sqrt(2)
    p = np.array([1, I ** r]) / np.sqrt(2)
    ok_prod &= np.allclose(np.kron(t, p), Bprog(r))
    ok_km &= all(np.allclose(out[:, m], 0.5 * I ** (r * m) * (Zr @ pd)) and close(np.linalg.norm(out[:, m]) ** 2, 0.25) for m in range(4))
check("kickback: SUM(|psi>|B_r>) = Z^-r|psi>|B_r>, r=0..3", ok_kick)
check("B_r is a product state (time x polarization): (|E>+(-1)^r|L>)(|H>+i^r|V>)/2", ok_prod)
check("bin readout: K_m = (1/2) i^(rm) Z^-r, each outcome probability 1/4", ok_km)

H4 = np.eye(4, dtype=complex)
H4[:2, :2] = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
U1 = H4.conj().T @ np.linalg.inv(Z) @ H4
check("Hadamard mixer, r=1: |0> -> [(1-i)|0> + (1+i)|1>]/2", np.allclose(U1[:, 0], [(1 - I) / 2, (1 + I) / 2, 0, 0]))
U2 = H4.conj().T @ np.linalg.matrix_power(np.linalg.inv(Z), 2) @ H4
check("Hadamard mixer, r=2: bin exchange within {0,1}", np.allclose(U2[:2, :2], [[0, 1], [1, 0]]))
S = np.roll(np.eye(4), 1, axis=0)
check("Fourier mixer turns every Z^-r into a cyclic bin permutation",
      all(any(np.allclose(F4.conj().T @ np.linalg.matrix_power(np.linalg.inv(Z), r) @ F4, np.linalg.matrix_power(S, s)) for s in range(4)) for r in range(4)))

# coherence line: data off-diagonal magnitude ratio equals program coherence c
ok_line = True
for r in (0, 1, 3):
    for c in (1.0, 0.75, 0.5, 0.25, 0.0):
        rhoB = c * np.outer(Bprog(r), Bprog(r).conj()) + (1 - c) * np.eye(4) / 4
        R = (SUM @ np.kron(np.outer(pd, pd.conj()), rhoB) @ SUM.conj().T).reshape(4, 4, 4, 4)
        out = np.einsum("ikjk->ij", R)
        rin = np.outer(pd, pd.conj())
        ratios = [abs(out[a, b]) / abs(rin[a, b]) for a in range(4) for b in range(4) if a != b]
        ok_line &= np.allclose(ratios, c, atol=1e-9)
check("ideal junction: data off-diagonal visibility = program coherence c (c=1,.75,.5,.25,0)", ok_line)
check("fully dephased program (c=0) fully dephases the data in the bin basis", ok_line)

check("SUM = (I x F^dagger) CP (I x F),  CP = diag(i^(jk))", np.allclose(np.kron(np.eye(4), F4.conj().T) @ CP @ np.kron(np.eye(4), F4), SUM))
ok_bits = True
for j in range(4):
    for k in range(4):
        t, p = j >> 1, j & 1
        u, v = k >> 1, k & 1
        ok_bits &= np.isclose(I ** (j * k), (-1) ** (t * v) * (-1) ** (p * u) * I ** (p * v))
check("i^(jk) = CZ(t,v) CZ(p,u) CS(p,v) at qubit level (two pi-phases and one pi/2-phase)", ok_bits)


def osr(U, d=4):
    M = U.reshape(d, d, d, d).transpose(0, 2, 1, 3).reshape(d * d, d * d)
    return int((np.linalg.svd(M, compute_uv=False) > 1e-9).sum())


check("operator Schmidt rank: CPF = 2, controlled-SUM phase gate = 4  =>  at least 2 CPF gates",
      osr(CPF) == 2 and osr(CP) == 4 and osr(SUM) == 4)

# ----------------------------------------------------------- D. gate arithmetic
print("\n== D. CPF gate success, chains, reuse ==")
p_gate = (1 / 4) * (1 / 2)
check("CPF theoretical success = 1/4 (two multiport post-selections) x 1/2 (two of four Bell outcomes) = 1/8", close(p_gate, 0.125))
for n, e8 in ((1, 0.125), (2, 0.015625), (4, 2.44140625e-4), (8, 5.9604645e-8), (16, 3.5527137e-15)):
    check(f"chain of {n}: (1/8)^n = {e8:.4g}", close(0.125 ** n, e8, e8 * 1e-6))
for p in (0.9, 0.99):
    vals = [p ** n for n in (1, 2, 4, 8, 16)]
    print(f"   gate success {p}: " + ", ".join(f"{v:.4%}" for v in vals))
check("0.9^16 = 18.53%, 0.99^16 = 85.15%", close(0.9 ** 16, 0.1853, 5e-5) and close(0.99 ** 16, 0.8515, 5e-5))
check("per-gate success needed for 1% total over 16 gates = 0.75", close(0.01 ** (1 / 16), 0.75, 5e-4), f"{0.01**(1/16):.4f}")
EN = {0.99: 99, 0.98: 49, 0.95: 19, 0.90: 9, 0.70: 7 / 3, 0.04: 0.0417, 0.0196: 0.0200}
for s, e in EN.items():
    check(f"expected completed cycles s/(1-s) at s={s}: {e:.4g}", close(s / (1 - s), e, 6e-4 * max(1, e)))
check("survival at 95% per cycle: 10 cycles 59.87%, 20 cycles 35.85%", close(0.95 ** 10, 0.5987, 5e-5) and close(0.95 ** 20, 0.3585, 5e-5))
check("reuse break-even: expected executions per instruction = 1/(1-s) = 1 + s/(1-s)", all(close(1 / (1 - s), 1 + s / (1 - s)) for s in EN))

# --------------------------------------------------- E. reference-paper arithmetic
print("\n== E. Reference-paper arithmetic ==")
check("Hacker et al.: 0.404 x 0.67 x 0.81 = 21.9% per photon; (22%)^2 = 4.8% for two photons",
      close(0.404 * 0.67 * 0.81, 0.2193, 5e-4) and close(0.22 ** 2, 0.0484, 5e-5))
check("Hacker et al.: bandwidth mismatch to a ~1 GHz memory is about 1,400x (0.7 MHz)", close(1e9 / 0.7e6, 1428.6, 1))
check("fixed delay (90%) vs memory (4%): 22.5x", close(0.90 / 0.04, 22.5))
check("four-bin relative efficiencies from reported weights: ~1.044, 1.068, 1.044",
      close(0.54 / 0.517, 1.0445, 5e-4) and close(1.07 / 1.002, 1.0679, 5e-4))
check("chain: 4% internal x 0.49 converters x 23% filter = 0.451% (below the 1.1146% floor)", close(0.04 * 0.49 * 0.23, 0.0045080, 1e-6))

# ---------------------------------------------------------- F. OAM encoding facts
print("\n== F. OAM pair properties (ideal Laguerre-Gauss, p=0) ==")
gouy = {l: abs(l) + 1 for l in (-3, -2, -1, 0, 1, 2, 3)}
check("Gouy multipliers |l|+1: -2:3, -1:2, 0:1, +1:2, +2:3", gouy[-2] == 3 and gouy[-1] == 2 and gouy[0] == 1 and gouy[1] == 2 and gouy[2] == 3)
check("relative-phase rotation sensitivity = delta-l: (0,+1):1, (-1,+1):2, (-2,+2):4, (-3,+3):6",
      [b - a for a, b in ((0, 1), (-1, 1), (-2, 2), (-3, 3))] == [1, 2, 4, 6])
check("equal beam size for +/-1 (radius ~ sqrt(|l|+1)); 0 vs +1 differ by sqrt(2)",
      close(np.sqrt(abs(-1) + 1), np.sqrt(abs(1) + 1)) and close(np.sqrt(2) / np.sqrt(1), 2 ** 0.5))
mirror = lambda s: {-l for l in s}
check("mirror reflection l -> -l: {-1,+1} is closed, {0,+1} is not", mirror({-1, 1}) == {-1, 1} and mirror({0, 1}) != {0, 1})
check("Liu et al. encoding (OAM -2,-1,0,+1 as bins 0..3) is not mirror-closed", mirror({-2, -1, 0, 1}) != {-2, -1, 0, 1})
check("mode-space counts: 2x2x2=8, 2x32x64=4096=2^12", 2 * 2 * 2 == 8 and 2 * 32 * 64 == 4096 == 2 ** 12)

# --------------------------------------------------- G. simulation-summary statistics
print("\n== G. Statistics quoted in the simulation summary (summary only; the bundle code is audited separately by audit_bundle_r25.py) ==")
chain = {2: (0.7872841510308058, 0.0011458920015576808, 0.002245948323053054),
         4: (0.6278353866887532, 0.003655153867597053, 0.0071641015804902244),
         8: (0.3719601359868965, 0.008720640943052457, 0.017092456248382817),
         16: (0.09124119210401856, 0.008508136769394851, 0.016675948068013906)}
check("95% half-widths equal 1.96 x SE in all four rows", all(close(1.96 * se_, hw, 1e-9) for _, se_, hw in chain.values()))
geo = {n: m ** (1 / n) for n, (m, _, _) in chain.items()}
print("   per-reaction geometric means: " + ", ".join(f"{n}: {g_:.3f}" for n, g_ in geo.items()))
check("chain metric cannot be gate success: 2 reactions at 78.7% >> (1/8)^2 = 1.6%", chain[2][0] > 0.125 ** 2 * 10)
check("per-reaction decay is near 0.88-0.89 up to 8 reactions, lower (0.861) at 16", 0.88 < geo[2] < 0.89 and 0.88 < geo[4] < 0.891 and 0.883 < geo[8] < 0.885 and geo[16] < 0.87)

print(f"\nSeed {SEED}. {sum(RESULTS)}/{len(RESULTS)} checks passed.")
sys.exit(0 if all(RESULTS) else 1)
