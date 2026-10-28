"""Karwa Chauth (hosted by Aditi, 2026): the puzzles, Gauri Maa's lines and screen texts."""
from kit import E, T3, W, caption, col, letters, row


# ---------------------------------------------------------------- card bodies (pictures that need more than one line)

def body_split():
    return ('<div class="split">'
            '<div class="half top">BANANA</div>'
            '<div class="half bot">BANANA</div></div>')


def body_sieve_moon():
    """The moon seen through a chhalni (sieve)."""
    import math
    lines = []
    for k in range(-5, 6):
        d = k * 34
        h = math.sqrt(max(190 ** 2 - d ** 2, 0))
        lines.append(f'<line x1="{210 + d}" y1="{210 - h:.0f}" x2="{210 + d}" y2="{210 + h:.0f}"/>')
        lines.append(f'<line x1="{210 - h:.0f}" y1="{210 + d}" x2="{210 + h:.0f}" y2="{210 + d}"/>')
    mesh = ('<svg width="420" height="420" viewBox="0 0 420 420" style="position:absolute;left:0;top:0">'
            '<g stroke="#8D6E63" stroke-width="3.5" opacity=".85">' + "".join(lines) + '</g>'
            '<circle cx="210" cy="210" r="196" fill="none" stroke="#8D5524" stroke-width="22"/>'
            '<circle cx="210" cy="210" r="196" fill="none" stroke="#FFC93C" stroke-width="6" stroke-dasharray="4 18"/></svg>')
    moon = E("1f315", 300, "position:absolute;left:60px;top:60px")
    sky = ('<div style="position:absolute;left:14px;top:14px;width:392px;height:392px;border-radius:50%;'
           'background:radial-gradient(circle at 50% 45%, #2a3a78 0%, #0d1530 75%)"></div>')
    handle = ('<div style="position:absolute;left:400px;top:190px;width:150px;height:40px;border-radius:20px;'
              'background:#8D5524;border:5px solid #5D3A17"></div>')
    return f'<div style="position:relative;width:560px;height:420px">{sky}{moon}{mesh}{handle}</div>'


def body_saat_phere():
    ring = ('<svg width="420" height="420" viewBox="0 0 420 420" style="position:absolute;left:0;top:0">'
            '<defs><marker id="sp" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto">'
            '<path d="M0,0 L6,3 L0,6 Z" fill="#E2412E"/></marker></defs>'
            '<path d="M 210 26 A 184 184 0 1 1 46 126" fill="none" stroke="#E2412E" stroke-width="13" '
            'stroke-linecap="round" marker-end="url(#sp)"/></svg>')
    fire = E("1f525", 230, "position:absolute;left:95px;top:90px")
    return row(f'<div style="position:relative;width:420px;height:420px">{ring}{fire}</div>',
               T3("×7", 220, "#FF8F1F", "#A85400"), gap=50)


def body_nirjala():
    return (f'<div style="position:relative;width:340px;height:340px">{E("1f4a7", 340)}'
            f'{E("274c", 300, "position:absolute;left:20px;top:20px;opacity:.92")}</div>')


def body_shringar():
    items = ["1f484", "1f48d", "1fa9e", "1f338"]
    rows = [row(*[E(c, 104) for c in items[r:] + items[:r]], gap=30) for r in range(4)]
    return col(*rows, caption("COUNT THEM, IN HINDI", "margin-top:24px"), gap=14)


def body_long_age():
    return ('<svg width="980" height="250" viewBox="0 0 980 250" aria-hidden="true">'
            '<text x="0" y="226" textLength="980" lengthAdjust="spacingAndGlyphs" '
            'style="font-family:Anton;font-size:250px;fill:#111">AGE</text></svg>')


def body_sauce():
    return col(row(E("1f345", 230), W("SAUCE", 170), gap=40), caption("SAY IT DESI-STYLE!", "margin-top:40px"))


def body_moonrise():
    horizon = ('<div style="width:760px;height:16px;border-radius:8px;'
               'background:linear-gradient(90deg,#1B5E20,#43A047,#1B5E20)"></div>')
    return col(row(E("1f319", 250), E("2b06-fe0f", 200), gap=40), horizon, gap=20)


def body_ahoi():
    return col('<div class="bubble">AHOY!</div>',
               row(E("26f5", 230), T3("8", 260, "#8E44FF", "#4B1FA3"), gap=70, style="margin-top:70px"))


def body_arghya():
    return row('<div class="bubble">ARGH!</div>', T3("YA", 230, "#1F6BFF", "#0B3A9E"), gap=70)


def body_red_pair():
    dress = lambda: E("1f457", 220, "filter:hue-rotate(140deg) saturate(1.8)")
    return row(T3("RED", 190, "#E53935", "#8E1B1B"), dress(), dress(), gap=30)


def body_veeravati():
    boys = "".join(E("1f466", 100, f"margin-left:{-14 if i else 0}px") for i in range(7))
    family = row(f'<div class="row" style="gap:0">{boys}</div>', E("1f478", 140), gap=36)
    trick = row(E("1f333", 170), E("1f525", 130, "margin-left:-70px;margin-top:40px"), E("1fa9e", 150), E("1f315", 120), gap=30)
    return col(family, trick, caption("WHO IS THE SISTER?", "margin-top:30px"), gap=34)


def body_tukda():
    return row(E("1f315", 280), T3("+", 180, "#555", "#222"), E("1f9e9", 260), gap=40)


def body_janam():
    return row(E("1f476", 220), E("1f476", 220), T3("+", 160, "#555", "#222"), E("1f91d", 230), gap=34)


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

PUZZLES = [
    # ---- easy
    dict(level="easy", cat="Karwa Chauth",
         body=row(E("1f3fa", 300), T3("4th", 260, "#E53935", "#8E1B1B"), gap=60),
         answer="KARWA CHAUTH", deva="करवा चौथ",
         explain=":1f3fa: <b>Karwa</b> (clay pot) + <b>Chauth</b> (4th day) → <b>KARWA CHAUTH</b>",
         hint="Name the pot, then say 4th in Hindi"),
    dict(level="easy", cat="Shringar",
         body=row(T3("ME", 220, "#2E9D4F", "#145A2A"), E("1f414", 260), T3("D", 240, "#E53935", "#8E1B1B"), gap=36),
         answer="MEHENDI", deva="मेहंदी",
         explain="<b>ME</b> + :1f414: <b>HEN</b> + <b>D</b> → Me-hen-D → <b>MEHENDI</b>",
         hint="Say it out loud: me + bird + letter"),
    dict(level="easy", cat="Shringar",
         body=row(E("1f5d1-fe0f", 290), T3("D", 290, "#E53935", "#8E1B1B"), gap=60),
         answer="BINDI", deva="बिंदी",
         explain=":1f5d1-fe0f: <b>BIN</b> + <b>D</b> → Bin-D → <b>BINDI</b>",
         hint="Where does rubbish go? Add a letter"),
    dict(level="easy", cat="Shringar",
         body=row(W("SIN", 200), E("1f6aa", 300), gap=50),
         answer="SINDOOR", deva="सिंदूर",
         explain="<b>SIN</b> + :1f6aa: <b>DOOR</b> → Sin-door → <b>SINDOOR</b>",
         hint="Say it out loud: it goes in the parting"),
    dict(level="easy", cat="Puja",
         body=row(E("2702-fe0f", 280), T3("HA", 260, "#FF8F1F", "#A85400"), gap=60),
         answer="KATHA", deva="कथा",
         explain=":2702-fe0f: <b>CUT</b> + <b>HA</b> → Cut-ha → <b>KATHA</b><br>The story told during the evening puja",
         hint="What do scissors do? Add HA"),
    dict(level="easy", cat="Karwa Chauth",
         body=row(T3("SU", 250, "#8E44FF", "#4B1FA3"), E("1f917", 290), gap=50),
         answer="SUHAAG", deva="सुहाग",
         explain="<b>SU</b> + :1f917: <b>HUG</b> → Su-hug → <b>SUHAAG</b>",
         hint="SU + what this face is doing"),
    dict(level="easy", cat="Food",
         body=row(E("1f511", 290), T3("R", 290, "#1F6BFF", "#0B3A9E"), gap=60),
         answer="KHEER", deva="खीर",
         explain=":1f511: <b>KEY</b> + <b>R</b> → Key-R → <b>KHEER</b>",
         hint="Say it out loud: a sweet dish"),
    dict(level="easy", cat="Karwa Chauth",
         body=row(T3("V", 320, "#FF8F1F", "#A85400"), E("1f400", 290), gap=50),
         answer="VRAT", deva="व्रत",
         explain="<b>V</b> + :1f400: <b>RAT</b> → V-rat → <b>VRAT</b><br>The Karwa Chauth fast, from sunrise to moonrise",
         hint="Letter + animal: what everyone's keeping today"),
    dict(level="easy", cat="Shringar",
         body=row(E("1f95c", 290), T3("H", 290, "#2E9D4F", "#145A2A"), gap=60),
         answer="NATH", deva="नथ",
         explain=":1f95c: <b>NUT</b> + <b>H</b> → Nut-H → <b>NATH</b>, the bridal nose ring",
         hint="Say it out loud: worn on the nose"),
    dict(level="easy", cat="Karwa Chauth",
         body=body_sieve_moon(),
         answer="CHHALNI SE CHAND", deva="छलनी से चाँद",
         key="Moon through the chhalni", key_deva="छलनी से चाँद",
         explain="The <b>moon</b>, seen through a <b>chhalni</b> (sieve)<br>→ how the fast ends tonight :1f319:",
         hint="How will you look at the moon tonight?"),
    dict(level="easy", cat="Shaadi",
         body=body_saat_phere(),
         answer="SAAT PHERE", deva="सात फेरे",
         explain="Seven rounds of the :1f525: fire → <b>SAAT PHERE</b><br>The wedding vows that Karwa Chauth celebrates",
         hint="Count the rounds, in Hindi"),

    # ---- medium
    dict(level="medium", cat="Karwa Chauth",
         body=row(W("SIR", 200), T3("G", 300, "#FF8F1F", "#A85400"), gap=50),
         answer="SARGI", deva="सरगी",
         explain="<b>SIR</b> + <b>G</b> → Sir-G → <b>SARGI</b><br>The pre-dawn meal from the saas",
         hint="Eaten before sunrise"),
    dict(level="medium", cat="Shringar",
         body=row(E("1f4b3", 280), W("ALL", 200), gap=50),
         answer="PAYAL", deva="पायल",
         explain=":1f4b3: <b>PAY</b> + <b>ALL</b> → Pay-all → <b>PAYAL</b>, the anklet",
         hint="What do you do with a card? Worn on the ankle"),
    dict(level="medium", cat="Karwa Chauth",
         body=row(W("PA", 220), E("1f375", 290), gap=50),
         answer="PATI", deva="पति",
         explain="<b>PA</b> + :1f375: <b>TEA</b> → Pa-tea → <b>PATI</b><br>The one the fast is kept for!",
         hint="PA + a drink: the fast is for him"),
    dict(level="medium", cat="Katha",
         body=row(W("TRUTH", 160), E("1f690", 290), gap=50),
         answer="SATYAVAN", deva="सत्यवान",
         explain="<b>Satya</b> (truth) + :1f690: <b>VAN</b> → <b>SATYAVAN</b><br>Savitri's husband in the Karwa Chauth story",
         hint="Translate TRUTH into Hindi, keep the vehicle"),
    dict(level="medium", cat="Katha",
         body=row(E("1f6df", 280), E("1f333", 290), gap=70),
         answer="SAVITRI", deva="सावित्री",
         explain=":1f6df: <b>SAVE</b> + :1f333: <b>TREE</b> → Save-tree → <b>SAVITRI</b><br>She won her husband back from Yamraj",
         hint="Lifebuoy + tree: a famously devoted wife"),
    dict(level="medium", cat="Katha",
         body=row(E("1f60b", 280), E("1f451", 280), gap=70),
         answer="YAMRAJ", deva="यमराज",
         explain=":1f60b: <b>YUM</b> + :1f451: <b>RAJ</b> (king) → <b>YAMRAJ</b><br>Savitri followed him to save Satyavan",
         hint="Yummy face + king, in Hindi"),
    dict(level="medium", cat="The Moon",
         body=row(E("1f319", 250), E("1f40f", 250), T3("A", 260, "#1F6BFF", "#0B3A9E"), gap=40),
         answer="CHANDRAMA", deva="चंद्रमा",
         explain=":1f319: <b>Chand</b> (moon) + :1f40f: <b>RAM</b> + <b>A</b> → <b>CHANDRAMA</b>",
         hint="Moon in Hindi + animal + letter"),
    dict(level="medium", cat="Karwa Chauth",
         body=row(E("1f6d2", 290), E("2714-fe0f", 260), gap=70),
         answer="KARTIK", deva="कार्तिक",
         explain=":1f6d2: <b>CART</b> + :2714-fe0f: <b>TICK</b> → Cart-tick → <b>KARTIK</b><br>The month Karwa Chauth falls in",
         hint="Say it out loud: a month of festivals"),
    dict(level="medium", cat="Gods",
         body=row(E("1f404", 290), T3("RI", 270, "#E53935", "#8E1B1B"), gap=50),
         answer="GAURI", deva="गौरी · माँ पार्वती", key="Gauri / Parvati",
         explain=":1f404: <b>Gau</b> (cow) + <b>RI</b> → <b>GAURI</b><br>Maa Parvati, worshipped on Karwa Chauth",
         hint="Cow in Hindi + RI"),
    dict(level="medium", cat="Songs",
         body=row(E("1fadb", 290), W("YA!", 200), gap=50),
         answer="PIYA", deva="पिया",
         explain=":1fadb: <b>PEA</b> + <b>YA</b> → Pea-ya → <b>PIYA</b>, the beloved in every song",
         hint="A green vegetable + YA"),
    dict(level="medium", cat="Food",
         body=row(W("2+2=4", 160), T3("RI", 250, "#FF8F1F", "#A85400"), gap=50),
         answer="MATHRI", deva="मठरी",
         explain="<b>MATH</b> + <b>RI</b> → Math-ri → <b>MATHRI</b><br>The crunchy snack in the sargi and the baya",
         hint="What subject is this? Add RI"),
    dict(level="medium", cat="Karwa Chauth",
         body=body_sauce(),
         answer="SAAS", deva="सास",
         explain=":1f345: <b>SAUCE</b>, said desi-style → <b>SAAS</b><br>She sends the sargi!",
         hint="Who sends the sargi?"),
    dict(level="medium", cat="Shringar",
         body=row(T3("2", 300, "#8E44FF", "#4B1FA3"), E("1f342", 290), gap=60),
         answer="DUPATTA", deva="दुपट्टा",
         explain="<b>Do</b> (2) + :1f342: <b>patta</b> (leaf) → <b>DUPATTA</b>",
         hint="Say both in Hindi"),
    dict(level="medium", cat="Karwa Chauth",
         body=body_nirjala(),
         answer="NIRJALA", deva="निर्जला",
         explain="<b>Nir</b> (without) + :1f4a7: <b>jal</b> (water) → <b>NIRJALA</b><br>A fast without even water",
         hint="No water, in Hindi"),
    dict(level="medium", cat="Shringar",
         body=body_shringar(),
         answer="SOLAH SHRINGAR", deva="सोलह श्रृंगार",
         explain="<b>Solah</b> (16) × <b>shringar</b> (adornments) → <b>SOLAH SHRINGAR</b>",
         hint="Count them, in Hindi"),
    dict(level="medium", cat="Karwa Chauth",
         body=body_long_age(),
         answer="LAMBI UMAR", deva="लंबी उम्र",
         explain="A really <b>long</b> (lambi) <b>AGE</b> (umar) → <b>LAMBI UMAR</b><br>What the vrat prays for",
         hint="Look at its shape, then say it in Hindi"),
    dict(level="medium", cat="Karwa Chauth",
         body=row(E("2b06-fe0f", 260), E("1f3fa", 290), gap=60),
         answer="UPVAS", deva="उपवास",
         explain=":2b06-fe0f: <b>UP</b> + :1f3fa: <b>VASE</b> → Up-vase → <b>UPVAS</b>, a fast",
         hint="Direction + a pot: another word for vrat"),

    # ---- hard
    dict(level="hard", cat="Karwa Chauth",
         body=row(E("1f6b6", 280), E("1f9b5", 280), gap=60),
         answer="CHHALNI", deva="छलनी",
         explain=":1f6b6: <b>Chal</b> (walk) + :1f9b5: <b>KNEE</b> → <b>CHHALNI</b><br>The sieve for seeing the moon",
         hint="Walk, in Hindi + the joint in your leg"),
    dict(level="hard", cat="Puja",
         body=body_arghya(),
         answer="ARGHYA", deva="अर्घ्य",
         explain="<b>ARGH!</b> + <b>YA</b> → <b>ARGHYA</b><br>The water offered to the moon from the karwa",
         hint="What do you offer the moon?"),
    dict(level="hard", cat="The Moon",
         body=body_moonrise(),
         answer="CHANDRODAY", deva="चंद्रोदय",
         explain="<b>Chandra</b> (moon) + <b>uday</b> (rise) → <b>CHANDRODAY</b><br>Everyone's favourite moment tonight!",
         hint="Moon + rise, in Sanskrit"),
    dict(level="hard", cat="Festivals",
         body=body_ahoi(),
         answer="AHOI ASHTAMI", deva="अहोई अष्टमी",
         explain="<b>AHOY!</b> + <b>8</b> (ashtami) → <b>AHOI ASHTAMI</b><br>The mothers' fast, four days after Karwa Chauth",
         hint="What sailors shout + 8th day in Hindi"),
    dict(level="hard", cat="Puja",
         body=row(E("1f45e", 210), E("1f41d", 200), E("1f404", 210), E("1f915", 210), gap=30),
         answer="SHUBH MUHURAT", deva="शुभ मुहूर्त",
         explain=":1f45e: <b>SHOE</b> + :1f41d: <b>BEE</b> + :1f404: <b>MOO</b> + :1f915: <b>HURT</b><br>→ <b>SHUBH MUHURAT</b>, the auspicious time for the puja",
         hint="Shoe, bee… what does a cow say?"),
    dict(level="hard", cat="Shringar",
         body=row(W("MARS", 170, color="#D84315"), E("1f9f5", 280), gap=60),
         answer="MANGALSUTRA", deva="मंगलसूत्र",
         explain="<b>Mangal</b> (Mars) + :1f9f5: <b>sutra</b> (thread) → <b>MANGALSUTRA</b>",
         hint="Translate both: the planet + thread"),
    dict(level="hard", cat="Shringar",
         body=body_red_pair(),
         answer="LAAL JODA", deva="लाल जोड़ा",
         explain="<b>Laal</b> (red) + <b>joda</b> (pair, outfit) → <b>LAAL JODA</b><br>The bridal red worn on Karwa Chauth",
         hint="Translate: red + pair"),
    dict(level="hard", cat="The Moon",
         body=body_tukda(),
         answer="CHAND KA TUKDA", deva="चाँद का टुकड़ा",
         explain=":1f315: <b>Chand</b> + :1f9e9: a <b>piece</b> (tukda) → <b>CHAND KA TUKDA</b><br>Someone too lovely for words",
         hint="A piece of the moon, in Hindi"),
    dict(level="hard", cat="Katha",
         body=body_veeravati(),
         answer="VEERAVATI", deva="वीरावती", key="Queen Veeravati",
         explain="Seven brothers faked the moon with a :1f525: fire and :1fa9e: mirror<br>to end their sister <b>VEERAVATI</b>'s fast",
         hint="The queen in the Karwa Chauth katha"),
    dict(level="hard", cat="Karwa Chauth",
         body=body_janam(),
         answer="JANAM JANAM KA SAATH", deva="जनम जनम का साथ",
         explain=":1f476: <b>Janam</b> (birth) × 2 + :1f91d: <b>saath</b> (together)<br>→ <b>JANAM JANAM KA SAATH</b>, together for every lifetime",
         hint="Birth, birth… and together"),
]

# ---------------------------------------------------------------- what Gauri Maa says (female voice)

BLESSINGS = [
    {"open_hi": "सही बोला बेटा! तुमने तो कमाल कर दिया!", "open_en": "Right you are, child! You've done wonders!", "hi": "मैं तुम्हें तेज़ दिमाग़ और खुश दिल का आशीर्वाद देती हूँ।", "en": "I bless you with a sharp mind and a happy heart.", "close_hi": "तथास्तु!", "close_en": "Tathastu!"},
    {"open_hi": "सही बोला! शाबाश, क्या दिमाग़ पाया है!", "open_en": "Spot on! Shabash, what a brain!", "hi": "आज चाँद तुम्हारे लिए सबसे पहले निकले!", "en": "May the moon rise for you first tonight!", "close_hi": "जाओ, मौज करो!", "close_en": "Now go and have fun!"},
    {"open_hi": "एकदम सही! इतनी चमक तो पूनम के चाँद में भी नहीं!", "open_en": "Exactly right! Not even the full moon shines like that!", "hi": "तुम्हारी मेहंदी हमेशा गहरी रचे!", "en": "May your mehendi always come out dark and lovely!", "close_hi": "खुश रहो!", "close_en": "Stay happy!"},
    {"open_hi": "सही बोला वत्स! मैं प्रसन्न हुई!", "open_en": "Right you are, my child! I am pleased!", "hi": "तुम्हारी सरगी हमेशा डबल हो, और भूख कभी न लगे!", "en": "May your sargi always be double, and hunger never find you!", "close_hi": "जय हो!", "close_en": "Jai ho!"},
    {"open_hi": "सही पकड़े हो! तुम तो छुपे रुस्तम निकले!", "open_en": "You got it! You're a hidden genius!", "hi": "तुम्हारा वाई-फ़ाई हमेशा तेज़ चले और फ़ोन की बैटरी कभी ख़त्म न हो।", "en": "May your Wi-Fi always be strong and your battery never run out.", "close_hi": "जीते रहो!", "close_en": "Live long!"},
    {"open_hi": "सही बोला बेटा! कैलाश तक तालियाँ बज रही हैं!", "open_en": "Right you are, child! They're clapping all the way up on Kailash!", "hi": "तुम्हें अच्छी सेहत और ढेर सारी हँसी का वरदान मिले।", "en": "I bless you with good health and lots of laughter.", "close_hi": "तथास्तु!", "close_en": "Tathastu!"},
    {"open_hi": "वाह बेटा, बिल्कुल सही! महादेव भी मुस्कुरा रहे हैं!", "open_en": "Wah, child, absolutely right! Even Mahadev is smiling!", "hi": "तुम्हारे घर में प्यार और मिठाई कभी कम न हो।", "en": "May your home never run short of love or sweets.", "close_hi": "कल्याण हो!", "close_en": "Bless you!"},
    {"open_hi": "सही बोला! इतना तेज़ तो चाँद भी नहीं निकलता!", "open_en": "Spot on! Even the moon doesn't come out that fast!", "hi": "तुम्हारी जोड़ी सलामत रहे, और झगड़े हमेशा छोटे!", "en": "May your pair stay strong and your squabbles stay small!", "close_hi": "मुस्कुराते रहो!", "close_en": "Keep smiling!"},
    {"open_hi": "सही बोला बेटा! गणेश जी ने भी ताली बजाई!", "open_en": "Right you are, child! Even Ganesh ji clapped!", "hi": "तुम्हें गणेश जी जैसी तेज़ याददाश्त मिले!", "en": "May you have a memory as sharp as Ganesha's!", "close_hi": "विजयी भव!", "close_en": "Be victorious!"},
    {"open_hi": "एकदम सही! आज की पहेली रानी तुम ही हो!", "open_en": "Exactly right! You're tonight's puzzle queen!", "hi": "टीवी का रिमोट तुम्हें हमेशा पहली बार में मिल जाए।", "en": "May you always find the TV remote on the first try.", "close_hi": "तथास्तु!", "close_en": "Tathastu!"},
    {"open_hi": "सही बोला बेटा! यह तो तुमने चुटकियों में हल कर दिया!", "open_en": "Right you are, child! You solved that in a snap!", "hi": "तुम्हारी सारी मनोकामनाएँ पूरी हों, एक-एक पहेली करके।", "en": "May all your wishes come true, one puzzle at a time.", "close_hi": "ऐसे ही चमकते रहो!", "close_en": "Keep shining!"},
    {"open_hi": "बिल्कुल सही! तुम्हारी बुद्धि को प्रणाम!", "open_en": "Absolutely right! I bow to your wisdom!", "hi": "तुम्हें शांत मन और मज़बूत शरीर का वरदान मिले।", "en": "May you have a calm mind and a strong body.", "close_hi": "आयुष्मान भव!", "close_en": "May you live long!"},
    {"open_hi": "सही बोला! तुम्हारा दिमाग़ तो करवे के पानी जैसा साफ़ है!", "open_en": "Spot on! Your mind is as clear as the water in the karwa!", "hi": "तुम्हारी थाली हमेशा भरी रहे, और दिल उससे भी ज़्यादा।", "en": "May your plate always be full and your heart even fuller.", "close_hi": "खुश रहो!", "close_en": "Stay happy!"},
    {"open_hi": "सही बोला वत्स! मेरा दिल खुश कर दिया!", "open_en": "Right you are, my child! You've made my heart glad!", "hi": "तुम्हें सच्चे दोस्त और प्यार भरा परिवार मिले।", "en": "May you have true friends and a loving family.", "close_hi": "सदा सुखी रहो!", "close_en": "Be happy always!"},
    {"open_hi": "सही पकड़े हो! एक नंबर!", "open_en": "You got it! Number one!", "hi": "तुम्हारी मुस्कान से पूरा घर रोशन रहे, दीयों से भी ज़्यादा।", "en": "May your smile light up the house, brighter than the diyas.", "close_hi": "जय हो!", "close_en": "Jai ho!"},
    {"open_hi": "सही बोला बेटा! सौ में सौ नंबर!", "open_en": "Right you are, child! A hundred out of a hundred!", "hi": "तुम्हारी चूड़ियाँ हमेशा खनकती रहें, और तुम्हारी हँसी भी!", "en": "May your bangles always jingle, and your laughter too!", "close_hi": "मौज करो!", "close_en": "Enjoy!"},
    {"open_hi": "सही बोला! तीनों लोकों में तुम्हारी चर्चा होगी!", "open_en": "Spot on! All three worlds will be talking about you!", "hi": "तुम्हारी चाबियाँ फिर कभी न खोएँ!", "en": "May you never lose your keys again!", "close_hi": "तथास्तु!", "close_en": "Tathastu!"},
    {"open_hi": "जय हो! सही बोला बेटा, तुम तो सबसे होशियार निकले!", "open_en": "Jai ho! Right you are, child, you're the cleverest of all!", "hi": "तुम्हें जीनियस का दिमाग़ और संत का दिल मिले।", "en": "May you have the brain of a genius and the heart of a saint.", "close_hi": "मेरा आशीर्वाद सदा तुम्हारे साथ है!", "close_en": "My blessings are always with you!"},
    {"open_hi": "सही बोला! तुम्हारा जवाब तो छलनी से भी साफ़ छनकर आया!", "open_en": "Spot on! That answer came through cleaner than a chhalni!", "hi": "व्रत के दिन तुम्हें भूख कम और प्यार ज़्यादा मिले!", "en": "On fasting days, may you feel less hunger and more love!", "close_hi": "जाओ, मौज करो!", "close_en": "Now go and have fun!"},
    {"open_hi": "एकदम सही बोला! मैं बहुत प्रसन्न हुई!", "open_en": "Exactly right! I am very pleased!", "hi": "तुम्हें हर त्यौहार पर नए कपड़े और ढेर सारे तोहफ़े मिलें!", "en": "May every festival bring you new clothes and lots of gifts!", "close_hi": "विजयी भव!", "close_en": "Be victorious!"},
    {"open_hi": "सही बोला बेटा! आज तो चाँद भी तुम्हें देखने जल्दी आएगा!", "open_en": "Right you are, child! The moon will come out early just to see you!", "hi": "तुम्हारी ज़िंदगी चाँदनी जैसी रोशन रहे।", "en": "May your life glow like moonlight.", "close_hi": "सदा खुश रहो!", "close_en": "Always be happy!"},
    {"open_hi": "सही बोला! वाह, क्या बात है!", "open_en": "Spot on! Wah, wonderful!", "hi": "ट्रैफ़िक में भी तुम्हें हमेशा हरी बत्ती मिले!", "en": "May you always get green lights, even in traffic!", "close_hi": "जीते रहो!", "close_en": "Live long!"},
    {"open_hi": "सही बोला बेटा! तुम्हारा दिमाग़ तो सोलह श्रृंगार से भी ज़्यादा सजा है!", "open_en": "Right you are, child! Your mind is more dressed up than solah shringar!", "hi": "तुम्हारे घर में हर दिन त्यौहार जैसा हो।", "en": "May every day in your home feel like a festival.", "close_hi": "कल्याण हो!", "close_en": "Bless you!"},
    {"open_hi": "बिल्कुल सही! सबने सुना?", "open_en": "Absolutely right! Did everyone hear that?", "hi": "चाँद निकलते ही इस भक्त को एक्स्ट्रा मिठाई मिलनी चाहिए!", "en": "As soon as the moon is out, this one gets extra sweets!", "close_hi": "जय हो!", "close_en": "Jai ho!"},
    {"open_hi": "वाह, बिल्कुल सही जवाब!", "open_en": "Wah, absolutely the right answer!", "hi": "तुम्हारी जोड़ी जनम जनम सलामत रहे!", "en": "May your pair stay together for lifetimes!", "close_hi": "सदा सुहागन रहो!", "close_en": "Sada suhagan raho!"},
    # the host, Aditi, gets roped in
    {"open_hi": "सही बोला बेटा! वाह, क्या बात है!", "open_en": "Right you are, child! Wah, wonderful!", "hi": "मैं अदिति को बोलती हूँ, तुम्हें डबल मिठाई दे दे!", "en": "I'll tell Aditi to give you double sweets!", "close_hi": "जाओ, मिठाई लो!", "close_en": "Go get your sweets!"},
    {"open_hi": "एकदम सही बोला! शाबाश!", "open_en": "Exactly right! Shabash!", "hi": "अदिति, इस भक्त को आज एक्स्ट्रा मठरी देना, ये मेरा आदेश है!", "en": "Aditi, give this one extra mathri today. That's my order!", "close_hi": "तथास्तु!", "close_en": "Tathastu!"},
    {"open_hi": "सही बोला बेटा! अदिति की पूजा सफल हो गई!", "open_en": "Right you are, child! Aditi's puja is a success!", "hi": "अदिति की तरफ़ से डबल मिठाई, और मेरी तरफ़ से डबल आशीर्वाद!", "en": "Double sweets from Aditi, and double blessings from me!", "close_hi": "जय हो!", "close_en": "Jai ho!"},
    {"open_hi": "सही पकड़े हो! सब लोग ज़ोर से ताली बजाओ!", "open_en": "You got it! Everyone, a big round of applause!", "hi": "मैं अदिति को बोलती हूँ, अगले करवा चौथ का पहला न्योता तुम्हें ही भेजे!", "en": "I'll tell Aditi to send you the very first invite next Karwa Chauth!", "close_hi": "जाओ, मौज करो!", "close_en": "Now go and have fun!"},
    {"open_hi": "सही बोला वत्स! मैं बहुत प्रसन्न हुई!", "open_en": "Right you are, my child! I am very pleased!", "hi": "अदिति, चाँद निकलते ही पहला लड्डू इसी को देना!", "en": "Aditi, the moment the moon is out, the first laddoo goes to this one!", "close_hi": "तथास्तु!", "close_en": "Tathastu!"},
]

WRONGS = [
    {"hi": "अरे बेटा, ये जवाब सुनकर तो चाँद भी बादलों में छुप गया!", "en": "Child, that answer made even the moon hide behind the clouds!"},
    {"hi": "वत्स, लगता है भूख से दिमाग़ सो गया! बस थोड़ी देर और, फिर चाँद निकलेगा।", "en": "Hunger has put your brain to sleep! Just a little longer, the moon is coming."},
    {"hi": "अरे, ऐसे जवाब दोगे तो चाँद आज निकलेगा ही नहीं!", "en": "Answers like that and the moon won't come out at all tonight!"},
    {"hi": "मैंने तीनों लोक देखे हैं, पर ऐसा जवाब कभी नहीं सुना!", "en": "I have seen all three worlds, but never an answer like that!"},
    {"hi": "बेटा, ध्यान लगाओ... मोबाइल पर नहीं, पहेली पर!", "en": "Concentrate, child... on the puzzle, not the phone!"},
    {"hi": "गलत! पर कोई बात नहीं, मैं दयालु हूँ। एक और मौका!", "en": "Wrong! But never mind, I am merciful. One more chance!"},
    {"hi": "अरे अरे अरे! ये जवाब सुनकर तो महादेव का डमरू भी चुप हो गया!", "en": "Oh dear! Even Mahadev's damru went quiet at that answer!"},
    {"hi": "ये जवाब तो छलनी जैसा है, पूरा छेदों से भरा!", "en": "That answer is like a chhalni: full of holes!"},
    {"hi": "तुम्हारी तपस्या अभी अधूरी है, फिर से कोशिश करो!", "en": "Your penance is not complete yet. Try again!"},
    {"hi": "ये जवाब तो लड्डू की तरह गोल-मोल है! फिर से सोचो।", "en": "That answer is as round and wobbly as a laddoo! Think again."},
    {"hi": "अरे बेटा, नंदी को भेजूँ? तुम्हारा दिमाग़ ढूँढकर ले आएगा!", "en": "Shall I send Nandi to go and find your brain?"},
    {"hi": "ज़रा अपना वाई-फ़ाई चेक करो, दिमाग़ से कनेक्शन टूट गया है!", "en": "Check your Wi-Fi, child. The connection to your brain is down!"},
    {"hi": "बेटा, ये पहेली है, अंताक्षरी नहीं! फिर से सोचो।", "en": "Child, this is a puzzle, not antakshari! Think again."},
    {"hi": "अरे वत्स, गलत! गणेश जी ने तो अपना लड्डू तक नीचे रख दिया!", "en": "Wrong, my child! Ganesh ji has even put down his laddoo!"},
    {"hi": "गलत जवाब! चिंता मत करो, अगली बार मैं थोड़ा इशारा दूँगी... शायद!", "en": "Wrong answer! Don't worry, next time I'll drop a little hint... maybe!"},
    {"hi": "अरे बेटा, ये तो वैसा हुआ जैसे करवे में पानी की जगह चाय डाल दी!", "en": "Child, that's like filling the karwa with chai instead of water!"},
    {"hi": "वत्स, इतनी जल्दी क्या है? पहले सोचो, फिर बोलो!", "en": "What's the hurry, my child? Think first, then speak!"},
    {"hi": "अरे! इस जवाब से तो मेरा मुकुट भी टेढ़ा हो गया!", "en": "Oh! That answer has knocked my crown crooked!"},
    {"hi": "लगता है आज दिमाग़ ने भी व्रत रखा है! उसे थोड़ी सरगी खिलाओ।", "en": "Looks like your brain is fasting too! Feed it some sargi."},
    {"hi": "गलत, गलत, गलत! पर तुम्हारी मुस्कान सही है, इसलिए माफ़ किया!", "en": "Wrong, wrong, wrong! But your smile is right, so you're forgiven!"},
    {"hi": "अरे बेटा, ये जवाब तो कच्ची मेहंदी जैसा है, रंग ही नहीं चढ़ा!", "en": "That answer is like fresh mehendi: the colour hasn't come through!"},
    {"hi": "इतनी देर में तो चाँद निकल आता! फिर से सोचो।", "en": "The moon would have risen by now! Think again."},
    {"hi": "अरे, ऐसा जवाब सुनकर तो मेरी चूड़ियाँ भी खनकना भूल गईं!", "en": "My bangles forgot how to jingle when they heard that!"},
    {"hi": "अरे बेटा, गलत! छलनी से देखो, शायद सही जवाब दिख जाए!", "en": "Wrong, child! Try looking through the chhalni, maybe the answer will show!"},
    {"hi": "तुम्हारा जवाब सुनकर तो सासू माँ ने भी माथा पकड़ लिया!", "en": "Your answer made even the mother-in-law clutch her forehead!"},
    {"hi": "हे भक्त, लगता है आज दिमाग़ छुट्टी पर है! उसे वापस बुलाओ।", "en": "Looks like your brain is on holiday today! Call it back."},
    {"hi": "अरे बेटा! ऐसे जवाब दोगे तो अदिति मिठाई आधी कर देगी!", "en": "Answers like that, child, and Aditi will cut your sweets in half!"},
    {"hi": "अदिति, इस भक्त को एक मठरी और खिलाओ, शायद दिमाग़ चल पड़े!", "en": "Aditi, feed this one another mathri. Maybe the brain will start working!"},
    {"hi": "अदिति, इसकी क्लासेस लगाओ! पहेली की ट्यूशन ज़रूरी है।", "en": "Aditi, give this one some classes! Puzzle tuition is a must."},
    {"hi": "अदिति, चाँद निकलते ही इसे एक गिलास ठंडा पानी देना, दिमाग़ जगाना पड़ेगा!", "en": "Aditi, once the moon is out, give this one cold water. That brain needs waking up!"},
    {"hi": "अरे वत्स, अदिति ने इतनी मेहनत से पूजा रखी, और तुम ऐसा जवाब दे रहे हो?", "en": "Aditi worked so hard on this puja, and you give an answer like that?"},
    {"hi": "अदिति, इसकी मिठाई तब तक रोक के रखो, जब तक सही जवाब न आए!", "en": "Aditi, hold back this one's sweets until the right answer comes!"},
]

# Spoken when someone taps the cartoon on the welcome screen.
WELCOME = {"key": "welcome", "hi": "करवा चौथ की पूजा में आप सबका स्वागत है! इस पूजा की यजमान हैं, अदिति। चलो, पहेलियाँ शुरू करते हैं!",
           "en": "Welcome to Karwa Chauth, hosted by Aditi! Come, let's start the puzzles!"}

# Words on the screens that depend on the festival.
TEXTS = {
    "round2_icon": "1f319",
    "round2_sub": "{n} puzzles on Karwa Chauth: sargi, shringar,<br>the katha &amp; the moon",
    "end_big": "Karwa Chauth ki<br>Shubhkamnayein!",
    "end_deva": "करवा चौथ की हार्दिक शुभकामनाएँ",
    "welcome_footer_deva": "आप सभी का हार्दिक स्वागत है",
    "welcome_footer_en": "Get comfy, keep an eye on the sky, and get ready to puzzle!",
}
