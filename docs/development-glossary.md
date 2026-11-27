# PhaseKeep development glossary — HDOC

Updated 2026-11-27. **Development terminology adopted for review; separate from the frozen Edition 03 Revision H glossary.** HDOC belongs under Geometric Encoding Axies (GEA). It does not replace GEA or the Buddy System. No new physical capability or engineering advantage is established here.

[Research development](research-development.md) · [Frozen glossary](../library/markdown/A1-glossary.md) · [Library reader](https://tyses101.github.io/phasekeep-research/reader.html)

## High-Dimensional Orthogonal Configurations (HDOC)

**Families of mutually orthogonal quantum states, or mutually orthogonal subspaces, in a specified high-dimensional encoding space. Their structure and relationships are studied relative to a stated reference basis, subsystem partition, and allowed transformations.**

HDOC is a PhaseKeep organizational term for established mathematical objects, not a claim of new physics. The plural describes families and their relationships. A family need not span the full space; call it a basis only when it is complete. For subspaces, orthogonality requires every vector in one subspace to be orthogonal to every vector in the other; trivial intersection alone is insufficient.

Every description must specify the state space, reference basis, subsystem partition, and allowed operations. Amplitude distribution and coherence depend on the reference basis; separability depends on the partition; physical reachability and cost depend on the available operations.

## Capacity and flexibility

**Encoding capacity**, in this discussion, describes the dimension of the available encoding space. A dimension d supports at most d mutually orthogonal pure states. This is not by itself a communication-rate or computational-performance claim.

**Configuration flexibility** describes how that space can be organized and manipulated using the allowed operations. It is a descriptive distinction, not a new quantified resource measure. Amplitudes, relative phases, entanglement structure, occupied subspaces, preparation bases and measurement bases can change without increasing the space's dimension or changing the physical Encoding Axies. Which changes are reachable remains a device-dependent question.

An active transformation of a state, a change of measurement setting, and a passive change of coordinates are distinct actions. Merely rewriting a state in another basis does not physically transform it.

## Established mathematical vocabulary

| Term | Meaning and required context |
|---|---|
| Orthogonality | For pure states, zero inner product. Orthogonal states are perfectly distinguishable in principle by a suitable measurement; restricted apparatus may not implement it. Mixed states are perfectly distinguishable when their supports are orthogonal. |
| Overlap | For normalized pure states, the inner product is an overlap amplitude; its squared magnitude is the corresponding projective transition probability. State the convention. Mixed-state comparisons require a specified measure such as fidelity. |
| Completeness | A family spans the stated space. A complete orthonormal family in dimension d contains d states. |
| Mutual unbiasedness | Two orthonormal bases satisfy squared overlap 1/d for every cross-basis pair. Distinct orthonormal bases need not be mutually unbiased. |
| Separability | Across a specified partition, a pure state factors into subsystem states. A mixed separable state is a convex mixture of product states and may retain classical correlations. |
| Nonseparability | Failure of separability across the specified partition. For polarization and OAM on one photon, retain the library's qualification about internal nonseparability. |
| Unitary equivalence | A common unitary maps one specified family to the other. Any two complete orthonormal bases of the same finite-dimensional space admit such a map. This does not imply equal physical cost or reachability using restricted operations. |
| Coherence | Off-diagonal state components relative to a specified basis, associated with interference. Relative phases matter; global phase does not distinguish physical pure states. |
| Degeneracy | Multiple linearly independent eigenstates share an eigenvalue of a specified observable. This does not mean the states are identical. |

## Four layers of description

| Category | What to record |
|---|---|
| Configuration structure | Amplitudes, relative phases and occupation probabilities in a named reference basis. |
| Configuration relations | State overlap, orthogonality, family completeness and inter-basis mutual unbiasedness. |
| Internal correlations | Separability and entanglement measures across explicitly named partitions. |
| Configuration transformations | Active maps, basis conversions, subspace transfers, preserved properties and implementation constraints. |

Relations between states must not be confused with correlations within a state. A basis can contain only product states, only entangled states, or both. A basis containing both is a **mixed-composition basis**, not a mixed quantum state.

## Connection to existing PhaseKeep terms

Internal Entanglement and Coupled Photonic Entanglement (CPE) locate relationships within a photon or between photons. Symmetric Encoded Entanglement (SEE) and Nonsymmetric Encoded Entanglement (NEE) describe corresponding or noncorresponding encoded properties in the applicable arrangements. These are contextual descriptors, not independent switches that apply to every state. A separable state has no entanglement across the chosen partition to label SEE or NEE.

HDOC describes configuration families and their relationships. Controlled Transformation (CT) remains the broader operation category. Entangled Encoded Transformation (EET) describes deliberate changes to entanglement organization. Separability and nonseparability need no new acronyms.

A common unitary preserves state overlaps and orthogonality. Local unitaries preserve entanglement across their specified partition; operations coupling those subsystems may change it. Entangling capability is a property of an operation over possible inputs, not a guarantee that it entangles each input. Claims of preserving an entanglement amount must identify both the measure and partition.

## Proposed five-basis investigation — not executed

Construct a complete set of five mutually unbiased bases for the four-dimensional Tetragon, modeled as polarization times a two-mode OAM space. Record explicit vectors, ordering, phases, partition and reference basis before assigning physical interpretations.

| Research object | Planned quantity |
|---|---:|
| Dimension | 4 |
| Mutually unbiased bases | 5 |
| Distinct pure-state rays in their union | 20 |
| Unordered basis-pair comparisons | 10 |
| Directed transformations between different bases | 20 |

For basis matrices B_i with ordered basis vectors as columns, verify B_i† B_i = I and every cross-basis squared overlap equals 1/4. The active map U_(j←i) = B_j B_i† sends the kth vector of basis i to the kth vector of basis j. The passive coordinate conversion is B_j† B_i. Pairing and phase conventions affect the selected active map and must be recorded; there is no unique implementation cost for an unlabeled pair of bases.

For each active map, distinguish behavior on the four selected basis inputs from its capability on arbitrary product inputs. Classify separability preservation and entangling capability across polarization | OAM. Identify candidate optical implementations only with supporting sources and explicit apparatus assumptions. Record component count, calibration/stabilization requirements, loss, success probability and fidelity where supported; otherwise mark them UNVERIFIED. Mathematical existence alone supplies none of those costs.

Compare equivalent tasks and include the cost of entering and leaving a configuration. Investigate whether choosing the configuration in which an operation runs reduces total cost relative to a stated baseline. This overlaps established basis optimization and quantum compilation; novelty and benefit require specific comparative results.

**Configuration compatibility** remains a provisional research question, not an adopted glossary term or metric: suitability for the next operation, available components, existing entanglement, intended measurement and coherent continuation. An Intelligent Register could choose configurations from preparation records and calibrated models; it cannot freely inspect an unknown quantum state.

## Evidence and source status

Complete sets of d+1 mutually unbiased bases exist in prime-power dimensions. Thus dimensions 2, 4, 8, 16 and 4096 admit respectively 3, 5, 9, 17 and 4097 bases. This does not increase the maximum number of mutually orthogonal states in one such space beyond d, or establish practical access to every basis.

| Source | Relevance | Reading scope |
|---|---|---|
| [Wootters and Fields (1989)](https://doi.org/10.1016/0003-4916(89)90322-9) | Prime-power MUB construction | Publisher search summary; not full-text verified here. |
| [Wieśniak, Paterek and Zeilinger (2011)](https://arxiv.org/abs/1102.2080) | Entanglement constraints in complete MUB sets | Abstract inspected; full text not reviewed here. |
| [Lawrence (2011)](https://doi.org/10.1103/PhysRevA.84.022338) | Entanglement patterns under the stated generalized-Pauli eigenbasis assumption | Abstract inspected; do not extend its assumptions to arbitrary constructions. |

The unnamed 2026 review in the planning material remains unidentified and is not used as evidence. Earlier conversational numerical checks concerned illustrative vertex, distributed, Bell and mixed-composition bases, not a complete five-MUB construction. They were not independently reproduced by the user. **The five-basis experiment, transformation classification, optical implementation assessment and cost comparison remain PROPOSED and unexecuted.** No experimental measurements or new DOI are produced by this glossary update.

Revision H, its original archive, checksum manifest, release and educational library remain unchanged.
