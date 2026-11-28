# Errata and annotations

**Status: working development record. Corrections are dated, never silent.** Original checkpoint files are preserved byte for byte, including the statements corrected below. Each entry gives the original statement, the correction, and the page where the correction was first made. The identifiers E1 to E4 are the ones used in the original checkpoint pages and are not renumbered. All checkpoint files were packaged on 2026-11-27, so the date column reads the same for each; the "first made in" column gives the order.

## Corrections made inside the checkpoints

| ID or topic | Affects | First made in | Original statement | Correction |
|---|---|---|---|---|
| Wording on "correct results per run" | [V0.4](checkpoints/v0.4.md) section 7 | [V0.5](checkpoints/v0.5.md) section 3 | The Buddy never gives more correct results per run than the same encoding without it. | True only for the rejection-based Pauli model of that page, where the Buddy only removes outputs. It does not apply to error-correcting architectures. |
| Z-type faults and "commute through everything" | V0.5 reply | [V0.6](checkpoints/v0.6.md) section 3 | Z-type errors commute through everything. | A Z-type fault commutes with ZZ, so the ZZ check cannot see it, but it does not commute with every computational operation: through a logical X rotation it becomes a mix of Z and Y. |
| Pauli-frame limit of the V0.5 chain model | V0.5 | V0.6 section 3 | (Not stated.) | The chain model treats a fault as a Pauli frame that stays a Pauli: exact for idle and Clifford segments only. |
| CNOT Hadamard "incompatible with parity" | earlier discussion (before V0.6) | V0.6 section 3 | The CNOT implementation is incompatible with parity. | Relative to a fixed ZZ check its midpoint is amplitude-dependent; relative to the transported check it is a valid code. It is compatible, restricted to a moved check. |
| **E1** | [V0.7](checkpoints/v0.7.md) section 7 | [V0.8](checkpoints/v0.8.md) section 1 | An X fault on axis a "before the Hadamard" is invisible, fidelity 0.29. | True only after the first CNOT. At position 0 the fault is detected with probability 1. A Pauli error leaves a Haar-random logical input with mean fidelity exactly 1/3; 0.29 and 0.32 were 100-sample estimates. |
| **E2** | V0.7 | V0.8 section 1 | Controlled-phase routes 4 versus 1; edge geometry preserves local checks under inter-photon routes. | Computed in V0.8: all four physical controlled-phase pairs preserve both local checks in both geometries; 4 (diagonal, diagonal) and 1 (edge, edge) implement the logical controlled phase. The V0.7 table was right; its tag was stronger than its computation. |
| **E3** | V0.7 | V0.8 section 1 | Mean fidelity 0.826 for a wrong-angle controlled phase. | The 300-sample estimate is replaced by the exact value 1 − 0.3(1 − cos d); at φ = 2.0 it is 0.8248. |
| **E4** | [V0.8](checkpoints/v0.8.md) page and an earlier chat statement | [V0.9](checkpoints/v0.9.md) section 1 | During conversion the verification "must be suspended or follow the transported group" (and, in chat, that no valid check exists). | The first half is too strong. The transported checks exist at every step and read +1 exactly on converted logical states (worst deviation 8.9e-16). What stops being valid is the complete original check set. Whether Buddy can physically measure the intermediate weight-3 checks is open. |
| V0.9 ranking is for uniform Pauli noise only | [V0.9](checkpoints/v0.9.md) section 4 | [V1.0](checkpoints/v1.0.md) section 1 | (Implicit) flagged is best. | Its qubits were generic and noise uniform; under X-bias the ranking reverses. No numerical error was found in V0.9. |
| V0.9 "unusable = rejection" metric | V0.9 section 7 | V1.0 section 1 | Selection by rejection and silent probability per round started. | Not meaningful when rounds can fail to complete. V1.0 separates completion, rejection, heralding and silence. |
| Literature attribution, Majorana | chat statement before V1.0 | V1.0 section 1 | The 2025 X/Z measurement asymmetry was attributed to a newer device. | It belongs to the earlier 2025 device. All Majorana statements remain UNVERIFIED. |

## Mistakes made during construction (fixed before delivery, kept for the record)

- V0.9: an inverted dominance test listed the worst configuration as optimal; a raw-weight versus stabilizer-coset-weight misreport; an over-stated concurrency assertion replaced by a distribution check; "5 times more second-order damage" corrected to about 4 times.
- V1.0: a normal approximation that returned one run for a 41% click probability, replaced by an exact binomial threshold test that reproduces V0.9's 119,829; a silent-damage metric multiplied by completion probability that favoured joint rounds only because they fail more often; a shadowed variable; a float threshold too tight; "970 times" corrected to about 420 times; two page cells.

## Development-layer annotations (2026-11-27)

| Topic | Note |
|---|---|
| Expansion of GEA | The publication instructions write "Geometric Entanglement Architecture". The frozen glossary and all checkpoints use "Geometric Encoding Axies". Neither is changed; the discrepancy is listed in the [register of terms](register-of-terms.md) for the project owner to resolve. |
| NEE to Convergent Entanglement | Terminology transition recorded in the register. Historical documents keep NEE. |
| Reviewer statement qualified: "preparing resources ahead of demand could move probabilistic operations off the active path" | V1.0's circuits show the eight data-touching gates and the interleaved flag gates remain on the active path. See [Active-information versus replaceable-resource exposure](active-vs-replaceable.md). Any DDQT link is a proposed direction requiring source reconciliation. |
| Data-touching versus ancilla-only gate split | Not part of the V1.0 package; added as post-V1.0 annotation [A01](../../annotations/a01-active-exposure/count_gate_exposure.py). |
| Pull request #1 | Merged before this consolidation; content preserved. See [Repository reconciliation](repository-reconciliation.md). |

## Corrections, 2026-11-28

| Topic | Affects | Original statement | Correction |
|---|---|---|---|
| Alternating versus winding phase on larger rings | [Register geometry](atomic-register/02_the_full_story/02_register_geometry.md), "Larger rings"; and the first draft of Edition 04 Volume 18, section 18.4 | On eight sites, "the staggered shift maps ℓ = +1 to +3", and the staggered flip "only works for four sites" | Two different phase patterns coincide on four sites. The **alternating** phase (−1)ʲ is set by the geometry's alternating sites; it shifts modes by N/2, so on eight sites +1 → 5 ≡ −3 and codes such as {0, 4} stay closed [DERIVED]. The **twice-winding** phase e^{2iφⱼ} is set by the desired mode change; it shifts modes by 2, so on eight sites +1 → +3 [SIMULATED `ring_chiral.py`, which used this pattern]. Closure depends on ring size and the chosen modes. **The four-site register's mathematics is unchanged;** the correction concerns only generalizing it to larger structures, where the four-site coincidence must not be assumed |
| Ground-state hopping limitation | Edition 04 Volume 18, section 18.1 (first draft) | "An excitation sitting among ground-state atoms does not hop" | True for the resonant S/P exchange mechanism modelled; other transport mechanisms (for example Rydberg dressing) are not covered by that statement |
| Atoms and orbital angular momentum | Edition 04 Volume 17, section 17.6 (first draft) | A point-like atom cannot hold a twist-like pattern | A single atom does carry electronic orbital angular momentum; what it cannot hold is a phase pattern spread across separate atoms |

## How to report an error

Open a [correction issue](https://github.com/tyses101/phasekeep-research/issues/new/choose). See [Contributing](contributing.md).

## Atomic-register update, 2026-11-28

[PROPOSED] [Read superseded assumptions and corrections](atomic-register/03_reference/evidence_and_failures.md). Model-based development; no hardware demonstration or novelty claim.
