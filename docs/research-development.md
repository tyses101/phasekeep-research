# PhaseKeep research development

**Status: working draft for review. Not part of Revision H.** Revision H (release `edition-03-rev-h`) is frozen and is not changed by this page. Terminology here is provisional. Nothing on this page has been measured.

Evidence tags used below: **DERIVED** (follows from the mathematics and was checked by a program), **REPORTED** (stated in a paper; the read status is given in the source table), **PROPOSED** (a design idea or a name, not tested), **UNVERIFIED** (not yet checked by anyone other than the author), **MEASURED** (none yet).

## 1. The research question

> Can deliberate geometric organization and controlled transformation of photonic entanglement improve the efficiency, controllability, reliability or continuity of equivalent quantum operations?

This is a question, not a result. No advantage has been demonstrated. "Equivalent" matters: any comparison has to be between ways of doing the same operation, with the same target and the same success criterion. Section 7 says what such a comparison would need.

The working order of the research programme is: generation, encoding, entanglement organization, controlled transformation, verification, preservation, continuation of computation. This is a reading order for the questions, not a claim that each step has been shown to work.

## 2. What is established physics and what is PhaseKeep naming

| Term | Meaning on this page | Classification |
|---|---|---|
| Hyperentanglement | Entanglement across two or more degrees of freedom of the same photon pair. | Established physics |
| High-dimensional entanglement | Schmidt rank (pure state) or Schmidt number (mixed state) above 2 across a stated partition. | Established physics |
| Entanglement preservation | Keeping a stated entanglement property through storage, transmission or operations. | Established research objective |
| Hybrid entanglement | Entanglement between different degrees of freedom. | Established physics; Nonsymmetric Encoded Entanglement (NEE) maps onto it |
| Internal Entanglement | Non-separability between distinct encoded properties of a single photon. | PhaseKeep educational term. The literature debates whether to call this "entanglement" (see sources). The library's own wording is "non-separable". |
| Coupled Photonic Entanglement (CPE) | Entanglement between separate photonic subsystems. | PhaseKeep educational term for inter-photon entanglement |
| Symmetric Encoded Entanglement (SEE) | Entanglement arranged between corresponding encoded properties across separate registers. | PhaseKeep classification, defined relative to a chosen partition |
| Nonsymmetric Encoded Entanglement (NEE) | Entanglement arranged between noncorresponding encoded properties across separate registers. | PhaseKeep classification; related to hybrid entanglement |
| Integrated Entangled Environment (IEE) | An organized configuration of encoded subsystems with specified entanglement relationships, inside a State Space Environment. | Proposed architectural concept, provisional (section 5) |
| Entangled Encoded Transformation (EET) | A controlled transformation intended to change how entanglement is organized. | Proposed; a specialized Controlled Transformation (CT) |

None of these names is a claim of new physics. They are labels for relationships that are already described by standard quantum information theory.

## 3. Quantity versus organization

The point of the new terms is to separate two properties that are easy to confuse:

- **Quantity** of entanglement between two parts, for example the number of ebits across the photon-A | photon-B partition.
- **Organization** of that entanglement, meaning which encoded properties are paired with which.

Every statement about organization depends on a stated partition. Here the partition is four two-level subsystems: A-polarization, A-OAM, B-polarization, B-OAM. SEE and NEE describe how entanglement maps onto these four chosen axes. They are not intrinsic kinds of entanglement.

### Worked example (DERIVED, [`code/entanglement_organization.py`](../code/entanglement_organization.py))

Two photons, each carrying a Tetragon (polarization × OAM ±1, four addresses per photon). The joint Hilbert space is 16-dimensional; this does not mean that all 16 basis states are simultaneously occupied.

| | Matching (SEE-type) | Cross (NEE-type) | GHZ-type, four subsystems |
|---|---|---|---|
| Schmidt rank across photon A \| photon B | 4 | 4 | 2 |
| Entanglement between the photons | 2 ebits | 2 ebits | 1 ebit |
| Rank across the matched split (A-pol,B-pol \| A-OAM,B-OAM) | 1 | 4 | 2 |
| Rank across the cross split (A-pol,B-OAM \| A-OAM,B-pol) | 4 | 1 | 2 |
| Product of two entangled pairs? | Yes, matched split only | Yes, cross split only | No, under any split |
| Genuinely multipartite entangled? | No | No | Yes |

How to read it: the matching and cross states hold the same amount of entanglement between the photons. They differ only in which properties are paired. A rank of 1 across a split means the state factors across it, so under the matched split the matching state is one polarization Bell pair times one OAM Bell pair.

Three results the program checks:

1. Single-axis local unitary transformations preserve the relevant pairing structure and bipartite entanglement. The program checks random local unitary rotations on all four subsystems for the matching example, retaining its pairing and 2 ebits.
2. A SWAP of the two axes on photon B turns the matching state exactly into the cross state. The inter-photon entanglement stays at 2 ebits. The ideal axis SWAP is a coupled operation: it does not generate entanglement between the two swapped axes from their product states, but can reorganize existing entanglement relationships with other subsystems.
3. Four levels per photon do not guarantee high-dimensional entanglement. A state built from two of the four levels on each side has Schmidt rank 2 and 1 ebit.

The third column is there so that the diagrams do not suggest that all entanglement is made of pairs. A GHZ-type state across the four subsystems is entangled, is not a set of pairs under any of the three splits tested, and has only 1 ebit between the photons even though each photon has four levels.

### Limits of this check

The worked-example table displays three bipartitions. The multipartite verification function checks all seven unique bipartitions of the four subsystems, with some redundant complementary checks (and returns early if it finds a rank-1 cut). The examples use ideal pure states with equal weights. They say nothing about noise, loss, mixed states, or how these states would be made or measured. Genuine multipartite entanglement is tested by the condition that no bipartition gives rank 1. Claude reported passing checks; the earlier attempted independent ZIP verification did not successfully execute. This repository integration records its own single lightweight regression run below. Independent mathematical reimplementation remains pending.

## 4. Conceptual organization

This is a conceptual organizational structure, not a strict mathematical hierarchy.

| Group | Terms and role |
|---|---|
| Foundational pillars | Geometric Encoding Axies (GEA); Buddy System |
| Environments | State Space Environment (SSE); Integrated Entangled Environment (IEE), explicitly PROPOSED and provisional |
| Entanglement framework — location | Internal Entanglement (within one photon); Coupled Photonic Entanglement (CPE, between photons) |
| Entanglement framework — organization | Symmetric Encoded Entanglement (SEE, corresponding encoded properties); Nonsymmetric Encoded Entanglement (NEE, noncorresponding encoded properties) |
| Entanglement framework — extent | Hyperentanglement; High-Dimensional Entanglement |
| Operations and objectives | Controlled Transformation (CT); Entangled Encoded Transformation (EET), a specialized CT; Entanglement Preservation |

Notes on the definitions:

- "Symmetric" in SEE and "nonsymmetric" in NEE describe arrangements relative to specified Encoding Axies and subsystem partitions. They do not describe mathematical symmetry or asymmetry of the entire quantum state. NEE concerns noncorresponding encoded properties; section 2 cross-references conventional hybrid entanglement.
- SEE and NEE describe particular arrangements that can exist within CPE. They do not cover every entangled state.
- Hyperentanglement and high-dimensional entanglement are different properties. A pair entangled in four OAM states is high-dimensional but not hyperentangled. A polarization pair plus an OAM pair on the same two photons is both.
- "Coupled" is used twice in the library: CPE names a relationship between photons, and a *coupled operation* (Volume 6) is one that does not factor per axis. They are different things, one a state relationship and one a transformation. They are kept apart by always writing "CPE" or "coupled operation".
- Preservation always names what is kept: the amount of entanglement, its dimension, its pairing, or fidelity to a target state. Keeping one does not keep the others.

## 5. Integrated Entangled Environment (provisional)

The proposed distinction is between what a system makes possible and how entanglement is currently organized in it:

| State Space Environment (SSE) | Integrated Entangled Environment (IEE) |
|---|---|
| Available state space | Prepared entangled configuration |
| Available Encoding Axies | Participating encoded subsystems |
| Available transformations | Specified entanglement relationships |
| Physical connectivity | Organization of quantum correlations |
| Operational constraints | Required entanglement preservation |

IEE remains explicitly **PROPOSED** and provisional. It has not yet been shown to do work that "an SSE holding entangled registers" does not, and "integrated" is already a common word in photonics. It stays only if a later reporting format or an experiment needs it, and it will be dropped otherwise. An IEE does not imply genuine multipartite entanglement.

An Intelligent Register could coordinate operations from known preparation information, calibrated transformations and measurement results. It cannot inspect the complete unknown quantum state, and any description that implies it can is wrong.

## 6. Reporting an Entangled Encoded Transformation

An EET is a Controlled Transformation whose purpose is to change entanglement organization. The independent / coupled / entangling classification from Volume 6 describes how it behaves mathematically. EET describes why it is applied. Both are kept.

Every EET report should fill in this table. Evidence classifications are mandatory for each individual reported property, not merely for the row or EET as a whole. If a cell contains multiple claims, label each claim separately; an ideal-map result must not lend its evidence status to a physical-device, loss or coherence claim.

| | Before | Operation | After | Evidence tag |
|---|---|---|---|---|
| Encoding | Initial encoding | Targeted Axies | Resulting encoding | |
| Entanglement | Initial entanglement (amount, partition) | Applied transformation and its class (independent / coupled / entangling) | Resulting entanglement | |
| Arrangement | Pairing before | Intended change | Pairing after | |
| Coherence | Coherence at input | Expected losses | Remaining coherence | |
| Carriers | Available carriers | Required resources | Available output carriers | |

Example entry (the ideal SWAP re-pairing above): encoding, two Tetragons in the specified ideal model [DERIVED]; inter-photon entanglement, 2 ebits before and after [DERIVED]; operation, axis SWAP on photon B, coupled and non-entangling on product inputs of the swapped axes [DERIVED]; arrangement, matching to cross [DERIVED]. Physical implementation [UNVERIFIED], device losses [UNVERIFIED] and experimentally retained coherence [UNVERIFIED] are unspecified; they are not consequences of the ideal-map calculation. An EET is wider than this one example, since it could also produce more complex correlation structures, but the SWAP case is the only one checked so far.

## 7. How the question could be tested

None of this has been done. It is the minimum a fair comparison would need.

1. **Fix the task.** Choose a target operation and a success criterion before comparing methods, for example a stated transformation on stated inputs to a stated fidelity.
2. **Fix the baselines.** At least one conventional way of doing the same operation, and one PhaseKeep organization, using the same photon source and the same loss budget.
3. **Name what is being compared:** efficiency (resources or success probability), controllability (how many independent settings and how precisely they are set), reliability (fidelity and variance over repeats), continuity (whether the state survives a sequence of operations and the herald and Buddy checks still pass).
4. **Count the cost of checking.** The currently proposed PhaseKeep verification approach uses destructive measurements in multiple bases across repeated preparations. This does not claim that all possible quantum verification methods are necessarily destructive. A scheme whose check costs more than it saves has not improved efficiency.
5. **Report failures and unknowns.** Buddy Checks return PASS, FAIL or UNKNOWN, and UNKNOWN is a legitimate result.

Related open items:

- Whether the independent / coupled / entangling sorting predicts cost for the same task is open (Volume 11). The operator-rank gate-count floor is a lower bound that is not tight: SWAP has operator Schmidt rank 4, the floor for CNOT gates is 2, and the exact circuit uses 3. It does not predict optical component count.
- A physical device for the axis SWAP is open (Volume 5).
- Nondestructive certification of the encoded state (A04) and apparatus mapping (A02) are open.
- Encoding-basis counts alone cannot certify coherence or entanglement. An entangled pair's joint address counts equal those of a classical pairing with no entanglement.

## 8. What this page does not claim

- No quantum or efficiency advantage has been shown.
- No measurement of any PhaseKeep state exists. Everything quantitative above is ideal-state mathematics.
- The five two-Tetragon correlation patterns are not reported by any paper cited here. Graffitti et al. made a hyperentangled source and tomography against a GHZ-type target, and reported no gates and no Bell violation. It is not evidence for the matching or cross states.
- The names are labels. They do not name new physical phenomena.
- Operator Schmidt rank measures how far an operation is from factoring per axis. It is not interaction strength and not entangling power.

## 9. Pending checks

- Comprehensive naming-conflict search for the abbreviations SEE, NEE, CPE, EET and IEE. Not done.
- Full-text verification of every cited source. Only one source was read in full, through an automated reader whose equations came out garbled.
- Independent mathematical reimplementation of the new program, preferably in a different language or library, and independent review of the Volume 6 checks remain pending. The single integration regression run is not a mathematical reimplementation.
- Reconcile the A03 / A04 numbering with R30 (library: A03 herald validity, A04 nondestructive certification).
- Unsourced inputs in the memory-chain estimate (4%, 12.6%, 0.49, 23%) remain unsourced.

## 10. Sources and read status

| Source | Used for | Read status |
|---|---|---|
| Graffitti et al., arXiv:2006.01845 | Hyperentanglement; polarization-OAM non-separability; 16-dimensional tomography (fidelity 95.0%, purity 92.4% against a GHZ-type target) | Full text through an automated reader; equations garbled and one state-label inconsistency reported. Numbers to be checked against the PDF. |
| Terhal and Horodecki, quant-ph/9911117 | Schmidt number | Abstract only |
| Ma, Qarry, Kofler, Jennewein, Zeilinger, arXiv:0904.3245 | Hybrid entanglement | Abstract only |
| Aiello et al., arXiv:1409.0213 | Debate on "classical entanglement" within one beam | Abstract only |
| Barreiro et al., Nature Physics 4, 282 (2008) | Hyperentanglement and Bell-state analysis | Opening summary only |
| Barreiro et al., quant-ph/0507128 | Hyperentanglement | Abstract only |
| Babazadeh et al., arXiv:1702.07299 | High-dimensional single-photon OAM gates (as cited in the library) | Abstract only |
| Ozawa and Price, arXiv:1910.00376 | Synthetic-dimension background (as cited in the library; verification of its use remains pending in the separate research workflow) | Abstract only |

The remaining references in the library (Appendix 3) have their own recorded read status. "Abstract only" means the claim was taken from the abstract and not checked against the body of the paper.

## 11. Feedback

Corrections and challenges are welcome through [GitHub Issues](https://github.com/tyses101/phasekeep-research/issues/new/choose), using the correction template. Revision H and its release assets are unchanged by this page.

## 12. Integration verification record

The supplied archive's four manifest checksums were verified during this integration.
Claude's earlier passing checks are reported provenance, not independently
confirmed results; the attempted separate independent ZIP verification did not
successfully execute. Codex executed the supplied program once as the requested
lightweight regression check: it exited successfully and reported `ALL PASS`.
This does not constitute independent mathematical reimplementation. No additional
simulation, literature verification or independent mathematical reimplementation
is part of this update. All source read statuses above remain as supplied.

Revision H remains the [frozen educational baseline](../library/index.html), with
its [release](https://github.com/tyses101/phasekeep-research/releases/tag/edition-03-rev-h)
and original bytes unchanged. This page is provisional development documentation.
