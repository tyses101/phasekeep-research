# States, Measurement and Why Reading Is Hard

*Superposition, amplitudes, phase, fidelity, and the no-cloning rule*


## What you will learn

What a quantum state is, why "blend" is not a joke, why one measurement cannot reveal an unknown state, and why that last fact matters for everything that follows.

## 2.1 One photon, many possibilities

Ask a photon with polarization H which way it is polarized and it says H, every time. Ask a photon in V, and it says V. Quantum physics allows something else: a photon whose polarization is a **blend** of H and V. This is called a **superposition**.

A blend is not "H or V but we do not know which". Experiments show that the two possibilities can interfere with each other, the way two ripples on a pond combine. So the blend is a real thing with its own properties.

## 2.2 Amplitudes and probabilities

We describe the blend with two numbers, called **amplitudes**, one for each possibility. Write the state as

```
state = a × H + b × V
```

The chance of finding H when you measure is the square of the size of a, and the chance of finding V is the square of the size of b. These chances add to one.

>
> **In plain words**
> Example: a = b = 0.7071. Each chance is 0.7071² = 0.5. A measurement gives H half the time and V half the time. The photon was not secretly one or the other beforehand; the blend itself has this 50/50 property.


## 2.3 Phase: the part people forget

Amplitudes can be negative or even complex. Two blends with the same probabilities can still be *different states*:

- (H + V) / √2
- (H − V) / √2

Measuring H or V gives 50/50 for both. But a different measurement (diagonal polarization) tells them apart perfectly. The sign is called the **relative phase**, and it is the very thing that quantum memories and quantum gates must preserve.

>
> **Key idea**
> Probabilities tell you only part of a state. The relative phases between the amplitudes are equally real, and they are the first thing noise destroys.


## 2.4 One measurement cannot reveal an unknown state

If someone hands you a photon in an unknown blend and you measure it, you get one result (H or V). The blend is gone. You learn a single bit about a state that needed more numbers to describe. Repeating the measurement on the *same* photon does not help, because after the first measurement the photon is no longer in the blend.

To learn an unknown state you would need many identical copies. But there is a theorem, the **no-cloning theorem**, that says you cannot make perfect copies of an unknown quantum state. So an unknown state cannot be "backed up" the way a computer file can.

>
> **Common mistake**
> **Common mistake.** "Four outcomes means four bits." Four addresses (as in [Volume 3](03-encoding-axies.md)) return only two bits of ordinary information when read out, and a single reading returns just one address. The *state* (all the amplitudes and phases together) is richer than any one reading, but you cannot read it all out in one go.


This matters in two ways later in the library:

1. A **known recipe** can be rebuilt. If we know how a state was prepared, we can prepare it again from scratch.
2. An **unknown state** that was the result of a computation cannot be re-made if lost. This is why keeping it alive (memory, [Volume 8](08-memory-and-loss.md)) and checking it without destroying it (Buddy Checks, [Volume 7](07-buddy-checks.md)) are central problems.

## 2.5 A four-level system

One photon with two polarizations and two twists can be in a blend of four addresses. We write its state as

```
state = a|00⟩ + b|01⟩ + c|10⟩ + d|11⟩
```

where the squared sizes of a, b, c, d add to one. [Volume 3](03-encoding-axies.md) says what each address means. Here we only need the counting.

**Figure.** The four addresses as the corners of a square: horizontal edges change the twist, vertical edges change the polarization.

*Picture description:* A square with four corners. Top left 00 is horizontal polarization with twist minus one. Top right 01 is horizontal with twist plus one. Bottom left 10 is vertical with twist minus one. Bottom right 11 is vertical with twist plus one. The horizontal edges flip the twist, the vertical edges flip polarization. Corners 00 and 11 differ in both properties, as do 01 and 10.

>
> **Go deeper (optional math)**
> A pure state of a d-level system has d complex amplitudes. Normalization removes one real number and the unobservable global phase removes another, so it takes **2d − 2 real parameters** to specify it [DERIVED]. For d = 2 that is 2 (the two angles on a sphere), for d = 4 it is 6.


## 2.6 How good can a classical copy be?

Suppose a state is chosen at random and handed to you once. You measure it, then build a new photon from your result. How closely does the new photon match the original, on average? For random pure states in d dimensions the best average match, called fidelity, from this measure-and-rebuild approach is **2/(d+1)** [DERIVED] (a standard result). For d = 2 it is 2/3. For our d = 4 it is **2/5 = 0.40**.

So a quantum memory that returns a hidden random four-address state with fidelity above 0.40 is doing something a classical measure-and-resend device cannot. Different tests use different benchmarks, and [Volume 8](08-memory-and-loss.md) explains why we keep them apart.

>
> **Try it**
> Check the formula. For d = 2, the benchmark is 2/(2+1). What is it? (2/3, about 0.667.) For d = 4? (2/5 = 0.40.) What happens as d grows? (The benchmark falls toward zero, so a larger system is easier to certify as "nonclassical" but harder to build.)


## 2.7 What "fidelity" means

Fidelity is a score from 0 to 1 for how close one quantum state is to another. 1 means identical. A fidelity of 0.9 does not mean "90% of photons survive"; survival and state quality are separate numbers, and mixing them up is one of the most common errors in the field. We report them separately everywhere in this library.

>
> **Evidence status**
> **Evidence status.** Superposition, amplitude, phase, no-cloning, parameter count and the 2/(d+1) benchmark: standard results [DERIVED]. The four-address labelling is our convention. No PhaseKeep measurement of any of this exists [MEASURED] is none yet.


## Try it

1. A photon is in the state (H + V)/√2. What is the probability of measuring V? (0.5.)
2. Two blends: (H + V)/√2 and (H − V)/√2. Can a single H-or-V measurement tell them apart? (No. Both give 50/50.)
3. A friend says "I will just measure your photon and send you a copy." For a random 4-level state, what fidelity can the copy reach on average? (0.40.)

## Summary

>
> **Key idea**
> A quantum state is a list of amplitudes with phases. One measurement gives only one outcome and destroys the blend. An unknown state cannot be copied. Everything PhaseKeep does has to keep the amplitudes and the phases intact.



---
*(c) 2026 Tyler O'Bryan, where applicable. PhaseKeep Research. Text CC BY 4.0, code MIT. AI-assisted research, documentation and numerical analysis. Draft for technical review.*
