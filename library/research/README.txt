PhaseKeep research scripts (copies bundled with the Learning Library)
=====================================================================
These are the scripts described in Volume 9. Run them with:  python3 -I <script>

Stand-alone (need Python 3 and NumPy only). All three were re-run from this folder
when the library was assembled and pass:
  verify_r25.py                       71 arithmetic checks (memory, benchmarks, chains)
  spec/build_spec_draft.py [outdir]   12 numerical checks; rewrites the component CSV,
                                      which reproduces spec/physical_architecture_spec_draft.csv exactly
  a06/a06_precursor_sim.py [outdir]   A06 shared-vs-individual simulation, 19 self-checks,
                                      writes the 120-row results table (see a06/A06_precursor_report.md)

Need the Codex feasibility bundle, which is NOT included here:
  audit_bundle_r25.py <bundle_dir>               read-only audit of the bundle's results and hashes
  outcome_resolved_herald_r30.py <bundle_dir>    R30 herald analysis (refuses to run on a modified
                                                 bundle unless --allow-modified is given)
They are included so a reader can see exactly what was checked. They cannot be run without the bundle.

Scope reminder: passing these scripts tests the arithmetic and the models. It does not test any
laboratory result. All error and loss inputs in the A06 simulation are assumptions.
