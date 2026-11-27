# Intelligent Registers

*A controller that composes only operations we can support*


## What you will learn

What a *register* is, three descriptive forms of register, and how a classical controller could pick the best supported sequence of operations. This volume is the most speculative in the series; everything here is [PROPOSED].

## 10.1 What a register is

A **register** is an information-bearing system with a defined set of states. PhaseKeep describes three forms. They are descriptions, not three new devices.

| Form | Meaning |
|---|---|
| **Binary Register** | A two-state encoding baseline. A coherent quantum version is a qubit; an ordinary classical bit is not a qubit. |
| **Structured Register** | A fixed encoding arrangement, such as the four-state Tetragon. |
| **Adaptive Register** | A register whose logical mapping or physical encoding can be selected or reconfigured within supported capabilities. |

>
> **Common mistake**
> **Simpler is not worse.** A binary register is not inherently inferior. Choose the smallest representation that meets the goal. Several binary registers can also together form a larger system.


## 10.1b What a register description should record

Beyond the number of states, a register specification could list the properties the compiler needs [PROPOSED]: the EA contents, the address geometry, the state dimension, **separability** (can the axes be treated independently?), closure, symmetry (chances for a shared operation), the coherence requirements (which phases must survive) and physical compatibility (which parts can do the operation). The full table is in [Volume 4](04-geometric-encoding.md), section 4.9.

The compiler can learn these from a known preparation record and from the mathematical description of the state. It cannot inspect an unknown photon and read them off.

## 10.2 Intelligent compilation

A classical **controller** (an ordinary computer) is given three things: a mathematical goal, a description of the register, and a *characterized* library of parts (parts whose behaviour has been measured). It then picks an EA mapping and a sequence of CT operations. It must

- preserve the intended calculation, including relative phases,
- count the cost of preparation, routing, readout and calibration.

Example: swapping H and V on the Tetragon can use one half-wave plate. But a swap applied *only to one twist* needs a different operation. The compiler cannot quietly replace the second by the first.

## 10.3 Intelligent execution

1. Establish the intended logical operation and the accuracy required.
2. Choose a supported register configuration and physical route.
3. Check closure, compatibility, resources and expected loss.
4. Configure and run the characterized CT operations.
5. Use the available Buddy Checks to continue, retry where physically allowed, or stop.

Preparation records and equipment readings can guide adaptation today. Trustworthy live certification of a quantum state is a separate, unresolved problem (A04). A failed operation on an unknown state cannot necessarily be undone or retried.

## 10.4 A useful objective for the compiler

For each candidate sequence estimate: probability of useful completion, error, resource cost and delay. Compare *only* sequences that do the same logical task. Use measured data when it exists, and label modelled inputs [ASSUMED]. **Reject** unsupported operations rather than inventing a mechanism for them.

## 10.5 State space and the environment around it

Two ideas are easy to run together, so we separate them.

- The **State Space (SS)** is the mathematical space of every available quantum state: the four addresses of the Tetragon *and* every coherent combination of them, with its amplitudes, phases and correlations. It says what information *can exist*.
- The **State Space Environment (SSE)** is the physical resources and control that make that space accessible and useful. It says what the information *can do*, and unlike the abstract space it has losses, costs and timing.

In the vocabulary of [Volume 4](04-geometric-encoding.md), the SS is the address geometry plus the state-space geometry (both mathematical). The SSE is the optical-mode geometry plus the execution geometry (both physical), together with the controller. It is a name for the whole stack seen together, not a new subsystem or pillar [PROPOSED].

Three things can be changed during a computation: **occupation** (which addresses carry amplitude), **connectivity** (which addresses the machinery can couple coherently) and **correlation** (how the encoded properties, amplitudes and phases relate). They are distinct, though changing one can affect the others [PROPOSED].

Three kinds of address set can also differ inside one environment: the addresses that are **available**, the addresses **active** in the current state (its support), and the relationships the physical devices can actually **operate** on. A register could have eight available addresses, four active ones and a transformation that acts on only two of them. Closure ([Volume 5](05-controlled-transformations.md)) is the question of whether the operations stay inside the available set.

>
> **Common mistake**
> **Compare with the right thing.** Against classical computing, configurable multilevel subspaces and encoding-aware compilation look new. Against quantum computing they are not: qudit encodings, subspace encodings, quantum control and hardware-aware compilation already exist. Any PhaseKeep contribution is in how these are combined for photons, not in inventing them.


## 10.6 Three corrections when reading the drawings

Pictures of squares, lines and triangles are useful, but three points keep them honest. They apply whenever the active set of addresses changes during a computation.

1. **The shape alone is not the state.** The state (00 + 01 + 10 + 11)/2 and the state (00 + 01 + 10 − 11)/2 occupy the same four addresses and give the same measurement probabilities (0.25 each). Yet the first is separable (Schmidt weights 1 and 0) and the second is maximally non-separable (0.5 and 0.5). One sign changes the correlation structure without changing the picture [DERIVED]. A description must therefore record amplitudes and phases, not just which vertices are occupied.
2. **Occupied vertices are a set, not a shape of edges.** Three occupied addresses are sometimes drawn as a triangle. But the square and cube graphs have no triangles: any two of three addresses on a square include a diagonal pair. The "triangle" is a *group of addresses* [DERIVED].
3. **An unknown state cannot simply be squeezed.** A reversible operation cannot concentrate an unknown four-address state into two addresses, because that would lose information. Contraction works only for a *known class* of states, or when the information is kept elsewhere. Dropping an occupied address by measuring or filtering is a loss [DERIVED].

A related fact, checked by `tetragon.py` and set as an exercise in [Volume 14](14-workbook.md): rotations in lines that share an address generally do **not commute**, so the order of operations matters, while rotations in disjoint lines do commute [DERIVED].

## 10.7 Capability versus cost

The photon already has superposition, interference, phase and correlation. Geometry creates none of them. What a good arrangement might change is the *cost* of a task: two encodings with the same number of states can differ in the parts, loss and error needed for the same operation. A06 tested one narrow case of this ([Volume 4](04-geometric-encoding.md), section 4.6). Whether the idea holds more widely is a hypothesis [PROPOSED], and the test is to compare two encodings of the same size on the same task, counting parts, loss and error.

>
> **Common mistake**
> **Capability versus cost.** A register's computational *capability* is set by the operations it can reach, not by how its states are drawn. A geometric arrangement can only change the *cost* of an operation. Describing the evolution of a state as "a geometric operation" restates ordinary quantum evolution. A claimed advantage would have to be shown as a lower measured cost, and none has been.


## 10.8 What this does not claim

- It does not claim a speedup. A classical controller choosing among the same operations establishes no advantage by itself, and geometric descriptions change cost, not capability.
- It has not been built. Live adaptive quantum execution has not been demonstrated by PhaseKeep.
- The only simulation relevant to it is the narrow A06 comparison of shared versus individual operations [SIMULATED].

>
> **Evidence status**
> **Evidence status.** Adaptive register, intelligent compilation and the State Space Environment as a name for the stack: [PROPOSED]. The state examples in 10.6 and the non-commuting rotations: [DERIVED]. A06: [SIMULATED] with [ASSUMED] inputs. [MEASURED]: none.


## Try it

Compare a two-state polarization register with a Tetragon for a task that only needs a polarization swap. Which is better? (The simpler one, if no twist information is needed. But if the twist carries information that matters, throwing it away is not a valid shortcut.)

## Summary

>
> **Key idea**
> An adaptive register would let a controller choose how to encode and which supported operations to apply. Describing operations through lines, faces and shared structure may make them cheaper to compile, but it changes cost, not capability. It is an idea, not a demonstration, and it must reject operations that nothing can support.



---
*(c) 2026 Tyler O'Bryan, where applicable. PhaseKeep Research. Text CC BY 4.0, code MIT. AI-assisted research, documentation and numerical analysis. Draft for technical review.*
