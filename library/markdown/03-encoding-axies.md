# Encoding Axies and the Tetragon

*How a single photon carries four addresses*


## What you will learn

What an **Encoding Axis** is, how two of them make a four-address photon (the Tetragon), and what the word "address" does and does not mean.

## 3.1 What is an Encoding Axis?

An **Encoding Axis (EA)** is one physical property of light that we choose to carry a label, where the possible values are clearly distinguishable. (The plural is written **Axies** in the project's own spelling; "Axes" is the same word.)

Polarization is an EA with two values, H and V. Twist is an EA with two values, −1 and +1. Other properties of light could in principle be EAs too: which path the photon takes, its color (frequency), or the radial shape of its beam. Those are *candidates*, not adopted.

>
> **Key idea**
> **Time is not an EA here.** Time is the machine's clock: it tells us *when* a photon arrives. We do not use it as a label in the current design. An earlier memory model used four time slots as the label ([Volume 8](08-memory-and-loss.md)); the ORCA memory paper's abstract reports storing and retrieving four independent time-bin modes. The current design treats time as external. This library does not record why that choice was made.


## 3.2 The Tetragon: two axes, four addresses

The Tetragon (formal name PK-Q4) combines polarization (H/V) with twist (−1/+1).

| Address | Polarization | Twist |
|---|---|---|
| 00 | H | −1 |
| 01 | H | +1 |
| 10 | V | −1 |
| 11 | V | +1 |

Read each address as two binary digits: the first says polarization (0 is H, 1 is V), the second says twist (0 is −1, 1 is +1).

**Figure.** The Tetragon. Moving sideways changes the twist; moving up or down changes the polarization; moving corner to corner changes both.

*Picture description:* A square with four corners. Top left 00 is horizontal polarization with twist minus one. Top right 01 is horizontal with twist plus one. Bottom left 10 is vertical with twist minus one. Bottom right 11 is vertical with twist plus one. The horizontal edges flip the twist, the vertical edges flip polarization. Corners 00 and 11 differ in both properties, as do 01 and 10.

## 3.3 A state, not just an address

One photon is not forced to sit on one corner. It can be in a blend of all four:

```
a|00⟩ + b|01⟩ + c|10⟩ + d|11⟩
```

with the squared sizes of a, b, c, d adding to one, and with phases that matter ([Volume 2](02-quantum-states.md)). Measuring it returns one address with probability |a|², |b|², |c|² or |d|².

>
> **In plain words**
> **Two kinds of blend.** A blend of two addresses on one *edge* of the square, such as 00 + 01, can be written as one polarization times one twist blend. A blend across a *diagonal*, such as 00 + 11, cannot: its polarization and twist are tied together. [Volume 4](04-geometric-encoding.md) explains why that matters.


>
> **Common mistake**
> **An address is not a bit-string you can read in full.** One detection gives one address. The blend, with all its phases, is only available as long as the photon is not measured.


## 3.4 Why bother with a second axis?

Compare the options for a single photon:

| Encoding | Distinct addresses | Comment |
|---|---|---|
| Polarization only | 2 | Simple and robust. Standard qubit. |
| Polarization × twist ±1 | 4 | The Tetragon. Needs twist devices. |
| Four time slots | 4 | Used in earlier memory modelling; not part of the current design. |

The attraction is more states per photon without needing more photons, and the fact that polarization and twist can be changed independently by different devices. The price is that twist devices are less mature than polarization ones.

## 3.5 What can go wrong

- **Crosstalk**: a twist sorter sends some of the −1 light to the +1 output, and the reverse.
- **Loss**: each device loses some light, and high-twist beams are harder to pass through small optics.
- **Closure**: a device that was meant to flip −1 and +1 might also push light into twist 0 or +3. A device is useful only if it keeps the photon inside the four addresses ("closure"). In [Volume 5](05-controlled-transformations.md) we check this device by device.

>
> **Go deeper (optional math)**
> Single-photon benchmarks are also affected by the axis count. Because the number of levels d = 4, the best classical measure-and-resend fidelity for hidden random states is 2/(d+1) = 0.40 [DERIVED]. A memory test using only a known set of coherent states uses a different benchmark, 0.482253 at mean photon number 0.25 [DERIVED]; [Volume 8](08-memory-and-loss.md) explains why these are separate tests.


## 3.6 Naming: Axies, Axes, and the family

PhaseKeep names registers by how many binary labels they use. The Tetragon uses two. Adding more axes gives larger registers; [Volume 4](04-geometric-encoding.md) names them. The names are labels for *mathematical structures*. They do not say that the hardware exists.

>
> **Evidence status**
> **Evidence status.** The four-address basis is a convention [DERIVED]. Preparing and characterizing the *complete* Tetragon on a PhaseKeep bench: [PROPOSED]; audit item A02 ([Volume 9](09-research-lab.md)). "Time as an external clock" is a design choice [PROPOSED].


## Try it

1. Which address is V with twist −1? (10.)
2. Which two addresses differ in *both* properties? (00 and 11, or 01 and 10.)
3. A device flips only the twist. Which address does 01 become? (00.)
4. A device flips both. Which address does 10 become? (01.)

## Summary

>
> **Key idea**
> An EA is a distinguishable property of light used as a label. The Tetragon uses two EAs, polarization and twist, giving four addresses. A state is a blend over the addresses; reading returns one address.



---
*(c) 2026 Tyler O'Bryan, where applicable. PhaseKeep Research. Text CC BY 4.0, code MIT. AI-assisted research, documentation and numerical analysis. Draft for technical review.*
