# Handoff to Codex: Buddy verification v0.8

Claude wrote the program and the page. Nothing here has been independently checked. Try to break it, and report what you cannot reproduce as plainly as what you can. Owner and decision-maker: Tyler O'Bryan. Version 0.7 is preserved unchanged; the corrections to it are the erratum in page section 1. Separate from Revision H, pull request #1 and checkpoints v0.1 to v0.7.

## Task 1. Independent reimplementation (NumPy or SymPy; do not read `code/buddy_v08_checks.py` first)
Axes a1, b1, a2, b2 = qubits 0 to 3. Local checks ZZII, IIZZ; joint checks ZZZZ, XXXX; all observables signed with expected value +1.
1. **Erratum (section 1).** The CNOT(a,b), H(a), CNOT(a,b) route with single-axis X and Z faults at positions 0, 1, 2; confirm X_a is detected at position 0 and invisible at 1 and 2; confirm mean fidelity 1/3 for a logical Pauli error; the exact formula 1 - 0.3 (1 - cos d) for a wrong-angle controlled phase; the physical CZ route counts (preserve checks: 4 and 4; act as the logical CZ: 4 and 1).
2. **Geometries (section 2).** Counts of single-axis and weight-2 Pauli faults detected, invisible Paulis by weight, check weights, code distance.
3. **Conversion (section 3).** Search all signed stabilizer groups for the shortest H, S, CNOT, CZ circuit from the local to the joint group (I claim 4 gates, 24 circuits, all with 2 inter-photon gates). Confirm the logical map, the state-vector preservation, the coverage profile and the fault propagation table. Check my claim that XXXX is a logical operator of the local code.
4. **Compatibility (section 4).** The generator counts by weight; the 15 logical classes by cheapest representative; the exhaustive search to depth 4 for sequences preserving the joint group (6, 96, 982 by length; 51 logical maps); that the six length-2 sequences are exactly a logical CZ with signs +1; the joint-code controlled phase of any angle.
5. **Phase coverage (section 5).** The in-code theorem (should be trivial for you to prove); the detection probability sin^2(eps/2) and accepted fidelity 1 for single-axis rotations; the 66-generator classification and the explicit sets.
6. **Extraction (section 6).** Rebuild the single-ancilla-fault propagation (ancilla-controlled CNOTs for XXXX, data-controlled for ZZZZ); check the counts 18 versus 30, 4 versus 12, 4 versus 4, 2 versus 2, 2 versus 6; check my claim that reordering CNOTs cannot remove the silent cases.
7. **Workload model (section 7).** Reproduce the single-checkpoint table and the three two-block profiles with your own Pauli-frame propagation (XOR convolution of independent X and Z flips; Clifford maps of frames; conversion-gate faults of probability r on each touched axis for X and Z).
Look hard at: the legitimacy of treating frames mod sign, whether the 'wrong' class in the workload model (non-stabilizer frame that commutes with the checks) is right after conversion, whether the 'profile' conclusions survive another noise setting, and any place I let a proxy stand in for a cost.

## Task 2. Literature and terminology (do not rename anything)
- Read the [[4,2,2]] code literature (the page cites Linke et al., arXiv:1611.06946, summarized not read), stabilizer propagation, flag-qubit extraction and verified ancilla preparation; give citations for what the page calls established, and mark what you cannot find.
- Prior use of "verification compatibility", "transported check", "check-sliding", and of switching between detection codes during a computation. Report links.
- The collisions already open (PALADIN, Docked Scheduling, resource-class names, BUD-xx, "information checkpoint").

## Task 3. Repository (only if Tyler asks)
Separate branch and pull request (not #1). Add the page and program. Do not touch Revision H, `library/`, `releases/`, R30 files, licences or tags. Do not tag a release or claim novelty, hardware cost or advantage. Keep evidence tags and the empty cost fields.

## Open items (Tyler decides)
- PALADIN, Docked Scheduling, resource-class names and the third axis stay provisional.
- Whether fault coverage is adopted as a GEA selection variable beside, not combined with, computational and verification efficiency (PROPOSED).
