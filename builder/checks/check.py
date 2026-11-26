#!/usr/bin/env python3
"""Play-test a built festival app in a headless browser.

  python checks/check.py events/<slug>                 all checks on build/<slug>/site
  python checks/check.py events/<slug> --only fit,names

Checks:
  load     every voice clip preloads, no failed requests, no page errors
  lips     a wrong answer and a right answer: the cartoon's mouth moves through shapes and ends at rest
  welcome  tapping the cartoon on the welcome screen plays the welcome line with moving lips
  fit      every blessing and wrong-answer line fits its speech bubble (landscape + portrait, Hindi + English)
  names    150 simulated questions: lines naming the hosts are at least 6 questions apart; nothing repeats too soon
  hosts    (events with a Hosts setting) typed names show on the welcome card and in the lines, the voice says them
           from the name bank with moving lips, unknown names fall back to "यजमान जी", clearing them goes generic
"""
import argparse
import random
import re
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "engine"))
from event import Event  # noqa: E402

SAMPLE = """async ([ms, sel]) => { const out = []; const t0 = performance.now();
  while (performance.now() - t0 < ms) { const s = document.querySelector(sel);
    out.push(s ? (s.getAttribute('data-m') || '-') : '_'); await new Promise(r => setTimeout(r, 40)); } return out.join(''); }"""
OVERLAY_SVG = "#oops:not([hidden]) svg.bhag, #bless:not([hidden]) svg.bhag"


def squash(s):
    return "".join(c for i, c in enumerate(s) if i == 0 or s[i - 1] != c)


class Server:
    def __init__(self, folder, port):
        self.url = f"http://localhost:{port}/"
        self.p = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "-d", str(folder)],
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1)

    def stop(self):
        self.p.terminate()


def fresh(pg, url, state):
    pg.goto(url)
    pg.evaluate("([k, s]) => localStorage.setItem(k, JSON.stringify(s))", [EV.cfg["storage_key"], state])
    pg.reload()
    pg.wait_for_timeout(1000)


def check_load(b, url):
    pg = b.new_page(viewport={"width": 1280, "height": 720})
    reqs, bad, errs = [], [], []
    pg.on("response", lambda r: (reqs.append(r.url), r.status >= 400 and bad.append((r.status, r.url))))
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(url); pg.wait_for_timeout(1200)
    pg.click(".brand"); pg.wait_for_timeout(3000)   # any tap in the app turns sound on
    mp3 = [u for u in reqs if u.endswith(".mp3")]
    expect = len(EV.lines())
    ok = not bad and not errs and len(set(mp3)) == expect
    print(f"load: {len(set(mp3))}/{expect} clips preloaded | failed {bad or 'none'} | errors {errs or 'none'}")
    pg.close()
    return ok


def check_lips(b, url):
    pg = b.new_page(viewport={"width": 1280, "height": 720})
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    fresh(pg, url, {"at": "w1"})
    pg.click(".brand"); pg.wait_for_timeout(1500)
    pg.click("#wrongBtn"); w = squash(pg.evaluate(SAMPLE, [7000, OVERLAY_SVG]))
    pg.wait_for_timeout(1500)
    pg.click("#rightBtn"); r = squash(pg.evaluate(SAMPLE, [11000, OVERLAY_SVG]))
    print("lips: wrong", w[:60], "| right", r[:60])
    ok = len(set(w) - set("X-_")) >= 4 and len(set(r) - set("X-_")) >= 4 and not errs
    pg.close()
    return ok


def check_welcome(b, url):
    pg = b.new_page(viewport={"width": 1280, "height": 720})
    errs, clips = [], []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    key = EV.content.WELCOME["key"]
    pg.on("request", lambda r: r.url.endswith(f"-{key}.mp3") and clips.append(r.url))
    fresh(pg, url, {"at": "welcome"})
    first = pg.inner_text("#mainBtn")
    pg.click(".wl-god"); seq = squash(pg.evaluate(SAMPLE, [6000, "#content svg.bhag"]))
    print(f"welcome: button '{first}' | clip fetched {bool(clips)} | mouth {seq[:50]}")
    ok = bool(clips) and len(set(seq) - set("X-_")) >= 4 and not errs
    pg.close()
    return ok


def check_fit(b, url):
    ok = True
    probe = """(sel) => { const ov = document.querySelector(sel), bub = ov.querySelector('.bl-bubble'), body = ov.querySelector('.bl-body');
      return [parseFloat(bub.style.getPropertyValue('--bf') || 1), bub.offsetHeight, body.clientHeight, bub.scrollWidth > bub.clientWidth + 2]; }"""
    nb, nw = len(EV.content.BLESSINGS), len(EV.content.WRONGS)
    runs = [(n, vp, lang, "") for n, vp in [("landscape", {"width": 1280, "height": 720}), ("portrait", {"width": 390, "height": 844})]
            for lang in ("hi", "en")]
    if EV.hostable:  # the longest names people are likely to type
        runs += [(n, vp, "hi", "Chandrashekhar, Subramaniam, Venkatesh") for n, vp in
                 [("landscape", {"width": 1280, "height": 720}), ("portrait", {"width": 390, "height": 844})]]
    for name, vp, lang, hosts in runs:
            pg = b.new_page(viewport=vp)
            fresh(pg, url, {"at": "p1", "voice": False, "sfx": False, "lang": lang, "hostText": hosts,
                            "decks": {"w": {"n": nw, "q": list(range(nw))[::-1], "recent": []},
                                      "b": {"n": nb, "q": list(range(nb))[::-1], "recent": []}}})
            worst, bad = 1.0, []
            for i in range(nw):
                pg.click("#wrongBtn"); pg.wait_for_timeout(110)
                k, h, ch, wide = pg.evaluate(probe, "#oops"); worst = min(worst, k)
                if h > ch - 30 or wide:
                    bad.append(f"wrong {i + 1}")
                pg.click("#oops", position={"x": 20, "y": 20}); pg.wait_for_timeout(70)
            for i in range(nb):
                pg.click("#rightBtn"); pg.wait_for_timeout(140)
                k, h, ch, wide = pg.evaluate(probe, "#bless"); worst = min(worst, k)
                if h > ch - 30 or wide:
                    bad.append(f"blessing {i + 1}")
                pg.click("#bless", position={"x": 20, "y": 20}); pg.wait_for_timeout(70)
                pg.click("#ansBtn"); pg.wait_for_timeout(70)
            print(f"fit: {name:9s} {lang}{' + long host names' if hosts else ''}: smallest text scale {worst:.2f} | overflowing: {bad or 'none'}")
            ok = ok and not bad
            pg.close()
    return ok


def check_names(b, url, questions=150, seed=7):
    state = {"at": "w1", "voice": False, "sfx": False}
    names = EV.name_words
    if EV.hostable:
        state["hostText"] = "Asha, Ravi"
        names = ["आशा", "रवि", "Asha", "Ravi"]
    if not names:
        print("names: no hosts configured, skipped"); return True
    named = re.compile("|".join(re.escape(n) for n in names))
    random.seed(seed)
    pg = b.new_page(viewport={"width": 1280, "height": 720})
    fresh(pg, url, state)
    events, q = [], 0
    while q < questions:
        if not pg.is_visible("#wrongBtn"):
            if pg.inner_text("#mainBtn").strip().upper() == "BACK TO START":
                pg.click("#mainBtn")
            else:
                pg.keyboard.press("ArrowRight")
            pg.wait_for_timeout(60)
            continue
        q += 1
        if q == questions // 2:
            pg.reload(); pg.wait_for_timeout(900)          # closing and reopening the app keeps the rules
        for _ in range(random.choice([0, 0, 1, 1, 2])):
            pg.keyboard.press("w"); pg.wait_for_timeout(40)
            events.append((q, "w", pg.inner_text("#oopsText"))); pg.keyboard.press("Escape")
        pg.keyboard.press("r"); pg.wait_for_timeout(40)
        events.append((q, "b", pg.inner_text("#blessOpen") + " " + pg.inner_text("#blessText")))
        pg.keyboard.press("Escape"); pg.keyboard.press("ArrowRight"); pg.wait_for_timeout(60)
    pg.close()
    nq = [qn for qn, _, t in events if named.search(t)]
    gaps = [y - x for x, y in zip(nq, nq[1:])]
    closest = {}
    for kind in "wb":
        seq = [t for _, k, t in events if k == kind]
        last, worst = {}, 10 ** 9
        for j, t in enumerate(seq):
            if t in last:
                worst = min(worst, j - last[t])
            last[t] = j
        closest[kind] = worst
    print(f"names: {len(nq)} name lines in {questions} questions | gaps {min(gaps) if gaps else '-'}..{max(gaps) if gaps else '-'} "
          f"| closest repeat: wrong {closest['w']} lines, blessing {closest['b']} lines")
    return (not gaps or min(gaps) >= 6) and min(closest.values()) >= 8


def check_hosts(b, url):
    if not EV.hostable:
        print("hosts: this event has no Hosts setting, skipped"); return True
    ok = True
    pg = b.new_page(viewport={"width": 1280, "height": 720})
    errs, reqs = [], []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("request", lambda r: reqs.append(r.url.rsplit("/", 1)[1]))
    # no names: the welcome card offers to add them
    fresh(pg, url, {"at": "welcome"})
    add_visible = pg.is_visible(".wl-add") and not pg.is_visible(".wl-hosts")
    # type names in the Menu, as a person would
    pg.click(".wl-add"); pg.wait_for_timeout(400)
    pg.fill("#hostIn", "Reshma, Shobhit"); pg.press("#hostIn", "Enter"); pg.wait_for_timeout(300)
    note = pg.inner_text("#hostNote")
    pg.click("#gridSheet [data-close]"); pg.wait_for_timeout(300)
    card = pg.inner_text(".wl-hosts") if pg.is_visible(".wl-hosts") else ""
    pg.click(".wl-god"); seq = squash(pg.evaluate(SAMPLE, [8000, "#content svg.bhag"]))
    voice = EV.voices[0]
    got_bank = f"names-{voice}.mp3" in reqs and f"names-{voice}.json" in reqs
    got_pieces = any(f"-{EV.content.WELCOME['host']['key']}0.mp3" in r for r in reqs)
    print(f"hosts: add-button {add_visible} | note '{note[:60]}' | card '{card}' | name pack {got_bank} | pieces {got_pieces} | mouth {seq[:40]}")
    ok = add_visible and "रेशमा" in note and card == "Reshma and Shobhit" and got_bank and got_pieces and len(set(seq) - set("X-_")) >= 4
    # a host line on a puzzle shows the names
    host_w = [i for i, w in enumerate(EV.content.WRONGS) if "host" in w]
    nb, nw = len(EV.content.BLESSINGS), len(EV.content.WRONGS)
    fresh(pg, url, {"at": "p1", "hostText": "Reshma, Shobhit", "decks": {"w": {"n": nw, "q": [host_w[0]], "recent": []}}})
    pg.click(".brand"); pg.click("#wrongBtn"); pg.wait_for_timeout(300)
    line = pg.inner_text("#oopsText") + " " + pg.inner_text("#oopsEn")
    seq = squash(pg.evaluate(SAMPLE, [6000, OVERLAY_SVG]))
    print(f"hosts: wrong-answer line '{line[:70]}' | mouth {seq[:40]}")
    ok = ok and bool(re.search("रेशमा|शोभित", line)) and len(set(seq) - set("X-_")) >= 4
    # a name the bank doesn't know
    fresh(pg, url, {"at": "welcome", "hostText": "Xyzzy"})
    pg.click("#gridBtn"); pg.wait_for_timeout(300)
    unknown_note = pg.inner_text("#hostNote")
    pg.fill("#hostIn", ""); pg.press("#hostIn", "Enter"); pg.wait_for_timeout(300)
    pg.click("#gridSheet [data-close]"); pg.wait_for_timeout(300)
    cleared = pg.is_visible(".wl-add") and not pg.is_visible(".wl-hosts")
    print(f"hosts: unknown name note '{unknown_note[:80]}' | cleared back to general {cleared} | errors {errs or 'none'}")
    ok = ok and "यजमान जी" in unknown_note and cleared and not errs
    pg.close()
    return ok


CHECKS = {"load": check_load, "lips": check_lips, "welcome": check_welcome, "fit": check_fit, "names": check_names, "hosts": check_hosts}


def main():
    global EV
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("event")
    ap.add_argument("--site", help="built site folder (default build/<slug>/site)")
    ap.add_argument("--only", default=",".join(CHECKS))
    ap.add_argument("--port", type=int, default=8790)
    a = ap.parse_args()
    EV = Event(a.event)
    site = Path(a.site) if a.site else HERE.parent / "build" / EV.slug / "site"
    from playwright.sync_api import sync_playwright
    srv = Server(site, a.port)
    results = {}
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
            for name in a.only.split(","):
                results[name] = CHECKS[name](b, srv.url)
            b.close()
    finally:
        srv.stop()
    print("RESULT:", " ".join(f"{k}={'ok' if v else 'FAIL'}" for k, v in results.items()))
    sys.exit(0 if all(results.values()) else 1)


EV = None
if __name__ == "__main__":
    main()
