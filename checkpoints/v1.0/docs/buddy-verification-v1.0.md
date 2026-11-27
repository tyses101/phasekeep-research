# Buddy verification, version 1.0: which version 0.9 results survive photonic reality?

Project: PhaseKeep Research. Owner: Tyler O'Bryan. Written by Claude. Versions 0.1 to 0.9, Revision H and pull request #1 are preserved unchanged. Nothing here has been independently reproduced, and nothing here is a hardware result or a claim of advantage over any architecture. Physical feasibility is the central question of this version, and most of the answers below are of the form "it depends on a physical property nobody has measured for this system".

Evidence tags: **DERIVED** (exact within the stated model: ideal Clifford circuits plus Pauli, erasure and loss-like faults, exact Pauli-frame propagation, exact convolution of independent location faults, small state-vector simulations), **ASSUMED** (a rate, success probability, hosting rule or bias I chose as an example), **PROPOSED** (a design idea), **UNVERIFIED** (literature seen at title, abstract or excerpt level only), **MEASURED** (none), **BLOCKED** (needs something I do not have).

Central question: *Can deliberate geometric organization and controlled transformation of photonic entanglement improve the efficiency, controllability, reliability or continuity of equivalent quantum operations?*
Programme question (subordinate): *Can a photonic processor adapt its information geometry, verification requirements and physical execution routes in response to changing operational conditions, while achieving a measurable advantage over conventional architectures?*
The question version 1.0 puts: **which of the version 0.9 conclusions survive when photons are lost, interactions are probabilistic, noise is biased, rounds repeat, and readout is destructive?**

**How version 1.0 stays comparable with 0.9.** Every new mechanism has a switch that reduces to the version 0.9 assumptions. With loss, bias and incoming faults off, the new engine reproduces the published version 0.9 silent and rejection probabilities within 1% (checked), and with idle and incoming faults on it reproduces the 0.9 model M3 value. Differences below are therefore attributable to the mechanism named. Structural counts are proxies, not costs; no combined score is formed; the physical-cost fields stay empty (audit item A02); the conventional local round remains the baseline.

## 0. Summary

| Question | Answer within the model | Tag |
|---|---|---|
| Does the local geometry avoid inter-photon interactions? | **Not if photon detection destroys the photon.** An ancilla then has to be a separate photon and every data-ancilla gate is an inter-photon gate: 4 per round (local), 8 (joint). The local advantage is a factor of 2, not a different kind of operation. A nondestructive readout would lower the counts to 0 and 4, but its feasibility is unverified and itself built from probabilistic gates | DERIVED on an ASSUMED readout rule |
| What do probabilistic inter-photon gates do to verification? | If a failed gate aborts the round: completion probability s^n, for example 0.100 (joint) and 0.032 (flagged) at s = 0.75, and 0.0039 and 0.00024 at s = 0.5. Verification of unknown data is only usable with gates whose failure is both heralded and benign. Whether such gates exist at useful success probability is open | DERIVED on ASSUMED s |
| Does loss change the version 0.9 ranking? | Heralded ancilla loss costs rejections in proportion to ancilla resources: at 1% per photon per gate, 3.9% of local rounds, 14% of flagged rounds and 22% of verified-cat rounds are rejected by loss alone. Unheralded loss is much worse than any extraction design can fix (next two rows) | DERIVED |
| What if ancilla loss is not heralded? | Silent damage rises about 10 times (local) and about 60 times (flagged) at 1%: heralding the ancilla is worth more than the flag | DERIVED |
| What if data loss is not heralded? | A floor appears: the flagged round's silent probability at 0.1% loss is 9.7e-4, about 400 times its loss-free value (2.3e-6) and only 10 to 30% below the conventional joint round. If data loss is found at final readout, the cost is discarded runs, not wrong answers | DERIVED |
| Is the version 0.9 ranking robust to biased noise? | **No.** Z-biased noise favours the joint codes (local silent probability about 20 times the flagged round's). **X-biased noise reverses the ranking:** at bias 100 the local round beats every joint round. With biased ancillas only, the flagged round wins; with Z-biased data, conventional joint beats flagged | DERIVED on ASSUMED bias |
| Does repeated verification keep data safe? | It slows accumulation but does not stop it, and costs runs. At p = 1e-3 over 20 rounds, 0.20% of the still-accepted flagged-joint runs are damaged (3.7% local, 7.7% with no verification), but only 64% of flagged runs are still accepted. At p = 1e-2 only 1.2% remain | DERIVED |
| Does coherent amplification make reference preparations cheap? | Yes for a constant, coherently accumulating error: d = 0.01 rad needs 119,829 single-gate runs, 48 runs with 50 gates, and 2 runs of 256 gates (512 gate uses, a factor 234), still about 2,600 times fewer gate uses at 1% stochastic noise per gate. An error that alternates in sign never accumulates | DERIVED on ASSUMED noise |
| Can one mechanism serve verification, computation and characterization? | As a **selection** problem, yes: the three roles differ only in which Pauli product is measured (stabilizer, logical operator, or reference-state observable), and a stabilizer is the only kind that leaves unknown information undisturbed. Whether one physical coupler can do all three is not shown | DERIVED (classification), hardware open |
| Does the capability report need new fields? | Yes: ancilla heralding, inter-photon gate success and failure type, photons consumed, per-observable readout error, nondestructive-readout availability. Under a physical profile the Pareto sets change and can become empty | PROPOSED, demonstrated on a toy |

## 1. Corrections and clarifications

**To version 0.9.** I found no numerical error in version 0.9 by re-deriving its numbers in the new engine. Two clarifications to its page: (i) its "qubits" were generic and noise was uniform, so its section 4 ranking is a statement about uniform Pauli noise only (section 5 below shows it reverses under X-bias); (ii) its section 7 selection used "unusable = rejection" and silent probability per round started, which is not meaningful when rounds can fail to complete; version 1.0 separates completion, rejection, heralding and silence.

**Mistakes of mine in this version (fixed before delivery).** (a) My first amplification statistics used a normal approximation that returned "1 run" for a 41% click probability; I replaced it with an exact binomial threshold test, which reproduces version 0.9's 119,829 runs. (b) I first multiplied silent probability by the completion probability in the abort profile, which made the joint rounds look better because they fail more often; I now report silent damage per completed round. (c) A variable I reused shadowed the Pauli list and crashed the program, caught at the first run. (d) One float threshold in a check was too tight.

**Corrections you made earlier and I have kept.** The 2025 X/Z asymmetry belongs to Microsoft's earlier device, not Majorana 2; my literature entries for Majorana below rest on secondary coverage only.

## 2. Literature (all UNVERIFIED unless stated; abstract or excerpt level)

| Topic | What I saw | Status |
|---|---|---|
| Linear-optics two-qubit gates (review arXiv:1607.03935, partial) | Success probabilities quoted there: nonlinear sign shift 1/4, conditional sign from two of them 1/16, an efficient conditional sign 2/27, a postselected polarization CNOT 1/9, linear-optics teleportation Bell measurement 1/2. The review excerpt I read did not say what a failure does to the data | My s values (1, 0.75, 0.5, 0.25, 1/9) are chosen to span these; **what failure does to the data is open** |
| Deterministic intra-photon gate (Fiorentino and Wong, quant-ph/0402208, abstract) | A linear-optical CNOT between the polarization and momentum qubits of one photon, described as deterministic | Supports "gates between axes of one photon can be deterministic"; no performance figures seen |
| Fusion-based quantum computation (arXiv:2101.09310, abstract) | Entangling measurements ("fusions") on small resource states; fusions probabilistic in linear optics; one quoted figure is a ballistic scheme tolerating 10.4% photon loss in each fusion | Shows the field's own answer to probabilistic gates and loss; not modelled here |
| Measuring a photonic qubit without destroying it (quant-ph/0312048, abstract) | A scheme and demonstration using linear optics and photodetection of ancillary modes, which creates a single-photon-level nonlinearity non-deterministically | Supports "nondestructive readout exists in principle" and that it is probabilistic. A published comment on it exists (quant-ph/0406120, title only seen); **I did not read it** |
| Majorana tetrons (arXiv:2507.08795, abstract; coverage of the June 2026 InAs-Pb result) | 2025 device: X loop 14.5 µs and Z loop 12.4 ms parity switching, assignment errors 16% and 0.5%. The newer paper is a characterization experiment reporting Z parity only (about 22 s), no gates or entanglement; critics dispute topological identity; the June 2026 criticism by Legg concerns the 2025 Nature paper | Used only as a prompt for per-observable readout error; no Majorana claim is relied on |

## 3. What the model adds

- **Photons and readout.** Data qubits are the axes of two photons (a1, b1 and a2, b2). I assume detecting a photon destroys it, so an ancilla is its own photon (at most K ancilla qubits per photon in the hosting study). **ASSUMED.** An alternative (ancilla as an extra degree of freedom of a data photon, needing a nondestructive readout) is reported as a lower bound.
- **Loss.** A photon loses with probability q at each two-qubit gate it takes part in. An ancilla photon's loss is **heralded** by a missing click (fraction h of the time) or **unheralded** (the ancilla becomes a random qubit). A data photon's loss is **latent** (found at final readout, the run is discarded) or **unheralded** (both axes become a random Pauli). **ASSUMED.**
- **Probabilistic gates.** Each inter-photon gate succeeds with probability s. Two bookkeeping modes: a failure **aborts** the round, or a failure is **benign** and the gate is retried (attempts n/s). Which is physical is open.
- **Bias.** Z or X Paulis at faulted locations carry weight b against 1 for the others, on all qubits, data only, or ancillas only. b = 1 is version 0.9.
- **Readout asymmetry.** Z-basis and X-basis readout flips can differ.
- **Repeated rounds.** Incoming data faults (p per axis per round) plus the round's own faults, over R rounds, exactly, with rejection ending a run; compared with no verification.
- **Engine validation.** The generalized exact engine was checked by 40,000 Monte Carlo rounds with every mechanism on, and the repeated-round recursion against the single-round engine.

## 4. Feasibility structure and probabilistic gates (priorities 1 and 2)

Inter-photon two-qubit gates per round under destructive readout (ancilla photons consumed in brackets), K ancilla qubits per ancilla photon:

| Round | Total 2q gates | K = 1 | K = 2 | K = 5 | Nondestructive lower bound |
|---|---|---|---|---|---|
| Local conventional | 4 | 4 (2) | 4 (2) | 4 (2) | 0 |
| Joint conventional | 8 | 8 (2) | 8 (2) | 8 (2) | 4 |
| Joint flagged | 12 | 12 (4) | 8 (2) | 8 (2) | 4 |
| Joint verified cat | 18 | 18 (10) | 14 (6) | 8 (2) | 4 |
| Joint cooperative, verified | 14 | 14 (6) | 12 (4) | 8 (2) | 4 |
| ZZZZ only (partial joint) | 4 | 4 (1) | 4 (1) | 4 (1) | 2 |

Consequences. A flag that shares its ancilla's photon costs no extra inter-photon gates, but needs a second axis on that photon. A cat ancilla needs many axes per photon to approach the joint conventional count. Completion probability s^n for n inter-photon gates (K = 1):

| Round | n | s = 0.75 | s = 0.5 | s = 0.25 | s = 1/9 |
|---|---|---|---|---|---|
| Local conventional | 4 | 0.316 | 0.0625 | 3.9e-3 | 1.5e-4 |
| Joint conventional | 8 | 0.100 | 3.9e-3 | 1.5e-5 | 2.3e-8 |
| Joint flagged | 12 | 0.032 | 2.4e-4 | 6.0e-8 | 3.5e-12 |
| Joint verified cat | 18 | 0.0056 | 3.8e-6 | 1.5e-11 | 6.7e-18 |

Expected inter-photon gate attempts per **completed** round at s = 0.5: 30, 510, 8,190 and 524,286 if a failure aborts and restarts the round; 8, 16, 24 and 36 if failures are benign and retried. **Negative result:** the gap between those two columns is the whole feasibility question. If a failed gate disturbs a data photon, joint verification of unknown data is not usable at s below about 0.75, and the flagged round is worse than the conventional one by the same factor again.

## 5. Loss, bias and readout (priorities 1 and 3)

**Loss** (gate faults p = 1e-3; q per photon per two-qubit gate; data loss latent; ancilla loss heralded, h = 1). Survival of data through a round (4 data participations local, 8 joint) is 0.9606 and 0.9227 at q = 1e-2. Rejections from heralded ancilla loss at q = 1e-2: 0.0388 (local), 0.0746 (joint), 0.1381 (flagged), 0.2160 (verified cat). Usable rounds (accepted and no data loss): 0.918, 0.847, 0.783, 0.701. Silent probability barely moves (5.1e-4, 2.5e-4, 2.0e-6, 7.6e-6).

| Variant at q = 1e-2 | Local silent | Joint silent | Flagged silent |
|---|---|---|---|
| Ancilla loss heralded | 5.1e-4 | 2.5e-4 | 2.0e-6 |
| Ancilla loss unheralded | 5.4e-3 | 5.1e-3 | 1.2e-4 |

| Data loss **unheralded**, silent probability | q = 1e-3 | q = 1e-2 | q = 5e-2 |
|---|---|---|---|
| Local | 1.5e-3 | 9.9e-3 | 3.7e-2 |
| Joint conventional | 1.2e-3 | 9.1e-3 | 2.9e-2 |
| Joint flagged | 9.7e-4 | 8.2e-3 | 2.4e-2 |
| Joint verified cat | 9.5e-4 | 7.3e-3 | 2.1e-2 |

Reading: **heralding of loss matters more than extraction design.** If data loss is found only at final readout, it costs discarded runs; if it can masquerade as a valid state, it sets a floor that none of the extraction methods removes.

**Bias** (silent probability per round, p = 1e-3, version 0.9 model M3, b multiplies the biased Pauli):

| Noise | Local | Joint conv. | Joint flagged | Verified cat | ZZZZ only | Lowest |
|---|---|---|---|---|---|---|
| Uniform (version 0.9) | 1.1e-2 | 4.0e-4 | 3.9e-4 | 1.9e-3 | 8.5e-3 | flagged |
| Z-biased, all, b = 100 | 3.2e-2 | 1.5e-3 | 1.4e-3 | 5.6e-3 | 2.6e-2 | flagged |
| **X-biased, all, b = 100** | **4.0e-4** | 1.4e-3 | 1.3e-3 | 5.5e-3 | **3.8e-4** | **ZZZZ only / local** |
| Z-biased data only, b = 100 | 3.2e-2 | **7.5e-4** | 1.3e-3 | 6.1e-3 | 2.5e-2 | joint conventional |
| X- or Z-biased ancillas only, b = 100 | 1.0e-2 to 1.1e-2 | 6.1e-4 to 6.3e-4 | **3.9e-4 to 4.1e-4** | 1.5e-3 to 2.6e-3 | 7.9e-3 to 9.3e-3 | flagged |

This reverses the version 0.9 ranking for X-dominated noise (consistent in direction with version 0.8's workload result) and shows that a flag helps when the ancilla's own hook is the problem, not when the data's idle Z faults are. It supports **choosing a configuration from a noise-bias estimate**, which is cheap in principle: reference preparations can estimate bias.

**Readout asymmetry** (illustrative factor): with X-basis readout flipping 30 times as often as Z-basis readout, flagged rejection rises from 0.0161 to 0.0723 and its silent probability about 2.6 times; conventional joint rejection from 0.0086 to 0.0373; the local round and the ZZZZ-only partial round, which use Z-basis readout only, do not change. An IQA that knows per-observable error can offer the partial check.

## 6. Repeated verification and accumulated damage (priority 4)

Incoming faults p per axis per round plus the round's own faults (M2), exact, a rejected round ends the run. "Damaged" = accepted and left with a detectable or silent data error.

| p = 1e-3, R = 20 | Still accepted | Accepted and damaged | Damaged given accepted | Silent |
|---|---|---|---|---|
| Local conventional | 0.833 | 0.031 | 3.7% | 3.0e-2 |
| Joint conventional | 0.746 | 0.0057 | 0.77% | 4.1e-3 |
| Joint flagged | 0.644 | 0.0013 | 0.20% | 1.1e-4 |
| Joint verified cat | 0.464 | 0.0014 | 0.30% | 1.8e-4 |
| No verification | 1.000 | 0.077 | 7.7% | (joint code) 7.6e-4 |

Silent damage accumulates almost linearly in R (15 to 20 times the one-round value over 20 rounds). At p = 1e-2 over 20 rounds only 1.2% of flagged and 0.05% of verified-cat runs are still accepted (16% local). **Detect-and-reject verification is unusable for long computations at that fault rate**, whatever the extraction design.

## 7. Coherent amplification with reference preparations (priority 5)

Repeating the gate N times turns a constant angle error d into Nd, so the reference click probability is exactly sin²(Nd/2) (state-vector check). Runs for 95% detection, at most 5% false alarms (exact binomial threshold; at no stochastic noise this is version 0.9's criterion), with stochastic error probability eps per gate use flipping the outcome with probability 1/2 (ASSUMED):

| d (rad) | eps | N = 1 runs | Best N | Runs | Gate uses | Saving in gate uses |
|---|---|---|---|---|---|---|
| 0.01 | 0 | 119,829 | 256 | 2 | 512 | 234 times |
| 0.01 | 1e-3 | 8,887,591 | 256 | 5 | 1,280 | 6,943 times |
| 0.01 | 1e-2 | 88,127,041 | 128 | 268 | 34,304 | 2,569 times |
| 0.03 | 0 | 13,314 | 64 | 3 | 192 | 69 times |
| 0.1 | 0 | 1,198 | 16 | 5 | 80 | 15 times |

Your 50-gate example reproduces (48 runs, 2,400 gate uses at d = 0.01); larger N does better still. Limits: the amplified signal grows 4 times when N doubles for a coherent error and 2 times for a stochastic one (a usable test for which is which); **an error that alternates in sign on successive uses does not accumulate** (click probability 4e-15 after 50 uses); the sequence must be a repeat of the same operation, so it characterizes the apparatus, not an individual unknown state; other coherent errors amplify too and are not separated from the one wanted.

## 8. One measurement mechanism, several purposes (priority 6)

For both codes the 255 non-identity Pauli products split into 3 stabilizer elements, 60 logical operators and 192 that anticommute with a check. Measured on random code-space states: a **stabilizer** product has a certain outcome and leaves the state untouched (fidelity 1.000, which is what verification needs); a **logical** product has a random outcome and disturbs the state (post-measurement fidelity 0.57 to 0.61, which is computation, or a reference measurement on a reference state); a product that **anticommutes with a check** also takes the state out of the code. The cheapest member of each class: stabilizer weight 2 (local) or 4 (joint), logical weight 1 or 2.

| Purpose | Observable class | Note |
|---|---|---|
| Structural verification | Stabilizer | The only class that does not disturb unknown information |
| Computation by measurement | Logical operator | Deliberate disturbance; the V0.8 finding that XXXX is a logical operator of the local code is an instance |
| Apparatus characterization | Any, on a **reference** state | Not on unknown data |
| Heralding, ancilla readiness | Observable of the ancilla itself | A stabilizer of the cat state in the verified cat |

What this supports: "the same coupler, a different selected observable" is a coherent design statement; IQA's job is to select the class. What it does not show: that one photonic coupler can implement weight-4 products, weight-2 logical products and reference analysis without separate hardware. Whether to define Buddy by purpose rather than by components stays open.

## 9. Capability report version 2 and selection under physical profiles (priority 7)

PROPOSED row fields (values from this page; `physical_cost` stays empty): silent probability per completed round, unusable fraction (rejected, heralded, lost, aborted), inter-photon gate attempts per completed round, ancilla photons consumed, single-axis coverage, completion probability, plus the declared physical parameters (p, q, s, failure type, K, readout availability).

| Profile (ASSUMED) | Requirement A: silent ≤ 1e-4, unusable ≤ 20% | Requirement B: silent ≤ 1e-3, attempts ≤ 12 |
|---|---|---|
| P0 ideal (version 0.9) | flagged joint | local, joint conventional, flagged, ZZZZ-only |
| P1 loss 1e-2, ancilla heralded | **nothing feasible** (flagged unusable 0.218) | same four |
| P2 s = 0.5, benign failures retried | nothing feasible | local, ZZZZ-only |
| P3 s = 0.75, failures abort | nothing feasible | local, ZZZZ-only |

"Nothing feasible" goes back to GEA or IQA to relax the requirement, change geometry or add heralding. Completion probabilities at P3: 0.316 (local, ZZZZ-only), 0.100 (conventional joint), 0.032 (flagged), 0.0056 (verified cat).

## 10. What I expected and was wrong about

- I expected the local geometry to need no inter-photon gates, since its check lives on one photon. With destructive readout it needs 4 per round.
- I expected the flagged round to stay best under any noise. It loses to the local round under X-biased noise and to the conventional joint round under Z-biased data.
- I expected loss to mostly cost throughput. Unheralded loss is the dominant error source, ten to hundreds of times larger than anything extraction design buys.
- I expected the amplification table to need a careful stochastic model to stay impressive. The gains survive 1% stochastic noise per gate in this model; the real limit is whether the error accumulates coherently.
- The mistakes in section 1.

## 11. Limits

- Still Pauli, erasure and loss-like faults on ideal Clifford circuits. No model of a real heralded gate's internals, partial distinguishability, dark counts, detector inefficiency beyond a per-gate loss, or timing. Loss is per gate participation, not per unit time stored.
- The destructive-readout rule, the hosting limits, the benign-or-abort choice, the heralding fractions and all rates are assumptions. The feasibility of a nondestructive readout and of benign-failure gates is unresolved by this page.
- Uniform or simple bias models only; no correlated or non-Markovian noise; amplification noise model is one line.
- Four axes, distance-2 code, one-ancilla-per-check rounds; conversion circuits under the physical model are not studied (the conversion has two inter-photon gates, so every conclusion about s applies to it directly: not computed).
- The capability profiles are illustrations. Majorana literature is not relied on.
- Literature at abstract or excerpt level. Nothing independently reproduced.

## 12. Suggestions (PROPOSED)

1. **Add to the capability report:** ancilla-loss heralding fraction, inter-photon gate success and failure type (benign or destructive), ancilla photons consumed, per-observable readout error, nondestructive-readout availability, and the declared noise bias.
2. **Make heralding of loss an explicit requirement** in IQA, ahead of extraction sophistication.
3. **Let GEA choose local or joint from an estimated noise bias,** using reference preparations (amplified where the error is coherent) as the estimator; treat the choice as a hypothesis to test, not a result.
4. **Run apparatus characterization as amplification sequences:** IQA specifies the sequence and expected outcome, Controlled Transformation executes it, Buddy measures the deviation.
5. **Keep Buddy's architecture open.** The classification supports a shared mechanism with a selected observable; the feasibility evidence points the other way for the gates it would need.
6. **Next (version 1.1 candidates):** a gate-level model of one heralded two-photon gate with explicit failure types; per-time loss; the conversion under the physical model; a full read of the photonic-gate and fusion literature; independent reproduction.

## 13. Reproduction

`python3 -I code/buddy_v10_checks.py` (standard library only; about 30 seconds). Last line `ALL PASS`; 29 checks. Parts: A regression to version 0.9; B hosting; C probabilistic gates; D loss; E bias and readout; F repeated rounds; G amplification; H shared mechanism; I capability report 2; J result checks and engine validation.
