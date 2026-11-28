"""Build a lightweight searchable entry point without duplicating chapter bodies."""
from pathlib import Path
import re, html
root = Path(__file__).resolve().parents[1]
reader = (root / 'reader.html').read_text(encoding='utf-8')
chapters = re.findall(r'<section class="chapter" id="([^"]+)" data-title="([^"]+)"', reader)
cards = ''.join('<li><a href="reader.html#'+slug+'">'+title+'</a></li>' for slug,title in chapters)
page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Start Here · PhaseKeep Research</title>
<style>body{margin:0;background:#101722;color:#e8edf5;font:18px/1.65 system-ui}main{max-width:940px;margin:auto;padding:32px 20px}a{color:#8bd8ed}h1{font-size:clamp(2rem,6vw,3.5rem);line-height:1.1}nav{display:flex;flex-wrap:wrap;gap:18px}input{box-sizing:border-box;width:100%;padding:14px;font:inherit;border-radius:8px;border:1px solid #62748b;background:#182433;color:inherit}li{padding:10px;border-bottom:1px solid #304158}ul{padding-left:24px}.note{border-left:3px solid #8bd8ed;padding:12px 18px;background:#182433}:focus-visible{outline:3px solid #f4cc74;outline-offset:4px}</style>
<main><nav><a href="reader.html">Open reader</a><a href="development/index.html">Research development</a><a href="https://github.com/tyses101/phasekeep-research">Repository</a></nav>
<h1>Start with the physics.<br>Follow the research.</h1><p>An open learning library and research record, from photonic encoding and quantum relationships to atomic registers, control and assurance.</p>
<p class="note">Two pillars: <strong>Geometric Encoding Axies (GEA)</strong> and <strong>Integrated Quantum Assurance (IQA)</strong>. No demonstrated quantum computer or hardware advantage is claimed. Evidence labels, failed approaches and corrections remain part of the story.</p>
<h2>Choose your starting point</h2><ol><li><a href="reader.html#phasekeep-from-the-beginning">The whole journey in plain language</a></li><li><a href="reader.html">Learn from the beginning</a>: frozen Edition 03 Revision H, then Edition 04.</li><li><a href="reader.html#register-of-terms">Look up terminology</a>, then follow the linked mathematical and research sources.</li></ol>
<p><strong>Historical versus current:</strong> Edition 03 is frozen. Edition 04, Volumes 15–23 and Appendices 7–10, is a dated research snapshot as of 28 November 2026. Working research records retain their own verification limits.</p>
<p><a href="reader.html?view=all">Read continuously and search all text</a> · <a href="development/atomic-register/README.html">Atomic-register research chapters</a> · <a href="development/errata.html">Corrections</a></p>
<h2>Unified contents</h2><label for="search">Find a chapter or research index</label><input id="search" type="search" placeholder="Try glossary, workbook, timeline, sources"><ul id="contents">'''+cards+'''</ul><p id="count" role="status"></p>
<p>Use Previous/Next in the reader, or Continuous mode with your browser's Find command. The reader can be saved for offline reading. Sources, simulations and reproduction instructions remain linked rather than duplicated.</p>
<footer>Tyler O'Bryan · Text CC BY 4.0 · Code MIT · <a href="NOTICE.txt">Authorship and attribution</a></footer></main>
<script>const rows=[...document.querySelectorAll('#contents li')];document.querySelector('#search').addEventListener('input',e=>{const q=e.target.value.toLowerCase();rows.forEach(r=>r.hidden=!r.textContent.toLowerCase().includes(q));document.querySelector('#count').textContent=rows.filter(r=>!r.hidden).length+' entries';});</script></html>'''
(root/'research-index.html').write_text(page,encoding='utf-8',newline='\n')
print('Built research-index.html:',len(chapters),'entries')
