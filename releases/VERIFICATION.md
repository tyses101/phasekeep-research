# Independent publication verification

Verification executed from the supplied Revision H ZIP; earlier AI reports were
not treated as test results. Full numerical stdout is in verification-logs/.

| Check | Actual result |
|---|---|
| ZIP integrity, both supplied archives | PASS |
| Revision H checksum manifest | 100/100 PASS; 101 files, only manifest unlisted |
| All original library bytes in repository | 101/101 identical, including every research script |
| Educational runner | All six programs PASS |
| two_tetragons.py separately | PASS |
| Research arithmetic | 71/71 PASS |
| Component specification | All checks PASS; 12 component records regenerated |
| A06 simulation | 19 self-checks PASS; complete 120-row sweep regenerated |
| Ledger | 46 rows; CSV byte-identical |
| Ledger Markdown | Text-identical; only Windows CRLF vs original LF differs in temporary output |
| Internal HTML links and fragments | 420 checked across 23 pages; zero broken |
| Desktop/mobile rendering | 23 pages at each of 1440×1000 and 390×844; zero document overflow/broken images |
| Visual inspection | Desktop index and mobile two-photon page inspected; content readable |
| CITATION.cff | CFF 1.2.0 schema validation PASS |
| .zenodo.json | JSON and required intended metadata checked; no DOI invented |
| Correction issue form | YAML valid; location, revision, explanation and source fields present |
| Official CC BY 4.0 legal code | Retrieved from official text URL, content markers checked, original bytes retained |

The original index displays a minor literal `# index` line; this is retained as
part of the unchanged snapshot and does not block reading or navigation.

## Failures investigated and limits

- The default `python` launcher was a Windows Store alias. Checks used the bundled
  Python runtime with NumPy instead.
- Python urllib received HTTP 403 from the legal-code URL. PowerShell downloaded
  the official plain text successfully; content was independently checked. It is
  not an HTML error page. SHA-256 is recorded in PUBLICATION_NOTES and asset checksums.
- The initial `python -m cffconvert` invocation failed because the package has no
  module entry point; direct `Citation.validate()` schema validation succeeded.
- Regenerated ledger Markdown differs only by operating-system newline encoding.
  The original file and all scientific results were left unchanged.
- Floating-point output comparisons use relative tolerance 1e-10 and absolute
  tolerance 1e-12; detailed maxima are in verification.json. These are platform
  comparison tolerances, not changed scientific acceptance criteria.
- `audit_bundle_r25.py` and `outcome_resolved_herald_r30.py` require the separate
  feasibility bundle absent from these supplied archives. They were not executed
  against a guessed older bundle. Their bytes match the Revision H manifest;
  earlier release-record provenance beyond that manifest is not established here.
- Rendering checks do not constitute comprehensive accessibility certification.
- Secret/private-information inspection is scoped to the intended staged files;
  unrelated computer files, credentials and older archives are not included.

## Scientific limitations remain open

Historical A03/A04 numbering reconciliation; full-text source review; verification
of memory-chain inputs 4%, 12.6%, 0.49 and 23%; independent B03 proof review; B05
archival/DOI completion; experimental validation; nondestructive verification and
computational continuation; and reduced physical cost for equivalent operations.
No hardware measurements, built quantum computer or quantum advantage are claimed.

## Staged-file review

All 126 intended files were reviewed by file list and content-scanned, including
PDF extracted text and EPUB text. No credential patterns, private-key blocks,
local user-directory paths, email addresses or SSN patterns were found.
The staged set consists of the 101 original library files and 25 publication
files. No original ZIP, older revision, personal file or local configuration is staged.
The final publication adds these release notes and the distribution manifest.
