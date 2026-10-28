#!/usr/bin/env python3
"""Screenshot every puzzle (question and answer) of a built app and make contact sheets to look at.

  python checks/cards.py events/<slug>            -> build/<slug>/review/cards-1.png, cards-2.png, ... (+ one PNG per card)

Look at every sheet before shipping: is each picture clear, is nothing cut off or overlapping, does the answer
card explain the trick?
"""
import argparse
import subprocess
import sys
import time
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "engine"))
from event import Event  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("event")
    ap.add_argument("--site")
    ap.add_argument("--port", type=int, default=8791)
    a = ap.parse_args()
    ev = Event(a.event)
    site = Path(a.site) if a.site else HERE.parent / "build" / ev.slug / "site"
    out = site.parent / "review"
    (out / "cards").mkdir(parents=True, exist_ok=True)
    ids = [f"w{i}" for i in range(1, len(ev.content.WARMUPS) + 1)] + [f"p{i}" for i in range(1, len(ev.content.PUZZLES) + 1)]
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(a.port), "-d", str(site)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    shots = []
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page(viewport={"width": 1280, "height": 720})
            pg.goto(f"http://localhost:{a.port}/")
            for sid in ids:
                pg.evaluate("([k, s]) => localStorage.setItem(k, JSON.stringify(s))",
                            [ev.cfg["storage_key"], {"at": sid, "voice": False, "sfx": False}])
                pg.reload(); pg.wait_for_timeout(700)
                q = out / "cards" / f"{sid}-q.png"; pg.screenshot(path=str(q))
                pg.click("#ansBtn"); pg.wait_for_timeout(500)
                ans = out / "cards" / f"{sid}-a.png"; pg.screenshot(path=str(ans))
                shots.append((sid, q, ans))
            b.close()
    finally:
        srv.terminate()
    # contact sheets: each row is one puzzle, question left and answer right
    tw, th, per = 640, 360, 6
    for n in range(0, len(shots), per):
        chunk = shots[n:n + per]
        sheet = Image.new("RGB", (tw * 2 + 30, (th + 34) * len(chunk)), "#222")
        d = ImageDraw.Draw(sheet)
        for r, (sid, q, ans) in enumerate(chunk):
            y = r * (th + 34)
            d.text((8, y + 8), sid.upper(), fill="#fff")
            sheet.paste(Image.open(q).convert("RGB").resize((tw, th)), (0, y + 30))
            sheet.paste(Image.open(ans).convert("RGB").resize((tw, th)), (tw + 30, y + 30))
        path = out / f"cards-{n // per + 1}.png"
        sheet.save(path)
        print(path)


if __name__ == "__main__":
    main()
