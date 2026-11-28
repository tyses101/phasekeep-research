"""Build the offline reader. Never rewrites any source.

Contents, in order:
  1. Edition 03, Revision H (frozen): chapters taken unchanged from library/ HTML.
  2. Edition 04 (working draft): chapters from library-edition-04/ HTML.
  3. The whole story: the development site's one-page overview (development/phasekeep-from-the-beginning.html).
Chapter, anchor and figure IDs are namespaced so the combined book has no collisions; existing Edition 03 anchors
(#<chapter-stem> and #<chapter-stem>--<id>) are unchanged. The previous frozen-only reader is kept as reader-rev-h.html.
"""
from pathlib import Path
import html
import posixpath
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / 'library'
ED4 = ROOT / 'library-edition-04'
STORY = 'phasekeep-from-the-beginning.html'
GITHUB = 'https://github.com/tyses101/phasekeep-research/blob/main/'
CARD = r'<a class="card" href="([^"]+)">.*?<b>(.*?)</b>'

# (group label, base folder, [(file, title)], markdown path for "Markdown on GitHub", note shown at top of chapter)
groups = [('Edition 03 · Revision H (frozen)', 'library',
           re.findall(CARD, (LIB / 'index.html').read_text(encoding='utf-8')), 'library/markdown', None)]
if (ED4 / 'index.html').exists():
    groups.append(('Edition 04 · working draft', 'library-edition-04',
                   re.findall(CARD, (ED4 / 'index.html').read_text(encoding='utf-8')), 'library-edition-04/markdown',
                   'Edition 04 working draft · research snapshot as of 28 November 2026 · not frozen'))
if (ROOT / 'development' / STORY).exists():
    groups.append(('The whole story', 'development', [(STORY, 'PhaseKeep from the beginning')], 'docs/development',
                   'Educational overview from the development site · research snapshot as of 28 November 2026'))

groups.append(('Research reference and working records', 'development', [
    ('register-of-terms.html', 'Consolidated terminology and definitions'),
    ('timeline.html', 'Research development timeline'),
    ('negative-results.html', 'Negative results'),
    ('errata.html', 'Corrections and errata'),
    ('open-problems.html', 'Open research questions'),
    ('reproducibility.html', 'Simulation and reproduction resources'),
    ('literature.html', 'References and verification status')], 'docs/development',
    'Current development reference; evidence qualifications and historical corrections retained'))

slug_of = {}
for _, base, items, _, _ in groups:
    for name, _ in items:
        stem = Path(name).stem
        assert stem not in slug_of.values(), f'duplicate chapter id {stem}'
        slug_of[posixpath.join(base, name)] = stem

sections, options, number = [], [], 0
for label, base, items, md_dir, note in groups:
    opts = []
    for name, title in items:
        slug = slug_of[posixpath.join(base, name)]
        text = (ROOT / base / name).read_text(encoding='utf-8')
        body = re.search(r'<main[^>]*>(.*?)</main>', text, re.S).group(1)
        body = re.sub(r'<div class="nav">.*?</div>', '', body, flags=re.S)
        # Namespace all IDs, including inline SVG references, across the combined book.
        body = re.sub(r'\bid="([^"]+)"', lambda m: f'id="{slug}--{m[1]}"', body)
        body = re.sub(r'url\(#([^)]+)\)', lambda m: f'url(#{slug}--{m[1]})', body)

        def link(match, base=base, slug=slug):
            target = html.unescape(match[1]); parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or target.startswith('mailto:'):
                return match[0]
            if not parsed.path and parsed.fragment:
                return f'href="#{slug}--{html.escape(parsed.fragment, quote=True)}"'
            path = posixpath.normpath(posixpath.join(base, parsed.path))
            if path in slug_of:
                anchor = slug_of[path] + ('--' + parsed.fragment if parsed.fragment else '')
                return f'href="#{html.escape(anchor, quote=True)}"'
            return f'href="{html.escape(path + ("#" + parsed.fragment if parsed.fragment else ""), quote=True)}"'
        body = re.sub(r'href="([^"]+)"', link, body)
        md = f'{GITHUB}{md_dir}/{slug}.md'
        sources = f'<p class="source-links"><a href="{base}/{name}">Original HTML</a> · <a href="{md}">Markdown on GitHub</a></p>'
        banner = f'<p class="edition-note">{html.escape(note)}</p>' if note else ''
        sections.append(f'<section class="chapter" id="{slug}" data-title="{html.escape(html.unescape(title), quote=True)}">{sources}{banner}{body}</section>')
        opts.append(f'<option value="{slug}">{number + 1}. {title}</option>')
        number += 1
    options.append(f'<optgroup label="{html.escape(label, quote=True)}">' + ''.join(opts) + '</optgroup>')

style = re.search(r'<style>(.*?)</style>', (LIB / 'index.html').read_text(encoding='utf-8'), re.S).group(1)
page = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>PhaseKeep · Library reader</title><meta name="description" content="Read the PhaseKeep library: the frozen Edition 03 (Revision H), the Edition 04 working draft and the one-page story, with chapter navigation or continuous scrolling. Works offline.">
<style>''' + style + '''
.reader-bar{position:sticky;top:0;z-index:20;background:var(--bg);border-bottom:1px solid var(--line);padding:12px 16px;font:15px/1.5 system-ui}
.reader-inner{max-width:960px;margin:auto;display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.reader-title{font-weight:750;margin-right:auto}.reader-inner a{color:var(--acc)}
.reader-controls{width:100%;display:flex;align-items:center;flex-wrap:wrap;gap:10px}
button,select{font:inherit;color:var(--fg);background:var(--card);border:1px solid var(--line);border-radius:6px;padding:9px 12px;min-height:44px}
button{cursor:pointer}button:disabled{opacity:.45;cursor:default}select{flex:1;min-width:140px;max-width:100%}
.mode{display:flex;align-items:center;gap:6px;white-space:nowrap}.mode input{width:20px;height:20px}
.reader-main{max-width:760px;margin:auto;padding:20px 16px 64px}.chapter{scroll-margin-top:180px}.chapter [id]{scroll-margin-top:180px}
.chapter+.chapter{margin-top:64px;border-top:3px solid var(--line);padding-top:32px}
.chapter[hidden]{display:none}.source-links,.reader-hint{font:14px/1.6 system-ui;color:var(--mut)}
.edition-note{font:14px/1.5 system-ui;background:var(--key);border-left:4px solid var(--keyb);padding:8px 12px;border-radius:4px}
.reader-bottom{display:flex;justify-content:space-between;gap:12px;margin-top:24px}
.skip{position:absolute;left:-9999px}.skip:focus{left:12px;top:12px;z-index:30;background:var(--card);padding:12px}
:focus-visible{outline:3px solid var(--acc);outline-offset:3px}
@media(max-width:560px){.reader-controls select{order:-1;flex-basis:100%;width:100%}.reader-controls{gap:8px}.mode{margin-left:auto}.reader-title{width:100%}.reader-main{padding-top:12px}}
@media print{.reader-bar,.reader-bottom,.source-links,.reader-hint{display:none}.chapter[hidden]{display:block}.chapter{break-before:page}}
</style></head><body>
<a class="skip" href="#reading">Skip to reading</a>
<header class="reader-bar"><div class="reader-inner"><a class="reader-title" href="index.html">PhaseKeep · Library reader</a><a href="library/index.html">Edition 03 (frozen)</a><a href="library-edition-04/index.html">Edition 04 (draft)</a><a href="development/index.html">Research site</a>
<nav class="reader-controls" aria-label="Chapter navigation"><button id="prev" type="button">Previous</button><label class="skip" for="chapters">Choose chapter</label><select id="chapters">''' + ''.join(options) + '''</select><button id="next" type="button">Next</button><label class="mode"><input type="checkbox" id="continuous"> Continuous</label></nav>
<span id="position" aria-live="polite"></span></div></header>
<main id="reading" class="reader-main" tabindex="-1"><p class="reader-hint">Edition 03 Revision H is frozen; Edition 04 is a working draft and a dated research snapshot. New to PhaseKeep? Read <a href="#phasekeep-from-the-beginning">PhaseKeep from the beginning</a>, the whole story on one page. Choose a chapter or turn on Continuous to read and search everything (Ctrl/Cmd+F). Save this HTML file to read offline. Original Markdown and HTML links are available in every chapter. The previous frozen-only reader is kept as <a href="reader-rev-h.html">reader-rev-h.html</a>.</p>
<noscript><p>JavaScript is off: the full book is shown below. Use your browser's Find feature to locate a chapter.</p></noscript>
''' + '\n'.join(sections) + '''
<nav class="reader-bottom" aria-label="Bottom chapter navigation"><button id="prev-bottom" type="button">Previous chapter</button><button id="next-bottom" type="button">Next chapter</button></nav>
</main><script>
'use strict';
const chapters = [...document.querySelectorAll('.chapter')];
const select = document.querySelector('#chapters');
const continuous = document.querySelector('#continuous');
let current = 0;
function render(scroll = false) {
  chapters.forEach((chapter, i) => { chapter.hidden = !continuous.checked && i !== current; });
  select.value = chapters[current].id;
  for (const id of ['prev','prev-bottom']) document.getElementById(id).disabled = current === 0;
  for (const id of ['next','next-bottom']) document.getElementById(id).disabled = current === chapters.length - 1;
  document.querySelector('#position').textContent = `${current + 1} of ${chapters.length} · ${chapters[current].dataset.title}`;
  document.title = `${chapters[current].dataset.title} · PhaseKeep reader`;
  if (scroll) chapters[current].scrollIntoView({block:'start'});
}
function navigate(index) {
  current = Math.max(0, Math.min(chapters.length - 1, index));
  history.pushState(null, '', '#' + chapters[current].id);
  render(true);
}
function fromHash() {
  let target; try { target = document.getElementById(decodeURIComponent(location.hash.slice(1))); } catch { target = null; }
  const chapter = target?.closest('.chapter');
  if (chapter) current = chapters.indexOf(chapter);
  render();
  if (target && chapter) requestAnimationFrame(() => target.scrollIntoView({block:'start'}));
}
select.addEventListener('change', () => navigate(chapters.findIndex(c => c.id === select.value)));
for (const id of ['prev','prev-bottom']) document.getElementById(id).addEventListener('click', () => navigate(current - 1));
for (const id of ['next','next-bottom']) document.getElementById(id).addEventListener('click', () => navigate(current + 1));
continuous.checked = new URLSearchParams(location.search).get('view') === 'all';
continuous.addEventListener('change', () => {
  const url = new URL(location.href);
  if (continuous.checked) url.searchParams.set('view','all'); else url.searchParams.delete('view');
  history.replaceState(null,'',url); render(true);
});
window.addEventListener('hashchange', fromHash);
window.addEventListener('popstate', () => { continuous.checked = new URLSearchParams(location.search).get('view') === 'all'; fromHash(); });
fromHash();
</script></body></html>
'''
(ROOT / 'reader.html').write_text(page, encoding='utf-8', newline='\n')
print(f'Built reader.html from {number} chapters in {len(groups)} groups (frozen chapters unchanged).')
