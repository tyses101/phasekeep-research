# Handoff to Codex: Buddy verification v1.0

Claude wrote the program and the page. Nothing here has been independently checked, and the photonic literature was read at abstract or excerpt level only. Try to break it, and report what you cannot reproduce as plainly as what you can. Owner and decision-maker: Tyler O'Bryan. Versions 0.1 to 0.9 are preserved unchanged. Separate from Revision H and pull request #1.

## Task 1. Independent reimplementation (do not read `code/buddy_v10_checks.py` first)
Use the circuits and fault families defined in the version 0.9 handoff, then add:
1. **Regression.** With every new mechanism off, reproduce the version 0.9 exact silent and rejection probabilities at p = 1e-3 (local, joint, flagged, verified cat).
2. **Loss.** A photon loses with probability q at each two-qubit gate it takes part in. Ancilla photon: heralded (the round is flagged) or unheralded (the ancilla becomes a uniformly random single-qubit Pauli). Data photon: latent (survival factor (1-q)^n, n = data-ancilla gates) or unheralded (both of its axes become a uniformly random Pauli, identity included, 16 options). Reproduce the loss tables, in particular the 10 and 60 times rise in silent damage when ancilla loss is unheralded, and the 9.7e-4 floor for the flagged round at q = 1e-3.
3. **Hosting.** Ancillas never share a photon with data (destructive readout). Reproduce the inter-photon gate counts for K = 1, 2, 5 by minimising over groupings of each check's ancilla qubits, and the optimistic nondestructive-readout bound (hosts photon A, photon B or own photon).
4. **Probabilistic gates.** s^n completion, the abort and retry attempt counts.
5. **Bias.** A weight b on the Z (or X) Pauli at faulted locations (single-qubit faults, and per qubit inside two-qubit faults). Reproduce the bias table, especially the X-bias reversal (local and ZZZZ-only below every joint round at b = 100) and the ancilla-only and data-only rows.
6. **Repeated rounds.** Exact recursion over the 256 data frames: incoming faults, then a round that accepts iff its detector flips equal the syndrome of the existing frame. Reproduce the 20-round table.
7. **Amplification.** The click probability sin^2(Nd/2), the exact binomial threshold test (95% detection, 5% false alarm; at no stochastic noise it is 1 - (1-s)^R >= 0.95), the table, and the alternating-sign failure.
8. **Observable classes.** 3 stabilizer, 60 logical, 192 check-disturbing products; the disturbance numbers.
Look hard at: whether per-gate-participation loss is a fair model; whether the unheralded-data-loss twirl and the "latent" accounting are what Tyler means; the hosting rule (ancilla = separate photon) and whether nondestructive readout changes the counts as claimed; whether the abort and retry modes bracket real heralded gates; the independence assumptions in the repeated-round recursion; whether 'silent per completed round' is the right headline metric.

## Task 2. Literature (do not rename anything)
Read in full: linear-optics gate success probabilities and what failure does to the data (review arXiv:1607.03935 and the gate papers it cites), fusion-based quantum computation (arXiv:2101.09310), the deterministic intra-photon CNOT (quant-ph/0402208), nondestructive photonic-qubit measurement (quant-ph/0312048 and the comment and reply, quant-ph/0406120 and quant-ph/0507175), loss tolerance and heralding of loss in dual-rail or polarization encodings, and coherent error amplification in gate-set characterization. Mark what you cannot find. Check the Majorana entries against primary sources; none is relied on.

## Task 3. Repository (only if Tyler asks)
Separate branch and pull request (not #1). Add the page and program. Do not touch Revision H, `library/`, `releases/`, research scripts, licences, tags or R30 files. No release, novelty, cost or advantage claims. Keep evidence tags and empty cost fields. IQA stays outside the frozen vocabulary and library.

## Open items (Tyler decides)
- Whether version 1.1 models one heralded two-photon gate in detail (failure types), per-time loss, and the conversion circuits under the physical model.
- Whether the capability-report fields in page section 12 are adopted.
- PALADIN, Docked Scheduling, resource-class names, BUD-xx identifiers and the third axis remain provisional.
