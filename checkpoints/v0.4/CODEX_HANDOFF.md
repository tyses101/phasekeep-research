# Handoff to Codex: Buddy verification v0.4

Claude wrote the program and the page. Nothing here has been independently checked. Try to break it, and report what you cannot reproduce as plainly as what you can. Owner and decision-maker: Tyler O'Bryan. This package is separate from Revision H, pull request #1 and the earlier checkpoints v0.1 to v0.3.

## Task 1. Independent reimplementation (NumPy or SymPy, without reading `code/buddy_checks.py` first)
Convention: axes a, b (Tetragon axes, qubit on a,b) and c (Buddy ancilla), index 4a + 2b + c. Diagonal logical |0> = |00>, |1> = |11>. Extraction = CNOT(a to c), CNOT(b to c), read c.
1. BUD-01: valid state unchanged with c = 0; one flip gives c = 1 and unchanged amplitudes; one phase error gives c = 0; filtering on c = 0 gives probability = even weight with survivors unchanged; coherence between even and odd parity sectors of the data is zero after extraction and within the even sector is unchanged.
2. BUD-02: for the 15 non-identity two-axis Paulis, classify detected / harmless / undetected logical for the diagonal code (span{00,11}, check ZZ) and the edge code (span{00,01}, check ZI). Expect 8 / 1 / 6 for both. Expect single-axis (6 errors): diagonal 4 detected and 2 logical Z; edge 2 detected, 1 harmless, 3 logical. Check the edge code with the qubit on the other axis and other edge or diagonal choices for the same counts.
3. BUD-03: every single X, Y, Z fault on c, a, b at the three positions (before CNOT1, between, after CNOT2): table in section 6 of the page. Confirm especially Z on c between the CNOTs gives a logical Z on the data with c = 0 (false acceptance), and X on c at any position gives c = 1 with untouched data. Also confirm the timing-window cases (flip on a or b after its CNOT passes the round).
4. BUD-04: reproduce the outcome probabilities by your own enumeration of the stated Pauli model (X on each data axis x, Z on each data axis z, ancilla X fault gx, ancilla Z fault between CNOTs gz acting as Z on axis a, loss l). Confirm the exact threshold gz < 2x(1-x) (flip noise only), accepted-correct never above the no-Buddy correct probability, and the D* values in section 7. Check the model's choice that a Z fault between the CNOTs acts as Z on axis a and whether the choice of axis matters.
5. Look for flaws in the model assumptions: independence, no correlated faults, no leakage, loss modelled as separate, and the definition of "correct" (identity on the code up to a global phase).

## Task 2. Literature and terminology (do not rename anything)
- Read the sources in section 12 of the page in full and report what they support or contradict. Confirm whether ancilla-based parity extraction and its fault propagation (the Z-fault result) are standard, and give citations. Report the first use of "ancilla" in quantum information if you can establish it.
- Abbreviation and name conflicts for **PALADIN** (all fields, including quantum, photonics, and engineering fault management), **BUD-xx / PAL-xx / INT-xx** identifiers, "information checkpoint" (check collision with classical checkpointing), and the existing set SEE, NEE, CPE, EET, IEE, DS. Report links.
- Whether "heralding / detecting / continuation" as three functions has a precedent or a conflicting use. Library check: "herald" appears in Volume 7 as herald probability versus herald reliability.

## Task 3. Repository (only if Tyler asks)
Prepare a separate branch and pull request (not #1). Add the page and program. Do not touch Revision H, `library/`, `releases/`, R30 files, licences or tags. Do not tag a release. Do not claim a novelty, a hardware cost or an advantage. Keep evidence tags and the empty cost fields. Do not add PALADIN to any library or landing page as an adopted term.

## Open items (Tyler decides)
- PALADIN stays provisional until the checks above are done.
- The third Encoding Axie is undecided.
- Whether the wider program question is adopted next to the central question, which is unchanged.
