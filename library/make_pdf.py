#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tyler O'Bryan, where applicable
"""Builds PhaseKeep-Learning-Library-complete.pdf from the built HTML pages, with bookmarks.
Needs: Playwright (Chromium) and pypdf. Run after build.py."""
import io, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build

stems = ["index"] + [s for s, *_ in build.BOOKS if (build.SRC / f"{s}.md").exists()]
w = PdfWriter(); pos = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    for s in stems:
        pg.goto((HERE / f"{s}.html").as_uri())
        data = pg.pdf(format="A4", print_background=True, margin={"top": "16mm", "bottom": "16mm", "left": "14mm", "right": "14mm"})
        r = PdfReader(io.BytesIO(data)); pos.append((s, len(w.pages)))
        for pgx in r.pages: w.add_page(pgx)
    b.close()
for s, i in pos: w.add_outline_item(s, i)
w.add_metadata({"/Title": "PhaseKeep Learning Library, Edition 03 (complete)"})
with open(HERE / "PhaseKeep-Learning-Library-complete.pdf", "wb") as f: w.write(f)
print("pdf pages", len(w.pages))
