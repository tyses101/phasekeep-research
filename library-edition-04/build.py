#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tyler O'Bryan, where applicable
"""Builds the PhaseKeep Learning Library, Edition 04 (working draft), from src/ into this folder.

Edition 04 is a dated research snapshot that continues the frozen Edition 03 (Revision H) from Volume 15.
It reuses the Edition 03 formatting code by importing ../library/build.py READ-ONLY; nothing under library/
is written. Same source syntax as Edition 03 (see that file's docstring).

Run:  python3 -I build.py      (standard library only)
"""
import html, importlib.util, re, sys
from pathlib import Path

sys.dont_write_bytecode = True   # never leave __pycache__ inside the frozen library/ folder

HERE = Path(__file__).resolve().parent
SRC = HERE / "src"
ED3 = HERE.parent / "library"
sys.path.insert(0, str(ED3))
spec = importlib.util.spec_from_file_location("ed3build", ED3 / "build.py")
ed3 = importlib.util.module_from_spec(spec); spec.loader.exec_module(ed3)

SNAPSHOT = "research snapshot as of 28 November 2026"
BOOKS = [  # (file stem, label, title, subtitle)
    ("15-relationships", "15", "Relationships Between Properties", "When the information lives between things, not inside them"),
    ("16-lights-many-handles", "16", "Light's Many Handles", "Momentum, spin, twist, and why stability depends on the disturbance"),
    ("17-from-light-to-atoms", "17", "From Light to Atoms", "Why the research looked beyond photon-only execution, and what atoms offer and cost"),
    ("18-four-atom-ring", "18", "The Four-Atom Ring", "A register made of four atoms and one hopping excitation, and the honest surprise inside it"),
    ("19-making-registers-talk", "19", "Making Registers Talk", "Coupling two rings, frequency planning, gentle pulses, the echo, and testing on today's computers"),
    ("20-when-things-go-wrong", "20", "When Things Go Wrong", "A story of simulated failures, and the rules each one taught"),
    ("A7-glossary-additions", "A7", "Glossary Additions", "Terms used in Edition 04, with their status"),
    ("A8-ledger-additions", "A8", "Ledger Additions", "Every number in Edition 04, its evidence tag and where it came from"),
    ("A9-sources-additions", "A9", "Sources Additions", "What was read for Edition 04, and how closely"),
    ("A10-edition-notes", "A10", "Edition 04 Notes", "What this edition is, how it relates to the frozen Edition 03, and what comes next"),
]
STEM_BY_NUM = {l: s for s, l, t, sub in BOOKS if l.isdigit()}
ED3_BY_NUM = ed3.STEM_BY_NUM
APPX = {"7": "A7-glossary-additions", "8": "A8-ledger-additions", "9": "A9-sources-additions", "10": "A10-edition-notes"}


def xlink(md, stem):
    """Link 'Volume N' (Edition 03 volumes go to ../library/) and 'Appendix N' mentions."""
    out, fence = [], False
    for ln in md.split("\n"):
        if ln.startswith("```"):
            fence = not fence; out.append(ln); continue
        if fence or ln.startswith("#") or ln.startswith("    "):
            out.append(ln); continue
        parts = re.split(r"(\[[^\]]*\]\([^)]*\)|`[^`]*`)", ln)
        for k in range(0, len(parts), 2):
            def vol(m):
                n = m.group(1)
                if n in STEM_BY_NUM and STEM_BY_NUM[n] != stem:
                    return f"[Volume {n}]({STEM_BY_NUM[n]}.html)"
                if n in ED3_BY_NUM:
                    return f"[Volume {n}](../library/{ED3_BY_NUM[n]}.html)"
                return m.group(0)
            p = re.sub(r"\bVolume (\d+)\b", vol, parts[k])
            p = re.sub(r"\bAppendix (\d+)\b", lambda m: f"[Appendix {m.group(1)}]({APPX[m.group(1)]}.html)" if m.group(1) in APPX else
                       (f"[Appendix {m.group(1)}](../library/{ {'1':'A1-glossary','2':'A2-ledger','3':'A3-sources','4':'A4-math-refresher','5':'A5-faq','6':'A6-edition-notes'}[m.group(1)] }.html)"
                        if m.group(1) in "123456" else m.group(0)), p)
            parts[k] = p
        out.append("".join(parts))
    return "\n".join(out)


FOOT = ("Edition 04 working draft · " + SNAPSHOT + " · © 2026 Tyler O'Bryan, where applicable · PhaseKeep Research · "
        "text CC BY 4.0, code MIT (see NOTICE.txt) · AI-assisted research, documentation and numerical analysis · "
        "Edition 03 Revision H remains the frozen baseline. PhaseKeep is an exploratory research proposal, not a demonstrated "
        "quantum computer. No PhaseKeep hardware measurement exists yet.")


def page(title, eyebrow, sub, body, idx):
    prev_ = BOOKS[idx - 1] if idx > 0 else None
    next_ = BOOKS[idx + 1] if idx + 1 < len(BOOKS) else None
    nav = '<div class="nav"><span>' + (f'<a href="{prev_[0]}.html">← {html.escape(prev_[2])}</a>' if prev_ else '<a href="../library/index.html">← Edition 03 (frozen)</a>') + \
          "</span><span>" + (f'<a href="{next_[0]}.html">{html.escape(next_[2])} →</a>' if next_ else "") + "</span></div>"
    banner = ('<div class="box key"><div class="bt">Working draft</div><p>This is <strong>Edition 04</strong>, a ' + SNAPSHOT +
              '. It is not frozen and may be revised. <a href="../library/index.html">Edition 03 Revision H</a> is the frozen baseline.</p></div>')
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} · PhaseKeep Learning Library, Edition 04</title><meta name="description" content="{html.escape(sub)}">
<style>{ed3.CSS}</style></head><body>
<a class="skip" href="#main">Skip to content</a>
<div class="top" role="navigation" aria-label="Library"><div><a href="index.html"><strong>PhaseKeep Learning Library · Edition 04 (draft)</strong></a><span class="sp"></span><a href="../library/index.html">Edition 03</a><a href="A7-glossary-additions.html">Glossary</a><a href="A8-ledger-additions.html">Ledger</a><a href="A9-sources-additions.html">Sources</a></div></div>
<main id="main" class="wrap"><div class="eyebrow">{html.escape(eyebrow)}</div><h1>{html.escape(title)}</h1><p class="sub">{html.escape(sub)}</p>
{banner}
{body}
{nav}
<footer>{FOOT}</footer>
</main></body></html>"""


def build():
    combined = []
    for idx, (stem, label, title, sub) in enumerate(BOOKS):
        f = SRC / f"{stem}.md"
        if not f.exists():
            print("skip (no source):", stem); continue
        text = re.sub(r"^# .*\n", "", f.read_text(encoding="utf-8"), count=1)
        text = xlink(text, stem)
        eyebrow = "Volume " + label if label.isdigit() else "Appendix " + label[1:]
        (HERE / f"{stem}.html").write_text(page(title, eyebrow, sub, ed3.block(text), idx), encoding="utf-8")
        (HERE / "markdown").mkdir(exist_ok=True)
        pm = f"# {title}\n\n*{sub}*\n\n*Edition 04 working draft, {SNAPSHOT}.*\n\n" + ed3.portable(text) + \
             "\n\n---\n*(c) 2026 Tyler O'Bryan, where applicable. PhaseKeep Research. Text CC BY 4.0, code MIT. AI-assisted research, documentation and numerical analysis. Working draft.*\n"
        (HERE / "markdown" / f"{stem}.md").write_text(pm, encoding="utf-8")
        combined.append(f"\n\n---\n\n## {('Volume ' + label + ': ') if label.isdigit() else ''}{title}\n\n*{sub}*\n\n" +
                        re.sub(r"^## ", "### ", re.sub(r"^### ", "#### ", ed3.portable(text, links=False), flags=re.M), flags=re.M))
        print("built", stem)
    cards = "".join(f'<a class="card" href="{s}.html"><span class="n">{"VOLUME " + l if l.isdigit() else "APPENDIX " + l[1:]}</span><b>{html.escape(t)}</b>{html.escape(sub)}</a>'
                    for s, l, t, sub in BOOKS if (SRC / f"{s}.md").exists())
    idx_src = SRC / "index.md"
    intro = ed3.block(idx_src.read_text(encoding="utf-8").split("\n", 1)[1]) if idx_src.exists() else ""
    (HERE / "index.html").write_text(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>PhaseKeep Learning Library · Edition 04 (working draft)</title><meta name="description" content="Edition 04 continues the PhaseKeep learning library from Volume 15 as a dated research snapshot.">
<style>{ed3.CSS}</style></head><body>
<div class="wrap"><div class="eyebrow">Open learning · Edition 04 (working draft) · {SNAPSHOT}</div><h1>PhaseKeep Learning Library</h1>
<p class="sub">Continuing the series from Volume 15.</p>
{intro}
<h2>Edition 04 so far</h2><div class="cards">{cards}</div>
<p><a href="../library/index.html">Edition 03, Revision H (frozen): Start Here and Volumes 1–14 →</a></p>
<footer>{FOOT}</footer></div></body></html>""", encoding="utf-8")
    print("built index")
    toc = "\n".join(f"- {('Volume ' + l + ': ') if l.isdigit() else ''}{t}" for s_, l, t, sub in BOOKS if (SRC / f"{s_}.md").exists())
    head = ("# PhaseKeep Learning Library, Edition 04 (working draft, complete text)\n\n*" + SNAPSHOT.capitalize() + ".*\n\n"
            "*(c) 2026 Tyler O'Bryan, where applicable. PhaseKeep Research. Text CC BY 4.0, code MIT (see NOTICE.txt). AI-assisted research, "
            "documentation and numerical analysis. Edition 03 Revision H remains the frozen baseline.*\n\n"
            + (ed3.portable(idx_src.read_text(encoding="utf-8").split("\n", 1)[1]) if idx_src.exists() else "") + "\n\n## Contents\n\n" + toc)
    full = head + "".join(combined)
    (HERE / "PhaseKeep-Learning-Library-Edition-04-complete.md").write_text(full, encoding="utf-8")
    (HERE / "PhaseKeep-Learning-Library-Edition-04-complete.txt").write_text(full.replace("**", "").replace("> ", "  "), encoding="utf-8")
    print("built combined text,", len(full.split()), "words")


if __name__ == "__main__":
    build()
