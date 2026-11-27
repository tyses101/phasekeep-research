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

## Publication completed — 2026-11-27

[GitHub development pre-release](https://github.com/tyses101/phasekeep-research/releases/tag/research-development-v1.0), tag `research-development-v1.0`, targets `aaf0f6ce164e22cb8721d6901ad85f2e9fc887eb`. All 16 assets were downloaded without authentication and matched their local SHA-256 hashes. All eleven original checkpoint ZIP hashes matched the committed inventory; all 196 internal distribution manifest entries passed. These are artifact-integrity checks, not independent scientific reproduction.

Complete ZIP SHA-256: `83f5a82c8c283c3700225a3106ec4cfecf73ca8fc07266830dc88c1f7998e96c`.

[Release checksum manifest](https://github.com/tyses101/phasekeep-research/releases/download/research-development-v1.0/RESEARCH-DEVELOPMENT-V1.0-SHA256SUMS.txt).

[Zenodo version DOI: 10.5281/zenodo.24589667](https://doi.org/10.5281/zenodo.24589667). [All-versions DOI: 10.5281/zenodo.24589666](https://doi.org/10.5281/zenodo.24589666). Zenodo archives the tagged repository source snapshot, not the sixteen separately attached GitHub assets. Its inherited Revision H title/version were corrected to the development release. This DOI is not a separate DOI for the original Revision H release.

The release notes and asset manifest were reconstructed from the verified local files and handoff; the supplied verification report and original archives were preserved. Its pre-publication statements remain historical. Revision H remains Latest and unchanged. The public development landing page returned HTTP 200. No new scientific simulation was run.

The stable release remains Edition 03, Revision H (`edition-03-rev-h`). The development release is theoretical and computational research; "V1.0" names the research checkpoint, not product maturity.

## Licence

Text under CC BY 4.0, code under MIT, as set out in the [development README](README.md).
