# Reproducibility

**Status: working development record, 2026-11-27.** What was run, by whom, and what that does and does not establish.

:::watch The successful execution of all eleven programs is author-side computational validation
Claude wrote the programs and ran them. That checks internal consistency of the models. It is **not independent numerical reproduction**, which remains pending, and it is **not physical validation**, which remains pending.
:::

## Six kinds of validation, kept separate

| # | Kind | State |
|---|---|---|
| 1 | Author-side mathematical derivation | Done within each checkpoint's stated model |
| 2 | Author-side program execution | **Done** for all eleven checkpoints, 2026-11-27 |
| 3 | Regression validation | V0.9 and V1.0 contain regression checks against their predecessors; V1.0 reproduces V0.9's published silent and rejection probabilities within 1% under its generalized engine |
| 4 | Re-execution of an existing implementation | **Done**: the eleven programs, and annotation [A01](../../annotations/a01-active-exposure/count_gate_exposure.py) over the V1.0 circuits |
| 5 | Independent numerical reproduction | **Pending.** Nobody other than the author has written or run an independent implementation |
| 6 | Physical experimental validation | **Pending.** No hardware measurement exists |

## How to reproduce

Requirements for every checkpoint: Python 3, standard library only, no network, no packages. Recorded with Python 3.13.18 on Linux. Run each program from its own `code/` directory, using Python's isolated mode (`-I`), after verifying the manifest:

```sh
cd checkpoints/v1.0
sha256sum -c SHA256SUMS.txt
cd code
python3 -I buddy_v10_checks.py
```

A passing program prints `ALL PASS` as its last line and exits with status 0. Programs for V0 to V0.3 print their parts and `ALL PASS`; V0.4 onward print one `PASS` line per check. Do not edit a program to make it pass. A failing check is a result and should be reported through a [correction issue](contributing.md).

## Index of the eleven checkpoints

| Checkpoint | Source directory and original archive | Command (from `code/`) | Documented checks | Recorded 2026-11-27 |
|---|---|---|---|---|
| [V0](checkpoints/v0.md) | `checkpoints/v0/`, `phasekeep-tetragon-map-v0.zip` | `python3 -I tetragon_map.py` | four parts | exit 0, `ALL PASS`, 4.3 s |
| [V0.1](checkpoints/v0.1.md) | `checkpoints/v0.1/`, `…-v0.1.zip` | `python3 -I tetragon_map.py` | seven parts | exit 0, `ALL PASS`, 33.0 s |
| [V0.2](checkpoints/v0.2.md) | `checkpoints/v0.2/`, `…-v0.2.zip` | `python3 -I tetragon_map.py` | nine parts | exit 0, `ALL PASS`, 31.3 s |
| [V0.3](checkpoints/v0.3.md) | `checkpoints/v0.3/`, `…-v0.3.zip` | `python3 -I tetragon_map.py` | eleven parts | exit 0, `ALL PASS`, 32.8 s |
| [V0.4](checkpoints/v0.4.md) | `checkpoints/v0.4/`, `…-v0.4.zip` | `python3 -I buddy_checks.py` | 26 | exit 0, 26 PASS lines, `ALL PASS`, 0.2 s |
| [V0.5](checkpoints/v0.5.md) | `checkpoints/v0.5/`, `…-v0.5.zip` | `python3 -I buddy_v05_checks.py` | 33 | exit 0, 33 PASS lines, `ALL PASS`, 0.2 s |
| [V0.6](checkpoints/v0.6.md) | `checkpoints/v0.6/`, `…-v0.6.zip` | `python3 -I buddy_v06_checks.py` | 33 | exit 0, 33 PASS lines, `ALL PASS`, 0.7 s |
| [V0.7](checkpoints/v0.7.md) | `checkpoints/v0.7/`, `…-v0.7.zip` | `python3 -I buddy_v07_checks.py` | 33 | exit 0, 33 PASS lines, `ALL PASS`, 8.5 s |
| [V0.8](checkpoints/v0.8.md) | `checkpoints/v0.8/`, `…-v0.8.zip` | `python3 -I buddy_v08_checks.py` | 48 | exit 0, 48 PASS lines, `ALL PASS`, 5.3 s |
| [V0.9](checkpoints/v0.9.md) | `checkpoints/v0.9/`, `…-v0.9.zip` | `python3 -I buddy_v09_checks.py` | 33 | exit 0, 33 PASS lines, `ALL PASS`, 15.9 s |
| [V1.0](checkpoints/v1.0.md) | `checkpoints/v1.0/`, `…-v1.0.zip` | `python3 -I buddy_v10_checks.py` | 29 | exit 0, 29 PASS lines, `ALL PASS`, 23.1 s |

Every manifest (`SHA256SUMS.txt`, four files each) verified OK, and every extracted archive was byte-identical to the delivered folder now in `checkpoints/`. The research question of each checkpoint is on its page and in the [timeline](timeline.md); known limitations are on each page; evidence status is DERIVED inside stated models and ASSUMED for all noise and gate inputs.

Complete records are in `reproduction/execution-logs/` (one record and one unedited standard output per checkpoint) and the archive inventory with sizes and SHA-256 hashes is in `reproduction/ARCHIVE-INVENTORY.md`. The original archives are not committed to Git; see [Downloads](downloads.md).

## What a pass does and does not mean

- It shows the stated numbers follow from the stated model by the stated code, on one interpreter.
- It does not show the model describes a device, that an assumption is true, or that a result is new.
- The checks were written by the author of the results. A bug that a check shares with the model it tests would pass.
- Floating-point tolerances are those inside each program, and no program was changed to obtain a pass.

## Dependencies and missing materials

No third-party package is needed. Missing materials that affect interpretation, not execution: the original DDQT documents; full texts of the cited papers; the separate feasibility bundle that two Revision H research scripts need (not supplied, as the frozen README states).

## The frozen library and the pull request #1 program

The Revision H library has its own reproduction instructions and checksum manifest (100 of 100 files verified in the same session). The pull request #1 program `code/entanglement_organization.py` was run once by Codex as a regression, and was re-run for this consolidation (see the release verification report).
