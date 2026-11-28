# Development register of terms

**Status: working development record, 2026-11-27. Separate from the frozen Revision H glossary.** This register labels the status of every term used in the development layer. It does not edit, replace or extend the frozen vocabulary, and it invents no definition for a missing identifier. Where the origin of a term or a conflict between sources is unresolved, the entry says so.

## Status labels

| Label | Meaning |
|---|---|
| **Frozen (Rev H)** | Defined in the frozen Revision H library (Appendix 1 and Appendix 6). Not changed here. |
| **Working (development)** | Adopted in the development documents of this repository for review. |
| **Provisional** | A proposed name or architecture. A literature or naming-conflict check is pending. |
| **Pending source reconciliation** | Used in the checkpoints, but its original definition is not in the repository. |

## Terms

| Term | Status | Where defined | Note |
|---|---|---|---|
| Encoding Axis, Encoding Axies (EA) | Frozen (Rev H) | [Frozen glossary](../../library/markdown/A1-glossary.md) | A physical property of light that carries a label with distinguishable values. |
| Controlled Transformation (CT) | Frozen (Rev H) | [Frozen glossary](../../library/markdown/A1-glossary.md) | A physical operation we can set and repeat that changes the encoded information. |
| Geometric Encoding Axies (GEA) | Frozen (Rev H) | [Frozen glossary](../../library/markdown/A1-glossary.md) | Owner reaffirmed **Geometric Encoding Axies** as the current expansion on 2026-11-27. Earlier publication instructions used "Geometric Entanglement Architecture"; that wording is retained here as historical provenance, not the adopted expansion. |
| Tetragon (PK-Q4) | Frozen (Rev H) | [Frozen glossary](../../library/markdown/A1-glossary.md) | The four-address register H/V polarization by twist −1/+1. |
| Buddy System, Buddy Check | Frozen (Rev H) | [Frozen glossary](../../library/markdown/A1-glossary.md) | The checkpoints study configurable verification resources separately; Buddy's final physical form is open. See [Buddy](buddy.md). |
| Intelligent Registers | Frozen (Rev H) | [Volume 10](../../library/markdown/10-intelligent-registers.md) | Register family and the proposed prepared-instruction scheme PK-E. Not redefined here. |
| State Space (SS), State Space Environment (SSE) | Frozen (Rev H) | [Frozen glossary](../../library/markdown/A1-glossary.md) | Mathematical space of available states, and the physical resource that realizes it. |
| PKC (PhaseKeep Conductor) | Frozen (Rev H) | [Frozen glossary](../../library/markdown/A1-glossary.md) | Classical supervisory system for scheduling, synchronization, resource management and optimization. |
| DDQT (Demand-Driven Quantum Threading) | Frozen (Rev H) | [Frozen glossary](../../library/markdown/A1-glossary.md) | One operating mode of quantum threading. Any link to offline ancilla preparation is a proposed research direction requiring source reconciliation, not a demonstrated integration. The original DDQT documents are not in this repository. |
| High-Dimensional Orthogonal Configurations (HDOC) | Working (development) | [Development glossary](../development-glossary.md) | Adopted under GEA on 2026-11-27 (commit `fa7e48d`). |
| Internal Entanglement | Provisional | [Research development](../research-development.md) | Non-separability between distinct encoded properties of one photon. |
| Coupled Photonic Entanglement (CPE) | Provisional | [Research development](../research-development.md) | Entanglement between separate photonic subsystems. Naming-conflict search not done. |
| Symmetric Encoded Entanglement (SEE) | Provisional | [Research development](../research-development.md) | Corresponding encoded properties across separate registers. Naming-conflict search not done. |
| Nonsymmetric Encoded Entanglement (NEE) | Provisional; historical | [Research development](../research-development.md) | **Transition recorded 2026-11-27:** the project owner proposes Convergent Entanglement as the replacement. NEE is preserved unchanged in historical documents. |
| Convergent Entanglement | Provisional | Owner-supplied definition, 2026-11-27 | Entanglement between noncorresponding Encoding Axies of separate registers, relative to a specified subsystem partition. Proposed replacement for NEE. It is not claimed to be an exhaustive classification, and complex multipartite states need not decompose into these categories. Naming-conflict investigation pending. |
| Entangled Encoded Transformation (EET) | Provisional | [Research development](../research-development.md) | A specialized CT intended to change how entanglement is organized. |
| Integrated Entangled Environment (IEE) | Provisional | [Research development](../research-development.md) | Proposed; explicitly provisional there. |
| PALADIN | Working (development); implementation unvalidated | Owner-supplied definition, 2026-11-27; first appears in checkpoint [V0.4](checkpoints/v0.4.md) | Protective Autonomous Logic for Anomaly Detection, Isolation and Neutralization. See [PALADIN](paladin.md). |
| Docked Scheduling (DS) | Working (development); implementation unvalidated | Owner-supplied definition, 2026-11-27; first appears as a "provisional name" in checkpoint [V0.1](checkpoints/v0.1.md) | See [Docked Scheduling](docked-scheduling.md). |
| Integrated Quantum Assurance (IQA) | Working (development) name; exploratory framework | Owner naming decision, 2026-11-27; [IQA](iqa.md) | Current expansion; a primary research pillar alongside GEA. Encompasses verification, preservation, resource preparation, operational integrity and quantum information continuity. No implementation or validation claim. |
| Independent Quantum Assurance (IQA) | Historical provisional expansion; superseded | Earlier owner-supplied definition, 2026-11-27; preserved below and on [IQA](iqa.md) | Assurance requirements specified separately from assessment mechanisms. Historical occurrences and stable IQA identifiers remain unchanged. |
| Resource classes (helper types for Buddy), "information checkpoint" | Pending source reconciliation | Checkpoint [V0.5](checkpoints/v0.5.md) | Names used in the checkpoints as proposals; no name check has been done. |
| BUD-01 to BUD-04, PAL-01, INT-01 | Pending source reconciliation | Checkpoints [V0.4](checkpoints/v0.4.md) and later | **Working identifiers** for studies in the checkpoints. They are not registry entries; no identifier has been renumbered. |
| Third axis ("path", provisionally) | Pending source reconciliation | Checkpoint [V0.8](checkpoints/v0.8.md) | The choice of a third encoding axis is open. |
| Buddy memory, execution, interface and resource branches | Pending source reconciliation | none in this repository | Named in the publication instructions; no definition was supplied or found. None is defined here. |

## QDE extension identifiers (2026-11-27)

[PROPOSED] **PROVISIONAL** additions using this register's existing term-based scheme. No BUD, PAL, INT, checkpoint or frozen identifier is reassigned. Definitions and evidence boundaries are in the [framework](qde-relational.md).

| Identifier | Provisional definition and boundary |
|---|---|
| QDE | [PROPOSED] Quantum Dimensional Environment: organizing framework under GEA for a joint state space, partitions, relations and available evolution; not the bath. QDE/IEE reconciliation remains open. |
| Convergent Quantum Relationships | [PROPOSED] Classification of contextual state properties and relations; broader than Convergent Entanglement, which retains its existing meaning. |
| QIJ | [PROPOSED] Quantum Interaction Junction: role of a specified interaction process, not a demonstrated device. |
| QIJ-I | [PROPOSED] Instruction role. |
| QIJ-D | [PROPOSED] Data role. |
| QIJ-V | [PROPOSED] Verification role. |
| QIJ-R | [PROPOSED] Resource preparation/known-state recreation role. |
| QIJ-T | [PROPOSED] Coherent transfer role. |
| ASV | [PROPOSED] Alternating Stacked Verification within Integrated Quantum Assurance; rotating roles and accumulated evidence, with disturbance and correlated faults explicitly modelled. Buddy System remains named. |

## Distinctions to keep

- **GEA** organizes encoding geometry; **CT** is a physical operation; **SSE** is the space and its realizing resource.
- **Buddy** is the verification, assistance, preservation and continuation function; **IQA**, now Integrated Quantum Assurance, is the exploratory assurance framework; its earlier specification-versus-implementation distinction is preserved as historical context, not an implemented architectural change; **PALADIN** is physical protection of hardware, distinct from verifying information.
- **PKC** is the classical supervisor; **Docked Scheduling** is a scheduling method inside it; **DDQT** is a threading mode that also uses scheduling. A shared name or shared scheduling does not make them the same thing.
- A detector herald does not necessarily certify a valid, reusable quantum output (frozen README statement).

## Not found in the repository

IQA, PALADIN, Docked Scheduling, Convergent Entanglement, BUD-xx and the resource-class names do not occur in Revision H or in the pull request #1 material (checked by text search on 2026-11-27). They enter the repository with this development layer, labelled as above.

## IQA naming decision (2026-11-27)

The owner adopts **Integrated Quantum Assurance (IQA)**, superseding the earlier provisional expansion **Independent Quantum Assurance**. GEA (Geometric Encoding Axies) and IQA are the two primary research pillars of the current direction. IQA is an exploratory framework encompassing verification, preservation, resource preparation, operational integrity and quantum information continuity.

PhaseKeep remains an evolving collection of research directions without a predetermined technological destination. The objective is discovery rather than confirmation; a modest, independently verifiable contribution to an existing field is worthwhile. No experimental validation, demonstrated quantum computing capability or established breakthrough follows from this naming decision.

For historical traceability, the earlier definition is preserved verbatim:

> An architectural principle that independently establishes the assurance requirements of prepared and evolving quantum information, separating the specification of expected quantum properties from the physical mechanisms used to assess them. Independence refers to the separation of specification and implementation, not physical isolation or independence from hardware capabilities.

This is a naming and research-scope decision, not an architecture revision. Buddy System terminology and functions remain documented. Historical documents, checkpoints, stable identifiers and frozen releases are not renamed or rewritten. A broader naming-conflict investigation remains pending.
