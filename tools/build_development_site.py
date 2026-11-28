#!/usr/bin/env python3
"""Build the PhaseKeep research-development website from Markdown sources.

Standard library only.  Run from anywhere:  python3 -I tools/build_development_site.py
Add --check to verify that the files on disk are exactly what the sources produce.

Inputs (never modified):
  docs/development/**/*.md       authored development pages
  checkpoints/*/README.md, CODEX_HANDOFF.md, docs/*.md
                                 original checkpoint files, rendered unchanged
Outputs (fully regenerated):
  development/**/*.html

Design rules
  * No Markdown construct is silently dropped.  Anything this converter does not
    support (raw HTML, images, footnotes, reference links, unknown LaTeX, unknown
    escapes, broken table rows, links to missing files or anchors) stops the build
    with a file:line message.
  * It never writes outside development/ and never reads or writes library/, releases/,
    reader.html or any licence file.
  * Equations in the original checkpoint pages are plain text and are shown as written.
    New pages may use $...$ for small inline formulas (see MATH below).
"""
import html, os, re, sys, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEV_SRC = os.path.join(ROOT, "docs", "development")
CK_SRC = os.path.join(ROOT, "checkpoints")
OUT = os.path.join(ROOT, "development")
GH = "https://github.com/tyses101/phasekeep-research/blob/main/"
TAGS = ["DERIVED", "REPORTED", "SIMULATED", "ASSUMED", "PROPOSED", "MEASURED", "UNVERIFIED", "BLOCKED"]

# Order of the authored pages (path relative to docs/development, without .md).  The menu group is the first item.
ORDER = [
    ("Latest development", ["checkpoints/hybrid-atomic-2026-11-28"]),
    ("Atomic-register research", ['atomic-register/01_the_short_version', 'atomic-register/02_the_full_story/00_contents', 'atomic-register/02_the_full_story/01_architecture', 'atomic-register/02_the_full_story/02_register_geometry', 'atomic-register/02_the_full_story/03_physical_development', 'atomic-register/02_the_full_story/04_digital_reference', 'atomic-register/02_the_full_story/05_ramm_instructions', 'atomic-register/02_the_full_story/06_iqa', 'atomic-register/02_the_full_story/07_imperfections_P2CIM', 'atomic-register/02_the_full_story/08_drift_E5', 'atomic-register/02_the_full_story/09_finite_control_E6', 'atomic-register/02_the_full_story/10_echo_timing_E7', 'atomic-register/02_the_full_story/11_envelope_balance_E7D', 'atomic-register/02_the_full_story/12_platforms_G0', 'atomic-register/02_the_full_story/13_pending', 'atomic-register/02_the_full_story/14_framing', 'atomic-register/03_reference/evidence_and_failures', 'atomic-register/03_reference/experiments', 'atomic-register/03_reference/reproduce', 'atomic-register/03_reference/sources', 'atomic-register/03_reference/terms', 'atomic-register/03_reference/timeline', 'atomic-register/05_whats_next', 'atomic-register/README', 'checkpoints/atomic-register-2026-11-28']),
    ("Overview", ["phasekeep-from-the-beginning", "README", "plain-language-overview"]),
    ("Question", ["central-question", "research-status"]),
    ("Architecture and terms", ["register-of-terms", "tetragon", "gea", "qde-relational", "buddy", "iqa", "paladin", "docked-scheduling"]),
    ("Physical feasibility", ["physical-feasibility", "active-vs-replaceable"]),
    ("Timeline", ["timeline", "checkpoints/v0", "checkpoints/v0.1", "checkpoints/v0.2", "checkpoints/v0.3",
                  "checkpoints/v0.4", "checkpoints/v0.5", "checkpoints/v0.6", "checkpoints/v0.7",
                  "checkpoints/v0.8", "checkpoints/v0.9", "checkpoints/v1.0", "checkpoints/qde-2026-11-27"]),
    ("Results and evidence", ["computational-results", "negative-results", "errata", "literature", "open-problems"]),
    ("Reproduce and download", ["reproducibility", "downloads", "roadmap-v1.1"]),
    ("Project", ["repository-reconciliation", "citing", "contributing"]),
]

MATH_CMDS = {r"\pi": "π", r"\epsilon": "ε", r"\varepsilon": "ε", r"\delta": "δ", r"\theta": "θ", r"\geq": "≥",
             r"\leq": "≤", r"\approx": "≈", r"\times": "×", r"\cdot": "·", r"\pm": "±", r"\sigma": "σ",
             r"\alpha": "α", r"\beta": "β", r"\rangle": "⟩", r"\langle": "⟨", r"\to": "→", r"\ne": "≠"}


class BuildError(Exception):
    pass


def fail(path, line, msg):
    raise BuildError("%s:%d: %s" % (os.path.relpath(path, ROOT), line, msg))


# ---------------------------------------------------------------- inline
def render_math(expr, path, line):
    out, i = [], 0
    def group(j):
        if j < len(expr) and expr[j] == "{":
            d, k = 1, j + 1
            while k < len(expr) and d:
                d += (expr[k] == "{") - (expr[k] == "}")
                k += 1
            if d:
                fail(path, line, "unbalanced braces in math: $%s$" % expr)
            return expr[j + 1:k - 1], k
        m = re.match(r"[A-Za-z0-9.+-]", expr[j:])
        if not m:
            fail(path, line, "bad ^ or _ in math: $%s$" % expr)
        return expr[j], j + 1
    while i < len(expr):
        c = expr[i]
        if c == "\\":
            m = re.match(r"\\[A-Za-z]+", expr[i:])
            cmd = m.group(0) if m else None
            if cmd == r"\sqrt":
                g, i = group(i + len(cmd))
                out.append("√(" + render_math(g, path, line) + ")")
            elif cmd in MATH_CMDS:
                out.append(MATH_CMDS[cmd]); i += len(cmd)
            else:
                fail(path, line, "unsupported math command %r in $%s$" % (cmd or expr[i:i + 2], expr))
        elif c in "^_":
            g, i = group(i + 1)
            tag = "sup" if c == "^" else "sub"
            out.append("<%s>%s</%s>" % (tag, render_math(g, path, line), tag))
        elif c in "{}":
            i += 1
        else:
            out.append(html.escape(c)); i += 1
    return "".join(out)


def inline(text, path, line, links):
    """Render inline Markdown.  links: list collecting (url, line) for later validation."""
    stash = []
    def keep(s):
        stash.append(s)
        return "\x00%d\x00" % (len(stash) - 1)
    def code(m):
        return keep("<code>%s</code>" % html.escape(m.group(2)))
    text = re.sub(r"(`+)(.+?)\1", code, text)
    text = re.sub(r"(?<!\\)\$([^$\n]+?)(?<!\\)\$", lambda m: keep('<span class="math">%s</span>' % render_math(m.group(1), path, line)), text)
    if re.search(r"(?<!\\)\$", text):
        fail(path, line, "unpaired $ (escape a literal dollar sign as \\$)")
    # escapes
    def esc(m):
        return keep(html.escape(m.group(1)))
    text = re.sub(r"\\([\\`*_{}\[\]()#+\-.!|$<>~])", esc, text)
    if "\\" in text:
        fail(path, line, "unsupported backslash sequence: " + text[text.index("\\"):][:20])
    if re.search(r"</?[A-Za-z][^>]*>", text):
        fail(path, line, "raw HTML is not supported: " + re.search(r"</?[A-Za-z][^>]*>", text).group(0))
    if "![" in text:
        fail(path, line, "images are not supported")
    if "[^" in text:
        fail(path, line, "footnotes are not supported")
    text = html.escape(text, quote=False)
    def link(m):
        links.append((m.group(2), line))
        return keep('<a href="%s">%s</a>' % ("\x01%d\x01" % (len(links) - 1), inline_nolink(m.group(1))))
    def inline_nolink(t):
        t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
        t = re.sub(r"(?<![\w*])\*(?![\s*])([^*\n]+?)(?<![\s*])\*(?![\w*])", r"<em>\1</em>", t)
        return t
    text = re.sub(r"\[([^\]\n]+)\]\(([^)\s]+)\)", link, text)
    if re.search(r"\]\[", text):
        fail(path, line, "reference-style links are not supported")
    text = inline_nolink(text)
    # evidence chips
    for t in TAGS:
        text = text.replace("<strong>%s</strong>" % t, '<span class="tag t-%s">%s</span>' % (t, t))
        text = text.replace("[%s]" % t, '<span class="tag t-%s">%s</span>' % (t, t))
    def unstash(s):
        while True:
            n = re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], s)
            if n == s:
                return n
            s = n
    return unstash(text)


# ---------------------------------------------------------------- blocks
def slug(t):
    t = re.sub(r"<[^>]+>", "", t).lower()
    t = re.sub(r"[^\w\s-]", "", t, flags=re.U)
    return re.sub(r"\s+", "-", t.strip())


LIST_RE = re.compile(r"^(\s*)([-*]|\d+\.)\s+(.*)$")


def parse(path, src):
    lines = src.split("\n")
    n, i = len(lines), 0
    out, heads, links, ids = [], [], [], {}
    title = None
    def table_cells(row, ln):
        row = row.strip()
        if not (row.startswith("|") and row.endswith("|")):
            fail(path, ln, "table row must start and end with |")
        cells, cur, k = [], "", 1
        body = row[1:-1]
        sep_row = bool(re.match(r"^[\s:|-]+$", body))
        k = 0
        in_code = False
        while k < len(body):
            ch = body[k]
            if ch == "`":
                in_code = not in_code
            if ch == "\\" and k + 1 < len(body) and body[k + 1] == "|":
                cur += "\\|"; k += 2; continue
            if (ch == "|" and not in_code and not sep_row and k + 1 < len(body) and not body[k + 1].isspace()):
                cur += ch          # |0>, |alpha - beta|^2: a pipe glued to the next character is text, not a cell border
            elif ch == "|" and not in_code:
                cells.append(cur.strip()); cur = ""
            else:
                cur += ch
            k += 1
        cells.append(cur.strip())
        return cells
    def parse_list(i, base):
        items, ordered, start = [], False, None
        while i < n:
            m = LIST_RE.match(lines[i])
            if not m or len(m.group(1)) < base:
                break
            if len(m.group(1)) > base:
                break
            ordered = m.group(2)[0].isdigit()
            if start is None and ordered:
                start = int(m.group(2)[:-1])
            text, ln = m.group(3), i + 1
            i += 1
            sub = ""
            while i < n:
                if lines[i].strip() == "":
                    j = i
                    while j < n and lines[j].strip() == "":
                        j += 1
                    if j < n and LIST_RE.match(lines[j]) and len(LIST_RE.match(lines[j]).group(1)) > base:
                        i = j
                        continue
                    break
                mm = LIST_RE.match(lines[i])
                if mm and len(mm.group(1)) > base:
                    inner, i = parse_list(i, len(mm.group(1)))
                    sub += inner
                    continue
                if mm and len(mm.group(1)) <= base:
                    break
                if re.match(r"^\s{2,}\S", lines[i]):
                    text += " " + lines[i].strip(); i += 1
                    continue
                break
            items.append("<li>%s%s</li>" % (inline(text, path, ln, links), sub))
        tag = "ol" if ordered else "ul"
        attr = ' start="%d"' % start if ordered and start not in (None, 1) else ""
        return "<%s%s>%s</%s>" % (tag, attr, "".join(items), tag), i
    def blocks(i, stop=None):
        nonlocal title
        res = []
        while i < n:
            ln = lines[i]
            if stop and ln.strip() == stop:
                return "".join(res), i
            if ln.strip() == "":
                i += 1; continue
            if ln.startswith("```"):
                lang = ln[3:].strip()
                j = i + 1
                buf = []
                while j < n and not lines[j].startswith("```"):
                    buf.append(lines[j]); j += 1
                if j >= n:
                    fail(path, i + 1, "unterminated code fence")
                res.append('<pre><code%s>%s</code></pre>' % (' class="lang-%s"' % html.escape(lang) if lang else "", html.escape("\n".join(buf))))
                i = j + 1; continue
            m = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", ln)
            if m:
                lvl = len(m.group(1))
                if lvl > 4:
                    fail(path, i + 1, "headings deeper than level 4 are not supported")
                h = inline(m.group(2), path, i + 1, links)
                sid = slug(h)
                k = ids.get(sid, 0); ids[sid] = k + 1
                if k:
                    sid += "-%d" % k
                if lvl == 1 and title is None:
                    title = re.sub(r"<[^>]+>", "", h)
                if lvl in (2, 3):
                    heads.append((lvl, sid, re.sub(r"<[^>]+>", "", h)))
                res.append('<h%d id="%s">%s</h%d>' % (lvl, sid, h, lvl)); i += 1; continue
            if re.match(r"^(---|\*\*\*|___)\s*$", ln):
                res.append("<hr>"); i += 1; continue
            if ln.startswith(":::"):
                m = re.match(r"^:::\s*(key|plain|try|watch|evidence|deeper|story)\s+(.*\S)\s*$", ln)
                if not m:
                    fail(path, i + 1, "box syntax is ':::  key|plain|try|watch|evidence  Title'")
                inner, j = blocks(i + 1, stop=":::")
                if j >= n:
                    fail(path, i + 1, "unterminated ::: box")
                res.append('<div class="box %s"><div class="bt">%s</div>%s</div>' % (m.group(1), inline(m.group(2), path, i + 1, links), inner))
                i = j + 1; continue
            if ln.startswith(">"):
                buf = []
                while i < n and lines[i].startswith(">"):
                    buf.append(re.sub(r"^>\s?", "", lines[i])); i += 1
                res.append("<blockquote>%s</blockquote>" % inline(" ".join(buf), path, i, links)); continue
            if ln.startswith("|"):
                if i + 1 >= n or not re.match(r"^\|[\s:|-]+\|\s*$", lines[i + 1]):
                    fail(path, i + 1, "table without a separator row")
                head = table_cells(ln, i + 1)
                sep = table_cells(lines[i + 1], i + 2)
                if len(sep) != len(head):
                    fail(path, i + 2, "separator row has %d cells, header has %d" % (len(sep), len(head)))
                aligns = []
                for s in sep:
                    aligns.append("right" if s.endswith(":") and not s.startswith(":") else "left")
                rows = []
                j = i + 2
                while j < n and lines[j].startswith("|"):
                    cells = table_cells(lines[j], j + 1)
                    if len(cells) != len(head):
                        fail(path, j + 1, "table row has %d cells, header has %d" % (len(cells), len(head)))
                    rows.append(cells); j += 1
                t = "<div class=\"tw\" tabindex=\"0\" role=\"region\" aria-label=\"Table (scrolls sideways on narrow screens)\"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (
                    "".join("<th>%s</th>" % inline(c, path, i + 1, links) for c in head),
                    "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c, path, k + i + 3, links) for c in r) for k, r in enumerate(rows)))
                res.append(t); i = j; continue
            if LIST_RE.match(ln):
                h, i = parse_list(i, len(LIST_RE.match(ln).group(1)))
                res.append(h); continue
            if re.match(r"^\s*<", ln) and re.match(r"^\s*</?[A-Za-z!]", ln):
                fail(path, i + 1, "raw HTML blocks are not supported")
            if re.match(r"^\s*(\[[^\]]+\]:)", ln) and not re.match(r"^\s*\[(%s)\]:" % "|".join(TAGS), ln):
                fail(path, i + 1, "reference definitions are not supported")
            buf, start = [], i
            while i < n and lines[i].strip() != "" and not re.match(r"^(#{1,6}\s|```|\||>|:::)", lines[i]) and not (buf and LIST_RE.match(lines[i])):
                if re.match(r"^(===+|---+)\s*$", lines[i]):
                    fail(path, i + 1, "setext headings are not supported")
                buf.append(lines[i].strip()); i += 1
            res.append("<p>%s</p>" % inline(" ".join(buf), path, start + 1, links))
        return "".join(res), i
    body, _ = blocks(0)
    return body, (title or os.path.basename(path)), heads, links, ids


# ---------------------------------------------------------------- site model
CSS = r"""
:root{--bg:#faf8f3;--fg:#1f2933;--mut:#5d6b78;--line:#ddd8cc;--card:#fff;--acc:#1b5e86;--acc2:#7a4a12;
--key:#e5f0f7;--keyb:#1b5e86;--plain:#eaf5ec;--plainb:#2f7d4a;--deeper:#f1ecf8;--deeperb:#6a4aa0;--try:#fdf3dc;--tryb:#a8730a;
--watch:#fbe6e3;--watchb:#b3382b;--evidence:#eceef1;--evidenceb:#56606d;--story:#f6efe6;--storyb:#8b5a2b}
@media (prefers-color-scheme:dark){:root{--bg:#14181d;--fg:#e4e8ec;--mut:#9aa6b2;--line:#2c343d;--card:#1b2128;--acc:#7cc0ea;--acc2:#e0b277;
--key:#16303f;--keyb:#6fb3dc;--plain:#16301f;--plainb:#6fcf8d;--deeper:#2a2140;--deeperb:#b79ae8;--try:#3a2e12;--tryb:#e8b84f;
--watch:#3c1b18;--watchb:#f08c80;--evidence:#232a31;--evidenceb:#a0abb7;--story:#33271a;--storyb:#d9a66a}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font:18px/1.7 Georgia,'Gelasio','Times New Roman',serif}
.top{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--line);font:14px/1.4 system-ui,sans-serif}
.top .in{max-width:860px;margin:auto;padding:8px 16px;display:flex;gap:6px 16px;flex-wrap:wrap;align-items:center}
.top a{color:var(--acc);text-decoration:none}.top .brand{font-weight:700;color:var(--fg)}
.top details{width:100%}.top summary{cursor:pointer;padding:6px 0;min-height:44px;display:flex;align-items:center}
.menu{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px 18px;padding:6px 0 12px}
.menu b{display:block;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--mut);margin-bottom:2px}
.menu a{display:block;padding:4px 0;min-height:32px}
.status{background:var(--try);border-bottom:1px solid var(--tryb);font:13px/1.45 system-ui,sans-serif}
.status div{max-width:860px;margin:auto;padding:6px 16px}
.wrap{max-width:860px;margin:0 auto;padding:24px 16px 72px}
h1{font:700 2.05rem/1.2 system-ui,'Inter',sans-serif;margin:.2em 0 .4em}
h2{font:700 1.4rem/1.3 system-ui,'Inter',sans-serif;margin:2em 0 .4em;padding-top:.5em;border-top:1px solid var(--line)}
h3{font:700 1.1rem/1.35 system-ui,'Inter',sans-serif;margin:1.5em 0 .3em}h4{font:700 1rem/1.35 system-ui,sans-serif;margin:1.2em 0 .2em}
p,li{max-width:72ch}li{margin:.25em 0}a{color:var(--acc)}
pre{background:var(--evidence);padding:12px 14px;border-radius:8px;overflow-x:auto;margin:1em 0}pre code{background:none;padding:0;white-space:pre;overflow-wrap:normal}
code{font:.86em ui-monospace,Menlo,Consolas,monospace;background:var(--evidence);padding:1px 5px;border-radius:4px;overflow-wrap:anywhere}
.math{font-family:'Cambria Math','STIX Two Math',Georgia,serif;font-style:italic;white-space:nowrap}
blockquote{margin:1em 0;padding:.2em 1em;border-left:3px solid var(--line);color:var(--mut)}
.tw{overflow-x:auto;margin:1em 0;border:1px solid var(--line);border-radius:8px;background:var(--card);-webkit-overflow-scrolling:touch}
table{border-collapse:collapse;width:100%;min-width:34rem;font:15px/1.5 system-ui,sans-serif}
th,td{padding:8px 11px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line)}th{background:var(--evidence)}tr:last-child td{border-bottom:0}
.box{margin:1.3em 0;padding:12px 16px;border-radius:8px;border-left:5px solid var(--evidenceb);background:var(--evidence);font:16px/1.65 system-ui,sans-serif}
.box>.bt{font:700 12px system-ui,sans-serif;letter-spacing:.1em;text-transform:uppercase;margin-bottom:4px}
.box table{min-width:0;font-size:14px}.box .tw{background:transparent}.box p,.box li{max-width:none}.box p:last-child{margin-bottom:0}
.key{background:var(--key);border-color:var(--keyb)}.key>.bt{color:var(--keyb)}
.plain{background:var(--plain);border-color:var(--plainb)}.plain>.bt{color:var(--plainb)}
.try{background:var(--try);border-color:var(--tryb)}.try>.bt{color:var(--tryb)}
.watch{background:var(--watch);border-color:var(--watchb)}.watch>.bt{color:var(--watchb)}
.deeper{background:var(--deeper);border-color:var(--deeperb)}.deeper>.bt{color:var(--deeperb)}
.story{background:var(--story);border-color:var(--storyb)}.story>.bt{color:var(--storyb)}
.tag{display:inline-block;font:700 11px system-ui,sans-serif;letter-spacing:.04em;padding:1px 7px;border-radius:99px;vertical-align:1px;border:1px solid currentColor}
.t-DERIVED,.t-REPORTED{color:var(--plainb)}.t-SIMULATED{color:var(--keyb)}.t-ASSUMED,.t-UNVERIFIED{color:var(--tryb)}
.t-PROPOSED{color:var(--evidenceb)}.t-MEASURED{color:var(--deeperb)}.t-BLOCKED{color:var(--watchb)}
.toc{font:15px/1.5 system-ui,sans-serif;margin:1em 0;border:1px solid var(--line);border-radius:8px;padding:6px 14px;background:var(--card)}
.toc summary{cursor:pointer;min-height:36px;display:flex;align-items:center}.toc ul{margin:.2em 0 .6em;padding-left:1.2em}
.nav{display:flex;justify-content:space-between;gap:12px;margin-top:3em;padding-top:1em;border-top:1px solid var(--line);font:15px system-ui,sans-serif}
.orig{font:14px/1.5 system-ui,sans-serif;color:var(--mut);border:1px dashed var(--line);border-radius:8px;padding:8px 12px;margin:0 0 1.2em}
footer{margin-top:3em;font:13px/1.5 system-ui,sans-serif;color:var(--mut);border-top:1px solid var(--line);padding-top:1em}
a.skip{position:absolute;left:-999px;top:0}a.skip:focus{left:8px;top:8px;background:var(--card);padding:8px 12px;z-index:9;border:1px solid var(--line)}
a:focus-visible,summary:focus-visible{outline:3px solid var(--acc);outline-offset:2px}
@media (max-width:560px){.top{position:static}table{min-width:24rem}.box table{min-width:0}.box th,.box td{padding:6px 7px;font-size:13px;overflow-wrap:anywhere}body{font-size:17px}h1{font-size:1.7rem}.nav{flex-direction:column}}
@media print{.top,.nav,.status{display:none}body{background:#fff;color:#000;font-size:11.5pt}pre{white-space:pre-wrap}}
"""


def collect_pages():
    pages = []  # dict(src, out, kind, group, label)
    seen = set()
    for group, names in ORDER:
        for nm in names:
            src = os.path.join(DEV_SRC, nm + ".md")
            if not os.path.isfile(src):
                raise BuildError("page listed in ORDER is missing: docs/development/%s.md" % nm)
            out = "index.html" if nm == "README" else nm + ".html"
            pages.append(dict(src=src, out=out, kind="dev", group=group))
            seen.add(os.path.abspath(src))
    for root, _, files in os.walk(DEV_SRC):
        for f in files:
            if f.endswith(".md") and os.path.abspath(os.path.join(root, f)) not in seen:
                raise BuildError("authored page not listed in ORDER (would be silently omitted): " + os.path.relpath(os.path.join(root, f), ROOT))
    for v in sorted(os.listdir(CK_SRC)) if os.path.isdir(CK_SRC) else []:
        d = os.path.join(CK_SRC, v)
        if not os.path.isdir(d):
            continue
        for rel in ["README.md", "CODEX_HANDOFF.md"] + ["docs/" + f for f in sorted(os.listdir(os.path.join(d, "docs"))) if f.endswith(".md")]:
            src = os.path.join(d, rel)
            if os.path.isfile(src):
                pages.append(dict(src=src, out="source/%s/%s.html" % (v, rel[:-3]), kind="orig", group="Source", ck=v))
    return pages


def resolve_link(url, src, pages_by_src, outs, line):
    """Return (kind, target) where kind is 'ext', 'page', 'file', 'anchor'."""
    if re.match(r"^(https?:|mailto:)", url):
        return "ext", url, None
    if url.startswith("#"):
        return "anchor", None, url[1:]
    u, _, frag = url.partition("#")
    tgt = os.path.normpath(os.path.join(os.path.dirname(src), u))
    if tgt in pages_by_src:
        return "page", pages_by_src[tgt], frag
    if os.path.isdir(tgt):
        idx = os.path.join(tgt, "index.html")
        if os.path.isfile(idx):
            return "file", idx, None
    if os.path.isfile(tgt):
        rel = os.path.relpath(tgt, ROOT).replace(os.sep, "/")
        if rel.endswith(".md"):
            if rel.startswith("library/markdown/"):
                h = os.path.join(ROOT, "library", os.path.basename(rel)[:-3] + ".html")
                if os.path.isfile(h):
                    return "file", h, frag
            return "ext", GH + rel.replace(os.sep, "/") + ("#" + frag if frag else ""), None
        return "file", tgt, frag
    return "missing", tgt, None


def page_html(pg, body, title, heads, nav_idx, pages, links_r):
    outp = os.path.join(OUT, pg["out"])
    depth_rel = os.path.relpath(OUT, os.path.dirname(outp))
    def href(p):
        return os.path.relpath(os.path.join(OUT, p["out"]), os.path.dirname(outp)).replace(os.sep, "/")
    groups = []
    for g, _ in ORDER:
        items = [p for p in pages if p["kind"] == "dev" and p["group"] == g]
        groups.append((g, items))
    def label(p):
        return p["title"]
    menu = "".join('<div><b>%s</b>%s</div>' % (html.escape(g), "".join('<a href="%s">%s</a>' % (href(p), html.escape(label(p))) for p in items)) for g, items in groups)
    site_root = os.path.relpath(ROOT, os.path.dirname(outp)).replace(os.sep, "/")
    toc = ""
    h2 = [h for h in heads if h[0] == 2]
    if len(h2) >= 4:
        toc = '<details class="toc"><summary>On this page</summary><ul>%s</ul></details>' % "".join('<li><a href="#%s">%s</a></li>' % (i, html.escape(t)) for _, i, t in h2)
    banner = ""
    if pg["kind"] == "orig":
        rel = os.path.relpath(pg["src"], ROOT).replace(os.sep, "/")
        banner = ('<div class="orig">Original checkpoint file <code>%s</code>, rendered here without any change to its text. '
                  'The Markdown source is the authoritative copy (<a href="%s/%s">raw file</a>). '
                  'Later corrections are in <a href="%s">Errata</a>.</div>') % (rel, site_root, rel, href(next(p for p in pages if p["out"] == "errata.html")))
    prev_next = ""
    dev = [p for p in pages if p["kind"] == "dev"]
    if pg["kind"] == "dev":
        k = dev.index(pg)
        a = '<a href="%s">← %s</a>' % (href(dev[k - 1]), html.escape(dev[k - 1]["title"])) if k > 0 else "<span></span>"
        b = '<a href="%s">%s →</a>' % (href(dev[k + 1]), html.escape(dev[k + 1]["title"])) if k + 1 < len(dev) else "<span></span>"
        prev_next = '<nav class="nav" aria-label="Previous and next page">%s%s</nav>' % (a, b)
    if toc and "</h1>" in body:
        body = body.replace("</h1>", "</h1>" + toc, 1)       # contents list sits right under the page title
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s · PhaseKeep development</title>
<meta name="description" content="PhaseKeep Research development layer: provisional, model-based, no hardware measurements.">
<style>%(css)s</style></head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><nav class="in" aria-label="Site"><a class="brand" href="%(root)s/index.html">PhaseKeep Research</a>
<a href="%(home)s">Development</a><a href="%(root)s/library/index.html">Learning library (frozen Rev H)</a>
<a href="%(root)s/reader.html">Reader</a>
<details><summary>All development pages</summary><div class="menu">%(menu)s</div></details></nav></header>
<div class="status"><div><strong>Research-development layer.</strong> Provisional and model-based. No hardware measurement exists; no physical advantage is claimed. Revision H is frozen and separate.</div></div>
<main class="wrap" id="main">%(banner)s%(body)s%(nav)s
<footer>Tyler O'Bryan · PhaseKeep Research · AI-assisted research, documentation and numerical analysis. Authored text: CC BY 4.0. Code: MIT. See the <a href="%(root)s/docs/development/README.md">licence scope</a> and <a href="%(root)s/NOTICE.txt">NOTICE</a>.</footer></main></body></html>
""" % dict(title=html.escape(title), css=CSS, root=site_root, home=os.path.relpath(os.path.join(OUT, "index.html"), os.path.dirname(outp)).replace(os.sep, "/"),
          menu=menu, banner=banner, body=body, nav=prev_next)


def build():
    pages = collect_pages()
    pages_by_src = {os.path.normpath(p["src"]): p for p in pages}
    parsed = {}
    for p in pages:
        with open(p["src"], encoding="utf-8", newline="") as f:
            src = f.read()
        if "\r" in src:
            raise BuildError("%s has CR characters; expected LF line endings" % os.path.relpath(p["src"], ROOT))
        body, title, heads, links, ids = parse(p["src"], src)
        p["title"] = title
        parsed[p["src"]] = (body, heads, links, ids)
    outs = {}
    for p in pages:
        body, heads, links, ids = parsed[p["src"]]
        outp = os.path.join(OUT, p["out"])
        # validate and rewrite links
        def sub(m):
            idx = int(m.group(1))
            url, line = links[idx]
            kind, tgt, frag = resolve_link(url, p["src"], pages_by_src, outs, line)
            if kind == "ext":
                return html.escape(tgt if tgt else url, quote=True)
            if kind == "anchor":
                if frag not in ids:
                    fail(p["src"], line, "anchor #%s not found in this page" % frag)
                return "#" + frag
            if kind == "missing":
                fail(p["src"], line, "link target does not exist: " + url)
            if kind == "page":
                tids = parsed[tgt["src"]][3]
                if frag and frag not in tids:
                    fail(p["src"], line, "anchor #%s not found in %s" % (frag, os.path.relpath(tgt["src"], ROOT)))
                r = os.path.relpath(os.path.join(OUT, tgt["out"]), os.path.dirname(outp)).replace(os.sep, "/")
                return r + ("#" + frag if frag else "")
            r = os.path.relpath(tgt, os.path.dirname(outp)).replace(os.sep, "/")
            return r + ("#" + frag if frag else "")
        body = re.sub(r"\x01(\d+)\x01", sub, body)
        outs[outp] = page_html(p, body, p["title"], heads, None, pages, links)
    return outs


def main():
    check = "--check" in sys.argv
    try:
        outs = build()
    except BuildError as e:
        print("BUILD ERROR:", e, file=sys.stderr)
        return 2
    if check:
        bad = 0
        for path, text in outs.items():
            try:
                with open(path, encoding="utf-8", newline="") as f:
                    if f.read() != text:
                        print("STALE:", os.path.relpath(path, ROOT)); bad += 1
            except FileNotFoundError:
                print("MISSING:", os.path.relpath(path, ROOT)); bad += 1
        extra = []
        expected_paths = {os.path.normpath(path) for path in outs}
        for root, _, files in os.walk(OUT):
            for f in files:
                p = os.path.join(root, f)
                if os.path.normpath(p) not in expected_paths:
                    extra.append(os.path.relpath(p, ROOT))
        for e in extra:
            print("UNEXPECTED:", e); bad += 1
        print("check: %d pages, %d problems" % (len(outs), bad))
        return 1 if bad else 0
    for path, text in outs.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(text)
    print("wrote %d pages under development/" % len(outs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
