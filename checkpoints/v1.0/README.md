# PhaseKeep Tetragon map, Buddy verification v1.0

Question: which of the version 0.9 conclusions survive photon loss, probabilistic two-photon gates, biased noise, repeated rounds and destructive photon readout? Answer within the model: fewer than hoped. With destructive readout even the local check needs inter-photon gates (4 versus 8); if a failed gate disturbs the data, joint verification of unknown data is unusable below roughly s = 0.75; unheralded loss sets a silent-error floor that extraction design cannot lower; X-biased noise reverses the version 0.9 ranking in favour of the local geometry; detect-and-reject verification stops being usable at p = 1e-2 over 20 rounds; coherent amplification cuts reference-preparation cost by factors of tens to thousands when the error accumulates coherently.

- `docs/buddy-verification-v1.0.md`: the page (evidence-tagged; mistakes and clarifications in section 1; literature in section 2; what I expected and was wrong about in section 10; limits in section 11).
- `code/buddy_v10_checks.py`: 29 checks, standard library only, about 30 seconds. Run `python3 -I code/buddy_v10_checks.py`; last line `ALL PASS`.
- `CODEX_HANDOFF.md`: what to reproduce and attack.
- `SHA256SUMS.txt`: `sha256sum -c SHA256SUMS.txt`.

Model results only: ideal Clifford gates with Pauli, erasure and loss-like faults; rates, success probabilities, hosting and heralding rules are assumptions; photonic-gate literature seen at abstract level. No hardware claim, no advantage claim, no release or DOI claim. IQA stays a provisional working name outside the frozen vocabulary; Buddy's architecture is deliberately left open. Versions 0.1 to 0.9 are preserved unchanged. Separate from Revision H and pull request #1.
