# Downloads

**Status: working development record, 2026-11-27.** What can be downloaded now, and what is planned.

## Available now: in this repository

| What | Where | Notes |
|---|---|---|
| Original checkpoint source directories, unzipped | `checkpoints/v0/` to `checkpoints/v1.0/` | Each has `README.md`, `CODEX_HANDOFF.md`, `SHA256SUMS.txt`, `code/` and `docs/`. Unchanged from the original archives. |
| Development documentation (Markdown) | `docs/development/` | Authoritative source. |
| Generated website | `development/` | Built by `python3 -I tools/build_development_site.py`. |
| Execution records | `reproduction/execution-logs/` | One record and one unedited standard output per checkpoint, plus three regression records. |
| Original archive inventory | `reproduction/ARCHIVE-INVENTORY.md`, `reproduction/ARCHIVE-SHA256SUMS.txt` | Names, byte sizes and SHA-256 hashes of the eleven original archives. |
| Annotation A01 | `annotations/a01-active-exposure/` | Post-V1.0 gate-exposure count and its recorded execution. |

To download a single directory, use GitHub's "Download ZIP" for the repository, or clone it.

## Not committed to Git

The eleven original archives (`phasekeep-tetragon-map-v0.zip` to `phasekeep-tetragon-map-v1.0.zip`) are not in the Git tree because the repository ignores `*.zip`. Each one's size and SHA-256 hash is in the [archive inventory](../../reproduction/ARCHIVE-INVENTORY.md), so an archive obtained from any source can be checked against it.

## Development release (separate from the stable release)

A public **development pre-release** named "PhaseKeep Research Development — V0–V1.0 Consolidation", tag `research-development-v1.0`, is planned to carry the eleven original archives, a consolidated distribution, a checksum manifest, a verification report and the licence texts. **Until that release exists and its assets have been downloaded and verified, no downloadable ZIP archive of the checkpoints is claimed to be publicly available.** The release status and its asset hashes are recorded in the [repository reconciliation](repository-reconciliation.md) page once it is made.

The stable release remains Edition 03, Revision H (`edition-03-rev-h`). The development release is theoretical and computational research; "V1.0" names the research checkpoint, not product maturity.

## Licence

Text under CC BY 4.0, code under MIT, as set out in the [development README](README.md).
