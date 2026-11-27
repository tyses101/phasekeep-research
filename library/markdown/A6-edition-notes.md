# Edition Notes

*What changed from Edition 02, naming decisions, and how this library was checked*


## Revision log

- **Revision a** (26 November 2026, afternoon): the first complete draft, Start Here and Volumes 1 to 14 with appendices.
- **Revision b** (26 November 2026, evening): added geometry as a way to describe operations ([Volume 4](04-geometric-encoding.md), section 4.10), the State Space and State Space Environment distinction ([Volume 10](10-intelligent-registers.md), section 10.5), three corrections for reading geometric drawings ([Volume 10](10-intelligent-registers.md), section 10.6), the capability-versus-cost caution ([Volume 10](10-intelligent-registers.md), section 10.7), a short list of Tetragon bench checks with the single-photon simulability caveat ([Volume 11](11-experiments.md), section 11.4), tesseract counts, new exercises 23 to 28, new example checks, and the research and EPUB additions.
- **Revision c** (26 November 2026, late evening): added *First Words*, a starting glossary of every background term for a reader who knows nothing yet. Following the project owner's instruction to keep imaginative speculation to a minimum, removed from revision b: an instruction table for geometric operation compilation, the Dynamic State Geometry name and loop, a long property table for the environment, six ranked research directions with difficulty labels, and an illustrative optimizer table. Kept: the established corrections, the capability-versus-cost caution and the single-photon simulability caveat. The copy you hold is the one whose `VERSION.txt` says revision c or later.
- **Revision h** (26 November 2026, late evening): publication preparation only, with no scientific change. Added authorship, attribution, licence and third-party notices (`NOTICE.txt`, two licence files, page footers, source-code headers), recorded the vocabulary freeze, confirmed the PKC, DDQT and AIS terms, added PK-BS, and wrote down the A03/A04 traceability note. The scripts in `research/` were left unchanged on purpose so that their recorded hashes stay valid. The R30 `published_utc` field was not set, since it is set only when the release goes live.
- **Revision g** (26 November 2026, late evening): two accuracy corrections after independent review. The operator-rank gate-count floor now states its gate model and gives the SWAP-versus-CNOT example (floor 2, exact circuit 3). The [Volume 7](07-buddy-checks.md) caution now reads "encoding-basis counts alone cannot certify quantum coherence or entanglement", since joint counts can show classical correlation. No numbers changed.
- **Revision f** (26 November 2026, late evening): one derived caution added to [Volume 7](07-buddy-checks.md), section 7.4: counting clicks in the encoding basis cannot distinguish states that differ only in a relative phase or correlation, so certifying a correlation needs other bases. No numbers changed. Other points raised in a reflective discussion (priority rankings, "nearly free" operations, preservation during reconfiguration) were not adopted because they are untested.
- **Revision e** (26 November 2026, late evening): wording corrections after an independent review of revision d. "Largest possible coupling" was replaced by "maximal operator Schmidt rank", which is a statement about the operation not factoring, not about physical strength or entangling power. The non-entangling property of SWAP is exact, and the 200 random inputs are only a spot check. One open question was added on whether the sorting of operations predicts cost. No numbers changed.
- **Revision d** (26 November 2026, late evening): high-dimensional entanglement adopted by the project owner as the cornerstone, stated in Start Here as a framing and not a new pillar. New [Volume 6](06-two-photons.md) section 6.7 on two entangled Tetragons (joint dimensions, ebit counts, five correlation patterns, and the derived result that four of the five are a polarization pair times a twist pair while the cyclic rotation needs a coupled operation), the program `two_tetragons.py`, ledger rows L41 to L46, exercises 29 to 33, an independent / coupled / entangling sorting of operations, and four new source entries read at abstract level. Not adopted from the source discussion: a mapping table that matched PhaseKeep concepts to research fields (several matches overreached), the three research questions, and the term "dynamic entanglement geometry".

## Authorship, attribution and licence

| Item | Setting |
|---|---|
| Author and project originator | Tyler O'Bryan |
| Project identity | PhaseKeep Research |
| Attribution | AI-assisted research, documentation and numerical analysis |
| Copyright | © 2026 Tyler O'Bryan, where applicable |
| Educational material | Creative Commons Attribution 4.0 (CC BY 4.0) |
| Source code | MIT License |
| Corrections and feedback | GitHub Issues, once a public repository exists. No contact address is given because none exists yet |
| Status | Draft for technical review |

Neither licence establishes ownership of underlying scientific concepts, and copyright may not subsist in material generated entirely by an AI system. Cited works are summarized in our own words and remain the property of their authors and publishers. Details are in `NOTICE.txt`, `LICENSE-TEXT-CC-BY-4.0.txt` and `LICENSE-CODE-MIT.txt`.

## Vocabulary freeze

The core vocabulary is frozen as of revision h: EA, CT, GEA, the Buddy System and Buddy Checks, PK-BS, PKC, DDQT, AIS, the Tetragon and the register family names, and the evidence tags. High-dimensional entanglement is the scientific cornerstone, with GEA and the Buddy System as the two pillars. A new term needs a literature check and a demonstrated purpose before it is added.

## Audit item labels: traceability

The audit item labels are **not renumbered** here. This library uses the R30 table:

| Label used here | Meaning in this library |
|---|---|
| A03 | Do accepted heralds indicate valid outputs? |
| A04 | Do outputs stay usable without destructive verification (nondestructive certification)? |

An earlier edition's notes labelled nondestructive certification as A03. The historical audit records were not available for this check, so which numbering is authoritative is **pending reconciliation by the project owner**. Until then, check the meaning, not only the number, when citing A03 or A04.

## What this edition is

Edition 03 reorganizes the Edition 02 learning library into a book series for readers with no physics background, with every claim labelled by how well it is supported. It is a **draft for technical review**, prepared on 26 November 2026.

## From Edition 02 to Edition 03

| Edition 02 | Edition 03 |
|---|---|
| Start Here | Start Here |
| Light and encoding | Volumes 1, 2 and 3 (light, quantum states, Encoding Axies) |
| Geometric encoding | [Volume 4](04-geometric-encoding.md) |
| Controlled transformations | Volumes 5 and 6 |
| Buddy checks and continuity | Volumes 7 and 8 |
| Research lab | [Volume 9](09-research-lab.md) and [Appendix 3](A3-sources.md) |
| Intelligent registers | [Volume 10](10-intelligent-registers.md) |
| Experiments and questions | [Volume 11](11-experiments.md) and [Volume 14](14-workbook.md) |
| Glossary | [Appendix 1](A1-glossary.md) |
| Sharing, README | The `README.txt` in the download |
| New in Edition 03 | Volumes 12, 13, 14; Appendices 2, 4, 5, 6; the `code` and `research` folders; the Ledger; an EPUB edition |

## Naming decisions in force

- **EA** (Encoding Axes, "Axies") and **CT** (Controlled Transformation) are the working terms. PTEA and TV are retired.
- **GEA** and the **Buddy System** are the two pillars. **High-dimensional entanglement** is the adopted scientific cornerstone beneath them.
- **State Space Environment (SSE)** is a descriptive term for the whole physical-plus-control stack. It is not a pillar. Dynamic State Geometry (DSG) was suggested as a name for evolving geometric structures and is not used in this library.
- **PQGS** (Photonic Quantum Geometric Superpositions) is a descriptive term inside GEA. It is not a third pillar, and "geometric" does not mean geometric phase.
- **Time** is an external clock in the current design, not an EA.

## How it was checked

- Every derived number was recomputed in code. The Ledger generator stops if one does not match ([Appendix 2](A2-ledger.md)).
- Five example programs reproduce the main numbers with Python alone ([Volume 14](14-workbook.md)).
- Every internal link and table was validated, and every page was rendered at desktop and phone width with no horizontal scrolling.
- The recorded corrections are in [Volume 9](09-research-lab.md), section 9.6.

## What was not checked

- No experiment exists; nothing is [MEASURED].
- Source checks were at abstract level only. The Hacker abstract confirms the 76.2 % fidelity and the π phase but not the transmission, wavelength or bandwidth; the ORCA memory abstract gives no efficiency figures, so the memory-chain inputs remain unconfirmed ([Appendix 3](A3-sources.md)).
- Other cited works were read at abstract level only ([Volume 13](13-wider-field.md)).
- The proof of the joint classical bound awaits independent review.
- The apparatus mapping (A02) is pending.
- The definitions of PKC, DDQT and AIS were recovered from earlier project discussions. They were confirmed by the project owner's publication instructions of 26 November 2026 ([Appendix 1](A1-glossary.md)). AIS-3 remains an undefined research hypothesis.
- Historical audit records were not available for this check. The A03 and A04 labels follow the R30 table and are still to be reconciled (see below).
- Authorship, attribution and licence are recorded in `NOTICE.txt`. The full, unmodified CC BY 4.0 legal code is not included and must be added before public posting.

## Known limits of the format

The pictures are drawn in the web pages and described in words in the Markdown and text files. The PDF contains the drawn pictures. Mathematical expressions are written in plain Unicode text, which any application can display, rather than in a typeset formula format.


---
*(c) 2026 Tyler O'Bryan, where applicable. PhaseKeep Research. Text CC BY 4.0, code MIT. AI-assisted research, documentation and numerical analysis. Draft for technical review.*
