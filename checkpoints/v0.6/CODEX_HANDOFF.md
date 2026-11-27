# Handoff to Codex: Buddy verification v0.6

Claude wrote the program and the page. Nothing here has been independently checked. Try to break it, and report what you cannot reproduce as plainly as what you can. Owner and decision-maker: Tyler O'Bryan. Separate from Revision H, pull request #1 and checkpoints v0.1 to v0.5.

## Task 1. Independent reimplementation (NumPy or SymPy; do not read `code/buddy_v06_checks.py` first)
Diagonal encoding |0> = |00>, |1> = |11>, check ZZ, data axes a, b, ancilla c, index 4a + 2b + c, U_ext = CNOT(a to c) CNOT(b to c).
1. **Compatibility map (page section 4).** Build the six implementations (Z via ZI, S via ZI rotation by pi/2, X via X then X, X via XX rotation by pi, H via Rz(pi/2) Rx(pi/2) Rz(pi/2) with generators ZI and XX, H via CNOT(a to b), H on a, CNOT(a to b)). Confirm each gives the target logical operation up to a global phase and leaves nothing outside the code. Confirm the odd-ZZ-weight along each path (0 for A, 1 for the middle of X then X, |alpha - beta|^2 / 2 at the midpoint of the CNOT implementation) and the transported stabilizer along each path (ZZ; ZZ, -ZZ, ZZ; ZZ, IZ, ZZ). Confirm the geometry-change row (CNOT maps the code to axis b = 0) and the mean fidelity of about 0.5 after a PASS at the CNOT midpoint.
2. **Sliding (section 5).** U_ext = P_even (x) 1 + P_odd (x) X_c. Check-then-gate equals gate-then-check exactly for gates commuting with ZZ; the coverage statements (position of the fault against position of the check, and the moved check Z_b after a CNOT).
3. **Propagation (section 6).** Overlap invariance, preservation of detectability against the transported check, and the cos/sin decomposition of a logical Z fault through a logical X rotation. Check the sign convention of the Y component.
4. **Accumulation (section 7).** Closed forms (1 - g)^m and (1 + (1 - 2g)^m) / 2.
5. **Spacing and productivity (section 8).** Reproduce the table with your own dynamic programme (X and Z faults on each data axis; ancilla X fault gx flips the report; ancilla Z fault gz acts as a Z on axis a; loss l; rejected and lost runs stop; segments executed counted before each segment). Check whether the choice of axis for the harmful Z matters and whether the assumption that wrong outputs are identifiable changes the segment comparison.
6. **Concurrency condition (section 9).** The commutator conditions for the listed Pauli generators.
Look hard at: whether class labels A, B, C are defined consistently, the transported-check argument, and any implementation I treated as equivalent that is not.

## Task 2. Literature and terminology (do not rename anything)
- Read about stabilizer transport through Clifford gates, quantum nondemolition parity measurement and verified state preparation; give citations for what the page cites as "established" and mark anything you cannot find.
- Check for prior use of "check-sliding", "transported check", "verification compatibility", and of the A, B, C classes as I defined them. Report links. Also the collisions already open (PALADIN, Docked Scheduling, resource-class names, BUD-xx identifiers).
- Whether the CNOT-conjugated Hadamard is standard and whether a generator-based logical Hadamard (Rz Rx Rz with ZI and XX generators) corresponds to a known photonic or generic implementation.

## Task 3. Repository (only if Tyler asks)
Separate branch and pull request (not #1). Add the page and program. Do not touch Revision H, `library/`, `releases/`, R30 files, licences or tags. Do not tag a release, claim a novelty, a hardware cost or an advantage. Keep evidence tags and the empty cost fields. Do not add PALADIN or the resource-class names as adopted terms.

## Open items (Tyler decides)
- PALADIN, Docked Scheduling, resource-class names and the third axis stay provisional.
- Whether GEA should use implementation compatibility as a selection criterion (a PROPOSED use).
