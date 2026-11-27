#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tyler O'Bryan, where applicable
"""Builds the PhaseKeep Learning Library (Edition 03) from Markdown sources in src/ into self-contained HTML pages.

Run:  python3 build.py            (standard library only; writes HTML next to this file)
Source syntax (a small Markdown subset):
  # Title (first line)   ## Section   ### Subsection
  paragraphs, - bullets, 1. numbered, | tables |, **bold**, *italic*, `code`, [text](url), > quote
  ::: kind  ...  :::     callout. kinds: plain, key, deeper, try, watch, evidence, story
  {{fig:name|Caption}}   inline SVG figure from figures.py
  [[TAG]]                evidence pill: DERIVED REPORTED ASSUMED SIMULATED PROPOSED MEASURED UNVERIFIED BLOCKED
"""
import html, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "src"
sys.path.insert(0, str(HERE))
import figures  # noqa: E402

BOOKS = [  # (file stem, short label, title, subtitle)
    ("00-start-here", "Start", "Start Here", "What PhaseKeep is, how to read this library, and how we keep ourselves honest"),
    ("00b-first-words", "W", "First Words", "A starting glossary of every background word, for a reader who knows nothing yet"),
    ("01-light", "1", "Light, Waves and Photons", "Polarization, interference, and the twisting beams called OAM"),
    ("02-quantum-states", "2", "States, Measurement and Why Reading Is Hard", "Superposition, amplitudes, phase, fidelity, and the no-cloning rule"),
    ("03-encoding-axies", "3", "Encoding Axies and the Tetragon", "How a single photon carries four addresses"),
    ("04-geometric-encoding", "4", "Geometric Encoding", "Squares, cubes and hypercubes as a map of states"),
    ("05-controlled-transformations", "5", "Controlled Transformations", "The optical parts that change a state, and what each one does to it"),
    ("06-two-photons", "6", "Two Photons: Making Light Interact", "Why photons ignore each other, and how a heralded gate fakes it"),
    ("07-buddy-checks", "7", "The Buddy System and Buddy Checks", "Detection is not verification"),
    ("08-memory-and-loss", "8", "Memory, Loss and Survival", "Why almost every number in this project is a loss number"),
    ("09-research-lab", "9", "The Research Lab", "Evidence, scripts, audits, negative results and what is blocked"),
    ("10-intelligent-registers", "10", "Intelligent Registers", "A controller that composes only operations we can support"),
    ("11-experiments", "11", "Experiments, Open Questions and Contributing", "What to build first, what would prove us wrong, how to help"),
    ("12-journey", "12", "One Photon's Journey", "A single worked example from preparation to storage, with the numbers"),
    ("13-wider-field", "13", "The Wider Field", "Where PhaseKeep sits among other photonic approaches, and what we do not know"),
    ("14-workbook", "14", "Workbook and Code", "Exercises with answers, and short programs so you can check the numbers yourself"),
    ("A1-glossary", "A1", "Glossary", "Every term in one place"),
    ("A2-ledger", "A2", "The Ledger of Numbers", "Every number used in the library, its evidence tag and where it came from"),
    ("A3-sources", "A3", "Sources and Read Status", "What was actually read, what was supplied, what is unchecked"),
    ("A4-math-refresher", "A4", "Math Refresher", "Just enough complex numbers, vectors and matrices"),
    ("A5-faq", "A5", "Questions and Misconceptions", "Straight answers to the questions people ask first"),
    ("A6-edition-notes", "A6", "Edition Notes", "What changed from Edition 02, naming decisions, and how this library was checked"),
]
LABEL = {s: (l, t, sub) for s, l, t, sub in BOOKS}
TAGS = {"DERIVED": "Worked out mathematically; checked by running code",
        "REPORTED": "Stated by a published source we read (scope noted)",
        "ASSUMED": "An input we chose; not measured",
        "SIMULATED": "Output of a computer model",
        "PROPOSED": "A design or idea, not shown to work",
        "MEASURED": "Measured by PhaseKeep in a lab (none yet)",
        "UNVERIFIED": "Supplied or remembered; not checked",
        "BLOCKED": "Cannot proceed without something we do not have"}
KIND_TITLE = {"plain": "In plain words", "key": "Key idea", "deeper": "Go deeper (optional math)", "try": "Try it",
              "watch": "Common mistake", "evidence": "Evidence status", "story": "Why this matters"}

CSS = """
:root{--bg:#faf8f3;--fg:#1f2933;--mut:#5d6b78;--line:#ddd8cc;--card:#ffffff;--acc:#1b5e86;--acc2:#7a4a12;
--key:#e5f0f7;--keyb:#1b5e86;--plain:#eaf5ec;--plainb:#2f7d4a;--deeper:#f1ecf8;--deeperb:#6a4aa0;--try:#fdf3dc;--tryb:#a8730a;
--watch:#fbe6e3;--watchb:#b3382b;--evidence:#eceef1;--evidenceb:#56606d;--story:#f6efe6;--storyb:#8b5a2b}
@media (prefers-color-scheme:dark){:root{--bg:#14181d;--fg:#e4e8ec;--mut:#9aa6b2;--line:#2c343d;--card:#1b2128;--acc:#7cc0ea;--acc2:#e0b277;
--key:#16303f;--keyb:#6fb3dc;--plain:#16301f;--plainb:#6fcf8d;--deeper:#2a2140;--deeperb:#b79ae8;--try:#3a2e12;--tryb:#e8b84f;
--watch:#3c1b18;--watchb:#f08c80;--evidence:#232a31;--evidenceb:#a0abb7;--story:#33271a;--storyb:#d9a66a}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font:18px/1.7 Georgia,'Gelasio','Times New Roman',serif}
.top{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--line);font:14px system-ui,sans-serif}
.top div{max-width:760px;margin:auto;padding:8px 16px;display:flex;gap:14px;flex-wrap:wrap;align-items:center}
.top a{color:var(--acc);text-decoration:none}.top .sp{flex:1}
.wrap{max-width:760px;margin:0 auto;padding:28px 16px 72px}
.eyebrow{font:600 12px system-ui,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--mut)}
h1{font:700 2.1rem/1.2 system-ui,'Inter',sans-serif;margin:.2em 0 .2em}
h2{font:700 1.45rem/1.3 system-ui,'Inter',sans-serif;margin:2.1em 0 .4em;padding-top:.5em;border-top:1px solid var(--line)}
h3{font:700 1.1rem/1.35 system-ui,'Inter',sans-serif;margin:1.6em 0 .3em}
.sub{font:1.08rem/1.5 system-ui,sans-serif;color:var(--mut);margin:0 0 1.4em}
p,li{max-width:68ch}li{margin:.25em 0}a{color:var(--acc)}
pre{background:var(--evidence);padding:12px 14px;border-radius:8px;overflow-x:auto;margin:1em 0}pre code{background:none;padding:0;overflow-wrap:normal;white-space:pre}
code{font:.86em ui-monospace,Menlo,Consolas,monospace;background:var(--evidence);padding:1px 5px;border-radius:4px;overflow-wrap:anywhere}
blockquote{margin:1em 0;padding:.2em 1em;border-left:3px solid var(--line);color:var(--mut)}
.tw{overflow-x:auto;margin:1em 0;border:1px solid var(--line);border-radius:8px;background:var(--card)}
table{border-collapse:collapse;width:100%;font:15px/1.5 system-ui,sans-serif}
th,td{padding:8px 11px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line)}th{background:var(--evidence)}tr:last-child td{border-bottom:0}
.box{margin:1.3em 0;padding:12px 16px;border-radius:8px;border-left:5px solid var(--evidenceb);background:var(--evidence);font:16px/1.65 system-ui,sans-serif}
.box>.bt{font:700 12px system-ui,sans-serif;letter-spacing:.1em;text-transform:uppercase;margin-bottom:4px}
.box p,.box li{max-width:none}.box p:last-child{margin-bottom:0}.box ul,.box ol{margin:.3em 0}
.key{background:var(--key);border-color:var(--keyb)}.key>.bt{color:var(--keyb)}
.plain{background:var(--plain);border-color:var(--plainb)}.plain>.bt{color:var(--plainb)}
.deeper{background:var(--deeper);border-color:var(--deeperb)}.deeper>.bt{color:var(--deeperb)}
.try{background:var(--try);border-color:var(--tryb)}.try>.bt{color:var(--tryb)}
.watch{background:var(--watch);border-color:var(--watchb)}.watch>.bt{color:var(--watchb)}
.evidence{background:var(--evidence);border-color:var(--evidenceb)}.evidence>.bt{color:var(--evidenceb)}
.story{background:var(--story);border-color:var(--storyb)}.story>.bt{color:var(--storyb)}
.tag{display:inline-block;font:700 11px system-ui,sans-serif;letter-spacing:.04em;padding:1px 7px;border-radius:99px;vertical-align:1px;border:1px solid currentColor}
.t-DERIVED,.t-REPORTED{color:var(--plainb)}.t-SIMULATED{color:var(--keyb)}.t-ASSUMED,.t-UNVERIFIED{color:var(--tryb)}
.t-PROPOSED{color:var(--evidenceb)}.t-MEASURED{color:var(--deeperb)}.t-BLOCKED{color:var(--watchb)}
figure{margin:1.6em 0}figure svg{width:100%;height:auto;display:block;background:var(--card);border:1px solid var(--line);border-radius:8px}
figcaption{font:14px/1.5 system-ui,sans-serif;color:var(--mut);margin-top:6px}
svg text{font-family:system-ui,sans-serif;fill:var(--fg)}svg .m{fill:var(--mut)}svg .line{stroke:var(--fg);fill:none}
svg .a{fill:var(--keyb);stroke:var(--keyb)}svg .b{fill:var(--tryb);stroke:var(--tryb)}svg .c{fill:var(--plainb);stroke:var(--plainb)}
svg .d{fill:var(--watchb);stroke:var(--watchb)}svg .e{fill:var(--deeperb);stroke:var(--deeperb)}svg .soft{fill:var(--evidence);stroke:var(--line)}
.nav{display:flex;justify-content:space-between;gap:12px;margin-top:3em;padding-top:1em;border-top:1px solid var(--line);font:15px system-ui,sans-serif}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px;margin:1em 0}
.card{display:block;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px;text-decoration:none;color:var(--fg);font:15px/1.45 system-ui,sans-serif}
.card b{display:block;color:var(--acc);font-size:16px}.card span.n{font-size:12px;letter-spacing:.1em;color:var(--mut)}
a.skip{position:absolute;left:-999px}a.skip:focus{left:8px;top:8px;background:var(--card);padding:6px 10px;z-index:9}
footer{margin-top:3em;font:13px/1.5 system-ui,sans-serif;color:var(--mut)}
@media print{pre{white-space:pre-wrap}.top,.nav{display:none}body{background:#fff;color:#000;font-size:11.5pt}.box{break-inside:avoid}h2{break-after:avoid}}
"""


STEM_BY_NUM = {l: s for s, l, t, sub in BOOKS if l.isdigit()}


def xlink(md, stem):
    """Turn 'Volume N' and 'Appendix N' mentions into links; in the glossary also turn [N] volume references into links."""
    out, fence = [], False
    for ln in md.split("\n"):
        if ln.startswith("```"):
            fence = not fence
            out.append(ln)
            continue
        if fence or ln.startswith("#") or ln.startswith("    "):
            out.append(ln)
            continue
        parts = re.split(r"(\[[^\]]*\]\([^)]*\)|`[^`]*`)", ln)
        for k in range(0, len(parts), 2):
            p = parts[k]
            p = re.sub(r"\bVolume (\d+)\b", lambda m: f"[Volume {m.group(1)}]({STEM_BY_NUM[m.group(1)]}.html)" if m.group(1) in STEM_BY_NUM and STEM_BY_NUM[m.group(1)] != stem else m.group(0), p)
            p = re.sub(r"\bAppendix (\d)\b", lambda m: f"[Appendix {m.group(1)}]({ {'1':'A1-glossary','2':'A2-ledger','3':'A3-sources','4':'A4-math-refresher','5':'A5-faq','6':'A6-edition-notes'}[m.group(1)] }.html)", p)
            if stem == "A1-glossary":
                p = re.sub(r"\[(\d+(?:, \d+)*)\]", lambda m: ", ".join(f"[Vol. {n}]({STEM_BY_NUM[n]}.html)" if n in STEM_BY_NUM else n for n in m.group(1).split(", ")), p)
            parts[k] = p
        out.append("".join(parts))
    return "\n".join(out)


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", lambda m: f"<code>{m.group(1)}</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"\[\[([A-Z]+)\]\]", lambda m: f'<span class="tag t-{m.group(1)}" title="{html.escape(TAGS.get(m.group(1), ""))}">{m.group(1)}</span>', s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', s)
    return s


def block(md):
    lines = md.split("\n")
    out, i = [], 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1
            continue
        if ln.startswith("```"):
            j, buf = i + 1, []
            while j < len(lines) and not lines[j].startswith("```"):
                buf.append(lines[j]); j += 1
            out.append("<pre><code>" + html.escape("\n".join(buf), quote=False) + "</code></pre>")
            i = j + 1
            continue
        m = re.match(r"^::: *(\w+)\s*$", ln)
        if m:
            kind, j, buf, depth = m.group(1), i + 1, [], 1
            while j < len(lines):
                if re.match(r"^::: *\w+\s*$", lines[j]):
                    depth += 1
                elif lines[j].strip() == ":::":
                    depth -= 1
                    if depth == 0:
                        break
                buf.append(lines[j])
                j += 1
            out.append(f'<div class="box {kind}"><div class="bt">{KIND_TITLE.get(kind, kind)}</div>{block(chr(10).join(buf))}</div>')
            i = j + 1
            continue
        m = re.match(r"^\{\{fig:(\w+)\|(.*)\}\}\s*$", ln)
        if m:
            out.append(f"<figure>{figures.get(m.group(1))}<figcaption>{inline(m.group(2))}</figcaption></figure>")
            i += 1
            continue
        m = re.match(r"^(#{2,3}) +(.*)$", ln)
        if m:
            n = len(m.group(1))
            text = m.group(2)
            slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
            out.append(f'<h{n} id="{slug}">{inline(text)}</h{n}>')
            i += 1
            continue
        if ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(lines[i])
                i += 1
            cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
            head, body = cells[0], [r for r in cells[2:]]
            t = "<div class='tw'><table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>"
            t += "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body) + "</tbody></table></div>"
            out.append(t)
            continue
        if re.match(r"^\s*[-*] ", ln):
            items = []
            while i < len(lines) and re.match(r"^\s*[-*] ", lines[i]):
                items.append(re.sub(r"^\s*[-*] ", "", lines[i]))
                i += 1
            out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>")
            continue
        if re.match(r"^\s*\d+\. ", ln):
            items = []
            while i < len(lines) and re.match(r"^\s*\d+\. ", lines[i]):
                items.append(re.sub(r"^\s*\d+\. ", "", lines[i]))
                i += 1
            out.append("<ol>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ol>")
            continue
        if ln.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i][1:].strip())
                i += 1
            out.append("<blockquote><p>" + inline(" ".join(buf)) + "</p></blockquote>")
            continue
        buf = []
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{2,3} |\||::: |```|\{\{fig|\s*[-*] |\s*\d+\. |>)", lines[i]):
            buf.append(lines[i].strip())
            i += 1
        out.append("<p>" + inline(" ".join(buf)) + "</p>")
    return "\n".join(out)


def portable(md, links=True):
    """Markdown that reads correctly in any editor: callouts become quotes, figures become text descriptions."""
    out, lines, i = [], md.split("\n"), 0
    stack = []
    for ln in lines:
        m = re.match(r"^::: *(\w+)\s*$", ln)
        if m:
            stack.append(m.group(1))
            out.append(">")
            out.append(f"> **{KIND_TITLE.get(m.group(1), m.group(1))}**")
            continue
        if ln.strip() == ":::":
            if stack:
                stack.pop()
            out.append("")
            continue
        m = re.match(r"^\{\{fig:(\w+)\|(.*)\}\}\s*$", ln)
        if m:
            ln = f"**Figure.** {m.group(2)}\n\n*Picture description:* {figures.describe(m.group(1))}"
        ln = re.sub(r"\[\[([A-Z]+)\]\]", r"[\1]", ln)
        if links:
            ln = re.sub(r"\]\(([\w.-]+)\.html\)", r"](\1.md)", ln)
        else:
            ln = re.sub(r"\[([^\]]+)\]\([\w.-]+\.html\)", r"\1", ln)
        out.append(("> " + ln if ln.strip() else ">") if stack else ln)
    return "\n".join(out)


def page(title, eyebrow, sub, body, idx):
    prev_ = BOOKS[idx - 1] if idx > 0 else None
    next_ = BOOKS[idx + 1] if idx + 1 < len(BOOKS) else None
    nav = '<div class="nav"><span>' + (f'<a href="{prev_[0]}.html">← {html.escape(prev_[2])}</a>' if prev_ else "") + "</span><span>" + (f'<a href="{next_[0]}.html">{html.escape(next_[2])} →</a>' if next_ else "") + "</span></div>"
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} · PhaseKeep Learning Library</title><meta name="description" content="{html.escape(sub)}">
<style>{CSS}</style></head><body>
<a class="skip" href="#main">Skip to content</a>
<div class="top" role="navigation" aria-label="Library"><div><a href="index.html"><strong>PhaseKeep Learning Library</strong></a><span class="sp"></span><a href="A1-glossary.html">Glossary</a><a href="A2-ledger.html">Ledger</a><a href="A3-sources.html">Sources</a><a href="A5-faq.html">FAQ</a></div></div>
<main id="main" class="wrap"><div class="eyebrow">{html.escape(eyebrow)}</div><h1>{html.escape(title)}</h1><p class="sub">{html.escape(sub)}</p>
{body}
{nav}
<footer>Edition 03 draft · © 2026 Tyler O'Bryan, where applicable · PhaseKeep Research · text CC BY 4.0, code MIT (see NOTICE.txt) · AI-assisted research, documentation and numerical analysis · educational, technical review invited. PhaseKeep is an exploratory research proposal, not a demonstrated quantum computer. No PhaseKeep hardware measurement exists yet.</footer>
</main></body></html>"""


def build():
    combined = []
    for idx, (stem, label, title, sub) in enumerate(BOOKS):
        f = SRC / f"{stem}.md"
        if not f.exists():
            print("skip (no source):", stem)
            continue
        text = f.read_text(encoding="utf-8")
        text = re.sub(r"^# .*\n", "", text, count=1)
        text = xlink(text, stem)
        eyebrow = "Volume " + label if label.isdigit() else ("Appendix " + label[1:] if label.startswith("A") else "Start here")
        (HERE / f"{stem}.html").write_text(page(title, eyebrow, sub, block(text), idx), encoding="utf-8")
        (HERE / "markdown").mkdir(exist_ok=True)
        pm = f"# {title}\n\n*{sub}*\n\n" + portable(text) + "\n\n---\n*(c) 2026 Tyler O'Bryan, where applicable. PhaseKeep Research. Text CC BY 4.0, code MIT. AI-assisted research, documentation and numerical analysis. Draft for technical review.*\n"
        (HERE / "markdown" / f"{stem}.md").write_text(pm, encoding="utf-8")
        combined.append(f"\n\n---\n\n## {('Volume ' + label + ': ') if label.isdigit() else ''}{title}\n\n*{sub}*\n\n" + re.sub(r"^## ", "### ", re.sub(r"^### ", "#### ", portable(text, links=False), flags=re.M), flags=re.M))
        print("built", stem)
    cards = "".join(f'<a class="card" href="{s}.html"><span class="n">{"VOLUME " + l if l.isdigit() else ("APPENDIX " + l[1:] if l.startswith("A") else "START")}</span><b>{html.escape(t)}</b>{html.escape(sub)}</a>' for s, l, t, sub in BOOKS)
    idx_src = SRC / "index.md"
    intro = block(idx_src.read_text(encoding="utf-8")) if idx_src.exists() else ""
    (HERE / "index.html").write_text(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>PhaseKeep Learning Library · Edition 03</title><meta name="description" content="A plain-language book series about optical quantum information and the PhaseKeep research proposal.">
<style>{CSS}</style></head><body>
<div class="wrap"><div class="eyebrow">Open learning · Edition 03 (draft)</div><h1>PhaseKeep Learning Library</h1>
<p class="sub">Friends in all the right dimensions.</p>
{intro}
<h2>The series</h2><div class="cards">{cards}</div>
<footer>© 2026 Tyler O'Bryan, where applicable · PhaseKeep Research · text CC BY 4.0, code MIT (see NOTICE.txt) · AI-assisted research, documentation and numerical analysis · educational; technical review invited. PhaseKeep is an exploratory research proposal, not a demonstrated quantum computer.</footer></div></body></html>""", encoding="utf-8")
    print("built index")
    toc = "\n".join(f"- {('Volume ' + l + ': ') if l.isdigit() else ''}{t}" for s_, l, t, sub in BOOKS if (SRC / f"{s_}.md").exists())
    head = "# PhaseKeep Learning Library, Edition 03 (complete text)\n\n*Friends in all the right dimensions.*\n\n*(c) 2026 Tyler O'Bryan, where applicable. PhaseKeep Research. Text CC BY 4.0, code MIT (see NOTICE.txt). AI-assisted research, documentation and numerical analysis. Draft for technical review.*\n\n" + (portable(idx_src.read_text(encoding="utf-8")) if idx_src.exists() else "") + "\n\n## Contents\n\n" + toc
    full = head + "".join(combined)
    (HERE / "PhaseKeep-Learning-Library-complete.md").write_text(full, encoding="utf-8")
    (HERE / "PhaseKeep-Learning-Library-complete.txt").write_text(full.replace("**", "").replace("> ", "  "), encoding="utf-8")
    print("built combined text,", len(full.split()), "words")


if __name__ == "__main__":
    build()
