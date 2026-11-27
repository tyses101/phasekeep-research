# Buddy verification, version 0.7: does verification stay manageable as the computation grows?

Project: PhaseKeep Research. Owner: Tyler O'Bryan. Written by Claude. Separate from Revision H, pull request #1 and checkpoints v0.1 to v0.6. Nothing here has been independently reproduced, and nothing here claims a hardware result or an advantage over any architecture.

Evidence tags: **DERIVED** (follows from the stated model: ideal unitaries, exact Pauli algebra or 16-dimensional state vectors), **ASSUMED** (a noise value or an ensemble I chose as an example), **PROPOSED** (a design idea), **UNVERIFIED** (literature recalled, not read), **MEASURED** (none), **BLOCKED** (needs something I do not have).

Central question: *Can deliberate geometric organization and controlled transformation of photonic entanglement improve the efficiency, controllability, reliability or continuity of equivalent quantum operations?*
Programme question (subordinate): *Can a photonic processor adapt its information geometry, verification requirements and physical execution routes in response to changing operational conditions, while achieving a measurable advantage over conventional architectures?*
The question V0.7 puts to the first: **can computational complexity grow without verification complexity growing in proportion?** The answer below is "sometimes, and which times is a property of the route".

## 1. What the verification variable is (answer to a question asked during this build)

Four things are tracked, and they are separate.

| Item | Meaning | Known before the photon is launched? |
|---|---|---|
| Observable | the property to measure; here a parity such as ZZ (DERIVED: a stabilizer of the code; established quantum theory, not new physics) | yes |
| Expected value | what valid information must give; +1 for the diagonal Tetragon | yes, **including its sign as it is transported** |
| Measured value | what Buddy observed: PASS, FAIL or UNKNOWN | no |
| Verification cost | what obtaining the evidence cost the computation | not quantified here (physical cost fields stay empty, audit item A02) |

Two qualifications that the version 0.6 and 0.7 results make concrete.
1. **The sign can change.** In version 0.6 the route "X via X_a then X_b" transports the check ZZ to -ZZ at the midpoint and back. A register that stored only "+1" would be wrong mid-route. The expected value is part of the transported plan. [DERIVED, v0.6 class B; the v0.7 group tracking carries signs and requires +1 at endpoints]
2. **PASS confirms the checked property only.** Section 3 gives a direct counter-example: a controlled phase with the wrong angle passes both local checks. A "classical verification plan" carried by the Intelligent Register is a PROPOSED use; its sufficiency has to be argued per checkpoint.

## 2. What was done

| Part | Study | Method |
|---|---|---|
| 0 | Pauli-algebra engine validated against explicit matrices on random sequences (2 and 3 axes) | matrices |
| 1 | Transported-check complexity for one Tetragon | exact Pauli algebra |
| 2 | Two Tetragons: local checks during inter-photon operations | 16-dimensional state vectors |
| 3 | 2, 4 and 8 photons: fixed generators versus the transported group | exact Pauli algebra |
| 4 | Non-commuting steps, term growth, equivalent routes | exact Pauli algebra, ASSUMED ensembles |
| 5 | Measure, transport or defer around an excursion out of the code | state vectors |
| 6 | Preparation geometry, criteria kept separate | matrices |
| 7 | Productivity under explicit output-identifiability assumptions | the version 0.5 dynamic programme |

33 checks, run time about 7 seconds, standard library only. Run `python3 -I code/buddy_v07_checks.py`; the last line is `ALL PASS`.

**How to read the numbers.** Term count, support size (axes, photons) and interaction order are *structural proxies*. They are not measurement costs, and no combined score is formed anywhere. Measuring a transported observable by reversing the computational prefix is one possible implementation; it is not shown to be the cheapest, and a many-term observable need not be expensive to measure, nor a one-term observable cheap.

## 3. One Tetragon: when does the transported check get complicated? [DERIVED]

- **Clifford steps** (H, S, CNOT, CZ) keep the transported check a **single Pauli string** (300 random sequences of 12 steps; maximum one term).
- **By construction rule.** Every Pauli that commutes with ZZ (the 6 logical operators of the diagonal Tetragon, outside the check itself) generates rotations of **any angle** that leave ZZ unchanged. So "logical operations built from normalizer generators" never grow the check.
- **The other 8 two-axis Paulis anticommute** with ZZ; a rotation about one of them by a generic angle turns ZZ into **two terms** (cos t times ZZ plus sin t times another string) and returns to one term only at multiples of pi/2.
- With a mixed ensemble of Clifford steps and generic non-commuting rotations (ASSUMED), the mean number of terms rose 1.19, 1.44, 1.71, 2.05, 2.44, 2.86 over six steps; the maximum seen was 9.
- **Measuring by reversing the prefix** equals measuring U S U-dagger exactly (60 random cases). This is an implementation option, not a cost statement.
- **Equivalent routes.** A logical X rotation as one coupled XX rotation, or as CNOT, single-axis X rotation, CNOT, gives the same unitary, keeps one term throughout, and differs in what it needs: one 2-axis rotation generator, versus a 1-axis rotation plus two CNOTs (themselves two-axis operations). The transported check along the second is IZ, IZ, ZZ. Which is "simpler" depends on which cost you count, and that is a physical question this study does not answer.

## 4. Two Tetragons: do local checks survive inter-photon operations? [DERIVED]

- **All four physical controlled-phase routes** (axis a or b of photon 1 with axis a or b of photon 2) commute with **both** local checks and implement the logical controlled-phase on the code. So the number of ways to connect two photons (four) is not paid for with extra verification structure: the same two local checks serve every route.
- **Preserving both checks does not show the intended operation worked.** A controlled phase with the wrong angle (phi = 2.0 instead of pi) passes both checks (odd weight about 1e-16) and has mean fidelity 0.826 with the intended logical operation. A check on the code space cannot see a wrong relative phase inside it. This is the same limit stated for preparation in version 0.6, now shown for an inter-photon gate.
- **Three routes to the same logical CNOT** (photon 1 controls photon 2), all verified up to a global phase:
  - (P) two physical CNOTs, axis a to a and axis b to b;
  - (G) logical Hadamard from generators, controlled phase, logical Hadamard;
  - (T) three generator rotations Z_c, X_t and Z_c X_t.
- **Their verification behaviour differs.**
  - (G) and (T) keep both local checks at **exactly zero odd weight at every sub-step**.
  - (T) needs a generator touching **3 axes across two photons**; (G) needs at most 2-axis generators.
  - (P) leaves the code after the first CNOT: photon 2's check then reads odd with probability equal to the probability that photon 1 is logical 1, an amplitude-dependent reading. After the second CNOT both checks are valid again.
  - A lone physical CNOT between axes of two photons is not a logical gate: photon 2's check reads between 0 and 1 depending on the state.
- **The trade-off this exposes** is between *verification compatibility* and *interaction order*. The route that keeps the checks valid throughout needs the more demanding interaction. That trade-off is the content of the proposed criterion list in section 8, not a ranking.

## 5. Register scaling: 2, 4 and 8 photons [DERIVED within the model]

Random logical sequences of 25 operations (ASSUMED ensemble), tracking (a) the **fixed** local generators transported by the operations and (b) the **minimum-weight basis of the transported group** (the lowest-weight equivalent checks):

| Photons | Route mix | Local checks valid after every step | Fixed generator: max axes, photons | Lowest-weight basis: max axes, photons |
|---|---|---|---|---|
| 2, 4, 8 | compatible routes only | yes | 2, 1 | 2, 1 |
| 2 | with two-CNOT route | no (mid-route only) | 4, 2 | 3, 2 |
| 4 | with two-CNOT route | no (mid-route only) | 8, 4 | 3, 2 |
| 8 | with two-CNOT route | no (mid-route only) | 10, 5 | 3, 2 |

Findings:
1. **Compatible routes keep verification exactly local at any size.** Every local check stays one weight-2 check on one photon, however many photons interact.
2. **Spreading of fixed generators is partly an artefact of which generator you follow.** With the two-CNOT route, the *fixed* generators spread (10 axes over 5 photons at 8 photons), but at every logical-gate endpoint the original local checks are valid again and a weight-2, one-photon check exists. The code space is preserved by a logical gate, so the group is unchanged.
3. **True spreading exists only mid-operation.** Between the two physical CNOTs the lowest-weight basis has weight 3 across two photons: no weight-2 check exists there, at any register size.
4. **Invisible faults do not accumulate per photon.** Of 16^n two-axis Pauli strings, 8^n commute with every local check (brute force for n = 1, 2, 3; formula for any n); 2^n of those are products of the checks (harmless) and 8^n - 2^n are undetected logical errors. Single-axis faults: 6n of them, 4n detected, 2n invisible; the detected fraction is 2/3 at 2, 4 or 8 photons. **Corollary: adding photons does not make a given fault less visible, but it does give the register more places where an invisible fault can be made.** Both statements are true, and the second is not a verification-cost statement.

## 6. Non-commuting steps: how fast does the check grow? [ASSUMED ensemble, 30 steps]

| Photons | Fraction of incompatible steps | Mean terms in photon 0's check | Mean photons touched | Max terms |
|---|---|---|---|---|
| 2, 4, 8 | 0 | 1.00 | 1.00 | 1 |
| 2 | 0.05 / 0.10 | 25.65 / 60.18 | 1.37 / 1.68 | 129 / 247 |
| 4 | 0.05 / 0.10 | 7.82 / 66.48 | 1.37 / 1.70 | 169 / 1389 |
| 8 | 0.05 / 0.10 | 2.50 / 11.93 | 1.15 / 1.45 | 27 / 208 |

Reading it carefully:
- With **no** incompatible steps the check stays one term on one photon, at every size.
- With a few incompatible single-axis rotations the term count can become large. **The values depend on the ensemble I chose, and the decline with photon number is mostly because a random step touches photon 0 less often in a bigger register.** It does not show that bigger registers are easier to verify.
- Terms grow far faster than photons touched. A many-term observable is a statement about the Pauli expansion, not about measurement cost; that separate question stays open.
- **Compatible-only restriction is the controlling design variable**, not the register size.

## 7. Measure, transport or defer around an excursion [DERIVED]

Route: logical Hadamard on the diagonal Tetragon as CNOT(a to b), H on a, CNOT(a to b). The geometry is diagonal, then edge (b = 0 after the first CNOT, check IZ), then diagonal again. Single-axis faults inserted at three points (0: before the first CNOT; 1: after it, just before IZ is read; 2: after H, after IZ was read):

| Fault | at 0: IZ in the middle / ZZ at the end | at 1 | at 2 (IZ already read) |
|---|---|---|---|
| X_a | seen 1.00 / seen 1.00 | 0 / 0 | not reached / 0 |
| X_b | 1.00 / 1.00 | 1.00 / 1.00 | not reached / 1.00 |
| Z_a, Z_b | 0 / 0 | 0 / 0 | not reached / 0 |

(entries are probabilities that the check reads odd; all state-independent.)

1. **Detectability follows the geometry the fault is made in.** X_a is caught if made while the geometry is diagonal (both axes covered) and is **invisible** if made while the geometry is edge (only the idle axis b is covered): in the edge geometry X_a is the logical X, and it passes through the rest of the route into the code space. This is the single-axis 4-of-6 versus 2-of-6 result of version 0.3, now shown inside one route.
2. **Deferring the check costs nothing in detectability here for faults on the idle axis**: X_b is caught by the end check wherever it happened. What deferral changes is the timing of the report and how much computation continues past a fault.
3. **Every Z fault is invisible to both checks at every insertion point.** Invisible is not harmless: X_a or Z_a made before the Hadamard leaves the output in the code (both checks pass) with mean fidelity 0.29 and 0.32 against the intended output. Z_b does nothing there because that axis is in the state |0>.
4. **Correction of a prediction I made earlier in this build**: I expected some Z faults inside the excursion to be seen with a state-dependent probability. They are not, in this route. The first version of two checks failed because my expectation was wrong, not the program; I re-derived the propagation by hand before changing the assertions.

## 8. Preparation geometry: criteria kept separate [DERIVED where stated, PROPOSED as a list]

For each logical gate in each geometry, the generator route is correct and preserves the geometry's own check throughout. Largest single generator: diagonal 1 to 2 axes; edge 1 axis (on the carrier axis).

| Criterion | Diagonal | Edge | Status |
|---|---|---|---|
| Single-axis faults detected by the geometry's own check | 4 of 6 | 2 of 6 | DERIVED |
| Physical CZ routes between two photons | 4 | 1 | DERIVED (v0.3) |
| Largest generator in the gate routes | 2 axes | 1 axis | DERIVED |
| Local checks preserved by every compatible route | yes | yes | DERIVED |
| Encoding capacity | 2 states per photon | 2 states per photon | DERIVED, equal |
| Physical transmission | not assessed | not assessed | BLOCKED (needs hardware) |
| Structural continuity, transformation complexity in hardware terms | not assessed | not assessed | UNVERIFIED |

**The six criteria you listed (encoding capacity, transformation complexity, verification complexity, structural continuity, fault detectability, physical transmission) stay separate. No score is formed.** Three can be partly computed in the model; two (continuity, transmission) need a physical model I do not have. The diagonal geometry buys fault detectability and routing freedom with a larger generator; the edge geometry has the opposite profile. Neither dominates.

## 9. Productivity under two output-identifiability assumptions [ASSUMED parameters]

Eight segments, harmful Z fault rate 0.001, ancilla X fault 0.002, ancilla harmful Z 0.003, loss 0.002. Mode I: wrong outputs are identified and discarded at the end. Mode II: they are not, and every accepted output is used.

| Segment X rate | Mode I: segments per accepted-correct, unchecked | best checked policy | Mode II: wrong share of accepted, unchecked | best checked |
|---|---|---|---|---|
| 0.005 | 8.79 | 8.74 (spacing 2 or 4) | 9.0% | 2.0% (spacing 8) |
| 0.01 | 9.49 | 9.20 (spacing 2) | 15.7% | 2.5% (spacing 4) |
| 0.02 | 10.97 | 10.22 (spacing 2) | 27.1% | 3.4% (spacing 2) |
| 0.05 | 15.89 | 13.96 (spacing 1) | 49.7% | 6.0% (spacing 1) |
| 0.1 | 23.84 | **24.01 (no checked policy beats unchecked)** | 66.5% | 12.5% (spacing 1) |

- **The best spacing depends on the assumption.** At several noise levels the spacing that is best under Mode I differs from the one best under Mode II (0.005: 4 vs 8; 0.01: 2 vs 4; 0.1: 8 vs 1).
- **At high noise (x = 0.1) checking never pays under Mode I, yet it is the only thing that keeps the accepted outputs mostly correct under Mode II.** Whether that counts as benefit depends on whether wrong outputs can be recognised later. This is the identifiable-versus-silently-incorrect distinction you agreed with.
- **Accumulation example (1% fault per checkpoint, 100 checkpoints)**: irreversible rejection gives 36.60% correct accepted, 0% wrong accepted; undetected phase faults give 56.63% correct accepted and 43.37% wrong accepted. Under Mode I the second machine looks better; under Mode II it is the worse one. Numbers come from the stated simplified model.

## 10. Corrections and refinements to earlier statements

- Earlier (v0.5): "Z-type errors commute through everything" was withdrawn in v0.6. v0.7 adds: *every Z fault is invisible to the parity checks*, but invisible is not harmless (section 7 item 3).
- A check "spreading across registers" is an artefact of tracking a fixed generator. For logical gates that preserve the code space, local checks exist at the endpoints; real spreading exists only mid-operation (section 5).
- Preserving a local check is not evidence that the intended operation happened (section 4).
- Term count is not measurement cost (section 2).

## 11. Limits

All gates are ideal. The fault model is independent Pauli faults on axes (the Pauli-frame statements of version 0.5 are exact only for idle and Clifford segments; for rotations the "invisible/detected" statements here are about the transported observable, not about frames). Ensembles and rates are ASSUMED examples. Nothing here is a measurement of any device, a cost, or a comparison with a conventional architecture. The literature (stabilizer transport through Clifford gates, QND parity measurement, verified ancilla preparation, linear-optics gates) is UNVERIFIED: I recalled titles and did not read papers.

## 12. What this suggests for GEA (PROPOSED, not adopted)

1. **Verification compatibility as one selection criterion**, listed next to transmission, transformation complexity and controllability, not combined with them.
2. **Prefer routes whose generators lie in the normalizer of the active check**; they keep verification structurally flat as the register grows.
3. **Treat an excursion out of the code as a scheduled interval** in which the check is moved, deferred or not read, and record which faults are covered in that interval.
4. **Do not use a PASS as proof of the operation.** Add checks that test what the local checks cannot (relative phase), or accept the limit explicitly.

## 13. Next study (suggestion)

Four and eight photons with ensembles drawn from stated circuit families (not random), reporting terms, support and interaction order per family; a physical-cost model for one candidate route pair (P versus G) once hardware assumptions are chosen; a test of the relative-phase gap (what extra check catches the wrong-angle controlled phase).

## 14. Open (not resolved here)

Independent reproduction (see CODEX_HANDOFF.md); literature reading; name checks for PALADIN, Docked Scheduling, the resource-class names, BUD-xx and "information checkpoint"; the third axis ("path, provisionally"); audit items A03 and A04; Zenodo and DOI (nothing claimed); decisions on pull request #1.
