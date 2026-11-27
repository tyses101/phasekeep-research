# Handoff to Codex: Tetragon map v0.3

Claude wrote the program and the page. Nothing here has been independently checked. Try to break it, and report what you cannot reproduce as plainly as what you can.

## Task 1. Independent reimplementation
Reimplement the four parts with NumPy (or SymPy) without reading `code/tetragon_map.py` first. Confirm:
1. The six Bell-family operation rows and Gram = identity. Overlaps of the encoding basis with the Bell basis are 0 and 0.7071.
2. Permutations of {A,B,C,D}: 4 from single-axis Clifford operations, 24 from local Cliffords on both axes. Controlled phase and S on both axes both give A<->B. The axis SWAP fixes all four labels.
3. Time control: 1 ebit for superposed time bins with "none then flip", 0 otherwise.
4. 15 commuting Pauli triples; 6 spreads (partitions into 5 triples); each spread = 3 product + 2 entangled bases and pairwise unbiased; each basis in 2 spreads; encoding triple {IZ,ZI,ZZ} and Bell triple {XX,YY,ZZ} in no common spread.
5. 225-pair map: 81 / 36 / 108 and the breakdown by product or entangled, with the stated route order. Check the 108 "one entangling gate" pairs really cannot be reached by local operations, and look for any pair my search labels wrongly.
6. The hand claim that a single-axis unitary keeping the Bell set in itself must be a Pauli (4 of 24), for all unitaries, not only Cliffords.

7. Persistence: 200 random single-axis operations on either axis equal one 2x2 unitary applied to one axis (left-multiply for polarization, right-multiply by the transpose for OAM).
8. Restricted subspaces: the table in section 6 of the page, including that the pairs are Z-Z, S-S and S-dagger-S-dagger on span{00,11} and Z-Z, S-S-dagger and S-dagger-S on span{01,10}, and none elsewhere. Search beyond coordinate subspaces and a larger gate list, and look for any pair I missed.
9. The parity statements: parity +1 inside span{00,11}, -1 after one flip for any amplitudes, +1 after one phase error, and logical flip = both axes.
10. Encoding switching: over the 12 ordered two-vertex encodings the 144-pair table in section 7 of the page (edge-edge 24/8/32, edge-diagonal 64 entangling, diagonal-diagonal 12/4). Check whether any edge to diagonal switch can avoid an entangling gate (it should not: edge encodings give product states for every x, diagonal encodings do not).

11. Logical gates against geometry (section 8 of the page): for G in X, Z, S, H, the cheapest route class from each of the 8 edge and 4 diagonal encodings with the output encoding fixed or free. Check especially that H from a diagonal encoding cannot avoid an entangling gate, and that X is a pure relabelling.
12. Targeted verification (section 9): on span{00,11}, expectation of ZZ is 1 and the expectations of XX, YX and ZI equal the logical Bloch components 2Re(a*b), 2Im(a*b) and |a|^2-|b|^2.

13. Leakage bias (section 9): XX and YX commute with ZZ, and the measured value is within eps of (1 - eps) times the true logical value. Prove it, and say what is not covered.
14. Operational redundancy (section 10): axes that can carry Z, S, X, H by a single-axis operation (edge 1,1,1,1; diagonal 2,2,0,0), and equivalent axis pairs for a physical CZ between two photons (1, 2, 4). Check the counts independently and look for routes I missed (other gates, other axes, non-Clifford operations).

## Task 2. Read the prior art
Read the eleven sources in section 12 of the page (full text), update the status column, and say which claims in the page they support or contradict. Also read, from memory unverified: Pauli-frame tracking, the teleportation-based gate construction (Gottesman and Chuang), the one-way quantum computer (Raussendorf and Briegel), the two-qubit parity code and decoherence-free subspaces. Pay particular attention to: whether an axis-SWAP device exists (quant-ph/0407136, bears on Volume 5), and how many bases certification needs (arXiv:1709.07344, bears on the Buddy cost remark that complete tomography needs d+1 bases).

## Task 3. Novelty and terminology
Search for existing treatment of: classifying the stabilizer-basis map by operation class for a photon's polarization and OAM; entanglement as a persistent operating configuration (compare one-way and resource-state computing); hardware-aware compilation for photonic axes. Report links. Also check the abbreviations SEE, NEE, CPE, EET, IEE and DS for conflicts. Do not rename anything.

## Task 4. Repository
Prepare a separate branch and pull request (not #1). Add the page and the program. Do not touch Revision H, `library/`, `releases/`, R30, licences or tags. Do not tag a release. Do not claim a novelty, a hardware cost or an advantage. Keep evidence tags and the empty cost fields.

## Open items (Tyler decides)
- Whether Docked Scheduling gets a section at all; the page only describes the classical-schedule meaning.
- How far to take the persistent-entanglement hypothesis before any apparatus numbers exist.
