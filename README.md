# PhaseKeep Research

**Draft for technical review · Author and project originator: Tyler O'Bryan**

**No experimental hardware measurements have been produced by this project.**
No functioning quantum computer or quantum advantage has been demonstrated.

PhaseKeep is an evolving collection of open, independent research directions,
with **Geometric Encoding Axies (GEA)** and **Integrated Quantum Assurance (IQA)**
as its two primary research pillars. Through theoretical analysis, simulation
and collaborative investigation, it explores photonic information processing
and emerging quantum architectures without a predetermined technological destination.

IQA is an exploratory framework encompassing verification, preservation,
resource preparation, operational integrity and quantum information continuity.
Our objective is discovery rather than confirmation: even a modest, independently
verifiable contribution to an existing field is worthwhile. This direction
implies no experimental validation, demonstrated quantum computing capability
or established scientific breakthrough.

The [IQA naming decision](docs/development/register-of-terms.md#iqa-naming-decision-2026-11-27)
supersedes the earlier provisional expansion, Independent Quantum Assurance.
Buddy System terminology, historical definitions, stable identifiers and frozen
releases remain intact; this naming decision does not modify the architecture.
A detector herald does not necessarily certify a valid, reusable quantum output.

## Guiding philosophy

We do not know everything, and perhaps we do not yet know everything about the things we believe we understand. Even established knowledge can contain unexplored relationships, overlooked possibilities, and opportunities for discovery.

PhaseKeep exists to explore those possibilities with curiosity, intellectual humility, scientific rigor, and a willingness to be proven wrong.

We question not to dismiss established science, but to discover what more it may have to offer.

## Start reading

**[Start Here: unified research index](https://tyses101.github.io/phasekeep-research/research-index.html)** — searchable contents across both editions, terminology, timeline, corrections and reproduction resources.

**New here?** [PhaseKeep from the beginning](https://tyses101.github.io/phasekeep-research/development/phasekeep-from-the-beginning.html)
tells the whole story on one page, from the first question to the latest research, and links to every detailed page.

The **Learning Library, Edition 04 (working draft)** continues the book series from Volume 15 as a
dated research snapshot. Edition 03 Revision H stays frozen. The reader carries both editions, clearly labelled.

**[Open the library reader](https://tyses101.github.io/phasekeep-research/reader.html)**
for previous/next navigation and a chapter selector, or
[read continuously](https://tyses101.github.io/phasekeep-research/reader.html?view=all)
to scroll and search the entire book with your browser's Find command.
The self-contained `reader.html` also works offline when downloaded and opened
directly. It presents the original HTML content without modifying the frozen files.

For individual files, use GitHub's **Preview** view for `.md` documents and
GitHub Pages for rendered `.html` pages. GitHub's file view shows HTML source;
Pages serves Markdown as a file rather than a formatted reading page. Every
reader chapter links to its original HTML and Markdown on GitHub.

The **Learning Library, Edition 03, Revision H** introduces the ideas for
self-taught readers, with deeper mathematical material for researchers and
engineers. Read [Start Here](library/markdown/00-start-here.md), then
[First Words](library/markdown/00b-first-words.md). The [HTML library](library/index.html)
works offline. [Open the hosted library](https://tyses101.github.io/phasekeep-research/library/).
The [PDF](library/PhaseKeep-Learning-Library-complete.pdf) and
[EPUB](library/PhaseKeep-Learning-Library.epub) are included.

| Location | Contents |
|---|---|
| `library/markdown/` | Volumes and appendices readable on GitHub |
| `library/src/` | Original editable source |
| `library/code/` | Six educational numerical examples and their runner |
| `library/research/` | Original research scripts, reports and simulation results |
| `library/ledger.csv` | 46 numeric entries and evidence classifications |
| `releases/` | Provenance, verification and publication notes |

The library stays together to preserve relative links, executable paths and
its original checksum manifest. The untouched original ZIP is a release asset;
it is not committed to Git. See [publication notes](releases/PUBLICATION_NOTES.md)
for the distinction between the original snapshot and current repository notices.

The reader is a separate navigation aid. Maintainers can regenerate it with
`python tools/build_reader.py`; this reads the frozen HTML and never rewrites it.

## Exploration pack S (S01–S31)

Read the [consolidated scientific review](explorations/consolidated-review.md)
and [study index with execution records](explorations/README.md). PR #3 was
merged with owner authorization on 2026-11-27. The author reports all 31
full-regression scripts passed at head `1ebe4a4`; this is author-side validation,
not independent reproduction. The pack is exploratory, not V1.1 or a new release.

## Provisional research development

The **[development glossary: HDOC](docs/development-glossary.md)** records
High-Dimensional Orthogonal Configurations under GEA, the mathematical
distinctions, and the proposed five-basis investigation. It is separate from
the frozen Revision H glossary; the proposed experiment has not been run.

Revision H is the **frozen educational baseline**. The separate
[research-development document](docs/research-development.md) is provisional,
does not revise that baseline, and retains its open scientific questions and
evidence limitations. The [Pages landing page](https://tyses101.github.io/phasekeep-research/)
links to this document alongside the frozen library.

The **[development record, checkpoints V0 to V1.0](docs/development/README.md)**
([web version](https://tyses101.github.io/phasekeep-research/development/index.html))
collects eleven model-based checkpoints with their source packages under
`checkpoints/`, results, negative results, dated errata, terminology, open
problems and a proposed V1.1 roadmap. It is provisional development
documentation, separate from Revision H. No hardware measurement has been
produced, no advantage over any architecture has been shown, and the numerical
checks are author-side, not independent reproduction. See
[reproducibility](docs/development/reproducibility.md).

Run the new standard-library-only example from the repository root:

```sh
python code/entanglement_organization.py
```

This is a regression example, not experimental validation or independent
mathematical reimplementation. Use [GitHub Issues](https://github.com/tyses101/phasekeep-research/issues/new/choose)
for corrections and feedback.

## Reproduce the examples

With Python 3, run from the repository root:

```sh
python library/code/run_all.py
python library/code/two_tetragons.py
```

These examples use only the standard library. Research arithmetic, A06 and ledger
regeneration additionally require NumPy (`python -m pip install numpy`).

```sh
python -I library/research/verify_r25.py
python -I library/research/spec/build_spec_draft.py /path/to/temporary/spec-output
python -I library/research/a06/a06_precursor_sim.py /path/to/temporary/a06-output
```

To regenerate the ledger, first copy `library/` to a temporary directory, then
run `python make_ledger.py` inside that copy. It writes `ledger.csv` and
`src/A2-ledger.md`; do not overwrite the archival snapshot to test it.
From `library/`, `sha256sum -c SHA256SUMS.txt` verifies all 100 listed files.
Two research scripts require a separate feasibility bundle that is not supplied
here: see [research instructions](library/research/README.txt). Their presence
does not imply that those analyses can be reproduced from this repository alone.

## Read the evidence labels

| Label | Meaning |
|---|---|
| DERIVED | Mathematical result under stated assumptions |
| REPORTED | Result reported by a cited source; reading scope is recorded |
| SIMULATED | Output of a model, not experimental validation |
| ASSUMED | Selected input rather than a measurement |
| PROPOSED | Architectural proposal, not demonstrated capability |
| MEASURED | Reserved for project hardware measurements; none exist |
| UNVERIFIED | Claim or source not yet checked |
| BLOCKED | Work cannot proceed without missing evidence or capability |

Passing code checks establishes numerical consistency within the models, not
their physical validity, hardware feasibility or superiority. Negative findings,
uncertainty statements and evidence classifications are retained.

## What we are asking reviewers to look at


These are open questions, not settled results:

1. **Heralded two-photon operations.** In our reconstruction of a published gate, the herald fires on 0.375 of runs, and in the worst case only one third of those give an occupancy-valid output (ideal detectors, reconstruction-specific). Does our reconstruction match the published apparatus (audit item A02)?
2. **Certification without consuming the photon (A04).** Is there a trustworthy, non-consuming success signal for a heralded output?
3. **Two entangled Tetragons.** The cyclic correlation pattern needs a coupled polarization-OAM operation (an axis SWAP plus a flip). Is the analysis in Volume 6, section 6.7 right, and is there a practical device for it?
4. **Twist mixing.** Is there a practical device that mixes OAM -1 and +1 beyond swap or phase?
5. **Memory certification bound (B03).** The joint classical bound for four-mode memory certification needs an independent proof review.
6. **Inputs we could not source.** The memory-chain efficiencies (4%, 12.6%, 0.49, 23%) are unconfirmed.


## Scientific work still open

- Reconciliation of historical A03/A04 numbering; existing R30 numbering is retained.
- Full-text review of cited papers and source verification for memory-chain inputs of 4%, 12.6%, 0.49 and 23%.
- Independent review of the B03 joint-bound proof.
- B05 archival and DOI completion.
- Experimental hardware validation, nondestructive verification and computational continuation.
- Demonstration of reduced physical costs for equivalent logical operations.

Publication does not complete any of these scientific items. Architectural
terminology is frozen. The existing R29 website and the separate
`QT-2026-11-26-R30` deployment are outside this publication.

## Corrections and citation

Use [GitHub Issues](https://github.com/tyses101/phasekeep-research/issues/new/choose) to report the volume, section,
revision, explanation and supporting source or derivation. The original starter
kit's [review invitations](REVIEW_REQUEST_DRAFT.md) are drafts and have not been posted.

Suggested citation: Tyler O'Bryan. *PhaseKeep Learning Library, Edition 03,
Revision H*. PhaseKeep Research, 2026. Draft for technical review. Cite the release
tag `edition-03-rev-h` and the commit used. See [CITATION.cff](CITATION.cff).
Zenodo preservation is enabled. The development snapshot has DOI
[10.5281/zenodo.24589667](https://doi.org/10.5281/zenodo.24589667).
This is not a separate DOI for the original Revision H release.
See [development downloads](docs/development/downloads.md) for all 16 release assets.

## Licence and attribution

© 2026 Tyler O'Bryan, where applicable. **AI-assisted research, documentation and
numerical analysis.** Educational text, original figures and tables are
[CC BY 4.0](LICENSE-TEXT-CC-BY-4.0.txt); original source code is
[MIT](LICENSE-CODE-MIT.txt). See [LICENSE](LICENSE) and [NOTICE.txt](NOTICE.txt).
Third-party rights remain with their holders. Copyright protection may not apply
to entirely AI-generated material, and these licences do not establish ownership
of underlying scientific ideas. PhaseKeep Research is a project identity, not a
claim of incorporation, accreditation or institutional affiliation.
