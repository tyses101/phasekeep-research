# Volume 11: Experiments, Open Questions and Contributing

## What you will learn

What to build first, what each experiment can and cannot show, what is still unanswered, and how to send a correction.

## 11.1 A learning path

1. **Polarization with ordinary light.** Malus's law says the intensity passing a second polarizer is I = I₀ cos²θ, where θ is the angle between the polarizers.
2. Study spatial phase and twisted beams (OAM).
3. Study mixing of modes and relative phase.
4. Only then think about single photons and photon pairs.

Classical (bright) light teaches how modes transform. It **cannot** show single-photon behaviour, multi-photon interference or any quantum advantage.

## 11.2 Three practical investigations

| Investigation | Record | What it does not show |
|---|---|---|
| Polarization rotation | Intensity in and out, angle, extinction | Quantum advantage |
| Twist −1/+1 discrimination | Confusion matrix, transmission, phase sensitivity | Full state tomography from one detection |
| Shared waveplate | Retardance, axis, loss across modes, fixed and scaled aperture | Universal gate efficiency |

::: watch
**Safety first.** Use enclosed, low-power setups and proper laser safety procedures. These are learning objectives, not an equipment or safety specification.
:::

## 11.3 The bench order for a real test

Start with an enclosed low-power coherent-light bench. Then:

1. Characterize polarization and the ±1 modes.
2. Measure waveplate retardance, axis, transmission and cross-mode behaviour.
3. Test coherent *superpositions*, not just the basis states.
4. Measure sorter **crosstalk** separately from **transmission**.
5. Repeat with a fixed aperture and with a scaled aperture.
6. Establish a real baseline *before* comparing costs.

Later: heralded sources, and two successive operations with a final characterization. **Do not infer nondestructive verification from destructive data.**

## 11.4 What a Tetragon bench test would show

A Tetragon test cannot show computing power, but it can show how cleanly and cheaply the basic operations can be done. These are plans, not results [[PROPOSED]], and none has been done. In each case report the test states used, the fidelity against a stated benchmark, the loss, and survival and fidelity separately:

- prepare chosen four-address pure states;
- act on individual addresses and on selected pairs, and report crosstalk to the others;
- apply one shared operation across equivalent lines, and report the part count and loss against doing each line separately;
- create and remove non-separability between polarization and twist, with Schmidt weights found by a full state characterization;
- keep coherence through successive operations;
- as the first multi-photon target, produce two entangled Tetragons and report the entanglement by a full state characterization of the pair, with the loss counted. Pairs hyperentangled in polarization and OAM of ±1 have been produced by a source in the literature (Volume 6, section 6.7), so the first target is a reproduction and a measurement of cost, not a new physical effect. The pattern changes of Volume 6 can then be tried on photon B alone.

Non-separability between two properties of **one** photon is much easier to produce than entanglement between two photons, so it is a useful intermediate stage. It is not a substitute for the two-photon interactions of Volume 6, because a tie between two properties of one photon does not let one photon's operation depend on another photon's state. Bright (classical) light is the natural first test, with single photons later. Each result should also say which Buddy Check answer it earns: a result with no certification of the output stays UNKNOWN.

::: watch
**A four-level photon is easy to simulate.** A single photon in a four-level system is described by four amplitudes, and any operation on it is a 4 × 4 matrix. A classical computer handles that instantly. So the Tetragon can test *how cheaply and cleanly* operations can be done, but it cannot show a computing advantage, whatever the geometry. The same goes for interference on one photon's modes: wave optics does that classically too. Any advantage claim must come from scaling and from multi-photon interaction, and it must be measured against the best classical alternative.
:::

## 11.5 A fair comparison

Compare identical tasks with the same inputs and the same output requirements. Count preparation, parts, calibration, detection, failed attempts and readout. Report uncertainty and negative results. A numerical self-check tests the model, not the lab.

## 11.6 Open questions

- Which published sorter gives a realistic baseline for A06?
- How does waveplate retardance vary across real Laguerre-Gaussian modes, once common offsets are removed?
- Which CT sequences keep the Tetragon intact, including superpositions?
- Can a herald certify surviving occupancy *without consuming* the computational photons? (A04, BV-05)
- Can an encoding-aware compiler beat a conventional one with matched resources?
- Does the independent / coupled / entangling sorting of operations (Volume 6, section 6.7) predict the parts, loss and calibration needed for the *same* task, once measured?
- Which device mixes twist −1 and +1 beyond a swap or a phase, and what are its loss and crosstalk?
- Does the published apparatus match our reconstruction? (A02)
- Can a timing-free Tetragon memory preserve relative phase? (B02)

## 11.7 What would prove us wrong

Good ideas say what would count against them. Here are things that would:

- A published apparatus whose heralds *are* reliable in the very configuration we reconstructed (A02 would then show our model was incomplete).
- A shared operation whose cost, measured on a real bench, is *not* lower than individually addressing the states.
- A memory chain whose measured overall efficiency stays below the threshold of Volume 8.
- A counterexample to the joint classical bound (B03).

## 11.8 Contribute a correction or an experiment

Send:

- the exact claim and its evidence tag,
- the assumptions and the derivation or source,
- a reproducible procedure, the observed result and its limitations.

For simulations include code, random seed, dependency versions and raw output. For physical experiments include the apparatus, calibration, uncertainty and safety conditions. Do not send personal data or material you do not have the right to share. **Negative results are welcome.** A useful correction is a contribution, not a defeat.

## 11.9 Discussion questions

1. Why does a large state space not equal a large readable memory?
2. When is a shared operation cheaper than sorting first?
3. What is the difference between a herald and a valid output?
4. Which claims in this library could a single counterexample disprove?

::: evidence
**Evidence status.** These are plans and questions: [[PROPOSED]]. No PhaseKeep experiment has been done; [[MEASURED]] is none.
:::

## Summary

::: key
Start simple, with bright light and a careful record. Measure separate things separately, test superpositions, keep your baselines honest, and welcome the result that says you were wrong.
:::
