# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tyler O'Bryan, where applicable
"""Buddy verification, version 0.5: repeated checkpoints, reusable ancilla, path filtering, detect/reject/correct,
temporal validity. Plain Python, no packages.

Evidence: every result is [[DERIVED]] inside the stated model (ideal gates, or the stated independent-Pauli fault model).
Noise values are [[ASSUMED]] sweep values and examples, not measurements. Nothing here says what a device costs.

Conventions are those of version 0.4: axes a, b carry the logical qubit (diagonal encoding, |0>=|00>, |1>=|11>, ZZ=+1),
the Buddy ancilla reads parity by CNOT(a->anc), CNOT(b->anc); report 0 = PASS-like (even), 1 = FAIL-like (odd).
A data "Pauli frame" (fx1, fx2, fz1, fz2) tracks X and Z faults on the two data axes; the output is correct when
fx1 = fx2 = 0 and fz1 = fz2 (ZZ acts as the identity on the code).

Parts
  1. Repeated checkpoints along one computation (exact dynamic programming): accumulation, spacing, selective checking
  2. Reusable (stationary) ancilla across photons: no reset, imperfect reset, ideal reset; combined parity
  3. Path-style parity router: FAIL signal versus silence, loss, UNKNOWN
  4. Detect, reject, correct: the two-axis parity code cannot correct; a three-axis repetition code can correct single flips
  5. Temporal validity of evidence: how long a correct state stays correct (closed form against exact enumeration)
"""
import math, random
from itertools import product
from collections import defaultdict

random.seed(20261127)
results = []
def check(name, ok_):
    results.append((name, bool(ok_)))
    print(("PASS  " if ok_ else "FAIL  ") + name)
def near(a, b, t=1e-12): return abs(a - b) < t
def pr(v, p): return p if v else 1 - p
def frame_ok(f): return f[0] == 0 and f[1] == 0 and f[2] == f[3]

# ---------------------------------------------------------------- v0.4 single-checkpoint model (reimplemented)
def model_v04(x, z, gx, gz, l):
    out = dict(acc_correct=0.0, false_acc=0.0, false_rej=0.0, rej_damaged=0.0, lost=l)
    for fx1, fx2, fz1, fz2, ax, az in product((0, 1), repeat=6):
        w = pr(fx1, x) * pr(fx2, x) * pr(fz1, z) * pr(fz2, z) * pr(ax, gx) * pr(az, gz) * (1 - l)
        ok_ = fx1 == 0 and fx2 == 0 and (fz1 ^ fz2 ^ az) == 0
        accepted = (fx1 ^ fx2 ^ ax) == 0
        key = ('acc_correct' if ok_ else 'false_acc') if accepted else ('false_rej' if ok_ else 'rej_damaged')
        out[key] += w
    out['accepted'] = out['acc_correct'] + out['false_acc']
    return out

# =============================================================== 1. repeated checkpoints
print("== 1. repeated checkpoints along one computation (exact dynamic programming) ==")
def seg(dist, x, z):
    new = defaultdict(float)
    for f, w in dist.items():
        for e in product((0, 1), repeat=4):
            pw = pr(e[0], x) * pr(e[1], x) * pr(e[2], z) * pr(e[3], z)
            new[tuple(a ^ b for a, b in zip(f, e))] += w * pw
    return new
def chk(dist, gx, gz, l, acc):
    new = defaultdict(float)
    acc['interactions'] += sum(dist.values())
    for f, w in dist.items():
        for ax, az, lo in product((0, 1), repeat=3):
            pw = w * pr(ax, gx) * pr(az, gz) * pr(lo, l)
            if lo: acc['lost'] += pw; continue
            g = list(f); g[2] ^= az                       # harmful ancilla Z fault acts as Z on axis a
            if (g[0] ^ g[1]) ^ ax: acc['false_rej' if frame_ok(g) else 'rej_damaged'] += pw
            else: new[tuple(g)] += pw
    return new
def run(xs, z, checks, gx=0.0, gz=0.0, l=0.0):
    """xs: per-segment data flip probability; checks: set of segment indices after which a checkpoint is made.
    Rejected and lost runs stop. Returns outcome probabilities and the expected number of Buddy interactions per run."""
    dist = {(0, 0, 0, 0): 1.0}; acc = defaultdict(float)
    for i, x in enumerate(xs):
        dist = seg(dist, x, z)
        if i in checks: dist = chk(dist, gx, gz, l, acc)
    for f, w in dist.items(): acc['acc_correct' if frame_ok(f) else 'false_acc'] += w
    acc['accepted'] = acc['acc_correct'] + acc['false_acc']
    return acc

# 1a. one segment, one checkpoint reproduces version 0.4 exactly
same = True
for (x, z, gx, gz, l) in [(0.05, 0.0, 0, 0, 0), (0.02, 0.01, 0.003, 0.004, 0.01), (0.2, 0.05, 0.05, 0.1, 0.02)]:
    a = run([x], z, {0}, gx, gz, l); m = model_v04(x, z, gx, gz, l)
    same &= all(near(a[k], m[k]) for k in ('acc_correct', 'false_acc', 'false_rej', 'rej_damaged', 'lost'))
check("one segment with one checkpoint reproduces the version 0.4 model exactly", same)

# 1b. accumulated Buddy-induced faults (x = z = 0, so only the Buddy acts)
okZ = okX = okL = okI = True
for m_ in range(1, 7):
    c = set(range(m_))
    a = run([0.0] * m_, 0.0, c, gz=0.01); okZ &= near(a['false_acc'], (1 - (1 - 2 * 0.01) ** m_) / 2) and near(a['acc_correct'], (1 + (1 - 2 * 0.01) ** m_) / 2)
    a = run([0.0] * m_, 0.0, c, gx=0.01);  okX &= near(a['acc_correct'], 0.99 ** m_) and near(a['false_rej'], 1 - 0.99 ** m_)
    a = run([0.0] * m_, 0.0, c, l=0.01);   okL &= near(a['acc_correct'], 0.99 ** m_) and near(a['lost'], 1 - 0.99 ** m_)
    a = run([0.0] * m_, 0.0, c, gx=0.1);   okI &= near(a['interactions'], sum(0.9 ** k for k in range(m_)))
check("m checkpoints, harmful Buddy Z faults only: false acceptance = (1 - (1-2g)^m)/2 (an odd number of faults), accepted-correct = (1 + (1-2g)^m)/2",
      okZ)
check("m checkpoints, ancilla X faults only: accepted-correct = (1-g)^m and the rest are false rejections of good data", okX)
check("m checkpoints, loss in the interaction only: accepted-correct = (1-l)^m", okL)
check("expected Buddy interactions per run = sum of (1-g)^k: a rejected run stops using Buddy resources", okI)

# 1c. flip noise only, no Buddy faults: what checking at different spacings does
T, x = 8, 0.05
none = run([x] * T, 0.0, set())
end = run([x] * T, 0.0, {T - 1}); every = run([x] * T, 0.0, set(range(T)))
p_even_axis = (1 + (1 - 2 * x) ** T) / 2
check("flip noise only, no checkpoint: the output is correct exactly when each axis has an even number of flips, P = ((1+(1-2x)^T)/2)^2 (flips on the same axis can cancel)",
      near(none['acc_correct'], p_even_axis ** 2))
check("a single checkpoint at the end gives the same accepted-correct probability as no checkpoint; it only removes the 'both axes odd' wrong outputs",
      near(end['acc_correct'], none['acc_correct']) and near(end['false_acc'], ((1 - (1 - 2 * x) ** T) / 2) ** 2))
u_, v_ = (1 - x) ** 2, x ** 2
check("a checkpoint after every segment passes a run only if each segment's flips come in matching pairs, so accepted-correct = ((u+v)^T + (u-v)^T)/2 and false acceptance = ((u+v)^T - (u-v)^T)/2 with u = (1-x)^2, v = x^2 (the undetectable event is a double flip inside one segment)",
      near(every['acc_correct'], ((u_ + v_) ** T + (u_ - v_) ** T) / 2) and near(every['false_acc'], ((u_ + v_) ** T - (u_ - v_) ** T) / 2))
check("with flip noise only, checking every segment lowers false acceptance far below end-only checking and also accepts FEWER correct runs than no Buddy (it discards runs whose flips would have cancelled)",
      every['false_acc'] < end['false_acc'] / 5 and every['acc_correct'] < none['acc_correct'])

# 1d. spacing with Buddy faults: an interior optimum exists (ASSUMED parameters)
print("  spacing sweep, T = 8 segments, ASSUMED x = 0.02, z = 0.001, gx = 0.002, gz = 0.003, loss = 0.002")
print("      spacing  checkpoints  accepted-correct  false acceptance  wrong among accepted  Buddy interactions")
conds = {}
for s in (1, 2, 4, 8):
    a = run([0.02] * 8, 0.001, {i for i in range(8) if (i + 1) % s == 0}, 0.002, 0.003, 0.002)
    conds[s] = a['false_acc'] / a['accepted']
    print(f"      {s:7d}  {8 // s:11d}  {a['acc_correct']:16.4f}  {a['false_acc']:16.5f}  {conds[s]:20.5f}  {a['interactions']:18.2f}")
check("with these assumed parameters the share of wrong outputs among accepted is lowest at an intermediate spacing, not at the densest or the sparsest checking",
      min(conds, key=conds.get) in (2, 4))
bestcheck = run([0.02] * 8, 0.001, set(), 0, 0, 0)
check("with these assumed parameters every spacing lowers the wrong share well below the unchecked error rate (about 27%) while cutting accepted-correct by less than 8% relative to unchecked",
      all(c < 0.05 for c in conds.values()) and bestcheck['acc_correct'] < 0.74
      and all(run([0.02] * 8, 0.001, {i for i in range(8) if (i + 1) % s == 0}, 0.002, 0.003, 0.002)['acc_correct'] > 0.92 * bestcheck['acc_correct'] for s in (1, 2, 4, 8)))

# 1e. selective checking: one sensitive segment (ASSUMED)
xs = [0.005] * 8; xs[3] = 0.1
sel = {}
for name, c in (("end only", {7}), ("after sensitive only", {3}), ("sensitive + end", {3, 7}), ("every segment", set(range(8)))):
    a = run(xs, 0.001, c, 0.002, 0.003, 0.002)
    sel[name] = (a['acc_correct'], a['false_acc'] / a['accepted'], a['interactions'])
print("  selective sweep: segment 4 has flip probability 0.1, the others 0.005 (ASSUMED); z = 0.001, gx = 0.002, gz = 0.003, loss = 0.002")
print("      policy                 accepted-correct  wrong among accepted  Buddy interactions")
for k, (pa, cw, it) in sel.items(): print(f"      {k:22s} {pa:16.4f}  {cw:20.5f}  {it:18.2f}")
check("example where selective checking (after the sensitive segment and at the end) beats both end-only and every-segment checking on wrong-among-accepted, with fewer interactions than every-segment",
      sel["sensitive + end"][1] < sel["end only"][1] and sel["sensitive + end"][1] < sel["every segment"][1]
      and sel["sensitive + end"][2] < sel["every segment"][2])
check("the same example shows a check placed only after the sensitive segment is worse than end-only (later flips go unseen): where to check matters",
      sel["after sensitive only"][1] > sel["end only"][1])

# =============================================================== 2. reusable ancilla
print("== 2. one stationary ancilla serving a stream of photons ==")
def kron_state(p1, p2):
    return {k1 + k2 + (0,): x1 * x2 for k1, x1 in p1.items() for k2, x2 in p2.items()}
def cnot(s, c, t):
    o = {}
    for k, x in s.items():
        k = list(k)
        if k[c]: k[t] ^= 1
        k = tuple(k); o[k] = o.get(k, 0) + x
    return o
def extract(s, a, b, anc): return cnot(cnot(s, a, anc), b, anc)
def rc(): return complex(random.gauss(0, 1), random.gauss(0, 1))
def photon_state(flip):
    al, be = rc(), rc(); n = math.sqrt(abs(al) ** 2 + abs(be) ** 2); al /= n; be /= n
    return {(1, 0): al, (0, 1): be} if flip else {(0, 0): al, (1, 1): be}
def anc_report(s):
    d = defaultdict(float)
    for k, x in s.items(): d[k[4]] += abs(x) ** 2
    assert min(d[0], d[1]) < 1e-12; return 1 if d[1] > 0.5 else 0
def reset(s): return {k[:4] + (0,): x for k, x in s.items()}
ok_none = ok_sum = ok_mask = ok_rst = ok_blank = True
for _ in range(60):
    for f1, f2, f3 in product((0, 1), repeat=3):
        s = kron_state(photon_state(f1), photon_state(f2))
        t = extract(extract(s, 0, 1, 4), 2, 3, 4)                     # no reset between photons 1 and 2
        ok_sum &= anc_report(t) == (f1 ^ f2)
        ok_mask &= (anc_report(t) == 0) if (f1 and f2) else True
        t1 = extract(s, 0, 1, 4); r1 = anc_report(t1)                 # read out and reset after photon 1
        r2 = anc_report(extract(reset(t1), 2, 3, 4))
        ok_rst &= (r1, r2) == (f1, f2)
    s = kron_state(photon_state(0), photon_state(0)); t = extract(s, 0, 1, 4)
    ok_blank &= all(k[4] == 0 for k in t) and all(abs(t[k] - s[k]) < 1e-12 for k in s)
check("no reset between photons: the ancilla reports the combined parity of both photons (deterministic)", ok_sum)
check("no reset: two flipped photons give PASS (the flips cancel), so the combined parity cannot stand in for independent checks", ok_mask)
check("with readout and reset after each photon each photon is judged on its own", ok_rst)
check("after a valid photon the ancilla is |0> for every pair of logical amplitudes: it stores nothing about the state, only a parity bit when something is wrong", ok_blank)

def stream(x, z, gx, gz, l, eps_reset_fail):
    """Steady state of one ancilla serving an endless stream of photons, one checkpoint each.
    eps_reset_fail: probability that reset leaves the ancilla at its previous value (0 = ideal, 1 = never reset).
    A lost photon still interacted with the ancilla (ASSUMED)."""
    q_odd = 2 * x * (1 - x)
    qr = q_odd * (1 - gx) + (1 - q_odd) * gx                      # probability that the ancilla value flips by this photon
    a, b = qr, 1 - (eps_reset_fail * (1 - qr) + (1 - eps_reset_fail) * qr)   # 0->1 and 1->0 transition probabilities
    pi1 = a / (a + b) if a + b > 0 else 0.0
    out = dict(acc_correct=0.0, false_acc=0.0, false_rej=0.0, rej_damaged=0.0, lost=l)
    for u_prev, rf, fx1, fx2, fz1, fz2, ax, az in product((0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1)):
        w = (pi1 if u_prev else 1 - pi1) * pr(rf, eps_reset_fail) * pr(fx1, x) * pr(fx2, x) * pr(fz1, z) * pr(fz2, z) * pr(ax, gx) * pr(az, gz) * (1 - l)
        u_start = u_prev if rf else 0
        report = u_start ^ fx1 ^ fx2 ^ ax
        ok_ = fx1 == 0 and fx2 == 0 and (fz1 ^ fz2 ^ az) == 0
        key = ('acc_correct' if ok_ else 'false_acc') if report == 0 else ('false_rej' if ok_ else 'rej_damaged')
        out[key] += w
    out['accepted'] = out['acc_correct'] + out['false_acc']
    return out
a = stream(0.02, 0.001, 0.002, 0.003, 0.005, 0.0); m = model_v04(0.02, 0.001, 0.002, 0.003, 0.005)
check("ideal reset: the reused ancilla gives exactly the version 0.4 per-checkpoint outcomes (reusing the hardware changes nothing in this model)",
      all(near(a[k], m[k]) for k in ('acc_correct', 'false_acc', 'false_rej', 'rej_damaged', 'lost')))
n0 = stream(0.02, 0.0, 0, 0, 0, 1.0); pcor = (1 - 0.02) ** 2
check("never reset: the ancilla value random-walks, half of all photons are rejected whatever their quality (accepted = 1/2) and good photons are falsely rejected half the time",
      near(n0['accepted'], 0.5) and near(n0['false_rej'], pcor / 2))
check("never reset, flip noise: more wrong outputs are accepted than with ideal reset (cancelled flips pass)",
      n0['false_acc'] > stream(0.02, 0.0, 0, 0, 0, 0.0)['false_acc'])
print("  imperfect reset: probability the reset leaves the old value (ASSUMED), x = 0.02, z = 0.001, gx = gz = 0.002, loss = 0")
print("      reset failure   accepted-correct  false acceptance  false rejection")
fr_prev = -1; mono = True; fa_prev = -1; mono2 = True
for e in (0.0, 0.001, 0.01, 0.1):
    s_ = stream(0.02, 0.001, 0.002, 0.002, 0.0, e)
    print(f"      {e:13.3f}   {s_['acc_correct']:16.5f}  {s_['false_acc']:16.6f}  {s_['false_rej']:14.5f}")
    mono &= s_['false_rej'] > fr_prev; fr_prev = s_['false_rej']
    mono2 &= s_['false_acc'] >= fa_prev - 1e-15; fa_prev = s_['false_acc']
check("imperfect reset raises false rejection first (a stale FAIL contaminates the next photon) and never lowers false acceptance", mono and mono2)
# within one computation, reset failure is invisible: a run that is still going has just reported 0, so the ancilla is already at 0
def run_with_ancilla(xs, z, gx, gz, l, eps_reset_fail):
    """Same dynamic programme with the ancilla value u carried between checkpoints of one computation."""
    dist = {((0, 0, 0, 0), 0): 1.0}; acc = defaultdict(float)
    for x in xs:
        nd = defaultdict(float)
        for (f, u), w in dist.items():
            for e in product((0, 1), repeat=4):
                nd[(tuple(a ^ b for a, b in zip(f, e)), u)] += w * pr(e[0], x) * pr(e[1], x) * pr(e[2], z) * pr(e[3], z)
        dist = nd; nd = defaultdict(float)
        for (f, u), w in dist.items():
            for rf, ax, az, lo in product((0, 1), repeat=4):
                pw = w * pr(rf, eps_reset_fail) * pr(ax, gx) * pr(az, gz) * pr(lo, l)
                if lo: acc['lost'] += pw; continue
                g = list(f); g[2] ^= az
                u_end = (u if rf else 0) ^ g[0] ^ g[1] ^ ax
                if u_end: acc['false_rej' if frame_ok(g) else 'rej_damaged'] += pw
                else: nd[(tuple(g), 0)] += pw
        dist = nd
    for (f, u), w in dist.items(): acc['acc_correct' if frame_ok(f) else 'false_acc'] += w
    return acc
ref = run([0.03] * 4, 0.001, set(range(4)), 0.002, 0.003, 0.002)
chain_same = True
for e in (0.0, 0.5, 1.0):
    a = run_with_ancilla([0.03] * 4, 0.001, 0.002, 0.003, 0.002, e)
    chain_same &= all(near(a[k], ref[k]) for k in ('acc_correct', 'false_acc', 'false_rej', 'rej_damaged', 'lost'))
check("repeated checkpoints on ONE computation do not depend on reset quality: a run still alive has just read 0, so the ancilla is already clean (reset failure matters only after a FAIL, i.e. across photons or runs)",
      chain_same)

# =============================================================== 3. path-style parity router
print("== 3. parity router: even continues, odd goes to a rejection detector ==")
def router(q_odd, t, eta, leak):
    """q_odd: probability the incoming photon has odd parity; t: probability the photon survives to a port;
    eta: detector efficiency on the rejection port; leak: probability an odd photon exits the continue port."""
    ev = {k: 0.0 for k in ('continues_even', 'continues_odd_leak', 'fail_signal', 'odd_undetected', 'lost')}
    for odd, surv, det, lk in product((0, 1), repeat=4):
        w = pr(odd, q_odd) * pr(surv, t) * pr(det, eta) * pr(lk, leak)
        if not surv: ev['lost'] += w
        elif not odd: ev['continues_even'] += w
        elif lk: ev['continues_odd_leak'] += w
        elif det: ev['fail_signal'] += w
        else: ev['odd_undetected'] += w
    ev['silent'] = 1 - ev['fail_signal']
    ev['continues'] = ev['continues_even'] + ev['continues_odd_leak']
    return ev
r = router(0.02, 0.9, 0.8, 0.0)
check("the five router outcomes sum to 1 and FAIL signal = q * t * eta, continuing photons = (1-q) * t", near(r['fail_signal'] + r['continues'] + r['odd_undetected'] + r['lost'], 1)
      and near(r['fail_signal'], 0.02 * 0.9 * 0.8) and near(r['continues'], 0.98 * 0.9))
check("with loss, no FAIL signal is not PASS: P(photon continues | no signal) = (1-q)t / (1 - q t eta) < 1, so silence is UNKNOWN",
      near(r['continues'] / r['silent'], 0.98 * 0.9 / (1 - 0.02 * 0.9 * 0.8)) and r['continues'] / r['silent'] < 0.95)
r1 = router(0.02, 1.0, 1.0, 0.0)
check("with no loss, a perfect detector and a perfect router, silence implies the photon continues (UNKNOWN collapses to PASS only in the loss-free ideal)",
      near(r1['continues'] / r1['silent'], 1.0))
rl = router(0.02, 0.9, 0.8, 0.05)
check("router leakage (extinction less than perfect) lets odd photons continue unflagged: continuing-wrong probability = q t leak",
      near(rl['continues_odd_leak'], 0.02 * 0.9 * 0.05))

# =============================================================== 4. detect, reject, correct
print("== 4. detect, reject, correct ==")
def two_qubit(al, be): return {(0, 0): al, (1, 1): be}
def flip(s, ax):
    o = {}
    for k, x in s.items():
        k = list(k); k[ax] ^= 1; o[tuple(k)] = o.get(tuple(k), 0) + x
    return o
def fid(s, ref):
    keys = set(s) | set(ref); return abs(sum(s.get(k, 0).conjugate() * ref.get(k, 0) for k in keys)) ** 2
ok_ind = ok_wrong = True
for _ in range(100):
    al, be = (lambda v: (v[0] / math.sqrt(abs(v[0]) ** 2 + abs(v[1]) ** 2), v[1] / math.sqrt(abs(v[0]) ** 2 + abs(v[1]) ** 2)))((rc(), rc()))
    ref = two_qubit(al, be)
    fa, fb = flip(ref, 0), flip(ref, 1)
    parity = lambda s: {sum(k) % 2 for k in s}
    ok_ind &= parity(fa) == parity(fb) == {1}                       # same syndrome
    recovered = flip(fa, 1)                                          # wrong guess: the flip was on axis a, undo axis b
    ok_wrong &= abs(fid(recovered, ref) - (2 * (al.conjugate() * be).real) ** 2) < 1e-12 and fid(recovered, ref) < 1 - 1e-6 or abs(al * be) < 1e-6
check("two-axis parity code: a flip on axis a and a flip on axis b give the same syndrome, and undoing the wrong one applies a logical X, so single flips are detected but cannot be corrected (hand argument checked on 100 states)",
      ok_ind and ok_wrong)
# three-axis repetition code span{000,111}, checks Z1Z2 and Z2Z3
def synd(k): return (k[0] ^ k[1], k[1] ^ k[2])
ok_syn = ok_cor = ok_dbl = ok_z = True
syn_seen = {}
for _ in range(50):
    al, be = (lambda v: (v[0] / math.sqrt(abs(v[0]) ** 2 + abs(v[1]) ** 2), v[1] / math.sqrt(abs(v[0]) ** 2 + abs(v[1]) ** 2)))((rc(), rc()))
    ref = {(0, 0, 0): al, (1, 1, 1): be}
    for ax in range(3):
        s = flip(ref, ax); ks = {synd(k) for k in s}; ok_syn &= len(ks) == 1
        sy = ks.pop(); syn_seen[sy] = ax
        ok_cor &= fid(flip(s, ax), ref) > 1 - 1e-12
    ok_syn &= len(syn_seen) == 3 and (0, 0) not in syn_seen
    decode = {v: k for k, v in syn_seen.items()}
    for a_, b_ in ((0, 1), (0, 2), (1, 2)):                        # two flips decode to the wrong axis: logical error
        s = flip(flip(ref, a_), b_); sy = synd(next(iter(s)))
        out = flip(s, syn_seen[sy]); ok_dbl &= fid(out, ref) < 1 - 1e-6 or abs(al * be) < 1e-6
    for ax in range(3):                                             # a Z error on any axis is an undetected logical Z
        s = {k: (-x if k[ax] else x) for k, x in ref.items()}
        ok_z &= {synd(k) for k in s} == {(0, 0)} and abs(fid(s, ref) - (abs(al) ** 2 - abs(be) ** 2) ** 2) < 1e-12
check("three-axis repetition code with two parity checks: each single flip has its own syndrome and applying the matching X restores the state exactly", ok_syn and ok_cor)
check("the same code decodes two flips to the wrong axis, giving a logical error, and offers no protection against Z errors (a Z on any of three axes is an undetected logical Z)", ok_dbl and ok_z)
check("syndrome extraction is separate from recovery: the syndrome identifies WHICH axis flipped without anything being applied, and the correction can be a physical X or a tracked frame update (not simulated here)",
      len(syn_seen) == 3)

# =============================================================== 5. temporal validity of evidence
print("== 5. how long does a correct, verified state stay correct? ==")
def valid_after(k, x, z):
    dist = {(0, 0, 0, 0): 1.0}
    for _ in range(k): dist = seg(dist, x, z)
    return sum(w for f, w in dist.items() if frame_ok(f))
def valid_closed(k, x, z):
    ex = (1 + (1 - 2 * x) ** k) / 2; ez = (1 + (1 - 2 * z) ** k) / 2
    return ex ** 2 * (ez ** 2 + (1 - ez) ** 2)
okv = all(near(valid_after(k, x, z), valid_closed(k, x, z)) for k in range(0, 7) for x in (0.0, 0.01, 0.1) for z in (0.0, 0.005, 0.1))
check("closed form for the probability that a state correct at a checkpoint is still correct k segments later: ((1+(1-2x)^k)/2)^2 * [ez^2 + (1-ez)^2], ez = (1+(1-2z)^k)/2 (matches exact enumeration)", okv)
print("  validity of a PASS after k further segments (ASSUMED x = 0.01, z = 0.001): " + ", ".join(f"k={k}: {valid_closed(k, 0.01, 0.001):.4f}" for k in (0, 1, 2, 4, 8, 16, 32)))
check("evidence decays with the number of operations since the check, and the form is the same for any carrier: a maximum evidence age is a scheduling variable, not a property of time as an Encoding Axie",
      valid_closed(0, 0.01, 0.001) == 1 and valid_closed(4, 0.01, 0.001) > valid_closed(16, 0.01, 0.001) > valid_closed(64, 0.01, 0.001) > 0.2)
check("the validity of a PASS never reaches 0 for flip noise alone: it tends to 1/4 as flips on each axis become even or odd with equal chance (the 'even-even' share)",
      abs(valid_closed(10 ** 6, 0.01, 0.0) - 0.25) < 1e-6)

print()
bad = [n for n, ok_ in results if not ok_]
print("ALL PASS" if not bad else "FAILURES: " + "; ".join(bad))
raise SystemExit(0 if not bad else 1)
