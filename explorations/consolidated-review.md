# Consolidated scientific review: exploration pack S (S01 to S31)

**Status: exploratory, author-side, not independently reproduced. Not a checkpoint, not V1.1.**
Written by Claude (session of 2026-11-27) for the owner, Tyler O'Bryan, at the end of the bounded S26 to S31 series. It sits on branch `research-development/exploration-pack-s1` and goes with pull request #3, which stays **unmerged** until the owner has read it.

Nothing here is a hardware claim, an advantage claim or a novelty claim. Every number below is computed by a script in this folder on stated, mostly **assumed**, rates. The tag on each statement says what kind of statement it is.

| Tag | Meaning |
|---|---|
| DERIVED | An exact result inside a stated model (closed form, exhaustive enumeration, or exact arithmetic on a finite fault set). It is only as good as the model. |
| NUMERICAL OBSERVATION | A value read from a computed grid; it holds on the grid and is not extrapolated. |
| ASSUMED | A free parameter or a modelling choice I fixed (idle ratios, bias, gate success, requirements, "a heralded failure is fatal"). |
| PROPOSED | A definition or convention I introduced (layer counting, the in-place conversion, the oracle policy). Not an existing PhaseKeep definition. |
| UNVERIFIED | An external claim I did not check, or checked only partly. |
| MEASURED | A hardware measurement. **There are none.** |
| BLOCKED | Needs a parameter or a fact the repository does not contain. |

## 1. Provenance and standing limits

- V0 to V1.0, release `research-development-v1.0` and the Zenodo record were produced by Codex before this pack. **I have not verified the DOI** (10.5281/zenodo.24589667); my fetch of doi.org was not permitted and I did not work around it.
- Every script here was written and executed by me. That is **not independent reproduction** and I do not call it that. Where an exploration reproduces a V0.9 or V1.0 number (S05, S18, S19, S21), it does so with a different engine that I also wrote. Open problem 15 (independent reproduction) stays open.
- Preserved and untouched: Rev H, the historical checkpoints, licences and NOTICE. The IQA definition and the Docked Scheduling definitions are used as written; Docked Scheduling has no timing model in the repository and I did not invent a scheduler.
- Terminology conflict to be aware of: V0.8's "adaptive switching" is a conversion between local and joint verification geometries (two inter-photon gates). S31's "adaptive conversion" and "adaptive handoff" are **different** proposed operations (in-place re-encoding into a three-qubit code, and transfer to a separate register). The names collide; the objects do not.

## 2. What was asked and what was done

The owner asked for a bounded set of focused investigations, then a stop and this review. The plan was S27 to S31 after S26.

| Study | Question | Outcome in one line | Tag |
|---|---|---|---|
| S26 | How much worse than a gate may idling be before flagging stops paying? | Flagging pays only below a critical idle-to-gate ratio rho\*(p); V0.9's single crossing is one point of that curve. | DERIVED; rho ASSUMED |
| S27 | Is S26's inverse-square-root scaling a law? | No: an intermediate asymptote with a derivable range, exponent between 1/2 and 1. | DERIVED + NUMERICAL OBSERVATION |
| S28 | What happens over repeated rounds? | V1.0's order of damage given acceptance does not survive idle faults; the metric chosen decides the ranking. | DERIVED + NUMERICAL OBSERVATION |
| S29 | Which geometry is preferable for continuity? | Below four qubits the distance is 1, so only noise-specific protection and loss exposure can matter. | DERIVED + NUMERICAL OBSERVATION |
| S30 | Can the two logical qubits be handed to a separate register, and when does that beat idling? | Yes in six ways in the ideal model; only direct encoded transfer has no first-order silent fault; break-even needs a quieter memory. | DERIVED on ASSUMED rates |
| S31 | Do fixed operation, adaptive conversion and adaptive handoff differ over an operating envelope? | The oracle beats the best fixed option by 0 to 6.2 percentage points, and only under assumptions that are themselves the whole benefit. | DERIVED on ASSUMED rates |

### The model in one paragraph

Fault model M2 (V0.9): a non-identity Pauli with equal weight after each gate, plus preparation and measurement flips, each location failing with probability p. Single faults are classified exactly into harmless, detected, or silent (undetected and wrong). Idle locations fail with probability rho x p (rho ASSUMED); waits are counted in layers. Pauli noise can be biased (Z-dominant weights 1 : 1 : b). Silent probability S, rejection R (a detected fault ends the run), heralded abort A = 1 - s^g (g inter-photon gates, gate success s; fatal, ASSUMED), loss L = 1 - (1 - A)(1 - R), and correct completion CC = (1 - A)(1 - R - S) are reported **separately and never combined into a score**.

## 3. Findings

### 3.1 The idle-fault boundary of flagging (S26 to S28)

- **S26, DERIVED.** With idle locations failing at rho x p, the conventional joint round overtakes the flagged one when rho exceeds rho\*(p): 3.298, 1.891, 1.025, 0.588, 0.336 for p = 1e-4, 3e-4, 1e-3, 3e-3, 1e-2 under V0.9's serial counting (at rho = 1 this returns V0.9's crossing at p = 1.0496e-3). Under per-layer counting with one-gate-time measurement layers (PROPOSED) the values are 11.16, 6.45, 3.550, 2.11, 1.36. V0.9's negative result is a boundary in two parameters, not a single crossing.
- **S27, DERIVED + NUMERICAL OBSERVATION.** The second-order silent coefficient is exactly A + B rho + C rho^2 per round and convention. The first-order balance gives a closed form rho\*(p) = (-dB + sqrt(dB^2 + 4 dC (T/p - dA))) / (2 dC), T = 4/15. The exponent -d ln rho\* / d ln p lies in (1/2, 1) and is 1/2 only when rho\* >> dB/dC. The closed form is within 5 % of the exact value up to p of about 1e-3 to 2e-3; over p = 1e-3 to 1e-2 the exact exponent is **below** 1/2 (0.42 to 0.48) while the closed form says above. rho\* tends to a positive floor (0.015 serial). **The layered figure 3.55 holds only for one-gate-time measurement layers (1.03 at six).**
- **S28, DERIVED + NUMERICAL OBSERVATION.** A frame-chain engine reproduces V1.0's repeated-round table at R = 20 with idle faults off and the exact single-round distribution at R = 1. V1.0's accepted-fraction order holds under every idle convention; **V1.0's order of damage given acceptance does not survive any of the four conventions.** On silent probability per run the flagged round has no crossing for rho = 0.01 to 100 after 20 rounds; among accepted runs the critical ratio falls from 0.994 / 3.397 / 1.012 (R = 1; serial, m = 1, m = 6) to 0.783 / 2.253 / 0.809 (R = 20). Whether a run, an accepted run or a completed operation is the unit changes the answer.

### 3.2 Which geometry for continuity (S29)

- Any register under four qubits that holds two logical qubits has distance 1 for universal detection. This is a statement about **universal** detection (the Singleton bound); it does not forbid noise-specific protection, and an earlier over-strong sentence of mine on this point was corrected at the owner's request. **DERIVED.**
- Memory-only exact first-order silent probabilities per layer (q the per-qubit idle probability, Pauli weights 1 : 1 : b with b the dominant component): unencoded U2 2q; X3 (three qubits, one XXX stabilizer) 3q w_X/(2+b), with w_X = 1 under Z-dominant bias and b under X-dominant bias, and the mirror for Z3 (ZZZ); C4 has no first-order term and its second order is 2.00 q^2 unbiased. X3 beats C4 only for a bias of at least about 1/(q w) - 2 (1005 at q = 1e-3, w = 1; 107 at w = 10). **DERIVED.**
- Loss exposure (photons, not qubits): C4 on two two-axis photons has both single losses fatal; on four one-axis photons no single loss is fatal but all six pairs are; U2 on one photon has one fatal single loss; X3 and Z3 on two photons have two. **DERIVED.**
- Negative controls: a GHZ state and its phase partner share every reduced state on every subset yet are orthogonal, so correlation patterns do not determine the state. A logical Pauli, a coherent logical phase and a skipped operation pass every structure test and fail only against the reference fidelity. **DERIVED.**

### 3.3 Logical handoff to a separate register (S30)

Setting: source [[4,2,2]] on two photons, the two logical qubits entangled with two reference qubits (a Choi state), destination qubits prepared in |0>. All of the following were verified against **independent entangled targets**, not against the source's own correlation pattern.

- **Six mechanisms** reproduce the intended state with fidelity 1 (DERIVED, ideal gate-level model): decode-and-move (M1), SWAP (M2; its third CNOT is idle on a |0> destination, so M1 and M2 coincide), teleportation with offline Bell pairs, measurement and feedforward (M3), decode then route the photon (M4), direct encoded transfer of the four code qubits (M5), and decode, move and enter a three-qubit code (M6x, M6z). Arbitrary logical states, relative phases and external entanglement are preserved.
- **Computational handoff**, U E_A = E_B G with G a logical Pauli (Z), H, CZ and T (non-Clifford), reproduces the target with G applied (fidelity 1; the plain handoff scores 0, 0, 0.250 and 0.854 against those targets, so the check can tell them apart). Applying G at the destination adds no inter-photon gate; it adds one first-order fault location for H, CZ and T (none for a Pauli, which is a frame update). **The Choi fidelity depends only on the trace of the error operator, so T-propagated errors score like Clifford ones: this is an entanglement-fidelity statement, not a statement about every input state.**
- **No circuit is shown minimal.** Exact Schmidt-rank lower bounds on gates across the relevant cut are 2, 1, 2, 2; the circuits used need 3 to 8.
- **Only direct encoded transfer (M5) has no first-order silent fault.** First-order silent coefficients of the transfer itself: M1 33/5, M2 31/5, M3 289/15, M4 7/5, M6x and M6z 112/15, M5 0 (the decode window and the move leave the data unprotected).
- **Corrected round trips** (source register discarded while parked; syndrome qubits read out at decode; all four source qubits reset and freshly prepared at return and charged; final check = code stabilizers, no detection flags, ancilla back in |0> for M6): first-order silent probability of the whole round trip M1 13.2 p, M6x 14.9 p, M5 0 (with exact second order 70.08 p^2 + 20.8 p q per parked layer, q the continuity idle probability).
- **Break-even against idling in C4** (p = 1e-3, rho_p = 1, rho_m the continuity memory's idle ratio): M1 first wins at w = 93 layers with a perfect continuity memory (an asymptote w\* = sqrt(c1/(c2 rho_p^2 p)); the exact crossing deviates by +14.5 / 3.9 / 1.3 / 0.4 % at p = 1e-3 ... 1e-6), at 241 to 1180 layers with a continuity memory ten times quieter, and never at equal idle rate. **M5 never wins at equal idle rate** (it adds gates to the same code). Handoff into X3 (M6x) wins only under Z bias of about 100 (101 to 933 layers, at equal idle rates).
- **Negative controls** (five faulty handoffs, one of which keeps the destination maximally entangled with the reference) pass every structure test and have fidelity 0.500, 0.250, 0.250, 0.000 and 0.978 with the intended state.
- **Loss exposure during the transfer** itself involves 3, 4, 2, 4, 4 photons (M1, M3, M4, M5, M6x), more than the source's two. A smaller parked register lowers exposure only after the transfer.

### 3.4 Fixed operation, adaptive conversion and adaptive handoff (S31)

Options: STAY (idle in C4), CONV (PROPOSED in-place re-encoding of the same photons into X3 or Z3), and handoff to a second register by M1, M5 or M6x. The continuity memory idles at f_m times the source rate (f_m = 1 or 0.1, ASSUMED). The oracle policy knows the condition exactly and picks, among options meeting the stated requirement, the one with the fewest inter-photon gates (a stated tie rule, not a score). Requirements, IQA-style, on silent probability and loss: R1 (S <= 1e-3, L <= 0.10), R2 (S <= 1e-2, L <= 0.30), R3 (S <= 1e-4, L <= 0.30). Envelope: p in {1e-4, 1e-3, 3e-3}, rho_p in {0.1, 0.3, 1, 3}, f_m in {1, 0.1}, two biases (1 and Z-dominant 100), s in {1, 0.99, 0.9}, w in {3, 10, 30, 100, 300, 1000}: 288 conditions per value of s.

- **Best fixed option at s = 1** is, for all three requirements, "always hand off by M5": it meets R1, R2, R3 in 56.9 %, 75.0 % and 33.3 % of the conditions. **The oracle adds +2.1, 0.0 and +6.2 percentage points** over it at s = 1; at s = 0.99, 0.0, 0.0 and +6.2; at s = 0.9, nothing. (At s = 0.99 for R1 the best fixed option is STAY.) NUMERICAL OBSERVATION on ASSUMED rates.
- **Where the handoff meets a requirement that staying fails** ("adaptive-only", s = 1): 34, 36 and 22 of 288 conditions (11.8, 12.5, 7.6 %); 23.6, 25.0, 15.3 % of the f_m = 0.1 half; **none at f_m = 1** (equal-quality memory: checked on the whole grid). All of these cases pick M5. The benefit is therefore **the assumed ten-times-quieter continuity memory plus near-perfect two-photon gates**, not geometry as such.
- **Solved thresholds** at the 34 / 36 / 22 conditions (fatal-abort reading): gate success s\* of at least 0.9943 to 0.9982 (R1), 0.9803 to 0.9897 (R2), 0.9783 to 0.9795 (R3); the transfer gates may be worse than ordinary gates by a factor kappa\* with median 3.26 / 5.38 / 6.13 and minimum 1.09 / 1.79 / 1.02.
- **Decision robustness:** a policy that believes the idle ratio or the wait is a factor two too low misses the requirement at a true condition in 12 of 34, 18 of 36 and 8 of 22 of those cases; one that believes it a factor two too high declares the requirement unreachable in 18 of 34, 10 of 36 and 11 of 22. **The cost of estimating p, rho and w is not modelled**, so the oracle is an upper bound (IQA's own text says the cost of adaptation is not established).
- **In-place conversion alone** (CONV into X3) lowers both silent probability and rejection only under Z bias of about 100 or more: windows of 53 to 1036 layers at p = 1e-3, b = 100, and 45 to 545 at b = 1000; none at b = 1 or 10, where its rejection is lower over a long window starting at about 8 to 13 layers but its silent probability is higher at every wait. (The unbiased row of the table below shows this: CONV's silent probability is 0.095 against staying's 0.015.) Example at p = 1e-3, rho = 1, w = 100, b = 100: silent 0.029 against 0.039, rejection 0.24 against 0.28. The gain is modest and never turns a failing requirement into a passing one. (An earlier statement of mine that its rejection is "as high as staying's" was wrong; it is lower. See section 9.)
- **Metrics side by side, not combined.** At p = 1e-3, rho_p = 1, f_m = 0.1, unbiased, w = 100, s = 1 (NUMERICAL OBSERVATION; one condition, not a ranking):

| Option | Inter-photon gates | Silent S | Rejection R | Correct completions per attempt | Inter-photon gates per correct completion (s = 1 / 0.99 / 0.9) |
|---|---|---|---|---|---|
| STAY | 0 | 0.0151 | 0.3102 | 0.675 | n/a |
| CONV (X3) | 8 | 0.0951 | 0.1797 | 0.725 | 11.0 / 12.0 / 25.6 |
| M1 | 14 | 0.0330 | 0.0103 | 0.957 | 14.6 / 16.8 / 64.0 |
| M5 | 16 | 0.00047 | 0.0598 | 0.940 | 17.0 / 20.0 / 91.9 |
| M6x | 18 | 0.0248 | 0.0343 | 0.941 | 19.1 / 22.9 / 127.5 |

At this condition M1 completes correctly more often than M5 yet is silently wrong about seventy times as often (0.0330 against 0.00047). Which one is "better" depends on whether the requirement is on completions or on silent errors; the pack deliberately does not choose a weighting. At s = 0.9 the correct completions per attempt drop to 0.31 (CONV), 0.22 (M1), 0.17 (M5), 0.14 (M6x), against 0.675 for staying.

## 4. Hypothesis ledger

| Hypothesis from the discussion | What the evidence says | Tag | Still missing |
|---|---|---|---|
| Geometric conversion and handoff can be a single logical transformation between distinct registers (U E_A = E_B G, G = I) | Possible in the ideal gate-level model: M1, M5 and M6 are such transformations and are verified against entangled references. Their cost is 14 to 18 inter-photon gates per round trip and a first-order silent window for all but M5. | DERIVED | A cheaper unified circuit is not found; none of the circuits is shown minimal. |
| The two logical qubits of [[4,2,2]] can go into a smaller continuity register preserving arbitrary states and external entanglement | Yes in the ideal model. The smaller register has distance 1; protection is noise-specific only. | DERIVED | Physical realisability of the transfer gates; loss during transfer (3 to 4 photons touched). |
| Break-even versus idling exists | Only with a continuity memory ten times quieter than the source (or perfect), after tens to hundreds of layers, and near-perfect two-photon gates (about 0.98 to 0.998). Never at equal memory quality. | DERIVED on ASSUMED rates | Any platform's real memory-to-source idle ratio. |
| Returning to a different computational geometry is beneficial | Entering X3 in place helps modestly under Z bias of about 100 or more; no benefit unbiased. | NUMERICAL OBSERVATION | A platform with that bias; the return path to a computational geometry other than C4 was not studied. |
| Alternative continuity encodings compensate for lost redundancy | X3 or Z3 beats C4 only for bias above about 1/(q w) - 2; otherwise not. | DERIVED | Real bias values. |
| Continuity is an intrinsic function of GEA | **Not supported by these results, and not refuted.** It is a framing rather than a falsifiable claim. U E_A = E_B G describes the circuits well, but every benefit found comes from an assumed memory and assumed gate quality, not from the geometric relation. | Interpretation of DERIVED results | A platform-independent advantage of relational structure would need a different experiment (section 8). |
| Pairwise relationships describe the state | **No** (GHZ and its phase partner; stabilizer-preserving wrong operations). | DERIVED | n/a |
| Unified computational handoff beats separate transfer, conversion and gate | **Not decided.** Correctness for Z, H, CZ, T is verified; a unified synthesis against a separate gate was not done. | OPEN | Section 8, item 3. |
| An adaptive policy beats the best fixed one | 0 to 6.2 percentage points of the envelope, conditional on the assumptions above and an oracle with free estimation. | DERIVED on ASSUMED rates | Estimator cost; timing. |

## 5. The bottleneck map: what was and was not modelled

From the latency and bandwidth discussion, seven locations were proposed. The investigation counts operations, depth and layers, **not seconds**; no timing parameters exist in the repository.

| Location | Modelled here | Not modelled |
|---|---|---|
| 1 Resource preparation | Offline Bell pairs for teleportation are charged (preparation faults, operations); fresh preparation at return is charged | Retries, rate of usable resources, deterioration of a prepared destination while it waits |
| 2 State injection | Not modelled | Synchronisation, admission rate |
| 3 Geometric conversion | In-place conversion into X3/Z3 (8 inter-photon gates) | Parallel conversions |
| 4 Handoff | Gates, depth, measurement, feedforward as operation counts; heralded failure as an assumed fatal abort | Heralding latency, loss during transfer as a rate, classical control latency |
| 5 Retrieval | Return path charged (fresh preparation, re-encoding) | Readout time, mode count |
| 6 Verification | Buddy rounds in S26 to S28; final check in S30 | Concurrent integrity checks |
| 7 Detection | Not modelled | Detector response and recovery |

The throughput metric proposed ("successfully completed, logically correct operations per second") cannot be computed without timings (**BLOCKED**). The substitute reported is correct completions per attempt and inter-photon gates per correct completion (table in 3.4). Multiplying by an attempt rate is straightforward once a platform supplies one. Relational bandwidth and handoff congestion (several primary registers, one continuity register) have **no model here**.

## 6. Negative results and limits

1. No handoff mechanism removes the first-order silent window except direct encoded transfer, and that one moves a code to a code. The decode-based handoffs pay 13 to 15 p silent per round trip.
2. At equal memory quality no handoff or conversion helps anywhere on the grid.
3. The benefit that remains rests on a ten-times-quieter continuity memory (ASSUMED) and two-photon gate success of about 0.98 or higher with failure assumed fatal (ASSUMED). Both are free parameters, not findings.
4. The best adaptive policy gains 0 to 6.2 percentage points over the best fixed one and needs idle ratio and wait known to better than a factor two. The estimation cost is not modelled.
5. No circuit is shown minimal. The cross-cut lower bounds (2, 1, 2, 2) are below the circuits (3 to 8); the true optimum is unknown.
6. First-order classification and neglected terms: second-order terms of M1 to M4 and M6 and gate-by-memory cross terms (except for M5) are neglected in S31's envelope.
7. Unheralded loss is not modelled as a rate; only exposure counts (single and pair losses) are derived. Coherent faults were studied only in S22 (flagged round), not for handoff. Correlated subsystem erasure, imperfect resource preparation beyond charged P0 locations, and non-Pauli noise in the handoff are not modelled.
8. Fidelity checks use the maximally entangled Choi target; they certify arbitrary logical states, phases and external entanglement in the ideal model, and they are entanglement-fidelity statements for non-Clifford G.
9. "Geometric equivalence" of two encodings was never taken as evidence of physically realizable transfer. Nothing here shows that the transfer gates exist at the assumed quality on any platform.
10. S26 to S28's results are about V0.9's Pauli model of the buddy rounds, not a device.

## 7. Established literature and where PhaseKeep might differ

This was a **targeted check, not an exhaustive novelty assessment**. For each entry below I opened the arXiv or publisher listing page (title, authors, abstract; the full texts were not read) in this session unless stated. None of these mechanisms is claimed as new by this pack.

| Function | Established work (verified from listing pages) | Relation to this pack |
|---|---|---|
| Teleported gates | Gottesman and Chuang, "Quantum Teleportation is a Universal Computational Primitive" (arXiv:quant-ph/9908010); Nature 402, 390 to 393 (1999) | The M3 teleportation handoff and any "gate during transfer" idea sit inside this framework. A unified computational handoff must be compared against it. |
| One-way (measurement-based) computing | Raussendorf and Briegel, PRL 86, 5188 (2001) (reference as quoted on the arXiv page of quant-ph/0108067, "Computational model underlying the one-way quantum computer"; the PRL page itself was not opened) | Graph-state relational structure is established mathematics, as the owner's refinement says. |
| Code switching / transversal-gate universality | Paetznick and Reichardt, "Universal fault-tolerant quantum computation with only transversal gates and error correction" (arXiv:1304.3709; PRL 111, 090505); "Efficient fault-tolerant code switching via one-way transversal CNOT gates" (arXiv:2409.13465; title seen in search results only, authors and abstract not opened) | Converting between encodings is an established topic; S30's in-place conversion into X3 and Z3 is a small, non-fault-tolerant instance. I did not check whether the first paper's body uses code switching; its abstract does not. |
| Gauge fixing | Bombin, "Gauge Color Codes: Optimal Transversal Gates and Gauge Fixing in Topological Stabilizer Codes" (arXiv:1311.0879) | X3/Z3 as a re-chosen stabilizer subgroup is conceptually related; I did not analyse the relation. |
| Lattice surgery | Horsman, Fowler, Devitt and Van Meter, "Surface code quantum computing by lattice surgery" (arXiv:1111.4022; New J. Phys. 14, 123011) | Code merging and splitting by measurement is the nearest established analogue of logical-information transfer between code patches. |
| Modular quantum computing with photonic links | Monroe et al., "Large-scale modular quantum-computer architecture with atomic memory and photonic interconnects", Phys. Rev. A 89, 022317 (2014) | The separation of memory and processing qubits connected by photons is established. |
| Distributed teleported gates, experiment | Main et al., "Distributed quantum computing across an optical network link" (arXiv:2407.00835; Nature 2025). Abstract: two trapped-ion modules about 2 m apart, circuit and network qubits, teleported CZ at 86 % fidelity, Grover search 71 % success, distributed iSWAP and SWAP with 2 and 3 gate teleportations. | The closest experiment found. Its abstract describes **circuit and network qubits** and a **teleported gate**; it does not mention an "auxiliary" qubit or a transfer to an auxiliary qubit and back. The description in the discussion I was given ("transfer to an auxiliary qubit, operate, transfer back", "86.2 %") is **UNVERIFIED** against the full text; the abstract gives 86 % and about 2 m (consistent with the quoted 6.6 ft). |
| Optical quantum memory | Lvovsky, Sanders and Tittel, "Optical quantum memory" (arXiv:1002.4659; journal reference not shown on the page) | Memory mapping between photon and matter is an established field; S30's "continuity register" is not tied to any such interface. |
| [[4,2,2]] error detection, experiment | Linke et al., "Fault-tolerant quantum error detection" (arXiv:1611.06946; DOI 10.1126/sciadv.1701074): a four-qubit error-detection protocol | The code family used throughout is demonstrated experimentally; this pack's circuits are not. |

Cited from memory and **not checked this session**: Bennett et al., PRL 70, 1895 (1993) (teleportation); Bose, PRL 91, 207901 (2003) (state transfer through spin chains); Knill and Laflamme (1997) for the quantum Singleton bound; the original [[4,2,2]] constructions. **UNVERIFIED** as stated: the "Yale 2020, Modular Quantum Information Processors" reference from the discussion; the nearest items my searches returned were Zhou et al., "Realizing all-to-all couplings among detachable quantum modules using a microwave quantum state router" (arXiv:2109.06848; M. Hatridge is among the authors, affiliation not shown on the page I read; microwave superconducting modules; an average full-iSWAP time of 764 ns reported) and a 2020 Yale thesis whose title I did not read. Neither is a match I can confirm.

**Where a distinct, testable contribution could lie** (an assessment, not a claim): the existing literature already transfers, teleports, switches and merges. What this pack adds is (a) an exact accounting of the unprotected window and the break-even for a specific small code transfer, with the break-even quantities as explicit formulas, and (b) a requirement-based comparison of fixed and adaptive policies with the cost of adaptation named but not yet measured. Both are statements about a stated noise model. Whether "relational organisation" gives an advantage over established code-conversion and gate-teleportation methods under equivalent assumptions is **not shown** and has not been tested against those baselines.

## 8. Backlog from the owner's documents: not investigated here

The owner's research-direction documents list items beyond S31. Following the instruction to finish the bounded review first, none is started. In the owner's priority order, with a first well-posed question and what would count against it:

| # | Item | First well-posed question | What would count against it | Blocked on |
|---|---|---|---|---|
| 1 | Relational structures and their transformation costs | What is the true minimum number of cross-cut gates for the [[4,2,2]] to X3/Z3/U2 transformations (exhaustive search for small n)? Close the gap between the Schmidt bound (1 to 2) and the circuits (3 to 8). | The bound is tight at the circuits used (then nothing is saved). | Nothing; computable. |
| 2 | Logical-state preservation across geometries | Done in the ideal model (S30). Remaining: preservation under coherent and correlated faults. | A coherent fault breaks fidelity far beyond its Pauli twirl (as S22 found for the flagged round). | Noise model choice. |
| 3 | Prepared destination registers | How long may an offline-prepared, verified destination wait before its deterioration cancels the benefit; just-in-time against ahead-of-time preparation. S30 charges the offline operations but not the destination's own waiting. | Prepared destinations cost as much as the transfer they save (as S04 found for most offline preparation). | Waiting-time and retry model. |
| 4 | Unified computational handoff | Synthesise U with U E_A = E_B G for G = CZ, H, T at minimum inter-photon gates; compare against decode-and-move followed by G, and against gate teleportation (Gottesman and Chuang) as the baseline. | The unified circuit needs at least the sum of the separate costs. | Nothing; computable. |
| 5 | Dynamic geometric allocation | Does expanding or contracting the encoding (C4 to a larger code and back) beat the best fixed code on S31's envelope after conversion and verification costs? | No window on the grid, as for CONV. | Choice of larger codes. |
| 6 | Continuous computational progression, relational bandwidth, handoff congestion, throughput per second | Queueing of several primary registers for one continuity register; idle time converted into useful work. | Congestion makes the continuity register the bottleneck at any realistic occupancy. | **Timing parameters, platform choice.** |
| 7 | Relational integrity and verification | Which collective constraints detect which faults at lower cost than the Buddy rounds, and which wrong-but-structure-preserving operations they miss. Negative controls exist (S29, S30); verification cost does not. | Relational checks miss operations that stabilizer checks also miss at no saving. | Definition link to IQA/Buddy. |
| 8 | Literature topics not covered | Code switching, gauge fixing and lattice surgery costs against S30's circuits; memory-interface fidelities. | n/a | Reading full texts. |

Items 1 and 4 are computable now and are where I would put the next bounded effort, if the owner decides to continue. I am not starting them.

## 9. My own errors in this series (kept visible)

- **S30, first commit.** The round trips retained the source qubits, so the return path uncomputed forward faults and the handoff looked too good. Corrected by discarding the source, reading out syndromes, and charging fresh preparation; the corrected numbers are the recorded ones (commit 5dadd71, `run-history.txt`).
- **S31, first reading.** I compared the oracle with staying only, which overstated the benefit because the best fixed option is already a handoff; the table now reports gain over the best fixed option. I also replaced a tautological check with an independent recount.
- **S31, the in-place conversion.** I claimed its rejection was as high as staying's. I had not computed it. Computing it (check K2c) showed the rejection is lower over long windows that start at about 8 to 17 layers, and under strong Z bias the silent probability is lower too. The README and `run-history.txt` were corrected before commit.
- **S30, labels and windows.** A wrong-axis syndrome helper, a control that only reordered commuting gates, a tolerance chosen before seeing values, and break-even scans extended to 200000 layers (invalid extrapolation; capped at 3000). All logged in the run histories and the README's mistakes list (items 21 to 25 for S27 to S31).
- Carried over from earlier in the pack: the Singleton-bound over-statement (retracted), the S06 conjecture (false at n = 5), and the S14 K0 check that labelled resource counts as verification.

## 10. Items for the owner outside this folder (not changed)

1. The Zenodo DOI is **not verified by me**.
2. `docs/development/open-problems.md` items 19 and 20 still say authorization is pending and that no DOI exists or is claimed; `citing.md` says otherwise.
3. `docs/development/citing.md` has an empty "DOI and archive status" heading before "Publication completed".
4. Suggested caveat (text in the README, not applied) for `active-vs-replaceable.md` and roadmap row 4: offline preparation changes only the verified-cat round's ancilla-only gates.
5. The licence of this folder's text pages is **proposed, not assigned**; neither NOTICE.txt nor the development licence-scope statement names the folder.
6. The layered figure 3.55 for S26's critical ratio is for one-gate-time measurement layers only (S27).

## 11. Reproducing and checking

- `python3 explorations/run_all.py` runs the short variants of S01 to S31; `--full` adds the long ones (S05's verified-cat state-vector run, S06's n = 5 case, S15 and S16 full variants); `--only S31` runs one study; `--write-records` (with `--full`) rewrites the `execution-record.txt` files. Each script prints `ALL PASS` only if all its checks pass; the time and exit code of each study are in `run_all.py`'s output.
- Python and numpy only; no network access is needed.
- What independent reproduction would need: a second author re-implementing the fault classification (S02 and S30's `classify`) from the model description in section 2 and comparing the first-order coefficients (for example 33/5, 31/5, 289/15, 7/5, 112/15, 0), and then the closed forms in S27 and S30, without reading my code. The coefficients are small exact fractions, which makes them a good first check.

## 12. Decision points for the owner (not actions I took)

1. Read this review and the README; decide whether PR #3 may be merged. It is unmerged.
2. Decide whether any backlog item (section 8) starts a new series. I would suggest items 1 and 4 first because both are exact and need no platform parameters.
3. Supply timing and platform parameters if throughput per second, congestion or pipelining is to be investigated.
4. V1.1 has not been initiated and is not proposed by this pack.
