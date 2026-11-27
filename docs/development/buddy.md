# Buddy System: development research

**Status: working development record, 2026-11-27. The Buddy System is a Frozen (Rev H) term. Its final physical architecture is open and is not decided here.**

:::plain In plain words
The Buddy System is the project's name for helper photons and checks that look after a computation: preparing things, assisting, verifying, preserving and continuing. The checkpoints from V0.4 to V1.0 ask a narrow question first: can a helper check a property of the data without reading the data, and does that make the whole computation more reliable?
:::

## Frozen definition

"The proposed way to manage preparation, assistance, verification, preservation and continuation using helper (ancillary) photons" ([frozen glossary](../../library/markdown/A1-glossary.md), [Volume 7](../../library/markdown/07-buddy-checks.md)). A Buddy Check answers PASS, FAIL or UNKNOWN based only on demonstrated evidence.

## What the checkpoints studied

Only the verification responsibility, in stages. Other Buddy responsibilities (preparation, assistance, preservation, continuation) are not studied.

| Stage | Checkpoint | Finding [DERIVED, inside the stated models] |
|---|---|---|
| A parity check detects flips and misses phase errors | [V0.4](checkpoints/v0.4.md) | The Buddy can lower reliability if its own faults are not small |
| Repeated checks, reuse, routers | [V0.5](checkpoints/v0.5.md) | Spacing matters; silence is not PASS |
| Compatibility with how a gate is built | [V0.6](checkpoints/v0.6.md) | Compatibility depends on implementation, and on transporting the check |
| What a PASS means | [V0.7](checkpoints/v0.7.md) | It confirms the checked property only |
| Local versus joint geometries | [V0.8](checkpoints/v0.8.md) | Neither covers the other; adaptive switching depends on workload |
| Reliability of the extraction itself | [V0.9](checkpoints/v0.9.md) | Flags remove first-order silent damage, not second-order; not always best |
| Physical feasibility | [V1.0](checkpoints/v1.0.md) | Probabilistic gates and unheralded loss may decide usability |

## Configurations examined

Local conventional, joint conventional, joint flagged, joint verified-cat, a cooperative variant and a ZZZZ-only partial joint round. Working identifiers (BUD-xx) label early studies and are not a registry. No configuration is best on every separate metric, and the best one changes with the assumed noise. That supports the *possibility* that Buddy has several configurations selected by IQA; it does not show they are worth their combined complexity.

## A detector herald is not a certificate

A heralded outcome does not necessarily certify a valid, reusable quantum output (frozen README statement). The checkpoints add that **heralded failure is not safe retry**: a failed inter-photon gate can disturb a data photon. V1.0 reports completion probability and conditional correctness side by side so that completing fewer runs never makes an architecture look reliable.

## Established techniques versus PhaseKeep-specific proposals

Parity checks, stabilizer codes, flag qubits, cat-state ancillas, repeated syndrome extraction and reference-state characterization are established techniques of quantum information, recalled here at title or abstract level and UNVERIFIED in full text. PhaseKeep's proposals are the selection among configurations by assurance requirements (IQA), the Tetragon geometries, and hosting several ancillary axes in one photon. None is claimed as new physics.

## Open

Physical form of the Buddy; whether a nondestructive parity measurement exists; correlated loss in shared ancillary hosting; whether one coupler can serve verification, computation and characterization. See [Open problems](open-problems.md) and [Active information versus replaceable resources](active-vs-replaceable.md).
