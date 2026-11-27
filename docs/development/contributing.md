# Contributing and corrections

**Status: working development record, 2026-11-27.**

Corrections, overclaim reports, missing sources and independent reproductions are welcome, and the project would rather be told about an error than not.

## How to report

1. Open a [correction issue](https://github.com/tyses101/phasekeep-research/issues/new/choose) and fill in the template: where (checkpoint and section, page or file), the kind of comment, and what is wrong or unclear.
2. Say which commit, tag or checkpoint you read.
3. If you re-ran a program, say the interpreter version, the command and the result, including failures.

## What is most useful

- **Independent numerical reproduction.** A reimplementation in another language or library, compared against the checkpoint's published numbers, is the single most valuable contribution. It is pending for all eleven checkpoints.
- **What a failed heralded gate does to the data**, with a source. This decides the feasibility question.
- **Naming conflicts** for the provisional terms in the [register](register-of-terms.md).
- **Source checks:** full-text confirmation or refutation of any entry in [Literature](literature.md).
- **Errors in the mathematics or the evidence tags.** Say which tag you think is wrong.

## How corrections are handled

Original checkpoint files are never edited. A correction becomes a dated entry in [Errata](errata.md) or a new checkpoint, and the original statement stays visible. Corrections to the website pages are made in the Markdown source and the HTML is regenerated with `python3 -I tools/build_development_site.py`.

## Pull requests

Open an issue first. Changes to anything frozen (`library/`, `releases/`, licence files, `NOTICE.txt`, the stable release) are not accepted through pull requests; those need an owner decision recorded in the repository.
