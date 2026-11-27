# A plain-language overview

**Status: working development record, 2026-11-27. For readers new to quantum computing.** The technical pages are complete and unabridged; this page only explains the ideas. It makes no claim beyond them.

## What is PhaseKeep trying to find out?

Quantum computers store information in fragile things, and light is one candidate. A single particle of light, a photon, can carry several independent properties at once: which way its electric field wiggles (polarization) and how its wavefront twists (orbital angular momentum). PhaseKeep asks whether organizing those properties deliberately, and changing the organization on demand, could make quantum operations cheaper, more controllable, more reliable or easier to keep going. That is an open question. **No hardware has been built or measured, and no advantage has been shown.**

## What is a Tetragon?

A Tetragon is one photon used to hold four possible values (two polarizations times two twists). The first checkpoints, V0 to V0.3, ask in ideal mathematics what simple operations can do to those four values.

## What is the Buddy System?

A quantum computation is easily damaged, and looking at the data directly destroys it. The Buddy System is the proposal to use helper photons and clever checks that test a property of the data, such as "is the number of flips even?", without reading the data itself. Checkpoints V0.4 to V1.0 study that idea with simulated faults.

## What did the later checkpoints find?

- **A check can fail too.** The helper can damage the data it protects, and some errors, such as a wrong angle, pass the check anyway.
- **Smarter checks help, but not completely or always.** Extra flag helpers remove one class of silent damage, but not the next, and they lose in some noise conditions.
- **The physical interactions may decide everything.** In the model, joining a helper photon to a data photon is the expensive step, and it may only sometimes work. If a failure also disturbs the data, checking can be worse than not checking. If a helper silently disappears, the damage is larger than any cleverness in the check can buy back.
- **Some failures only waste a helper; others can ruin the information.** Counting how many interactions touch the data and how many touch only helpers is one way to see how exposed the information is.

## What this does not say

These are calculations under assumed numbers. They are not measurements, and they do not show that a PhaseKeep machine could work or could not. They show where the proposal looks fragile, which is useful for deciding what to test first.

## Where to go next

[Research status](research-status.md), then the [timeline](timeline.md) and [physical feasibility](physical-feasibility.md). The frozen [learning library](../../library/markdown/00-start-here.md) is the gentler, longer introduction.
