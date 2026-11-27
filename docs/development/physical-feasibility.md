# Physical feasibility

**Status: working development record, 2026-11-27. This is the central open question of the development layer. Every number below is a calculation under assumed rates, from checkpoint [V1.0](checkpoints/v1.0.md) unless stated; none is measured.**

:::plain In plain words
Checking a quantum computation needs helper photons that interact with the data photons. If those interactions only sometimes work, or if a helper photon can silently vanish, the checking can fail more often than the computation it is protecting. The modelled numbers say this may decide whether verification is usable at all. Nobody has built or measured the hardware, so these are warnings from a model, not facts about a device.
:::

## The question

Can the Buddy's verification rounds be carried out with photons, given photon loss and probabilistic photon-photon gates? Earlier checkpoints assumed ideal gates. V1.0 relaxes that, and compares its results directly against [V0.9](checkpoints/v0.9.md), without silently replacing V0.9's assumptions.

## Assumptions that decide the answer [ASSUMED]

- Detecting a photon destroys it, so every ancilla is its own photon and every data-ancilla gate is an inter-photon gate. The local geometry's advantage is therefore a factor of 2 (4 gates against 8), not a different kind of operation.
- Each inter-photon gate succeeds with probability *s*. Whether a failed gate **aborts** the round, or is **benign** and simply retried, is open and decides the result.
- Loss is per photon per gate participation. Ancilla loss may be heralded or unheralded; data loss may be latent or unheralded.
- Gates between axes of one photon are assumed deterministic and free (supported only by an abstract-level source, [Literature](literature.md)).

## Findings [DERIVED on the assumptions above]

1. **Probabilistic gates dominate.** If any failed gate aborts the round, completion probability is $s^n$ for n inter-photon gates. At *s* = 0.75 the four rounds complete 31.6%, 10.0%, 3.2% and 0.56% of the time (local, joint, flagged, verified cat); at *s* = 0.5, 6.3%, 0.39%, 0.024% and 0.00038%. Abort-and-restart needs 30, 510, 8,190 and 524,286 gate attempts per completed round at *s* = 0.5, against 8, 16, 24 and 36 if failures are benign.
2. **A failed gate that leaves the data intact is different from one that destroys it.** The gap between those two columns is the feasibility question. If failure disturbs a data photon, joint verification of unknown data is not usable at *s* below about 0.75.
3. **Loss changes the ranking's price.** Heralded ancilla loss at 1% per photon per gate rejects 3.9%, 7.5%, 14% and 22% of rounds. Unheralded ancilla loss raises silent damage about 10 times (local) and about 60 times (flagged). **Establishing that the carrier is still present may matter more than sophisticated detection of errors in what it carries.**
4. **Unheralded data loss sets a floor.** At 0.1% loss the flagged round's silent probability is 9.7e-4, about 400 times its loss-free value, only 10 to 30% below the conventional joint round.
5. **The V0.9 ranking is model-dependent.** Under strong X-bias the local round and a ZZZZ-only round beat the joint rounds; under Z-biased data only the conventional joint beats flagged; with biased ancillas only flagged wins. No configuration is best everywhere. A ranking by silent-error probability is not a statement about architectural superiority.
6. **Repeated verification slows but does not stop damage**, and costs runs: at *p* = 1e-3 over 20 rounds, 64% of flagged runs remain accepted, of which 0.20% are damaged.
7. **Coherent amplification reduces characterization cost** for a constant error (119,829 runs to 48, or to 2 with 256-gate sequences at 0.01 rad), an established principle, and says nothing about an individual state.

## Ancillary hosting: a structural hypothesis

If one ancilla photon hosts several ancillary axes, V1.0 counts fewer inter-photon gates: flagged 12 to 8 with two axes per photon, verified cat 18 to 8 and cooperative 14 to 8 with five-axis hosting. The floor of 8 comes from the gates that touch data. These are counts under an assumed hosting arrangement. The loss and noise tables use one ancilla qubit per photon (K = 1), and correlated loss of everything on a shared photon, independent control and readout are unstudied. It is a hypothesis that multidimensional photons could serve as verification resources, not a demonstrated capability.

## Active information versus replaceable resources

A separate page splits the gates by what they expose: [Active-information versus replaceable-resource exposure](active-vs-replaceable.md).

## Heralding, success and failure are separate

The classification used (success, heralded benign, heralded destructive, unheralded, detected or undetected data loss, ancilla loss, false heralding, unknown) is kept in the checkpoint reports. A herald does not certify a valid output, and a heralded failure is not a safe retry. V1.0 discards heralded-loss runs, and reports completion and conditional correctness together.

## What is not shown

- No gate-level model of a real heralded gate; no dark counts, partial distinguishability or timing.
- No per-time loss, so scheduling and storage effects are absent.
- The conversion circuit under the physical model is not computed in V1.0 (it has two inter-photon gates, so completion $s^2$ applies if a failure aborts it).
- No nondestructive photon-presence or parity measurement is shown to exist at useful success probability.
- Nothing is measured, and no advantage is claimed.
