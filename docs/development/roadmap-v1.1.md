# Proposed roadmap: V1.1

**Status: PROPOSED. Nothing on this page has been done, and no V1.1 experiment is started by this publication.** Every item needs separate authorization before work begins. The list is the project owner's priority order, written 2026-11-27.

:::try Proposal only
These are research directions, not findings. They do not describe capabilities PhaseKeep has.
:::

| Priority | Direction | Why it follows from V1.0 |
|---|---|---|
| 1 | Full-text review of the photonic-gate, fusion-based computing and teleportation literature | All V1.0 literature is abstract or excerpt level. The excerpt read did not say what a failed gate does to the data. |
| 2 | Gate-level modelling of heralded two-photon interactions with explicit failure consequences | Abort versus benign failure decides whether joint verification is usable ([Physical feasibility](physical-feasibility.md)). |
| 3 | Geometry conversion under realistic interaction failure and loss | Conversion has two inter-photon gates. |
| 4 | Offline ancillary preparation and resource scheduling | The data-touching gates stay on the active path; what offline preparation could change is for the ancilla-only gates ([Active-information versus replaceable-resource exposure](active-vs-replaceable.md)). Relates to Docked Scheduling and DDQT only after the original DDQT documents are read. |
| 5 | Shared ancillary hosting with correlated loss and realistic control assumptions | The hosting counts are structural; the noise tables use one ancilla qubit per photon. |
| 6 | Nondestructive photon-presence and parity measurement | It would lower the inter-photon gate counts to 0 and 4, but is itself probabilistic in the abstracts seen. |
| 7 | Time-dependent storage and propagation loss | V1.0 loss is per gate participation. |
| 8 | Repeated verification under physically motivated noise | V1.0 uses simple Pauli and bias models. |
| 9 | Independent numerical reproduction | All execution to date is author-side ([Reproducibility](reproducibility.md)). |
| 10 | Comparison with competent established photonic architectures | No comparison with a conventional architecture has been made; that comparison is the subordinate question. |

## Notes on conversion

Keep the distinction between **heralded failure** and **silent conversion error**. The two-inter-photon-gate conversion has completion probability $s^2$ under the independent abort model (0.5625 at s = 0.75, 0.25 at s = 0.5). That is a completion probability, and it is **not directly comparable** to V0.8's undetected conversion-fault thresholds (a break-even near 2e-4 in the base profile), which measure a different quantity.

## Ground rules for V1.1

- Preserve every earlier checkpoint. A V1.1 result that disagrees with an earlier one is reported as such, not by silently replacing assumptions.
- Report negative results. Do not combine incompatible metrics into one score.
- Keep the local geometry as the baseline.
- No hardware advantage claim without a measurement.
