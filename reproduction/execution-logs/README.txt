Execution records for the eleven checkpoint programs, 2026-11-27.

<checkpoint>.record.txt   what was run and what came back: archive size and SHA-256, interpreter,
                          manifest check, byte comparison of the extracted archive with the delivered
                          folder, command, exit status, elapsed seconds, last output lines.
<checkpoint>.stdout.txt   the program's complete standard output, unedited.

The line "FAIL_markers=" in a record counts occurrences of the letters FAIL or the word Traceback in the
program output. Buddy checks print FAIL as a verdict label and "failure" appears in descriptions, so a
nonzero count is not a failed check. No program wrote to standard error, and every program printed
ALL PASS as its last line. PASS_lines counts lines that contain the word PASS, including the final line.

These are author-side executions by Claude. They are not independent reproduction.

regression-*.txt          re-execution on 2026-11-27 of the pull request #1 program
                          (code/entanglement_organization.py) and two Revision H example programs
                          (library/code/run_all.py, library/code/two_tetragons.py), each from a scratch
                          copy, python3 -I. All three exited 0 with ALL PASS. These programs are not changed.
