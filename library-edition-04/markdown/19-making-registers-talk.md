# Making Registers Talk

*Coupling two rings, frequency planning, gentle pulses, the echo, and testing on today's computers*

*Edition 04 working draft, research snapshot as of 28 November 2026.*


>
> **In plain words**
> One ring on its own can only do so much. To compute, two rings must influence each other, and only in the way we intend. This volume shows:
> - how two rings are coupled
> - how to keep them from swapping contents by accident
> - why gentle pulses beat abrupt ones
> - a simple "echo" that cancels a whole class of hardware imperfections exactly
> - how the logic can be tested on today's quantum computers
>
> Everything here comes from ideal simulations: careful models, not hardware.


## 19.1 Two rings, one deliberate interaction

Put two four-atom rings near each other. Rydberg atoms in neighbouring rings push on each other, and the strength depends on which internal level each marked excitation is in. Arrange it so that the push acts **only when both excitations are in level R2**. Then, after the right amount of time, the pair picks up a phase of exactly π in that one case and nothing otherwise. That is a standard two-qubit gate, called a controlled-Z (CZ). [DERIVED]

But real atoms sit at different distances. The atoms of the two rings that face each other push harder than the far ones. Split the interaction into two parts:
- **The average part:** the same for every pair of atoms. This produces the intended gate.
- **The uneven part:** how much each pair differs from the average. This is an **error**: it can scramble the ring patterns.

Much of the design work is about keeping the uneven part from doing damage.

## 19.2 Frequency planning: keeping rings from trading contents

Each ring's standing waves sit at energies ±2J, and its travelling modes at 0. Now consider two rings together. With equal hopping in both, some combinations of a standing wave in one ring and the opposite standing wave in the other add up to **zero**. That is exactly the energy of states *outside* the register. The interaction can then push the register out of its code at no energy cost.

[DERIVED] Working through every combination, this happens whenever the ratio of the two rings' hopping strengths is **1, 2 or ½**. Away from those ratios the register's energies and the outside energies never coincide. The safest choice is a ratio of **1.5**, where the smallest gap equals the weaker ring's hopping.

[SIMULATED] The simulations confirm it. Settings: interaction strength one-twentieth of the weaker hopping, rings two ring-widths apart.

| Hopping ratio | Worst leakage out of the register |
|---|---|
| 1.0 | 100% |
| 1.425 | 3.9% |
| **1.5** | **3.0%** |
| 1.575 | 2.4% |
| 2.0 | 100% |

Giving neighbouring registers **different natural frequencies** so they don't interfere is called **frequency planning**. It's familiar from radio, and from superconducting quantum computers.

## 19.3 Gentle beats abrupt

How you switch the interaction on matters. Switch it on suddenly, and the register is jolted; part of it is knocked out of the code and stays out. Ramp it up and down smoothly, following a sin² curve, and the register adjusts as it goes and returns cleanly at the end.

[SIMULATED] For the same total gate time:

| Pulse | Final leakage |
|---|---|
| Abrupt on/off | 2.2 × 10⁻² |
| Smooth (sin²) | 2.3 × 10⁻⁶ |

That's about ten thousand times less leakage. The register still leaves the code *temporarily* during the pulse, but comes back.

## 19.4 The echo

While the rings interact, each ring's own hopping keeps running in the background, and real hopping strengths are never exactly what we intend. Here is a remarkably simple fix.

Recall the staggered flip from [Volume 18](18-four-atom-ring.md): a half-turn of phase on every second atom. Every hop in a four-atom ring connects an "odd" atom to an "even" one. The flip therefore **reverses the sign of every hop**, whatever its strength.

So: run for a while, flip, run for the same time, flip back. The second half undoes the first half's hopping exactly. [DERIVED] In symbols, S·e^(−iHt)·S·e^(−iHt) = 1, where S is the flip and H is the hopping. That holds **even if the hopping strengths are wrong or uneven**, as long as they stay steady.

The average interaction, meanwhile, is unaffected by the flip and by the hopping. It keeps accumulating, so the intended gate survives the echo. [SIMULATED] Results:
- With the echo, the gate's average fidelity rose from 98.22% to **99.989%** in the standard model.
- With a 10% hopping error and a uniform interaction, the echo's cancellation was exact to about 10⁻¹⁴.
- That stays true even when the two internal levels hop at different rates.

>
> **Common mistake**
> The echo cancels hopping that is wrong but **steady**. [Volume 20](20-when-things-go-wrong.md) shows what happens when hopping changes *during* the operation, and when the interaction is uneven. Both break the exact cancellation.


## 19.5 Three instructions

The echo gives the register three distinct modes of operation. PhaseKeep's working names for them ([Appendix 7](A7-glossary-additions.md)):

| Instruction | What it does | What it relies on |
|---|---|---|
| **HOLD** | Keeps the ring pattern still: hopping cancelled by the echo | Steady hopping |
| **ROTATE** | Lets hopping act on purpose, rotating the pattern's phase | Accurately known hopping and timing |
| **COUPLE** | Interacts two registers while each one's hopping cancels | Steady hopping and a uniform interaction |

The layer that chooses which registers receive which instruction is called **RAMM** (Random Access Multispatial Matrix), a working development term. RAMM is about **addressing and control**. It is not a memory, and not "quantum RAM" in the technical sense.

>
> **Common mistake**
> HOLD is not a quantum memory. It cancels hopping, nothing else. Decay and other disturbances carry on. And a register can't HOLD and ROTATE on the same axis at the same time, so a scheduler must keep them apart.


## 19.6 Testing the logic on today's quantum computers

The register doesn't need its own hardware to have its *logic* tested. [Volume 18](18-four-atom-ring.md) showed that one ring is two qubits with a code on top. So the whole design can run on an existing quantum computer [DERIVED]:

| | Physical-style encoding (one qubit per atom-and-level) | Compact encoding (Gray code) |
|---|---|---|
| One ring | 8 qubits | 3 qubits |
| Two rings | 16 qubits | 6 qubits |
| One ring's hopping | Exact in a single step: 8 two-qubit gates | **No two-qubit gates**: single-qubit rotations only |
| Built-in check | Count the excitations (catches loss) | Parity check X₁X₂ (catches some errors) |

[DERIVED] The intended two-register gate, the clean controlled-Z from 19.1, is then **one CZ between the two internal qubits**. That's six qubits and one entangling gate, small enough for today's cloud quantum computers.

[REPORTED] By contrast, copying the *uneven* interaction faithfully into a circuit took 36 two-qubit gates per time slice after optimization (130 before), and 2,304 for a full 64-slice gate. That cost reproduces the hardware's imperfection, not the intended logic.

[PROPOSED] Nobody has run either version on real hardware yet.

## Summary

- **Two rings interact through a level-dependent push.** Its average makes a clean CZ gate; its unevenness is an error.
- **Hopping ratios of 1, 2 and ½ let rings trade contents** at no energy cost. A ratio of 1.5 is safest.
- **Smooth sin² pulses** leak about ten thousand times less than abrupt ones in the same time.
- **The staggered-flip echo cancels steady hopping exactly,** even uneven or miscalibrated hopping, while the intended gate survives.
- **Three working instructions:** HOLD, ROTATE, COUPLE, chosen by RAMM.
- **The logic fits on six qubits and one CZ.** It can be tested on existing quantum computers, and hasn't been yet.

## Try it

1. Why is a hopping ratio of exactly 1 dangerous? *Answer: some register states then have the same energy as states outside the register, so the interaction can push the register out at no cost.*
2. Does the echo cancel a hopping strength that is 10% too large but steady? *Answer: yes, exactly, because the flip reverses every hop regardless of strength.*
3. Which instruction depends most on knowing the hopping strength accurately? *Answer: ROTATE.*
4. How many qubits does the compact encoding need for three rings? *Answer: nine.*


---
*(c) 2026 Tyler O'Bryan, where applicable. PhaseKeep Research. Text CC BY 4.0, code MIT. AI-assisted research, documentation and numerical analysis. Working draft.*
