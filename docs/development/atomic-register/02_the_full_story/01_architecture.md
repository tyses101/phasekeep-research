# 1. Architecture

[← Contents](00_contents.md) · [Next: register geometry →](02_register_geometry.md)

> **In plain words:** PhaseKeep is a set of cooperating parts: one organizes the information, one holds it, one addresses it, one runs operations, one checks integrity, and one coordinates the rest. This update adds new parts and new uses for old ones. Nothing existing is renamed or retired.

[ASSUMED] Scope: numerical statements apply only to the stated model, sequence and sampled parameters. They are not hardware guarantees.

## The components and how they relate

| Term | Role in this update | Status |
|---|---|---|
| **GEA**: Geometric Encoding Axies | Organizes encoding axes. Now also used for **carrier-independent** encoding (photonic and atomic), as a development-layer extension | Frozen term; extension PROPOSED |
| **QDE**: Quantum Dimensional Environment | Joint state space and relationships (unchanged since `e5f1507`) | PROPOSED |
| **MSR**: Multispatial Register (written MSR^Ξ, or MSR[d₁,d₂,…]) | A persistent computational register, described by its **axis signature** (e.g. Tetragon = [2,2]) | PROPOSED (new) |
| **RAMM**: Random Access Multispatial Matrix | **Coherent register addressing and control.** Not QRAM, and not a memory | PROPOSED (new) |
| **PK-E** | Frozen meaning: *the proposed prepared-instruction execution scheme*. Register execution in this update is described as RAMM/QIJ operations, not a redefinition of PK-E | Frozen; new usage PROPOSED |
| **PK-M** | Frozen meaning: *the proposed four-mode atomic-vapor memory*. Kept distinct from register persistence | Frozen |
| **PK-LMI**: PhaseKeep Light-Matter Interface | Coherent transfer between carriers. Shared transfer requirement for photonic and atomic tracks | Pending source reconciliation |
| **QIJ**: Quantum Interaction Junction | The physical interaction mechanisms. Now hosts the ring-mode echo, pulse shaping and composite flips as techniques | PROPOSED |
| **IAD**: Inter-Axial Dynamics | How encoding axes evolve and couple, including disturbances and controls | PROPOSED (new) |
| **IQA**: Integrated Quantum Assurance | Integrity checks, organized into three levels (chapter 6) | Working |
| **ASV**: Alternating Stacked Verification | Unchanged: rotating verification roles within IQA | PROPOSED |
| **Buddy System** | Unchanged name; now framed as **encoded redundancy**, never copying unknown states | Frozen |
| **PKC**: PhaseKeep Conductor | Classical supervisor. Candidate for operation-dependent register selection | Frozen |
| **DDQT** / **AIS** | Unchanged frozen definitions. DDQT gains a scheduling constraint (HOLD and ROTATE can't share an axis) | Frozen |

## How a computation flows (PROPOSED)

```
PKC (classical supervisor)
 └─ RAMM: selects registers and operations
     └─ MSR: persistent register (e.g. two Tetragon rings)
         ├─ stable storage between operations (shelving: unverified)
         └─ QIJ: activation → HOLD / ROTATE / COUPLE → deactivation
              └─ IQA: excitation count, parity, (future) logical redundancy
```

## Implementation tracks (kept separate)

| Track | Encoding | Status |
|---|---|---|
| Photonic | polarization × OAM (Tetragon) | Earlier work; IAD-01 stability study proposed |
| Atomic, individual atoms | internal state × ring site mode | Ideal-model SIMULATED |
| Atomic, collective excitation (ensemble) | internal state × spin-wave phase | PROPOSED; negative results in ch. 3 |
| Digital reference | compact (3 qubits per ring) or one-hot (8) | SIMULATED; no hardware run |

**Carrier independence is an aim, not a result.** No architecture has been shown on more than one carrier.
