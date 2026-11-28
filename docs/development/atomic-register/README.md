# PhaseKeep research update: start here

**What this is:** everything PhaseKeep worked out between repository checkpoint `e5f1507` and 28 November 2026. It covers the ideas, the maths, the simulations, the things that failed and what is still open, all packaged so that Codex can check it and merge it into the [PhaseKeep repository](https://github.com/tyses101/phasekeep-research).

**Status:** development research record; see the dated integration checkpoint. and nothing here is a hardware measurement. Results include DERIVED, SIMULATED and explicitly REPORTED material. Missing A-series implementations and unresolved literature details are not independently verified.

---

## Choose how deep to go

| You have | Read | You'll come away with |
|---|---|---|
| **5 minutes** | [The short version](01_the_short_version.md) | What PhaseKeep tried, what worked, what didn't, in plain words |
| **30 minutes** | The short version, then the first line of every chapter in [the full story](02_the_full_story/00_contents.md) | The whole arc, with the key numbers |
| **An afternoon** | [The full story](02_the_full_story/00_contents.md), then [how to check it](03_reference/reproduce.md) | Every result, and how to rerun it yourself |
| **You're Codex** | [Integration checkpoint](../checkpoints/atomic-register-2026-11-28.md) | Exactly what to verify, where it goes in the repo, and the open discrepancies |

## Map of the package

```
README.md                       ← you are here
01_the_short_version.md         plain-language summary
02_the_full_story/              14 short chapters, each opens with "In plain words"
03_reference/                   look-it-up material
   terms.md                       every PhaseKeep term, its status, and what it means
   timeline.md                    what happened, in order
   experiments.md                 every experiment: question, script, result, evidence class
   evidence_and_failures.md       what's proven how, every negative result, superseded ideas, audit
   sources.md                     papers, DOIs and verification status
   reproduce.md                   how to rerun everything
04_codex_handoff/               integration instructions for Codex
   handoff.md                     checklist, repo placement map, discrepancies to resolve
05_whats_next.md                open research, in priority order
code/                           all simulation scripts (Python + NumPy only)
   results/                       raw CSV outputs and run logs
supporting/                     earlier working documents, kept as-is for the record
```

## How to read the evidence labels
Every claim carries one of the project's standard labels:

| Label | Meaning |
|---|---|
| **DERIVED** | Follows mathematically from stated assumptions |
| **SIMULATED** | Computed in a stated numerical model, with a script in `code/` |
| **REPORTED** | Stated by an independent run or external source, not re-run in this package |
| **ASSUMED** | Taken as given for a model |
| **PROPOSED** | A design idea, not yet tested |
| **MEASURED** | From hardware. **There are none in this update.** |
| **UNVERIFIED** | Not yet checked: from memory, or a source we couldn't read |
| **BLOCKED** | Can't proceed until something else is resolved |

## Three things to know up front
1. **The register is not a new kind of quantum bit.** Mathematically it's a small, known structure. Anything new would be in how it's built and controlled. See [chapter 2](02_the_full_story/02_register_geometry.md).
2. **Failures are kept on purpose.** Several promising ideas failed in simulation, and each failure is recorded with the reason, because the reasons are the most useful results. See [evidence and failures](03_reference/evidence_and_failures.md).
3. **Physics feasibility is open.** No platform has demonstrated this register, and atomic decay is the biggest known obstacle. See [chapter 12](02_the_full_story/12_platforms_G0.md).

## Licence and openness
The code and documents are intended to go into the public repository under its existing licence. Codex should confirm the licence files cover the new material before merging (see the handoff checklist).

[REPORTED] Earlier separate re-run: ChatGPT at the owner's request, 27–28 November 2026; A-series scripts absent. See the [integration checkpoint](../checkpoints/atomic-register-2026-11-28.md) for this publication's verification.
