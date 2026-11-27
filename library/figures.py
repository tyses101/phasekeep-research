# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tyler O'Bryan, where applicable
"""Inline SVG figures for the PhaseKeep Learning Library. Each figure has a text description so it is usable without
seeing the picture (screen readers, plain-text editions). get(name) -> svg string; describe(name) -> plain text."""
import html, math

DESC = {}


def _svg(name, w, h, body, title, desc):
    DESC[name] = desc
    return (f'<svg viewBox="0 0 {w} {h}" role="img" aria-labelledby="t-{name} d-{name}" xmlns="http://www.w3.org/2000/svg">'
            f'<title id="t-{name}">{html.escape(title)}</title><desc id="d-{name}">{html.escape(desc)}</desc>{body}</svg>')


def _box(x, y, w, h, text, cls="soft", sub=None):
    t = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" class="{cls}" stroke-width="1.5" fill-opacity=".18"/>'
    t += f'<text x="{x + w / 2}" y="{y + h / 2 + (-2 if sub else 5)}" text-anchor="middle" font-size="14" font-weight="700">{html.escape(text)}</text>'
    if sub:
        t += f'<text x="{x + w / 2}" y="{y + h / 2 + 16}" text-anchor="middle" font-size="11" class="m">{html.escape(sub)}</text>'
    return t


def fig_map():
    items = [("Source", "light, photons", "c"), ("Prepare", "make the state", "c"), ("Encode (EA)", "pick the carriers", "b"),
             ("Transform (CT)", "change the state", "b"), ("Buddy Check", "can we go on?", "d"), ("Continue", "or measure", "soft")]
    body = ""
    for i, (a, b, c) in enumerate(items):
        x = 12 + i * 104
        body += _box(x, 40, 92, 62, a, c, b)
        if i < len(items) - 1:
            body += f'<path d="M{x + 92} 71 h12" class="line" stroke-width="2"/><path d="M{x + 99} 66 l6 5 l-6 5" class="line" stroke-width="2"/>'
    body += '<text x="12" y="24" font-size="12" class="m">Green: familiar lab technology · Amber: proposed, parts exist · Red: unresolved</text>'
    body += '<text x="12" y="132" font-size="12" class="m">Time is a clock that runs the whole machine. It is not one of the carriers.</text>'
    body += '<path d="M12 140 H628" class="line" stroke-width="1" stroke-dasharray="4 4"/>'
    return _svg("map", 640, 152, body, "The PhaseKeep pipeline",
                "Six boxes in a row joined by arrows: Source, Prepare, Encode (EA), Transform (CT), Buddy Check, Continue or measure. "
                "Source and Prepare are familiar laboratory technology, Encode and Transform are proposed but built from existing parts, and Buddy Check is unresolved. "
                "A dashed line beneath says time is a clock for the whole machine, not one of the carriers.")


def fig_polarization():
    body = '<text x="320" y="22" text-anchor="middle" font-size="13" class="m">Looking along the beam. The arrow shows which way the electric field swings.</text>'
    for cx, label, ang, cls in ((110, "H (horizontal)", 0, "a"), (320, "V (vertical)", 90, "b"), (530, "Diagonal = H and V together", 45, "e")):
        body += f'<circle cx="{cx}" cy="110" r="62" class="soft" fill-opacity=".25" stroke-width="1"/>'
        dx, dy = 52 * math.cos(math.radians(ang)), -52 * math.sin(math.radians(ang))
        body += f'<line x1="{cx - dx}" y1="{110 - dy}" x2="{cx + dx}" y2="{110 + dy}" class="{cls}" stroke-width="4"/>'
        body += f'<circle cx="{cx + dx}" cy="{110 + dy}" r="5" class="{cls}"/><circle cx="{cx - dx}" cy="{110 - dy}" r="5" class="{cls}"/>'
        body += f'<text x="{cx}" y="198" text-anchor="middle" font-size="13" font-weight="700">{label}</text>'
    return _svg("polarization", 640, 212, body, "Three polarization directions",
                "Three circles seen head-on. The first has a horizontal line, labelled H. The second has a vertical line, labelled V. "
                "The third has a slanted line, labelled diagonal, which is a combination of H and V together.")


def fig_oam():
    body = '<text x="320" y="20" text-anchor="middle" font-size="13" class="m">Colour shows the phase of the wave at each angle around the beam.</text>'
    for k, (cx, l) in enumerate(((110, -1), (320, 0), (530, 1))):
        n = 36
        for s in range(n):
            a0, a1 = 2 * math.pi * s / n, 2 * math.pi * (s + 1) / n
            hue = (360 * (l * (s + .5) / n)) % 360
            r0, r1 = 34, 62
            p = (f"M{cx + r1 * math.cos(a0):.1f} {105 - r1 * math.sin(a0):.1f} A{r1} {r1} 0 0 0 {cx + r1 * math.cos(a1):.1f} {105 - r1 * math.sin(a1):.1f} "
                 f"L{cx + r0 * math.cos(a1):.1f} {105 - r0 * math.sin(a1):.1f} A{r0} {r0} 0 0 1 {cx + r0 * math.cos(a0):.1f} {105 - r0 * math.sin(a0):.1f}Z")
            body += f'<path d="{p}" fill="hsl({hue:.0f},65%,55%)"/>'
        arrow = {-1: "turns clockwise", 0: "no twist", 1: "turns counter-clockwise"}[l]
        body += f'<text x="{cx}" y="188" text-anchor="middle" font-size="15" font-weight="700">ℓ = {"+" if l > 0 else ("−" if l < 0 else "")}{abs(l)}</text>'
        body += f'<text x="{cx}" y="206" text-anchor="middle" font-size="12" class="m">{arrow} once per lap</text>'
    return _svg("oam", 640, 218, body, "Three twisting beams",
                "Three rings coloured by phase. For ell equal to minus one the colours cycle once around the ring one way. For ell equal to zero the whole ring is one colour, "
                "so there is no twist. For ell equal to plus one the colours cycle once around the ring the other way.")


def fig_tetragon():
    pts = {"00": (170, 50), "01": (470, 50), "10": (170, 190), "11": (470, 190)}
    lab = {"00": "H, ℓ = −1", "01": "H, ℓ = +1", "10": "V, ℓ = −1", "11": "V, ℓ = +1"}
    body = ('<line x1="170" y1="50" x2="470" y2="50" class="a" stroke-width="3"/><line x1="170" y1="190" x2="470" y2="190" class="a" stroke-width="3"/>'
            '<line x1="170" y1="50" x2="170" y2="190" class="b" stroke-width="3"/><line x1="470" y1="50" x2="470" y2="190" class="b" stroke-width="3"/>')
    for k, (x, y) in pts.items():
        body += f'<circle cx="{x}" cy="{y}" r="22" class="soft" stroke-width="2" fill-opacity=".6"/><text x="{x}" y="{y + 5}" text-anchor="middle" font-size="15" font-weight="700">{k}</text>'
        body += f'<text x="{x + (-34 if x < 300 else 34)}" y="{y + (-30 if y < 100 else 44)}" text-anchor="{"end" if x < 300 else "start"}" font-size="12" class="m">{lab[k]}</text>'
    body += '<text x="320" y="38" text-anchor="middle" font-size="13" class="a" font-weight="700" stroke="none">flip the twist (OAM exchange)</text>'
    body += '<text x="320" y="214" text-anchor="middle" font-size="13" class="a" font-weight="700" stroke="none">flip the twist (OAM exchange)</text>'
    body += '<text x="150" y="124" text-anchor="end" font-size="13" class="b" font-weight="700" stroke="none">flip polarization</text><text x="490" y="124" font-size="13" class="b" font-weight="700" stroke="none">flip polarization</text>'
    return _svg("tetragon", 640, 232, body, "The Tetragon: four addresses on a square",
                "A square with four corners. Top left 00 is horizontal polarization with twist minus one. Top right 01 is horizontal with twist plus one. "
                "Bottom left 10 is vertical with twist minus one. Bottom right 11 is vertical with twist plus one. The horizontal edges flip the twist, the vertical edges flip polarization. "
                "Corners 00 and 11 differ in both properties, as do 01 and 10.")


def fig_cube():
    ox, oy, s, dx, dy = 200, 200, 170, 90, -70
    def P(b):
        x, y, z = (int(c) for c in b)
        return ox + s * x + dx * z, oy - s * y * 0 + dy * z - 0 + (0 if y == 0 else -s)
    # vertices: bits (x,y,z); y goes up
    def pt(b):
        x, y, z = (int(c) for c in b)
        return ox + s * x + dx * z, oy - 120 * y + dy * z
    v = [f"{x}{y}{z}" for x in (0, 1) for y in (0, 1) for z in (0, 1)]
    body = ""
    for a in v:
        for b in v:
            if a < b and sum(c1 != c2 for c1, c2 in zip(a, b)) == 1:
                k = [i for i in range(3) if a[i] != b[i]][0]
                cls = ("a", "b", "c")[k]
                (x1, y1), (x2, y2) = pt(a), pt(b)
                body += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{cls}" stroke-width="2.5"/>'
    for a in v:
        x, y = pt(a)
        body += f'<circle cx="{x}" cy="{y}" r="17" class="soft" stroke-width="1.5" fill-opacity=".8"/><text x="{x}" y="{y + 4}" text-anchor="middle" font-size="11" font-weight="700">{a}</text>'
    body += '<text x="470" y="60" font-size="13" class="a" font-weight="700" stroke="none">blue edges: flip bit 1</text><text x="470" y="82" font-size="13" class="b" font-weight="700" stroke="none">amber edges: flip bit 2</text><text x="470" y="104" font-size="13" class="c" font-weight="700" stroke="none">green edges: flip bit 3</text>'
    body += '<text x="470" y="140" font-size="12" class="m">8 corners = 8 states</text><text x="470" y="158" font-size="12" class="m">12 edges, 6 square faces</text>'
    return _svg("cube", 640, 240, body, "A three-bit cube",
                "A cube drawn in perspective. Its eight corners are labelled with three-bit addresses from 000 to 111. Each edge connects two addresses that differ in exactly one bit, "
                "and edges are coloured by which bit they flip. The cube has 8 corners, 12 edges and 6 square faces.")


def fig_herald():
    body = '<text x="20" y="26" font-size="13" class="m">One specific input, 100 attempts of the modeled analyzer (the numbers are fractions of all attempts)</text>'
    body += '<rect x="20" y="44" width="150" height="46" class="c" fill-opacity=".55" stroke-width="1.5"/><rect x="170" y="44" width="300" height="46" class="d" fill-opacity=".55" stroke-width="1.5"/>'
    body += '<text x="95" y="73" text-anchor="middle" font-size="15" font-weight="700">12.5 correct</text><text x="320" y="73" text-anchor="middle" font-size="15" font-weight="700">25 false alarms</text>'
    body += '<path d="M20 100 H470" class="line" stroke-width="1.5"/><text x="245" y="120" text-anchor="middle" font-size="14" font-weight="700">37.5 detector clicks say “success”</text>'
    body += '<text x="20" y="160" font-size="14">Of the 37.5 “successes”, 12.5 are real: reliability = 12.5 / 37.5 = 1/3.</text>'
    body += '<text x="20" y="184" font-size="13" class="m">Keeping only some of the four detector patterns lowers the rate but leaves the ratio at 1/3.</text>'
    return _svg("herald", 640, 200, body, "A herald that is wrong two times in three",
                "A bar split into two parts. The left part, 12.5 out of 100 attempts, is correct outputs. The right part, 25 out of 100, is false alarms. "
                "Together they make 37.5 detector clicks that announce success. Only one third of those announcements are real, and keeping a subset of the detector patterns does not change that ratio.")


def fig_shared():
    body = '<text x="160" y="22" text-anchor="middle" font-size="14" font-weight="700">Shared: 1 plate</text><text x="480" y="22" text-anchor="middle" font-size="14" font-weight="700">Individual: sort, many plates, unsort</text>'
    for i in range(6):
        y = 44 + i * 22
        body += f'<line x1="20" y1="{y}" x2="300" y2="{y}" class="a" stroke-width="2"/>'
    body += '<rect x="140" y="36" width="22" height="140" rx="4" class="b" fill-opacity=".5" stroke-width="2"/><text x="151" y="196" text-anchor="middle" font-size="12" class="m">one waveplate</text>'
    body += _box(330, 40, 60, 130, "Sorter", "d", "N−1 stages") + _box(560, 40, 60, 130, "Unsorter", "d", "N−1 stages")
    for i in range(6):
        y = 52 + i * 20
        body += f'<line x1="390" y1="{y}" x2="560" y2="{y}" class="a" stroke-width="2"/><rect x="465" y="{y - 7}" width="12" height="14" class="b" fill-opacity=".6"/>'
    body += '<text x="475" y="196" text-anchor="middle" font-size="12" class="m">one waveplate per mode</text>'
    body += '<text x="320" y="224" text-anchor="middle" font-size="13">At 8 modes the model counts 1 element versus 50 for the in-place job (counting rule in Volume 5).</text>'
    return _svg("shared", 640, 238, body, "One shared waveplate versus sorting",
                "Left: a bundle of parallel beams passes through a single waveplate. Right: the same bundle must first go through a sorter that separates the modes, "
                "then a separate waveplate on each beam, then an unsorter to recombine them. With eight modes the illustrative model counts 1 optical element on the left and 50 on the right.")


def fig_chain():
    ideal, drift = [80.0, 67.0, 48.0, 24.3], [78.7, 62.8, 37.2, 9.1]
    xs = ["2", "4", "8", "16"]
    body = '<text x="320" y="20" text-anchor="middle" font-size="13" class="m">Fidelity given that every herald fired (percent), modeled, not measured</text>'
    body += '<line x1="60" y1="190" x2="620" y2="190" class="line" stroke-width="1.5"/><line x1="60" y1="36" x2="60" y2="190" class="line" stroke-width="1.5"/>'
    for g, x in enumerate(xs):
        bx = 90 + g * 135
        for j, (v, cls) in enumerate(((ideal[g], "a"), (drift[g], "b"))):
            h = v * 1.45
            body += f'<rect x="{bx + j * 48}" y="{190 - h:.1f}" width="42" height="{h:.1f}" class="{cls}" fill-opacity=".6" stroke-width="1.5"/><text x="{bx + j * 48 + 21}" y="{190 - h - 5:.1f}" text-anchor="middle" font-size="12" font-weight="700">{v}</text>'
        body += f'<text x="{bx + 45}" y="210" text-anchor="middle" font-size="13">{x} reactions</text>'
    body += '<rect x="400" y="40" width="12" height="12" class="a" fill-opacity=".6"/><text x="418" y="51" font-size="12">ideal parts</text><rect x="400" y="58" width="12" height="12" class="b" fill-opacity=".6"/><text x="418" y="69" font-size="12">with assumed phase drift</text>'
    return _svg("chain", 640, 224, body, "Fidelity falls as reactions are chained",
                "A grouped bar chart. For 2, 4, 8 and 16 chained reactions, fidelity given that every herald fired is 80.0, 67.0, 48.0 and 24.3 percent with ideal parts, "
                "and 78.7, 62.8, 37.2 and 9.1 percent with an assumed phase drift. These are modeled values, not measurements.")


def _glyph(cx, cy, kind):
    if kind == "H":
        return f'<line x1="{cx-11}" y1="{cy}" x2="{cx+11}" y2="{cy}" class="a" stroke-width="3.5"/>'
    if kind == "D+":
        return f'<line x1="{cx-8}" y1="{cy+8}" x2="{cx+8}" y2="{cy-8}" class="e" stroke-width="3.5"/>'
    if kind == "D-":
        return f'<line x1="{cx-8}" y1="{cy-8}" x2="{cx+8}" y2="{cy+8}" class="e" stroke-width="3.5"/>'
    return f'<circle cx="{cx}" cy="{cy}" r="10" class="b" stroke-width="2" fill="none"/><text x="{cx}" y="{cy+4}" text-anchor="middle" font-size="11" font-weight="700">{kind}</text>'


def fig_vortex():
    body = ""
    panels = ((160, "Edge blend (00 + 01)/\u221a2", "H polarization everywhere", ["H"] * 8),
              (480, "Diagonal blend (00 + 11)/\u221a2", "polarization changes around the beam", ["D+", "R", "D-", "L"] * 2))
    for cx, title, sub, kinds in panels:
        body += f'<circle cx="{cx}" cy="116" r="66" class="soft" fill-opacity=".18" stroke-width="1"/>'
        body += f'<text x="{cx}" y="120" text-anchor="middle" font-size="10" class="m">beam axis</text>'
        for k, kind in enumerate(kinds):
            a = math.radians(45 * k)
            body += _glyph(round(cx + 66 * math.cos(a), 1), round(116 - 66 * math.sin(a), 1), kind)
        body += f'<text x="{cx}" y="22" text-anchor="middle" font-size="14" font-weight="700">{title}</text>'
        body += f'<text x="{cx}" y="206" text-anchor="middle" font-size="12" class="m">{sub}</text>'
    body += '<text x="320" y="228" text-anchor="middle" font-size="11" class="m">Marks sit at eight angles around the beam. Line = linear polarization, circle marked R or L = circular polarization of one handedness or the other.</text>'
    return _svg("vortex", 640, 240, body, "Polarization around the beam for an edge blend and a diagonal blend",
                "Two rings seen head-on, each with eight marks placed at equal angles around the beam axis. In the left ring, the edge blend, every mark is the same horizontal line, "
                "so the polarization is uniform. In the right ring, the diagonal blend, the marks cycle through a diagonal line, a circle marked R, the opposite diagonal line, "
                "and a circle marked L, and this cycle repeats twice around the ring.")


def fig_journey():
    items = [("Prepare", "a known recipe", "b"), ("Transform", "waveplate, mirror", "b"), ("Interact", "heralded gate", "d"),
             ("Check", "UNKNOWN", "d"), ("Store", "memory chain", "d")]
    subs = ["PROPOSED", "closure checked", "valid 0.125 in model", "no safe test yet", "0.451 % < 1.1146 %"]
    body = ""
    for i, ((a, b, c), sub) in enumerate(zip(items, subs)):
        x = 10 + i * 124
        body += _box(x, 34, 108, 66, a, c, b)
        body += f'<text x="{x+54}" y="118" text-anchor="middle" font-size="11" class="m">{sub}</text>'
        if i < len(items) - 1:
            body += f'<path d="M{x+108} 67 h16" class="line" stroke-width="2"/><path d="M{x+118} 62 l6 5 l-6 5" class="line" stroke-width="2"/>'
    body += '<text x="10" y="20" font-size="12" class="m">Amber: proposed, parts exist · Red: low yield or unresolved</text>'
    body += '<text x="320" y="156" text-anchor="middle" font-size="13" font-weight="700">Illustrative joint yield: 0.125 \u00d7 0.00451 = 0.056 % (about 1 run in 1,800)</text>'
    body += '<text x="320" y="176" text-anchor="middle" font-size="11" class="m">Simple product of two modelled numbers, assuming independence. An illustration, not a result.</text>'
    return _svg("journey", 640, 190, body, "One photon's journey, with the numbers",
                "Five boxes in a row joined by arrows: Prepare, Transform, Interact, Check, Store. Under them: Prepare is proposed, Transform has had its closure checked, "
                "Interact has a modelled valid probability of 0.125, Check has no safe test yet and is marked unknown, and Store has a chain efficiency of 0.451 percent, below the 1.1146 percent threshold. "
                "A line underneath multiplies 0.125 by 0.00451 to give an illustrative joint yield of 0.056 percent, about one run in 1,800, with a note that this is an illustration and not a result.")


FIGS = {"map": fig_map, "polarization": fig_polarization, "oam": fig_oam, "tetragon": fig_tetragon, "cube": fig_cube,
        "herald": fig_herald, "vortex": fig_vortex, "journey": fig_journey, "shared": fig_shared, "chain": fig_chain}


def get(name):
    return FIGS[name]()


def describe(name):
    FIGS[name]()
    return DESC[name]
