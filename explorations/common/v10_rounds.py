"""Shared, read-only loader for the V1.0 round circuits (used by the exploration scripts).

It parses checkpoints/v1.0/code/buddy_v10_checks.py with the ast module and executes ONLY the
circuit-builder definitions (so none of the V1.0 checks run and no checkpoint file is changed),
exactly as annotation A01 does.  Returns the operation lists for the rounds V1.0 defines.
Op tuples: ('P0',q) ('P+',q) ('H',q) ('CNOT',c,t) ('CZ',a,b) ('MZ',q,r) ('MX',q,r);
qubits 0..3 are data axes (a1,b1,a2,b2 = photon 0: axes 0,1; photon 1: axes 2,3).
"""
import ast, os

_HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(_HERE, "..", "..", "checkpoints", "v1.0", "code", "buddy_v10_checks.py"))
_FUNCS = {"touched", "z_conv", "x_conv", "z_flag", "x_flag", "cat_prep", "cat_check", "build_round"}


def load():
    with open(SRC, encoding="utf-8") as f:
        tree = ast.parse(f.read(), SRC)
    keep = [n for n in tree.body if (isinstance(n, ast.FunctionDef) and n.name in _FUNCS)
            or (isinstance(n, ast.ClassDef) and n.name == "Builder")
            or (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "AX" for t in n.targets))]
    ns = {}
    exec(compile(ast.Module(body=keep, type_ignores=[]), SRC, "exec"), ns)
    br, AX = ns["build_round"], ns["AX"]
    z_conv, x_conv, z_flag, x_flag, cat_check = (ns[k] for k in ("z_conv", "x_conv", "z_flag", "x_flag", "cat_check"))
    specs = {
        "L conv (baseline)": [(z_conv, [0, 1]), (z_conv, [2, 3])],
        "J conv": [(z_conv, AX), (x_conv, AX)],
        "J flag": [(z_flag, AX), (x_flag, AX)],
        "J cat (verified)": [(cat_check, "Z", [[0], [1], [2], [3]], True), (cat_check, "X", [[0], [1], [2], [3]], True)],
        "J ZZZZ only (partial)": [(z_conv, AX)],
    }
    out = {}
    for name, sp in specs.items():
        B = br(sp)
        out[name] = dict(ops=list(B.ops), dets=list(B.dets), nq=B.nq, nr=B.nr, code="L" if name.startswith("L ") else ("Z" if "ZZZZ" in name else "J"))
    return out
