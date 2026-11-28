"""Run every PhaseKeep model script and store its stdout/stderr in results/logs/<script>.log.
Usage:  python -I run_all.py            (all scripts; the E7/E7-D scripts take several minutes)
        python -I run_all.py --quick    (skip p2cim, e7_timing, e7d_notch, e7d_followup)
Requires: Python 3.9+ and NumPy (no SciPy). Each script is run with -I from this folder."""
import subprocess, sys, os, time
HERE = os.path.dirname(os.path.abspath(__file__)); LOGS = os.path.join(HERE, "results", "logs")
os.makedirs(LOGS, exist_ok=True)
ORDER = ["lie_check.py", "confine_robust.py", "ring_lie.py", "ring_chiral.py", "ring_gauge.py",
         "two_ring.py", "two_ring_shaped.py", "two_ring_echo.py", "ref01_onehot.py", "ref01_diagnostics.py",
         "ref_tolerance.py", "echo_combined.py", "echo_statedep.py", "p2cim.py", "p2cim_analyze.py",
         "e5_drift.py", "e6_flips.py", "e7_timing.py", "e7d_notch.py", "e7d_followup.py"]
SLOW = {"p2cim.py", "e7_timing.py", "e7d_notch.py", "e7d_followup.py"}
summary = []
for s in ORDER:
    if "--quick" in sys.argv and s in SLOW: continue
    t0 = time.time()
    p = subprocess.run([sys.executable, "-I", s], cwd=HERE, capture_output=True, text=True)
    with open(os.path.join(LOGS, s.replace(".py", ".log")), "w", encoding="utf-8") as f:
        f.write(p.stdout + ("\n--- stderr ---\n" + p.stderr if p.stderr.strip() else ""))
    summary.append(f"{s:24s} exit {p.returncode}  {time.time()-t0:7.1f} s")
    print(summary[-1], flush=True)
    # two_ring.py also has a spacing sweep mode
    if s == "two_ring.py":
        p = subprocess.run([sys.executable, "-I", s, "D"], cwd=HERE, capture_output=True, text=True)
        open(os.path.join(LOGS, "two_ring_spacing.log"), "w", encoding="utf-8").write(p.stdout)
        summary.append(f"{'two_ring.py D':24s} exit {p.returncode}"); print(summary[-1], flush=True)
open(os.path.join(LOGS, "SUMMARY.txt"), "w").write("\n".join(summary) + "\n")
