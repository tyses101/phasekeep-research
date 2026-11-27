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

## Publication completed — 2026-11-27

[GitHub development pre-release](https://github.com/tyses101/phasekeep-research/releases/tag/research-development-v1.0), tag `research-development-v1.0`, targets `aaf0f6ce164e22cb8721d6901ad85f2e9fc887eb`. All 16 assets were downloaded without authentication and matched their local SHA-256 hashes. All eleven original checkpoint ZIP hashes matched the committed inventory; all 196 internal distribution manifest entries passed. These are artifact-integrity checks, not independent scientific reproduction.

Complete ZIP SHA-256: `83f5a82c8c283c3700225a3106ec4cfecf73ca8fc07266830dc88c1f7998e96c`.

[Release checksum manifest](https://github.com/tyses101/phasekeep-research/releases/download/research-development-v1.0/RESEARCH-DEVELOPMENT-V1.0-SHA256SUMS.txt).

[Zenodo version DOI: 10.5281/zenodo.24589667](https://doi.org/10.5281/zenodo.24589667). [All-versions DOI: 10.5281/zenodo.24589666](https://doi.org/10.5281/zenodo.24589666). Zenodo archives the tagged repository source snapshot, not the sixteen separately attached GitHub assets. Its inherited Revision H title/version were corrected to the development release. This DOI is not a separate DOI for the original Revision H release.

The release notes and asset manifest were reconstructed from the verified local files and handoff; the supplied verification report and original archives were preserved. Its pre-publication statements remain historical. Revision H remains Latest and unchanged. The public development landing page returned HTTP 200. No new scientific simulation was run.
