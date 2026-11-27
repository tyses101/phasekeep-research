#!/usr/bin/env python3
"""Run every exploration script (S01-S28) with `python3 -I`, check each verdict, and optionally rewrite the execution records.

  python3 explorations/run_all.py                     short variants (no S05 --cat, no S06 --n5, no S15 --pairs, no S16 --full), about 8 minutes, no files written
  python3 explorations/run_all.py --full              the variants whose records are committed (adds S05 --cat about 7 min, S06 --n5 about 15 min, S15 --pairs 20 to 30 min, S16 --full about 13 min)
  python3 explorations/run_all.py --full --write-records   also rewrite each execution-record.txt in the A01 format
  add  --only S07,S11  to run (and, with --write-records, rewrite the records of) just those scripts

Scripts run in parallel processes.  A script passes when its exit status is 0 and its last output line is "ALL PASS".
Executor statement written into the records: author-side re-execution; not an independent reproduction.
"""
import concurrent.futures as cf, os, platform, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = [  # (id, relative script, args shown in the record, long-variant args)
    ("S01", "s01-five-mub/five_mub.py", []),
    ("S02", "s02-photon-level-distance/photon_distance.py", []),
    ("S03", "s03-hosted-codes/hosted_codes.py", []),
    ("S04", "s04-docked-scheduling/docked_exposure.py", []),
    ("S05", "s05-statevector-crosscheck/statevector_crosscheck.py", ["--cat"]),
    ("S06", "s06-basis-change-cost/basis_change_cost.py", ["--n5"]),
    ("S07", "s07-failure-semantics/failure_semantics.py", []),
    ("S08", "s08-conversion-failure/conversion_failure.py", []),
    ("S09", "s09-ancilla-cohosting/ancilla_cohosting.py", []),
    ("S10", "s10-dph2-harmless-extraction/dph2_extraction.py", []),
    ("S11", "s11-conversion-fault-price/conversion_fault_price.py", []),
    ("S12", "s12-recovery-charged-completion/recovery_completion.py", []),
    ("S13", "s13-recovery-cost/recovery_cost.py", []),
    ("S14", "s14-teleportation-verification/teleport_verification.py", []),
    ("S15", "s15-teleportation-silent-faults/teleport_silent.py", ["--pairs"]),
    ("S16", "s16-readout-weighting/readout_weighting.py", ["--full"]),
    ("S17", "s17-resource-design/resource_design.py", []),
    ("S18", "s18-m3-reproduction/m3_reproduction.py", []),
    ("S19", "s19-v10-exact-reproduction/v10_exact_reproduction.py", []),
    ("S20", "s20-teleport-silent-probability/teleport_silent_probability.py", []),
    ("S21", "s21-v10-remaining-sections/v10_remaining_sections.py", []),
    ("S22", "s22-coherent-rotations/coherent_rotations.py", []),
    ("S23", "s23-flag-design-search/flag_design_search.py", []),
    ("S24", "s24-idle-convention-bias-table/idle_convention_bias_table.py", []),
    ("S25", "s25-teleport-idle-faults/teleport_idle_faults.py", []),
    ("S26", "s26-idle-to-gate-ratio/idle_to_gate_ratio.py", []),
    ("S27", "s27-rho-star-scaling/rho_star_scaling.py", []),
    ("S28", "s28-repeated-rounds-layered-idle/repeated_rounds_layered_idle.py", []),
]
LONG = {"S05", "S06", "S15", "S16"}

def versions():
    out = ["Python " + platform.python_version()]
    try:
        import numpy; out.append("numpy " + numpy.__version__)
    except ImportError: out.append("numpy not installed")
    return ", ".join(out)

def run(item, full):
    sid, rel, args = item
    use = args if (full or sid not in LONG) else []
    path = os.path.join(HERE, rel); t0 = time.time()
    p = subprocess.run([sys.executable, "-I", path] + use, capture_output=True, text=True, cwd=os.path.dirname(path))
    out = (p.stdout + p.stderr).rstrip("\n"); last = out.splitlines()[-1] if out else ""
    return sid, rel, use, p.returncode, out, last.strip() == "ALL PASS", time.time() - t0

def main():
    full = "--full" in sys.argv; write = "--write-records" in sys.argv
    if write and not full: sys.exit("--write-records needs --full (the committed records are the full variants)")
    only = None
    if "--only" in sys.argv: only = set(sys.argv[sys.argv.index("--only") + 1].split(","))
    todo = [it for it in SCRIPTS if only is None or it[0] in only]
    t0 = time.time(); results = []
    with cf.ThreadPoolExecutor(max_workers=max(1, os.cpu_count() or 1)) as ex:
        futs = [ex.submit(run, it, full) for it in todo]
        for f in cf.as_completed(futs):
            r = f.result(); results.append(r)
            print("%-4s %-4s %6.1f s  exit %d  %s" % (r[0], "PASS" if (r[3] == 0 and r[5]) else "FAIL", r[6], r[3], " ".join([r[1]] + r[2])), flush=True)
    results.sort(key=lambda r: r[0])
    if write:
        for sid, rel, args, rc, out, ok, dt in results:
            rec = os.path.join(HERE, os.path.dirname(rel), "execution-record.txt")
            cmd = "python3 -I explorations/%s%s" % (rel, (" " + " ".join(args)) if args else "")
            with open(rec, "w", encoding="utf-8") as fh:
                fh.write("# %s execution record\ndate: %s\ninterpreter: %s\ncommand: %s\nexecutor: Claude (author-side re-execution of the scripts in this folder; not independent reproduction)\nwall-clock: %.0f s\n\n%s\nexit=%d\n" %
                         (sid, time.strftime("%Y-%m-%d"), versions(), cmd, dt, out, rc))
    bad = [r[0] for r in results if not (r[3] == 0 and r[5])]
    print("total wall-clock %.0f s; %s" % (time.time() - t0, "ALL SCRIPTS PASS" if not bad else "FAILED: " + ", ".join(bad)))
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
