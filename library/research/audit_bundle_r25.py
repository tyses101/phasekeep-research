#!/usr/bin/env python3
"""Read-only audit of the Codex feasibility bundle (62cc006a ZIP) for the R25 update.

Usage:  python3 -I audit_bundle_r25.py /path/to/extracted/bundle
It only READS the packaged results; it never runs the bundle's code.
(The bundle's own run is separate: `python3 verify_suite.py --rerun` in a COPY.)
Scope: checks that numbers quoted in REVIEW.txt / the R25 page match the packaged
result files, and that packaged hashes match. It does NOT validate the mapping from
the published apparatus (arXiv 2407.16356) to the bundle's reconstructed network.
"""
import csv, hashlib, json, sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
R = ROOT / "results"
fails = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))
    if not ok:
        fails.append(name)


def near(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(b))


# 1. packaged hashes
bad = []
for line in (ROOT / "SHA256SUMS.txt").read_text().splitlines():
    if not line.strip():
        continue
    h, name = line.split(None, 1)
    name = name.strip().lstrip("*")
    if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != h:
        bad.append(name)
check("SHA256SUMS: every packaged file matches", not bad, ",".join(bad))

# 2. SIM-04 counterexample (REVIEW.txt: |7,0> raw .375, valid .125)
g = json.loads((R / "sim04_gate.json").read_text())
for d in ("4", "8"):
    c = g[d]["counterexample"]
    check(f"SIM-04 d={d}: ideal success 1/8 on every tested input",
          near(g[d]["postselected_success_min"], .125, 1e-9) and near(g[d]["postselected_success_max"], .125, 1e-9))
    check(f"SIM-04 d={d}: counterexample herald .375 / valid .125 / false .25",
          near(c["herald_probability"], .375) and near(c["valid_two_register_probability"], .125)
          and near(c["false_herald_probability"], .25), f"input={c['input']}")
    check(f"SIM-04 d={d}: false share of heralds = 2/3 for that input",
          near(c["false_herald_probability"] / c["herald_probability"], 2 / 3))
    check(f"SIM-04 d={d}: worst herald-only fidelity = 1/3", near(g[d]["worst_herald_only_fidelity"], 1 / 3))
# herald-probability pattern across d=4 basis inputs: which inputs are inflated
hp = g["4"]["basis_herald_probabilities"]
inflated = [i for i, p in enumerate(hp) if near(p, .375)]
check("SIM-04 d=4: exactly 3 of 16 basis inputs have inflated herald (indices 12,13,14)",
      inflated == [12, 13, 14], str(inflated))
check("SIM-04 d=4/8: Haar-average herald-only fidelity ~0.742 / ~0.824",
      abs(g["4"]["average_haar_herald_only_fidelity"]["mean"] - .7418) < 5e-4
      and abs(g["8"]["average_haar_herald_only_fidelity"]["mean"] - .8241) < 5e-4)

# 3. SIM-06 chain table
rows = list(csv.DictReader(open(R / "sim06_chains.csv")))
ideal = {int(r["length"]): r for r in rows if r["scenario"] == "ideal"}
check("SIM-06 ideal 2-stage all-herald probability = 0.01953125 (=5/256)",
      near(float(ideal[2]["probability_all_heralds"]), .01953125, 1e-12))
check("SIM-06 ideal 2-stage herald-conditional fidelity ~ .80020",
      abs(float(ideal[2]["final_fidelity_given_all_heralds"]) - .80020) < 5e-5)
check("SIM-06 ideal 16-stage probability ~ 1.47e-14 and fidelity ~ .24334",
      abs(float(ideal[16]["probability_all_heralds"]) / 1.4725e-14 - 1) < 1e-3
      and abs(float(ideal[16]["final_fidelity_given_all_heralds"]) - .24334) < 5e-5)
check("SIM-06 false heralds RAISE chain probability above (1/8)^n (n=16)",
      float(ideal[16]["probability_all_heralds"]) > (1 / 8) ** 16,
      f"{float(ideal[16]['probability_all_heralds']):.3e} vs {(1/8)**16:.3e}")
check("SIM-06 fidelity given valid-registers >> given heralds (ideal, n=2)",
      float(ideal[2]["final_fidelity_given_valid_registers"]) > .98 > float(ideal[2]["final_fidelity_given_all_heralds"]))

# 4. The 'chain metric' (78.73/62.78/37.20/9.12 %) is defined: correlated-phase replicates
cp = list(csv.DictReader(open(R / "sim06_correlated_phase_replicates.csv")))
mean = {}
for n in (2, 4, 8, 16):
    xs = [float(r["herald_conditional_fidelity"]) for r in cp if int(r["length"]) == n]
    mean[n] = sum(xs) / len(xs)
check("Codex chain metric = mean herald-conditional fidelity over 12 correlated-phase replicates (sd .05 rad, same profile every stage)",
      all(abs(mean[n] - t) < 5e-5 for n, t in zip((2, 4, 8, 16), (.7873, .6278, .3720, .0912))),
      ", ".join(f"{n}:{mean[n]*100:.2f}%" for n in mean))
ideal_f = {n: float(ideal[n]["final_fidelity_given_all_heralds"]) for n in (2, 4, 8, 16)}
check("noise-free (false-herald-only) fidelity already caps the chain: 80.0 / 67.0 / 48.0 / 24.3 %",
      all(abs(ideal_f[n] - t) < 5e-4 for n, t in zip((2, 4, 8, 16), (.8002, .6695, .4800, .2433))))
check("phase drift (sd .05 rad) costs only ~1.3 points at 2 stages (false-herald dominated there)",
      0 < ideal_f[2] - mean[2] < .02, f"{(ideal_f[2]-mean[2])*100:.2f} points")
check("...but it matters for long chains: costs ~11 points at 8 and ~15 points at 16 stages",
      .09 < ideal_f[8] - mean[8] < .13 and .13 < ideal_f[16] - mean[16] < .17,
      f"{(ideal_f[8]-mean[8])*100:.1f} / {(ideal_f[16]-mean[16])*100:.1f} points")

# 5. verification.json recorded state
v = json.loads((R / "verification.json").read_text())
check("Packaged verification.json: all recorded checks passed", all(c["passed"] for c in v["checks"]),
      f"{len(v['checks'])} checks")

print()
print("ALL PASS" if not fails else f"{len(fails)} FAILED: {fails}")
sys.exit(0 if not fails else 1)
