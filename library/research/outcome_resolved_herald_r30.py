#!/usr/bin/env python3
"""Outcome-resolved herald analysis of the Codex feasibility bundle (R30 proposal).

Usage:  python3 -I outcome_resolved_herald_r30.py /path/to/extracted/bundle [--allow-modified]
Needs only numpy. READ-ONLY with respect to the bundle: it imports nothing from the bundle's
scripts except the three public optics functions (network, scatter, fock_basis), loaded by
executing optics.py in memory. It does not run run_suite.py or verify_suite.py.

Method (behavioral, not source-layout dependent):
  1. Build the modeled scattering network with optics.network(d) and propagate each logical
     input (one photon per register, plus two auxiliary photons each in (p+r)/sqrt2 ... exactly as
     the bundle's instrument prepares them) with optics.scatter.
  2. Classify every output Fock state by the auxiliary detector outcome class (u,v) of ideal
     photon-number-resolving detection, and by whether the computational output is occupancy-valid
     (exactly one photon in each register). This is this script's OWN aggregation.
  3. Cross-check it against the bundle's saved simulation results (results/sim04_raw.npz,
     sim04_gate.json), including 256 saved random (Haar) superposition inputs, and against the
     bundle's own optics.instrument(d) total herald operator.

TERMINOLOGY: "occupancy-valid" means exactly one photon in each computational output register. It is a
photon-number condition only. It does not certify state fidelity, coherence or correctness of the operation.
"Logical inputs" are the d*d inputs with one photon per register (and their superpositions); inputs with
vacuum or bunched computational occupancy, and loss, are outside this analysis.

SCOPE (read before quoting): exploratory and specific to the bundle's reconstruction (ideal PNR
auxiliary detectors; selector, auxiliary Hadamard, PBS and analyzer as modeled). It does not show
that the reconstruction matches the published apparatus (audit item A02), covers no other
analyzer arrangement, and is not independently reviewed. Shared scattering matrix: this tests
aggregation and consistency, not the physics mapping.
"""
import hashlib, itertools, math, sys, types
from collections import defaultdict
from pathlib import Path
import numpy as np

# ---- declared tolerances -------------------------------------------------------------------
TOL_PROB = 1e-10      # probabilities, norms, agreement with saved results
TOL_EQ = 1e-12        # exact equalities that should hold to rounding
TOL_BOUND = 1e-9      # eigenvalue-based reliability bounds
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
ROOT = Path(ARGS[0] if ARGS else ".")
ALLOW_MODIFIED = "--allow-modified" in sys.argv

# ---- guard: bundle integrity ---------------------------------------------------------------
sums = {}
for line in (ROOT / "SHA256SUMS.txt").read_text().splitlines():
    if line.strip():
        h, name = line.split(None, 1)
        sums[name.strip().lstrip("*")] = h
needed = ["optics.py", "results/sim04_raw.npz", "results/sim04_gate.json"]
bad = [n for n in needed if hashlib.sha256((ROOT / n).read_bytes()).hexdigest() != sums.get(n)]
print("bundle files used:", ", ".join(f"{n} sha256={sums[n][:12]}..." for n in needed))
print(f"tolerances: prob {TOL_PROB}, equality {TOL_EQ}, bound {TOL_BOUND}")
if bad and not ALLOW_MODIFIED:
    sys.exit(f"GUARD: bundle files do not match SHA256SUMS.txt: {bad} (use --allow-modified to override)")

optics = types.ModuleType("optics_bundle")
exec(compile((ROOT / "optics.py").read_text(), "optics_bundle", "exec"), optics.__dict__)
saved_gate = __import__("json").loads((ROOT / "results/sim04_gate.json").read_text())
saved_raw = np.load(ROOT / "results/sim04_raw.npz")

fails = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))
    if not ok:
        fails.append(name)


def whitened_reliability_range(E, G):
    """min/max over inputs with nonzero herald of <psi|G|psi>/<psi|E|psi>."""
    w, V = np.linalg.eigh((E + E.conj().T) / 2)
    keep = w > 1e-10
    B = V[:, keep] / np.sqrt(w[keep])
    M = B.conj().T @ G @ B
    ev = np.linalg.eigvalsh((M + M.conj().T) / 2)
    return ev.min(), ev.max()


def outcome_resolved(d):
    """Own aggregation. Returns dict with per-(u,v) E,G operators on the d*d logical inputs,
    plus conservation bookkeeping. Ports: 0..d-1 A-left, d..2d-1 aux1, 2d..3d-1 B-left-comp... as in optics.network."""
    p, r = 1, d - 1
    U = optics.network(d)
    det_modes = (d + p, d + r, 3 * d + p, 3 * d + r)
    n_in = d * d
    rows = defaultdict(lambda: np.zeros(n_in, complex))        # out Fock state -> amplitude per logical input
    for a, b in itertools.product(range(d), repeat=2):
        col = a * d + b
        inputs = (a, 2 * d + b)                                  # register A mode a; register B mode b (port 2d+b)
        state = defaultdict(complex)
        for aa, bb in itertools.product((p, r), repeat=2):       # auxiliary photons: equal superposition over p,r
            for out, amp in optics.scatter(inputs + (d + aa, 3 * d + bb), U).items():
                state[out] += amp / 2
        for out, amp in state.items():
            rows[out][col] = amp
    E = {uv: np.zeros((n_in, n_in), complex) for uv in itertools.product((0, 1), repeat=2)}
    G = {uv: np.zeros((n_in, n_in), complex) for uv in E}
    total_mass = np.zeros(n_in)
    offcode = np.zeros(n_in)
    nomatch = np.zeros(n_in)
    for out, row in rows.items():
        total_mass += np.abs(row) ** 2
        det = [x for x in out if x // d in (1, 3)]
        if any(x not in det_modes for x in det):                 # off-code auxiliary mode: rejected
            offcode += np.abs(row) ** 2
            continue
        counts = [det.count(x) for x in det_modes]
        hit = False
        for u, v in itertools.product((0, 1), repeat=2):
            want = [int(u == 0), int(u == 1), int(v == 0), int(v == 1)]
            if counts == want:                                   # ideal PNR: exact click pattern
                hit = True
                outer = np.outer(row.conj(), row)
                E[(u, v)] += outer
                comp = sorted(x if x < d else x - d for x in out if x // d in (0, 2))
                if len(comp) == 2 and comp[0] < d <= comp[1]:     # one photon in each register
                    G[(u, v)] += outer
        if not hit:
            nomatch += np.abs(row) ** 2
    return dict(E=E, G=G, total=total_mass, offcode=offcode, nomatch=nomatch)


for d in (4, 8):
    print(f"\n=== d = {d} ===")
    R = outcome_resolved(d)
    n_in = d * d
    E_tot = sum(R["E"].values())
    G_tot = sum(R["G"].values())
    h, v = np.real(np.diag(E_tot)), np.real(np.diag(G_tot))

    # 1. conservation of probability across all output sectors
    herald_mass = h
    check(f"d={d}: probability conserved: herald + off-code rejected + other click patterns = total = 1 for every input",
          np.allclose(R["total"], 1, atol=TOL_PROB)
          and np.allclose(herald_mass + R["offcode"] + R["nomatch"], R["total"], atol=TOL_PROB),
          f"max |total-1| = {np.max(abs(R['total'] - 1)):.1e}")

    # 2. agreement with the original simulation
    inst = optics.instrument(d)
    g = inst["good"]
    check(f"d={d}: own total herald operator equals the bundle's optics.instrument(d)['E'] on the logical block",
          np.max(abs(E_tot - inst["E"][np.ix_(g, g)])) < TOL_PROB,
          f"max dev {np.max(abs(E_tot - inst['E'][np.ix_(g, g)])):.1e}")
    X = saved_raw[f"d{d}_inputs"]                                # all 16/64 basis + 256 saved Haar inputs
    h_saved, g_saved = saved_raw[f"d{d}_herald"], saved_raw[f"d{d}_good"]
    h_mine = np.real(np.sum(X.conj() * (E_tot @ X), axis=0))
    g_mine = np.real(np.sum(X.conj() * (G_tot @ X), axis=0))
    check(f"d={d}: herald probability agrees with saved results on all {X.shape[1]} saved inputs (basis + random superpositions)",
          np.max(abs(h_mine - h_saved)) < TOL_PROB, f"max dev {np.max(abs(h_mine - h_saved)):.1e}")
    check(f"d={d}: occupancy-valid-output probability agrees with saved results on all {X.shape[1]} saved inputs",
          np.max(abs(g_mine - g_saved)) < TOL_PROB, f"max dev {np.max(abs(g_mine - g_saved)):.1e}")
    ce = saved_gate[str(d)]["counterexample"]
    i = (d - 1) * d
    check(f"d={d}: counterexample |{d-1},0> matches sim04_gate.json (herald, occupancy-valid, false)",
          abs(h[i] - ce["herald_probability"]) < TOL_PROB and abs(v[i] - ce["valid_two_register_probability"]) < TOL_PROB
          and abs((h[i] - v[i]) - ce["false_herald_probability"]) < TOL_PROB)

    # 3. equal distribution of herald / valid / false mass over the four outcome classes
    print(f"   outcome class (u,v): raw herald / occupancy-valid / false for input |{d-1},0>")
    for uv in sorted(R["E"]):
        e, gg = R["E"][uv][i, i].real, R["G"][uv][i, i].real
        print(f"     {uv}: {e:.6f} / {gg:.6f} / {e - gg:.6f}")
    dev_e = max(np.max(abs(R["E"][uv] - E_tot / 4)) for uv in R["E"])
    dev_g = max(np.max(abs(R["G"][uv] - G_tot / 4)) for uv in R["G"])
    false_cls = [(R["E"][uv] - R["G"][uv]) for uv in R["E"]]
    dev_f = max(np.max(abs(f - (E_tot - G_tot) / 4)) for f in false_cls)
    check(f"d={d}: herald, occupancy-valid and false mass are each split equally (1/4) over the four outcome classes, as operators on ALL logical inputs",
          max(dev_e, dev_g, dev_f) < TOL_EQ, f"max dev {max(dev_e, dev_g, dev_f):.1e}")

    # 4. identical reliability across classes (selected input and worst case over all inputs)
    rel_sel = [R["G"][uv][i, i].real / R["E"][uv][i, i].real for uv in sorted(R["E"])]
    check(f"d={d}: reliability for |{d-1},0> is 1/3 in every outcome class", np.allclose(rel_sel, 1 / 3, atol=TOL_EQ),
          ", ".join(f"{x:.6f}" for x in rel_sel))
    lo_all, hi_all = whitened_reliability_range(E_tot, G_tot)
    lo_cls = [whitened_reliability_range(R["E"][uv], R["G"][uv])[0] for uv in sorted(R["E"])]
    check(f"d={d}: worst-case reliability over all logical inputs (superpositions included) = 1/3, overall and in each class",
          abs(lo_all - 1 / 3) < TOL_BOUND and abs(hi_all - 1) < TOL_BOUND and all(abs(x - 1 / 3) < TOL_BOUND for x in lo_cls),
          f"overall {lo_all:.6f}..{hi_all:.6f}")

    # 5. throughput versus reliability when discarding classes
    print("   keep k classes -> herald probability / reliability, input |%d,0>:" % (d - 1))
    for k in (4, 3, 2, 1):
        hh = k * R["E"][(0, 0)][i, i].real
        vv = k * R["G"][(0, 0)][i, i].real
        print(f"     k={k}: {hh:.6f} / {vv / hh:.6f}")

    # 6. controls and which inputs are affected
    ctrl = [0, n_in - 1]                                         # |0,0> and |d-1,d-1>
    check(f"d={d}: zero false-herald mass for the two control inputs |0,0> and |{d-1},{d-1}> (and occupancy-valid = 1/8)",
          all(abs(h[c] - v[c]) < TOL_PROB and abs(v[c] - .125) < TOL_PROB for c in ctrl))
    affected = [k for k in range(n_in) if h[k] - v[k] > 1e-9]
    check(f"d={d}: false heralds only on inputs |{d-1},j>, j<{d-1}, each exactly 0.25",
          affected == [(d - 1) * d + j for j in range(d - 1)] and np.allclose(h[affected] - v[affected], .25, atol=TOL_PROB),
          f"{len(affected)} of {n_in} basis inputs")

print("\nInterpretation limits: ideal PNR auxiliary detectors only; imperfect detectors, other analyzer arrangements, "
      "and the mapping to the published apparatus (A02) are NOT tested. In this reconstruction the outcome LABEL carries no "
      "information about occupancy validity; occupancy validity (one photon per register) is not state fidelity or coherence, and this does not exclude other verification measurements (BV-03..05).")
print("\nALL PASS" if not fails else f"\n{len(fails)} FAILED: {fails}")
sys.exit(0 if not fails else 1)
