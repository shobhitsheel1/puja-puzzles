"""Satyanarayan Puja (Reshma and Shobhit, 2026): the puzzles, Bhagwan's lines and screen texts.

A new event copies this file and replaces everything with puzzles and lines made for its own festival.
"""
from kit import E, T3, W, caption, col, letters, row


# ---------------------------------------------------------------- card bodies (pictures that need more than one line)

def body_split():
    return ('<div class="split">'
            '<div class="half top">BANANA</div>'
            '<div class="half bot">BANANA</div></div>')


def body_ravan():
    faces = []
    for i in range(10):
        dy = round(((i - 4.5) ** 2) * 3.2)
        faces.append(E("1f620", 112, f"margin-left:{-22 if i else 0}px;transform:translateY({dy}px)"))
    crown = E("1f451", 140, "margin-bottom:-30px")
    return col(crown, f'<div class="row" style="gap:0;padding-bottom:60px">{"".join(faces)}</div>')


def body_rekha():
    line = ('<svg width="840" height="80" viewBox="0 0 840 80" style="margin-top:6px;overflow:visible">'
            '<path d="M14,46 C 120,24 220,62 330,42 S 560,22 690,44 S 800,50 826,36" '
            'stroke="#E2412E" stroke-width="16" fill="none" stroke-linecap="round" '
            'style="filter:drop-shadow(0 0 10px rgba(255,140,0,.75))"/></svg>')
    return col(W("LAKSHMAN", 128), line, gap=10)


def body_makhan():
    blank = '<span class="blank"></span>'
    lt = lambda c: f'<span class="mk">{c}</span>'
    word = (f'<div class="row" style="gap:22px;align-items:flex-end">'
            f'{lt("M")}{blank}{lt("K")}{lt("H")}{blank}{lt("N")}</div>')
    steps = [(-12, 1.0), (14, .8), (-12, .6), (14, .42)]
    feet = "".join(E("1f463", 84, f"transform:translateY({dy}px) rotate(90deg);opacity:{o}") for dy, o in steps)
    trail = f'<div class="row" style="gap:34px;align-self:flex-end;margin-top:54px">{feet}</div>'
    return col(word, trail)


def body_narad():
    bubble = '<div class="bubble">NARAYAN<br>NARAYAN!</div>'
    notes = E("1f3b6", 96, "position:absolute;right:-70px;top:-50px;transform:rotate(12deg)")
    return col(f'<div style="position:relative">{bubble}{notes}</div>',
               caption("WHO SAYS THIS?", "margin-top:58px"))


def body_chalisa():
    honey = (f'<div style="position:relative">{E("1f36f", 220)}'
             f'{E("1f41d", 74, "position:absolute;right:-26px;top:-30px;transform:rotate(-12deg)")}</div>')
    return row(honey, E("1f468", 220), T3("40", 200, "#FF7A2F", "#A8400E"), gap=44)


def body_handi():
    g = '<div class="gv">GOVINDA</div>'
    rope = '<div style="width:800px;height:9px;background:#6D4C41;border-radius:5px"></div>'
    string = '<div style="width:6px;height:40px;background:#6D4C41"></div>'
    pot = E("1f3fa", 165)
    return col(rope, string, pot,
               '<div style="height:18px"></div>',
               row(g, gap=14), row(g, g, gap=14), row(g, g, g, gap=14), gap=0)


def body_manthan():
    import math
    order = ["U", "A", "D", "S", "A", "R", "M"]
    R = 205
    c = 280
    parts = []
    for k, ch in enumerate(order):
        a = -90 + k * 360 / len(order)
        x = c + R * math.cos(math.radians(a))
        y = c + R * math.sin(math.radians(a))
        parts.append(f'<div class="orb" style="left:{x:.0f}px;top:{y:.0f}px;'
                     f'transform:translate(-50%,-50%) rotate({a + 90 + 18:.0f}deg)">{ch}</div>')
    arcs = ('<svg width="560" height="560" viewBox="0 0 560 560" style="position:absolute;left:0;top:0;overflow:visible">'
            '<defs><marker id="ah" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto">'
            '<path d="M0,0 L6,3 L0,6 Z" fill="#1E88E5"/></marker></defs>'
            '<g fill="none" stroke="#1E88E5" stroke-width="11" stroke-linecap="round" marker-end="url(#ah)">'
            '<path d="M 280 6 A 274 274 0 0 1 529 166"/>'
            '<path d="M 280 554 A 274 274 0 0 1 31 394"/></g></svg>')
    wave = E("1f30a", 170, "position:absolute;left:195px;top:195px")
    return f'<div style="position:relative;width:560px;height:560px">{arcs}{wave}{"".join(parts)}</div>'


def body_obstacles():
    word = '<div class="strike"><span>OBSTACLES</span></div>'
    return col(row(E("1f6a7", 140), E("1f6a7", 140), E("1f6a7", 140), gap=40), word, gap=34)


def body_avatar():
    seq = row(E("1f41f", 165), E("1f422", 165), E("1f417", 165), E("1f981", 165), E("2753", 165), gap=22)
    return col(seq, caption("WHAT COMES NEXT?", "margin-top:46px"))


def body_mara():
    return col(W("MARA MARA", 128), W("MARA MARA", 128),
               caption("SAY IT FAST!", "margin-top:36px"), gap=4)


def body_eyes():
    eye = "1f441-fe0f"
    return col(E(eye, 200), row(E(eye, 200), E(eye, 200), gap=170), gap=14)


def body_harerama():
    h, r = "1f407", "1f40f"
    return col(row(E(h, 178), E(r, 178), E(h, 178), E(r, 178), gap=30),
               row(E(r, 178), E(r, 178), E(h, 178), E(h, 178), gap=30), gap=30)


def body_kumbh():
    return row(E("1f3fa", 300), E("1f442", 270),
               E("1f4a4", 140, "align-self:flex-start;margin-left:-40px;margin-top:-34px"), gap=50)


def body_chakravyuh():
    import math
    c = 260
    rings = [(150, 30), (200, 205), (250, 115)]   # radius, angle of the gap
    arcs = []
    for r, gap in rings:
        g0, g1 = math.radians(gap - 21), math.radians(gap + 21)
        x0, y0 = c + r * math.cos(g1), c + r * math.sin(g1)
        x1, y1 = c + r * math.cos(g0), c + r * math.sin(g0)
        arcs.append(f'<path d="M {x0:.1f} {y0:.1f} A {r} {r} 0 1 1 {x1:.1f} {y1:.1f}"/>')
    svg = ('<svg width="520" height="520" viewBox="0 0 520 520" style="position:absolute;left:0;top:0" aria-hidden="true">'
           '<g fill="none" stroke="#B71C1C" stroke-width="17" stroke-linecap="round">' + "".join(arcs) + '</g></svg>')
    name = ('<div class="w" style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);'
            'font-size:40px;letter-spacing:-1px;color:#111">ABHIMANYU</div>')
    return f'<div style="position:relative;width:520px;height:520px">{svg}{name}</div>'


def body_saptarishi():
    pts = [(62, 96), (176, 62), (272, 102), (366, 150), (386, 272), (562, 302), (588, 160)]
    links = [(0, 1), (1, 2), (2, 3), (3, 6), (6, 5), (5, 4), (4, 3)]
    w, h = 660, 380
    lines = "".join(f'<line x1="{pts[a][0]}" y1="{pts[a][1]}" x2="{pts[b][0]}" y2="{pts[b][1]}"/>' for a, b in links)
    stars = "".join(E("2b50", 66, f"position:absolute;left:{x - 33}px;top:{y - 33}px") for x, y in pts)
    sky = (f'<div style="position:relative;width:{w}px;height:{h}px;border-radius:30px;'
           'background:radial-gradient(120% 120% at 30% 20%, #26346a 0%, #0d1530 72%)">'
           f'<svg width="{w}" height="{h}" style="position:absolute;left:0;top:0" aria-hidden="true">'
           '<g stroke="rgba(255,255,255,.6)" stroke-width="4" stroke-dasharray="3 11" stroke-linecap="round">'
           f'{lines}</g></svg>{stars}</div>')
    return col(sky, caption("WHO ARE THESE SEVEN?", "margin-top:34px"))


def body_dussehra():
    num = lambda n: f'<span class="mk" style="font-size:132px">{n}</span>'
    r1 = row(*[num(n) for n in range(1, 6)], gap=52)
    r2 = row(*[num(n) for n in range(6, 10)], '<span class="strike" style="font-size:132px">10</span>', gap=52)
    return col(r1, r2, gap=26)


def body_diwali():
    arrow = ('<svg width="200" height="130" viewBox="0 0 200 130" aria-hidden="true">'
             '<path d="M 18 40 C 70 -6, 150 4, 158 78" fill="none" stroke="#FF8F1F" stroke-width="15" stroke-linecap="round"/>'
             '<path d="M 128 66 L 160 112 L 190 62 Z" fill="#FF8F1F"/></svg>')
    flipped = W("RAM", 160, style="transform:scaleX(-1)")
    return row(flipped, arrow, W("AYODHYA", 120), gap=16)


def body_navgraha():
    p = lambda: E("1fa90", 150)
    return col(row(p(), p(), p(), gap=34), row(p(), p(), p(), gap=34), row(p(), p(), p(), gap=34), gap=18)


# ---------------------------------------------------------------- warm-ups (general English rebus puzzles to learn the tricks)

WARMUPS = [
    dict(body=row(E("1f41d", 310), E("1f343", 300), gap=70),
         answer="BELIEF", trick="Trick: say it out loud",
         explain=":1f41d: <b>BEE</b> + :1f343: <b>LEAF</b> → Be-leaf → <b>BELIEF</b>",
         hint="Say both pictures out loud"),
    dict(body=row(W("CYCLE", 120, "a"), W("CYCLE", 120, "a"), W("CYCLE", 120, "a"), gap=34),
         answer="TRICYCLE", trick="Trick: count",
         explain="Three × CYCLE → <b>TRI-CYCLE</b>",
         hint="Count the cycles"),
    dict(body=col(W("MIND", 140),
                  '<div style="width:600px;height:14px;background:#111;border-radius:7px;margin:12px 0 8px"></div>',
                  W("MATTER", 140)),
         answer="MIND OVER MATTER", trick="Trick: look where it sits",
         explain="<b>MIND</b> is written <b>OVER</b> <b>MATTER</b>",
         hint="Where is MIND?"),
    dict(body=letters(["B C F G H J", "K L M N O P", "Q R S T U V", "W X Y Z"]),
         answer="NO IDEA", trick="Trick: spot what's missing",
         explain="No <b>I</b>, <b>D</b>, <b>E</b> or <b>A</b> in the alphabet → <b>NO IDEA</b>",
         hint="Which letters are missing?"),
    dict(body=body_split(),
         answer="BANANA SPLIT", trick="Trick: it does what it says",
         explain="The word <b>BANANA</b> is <b>split</b> in two",
         hint="What happened to the banana?"),
    dict(body=W("DEAL", 400, "a", style="line-height:1.02"),
         answer="BIG DEAL", trick="Trick: size matters",
         explain="A really <b>BIG</b> “DEAL”",
         hint="How big is it?"),
]

# ---------------------------------------------------------------- main puzzles, in play order: easy, then medium, then hard
# level: easy / medium / hard. cat: small label shown on the card. deva: answer in Devanagari.
# key / key_deva (optional): how the answer reads in the host's answer key.

PUZZLES = [
    dict(level="easy", cat="Puja",
         body=col(W("TRUTH", 134), W("NARAYAN", 134), gap=6),
         answer="SATYANARAYAN", deva="सत्यनारायण",
         explain="<b>Satya</b> means truth: <b>TRUTH + NARAYAN</b> → <b>SATYANARAYAN</b>",
         hint="Translate TRUTH into Hindi"),
    dict(level="easy", cat="Puja",
         body=row(E("1f64f", 310), E("1f622", 300), gap=70),
         answer="PRASAD", deva="प्रसाद",
         explain=":1f64f: <b>PRAY</b> + :1f622: <b>SAD</b> → Pray-sad → <b>PRASAD</b>",
         hint="Say the two pictures out loud"),
    dict(level="easy", cat="Puja",
         body=col(*[W("AMRIT", 94, style="line-height:1.04") for _ in range(5)]),
         answer="PANCHAMRIT", deva="पंचामृत",
         explain="<b>Panch</b> (5) × <b>AMRIT</b> → <b>PANCHAMRIT</b><br>Milk, curd, ghee, honey &amp; sugar",
         hint="Count them, in Hindi"),
    dict(level="easy", cat="Mantra",
         body=body_harerama(),
         answer="HARE RAMA HARE RAMA<br>RAMA RAMA HARE HARE", deva="हरे राम हरे राम, राम राम हरे हरे",
         answer_html='HARE RAMA<span class="lbl"></span> HARE RAMA<br>RAMA RAMA<span class="lbl"></span> HARE HARE',
         key="Hare Rama mantra", key_deva="हरे राम हरे राम",
         explain=":1f407: <b>HARE</b> + :1f40f: <b>RAM</b> → the <b>Hare Rama</b> mantra",
         hint="Name the two animals: it's a chant"),
    dict(level="easy", cat="Puja",
         body=row(E("1f527", 300), E("1f440", 300), gap=70),
         answer="TULSI", deva="तुलसी",
         explain=":1f527: <b>TOOL</b> + :1f440: <b>SEE</b> → Tool-see → <b>TULSI</b>",
         hint="Say it out loud: a plant in every Hindu home"),
    dict(level="easy", cat="Ramayan",
         body=body_ravan(),
         answer="RAVAN", deva="रावण · दशानन", key="Ravan / Dashanan",
         explain="Ten faces = <b>dash + anan</b> → <b>DASHANAN</b><br>That's Ravan, the ten-headed king",
         hint="Count the faces: who has this many?"),
    dict(level="easy", cat="Epics",
         body=W("BHARAT", 330, "a", style="line-height:1.02"),
         answer="MAHABHARAT", deva="महाभारत",
         explain="<b>Maha</b> (big, great) + <b>BHARAT</b> → <b>MAHABHARAT</b>",
         hint="Say how big it is, in Hindi"),
    dict(level="easy", cat="Puja",
         body=row(E("1f3a8", 300), E("1f375", 300), gap=70),
         answer="AARTI", deva="आरती",
         explain=":1f3a8: <b>ART</b> + :1f375: <b>TEA</b> → Art-tea → <b>AARTI</b>",
         hint="Say it out loud: sung with a diya"),
    dict(level="easy", cat="Gods",
         body=body_eyes(),
         answer="TRINETRA", deva="त्रिनेत्र · भगवान शिव", key="Trinetra / Shiva",
         explain="<b>Tri</b> (3) + <b>netra</b> (eyes) → <b>TRINETRA</b><br>Lord Shiva, with his third eye",
         hint="Count the eyes, in Sanskrit"),
    dict(level="easy", cat="Ramayan",
         body=body_rekha(),
         answer="LAKSHMAN REKHA", deva="लक्ष्मण रेखा",
         explain="<b>Rekha</b> means line: <b>LAKSHMAN</b> + a line → <b>LAKSHMAN REKHA</b>",
         hint="What did Lakshman draw?"),
    dict(level="medium", cat="Puja",
         body=row(T3("V", 320, "#FF8F1F", "#A85400"), E("1f400", 290), gap=50),
         answer="VRAT", deva="व्रत",
         explain="<b>V</b> + :1f400: <b>RAT</b> → V-rat → <b>VRAT</b><br>As in the Satyanarayan Vrat Katha",
         hint="Letter + animal: Satyanarayan ___ Katha"),
    dict(level="medium", cat="Ramayan",
         body=body_kumbh(),
         answer="KUMBHKARAN", deva="कुंभकर्ण",
         explain=":1f3fa: <b>Kumbh</b> (pot) + :1f442: <b>karna</b> (ear) → <b>KUMBHKARAN</b><br>Ravan's brother, the great sleeper :1f4a4:",
         hint="Pot + ear… and lots of sleep"),
    dict(level="medium", cat="Gods",
         body=row(E("1f333", 250), E("1f45f", 250), T3("L", 270, "#2E9D4F", "#145A2A"), gap=40),
         answer="TRISHUL", deva="त्रिशूल",
         explain=":1f333: <b>TREE</b> + :1f45f: <b>SHOE</b> + <b>L</b> → Tree-shoe-L → <b>TRISHUL</b>",
         hint="Say it out loud: Shiva carries it"),
    dict(level="medium", cat="Gods",
         body=row(E("1f340", 214), E("1f92b", 214), T3("ME", 178, "#E53935", "#8E1B1B"), gap=44),
         answer="LAKSHMI", deva="लक्ष्मी",
         explain=":1f340: <b>LUCK</b> + :1f92b: <b>SHH</b> + <b>ME</b> → Luck-sh-me → <b>LAKSHMI</b>",
         hint="Luck + shh + me"),
    dict(level="medium", cat="Krishna",
         body=body_makhan(),
         answer="MAKHAN CHOR", deva="माखन चोर",
         explain="Someone stole the A's from <b>MAKHAN</b><br>→ <b>MAKHAN CHOR</b>, little Krishna the butter thief",
         hint="Who took the A's?"),
    dict(level="medium", cat="Ramayan",
         body=row(T3("K", 260, "#E53935", "#8E1B1B"), E("1f511", 260), T3("E", 260, "#1F6BFF", "#0B3A9E"), gap=36),
         answer="KAIKEYI", deva="कैकेयी",
         explain="<b>K</b> + :1f511: <b>KEY</b> + <b>E</b> → K-key-E → <b>KAIKEYI</b><br>Ram's stepmother",
         hint="Letter + key + letter: Ram's stepmother"),
    dict(level="medium", cat="Satyanarayan Katha",
         body=body_narad(),
         answer="NARAD MUNI", deva="नारद मुनि",
         explain="Narad Muni's famous line!<br>He's in <b>Chapter 1</b> of the Satyanarayan Katha",
         hint="Who says this? He's in the Katha"),
    dict(level="medium", cat="Festivals",
         body=row(E("1f382", 290), T3("8", 320, "#8E44FF", "#4B1FA3"), gap=60),
         answer="JANMASHTAMI", deva="जन्माष्टमी",
         explain=":1f382: <b>Janm</b> (birth) + <b>ashtami</b> (8th day)<br>→ <b>JANMASHTAMI</b>, Krishna's birthday",
         hint="Birthday + 8th day, in Hindi"),
    dict(level="medium", cat="Bhakti",
         body=body_chalisa(),
         answer="HANUMAN CHALISA", deva="हनुमान चालीसा",
         explain=":1f36f: <b>HONEY</b> + :1f468: <b>MAN</b> → Hanuman<br><b>40 = chalis</b> → <b>HANUMAN CHALISA</b> (40 verses)",
         hint="Honey + man… and 40 in Hindi"),
    dict(level="medium", cat="Mahabharat",
         body=row(E("1f697", 290), E("1f645", 270), gap=80),
         answer="KARNA", deva="कर्ण",
         explain=":1f697: <b>CAR</b> + :1f645: <b>NA</b> (no, in Hindi) → <b>KARNA</b>",
         hint="Car + how you say 'no' in Hindi"),
    dict(level="medium", cat="Festivals",
         body=body_handi(),
         answer="DAHI HANDI", deva="दही हांडी",
         explain="A pyramid of <b>Govindas</b> reaching for the pot<br>→ <b>DAHI HANDI</b>, a Janmashtami favourite",
         hint="A Janmashtami game"),
    dict(level="medium", cat="Gods",
         body=T3("THROAT", 170, "#1F6BFF", "#0B3A9E"),
         answer="NEELKANTH", deva="नीलकंठ",
         explain="<b>Neel</b> (blue) + <b>kanth</b> (throat) → <b>NEELKANTH</b><br>Shiva held the halahal poison in his throat",
         hint="Translate both: blue + throat"),
    dict(level="medium", cat="Puja",
         body=body_navgraha(),
         answer="NAVGRAHA", deva="नवग्रह",
         explain="<b>Nav</b> (9) × <b>graha</b> (planets) → <b>NAVGRAHA</b><br>The nine planets, worshipped in the puja too",
         hint="Count them, in Sanskrit"),
    dict(level="medium", cat="Gods",
         body=row(E("1f320", 300), E("1f195", 300), gap=70),
         answer="VISHNU", deva="विष्णु",
         explain=":1f320: <b>WISH</b> + :1f195: <b>NEW</b> → Wish-new → <b>VISHNU</b>",
         hint="What do you make on a shooting star?"),
    dict(level="medium", cat="Festivals",
         body=row(E("1f40f", 290), T3("9", 320, "#FF8F1F", "#A85400"), gap=60),
         answer="RAM NAVAMI", deva="राम नवमी",
         explain=":1f40f: <b>RAM</b> + <b>9</b> (navami, the 9th day) → <b>RAM NAVAMI</b>",
         hint="Animal + 9th day, in Hindi"),
    dict(level="medium", cat="Puranas",
         body=body_manthan(),
         answer="SAMUDRA MANTHAN", deva="समुद्र मंथन",
         explain="<b>SAMUDRA</b>, all churned up → <b>SAMUDRA MANTHAN</b>",
         hint="Unscramble it… then what happened to it?"),
    dict(level="medium", cat="Mahabharat",
         body=body_chakravyuh(),
         answer="CHAKRAVYUH", deva="चक्रव्यूह",
         explain="<b>ABHIMANYU</b> trapped inside the rings<br>→ <b>CHAKRAVYUH</b>, the wheel formation",
         hint="Who went in and couldn't get out?"),
    dict(level="medium", cat="Gods",
         body=body_obstacles(),
         answer="VIGHNAHARTA", deva="विघ्नहर्ता · श्री गणेश", key="Vighnaharta / Ganesha",
         explain="<b>Vighna</b> (obstacles) + <b>harta</b> (remover)<br>→ <b>VIGHNAHARTA</b>, Lord Ganesha",
         hint="What happens to the obstacles?"),
    dict(level="hard", cat="Puja",
         body=row(E("1f45e", 240), E("1f41d", 230), E("1f9ea", 240), gap=44),
         answer="SHUBH LABH", deva="शुभ लाभ",
         explain=":1f45e: <b>SHOE</b> + :1f41d: <b>BEE</b> + :1f9ea: <b>LAB</b> → Shoe-bee lab<br>→ <b>SHUBH LABH</b>, written by the door at Diwali",
         hint="Shoe + bee + lab: written by the door at Diwali"),
    dict(level="hard", cat="Ramayan",
         body=letters(["B C D E F G", "H J K L M N", "O P Q R U V", "W X Y Z"]),
         answer="SITA HARAN", deva="सीता हरण",
         explain="<b>S</b>, <b>I</b>, <b>T</b> and <b>A</b> are missing from the alphabet<br>→ <b>SITA HARAN</b>",
         hint="Which four letters are missing?"),
    dict(level="hard", cat="Ramayan",
         body=row(E("2601-fe0f", 290, "filter:brightness(.8) saturate(1.4) drop-shadow(0 12px 10px rgba(0,0,0,.18))"),
                  E("1f50a", 260), gap=70),
         answer="MEGHNAD", deva="मेघनाद",
         explain=":2601-fe0f: <b>Megh</b> (cloud) + :1f50a: <b>naad</b> (sound) → <b>MEGHNAD</b><br>Ravan's son, named for his thunder-like roar",
         hint="Translate both: cloud + sound. Ravan's son"),
    dict(level="hard", cat="Gods",
         body=T3("CLOTH", 200, "#FFC21A", "#9A6B00"),
         answer="PITAMBAR", deva="पीतांबर",
         explain="<b>Peet</b> (yellow) + <b>ambar</b> (cloth) → <b>PITAMBAR</b><br>Lord Vishnu's yellow garment",
         hint="Translate both: yellow + cloth"),
    dict(level="hard", cat="Puranas",
         body=row(E("1f320", 260), E("1f333", 290), gap=70),
         answer="KALPAVRIKSHA", deva="कल्पवृक्ष",
         explain=":1f320: <b>WISH</b> + :1f333: <b>TREE</b> → <b>KALPAVRIKSHA</b><br>The wish-granting tree from Samudra Manthan",
         hint="Translate: wish + tree"),
    dict(level="hard", cat="Puranas",
         body=body_avatar(),
         answer="VAMANA", deva="वामन अवतार", key="Vamana (Vishnu's 5th avatar)",
         explain="Matsya :1f41f:, Kurma :1f422:, Varaha :1f417:, Narasimha :1f981:<br>…then <b>VAMANA</b>, Vishnu's 5th avatar",
         hint="Vishnu's avatars, in order"),
    dict(level="hard", cat="Festivals",
         body=body_dussehra(),
         answer="DUSSEHRA", deva="दशहरा",
         explain="<b>Das</b> (10) + <b>hara</b> (defeated) → <b>DUSSEHRA</b><br>The day Ram defeated ten-headed Ravan",
         hint="What happened to 10?"),
    dict(level="hard", cat="Gods",
         body=col(W("17 ÷ 5 = 3", 128), row(W("REMAINDER =", 82, style="letter-spacing:0"), E("1f40d", 170), gap=26), gap=34),
         answer="SHESHNAAG", deva="शेषनाग",
         explain="<b>Shesh</b> means remainder + :1f40d: <b>naag</b> (snake)<br>→ <b>SHESHNAAG</b>, Vishnu's serpent bed",
         hint="What's 'remainder' in Hindi?"),
    dict(level="hard", cat="Festivals",
         body=body_diwali(),
         answer="DIWALI", deva="दीपावली",
         explain="<b>RAM</b> turned around = Ram coming back<br>Ram returns to Ayodhya → <b>DIWALI</b>",
         hint="Ram is facing the other way… where is he going?"),
    dict(level="hard", cat="Puranas",
         body=body_saptarishi(),
         answer="SAPTARISHI", deva="सप्तर्षि",
         explain="The 7 stars of the Big Dipper are the <b>SAPTARISHI</b><br><b>Sapta</b> (7) + <b>rishi</b> (sages)",
         hint="Seven sages in the night sky"),
    dict(level="hard", cat="Ramayan",
         body=body_mara(),
         answer="RAMA RAMA", deva="मरा मरा → राम राम", key="Rama Rama (Valmiki's chant)", key_deva="राम राम",
         explain="Say <b>MARA MARA</b> fast and it becomes <b>RAMA RAMA</b><br>That's how Valmiki first chanted Ram's name",
         hint="Say it really fast"),
]

# ---------------------------------------------------------------- what the cartoon says
# Spoken by the natural Hindi voice (the *_hi text); *_en is the subtitle and the English-mode text.
# A line that is re-worded after its clip was recorded gets a new "key" (like b26v2) so phones never
# play the old recording.

BLESSINGS = [
    {"open_hi": "सही बोला बेटा! तुमने तो कमाल कर दिया!", "open_en": "Right you are, child! You've done wonders!", "hi": "मैं तुम्हें तेज़ दिमाग़ और खुश दिल का आशीर्वाद देता हूँ।", "en": "I bless you with a sharp mind and a happy heart.", "close_hi": "तथास्तु!", "close_en": "Tathastu!"},
    {"open_hi": "सही बोला! शाबाश, क्या दिमाग़ पाया है!", "open_en": "Spot on! Shabash, what a brain!", "hi": "तुम्हें और शक्ति, और बुद्धि और ढेर सारे लड्डू मिलें!", "en": "May you get more power, more wisdom and lots of laddoos!", "close_hi": "जाओ, मौज करो!", "close_en": "Now go and have fun!"},
    {"open_hi": "सही बोला बेटा! तुम्हारा दिमाग़ तो मेरे सुदर्शन चक्र से भी तेज़ चलता है!", "open_en": "Right you are, child! Your mind spins faster than my Sudarshan chakra!", "hi": "तुम्हारा वाई-फ़ाई हमेशा तेज़ चले और फ़ोन की बैटरी कभी ख़त्म न हो।", "en": "May your Wi-Fi always be strong and your battery never run out.", "close_hi": "जीते रहो!", "close_en": "Live long!"},
    {"open_hi": "एकदम सही बोला! वैकुंठ तक तालियाँ बज रही हैं!", "open_en": "Exactly right! They're clapping all the way up in Vaikunth!", "hi": "तुम्हें अच्छी सेहत और ढेर सारी हँसी का वरदान मिले।", "en": "I bless you with good health and lots of laughter.", "close_hi": "खुश रहो!", "close_en": "Stay happy!"},
    {"open_hi": "सही बोला वत्स! मैं प्रसन्न हुआ!", "open_en": "Right you are, my child! I am pleased!", "hi": "हर परीक्षा आसान हो और हर जवाब सही हो।", "en": "May every exam be easy and every answer be right.", "close_hi": "विजयी भव!", "close_en": "Be victorious!"},
    {"open_hi": "सही बोला बेटा! तुम तो छुपे रुस्तम निकले!", "open_en": "Right you are, child! You're a hidden genius!", "hi": "तुम्हें गणेश जी जैसी तेज़ याददाश्त मिले!", "en": "May you have a memory as sharp as Ganesha's!", "close_hi": "तथास्तु!", "close_en": "Tathastu!"},
    {"open_hi": "सही पकड़े हो! इतना तेज़ तो गरुड़ भी नहीं उड़ता!", "open_en": "You got it! Even Garuda doesn't fly that fast!", "hi": "तुम्हें हनुमान जी जैसा साहस मिले।", "en": "May you have courage like Hanuman.", "close_hi": "जय हो!", "close_en": "Jai ho!"},
    {"open_hi": "सही बोला बेटा! नारद जी भी हैरान रह गए!", "open_en": "Right you are, child! Even Narad ji is amazed!", "hi": "तुम्हारी चाय हमेशा गरम रहे और चिंताएँ हमेशा छोटी।", "en": "May your chai always be hot and your worries always be small.", "close_hi": "मौज करो!", "close_en": "Enjoy!"},
    {"open_hi": "सही बोला! आज तो प्रसाद तुम्हारे नाम!", "open_en": "Spot on! Today the prasad is all yours!", "hi": "तुम्हें प्रसाद हमेशा डबल मिले!", "en": "May you always get a double helping of prasad!", "close_hi": "खाओ और मुस्कुराओ!", "close_en": "Eat and smile!"},
    {"open_hi": "हाँ बेटा, एकदम सही! तुमने तो मेरा दिन बना दिया!", "open_en": "Yes, child, exactly right! You've made my day!", "hi": "टीवी का रिमोट तुम्हें हमेशा पहली बार में मिल जाए।", "en": "May you always find the TV remote on the first try.", "close_hi": "तथास्तु!", "close_en": "Tathastu!"},
    {"open_hi": "सही बोला बेटा! तुम्हारा जवाब सुनकर शेषनाग भी जाग गए!", "open_en": "Right you are, child! Your answer woke up Sheshnaag!", "hi": "तुम्हें ट्रैफ़िक में भी धैर्य का आशीर्वाद मिले!", "en": "I bless you with patience, even in traffic!", "close_hi": "शांत रहो, सुखी रहो!", "close_en": "Stay calm, stay happy!"},
    {"open_hi": "सही बोला! मेरा शंख भी तुम्हारे लिए बज रहा है!", "open_en": "Spot on! Even my conch is blowing for you!", "hi": "तुम्हारा घर हमेशा खुशियों, शांति और मिठाइयों से भरा रहे।", "en": "May your home be full of joy, peace and sweets.", "close_hi": "कल्याण हो!", "close_en": "Bless you!"},
    {"open_hi": "बिल्कुल सही बोला! लक्ष्मी जी भी मुस्कुरा रही हैं!", "open_en": "Absolutely right! Even Lakshmi ji is smiling!", "hi": "तुम पर लक्ष्मी जी की कृपा और सरस्वती जी का ज्ञान बना रहे।", "en": "May Lakshmi's prosperity and Saraswati's wisdom stay with you.", "close_hi": "तथास्तु!", "close_en": "Tathastu!"},
    {"open_hi": "सही बोला बेटा! यह तो तुमने चुटकियों में हल कर दिया!", "open_en": "Right you are, child! You solved that in a snap!", "hi": "तुम्हारी सारी मनोकामनाएँ पूरी हों, एक-एक पहेली करके।", "en": "May all your wishes come true, one puzzle at a time.", "close_hi": "ऐसे ही चमकते रहो!", "close_en": "Keep shining!"},
    {"open_hi": "सही बोला भक्त! तुमने तो मेरा दिल जीत लिया!", "open_en": "Right you are, devotee! You've won my heart!", "hi": "तुम्हें सच्चे दोस्त और प्यार भरा परिवार मिले।", "en": "May you have true friends and a loving family.", "close_hi": "सदा सुखी रहो!", "close_en": "Be happy always!"},
    {"open_hi": "सही बोला बेटा! यह जवाब तो ब्रह्मास्त्र जैसा था!", "open_en": "Right you are, child! That answer hit like a Brahmastra!", "hi": "सफलता हमेशा तुम्हारे क़दम चूमे।", "en": "May success follow you wherever you go.", "close_hi": "विजयी भव!", "close_en": "Be victorious!"},
    {"open_hi": "सही पकड़े हो भक्त! एक नंबर!", "open_en": "You got it, devotee! Number one!", "hi": "तुम्हारी मुस्कान से पूरा घर रोशन रहे।", "en": "May your smile light up the whole house.", "close_hi": "मुस्कुराते रहो!", "close_en": "Keep smiling!"},
    {"open_hi": "सही बोला बेटा! सौ में सौ नंबर!", "open_en": "Right you are, child! A hundred out of a hundred!", "hi": "तुम्हारी थाली हमेशा भरी रहे और दिल उससे भी ज़्यादा।", "en": "May your plate always be full and your heart even fuller.", "close_hi": "तथास्तु!", "close_en": "Tathastu!"},
    {"open_hi": "बिल्कुल सही बोला! तुम्हारी बुद्धि को प्रणाम!", "open_en": "Absolutely right! I bow to your wisdom!", "hi": "तुम्हें शांत मन और मज़बूत शरीर का वरदान मिले।", "en": "May you have a calm mind and a strong body.", "close_hi": "आयुष्मान भव!", "close_en": "May you live long!"},
    {"open_hi": "सही बोला बेटा! तीनों लोकों में तुम्हारी चर्चा होगी!", "open_en": "Right you are, child! All three worlds will be talking about you!", "hi": "तुम में हमेशा दिवाली वाले बच्चे जैसी ऊर्जा बनी रहे!", "en": "May you always have the energy of a child on Diwali!", "close_hi": "जय हो!", "close_en": "Jai ho!"},
    {"open_hi": "सही बोला! तुम तो पूरे ज्ञानी निकले!", "open_en": "Spot on! You turned out to be a true sage!", "hi": "तुम्हारी चाबियाँ फिर कभी न खोएँ!", "en": "May you never lose your keys again!", "close_hi": "तथास्तु!", "close_en": "Tathastu!"},
    {"open_hi": "जय हो! सही बोला बेटा, तुम तो मेरे सबसे होशियार भक्त निकले!", "open_en": "Jai ho! Right you are, child, you're my smartest devotee!", "hi": "तुम्हें जीनियस का दिमाग़ और संत का दिल मिले।", "en": "May you have the brain of a genius and the heart of a saint.", "close_hi": "मेरा आशीर्वाद सदा तुम्हारे साथ है!", "close_en": "My blessings are always with you!"},
    # the hosts, Reshma and Shobhit, get roped in
    {"open_hi": "सही बोला बेटा! वाह, क्या बात है!", "open_en": "Right you are, child! Wah, wonderful!", "hi": "मैं रेशमा को बोलता हूँ, तुम्हें डबल प्रसाद दे दे!", "en": "I'll tell Reshma to give you double prasad!", "close_hi": "जाओ, प्रसाद लो!", "close_en": "Go get your prasad!"},
    {"open_hi": "एकदम सही बोला! शाबाश!", "open_en": "Exactly right! Shabash!", "hi": "शोभित, इस भक्त को आज एक्स्ट्रा लड्डू देना, ये मेरा आदेश है!", "en": "Shobhit, give this devotee extra laddoos today. That's my order!", "close_hi": "तथास्तु!", "close_en": "Tathastu!"},
    {"open_hi": "सही बोला बेटा! रेशमा और शोभित की पूजा सफल हो गई!", "open_en": "Right you are, child! Reshma and Shobhit's puja is a success!", "hi": "रेशमा और शोभित की तरफ़ से डबल प्रसाद, और मेरी तरफ़ से डबल आशीर्वाद!", "en": "Double prasad from Reshma and Shobhit, and double blessings from me!", "close_hi": "जय हो!", "close_en": "Jai ho!"},
    {"key": "b26v2", "open_hi": "सही पकड़े हो! देखो, ऐसे होते हैं असली भक्त!", "open_en": "You got it! See, that's what a true devotee looks like!", "hi": "तुम्हें हर पूजा में सबसे आगे वाली सीट मिले!", "en": "May you always get a front-row seat at every puja!", "close_hi": "मौज करो!", "close_en": "Enjoy!"},
    {"open_hi": "सही बोला वत्स! मैं बहुत प्रसन्न हुआ!", "open_en": "Right you are, my child! I am very pleased!", "hi": "रेशमा, इसे पंचामृत की पहली कटोरी देना!", "en": "Reshma, give this one the first bowl of panchamrit!", "close_hi": "तथास्तु!", "close_en": "Tathastu!"},
    {"key": "b28v2", "open_hi": "वाह बेटा, बिल्कुल सही जवाब!", "open_en": "Wah, child, absolutely right!", "hi": "इस घर में हमेशा तुम्हारे जैसे होशियार मेहमान आते रहें!", "en": "May this home always be full of clever guests like you!", "close_hi": "कल्याण हो!", "close_en": "Bless you!"},
    {"key": "b29v2", "open_hi": "सही बोला बेटा! सब लोग ज़ोर से ताली बजाओ!", "open_en": "Right you are, child! Everyone, a big round of applause!", "hi": "मैं शोभित को बोलता हूँ, अगली पूजा का पहला न्योता तुम्हें ही भेजे!", "en": "I'll tell Shobhit to send you the very first invite to the next puja!", "close_hi": "जाओ, मौज करो!", "close_en": "Now go and have fun!"},
    {"key": "b30v2", "open_hi": "बिल्कुल सही! सबने सुना?", "open_en": "Absolutely right! Did everyone hear that?", "hi": "इस भक्त को प्रसाद के साथ एक्स्ट्रा हलवा भी मिलना चाहिए!", "en": "This devotee deserves extra halwa with the prasad!", "close_hi": "तथास्तु!", "close_en": "Tathastu!"},
]

WRONGS = [
    {"hi": "अरे बेटा, ये जवाब सुनकर तो मेरा सुदर्शन चक्र भी रुक गया!", "en": "Child, that answer made even my Sudarshan chakra stop spinning!"},
    {"hi": "वत्स, लगता है प्रसाद ज़्यादा खा लिया, दिमाग़ सो गया!", "en": "Too much prasad, my child? Your brain has gone to sleep!"},
    {"hi": "हे भक्त! ऐसी गलती तो कुंभकर्ण भी नींद में नहीं करता!", "en": "Not even Kumbhkaran makes this mistake in his sleep!"},
    {"hi": "अरे, नारद जी हँस-हँस कर लोटपोट हो गए! फिर से सोचो।", "en": "Narad ji is rolling with laughter! Think again."},
    {"hi": "मैंने तीनों लोक देखे हैं, पर ऐसा जवाब कभी नहीं सुना!", "en": "I have seen all three worlds, but never an answer like that!"},
    {"hi": "बेटा, ध्यान लगाओ... मोबाइल पर नहीं, पहेली पर!", "en": "Concentrate, child... on the puzzle, not the phone!"},
    {"hi": "गलत! पर कोई बात नहीं, मैं दयालु हूँ। एक और मौका!", "en": "Wrong! But never mind, I am merciful. One more chance!"},
    {"hi": "अरे अरे अरे! तुम्हारा जवाब सुनकर शेषनाग ने भी करवट बदल ली!", "en": "Oh dear! Even Sheshnaag rolled over when he heard that!"},
    {"hi": "हे वत्स, ये उत्तर तो पाताल लोक से आया लगता है!", "en": "My child, that answer seems to have come straight from the underworld!"},
    {"hi": "तुम्हारी तपस्या अभी अधूरी है, फिर से कोशिश करो!", "en": "Your penance is not complete yet. Try again!"},
    {"hi": "ये जवाब तो लड्डू की तरह गोल-मोल है! फिर से सोचो।", "en": "That answer is as round and wobbly as a laddoo! Think again."},
    {"hi": "अरे बेटा, गरुड़ जी को भेजूँ? तुम्हारा दिमाग़ ढूँढकर ले आएँगे!", "en": "Shall I send Garuda to go and find your brain?"},
    {"hi": "अरे बेटा! ऐसे जवाब दोगे तो रेशमा प्रसाद आधा कर देगी!", "en": "Answers like that, child, and Reshma will cut your prasad in half!"},
    {"hi": "शोभित, इस भक्त को एक लड्डू और खिलाओ, शायद दिमाग़ चल पड़े!", "en": "Shobhit, feed this devotee one more laddoo. Maybe the brain will start working!"},
    {"hi": "अरे बेटा शोभित, इसकी क्लासेस लगाओ! पहेली की ट्यूशन ज़रूरी है।", "en": "Shobhit beta, give this one some classes! Puzzle tuition is a must."},
    {"key": "w16v2", "hi": "इसका प्रसाद तब तक रुका रहेगा, जब तक सही जवाब न आए!", "en": "No prasad for this one until the right answer comes!"},
    {"key": "w17v2", "hi": "ज़रा अपना वाई-फ़ाई चेक करो, दिमाग़ से कनेक्शन टूट गया है!", "en": "Check your Wi-Fi, child. The connection to your brain is down!"},
    {"hi": "रेशमा, एक कप कड़क चाय लाओ, इस भक्त का दिमाग़ जगाना पड़ेगा!", "en": "Reshma, bring a cup of strong chai. This devotee's brain needs waking up!"},
    {"hi": "अरे वत्स, रेशमा और शोभित ने इतनी मेहनत से पूजा रखी, और तुम ऐसा जवाब दे रहे हो?", "en": "Reshma and Shobhit worked so hard on this puja, and you give an answer like that?"},
    {"key": "w20v2", "hi": "पीछे वाली लाइन में जाकर बैठो, आगे की सीट होशियार भक्तों के लिए है!", "en": "Off you go to the back row! The front seats are for clever devotees."},
    {"hi": "रेशमा, इसके पंचामृत में थोड़े बादाम ज़्यादा डालना, याददाश्त के लिए!", "en": "Reshma, put a few extra almonds in this one's panchamrit, for the memory!"},
    {"hi": "हे भक्त, ये जवाब सुनकर मेरे शंख की आवाज़ भी बैठ गई!", "en": "Devotee, that answer made even my conch lose its voice!"},
    {"hi": "बेटा, ये पहेली है, अंताक्षरी नहीं! फिर से सोचो।", "en": "Child, this is a puzzle, not antakshari! Think again."},
    {"hi": "अरे वत्स, गलत! गणेश जी ने तो अपना लड्डू तक नीचे रख दिया!", "en": "Wrong, my child! Ganesh ji has even put down his laddoo!"},
    {"hi": "हनुमान जी ने पूरा पहाड़ उठा लिया था, और तुमसे एक पहेली नहीं उठ रही?", "en": "Hanuman ji lifted a whole mountain, and you can't lift one little puzzle?"},
    {"hi": "गलत जवाब! चिंता मत करो, अगली बार मैं थोड़ा इशारा दूँगा... शायद!", "en": "Wrong answer! Don't worry, next time I'll drop a little hint... maybe!"},
    {"hi": "अरे बेटा, ये तो वैसा हुआ जैसे दिवाली पर पटाखा फुस्स हो जाए!", "en": "Child, that's like a Diwali cracker that fizzles out!"},
    {"hi": "वत्स, इतनी जल्दी क्या है? पहले सोचो, फिर बोलो!", "en": "What's the hurry, my child? Think first, then speak!"},
    {"hi": "अरे! इस जवाब से तो मेरा मुकुट भी टेढ़ा हो गया!", "en": "Oh! That answer has knocked my crown crooked!"},
    {"hi": "हे भक्त, लगता है आज दिमाग़ छुट्टी पर है! उसे वापस बुलाओ।", "en": "Looks like your brain is on holiday today! Call it back."},
    {"hi": "गलत, गलत, गलत! पर तुम्हारी मुस्कान सही है, इसलिए माफ़ किया!", "en": "Wrong, wrong, wrong! But your smile is right, so you're forgiven!"},
    {"key": "w32v2", "hi": "अगली पूजा से पहले पहेलियों की प्रैक्टिस करके आना!", "en": "Practise your puzzles before the next puja, child!"},
]

# Spoken when someone taps the cartoon on the welcome screen.
WELCOME = {"key": "welcome2", "hi": "सत्यनारायण पूजा में आप सबका स्वागत है! इस पूजा के यजमान हैं, रेशमा और शोभित। चलो, पहेलियाँ शुरू करते हैं!",
           "en": "Welcome to the Satyanarayan Puja, hosted by Reshma and Shobhit! Come, let's start the puzzles!"}

# Words on the screens that depend on the festival.
TEXTS = {
    "round2_icon": "1f6d5",
    "round2_sub": "{n} puzzles on Satyanarayan Puja, Ramayan,<br>Mahabharat &amp; more",
    "end_big": "Satyanarayan Bhagwan<br>ki Jai!",
    "end_deva": "सत्यनारायण भगवान की जय",
    "welcome_footer_deva": "आप सभी का हार्दिक स्वागत है",
    "welcome_footer_en": "Grab some prasad, get comfy, and get ready to puzzle!",
}
