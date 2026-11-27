#!/usr/bin/env python3
"""Draft Physical Architecture Specification, component records (Tetragon: H/V x OAM {-1,+1}).

Run: python3 -I build_spec_draft.py [outdir]   (numpy only; exit 0 only if every math/closure claim below checks out)

Every operation and closure entry in the CSV is checked numerically here, so the "DERIVED" tag means the claim was
computed, not asserted. Costs, compatibility limits and sources are NOT filled in unless stated: they are TBD or
'unverified' and must not be read as evidence. Nothing here is a verified equipment specification.
"""
import csv, math, sys, itertools
from pathlib import Path
import numpy as np

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "spec_out")
OUT.mkdir(parents=True, exist_ok=True)
checks = []


def check(name, ok, detail=""):
    checks.append((name, bool(ok)))
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))


I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], complex)
Z = np.diag([1, -1]).astype(complex)


def retarder(gamma, theta):
    """Jones matrix of a linear retarder: retardance gamma, fast axis at angle theta from H (H/V basis), up to nothing."""
    n_z, n_x = math.cos(2 * theta), math.sin(2 * theta)
    return math.cos(gamma / 2) * I2 - 1j * math.sin(gamma / 2) * (n_z * Z + n_x * X)


def same_up_to_phase(A, B):
    k = np.vdot(B.flatten(), A.flatten())
    return abs(abs(k) - np.linalg.norm(A) * np.linalg.norm(B)) < 1e-12 and abs(abs(k) - np.linalg.norm(A) ** 2) < 1e-12


# 1. half-wave plate at 45 deg = -iX
hwp = retarder(math.pi, math.pi / 4)
check("HWP at 45 deg equals -iX exactly (global phase -i)", np.max(abs(hwp - (-1j) * X)) < 1e-12)
# 2. QWP(0 deg) is a polarization phase gate; two QWPs = HWP at 0 deg = Z up to phase
q0 = retarder(math.pi / 2, 0.0)
check("QWP at 0 deg is a unitary phase gate diag(e^-i pi/4, e^+i pi/4) (relative phase i between H and V)", np.max(abs(q0 - np.diag([np.exp(-1j * math.pi / 4), np.exp(1j * math.pi / 4)]))) < 1e-12)
check("two QWPs at 0 deg equal a HWP at 0 deg (= -iZ)", np.max(abs(q0 @ q0 - (-1j) * Z)) < 1e-12)

# 3. OAM operations on the basis {-1,+1} versus the control pair {0,+1} (modes are integers l)


def reflection(l):          # image reflection: l -> -l
    return -l


def rotation_phase(l, phi):  # image rotation by phi (sign convention chosen: exp(-i l phi))
    return np.exp(-1j * l * phi)


for name, basis in (("{-1,+1}", [-1, 1]), ("{0,+1}", [0, 1])):
    closed = all(reflection(l) in basis for l in basis)
    check(f"reflection closure on OAM {name}: {'closed' if name == '{-1,+1}' else 'NOT closed'}", closed == (name == "{-1,+1}"))
phi = 0.37
rel = rotation_phase(1, phi) / rotation_phase(-1, phi)
check("rotation by phi gives relative phase exp(-2i phi) between l=+1 and l=-1 (sensitivity = delta-l = 2)", abs(rel - np.exp(-2j * phi)) < 1e-12)
rel01 = rotation_phase(1, phi) / rotation_phase(0, phi)
check("for {0,+1} the same rotation gives exp(-i phi) (sensitivity delta-l = 1)", abs(rel01 - np.exp(-1j * phi)) < 1e-12)

# 4. q-plate (half-wave, charge q): l -> l + 2q*s with s = +1/-1 for the two circular polarizations (convention-dependent sign)


def qplate_map(l, s, q=1):
    return l + 2 * q * s


code = [-1, 1]
for q in (1, 0.5):
    inside = [(l, s, qplate_map(l, s, q)) for l in code for s in (1, -1) if qplate_map(l, s, q) in code]
    total = len(code) * 2
    check(f"q-plate q={q}: only {len(inside)} of {total} (l, circular polarization) inputs stay inside {{-1,+1}}; closure fails",
          len(inside) < total, str(inside))

# 5. beam splitter two-photon behavior (bunching): |1,1> -> (|2,0> - |0,2>)/sqrt2, coincidence probability 0
B = np.array([[1, 1], [1, -1]], complex) / math.sqrt(2)
perm = B[0, 0] * B[1, 1] + B[0, 1] * B[1, 0]                     # amplitude for one photon in each output (permanent)
check("50:50 beam splitter: coincidence amplitude (permanent) = 0, so both photons leave together (bunching)", abs(perm) < 1e-12)

# 6. PBS: routes H and V to different paths (isometry into the path axis); not closed in the polarization x OAM space
PBS = np.array([[1, 0], [0, 0], [0, 0], [0, 1]], complex)       # (pol) -> (path, pol-label) ; columns H, V
check("PBS is an isometry from polarization into path: output leaves the original encoding space until recombined", np.max(abs(PBS.conj().T @ PBS - I2)) < 1e-12)

# 7. sorter / inverse sorter as permutations of the mode basis (ideal)
Nm = 4
P = np.eye(Nm)[[2, 0, 3, 1]]
check("ideal sorter then inverse sorter is the identity (ideal)", np.max(abs(P.T @ P - np.eye(Nm))) < 1e-12)

# ---------------- records ----------------
# evidence tags: DERIVED (checked above); REPORTED only where a source was actually read in this project, else 'REPORTED (unverified)'
rows = [
 dict(id="C01", component="Half-wave plate", operation="Polarization exchange, -iX at 45 deg (checked)", control="axis, retardance",
      closure_tetragon="Closed: acts on polarization only, leaves OAM unchanged", risks="mode-dependent retardance (A06 parameter kappa, assumed); axis error; two-photon effects none (single element)",
      cost="1 element (A06 count); calibration parameters: 2 (axis, retardance)", compatibility="TBD: wavelength, aperture, retardance vs wavelength",
      evidence="DERIVED; SIMULATED (A06, ASSUMED errors)", sources="unverified", buddy_check="none needed for a single-photon linear element; verify by process tomography with coherent light (PROPOSED)"),
 dict(id="C02", component="Quarter-wave plate", operation="Polarization phase gate: relative phase i between H and V at 0 deg; two plates equal a half-wave plate (checked)", control="axis, retardance",
      closure_tetragon="Closed for polarization; converts linear to circular at 45 deg (changes readout basis)", risks="polarization error; wavelength dependence",
      cost="1 element", compatibility="TBD", evidence="DERIVED", sources="unverified", buddy_check="as C01"),
 dict(id="C03", component="Image reflection optics", operation="OAM reversal l -> -l, convention-dependent phases", control="orientation",
      closure_tetragon="Closed on OAM {-1,+1}; NOT closed on {0,+1} (checked)", risks="phase error, alignment, reflection phase convention",
      cost="TBD", compatibility="TBD", evidence="DERIVED", sources="unverified", buddy_check="interferometric (identical intensity profiles for +-1)"),
 dict(id="C04", component="Image rotation optics (e.g. Dove prism)", operation="Phase exp(-i l phi) per mode; relative phase exp(-2i phi) between +1 and -1 (checked)", control="rotation angle",
      closure_tetragon="Closed (diagonal in OAM); sensitivity = delta-l: 2 for {-1,+1}, 1 for {0,+1} (checked)", risks="differential phase drift; rotation error",
      cost="TBD", compatibility="TBD", evidence="DERIVED", sources="unverified", buddy_check="interferometric"),
 dict(id="C05", component="Q-plate", operation="Polarization-conditioned OAM shift l -> l + 2q*s (s = +-1 for circular polarizations; sign convention-dependent)", control="retardance, charge q",
      closure_tetragon="NOT closed on {-1,+1}: a charge-1 plate keeps only some inputs in the code, the rest go to l = +-3; q = 1/2 leaves to l = 0 or +-2 (checked)", risks="code-space leakage; retardance error leaves unconverted light",
      cost="TBD", compatibility="TBD", evidence="DERIVED; REPORTED (Marrucci 2006 and Piccirillo 2010 supplied by a collaborator, not rechecked here)", sources="unverified", buddy_check="measure leakage into l outside the code"),
 dict(id="C06", component="Beam splitter", operation="Coherent two-path mixing; for two photons, bunching: |1,1> -> (|2,0> - |0,2>)/sqrt2 (checked)", control="mixing ratio, phase",
      closure_tetragon="Not applicable (path degree of freedom)", risks="loss, imbalance, two-photon bunching (the sector behind the false heralds in the reconstructed analyzer, R30)",
      cost="1 element", compatibility="TBD", evidence="DERIVED", sources="unverified", buddy_check="count both-photons-in-one-port events explicitly"),
 dict(id="C07", component="Polarizing beam splitter", operation="Polarization-dependent routing: isometry from polarization into path (checked)", control="extinction ratio",
      closure_tetragon="Leaves the polarization x OAM space until the paths are recombined", risks="crosstalk; extinction ratio; path phase",
      cost="1 element", compatibility="TBD", evidence="DERIVED", sources="unverified", buddy_check="TBD"),
 dict(id="C08", component="Phase modulator", operation="Controlled phase shift diag(1, e^{i a})", control="applied phase",
      closure_tetragon="Closed", risks="drift; unwanted modulation", cost="TBD", compatibility="TBD", evidence="DERIVED", sources="unverified", buddy_check="interferometric"),
 dict(id="C09", component="OAM sorter", operation="Mode-to-path conversion (ideal: permutation of the mode basis, checked)", control="mode selection",
      closure_tetragon="Leaves the OAM axis for the path axis; restored only by C10", risks="crosstalk; loss; published devices differ (Berkhout 2010: 11 states, abstract checked; Mirhosseini 2013: separation efficiency above 92%, abstract checked; transmission not extracted)",
      cost="A06 convention (ASSUMED): N-1 interferometers x 3 elements", compatibility="TBD", evidence="REPORTED (abstracts only); SIMULATED (A06 tree model, ASSUMED errors)", sources="partly checked", buddy_check="crosstalk matrix and transmission reported separately (PROPOSED)"),
 dict(id="C10", component="Inverse sorter", operation="Path-to-mode conversion; ideal sorter followed by inverse is the identity (checked)", control="relative path phases",
      closure_tetragon="Restores the OAM axis if path phases are kept", risks="coherence loss from path-phase drift", cost="same as C09", compatibility="TBD", evidence="DERIVED; SIMULATED (A06)", sources="unverified", buddy_check="TBD"),
 dict(id="C11", component="Photodetector", operation="Measurement (POVM), destructive", control="threshold, timing",
      closure_tetragon="Consumes the photon", risks="dark counts; inefficiency; photon-number resolution", cost="TBD", compatibility="TBD", evidence="DERIVED", sources="unverified", buddy_check="cannot authorize reuse of the photon it consumes; can characterize a separate test ensemble"),
 dict(id="C12", component="Buddy interaction (heralded two-photon CPF, reconstruction of Liu et al.)", operation="Conditional phase flip of one joint state, ideal success 1/8 (reported and reproduced in the bundle's model)", control="interaction and measurement configuration",
      closure_tetragon="Valid-sector only; occupancy-valid condition required", risks="false heralds: in the reconstructed analyzer reliability is 1/3 worst case, 100% best case, independent of auxiliary outcome class (R30); apparatus mapping (A02) pending",
      cost="2 auxiliary photons per attempt", compatibility="TBD", evidence="REPORTED (Liu et al. 2024, post-selection condition and 1/4, 1/8 confirmed from the paper); SIMULATED (bundle); apparatus mapping unresolved", sources="partly checked", buddy_check="UNRESOLVED (A03)"),
]
fields = ["id", "component", "operation", "control", "closure_tetragon", "risks", "cost", "compatibility", "evidence", "sources", "buddy_check"]
with open(OUT / "physical_architecture_spec_draft.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)
bad = [n for n, ok in checks if not ok]
print(f"\n{len(rows)} component records written to {OUT / 'physical_architecture_spec_draft.csv'}")
print("ALL CHECKS PASS" if not bad else f"FAILED: {bad}")
sys.exit(0 if not bad else 1)
