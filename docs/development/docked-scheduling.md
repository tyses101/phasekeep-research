# Docked Scheduling (DS)

**Status: working development concept; implementation unvalidated. Not part of the frozen Rev H vocabulary.**

:::plain In plain words
Docked Scheduling is a classical timetable. Photons, control hardware and resources are brought together into shared time windows so everything is ready at once. The timetable does not look at the quantum state, and time is not used as a storage property of the data.
:::

## Definition (project owner, 2026-11-27)

A classical scheduling method within the PhaseKeep Conductor (PKC) that coordinates photon arrival, physical control readiness and resource availability within synchronized execution windows, without requiring inspection of the encoded quantum state or introducing time as an Encoding Axie.

## Where it appears in the checkpoints

[V0.1](checkpoints/v0.1.md) section 4 separates two meanings of "time". A classical schedule, called there "Docked Scheduling (provisional name)", creates no entanglement. A time bin in superposition that selects an operation is a quantum control register and is a different thing. The ideal-model example creates 1 ebit between time and polarization only in the second case [DERIVED].

## Relationships

- **PKC:** the frozen classical supervisor for scheduling, synchronization, resource management and optimization. DS is described as a method within it.
- **DDQT:** the frozen operating mode of quantum threading, with scheduling that can be classical. Both use scheduling; this register does not identify them. Preparing resources ahead of demand is part of the frozen inventory-based DDQT mode, but any claim that DS or DDQT removes probabilistic operations from the active path is a proposed research direction requiring source reconciliation. V1.0 found that, in the modelled flagged round, the flag gates are interleaved with the data couplings, and preparing resources offline does not remove the eight data-touching inter-photon gates.
- **Time as an Encoding Axie:** the frozen design does not treat time as an EA. DS does not introduce it.

## Limits

No scheduling algorithm, timing model or synchronization tolerance has been derived or tested in the checkpoints. V1.0 notes that loss in its model is per gate participation, not per unit time stored, so time-dependent loss and scheduling are a roadmap item, not a result ([roadmap](roadmap-v1.1.md)).
