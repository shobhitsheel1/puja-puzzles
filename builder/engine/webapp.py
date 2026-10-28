"""Turn the built app into a standalone web app for GitHub Pages: no Claude bar, an Add to Home Screen icon,
and it keeps working offline once opened."""
import json
import shutil

from PIL import Image

import common as R

FLUENT_MIT = """Fluent Emoji (3D) by Microsoft, https://github.com/microsoft/fluentui-emoji

MIT License

Copyright (c) Microsoft Corporation.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


def _page(ev, app_dir):
    cfg = ev.cfg
    title, desc = cfg["app_title"], cfg["description"]
    src = (app_dir / "index.html").read_text(encoding="utf-8")
    drop = [
        f"<title>{title}</title>\n",
        '<meta name="claude:viewport-fit-sides" content="cover">\n',
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n',
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n',
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Baloo+2:wght@800&family=Luckiest+Guy&family=Poppins:wght@600;700;800;900&display=swap">\n',
    ]
    for d in drop:
        assert src.count(d) == 1, d
        src = src.replace(d, "")
    hot = ("window.claude?.hot?.snapshot?.(() => ({state: S}));\n"
           "window.claude?.hot?.ready ? window.claude.hot.ready(start) : start(window.claude?.hot?.data ?? {});")
    assert src.count(hot) == 1
    src = src.replace(hot, "start({});\n"
                      "if ('serviceWorker' in navigator) window.addEventListener('load', () => "
                      "navigator.serviceWorker.register('sw.js').catch(() => {}));")
    head = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#2c0609">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="{title}">
<meta name="application-name" content="{title}">
<meta name="format-detection" content="telephone=no">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">
<style>
{R.FONT_CSS}
:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}
[hidden]{{display:none!important}}
</style>
</head>
<body>
"""
    return head + src + "\n</body>\n</html>\n"


def _icon_html(site, garland, maskable):
    k = 0.84 if maskable else 1.0
    flowers = []
    n = 9
    for i in range(n):
        x = -40 + i * (1104 / (n - 1))
        t = (x - 512) / 552
        y = 70 + 60 * (1 - t * t)
        style = "filter:hue-rotate(18deg) saturate(1.25) brightness(1.12);" if i % 2 else ""
        flowers.append(f'<img src="{(site / "assets" / f"{garland}.webp").as_uri()}" style="position:absolute;'
                       f'left:{x - 75:.0f}px;top:{y - 75:.0f}px;width:150px;height:150px;{style}">')
    fonts = R.FONT_CSS.replace("url(fonts/", "url(" + (site / "fonts").as_uri() + "/")
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{fonts}
html,body{{margin:0;width:1024px;height:1024px;overflow:hidden}}
.bg{{position:relative;width:1024px;height:1024px;background:radial-gradient(circle at 50% 52%, #b42c33 0%, #6e1119 55%, #2c0609 100%)}}
.grp{{position:absolute;left:0;top:0;width:1024px;height:1024px;transform:scale({k});transform-origin:512px 560px}}
.card{{position:absolute;left:197px;top:300px;width:630px;height:540px;background:#fff;border:30px solid #E2412E;border-radius:26px;
  transform:rotate(-5deg);box-shadow:0 34px 60px rgba(0,0,0,.45);display:flex;align-items:center;justify-content:center}}
.q{{position:relative;font-family:'Luckiest Guy';font-size:430px;line-height:1;margin-top:58px}}
.q .b{{position:absolute;left:0;top:0;-webkit-text-stroke:44px #0b0b0b;color:#0b0b0b;text-shadow:0 18px 0 #0b0b0b}}
.q .f{{position:relative;color:#7CF542}}
</style></head><body><div class="bg">{"".join(flowers)}
<div class="grp"><div class="card"><div class="q"><div class="b">?</div><div class="f">?</div></div></div></div>
</div><script>document.fonts.ready.then(()=>{{window.__ready=true}})</script></body></html>"""


def _icons(ev, site, work):
    from playwright.sync_api import sync_playwright
    work.mkdir(parents=True, exist_ok=True)
    garland = ev.cfg["decor"]["garland"]
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1024, "height": 1024})
        for name, mask in (("icon-1024.png", False), ("icon-maskable-1024.png", True)):
            f = work / ("icon_mask.html" if mask else "icon.html")
            f.write_text(_icon_html(site, garland, mask), encoding="utf-8")
            pg.goto(f.as_uri())
            pg.wait_for_function("window.__ready === true")
            pg.wait_for_timeout(200)
            pg.screenshot(path=str(work / name))
        b.close()
    big = Image.open(work / "icon-1024.png").convert("RGB")
    mask = Image.open(work / "icon-maskable-1024.png").convert("RGB")
    big.resize((180, 180), Image.LANCZOS).save(site / "icons" / "apple-touch-icon.png", optimize=True)
    big.resize((192, 192), Image.LANCZOS).save(site / "icons" / "icon-192.png", optimize=True)
    big.resize((512, 512), Image.LANCZOS).save(site / "icons" / "icon-512.png", optimize=True)
    mask.resize((512, 512), Image.LANCZOS).save(site / "icons" / "icon-maskable-512.png", optimize=True)


def _service_worker(ev, files):
    cfg = ev.cfg
    prefix = cfg["cache_prefix"]
    cache = f'{prefix}{cfg["cache_version"]}'
    return f"""// Keeps {cfg["app_title"]} working offline once it has been opened.
const CACHE = '{cache}', PREFIX = '{prefix}';
const FILES = {json.dumps(files, indent=2)};

self.addEventListener('install', event => {{
  // 'reload' skips the browser's short-term cache, so a new version always saves fresh files.
  event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(FILES.map(f => new Request(f, {{cache: 'reload'}}))))
    .then(() => self.skipWaiting()));
}});

self.addEventListener('activate', event => {{
  // Only this app's old versions: other apps on the same github.io address keep their own saved files.
  event.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k.startsWith(PREFIX) && k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
}});

self.addEventListener('fetch', event => {{
  const req = event.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== self.location.origin) return;
  if (req.mode === 'navigate') {{
    // Fresh page when online, saved copy when offline.
    event.respondWith(fetch(req).then(res => {{
      const copy = res.clone();
      caches.open(CACHE).then(c => c.put('index.html', copy));
      return res;
    }}).catch(() => caches.match('index.html')));
    return;
  }}
  event.respondWith(caches.match(req, {{ignoreSearch: true}}).then(hit => hit || fetch(req)));
}});
"""


def build_site(ev, app_dir, site, work):
    cfg, ch = ev.cfg, ev.character
    title, desc = cfg["app_title"], cfg["description"]
    if site.exists():
        shutil.rmtree(site)
    for d in ("assets", "fonts", "icons", "licenses"):
        (site / d).mkdir(parents=True)
    (site / "index.html").write_text(_page(ev, app_dir), encoding="utf-8")
    for f in (app_dir / "assets").iterdir():
        shutil.copy(f, site / "assets" / f.name)
    for f, pkg in R.FONT_FILES.items():
        shutil.copy(R.VENDOR / pkg / "package/files" / f, site / "fonts" / f)
    for name, pkg in [("Poppins-OFL.txt", "fontsource-poppins-5.3.0"), ("Anton-OFL.txt", "fontsource-anton-5.3.0"),
                      ("Baloo2-OFL.txt", "fontsource-baloo-2-5.3.0"), ("LuckiestGuy-Apache-2.0.txt", "fontsource-luckiest-guy-5.3.0")]:
        shutil.copy(R.VENDOR / pkg / "package/LICENSE", site / "licenses" / name)
    cards = "\n\n".join((R.TTS / f"vits-piper-hi_IN-{v}-medium" / "MODEL_CARD").read_text() for v in ev.voices)
    (site / "licenses" / "Hindi-voices.txt").write_text(
        "The spoken Hindi lines (assets/v-*.mp3) were generated with Piper text-to-speech voices,\n"
        "run offline with sherpa-onnx (https://github.com/k2-fsa/sherpa-onnx). Non-commercial use only.\n\n" + cards,
        encoding="utf-8")
    rhubarb = next((R.VENDOR / "rhubarb" / "x").glob("*/LICENSE.md")).read_text(encoding="utf-8")
    (site / "licenses" / "RhubarbLipSync-MIT.txt").write_text(
        f"{ch['name']}'s mouth timings were worked out with Rhubarb Lip Sync, https://github.com/DanielSWolf/rhubarb-lip-sync\n\n"
        + rhubarb.split("## Third-party dependencies")[0].rstrip() + "\n", encoding="utf-8")
    (site / "licenses" / "FluentEmoji-MIT.txt").write_text(FLUENT_MIT, encoding="utf-8")
    _icons(ev, site, work)

    manifest = {
        "name": title, "short_name": title, "description": desc,
        "start_url": "./", "scope": "./", "display": "standalone", "orientation": "any",
        "background_color": "#2c0609", "theme_color": "#2c0609",
        "icons": [
            {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
            {"src": "icons/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        ],
    }
    (site / "manifest.webmanifest").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    files = ["./", "index.html", "manifest.webmanifest"]
    for d in ("icons", "fonts", "assets"):
        files += [f"{d}/{p.name}" for p in sorted((site / d).iterdir())]
    (site / "sw.js").write_text(_service_worker(ev, files), encoding="utf-8")
    (site / ".nojekyll").write_text("", encoding="utf-8")
    voices = ", ".join(f'"{v}"' for v in ev.voices)
    (site / "README.md").write_text(f"""# {title}

{desc} {cfg.get("readme_summary", "")}

**Play:** open the GitHub Pages link on your phone, then use Share → Add to Home Screen to get it as an app.
Turn the phone sideways for the TV layout. Tap **Right** or **Wrong** after each guess; swipe to move between puzzles.

## Credits

- 3D emoji pictures: [Fluent Emoji](https://github.com/microsoft/fluentui-emoji) by Microsoft (MIT)
- Fonts: Poppins, Anton and Baloo 2 (SIL Open Font License), Luckiest Guy (Apache 2.0)
- {ch['name']}'s Hindi voice: recorded with the Piper voices {voices}, run offline with sherpa-onnx. Non-commercial use only (see licenses/Hindi-voices.txt).
- Lip sync: mouth timings worked out from each voice line with [Rhubarb Lip Sync](https://github.com/DanielSWolf/rhubarb-lip-sync) by Daniel Wolf (MIT)

License texts are in the `licenses` folder. Built with the festival puzzle builder in `builder/`.
""", encoding="utf-8")
    total = sum(p.stat().st_size for p in site.rglob("*") if p.is_file())
    print("web app:", sum(1 for p in site.rglob("*") if p.is_file()), "files,", total // 1024, "KB ->", site)
