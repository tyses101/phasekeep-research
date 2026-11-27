# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tyler O'Bryan, where applicable
"""Volume 1-5: the Tetragon, its operations, and edge versus diagonal blends. Plain Python only (no NumPy).
Address k = 2*p + t:  p = polarization (0 = H, 1 = V), t = twist (0 = -1, 1 = +1).  Order: 00, 01, 10, 11."""
import cmath, math

NAMES = ["H,-1", "H,+1", "V,-1", "V,+1"]

def apply(m, v):                      # m: 4x4 list of lists, v: list of 4 amplitudes
    return [sum(m[r][c] * v[c] for c in range(4)) for r in range(4)]

def kron2(a, b):                      # a acts on polarization, b on twist (both 2x2)
    return [[a[i // 2][j // 2] * b[i % 2][j % 2] for j in range(4)] for i in range(4)]

I2 = [[1, 0], [0, 1]]
X = [[0, 1], [1, 0]]
HWP45 = [[0, -1j], [-1j, 0]]          # half-wave plate at 45 degrees = -iX on polarization
MIRROR = X                            # a reflection swaps twist -1 and +1

def rotation(phi):                    # image rotation by phi: phase exp(-i*l*phi), l = -1 / +1
    return [[cmath.exp(1j * phi), 0], [0, cmath.exp(-1j * phi)]]

def basis(k):
    v = [0j] * 4; v[k] = 1; return v

def weights(v):
    """Schmidt weights of a 2x2 coefficient matrix [[v0, v1], [v2, v3]] (rows: polarization, columns: twist)."""
    a, b, c, d = v
    g = [[abs(a)**2 + abs(c)**2, a.conjugate() * b + c.conjugate() * d],
         [b.conjugate() * a + d.conjugate() * c, abs(b)**2 + abs(d)**2]]   # M^dagger M
    tr = (g[0][0] + g[1][1]).real
    det = (g[0][0] * g[1][1] - g[0][1] * g[1][0]).real
    disc = max(tr * tr / 4 - det, 0.0)
    l1, l2 = tr / 2 + math.sqrt(disc), tr / 2 - math.sqrt(disc)
    return sorted([round(l1, 12), round(max(l2, 0.0), 12)], reverse=True)

def main():
    # 1. V,-1 (address 10) through a half-wave plate and a mirror becomes H,+1 (address 01), up to a global phase
    out = apply(kron2(I2, MIRROR), apply(kron2(HWP45, I2), basis(2)))
    k = max(range(4), key=lambda i: abs(out[i]))
    assert k == 1 and abs(abs(out[k]) - 1) < 1e-12
    print("V,-1 -> HWP -> mirror ->", NAMES[k], "(amplitude", complex(round(out[k].real, 12), round(out[k].imag, 12)), ")")

    # 2. Edge and diagonal blends
    s = 1 / math.sqrt(2)
    edge = [s, s, 0, 0]; diag = [s, 0, 0, s]
    print("edge blend Schmidt weights    ", weights(edge))
    print("diagonal blend Schmidt weights", weights(diag))
    assert weights(edge) == [1.0, 0.0] and weights(diag) == [0.5, 0.5]

    # 3. Independent operations on each axis never change the weights
    ops = kron2(HWP45, rotation(0.7))
    assert weights(apply(ops, diag)) == [0.5, 0.5] and weights(apply(ops, edge)) == [1.0, 0.0]
    print("independent single-axis operations leave the Schmidt weights unchanged: OK")

    # 4. Rotation gives a relative phase exp(-2i*phi) between twist +1 and -1
    phi = math.pi / 4
    out = apply(kron2(I2, rotation(phi)), edge)
    rel = out[1] / out[0]
    print("relative phase after rotating by pi/4:", complex(round(rel.real, 12), round(rel.imag, 12)), "(expected -i)")
    assert abs(rel - cmath.exp(-2j * phi)) < 1e-12

    # 5. Two quarter-wave plates in a row make one half-wave plate
    qwp = [[1, -1j], [-1j, 1]]
    qwp = [[x * s for x in row] for row in qwp]   # one common form of a quarter-wave plate at 45 degrees
    prod = [[sum(qwp[i][k] * qwp[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    assert all(abs(prod[i][j] - HWP45[i][j]) < 1e-12 for i in range(2) for j in range(2))
    print("QWP x QWP = HWP(45): OK")

    # 6. Same occupied vertices and probabilities, different correlations (Volume 4, section 4.11)
    half = [0.5, 0.5, 0.5, 0.5]; half_minus = [0.5, 0.5, 0.5, -0.5]
    assert all(abs(abs(x) ** 2 - 0.25) < 1e-12 for x in half + half_minus)
    print("all-plus state weights ", weights(half), "(separable)")
    print("one-minus state weights", weights(half_minus), "(maximally non-separable)")
    assert weights(half) == [1.0, 0.0] and weights(half_minus) == [0.5, 0.5]

    # 7. Selective mixing of the diagonal pair 00 and 11 creates non-separability; a global double flip does not
    th = math.pi / 4
    mix = [[0j] * 4 for _ in range(4)]
    mix[0][0] = mix[3][3] = math.cos(th); mix[3][0] = math.sin(th); mix[0][3] = -math.sin(th); mix[1][1] = mix[2][2] = 1
    out = apply(mix, basis(0))
    print("rotate 00 toward 11 by pi/4 ->", [round(abs(x) ** 2, 3) for x in out], "weights", weights(out))
    assert weights(out) == [0.5, 0.5]
    assert weights(apply(kron2(X, X), basis(0))) == [1.0, 0.0]
    print("double flip X(x)X on 00 gives 11, still separable: OK")

    # 8. Rotations in overlapping lines do not commute; rotations in disjoint lines do (Volume 10, section 10.6)
    def pair_rotation(a, b, t):
        m = [[1 if r == c else 0 for c in range(4)] for r in range(4)]
        m = [[complex(x) for x in row] for row in m]
        m[a][a] = m[b][b] = math.cos(t); m[b][a] = math.sin(t); m[a][b] = -math.sin(t)
        return m
    def mul(p, q): return [[sum(p[i][k] * q[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
    def same(p, q): return all(abs(p[i][j] - q[i][j]) < 1e-12 for i in range(4) for j in range(4))
    r_a, r_b, r_c = pair_rotation(0, 1, 0.7), pair_rotation(1, 3, 0.7), pair_rotation(2, 3, 0.7)
    assert not same(mul(r_a, r_b), mul(r_b, r_a))
    assert same(mul(r_a, pair_rotation(2, 3, 0.7)), mul(pair_rotation(2, 3, 0.7), r_a))
    print("rotations in lines sharing an address do not commute; disjoint lines do: OK")
    print("tetragon.py: ALL PASS")

if __name__ == "__main__":
    main()
