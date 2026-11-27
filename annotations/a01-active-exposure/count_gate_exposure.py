#!/usr/bin/env python3
"""Annotation A01 (post-V1.0): split the V1.0 round circuits' two-qubit gates into
data-touching gates and ancilla-only gates.

This is a COUNT over circuits that the unmodified V1.0 program already defines. It runs
no new simulation and changes no checkpoint file. It reads checkpoints/v1.0/code/buddy_v10_checks.py
(read-only), takes only the circuit-builder definitions from it (via the ast module, so the
V1.0 checks are not executed), builds the V1.0 rounds, and tallies gates.

Convention (V1.0): qubits 0..3 are the four data axes; qubits >= 4 are ancilla qubits.
  data-touching gate : a two-qubit gate with exactly one data qubit
  ancilla-only gate  : a two-qubit gate with both qubits >= 4
Under V1.0's destructive-readout rule every ancilla qubit sits on its own ancilla photon,
so (with one ancilla qubit per photon, K = 1) every data-touching gate is an inter-photon gate.

Run:  python3 -I annotations/a01-active-exposure/count_gate_exposure.py
Standard library only. Exit status 0 only if every total matches the V1.0 page's K = 1 column.
"""
import ast, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, "..", "..", "checkpoints", "v1.0", "code", "buddy_v10_checks.py"))
WANT_FUNCS = {"touched", "resources", "z_conv", "x_conv", "z_flag", "x_flag", "cat_prep", "cat_check", "build_round"}
WANT_CLASSES = {"Builder"}

with open(SRC, encoding="utf-8") as f:
    tree = ast.parse(f.read(), SRC)
keep = []
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in WANT_FUNCS:
        keep.append(node)
    elif isinstance(node, ast.ClassDef) and node.name in WANT_CLASSES:
        keep.append(node)
    elif isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "AX" for t in node.targets):
        keep.append(node)
missing = (WANT_FUNCS | WANT_CLASSES | {"AX"}) - {getattr(n, "name", None) or "AX" for n in keep}
if missing:
    sys.exit("could not find in V1.0 source: %s" % sorted(missing))
ns = {}
exec(compile(ast.Module(body=keep, type_ignores=[]), SRC, "exec"), ns)
build_round, z_conv, x_conv, z_flag, x_flag, cat_check, AX = (ns[k] for k in ("build_round", "z_conv", "x_conv", "z_flag", "x_flag", "cat_check", "AX"))

CONFIGS = [  # same definitions as the V1.0 ROUNDS table, with the totals the V1.0 page gives at K = 1
    ("Local conventional",        [(z_conv, [0, 1]), (z_conv, [2, 3])], 4),
    ("Joint conventional",        [(z_conv, AX), (x_conv, AX)], 8),
    ("Joint flagged",             [(z_flag, AX), (x_flag, AX)], 12),
    ("Joint verified cat",        [(cat_check, "Z", [[0], [1], [2], [3]], True), (cat_check, "X", [[0], [1], [2], [3]], True)], 18),
    ("Joint cooperative, verified", [(cat_check, "Z", [[0, 1], [2, 3]], True), (cat_check, "X", [[0, 1], [2, 3]], True)], 14),
    ("ZZZZ only (partial joint)", [(z_conv, AX)], 4),
]
ok = True
print("%-30s %6s %14s %14s   %s" % ("round", "total", "data-touching", "ancilla-only", "completion at s=0.5 if only data-touching gates must succeed"))
for name, spec, v10_total in CONFIGS:
    B = build_round(spec)
    two = [o for o in B.ops if o[0] in ("CNOT", "CZ")]
    data = sum(1 for o in two if (o[1] < 4) != (o[2] < 4))
    anc = sum(1 for o in two if o[1] >= 4 and o[2] >= 4)
    both_data = sum(1 for o in two if o[1] < 4 and o[2] < 4)
    match = (len(two) == v10_total and both_data == 0 and data + anc == len(two))
    ok &= match
    print("%-30s %6d %14d %14d   %.8g   %s" % (name, len(two), data, anc, 0.5 ** data, "matches V1.0 total" if match else "MISMATCH"))
print("RESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
