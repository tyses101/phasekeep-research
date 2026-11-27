# Volume 9: The Research Lab

## What you will learn

How the project checks itself: the scripts, the audit list, the corrections we made to our own claims, and what is still blocked. If you only want to know whether to trust a number, this volume and the Ledger (Appendix 2) are where to look.

## 9.1 The evidence system

Every claim carries a label (explained in Start Here). The labels exist because most research mistakes are not arithmetic errors; they are a *simulation result being quoted as a measurement*, or a *published result being quoted as ours*. No physical measurement by PhaseKeep exists. The tag [[MEASURED]] is reserved for the day one does.

## 9.2 The scripts

Each script is plain Python and can be rerun. Passing a script tests the **model and the arithmetic**, not the laboratory.

| Script | What it does | Result |
|---|---|---|
| `verify_r25.py` | Re-derives the memory, single-photon-benchmark and chain numbers | 71 of 71 checks pass |
| `audit_bundle_r25.py` | Read-only audit of the Codex feasibility bundle: file hashes, a counterexample, the chain table | All pass |
| `outcome_resolved_herald_r30.py` | Rebuilds the herald outcome classes from the optical network and cross-checks them two ways | Pass; also refuses to run on a modified package unless told to |
| `a06_precursor_sim.py` | Shared versus individually addressed operation (A06) | 19 self-checks pass; 120 result rows |
| `build_spec_draft.py` | Numerical checks behind the component specification | 12 checks pass |

The scripts are bundled in the `research` folder of the download. The first, third and fifth rows run on their own with Python and NumPy (they were re-run from that folder when this library was assembled). The second and fourth need the Codex feasibility bundle, which is not included; they are there so you can see exactly what was checked. The simpler programs in the `code` folder (Volume 14) need nothing but Python.

## 9.3 The audit list

| Item | Question | Status |
|---|---|---|
| **A01** | Can the Codex bundle's numbers be reproduced? | **Resolved.** 27 of 27 checks in the saved environment; 26 of 27 in a second environment, where only an exact-bytes comparison failed (rounding-level differences, 1.6 × 10⁻¹⁴ at most) |
| **A02** | Does the reconstruction match the published apparatus? | **Pending** |
| **A03** | Do accepted heralds indicate valid outputs? | In the reconstruction, **no** for some inputs (Volume 7) |
| **A04** | Do outputs stay usable without destructive verification? | **Open** |
| **A05** | Two successive reactions with reliable intermediate certification? | **Open** |
| **A06** | Is a shared transformation cheaper than addressing each state? | **Done as a simulation** with assumed inputs |

The verification steps for the heralded gate are numbered BV-01 to BV-06:

| Step | What | Status |
|---|---|---|
| BV-01 | Catalogue every photon-number output sector | Done for the reconstruction at d = 4 and 8 (up to two photons); not for hardware |
| BV-02 | Find indistinguishable success and failure patterns | Found in the model |
| BV-03 | Alternative auxiliary analyzer configurations | Open |
| BV-04 | Additional verification resources | Open |
| BV-05 | Non-destructive photon-number verification | Open |
| BV-06 | Two successive verified reactions | Open, blocked on BV-03 to BV-05 |

## 9.4 The A06 result in brief

A06 asked: if we want to apply a change to many addresses, is it cheaper to use one shared operation, or to separate the addresses, change each one, and put them back? The operation was an H/V exchange applied to every twist mode, each mode left in place. It accounted for **Before, Operation and After** (Volume 7) and swept the number of modes, plate retardance drift, a rotation error and an element error.

- When the state can stay where it is, the shared operation needs 1 part against 8 to 218 (for N = 2 to 32).
- When the full twist must be read out afterwards, the saving is about 14 % (N = 2) to 20 % (N = 32) in parts counted.
- Under the default assumptions the shared design keeps fidelity near 0.9996; the individual design falls to 0.99471 at N = 32, with transmission 0.937.
- The shared design loses only if a real plate's retardance varies across modes by roughly 13 to 20 times the assumed amount. That is the first thing to measure.
- **Every error number is an assumption**, the separating device is an illustrative model (published sorters are different devices), and preparation and detection were not simulated [[SIMULATED]].

## 9.5 The component specification

The draft Physical Architecture Specification has 12 records. For each one it lists the operation, the control, whether the photon stays in the four addresses, risks, cost, compatibility, evidence and the Buddy Check status [[PROPOSED]].

| ID | Component |
|---|---|
| C01 | Half-wave plate |
| C02 | Quarter-wave plate |
| C03 | Image reflection optics |
| C04 | Image rotation optics (for example a Dove prism) |
| C05 | Q-plate |
| C06 | Beam splitter |
| C07 | Polarizing beam splitter |
| C08 | Phase modulator |
| C09 | OAM sorter |
| C10 | Inverse sorter |
| C11 | Photodetector |
| C12 | Buddy interaction (heralded two-photon controlled-phase-flip, a reconstruction of Liu et al.) |

Notable statuses: C11 (the detector) cannot authorize reuse of the photon it consumes; it can only characterize a separate test ensemble. C12's Buddy Check is **UNRESOLVED**. Records C05 and C09 rest on references that were supplied or read only as abstracts (Appendix 3).

## 9.6 Mistakes we made, and fixed

This list is here on purpose. A project that lists no mistakes has not looked.

1. **A wrong explanation of chain decay.** We said the decay of fidelity along a chain of gates was "dominated by false heralds" at every length. Measurement showed phase drift matters more at long chains (about 1.3 points at 2 stages, about 11 and 15 at 8 and 16). The claim was withdrawn and the check rewritten with measured values.
2. **A wrong date.** The heralded gate paper is a July 2024 preprint, not a 2026 one.
3. **A "metric undefined" claim.** The chain metric was defined after all; the earlier statement was wrong.
4. **A mutation test that tested nothing.** Our first deliberate-error test changed a phase that has no effect on photon-number probabilities, so it could not fail. We replaced it with a beam-splitter angle change, which broke the equal split as it should.
5. **A brittle guard.** The first R30 script identified the right package by a source-text match. It was replaced by a behavioural check.
6. **A cached web page.** A page fetch returned an older revision once; a second fetch returned the new one. The cause was not determined.

## 9.7 Integrity versus reproducibility

Two different things are checked and should not be confused. **Package integrity** asks "are these the same files?" and is checked with hashes. **Reproducibility** asks "does running the code give the same numbers?" and is checked by rerunning. A matching hash does not show the numbers are right; matching numbers do not show the files are unmodified.

## 9.8 The blocked register

Things we cannot do yet, and what each is waiting for.

| ID | Item | Waiting for |
|---|---|---|
| B01 | Physical joint gate | Wavelength, bandwidth and phases (including π/2) in one mechanism |
| B02 | Four-mode memory phase preservation | A measurement; the reference paper measured no relative phase |
| B03 | Joint-bound proof | Independent review |
| B04 | Effective detector bound of about 0.95 | A derivation or a reference |
| B05 | Permanent archive and DOI | A repository account (a temporary mirror exists) |
| B06 | A trustworthy success signal that does not consume the outputs | BV-03 to BV-05 |
| B07 | Apparatus mapping for the simulation bundle | Independent review of the reconstruction against the published apparatus |

::: evidence
**Evidence status.** Script outcomes: reported by running them; the independent rerun of R30 (20 of 20) is [[REPORTED]] by a second party. A06: [[SIMULATED]]. Specification: [[PROPOSED]]. Everything in the blocked register: [[BLOCKED]].
:::

## Try it

1. A package's hash matches. Does that mean the numbers in it are correct? (No. It means the files are unchanged.)
2. Why is a mutation test that cannot fail worthless? (It does not show your checks would catch a real mistake.)
3. Which audit item is the first one to finish before designing any remedy for the false heralds? (A02, the apparatus mapping.)

## Summary

::: key
The project checks itself with rerunnable scripts, a numbered audit list, a public list of our own corrections, and a blocked register. A pass means the model and arithmetic hold up; it never means the laboratory has confirmed anything.
:::
