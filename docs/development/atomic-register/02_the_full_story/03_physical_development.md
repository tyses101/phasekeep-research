# 3. Physical development: from photons to atoms

[← Register geometry](02_register_geometry.md) · [Next: digital reference →](04_digital_reference.md)

> **In plain words:** we started with information stored in a single photon's polarization and twist. Photons are hard to store and hard to make interact, so we moved the register into atoms. Along the way several ideas were tried and dropped. They're listed here with the reasons, because the reasons shaped the final design.

[ASSUMED] Scope: numerical statements apply only to the stated model, sequence and sampled parameters. They are not hardware guarantees.

## The sequence, with what each step contributed

| Step | Idea | Outcome | Evidence |
|---|---|---|---|
| 1 | Photonic Tetragon (polarization × OAM ±1) | ±1 OAM pairs share Gouy phase for matched radial modes and propagation parameters. A spin-orbit compensated subspace (\|L,−1⟩, \|R,+1⟩) is invariant under a common axial spin-plus-orbit rotation in the stated convention, but **not** to birefringence | DERIVED |
| 2 | Q-plate | A *generator* of polarization-OAM states, **not** a closed gate on ±1 (a suitably tuned q = 1/2 plate shifts OAM by ±1 according to spin, and can map +1 → +2) | DERIVED |
| 3 | Rydberg qutrit paper (Jiao et al. 2025) | A stored photon, then three Rydberg levels prepared by microwave (60S–59P–59S chain). **Not** storage of an incoming encoded qutrit. g⁽²⁾(0) = 0.45 | REPORTED (paper, Sections I–IV read) |
| 4 | Atomic "matter Tetragon" (electron × nuclear spin, J = I = ½) | Concurrence of the m = 0 eigenstates = 1/√(1 + (b/A)²). The field selects exchange (SWAP-type) versus Ising (CZ-type) gates. m = 0 clock states are first-order field-insensitive | DERIVED |
| 5 | Ensemble register: internal × spin-wave OAM | Microwave + Raman control is **incomplete** (10/15) and **leaks** (B, C → ±3). Superseded | SIMULATED `lie_check.py`, `confine_robust.py` |
| 6 | Energetic confinement Δℓ² | Fixes leakage (1/(1+16Δ²) envelope) but leaves a phase error ∝ 1/Δ and is still not universal. **No physical source for ℓ-dependent energy was specified in this frozen-ensemble model.** Superseded | SIMULATED `confine_robust.py` |
| 7 | Four-site ring of individual atoms | Phase-pattern flips are exact. Universality needs **hopping** (7 → 63) | SIMULATED `ring_lie.py` |
| 8 | Synthetic flux | At flux 2π the "chiral" splitting is a **relabelling**: the code states carry no current. The tested non-trivial flux (π) gives current and energy splitting. Zero-flux degenerate travelling modes can also carry current; flux is not required for circulation itself. The standing-wave code needs no flux | SIMULATED `ring_gauge.py` |
| 9 | Asymmetric hopping between rings | Hopping ratios 1 and 2 leak **completely**. Ratio about 1.5 works (frequency planning) | SIMULATED `two_ring.py` |
| 10 | Inter-ring conditional interaction | State-dependent (R2–R2) interaction. Its average is the intended gate, and its spatial unevenness is the error | SIMULATED `two_ring*.py` |

## Superseded assumption, flagged clearly
**The single-excitation picture of hopping was oversimplified.** Resonant dipolar exchange works with **all ring atoms in Rydberg states**: an nS background with an nP excitation that hops. A Rydberg excitation among ground-state atoms does not hop.
- **Decay exposure:** 8 Rydberg atoms during a two-ring gate, not 2. For a 10 µs gate at a 50 µs lifetime, survival is about **19%**, not 66%. [DERIVED from ASSUMED lifetimes]
- **Hopping rates:** the two internal levels likely hop at different rates. Chapter 5 shows this is harmless for HOLD and COUPLE. [SIMULATED `echo_statedep.py`]

## Coherent transfer and shelving (PROPOSED, unverified)
- **The planned cycle:** stable ground-state storage → Rydberg activation → operation → deactivation.
- **What shelving does and doesn't do:** it protects *between* operations, not *during* them. Every gate runs in Rydberg states.
- **Beam geometry:** shelving beams must not imprint site-dependent phases. Perpendicular propagation is one candidate; phase matching or calibrated phase compensation must be established.
- **PK-LMI requirement:** preserve amplitudes, relative phases, inter-axis correlations and external entanglement, with an explicit correspondence table and process-fidelity test.

**Physical feasibility is not established.**
