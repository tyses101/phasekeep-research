# One Photon's Journey

*A single worked example from preparation to storage, with the numbers*


## What you will learn

This volume follows one photon through the whole PhaseKeep pipeline, using the numbers from earlier volumes. By the end you can see, in one place, which steps are well understood and which ones swallow most of the light.

>
> **Common mistake**
> **This is a worked illustration, not an experiment.** Every probability below comes from a model or an assumption in an earlier volume. The final "joint yield" is a simple product of two such numbers and assumes they are independent. Nothing here has been measured.


**Figure.** The five steps, with the key number for each. Red boxes are where the project is weakest.

*Picture description:* Five boxes in a row joined by arrows: Prepare, Transform, Interact, Check, Store. Under them: Prepare is proposed, Transform has had its closure checked, Interact has a modelled valid probability of 0.125, Check has no safe test yet and is marked unknown, and Store has a chain efficiency of 0.451 percent, below the 1.1146 percent threshold. A line underneath multiplies 0.125 by 0.00451 to give an illustrative joint yield of 0.056 percent, about one run in 1,800, with a note that this is an illustration and not a result.

## 12.1 The task

We have a photon in address **10** (vertical polarization, twist −1). We want to (1) change it with ordinary optics, (2) make it interact with a second photon, (3) decide whether the interaction worked, and (4) store the result.

## 12.2 Step 1: Prepare (Before)

The **Before** question ([Volume 7](07-buddy-checks.md)) is: what state, what resources, are they compatible? Here the state is the single address |V, −1⟩, prepared from a **known recipe**. Because the recipe is known, if this photon is lost we can simply make another [PROPOSED]. (The result of a later computation would not have that safety net; [Volume 2](02-quantum-states.md).)

## 12.3 Step 2: Transform (CT)

Pass the photon through a half-wave plate at 45° and then a mirror ([Volume 5](05-controlled-transformations.md)).

| After | Polarization | Twist | Address |
|---|---|---|---|
| Start | V | −1 | 10 |
| Half-wave plate | H | −1 | 00 |
| Mirror | H | +1 | 01 |

The plate also multiplies the state by −i, a global phase that cannot be observed on its own. Both devices keep the photon in the four addresses (closure, [Volume 5](05-controlled-transformations.md)) [DERIVED]. The program `tetragon.py` in the `code` folder checks this.

A blend behaves the same way. Take the edge blend (00 + 01)/√2 and rotate the image by π/4. The twist +1 part acquires a phase of −i relative to the twist −1 part, so the state becomes (00 − i·01)/√2 (up to a global phase and a sign convention). It is still separable, because independent single-axis operations cannot change that ([Volume 4](04-geometric-encoding.md)) [DERIVED].

Both operations here are **shared** ones: they act on the whole beam at once, which is the cheap kind ([Volume 4](04-geometric-encoding.md), A06) [SIMULATED].

## 12.4 Step 3: Interact (the heralded gate)

To make our photon interact with a second one, we use the heralded controlled-phase-flip gate of [Volume 6](06-two-photons.md), which needs two helper photons.

- The published gate's theoretical success rate is **1/8** [REPORTED].
- In our computer reconstruction, for inputs where the first register is in the top address and the second in a lower one, the three possibilities per attempt are [SIMULATED]:

| Outcome | Probability | Out of 1,000 attempts |
|---|---|---|
| Herald fires **and** output is valid | 0.125 | 125 |
| Herald fires but output is **not** valid (false herald) | 0.25 | 250 |
| No herald | 0.625 | 625 |

The herald fires 375 times, so the herald probability is 0.375. But only 125 of those 375 are valid, so the **reliability** is 125/375 = **1/3**, not 0.375 ([Volume 7](07-buddy-checks.md)).

## 12.5 Step 4: Buddy Check

Can we answer PASS, FAIL or UNKNOWN for the specific photon in our hands?

- **Not PASS.** The herald is right only one time in three here, and we have no safe way to confirm the output without destroying it (audit items A03 and A04, [Volume 9](09-research-lab.md)).
- **Not FAIL.** We have no evidence that this particular photon is bad.
- So the honest answer is **UNKNOWN**. A system that continued on UNKNOWN would be continuing on hope.

## 12.6 Step 5: Store

To store the photon, the memory chain must return it with enough efficiency to beat the classical bound ([Volume 8](08-memory-and-loss.md)). With the supplied example chain:

```
internal 4 %  ×  converters 0.49  ×  filter 23 %  =  0.451 %
```

The threshold for the test at n̄ = 0.25 is **1.1146 %**. The chain is below it, so this memory would **fail** the certification even before noise [DERIVED] arithmetic on supplied numbers.

## 12.7 The total

Per attempt, the chance of a valid interaction (0.125) times the chance of the photon surviving the memory chain (0.00451) gives 0.000564, about **0.056 %**, or roughly one run in 1,800 [DERIVED] arithmetic. This multiplies two numbers as if they were independent, and ignores everything else (preparation, detection, the second photon's own losses).

What would change it? Try better memory inputs: an internal efficiency of 12.6 % and a filter of 90 %, with converters 0.49, give an overall efficiency of 5.557 % (this row passes the threshold with margin +0.0975). The same product then gives 0.125 × 0.05557 = 0.69 %, about one run in 144. The memory chain, not the optics, dominates the loss.

| Case | Memory efficiency | Joint yield | One run in |
|---|---|---|---|
| Supplied example chain | 0.451 % | 0.056 % | about 1,800 |
| Better internal efficiency and filter | 5.557 % | 0.69 % | about 144 |

## 12.8 What the balance sheet looks like

| Step | What we know | Evidence |
|---|---|---|
| Prepare | Known recipes can be remade; PhaseKeep build not done | [PROPOSED] |
| Transform | Closure of waveplate, mirror and rotation | [DERIVED] |
| Interact | Published gate works at 1/8 with post-selection; our model's herald is 1/3 reliable at worst | [REPORTED], [SIMULATED] |
| Check | No safe nondestructive test yet | [BLOCKED] |
| Store | Supplied chain fails the threshold; better chains pass on paper | [DERIVED] on [ASSUMED] inputs |

>
> **Evidence status**
> **Evidence status.** All numbers are in the Ledger ([Appendix 2](A2-ledger.md)). Nothing in this volume is [MEASURED].


## Try it

1. In 12.3, what address results if you swap the order: mirror first, then the half-wave plate? (Same result: 01. The two operations act on different axes and commute.)
2. With 5,000 attempts, how many valid outputs, heralds and false heralds do you expect? (625, 1,875 and 1,250.)
3. Which factor in the 12.7 product has the most room to grow? (The memory efficiency: it could in principle rise about 220-fold, from 0.451 % to 100 %, while the gate's valid probability could rise at most 8-fold, from 0.125 to 1.)

## Summary

>
> **Key idea**
> The optics that change a photon are well understood and cheap. The costs are in making photons interact (1 in 8, with false signals) and in storing the result (a chain that loses most of the light). The Buddy Check says UNKNOWN because we cannot yet verify the output without destroying it.



---
*(c) 2026 Tyler O'Bryan, where applicable. PhaseKeep Research. Text CC BY 4.0, code MIT. AI-assisted research, documentation and numerical analysis. Draft for technical review.*
