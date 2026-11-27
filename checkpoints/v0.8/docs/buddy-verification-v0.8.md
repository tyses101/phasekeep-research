# Buddy verification, version 0.8: local versus joint verification geometries, and moving between them

Project: PhaseKeep Research. Owner: Tyler O'Bryan. Written by Claude. Version 0.7 is preserved unchanged as a historical checkpoint; the corrections to it are in section 1 as an erratum. Separate from Revision H, pull request #1 and checkpoints v0.1 to v0.7. Nothing here has been independently reproduced, and nothing here is a hardware result or a claim of advantage over any architecture.

Evidence tags: **DERIVED** (follows from the stated model: ideal unitaries, exact Pauli algebra, 16-dimensional state vectors, exact enumeration or exact Pauli-frame propagation), **ASSUMED** (a noise value, workload or gate set I chose as an example), **PROPOSED** (a design idea), **UNVERIFIED** (literature recalled or only summarized, not read), **MEASURED** (none), **BLOCKED** (needs something I do not have).

Central question: *Can deliberate geometric organization and controlled transformation of photonic entanglement improve the efficiency, controllability, reliability or continuity of equivalent quantum operations?*
Programme question (subordinate): *Can a photonic processor adapt its information geometry, verification requirements and physical execution routes in response to changing operational conditions, while achieving a measurable advantage over conventional architectures?*
The question V0.8 puts: **can the system change which errors it can see, by reorganizing the same four axes, without destroying the logical information, and does the change pay?**

**How to read the numbers.** Gate counts, weights, photon spans, interaction orders and fault-location counts are *structural proxies*, not costs. Probability tables use independent Pauli faults with ASSUMED rates and ideal checks. No combined score is formed anywhere. The local geometry stays the baseline in every table; the joint geometry is never presented as a replacement.

## 0. Summary of what was found

| Question | Answer within the model | Tag |
|---|---|---|
| Can unknown logical information be moved between the local and joint geometries? | Yes, by a unitary: 4 elementary gates (two single-axis Hadamards and two inter-photon CNOTs), found by exhaustive search; all 24 shortest circuits have 2 inter-photon gates. Measurement alone cannot do it | DERIVED |
| What does conversion do to coverage? | It changes coverage of **future** faults only. A fault made before conversion keeps its detectability; mid-conversion the register is in neither code | DERIVED |
| Do the joint checks close the relative-phase gap? | **No for the gap that matters most**: a wrong angle on an in-code rotation passes both joint checks exactly as it passes both local checks. **Yes for Z-type noise that leaves the code**: coherent Z rotations on one axis are detected with probability sin^2(eps/2) and the accepted output is unchanged | DERIVED |
| Is the joint code a superset of the local code's coverage? | No. 8 of the 66 weight-1 or 2 coupling generators are seen only by the local code (cross-photon XX and YY) and 8 only by the joint code | DERIVED |
| Which operations preserve the joint code? | No single elementary gate does. The shortest physical operations are **pairs of controlled-phase gates**, and each pair is exactly a logical controlled phase between the two logical qubits | DERIVED |
| Does joint verification create correlated errors? | Yes in extraction (12 multi-axis data errors from single ancilla faults versus 4) and in conversion (single faults become two-photon faults). The number of **silent** logical cases is the same (4 each): the added damage is of the kind the next joint round flags | DERIVED |
| Does adaptive switching pay? | Depends on the workload. Over simply staying joint: 6.6% fewer accepted-wrong in the base profile, lost at a conversion-fault probability near 2e-4; 62.5% fewer in a strongly X-dominated profile, with a break-even above 1e-2. Over staying local the gain comes from the joint code, not from switching | DERIVED on ASSUMED workloads |

## 1. Erratum to version 0.7

Version 0.7 stays as published. These three corrections (plus one numerical refinement and one convention) are recorded here.

**E1. Insertion point of the X_a fault (page section 7, and the program's printed line).** Version 0.7 said an X_a fault "before the Hadamard" is invisible and has fidelity 0.29. That is true only **after the first CNOT**. Computed here for the route CNOT(a to b), H on a, CNOT(a to b); positions: 0 before the first CNOT, 1 after it, 2 after H.

| Fault | Position | P(final ZZ reads odd) | Mean fidelity with the ideal output |
|---|---|---|---|
| X_a | 0 | **1.000** (detected) | 0.000 |
| X_a | 1 | 0.000 (invisible) | 0.323 |
| X_a | 2 | 0.000 | 0.333 |
| Z_a | 0, 1, 2 | 0.000 | 0.333, 0.341, 0.346 |
| X_b | 0, 1, 2 | 1.000 | 0.000 |
| Z_b | 0 | 0.000 | 0.328 |
| Z_b | 1, 2 | 0.000 | 1.000 (axis b is in the state 0, so nothing happens) |

A logical Pauli error leaves a Haar-random logical input with mean fidelity exactly 1/3 against the intended output; the 0.29 and 0.32 in version 0.7 were 100-sample estimates of that.

**E2. Two rows that version 0.7 did not compute.** "Controlled-phase routes 4 versus 1" was carried from version 0.3, and "edge geometry preserves local checks under inter-photon routes" was asserted by an argument. Both are computed here: of the four physical controlled-phase axis pairs, **all four preserve both local checks in both geometries** (a diagonal gate commutes with Z-type checks), and the number that implement the logical controlled phase is **4 for diagonal-diagonal and 1 for edge-edge** (the other three edge routes touch an idle axis and act as the identity on the code). The version 0.7 table was right; its tag was stronger than its computation.

**E3. The 0.826 fidelity.** It was a 300-sample estimate. For a controlled phase with angle error d and Haar-random logical input the mean fidelity is exactly **1 - 0.3 (1 - cos d)**, because E[p(1-p)] = 3/20 for p the weight of |11>. At phi = 2.0 (d = pi - 2) it is **0.8248**. For d = 0.1 rad the infidelity is 0.15%, for d = 0.6 rad it is 5.2%. The checks are blind to the error at every d; its size depends on d.

**Convention (from your review).** One convention is used throughout this version: *signed observables whose expected value for valid information is +1*. The transported check carries its sign; applying a sign change twice would be an error, and the program tracks signs exactly (XXXX times ZZZZ is +YYYY, verified against matrices).

## 2. The two geometries on the same four axes [DERIVED]

Axes (a1, b1, a2, b2). **Local** checks ZZII, IIZZ (the baseline). **Joint** checks ZZZZ, XXXX (the standard [[4,2,2]] error-detecting code).

| Property | Local | Joint |
|---|---|---|
| Physical axes / logical qubits / independent checks | 4 / 2 / 2 | 4 / 2 / 2 |
| Check weight, photons per check | 2 axes, 1 photon | 4 axes, 2 photons |
| Code distance (smallest logical operator) | 1 | 2 |
| Single-axis faults detected | 8 of 12 (every Z missed) | 12 of 12 |
| Weight-2 Pauli faults detected | 40 of 54 | 36 of 54 |
| Paulis commuting with both checks | 64 of 256 | 64 of 256 |
| of which harmless / undetected logical | 4 / 60 | 4 / 60 |
| Invisible Paulis by weight 1, 2, 3, 4 | 4, 14, 20, 25 | 0, 18, 24, 21 |

- **Capacity and invisible fraction are identical; what is detected moves.** The joint code trades 4 invisible single-axis faults for 4 more invisible two-axis ones (14 to 18) and gives up locality.
- **XXXX is a logical operator of the local code** (it commutes with both local checks and is not a product of them; it is the logical X of photon 1 times that of photon 2). Measuring it on locally encoded data would read logical information. So the joint geometry cannot be reached by adding a measurement, which is why the next section needs a unitary.
- ZZZZ, in contrast, is already the *product* of the two local checks.
- **Literature [UNVERIFIED beyond the title and a summary]:** the pair ZZZZ, XXXX on four qubits is the [[4,2,2]] error-detecting code; I confirmed through a fetch summary (not by reading the paper) that Linke et al., *Fault-tolerant quantum error detection* (arXiv:1611.06946), use it with stabilizers XXXX and ZZZZ and post-selection, and note that one of the two logical qubits in their construction is not fault tolerant. That is consistent in spirit with the extraction results below; I have not established that it is the same statement.

## 3. Conversion between the geometries [DERIVED, ASSUMED gate set]

Gate set (ASSUMED ideal elementary gates, not a hardware statement): H and S on one axis, CNOT and CZ on any axis pair.

**Result.** Breadth-first search over the signed two-check stabilizer groups on four axes (at most 21,420 exist; the search stops at the first depth that reaches the joint group): the shortest path from the local to the joint group is **4 gates**, and no circuit of 3 or fewer exists in this gate set; there are **24** such circuits and every one has **2 inter-photon gates** and leaves every logical operator at weight 2. One of them: H on a1, H on b1, CNOT(a1 to a2), CNOT(b1 to b2). Local logical operators go to joint-code logical operators: X1 to ZZII, Z1 to XIXI, X2 to IIXX, Z2 to ZIZI, and the induced map is a Pauli-to-Pauli map confirmed against matrices.

**Information is preserved** (16-dimensional state vectors): the four local logical basis states go to four orthonormal states inside the joint code space, both joint checks read +1 for any superposition, and the inverse circuit returns arbitrary logical superpositions exactly.

**Coverage profile along the circuit.**

| After | Single-axis faults detected | Check weights | Local checks valid | Joint checks valid |
|---|---|---|---|---|
| start | 8 | 2, 2, 4 | yes | no |
| H a1 | 8 | 2, 2, 4 | no | no |
| H b1 | 8 | 2, 2, 4 | no | no |
| CNOT a1 to a2 | 10 | 3, 3, 4 | no | no |
| CNOT b1 to b2 | 12 | 4, 4, 4 | no | yes |

- **Mid-conversion the register is in neither code.** Verification must be suspended or follow the transported group, and between the CNOTs the best available checks have weight 3.
- **Conversion changes coverage of future faults only.** For all 255 non-identity Paulis, "detected by a local check before" equals "detected by a joint check after": a Z fault made before conversion is still invisible afterwards.
- **Faults during conversion get correlated.** A single-axis fault inserted before the CNOTs reaches the end as a two-axis, two-photon fault (8 of 12 at every position before the first CNOT; 4 of 12 between the CNOTs). Classified by the joint checks at the end: 8 detected and 4 logical when inserted before the CNOTs, 10 and 2 between them, 12 and 0 after.
- The reverse conversion is the inverse circuit.

## 4. Gate compatibility [DERIVED]

**Rotation generators that preserve the checks for any angle**, by weight (nontrivial logical ones only counted separately):

| Weight | Local: commuting (logical) | Joint: commuting (logical) |
|---|---|---|
| 1 | 4 (4) | 0 (0) |
| 2 | 14 (12) | 18 (18) |
| 3 | 20 (20) | 24 (24) |
| 4 | 25 (24) | 21 (18) |

- The 15 non-trivial logical Pauli operators, cheapest representative of each: local has 2 of weight 1 (the Z-bar of each photon), 5 of weight 2, 4 of weight 3, 4 of weight 4. Joint has none below weight 2: 3 of weight 2 inside one photon, 6 of weight 2 across both, 6 of weight 3. **A joint-code logical rotation needs an interaction among at least two axes; a local logical Z rotation needs one.** That is an interaction-order cost on the joint side, kept apart from its coverage benefit.
- **The local code's controlled-phase routes do not preserve the joint code.** Each of the four physical CZ routes changes the joint group. The routes verified in versions 0.3 and 0.7 are specific to the local geometry.
- **No single elementary gate preserves the joint group.** Exhaustive search over sequences of up to 4 gates found 6 sequences of length 2, 96 of length 3 and 982 of length 4 that return the group to itself, reaching 51 distinct logical maps (50 non-identity).
- **The six shortest are pairs of controlled-phase gates**: the three ways to split the four axes into two pairs, in both orders. **Every one induces the same logical action, X1 to X1 Z2, Z1 to Z1, X2 to Z1 X2, Z2 to Z2, with all signs +1: a logical controlled phase between the two logical qubits**, confirmed on the state vectors. So in the joint code a logical CZ costs two physical CZs (each of which alone leaves the code), where in the local code one physical CZ sufficed. Another proxy kept separate, not a score.
- **A logical controlled phase of any angle exists using only joint-preserving generators** (Z-bar1 = ZIZI, Z-bar2 = ZZII, Z-bar1 Z-bar2 = IZZI: weight 2 each, two of them across both photons). It is correct on all four logical basis states and both joint checks stay at odd weight exactly 0 at every sub-step.
- **Transportation of the joint checks:** under joint-preserving operations they do not move; under the local routes, or mid-conversion, the group changes (section 3). The joint checks therefore follow the same rule as the local ones: compatible operations leave them fixed, others force them to move.

## 5. Phase-fault coverage [DERIVED]

1. **Theorem, tested.** Any product of rotations about generators that commute with a code's checks leaves the code space invariant, so **every check of that code passes with probability 1 whatever the angles**. Tested with 25 random logical states and 6 random rotations in each code: worst odd weight below 1e-12 for both. A wrong angle in such a rotation is a logical error that no stabilizer measurement of that code can see.
2. **The wrong-angle controlled phase in the joint code** (phi = 2.0, built from Z-bar1, Z-bar2, Z-bar1 Z-bar2 rotations) passes both joint checks (odd weight about 1e-16) with the same mean fidelity as the local version (0.8248 exact, sampled to within 0.02). **The joint geometry does not close the relative-phase gap for gates implemented by in-code generators.**
3. **Z-type noise that leaves the code is exposed.** A coherent Z rotation by 0.3 on one axis: local code detects it with probability 0 for every input and the unchecked output has mean fidelity 0.9819 (a logical phase error); joint code detects it with probability sin^2(0.15) = 0.0223 for every input, and the accepted output has fidelity 1.000000: the error is projected out. A coherent X rotation is treated identically by both codes.
4. **Neither code is a superset of the other.** Of the 66 coupling generators of weight 1 or 2: seen by both 40; seen only by the **local** code 8 (the cross-photon XX and YY couplings); seen only by the **joint** code 8 (the four single-axis Z rotations and the four same-photon XY and YX couplings); invisible to both 10 (ZZ couplings on any axis pair, and same-photon XX and YY). A crosstalk-type ZZ rotation between one axis of each photon is invisible to both codes.

**What this means for the phase gap.** It splits into two problems that the present results separate cleanly. *Phase noise that leaves the code* can be exposed by choosing a geometry (the joint code does it for single-axis Z). *A wrong angle on an intended in-code operation* cannot be exposed by any stabilizer check of that code, in either geometry; it needs the operational verification you described (reference preparations, equipment monitoring, or a different kind of redundancy). This supports your structural-versus-operational distinction with a proof-level statement rather than an example.

## 6. Extraction resources and correlated errors from the verifier [DERIVED]

Single Pauli faults on the extraction ancilla (ideal data, no flags, ancilla-based extraction with CNOTs):

| | Local (two checks) | Joint (two checks) |
|---|---|---|
| CNOTs per round, photons engaged per check | 4 (2 per check), 1 | 8 (4 per check), 2 |
| Ancilla fault locations x Pauli types | 18 | 30 |
| Data errors of weight 2 or more | 4 | 12 |
| Silent logical errors (invisible to the code) | 4 | 4 |
| of which the report is **not** flipped | 2 | 2 |
| Damaged data with an unflipped report (silent or caught later) | 2 | 6 |

- **Correlation rises, silent damage per fault location does not.** The joint extraction creates three times as many multi-axis data errors, but the same number are silent; the extra ones are caught by a later joint round. A joint round can say PASS and leave data damage that the next round will flag.
- Reordering the four CNOTs does not help: over all 24 orders of each check the count of silent logical damage with an unflipped report is exactly 1 per check, because a weight-2 hook error is a logical operator of the joint code in any order.
- Flag qubits, verified ancillae and fault-tolerant ordering are **not** studied here; they are the known mitigations for exactly this, and the next study should use them.

## 7. Adaptive selection [DERIVED on ASSUMED workloads]

**One checkpoint, independent X and Z faults on each axis (probabilities x, z), ideal check.**

| x | z | Local: accepted-wrong / rejected | Joint: accepted-wrong / rejected |
|---|---|---|---|
| 1e-3 | 0 | 2.0e-6 / 3.99e-3 | 6.0e-6 / 3.99e-3 |
| 1e-3 | 1e-4 | 4.0e-4 / 3.99e-3 | 6.1e-6 / 4.39e-3 |
| 1e-3 | 1e-3 | 3.98e-3 / 3.99e-3 | 1.2e-5 / 7.96e-3 |
| 1e-3 | 1e-2 | 3.91e-2 / 3.99e-3 | 5.9e-4 / 4.26e-2 |

- **X noise only:** the joint code accepts about **3 times** as many wrong outputs (6 invisible pair faults versus 2 at leading order in x^2) at the same rejection to first order. The local code is lower in accepted-wrong at no more rejection.
- **Z noise only:** to first order the local code accepts 4z wrong outputs (every single-axis Z is silent) and the joint code **turns exactly that into rejection** (rejected 4z, accepted-wrong of order z^2). Silent damage becomes identifiable discard, one for one.
- **Break-even:** the Z-noise level above which the joint code accepts fewer wrong outputs is z* = 1.00e-8, 1.00e-6, 1.02e-4 for x = 1e-4, 1e-3, 1e-2 (that is, z* is x^2 to within 2%). Above it the joint code accepts fewer wrong outputs and rejects more; the two numbers are reported separately.
- This is the identifiability distinction from version 0.7 in a new form: the joint code is worth its rejections exactly when silently wrong outputs are costly (Mode II) and not otherwise (Mode I).

**Two-block workload with conversion.** Two blocks of 50 segments; ideal check after each block; the adaptive policy converts between blocks; conversion-circuit faults are X and Z flips of probability r on each axis a gate touches (ASSUMED). Columns: accepted-wrong / rejected.

| Profile (x, z per axis per segment) | Fixed local | Fixed joint | Adaptive r=0 | r=2e-4 | r=1e-3 | r=3e-3 |
|---|---|---|---|---|---|---|
| X-dominated (5e-4, 1e-5), then Z-heavy (1e-4, 5e-4) | 8.5e-2 / 0.111 | 6.16e-3 / 0.1910 | 5.76e-3 / 0.1914 | 6.15e-3 / 0.1929 | 7.71e-3 / 0.1989 | 1.16e-2 / 0.2135 |
| Z-heavy, then X-dominated (reverse) | 8.5e-2 / 0.111 | 6.16e-3 / 0.1910 | 5.76e-3 / 0.1914 | 6.73e-3 / 0.1923 | 1.06e-2 / 0.1960 | 2.01e-2 / 0.2050 |
| Strongly X-dominated (2e-3, 0), then Z-heavy | 7.6e-2 / 0.317 | 3.88e-2 / 0.354 | 1.46e-2 / 0.379 | 1.48e-2 / 0.380 | 1.60e-2 / 0.384 | 1.87e-2 / 0.396 |

- **Versus staying local:** the large reduction in accepted-wrong comes from the joint code (at the price of about 8 points more rejection in the first two profiles), **not from switching**.
- **Versus staying joint:** the base profile gains 6.6% in accepted-wrong at a rejection change of +0.0004, and the gain is gone by a conversion-fault probability of about 2.1e-4 (8.3e-5 in the reverse profile). In the strongly X-dominated profile the gain is 62.5% in accepted-wrong and the break-even on accepted-wrong is above 1e-2, **with the rejected share 0.024 higher**. Adaptive switching in this model is a trade of silent damage for discard in blocks where the joint code's extra X-pair invisibility matters, and it earns that only if conversion is much more reliable than the blocks it separates.
- **Not a free gain anywhere in the printed range:** the adaptive policy's rejected share is higher than the fixed joint policy's in all three profiles, and raising r never lowers its rejected-plus-wrong total.

## 8. What I expected and was wrong about

1. I expected 3 logical operators of weight 1 in the local code; there are 2 (Z-bar1 Z-bar2 has weight 2).
2. I expected the joint extraction to have more *silent* logical damage; it has the same count (4 versus 4) over more locations, with 12 versus 4 multi-axis data errors.
3. I expected X-only rejection to be equal across the codes; it is equal only to first order (they differ at x^2).
4. I expected the adaptive policy to reject no more than the fixed joint one; it rejects slightly more in every profile.
These came up as failed assertions during the build; in each case I changed the claim to match the computed value and said so here.

## 9. What this suggests for GEA (PROPOSED, not adopted)

1. **Fault coverage as a separate selection variable**, next to computational efficiency (interaction order, gate counts) and verification efficiency (check weight, photons per check, extraction fault locations). Three columns, not a score.
2. **The local code stays the baseline**; the joint code is a candidate for blocks where silent Z damage dominates and where wrong outputs cannot be identified afterwards.
3. **Treat conversion as a scheduled interval** in which verification is suspended or follows the transported group, with the correlated-fault propagation of section 3 recorded.
4. **Do not expect geometry to fix a wrong angle**: that needs operational verification (reference preparations, equipment monitoring, or other redundancy), and the program now shows that no stabilizer choice can supply it.

## 10. Limits

All gates and conversions are ideal elementary gates from an ASSUMED set; nothing says a photonic platform provides them. Extraction is studied without flags or verified ancillae. Noise is independent Pauli faults with ASSUMED rates; checks are ideal in the workload model; the conversion-fault model is one example. Gate counts, weights, photon spans, interaction orders and fault-location counts are structural proxies. The literature on [[4,2,2]], stabilizer propagation and fault-tolerant extraction is UNVERIFIED; one source was summarized, not read. Nothing here concerns the physical cost of any check or conversion, and nothing is a comparison with a conventional architecture.

## 11. Next study (suggestion)

(1) The extraction of the joint checks with flags and verified ancillae, to see whether the silent cases fall to zero and at what resource cost; (2) a search for the cheapest conversion under restricted gate sets (no S, only inter-photon CZ and single-axis H, say); (3) named circuit families on 4 and 8 photons under each geometry, in terms of the proxies kept separate; (4) the operational-verification study (reference preparations) as the answer to the in-code wrong-angle gap.

## 12. Open (not resolved here)

Independent reproduction (see CODEX_HANDOFF.md); literature reading; name checks for PALADIN, Docked Scheduling, the resource-class names, BUD-xx and "information checkpoint"; the third axis ("path, provisionally"); audit items A03 and A04; Zenodo and DOI (nothing claimed); decisions on pull request #1.
