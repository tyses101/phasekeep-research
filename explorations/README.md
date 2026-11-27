# Exploration pack S: exact analyses on top of checkpoint V1.0

**Status: exploratory, post-V1.0, 2026-11-27. Author-side. Not a checkpoint, not V1.1, not a measurement.** Nothing here changes any earlier file. Every script runs with `python3 -I` and prints `ALL PASS` only if all of its own checks pass; each folder holds its recorded execution. All execution is by the same author (Claude) that wrote the scripts, so it is **not independent reproduction** ([Reproducibility](../docs/development/reproducibility.md)).

This pack answers the project owner's open-ended request of 2026-11-27 ("make educated and provable speculation based on all the data we have and anything we might have overlooked"). It was done without separate V1.1 authorization, so it is labelled exploratory: the owner decides whether any of it is adopted into the V1.1 roadmap, and the roadmap's own ground rules still apply (earlier checkpoints preserved; negative results reported; the local geometry kept as the baseline; no hardware advantage claim without a measurement).

Evidence tags as elsewhere in the repository: **DERIVED** (exact on the stated model), **ASSUMED** (a rule or rate I chose and can name), **PROPOSED**, **UNVERIFIED**, **MEASURED** (none), **BLOCKED**.

## What was added

```
explorations/
  README.md                      this page
  run_all.py                     runs every script, checks each verdict, can rewrite the execution records
  common/v10_rounds.py           read-only loader: parses V1.0's circuit builders without running V1.0's checks
  s01-five-mub/ … s12-recovery-charged-completion/        one script, one execution-record.txt (and run-history.txt where a claim was corrected)
```

Run everything: `python3 explorations/run_all.py` (short variants, a few minutes) or `python3 explorations/run_all.py --full` (adds the verified-cat state-vector run of S05, about 7 minutes, and the n = 5 case of S06, about 15 minutes). Standard library plus `numpy` (S01, S03 projector check, S05, S07 to S10; S06 and S11 need only the standard library and the other scripts; S12 needs numpy through S07). Python 3.13, numpy 2.5.3 were used.

## Results

| ID | Question | Headline result | Tag | Run |
|---|---|---|---|---|
| S01 | Five mutually unbiased bases of the 4-dimensional system formed by polarization and OAM (two qubits): how entangled, and what does moving between bases cost? | A complete set of 5 bases has 3 product and 2 maximally entangled bases here, and **at least 8 of the 20 states are entangled for any choice of tensor structure** (sum of purities is 16). 12 of the 20 directed basis maps need an entangling operation (operator Schmidt rank 2), 8 do not. The 20 states form a complex projective 2-design. | DERIVED | s01 |
| S02 | Photon-level distance and the unheralded-loss floor | The local code has photon-level distance 1 in all 15 ways to host its four axes. The joint [[4,2,2]] code has distance 2 only if every axis has its own photon. With two axes per photon the silent probability from unheralded loss is exactly 1 q to first order for the local code and for **all three** joint extraction designs (conventional, flagged, verified cat), so none of them removes V1.0's floor. With one axis per photon the first-order term is exactly 0 (3 q² remains). My expansion agrees with V1.0's printed slopes to 3 % (worst 2.5 %). | DERIVED; the 2.5 % residual is attributed, not tested | s02 |
| S03 | Can a photon with several axes be lost without losing the logical information? | Yes in principle (Singleton bound n − k ≥ 2m) and by certificate: [[6,2]] on 3 photons × 2 axes tolerates the loss of any one photon, **1.5 photons per logical qubit versus 2.0**. The price is check weight: 7.0 data-touching gates per logical qubit per conventional round versus 4.0. | DERIVED (random-search certificates, each verified on the explicit projector) | s03 |
| S04 | Where can offline preparation or Docked Scheduling help? | Only the verified-cat round has ancilla-only gates that are pre-interaction (10 of its 18). The flagged round's 4 ancilla-only gates are interleaved with data gates and cannot be moved off the active path. The saving DS shows (e.g. 16× at s = 0.5) comes from **retry granularity**, not from offline-ness; the real question is how long the data photon waits. | DERIVED on ASSUMED s | s04 |
| S05 | Independent re-implementation of V0.9's numbers (full state vectors instead of Pauli-frame propagation) | Reproduces V0.9's location counts, first-order coefficients and second-order silent coefficients for the local, joint conventional, flagged **and verified-cat** rounds (e.g. 9.902). Categories are branch-independent across the random cat readouts. | DERIVED (second implementation by the same author) | s05 |
| S06 | Minimum two-qubit cost of changing between stabilizer bases | Exact over all ordered pairs for n ≤ 5. The locally-related fraction falls 52 %, 25 %, 9.0 %, 2.55 % (n = 2…5) and is bounded by 6ⁿ/∏(2ⁱ+1), which tends to 0. **My conjecture "maximum cost = n − 1" was true for n ≤ 4 and is false at n = 5 (maximum 5); retracted.** | DERIVED; scope is stabilizer bases only | s06 |
| S07 | What does a heralded gate failure do to the logical information? (exact test on the real V1.0 circuits) | Two models, kept side by side (below). Model A: local never recoverable; joint conventional recoverable only at the first and last gate of each check; **flagged and verified-cat: every failure harmless** because the flag's \|+⟩ masks the partial parity; two axes per photon makes every data-touching failure fatal. Model B (ignores the ancilla): extraction design irrelevant, joint beats local only for s > 1/√3. | DERIVED on ASSUMED failure semantics | s07 |
| S08 | Conversion between local and joint geometry under gate failure | All 24 minimum circuits: both inter-photon failures fatal (loss 1 − s²). A 7-gate circuit (decode each photon, entangle the two information-free axes, re-encode) has only one fatal point, so P(complete before loss) with retry is s, **but only if a failure erases the two axes and not the whole photons**. It implements a different logical Clifford from the 4-gate circuits, and it has more silent-fault locations (S11). | DERIVED on ASSUMED semantics | s08 |
| S09 | What does hosting several ancilla qubits on one photon (V1.0's K) do to S07's result? | The K = 2 flagged round (8 inter-photon gates) has **exactly the conventional round's failure profile** (4 fatal points of 8): the flag is erased with its ancilla. Verified cat: K = 2 (14 gates) keeps 0 fatal points, K = 5 (8 gates) collapses to the conventional profile. | DERIVED on ASSUMED semantics | s09 |
| S10 | Is there a design where the code tolerates losing a whole photon **and** gate failures are harmless? | [[6,2]] on 3 photons × 2 axes with verified-cat extraction: 0 fatal points of 37 under whole-photon erasure (10 of 10 lightest certificates), and the same 0 for 9 further certificates of [[5,1]], [[7,3]] and [[8,4]]. Conventional extraction has 2 to 12 fatal points. That is an observation across 19 certificates in 4 families, not a proof. A negative control with a hosting that puts a logical operator on a photon fires exactly at those photons. Cost for [[6,2]]: 37 inter-photon gates versus 18 for [[4,2,2]]. | DERIVED on ASSUMED semantics; a design lead, not a recommendation | s10 |
| S11 | What does S08's one-fatal-point conversion cost in ordinary faults? | Using V0.8's own conversion fault model (X and Z flip on every axis a gate touches), the engine first reproduces V0.8's stated numbers (8/4, 10/2, 12/0). To first order the 24 minimum circuits have **2** undetected-wrong events per circuit (12 events; **0** if only two-qubit gates can fault); the 192 one-fatal-point circuits of at most 7 gates have **6 to 7** (of 26 events; 6 of 24 at two-qubit locations). So fewer fatal heralded points are bought with more silent faults. The two are different quantities and are deliberately not combined into a break-even. | DERIVED on the V0.8 fault model (ASSUMED) | s11 |
| S12 | How much of S07's "every flagged or cat failure is harmless" survives once recovering the erased axis is charged for? | Process (ASSUMED): a recoverable failure erases one axis, recovery succeeds with probability ρ (a second failure is fatal: any two erased axes of [[4,2,2]] are uncorrectable, checked), then the round is repeated; the local round has no recovery. **Conventional joint never beats the local s⁴, for any s in (0,1), even at ρ = 1** (it comes down to s + s² > s⁴ + s⁷). **Flagged and cat beat the local round iff ρ > 1/(1+s⁴)**. If recovery needs m inter-photon gates that all succeed, the joint round wins only above s = 0.755 (m = 1), 0.863 (m = 3), 0.932 (m = 8), 0.951 (m = 12). If the flagged round's ancilla failures also need recovery the crossovers rise (0.849, 0.918, 0.960, 0.971 for flagged) while the cat round is unchanged. S07's P = 1 is the ρ = 1 limit. The minimum m is **not** established (open). | DERIVED on an ASSUMED process (exact rational arithmetic, enumeration and Monte Carlo cross-checks) | s12 |

## Cross-cutting findings

**1. The answer depends on what a failed gate does, and that is still open (open problem 1).** The exploration does not resolve it; it turns it into a table (below) that a gate-level model or measurement could fill in. The semantics tested are *erasure*: a heralded failure destroys the qubits it acts on (either just those axes, "EraseAxis", or their whole photons, "ErasePhoton"). Erasure is the conservative end of the "destroys the qubits" family: a failure that merely measures the qubits in a known basis is a post-processing of an erasure, so a harmless erasure is also harmless there (argued, not tested). A benign failure (the gate does nothing and is retried) is V1.0's other case and is not affected by anything here.

**2. Two axes per photon is the structural weak point.** It appears in four independent places: the unheralded-loss floor (S02), every data-touching failure being fatal under photon erasure (S07), the conversion gaining nothing from clean axes (S08), and the ancilla co-hosting results (S09). The one geometry where the V1.0 joint code has photon-level distance 2 is one axis per photon (twice the photons). Codes that survive the loss of a 2-axis photon exist (S03) but cost more check weight (S10 puts a number on it).

**3. Extraction design matters for failure recoverability even though it does not matter for the loss floor.** S02 shows the unheralded-loss floor is identical for all joint designs; S07 and S09 show that whether a heralded failure leaves the information intact depends strongly on the design (flag and cat protect only while the ancilla qubits are on separate photons).

**4. Offline preparation helps only the verified-cat round (S04), and conversion is the more fragile primitive (S07, S08).**

**5. "Harmless failure" is a ceiling, and the price of recovery decides whether it is an advantage at all (S12).** S07's P = 1 for the flagged and cat rounds is the limit of free recovery. Charging a recovery that needs m inter-photon gates, the joint round beats the local round only above a crossover per-gate success (0.86 at m = 3, 0.93 at m = 8 for the cat round), and the conventional joint round never does. Below the crossover the local round, which simply loses the information, completes more often. This agrees in direction with the closed-form Model B crossover (s = 0.577) but is not the same quantity and the numbers are not comparable.

### Decision table (computed rows only; fatal points / failable inter-photon gates)

| Design (K = 1 unless stated) | Inter-photon gates | EraseAxis, one axis per photon | ErasePhoton, two axes per photon |
|---|---|---|---|
| Local conventional | 4 | 4 / 4 | 4 / 4 |
| Joint conventional | 8 | 4 / 8 | 8 / 8 |
| Joint flagged | 12 | 0 / 12 | 8 / 12 |
| Joint flagged, K = 2 | 8 | 4 / 8 | not computed |
| Joint verified cat | 18 | 0 / 18 | 8 / 18 |
| Joint verified cat, K = 2 | 14 | 0 / 14 | not computed |
| Joint verified cat, K = 5 | 8 | 4 / 8 | not computed |
| [[6,2]] on 3 photons × 2 axes, conventional | 19 | 0 / 19 | 5 / 19 |
| [[6,2]] on 3 photons × 2 axes, verified cat | 37 | 0 / 37 | 0 / 37 |

"Fatal" means the logical information is not recoverable from what survives at that instant. It is an **upper bound on usable outcomes**: harmless failures still erase qubits that must be rebuilt with further inter-photon gates (S12 charges for this under a stated process), and unheralded loss (S02) is a separate floor that none of this touches. Fatal points are not probabilities; the per-round loss probability is Σ over fatal gates of s^(i−1)(1 − s) (printed in S09).

## What would change these conclusions

Each line is a measurement or fact that would overturn or sharpen a result above. None has been made.

| If … | then … | From |
|---|---|---|
| a failed heralded gate leaves the data photons undisturbed (benign) | S07 to S10 do not apply; V1.0's retry counts (8, 16, 24, 36 attempts at s = 0.5) are the relevant cost | V1.0 |
| a failed gate erases or measures both photons completely (ErasePhoton, two axes per photon) | every data-touching failure of a [[4,2,2]] joint round is fatal, whatever the extraction design. For the conventional round the probability that the information survives is s⁸ against the local round's s⁴, never better for s < 1. The flagged and cat rounds add harmless ancilla-ancilla aborts, which raise their "information survives" figure at low s without completing anything; that figure is a ceiling and must not be read as a win | S07 (F4, B2) |
| the two degrees of freedom of one photon fail independently | the 7-gate conversion halves the fatal points (completion-before-loss s instead of s²) and flagged/cat extraction stay harmless at the baseline hosting | S08, S07 |
| unheralded data loss per gate participation q is of the order of the gate-fault probability p or larger | every round's silent probability is dominated by the same linear floor (exactly 1 q at two axes per photon, S02), so the choice between local and joint changes the silent number only modestly: in V1.0's own table (p = 1e-3) the flagged/local silent ratio is 0.65 at q = 1e-3, 0.83 at q = 1e-2 and 0.65 at q = 5e-2. A first-order estimate q / (0.533 p + q) overstates that ratio at q = 10 p (0.95 versus 0.83) because it omits second-order terms and V1.0's conditioning on no heralded ancilla loss, so I do not give a threshold | S02, V1.0 table |
| the ancilla qubit and its flag share a photon | the flag no longer protects against erased ancillas (same profile as the conventional round) | S09 |
| a gate-level model gives per-gate success s below about 0.58 in the accumulate-erasures model | local beats joint (one axis per photon): crossover s = 1/√3 | S07 (model B only) |
| rebuilding an erased axis needs m inter-photon gates, each succeeding with probability s | the flagged/cat joint round beats the local round only if s^m (1 + s⁴) > 1; the conventional joint round never does | S12 |
| a recovery cheaper than the m = 3 illustrated here exists (for instance a one- or two-gate repair) | the crossover s falls toward 0.75 and the joint advantage widens; this is the single most valuable open question the pack leaves | S12 |

## Mistakes and retractions in this pack

These statements of mine were wrong or over-stated and were caught by the scripts or by review; each is kept visible in the folder's `run-history.txt` or here.

1. **S02**: the first comparison with V1.0's printed slopes failed a 5 % tolerance (cat 5.4 %) because V1.0's column is conditioned on no heralded ancilla loss; fixed by dividing by (1 − q)^(ancilla locations), tolerance 3 %. The remaining 2.5 % is attributed to loss × gate-fault cross terms, **which I did not compute**. A vacuous `or True` check was removed.
2. **S04**: hard-coded unit counts were off by one (145/4713 versus 146/4714); replaced by checking the defining property. A circular check was removed.
3. **S05**: my first parse took V0.9's M3 table instead of M2; random cat readouts crashed the simulator until branches were enumerated.
4. **S06**: the "maximum = n − 1" pattern was falsified at n = 5 (above).
5. **S07**: an earlier single model concluded "extraction design does not matter"; the exact full-state version contradicts that, so both are kept (A and B) and the design-independence statement is limited to B. My first F4 claim ("no failure is recoverable at two axes per photon") was over-stated and my own check failed. The earlier draft was reported to the owner only as a superseded model.
6. **S08**: I claimed no conversion circuit has fewer than two fatal points; the exact search found a 7-gate counterexample (above). A vacuous sub-condition was removed from the check that describes it.
7. **S09**: I claimed the verified cat also degrades at K = 2; it does not (only at K = 5).
8. **S10**: two script bugs (wrong slice of V1.0's op list; phase correction for Y factors) and an over-broad label in the negative control.
9. **Review pass over the whole pack**: four checks that could not fail (S07 G0, S10 E2b and E2c, S11 P2d) were replaced by real conditions; S02's "c1 > 0" checks were made exact (c1 = 1, c2 = 3); a README threshold ("q ≥ 4.8 p") contradicted V1.0's own table and was removed; the README's statement that the joint round never beats the local one for s < 1 held only for the conventional round; and a description of S01 as "two ququarts' worth" was wrong.
10. **S12**: my first "independent" exact check was the closed form's own equations restated; replaced by an exhaustive enumeration of all gate outcomes. A sentence calling m = 3 "the smallest value I could argue is plausible" was an unsupported lower bound; it is now described as illustrative only.

## Relation to the open problems

| Open problem | What this pack adds | Resolved? |
|---|---|---|
| 1. What does a failed heralded gate do to the data? | A tested map from failure semantics to verdicts (S07 to S10), and what recovery has to cost for "harmless" to matter (S12) | **No.** The semantics are assumptions; a gate-level model or measurement is needed |
| 4. Several ancillary axes in one photon | Structural effect of co-hosting on failure recoverability (S09) and the loss floor (S02) | No (correlated loss and control are still unstudied) |
| 5. Conversion under realistic loss and failure | Erasure-type failure (S08) and the silent-fault price of the one-fatal-point circuit (S11); loss not modelled | Partly, under assumptions |
| 6, 10. Scheduling, DS and offline preparation | Which gates can move offline and where the saving comes from (S04) | No (waiting-time loss unmodelled; original DDQT documents not read) |
| 15. Independent numerical reproduction | A second implementation of V0.9's numbers by the same author (S05) | **No.** Still all author-side |
| 18. Non-Pauli noise | Nothing. Every fault model in the pack is a Pauli fault or an erasure | No |

## Suggested follow-ups (PROPOSED; S12 is an exploratory first step on item 1, the others are not started; each needs separate authorization under the roadmap)

1. Find the **minimum recovery circuit** for an erased axis or photon, with its own failures (S12 leaves its gate count m as a parameter and shows the verdict turns on it). "Harmless" in S07 to S10 is an upper bound until this is done.
2. Search for conversion circuits that realize a **chosen** logical Clifford with the fewest fatal points (S08 found that the minimum-fatal circuit induces a different one).
3. A gate-level model of one heralded two-photon interaction with explicit failure outcomes, to replace the erasure assumptions (roadmap priority 2). Failure treated as erasure resembles ideas in fusion-based and linear-optics error correction. **UNVERIFIED: I have not read that literature** (roadmap priority 1), so the resemblance is a pointer, not a citation.
4. Text for the owner to consider adding to the existing development pages (not applied here): the S04 caveat that offline preparation changes only the verified-cat round's ancilla-only gates, to [Active-information versus replaceable-resource exposure](../docs/development/active-vs-replaceable.md) and roadmap row 4.

## Not claimed

No experimental hardware validation, no demonstrated reduction of physical cost, no quantum or efficiency advantage, no independent reproduction, no statement about any real device's failure behaviour. Every probability is a calculation under assumed rates or semantics. The failure semantics (erasure of axes or photons), the hosting rules, the packing of ancilla qubits and the intra-photon-gates-are-ideal rule are assumptions and are named wherever they are used. Stabilizer-basis and Clifford-circuit results say nothing about non-stabilizer bases, continuous-variable or other high-dimensional photonic encodings.

## Licence

The Python scripts are Python programs and so fall under the repository's MIT code licence ([NOTICE.txt](../NOTICE.txt)). Neither NOTICE.txt nor the licence-scope statement in [docs/development/README.md](../docs/development/README.md) names this folder, so the licence of this page and of the record files is **proposed, not assigned**: CC BY 4.0, matching the development pages. The owner decides. Nothing here reproduces third-party material.
