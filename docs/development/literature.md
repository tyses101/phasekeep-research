# Literature and evidence status

**Status: working development record, 2026-11-27.** Every entry below is **UNVERIFIED** unless it says otherwise. "Read" here means the level recorded in the checkpoint pages, which is title, abstract or an excerpt, never full text. Abstract-level reading does not verify a claim against the body of a paper. Nothing in this table is used as evidence that a PhaseKeep configuration works.

## Established techniques that the checkpoints re-use

PhaseKeep makes no novelty claim for any of the following. They are named so that readers can see which parts of the checkpoints are standard.

| Technique | Where it appears | Source named in the checkpoint | Reading level |
|---|---|---|---|
| Ancilla-based parity and syndrome extraction for stabilizer codes | [V0.4](checkpoints/v0.4.md) onward | General knowledge, no paper cited | From memory, not looked up |
| Flag qubits for fault-tolerant extraction | V0.9 "J flag" | Chao and Reichardt; Chamberland and Beverland | Title or abstract level |
| Verified cat-state ancillas | V0.9 "J cat (verified)" | Shor (1996) | Title level |
| The [[k+2,k,2]] iceberg code with flags and post-selection ([[4,2,2]] is k = 2) | Joint geometry, flagged round | Self, Benedetti and Amaro; Linke et al., arXiv:1611.06946 | Abstract level |
| Steane-style and Knill-style extraction | V0.9 | Named only | **Not implemented**, not read |
| Code switching | Conversion in [V0.8](checkpoints/v0.8.md) | arXiv:1403.2734, arXiv:1703.03860 | Titles only |
| Pauli-frame tracking | [V0.2](checkpoints/v0.2.md) | General knowledge | From memory |
| Coherent error amplification by repeating a gate | [V1.0](checkpoints/v1.0.md) | General knowledge | From memory. An established principle; no invention is claimed |
| Rule of three for zero-event confidence bounds | [V0.2](checkpoints/v0.2.md) | General knowledge | From memory |

## Photonic gates, loss and readout (V1.0)

| Topic | What was seen | Reading level | Use |
|---|---|---|---|
| Linear-optics two-qubit gates (review arXiv:1607.03935, partial) | Success probabilities 1/4, 1/16, 2/27, 1/9 and 1/2 for several constructions. The excerpt did not say what a failure does to the data | Excerpt | The V1.0 success values (1, 0.75, 0.5, 0.25, 1/9) were chosen to span these; the effect of failure on data is open |
| Deterministic CNOT between two axes of one photon (quant-ph/0402208) | Described as deterministic | Abstract | Supports the assumption that gates between axes of one photon can be deterministic; no performance figures seen |
| Fusion-based quantum computation (arXiv:2101.09310) | Fusions are probabilistic in linear optics; one quoted scheme tolerates 10.4% photon loss per fusion | Abstract | The field's own treatment of probabilistic gates and loss; **not modelled** in V1.0 |
| Measuring a photonic qubit without destroying it (quant-ph/0312048) | Linear optics plus photodetection of ancillary modes; non-deterministic | Abstract | Supports that non-destructive readout exists in principle and is probabilistic. A published comment (quant-ph/0406120) exists and was **not read** |
| Majorana tetrons (arXiv:2507.08795 and coverage of a June 2026 InAs-Pb result) | 2025 device: X loop 14.5 µs, Z loop 12.4 ms, assignment errors 16% and 0.5%. The newer result is a characterization reporting Z parity only, with no gates; critics dispute the topological identity | Abstract and news coverage | Only a prompt for per-observable readout error. **The 2025 X/Z figures belong to the earlier device.** No Majorana claim is relied on |

## Earlier prior-art titles (V0.1 to V0.5)

Titles from a search, relevance inferred from the title only, none read: General U(4) gate for photon polarization and OAM (arXiv:1012.2704); single-photon two-qubit SWAP gate (quant-ph/0407136); deterministic CNOT for single-photon two-qubit logic (quant-ph/0402208); high-dimensional single-photon quantum gates (arXiv:1702.07299, cited in the frozen library at abstract level); arbitrary unitaries in OAM (arXiv:2106.11046); measurements in two bases for certifying high-dimensional entanglement (arXiv:1709.07344); characterization of high-dimensional entangled systems via mutually unbiased measurements (arXiv:1212.5825); entanglement in qudit circuit compression (arXiv:2209.14584); OneQ photonic compilation (arXiv:2209.01545); time-multiplexed photonic C-NOT (arXiv:2412.02478); fibre-loop multiplexed preparation (arXiv:1503.03546); linear-optics CNOT (Hofmann and Takeuchi 2002; Kok et al. review, quant-ph/0512071).

Each interface that PhaseKeep examines (gates between axes of one photon, certification cost, compilation, time multiplexing) already has published work. No claim is made that any intersection is unstudied, and novelty has not been established.

## Frozen library and pull request #1 sources

The Revision H source list and its read status are in [Appendix 3](../../library/markdown/A3-sources.md). Pull request #1's eight sources and read statuses are in [Research development](../research-development.md), section 10; only one was read in full, by an automated reader whose equations came out garbled.

## What remains to be done

Full-text reading of every source above that a result depends on; the DDQT originals; naming-conflict searches for SEE, NEE, CPE, EET, IEE, PALADIN, Docked Scheduling, Convergent Entanglement and IQA; and a review of the photonic-gate and fusion literature for what a failed heralded gate does to the data. See [Open problems](open-problems.md).
