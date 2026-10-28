"""Building blocks for puzzle cards. An event's content.py imports these to draw each picture.

Every helper returns an HTML string; the app shrinks the finished card to fit, so sizes are relative.
CSS classes available inside a card (defined in app.py): .w .t3 .emo .row .col .lrow .cap .split/.half .blank .mk
.bubble .gv .orb .strike .ie
"""
from common import img, inline  # noqa: F401  (re-exported for content files)


def E(code, size, style=""):
    """A 3D emoji picture. code = Fluent Emoji file name, e.g. "1f41d" (bee) or "2601-fe0f" (cloud)."""
    return (f'<img class="emo" src="assets/{code}.webp" '
            f'style="width:{size}px;height:{size}px;{style}">')


def W(text, size=120, font="p", color="#111", style=""):
    """A word. font "p" = Poppins Black, "a" = Anton (tall condensed)."""
    fam = "'Anton'" if font == "a" else "'Poppins'"
    weight = 400 if font == "a" else 900
    return (f'<div class="w" style="font-family:{fam};font-weight:{weight};'
            f'font-size:{size}px;color:{color};{style}">{text}</div>')


def shadow3d(depth, n=11):
    layers = [f"{i}px {i}px 0 {depth}" for i in range(1, n + 1)]
    layers.append("16px 22px 22px rgba(0,0,0,.28)")
    return ", ".join(layers)


def T3(text, size, face, depth, style=""):
    """Chunky 3D letters or numbers, e.g. T3("V", 320, "#FF8F1F", "#A85400")."""
    return (f'<div class="t3" style="font-size:{size}px;color:{face};'
            f'text-shadow:{shadow3d(depth)};{style}">{text}</div>')


def row(*items, gap=40, style=""):
    return f'<div class="row" style="gap:{gap}px;{style}">' + "".join(items) + "</div>"


def col(*items, gap=0, style=""):
    return f'<div class="col" style="gap:{gap}px;{style}">' + "".join(items) + "</div>"


def letters(rows, size=94, cell=114):
    """A grid of letters, e.g. an alphabet with some letters missing."""
    out = []
    for r in rows:
        cells = "".join(f'<span style="width:{cell}px">{ch}</span>' for ch in r.split())
        out.append(f'<div class="lrow" style="font-size:{size}px">{cells}</div>')
    return col(*out, gap=6)


def caption(text, style=""):
    """A small red instruction under the picture, e.g. "SAY IT FAST!"."""
    return f'<div class="cap" style="{style}">{text}</div>'
