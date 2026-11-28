# When Things Go Wrong

*A story of simulated failures, and the rules each one taught*

*Edition 04 working draft, research snapshot as of 28 November 2026.*


>
> **In plain words**
> [Volume 19](19-making-registers-talk.md) described the register when everything behaves. This volume is the opposite: a story of experiments, all in simulation, that went looking for trouble and found it. Each failure is kept, because each one taught a rule the hardware would have to obey. The rules at the end of this volume are the most practical results in Edition 04.


## 20.1 Why failures are results

A design that only works when everything is perfect isn't a design yet. So the research deliberately added imperfections:
- uneven atoms
- wrong hopping strengths
- drifting settings
- slow control pulses

Then it measured what broke. Edition 03 did the same for verification (Volumes 7 and 9). The habit carries on here.

Two numbers appear throughout:
- **Infidelity:** how far the actual operation is from the intended one, averaged over inputs.
- **Leakage:** how much of the register escapes its four allowed states, in the worst case.

They measure different failures. A register can stay entirely inside its states while doing the wrong thing.

## 20.2 One imperfection at a time

Start with one ring and one flaw: an atom whose energy is slightly off, a bond whose hopping is slightly too strong, or a bond with a small stray phase.

[SIMULATED] For all three, leakage grows as roughly **0.1 × (size of the flaw)²**, and **does not keep growing over time**. The hopping gap keeps it bounded, which is the protection [Volume 18](18-four-atom-ring.md) promised.

But one flaw behaves differently. A wrong **bond strength** changes the energy gap between the two standing waves. That makes the register's logical phase run at the wrong rate, and the error **accumulates**. [SIMULATED] A 1% bond error stays harmless over a short operation, but reaches an infidelity of about 2 × 10⁻³ over a longer one. The echo of [Volume 19](19-making-registers-talk.md) fixes exactly this, as long as the error is steady.

## 20.3 Two imperfections together

Next, combine flaws in the two-ring gate:
- a bond error ε
- an atom detuning δ
- interaction unevenness α (0 = perfectly even, 1 = as uneven as the side-by-side geometry)

The research mapped 180 combinations. [SIMULATED]

**The surprise was how strongly two isolated flaws were suppressed.** With the echo and smooth pulses, interaction unevenness on its own, and detuning on its own, each caused error growing as the **sixth power** of its size in the tested model. Halving either cut the error about 64-fold. (A steady bond error on its own was cancelled exactly by the echo, [Volume 19](19-making-registers-talk.md).) This is an observation about those two terms in this model, not about every possible imperfection.

**Combined, the protection weakens sharply.** A wrong bond strength together with an uneven interaction causes error growing only as the **square** of their product. The fitted rule:

  error ≈ 0.43 × (ε × α)²  (plus smaller terms)

That gives a practical budget for the combined term:

| Error you can tolerate | Largest allowed ε × α |
|---|---|
| 1 in 100 | 0.15 |
| 1 in 1,000 | 0.05 |
| 1 in 10,000 | 0.015 |
| 1 in 100,000 | 0.005 |

Two honest notes [SIMULATED]:
- **Two simpler error models failed.** Both were proposed in advance, both failed badly on held-out data, and both are kept on record.
- **The sixth-power suppression is a property of this model and this pulse sequence,** not a law of the architecture. Nobody has yet derived why it happens.

## 20.4 When settings drift

The echo cancels hopping that is wrong but **steady**. What if the hopping strength drifts while the gate runs?

[SIMULATED] With a 5% drift during one gate:

| How the hopping changes | Infidelity | Leakage |
|---|---|---|
| Not at all (a steady 5% error) | ~0 (exact cancellation) | ~0 |
| Slow steady ramp | 39% | 0.03% |
| A jump halfway through | 81–88% | tiny |
| Half an oscillation per echo half | 94% | tiny |
| Whole oscillations within each echo half | about 10⁻⁹ to 10⁻⁸ | tiny |

**Why** [DERIVED]: the echo cancels hopping only when **both halves contain the same total amount of it**. During a long gate, each half accumulates about 90 radians of hopping phase. So even a 1% mismatch between the halves leaves almost a radian of error.

>
> **Common mistake**
> **These errors are nearly invisible.** The register stays inside its allowed states (tiny leakage) while doing almost entirely the wrong thing. The checks of [Volume 21](21-checking-without-breaking-2.md) look for escapes from the allowed states, so they would report everything fine. Stability of the hopping *during* operations is therefore a hard requirement, not a refinement.


>
> **Go deeper (optional math)**
> "Equal total hopping in each half" is exact only when the drifting part has the same form as the hopping itself (a uniform rescaling), so that the Hamiltonians at different times commute. In the tested case the drift sat on one bond, so the condition is first-order: whole-oscillation drift left residuals around 10⁻⁹ to 10⁻⁸ rather than zero. [SIMULATED]


## 20.5 Real pulses take time

The echo's flip was assumed instantaneous. Real flips take time, and the hopping keeps running during them. During a flip, each ring behaves exactly like a two-level system pushed slightly off its intended axis. That is a classic problem with classic answers. [DERIVED]

[SIMULATED] At the **assumed** control strength (four times the weaker ring's hopping; hardware feasibility unverified):

| Flip | Result inside the gate |
|---|---|
| Simple square pulse | Fails: about 53% infidelity |
| Smooth pulse | Fails: about 40% |
| **Composite pulse** (four timed pushes, two forward and two reverse) | **Exact**, if the interaction is uniform or switched off during the flip |
| Composite pulse with the **uneven** interaction left on | 0.7% infidelity, 6.9% leakage |

The lesson: a control pulse designed in isolation can fail once the rest of the system is running. **The uneven interaction must be off, or the pulse designed together with it.** Composite pulses are also tuned to the expected hopping strength, which brings back a small sensitivity to bond errors (about 5 × 10⁻⁵ at 5%).

## 20.6 Where to put the flips

Moving the flips changes which kinds of drift cancel. [SIMULATED]

| Flip timing | Cancels | Blind to |
|---|---|---|
| Halfway (the original echo) | Steady errors, oscillations of ½ cycle per gate | Slow ramps, jumps, 1 cycle per gate |
| At ¼ and ¾ (symmetric echo) | Steady errors, slow ramps, midpoint jumps, 1 cycle per gate | ½ cycle per gate |
| Four flips | A broader range | Leaks more with uneven interactions |

Every arrangement has a blind spot. This is well known from a technique called dynamical decoupling, which echoes generalize. Here the best tested compromise is the symmetric echo, with the interaction pulsed separately in each segment. It is about 10 times worse than the original when nothing drifts (1.4 × 10⁻⁵ against 1.7 × 10⁻⁶), but around a thousand times better against slow drift.

## 20.7 The balance rule

One more idea seemed promising: keep the interaction on continuously, and only dip it ("notch" it) around each flip.

[SIMULATED] It didn't work.
- **What was tried:** 90 notch shapes, widths and depths.
- **What they gave:** all of them landed between 1.2 × 10⁻³ and 2.8 × 10⁻³.
- **The segmented approach:** 1.4 × 10⁻⁵.
- **Depth barely mattered.**

The failure was informative. [SIMULATED] A careful check showed the error growing as the *fourth* power of the unevenness, not the sixth. That is the observation. [PROPOSED] The explanation below fits the data, but has not yet been derived analytically or reproduced independently:
- **The shift:** the uneven interaction slightly shifts the register's energies.
- **Why it can cancel:** the shift reverses sign when the hopping reverses.
- **When it does cancel:** only if the interaction is, on average, **equally strong (squared) in both halves of the echo**.

| Interaction shape | Imbalance between halves | Infidelity |
|---|---|---|
| Separate smooth pulses per segment | 0 | 1.4 × 10⁻⁵ |
| Continuous, with notches | large (−0.95) | 1.8 × 10⁻³ |
| Flat-topped, with notches | smaller (−0.20) | 1.8 × 10⁻⁴ |
| Balanced, but with a steep notch | 0 | 4.2 × 10⁻⁴ (limited by leakage from the steep notch) |

Two cautions:
- **Balance is not sufficient on its own.** The balanced-but-steep notch still failed, through leakage.
- **Separate smooth pulses are the best tested compromise, not a proven optimum.** They are balanced, zero at every flip and gentle. Better shapes may exist; the planned joint optimization of pulses and interaction is meant to look for them.

## 20.8 What it all adds up to

Gathering the rules, each true **in these ideal models**:

1. **Budget errors together:** bond error × interaction unevenness ≲ 0.015 for errors of 1 in 10,000.
2. **Keep the hopping steady during operations:** the tested gate needs between-half stability of about 1 part in 10,000. This is the hardest requirement found, and the most hidden.
3. **Switch the uneven interaction off during flips,** make it uniform, or design the flips together with it.
4. **Use composite flips** at a control strength a few times the hopping (the tested value was assumed, not checked against hardware).
5. **Balance the interaction across the echo's halves,** with zeros at the flips and gentle ramps. Separate smooth pulses were the best tested way to do this.

None of these were known when the four-atom ring was first proposed. Every one came from something going wrong. They are what [Volume 22](22-which-machine.md) asks real hardware to meet.

## Summary

- **Isolated unevenness and detuning were strongly suppressed** in the tested model (sixth power). Combined flaws are much less so: the rule is ε × α ≲ 0.015.
- **Drifting hopping defeats the echo,** producing large, nearly invisible errors.
- **Composite flips work,** but only with the uneven interaction off or uniform.
- **Every echo timing has a blind spot.** Symmetric echoes handle slow drift best.
- **Balancing the interaction across the echo's halves** appears necessary but not sufficient in the tested shapes. Separate smooth pulses were the best tested compromise.

## Try it

1. Bond error 4%, unevenness 0.5. What error does the combined term predict? *Answer: 0.43 × (0.02)² ≈ 1.7 × 10⁻⁴.*
2. Why would a parity check miss the drift errors in 20.4? *Answer: the register stays inside its allowed states; the error is a wrong phase, not an escape.*
3. Which echo timing handles a slow ramp better, halfway or symmetric? *Answer: symmetric.*
4. Why did notches fail even at full depth? *Answer: the interaction was not balanced across the echo's halves, so the energy shift it causes didn't cancel.*


---
*(c) 2026 Tyler O'Bryan, where applicable. PhaseKeep Research. Text CC BY 4.0, code MIT. AI-assisted research, documentation and numerical analysis. Working draft.*
