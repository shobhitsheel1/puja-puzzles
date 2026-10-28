"""Talking-face parts shared by every festival cartoon (deity or mascot).

A cartoon (an event's deity.py) is one SVG with viewBox "0 0 600 740" and these hooks, which app.py animates:
  <svg class="{cls}" ...>          cls is "bhag" for the pop-ups and the welcome card
    <defs> ... {mouth_defs()} </defs>
    <g class="halo">  ...</g>       optional: slow spin behind the figure
    <g class="float"> ...           required: the whole figure bobs; on a wrong answer it shakes its head
        <g class="eyes">...</g>     required: eye whites, pupils and lashes, scaled shut for a blink
        {mouths(cx, cy, ...)}       required: the 9 lip-sync mouth shapes; the app shows one at a time
        class="chakra" / "glow"     optional: something that spins / something that pulses
    </g>
  </svg>
All ids must start with "bg" (e.g. id="bgSkin", fill="url(#bgSkin)"); finish() renames them so that three copies
of the cartoon can live on one page.

Mouth shapes follow Rhubarb Lip Sync: X rest, A closed (m b p), B teeth together (most consonants, ee),
C open (e, a), D wide open (aa), E rounded (o, er), F puckered (oo, w), G teeth on lower lip (f, v), H tongue up (l).
They are drawn for a face whose mouth centre is at (300, 352) with a 224-unit-wide head; mouths() moves and scales
them onto any other face.
"""

FACE_INK = "#1B2340"
MOUTH_IN = "#7A1E3C"
TONGUE = "#F27D9B"
TEETH = "#FFFDF6"
SHAPES = "XABCDEFGH"


def _contour(y, hw, top, bot, cx=300):
    """Mouth outline: an upper lip curve and a lower lip curve meeting at the corners."""
    l, r = cx - hw, cx + hw
    return (f"M {l} {y} C {cx - hw * .5:.1f} {y + top} {cx + hw * .5:.1f} {y + top} {r} {y} "
            f"C {cx + hw * .6:.1f} {y + bot} {cx - hw * .6:.1f} {y + bot} {l} {y} Z")


def _teeth(y, hw, top, h, cx=300):
    """A band of upper teeth that follows the upper lip."""
    l, r = cx - hw, cx + hw
    a, b = f"{cx - hw * .5:.1f}", f"{cx + hw * .5:.1f}"
    return (f'<path d="M {l} {y - 3} C {a} {y + top - 3} {b} {y + top - 3} {r} {y - 3} L {r} {y + h} '
            f'C {b} {y + top + h} {a} {y + top + h} {l} {y + h} Z" fill="{TEETH}"/>')


OPEN = {  # key: (y, half width, upper lip, lower lip, teeth height, tongue (cx, cy, rx, ry) or None)
    "C": (352, 30, -6, 42, 9, (300, 387, 18, 10)),
    "D": (350, 32, -10, 62, 10, (300, 401, 22, 13)),
    "E": (354, 21, -10, 36, 7, (300, 384, 13, 8)),
    "H": (352, 29, -6, 38, 8, (300, 369, 14, 13)),
    "G": (356, 26, -4, 24, 12, None),
    "B": (355, 29, 2, 24, 0, None),
}


def mouth_defs():
    """Clip paths for the open mouths. Put inside the cartoon's <defs>."""
    return "".join(f'<clipPath id="bgM{k}"><path d="{_contour(*OPEN[k][:4])}"/></clipPath>' for k in OPEN)


def mouths(cx=300, cy=352, scale=1.0, skin="#4A80E6", lip="#2F62CC", rest="#C2416A"):
    """The 9 mouth shapes, placed with the mouth centre at (cx, cy).

    skin: the face colour just around the mouth (used for the lower lip in "f / v").
    lip: lip colour for the puckered "oo" shape. rest: fill of the resting smile.
    """
    out = []
    for k in SHAPES:
        hide = '' if k == "X" else ' display="none"'
        if k == "X":
            body = f'<path d="M 270 352 Q 300 388 330 352 Q 300 366 270 352 Z" fill="{rest}" stroke="{FACE_INK}" stroke-width="3" stroke-linejoin="round"/>'
        elif k == "A":
            body = (f'<path d="M 271 356 Q 300 373 329 356" stroke="{FACE_INK}" stroke-width="4.5" fill="none" stroke-linecap="round"/>'
                    f'<path d="M 291 371 Q 300 374 309 371" stroke="{lip}" stroke-width="3" fill="none" stroke-linecap="round"/>')
        elif k == "F":
            body = (f'<ellipse cx="300" cy="362" rx="14" ry="15" fill="{lip}" stroke="{FACE_INK}" stroke-width="3"/>'
                    f'<ellipse cx="300" cy="362" rx="6.5" ry="8" fill="{MOUTH_IN}" stroke="{FACE_INK}" stroke-width="1.5"/>'
                    '<path d="M 293 373 Q 300 376 307 373" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" opacity=".35"/>')
        else:
            y, hw, top, bot, th, tongue = OPEN[k]
            d = _contour(y, hw, top, bot)
            inner = []
            if k == "B":
                inner.append(f'<path d="{d}" fill="{TEETH}"/>')
                inner.append(f'<path d="M {300 - hw + 3} {y + 7} Q 300 {y + 13} {300 + hw - 3} {y + 7}" stroke="#C9BFB3" stroke-width="1.8" fill="none"/>')
            else:
                inner.append(f'<path d="{d}" fill="{MOUTH_IN}"/>')
                if tongue:
                    inner.append(f'<ellipse cx="{tongue[0]}" cy="{tongue[1]}" rx="{tongue[2]}" ry="{tongue[3]}" fill="{TONGUE}"/>')
                inner.append(_teeth(y, hw, top, th))
                if k == "G":  # lower lip tucked up under the top teeth
                    inner.append(f'<path d="M {300 - hw - 4} {y + 12} Q 300 {y + 4} {300 + hw + 4} {y + 12} L {300 + hw + 4} {y + 40} L {300 - hw - 4} {y + 40} Z" fill="{skin}"/>')
                    inner.append(f'<path d="M {300 - hw + 2} {y + 11} Q 300 {y + 5} {300 + hw - 2} {y + 11}" stroke="{FACE_INK}" stroke-width="2.5" fill="none"/>')
            body = (f'<g clip-path="url(#bgM{k})">{"".join(inner)}</g>'
                    f'<path d="{d}" fill="none" stroke="{FACE_INK}" stroke-width="3.5" stroke-linejoin="round"/>')
        out.append(f'<g class="m m{k}"{hide}>{body}</g>')
    move = "" if (cx, cy, scale) == (300, 352, 1.0) else \
        f' transform="translate({cx} {cy}) scale({scale}) translate(-300 -352)"'
    return f'<g class="mouth"{move}>' + "".join(out) + "</g>"


def finish(svg, idp):
    """Give this copy of the cartoon its own ids (bgX -> {idp}X)."""
    return svg.replace('id="bg', f'id="{idp}').replace('url(#bg', f'url(#{idp}')
