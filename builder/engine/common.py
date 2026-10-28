"""Shared pieces: vendor paths, fonts, emoji helpers and festive decorations."""
import re
from pathlib import Path

BUILDER = Path(__file__).resolve().parent.parent
VENDOR = BUILDER / "vendor"
ASSET_SRC = VENDOR / "lobehub-fluent-emoji-3d-1.1.0/package/assets"   # Fluent Emoji 3D, file name = code point(s)
TTS = VENDOR / "tts"

FONT_FILES = {
    "poppins-latin-600-normal.woff2": "fontsource-poppins-5.3.0",
    "poppins-latin-700-normal.woff2": "fontsource-poppins-5.3.0",
    "poppins-latin-800-normal.woff2": "fontsource-poppins-5.3.0",
    "poppins-latin-900-normal.woff2": "fontsource-poppins-5.3.0",
    "anton-latin-400-normal.woff2": "fontsource-anton-5.3.0",
    "luckiest-guy-latin-400-normal.woff2": "fontsource-luckiest-guy-5.3.0",
    "baloo-2-devanagari-800-normal.woff2": "fontsource-baloo-2-5.3.0",
    "baloo-2-latin-800-normal.woff2": "fontsource-baloo-2-5.3.0",
}

FONT_CSS = """
@font-face{font-family:'Poppins';font-weight:600;src:url(fonts/poppins-latin-600-normal.woff2) format('woff2')}
@font-face{font-family:'Poppins';font-weight:700;src:url(fonts/poppins-latin-700-normal.woff2) format('woff2')}
@font-face{font-family:'Poppins';font-weight:800;src:url(fonts/poppins-latin-800-normal.woff2) format('woff2')}
@font-face{font-family:'Poppins';font-weight:900;src:url(fonts/poppins-latin-900-normal.woff2) format('woff2')}
@font-face{font-family:'Anton';font-weight:400;src:url(fonts/anton-latin-400-normal.woff2) format('woff2')}
@font-face{font-family:'Luckiest Guy';font-weight:400;src:url(fonts/luckiest-guy-latin-400-normal.woff2) format('woff2')}
@font-face{font-family:'Baloo 2';font-weight:800;src:url(fonts/baloo-2-devanagari-800-normal.woff2) format('woff2');
  unicode-range:U+0900-097F,U+1CD0-1CF9,U+200C-200D,U+20A8,U+20B9,U+20F0,U+25CC,U+A830-A839,U+A8E0-A8FF}
@font-face{font-family:'Baloo 2';font-weight:800;src:url(fonts/baloo-2-latin-800-normal.woff2) format('woff2');
  unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
"""

INLINE_EMOJI = re.compile(r":([0-9a-f]{4,5}(?:-[0-9a-f]{2,5})*):")


def inline(text):
    """Turn :1f64f: style codes in explanation text into small inline emoji images."""
    return INLINE_EMOJI.sub(lambda m: f'<img class="ie" src="assets/{m.group(1)}.webp">', text)


def img(code, size, style=""):
    return f'<img src="assets/{code}.webp" style="width:{size}px;height:{size}px;{style}">'


def mandala():
    cx = cy = 750
    parts = []
    rings = [(150, 12, 46, 96), (240, 16, 56, 120), (345, 24, 62, 136),
             (460, 30, 70, 150), (585, 36, 76, 160), (705, 48, 56, 110)]
    for r, n, w, h in rings:
        for k in range(n):
            a = 360 * k / n
            parts.append(f'<ellipse cx="{cx}" cy="{cy - r}" rx="{w / 2:.1f}" ry="{h / 2:.1f}" '
                         f'transform="rotate({a:.2f} {cx} {cy})"/>')
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r + h / 2 + 10:.1f}"/>')
    return ('<svg class="mandala" viewBox="0 0 1500 1500"><g fill="none" stroke="#FFD27A" stroke-width="3">'
            + "".join(parts) + "</g></svg>")


def leaf(x, y, rot, h=70):
    w = h * 0.46
    return (f'<svg style="position:absolute;left:{x - w / 2:.0f}px;top:{y:.0f}px;transform:rotate({rot}deg);transform-origin:50% 0" '
            f'width="{w:.0f}" height="{h}" viewBox="0 0 34 74">'
            '<defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7CCB5B"/>'
            '<stop offset="1" stop-color="#2E7D32"/></linearGradient></defs>'
            '<path d="M17 0 C 34 18 32 52 17 74 C 2 52 0 18 17 0 Z" fill="url(#lg)"/>'
            '<path d="M17 5 L17 68" stroke="#1B5E20" stroke-width="2.2" opacity=".7"/></svg>')


def tips():
    items = [("1f4e2", "Say it"), ("1f522", "Count"), ("1f4cd", "Position"),
             ("1f9e9", "Missing"), ("1f524", "Translate")]
    chips = "".join(f'<div class="tip">{img(c, 40)}{t}</div>' for c, t in items)
    return f'<div class="tipsh">Try these tricks</div><div class="tips">{chips}</div>'


MANDALA = mandala()
