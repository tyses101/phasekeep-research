# Light's Many Handles

::: plain
A photon offers several properties that can carry information. This volume separates them clearly:
- the momentum that carries it forward
- the spin we see as polarization
- the twist of its wavefront

Then it asks a practical question: when the outside world disturbs the light, which combinations of properties survive? The answer is the most important idea in this volume. **Stability is not a property of a state on its own. It depends on which disturbance you are facing.**
:::

## 16.1 One photon, three kinds of momentum

Light pushes. A photon carries momentum even though it has no mass. That momentum has three faces:

| Kind | What it describes | What you see |
|---|---|---|
| **Linear momentum** | Motion forward | Wavelength and direction of travel |
| **Spin angular momentum** | Rotation of the electric field | Circular polarization (left or right) |
| **Orbital angular momentum (OAM)** | Twist of the wavefront around the beam axis | A corkscrew wavefront and a doughnut-shaped beam |

Linear momentum depends only on wavelength: p = h/λ. [[DERIVED]] For visible light:

| Colour | Wavelength | Frequency | Photon energy | Momentum (kg·m/s) |
|---|---|---|---|---|
| Red | 650 nm | 461 THz | 1.91 eV | 1.02 × 10⁻²⁷ |
| Green | 532 nm | 564 THz | 2.33 eV | 1.25 × 10⁻²⁷ |
| Blue | 450 nm | 666 THz | 2.76 eV | 1.47 × 10⁻²⁷ |

Shorter wavelength means more momentum, but **not more speed**: in empty space light always travels at the same speed.

::: watch
**The wave does not come from the twist.** An ordinary beam with no twist is just as much a wave. OAM is not a separate engine inside the photon. It describes how the forward flow of momentum *circulates* around the axis. On a twisted wavefront the momentum at each point is tilted slightly sideways, and that sideways part adds up to an angular momentum of ℓħ per photon, where ℓ is the twist number. **Polarization does not create the twist either.** Circularly polarized light can have a flat wavefront, and twisted light can be linearly polarized.
:::

## 16.2 Families and axes

It is tempting to list every property as a separate "axis". But several of them are different descriptions of the same underlying freedom. Light really has three physical **families** [[DERIVED]]:

| Family | Different ways to describe it |
|---|---|
| **Polarization** | horizontal / vertical, circular left / right, any ellipse |
| **Spatial** | twist (OAM), ring structure (radial modes), path, position, sideways momentum |
| **Spectral–temporal** | frequency (colour), arrival time, pulse shape |

Choosing twist rather than path, for example, is often a choice of **basis** within the spatial family. That is the question Edition 03 called High-Dimensional Orthogonal Configurations (HDOC).

But a family can still hold **several independent encoding axes**. A photon could take one of two paths and, on each path, one of two twists: two binary axes from one family. The distinction to keep is:
- **physical family:** what nature provides
- **engineered encoding axis:** what we build from it, and must be able to control independently

## 16.3 Seeing a twist

A twisted beam has a dark centre: the phase spirals around a point where it is undefined, so the light must vanish there. Twists of **+1 and −1 produce the same doughnut of light**. A camera cannot tell them apart. Distinguishing them needs a phase-sensitive measurement: interference with a reference beam, a hologram or a mode sorter.

This matters for any register that stores information in the sign of the twist: reading it out is harder than looking.

## 16.4 Twins under focusing: the Gouy phase

When a beam is focused, it picks up an extra phase, called the **Gouy phase**, that depends on the beam's shape. For the standard family of twisted beams, the amount depends on 2p + |ℓ| + 1, where ℓ is the twist and p counts rings. [[DERIVED]] Because only the *size* of the twist enters, **+1 and −1 get exactly the same Gouy phase**, as long as their ring structure and beam parameters match. A superposition of +1 and −1 therefore does not drift during ideal focusing. A superposition of 0 and +1 would.

This is a real, but narrow, protection: it covers one mechanism, under matched conditions. It says nothing about turbulence, misalignment or other disturbances.

## 16.5 Rotations, and a combination that ignores them

Now rotate the whole beam about its axis by an angle θ. A twist of ℓ picks up a phase of ℓθ, so:

| Combination | Relative phase after rotation by θ |
|---|---|
| Twist +1 and −1 | 2θ |
| Twist +2 and −2 | 4θ |
| Twist 0 and +1 | θ |
| Circular polarization left and right | 2θ |

[[DERIVED]] Bigger twists are *more* sensitive to rotation. Polarization behaves like a twist of ±1, which makes sense: both are angular momentum.

Here is the elegant part. Spin and twist can be paired so that their angular momenta **cancel**: left-circular light with twist −1, and right-circular light with twist +1. Both carry *zero* total angular momentum along the beam. A rotation multiplies each by the same phase factor (one), so **any superposition of the two is unchanged by rotation of the whole beam**. That's whatever the angle. [[DERIVED]]

::: watch
This protection is **specific to rotation**. The same pair is *not* protected against birefringence (a material that slows one polarization more than another). That disturbance acts on polarization alone, and it scrambles the pair. **"Protected" always needs a "against what".**
:::

::: deeper
The general rule: a set of states is protected against a disturbance exactly when the disturbance acts on all of them by the same phase. That means they sit in one eigenspace of the disturbance's generator. For rotation the generator is the total angular momentum J = S + L, and the pair above has J = 0. Such sets are called decoherence-free subspaces in the literature. [[UNVERIFIED]] Hybrid spin–orbit states of this kind have been used for alignment-free quantum communication (reference to be checked; Appendix 9).
:::

## 16.6 A device that converts spin into twist

A **q-plate** is a patterned optical element that changes a photon's twist depending on its circular polarization. Left becomes right while gaining twist, and right becomes left while losing it. [[REPORTED]] Spin-to-orbital angular momentum conversion of this kind has been demonstrated (Marrucci, Manzo and Paparo, 2006; abstract level).

Two lessons [[DERIVED]]:
- **It generates the zero-angular-momentum pair.** Sending in horizontally polarized, untwisted light produces exactly the pair from 16.5. So a q-plate can *encode* a polarization qubit into the rotation-proof pair, and a second one can decode it.
- **It is not a closed gate on twists ±1.** Applied to a photon already twisted +1, it can give +2, which leaves a register built on ±1. Flipping a twist *within* ±1 needs a different element, such as an interferometer containing an image-rotating prism.

## 16.7 The principle: stability depends on the disturbance

Put together, these examples give one principle that runs through the rest of this edition:

| Configuration | Protected against | Not protected against |
|---|---|---|
| Twist ±1 pair | Gouy phase (matched beams) | Rotation (2θ), astigmatism |
| Spin–twist pair with J = 0 | Rotation of the whole beam | Birefringence |
| Horizontal / vertical polarization | Gouy phase | Rotation mixes them |

Rather than building checks that fight the physics, we can **choose configurations whose natural behaviour already preserves the information**, for the disturbances they will actually meet. Then we check for whatever is left. Volume 17 shows the same idea appearing in atoms.

## Summary

- **A photon has three kinds of momentum:** linear (forward), spin (polarization), orbital (twist). The wave exists without the twist.
- **Light has three physical families of properties.** Engineered encoding axes are built from them and must be independently controllable.
- **Twists ±1 look identical in brightness,** and share their focusing phase. Rotation still separates them.
- **Pairing spin and twist so their angular momenta cancel** gives a combination unchanged by rotation, but not by birefringence.
- **Stability always depends on the disturbance.**

## Try it

1. What relative phase do twists +3 and −3 pick up under a rotation by θ? *Answer: 6θ.*
2. Which pair, twist ±1 or twist 0 and +1, shares its Gouy phase under matched focusing? *Answer: twist ±1, because both have |ℓ| = 1.*
3. Which two spin–twist combinations have zero total angular momentum, taking left-circular as spin +1? *Answer: left-circular with twist −1, and right-circular with twist +1.*
4. Why can't a camera tell twist +1 from −1? *Answer: their intensity patterns are identical; only the phase differs.*
