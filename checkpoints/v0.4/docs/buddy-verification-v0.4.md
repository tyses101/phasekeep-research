# Buddy verification, version 0.4

**Status: working draft for review. Ideal-model mathematics and a stated Pauli-fault model only. Not part of Revision H and separate from pull request #1. Builds on, and does not replace, the Tetragon map v0.3 (v0.1 to v0.3 stay as earlier checkpoints).**

Evidence tags: **DERIVED** (checked by `code/buddy_checks.py` inside the stated model), **ASSUMED** (a parameter or modelling choice, not measured), **PROPOSED** (an idea or a test, not done), **UNVERIFIED** (supplied or remembered, and not checked), **MEASURED** (none exist). Physical cost fields are deliberately empty because no defensible apparatus parameters exist (audit item A02).

**Central research question (unchanged):** Can deliberate geometric organization and controlled transformation of photonic entanglement improve the efficiency, controllability, reliability or continuity of equivalent quantum operations?

**Program-level question (PROPOSED, subordinate to the central question):** Can a photonic processor adapt its information geometry, verification requirements and physical execution routes in response to changing operational conditions, while achieving a measurable advantage over conventional architectures?

## 1. What was done

The Buddy idea (a check that tests a property of the information without reading the information) was reduced to its simplest case: one diagonal-encoded Tetragon (logical |0> = |00>, |1> = |11>, even parity) and one auxiliary binary system, the Buddy ancilla. Four studies were run in one stdlib program, 26 checks, all `ALL PASS` (runs in under a second).

| Identifier | Study | Result [DERIVED] |
|---|---|---|
| BUD-01 | Ideal parity extraction | Two CNOTs onto the ancilla leave a valid even-parity state unchanged with the ancilla at 0. One flip gives ancilla 1 with the logical amplitudes carried through unchanged. One phase error leaves the ancilla at 0, so it is **not detected**. Keeping only ancilla = 0 gives a success probability equal to the even-parity weight, leaves survivors unchanged and returns the ancilla to |0>: the check turns flips into loss, it does not correct them. It destroys coherence **between** parity sectors and keeps coherence **within** the even sector. |
| BUD-02 | Detectable and undetectable errors | Over the 15 non-identity two-axis Paulis, both encodings detect 8, leave 6 as undetected logical errors and 1 harmless. The distribution differs (section 5). |
| BUD-03 | Buddy-induced faults | A Z fault on the ancilla between the two CNOTs becomes an undetected logical phase error **and** a PASS report. An X fault on the ancilla gives a false FAIL on valid data and leaves the data untouched (section 6). |
| BUD-04 | Accounting model | Under the stated Pauli model the Buddy never gives more correct results per run than the same encoding without it; it only lowers the share of wrong results among those accepted. With flip noise only, accepted outputs are purer than the no-Buddy baseline exactly when the harmful Buddy fault rate is below 2x(1-x), where x is the flip probability per axis (section 7). |

## 2. How to read it

- These are exact results for ideal gates (BUD-01, BUD-02, BUD-03) and for a **stated** independent-Pauli model (BUD-04). The noise values in BUD-04 are sweep inputs. They say how the answer depends on the inputs. They are not predictions about any device.
- "Buddy" here is one verification responsibility. Its physical carrier is open (section 8). No claim is made that a physical Buddy exists, that parity can be read without destroying the carrier, or that a Buddy improves any real system.
- The program names the helper "ancilla", which is the established term for an auxiliary quantum system that is used and then discarded or reset. The library glossary defines "Ancillary (auxiliary) photon" more narrowly, as a helper photon that is measured instead of kept. The two do not conflict, but the library wording is a special case of the general meaning.

## 3. Definitions (PROPOSED)

**Buddy.** One verification responsibility, with several possible physical implementations: ancillary photon, reference photon, auxiliary Encoding Axie, classical instrumentation, or a hybrid. It needs access to the properties the information is expected to obey. It does not hold a copy of the information (no-cloning forbids that).

**Heralding, detecting, continuation** (three functions, not three subsystems):

| | Question | Produces evidence | Can consume the information |
|---|---|---|---|
| Heralding | Did the intended event occur? | Yes, by a defined success signal | Depends on the protocol |
| Detecting | What condition exists? | Yes, by a measurement | Destructive version yes; nondestructive version only if the property is read without reading the logical content |
| Continuation | Can execution proceed? | No, it evaluates evidence | It must preserve what the next step needs |

A herald has a defined relationship to the event it reports and is not automatically proof of state fidelity (library: herald probability versus herald reliability). Authorization to continue does not prove physical integrity.

**Information checkpoint.** An execution boundary associated with a classical record of expected quantum properties, verification evidence and continuation criteria. It does not store a recoverable copy of an unknown quantum state. The machine may restart from a known preparation procedure. It cannot roll back an unknown computational state.

**Checkpoint record fields.** Expected geometry; expected property; heralding result; detection result and measurement type (destructive or nondestructive); each check's result as PASS, FAIL or UNKNOWN (the library's Buddy Check vocabulary); a confidence estimate for the Buddy's own report; properties **NOT TESTED** (this avoids the library tag UNVERIFIED, which means "supplied or remembered, and not checked"); continuation decision and basis. Hardware status belongs to PALADIN, not to Buddy.

**Four outcomes of a Buddy report** (the false acceptance row is the dangerous one):

| Information | Report | Outcome |
|---|---|---|
| Correct | PASS | True acceptance |
| Incorrect | FAIL | True rejection |
| Correct | FAIL | False rejection |
| Incorrect | PASS | **False acceptance** |

Errors the Buddy **fails to detect** and errors the Buddy **introduces** are separate engineering problems (sections 5 and 6). A Buddy earns its place only if it lowers the overall risk of undetected error after its own faults are counted.

## 4. BUD-01: ideal parity extraction [DERIVED]

Three binary axes (a, b carry the qubit, c is the ancilla), index 4a + 2b + c. Circuit: CNOT(a to c), CNOT(b to c), read c. Checked on 200 random logical states. The formula in the proposal, (alpha|00> + beta|11>)|0> for valid information and ancilla |1> for odd parity, is correct. The Buddy records parity without recording the logical amplitudes, but only within one parity sector: for a state that is a coherent superposition of even and odd parity, the read removes the coherence between the two. That is acceptable when odd parity means error. It would not be acceptable for an encoding whose valid states include both parities.

## 5. BUD-02: what is detected and what is not [DERIVED]

Diagonal code: span{00, 11}, check ZZ. Edge code: span{00, 01} (axis 1 fixed at 0, the qubit on axis 2), check on axis 1. For an edge encoding the only available check is on the idle axis, because checking the carrier axis would read the data.

| Error | Edge | Diagonal |
|---|---|---|
| X or Y on one axis | Idle axis: detected. Carrier axis: undetected logical X or Y | Detected on either axis |
| Z on a single axis | Idle axis: harmless. Carrier axis: undetected logical Z | Undetected logical Z (both axes) |
| Both axes flipped (XX, YY, XY, YX) | Idle axis flip detected, so detected | **Undetected logical error** (even number of flips) |
| All 15 non-identity two-axis Paulis | 8 detected, 6 logical, 1 harmless | 8 detected, 6 logical, 1 harmless |
| Single-axis errors only (6) | 2 detected, 1 harmless, 3 logical | 4 detected, 0 harmless, 2 logical |

Reading: the diagonal encoding sees flips on **both** carrier axes, which is what "both Axies through parity" means, and the edge encoding sees none on its carrier axis. Both are blind to phase errors, and the diagonal encoding also exposes two axes to them. The diagonal encoding is not "better at detection" in general: it is better at detecting single flips on the axes that carry the data, at the cost of capacity (two axes for one logical qubit, plus the ancilla).

## 6. BUD-03: faults in the Buddy and during the check [DERIVED]

Every single X, Y or Z fault on the ancilla or on either data axis, at three positions in the circuit (before the first CNOT, between the two, after the second). Outcome is classified against the original correct data and does not depend on the amplitudes (10 random states per fault).

**Faults on the Buddy ancilla (Buddy-induced):**

| Fault | Before CNOT1 | Between CNOTs | After CNOT2 |
|---|---|---|---|
| X | False rejection | False rejection | False rejection |
| Z | Harmless | **False acceptance** (becomes a logical phase error on the data) | Harmless |
| Y | False rejection | Rejection of data the Buddy also damaged | False rejection |

**Faults on the data during the check (not Buddy-induced, but they show a timing window):** Z faults always pass (false acceptance, as in section 5). A flip on axis a after its CNOT, or on axis b after the second CNOT, passes **this** round's check. It would be caught by the next round. A check detects errors that occurred before its own CNOTs act.

Consequences [DERIVED for the ideal circuit; PROPOSED for any design]:
- A Buddy report is evidence with its own error rates, so every report needs a confidence field.
- The harmful Buddy fault is a Z fault between the CNOTs. A design that makes that location less error-prone matters more than one that makes the ancilla readout better.
- PALADIN-style classical hardware diagnostics cannot necessarily see an ancilla phase error (section 9).

## 7. BUD-04: does the Buddy make the whole computation more reliable? [DERIVED in the model, parameters ASSUMED]

Model of one diagonal checkpoint: independent X faults on each data axis (probability x), Z faults on each data axis (z), an ancilla X fault (gx, flips the report), a harmful ancilla Z fault between the CNOTs (gz, acts as a Z on one data axis), loss in the Buddy interaction (l). Outcomes: accepted-correct, false acceptance, false rejection, rejection of damaged data, lost. They sum to 1 over the whole grid tested.

1. **No Buddy faults, no loss, no Z noise:** false acceptance is x^2 (a double flip), accepted-correct is (1-x)^2.
2. **The Buddy never raises the number of correct results per run.** Accepted-correct never exceeds the no-Buddy correct probability of the same encoding (for z up to 0.5). Its value is that fewer of the **accepted** outputs are wrong, and that a rejected run can stop before the rest of the computation is spent on it.
3. **A Buddy can lower reliability.** With no data noise at all, a 1% harmful ancilla fault rate gives 1% false acceptance, where the unchecked encoding is perfect.
4. **Exact threshold:** with flip noise only, accepted outputs are purer than the unchecked same-encoding baseline exactly when gz is below 2x(1-x), the probability of an odd number of data flips. The Buddy must not introduce more harmful faults than it removes. For example, at x = 1% the harmful Buddy fault rate must stay below 1.98%.
5. **Dephasing-dominated noise defeats it.** With Z noise z = 0.1 and small x, the diagonal encoding with a Buddy is not purer than a single unchecked axis, because it exposes two axes to Z and the Buddy cannot see Z.
6. **Break-even downstream cost D\*** (in units of one pre-checkpoint stage): the minimum cost of the rest of the computation above which checking pays, assuming wrong outputs can be identified and discarded at the end [ASSUMED]. Illustration with gz = 0.001, l = 0, Buddy interaction cost 0.2 stage: D\* is 10.7 at x = 1%, 5.3 at 2%, 2.1 at 5%, 1.1 at 10% [parameters ASSUMED, arithmetic DERIVED]. D\* is infinite (the Buddy never pays) when gz is above the purity limit, and rises with the Buddy's own cost.

The question the model answers is the one the review put: not whether the Buddy can detect an error, but whether adding it makes the whole computation more reliable than leaving it out. The answer depends on the noise ratio, the harmful Buddy fault rate and the cost of what follows. It is not yes or no in general.

## 8. Auxiliary Axie versus ancillary photon (PROPOSED; unresolved)

| Property | Auxiliary Axie | Separate ancillary photon |
|---|---|---|
| Additional photon required | No | Yes |
| Additional encoding capacity required | Yes (three axes for one logical qubit) | No |
| Interaction type | Intra-photon | Inter-photon |
| Independent carrier | No | Yes |
| Readout without destroying the data carrier | **Unresolved** | Possible in principle |
| Resource overhead | Unquantified | Unquantified |
| Fault propagation | Requires investigation (section 6 applies to the circuit either way) | Requires investigation |

- The third axis is **left unspecified**. Candidates (path, frequency, radial mode) are to be judged on controllability, coupling requirements, selective readout, loss and compatibility with the existing axes. Time stays outside the Encoding Axie architecture, because a quantum time-bin control would be a quantum control register, not the classical schedule of Docked Scheduling (v0.3, section 4).
- Intra-photon gates may be deterministic in principle, while photon-photon CNOTs in linear optics are probabilistic. This is **UNVERIFIED**: the search found only titles (Hofmann and Takeuchi, PRA 66, 024308 (2002); the linear optical quantum computing review quant-ph/0512071) and none was read.
- Reading one axis without destroying the others (and without reading the data) is the open engineering problem, and the filtering result in BUD-01 needs it.

## 9. PALADIN (PROPOSED; provisional)

Protective Autonomous Logic for Anomaly Detection, Isolation and Neutralization. **Neutralization** is defined narrowly as rendering an identified faulty component unable to interfere with continued system operation. It does not mean repairing corrupted quantum information.

| Responsibility | Buddy | PALADIN |
|---|---|---|
| Quantum parity verification | Yes | No |
| Hardware operating limits | Supporting evidence | Yes |
| Verification equipment diagnostics | Supporting evidence | Yes |
| Autonomous hardware isolation | No | Yes |
| Quantum error correction | Not established | No |
| Fault propagation containment | Information-level rejection | Physical isolation |

Two boundaries (section 6 is the evidence for the first): classical diagnostics may not see an ancilla phase error, and a failed quantum verification does not by itself identify a faulty component. PALADIN protects future operations and cannot recover information that is already destroyed.

Status: the name stays **provisional** until the abbreviation and literature checks are done. The vocabulary freeze (library Appendix 6) says a new term needs a literature check and a demonstrated purpose. The purpose proposed here is to keep hardware-fault handling separate from quantum-state evidence. That distinction is the thing to demonstrate. The function is close to standard fault detection, isolation and recovery practice in engineering systems [UNVERIFIED, from memory], so the check should look for that overlap. One quick search found no obvious conflict among the returned titles, which is not a conflict check.

## 10. Five-configuration comparison: specification (PROPOSED, nothing run)

Each configuration runs the **same logical workload** under comparable physical assumptions, with every noise and loss parameter swept and labelled ASSUMED.

| Configuration | Purpose |
|---|---|
| 1. Fixed edge, fused | Conventional baseline (including fusion of consecutive operations, v0.3 section 11) |
| 2. Fixed diagonal | Geometric redundancy and verification benefit |
| 3. Adaptive geometry | Whether switching produces a net benefit (switching costs from v0.3 section 7) |
| 4. Adaptive + Buddy | Verification cost and detection capability |
| 5. Adaptive + Buddy + PALADIN | Hardware faults, isolation and alternative routing |

The simulation must separate: errors introduced by computational operations; errors introduced by verification; errors detected and rejected; errors accepted without detection; photon loss; hardware unavailability; geometry conversion overhead; fault isolation and recovery overhead.

Principal results: accepted-correct output probability, false acceptance probability, resource cost per accepted correct result. Costs are reported in **separate units** (photons consumed, interactions, execution time, optical components) and are not merged into one score. Output is parameter sweeps and break-even curves: the aim is to find the conditions under which a Buddy pays, not to assume them.

Availability and transmission are separate quantities. Route availability (can the route be used) is not photon transmission (does the carrier survive it). If a photon is lost on one route, the machine cannot send the same photon through another, and PALADIN cannot recover information already destroyed. The 99.99% figure for four routes at 90% availability (v0.3 section 10) assumes independent routes and a controller that knows which are available before sending. Routes that share hardware would have correlated failures.

Metrics (PROPOSED): route availability; transmission; conditional fidelity; heralding reliability; detection sensitivity; false rejection rate; **false acceptance rate**; verification disturbance; continuation probability; fault containment time; recovery time; cost per accepted correct result.

Verification policies to compare (PROPOSED by the reviewer, untested): fixed (predetermined checkpoints), selective (at operations with elevated expected error risk), adaptive (frequency and geometry follow calibrated conditions and earlier evidence). The hypothesis that selective checking balances reliability against accumulated disturbance better than fixed checking is **untested**.

## 11. Working identifiers

The earlier stage labels B01 to B09 collide with audit items already in the library (B02 and B03 are used in `11-experiments.md`). Proposed working identifiers, not new scientific terminology: BUD-01 ideal parity extraction; BUD-02 detectable and undetectable errors; BUD-03 Buddy-induced faults; BUD-04 repeated verification overhead; BUD-05 auxiliary Axie versus ancillary photon; BUD-06 two-Tetragon verification; BUD-07 adaptive verification selection; PAL-01 autonomous hardware fault isolation; INT-01 integrated execution and continuation. Of these, BUD-01 to BUD-03 are done here, BUD-04 is done for one checkpoint only (accumulation over repeated checkpoints is not modelled), and BUD-05 to INT-01 are not started.

## 12. Prior art and sources (none read)

- Ancilla-based syndrome extraction for stabilizer codes is established quantum error-detection mathematics [UNVERIFIED, from memory; not looked up]. The circuit in BUD-01 is its simplest instance, so BUD-01 is a check of a known construction, not a new result.
- Fault propagation through the extraction circuit (the section 6 Z-fault result) is a known issue in that literature, and "flag" or fault-tolerant extraction designs address it [UNVERIFIED, from memory].
- Linear-optics CNOT: Hofmann and Takeuchi, PRA 66, 024308 (2002) (title only); Kok et al., review, quant-ph/0512071 (title only).
- The word "ancilla" is Latin for a female attendant. Its use in quantum information for an auxiliary system is standard. Who first used it there was not established.

## 13. Limits

- Ideal gates, then independent Pauli faults on one checkpoint. No correlated noise, no leakage out of the code, no measurement error beyond the ancilla X fault, no accumulation over repeated checkpoints, no loss correlated with the interaction.
- The Pauli model gives exact answers inside itself. Whether real noise is Pauli-like is not addressed.
- The break-even calculation assumes wrong outputs can be identified and discarded at the end. If they cannot, the accepted-output error rate is the right measure and D\* does not apply.
- No physical Buddy, nondestructive parity read, or cost figure exists in this work.

## 14. Next study (PROPOSED)

1. Independent reimplementation (Codex), then BUD-04 over repeated checkpoints with accumulation.
2. BUD-05 on a defined third axis once one is chosen; BUD-06 two-Tetragon verification.
3. The five-configuration simulation specified in section 10, after the baseline workload is fixed.
4. Abbreviation and literature checks for PALADIN, and the reading of the sources in section 12.

## 15. Pending

- Independent reproduction of all 26 checks.
- PALADIN name check; third-axis choice; whether the wider program question is adopted alongside the central one.
- Everything in the v0.3 Pending list (A03/A04 numbering, memory-chain inputs, licence text, Zenodo/DOI status, pull request #1 decisions).
