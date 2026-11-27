# GEA and Controlled Transformation in the development layer

**Status: working development record, 2026-11-27.** GEA, Encoding Axies and CT are Frozen (Rev H) terms and are not redefined here. This page records how the checkpoints used them.

:::plain In plain words
GEA is a way of drawing the states of a register as the corners of a square, cube or higher-dimensional cube, so that "which corner" and "how far apart" become geometry. A Controlled Transformation is any adjustable physical operation that changes what is stored. The checkpoints use these ideas to ask which operations are cheap and which need photons to interact.
:::

## Frozen definitions (quoted by reference)

- **GEA (Geometric Encoding Axies):** reading the states of a register as the corners of a square, cube or hypercube ([frozen glossary](../../library/markdown/A1-glossary.md), [Volume 4](../../library/markdown/04-geometric-encoding.md)).
- **CT (Controlled Transformation):** a physical operation we can set and repeat that changes the encoded information. "Controlled" means adjustable, not "conditioned on another qubit" ([Volume 5](../../library/markdown/05-controlled-transformations.md)).

**Terminology discrepancy, unresolved.** The 2026-11-27 publication instructions expand GEA as "Geometric Entanglement Architecture". The frozen glossary says "Geometric Encoding Axies", and every checkpoint uses that. This page keeps the frozen wording. See the [register of terms](register-of-terms.md).

## How the checkpoints used them

| Idea | Used in | Result |
|---|---|---|
| Edge versus diagonal encoding of one logical qubit | [V0.1](checkpoints/v0.1.md), [V0.2](checkpoints/v0.2.md), [V0.3](checkpoints/v0.3.md) | Same logical qubit, different physical cost per gate; no encoding is uniformly better |
| Local versus joint verification geometry on four axes | [V0.8](checkpoints/v0.8.md) | The two geometries see different faults; neither covers the other; conversion needs 2 inter-photon gates |
| Geometry chosen from noise conditions | [V0.8](checkpoints/v0.8.md), [V0.9](checkpoints/v0.9.md), [V1.0](checkpoints/v1.0.md) | The preferred geometry changes with assumed noise, including a reversal under X-bias [DERIVED on ASSUMED] |
| High-dimensional orthogonal configurations (HDOC) | [development glossary](../development-glossary.md) | A related working term; the five-basis investigation is proposed and unrun |

## Controlled Transformation under these checkpoints

- Conversion between the local and joint geometries is a CT: four elementary gates, two of them inter-photon ([V0.8](checkpoints/v0.8.md)).
- Under probabilistic inter-photon gates the conversion completes with probability about s² if a failure aborts it: 0.5625 at s = 0.75 and 0.25 at s = 0.5. This is not comparable to V0.8's undetected-fault break-even, which is about 2e-4 in that model ([V1.0](checkpoints/v1.0.md)).
- Verification, computation and characterization are different choices of the measured Pauli product, but this does not merge Buddy and CT ([Physical feasibility](physical-feasibility.md)).

## Limits

Gate sets are assumed. No claim that a photonic platform provides them. No physical cost has been assigned to any geometry or transformation.
