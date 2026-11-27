# Repository state and pull request #1 reconciliation

**Status: working development record, 2026-11-27.** What was found when this consolidation began, and what was done about it.

## Baseline observed

| Item | Finding | Method |
|---|---|---|
| `main` at the start | `fa7e48d` "Add HDOC development glossary and proposed five-basis investigation" | `git ls-remote`, clone |
| Pull request #1 | **Merged.** Title "Add provisional entanglement organization development material"; head `research-development/entanglement-organization` at `780ca09`; 1 commit, 4 changed files; merged 2026-11-27 08:52:41 UTC by the repository owner (merge commit `24da9cb`) | GitHub REST API once access was available, and git ancestry |
| Branch | `research-development/entanglement-organization` still exists at `780ca09`; it is preserved and untouched | `git ls-remote` |
| Commits on `main` after Revision H | `24da9cb` (merge of PR #1), `654b1da` (library reader), `fa7e48d` (HDOC glossary) | `git log` |
| Tags | `edition-03-rev-h` at `8c39243` | `git ls-remote` |
| Release | One: "PhaseKeep Learning Library — Edition 03, Revision H — Public Technical Review", not a pre-release, marked Latest. Five attached assets: the COMPLETE zip, `REV-H-ORIGINAL-SHA256SUMS.txt`, both licence texts, `ASSET-SHA256SUMS.txt` (the repository page shows seven because it counts two automatic source archives) | GitHub REST API |
| Revision H library | 100 of 100 listed files pass `sha256sum -c`; 101 files in total | `sha256sum -c`, read-only |
| Historical distribution manifest | `releases/DISTRIBUTION-SHA256SUMS.txt` lists 127 files; 125 match and 2 do not (`README.md` and `index.html`). The same two mismatch on `main` before this consolidation, because pull request #1 and the glossary commit edited them after that manifest was written. The manifest is a record of the original distribution and is left unchanged; it is not a statement about the current files | `sha256sum -c`, read-only |
| GitHub Pages | Enabled for the repository; the build source and live content were checked after merge (see the release verification report) | REST API reports `has_pages`; settings endpoint not readable |

## What the consolidation did with pull request #1

- Preserved its content: `docs/research-development.md`, `code/entanglement_organization.py`, the README and landing-page additions.
- Left its branch in place.
- Added only cross-links from the landing page and README, and one dated pointer note in `docs/research-development.md` (that file's existing text is otherwise unchanged).
- Carried its open items into [Open problems](open-problems.md): the SEE, NEE, CPE, EET, IEE naming-conflict search and the A03/A04 numbering reconciliation.
- Re-ran its program (`entanglement_organization.py`): exit 0, `ALL PASS` ([record](../../reproduction/execution-logs/regression-pr1-entanglement_organization.txt)).

## Files changed by the consolidation

Additions: `checkpoints/`, `docs/development/`, `development/`, `reproduction/`, `annotations/`, `tools/build_development_site.py`. Modifications: `README.md`, `index.html` and `docs/research-development.md`, additive links only. The full list and the byte-preservation report are in the release verification report.

## Zenodo and DOI

See [Citing](citing.md). Status unresolved; no DOI is claimed.
