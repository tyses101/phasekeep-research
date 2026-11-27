# Tetragon transformation map, version 0

**Status: working draft for review. Ideal-model mathematics only. Not part of Revision H and separate from pull request #1.**

Evidence tags: **DERIVED** (checked by `code/tetragon_map.py`, ideal noise-free operations), **PROPOSED** (an idea or a test, not done), **UNVERIFIED** (supplied or remembered, and not checked), **MEASURED** (none exist). Physical cost fields are deliberately empty because no defensible apparatus parameters exist (audit item A02).

## 1. What was done

One Tetragon (polarization H/V by OAM -1/+1, index = 2*pol + OAM) was analysed in four parts. All four run in one stdlib program and print `ALL PASS`.

| Part | Question | Result [DERIVED] |
|---|---|---|
| Bell family | Four maximally nonseparable states A=(00+11), B=(00-11), C=(01+10), D=(01-10), each over sqrt 2. Which operations move among them? | Single-axis flips and phase flips give the table in the pasted review exactly, signs included. Of the 24 permutations of {A,B,C,D}, single-axis Clifford operations produce 4 and local Cliffords on both axes produce all 24. A controlled phase and a local S on both axes induce the same relabelling (A and B swap). The axis SWAP leaves all four labels fixed and flips one sign. |
| Either-axis control | Does acting on polarization equal acting on OAM? | For state A, a rotation R on polarization equals R-transpose on OAM. This is a property of that one maximally entangled state, not of the operations. |
| Time | Does letting the photon's time bin choose the operation matter? | With time bins in superposition, "no operation in slot 0, polarization flip in slot 1" creates 1 ebit between time and polarization. The same operation in both slots creates none, and a single definite slot creates none. So a classical schedule adds no entanglement, and time as a quantum control does. |
| Stabilizer bases | What are the complete mutually unbiased bases (MUBs) in four dimensions? | Of the 15 Pauli-stabilizer bases, 9 are product bases and 6 are maximally entangled. They form 6 complete MUB sets of 5 bases. Each set has 3 product and 2 entangled bases, and each basis lies in exactly 2 sets. The encoding basis and the Bell basis are in no common set (overlaps are 0 and 0.707, not 0.5). |
| Basis map | Which operation class links each of the 225 ordered pairs of bases? | See the table below. |

Basis map (cheapest route found, searching single-axis Clifford, then local Clifford on both axes, then one controlled phase between local stages):

| From → to | Pairs | Route |
|---|---|---|
| Product → product | 81 | 45 single-axis, 36 local on both axes |
| Entangled → entangled | 36 | all single-axis |
| Product ↔ entangled | 108 | all need one entangling gate plus local operations |
| Total | 225 | 81 single-axis, 36 local on both axes, 108 with an entangling gate |

The single-axis count includes the 15 trivial pairs of a basis with itself.

## 2. How to read it

- **The entangled family is reachable by one axis because every maximally entangled two-qubit state is a one-sided unitary applied to one fixed state.** That is a standard fact, so the "reversal of intuition" is mild. It is the same fact as the either-axis result.
- **It maps whole bases onto bases.** It ignores which state goes where and the relative phases. "Complete coherent operation equivalence" is the finer question and is open.
- **Within the Bell family, single-axis control is the Pauli-type set only.** By hand (not checked by program for non-Clifford operations), a single-axis unitary that keeps the Bell set in itself must be a Pauli, so 4 of the 24 relabellings. Anything else in that encoding needs both axes. This bounds the hypothesis in section 3.
- **Basis changes have a price.** Moving between product and entangled bases always needs an entangling step in this ideal model. A passive change of description, an active transformation and a change of measurement basis can use similar matrices and are physically different. The cost of entering and leaving a configuration belongs in every comparison.

## 3. Hypothesis (PROPOSED)

> A sequence of useful operations that stays within one entanglement class could avoid repeatedly establishing and removing entanglement, and might be cheaper than the same sequence done conventionally.

Stages: establish the entanglement structure, manipulate within it, convert when the computation requires. Mapping unordered bases is not executing logical operations, so this is untested. A fair test names the task, the baseline gate set and the metric before comparing (see `docs/research-development.md`, section 7).

## 4. Time

The clock means a **classical schedule** (Docked Scheduling, provisional name). A time bin in superposition selecting the operation is a quantum control register and is not what the schedule means. Reusing one component for successive photons adds no loss per photon. Sending one photon repeatedly through a component needs a return path or storage, and loss compounds: at 99% per pass, 100 passes transmit 36.6% (illustrative, not an apparatus figure).

## 5. Prior art (titles from a search; none of these has been read)

Marked UNVERIFIED. Relevance is inferred from the title only.

| Title | Reference | Why it may matter |
|---|---|---|
| General U(4) gate for photon polarization and orbital angular momentum | arXiv:1012.2704 | Gates between the two axes of one photon |
| Single-photon two-qubit SWAP gate for entanglement manipulation | quant-ph/0407136 | An axis SWAP; bears on the open device question in Volume 5 |
| Deterministic Controlled-NOT gate for single-photon two-qubit logic | quant-ph/0402208 | Entangling gate between axes of one photon |
| High-Dimensional Single-Photon Quantum Gates: Concepts and Experiments | arXiv:1702.07299 | Already cited in the library at abstract level |
| Arbitrary unitaries in orbital angular momentum of single photons | arXiv:2106.11046 | OAM control |
| Measurements in two bases are sufficient for certifying high-dimensional entanglement | arXiv:1709.07344 | Cost of verification; may mean fewer than d+1 bases are needed to certify dimension |
| Characterization of high-dimensional entangled systems via mutually unbiased measurements | arXiv:1212.5825 | MUBs in verification |
| On the role of entanglement in qudit-based circuit compression | arXiv:2209.14584 | Compilation and entanglement |
| OneQ: A Compilation Framework for Photonic One-Way Quantum Computation | arXiv:2209.01545 | Photonic compilation; entanglement as a persistent resource |
| Demonstration of a quantum C-NOT Gate in a Time-Multiplexed fully reconfigurable photonic processor | arXiv:2412.02478 | Time multiplexing and component reuse |
| Multiplexed single-photon state preparation using a fibre-loop architecture | arXiv:1503.03546 | Loop-based reuse |

Reading: each interface PhaseKeep examines (gates between axes of one photon, certification cost, compilation, time multiplexing) already has work on it. No claim is made here that any intersection is unstudied, and novelty has not been established.

## 6. Limits

- Stabilizer bases and Clifford operations only. Other constructions and non-Clifford operations are not tested.
- The route search order is not a minimal gate count.
- Ideal pure states and noiseless operations. Nothing about loss, fidelity, noise, devices or measurement statistics.
- The program was written and run by one author and has not been independently reproduced.

## 7. Next ideal-model study (PROPOSED)

Preserve ordered state mappings and relative phases. For each candidate operation record:

| Field | Values |
|---|---|
| Works on | one known state / a stated family / arbitrary allowed inputs |
| Preserves relative phases | yes / no / not checked |
| Effect on entanglement | preserved / changed |
| Axis control needed | independent / coupled / entangling |
| Equivalent alternatives | listed |
| Cost of entering and leaving the configuration | listed |
| Physical cost | **empty until apparatus parameters exist** |

## 8. Pending

Independent numerical reimplementation (a different library), reading the sources in section 5, a literature check of novelty, and the abbreviation-conflict search. Docked Scheduling is a provisional proposed name and appears here only as described in section 4.
