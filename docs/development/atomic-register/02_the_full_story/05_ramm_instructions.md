# 5. RAMM instructions: HOLD, ROTATE, COUPLE

[← Digital reference](04_digital_reference.md) · [Next: integrity checks →](06_iqa.md)

> **In plain words:** a "flip" applied halfway through reverses the register's natural hopping. Run the same time before and after the flip, and the hopping cancels **exactly**, even if the hopping strengths are wrong or uneven. That gives three distinct operations:
> - **HOLD:** stand still, with hopping cancelled.
> - **ROTATE:** deliberately let hopping act.
> - **COUPLE:** interact two registers while hopping cancels.

[ASSUMED] Scope: numerical statements apply only to the stated model, sequence and sampled parameters. They are not hardware guarantees.

## Why the echo is exact [DERIVED]
- **The flip reverses hopping.** Every nearest-neighbour bond joins an even site to an odd site, so the staggered flip S gives **S H_hop S = −H_hop**, whatever the bond strengths or static bond phases.
- **So static hopping cancels:** S e^{−iH t} S e^{−iH t} = **I**.
- **The intended interaction survives.** A *uniform*, internally selective interaction V̄ = v·n_R2,A·n_R2,B commutes with hopping, because hopping preserves the internal state. It also commutes with S. So it accumulates while hopping cancels.

## Simulated confirmation [SIMULATED `echo_combined.py`, `echo_statedep.py`]
| Test | Infidelity |
|---|---|
| Bond +10% on one ring, interaction off | ~1e-13 (exact) |
| Bond +10%, uniform interaction | ~1e-14 (exact) |
| State-dependent hopping J_R2 = 1.3 J_R1, bond +10%, uniform V | ~4e-14 (exact) |
| + 3% site detuning | 2.2e-5 (6.7e-5 with state-dependent hopping) |
| Uneven V, no errors | 1.1e-4 |
| **Bond 10% + uneven V** (with or without detuning) | **~4e-3** (about 30× the sum of the separate effects) |

## The three instructions (PROPOSED primitives)
| Instruction | Function | Protection condition |
|---|---|---|
| **HOLD** | Preserve spatial information | Balanced echo; static bipartite hopping |
| **ROTATE** | Deliberate spatial logical-Z evolution | Needs calibrated hopping and duration |
| **COUPLE** | Conditional inter-register phase | Balanced echo; **uniform, internally selective** interaction |

**Limitations:**
- **HOLD isn't memory.** It cancels hopping only. Decay, dephasing and internal drift are untouched.
- **In these primitive definitions, HOLD cancels the hopping used by ROTATE.** A proposed scheduler must distinguish these objectives; composed or partially refocused controls have not been excluded.
- **Uneven interaction breaks exactness** (ch. 7).
- **Site detuning isn't cancelled.**
- **Time-dependent hopping and finite pulses add errors** (ch. 8, 9).

**Operation-dependent register selection** by PKC/DDQT is PROPOSED. Present it as an extension of established noise-aware compilation (UNVERIFIED reference; see sources).

## Earlier supporting results
- **Single-ring tolerance:** leakage ≈ 0.1·x² for a site, bond or phase error of size x. It stays bounded over time because of the hopping gap. Bond errors *grow* into a logical phase over time when not echoed: 2e-3 at 1% over T = 10/J. [SIMULATED `ref_tolerance.py`]
- **Pulse shaping and echo in the two-ring gate:**
  - sin² pulses cut final leakage by about 10⁴ at equal gate time
  - a 2-segment echo raises F_avg from 98.22% to 99.989%
  - synchronized composite flips (4 segments) recover 99.98868% with hopping left on

  [SIMULATED `two_ring_shaped.py`, `two_ring_echo.py`; composite: REPORTED, independent run]
