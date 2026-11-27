# Tetragon research

**Status: working development record, 2026-11-27.** The Tetragon (PK-Q4) is a Frozen (Rev H) term. This page summarizes what checkpoints [V0](checkpoints/v0.md) to [V0.3](checkpoints/v0.3.md) derived about it. Nothing here is measured.

:::plain In plain words
A Tetragon is one photon used to hold four possible values at once, by combining two properties of light: its polarization (two options) and its twist, called orbital angular momentum (two options used here). Four combinations make four addresses. The checkpoints ask what you can do to those four addresses with simple operations, using ideal mathematics.
:::

## What the Tetragon is

H/V polarization by OAM −1/+1, index = 2·pol + OAM. See the [frozen glossary](../../library/markdown/A1-glossary.md) and [Volume 3](../../library/markdown/03-encoding-axies.md). Whether one photon carrying two properties is "entangled" is a matter of definition that the library qualifies; the development pages follow that qualification.

## What was derived [DERIVED, ideal model]

| Topic | Result | Checkpoint |
|---|---|---|
| Bell-type states | Single-axis Cliffords reach 4 of the 24 relabellings; local Cliffords on both axes reach all 24 | [V0](checkpoints/v0.md) |
| Bases | 15 Pauli-stabilizer bases: 9 product, 6 entangled; 6 complete mutually unbiased sets of 5; 108 of 225 basis pairs need an entangling gate | [V0](checkpoints/v0.md) |
| Time | A classical schedule adds no entanglement; a time bin used as a quantum control can | [V0](checkpoints/v0.md) |
| Persistence | Operations inside an entangled class compose into one 2×2 unitary; entanglement never changes | [V0.1](checkpoints/v0.1.md) |
| Switching | Edge to diagonal always needs an entangling gate | [V0.1](checkpoints/v0.1.md) |
| Gates | Only logical X gains from a free output geometry | [V0.2](checkpoints/v0.2.md) |
| Redundancy | Z and S have 2 equivalent axes in the diagonal encoding; X and H have none by a single axis | [V0.3](checkpoints/v0.3.md) |

## What it does not show

- Every statement is for ideal pure states and noiseless Clifford operations.
- A larger state space is not by itself higher computational throughput, and entanglement is not by itself controllable communication.
- Equivalent in mathematics is not equal in physical cost: unitary equivalence of two bases says nothing about whether a device can reach one from the other.
- Two entangled Tetragons need a coupled polarization-OAM operation that is an open device question in the frozen library (Volume 6, section 6.7).
