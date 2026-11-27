PhaseKeep Learning Library, Edition 03 (draft)
==============================================

A plain-language book series about the PhaseKeep research proposal: photon
encoding (EA, GEA), controlled transformations (CT), the Buddy System, and
memory loss. No physics background is needed for the main text.

IMPORTANT: PhaseKeep has not built a quantum computer. No PhaseKeep hardware
measurement exists. Every claim carries an evidence tag (DERIVED, REPORTED,
SIMULATED, ASSUMED, PROPOSED, MEASURED, UNVERIFIED, BLOCKED).

WHERE TO START
  Open index.html in any web browser (double-click it). Or open
  PhaseKeep-Learning-Library-complete.pdf. Or read the plain text file.

WHICH FILE FOR WHICH APP
  index.html and 00-... to A4-...html   Web pages. Work offline, no internet,
                                        no scripts, no installs. Any browser,
                                        also screen readers (headings, skip
                                        link, picture descriptions included).
  PhaseKeep-Learning-Library-complete.pdf   One PDF with bookmarks.
  PhaseKeep-Learning-Library.epub           E-reader edition (Apple Books, Kindle apps,
                                            Kobo, Calibre). Figures included as pictures.
  PhaseKeep-Learning-Library-complete.txt   Everything as one plain-text file.
  PhaseKeep-Learning-Library-complete.md    Same, as Markdown (Notion, Obsidian,
                                            GitHub, Word import, any editor).
  markdown/                             One Markdown file per volume.
  ledger.csv                            Every number, its tag and source;
                                        opens in Excel, Sheets, any editor.
  code/                                 Five short Python programs that
                                        reproduce the key numbers (Python 3
                                        only; run:  python3 run_all.py).
  research/                             The project's own scripts, simulation and
                                        component specification (see its README).
  src/                                  The editable source text.
  NOTICE.txt, LICENSE-*.txt             Authorship, attribution and licences.
  build.py, figures.py, make_ledger.py  Rebuild everything (see below).

TECHNICAL NOTES
  All text files are UTF-8 and have ASCII file names. Pictures are inline
  SVG in the web pages and are described in words in the Markdown and text
  files ("Picture description"). Dark mode and print layout are automatic.

REBUILD AFTER EDITING src/
  python3 make_ledger.py     (needs NumPy; recomputes and checks the Ledger)
  python3 build.py           (Python standard library only)
  python3 make_epub.py       (optional; needs pandoc and Playwright)
  python3 make_pdf.py        (optional; needs Playwright and pypdf)

CONTENTS
  Start Here; First Words (a starting glossary); 1 Light; 2 Quantum States; 3 Encoding Axies; 4 Geometric
  Encoding; 5 Controlled Transformations; 6 Two Photons; 7 The Buddy System;
  8 Memory and Loss; 9 The Research Lab; 10 Intelligent Registers;
  11 Experiments; 12 One Photon's Journey; 13 The Wider Field;
  14 Workbook and Code; A1 Glossary; A2 Ledger of Numbers; A3 Sources;
  A4 Math Refresher; A5 Questions and Misconceptions; A6 Edition Notes.

STATUS, AUTHORSHIP AND LICENCE
  Draft for technical review. AI-assisted research, documentation and numerical analysis.
  Author and project originator: Tyler O'Bryan.  Project: PhaseKeep Research.
  (c) 2026 Tyler O'Bryan, where applicable.
  Text, figures and tables: CC BY 4.0 (LICENSE-TEXT-CC-BY-4.0.txt).
  Source code: MIT (LICENSE-CODE-MIT.txt).  Details: NOTICE.txt.
  The full, unmodified CC BY 4.0 legal code is not included; add it before public posting.
  Corrections: GitHub Issues once a public repository exists (none yet; no address is given).
  Sources were checked at abstract level only (see A3).
