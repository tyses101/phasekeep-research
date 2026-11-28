# Atomic-register documentation and reproduction checkpoint

[PROPOSED] Development update based on `e5f1507`, 2026-11-28. Start with the [reading guide](../atomic-register/README.md), [short version](../atomic-register/01_the_short_version.md) or [chapters](../atomic-register/02_the_full_story/00_contents.md).

[REPORTED] Source: owner-supplied PhaseKeep publication package, prepared by Claude. Prior A-series results were produced by a separate AI assistant (ChatGPT) at the owner's request on 27–28 November; their scripts are absent and results remain REPORTED. This integration reruns supplied implementations, not independently reimplemented models.

## Limits and corrections

[ASSUMED] Mixed-platform decay estimates are illustrative only. Sixth-order suppression, the epsilon-alpha budget and drift-stability requirement apply only to this model and sequence. PK-E remains prepared-instruction execution; PK-M remains the proposed four-mode atomic-vapor memory. New terms are provisional. Negative results and superseded assumptions remain available.

[DERIVED] For isometric code embedding C and unitary actual/target evolutions, W = C† U_target† U C gives the unconditional average target overlap (|Tr W|² + Tr W†W)/(d(d+1)). It is not success-conditioned fidelity. With K = C† U C, worst code leakage is the largest eigenvalue of I − K†K (equal to its spectral norm for an exact contraction). Reference-target leakage and numerical roundoff require care.

[DERIVED] The fitted exponent ln(I_full/I_uneven)/ln(k) is meaningful only for positive infidelities and non-unit k; it is an effective finite-ratio exponent. The envelope imbalance is the signed integral of g² divided by its total integral. At J_B/h = 1 MHz the time unit is 1/(2π) microseconds, giving the stated 2π slew conversion.

## Licence

Original authored text is CC BY 4.0 and original simulation code is MIT under the repository's existing licence files. Cited works remain their authors' work. No frozen source package, licence or release is changed.

## Reproduction

[SIMULATED] Re-run on Python 3.12.14 / NumPy 2.3.5: scripts through e7_timing.py completed with exit 0, including the spacing sweep. Five P2-CIM CSVs, E5, E6, E7 (90 rows), and the E7-D grid (90 rows) match supplied results at relative tolerance 1e-7, absolute tolerance 1e-10. The grid best is raised-cosine, width 0.2, residual 0.5, infidelity 0.00118678085.

[REPORTED] At the owner's request to merge promptly, the remaining e7d_notch.py follow-up and e7d_followup.py rerun are still pending at this commit. Their supplied values are REPORTED, not reproduced by this integration yet. The e7d_followup.csv and any supplied final envelope log must not be interpreted as fresh completion evidence. No all-tests-passed claim is made.

[DERIVED] The slew conversion was checked independently, separately from the pending full dynamical run. Source ZIP SHA-256: ff80aba1a704ee21b5adf19ee778564a8e1925afd17d59071e9cf4e2c7c936b8. ZIP members matched the supplied folder byte-for-byte. Frozen library/checkpoint/release sources: 168 files byte-identical to the base. No credential patterns found in new text/code.

[DERIVED] Independent envelope-only conversion: symmetric segmented normalized max slope = 0.019999909; multiplying by 2π gives 0.125663132 MHz/µs at J_B/h = 1 MHz. The earlier 0.8 value is superseded, not an alternative normalization of the same physical slew.

[REPORTED] Owner clarification: the earlier 0.8 MHz/µs divided by the 0.159155 µs time unit twice. The normalized slope requires only one time conversion.

[SIMULATED] Documentation discrepancy corrected from ring_gauge.py: zero-flux travelling modes have currents +0.5 and −0.5 in the script convention. Non-trivial flux is not necessary for current itself; it lifts the tested degeneracy. The tested flux-2π code modes have zero current.
