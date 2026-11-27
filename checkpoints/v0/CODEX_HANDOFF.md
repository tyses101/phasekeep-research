# Handoff to Codex: Tetragon map v0

Claude wrote the program and the page. Nothing here has been independently checked. Try to break it, and report what you cannot reproduce as plainly as what you can.

## Task 1. Independent reimplementation
Reimplement the four parts with NumPy (or SymPy) without reading `code/tetragon_map.py` first. Confirm:
1. The six Bell-family operation rows and Gram = identity. Overlaps of the encoding basis with the Bell basis are 0 and 0.7071.
2. Permutations of {A,B,C,D}: 4 from single-axis Clifford operations, 24 from local Cliffords on both axes. Controlled phase and S on both axes both give A<->B. The axis SWAP fixes all four labels.
3. Time control: 1 ebit for superposed time bins with "none then flip", 0 otherwise.
4. 15 commuting Pauli triples; 6 spreads (partitions into 5 triples); each spread = 3 product + 2 entangled bases and pairwise unbiased; each basis in 2 spreads; encoding triple {IZ,ZI,ZZ} and Bell triple {XX,YY,ZZ} in no common spread.
5. 225-pair map: 81 / 36 / 108 and the breakdown by product or entangled, with the stated route order. Check the 108 "one entangling gate" pairs really cannot be reached by local operations, and look for any pair my search labels wrongly.
6. The hand claim that a single-axis unitary keeping the Bell set in itself must be a Pauli (4 of 24), for all unitaries, not only Cliffords.

## Task 2. Read the prior art
Read the eleven sources in section 5 of the page (full text), update the status column, and say which claims in the page they support or contradict. Pay particular attention to: whether an axis-SWAP device exists (quant-ph/0407136, bears on Volume 5), and how many bases certification needs (arXiv:1709.07344, bears on the Buddy cost remark that complete tomography needs d+1 bases).

## Task 3. Novelty and terminology
Search for existing treatment of: classifying the stabilizer-basis map by operation class for a photon's polarization and OAM; entanglement as a persistent operating configuration (compare one-way and resource-state computing); hardware-aware compilation for photonic axes. Report links. Also check the abbreviations SEE, NEE, CPE, EET, IEE and DS for conflicts. Do not rename anything.

## Task 4. Repository
Prepare a separate branch and pull request (not #1). Add the page and the program. Do not touch Revision H, `library/`, `releases/`, R30, licences or tags. Do not tag a release. Do not claim a novelty, a hardware cost or an advantage. Keep evidence tags and the empty cost fields.

## Open items (Tyler decides)
- Whether Docked Scheduling gets a section at all; the page only describes the classical-schedule meaning.
- How far to take the persistent-entanglement hypothesis before any apparatus numbers exist.
