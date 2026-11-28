# Terms

[← Start here](../README.md)

Every term used in this update: what it means, where it comes from, and its status. **Frozen** terms come from the frozen Revision H library and are **not changed here**. New items are provisional until Codex reconciles them with the repository register (`docs/development/register-of-terms.md`).

## Existing terms (preserved)
| Term | Meaning | Status | Note for this update |
|---|---|---|---|
| EA / Encoding Axies | A physical property carrying a label with distinguishable values | Frozen (photonic definition) | Generalized EA for any carrier is a **development-layer proposal**. The frozen definition is untouched |
| GEA | Geometric Encoding Axies | Frozen | |
| CT | Controlled Transformation | Frozen | |
| Tetragon (PK-Q4) | Four-state register, polarization × OAM | Frozen | Atomic analogue = signature [2,2] |
| Register family (Qubit … Hyperion) | Registers of 1–12 binary axes | Frozen (Vol. 10) | Names = hypercube vertex counts. Confirmed natural for hopping (ch. 2) |
| SS / SSE | State space / its physical realization | Frozen | |
| Buddy System, Buddy Check | Verification and assistance function; PASS / FAIL / UNKNOWN | Frozen | Level-3 IQA is framed as encoded redundancy |
| PKC | Classical supervisor | Frozen | |
| DDQT | Demand-driven quantum threading | Frozen | New constraint: HOLD and ROTATE can't share an axis |
| AIS (AIS-1/2/3) | Instruction streaming levels | Frozen | Unchanged |
| **PK-M** | *Proposed four-mode atomic-vapor memory* | Frozen | Register persistence is **not** PK-M |
| **PK-E** | *Proposed prepared-instruction execution scheme* | Frozen | Historical package usage was loose; register execution here means RAMM/QIJ operations. Frozen PK-E is preserved |
| HDOC | High-Dimensional Orthogonal Configurations | Working | |
| IQA | Integrated Quantum Assurance | Working | Three-level organization proposed |
| QDE, QIJ (I/D/V/R/T), ASV | As merged at `06a56cf` | Provisional | **ASV = Alternating Stacked Verification.** An interim record wrongly said "adaptive" |
| PK-LMI | Light-matter interface | Pending source reconciliation | Shared transfer requirement (ch. 3) |
| VOM | Expansion supplied by the package only; owner definition unconfirmed | Pending, undefined | Not used here |

## New provisional terms (this update)
| Term | Meaning | Status |
|---|---|---|
| **MSR** (MSR^Ξ, or MSR[d₁,…]) | Multispatial Register: a persistent computational register, described by its axis signature | PROPOSED |
| **Axis signature** [d₁, d₂, …] | Dimensions of each encoding axis. Tetragon = [2,2], a single four-level axis = [4] | PROPOSED |
| **Trigon** [3], **Pentagon** [5] | Single-axis qudit aliases (qutrit, five-level) | PROPOSED. Naming-conflict check pending. Pentagon (5) ≠ Penteron (32) |
| **RAMM** | Random Access Multispatial Matrix: coherent register **addressing and control**. **Not QRAM, not memory** | PROPOSED |
| **IAD** | Inter-Axial Dynamics: evolution and coupling of axes, disturbances, controls | PROPOSED |
| **HOLD / ROTATE / COUPLE** | RAMM instruction primitives (ch. 5) | PROPOSED |
| **Ring-mode echo** | Staggered flips that reverse hopping. A technique under QIJ, deliberately **without** an acronym | SIMULATED |
| **Circulation correlations** | Internal state × ring-circulation entanglement. Non-trivial flux can lift the tested circulation degeneracy; current itself can exist at zero flux | PROPOSED |
| **G0** (A1, A2, B, C1, C2, D) | Physical-platform qualification branches | PROPOSED identifiers |
| **REF-01 … REF-05**, REF-03-I/P/N, REF-05-L | Digital-reference experiments | PROPOSED identifiers |
| **P2-CIM, E1–E7, E7-D, E8** | Experiment identifiers | Temporary labels |
| **IQA-DS** | Dual-species assurance | PROPOSED, provisional name |

## Retired from consideration (kept for the record)
| Term | Reason |
|---|---|
| "Spectral momentum" | Duplicate of frequency; never adopted |
| SSMF (Solid Space Modulation Field) | Never adopted; overlaps PK-M and PK-LMI |
| GCS and other "search" names | User rejected the "search" framing |
