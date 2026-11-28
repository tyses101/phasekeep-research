# What's next

[← Start here](README.md) · [Full pending list](02_the_full_story/13_pending.md)

> **In plain words:** first merge and verify this package. Then the three most useful steps are: test the simple two-ring gate on real quantum hardware; design pulses and interaction together (E8); and work out logical error protection. Atomic decay remains the main physical question.

## Priority order
| # | Item | Why now | Cost |
|---|---|---|---|
| 1 | **Codex integration and verification** | Makes everything reproducible and public | Low |
| 2 | **REF-03-I noisy simulation, then a cloud hardware run** | First real-world contact: 6 qubits, one CZ | Low to moderate (needs a cloud account) |
| 3 | **E8: joint interaction + pulse optimization** (segmented CPMG-4, interaction-aware flips) | Closes the ½-cycle drift blind spot; may allow the interaction to stay on | Moderate (local) |
| 4 | **Open-system model** (decay, dephasing, collective decay, erasure flagging) | Decay dominates every budget | Moderate |
| 5 | **REF-05-L and Buddy benchmarks** against repetition codes and [[4,2,2]] | No logical protection exists yet | Moderate |
| 6 | **G0 parameter retrieval** (superconducting and ion numbers; circular-Rydberg emission inhibition) | Platform ranking needs real numbers | Low to moderate |
| 7 | **Derive sixth-order suppression** | Is it general or sequence-specific? | Theory |
| 8 | **Prior-art and originality review** | Required before any novelty statement | Moderate |
| 9 | **Hypercube code protection** | Capacity versus protection for larger registers | Moderate |
