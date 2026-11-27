# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tyler O'Bryan, where applicable
"""Volume 6: controlled-SUM on two four-level registers, kickback and operator Schmidt rank. Plain Python only."""
import cmath, itertools

I = 1j
def w(k): return I ** (k % 4)            # i^k, exact for integer k

def sum_gate(j, k): return (j, (j + k) % 4)

def cp_phase(j, k): return w(j * k)      # controlled-phase i^(jk)

def rank(rows, tol=1e-9):                # rank of a small complex matrix by Gaussian elimination
    m = [list(map(complex, r)) for r in rows]; rk = 0
    for c in range(len(m[0])):
        p = next((r for r in range(rk, len(m)) if abs(m[r][c]) > tol), None)
        if p is None: continue
        m[rk], m[p] = m[p], m[rk]
        for r in range(len(m)):
            if r != rk:
                f = m[r][c] / m[rk][c]
                m[r] = [a - f * b for a, b in zip(m[r], m[rk])]
        rk += 1
    return rk

def main():
    assert sum_gate(2, 3) == (2, 1)
    print("SUM on (2, 3) ->", sum_gate(2, 3))
    # SUM = (I x F^dagger) CP (I x F) acting on basis states: check by direct amplitude calculation
    F = lambda a, b: w(a * b) / 2          # Fourier matrix
    for j, k in itertools.product(range(4), repeat=2):
        # direct: amplitude to land on |j, n> is sum_m conj(F(n, m)) * i^(j m) * F(m, k)
        for n in range(4):
            amp = sum(F(n, m).conjugate() * cp_phase(j, m) * F(m, k) for m in range(4))
            want = 1 if (j, n) == sum_gate(j, k) else 0
            assert abs(amp - want) < 1e-12, (j, k, n, amp)
    print("SUM = (I x F-dagger) CP (I x F): OK")
    # kickback: target in Fourier state B_r, control basis state j -> phase i^(-r j), target unchanged
    for r, j in itertools.product(range(4), repeat=2):
        B = [w(r * k) / 2 for k in range(4)]
        out = [B[(n - j) % 4] for n in range(4)]   # SUM shifts the target index by j
        phase = w(-r * j)
        assert all(abs(out[n] - phase * B[n]) < 1e-12 for n in range(4))
    print("kickback SUM|j>|B_r> = i^(-rj)|j>|B_r>: OK")
    # operator Schmidt rank of a diagonal two-register operator = rank of its 4x4 table of phases
    cp = [[cp_phase(j, k) for k in range(4)] for j in range(4)]
    cpf = [[-1 if (j, k) == (3, 3) else 1 for k in range(4)] for j in range(4)]
    print("operator Schmidt rank: CP =", rank(cp), ", CPF =", rank(cpf))
    assert rank(cp) == 4 and rank(cpf) == 2
    print("a circuit of m CPF gates reaches rank at most 2^m, so CP needs at least 2 (a lower bound only)")
    print("controlled_sum.py: ALL PASS")

if __name__ == "__main__":
    main()
