# Draft invitations for technical review (edit before posting; check each community's rules on AI-assisted content and self-promotion first)

## Short version (for r/Optics or r/QuantumComputing)

**Title:** Seeking technical review: a draft on organizing high-dimensional photonic entanglement (polarization x OAM), with open questions

I am sharing a draft learning library and verification package for review. It explores encoding a four-level system on one photon (H/V polarization x OAM of +/-1), what two entangled four-level systems look like, and what would be needed to check heralded operations without destroying the photon. It is AI-assisted, contains no experimental measurements, and every claim carries an evidence tag. The numbers come from calculations and simulations on assumed inputs, and several are explicitly unverified.

I would value correction on:
1. Whether our reconstruction of a published heralded gate matches the real apparatus, since in our reconstruction (ideal detectors) the herald is right only one time in three in the worst case.
2. Whether any non-consuming success signal for a heralded output is realistic.
3. Whether the operator-rank argument in Volume 6, section 6.7 (the cyclic correlation pattern needs a polarization-OAM axis SWAP) is right, and whether a practical device exists.
4. A device that mixes OAM -1 and +1 beyond swap or phase.
5. A proof review of the joint classical bound for four-mode memory certification.

Repository: https://github.com/tyses101/phasekeep-research. Issues are open for corrections. I am not claiming an advantage or a built system.
