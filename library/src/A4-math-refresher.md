# Math Refresher

Just enough to follow the "Go deeper" boxes. You never need this for the main text.

## Complex numbers

A complex number has the form a + bi, where i is the square root of −1, so i² = −1. Its **size** is √(a² + b²). The powers of i cycle: i⁰ = 1, i¹ = i, i² = −1, i³ = −i, i⁴ = 1. That is why four-level systems use i: i^k repeats every four steps.

## Probability from amplitude

If a state is a|H⟩ + b|V⟩, the probability of H is the squared size of a. The probabilities add to one.

::: try
a = 0.6 and b = 0.8. Probabilities? (0.36 and 0.64; they add to 1.)
:::

## Vectors and matrices

A state with d addresses is a column of d amplitudes. An operation is a d × d table of numbers (a **matrix**) that turns one column into another. Applying two operations in a row means multiplying their matrices.

The swap of H and V is the matrix with 0 on the diagonal and 1 off it, called **X**. The matrix **Z** has 1 and −1 on the diagonal. On four levels, Z|j⟩ = i^j|j⟩.

## Tensor products

Two registers together are described by multiplying their state lists. Two four-level registers give 4 × 4 = 16 joint states |j,k⟩. An operation on one register alone is its matrix combined with the identity on the other.

## Modular arithmetic

"(j + k) mod 4" means: add, then keep only the remainder after dividing by 4. So (2 + 3) mod 4 = 1. It is like a clock with four hours.

## Powers and logarithm-free estimates

A loss of 5 % per step leaves 0.95 after one step and 0.95ⁿ after n steps. Survival multiplies, it does not add.

## Binomial counts

C(n, k) ("n choose k") is the number of ways to pick k things from n: C(4, 2) = 6.

## Fourier transform on four levels

The **F** matrix has entries i^(jk)/2. It turns the address basis into a "phase" basis. In Volume 6 it appears inside the construction of SUM.
