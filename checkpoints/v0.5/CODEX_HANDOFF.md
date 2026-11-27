# Handoff to Codex: Buddy verification v0.5

Claude wrote the program and the page. Nothing here has been independently checked. Try to break it, and report what you cannot reproduce as plainly as what you can. Owner and decision-maker: Tyler O'Bryan. Separate from Revision H, pull request #1 and checkpoints v0.1 to v0.4.

## Task 1. Independent reimplementation (NumPy or SymPy; do not read `code/buddy_v05_checks.py` first)
Model: diagonal encoding, parity ancilla, report 0 = even. Pauli frame (fx1, fx2, fz1, fz2) on the two data axes; correct iff fx1 = fx2 = 0 and fz1 = fz2.
1. **Repeated checkpoints.** Independent X (prob x) and Z (prob z) faults on each data axis per segment; at each checkpoint an ancilla X fault (gx) flips the report, a harmful ancilla Z fault between the CNOTs (gz) acts as a Z on axis a, and loss l. Rejected and lost runs stop. Confirm: one segment with one checkpoint equals the v0.4 outcomes; the closed forms in section 6 of the page (harmful Z only, ancilla X only, loss only, expected interactions); the no-checkpoint, end-only and every-segment formulas for flip noise only; the spacing and selective tables (section 6).
2. **Reusable ancilla.** State-vector check of two photons sharing one ancilla with and without reset (combined parity, cancelled flips, ancilla |0> after a valid photon). Steady-state stream model with reset-failure probability: ideal reset equals v0.4, never reset gives accepted = 1/2, imperfect-reset table, and that reset failure does not matter within one computation. Check the stationary-distribution step, the assumption that a lost photon still interacted, and whether the order of events matters.
3. **Router.** P(FAIL) = q t eta, P(continues) = (1 - q) t, P(continues given silence) = (1 - q) t / (1 - q t eta), and the leakage term.
4. **Detect, reject, correct.** Two-axis parity code cannot correct (same syndrome, wrong recovery is a logical X); three-axis repetition code: distinct syndromes for single flips, exact recovery, wrong decoding of double flips, Z errors undetected.
5. **Temporal validity.** The closed form against enumeration for k up to 6, and the 1/4 limit.
Look hard at: independence assumptions, the definition of correct, the treatment of the harmful ancilla Z as a Z on axis a (does the choice of axis matter?), and whether the no-Buddy comparison is fair.

## Task 2. Literature and terminology (do not rename anything)
- Read the sources in section 13 of the page in full. Confirm the standard treatment of verified ancilla preparation, fault-tolerant extraction (harmful fault propagation) and the repetition code as a bit-flip code, with citations. Report the first use of "ancilla" in quantum information if you can establish it.
- Check collisions and prior use for: resource-class names (internal, companion, stationary, collective ancilla; "stationary" and "flying" qubits), "cooperative verification", "evidence age", "information checkpoint", PALADIN, Docked Scheduling, and the identifiers BUD-xx, PAL-xx, INT-xx. Report links.
- Whether a parity router with a rejection detector (path-based even/odd separation) has been described for polarization-OAM parity, and what the physical obstacles are.

## Task 3. Repository (only if Tyler asks)
Separate branch and pull request (not #1). Add the page and program. Do not touch Revision H, `library/`, `releases/`, R30 files, licences or tags. Do not tag a release, claim a novelty, a hardware cost or an advantage. Keep evidence tags and the empty cost fields. Do not add PALADIN or the resource-class names to the library or landing page as adopted terms.

## Open items (Tyler decides)
- PALADIN, Docked Scheduling and the resource-class names stay provisional.
- The third axis stays "path, provisionally".
- Whether cooperative verification becomes a study of its own.
