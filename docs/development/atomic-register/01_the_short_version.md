# The short version
*PhaseKeep research update, 27–28 November 2026. Development research record. No hardware measurements.*

[← Start here](README.md) · [Full story →](02_the_full_story/00_contents.md)

---

## The question
Can a quantum register use its **physical shape** (its geometry), its **energy structure** and its **symmetries** to compute and protect information more cheaply than conventional designs?

## What we tried
- **Light.** PhaseKeep started by storing information in two properties of a single photon: polarization and twist (orbital angular momentum, OAM). Four combinations make a "Tetragon".
- **Atoms.** Light is hard to keep, so we looked at atoms instead. That led to a design where **four atoms sit in a ring**, one excitation hops around it, and each excitation also has an internal "which level" state. Two such rings, coupled together, can compute.
- **Simulation.** We simulated that design in increasing detail: control, errors, timing and drift. Then we checked which real hardware could build it.

## What worked (in simulation)
- **Full control is possible.** Each ring can be fully controlled, but only if the excitation can hop between atoms.
- **A simple "flip" trick (an echo) cancels a whole class of hardware imperfections exactly.** These are uneven or miscalibrated hopping strengths, as long as they don't change during the operation.
- **The two-ring operation reduces to a standard gate** (one CZ), which makes it cheap to test on existing quantum computers.
- **Small imperfections on their own are suppressed extremely strongly.** Sixth-order scaling was observed over the tested parameter range for this model and sequence.

## What didn't work
- **Combined imperfections** are much worse than separate ones. The rule we found: hopping error × interaction unevenness must stay below about **0.015** for the dominant fitted contribution to a 1-in-10,000 error budget, not total accuracy.
- **Hopping strength that drifts *during* an operation** defeats the echo. A 5% slow ramp gives about 39% error. Worse, it's the kind of error our integrity checks **can't see**.
- **Several "smoother" pulse designs** turned out worse, and we found why: the interaction has to be **balanced** across the echo's two halves.
- **Our integrity checks** catch lost excitations and some errors, but **not every logical error**. No method for *recovering* information has been shown yet.

## The honest bottom line
- **The register isn't a new kind of qubit.** Mathematically it's a known structure: two qubits on a square, with a standard error-detecting code.
- **What needs prior-art comparison** is the way it's physically built and controlled. The tolerance rules found here can be tested experimentally.
- **No hardware has built it.** The biggest physical obstacle is **atomic decay**, which outweighs every other error we computed by a wide margin.

## What happens next
- **Publication:** see the dated integration checkpoint for verification scope.
- **Research:** the next work is joint pulse-and-interaction optimization (E8), testing the simple two-ring gate on real quantum hardware, and logical error protection.

See [what's next](05_whats_next.md).
