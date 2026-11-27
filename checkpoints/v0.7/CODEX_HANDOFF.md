# Handoff to Codex: Buddy verification v0.7

Claude wrote the program and the page. Nothing here has been independently checked. Try to break it, and report what you cannot reproduce as plainly as what you can. Owner and decision-maker: Tyler O'Bryan. Separate from Revision H, pull request #1 and checkpoints v0.1 to v0.6.

## Task 1. Independent reimplementation (NumPy or SymPy; do not read `code/buddy_v07_checks.py` first)
Photon i has axes a_i = 2i, b_i = 2i + 1, diagonal encoding |0> = |00>, |1> = |11>, local check S_i = Z(a_i) Z(b_i).
1. **Transported-check complexity (page section 3).** Conjugate ZZ through Clifford sequences (one term); through rotations about each of the 6 Paulis commuting with ZZ (unchanged) and each of the 8 anticommuting ones (two terms at generic angle). Confirm the equivalence of the XX rotation and the CNOT, X_a rotation, CNOT route, and the reversing-the-prefix identity.
2. **Two Tetragons (section 4).** On the 16-dimensional space: the four CZ routes commute with both local checks; the wrong-angle controlled phase (phi = 2.0) passes both checks (mean fidelity about 0.826 with the intended CZ on random logical inputs: confirm the number with your own sampling); routes P, G and T give the logical CNOT; sub-step odd weights (zero for G and T, amplitude-dependent for the mid-route of P); the three-axis generator of T.
3. **Scaling (section 5).** Pauli-group tracking for 2, 4, 8 photons: valid local checks after every step for compatible routes, at endpoints for route P; the minimum-weight basis of the transported group (weight 2 at endpoints, 3 mid-route). Brute-force the invisible-fault counts for n = 1, 2, 3 and confirm 8^n and 2^n.
4. **Growth (section 6).** Rebuild the non-commuting ensemble from its description. Treat the table as ensemble-dependent; check the "no incompatible step gives one term" row exactly.
5. **Excursion (section 7).** The fault table for CNOT, H_a, CNOT. Confirm that X_a made after the first CNOT is a logical error invisible to IZ and ZZ, and that Z faults are invisible everywhere. Check my statement that I first expected otherwise and was wrong.
6. **Productivity (section 9).** Reproduce the table with your own dynamic programme; check whether the best spacing differs between Modes I and II, and whether "no checked policy beats unchecked at x = 0.1 under Mode I" holds.
Look hard at: whether the group-minimum-weight argument (section 5 item 2) is legitimate for gates that preserve the code space, whether the "equivalent route" claims really are equal unitaries, and any place I let a proxy (terms, weight) stand in for a cost.

## Task 2. Literature and terminology (do not rename anything)
- Stabilizer propagation through Clifford and Pauli-rotation gates; stabilizer measurement and ancilla-based parity extraction; verified ancilla preparation; QND parity measurement; any prior use of "transported check", "check-sliding", "verification compatibility". Give citations for what the page calls established and mark what you cannot find.
- Open collisions: PALADIN, Docked Scheduling, resource-class names, BUD-xx, "information checkpoint".

## Task 3. Repository (only if Tyler asks)
Separate branch and pull request (not #1). Add the page and program. Do not touch Revision H, `library/`, `releases/`, R30 files, licences or tags. Do not tag a release or claim novelty, hardware cost or advantage. Keep evidence tags and the empty cost fields.

## Open items (Tyler decides)
- PALADIN, Docked Scheduling, resource-class names and the third axis stay provisional.
- Whether verification compatibility is adopted as a GEA selection criterion (PROPOSED, listed beside, not combined with, other criteria).
