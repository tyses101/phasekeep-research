# PhaseKeep Tetragon map, Buddy verification v0.7

Question: does verification stay manageable as the computation grows and registers interact? Answer within the model: yes for routes built from generators that commute with the check, no automatically for others; which one you get is a property of the route.

- `docs/buddy-verification-v0.7.md`: the page (evidence-tagged, with limits).
- `code/buddy_v07_checks.py`: 33 checks, standard library only, about 7 seconds. Run `python3 -I code/buddy_v07_checks.py`; last line `ALL PASS`.
- `CODEX_HANDOFF.md`: what to reproduce and attack.
- `SHA256SUMS.txt`: `sha256sum -c SHA256SUMS.txt`.

Model results only: ideal gates, Pauli fault model, assumed noise values. No hardware claim, no advantage claim, no release or DOI claim. Separate from Revision H, pull request #1 and v0.1 to v0.6.
