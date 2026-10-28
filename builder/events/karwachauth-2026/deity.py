"""The festival cartoon: a friendly, respectful Gauri Maa (Parvati), worshipped on Karwa Chauth.

She sits on a lotus in a red chunri with a gold border, blesses with her right hand (mehendi and red bangles)
and holds a decorated karwa (clay pot) in her left, with the crescent moon glowing behind her.
Follows the hooks described in engine/face.py (float, eyes, mouths, ids starting with "bg").
"""
import math

from face import finish, mouth_defs, mouths

INK = "#3A1A1A"
SKIN = "#F2B98C"
SKIN_D = "#D9925E"
RED = "#C8102E"


def _rays():
    out = []
    for k in range(24):
        a = math.radians(k * 15)
        x1, y1 = 300 + 150 * math.cos(a), 300 + 150 * math.sin(a)
        x2, y2 = 300 + 262 * math.cos(a), 300 + 262 * math.sin(a)
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>')
    return "".join(out)


def _stars():
    pts = [(96, 150, 9), (140, 74, 6), (470, 520, 7), (520, 420, 5), (70, 420, 6), (118, 250, 5)]
    out = []
    for x, y, r in pts:
        out.append(f'<path d="M {x} {y - r * 2} L {x + r * .5} {y - r * .5} L {x + r * 2} {y} L {x + r * .5} {y + r * .5} '
                   f'L {x} {y + r * 2} L {x - r * .5} {y + r * .5} L {x - r * 2} {y} L {x - r * .5} {y - r * .5} Z" fill="#FFF6C2"/>')
    return "".join(out)


PETAL = "M 0 0 C -40 -22 -42 -88 0 -124 C 42 -88 40 -22 0 0 Z"


def _lotus():
    back = "".join(f'<path d="{PETAL}" transform="translate(300 706) rotate({a}) scale(1.05)"/>' for a in (-72, -48, -24, 0, 24, 48, 72))
    front = "".join(f'<path d="{PETAL}" transform="translate(300 716) rotate({a}) scale(.86)"/>' for a in (-58, -30, 0, 30, 58))
    return (f'<g fill="url(#bgPetal)" stroke="#B8336A" stroke-width="3">{back}</g>'
            f'<g fill="url(#bgPetalLight)" stroke="#B8336A" stroke-width="3">{front}</g>')


def _arm(d, width=40):
    return (f'<path d="{d}" stroke="{INK}" stroke-width="{width + 8}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" stroke="{SKIN}" stroke-width="{width}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')


def _sleeve(d):
    return (f'<path d="{d}" stroke="{INK}" stroke-width="52" fill="none" stroke-linecap="round"/>'
            f'<path d="{d}" stroke="url(#bgRed)" stroke-width="44" fill="none" stroke-linecap="round"/>')


def _bangles(x1, y1, x2, y2, n=4):
    out = []
    for i in range(n):
        t = i / max(n - 1, 1)
        x, y = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
        c = "#FFC93C" if i in (0, n - 1) else RED
        out.append(f'<path d="M {x - 22:.1f} {y:.1f} Q {x:.1f} {y + 9:.1f} {x + 22:.1f} {y:.1f}" stroke="{c}" stroke-width="7" fill="none" stroke-linecap="round"/>')
    return "".join(out)


def _palm(x, y):
    """Blessing hand (abhaya mudra) with a mehendi flower and dots."""
    fingers = [(-28, -48, 14, 44), (-13, -58, 14, 54), (2, -56, 14, 52), (17, -46, 14, 42)]
    f = "".join(f'<rect x="{fx}" y="{fy}" width="{w}" height="{h}" rx="7"/>' for fx, fy, w, h in fingers)
    tips = "".join(f'<rect x="{fx}" y="{fy}" width="{w}" height="9" rx="4.5" fill="#B5462B" stroke="none"/>' for fx, fy, w, h in fingers)
    petals = "".join(f'<ellipse cx="1" cy="6" rx="4" ry="9" transform="rotate({a} 1 14)" />' for a in range(0, 360, 45))
    return (f'<g transform="translate({x} {y})">'
            f'<g fill="{SKIN}" stroke="{INK}" stroke-width="3.5">{f}<ellipse cx="36" cy="6" rx="10" ry="20" transform="rotate(28 36 6)"/>'
            '<rect x="-31" y="-14" width="64" height="58" rx="22"/></g>'
            f'{tips}<g fill="none" stroke="#B5462B" stroke-width="2.4">{petals}</g>'
            '<circle cx="1" cy="14" r="5" fill="#B5462B"/>'
            '<g fill="#B5462B"><circle cx="-18" cy="34" r="2.6"/><circle cx="-6" cy="38" r="2.6"/><circle cx="8" cy="38" r="2.6"/><circle cx="20" cy="34" r="2.6"/></g>'
            '</g>')


def _karwa(x, y):
    """A clay karwa with a spout, painted with dots and a flower, and a little lid."""
    return (f'<g transform="translate({x} {y})">'
            '<path d="M 40 -6 C 62 -14 74 -30 82 -44 L 90 -38 C 84 -20 70 2 46 10 Z" fill="url(#bgClay)" stroke="#6B2E12" stroke-width="3.5"/>'
            '<path d="M -50 0 C -62 50 -40 86 0 88 C 40 86 62 50 50 0 C 40 -18 -40 -18 -50 0 Z" fill="url(#bgClay)" stroke="#6B2E12" stroke-width="4"/>'
            '<path d="M -48 18 C -20 30 20 30 48 18" stroke="#FFC93C" stroke-width="6" fill="none"/>'
            '<path d="M -44 52 C -16 64 16 64 44 52" stroke="#FFF6E0" stroke-width="4" fill="none" stroke-dasharray="2 9" stroke-linecap="round"/>'
            '<g fill="#FFF6E0"><circle cx="0" cy="40" r="6"/><circle cx="-14" cy="40" r="4"/><circle cx="14" cy="40" r="4"/><circle cx="0" cy="27" r="4"/><circle cx="0" cy="53" r="4"/></g>'
            '<circle cx="0" cy="40" r="3" fill="#E2412E"/>'
            '<ellipse cx="0" cy="-8" rx="36" ry="10" fill="#A9542A" stroke="#6B2E12" stroke-width="3.5"/>'
            '<path d="M -30 -10 C -26 -32 26 -32 30 -10" fill="url(#bgClay)" stroke="#6B2E12" stroke-width="3.5"/>'
            '<circle cx="0" cy="-30" r="7" fill="url(#bgGold)" stroke="#9A5B00" stroke-width="2.5"/>'
            '</g>')


def svg(cls="bhag", idp="bg"):
    out = f"""<svg class="{cls}" viewBox="0 0 600 740" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Gauri Maa giving a blessing on Karwa Chauth">
<defs>
  <radialGradient id="bgHalo" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#FFF6C2" stop-opacity=".95"/><stop offset=".55" stop-color="#FFD25A" stop-opacity=".55"/><stop offset="1" stop-color="#FFB300" stop-opacity="0"/></radialGradient>
  <radialGradient id="bgFace" cx="45%" cy="38%" r="68%"><stop offset="0" stop-color="#FFDDBF"/><stop offset="1" stop-color="#EFAE7E"/></radialGradient>
  <linearGradient id="bgSkin" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F8C9A0"/><stop offset="1" stop-color="#E8A577"/></linearGradient>
  <linearGradient id="bgGold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE680"/><stop offset=".5" stop-color="#FFC93C"/><stop offset="1" stop-color="#E39B12"/></linearGradient>
  <linearGradient id="bgRed" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E8344F"/><stop offset="1" stop-color="#A80C25"/></linearGradient>
  <linearGradient id="bgChunri" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E02442"/><stop offset="1" stop-color="#9E0A22"/></linearGradient>
  <linearGradient id="bgClay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E88A4E"/><stop offset="1" stop-color="#B5552A"/></linearGradient>
  <linearGradient id="bgPetal" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFB3CC"/><stop offset="1" stop-color="#E8507F"/></linearGradient>
  <linearGradient id="bgPetalLight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE0EA"/><stop offset="1" stop-color="#FF8FB1"/></linearGradient>
  <radialGradient id="bgGlow" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#FFFBE0" stop-opacity="1"/><stop offset="1" stop-color="#FFD54F" stop-opacity="0"/></radialGradient>
  <radialGradient id="bgMoon" cx="40%" cy="40%" r="70%"><stop offset="0" stop-color="#FFFDF0"/><stop offset="1" stop-color="#FFE9A8"/></radialGradient>
  <mask id="bgCres"><rect width="600" height="740" fill="#fff"/><circle cx="512" cy="96" r="52" fill="#000"/></mask>
  {mouth_defs()}
</defs>
<g class="halo"><circle cx="300" cy="300" r="276" fill="url(#bgHalo)"/>
  <g stroke="#FFD54F" stroke-width="7" stroke-linecap="round" opacity=".6">{_rays()}</g></g>
<g class="glow"><circle cx="486" cy="112" r="92" fill="url(#bgGlow)"/></g>
<circle cx="486" cy="112" r="58" fill="url(#bgMoon)" stroke="#E0B54A" stroke-width="3" mask="url(#bgCres)"/>
{_stars()}
<g class="float">
  {_lotus()}
  <!-- chunri falling behind the head down to the shoulders -->
  <path d="M 300 150 C 186 150 150 236 156 330 C 160 410 168 470 188 548 L 412 548 C 432 470 440 410 444 330 C 450 236 414 150 300 150 Z" fill="url(#bgChunri)" stroke="#7A0618" stroke-width="4"/>
  <path d="M 300 162 C 196 162 164 240 170 330 C 174 408 182 468 200 540 M 300 162 C 404 162 436 240 430 330 C 426 408 418 468 400 540" stroke="url(#bgGold)" stroke-width="10" fill="none"/>
  <g fill="#FFD54F">{"".join(f'<circle cx="{x}" cy="{y}" r="4"/>' for x, y in [(196, 300), (190, 380), (198, 460), (404, 300), (410, 380), (402, 460), (224, 220), (376, 220)])}</g>
  <!-- body: red blouse and saree -->
  <path d="M 226 446 C 250 428 350 428 374 446 L 390 560 C 360 582 240 582 210 560 Z" fill="url(#bgRed)" stroke="{INK}" stroke-width="4"/>
  <path d="M 246 446 C 268 486 332 486 354 446 C 336 458 264 458 246 446 Z" fill="url(#bgSkin)" stroke="{INK}" stroke-width="3"/>
  <path d="M 340 444 C 312 500 270 540 214 556" stroke="url(#bgGold)" stroke-width="12" fill="none" stroke-linecap="round"/>
  <!-- necklace and mangalsutra -->
  <path d="M 252 452 C 268 494 332 494 348 452" stroke="url(#bgGold)" stroke-width="9" fill="none" stroke-linecap="round"/>
  <path d="M 262 456 C 276 510 324 510 338 456" stroke="#1B1B1B" stroke-width="5" fill="none" stroke-dasharray="1 6" stroke-linecap="round"/>
  <path d="M 292 504 L 300 520 L 308 504 Z" fill="url(#bgGold)" stroke="#9A5B00" stroke-width="2.5"/>
  <circle cx="300" cy="484" r="9" fill="#2E9D4F" stroke="#C77C00" stroke-width="3"/>
  <path d="M 214 548 C 260 568 340 568 386 548 L 389 574 C 340 594 260 594 211 574 Z" fill="url(#bgGold)" stroke="#9A5B00" stroke-width="3"/>
  <path d="M 148 622 C 148 560 220 546 300 546 C 380 546 452 560 452 622 C 452 656 380 670 300 670 C 220 670 148 656 148 622 Z" fill="url(#bgRed)" stroke="#7A0618" stroke-width="4"/>
  <path d="M 160 634 C 230 658 370 658 440 634" stroke="url(#bgGold)" stroke-width="10" fill="none" stroke-linecap="round"/>
  <g fill="#FFD54F" opacity=".9">{"".join(f'<circle cx="{x}" cy="{604 + (abs(x - 300) // 30) % 2 * 18}" r="4"/>' for x in range(190, 420, 30))}</g>
  <!-- left arm (viewer's right) holding the karwa -->
  {_sleeve("M 368 456 Q 412 476 420 520")}
  {_arm("M 420 528 L 432 560", 38)}
  {_bangles(424, 538, 432, 566)}
  {_karwa(452, 548)}
  <circle cx="420" cy="586" r="22" fill="{SKIN}" stroke="{INK}" stroke-width="4"/>
  <!-- right hand: blessing, with mehendi and bangles -->
  <circle class="glow" cx="196" cy="414" r="78" fill="url(#bgGlow)"/>
  {_sleeve("M 232 458 Q 212 486 208 512")}
  {_arm("M 206 522 L 200 492", 38)}
  {_bangles(200, 500, 202, 476)}
  {_palm(198, 432)}
  <!-- hair -->
  <path d="M 192 322 C 176 214 236 176 300 176 C 364 176 424 214 408 322 L 420 420 C 400 396 396 360 394 336 L 206 336 C 204 360 200 396 180 420 Z" fill="#1B1414"/>
  <circle cx="190" cy="320" r="20" fill="{SKIN}" stroke="{INK}" stroke-width="4"/>
  <circle cx="410" cy="320" r="20" fill="{SKIN}" stroke="{INK}" stroke-width="4"/>
  <circle cx="300" cy="306" r="112" fill="url(#bgFace)" stroke="{INK}" stroke-width="4"/>
  <!-- hair parted in the middle, with sindoor in the parting -->
  <path d="M 196 266 C 206 214 252 196 300 196 C 348 196 394 214 404 266 C 380 236 340 222 304 222 L 300 232 L 296 222 C 260 222 220 236 196 266 Z" fill="#1B1414"/>
  <path d="M 300 198 L 300 230" stroke="#E2121E" stroke-width="6" stroke-linecap="round"/>
  <!-- crown (mukut) -->
  <path d="M 236 204 C 244 176 262 162 270 140 C 278 122 290 108 300 84 C 310 108 322 122 330 140 C 338 162 356 176 364 204 C 336 194 264 194 236 204 Z" fill="url(#bgGold)" stroke="#9A5B00" stroke-width="4"/>
  <path d="M 252 174 C 276 166 324 166 348 174 M 266 144 C 284 138 316 138 334 144" stroke="#C77C00" stroke-width="3" fill="none"/>
  <ellipse cx="300" cy="160" rx="12" ry="16" fill="#E2412E" stroke="#8E1B1B" stroke-width="3"/>
  <ellipse cx="296" cy="154" rx="3.5" ry="5" fill="#fff" opacity=".8"/>
  <circle cx="264" cy="186" r="7" fill="#2E9D4F" stroke="#145A2A" stroke-width="2"/>
  <circle cx="336" cy="186" r="7" fill="#2E9D4F" stroke="#145A2A" stroke-width="2"/>
  <circle cx="300" cy="80" r="9" fill="#E2412E" stroke="#C77C00" stroke-width="3"/>
  <!-- maang tikka -->
  <path d="M 300 230 L 300 238" stroke="#C77C00" stroke-width="3"/>
  <circle cx="300" cy="246" r="9" fill="url(#bgGold)" stroke="#9A5B00" stroke-width="2.5"/>
  <circle cx="300" cy="246" r="3.5" fill="#E2412E"/>
  <!-- jhumka earrings -->
  <path d="M 190 340 L 190 352" stroke="#C77C00" stroke-width="3"/><path d="M 176 368 C 176 350 204 350 204 368 Z" fill="url(#bgGold)" stroke="#9A5B00" stroke-width="3"/>
  <g fill="#FFD54F" stroke="#9A5B00" stroke-width="1.5"><circle cx="180" cy="374" r="4"/><circle cx="190" cy="376" r="4"/><circle cx="200" cy="374" r="4"/></g>
  <path d="M 410 340 L 410 352" stroke="#C77C00" stroke-width="3"/><path d="M 396 368 C 396 350 424 350 424 368 Z" fill="url(#bgGold)" stroke="#9A5B00" stroke-width="3"/>
  <g fill="#FFD54F" stroke="#9A5B00" stroke-width="1.5"><circle cx="400" cy="374" r="4"/><circle cx="410" cy="376" r="4"/><circle cx="420" cy="374" r="4"/></g>
  <!-- brows, bindi -->
  <path d="M 240 280 Q 262 268 284 278 M 316 278 Q 338 268 360 280" stroke="#1B1414" stroke-width="5" fill="none" stroke-linecap="round"/>
  <circle cx="300" cy="272" r="8" fill="#D3122A"/>
  <circle cx="300" cy="272" r="2.5" fill="#FFD54F"/>
  <g class="eyes">
  <path d="M 234 308 Q 263 286 292 308 Q 263 324 234 308 Z" fill="#fff" stroke="#1B1414" stroke-width="4.5"/>
  <path d="M 308 308 Q 337 286 366 308 Q 337 324 308 308 Z" fill="#fff" stroke="#1B1414" stroke-width="4.5"/>
  <circle cx="264" cy="307" r="12" fill="#2B1B12"/><circle cx="336" cy="307" r="12" fill="#2B1B12"/>
  <circle cx="268" cy="302" r="4.5" fill="#fff"/><circle cx="340" cy="302" r="4.5" fill="#fff"/>
  <path d="M 236 304 L 222 294 M 240 299 L 230 288 M 364 304 L 378 294 M 360 299 L 370 288" stroke="#1B1414" stroke-width="4" stroke-linecap="round"/>
  </g>
  <path d="M 296 320 Q 301 334 307 326" stroke="{SKIN_D}" stroke-width="3.5" fill="none" stroke-linecap="round"/>
  <!-- nath (nose ring) with its chain to the ear -->
  <circle cx="287" cy="334" r="8" fill="none" stroke="url(#bgGold)" stroke-width="3"/>
  <circle cx="280" cy="338" r="2.6" fill="#E2412E"/>
  <path d="M 280 336 C 250 352 220 340 198 330" stroke="#E0A92A" stroke-width="2" fill="none" stroke-dasharray="2 3"/>
  <circle cx="238" cy="346" r="17" fill="#FF7F8F" opacity=".38"/><circle cx="362" cy="346" r="17" fill="#FF7F8F" opacity=".38"/>
  {mouths(skin="#F0B488", lip="#C2416A", rest="#C2304F")}
</g>
</svg>"""
    return finish(out, idp)
