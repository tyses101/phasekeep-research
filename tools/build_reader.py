"""Build the offline reader from frozen HTML; never rewrite library sources."""
from pathlib import Path
import html
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / 'library'
index = (LIB / 'index.html').read_text(encoding='utf-8')
chapters = re.findall(r'<a class="card" href="([^"]+)">.*?<b>(.*?)</b>', index)
slugs = {name: Path(name).stem for name, _ in chapters}
sections = []
options = []
for number, (name, title) in enumerate(chapters):
    slug = slugs[name]
    text = (LIB / name).read_text(encoding='utf-8')
    body = re.search(r'<main[^>]*>(.*?)</main>', text, re.S).group(1)
    body = re.sub(r'<div class="nav">.*?</div>', '', body, flags=re.S)
    # Namespace all IDs, including inline SVG references, across the combined book.
    body = re.sub(r'\bid="([^"]+)"', lambda m: f'id="{slug}--{m[1]}"', body)
    body = re.sub(r'url\(#([^)]+)\)', lambda m: f'url(#{slug}--{m[1]})', body)
    def link(match):
        target = html.unescape(match[1]); parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc:
            return match[0]
        if not parsed.path and parsed.fragment:
            return f'href="#{slug}--{html.escape(parsed.fragment, quote=True)}"'
        if parsed.path in slugs:
            anchor = slugs[parsed.path] + ('--' + parsed.fragment if parsed.fragment else '')
            return f'href="#{html.escape(anchor, quote=True)}"'
        return f'href="library/{html.escape(target, quote=True)}"'
    body = re.sub(r'href="([^"]+)"', link, body)
    sources = f'<p class="source-links"><a href="library/{name}">Original HTML</a> · <a href="https://github.com/tyses101/phasekeep-research/blob/main/library/markdown/{slug}.md">Markdown on GitHub</a></p>'
    sections.append(f'<section class="chapter" id="{slug}" data-title="{html.escape(html.unescape(title), quote=True)}">{sources}{body}</section>')
    options.append(f'<option value="{slug}">{number + 1}. {title}</option>')
style = re.search(r'<style>(.*?)</style>', index, re.S).group(1)
page = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>PhaseKeep · Library reader</title><meta name="description" content="Read the complete PhaseKeep Revision H library with chapter navigation or continuous scrolling. Works offline.">
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
.reader-bottom{display:flex;justify-content:space-between;gap:12px;margin-top:24px}
.skip{position:absolute;left:-9999px}.skip:focus{left:12px;top:12px;z-index:30;background:var(--card);padding:12px}
:focus-visible{outline:3px solid var(--acc);outline-offset:3px}
@media(max-width:560px){.reader-controls select{order:-1;flex-basis:100%;width:100%}.reader-controls{gap:8px}.mode{margin-left:auto}.reader-title{width:100%}.reader-main{padding-top:12px}}
@media print{.reader-bar,.reader-bottom,.source-links,.reader-hint{display:none}.chapter[hidden]{display:block}.chapter{break-before:page}}
</style></head><body>
<a class="skip" href="#reading">Skip to reading</a>
<header class="reader-bar"><div class="reader-inner"><a class="reader-title" href="index.html">PhaseKeep · Library reader</a><a href="library/index.html">Original library</a><a href="https://github.com/tyses101/phasekeep-research/blob/main/docs/research-development.md">Development draft</a>
<nav class="reader-controls" aria-label="Chapter navigation"><button id="prev" type="button">Previous</button><label class="skip" for="chapters">Choose chapter</label><select id="chapters">''' + ''.join(options) + '''</select><button id="next" type="button">Next</button><label class="mode"><input type="checkbox" id="continuous"> Continuous</label></nav>
<span id="position" aria-live="polite"></span></div></header>
<main id="reading" class="reader-main" tabindex="-1"><p class="reader-hint">Frozen Revision H · Choose a chapter or turn on Continuous to read and search the whole book (Ctrl/Cmd+F). Save this HTML file to read offline. Original Markdown and HTML links are available in every chapter.</p>
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
print(f'Built reader.html from {len(chapters)} unchanged chapters.')
