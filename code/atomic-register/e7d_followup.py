"""E7-D follow-ups.
(1) Matched-envelope verification: full notch vs uneven-only with the uneven amplitude multiplied by the same scale
    -> final unitaries should agree to roundoff (uniform part factors out).
(2) Balance hypothesis: second-order dressing phase from the uneven interaction ~ int dV^2 / E with E changing sign
    with the hopping. It cancels only if int g(t)^2 dt is equal over the +hopping and -hopping periods.
    Tests (alpha=0.5, no drift):
      sym-seg          : 3 sin^2 segments (balanced)                       [reference from E7: 1.4e-5]
      sym-cont-notch   : continuous sin^2 + full notches (unbalanced)       [E7-D: ~1.8e-3]
      orig-cont-notch  : continuous sin^2, flips at 1/2 and 1, notch at 1/2 (balanced by mirror symmetry)
      sym-flat-notch   : flat-top envelope (sin^2 ramps 0.1T) + notches at 1/4, 3/4 (balanced: equal +/- durations)
    Also reports the +/- imbalance of int g^2 and the max envelope slope in physical units (J_B/h = 1 MHz)."""
import numpy as np, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cim_core import operators, metrics, expmh
ops = operators(); v = 0.1; T = 2*np.pi/v; STEPS = 2400; dt = T/STEPS
t = (np.arange(STEPS) + 0.5)*dt
rc = lambda x: np.where(np.abs(x) < 1, 0.5*(1 + np.cos(np.pi*x)), 0.0)
def notch(flips, w, r=0.0):
    n = np.ones_like(t)
    for tf in flips: n *= 1 - (1 - r)*rc((t - tf*T)/(w*T/2))
    return n
def run_env(gu, gd, flips, alpha=0.5):
    """gu: envelope of uniform part, gd: envelope of uneven part (already scaled)."""
    U = np.eye(64, dtype=complex); k = 0
    for i in range(STEPS):
        U = expmh(ops["H0"] + gu[i]*ops["Vbar"] + gd[i]*alpha*ops["Vdev"], dt) @ U
        while k < len(flips) and (i + 1)*dt >= flips[k]*T - 1e-9: U = ops["FAB"] @ U; k += 1
    return U
area = lambda g: v*np.sum(g)*dt
def norm_env(g): return g*np.pi/area(g)
def sign_of_hop(flips):
    s = np.ones_like(t);
    for tf in flips: s[t > tf*T] *= -1
    return s
def imbalance(g, flips):
    s = sign_of_hop(flips); return np.sum(s*g**2)/np.sum(g**2)
def max_slope(g):                                   # in units of v per (1/J_B); convert: v = 0.1 J_B, 1/J_B = 159 ns
    return np.max(np.abs(np.diff(v*g)))/dt         # J_B^2 units
SYM, ORIG = [0.25, 0.75], [0.5, 1.0]
base = np.sin(np.pi*t/T)**2
Ut = run_env(norm_env(base), 0*base, SYM, alpha=0.0)
# (1) matched envelope
g_full = norm_env(base*notch(SYM, 0.2)); g_unif = norm_env(base)
U_full = run_env(g_full, g_full, SYM); U_match = run_env(g_unif, g_full, SYM)
print(f"(1) matched-envelope: ||U_full - U_match|| = {np.linalg.norm(U_full - U_match):.2e}  (full-notch peak factor {g_full.max()/g_unif.max():.3f})")
# (2) balance tests
segs = [(0, .25), (.25, .75), (.75, 1)]
g_seg = np.zeros_like(t)
for a, b in segs:
    m = (t >= a*T) & (t < b*T); g_seg[m] = np.sin(np.pi*(t[m] - a*T)/((b - a)*T))**2
ramp = np.clip(np.minimum(t, T - t)/(0.1*T), 0, 1); flat = np.sin(np.pi*ramp/2)**2
cases = {"sym-seg": (g_seg, SYM), "sym-cont-notch": (base*notch(SYM, 0.2), SYM),
         "orig-cont-notch": (base*notch([0.5], 0.2), ORIG), "sym-flat-notch": (flat*notch(SYM, 0.2), SYM),
         "sym-flat-notch w=0.1": (flat*notch(SYM, 0.1), SYM)}
for name, (g, fl) in cases.items():
    g = norm_env(g); inf, lk = metrics(run_env(g, g, fl), Ut)
    sl = max_slope(g)   # mean-interaction energy (units J_B, i.e. h x 1 MHz) per time unit 1/J_B (= 159 ns at J_B/h = 1 MHz)
    print(f"(2) {name:22s} imbalance {imbalance(g, fl):+.3f}  infidelity {inf:.2e}  leakage {lk:.2e}  peak/v {g.max():.2f}  "
          f"max d<V>/dt = {sl:.4f} J_B per (1/J_B)  (= {sl/0.159155:.3f} MHz/us at J_B/h = 1 MHz)")
