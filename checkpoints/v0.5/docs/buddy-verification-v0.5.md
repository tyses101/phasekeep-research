# Buddy verification, version 0.5

**Status: working draft for review. Ideal-model mathematics and a stated Pauli-fault model only. Not part of Revision H and separate from pull request #1. Builds on version 0.4 (not repackaged here); v0.1 to v0.4 stay as earlier checkpoints.**

Evidence tags: **DERIVED** (checked by `code/buddy_v05_checks.py` inside the stated model), **ASSUMED** (a parameter or modelling choice, not measured), **PROPOSED** (an idea or a test, not done), **UNVERIFIED** (supplied or remembered, and not checked), **MEASURED** (none exist). Physical cost fields are deliberately empty because no defensible apparatus parameters exist (audit item A02).

**Central research question (unchanged):** Can deliberate geometric organization and controlled transformation of photonic entanglement improve the efficiency, controllability, reliability or continuity of equivalent quantum operations?

**Program question (adopted by Tyler O'Bryan, subordinate to the central question):** Can a photonic processor adapt its information geometry, verification requirements and physical execution routes in response to changing operational conditions, while achieving a measurable advantage over conventional architectures? The central question sets what is investigated. The program question sets how findings are meant to be integrated into an operational machine.

## 1. What was done

Five studies, 33 checks, one stdlib program, all `ALL PASS` (under a second). All use the version 0.4 diagonal encoding (|0> = |00>, |1> = |11>) with a parity ancilla.

| Part | Study | Result [DERIVED] |
|---|---|---|
| 1 | Repeated checkpoints along one computation (exact dynamic programming) | A checkpoint chain reproduces the v0.4 single-checkpoint model exactly. Buddy-induced faults accumulate by closed forms. Spacing and placement matter: in the examples, checking every segment is worse than checking at an intermediate spacing, and checking only after the sensitive segment is worse than checking only at the end (section 6). |
| 2 | One stationary ancilla serving a stream of photons | With ideal reset, reuse changes nothing in this model. Without reset the ancilla reports **combined** parity, half of all photons are rejected whatever their quality, and flips can cancel. Reset quality matters only after a FAIL (section 7). |
| 3 | Parity router (even continues, odd goes to a rejection detector) | With loss, silence is not PASS. P(photon continues given no signal) falls below 1 as soon as loss exists (section 8). |
| 4 | Detect, reject, correct | The two-axis parity code detects single flips and cannot correct them. A three-axis repetition code with two checks corrects single flips and offers no phase protection (section 5). |
| 5 | Temporal validity of evidence | A closed form for how long a correct, verified state stays correct (section 9). |

## 2. How to read it

- Exact within the model. The Pauli model has independent X and Z faults on the two data axes, an ancilla X fault (flips the report), a harmful ancilla Z fault between the two CNOTs (acts as a Z on one data axis), and loss in the interaction. Every noise value is a sweep input or an example. None is a prediction about a device.
- The sweeps show how answers depend on inputs, and that the dependence can be non-monotonic. They do not say that any real Buddy helps.
- Resource classes, the lifecycle, the router and cooperative verification are PROPOSED architecture. Only the stated mathematics is DERIVED.

## 3. Correction to the v0.4 wording

Version 0.4 section 7 says the Buddy "never gives more correct results per run". That is **specific to the rejection-based Pauli model** of that page, in which the Buddy only removes outputs and cannot restore any. It does not apply to error-correcting architectures, which restore information (section 5). Version 0.4 is preserved unchanged. This page supersedes the wording.

Repeated checkpoints add a related point inside the same model: checking every segment can accept **fewer** correct runs than no checking, because two flips on one axis in different segments cancel, and a check after the first flip rejects a run that would have come out right (section 6).

## 4. Resource classes and a working Buddy definition (PROPOSED)

The five-layer hierarchy and the word "layer" are dropped. These are resource classes: selectable, not sequential, not mandatory. A checkpoint may use one or several.

| Resource class | Responsibility |
|---|---|
| Internal ancilla | Verification within a photonic register (an auxiliary Encoding Axie, left unspecified; path is the first candidate, provisionally) |
| Companion ancilla | Verification involving separate photonic registers |
| Stationary ancilla | Reusable quantum verification at checkpoints (atomic, spin or cavity-coupled system) |
| Collective ancillae | Coordinated extraction of multiple verification properties |
| Classical instrumentation | Equipment measurements and reference observations |

**Supervisory is not a resource class.** Interpreting evidence and authorizing continuation belongs to the Intelligent Register. Syndrome extraction by collective ancillae does not by itself constitute error correction.

Working definition (PROPOSED; the frozen Revision H glossary is not changed): **Buddy System: a coordinated set of ancillary quantum resources and classical instrumentation assigned to information checkpoints for heralding, detection and continuation assessment, with resources selected according to computational geometry, operational requirements and fault conditions.** "Ancilla" is the established term for an auxiliary quantum system used and then reset or discarded. It names a role, not a particle. Its first use in quantum information was not established. Buddy names the verification responsibility assigned to such a resource.

The path candidate is a priority judgment, not a ranking established by experiment. Candidates: path (first), frequency (second), radial mode (third), stationary spin (in parallel). Time stays outside the Encoding Axie architecture.

## 5. Detect, reject, correct (PART 4 [DERIVED])

| Capability | Function | Established here |
|---|---|---|
| Error detection | Identify that an error occurred | Yes, within the model (v0.4) |
| Error rejection | Prevent detected corrupted information from continuing | Yes, within the model (v0.4 and section 6) |
| Error correction | Restore the logical information under specified conditions | **Not established.** Shown to be impossible for the two-axis parity code |

- **Two-axis parity code.** A flip on axis a and a flip on axis b give the same syndrome (odd parity) and different states. Undoing the wrong one applies a logical X. So single flips are detected but cannot be corrected. Checked on 100 random logical states.
- **Three-axis repetition code** (span{000, 111}, checks on axes 1-2 and 2-3). Each single flip has its own syndrome and applying the matching X restores the state exactly. Two flips decode to the wrong axis and give a logical error. A Z error on any of the three axes is an undetected logical Z, so it exposes more axes to phase errors, and it uses three axes plus two ancilla bits for one logical qubit.
- Syndrome extraction identifies which axis flipped without anything being applied. The correction can be a physical X or a tracked frame update. Frame updates were not simulated.

## 6. Repeated checkpoints (PART 1 [DERIVED in the model; parameters ASSUMED])

Exact results (checkpoint count m, per-checkpoint fault rate g):
- Harmful Buddy Z faults only: false acceptance = (1 - (1 - 2g)^m) / 2, accepted-correct = (1 + (1 - 2g)^m) / 2.
- Ancilla X faults only: accepted-correct = (1 - g)^m, and the rest are false rejections of good data.
- Loss only: accepted-correct = (1 - l)^m.
- Expected Buddy interactions per run = the sum over k < m of (1 - g)^k. A rejected run stops using Buddy resources.

Flip noise only (no Buddy faults), T segments:
- No checkpoint: correct when each axis has an even number of flips, P = ((1 + (1 - 2x)^T) / 2)^2.
- One checkpoint at the end: the same accepted-correct probability as no checkpoint. It only removes the runs where both axes are odd.
- A checkpoint after every segment: accepted-correct = ((u + v)^T + (u - v)^T) / 2 and false acceptance = ((u + v)^T - (u - v)^T) / 2, with u = (1 - x)^2 and v = x^2. The undetected event is a double flip inside one segment. False acceptance falls far below end-only, and accepted-correct is lower than with no Buddy.

**Spacing sweep** (T = 8 segments, x = 0.02, z = 0.001, ancilla X fault 0.002, harmful Z fault 0.003, loss 0.002; ASSUMED). Unchecked: accepted-correct 0.7291, so about 27% of outputs wrong.

| Spacing | Checkpoints | Accepted-correct | False acceptance | Wrong among accepted | Buddy interactions |
|---|---|---|---|---|---|
| 1 | 8 | 0.6740 | 0.02941 | 0.04181 | 6.89 |
| 2 | 4 | 0.6952 | 0.02439 | 0.03389 | 3.55 |
| 4 | 2 | 0.7096 | 0.02552 | 0.03471 | 1.86 |
| 8 | 1 | 0.7241 | 0.03358 | 0.04432 | 1.00 |

For these inputs, the wrong share among accepted outputs is lowest at an intermediate spacing, and every spacing is far below the unchecked rate while giving up under 8% of the accepted-correct probability. Different inputs move the optimum.

**Selective example** (segment 4 has flip probability 0.1, others 0.005; z = 0.001, same Buddy faults; ASSUMED). Unchecked accepted-correct 0.7498.

| Policy | Accepted-correct | Wrong among accepted | Buddy interactions |
|---|---|---|---|
| End only | 0.7446 | 0.03962 | 1.00 |
| After the sensitive segment only | 0.7409 | 0.07213 | 1.00 |
| Sensitive segment and end | 0.7357 | 0.03731 | 1.80 |
| Every segment | 0.7031 | 0.05044 | 6.99 |

For these inputs, selective checking at the sensitive segment and at the end beats both extremes. A check only after the sensitive segment is worse than end-only, because later flips go unseen. This is an existence example for the hypothesis that selective checking can pay. It does not show that it does in any real system, and the fixed rule here is not an adaptive policy.

## 7. Reusable ancilla (PART 2 [DERIVED]; lifecycle PROPOSED)

The hardware can be reused. Its previous **state** cannot be ignored: it must be accounted for before the next interaction.

Lifecycle (PROPOSED): INITIALIZE, READY, INTERACT, READ, RESET, back to READY. Docked Scheduling accounts for initialization, interaction, readout and reset times. PALADIN handles identifiable hardware malfunctions. The Intelligent Register does not schedule an interaction with an ancilla whose readiness has not been established.

Results:
- **No reset between photons.** The ancilla reports the combined parity of the photons so far (checked on state vectors for two photons, all four flip patterns, 60 random states each). Two flipped photons report PASS. Combined parity is not useless: it measures a different property, which is useful when combined parity is deliberately the thing tested. It cannot substitute for independent checks.
- **Ideal reset.** Reuse gives exactly the v0.4 per-checkpoint outcomes.
- **Never reset** (steady state): half of all photons are rejected whatever their quality, good photons are falsely rejected half the time, and more wrong outputs are accepted than with ideal reset.
- **After a valid photon the ancilla is |0> for every pair of logical amplitudes.** It stores nothing about the state, only a parity bit when something is wrong. A parity ancilla is a witness, not a memory of the photon.
- **Imperfect reset** (steady state, x = 0.02, z = 0.001, gx = gz = 0.002, no loss; ASSUMED). False rejection rises first, since a stale FAIL contaminates the next photon, and false acceptance does not fall:

| Reset failure | Accepted-correct | False acceptance | False rejection |
|---|---|---|---|
| 0 | 0.95465 | 0.004302 | 0.00191 |
| 0.001 | 0.95462 | 0.004303 | 0.00195 |
| 0.01 | 0.95426 | 0.004316 | 0.00231 |
| 0.1 | 0.95035 | 0.004459 | 0.00622 |

- **Within one computation, reset quality does not matter in this model.** A run still alive has just read 0, so the ancilla is already clean. Reset matters across a FAIL, that is, across photons or runs. This model has no readout error.

## 8. Path-based parity filtering (PART 3 [DERIVED in the model]; device PROPOSED)

The idea (PROPOSED): separate the **physical rejection mechanism** from the **verification report**. A parity router sends even parity to the continuation path and odd parity to a rejection path with a detector. The survivors need not be read out, only routed. This is the filtering result of v0.4 realized spatially, and the rejection detector sits on the rejected port. Routing is not reading: reading the parity of a photon that continues is still the open problem. For this filter it may be needed only to establish continuation evidence, not to filter.

| Event | Observable |
|---|---|
| Odd parity, photon survives and is detected | FAIL signal |
| Even parity, photon survives | Continues (no signal) |
| Odd parity, photon survives but is not detected | Silence, and the photon does not continue |
| Photon lost | Silence |

With incoming odd probability q, survival t and detector efficiency eta: P(FAIL) = q t eta, P(continues) = (1 - q) t, and P(continues given silence) = (1 - q) t / (1 - q t eta). Example q = 0.02, t = 0.9, eta = 0.8: P(continues given silence) is about 0.895. So **no rejection signal means UNKNOWN, not PASS**, unless another resource class provides evidence that the photon passed. With no loss and a perfect detector and router, silence implies continuation. Router leakage (imperfect extinction) lets odd photons continue unflagged with probability q t times the leak. Open (UNVERIFIED): phase stability of the interferometer, an OAM-dependent router, presence evidence on the continuation path, and the router's effect on the even component's relative phase.

## 9. Temporal validity of evidence (PART 5; closed form DERIVED, use PROPOSED)

A valid report describes a condition established at a particular boundary. It is not a permanent guarantee. In the Pauli model the probability that a state correct at a checkpoint is still correct k segments later is

P(k) = ((1 + (1 - 2x)^k) / 2)^2 times [ ez^2 + (1 - ez)^2 ], with ez = (1 + (1 - 2z)^k) / 2

(matches exact enumeration). With x = 0.01 and z = 0.001 (ASSUMED): 1.0000 at k = 0, 0.9781, 0.9570, 0.9165, 0.8428, 0.7198, 0.5456 at k = 1, 2, 4, 8, 16, 32. For flip noise only it tends to 1/4, not 0.

PROPOSED use: a maximum **evidence age** (operations since the last check) is a classical scheduling constraint for Docked Scheduling. The Intelligent Register would re-verify or withhold authorization when the age exceeds the limit its calibrated noise implies. Time stays a classical schedule here, not an Encoding Axie. This section covers staleness between checkpoints. The within-circuit timing window of v0.4 section 6 (a flip after its own CNOT passes this round) is a different, narrower effect.

## 10. Cooperative verification (PROPOSED future investigation, nothing run)

Complementary resources with specialized responsibilities at one checkpoint: internal path ancilla (parity filtering), stationary ancilla (independent verification of an allowed property), classical instrumentation (hardware operating evidence), Intelligent Register (continuation decision), PALADIN (hardware fault isolation). The objective is sufficient evidence through complementary resources with minimum disturbance, not measuring everything. No demonstrated advantage. Open question for the study: does a second resource lower false acceptance more than it adds in its own faults, using the same accounting as section 6.

## 11. Simulation configurations requested for v0.5 and their status

| Configuration | Status |
|---|---|
| No Buddy | Done (baseline in section 6) |
| One Buddy checkpoint (reproduce v0.4) | Done, exact |
| Repeated independent checkpoints | Done |
| Reused ancilla with ideal reset | Done, equal to independent in this model |
| Reused ancilla with imperfect reset | Done (steady state across photons) |
| Reused ancilla without reset | Done (negative control) |
| Selectively activated Buddy | Done for a fixed rule; no adaptive policy |

Sweeps covered computational error rates, Buddy-induced errors, photon loss, reset errors and checkpoint spacing at the example points shown; they were not exhaustive grids. Reported: accepted-correct probability, false acceptance probability, wrong share among accepted, Buddy interactions (separate unit).

## 12. Working identifiers

BUD-01 to BUD-03 are in v0.4. BUD-04 is now done for repeated checkpoints in the Pauli model. BUD-05 (auxiliary Axie versus ancillary photon), BUD-06, BUD-07, PAL-01 and INT-01 are not started. PALADIN and Docked Scheduling remain provisional.

## 13. Prior art and sources (none read)

- Ancilla-based syndrome extraction, verified ancilla preparation and fault-tolerant extraction (including designs that suppress harmful fault propagation) are established quantum error-correction topics [UNVERIFIED, from memory]. The parity circuit here is a check of a known construction, not a new result.
- Cavity QED, photon-spin interfaces, quantum nondemolition measurement and flying-to-stationary qubit interactions are established fields [UNVERIFIED, from memory]. "Stationary" and "flying" qubits are common terms in quantum-network literature [UNVERIFIED].
- Linear-optics CNOT: Hofmann and Takeuchi, PRA 66, 024308 (2002); Kok et al. review, quant-ph/0512071 (titles only).

## 14. Limits

- Independent Pauli faults, one checkpoint model repeated. No correlated noise, no leakage out of the code, no readout error beyond the ancilla X fault, no loss correlated with the interaction, no timing window inside the circuit in part 1.
- Reuse is modelled as a steady-state stream, with a lost photon still having interacted. A different assumption changes numbers.
- The router results are probabilities of events, not an optical model.
- No physical Buddy, nondestructive parity read, resource-class comparison or cost figure exists in this work. The auxiliary-axis and stationary-ancilla comparisons remain unquantified.

## 15. Next study (PROPOSED)

1. Independent reimplementation (Codex) of all 33 checks.
2. Verified ancilla preparation and fault-tolerant extraction: verified preparation addresses initialization faults (ancilla X before the first CNOT), while the harmful fault is Z between the CNOTs, which needs a different fix. Study both in the fault model.
3. Path-based auxiliary Axie: interaction and readout requirements (theory).
4. Stationary ancilla timing in Docked Scheduling terms; multilevel resource-class comparison; PALADIN integration; cooperative verification.
5. The five-configuration comparison of v0.4 section 10, after a baseline workload is fixed.

## 16. Pending

PALADIN and identifier name checks; the third-axis decision (path provisional); independent reproduction; everything in the v0.3 and v0.4 Pending lists.
