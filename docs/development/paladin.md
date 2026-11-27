# PALADIN

**Status: working development architecture; physical implementation unvalidated. The name's abbreviation and literature checks are pending. Not part of the frozen Rev H vocabulary.**

:::plain In plain words
PALADIN is a proposed set of classical hardware safeguards. If a component misbehaves, PALADIN is meant to spot it, isolate it so it stops interfering, and report what is still available. It protects the machine. It does not repair a quantum state that is already damaged.
:::

## Definition (project owner, 2026-11-27; consistent with checkpoint V0.4)

**Protective Autonomous Logic for Anomaly Detection, Isolation and Neutralization.** A proposed physical protection architecture concerned with detecting anomalies, isolating malfunctioning components, preventing further interference, reporting resource availability and supporting validated reintegration.

**Neutralization** means preventing an identified faulty component from continuing to interfere with system operation. It does not imply quantum-state recovery.

## How it differs from Buddy

| Responsibility | Buddy | PALADIN |
|---|---|---|
| Quantum parity verification | Yes | No |
| Hardware operating limits | Supporting evidence | Yes |
| Verification-equipment diagnostics | Supporting evidence | Yes |
| Autonomous hardware isolation | No | Yes |
| Quantum error correction | Not established | No |
| Fault propagation containment | Information-level rejection | Physical isolation |

Source: [V0.4](checkpoints/v0.4.md), section 9. PALADIN is physical protection; Buddy checks are information verification. Classical diagnostics cannot necessarily see an ancilla phase error, and a failed quantum verification does not by itself identify a faulty component. PALADIN protects future operations and cannot recover information that is already destroyed.

## Reconciliation

The owner definition matches the V0.4 text. The V0.4 page also records the function as close to standard fault detection, isolation and recovery practice in engineering systems (UNVERIFIED, from memory) and notes that one quick search found no obvious conflict among returned titles, which is not a conflict check. The vocabulary rule that a new term needs a literature check and a demonstrated purpose still applies; the purpose proposed is to keep hardware-fault handling separate from quantum-state evidence.
