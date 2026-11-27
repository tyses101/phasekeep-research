# Buddy verification, version 0.9: how reliable is the verifier itself, and what should it become?

Project: PhaseKeep Research. Owner: Tyler O'Bryan. Written by Claude. Versions 0.1 to 0.8, Revision H and pull request #1 are preserved unchanged. The wording corrections to version 0.8 are in section 1 as an erratum. Nothing here has been independently reproduced, and nothing here is a hardware result or a claim of advantage over any architecture.

Evidence tags: **DERIVED** (follows from the stated model: ideal Clifford circuits, exact Pauli-frame propagation of every single fault and every pair of faults, exact convolution of independent location faults, 16- to 64-dimensional state vectors), **ASSUMED** (a noise value, fault model or gate set chosen as an example), **PROPOSED** (a design idea), **UNVERIFIED** (literature recalled or read only at abstract level), **MEASURED** (none), **BLOCKED** (needs something I do not have).

Central question: *Can deliberate geometric organization and controlled transformation of photonic entanglement improve the efficiency, controllability, reliability or continuity of equivalent quantum operations?*
Programme question (subordinate): *Can a photonic processor adapt its information geometry, verification requirements and physical execution routes in response to changing operational conditions, while achieving a measurable advantage over conventional architectures?*
The question version 0.9 puts: **how reliable is Buddy's own extraction, which established method should be the baseline, and what should Buddy's configurations be before anything is added to its responsibilities?**

**How to read the numbers.** The qubits in every circuit here are generic Pauli-noise qubits with ideal Clifford gates. No photon loss, no probabilistic two-photon gates, no hardware. The fault probability *p* is "per circuit location" and is a parameter, not a prediction. Gate counts, ancilla counts and measurement counts are *structural proxies*, not costs; the physical-cost fields stay empty (audit item A02). No combined score is formed anywhere; where a choice is shown, it is a feasible set and a Pareto set over separate metrics. The conventional local round remains the baseline in every table.

## 0. Summary

| Question | Answer within the model | Tag |
|---|---|---|
| Can flagged extraction remove silent logical damage from single ancilla faults? | **Yes at first order**: zero silent cases among all 196 single faults of the flagged joint round (model M2) and all 460 (model M3). The conventional joint round has 4 silent of 128 fault cases (all weight 2, the "hook"); the conventional local round has 8 of 68 (all weight 1, because the local code cannot see Z) | DERIVED |
| Does flagging remove silent damage altogether? | **No.** A distance-2 code needs two faults to fail silently, and fault pairs still do it: second-order coefficient 2.320 flagged versus 2.427 conventional joint (M2). Flagging only moves the dominant term from *p* to *p*² | DERIVED |
| Does the flagged round always beat the conventional one? | **No (negative result).** Counting only Buddy's own gate faults (M2) flagged is best at every *p* tested. Counting idle faults too (M3), the longer flagged circuit loses to the conventional joint round above *p* ≈ 1.1e-3 per location | DERIVED on ASSUMED fault model |
| Is the cooperative variant a good idea? | **Not in the form tested (negative result).** A two-cat-qubit round that couples the two axes of one photon to each cat qubit stays non-fault-tolerant even with a verified cat: a cat-qubit X fault after verification becomes a weight-2 logical error. 0.8 silent per unit *p* (M2) versus 0 for the flagged and verified-cat rounds | DERIVED |
| Does the extra verification machinery make the data safer? | **Mixed.** It removes silent damage but increases the number of fault cases that leave *some* damage on the data (3.2, 6.9, 9.1, 16.8 per unit *p* for local, joint, flagged, verified cat) and the rejection rate (flagged rejects about 3 times as often as local at *p* = 1e-3). Whether that pays depends on what the rejected rounds cost | DERIVED |
| Can verification run concurrently with computation? | **Partly.** An in-code rotation can be inserted after *k* data couplings of a check exactly when its generator commutes with the part of the check already coupled. Of 18 weight-2 joint generators, interior windows exist for 34 of 54 (generator, slot) pairs in the native order, and every generator has a window under some coupling order. Flags do not change the windows | DERIVED, confirmed by 1,638 state-vector simulations |
| Can reference preparations establish operational assurance? | For a *constant* error of an apparatus: yes, with a stated number of runs (12 runs for 1 rad, 119,829 for 0.01 rad at 95%). They say nothing about an individual unknown state, and a reference set must contain non-eigenstates of every error generator it is meant to expose | DERIVED |
| Does the evidence support "Buddy has several physical configurations selected by IQA"? | It supports the *possibility*: no configuration is best on all separate metrics, and the Pareto set changes with *p* and with the requirement. It does not show the configurations are worth their combined complexity, and every comparison is within one abstract fault model | DERIVED, hypothesis open |

## 1. Erratum to version 0.8

Version 0.8 stays as delivered. One wording correction to its page, one earlier chat statement, and one convention note.

**E4. What is valid during conversion.** Version 0.8's page says the verification "must be suspended or follow the transported group" during conversion. The first half is too strong. The correct statement: during the conversion circuit H(a1), H(b1), CNOT(a1 to a2), CNOT(b1 to b2) the **transported checks exist at every step and read +1 exactly on converted logical states** (worst deviation 8.9e-16 in the state-vector test). What stops being valid is the **complete original check set** (local checks after the first gate, joint checks before the last), and, for the half-way groups, neither full code's check set. Whether Buddy can *physically measure* the intermediate weight-3 checks is a separate, open question (it needs two-photon couplings).

| After n gates | Transported checks (signed, expected +1) | Weights | Photons per check |
|---|---|---|---|
| 0 | +ZZII, +IIZZ | 2, 2 | 1, 1 |
| 1 | +XZII, +IIZZ | 2, 2 | 1, 1 |
| 2 | +XXII, +IIZZ | 2, 2 | 1, 1 |
| 3 | +XXXI, +ZIZZ | 3, 3 | 2, 2 |
| 4 | +XXXX, +ZZZZ | 4, 4 | 2, 2 |

**Earlier chat statement (not in a delivered file).** I said "no valid check exists during conversion". That was wrong, and you corrected it; the table above is the correct statement.

**Convention note.** A check is a signed Pauli whose expected value for valid information is +1. Where an unsigned observable with a changing expected value is easier, state which one is used so the sign is not applied twice. Unchanged from version 0.8.

## 2. Established techniques versus PhaseKeep adaptations

I read the following **at abstract or excerpt level only**; none has been read in full or independently checked, and identifiers need confirmation against the repository's literature table. All of this is **UNVERIFIED** as to details.

| Technique | What I believe it establishes | Status in this page |
|---|---|---|
| Cat-state ancillas verified before use (Shor, 1996) | Fault-tolerant syndrome measurement with a prepared, checked ancilla | Implemented as "J cat (verified)" |
| Flag qubits (Chao and Reichardt; Chamberland and Beverland, arbitrary distance) | A flag ancilla wrapped around the middle of a check circuit catches the faults that would spread to more than one data error, with few extra qubits. The condition is that the leftover errors have distinct nontrivial syndromes | Implemented as "J flag" for ZZZZ and XXXX |
| The [[k+2,k,2]] iceberg code with flag ancillas and post-selection (Self, Benedetti and Amaro; the [[4,2,2]] code is the k = 2 case; also Linke et al., arXiv:1611.06946) | Syndrome circuits for this code family with no undetected logical error from single faults, with post-selection; logical gates are *not* fault tolerant | Our joint geometry is that code; our flagged round is an instance of the same idea (the paper's exact circuit order may differ: unchecked) |
| Steane-style and Knill-style extraction | Alternatives using encoded ancillas or teleportation | **Not implemented** here (the 4-axis code is too small for them to be a fair comparison) |
| Code switching (arXiv:1403.2734, 1703.03860; titles only) | Moving between codes with different gate sets | Related to the conversion of version 0.8; not read |
| "Quantum Assurance" as a name | Already used by other groups | Open from before; not studied here |

**What is PhaseKeep's, and what is not.** The flagged and verified-cat rounds are established methods applied to a code that is already in the literature. Version 0.9 adds only (i) the *local* four-axis geometry as a baseline, (ii) the question of choosing among configurations at run time, (iii) the concurrency-window rule, and (iv) the capability-report interface. None of these is claimed to be new; I have not searched for prior work on (ii) to (iv).

## 3. Fault models, and what "silent" means

Every circuit is a list of ideal Clifford operations (preparations in |0> or |+>, H, CNOT, CZ, Z or X measurement). A *location* is any gate, preparation or measurement (M2), plus every idle live qubit after every operation and one incoming fault per data axis (M3). A location fails with probability *p*, then applies a uniformly random non-identity Pauli to the qubits it touches (a measurement flips its result). Pauli faults propagate through Clifford circuits linearly, so one fault's effect is the XOR of its effects; this is how every single fault and every pair is enumerated, and how the exact distribution is computed.

For each fault case the program records the detector flips (parities of measurement records) and the data error left at the end of the round, and classifies it:
- **silent**: every detector reads PASS, and the data error is a logical operator of the code (accepted and wrong);
- **accepted-damaged**: PASS, but the data error is detectable by the code's checks (it will show in the next round);
- **rejected**: some detector fired (with or without damage on the data).

**Model M1** (ancilla-only faults, a single check at a time) reproduces the version 0.8 table exactly (18 versus 30 fault cases, 4 versus 12 multi-axis data errors, 2 versus 2 silent, 2 versus 6 damaged), so the engine agrees with the earlier program where they overlap.

**Weight must be taken modulo the stabilizers.** ZZZZ, XXXX and YYYY act trivially on the information, so a weight-3 error such as ZZZI is equivalent to the weight-1 error IIIZ. Version 0.9 first printed raw weights (the flagged round seemed to pass weight-4 errors), which was the wrong measure; modulo the stabilizer group the flagged and verified-cat rounds pass nothing worse than weight 1, as they should.

## 4. Priority 1 and 2: flagged and verified extraction against conventional extraction

Coefficients are per unit *p* for a single fault (first order) and for pairs of faults at different locations (second order). Model M2 (Buddy's own gate, preparation and measurement faults):

| Round | Locations | Fault cases | Silent, first order | Accepted-damaged | Rejected with no damage | Rejected with damage | Silent, second order |
|---|---|---|---|---|---|---|---|
| Local conventional (baseline) | 8 | 68 | 0.533 | 1.067 | 3.867 | 1.600 | 1.244 |
| Joint conventional | 12 | 128 | 0.267 | 2.133 | 4.133 | 4.533 | 2.427 |
| Joint flagged | 20 | 196 | **0.000** | 1.867 | 9.067 | 7.200 | 2.320 |
| Joint verified cat (4 cat qubits) | 40 | 316 | **0.000** | 2.667 | 17.733 | 14.133 | 9.902 |
| Joint cat, unverified | 32 | 248 | 1.867 | 4.267 | 12.800 | 8.533 | 12.338 |
| Joint cooperative (2 cat qubits, one per photon), verified | 28 | 240 | 0.800 | 2.133 | 12.933 | 8.533 | 10.000 |
| Joint cooperative, unverified | 20 | 172 | 2.133 | 2.133 | 8.000 | 5.067 | 4.933 |

Model M3 (adds idle faults and incoming data faults): silent first order 11.200 (local), 0.267 (joint), 0.000 (flagged), 0.000 (verified cat), 5.867, 4.133 and 4.800 for the other three. The local value is large because the local code cannot see the Z faults that Buddy's gates and idling leave on the data; this reflects the code, not just the extraction.

What each result means:
1. **Flagged extraction does eliminate first-order silent damage under both M2 and M3** (priority 1 answered, within the model). Modulo stabilizers every accepted round leaves at most a weight-1 data error, against weight 2 for the conventional joint round (10 fault cases).
2. **It does not eliminate silent damage**: the pair coefficient (2.320) is about the same as the conventional joint round's (2.427). The verified cat is about four times worse at second order (9.902) because it has 40 locations.
3. **Exact probabilities (no small-*p* expansion).** The probability per round of a silent logical error (model M2, *p* per location):

| Round | p = 1e-4 | p = 1e-3 | p = 1e-2 | p = 3e-2 |
|---|---|---|---|---|
| Local conventional | 5.33e-5 | 5.31e-4 | 5.14e-3 | 1.43e-2 |
| Joint conventional | 2.67e-5 | 2.66e-4 | 2.64e-3 | 7.74e-3 |
| Joint flagged | 2.32e-8 | 2.29e-6 | 2.07e-4 | 1.49e-3 |
| Joint verified cat | 9.88e-8 | 9.66e-6 | 7.73e-4 | 4.34e-3 |

   The exact engine was checked against 60,000-round Monte Carlo runs at *p* = 0.05 and against the first- and second-order coefficients.
4. **Negative result (M3).** With idle faults counted, flagged extraction has the lowest silent probability only up to about *p* = 1.1e-3 (the crossover predicted from the coefficients is 9.9e-4); above it the conventional joint round is better, and above about 2.2e-2 the verified cat. Values above a few percent are outside any reasonable use of the model.
5. **Rejection.** At *p* = 1e-3 (M2) the rejected fraction per round is 5.5e-3 (local), 8.6e-3 (joint), 1.6e-2 (flagged), 3.1e-2 (verified cat).

**Resource proxies per round** (not costs):

| Round | Two-qubit gates | One-qubit gates | Ancilla qubits | Measurements | Ancilla-ancilla gates |
|---|---|---|---|---|---|
| Local conventional | 4 | 0 | 2 | 2 | 0 |
| Joint conventional | 8 | 0 | 2 | 2 | 0 |
| Joint flagged | 12 | 0 | 4 | 4 | 4 |
| Joint verified cat | 18 | 2 | 10 | 10 | 10 |
| Joint cat, unverified | 14 | 2 | 8 | 8 | 6 |
| Joint cooperative, verified | 14 | 2 | 6 | 6 | 6 |
| Joint cooperative, unverified | 10 | 2 | 4 | 4 | 2 |

**Does additional verification improve overall reliability?** The model does not give a single answer. Under M3 at *p* = 1e-3 every joint round has a silent probability more than 5 times lower than the local round, but that depends on the noise containing Z faults (version 0.8 showed that X-dominated noise reverses this at the workload level), and it comes with 1.4 to 3 times more rejections and more data damage per round. I have not combined these, and I do not think they should be combined without a statement of what a rejected round costs.

## 5. Priority 3: concurrency with compatible computational transformations

A rotation about an in-code generator *g* (a Pauli commuting with every check of the code) inserted after *k* of a check's data couplings leaves the check outcome and the rotated state unchanged **exactly when *g* commutes with the part of the check already coupled** (the prefix product). Confirmed by state-vector simulation of the whole extraction round for every one of the 63 generators of each code, every slot, for the conventional joint, flagged joint and local rounds (1,638 simulations; probability 1 and fidelity 1 in every allowed case, failure in every disallowed one).

| Check | Generators | Interior slots allowed per generator (min / mean / max) |
|---|---|---|
| Joint ZZZZ or XXXX, native order, weight-2 in-code generators | 18 | 0 / 1.89 / 3, of 3 |
| Local ZZII or IIZZ, weight-1 in-code generators | 4 | 1 / 1.00 / 1, of 1 |
| Local, weight-2 in-code generators | 14 | 0 / 0.71 / 1, of 1 |

Distribution over the 18 joint weight-2 generators: 2 have no interior window in the native order, 4 have one, 6 have two, 6 have all three. Every one has an interior window under some coupling order. The flagged round has identical windows (the flag couples to the ancilla only). I did not simulate windows for the cat and cooperative rounds; their couplings are parallel, so the rule applies to subsets of axes rather than a fixed order (**not tested**). Faults *inside* a concurrent window were not studied.

## 6. Priority 4: the metrics, kept separate

Sections 4 and 5 give the separate quantities: interactions (two-qubit gate count), ancillary resources (ancilla qubits, measurements, ancilla-ancilla gates), rejection rate, silent damage, accepted-damaged, rejected-with-damage, and propagation. Two further propagation numbers (M2): fault cases leaving a data error of raw weight at least 2, out of all cases, are 16 of 68 (local), 48 of 128 (joint), 64 of 196 (flagged), 56 of 316 (verified cat); and the largest data error accepted modulo stabilizers is weight 1 for local, flagged and verified cat, and weight 2 for joint conventional, unverified cat and both cooperative rounds. The first-order mass of fault cases that leave *any* data error is 3.200, 6.933, 9.067, 16.800 for local, joint, flagged and verified cat: **Buddy's own mechanism damages the data more often as it becomes more elaborate**, even though most of that damage is flagged.

## 7. Priority 5: a provisional bidirectional IQA-Buddy interface

**PROPOSED, not an established implementation, and not part of the frozen vocabulary.** IQA stays a provisional working name. The aim is to separate *what is to be established* from *what Buddy can physically do*, parameterized by Buddy's capabilities and limits.

*Buddy to IQA, capability report.* One row per configuration the hardware can run. The program builds it from the computed quantities: code (local or joint), single-axis faults detected (8 or 12 of 12), silent-logical probability per round at a stated *p*, accepted-damaged probability, rejection probability, first- and second-order silent coefficients, interaction count, ancilla count, measurement count, ancilla-ancilla gates, mean interior windows for weight-2 in-code rotations, and `physical_cost` (empty). The *p* and the fault model travel with the row.

*IQA to Buddy, assurance request.* Hard constraints on separate metrics (for example "silent at most 1e-5 and rejection at most 5%" or "at most 4 ancillas"). The response is the feasible set and its Pareto set over the separate metrics; **no score is computed and nothing is chosen for the user**. Three example requirements were run at *p* = 1e-4, 1e-3 and 1e-2:

| Requirement | p = 1e-4 | p = 1e-3 | p = 1e-2 |
|---|---|---|---|
| A: silent at most 1e-5, rejection at most 5% | Pareto set: flagged | flagged | nothing feasible |
| B: silent at most 1e-3, rejection at most 1% | local, joint conventional, flagged | local, joint conventional | nothing feasible |
| C: silent at most 1e-3, at most 4 ancillas, at most 10 two-qubit gates | local, joint conventional | local, joint conventional | nothing feasible |

The selection changes with *p* and with the requirement, and "nothing feasible" is a legitimate answer that should go back to GEA (change geometry, accept more rejection, or relax the requirement).

*Buddy to IQA, evidence.* For each requested assurance objective, what was established. Derived from this page, for structural checks alone:

| Objective | Established by structural checks? |
|---|---|
| Preparation assurance | Yes, for the checked structure (both codes) |
| Continuation assurance | Yes, within the code's coverage; blind spots listed per code |
| Operational assurance | **No for in-code errors**: 0 of 63 in-code rotation generators are detected by the checks of either code |
| Extraction assurance | Zero first-order silent damage only for the flagged and verified-cat rounds, under the stated model |

**What the evidence says about the configurable-Buddy hypothesis.** It is not contradicted: the local conventional, joint conventional and joint flagged rounds each appear in some Pareto set and not in others. It is also not demonstrated: the comparison is within one abstract model, assumes uniform Pauli noise, and takes no account of the cost of the extra configurations. I recommend leaving Buddy's final form open, as you proposed.

## 8. Priority 6: reference preparations for operational assurance

A reference preparation is a known state sent through the same route. For a controlled phase with nominal angle φ and actual angle φ + d, a reference with the control in |+> and the target in |1> shows a click (output differs from the nominal) with probability exactly **sin²(d/2)**.

| Constant error d (rad) | Reference runs for at least one click with 95% confidence |
|---|---|
| 1.00 | 12 |
| 0.30 | 133 |
| 0.10 | 1,198 |
| 0.03 | 13,314 |
| 0.01 | 119,829 |

What this does **not** do:
- *Reference choice matters.* For an error rotation about generator *g* the click probability on a reference state is sin²(d/2)(1 − ⟨g⟩²). A Z-basis-only reference set gives zero clicks for the three logical error generators IZ, ZI and ZZ (3 of 15); adding X-basis products closes all fifteen. A single Bell reference misses XX, YY and ZZ.
- *It tests the apparatus under reference conditions, not an unknown state.* An unknown logical state hit by an in-code rotation passes every structural check yet has fidelity 0.35 to 0.57 with the intended output (three errors at 2.0 rad). An error that appears only in some runs, or only for some inputs, is not shown by references taken at other times or with other inputs. This is the limit already stated in version 0.7 and unchanged.

## 9. What I expected and was wrong about

- I expected the cooperative two-cat-qubit round to be a cheap fault-tolerant compromise. It is not (0.8 and 2.133 silent per unit *p*); grouping by photon makes every cat-qubit X fault a weight-2 logical Z.
- I expected flagging to win under every fault model. It wins under M2 and loses to the conventional joint round above about 1e-3 under M3.
- My first selection routine had the dominance test inverted and listed the verified cat (the worst by gate count) as the sole optimum; I caught it by reading the output rather than the assertion, and fixed it before the assertion that checks non-dominance.
- My first concurrency statement ("no generator has an interior window at every slot in a fixed order unless it commutes with every single factor") was not what the numbers show: six generators have all three slots. Replaced by the distribution above.
- I first reported the flagged round as passing weight-4 data errors. That was raw weight; modulo stabilizers it is weight 1.
- I expected the verified cat to cost modestly more than flagging. It has about 4 times the second-order silent damage and about 2 times the rejection of the flagged round.

## 10. Limits

- Pauli faults on ideal Clifford circuits only. No photon loss, no probabilistic or heralded two-photon gates, no leakage, no measurement-induced decoherence, no correlated or coherent noise. For photonic hardware these may dominate; this page cannot say.
- One fault model with uniform per-location probability and uniform Paulis. Version 0.8 showed that X-dominated or Z-dominated noise changes the ranking of the local and joint codes; it was not re-run here for extraction circuits.
- The ancilla qubits are assumed to exist and to be reset; their preparation, reuse and idle exposure between rounds are not modelled beyond M3's idle faults.
- Only a four-axis, distance-2 code. Larger codes, repeated rounds, correlations between rounds, and the conversion reliability thresholds (version 0.8's topic) are not studied here.
- Second-order coefficients are exact only for fault pairs at different locations in one round; third and higher orders appear only in the exact engine.
- Windows are for one rotation per round and not tested in the presence of faults. Cat and cooperative windows were not tested.
- Literature is read at abstract level; established-method claims need confirmation. No claim of novelty is made.
- Nothing independently reproduced.

## 11. Suggestions (PROPOSED)

1. **Make Buddy's own reliability a separate metric** in the capability report (silent probability, accepted-damaged, rejection) with the fault model and *p* stated, and never merge it with a coverage figure.
2. **Use the flagged joint round as the competent baseline** for joint extraction, and the conventional local round as the baseline for everything; do not propose the cooperative variant above in its photon-grouped form.
3. **Let IQA return a feasible set and a Pareto set** and let GEA choose; treat "nothing feasible" as a normal outcome.
4. **Add "concurrency window" as a GEA selection variable** beside verification compatibility, derived by the commutation rule in section 5.
5. **Treat reference preparations as apparatus assurance** with a declared reference set, a declared number of runs and a declared stationarity assumption; never label a single run's output as certified.
6. **Leave Buddy's architecture open** until a model with loss and probabilistic gates exists.

## 12. Reproduction

`python3 -I code/buddy_v09_checks.py` (standard library only; about 20 seconds). The last line is `ALL PASS`; 33 checks. The program prints every table above. Parts: A erratum and engine validation; B circuit-level enumerator and regression against version 0.8; C extraction methods; C2 exact probabilities; D concurrency; E metrics, capability report and selection; F reference preparations; G result checks.
