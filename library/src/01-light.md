# Volume 1: Light as Information

## What you will learn

By the end of this volume you can say what a photon is, what polarization is, what a "twist" of light is, and why a single photon can carry a small label made from both. No math is needed for the main text.

## 1.1 The photon

Light comes in the smallest possible pieces called **photons**. A dim laser beam is a stream of them. A single-photon source delivers them one at a time. One photon cannot be split in half by ordinary optics: it goes one way or the other, or, as Volume 2 explains, it can be in a *blend* of ways until it is measured.

::: plain
A photon is one indivisible packet of light. We care about it because it can carry a label (what we call *information*) in the shape of its wave, and it travels fast and far with little disturbance.
:::

## 1.2 Light is a wave, too

The same photon behaves like a wave. A wave has a direction it travels, a size (brightness, which for one photon means the *probability* of finding it), and a **shape** across the beam. Two shape properties matter here: which way the wave wiggles (polarization) and how its wavefront is arranged around the beam axis (twist).

## 1.3 Polarization: which way the light wiggles

Light wiggles sideways to its direction of travel. If it wiggles up and down it is **vertically polarized (V)**. If it wiggles left and right it is **horizontally polarized (H)**. Polarized sunglasses block one of these.

{{fig:polarization|The two basic polarizations, H and V, and the diagonal blends of them.}}

Two points make polarization useful as a label:

- H and V are completely distinguishable. A **polarizing beam splitter** sends H one way and V the other, so one measurement tells them apart.
- A **waveplate** (a slice of special crystal) changes polarization on purpose. A **half-wave plate** set at 45 degrees swaps H and V. That is a controlled, repeatable change and it is cheap, mature technology.

::: deeper
A half-wave plate at 45 degrees acts on the polarization qubit as the matrix −iX, where X swaps H and V. The factor −i is a global phase when the plate acts alone, which cannot be observed, but it matters if the operation is applied to only part of a larger superposition. We checked this closure: two quarter-wave plates in a row make one half-wave plate [[DERIVED]].
:::

## 1.4 Twist: orbital angular momentum

Most laser beams have a flat wavefront like a sheet of paper. A beam can instead have a wavefront shaped like a spiral staircase or a corkscrew going around the beam axis. Such a beam has **orbital angular momentum (OAM)**, and its twist number is written ℓ (the Greek letter *ell*, a whole number such as −1, 0, +1).

- ℓ = 0 is the ordinary flat beam.
- ℓ = +1 goes once around the axis, one way, per wavelength travelled.
- ℓ = −1 goes once around, the other way.
- A beam with ℓ ≠ 0 has a dark spot at the center, so its cross-section looks like a doughnut.

{{fig:oam|Twist numbers −1, 0 and +1. The twist changes how the wave phase advances around the beam axis; the doughnut shape appears when ℓ is not zero.}}

::: deeper
An ideal OAM mode has angular dependence exp(iℓφ), where φ is the angle around the axis, and carries orbital angular momentum ℓℏ per photon [[DERIVED]]. The common practical family is the Laguerre-Gaussian modes. With radial index p = 0 and an aperture of radius R, the fraction of power passing through is the regularized gamma function P(|ℓ|+1, 2R²/w²) for beam size w, which is what the A06 simulation used [[DERIVED]]; the aperture effect is why larger |ℓ| beams are harder to handle in small optics.
:::

Why use ℓ = −1 and ℓ = +1 for the label? They are mirror images of each other. They are the simplest pair of twisted beams that are each other's opposites. A mirror flips one into the other with a single reflection (ℓ becomes −ℓ), and the pair stays closed under that flip, which is a useful property for a four-address register.

::: watch
**Twist is not spin.** Polarization is sometimes called *spin* angular momentum of light. OAM is about the beam's spatial shape. They are separate properties, which is exactly why they can be combined. The one place they can be linked is a device called a q-plate, which ties them together. In this library the Tetragon treats them as two independent labels.
:::

## 1.5 Two labels on one photon

Polarization has two options (H or V). Twist, as we use it, has two options (−1 or +1). A photon can carry both at once, giving 2 × 2 = **4 combinations**. That is the idea behind the four-address photon introduced in Volume 3.

## 1.6 How you read a label

| Property | A typical way to read it | How clean is it |
|---|---|---|
| Polarization H/V | Polarizing beam splitter, then two detectors | Very clean; standard |
| Twist −1/+1 | A mode sorter, or a hologram or q-plate that converts twist to a spatial position | Works in labs; each method has loss and crosstalk |

::: evidence
**Evidence status.** Polarization and OAM definitions, and the half-wave-plate and mirror facts: [[DERIVED]] and standard physics. Which sorter PhaseKeep would use is [[PROPOSED]] and is audit item A02 in Volume 9. The sorter used in our computer model is illustrative only [[ASSUMED]]; published sorters are different devices.
:::

## Try it

1. A beam is in state V. You pass it through a half-wave plate at 45 degrees. What do you get? (Answer: H.)
2. A photon has twist +1. It reflects off one mirror. What twist does it have? (Answer: −1.)
3. How many different labels can a photon carry if it uses polarization only? Polarization plus twist (±1)? (Answer: 2, then 4.)

## Summary

::: key
A photon can carry a polarization label (H or V) and a twist label (−1 or +1) at the same time. Both can be changed with ordinary optics, and both can be read out. Together they give four addresses.
:::
