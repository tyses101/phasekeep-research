# Volume 7: The Buddy System and Buddy Checks

## What you will learn

Why a detector click that says "success" can be wrong, how to measure that, and how the Buddy System turns the problem into a checklist. This volume contains the project's most useful result so far, and it is a *cautionary* one.

## 7.1 The idea: a buddy for every photon

In the Buddy System, a computational photon is accompanied by **ancillary** ("buddy") photons that are prepared, used to help an operation, and then measured. The buddies are physical resources, not magic. The **Buddy System** is the proposed architecture for managing them in five stages: **preparation, assistance, verification, preservation and continuation**.

The key word is *verification*. In optics a gate often works only some of the time, and a helper detector click is supposed to tell us when. But a click is a **detection**, and detection is not the same as **verification**.

::: plain
A smoke alarm that goes off sometimes when there is no fire is not much use. A "success" signal that is sometimes wrong is the same: it tells you something happened, not that things are fine.
:::

## 7.2 Before, Operation, After

Every operation is described in three parts.

| Part | Question | Example |
|---|---|---|
| **Before** | What state is prepared, what resources are needed, are they compatible? | Two photons in addresses, plus two helper photons |
| **Operation** | What is the intended CT, how is it done physically, how can it fail? | The heralded controlled-phase-flip gate of Volume 6 |
| **After** | How well did it work, measured five ways (below) | See 7.4 |

## 7.3 Buddy Checks: PASS, FAIL or UNKNOWN

A **Buddy Check** is a test that decides whether it is safe to continue. It has *three* possible answers, on purpose:

- **PASS**: demonstrated evidence says the operation worked.
- **FAIL**: demonstrated evidence says it did not.
- **UNKNOWN**: we do not have the evidence. This is the honest default.

An answer is never PASS just because a detector clicked.

## 7.4 Five different ways to say "it worked"

People often use one word, "success", for five different numbers. We keep them separate.

| Measure | Plain meaning |
|---|---|
| **Herald probability** | How often does the success signal fire? |
| **Herald reliability** | Given that it fired, how often is the output actually valid? |
| **Output fidelity** | Given valid output, how close is the state to the target? |
| **Availability** | How often is a usable photon even there? |
| **Continuation yield** | What fraction of starting runs end up with a usable result you can carry on with? |

::: watch
**Common mistake.** Quoting herald probability as if it were reliability. The R30 result below shows how large the gap can be.
:::

::: watch
**Encoding-basis counts alone cannot certify quantum coherence or entanglement.** Joint counts can show that two properties are statistically linked, but not whether the link is quantum. The states (00 + 01 + 10 + 11)/2 and (00 + 01 + 10 − 11)/2 give the same probability, 0.25, for every address. Yet the first is separable and the second is maximally non-separable (Volume 4, section 4.8). Reading out the Tetragon address counts therefore cannot tell them apart. The same holds for a pair of Tetragons (Volume 6, section 6.7): the joint address counts of an entangled pair are identical to those of a purely classical pairing with the same address matches, which has no entanglement at all. Certifying a correlation needs measurements in other bases, in effect a state characterization, and that uses up the photons it measures [[DERIVED]]. A PASS for a correlation therefore needs more evidence than the address counts alone, which is one more reason the default answer is UNKNOWN. Correct addresses and correct probabilities can still hide incorrect quantum information, and a destructive test that passes does not show that the photon can carry on into the next operation.
:::

## 7.5 The R30 result: a worked example

The R29 and R30 research packages reconstructed, in a computer model, the published heralded gate of Volume 6 and asked: *when the herald fires, is the output actually the right kind of output?* The model used **ideal photon-number-resolving detectors** [[SIMULATED]].

For inputs where the first register is in the top address (3) and the second in a lower address (0, 1 or 2), the analyzer reported:

| Quantity | Value |
|---|---|
| Probability the herald fires | **0.375** (3/8) |
| Probability the output is *occupancy-valid* | **0.125** (1/8) |
| Probability of a *false herald* (fires but output not valid) | **0.25** (2/8) |
| **Reliability** = valid / herald | **1/3** |

"Occupancy-valid" is a narrow word. It means *exactly one photon in each computational output register*. It is **not** state fidelity and it says nothing about whether coherence survived.

For other inputs the reliability can be 100%. So "1/3" is the **worst case among the inputs studied**, and 100% the best.

::: key
In this reconstruction, for some inputs the success signal was wrong **two times out of three**. The herald was *telling the truth about something*, but not about what we needed.
:::

{{fig:herald|Heralds, valid outputs and false heralds. The herald fires 3 times in 8; only 1 of those is a valid output.}}

### What else we found

- Each of the four (u,v) auxiliary outcome classes carries **a quarter** of the valid and a quarter of the false weight (E/4 and G/4). Keeping fewer outcome classes therefore **does not** improve the reliability in this model.
- The false-herald operator is **diagonal in the logical basis** [[DERIVED]]. A false herald therefore doesn't scramble the addresses; it is an *occupancy error*, which a count of photons could in principle detect.
- An independent numerical rerun passed the supplied 20 checks [[REPORTED]]. A rerun checks the *code*, not the lab.

### What this does **not** say

- It is **not** a claim about all analyzers or all detectors.
- It is **not** a refutation of the published experiment. That experiment used post-selection on one photon per output port, and its reported overall success is 1/8 [[REPORTED]]. In that setting the occupancy is checked by detecting the photons, which consumes them.
- It is **not** a measurement. [[SIMULATED]] only.

## 7.6 Long chains of operations

The same model was extended to many gates in a row (SIM-06). The results are for the *ideal* model with no loss [[SIMULATED]]:

| Reactions in a row | Fidelity given all heralds (ideal) | With correlated phase drift, σ = 0.05 rad |
|---|---|---|
| 2 | 80.0 % | 78.7 % |
| 4 | 67.0 % | 62.8 % |
| 8 | 48.0 % | 37.2 % |
| 16 | 24.3 % | 9.1 % |

- The chance that every herald fires is 0.01953125 at 2 stages. That is larger than (1/8)² = 0.015625, because false heralds also count as "fired". At 16 stages the chance is 1.5 × 10⁻¹⁴.
- Given that the occupancy was valid at 2 stages, the fidelity is 98.5 %. So the false heralds, not just phase error, are what hurt.
- Phase drift costs about 1.3 points at 2 stages, and about 11 and 15 points at 8 and 16 stages. An earlier statement of ours that false heralds dominate *at every* length was **wrong** and was corrected after measurement.

{{fig:chain|Fidelity given heralds falls as the number of reactions grows, faster with correlated phase drift.}}

## 7.7 Reuse economics

If a photon can be reused, and each reuse survives with probability *s*, the expected number of successful reuses is s/(1 − s) [[DERIVED]]. With *s* = 0.95 that is 19. But survival compounds: after 10 cycles only 0.95¹⁰ = 59.87 % remain. A high per-step survival is not enough for a long computation.

## 7.8 The open problems

The audit items that connect to this volume (the full list is in Volume 9):

- **A02, apparatus mapping.** Does the reconstruction really match the published apparatus (routing, detector arrangement, acceptance conditions)? Pending. Until it is done, the false-herald result is a warning about *our reconstruction*, and no remedy should be designed.
- **A03, do accepted heralds indicate valid outputs?** In the reconstruction, no, for some inputs (this volume).
- **A04, do outputs stay usable without destructive verification?** Open. Measuring the output at the end can characterize *separate ensembles* of runs, but it cannot certify that the specific photon you just consumed can be reused.
- **A05, two successive reactions with reliable intermediate certification.** Open.

A04 and A05 are [[BLOCKED]]: a computer model alone cannot answer them.

::: deeper
In the model, the herald is a (u,v) outcome class of auxiliary measurements. Raw herald probability is 0.375 = 3/8; occupancy-valid probability is 0.125 = 1/8, so false heralds are 0.375 − 0.125 = 0.25. Reliability is 0.125/0.375 = 1/3. The script `outcome_resolved_herald_r30.py` rebuilds these from the optical network, cross-checks them against two independent code paths and the saved raw data, and uses stated tolerances: 1e-10 for probabilities and 1e-12 for equalities [[DERIVED]].
:::

::: evidence
**Evidence status.** R30 numbers: [[SIMULATED]] (ideal detectors, reconstruction-specific). Diagonal false-herald operator: [[DERIVED]]. Chain tables: [[SIMULATED]]. Published gate figures: [[REPORTED]]. Nondestructive certification: [[BLOCKED]]. Hardware: [[MEASURED]] none.
:::

## Try it

1. 1000 attempts give 375 heralds and 125 valid outputs. What is the reliability? (125/375 = 33.3 %, **not** 37.5 %.)
2. Why is "37.5 %" a trap? (That is the herald probability, which is a different measure.)
3. A friend says "the gate has fidelity 0.98 given valid occupancy, so it is nearly perfect." What did they leave out? (How often the output is valid at all, and how often the herald lies.)

## Summary

::: key
Detection is not verification. In our reconstruction the success signal fired for 3 runs in 8, and only 1 of those was valid. A Buddy Check says PASS only with evidence, FAIL when shown wrong, and otherwise UNKNOWN.
:::
