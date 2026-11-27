#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tyler O'Bryan, where applicable
"""Builds PhaseKeep-Learning-Library.epub from src/. Needs: pandoc and Playwright (for figure PNGs). Run after build.py.
Figures become PNG images with the written description as alt text."""
import re, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build, figures
from playwright.sync_api import sync_playwright

FIG = HERE / "epub_build" / "figs"; FIG.mkdir(parents=True, exist_ok=True)
names = sorted(figures.FIGS)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(device_scale_factor=2)
    for n in names:
        pg.set_content(f"<style>{build.CSS}</style><div style='width:660px;padding:8px;background:#fff'>{figures.get(n)}</div>")
        pg.locator("svg").screenshot(path=str(FIG / f"{n}.png"))
    b.close()

def fig_md(m):
    n = m.group(1)
    return f"![{figures.describe(n)}](figs/{n}.png)\n\n*Figure: {m.group(2)}*"

parts = []
for stem, label, title, sub in build.BOOKS:
    f = build.SRC / f"{stem}.md"
    if not f.exists():
        continue
    text = re.sub(r"^# .*\n", "", f.read_text(encoding="utf-8"), count=1)
    text = build.xlink(text, stem)
    text = re.sub(r"^\{\{fig:(\w+)\|(.*)\}\}\s*$", fig_md, text, flags=re.M)
    body = build.portable(text, links=False)
    body = re.sub(r"^### ", "#### ", re.sub(r"^## ", "### ", body, flags=re.M), flags=re.M)
    head = ("Volume " + label + ": " if label.isdigit() else "") + title
    parts.append(f"\n\n## {head}\n\n*{sub}*\n\n{body}")
intro = build.portable(re.sub(r"^# .*\n", "", (build.SRC / "index.md").read_text(encoding="utf-8"), count=1))
md = "---\ntitle: PhaseKeep Learning Library, Edition 03 (draft)\nlang: en\nauthor: PhaseKeep project (AI-assisted draft)\n---\n\n## About this library\n\n" + intro + "\n" + "".join(parts)
src = HERE / "epub_build" / "library.md"; src.write_text(md, encoding="utf-8")
out = HERE / "PhaseKeep-Learning-Library.epub"
subprocess.run(["pandoc", str(src), "-o", str(out), "--toc", "--toc-depth=2", "--split-level=2", "--resource-path", str(HERE / "epub_build")], check=True)
print("wrote", out.name, out.stat().st_size // 1024, "KB")
