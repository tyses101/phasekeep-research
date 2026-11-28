# 11. Envelope balance (E7-D)

[← Echo timing](10_echo_timing_E7.md) · [Next: platforms →](12_platforms_G0.md)

> **In plain words:** we tried "notching" the interaction down around each flip while keeping it on otherwise. It didn't help, and the reason turned out more useful than the fix would have been. The uneven interaction slightly shifts the register's energies, and that shift only cancels if the interaction is **equally strong, on average, in both halves of the echo**. Chopping the interaction into equal segments achieves that, and notches don't.

**Scripts:** `code/e7d_notch.py`, `code/e7d_followup.py`. **Data:** `code/results/e7d_*.csv`. **Evidence:** SIMULATED, plus a DERIVED mechanism.

[ASSUMED] Scope: numerical statements apply only to the stated model, sequence and sampled parameters. They are not hardware guarantees.

## The notch grid: negative result, kept
- **Configurations:** 3 profiles × 5 widths × 6 residual depths, at α = 0.5 with symmetric timing.
- **Result:** every configuration gives **1.2e-3 to 2.8e-3**, against **1.4e-5** for symmetric segmented sin².
- **Depth barely matters:** a 50% residual against 0% changes results by less than 2×. Width matters only weakly.

## Factorization check [SIMULATED]
- **Setup:** full notch versus "uneven-only" notch (uniform part left on), with the uneven amplitude matched by the peak factor **1.250**.
- **Result:** final unitaries agree to **6.7e-13**.
- **Meaning:** the uniform interaction factors out exactly. The only difference between the variants is the uneven amplitude.

## Effective scaling exponent p = ln(I_full/I_uneven-only)/ln k
| α | Infidelity ratio | p |
|---:|---:|---:|
| 0.25 | 2.39 | 3.9 |
| 0.5 | 2.43 | 4.0 |
| 1.0 | 2.45 | 4.0 |

Across α, full-notch infidelity also scales as about α⁴. So **notched continuous envelopes show fourth-order, not sixth-order, suppression.**

## Mechanism (proposed, supported) [DERIVED + SIMULATED]
- **The shift:** the uneven interaction shifts code energies at second order, by about δV²/E.
- **Why it can cancel:** E changes sign when hopping reverses, so the shift cancels only if **∫g(t)² is equal over the + and − hopping periods**.
- **What a leftover does:** a residual phase φ ∝ δV² gives infidelity ∝ δV⁴, which is p ≈ 4.

| Envelope | ∫g² imbalance (±) | Infidelity | Leakage |
|---|---:|---:|---:|
| Symmetric segmented | 0.00 | 1.4e-5 | 2.0e-4 |
| Symmetric continuous + notches | −0.95 | 1.8e-3 | 1.3e-3 |
| Flat-top + notches | −0.20 | 1.8e-4 | 2.3e-3 |
| Original timing, balanced continuous + notch | 0.00 | 4.2e-4 | 5.5e-3 |

**Reading the table:**
- **Imbalance drives the coherent error.** Reducing it helps (about 10× from −0.95 to −0.20).
- **Balance alone isn't enough.** Notches are steeper than a full sin² segment and leak.
- **Segmented sin² does everything at once:** it's balanced, zero at every flip, and gentler than the tested notch alternatives.

## Pareto and hardware numbers
- **Symmetric segmented is the Pareto point** among tested envelopes: best fidelity, low leakage, peak factor 1.0.
- **Uneven-only suppression helps by k⁴ ≈ 2.4×,** but can't fix an imbalanced envelope.
- **Slew-rate correction:** an earlier chat estimate of "≈0.8 MHz/µs" was off by 2π. Corrected and verified against the envelope definitions in `e7d_followup.py` (at J_B/h = 1 MHz, mean-interaction slew):

  | Envelope | Max slew |
  |---|---:|
  | Symmetric segmented | **0.126 MHz/µs** |
  | Others tested | 0.11–0.20 MHz/µs |

  [UNVERIFIED] Whether this slew is achievable with adequate fidelity depends on a specified device; no hardware bandwidth qualification was performed.

## Control objectives (supported design objectives, not proven necessary conditions)
1. **Balance** the interaction-envelope moments (∫g and ∫g²) across ± hopping periods.
2. **Suppress the non-commuting (uneven) component** around staggered flips, unless an interaction-aware sequence does as well.
3. **Keep ramps gentle.**
4. **Preserve the intended conditional phase.**
5. **Account for duration, peak strength and switching rate.**
