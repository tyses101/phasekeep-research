# PhaseKeep Tetragon map, Buddy verification v0.8

Question: can the same four axes be reorganized to change which errors are detected, without destroying the logical information, and does the change pay? Answer within the model: yes, a 4-gate unitary does it; the joint geometry exposes Z-type noise but not a wrong angle on an in-code gate; whether switching pays depends on the workload and on the conversion's own fault rate.

- `docs/buddy-verification-v0.8.md`: the page (evidence-tagged, with the erratum to v0.7 in section 1 and limits).
- `code/buddy_v08_checks.py`: 48 checks, standard library only, about 5 seconds. Run `python3 -I code/buddy_v08_checks.py`; last line `ALL PASS`.
- `CODEX_HANDOFF.md`: what to reproduce and attack.
- `SHA256SUMS.txt`: `sha256sum -c SHA256SUMS.txt`.

Model results only: ideal gates, Pauli fault model, assumed noise values and gate set. No hardware claim, no advantage claim, no release or DOI claim. Version 0.7 is preserved unchanged. Separate from Revision H, pull request #1 and v0.1 to v0.7.
