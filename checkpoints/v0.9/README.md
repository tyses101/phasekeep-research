# PhaseKeep Tetragon map, Buddy verification v0.9

Question: how reliable is Buddy's own extraction, how do established methods (flagged, verified-ancilla) compare with the conventional local baseline and a cooperative variant, and what should Buddy become before its responsibilities grow? Answer within the model: flagged joint extraction removes first-order silent damage but not second-order, it costs more rejections and more data-damaging fault cases, and with idle faults counted it loses to conventional joint extraction above about p = 1e-3; the cooperative variant tested is not fault tolerant; no configuration wins on every separate metric.

- `docs/buddy-verification-v0.9.md`: the page (evidence-tagged; erratum to v0.8 in section 1; established versus adapted techniques in section 2; what I expected and was wrong about in section 9; limits in section 10).
- `code/buddy_v09_checks.py`: 33 checks, standard library only, about 20 seconds. Run `python3 -I code/buddy_v09_checks.py`; last line `ALL PASS`.
- `CODEX_HANDOFF.md`: what to reproduce and attack.
- `SHA256SUMS.txt`: `sha256sum -c SHA256SUMS.txt`.

Model results only: ideal Clifford gates, Pauli faults, per-location fault probability as a parameter, no photon loss or probabilistic gates. No hardware claim, no advantage claim, no release or DOI claim. IQA stays a provisional working name outside the frozen vocabulary; Buddy's architecture is deliberately left open. Versions 0.1 to 0.8 are preserved unchanged. Separate from Revision H and pull request #1.
