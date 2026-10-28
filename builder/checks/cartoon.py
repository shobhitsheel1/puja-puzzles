#!/usr/bin/env python3
"""Draw an event's cartoon large, with all 9 lip-sync mouths, a blink and the full figure, to check the artwork.

  python checks/cartoon.py events/<slug>      -> build/<slug>/review/cartoon.png

Check: the face reads as the right deity or mascot for the festival, every mouth sits on the face (not on the chin
or nose), open mouths look natural, the eyes close fully in the blink, nothing is cut off at the edges.
"""
import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "engine"))
from event import Event  # noqa: E402
from face import SHAPES  # noqa: E402

NAMES = dict(X="rest", A="m b p", B="consonants", C="e / a", D="aa", E="o", F="oo / w", G="f / v", H="l")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("event")
    ap.add_argument("--face", default="", help='viewBox for the close-ups, e.g. "200 250 200 175"; default: around the mouth')
    a = ap.parse_args()
    ev = Event(a.event)
    out = HERE.parent / "build" / ev.slug / "review"
    out.mkdir(parents=True, exist_ok=True)
    css = ("".join(f'.bhag[data-m="{k}"] .m{k}{{display:inline}}' for k in SHAPES)
           + '.bhag[data-m]:not([data-m="X"]) .mX{display:none} .blink .eyes{transform-box:fill-box;transform-origin:center;transform:scaleY(.1)}')
    face = a.face or "180 180 240 240"
    cells = []
    for i, k in enumerate(SHAPES):
        s = ev.svg(idp=f"c{i}").replace('viewBox="0 0 600 740"', f'viewBox="{face}"', 1)
        s = s.replace('<svg class="bhag"', f'<svg class="bhag" data-m="{k}"', 1)
        cells.append(f'<div class="c"><div class="f">{s}</div><b>{k}</b> {NAMES[k]}</div>')
    blink = ev.svg(idp="bl").replace('viewBox="0 0 600 740"', f'viewBox="{face}"', 1).replace('<svg class="bhag"', '<svg class="bhag blink"', 1)
    cells.append(f'<div class="c"><div class="f">{blink}</div><b>blink</b></div>')
    full = ev.svg(idp="fu")
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
body{{margin:0;background:#5c0d16;font:18px sans-serif;color:#fff;display:flex;gap:16px;padding:12px}}
.g{{display:grid;grid-template-columns:repeat(5,220px);gap:10px}} .c{{text-align:center}}
.f svg{{width:220px;height:220px;background:#f3e6d0;border-radius:8px}} .full svg{{width:420px;height:518px}} {css}
</style></head><body><div class="g">{"".join(cells)}</div><div class="full">{full}</div></body></html>"""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1640, "height": 560})
        pg.set_content(html); pg.wait_for_timeout(300)
        pg.screenshot(path=str(out / "cartoon.png"), full_page=True)
        b.close()
    print(out / "cartoon.png")


if __name__ == "__main__":
    main()
