# Volume 14: Workbook and Code

## What you will learn

By doing: exercises on every main idea, with answers at the end, and five short programs that reproduce the key numbers of this library on your own computer.

## 14.1 Run the numbers yourself

The `code` folder holds five programs. They need only **Python 3** and nothing else (no NumPy, no internet). Open a terminal in the `code` folder and run:

```
python3 run_all.py
```

Each program checks its own results and prints ALL PASS, or stops with an error naming the failed check.

| Program | Reproduces |
|---|---|
| `hypercube_counts.py` | Corners, edges, squares and cubes (Volume 4) |
| `tetragon.py` | Waveplate, mirror and rotation on the four addresses; edge versus diagonal blends (Volumes 3 to 5) |
| `controlled_sum.py` | SUM, the Fourier construction, kickback and operator Schmidt ranks (Volume 6) |
| `herald_reliability.py` | Herald probability, reliability, a random simulation, reuse economics (Volume 7) |
| `memory_thresholds.py` | The classical bound, thresholds, chain and filter tables (Volume 8) |

A taste of the memory program:

```
def fidelity(eta, v=0.0, nbar=0.25):
    return (1 + v + nbar * (1 - math.sqrt(eta)) ** 2) ** -4

def threshold(nbar):
    return (1 - 1 / math.sqrt(1 + nbar)) ** 2
```

::: watch
A program that prints ALL PASS has confirmed the **arithmetic and the model**. It has not confirmed anything about a laboratory.
:::

## 14.2 Exercises

### Volumes 1 and 2: light and states

1. Two ideal polarizers are 60° apart and the light entering the first is already polarized along it. What fraction of the intensity gets through the second? (Use Malus's law, I = I₀ cos²θ.)
2. A twist −1 beam reflects off two mirrors. What is its twist afterwards?
3. A photon is in the state (3|H⟩ + 4i|V⟩)/5. What are the probabilities of H and V?
4. What is the best average fidelity of measure-and-resend for hidden random states in d = 3 and d = 8?
5. How many real numbers specify a pure state of 8 levels?

### Volumes 3 and 4: addresses and geometry

6. Which addresses are H with twist +1 and V with twist +1?
7. A device flips only polarization. Where does 11 go?
8. For a register with 5 binary axes, how many corners, edges, square faces and cubes are there?
9. Is (10 + 11)/√2 separable? What are its Schmidt weights?
10. Is (00 + 10)/√2 separable?

### Volumes 5 and 6: operations

11. A photon in H, +1 meets a mirror and then a half-wave plate at 45°. Which address does it end in?
12. An edge blend (|−1⟩ + |+1⟩)/√2 is rotated by φ = π/2. What is the new state, up to a global phase?
13. Compute SUM on the pair (3, 2).
14. What is the phase i^(jk) for j = 3, k = 2?
15. Gates that each succeed with probability 1/8 are used five times in a row, all required to succeed, and the successes are independent. What is the overall probability?

### Volumes 7 and 8: checking and memory

16. With the reconstruction's probabilities, how many heralds, valid outputs and false heralds do you expect from 2,000 attempts?
17. What is the joint classical bound for n̄ = 0.5, and the noiseless threshold efficiency?
18. A chain has internal efficiency 5 %, converters 0.6 and a filter of 0.5. Total efficiency? Does it pass the noiseless threshold at n̄ = 0.25?
19. Explain in one sentence why "37.5 %" is the wrong answer to "what is the herald reliability?"

### Volumes 9 to 12: judgement

20. Which evidence tag fits "I reran the script and got the same output"? Which fits "the published paper reports 1/8"?
21. A colleague says: "Our model shows the herald is wrong two times out of three, so the published experiment is flawed." What is wrong with that conclusion?
22. Using Volume 12's method, find the joint yield if the memory efficiency is 1.42 % (internal 12.6 %, converters 0.49, filter 0.23).
23. How many tesseracts (4-cubes) does a 6-axis register contain?
24. Is the state (00 + 01 + 10 − 11)/2 separable? Does it have the same measurement probabilities as the all-plus state?
25. Why can three occupied addresses not form a triangle of edges on the square or cube?
26. A mirror turns 00 into 01 and 10 into 11. Why does one mirror suffice for both, and what does that save?
27. Rotations are applied in the line {00, 01} and in the line {01, 11}. Do they commute? What if the lines are {00, 01} and {10, 11}?
28. Why can a single Tetragon photon not demonstrate a computing advantage, whatever geometry is used?
29. Two photons each carry a Tetragon and are in the equal blend "both at 00, both at 01, both at 10, both at 11". How many joint states exist, and how many ebits does the pair hold?
30. A half-wave plate at 45° is placed on photon B only. The pattern was "corresponding". What pattern results, and does the entanglement change?
31. Why does the cyclic rotation pattern need an operation that couples polarization and twist on one photon?
32. A pair is entangled across three addresses per photon, with equal weights. How many ebits?
33. The cyclic pattern can be made from an axis SWAP followed by a single flip. Does that mean it creates entanglement within photon B?

## 14.3 Answers

1. cos²60° = **0.25**.
2. **−1.** Two reflections flip twice.
3. H: 9/25 = **0.36**. V: 16/25 = **0.64**. (The factor i on V is a phase and does not change the probability.)
4. 2/(d+1): d = 3 gives **0.5**; d = 8 gives 2/9 ≈ **0.222**.
5. 2d − 2 = **14**.
6. **01** and **11**.
7. **01.**
8. Corners 32, edges 5 × 16 = **80**, square faces C(5,2) × 8 = **80**, cubes C(5,3) × 4 = **40**.
9. **Separable.** It is V ⊗ (−1 + +1)/√2. Schmidt weights **1 and 0**.
10. **Separable.** It is (H + V)/√2 ⊗ twist −1.
11. Mirror takes H,+1 to H,−1. The half-wave plate then gives V,−1: address **10** (up to a global phase).
12. The relative phase is e^(−2iφ) = e^(−iπ) = −1, so the state is (|−1⟩ − |+1⟩)/√2 (sign convention dependent).
13. (3, (3 + 2) mod 4) = **(3, 1)**.
14. i⁶ = i² = **−1**.
15. (1/8)⁵ = 1/32,768 ≈ **3.05 × 10⁻⁵**.
16. Heralds 0.375 × 2000 = **750**; valid 0.125 × 2000 = **250**; false 0.25 × 2000 = **500**.
17. Bound = (1.5/2)⁴ = **0.3164**. Threshold = (1 − 1/√1.5)² ≈ **3.367 %**.
18. 0.05 × 0.6 × 0.5 = **1.5 %**. It **passes** the noiseless threshold of 1.1146 % (fidelity margin about +0.0122 over the bound, with no noise).
19. Because 37.5 % is the probability that the herald fires; reliability is the fraction of heralds that are valid, 125/375 = 33.3 %.
20. The rerun is a **[[DERIVED]]** or **[[SIMULATED]]** check of the model (or **[[REPORTED]]** if a second party did it); the paper's 1/8 is **[[REPORTED]]**.
21. The result is for **our reconstruction** with **ideal detectors**; it has not been mapped to the published apparatus (A02), and that experiment relies on post-selection, so it is not a refutation.
22. 0.125 × 0.0142 = 0.001775, about **0.18 %**, roughly one run in 563. (This is the row with margin +0.0098 over the bound.)

23. C(6,4) × 2² = 15 × 4 = **60**.
24. **No, it is not separable** (Schmidt weights 0.5 and 0.5). It has **the same** probabilities, 0.25 for each address, as the all-plus state, which is separable.
25. The square and cube graphs are bipartite: any two of three addresses include a pair that differs in two axes (a diagonal), so the three cannot be pairwise adjacent. Three occupied addresses are a group, not a triangle of edges.
26. A mirror flips the twist whatever the polarization, so the two OAM exchanges are the same physical action. It saves hardware (one part instead of two), not computational steps.
27. Lines {00, 01} and {01, 11} share the address 01, so the rotations **do not commute**; order matters. Disjoint lines such as {00, 01} and {10, 11} act on different addresses and **do commute**.
28. Its state is four amplitudes and its operations are 4 × 4 matrices, which a classical computer simulates instantly. Geometry can change the cost of the operations, not what a four-level system can compute.
29. 4 × 4 = **16** joint states. The four equal Schmidt weights give log₂ 4 = **2 ebits**.
30. A half-wave plate flips polarization, which sends B's addresses 0, 1, 2, 3 to 2, 3, 0, 1: the **vertical reflection** pattern. The entanglement does **not** change, because an operation on one photon alone cannot change it.
31. Going from corresponding to cyclic rotation sends 00 to 01 and 01 to 11, so the new polarization depends on the old twist. One independent operation per axis cannot do that. It needs a coupled operation. The program `two_tetragons.py` shows its operator Schmidt rank is 4, the maximum for two two-level axes. That is a statement about the operation not being a product of one operation per axis. It does not measure physical interaction strength, and it does not mean the operation is entangling.
32. log₂ 3 ≈ **1.585 ebits**.
33. **No.** A SWAP of the two axes needs coordinated control of both, but it turns every product input into another product input. It is coupled, not entangling. A controlled phase, by contrast, can entangle.

## Summary

::: key
You can check this library's main numbers with five small programs and a few exercises. Doing so is the quickest way to find out which parts you actually understand.
:::
