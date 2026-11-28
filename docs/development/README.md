# PhaseKeep research development, checkpoints V0 to V1.0

**Status: working development record, written 2026-11-27. Provisional and model-based. Not part of Revision H.** The Learning Library, Edition 03, Revision H (release `edition-03-rev-h`) is the frozen educational baseline, and nothing on these pages changes it. **No experimental hardware measurement has been produced by this project, and no advantage over any architecture has been shown.**

**New here?** Start with [PhaseKeep from the beginning](phasekeep-from-the-beginning.md), one page that tells the whole story from the first question to the latest research in plain words. It links to every detailed page.

Evidence classes used on every page: **DERIVED**, **ASSUMED**, **PROPOSED**, **UNVERIFIED**, **MEASURED** (none exist), **BLOCKED**. They are the same classes as the frozen library, and [Research status](research-status.md) explains how they apply here.

:::key Research status at a glance
This is where the work stands. Read each line for what it does *not* say.

| Level | State | What it means |
|---|---|---|
| Mathematical derivation | **Established within stated models** [DERIVED] | Exact results for ideal gates, exact Pauli algebra and exact enumeration. They hold if the model holds, and say nothing about whether the model describes a device. |
| Computational validation | **Author-side only** [DERIVED] | 11 checkpoint programs ran from clean extracted copies and printed `ALL PASS`. That is numerical consistency inside the models, not independent reproduction. |
| Proposed architecture | **Open** [PROPOSED] | Buddy configurations, Integrated Quantum Assurance (IQA), PALADIN, Docked Scheduling and shared ancillary hosting are proposals. Buddy's physical form is deliberately not fixed. |
| Physical feasibility | **Unresolved, and the central question** [ASSUMED] | The V1.0 models show that probabilistic photon-photon interactions and photon loss may decide whether verification is usable at all. Whether suitable gates and readout exist is not known. |
| Hardware measurement | **None** [MEASURED] | Nothing has been built or measured. |
:::

## Guiding philosophy

We do not know everything, and perhaps we do not yet know everything about the things we believe we understand. Even established knowledge can contain unexplored relationships, overlooked possibilities, and opportunities for discovery.

PhaseKeep exists to explore those possibilities with curiosity, intellectual humility, scientific rigor, and a willingness to be proven wrong.

We question not to dismiss established science, but to discover what more it may have to offer.

## The question

The central question and the subordinate question are kept word for word on [one page](central-question.md).

## How to read this section

1. [Research status](research-status.md) explains the five levels above and the evidence classes.
2. [Timeline](timeline.md) lists V0 to V1.0 in order. Each [checkpoint page](checkpoints/v1.0.md) gives the question, model, assumptions, results, negative results, corrections, limits and reproduction command.
3. [Physical feasibility](physical-feasibility.md) is the V1.0 summary and the most important page for a reader judging viability.
4. [Errata](errata.md) lists every correction with its date. Original checkpoint files are never edited; corrections live in separate dated documents.
5. [Negative results](negative-results.md) and [Open problems](open-problems.md) are kept prominent on purpose.

## Where things live

| Location | Contents |
|---|---|
| `docs/development/` | These pages (Markdown source). |
| `development/` | The same pages as generated HTML for GitHub Pages, built by `tools/build_development_site.py`. |
| `checkpoints/vX/` | Original checkpoint source packages, unchanged, each with its own `SHA256SUMS.txt`. |
| `docs/research-development.md`, `docs/development-glossary.md` | Earlier provisional pages from pull request #1 and the HDOC glossary. Preserved. |
| `library/` | The frozen Revision H library. Preserved. |

## Licence scope

Original text written for this development layer, including every Markdown page under `docs/development/` and the checkpoint documents under `checkpoints/*/docs/` and the checkpoint `README.md` and `CODEX_HANDOFF.md` files, is licensed under **CC BY 4.0** (`LICENSE-TEXT-CC-BY-4.0.txt`). Original code, including every Python file under `checkpoints/` and `tools/build_development_site.py`, is licensed under **MIT** (`LICENSE-CODE-MIT.txt`). The generated HTML under `development/` carries the licence of the text it renders, CC BY 4.0, and the stylesheet and layout embedded in it are MIT. `SHA256SUMS.txt` files are data and carry no separate licence.

Cited papers are described in our own words and remain the work of their authors and publishers; nothing from them is reproduced. This statement leaves `LICENSE`, `NOTICE.txt` and both licence files unchanged, and it does not claim ownership of underlying scientific ideas. Material generated by AI may not carry copyright; the licences apply to the extent copyright subsists, as `NOTICE.txt` already says.

## Who wrote this

Project originator: Tyler O'Bryan. The checkpoints and these pages were prepared with AI assistance (Claude); the numerical checks were written and run by the same AI, so they are author-side. See [Reproducibility](reproducibility.md).

## QDE and relational computing proposal

[PROPOSED] The provisional [QDE, QIJ and ASV framework](qde-relational.md) extends the research questions under GEA and Integrated Quantum Assurance, with an [explicit dated documentation checkpoint](checkpoints/qde-2026-11-27.md). It includes a literature map and a proposed two-Tetragon benchmark, not new simulation results or an implemented architecture.

## Atomic-register update, 2026-11-28

[PROPOSED] [Start with the short version and chapters](atomic-register/README.md). Model-based development; no hardware demonstration or novelty claim.

## Hybrid atomic checkpoint, 2026-11-28

[PROPOSED] [Hybrid Atomic Registers and Dynamic Protected Geometry](checkpoints/hybrid-atomic-2026-11-28.md): recovered sources, limited numerical reproduction, corrections and deferred verification. Post-Edition 04 development; books unchanged.
