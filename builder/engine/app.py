"""Build the festival puzzle app for one event: one page with a landscape (TV) and a portrait layout.

python build.py events/<slug> runs this; see README.md. Everything that depends on the festival or the hosts comes
from the event folder (config.json, content.py, deity.py, voice/, lips.json).
"""
import json
import re
import shutil
from pathlib import Path

import common as R
from event import VOICE_INFO


# ------------------------------------------------------------------ decorations

def toran(width, n, sag, strands, leaf_ok, cls, garland, bell):
    out = []
    span = width + 48
    pts = []
    for i in range(n):
        x = -24 + i * span / (n - 1)
        t = (x - width / 2) / (span / 2)
        pts.append((x, 30 + sag * (1 - t * t)))
    d = "M " + " L ".join(f"{x:.0f},{y:.0f}" for x, y in pts)
    out.append(f'<svg class="tstring" width="{width}" height="200" aria-hidden="true"><path d="{d}" '
               'stroke="#8D5A2B" stroke-width="4" fill="none"/></svg>')
    for i in range(n - 1):
        x = (pts[i][0] + pts[i + 1][0]) / 2
        y = (pts[i][1] + pts[i + 1][1]) / 2
        if leaf_ok(x):
            out.append(R.leaf(x, y + 12, -8 if i % 2 else 8, 66))
    yellow = "filter:hue-rotate(18deg) saturate(1.25) brightness(1.12);"
    for sx in strands:
        out.append(f'<div style="position:absolute;left:{sx - 2}px;top:40px;width:4px;height:200px;background:#8D5A2B"></div>')
        for k in range(3):
            yy = 92 + k * 52
            out.append(f'<img alt="" src="assets/{garland}.webp" style="position:absolute;left:{sx - 28}px;'
                       f'top:{yy - 28}px;width:56px;height:56px;{yellow if k % 2 else ""}">')
        out.append(f'<img alt="" src="assets/{bell}.webp" style="position:absolute;left:{sx - 26}px;top:236px;width:52px;height:52px">')
    for i, (x, y) in enumerate(pts):
        out.append(f'<img alt="" src="assets/{garland}.webp" style="position:absolute;left:{x - 36:.0f}px;'
                   f'top:{y - 36:.0f}px;width:72px;height:72px;{yellow if i % 2 else ""}">')
    return f'<div class="toran {cls}" aria-hidden="true">' + "".join(out) + "</div>"


HYPH = re.compile(r"(?<![\w:/.\-])([A-Za-z]+(?:-[A-Za-z]+)+)(?![\w:/.\-])")


def nowrap(text):
    """Keep sound-alike words such as Pray-sad on one line."""
    return HYPH.sub(r'<span style="white-space:nowrap">\1</span>', text)


def outl(text, cls, size):
    return (f'<div class="outl {cls}" data-fit data-size="{size}">'
            f'<div class="b">{text}</div><div class="f">{text}</div></div>')


ASK = ('<div class="ask">' + R.img("1f914", 104)
       + '<div class="outl white askt"><div class="b">CAN YOU SOLVE IT?</div>'
         '<div class="f">CAN YOU SOLVE IT?</div></div></div>')

TIPS = R.tips()


# ------------------------------------------------------------------ slides

def slides(ev):
    cfg, tx, c = ev.cfg, ev.texts, ev.content
    WARMUPS, PUZZLES = c.WARMUPS, c.PUZZLES
    ch, fest, banner = ev.character, cfg["festival"], cfg["banner"]
    pill = cfg.get("pill", banner.title())
    rng = {k: f'{a}–{b}' for k, (a, b) in ev.level_ranges().items()}
    out = []
    out.append(dict(
        id="welcome", kind="intro", tile="Welcome", group="start",
        pills=[["num", pill]],
        prompt=outl("WELCOME!", "gold", 110),
        body=('<div class="wl">'
              f'<div class="wl-god" data-welcome role="button" aria-label="Hear {ch['name']}\'s welcome">{ev.svg(idp="wg")}</div>'
              '<div class="wl-txt">'
              '<div class="sub wl-a">Welcome to the</div>'
              f'<div class="big wl-b">{fest["en"]}</div>'
              f'<div class="wl-deva">{fest.get("hi_title", fest["hi"])}</div>'
              f'<div class="wl-div">{R.img(cfg["decor"]["lamp"], 58)}</div>'
              '<div class="sub wl-a">hosted by</div>'
              f'<div class="big wl-c">{ev.hosts_en}</div>'
              f'<div class="wl-tap" data-welcome>{R.img("1f50a", 40)}<span>Tap {ch["name"]} to hear {ch["pronoun"]} welcome</span></div>'
              '</div></div>'),
        footer=f'<div class="deva">{tx["welcome_footer_deva"]}</div>'
               f'<div class="exp">{tx["welcome_footer_en"]}</div>',
        bottom=banner))
    howto_items = [
        ("1f5bc-fe0f", "Every picture hides a <b>word, name or phrase</b>"),
        ("1f4e2", "<b>Say it out loud</b>: pictures sound like words"),
        ("1f522", "<b>Count</b>: one, two… or ek, do, teen!"),
        ("1f4cd", "<b>Notice where</b> words sit: over, under…"),
        ("1f9e9", "<b>Spot what's missing</b>"),
        ("1f524", "<b>Translate</b>: answers can be Hindi or Sanskrit"),
    ]
    out.append(dict(
        id="howto", kind="intro", tile="How to play", group="start",
        pills=[["num", pill]],
        prompt=outl("HOW TO PLAY", "gold", 104),
        body='<div class="howto">' + "".join(
            f'<div class="it">{R.img(c, 66)}<span>{t}</span></div>' for c, t in howto_items) + "</div>",
        footer=f'<div class="trick">{len(WARMUPS)} warm-ups, then {len(PUZZLES)} puzzles</div>'
               '<div class="exp">Shout out your answer. First correct guess wins the point!</div>',
        bottom=banner))
    for i, w in enumerate(WARMUPS, 1):
        out.append(dict(
            id=f"w{i}", kind="puzzle", tile=f"W{i}", group="warm", level="easy",
            pills=[["num", f"Warm-up {i} / {len(WARMUPS)}"], ["easy", "Easy"]],
            body=w["body"], hint=w["hint"],
            aPrompt=outl(w["answer"], "ans", 116),
            aFooter=f'<div class="trick">{w["trick"]}</div><div class="exp">{R.inline(nowrap(w["explain"]))}</div>',
            bottom=tx["warmup_bottom"]))
    out.append(dict(
        id="round2", kind="intro", tile="Round 2", group="start",
        pills=[["num", "Round 2"]],
        prompt=outl("WARM-UP DONE!", "ans", 104),
        body=(R.img(tx["round2_icon"], 200)
              + '<div class="big" style="font-size:88px;margin-top:14px">Now the real quiz!</div>'
              + f'<div class="sub" style="font-size:38px;margin-top:8px">{tx["round2_sub"].format(n=len(PUZZLES))}</div>'
              + f'<div class="chips" style="margin-top:34px"><div class="chip" style="background:#2E7D32">Easy {rng["easy"]}</div>'
              + f'<div class="chip" style="background:#E65100">Medium {rng["medium"]}</div><div class="chip" style="background:#B71C1C">Hard {rng["hard"]}</div></div>'),
        footer=TIPS, bottom=banner))
    for i, p in enumerate(PUZZLES, 1):
        n_lines = p["answer"].count("<br>") + 1
        out.append(dict(
            id=f"p{i}", kind="puzzle", tile=str(i), group="main", level=p["level"],
            pills=[["num", f"Puzzle {i} / {len(PUZZLES)}"], [p["level"], p["level"].title()], ["", p["cat"]]],
            body=p["body"], hint=p["hint"],
            aPrompt=outl(p.get("answer_html", p["answer"]), "ans", 116 if n_lines == 1 else 80),
            aFooter=f'<div class="deva">{p["deva"]}</div><div class="exp">{R.inline(nowrap(p["explain"]))}</div>',
            bottom=banner))
    out.append(dict(
        id="end", kind="intro", tile="The end", group="start",
        pills=[["num", "The End"]],
        prompt=outl("THAT'S A WRAP!", "ans", 104),
        body="",
        footer=f'<div class="deva">{tx["end_deva"]}</div>'
               '<div class="exp">Count your points. Who is today\'s puzzle champion? '
               '<img class="ie" alt="" src="assets/1f3c6.webp"></div>',
        bottom=banner))
    return out


def end_default(ev):
    tx = ev.texts
    return (R.img(tx["end_icon"], 150)
            + f'<div class="big" style="font-size:66px;margin-top:10px">{tx["end_big"]}</div>'
            + f'<div class="deva" style="color:#B3261E;text-shadow:none;font-size:52px;margin-top:8px">{tx["end_deva"]}</div>')


CSS = r"""
:root{
  /* Layout: a fixed festive stage (16:9 for TV, tall for phone) scaled to the screen; card left, answer column right. */
  color-scheme:dark;
  --maroon-hi:#a5262c; --maroon:#6e1119; --maroon-lo:#2c0609; --panel:#3d0a10;
  --marigold:#FFD54F; --marigold-soft:#FFE082; --saffron:#FF8F1F; --sindoor:#E2412E;
  --tulsi:#7CF542; --ink:#111111; --paper:#ffffff; --cream:#FFF4DA; --wheat:#FFE9B0;
  --line:rgba(255,213,79,.5); --veil:rgba(20,2,4,.74);
  --f-display:'Luckiest Guy','Arial Black',Impact,sans-serif;
  --f-body:'Poppins',-apple-system,'Segoe UI',Roboto,sans-serif;
  --f-cond:'Anton',Impact,'Arial Narrow',sans-serif;
  --f-deva:'Baloo 2','Kohinoor Devanagari','Noto Sans Devanagari',sans-serif;
}
html{height:100%;box-sizing:border-box}
*,*::before,*::after{box-sizing:border-box}
body{height:100%;margin:0;overflow:hidden;color:var(--paper);font-family:var(--f-body);
  background:radial-gradient(70% 70% at 50% 50%, rgba(255,166,51,.16), rgba(255,166,51,0) 70%),
             radial-gradient(140% 100% at 50% 40%, var(--maroon-hi) 0%, var(--maroon) 46%, var(--maroon-lo) 100%);
  background-color:var(--maroon-lo);
  padding-left:max(16px, env(safe-area-inset-left, 0px));padding-right:max(16px, env(safe-area-inset-right, 0px));
  -webkit-tap-highlight-color:transparent;-webkit-user-select:none;user-select:none;-webkit-text-size-adjust:100%}
#app{position:relative;width:100%;height:100%;overflow:hidden;touch-action:none}
.stage{position:absolute;left:0;top:0;transform-origin:0 0;font-family:var(--f-body)}
.stage.land{width:1920px;height:1080px}
.stage.port{width:1080px;height:1560px}
.stage img{max-width:none}
.land .tp,.port .tl{display:none}
.toran{position:absolute;left:0;top:0;pointer-events:none}
.tstring{position:absolute;left:0;top:0}
.mandala{position:absolute;opacity:.11;pointer-events:none;transform:translate(-50%,-50%)}
.land .mandala{left:670px;top:550px;width:1700px;height:1700px}
.port .mandala{left:540px;top:780px;width:1500px;height:1500px}

.brand{position:absolute;text-align:center;font-family:var(--f-display);color:var(--marigold);letter-spacing:3px;
  text-shadow:0 5px 0 #7a3300,0 10px 24px rgba(0,0,0,.5);white-space:nowrap}
.land .brand{left:1280px;width:550px;top:116px;font-size:66px}
.port .brand{left:0;width:1080px;top:116px;font-size:62px}
.pills{position:absolute;display:flex;flex-wrap:wrap;justify-content:center;gap:12px}
.land .pills{left:1280px;width:550px;top:200px;gap:10px}
.land .pill{font-size:21px;padding:6px 16px;letter-spacing:1px}
.port .pills{left:0;width:1080px;top:200px}
.pill{font-weight:800;font-size:25px;letter-spacing:1.5px;padding:7px 22px;border-radius:999px;color:var(--paper);
  background:rgba(255,255,255,.12);border:2px solid rgba(255,255,255,.42);text-transform:uppercase;white-space:nowrap}
.pill.num{background:var(--paper);color:#7a1016;border-color:var(--paper)}
.pill.easy{background:#2E7D32;border-color:#8BD48F}
.pill.medium{background:#E65100;border-color:#FFB74D}
.pill.hard{background:#B71C1C;border-color:#F4A3A3}

.prompt{position:absolute;display:flex;align-items:center;justify-content:center;text-align:center}
.land .prompt{left:1280px;width:550px;top:322px;height:268px}
.port .prompt{left:20px;width:1040px;top:270px;height:188px}
.outl{position:relative;display:inline-block;font-family:var(--f-display);line-height:1.04;letter-spacing:1px;text-align:center}
.port .outl{white-space:nowrap}
.land .outl{white-space:normal;text-wrap:balance;overflow-wrap:normal;word-break:keep-all}
.outl .b{position:absolute;left:0;top:0;right:0;bottom:0;-webkit-text-stroke:20px #0b0b0b;color:#0b0b0b;text-shadow:0 9px 0 #0b0b0b}
.outl .f{position:relative}
.lbl{display:inline}
.land .lbl{display:block}
.ans .f{color:var(--tulsi)} .white .f{color:var(--paper)} .gold .f{color:var(--marigold)}
.ask{display:flex;align-items:center;gap:20px}
.land .ask{flex-direction:column;gap:6px}
.port .askt{font-size:78px}
.land .askt{font-size:78px;max-width:550px}
.land .ask img{width:88px!important;height:88px!important}

.card{position:absolute;background:var(--paper);border:11px solid var(--sindoor);border-radius:6px;
  box-shadow:0 26px 60px rgba(0,0,0,.5);display:flex;align-items:center;justify-content:center;overflow:hidden;cursor:pointer}
.land .card{left:110px;top:150px;width:1120px;height:800px;border-width:14px}
.port .card{left:70px;top:470px;width:940px;height:620px}
.content{display:flex;flex-direction:column;align-items:center;justify-content:center;width:max-content;flex:none;transform-origin:center center}

.footer{position:absolute;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;--fs:1}
.land .footer{left:1280px;width:550px;top:598px;height:290px}
.port .footer{left:40px;width:1000px;top:1108px;height:176px}
.bottom{position:absolute;display:flex;align-items:center;justify-content:center;gap:16px;font-weight:700;font-size:21px;letter-spacing:5px;color:rgba(255,224,130,.88);white-space:nowrap}
.bottom img{width:62px;height:62px}
.land .bottom{left:110px;width:1120px;top:976px}
.port .bottom{left:0;width:1080px;top:1486px}

/* card content (shared with the printable cards) */
.row{display:flex;align-items:center;justify-content:center}
.col{display:flex;flex-direction:column;align-items:center;justify-content:center}
.w{line-height:1.08;letter-spacing:-1px;white-space:nowrap}
.t3{font-family:var(--f-body);font-weight:900;line-height:1;white-space:nowrap;letter-spacing:-2px;padding:0 18px 22px 0}
.emo{display:block;filter:drop-shadow(0 12px 10px rgba(0,0,0,.16))}
.lrow{display:flex;font-weight:800;line-height:1.12;color:var(--ink)}
.lrow span{display:inline-block;text-align:center}
.cap{font-weight:800;font-size:44px;color:var(--sindoor);letter-spacing:2px;white-space:nowrap}
.split{position:relative;width:880px;height:330px}
.half{position:absolute;left:50%;top:50%;font-weight:900;font-size:184px;line-height:1;color:var(--ink);white-space:nowrap;letter-spacing:-3px}
.half.top{-webkit-clip-path:inset(0 0 51% 0);clip-path:inset(0 0 51% 0);transform:translate(calc(-50% - 20px),calc(-50% - 14px))}
.half.bot{-webkit-clip-path:inset(49% 0 0 0);clip-path:inset(49% 0 0 0);transform:translate(calc(-50% + 20px),calc(-50% + 14px))}
.blank{display:inline-block;width:104px;height:17px;background:var(--ink);border-radius:9px;margin-bottom:20px}
.mk{font-weight:900;font-size:150px;line-height:1;color:var(--ink)}
.bubble{position:relative;background:var(--cream);border:9px solid var(--ink);border-radius:70px;padding:34px 72px 30px;font-weight:900;font-size:104px;
  line-height:1.04;color:var(--ink);text-align:center;letter-spacing:-1px;white-space:nowrap}
.bubble::after{content:'';position:absolute;left:120px;bottom:-44px;width:70px;height:70px;background:var(--cream);border-right:9px solid var(--ink);
  border-bottom:9px solid var(--ink);transform:rotate(45deg) skew(14deg,14deg)}
.gv{font-family:var(--f-cond);font-size:70px;line-height:1.14;color:var(--ink);padding:0 6px;letter-spacing:1px}
.orb{position:absolute;font-weight:900;font-size:88px;line-height:1;color:var(--ink)}
.strike{position:relative;font-weight:900;font-size:124px;line-height:1;color:var(--ink);letter-spacing:-1px;white-space:nowrap}
.strike::after{content:'';position:absolute;left:-26px;right:-26px;top:52%;height:15px;margin-top:-7px;background:var(--sindoor);border-radius:8px;transform:rotate(-3deg);opacity:.95}
.howto{display:flex;flex-direction:column;gap:16px;padding:0 10px}
.howto .it{display:flex;align-items:center;gap:22px;font-weight:600;font-size:33px;color:#222;white-space:nowrap}
.howto .it b{font-weight:800;color:var(--ink)}
.howto img{width:66px;height:66px}
.big{font-weight:900;color:var(--ink);text-align:center;letter-spacing:-1px}
/* welcome card */
.wl{display:flex;align-items:center;gap:30px}
.wl-god{width:410px;height:506px;flex:none;cursor:pointer;-webkit-tap-highlight-color:transparent}
.wl-god svg{width:100%;height:100%;display:block;overflow:visible}
.wl-txt{display:flex;flex-direction:column;align-items:center;white-space:nowrap}
.wl-a{font-size:50px;line-height:1.2}
.wl-b{font-size:96px;line-height:1.04}
.wl-deva{font-family:var(--f-deva);font-weight:800;font-size:60px;line-height:1.25;color:#B3261E;margin-top:6px}
.wl-div{display:flex;align-items:center;gap:18px;margin:16px 0 10px;align-self:stretch}
.wl-div::before,.wl-div::after{content:"";flex:1;height:4px;border-radius:2px;background:linear-gradient(90deg,rgba(255,143,31,0),#FF8F1F)}
.wl-div::after{background:linear-gradient(90deg,#FF8F1F,rgba(255,143,31,0))}
.wl-c{font-size:88px;line-height:1.08;color:var(--sindoor)}
.wl-tap{display:flex;align-items:center;gap:10px;margin-top:30px;font-weight:600;font-size:28px;color:#6b6b6b;cursor:pointer}
.sub{font-weight:600;color:#444;text-align:center}
.chips{display:flex;gap:12px;justify-content:center}
.chip{font-weight:800;font-size:30px;padding:9px 24px;border-radius:999px;color:var(--paper);white-space:nowrap}
.lb{display:flex;flex-direction:column;gap:14px;min-width:640px}
.lbt{font-family:var(--f-display);font-size:64px;color:var(--sindoor);text-align:center;margin-bottom:6px}
.lbr{display:flex;align-items:center;gap:22px;font-weight:800;font-size:50px;color:var(--ink);padding:6px 18px;border-radius:18px}
.lbr:first-of-type{background:#FFF4DA}
.lbr .nm{flex:1;white-space:nowrap}
.lbr .sc{font-variant-numeric:tabular-nums;color:#7a1016}
.lbr img{width:70px;height:70px}
.lbr .rk{width:70px;text-align:center;color:#999}

/* footer text */
.deva{text-wrap:balance;font-family:var(--f-deva);font-weight:800;font-size:calc(var(--fs) * 56px);line-height:1.12;color:var(--marigold);text-shadow:0 4px 0 #5a1a00,0 8px 18px rgba(0,0,0,.45)}
.trick{text-wrap:balance;font-family:var(--f-display);font-size:calc(var(--fs) * 46px);color:var(--marigold);letter-spacing:1px;text-shadow:0 4px 0 #5a1a00,0 8px 18px rgba(0,0,0,.45)}
.exp{text-wrap:balance;margin-top:8px;font-weight:600;font-size:calc(var(--fs) * 31px);line-height:1.42;max-width:980px;text-shadow:0 2px 8px rgba(0,0,0,.55)}
.exp b{font-weight:800;color:var(--marigold-soft)}
.ie{height:1.42em;width:1.42em;vertical-align:-.32em;margin:0 2px}
.tipsh{font-weight:700;font-size:21px;letter-spacing:5px;color:rgba(255,224,130,.9);text-transform:uppercase;margin-bottom:12px}
.tips{display:flex;flex-wrap:wrap;gap:10px;justify-content:center}
.tip{display:flex;align-items:center;gap:8px;font-weight:700;font-size:24px;color:var(--paper);background:rgba(0,0,0,.28);
  border:2px solid var(--line);padding:7px 16px 7px 9px;border-radius:999px;white-space:nowrap}
.tip img{width:40px;height:40px}
.hintbox{display:flex;align-items:center;gap:20px;text-align:left;background:rgba(0,0,0,.32);border:3px solid var(--marigold);border-radius:26px;padding:18px 26px;max-width:100%}
.hintbox img{width:76px;height:76px;flex:none}
.hl{font-family:var(--f-display);font-size:34px;color:var(--marigold);letter-spacing:1px}
.ht{font-weight:700;font-size:36px;line-height:1.25;color:var(--paper)}

/* controls on the stage */
.dock{position:absolute;display:flex;flex-direction:column;gap:14px}
.land .dock{left:1280px;width:550px;top:902px}
.port .dock{left:140px;width:800px;top:1300px}
.nav{display:flex;gap:14px;align-items:center}
.tools{display:flex;gap:12px}
.stage button{font-family:var(--f-body);cursor:pointer;touch-action:manipulation;-webkit-appearance:none;appearance:none}
.round{flex:none;width:92px;height:92px;border-radius:50%;background:rgba(255,255,255,.13);border:3px solid var(--line);display:flex;align-items:center;justify-content:center;padding:0}
.round svg{width:40px;height:40px}
.primary{flex:1;height:92px;border:0;border-radius:46px;background:var(--marigold);color:#5a1a00;font-weight:800;font-size:32px;letter-spacing:1.5px;
  text-transform:uppercase;box-shadow:0 7px 0 #a86a00;white-space:nowrap}
.primary.go{background:var(--tulsi);color:#0b3d0b;box-shadow:0 7px 0 #3a8a1f}
.tool{flex:1;height:62px;border-radius:31px;background:rgba(0,0,0,.28);border:2px solid var(--line);color:var(--paper);font-weight:700;font-size:24px;
  display:flex;align-items:center;justify-content:center;gap:8px;white-space:nowrap;padding:0 10px}
.tool img{width:36px;height:36px}
.tool.on{background:var(--marigold);color:#5a1a00;border-color:var(--marigold)}
.stage button:disabled{opacity:.35;cursor:default}
.stage button:focus-visible{outline:5px solid var(--paper);outline-offset:4px}
.stage button:active:not(:disabled){transform:translateY(3px)}

/* entrance + reveal motion */
@keyframes rise{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}
@keyframes pop{0%{opacity:0;transform:scale(.55) rotate(-4deg)}60%{opacity:1;transform:scale(1.08) rotate(1deg)}100%{transform:none}}
@keyframes cardin{from{opacity:.0;transform:translateX(var(--dx,40px))}to{opacity:1;transform:none}}
.in-card{animation:cardin .32s cubic-bezier(.2,.8,.2,1)}
.in-rise{animation:rise .36s cubic-bezier(.2,.8,.2,1)}
.in-pop .outl{animation:pop .5s cubic-bezier(.2,.9,.3,1.2)}
@media (prefers-reduced-motion: reduce){.in-card,.in-rise,.in-pop .outl{animation:none}}

/* overlays (real screen size, outside the stage) */
.sheet{position:fixed;left:0;top:0;right:0;bottom:0;z-index:50;display:flex;align-items:center;justify-content:center;
  background:var(--veil);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);
  padding:calc(env(safe-area-inset-top, 0px) + 12px) max(16px, env(safe-area-inset-right, 0px)) calc(env(safe-area-inset-bottom, 0px) + 12px) max(16px, env(safe-area-inset-left, 0px));
  touch-action:pan-y;-webkit-user-select:text;user-select:text}
.panel{width:min(760px,100%);max-height:100%;overflow:auto;-webkit-overflow-scrolling:touch;background:var(--panel);border:2px solid var(--line);border-radius:20px;
  padding:14px 18px 18px;box-shadow:0 20px 50px rgba(0,0,0,.5)}
.ph{display:flex;align-items:center;gap:12px;margin-bottom:8px}
.ph h2{flex:1;margin:0;font-family:var(--f-display);font-weight:400;font-size:28px;color:var(--marigold);letter-spacing:1px}
.x{width:44px;height:44px;border-radius:50%;border:2px solid var(--line);background:transparent;color:var(--paper);font-size:22px;line-height:1;cursor:pointer}
.sec{font-weight:700;font-size:12px;letter-spacing:3px;text-transform:uppercase;color:var(--wheat);opacity:.85;margin:12px 0 6px}
.tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(58px,1fr));gap:8px}
.tile{position:relative;height:50px;border-radius:12px;border:2px solid rgba(255,255,255,.18);background:rgba(255,255,255,.08);color:var(--paper);
  font:700 16px/1 var(--f-body);cursor:pointer;padding:0 6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.tile.wide{grid-column:span 2}
.tile.easy{border-color:#66bb6a}.tile.medium{border-color:#ffa040}.tile.hard{border-color:#ef6b6b}
.tile.done::after{content:'✓';position:absolute;right:5px;top:3px;font-size:12px;color:var(--tulsi)}
.tile.cur{background:var(--marigold);color:#5a1a00;border-color:var(--marigold)}
.prow{display:flex;align-items:center;gap:8px;padding:8px 0;border-bottom:1px solid rgba(255,255,255,.1)}
.prow .pn{flex:1;min-width:0;font:700 17px var(--f-body);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.prow .ps{width:44px;text-align:center;font:800 22px var(--f-body);font-variant-numeric:tabular-nums;color:var(--marigold)}
.sbtn{width:44px;height:44px;border-radius:12px;border:2px solid var(--line);background:rgba(255,255,255,.08);color:var(--paper);font:800 22px/1 var(--f-body);cursor:pointer}
.sbtn.plus{background:var(--marigold);color:#5a1a00;border-color:var(--marigold)}
.sbtn.rm{border-color:rgba(255,255,255,.2);font-size:18px;color:var(--wheat)}
.addrow{display:flex;gap:8px;margin-top:12px}
.addrow input{flex:1;min-width:0;height:46px;border-radius:12px;border:2px solid var(--line);background:rgba(0,0,0,.25);color:var(--paper);font:600 16px var(--f-body);padding:0 12px;-webkit-user-select:text;user-select:text}
.wbtn{height:46px;border-radius:12px;border:0;background:var(--marigold);color:#5a1a00;font:800 15px var(--f-body);padding:0 16px;cursor:pointer;text-transform:uppercase;letter-spacing:1px;white-space:nowrap}
.wbtn.ghost{background:transparent;border:2px solid var(--line);color:var(--paper)}
.foot{display:flex;gap:8px;justify-content:space-between;align-items:center;margin-top:14px;flex-wrap:wrap}
.empty{font:500 15px/1.5 var(--f-body);color:var(--wheat);opacity:.9;padding:8px 0}
.note{font:500 13px/1.45 var(--f-body);color:var(--wheat);opacity:.8;margin:10px 0 0}
.sheet button:focus-visible,.sheet input:focus-visible{outline:3px solid var(--paper);outline-offset:2px}

/* right / wrong buttons */
.judge{flex:1;height:92px;border:0;border-radius:46px;font-weight:800;font-size:30px;letter-spacing:1.5px;text-transform:uppercase;
  display:flex;align-items:center;justify-content:center;gap:10px;white-space:nowrap;padding:0 14px}
.judge svg{width:34px;height:34px;flex:none}
.judge.no{background:#E53935;color:#fff;box-shadow:0 7px 0 #8E1B1B}
.judge.yes{background:var(--tulsi);color:#0b3d0b;box-shadow:0 7px 0 #3a8a1f}
.tool{font-size:22px;gap:6px;padding:0 6px}
.tool img{width:32px;height:32px}

/* blessing */
.bless{position:absolute;z-index:20;border-radius:14px;overflow:hidden;cursor:pointer;display:flex;flex-direction:column;align-items:center;
  background:radial-gradient(70% 70% at 30% 55%, rgba(255,214,102,.30), rgba(255,214,102,0) 65%), linear-gradient(160deg,#7d1520,#35060b);
  border:6px solid var(--marigold);box-shadow:0 26px 60px rgba(0,0,0,.55)}
.land .bless{left:96px;top:136px;width:1148px;height:828px}
.port .bless{left:52px;top:452px;width:976px;height:656px}
.bl-banner{position:relative;z-index:2;margin-top:16px}
.bl-banner .outl{white-space:nowrap}
.land .bl-banner .outl{font-size:104px}
.port .bl-banner .outl{font-size:72px}
.bl-body{position:relative;z-index:2;flex:1;width:100%;display:flex;align-items:center;justify-content:center;gap:6px;padding:0 44px 34px}
.bl-god{flex:none}
.land .bl-god{width:470px;height:580px}
.port .bl-god{width:350px;height:432px}
.bl-god svg{width:100%;height:100%;display:block;overflow:visible}
.bl-bubble{position:relative;flex:1;max-width:680px;background:var(--paper);color:var(--ink);border-radius:36px;padding:32px 38px;box-shadow:0 14px 30px rgba(0,0,0,.35)}
.bl-bubble::before{content:'';position:absolute;left:-30px;top:38%;border-style:solid;border-width:22px 34px 22px 0;border-color:transparent var(--paper) transparent transparent}
.bl-bubble{--bf:1}
.bl-open{font-weight:800;color:#C2410C;line-height:1.25;margin-bottom:12px;text-wrap:balance}
.bl-open.hi{font-family:var(--f-deva);line-height:1.36}
.land .bl-open{font-size:calc(var(--bf) * 36px)}
.port .bl-open{font-size:calc(var(--bf) * 26px)}
.bl-text{font-weight:800;line-height:1.24;text-wrap:balance}
.land .bl-text{font-size:calc(var(--bf) * 42px)}
.port .bl-text{font-size:calc(var(--bf) * 30px)}
.bl-text.hi{font-family:var(--f-deva);line-height:1.38}
.bl-en{font-weight:600;color:#6b5b57;line-height:1.3;margin-top:8px}
.land .bl-en{font-size:calc(var(--bf) * 24px)}
.port .bl-en{font-size:calc(var(--bf) * 18px)}
.bl-tath{font-family:var(--f-display);color:#E65100;letter-spacing:1px;margin-top:14px}
.bl-tath.hi{font-family:var(--f-deva);font-weight:800;letter-spacing:0}
.land .bl-tath{font-size:calc(var(--bf) * 46px)}
.port .bl-tath{font-size:calc(var(--bf) * 34px)}
.bl-pts{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}
.bl-pts:empty{display:none}
.bl-ptl{width:100%;font-weight:700;font-size:calc(var(--bf) * 22px);letter-spacing:3px;text-transform:uppercase;color:#7a1016}
.bl-chip{font:800 calc(var(--bf) * 26px) var(--f-body);padding:9px 20px;border-radius:999px;border:3px solid var(--sindoor);background:var(--paper);color:#7a1016;cursor:pointer}
.bl-chip.got{background:var(--tulsi);border-color:#3a8a1f;color:#0b3d0b}
.bl-close{position:absolute;right:24px;bottom:14px;z-index:2;font-weight:700;font-size:21px;letter-spacing:3px;text-transform:uppercase;color:rgba(255,224,130,.75)}
.petals{position:absolute;left:0;top:0;width:100%;height:100%;pointer-events:none;z-index:1}
.petal{position:absolute;top:-60px;width:34px;height:20px;border-radius:50%;background:radial-gradient(circle at 30% 30%,#FFD54F,#FF8F1F 70%);
  animation-name:fall;animation-timing-function:linear;animation-fill-mode:forwards}
@keyframes fall{to{transform:translate(var(--sx),920px) rotate(var(--rot))}}
.bhag .float{animation:float 3s ease-in-out infinite alternate}
.bhag .chakra{transform-box:fill-box;transform-origin:center;animation:spin 3s linear infinite}
.bhag .glow{transform-box:fill-box;transform-origin:center;animation:glow 1.3s ease-in-out infinite alternate}
.bhag .halo{transform-box:fill-box;transform-origin:center;animation:spin 40s linear infinite}
@keyframes float{from{transform:translateY(6px)}to{transform:translateY(-8px)}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes glow{from{opacity:.55;transform:scale(.9)}to{opacity:1;transform:scale(1.12)}}
/* lip sync: the app puts the mouth shape being spoken in data-m (X rest, A-H talking) */
.bhag[data-m]:not([data-m="X"]) .mX{display:none}
.bhag[data-m="A"] .mA,.bhag[data-m="B"] .mB,.bhag[data-m="C"] .mC,.bhag[data-m="D"] .mD,
.bhag[data-m="E"] .mE,.bhag[data-m="F"] .mF,.bhag[data-m="G"] .mG,.bhag[data-m="H"] .mH{display:inline}
.bhag .eyes{transform-box:fill-box;transform-origin:center;animation:blink 4.8s infinite}
@keyframes blink{0%,93%,100%{transform:none}95.5%{transform:scaleY(.1)}}
@keyframes blessin{from{opacity:0;transform:scale(.86)}to{opacity:1;transform:none}}
.bless.in{animation:blessin .45s cubic-bezier(.2,.9,.3,1.2)}

/* wrong answer: Bhagwan shakes his head and his chakra stops */
.bless.oops{border-color:#FF6B6B;background:radial-gradient(70% 70% at 30% 55%, rgba(255,107,107,.20), rgba(255,107,107,0) 65%), linear-gradient(160deg,#5c0d16,#29050a)}
.oops .bhag .chakra{animation-play-state:paused}
.oops .bhag .float{transform-box:fill-box;transform-origin:50% 85%;animation:tsk 1.2s ease-in-out infinite}
@keyframes tsk{0%,100%{transform:rotate(0)}25%{transform:rotate(-3.5deg)}75%{transform:rotate(3.5deg)}}
.red .f{color:#FF4D4D}
.card.shake{animation:shake .5s}
@keyframes shake{10%,90%{transform:translateX(-6px)}20%,80%{transform:translateX(10px)}30%,50%,70%{transform:translateX(-16px)}40%,60%{transform:translateX(16px)}}
@media (prefers-reduced-motion: reduce){.bhag *,.bless.in,.card.shake,.petal{animation:none!important}}

/* sound settings in the menu */
.setrow{display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid rgba(255,255,255,.1)}
.setrow .sl{flex:1;min-width:0;font:700 16px var(--f-body)}
.tog{min-width:68px;height:40px;border-radius:20px;border:2px solid var(--line);background:rgba(255,255,255,.08);color:var(--paper);font:800 14px var(--f-body);cursor:pointer;text-transform:uppercase;letter-spacing:1px}
.tog[aria-pressed="true"]{background:var(--tulsi);color:#0b3d0b;border-color:var(--tulsi)}
.seg{display:flex;gap:6px}
.seg .tog{text-transform:none;letter-spacing:0;font-size:15px;padding:0 12px}
#voiceSel{flex:0 1 58%;min-width:0;height:42px;border-radius:12px;border:2px solid var(--line);background:#2a0609;color:var(--paper);font:600 16px var(--f-body);padding:0 8px}
"""

CHEV_L = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 4 7 12l8 8" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CHEV_R = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m9 4 8 8-8 8" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ICON_X = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18" fill="none" stroke="currentColor" stroke-width="3.6" stroke-linecap="round"/></svg>'
ICON_TICK = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m4.5 12.5 5 5 10-11" fill="none" stroke="currentColor" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'

JS = r"""
(function(){
const SL = __SLIDES__, ASK = __ASK__, TIPS = __TIPS__, END_DEFAULT = __END__, BLESSINGS = __BLESSINGS__, WRONGS = __WRONGS__;
const KEY = __KEY__;
const app = document.getElementById('app'), st = document.getElementById('stage');
const $ = id => document.getElementById(id);
const E = {pills:$('pills'), prompt:$('prompt'), card:$('card'), content:$('content'), footer:$('footer'),
  bottomText:$('bottomText'), main:$('mainBtn'), prev:$('prevBtn'), next:$('nextBtn'), hint:$('hintBtn'),
  wrong:$('wrongBtn'), right:$('rightBtn'), ans:$('ansBtn'), ansLbl:$('ansLbl'), bless:$('bless'), oops:$('oops')};
let S = {i:0, seen:{}, players:[], sfx:true, voice:true, lang:'hi', voiceName:''};
let revealed = false;  // answers always start hidden; only the ✓ marks are remembered
let hintOn = false;
const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

function load(){ try { const d = JSON.parse(localStorage.getItem(KEY) || 'null'); if (d && typeof d === 'object') adopt(d); } catch(e) {} }
function adopt(d){
  if (Number.isInteger(d.i) && d.i >= 0 && d.i < SL.length) S.i = d.i;
  const seen = d.seen || d.rev;
  if (seen && typeof seen === 'object') S.seen = seen;
  if (Array.isArray(d.players)) S.players = d.players.filter(p => p && typeof p.n === 'string').map(p => ({n:p.n.slice(0,24), s:Number(p.s)||0}));
  if (typeof d.sfx === 'boolean') S.sfx = d.sfx;
  if (typeof d.voice === 'boolean') S.voice = d.voice;
  if (d.lang === 'hi' || d.lang === 'en') S.lang = d.lang;
  if (typeof d.voiceName === 'string') S.voiceName = d.voiceName.slice(0, 120);
  if (d.decks && typeof d.decks === 'object') S.decks = d.decks;
  if (Number.isInteger(d.qCount)) S.qCount = d.qCount;
  if (typeof d.qLast === 'string') S.qLast = d.qLast;
  if (Number.isInteger(d.nameQ)) S.nameQ = d.nameQ;
  const at =typeof d.at === 'string' ? SL.findIndex(s => s.id === d.at) : -1;  // by name, so new slides don't shift it
  if (at >= 0) S.i = at;
}
function save(){ try { localStorage.setItem(KEY, JSON.stringify(S)); } catch(e) {} }

function isLand(){ return st.classList.contains('land'); }

function layout(){
  const W = app.clientWidth, H = app.clientHeight;
  if (!W || !H) return;
  const land = W >= H * 1.02;
  st.classList.toggle('land', land); st.classList.toggle('port', !land);
  const sw = land ? 1920 : 1080, sh = land ? 1080 : 1560;
  const s = Math.min(W / sw, H / sh);
  st.style.transform = 'translate(' + ((W - sw * s) / 2) + 'px,' + ((H - sh * s) / 2) + 'px) scale(' + s + ')';
  fit();
}

function fit(){
  const land = isLand();
  const c = E.content;
  c.style.transform = 'none';
  const cw = E.card.clientWidth, ch = E.card.clientHeight;
  const w = c.offsetWidth, h = c.offsetHeight;
  if (w && h) {
    const pad = land ? 70 : 60, cap = land ? 1.32 : 1;
    const s = Math.min(cap, (cw - pad) / w, (ch - pad) / h);
    c.style.transform = 'scale(' + s + ')';
  }
  const pw = E.prompt.clientWidth, ph = E.prompt.clientHeight;
  E.prompt.querySelectorAll('[data-fit]').forEach(el => {
    let fs = land ? 132 : (+el.dataset.size || 110);
    el.style.fontSize = fs + 'px';
    while ((el.offsetWidth > pw || el.offsetHeight > ph) && fs > 24) { fs -= 3; el.style.fontSize = fs + 'px'; }
  });
  const f = E.footer;
  let k = 1; f.style.setProperty('--fs', k);
  while (f.scrollHeight > f.clientHeight + 1 && k > 0.55) { k = Math.round((k - 0.05) * 100) / 100; f.style.setProperty('--fs', k); }
}

function endBody(){
  const ps = S.players.filter(p => p.n.trim());
  if (!ps.length) return END_DEFAULT;
  const sorted = ps.map((p, i) => ({...p, i})).sort((a, b) => b.s - a.s || a.i - b.i).slice(0, 6);
  const medal = ['1f947', '1f948', '1f949'];
  const rows = sorted.map((p, r) => '<div class="lbr">' + (r < 3 ? '<img alt="" src="assets/' + medal[r] + '.webp">' : '<span class="rk">' + (r + 1) + '</span>')
    + '<span class="nm">' + esc(p.n) + '</span><span class="sc">' + p.s + '</span></div>').join('');
  return '<div class="lb"><div class="lbt">Puzzle champions</div>' + rows + '</div>';
}

function hintBox(t){
  return '<div class="hintbox"><img alt="" src="assets/1f4a1.webp"><div><div class="hl">Hint</div><div class="ht">' + t + '</div></div></div>';
}

function anim(el, cls){ el.classList.remove(cls); void el.offsetWidth; el.classList.add(cls); }

function render(mode){
  const s = SL[S.i];
  const puzzle = s.kind === 'puzzle';
  const shown = puzzle && revealed;
  E.pills.innerHTML = s.pills.map(p => '<div class="pill ' + p[0] + '">' + p[1] + '</div>').join('');
  E.prompt.innerHTML = puzzle ? (shown ? s.aPrompt : ASK) : s.prompt;
  if (mode !== 'reveal') E.content.innerHTML = s.id === 'end' ? endBody() : s.body;
  E.footer.innerHTML = puzzle ? (shown ? s.aFooter : (hintOn && s.hint ? hintBox(s.hint) : TIPS)) : s.footer;
  E.bottomText.textContent = s.bottom;
  // buttons
  const judging = puzzle && !shown;
  E.wrong.hidden = !judging; E.right.hidden = !judging; E.main.hidden = judging;
  E.ans.disabled = !puzzle; E.ansLbl.textContent = shown ? 'Hide' : 'Answer';
  let label, go = false;
  if (puzzle) { label = 'Next'; go = true; }
  else if (s.id === 'welcome') { label = "Let's begin"; go = true; }
  else if (s.id === 'howto') { label = 'Start warm-ups'; go = true; }
  else if (s.id === 'round2') { label = 'Start the quiz'; go = true; }
  else { label = 'Back to start'; }
  E.main.textContent = label; E.main.classList.toggle('go', go);
  E.prev.disabled = S.i === 0; E.next.disabled = S.i === SL.length - 1;
  E.hint.disabled = !(puzzle && !shown && s.hint);
  E.hint.classList.toggle('on', hintOn && !E.hint.disabled);
  E.hint.setAttribute('aria-pressed', String(hintOn && !E.hint.disabled));
  fit();
  S.at = s.id;
  if (mode === 'reveal') { anim(E.prompt, 'in-pop'); anim(E.footer, 'in-rise'); }
  else if (mode === 'hint') { anim(E.footer, 'in-rise'); }
  else if (mode) { E.card.style.setProperty('--dx', mode === 'back' ? '-40px' : '40px'); anim(E.card, 'in-card'); anim(E.prompt, 'in-rise'); anim(E.footer, 'in-rise'); }
  save();
}

function go(i, dir){ i = Math.max(0, Math.min(SL.length - 1, i)); if (i === S.i) return; if (SL[S.i].id === 'welcome') hush(); closeFx(); hintOn = false; revealed = false; S.i = i; render(dir || 'fwd'); }
function next(){ go(S.i + 1, 'fwd'); }
function prev(){ go(S.i - 1, 'back'); }
function toggle(){ const s = SL[S.i]; if (s.kind !== 'puzzle') return; closeFx(); revealed = !revealed; if (revealed) S.seen[s.id] = 1; hintOn = false; render(revealed ? 'reveal' : 'hint'); }
function reveal(bless){ const s = SL[S.i]; revealed = true; S.seen[s.id] = 1; hintOn = false; render('reveal'); if (bless) showBlessing(); }
function judgeRight(){ if (SL[S.i].kind !== 'puzzle' || revealed) return; newQuestion(); hideWrong(); reveal(true); }
function judgeWrong(){ if (SL[S.i].kind !== 'puzzle' || revealed) return; newQuestion(); showWrong(); }
function primary(){
  const s = SL[S.i];
  if (s.kind === 'puzzle' && !revealed) reveal(false);
  else if (s.id === 'end') go(0, 'back');
  else next();
}
function toggleHint(){ if (E.hint.disabled) return; hintOn = !hintOn; render('hint'); }

E.main.addEventListener('click', primary);
E.next.addEventListener('click', next);
E.prev.addEventListener('click', prev);
E.hint.addEventListener('click', toggleHint);
E.right.addEventListener('click', judgeRight);
E.wrong.addEventListener('click', judgeWrong);
E.ans.addEventListener('click', toggle);
$('scoreBtn').addEventListener('click', () => openSheet('scores'));
$('gridBtn').addEventListener('click', () => openSheet('grid'));

// swipe anywhere, tap the card to flip
let p0 = null;
app.addEventListener('pointerdown', e => { wake(); unlock(); if (e.target.closest('button')) { p0 = null; return; } p0 = {x:e.clientX, y:e.clientY}; });
app.addEventListener('pointercancel', () => { p0 = null; });
app.addEventListener('pointerup', e => {
  if (!p0) return;
  const dx = e.clientX - p0.x, dy = e.clientY - p0.y; p0 = null;
  if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.2) { dx < 0 ? next() : prev(); return; }
  if (Math.abs(dx) < 14 && Math.abs(dy) < 14) {
    if (e.target.closest('[data-welcome]')) welcome();
    else if (e.target.closest('.card')) toggle();
  }
});
document.addEventListener('keydown', e => {
  if (e.target.closest && e.target.closest('input')) return;
  if (sheetOpen()) { if (e.key === 'Escape') closeSheets(); return; }
  if (e.key === 'Escape') { closeFx(); return; }
  if (e.key === 'r' || e.key === 'R') { judgeRight(); return; }
  if (e.key === 'w' || e.key === 'W') { judgeWrong(); return; }
  if (e.key === 'ArrowRight' || e.key === 'PageDown') { e.preventDefault(); next(); }
  else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); prev(); }
  else if (e.key === ' ' || e.key === 'Enter') { if (e.target.closest && e.target.closest('button')) return; e.preventDefault(); primary(); }
  else if (e.key === 'h' || e.key === 'H') toggleHint();
});

// keep the screen on while presenting, where the phone allows it
let lock = null;
async function wake(){ try { if (!lock && navigator.wakeLock && document.visibilityState === 'visible') { lock = await navigator.wakeLock.request('screen'); lock.addEventListener('release', () => { lock = null; }); } } catch(e) { lock = null; } }
document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible') wake(); });

// ---------------- sound: bell and buzzer from Web Audio, blessings from the phone's own voice
let actx = null, unlocked = false, voices = [];
function ctx(){
  try {
    if (!actx) { const C = window.AudioContext || window.webkitAudioContext; if (!C) return null; actx = new C(); }
    if (actx.state === 'suspended') actx.resume();
    return actx;
  } catch(e) { return null; }
}
function audio(){ return S.sfx ? ctx() : null; }
function unlock(){
  if (unlocked) return; unlocked = true;
  try { if (navigator.audioSession) navigator.audioSession.type = 'playback'; } catch(e) {}
  ctx();
  try { if ('speechSynthesis' in window) { const u = new SpeechSynthesisUtterance(' '); u.volume = 0; speechSynthesis.speak(u); } } catch(e) {}
  setTimeout(preloadClips, 300);
}
function tone(ctx, f, t0, dur, gain, type, dest){
  const o = ctx.createOscillator(), g = ctx.createGain();
  o.type = type || 'sine'; o.frequency.setValueAtTime(f, t0);
  g.gain.setValueAtTime(0.0001, t0); g.gain.exponentialRampToValueAtTime(gain, t0 + 0.012); g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
  o.connect(g); g.connect(dest || ctx.destination); o.start(t0); o.stop(t0 + dur + 0.05);
}
function chime(){
  const ctx = audio(); if (!ctx) return;
  const t = ctx.currentTime + 0.02;
  [[0, 660], [0.34, 990]].forEach(([dt, f]) =>
    [[1, .3, 2.4], [2.76, .13, 1.6], [5.4, .06, 1.0], [8.9, .03, .6]].forEach(([m, g, d]) => tone(ctx, f * m, t + dt, d, g)));
}
function buzz(){
  const ctx = audio(); if (!ctx) return;
  const t = ctx.currentTime + 0.02, lp = ctx.createBiquadFilter();
  lp.type = 'lowpass'; lp.frequency.value = 900; lp.connect(ctx.destination);
  tone(ctx, 233, t, 0.22, 0.28, 'sawtooth', lp); tone(ctx, 175, t + 0.24, 0.32, 0.28, 'sawtooth', lp);
}
// Apple's joke voices (Albert, Zarvox...) and the old Eloquence voices sound robotic, so never pick them.
const NOVELTY = /\b(albert|bad news|bahh|bells|boing|bubbles|cellos|deranged|good news|hysterical|jester|junior|organ|princess|ralph|superstar|trinoids|whisper|wobble|zarvox|fred|kathy|eddy|flo|grandma|grandpa|reed|rocko|sandy|shelley)\b/i;
function loadVoices(){
  try { voices = window.speechSynthesis ? (speechSynthesis.getVoices() || []) : []; } catch(e) { voices = []; }
  if (!$('gridSheet').hidden) drawVoices();
}
if ('speechSynthesis' in window) { loadVoices(); try { speechSynthesis.addEventListener('voiceschanged', loadVoices); } catch(e) { speechSynthesis.onvoiceschanged = loadVoices; } }
function usable(){ return voices.filter(v => !NOVELTY.test(v.name)); }
// The phone's own voice should match the cartoon: male or female voices rank first.
const MALE = /\b(rishi|ravi|prabhat|hemant|madhur|aaron|alex|arthur|daniel|gordon|lee|oliver|tom|thomas|male)\b/i;
const FEMALE = /\b(lekha|veena|isha|kalpana|neerja|swara|aditi|priya|samantha|karen|moira|tessa|fiona|kate|serena|victoria|allison|ava|susan|zoe|female)\b/i;
const PREFER = __PREFER__ === 'f' ? FEMALE : MALE;
function rank(v){ let s = 0; if (PREFER.test(v.name)) s += 6; if (/enhanced|premium|neural|natural|siri/i.test(v.name)) s += 3; if (/google/i.test(v.name)) s += 2; if (v.localService === false) s += 1; return s; }
function best(re){ const l = usable().filter(v => re.test(v.lang)); l.sort((a, b) => rank(b) - rank(a)); return l[0] || null; }
const HI = /^hi([-_]|$)/i, EN_IN = /^en[-_]IN/i;
function voiceFor(){
  if (S.voiceName) { const c = voices.find(v => v.name === S.voiceName); if (c) return c; }
  if (S.lang === 'hi') { const h = best(HI); if (h) return h; }
  return best(EN_IN) || best(/^en[-_](GB|AU|US|IE|ZA)/i) || best(/^en/i) || null;
}
// Built-in natural Hindi voices: every line is pre-recorded, so it sounds the same on every phone.
const NATURAL = __NATURAL__, NAT_DEFAULT = Object.keys(NATURAL)[0];
function naturalVoice(){
  if (S.lang !== 'hi') return null;
  if (!S.voiceName) return NAT_DEFAULT;
  const m = /^natural:(\w+)$/.exec(S.voiceName);
  return m && NATURAL[m[1]] ? m[1] : null;
}
const clips = {};
function clip(key, nat){
  const url = 'assets/v-' + nat + '-' + key + '.mp3';
  if (!clips[url]) {
    const c = ctx(); if (!c) return Promise.resolve(null);
    clips[url] = fetch(url).then(r => { if (!r.ok) throw new Error(r.status); return r.arrayBuffer(); })
      .then(b => new Promise((res, rej) => c.decodeAudioData(b, res, rej)))
      .catch(() => { delete clips[url]; return null; });
  }
  return clips[url];
}
function preloadClips(){
  const nat = naturalVoice(); if (!nat) return;
  const keys = (list, p) => list.map((x, i) => x.key || p + String(i + 1).padStart(2, '0'));  // a re-worded line gets a new key
  [WELCOME.key, 'tath', 'sample', 'test'].concat(keys(WRONGS, 'w'), keys(BLESSINGS, 'b')).forEach(k => clip(k, nat));
}
let voiceSrc = null, sayId = 0;
function stopClip(){ try { if (voiceSrc) voiceSrc.stop(); } catch(e) {} voiceSrc = null; }
function estimate(hi, en){ return Math.max(2, ((naturalVoice() || S.lang === 'hi') ? hi : en).length * 0.075); }
function say(hi, en, key){
  if (!S.voice) return Promise.resolve(0);
  hush();
  const nat = naturalVoice(), id = ++sayId;
  if (nat && key) {
    return clip(key, nat).then(buf => {
      if (id !== sayId) return 0;
      const c = ctx();
      if (!buf || !c) { speak(hi, en); return estimate(hi, en); }
      const src = c.createBufferSource(), t0 = c.currentTime + 0.05;
      src.buffer = buf; src.connect(c.destination); src.start(t0); voiceSrc = src;
      src.onended = () => { if (voiceSrc === src) { voiceSrc = null; lipStop(); } };
      lipFollow(c, t0, buf, nat, key);
      return buf.duration;
    });
  }
  speak(hi, en);
  return Promise.resolve(estimate(hi, en));
}
function speak(hi, en){
  if (!('speechSynthesis' in window)) return;
  try {
    if (!voices.length) loadVoices();
    const v = voiceFor(), hindi = v ? HI.test(v.lang) : S.lang === 'hi';
    const text = hindi ? hi : en, u = new SpeechSynthesisUtterance(text);
    if (v) { u.voice = v; u.lang = v.lang; } else u.lang = hindi ? 'hi-IN' : 'en-IN';
    u.rate = hindi ? 0.92 : 0.95; u.pitch = 1; u.volume = 1;
    const id = sayId, est = Math.max(1.5, text.length * (hindi ? 0.075 : 0.065));
    u.onstart = () => { if (id === sayId) lipChatter(est, 0); };
    u.onend = u.onerror = () => { if (id === sayId) lipStop(); };
    speechSynthesis.speak(u);
    lipChatter(est, 0.3);  // in case the phone never reports that it started talking
  } catch(e) {}
}
function hush(){ sayId++; stopClip(); lipStop(); try { if ('speechSynthesis' in window) speechSynthesis.cancel(); } catch(e) {} }

// ---------------- lip sync: the cartoon's mouth follows the voice
// Timings come from Rhubarb Lip Sync, worked out once for every recorded line: "@<onset ms>|" and then each mouth
// shape with its start in hundredths of a second, e.g. "X0B10C24". X rest, A closed (m b p), B teeth together,
// C open, D wide open, E rounded, F puckered (oo), G teeth on lip (f v), H tongue up (l).
const LIPS = __LIPS__;
let lipRaf = 0, lipTimer = 0;
// every copy of the cartoon on the page (the two pop-ups and the welcome card) moves its lips together
function mouth(m){ document.querySelectorAll('svg.bhag').forEach(s => { if (s.getAttribute('data-m') !== m) s.setAttribute('data-m', m); }); }
const WELCOME = __WELCOME__, SOUND = __SOUND__;
function welcome(){ say(WELCOME.hi, WELCOME.en, WELCOME.key); }
function lipStop(){ cancelAnimationFrame(lipRaf); clearTimeout(lipTimer); lipRaf = 0; lipTimer = 0; mouth('X'); }
function lipCues(nat, key){
  const s = LIPS[nat] && LIPS[nat][key], m = s && /^@(\d+)\|(.+)$/.exec(s);
  if (!m) return null;
  const cues = []; m[2].replace(/([A-HX])(\d+)/g, (_, k, t) => { cues.push([t / 100, k]); return ''; });
  return cues.length ? {onset: m[1] / 1000, cues} : null;
}
// When the voice first gets loud in the clip as this phone decoded it. Some MP3 decoders add a few hundredths of a
// second of silence at the start; comparing onsets keeps the mouth on the words anyway.
function onsetOf(buf){
  if (buf._on === undefined) {
    const d = buf.getChannelData(0), n = Math.min(d.length, Math.round(buf.sampleRate * 0.6));
    let i = 0; while (i < n && Math.abs(d[i]) < 0.02) i++;
    buf._on = i < n ? i / buf.sampleRate : null;
  }
  return buf._on;
}
function lipFollow(c, t0, buf, nat, key){
  lipStop();
  const L = lipCues(nat, key);
  if (!L) { lipChatter(buf.duration, t0 - c.currentTime); return; }
  const on = onsetOf(buf), shift = on == null ? 0 : Math.max(-0.2, Math.min(0.2, on - L.onset));
  const wallEnd = performance.now() + (buf.duration + 2) * 1000;
  let i = 0;
  const step = () => {
    const t = c.currentTime - t0 - shift;
    if (t > buf.duration || performance.now() > wallEnd) { lipStop(); return; }
    while (i + 1 < L.cues.length && L.cues[i + 1][0] <= t) i++;
    mouth(t < L.cues[0][0] ? 'X' : L.cues[i][1]);
    lipRaf = requestAnimationFrame(step);
  };
  lipRaf = requestAnimationFrame(step);
}
// The phone's own voices give no timings, so while one talks the mouth just chatters through speech-like shapes.
const CHATTER = 'BCDBCEACFBDHCBGECBDA';
function lipChatter(dur, delay){
  lipStop();
  const end = performance.now() + (Math.max(0, delay || 0) + dur) * 1000;
  let k = Math.floor(Math.random() * CHATTER.length);
  const tick = () => {
    if (performance.now() > end) { lipStop(); return; }
    mouth(CHATTER[k++ % CHATTER.length]);
    lipTimer = setTimeout(tick, 85 + Math.random() * 75);
  };
  lipTimer = setTimeout(tick, Math.max(0, delay || 0) * 1000);
}

// keep words like हँस-हँस or Wi-Fi on one line
function setText(el, s){ el.innerHTML = esc(s).replace(/(\S+-\S+)/g, '<span style="white-space:nowrap">$1</span>'); }
function shuffle(a){ for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }
// Lines that name the hosts are spaced out: after one is spoken on a question, the hosts aren't named
// again on that question or the next 5 (blessings and wrong answers together).
const NAMED = __NAMED__;
const named = line => NAMED.test(JSON.stringify(line));
function newQuestion(){ const id = SL[S.i].id; if (S.qLast !== id) { S.qLast = id; S.qCount = (S.qCount || 0) + 1; } }
function namesOk(){ return !Number.isInteger(S.nameQ) || (S.qCount || 0) - S.nameQ > 5; }
// A shuffled deck per kind of line, remembered on the phone, so no line comes back until every other one has been used,
// even if the app is closed in between. When a new round starts, the last few lines heard go to the back of it.
function deal(name, list){
  const n = list.length;
  const decks = (S.decks && typeof S.decks === 'object') ? S.decks : {};
  let d = decks[name];
  if (!d || d.n !== n || !Array.isArray(d.q)) d = {n, q: [], recent: []};
  d.q = d.q.filter((i, k, a) => Number.isInteger(i) && i >= 0 && i < n && a.indexOf(i) === k);
  d.recent = (Array.isArray(d.recent) ? d.recent : []).filter(i => Number.isInteger(i) && i >= 0 && i < n);
  const ok = namesOk(), usable = i => ok || !named(list[i]);
  if (!d.q.some(usable)) {
    // New round. Name lines still waiting for their turn are shuffled into it.
    const waiting = new Set(d.q), recent = d.recent.filter(i => !waiting.has(i));
    const rest = Array.from({length: n}, (_, i) => i).filter(i => !waiting.has(i) && !recent.includes(i));
    d.q = recent.concat(shuffle(rest.concat(d.q)));
  }
  if (!ok) {
    // Name lines that come up too soon go back to a random spot further down the line instead of piling up.
    let k = d.q.length - 1;
    while (k > 0 && !usable(d.q[k])) k--;
    d.q.splice(k + 1).forEach(x => d.q.splice(Math.floor(Math.random() * d.q.length), 0, x));
  }
  const i = d.q.pop();
  d.recent = d.recent.filter(x => x !== i).concat(i).slice(-10);
  if (named(list[i])) S.nameQ = S.qCount || 0;
  decks[name] = d; S.decks = decks; save();
  return i;
}
function nextWrong(){
  const i = deal('w', WRONGS);
  return Object.assign({key: 'w' + String(i + 1).padStart(2, '0')}, WRONGS[i]);
}
function fitBubble(ov){
  const bub = ov.querySelector('.bl-bubble'), body = ov.querySelector('.bl-body');
  let k = 1; bub.style.setProperty('--bf', k);
  while (bub.offsetHeight > body.clientHeight - 30 && k > 0.5) { k = Math.round((k - 0.05) * 100) / 100; bub.style.setProperty('--bf', k); }
}
function nextBlessing(){
  const i = deal('b', BLESSINGS);
  return Object.assign({key: 'b' + String(i + 1).padStart(2, '0')}, BLESSINGS[i]);
}
const still = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
function petals(){
  const box = $('petals'); box.innerHTML = '';
  if (still) return;
  for (let k = 0; k < 28; k++) {
    const p = document.createElement('i'); p.className = 'petal';
    p.style.left = (Math.random() * 100) + '%';
    p.style.animationDuration = (2.6 + Math.random() * 2.4) + 's';
    p.style.animationDelay = (Math.random() * 1.4) + 's';
    p.style.setProperty('--sx', (Math.random() * 160 - 80) + 'px');
    p.style.setProperty('--rot', (Math.random() * 720 - 360) + 'deg');
    if (k % 3 === 0) p.style.background = 'radial-gradient(circle at 30% 30%,#fff3c4,#FFC93C 70%)';
    box.appendChild(p);
  }
}
function drawPts(){
  const box = $('blessPts'); box.removeAttribute('data-done');
  const named = S.players.map((p, i) => [p, i]).filter(([p]) => p.n.trim());
  if (!named.length) { box.innerHTML = ''; return; }
  box.innerHTML = '<div class="bl-ptl">Give the point to</div>' + named.map(([p, i]) => '<button class="bl-chip" data-pt="' + i + '">' + esc(p.n) + '</button>').join('');
  box.querySelectorAll('[data-pt]').forEach(b => b.addEventListener('click', ev => {
    ev.stopPropagation();
    if (box.dataset.done) return;
    const p = S.players[+b.dataset.pt]; if (!p) return;
    p.s += 1; box.dataset.done = '1'; b.classList.add('got'); b.textContent = p.n + '  +1'; save();
  }));
}
function showBlessing(){
  const b = nextBlessing(), hi = S.lang === 'hi';
  const o = $('blessOpen'), t = $('blessText'), en = $('blessEn'), th = $('blessTath');
  setText(o, hi ? b.open_hi : b.open_en); o.classList.toggle('hi', hi);
  setText(t, hi ? b.hi : b.en); t.classList.toggle('hi', hi);
  en.textContent = b.en; en.hidden = !hi;
  th.textContent = (hi ? b.close_hi : b.close_en) + ' 🙏'; th.classList.toggle('hi', hi);
  drawPts();
  E.bless.hidden = false; anim(E.bless, 'in'); fitBubble(E.bless);
  petals(); chime();
  setTimeout(() => { if (!E.bless.hidden) say(b.open_hi + ' ' + b.hi + ' ' + b.close_hi, b.open_en + ' ' + b.en + ' ' + b.close_en, b.key); }, 500);
}
function hideBless(){ if (E.bless.hidden) return; E.bless.hidden = true; $('petals').innerHTML = ''; hush(); }
E.bless.addEventListener('click', e => { if (e.target.closest('.bl-chip')) return; hideBless(); });
let wrongT = null;
function showWrong(){
  hideBless();
  const w = nextWrong(), hi = S.lang === 'hi';
  const t = $('oopsText'), en = $('oopsEn');
  setText(t, hi ? w.hi : w.en); t.classList.toggle('hi', hi);
  en.textContent = w.en; en.hidden = !hi;
  E.oops.hidden = false; anim(E.oops, 'in'); fitBubble(E.oops);
  E.card.classList.remove('shake'); void E.card.offsetWidth; E.card.classList.add('shake');
  buzz();
  clearTimeout(wrongT); wrongT = setTimeout(hideWrong, 7000);
  setTimeout(() => {
    if (E.oops.hidden) return;
    say(w.hi, w.en, w.key).then(d => { if (E.oops.hidden) return; clearTimeout(wrongT); wrongT = setTimeout(hideWrong, (d + 1.4) * 1000); });
  }, 350);
}
function hideWrong(){ clearTimeout(wrongT); if (!E.oops.hidden) { E.oops.hidden = true; hush(); } E.card.classList.remove('shake'); }
E.oops.addEventListener('click', hideWrong);
function closeFx(){ hideBless(); hideWrong(); }

function drawSettings(){
  [['sfxTog', S.sfx], ['voiceTog', S.voice]].forEach(([id, on]) => { const b = $(id); b.setAttribute('aria-pressed', String(on)); b.textContent = on ? 'On' : 'Off'; });
  $('langHi').setAttribute('aria-pressed', String(S.lang === 'hi')); $('langEn').setAttribute('aria-pressed', String(S.lang === 'en'));
  drawVoices();
}
function drawVoices(){
  const sel = $('voiceSel'), list = usable();
  const hi = list.filter(v => HI.test(v.lang)), inEn = list.filter(v => EN_IN.test(v.lang)), other = list.filter(v => /^en/i.test(v.lang) && !EN_IN.test(v.lang));
  const opt = v => '<option value="' + esc(v.name) + '">' + esc(v.name) + '</option>';
  const grp = (label, arr) => arr.length ? '<optgroup label="' + label + '">' + arr.map(opt).join('') + '</optgroup>' : '';
  sel.innerHTML = '<option value="">Automatic' + (S.lang === 'hi' ? ' (' + NATURAL[NAT_DEFAULT] + ')' : '') + '</option>'
    + '<optgroup label="' + __NAT_LABEL__ + '">' + Object.entries(NATURAL).map(([k, n]) => '<option value="natural:' + k + '">' + n + '</option>').join('') + '</optgroup>'
    + grp('Phone voices: Hindi', hi) + grp('Phone voices: Indian English', inEn) + grp('Phone voices: other English', other);
  sel.value = (/^natural:/.test(S.voiceName) || list.some(v => v.name === S.voiceName)) ? S.voiceName : '';
  const nat = naturalVoice(), dev = voiceFor();
  $('voiceNote').textContent = nat ? 'Speaking with the built-in natural Hindi voice: ' + NATURAL[nat] + '.'
    : (S.lang === 'en' && /^natural:/.test(S.voiceName)) ? 'The natural voices speak Hindi only. Switch the language to हिंदी to use them.'
    : dev ? 'Speaking with your phone\'s voice: ' + dev.name + '.' : '';
}
$('langHi').addEventListener('click', () => { unlock(); S.lang = 'hi'; save(); drawSettings(); preloadClips(); say(SOUND.sample.hi, SOUND.sample.en, 'sample'); });
$('langEn').addEventListener('click', () => { unlock(); S.lang = 'en'; save(); drawSettings(); say(SOUND.sample.hi, SOUND.sample.en, 'sample'); });
$('voiceSel').addEventListener('change', e => { unlock(); S.voiceName = e.target.value; save(); drawVoices(); preloadClips(); say(SOUND.sample.hi, SOUND.sample.en, 'sample'); });
$('sfxTog').addEventListener('click', () => { unlock(); S.sfx = !S.sfx; save(); drawSettings(); if (S.sfx) chime(); });
$('voiceTog').addEventListener('click', () => { unlock(); S.voice = !S.voice; save(); drawSettings(); if (!S.voice) hush(); else say(SOUND.tath.hi, SOUND.tath.en, 'tath'); });
$('testSnd').addEventListener('click', () => { unlock(); chime(); setTimeout(() => say(SOUND.test.hi, SOUND.test.en, 'test'), 350); });

// ---------------- overlays
const sheets = {grid:$('gridSheet'), scores:$('scoreSheet')};
function sheetOpen(){ return !sheets.grid.hidden || !sheets.scores.hidden; }
function closeSheets(){ sheets.grid.hidden = true; sheets.scores.hidden = true; }
function openSheet(which){ closeSheets(); if (which === 'grid') { drawGrid(); drawSettings(); } else drawScores(); sheets[which].hidden = false; }
document.querySelectorAll('[data-close]').forEach(b => b.addEventListener('click', closeSheets));
Object.values(sheets).forEach(sh => sh.addEventListener('click', e => { if (e.target === sh) closeSheets(); }));

function drawGrid(){
  const groups = [['Start', s => s.id === 'welcome' || s.id === 'howto'], ['Warm-ups', s => s.group === 'warm'], ['Round 2', s => s.id === 'round2'], ['Puzzles', s => s.group === 'main'], ['Finish', s => s.id === 'end']];
  let html = '';
  for (const [name, test] of groups) {
    const tiles = SL.map((s, i) => [s, i]).filter(([s]) => test(s)).map(([s, i]) =>
      '<button class="tile ' + (s.level || 'wide') + (S.seen[s.id] ? ' done' : '') + (i === S.i ? ' cur' : '') + '" data-go="' + i + '">' + esc(s.tile) + '</button>').join('');
    html += '<div class="sec">' + name + '</div><div class="tiles">' + tiles + '</div>';
  }
  $('gridBody').innerHTML = html;
  $('gridBody').querySelectorAll('[data-go]').forEach(b => b.addEventListener('click', () => { closeSheets(); go(+b.dataset.go, +b.dataset.go < S.i ? 'back' : 'fwd'); }));
}
let armed = null;
function arm(btn, label, fn){
  if (armed === btn) { armed = null; fn(); return; }
  armed = btn; const orig = btn.dataset.label || btn.textContent; btn.dataset.label = orig; btn.textContent = label;
  setTimeout(() => { if (armed === btn) { armed = null; btn.textContent = orig; } }, 3000);
}
$('restartBtn').addEventListener('click', e => arm(e.currentTarget, 'Tap again to start over', () => { S.seen = {}; revealed = false; hintOn = false; closeSheets(); e.currentTarget.textContent = e.currentTarget.dataset.label; S.i = 0; render('back'); }));

function drawScores(){
  const list = $('scoreList');
  if (!S.players.length) { list.innerHTML = '<div class="empty">No players yet. Add a name or a team below, then tap + when they get one right.</div>'; }
  else list.innerHTML = S.players.map((p, i) => '<div class="prow"><span class="pn">' + esc(p.n) + '</span>'
    + '<button class="sbtn" data-d="-1" data-i="' + i + '" aria-label="Take a point from ' + esc(p.n) + '">−</button>'
    + '<span class="ps">' + p.s + '</span>'
    + '<button class="sbtn plus" data-d="1" data-i="' + i + '" aria-label="Give a point to ' + esc(p.n) + '">+</button>'
    + '<button class="sbtn rm" data-rm="' + i + '" aria-label="Remove ' + esc(p.n) + '">×</button></div>').join('');
  list.querySelectorAll('[data-d]').forEach(b => b.addEventListener('click', () => { const p = S.players[+b.dataset.i]; p.s = Math.max(0, p.s + (+b.dataset.d)); afterScore(); }));
  list.querySelectorAll('[data-rm]').forEach(b => b.addEventListener('click', () => { S.players.splice(+b.dataset.rm, 1); afterScore(); }));
}
function afterScore(){ save(); drawScores(); if (SL[S.i].id === 'end') { E.content.innerHTML = endBody(); fit(); } }
$('addForm').addEventListener('submit', e => {
  e.preventDefault();
  const inp = $('playerName'); const n = inp.value.trim().slice(0, 24);
  if (!n) { inp.focus(); return; }
  if (S.players.length >= 12) return;
  S.players.push({n, s:0}); inp.value = ''; afterScore();
});
$('resetScores').addEventListener('click', e => arm(e.currentTarget, 'Tap again to reset', () => { S.players.forEach(p => p.s = 0); e.currentTarget.textContent = e.currentTarget.dataset.label; afterScore(); }));

// ---------------- boot
function start(data){
  if (data && data.state) adopt(data.state); else load();
  layout();
  render(null);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => fit());
  if (document.fonts) document.fonts.addEventListener && document.fonts.addEventListener('loadingdone', () => fit());
}
window.addEventListener('resize', layout);
window.addEventListener('orientationchange', () => setTimeout(layout, 150));
if (window.ResizeObserver) new ResizeObserver(() => layout()).observe(app);
window.claude?.hot?.snapshot?.(() => ({state: S}));
window.claude?.hot?.ready ? window.claude.hot.ready(start) : start(window.claude?.hot?.data ?? {});
})();
"""


def build(ev, out):
    cfg, tx, ch = ev.cfg, ev.texts, ev.character
    decor = cfg["decor"]
    sl = slides(ev)
    toran_port = toran(1080, 19, 40, (46, 1034), lambda x: abs(x - 540) >= 330, "tp", decor["garland"], decor["bell"])
    toran_land = toran(1920, 31, 42, (56, 1864), lambda x: x < 110 or x > 1810, "tl", decor["garland"], decor["bell"])
    theme = "".join(f"{k}:{v};" for k, v in cfg.get("theme", {}).items())
    css = CSS + (":root{" + theme + "}\n" if theme else "")
    page = f"""<title>{cfg['app_title']}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Baloo+2:wght@800&family=Luckiest+Guy&family=Poppins:wght@600;700;800;900&display=swap">
<style>{css}</style>
<div id="app">
  <div class="stage land" id="stage">
    {R.MANDALA}
    {toran_port}
    {toran_land}
    <div class="brand">{cfg['app_title'].upper()}</div>
    <div class="pills" id="pills"></div>
    <div class="prompt" id="prompt" aria-live="polite"></div>
    <div class="card" id="card" role="button" aria-label="Puzzle card. Tap to show or hide the answer">
      <div class="content" id="content"></div>
    </div>
    <div class="footer" id="footer"></div>
    <div class="dock">
      <div class="nav">
        <button class="round" id="prevBtn" aria-label="Previous">{CHEV_L}</button>
        <button class="judge no" id="wrongBtn">{ICON_X}Wrong</button>
        <button class="judge yes" id="rightBtn">{ICON_TICK}Right</button>
        <button class="primary" id="mainBtn" hidden>Next</button>
        <button class="round" id="nextBtn" aria-label="Next">{CHEV_R}</button>
      </div>
      <div class="tools">
        <button class="tool" id="hintBtn" aria-pressed="false">{R.img("1f4a1", 32)}Hint</button>
        <button class="tool" id="ansBtn">{R.img("1f440", 32)}<span id="ansLbl">Answer</span></button>
        <button class="tool" id="scoreBtn">{R.img("1f3c6", 32)}Scores</button>
        <button class="tool" id="gridBtn">{R.img("1f9e9", 32)}Menu</button>
      </div>
    </div>
    <div class="bottom">{R.img(decor["lamp"], 62)}<span id="bottomText">{cfg["banner"]}</span>{R.img(decor["lamp"], 62, "transform:scaleX(-1)")}</div>
    <div class="bless" id="bless" hidden>
      <div class="petals" id="petals"></div>
      <div class="bl-banner"><div class="outl ans"><div class="b">{tx["right_banner"]}</div><div class="f">{tx["right_banner"]}</div></div></div>
      <div class="bl-body">
        <div class="bl-god">{ev.svg()}</div>
        <div class="bl-bubble"><div class="bl-open" id="blessOpen"></div><div class="bl-text" id="blessText"></div><div class="bl-en" id="blessEn" hidden></div><div class="bl-tath" id="blessTath">Tathastu! 🙏</div><div class="bl-pts" id="blessPts"></div></div>
      </div>
      <div class="bl-close">Tap to close</div>
    </div>
    <div class="bless oops" id="oops" hidden>
      <div class="bl-banner"><div class="outl red"><div class="b">{tx["wrong_banner"]}</div><div class="f">{tx["wrong_banner"]}</div></div></div>
      <div class="bl-body">
        <div class="bl-god">{ev.svg(idp="og")}</div>
        <div class="bl-bubble"><div class="bl-text" id="oopsText"></div><div class="bl-en" id="oopsEn" hidden></div></div>
      </div>
      <div class="bl-close">Tap to close</div>
    </div>
  </div>
</div>

<div class="sheet" id="gridSheet" hidden>
  <div class="panel" role="dialog" aria-modal="true" aria-labelledby="gridTitle">
    <div class="ph"><h2 id="gridTitle">Menu</h2><button class="x" data-close aria-label="Close">×</button></div>
    <div id="gridBody"></div>
    <div class="sec">Sound</div>
    <div class="setrow"><span class="sl">Bell and buzzer</span><button class="tog" id="sfxTog" aria-pressed="true">On</button></div>
    <div class="setrow"><span class="sl">{ch['name']}'s voice for blessings</span><button class="tog" id="voiceTog" aria-pressed="true">On</button></div>
    <div class="setrow"><span class="sl">Blessing language</span><div class="seg"><button class="tog" id="langHi" type="button" aria-pressed="true">हिंदी</button><button class="tog" id="langEn" type="button" aria-pressed="false">English</button></div></div>
    <div class="setrow"><label class="sl" for="voiceSel">Voice</label><select id="voiceSel"></select></div>
    <p class="note" id="voiceNote"></p>
    <div class="setrow"><span class="sl">Check the sound before you start</span><button class="wbtn ghost" id="testSnd" type="button">Play test</button></div>
    <p class="note">No sound? Turn off silent mode on your iPhone and turn the volume up.</p>
    <div class="foot"><span class="note">✓ means the answer has been shown.</span><button class="wbtn ghost" id="restartBtn">Start over</button></div>
  </div>
</div>

<div class="sheet" id="scoreSheet" hidden>
  <div class="panel" role="dialog" aria-modal="true" aria-labelledby="scoreTitle">
    <div class="ph"><h2 id="scoreTitle">Scores</h2><button class="x" data-close aria-label="Close">×</button></div>
    <div id="scoreList"></div>
    <form class="addrow" id="addForm" autocomplete="off">
      <input id="playerName" type="text" maxlength="24" placeholder="Player or team name" aria-label="Player or team name" enterkeyhint="done">
      <button class="wbtn" type="submit">Add</button>
    </form>
    <div class="foot"><span class="note">The leaderboard shows on the last card. Scores stay on this phone.</span><button class="wbtn ghost" id="resetScores" type="button">Reset scores to 0</button></div>
  </div>
</div>
<script>{JS}</script>
"""

    def js_str(v):
        return json.dumps(v, ensure_ascii=False).replace("</", "<\\/")

    nat = {k: VOICE_INFO[k][0] for k in ev.voices}
    genders = {VOICE_INFO[k][1] for k in ev.voices}
    nat_label = "Natural Hindi voices" + ({"m": ", male", "f": ", female"}.get(genders.pop(), "") if len(genders) == 1 else "")
    names = ev.name_words
    named = "/" + "|".join(re.escape(n) for n in names) + "/" if names else "/(?!)/"
    c = ev.content
    sound = {k: {"hi": v["hi"], "en": v["en"]} for k, v in ev.sound_check().items()}
    page = (page.replace("__SLIDES__", js_str(sl)).replace("__ASK__", js_str(ASK))
                .replace("__TIPS__", js_str(TIPS)).replace("__END__", js_str(end_default(ev)))
                .replace("__BLESSINGS__", js_str(c.BLESSINGS)).replace("__WRONGS__", js_str(c.WRONGS))
                .replace("__LIPS__", ev.lips_file.read_text(encoding="utf-8") if ev.lips_file.exists() else "{}")
                .replace("__WELCOME__", js_str(c.WELCOME)).replace("__SOUND__", js_str(sound))
                .replace("__KEY__", js_str(cfg["storage_key"])).replace("__PREFER__", js_str(ch.get("gender", "m")))
                .replace("__NATURAL__", js_str(nat)).replace("__NAT_LABEL__", js_str(nat_label))
                .replace("__NAMED__", named))
    leftover = re.findall(r"__[A-Z_]+__", page)
    assert not leftover, leftover
    out = Path(out)
    if out.exists():
        shutil.rmtree(out)
    (out / "assets").mkdir(parents=True)
    (out / "index.html").write_text(page, encoding="utf-8")
    codes = set(re.findall(r"assets/([0-9a-f\-]+)\.webp", page)) | {"1f947", "1f948", "1f949"}
    for code in sorted(codes):
        src = R.ASSET_SRC / f"{code}.webp"
        if not src.exists():
            raise SystemExit(f"no emoji picture named {code}.webp in {R.ASSET_SRC}")
        shutil.copy(src, out / "assets" / f"{code}.webp")
    wanted = {f"v-{v}-{k}.mp3" for v in ev.voices for k in ev.lines()}
    clips = [f for f in sorted(ev.voice_dir.glob("v-*.mp3")) if f.name in wanted] if ev.voice_dir.exists() else []
    for f in clips:
        shutil.copy(f, out / "assets" / f.name)
    missing = len(wanted) - len(clips)
    print("slides", len(sl), "| emoji", len(codes), "| voice clips", len(clips), f"(missing {missing})" if missing else "",
          "| page KB", len(page.encode()) // 1024)
    return out
