# Independent Quantum Assurance (IQA)

**Status: working development record, 2026-11-27. Provisional working name and architecture. Outside the frozen Rev H vocabulary and library. A naming check is pending.**

:::plain In plain words
IQA is the idea of writing down, separately from the hardware, what a prepared or evolving quantum state is supposed to satisfy, and then letting different mechanisms check it. "Independent" means specification is kept apart from implementation. It does not mean physically isolated.
:::

## Definition (project owner, 2026-11-27)

An architectural principle that independently establishes the assurance requirements of prepared and evolving quantum information, separating the specification of expected quantum properties from the physical mechanisms used to assess them. Independence refers to the separation of specification and implementation, not physical isolation or independence from hardware capabilities.

## What the checkpoints used it for

- **Capability reports.** V0.9 and V1.0 define a capability report listing, for each verification configuration, separate metrics (silent-error probability, rejection, completion, inter-photon gates, photons consumed, readout error and so on). No combined score is formed.
- **Selection.** For a stated requirement and physical profile, a feasible set and a Pareto set are computed. An empty feasible set is a valid answer.
- **Operational assurance.** Reference preparations establish whether an apparatus has a constant error, optionally amplified. This characterizes the apparatus. It does not certify an individual unknown state.
- **Division of labour (V1.0 suggestion, PROPOSED).** IQA specifies a characterization sequence and its expected outcome, a Controlled Transformation executes it, and Buddy measures the deviation.

## Limits and cautions

- Everything is demonstrated on abstract fault models and a toy set of physical profiles.
- Selecting a mechanism from an estimated noise bias is a hypothesis to test, not a result. The cost of adaptation is not established.
- IQA does not certify an individual unknown state; apparatus characterization is not individual-state certification.
- IQA is a working name. The naming-conflict search has not been done, and the term appears nowhere in the frozen library.

See [Buddy](buddy.md), [Physical feasibility](physical-feasibility.md) and [V1.0](checkpoints/v1.0.md).
