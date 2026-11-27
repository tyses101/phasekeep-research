# Tetragon transformation map, version 0.3

**Status: working draft for review. Ideal-model mathematics only. Not part of Revision H and separate from pull request #1.**

Evidence tags: **DERIVED** (checked by `code/tetragon_map.py`, ideal noise-free operations), **PROPOSED** (an idea or a test, not done), **UNVERIFIED** (supplied or remembered, and not checked), **MEASURED** (none exist). Physical cost fields are deliberately empty because no defensible apparatus parameters exist (audit item A02).

## 1. What was done

One Tetragon (polarization H/V by OAM -1/+1, index = 2*pol + OAM) was analysed in eleven parts. All eleven run in one stdlib program and print `ALL PASS`. Version 0.1 added persistence, restricted subspaces, switching between encodings and the loss metric. Version 0.2 adds logical gates against geometry and targeted verification (sections 8 and 9). Version 0.3 adds the leakage-bias bound and operational redundancy (sections 9 and 10). Versions 0.1 and 0.2 stay as earlier checkpoints.

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

## 5. Persistence inside an entangled class (DERIVED, then PROPOSED)

Treat a maximally entangled state as a stored 2x2 unitary M, so the state is (M x I) applied to one fixed state. An operation on polarization multiplies M on the left. An operation on OAM multiplies it on the right by the transpose. 200 random single-axis operations on either axis therefore equal one 2x2 unitary on one axis, and the entanglement never changes (Schmidt weights 0.5 and 0.5).

- Work done entirely inside the class is composing single-qubit unitaries. A single polarization qubit does that with no entangled resource, so that is the baseline, and establishing the entanglement is overhead for that work. Reading the result out into a product basis costs an entangling step (section 1).
- Three kinds of persistence are worth separating: state persistence (ordinary coherent circuit behaviour), structural persistence (keeping an entanglement relationship; may give no advantage) and resource persistence (prepared resources held ahead of demand; this is the inventory-based mode of DDQT and brings storage, loss and consumption).
- "Persistent" can mean a flying photon passing through successive components, which is an ordinary circuit and needs no memory. Persistence in time needs storage or a delay loop.
- Teleportation consumes the entangled pair and is one way to move an unknown state. It is not the only way; a direct coherent transfer needs no pair.
- Break-even form [PROPOSED]: the sum over N operations of the saving s_i must exceed P + C + M, where P is preparation, C is conversion back, and M is maintenance, storage and scheduling. Every term must be in one stated metric. All terms are currently unknown.

## 6. Restricted input subspaces (DERIVED for the ideal model; physical advantage PROPOSED)

Substitution means an operation U on one axis acts the same as an operation V on the other. Three levels:

| Level | Condition | Status |
|---|---|---|
| Known configuration | holds for one specified state | Applies to prepared, known resources (DDQT inventory) |
| Restricted subspace | (U_A - V_B) P_S = 0 up to a global phase, P_S the projector onto the permitted subspace | Unknown amplitudes inside a known subspace; tested below |
| Entire register | holds for every input | Generally unavailable for distinct, independently controlled axes |

Result, for the Tetragon coordinate subspaces and the gates Z, S, S-dagger, X, H:

| Subspace | Pairs that act the same (one axis, other axis) |
|---|---|
| span{00, 11} | Z with Z, S with S, S-dagger with S-dagger (any phase gate on either axis) |
| span{01, 10} | Z with Z, S with S-dagger, S-dagger with S |
| every other coordinate subspace | none |

X and H are never substitutable. Checked with 50 random amplitude pairs on span{00, 11}: any phase gate gives the same state on either axis, with the amplitudes unknown.

What else the same subspace does (this is the two-qubit parity code, established):

- Inside the subspace the parity ZZ is +1. A single flip on either axis moves the state to parity -1 for any amplitudes, so a flip is detectable without learning them.
- A single phase error leaves parity at +1, so it is not detected, and the subspace cannot say which axis suffered it.
- A logical flip needs both axes (XX).
- Capacity falls from four dimensions to two.
- The operations that are substitutable are those whose difference acts as the identity on the subspace, and those are the same operators a parity check measures. A subspace therefore trades capacity for cheaper phase control and for flip detection.
- If the photon leaves the subspace, substitution fails silently, so membership has to be verified. A device that measures the parity without destroying the photon is an open item and is not verified.
- Only coordinate subspaces and this small gate list were searched. Other subspaces are open.

## 7. Adaptive representation: what switching encodings costs (DERIVED for the ideal model)

An encoding is an isometry E that places a logical qubit x into the Tetragon, state = E x. Switching from E1 to E2 for every allowed x means a unitary U with U E1 = E2. Some U always exists, so the question is its class. Two-vertex encodings come in two kinds: an **edge** (one bit differs; the photon is a product state for every x) and a **diagonal** (both bits differ; the photon is entangled for almost every x). Over all 12 ordered two-vertex encodings (144 ordered pairs, cheapest route found):

| From → to | Pairs | Cheapest route found |
|---|---|---|
| Edge → edge | 64 | 24 single-axis, 8 local on both axes, 32 need an axis SWAP (coupled, non-entangling) |
| Edge ↔ diagonal | 64 | all need one entangling gate plus local operations |
| Diagonal → diagonal | 16 | 12 single-axis, 4 local on both axes |

Reading it: encodings with the same entanglement structure are cheap to switch between. Moving between a product-type and an entangled-type encoding always needs an entangling step, and the unknown data has to be carried through it. So adaptive representation pays only if the benefit of the new encoding (cheaper axis control, section 6; detectable flips) exceeds the cost of the switch, and the number of switches matters as much as the benefit per stretch.

Other constraints: the subspace holds one qubit of the four-dimensional register, so capacity falls to two dimensions and the rest must hold nothing unknown. Established background (from memory, unverified): quantum subspace codes, logical-operator equivalence, adaptive compilation.

## 8. Logical gates and the geometry (DERIVED for the ideal model)

Let G be the intended logical operation and E the encoding. Then U E1 = E2 G says one physical operation U carries out G and also changes the encoding from E1 to E2. With E2 = E1 the geometry is fixed. With E2 free, the encoding is allowed to change. Over the 12 ordered two-vertex encodings (8 edge, 4 diagonal), the cheapest route found:

| Logical gate | From edge, geometry fixed | From edge, geometry free | From diagonal, geometry fixed | From diagonal, geometry free |
|---|---|---|---|---|
| X | single-axis | frame update only | both axes | frame update only |
| Z | single-axis | single-axis | single-axis | single-axis |
| S | single-axis | single-axis | single-axis | single-axis |
| H | single-axis | single-axis | one entangling gate | one entangling gate |

Reading it:

- **Only the logical flip gains from a free output geometry.** A logical X can be done by relabelling the encoding, with no physical operation, because the controller keeps track of which vertex is now logical 0. This is the same idea as Pauli-frame tracking in error correction (established; from memory, UNVERIFIED). It is a bookkeeping change: measurement outcomes are read through the tracked label, and if a later step needs the original physical encoding the cost reappears. It works for Pauli flips. Frames can often be carried through Clifford operations by known rules, while non-Clifford gates generally need a conditional correction or an adapted later gate rather than a pure relabelling (from memory, UNVERIFIED). Relabelling also changes how later gates are implemented, for example S on one axis pairs with S-dagger on the other in the second diagonal (section 6).
- **For these four gates the edge encoding is never more expensive than the diagonal one,** and it is cheaper for X and for H. Z and S are single-axis in both.
- **The diagonal encoding is valuable for something else:** either axis can apply a phase gate (section 6) and a single flip is detectable by parity (section 9).
- **Baseline.** A sequence of single-qubit logical gates on an edge encoding fuses to one unitary on one axis (section 5), so with fusion enabled its cost does not grow with the sequence length. Any comparison of fixed against adaptive geometry has to use that baseline. For one logical qubit, adaptive switching cannot save operations against it. Geometry could still matter where fusion is blocked (for example by verification checkpoints), where the axis carrying the data is the lossy one, for verification, and in larger multi-qubit registers (not tested).
- **Compatibility, restated from the reviews:** logical phase flip is one designated axis (edge) or either axis (diagonal); logical bit flip is one axis (edge) or both axes (diagonal); the Hadamard gate needed an entangling gate from the diagonal encoding; single physical flips are detectable from the diagonal encoding through parity, and in the edge encoding only for the axis that is held fixed.

## 9. Targeted verification of the diagonal encoding (DERIVED for the ideal model; the nondestructive version is open)

Knowing the pattern lets us design tests for it. It does not by itself show the photon follows the pattern.

- **Local settings.** For the state alpha|00> + beta|11>, measuring both axes in Z gives the parity (+1 inside the subspace) and logical Z. Measuring both axes in X and multiplying gives logical X. Measuring one axis in Y and the other in X gives logical Y. That is three settings, against nine local settings for full two-qubit tomography. All are destructive single-axis measurements and need no entangling gate. Checked with 100 random amplitude pairs.
- **Leakage is a statistics question.** If no leaked events are seen in n shots, the leakage rate is below about 3/n at 95% confidence (the "rule of three"): about 300 shots for 1%, 3,000 for 0.1%. This assumes identically prepared test photons, so it verifies the apparatus on test photons and says nothing about one particular computational photon.
- **Leakage checks do not confirm content or coherence.** The XX and YX settings are needed for that.
- **Settings and membership checks overlap in the destructive case.** The ZZ shot already gives each photon's parity, so membership needs no extra setting. For two diagonal-encoded qubits the 9 settings include both parities. A nondestructive check during the computation is separate and open.
- **Leakage bias is bounded.** XX and YX both commute with ZZ, so they have no cross terms between the in-subspace and leaked parts. If a fraction eps has leaked into the odd-parity subspace, the measured XX or YX value is within eps of (1 - eps) times the true logical value (2000 random states, two operators each). eps comes from the ZZ setting. Arbitrary errors outside the subspace are not covered by this bound.
- **A nondestructive parity measurement** is the verification we want, and a photonic implementation is not established.
- **Larger registers.** For a stabilizer-type subspace of 2^3 = 8 dimensions inside 12 binary axes, membership is defined by 12 - 3 = 9 independent parity checks. This was not computed here, and general subspaces are open.

## 10. Two Tetragons and operational redundancy (DERIVED for the ideal subspace; benefits PROPOSED)

Question: how many physically distinct operations implement the same logical gate? Counted by program.

| Logical gate | Axes that can carry it by a single-axis operation, edge encoding | Same, diagonal encoding |
|---|---|---|
| Z | 1 | 2 |
| S | 1 | 2 |
| X | 1 | 0 (both axes needed) |
| H | 1 | 0 (an entangling gate is needed) |

Two photons, each carrying one logical qubit. A physical controlled-phase between one axis of photon A and one axis of photon B implements the logical controlled-phase gate for these axis pairs:

| Photon A encoding | Photon B encoding | Equivalent axis pairs |
|---|---|---|
| edge | edge | 1 |
| edge | diagonal | 2 |
| diagonal | diagonal | 4 |

A controlled-phase inside one diagonal-encoded photon acts as a logical Z on that qubit.

Reading it:

- **Redundancy exists for phase-type gates.** For X and H the diagonal encoding has no alternative route. It needs both axes or an entangling gate, so it depends on more hardware being available, not less. The diagonal encoding is not uniformly more robust.
- **Illustrative availability.** If each interaction is available with probability 0.9 and failures are independent: four routes give 99.99%, one route 90%, and two interactions both needed 81%. Independence is an assumption. Shared sources, shared calibration or a component used by two routes would cut the benefit.
- **Illustrative route choice** (hypothetical numbers from the review; not measured): the interactions' transmissions of 98%, 94%, 96% and 99% correspond to losses -ln(eta) of 0.020, 0.062, 0.041 and 0.010. A controller would choose the 99% route and fall back to the 98% route if the first became unavailable, with no change to the logical operation.
- **What it does not change.** One photon-to-photon entangling interaction is still needed. That is the expensive kind of interaction, and intra-photon and photon-to-photon costs must be modelled separately.
- **Equivalent is not independent.** The routes are equivalent on the specified subspace. That each is physically available, shares no component with another, and has the same error profile has not been established.
- **Hypothesis (PROPOSED):** encodings could be designed to maximise the number of physically distinct, equivalent routes, so a machine keeps operating as equipment conditions change. This must beat established redundancy and hardware-aware compilation to count as an advantage.

## 11. Cost metric and fusion (PROPOSED, with illustrative numbers)

- Use L = -ln(eta) for loss. It adds across components where transmissions multiply. At 99% per interaction (illustrative): 1 interaction leaves 99.0%, 10 leave 90.4%, 50 leave 60.5%, 100 leave 36.6%, 200 leave 13.4%. Keep latency, fidelity, throughput and component count as separate metrics and report each.
- **Fusion.** A sequence of known operations collapses to one unitary (ideal). Physically it is one apparatus setting that may need several elements (a general polarization unitary is said to need up to three wave plates; from memory, UNVERIFIED). The controller must know the whole sequence in advance.
- **Fusion against verification.** A destructive check on the computational photon ends that photon. A check inside a fused sequence prevents fusing across it. Checks on separate test photons need not interrupt fusion. Where to place verification is a research question.

## 12. Prior art (titles from a search; none of these has been read)

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

## 13. Limits

- Stabilizer bases and Clifford operations only. Other constructions and non-Clifford operations are not tested.
- The route search order is not a minimal gate count.
- Ideal pure states and noiseless operations. Nothing about loss, fidelity, noise, devices or measurement statistics.
- The restricted-subspace search covers coordinate subspaces and a small gate list only. The switching table covers two-vertex encodings and the same route order. The logical-gate table covers X, Z, S and H and the 12 coordinate output encodings only. The two-photon result is an ideal-subspace equivalence with one photon-to-photon interaction type (controlled phase).
- The program was written and run by one author and has not been independently reproduced.

## 14. Next ideal-model study (PROPOSED)

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

## 15. Pending

Independent numerical reimplementation (a different library), reading the sources in section 12, a literature check of novelty, and the abbreviation-conflict search. Docked Scheduling is a provisional proposed name and appears here only as described in section 4.
