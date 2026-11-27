# Memory, Loss and Survival

*Why almost every number in this project is a loss number*


## What you will learn

Why almost every number in this project is a **loss** number, how the memory test (PK-M) decides whether a stored state is better than a classical guess, and what efficiency the memory would need.

## 8.1 What a quantum memory is for

A memory holds a photon's state for a while and gives it back on command. We need one to line up timing and to hold results while other steps happen. A memory is *quantum* only if it preserves amplitudes and phases ([Volume 2](02-quantum-states.md)), not just the "which address".

## 8.2 The simple test: beat the classical guess

If someone only measures the incoming photon and builds a replacement from the result, the best they can do has a known fidelity. A memory is **certified** if it does *better* than that. Different test sets have different classical limits, and we keep them apart:

| Benchmark | Value | Applies to |
|---|---|---|
| 2/(d+1) | **0.40** for d = 4 | Hidden random pure states [DERIVED] |
| Entangled-target overlap | 0.25 | A different test using an entangled target [DERIVED] |
| Joint classical bound for coherent states | **0.482253** | Coherent states with mean photon number 0.25, four independent modes [DERIVED] |

The third is ((1 + n̄)/(1 + 2n̄))⁴ with n̄ = 0.25: (1.25/1.5)⁴ = (5/6)⁴ = 0.482253. The **proof** of this joint bound is [UNVERIFIED]: it is awaiting independent review.

>
> **Common mistake**
> **Do not mix the benchmarks.** A fidelity of 0.45 beats the 0.40 benchmark but not the 0.482253 one. Always say which test.


## 8.3 Four modes, four losses

In the memory design (PK-M) the four Tetragon addresses behave as four independent optical modes. Each mode suffers loss, and loss multiplies: the memory must be efficient enough that after loss and added noise, the state still beats the bound. In the model, the fidelity for a pure-loss memory with efficiency η and added thermal noise *v* per mode is

```
F = (1 + v + n̄ (1 − √η)²)⁻⁴
```

[DERIVED] for four independent Gaussian-ensemble modes. Two sanity checks:

- If the memory returns nothing (η = 0, no noise) the fidelity is 0.4096, which is *below* the bound 0.482253, so an empty memory fails the test, as it should.
- With no noise, the memory must pass a minimum efficiency (the **threshold**):

| Mean photon number n̄ | Minimum efficiency (noiseless) |
|---|---|
| 0.25 | **1.1146 %** |
| 1 | **8.5786 %** |

## 8.4 Noise eats the margin

A little thermal noise costs a lot. At 4 % efficiency, a noise of *v* = 0.04 per mode puts the fidelity **exactly on the bound**: no margin to spare. At 2 % efficiency with *v* = 0.0001 the model gives fidelity 0.508185. The analytic-anchored combined estimate, after a small correction of 0.001078, is 0.507107, which is 0.024854 above the bound [SIMULATED]. The quoted uncertainty covers Monte Carlo error only; systematic errors are not included.

## 8.5 The chain: where the light actually goes

The overall efficiency is a *product* of the parts in the chain. An example from the design notes:

```
internal memory 4 %  ×  converters 0.49  ×  filter 23 %  =  0.451 %
```

That is **below** the 1.1146 % threshold, so a memory built like that would **fail** the test, even before noise [DERIVED] arithmetic on supplied values.

How much filter transmission would be needed? The table gives the minimum filter transmission with zero margin and no noise:

| Internal efficiency | Converter efficiency | Filter must be at least |
|---|---|---|
| 4 % | 0.49 | **56.9 %** |
| 4 % | 0.81 | **34.4 %** |
| 12.6 % | 0.49 | **18.1 %** |
| 12.6 % | 0.81 | **10.9 %** |

And what happens to the margin with the filter choices:

| Internal | Filter | Overall efficiency | Margin over the bound |
|---|---|---|---|
| 4 % | 23 % | 0.451 % | −0.0272 (fails) |
| 4 % | 90 % | 1.764 % | +0.0198 |
| 12.6 % | 23 % | 1.420 % | +0.0098 |
| 12.6 % | 90 % | 5.557 % | +0.0975 |

(Converters 0.49 and no noise in all rows.) The memory paper these numbers are tied to is arXiv:2604.13900, "Dynamic rephasing in a telecom warm vapor quantum memory" (ORCA protocol, warm atomic vapor). Its abstract reports a 50-fold extension of storage time, GHz bandwidth, low noise, and storage and retrieval of four independent time-bin modes. It states **no efficiency figures**, so the internal efficiencies used here (4 % and 12.6 %) and the converter and filter values could not be confirmed from the abstract [UNVERIFIED].

## 8.6 Why the detector matters too

The test uses detectors. If the detector efficiency is too low, the result cannot be trusted. For the model with ideal noise and infinite statistics, the crossover is a **detector efficiency of 85.73 %**: below it the detector-aware bound drops under the classical bound and the test cannot certify anything [DERIVED].

## 8.7 An earlier design

An earlier design used four *time* modes. With an assumed retrieval chain of 0.70 × 0.04 × 0.70 the survival was 1.96 % [ASSUMED]. That is **not** a validation of the timing-free Tetragon, and it is not a quantum memory built by PhaseKeep. A memory-based design should always report survival and state fidelity as two separate numbers.

## 8.8 Known recipes versus unknown states

If a state was prepared by a known recipe and is lost, we can **prepare it again**. If an unknown state (the result of a computation) is lost, it cannot be rebuilt or copied. Memory loss is therefore much more costly for results than for inputs.

>
> **Go deeper (optional math)**
> The noiseless threshold comes from setting F = bound with v = 0: n̄(1 − √η)² = n̄/(1 + n̄), so η = (1 − 1/√(1+n̄))². For n̄ = 0.25 that is (1 − √0.8)² = 0.011146 and for n̄ = 1 it is (1 − √0.5)² = 0.085786 [DERIVED]. These and every other number in this volume are reproduced by `verify_r25.py` (71 checks pass).


>
> **Evidence status**
> **Evidence status.** Formulas, thresholds, chain arithmetic and filter tables: [DERIVED], run in code. The joint-bound proof: [UNVERIFIED]. Efficiency inputs (4 %, 0.49, 23 % and so on): [ASSUMED] or [REPORTED] from a supplied paper not independently checked. No memory has been [MEASURED] by PhaseKeep.


## Try it

1. A memory has overall efficiency 1 % and no noise, n̄ = 0.25. Does it pass? (No: 1 % is below 1.1146 %.)
2. You raise the filter transmission from 23 % to 90 %, internal 4 %, converters 0.49. New overall efficiency? (0.04 × 0.49 × 0.9 = 1.764 %. It now passes.)
3. A memory gives fidelity 0.45 on random hidden states. Is it better than classical? (Yes against 0.40 — but that does not show it beats the coherent-state bound of 0.482253, which is a different test.)

## Summary

>
> **Key idea**
> Loss multiplies along the chain. A memory is only useful if the overall efficiency clears a threshold (1.1146 % at n̄ = 0.25) *and* noise stays small. The supplied chain of 0.451 % fails; some alternatives pass. Always state which benchmark you are beating.



---
*(c) 2026 Tyler O'Bryan, where applicable. PhaseKeep Research. Text CC BY 4.0, code MIT. AI-assisted research, documentation and numerical analysis. Draft for technical review.*
