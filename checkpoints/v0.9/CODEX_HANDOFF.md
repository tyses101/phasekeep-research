# Handoff to Codex: Buddy verification v0.9

Claude wrote the program and the page. Nothing here has been independently checked, and the literature was read at abstract level only. Try to break it, and report what you cannot reproduce as plainly as what you can. Owner and decision-maker: Tyler O'Bryan. Versions 0.1 to 0.8 are preserved unchanged; the corrections to v0.8 are the erratum in page section 1. Separate from Revision H and pull request #1.

## Task 1. Independent reimplementation (do not read `code/buddy_v09_checks.py` first)
Data qubits 0 to 3 = a1, b1, a2, b2. Local checks ZZII, IIZZ; joint checks ZZZZ, XXXX; signed, expected +1.
1. **Erratum E4.** Transport the local checks through H(0), H(1), CNOT(0 to 2), CNOT(1 to 3) and confirm the five-row table (weights, photons, signs, all reading +1 on converted logical states).
2. **Fault model.** Implement a Pauli-frame simulator for the ancilla circuits in the page: conventional (ancilla in |0>, data-controlled CNOTs, Z measurement for ZZZZ; ancilla in |+>, ancilla-controlled CNOTs, X measurement for XXXX), flagged (flag in |+> for ZZZZ, |0> for XXXX, coupled to the ancilla before the second and after the second-to-last data CNOT, measured in the opposite basis), 4-qubit cat (prepared by H and a CNOT chain, optionally checked by a ZZ parity ancilla between the two ends, controlled-Z or controlled-X couplings, X measurements, parity detector) and the two-cat-qubit cooperative variant (cat qubit 0 couples axes 0 and 1, qubit 1 couples axes 2 and 3). Fault families: M2 = every non-identity Pauli after each gate on the touched qubits (15 for two-qubit gates, 3 otherwise, including preparations) and measurement flips; M3 = M2 plus every idle live qubit after every operation plus one incoming fault on each data axis. Reproduce the location, fault-case, silent, accepted-damaged and rejected counts in page section 4, in particular zero silent for flagged and verified cat, 4/15 for joint conventional, 8/15 for local.
3. **Second order and exact rates.** Reproduce the pair coefficients (1.244, 2.427, 2.320, 9.902) and the exact table (a different method is welcome, for example direct enumeration of fault subsets at one small p).
4. **Windows.** Confirm the commutation rule with your own state-vector code, and the counts: 34 of 54 pairs for the 18 weight-2 joint generators, distribution {0:2, 1:4, 2:6, 3:6}.
5. **References.** Confirm sin^2(d/2), the run counts, and the references-versus-generator table.
Look hard at: whether M2 really is the standard single-fault family; whether my classification of a fault case as "silent" (all detectors quiet and data error a non-stabilizer logical operator) matches Tyler's definition; how the flag circuit's gate order compares with the published flag circuits; whether ignoring faults between a check and the next round's preparation hides anything; the legitimacy of the uniform-Pauli, per-location-p comparison across circuits of different length.

## Task 2. Literature (do not rename anything)
Read in full Chao and Reichardt (flag qubits), Chamberland and Beverland (arbitrary-distance flags), Shor 1996 and Steane (ancilla verification), Knill, Self, Benedetti and Amaro (iceberg code syndrome circuits), Linke et al. arXiv:1611.06946, and the code-switching papers arXiv:1403.2734 and 1703.03860. Confirm identifiers and give citations for what page section 2 calls established; mark what you cannot find. Check prior use of "capability report" style interfaces between a verification specification and an extraction mechanism, and of choosing among extraction circuits at run time.

## Task 3. Repository (only if Tyler asks)
Separate branch and pull request (not #1). Add the page and program. Do not touch Revision H, `library/`, `releases/`, research scripts, licences, tags or R30 files. No release, novelty, cost or advantage claims. Keep evidence tags and empty cost fields. IQA stays outside the frozen vocabulary and library.

## Open items (Tyler decides)
- Whether to study conversion reliability thresholds and a loss-and-probabilistic-gate model before more is added to Buddy.
- Whether the cooperative variant should be retried with cross-photon grouping or a flagged cat.
- PALADIN, Docked Scheduling, resource-class names, BUD-xx identifiers and the third axis remain provisional.
