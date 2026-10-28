"""The festival cartoon: a friendly, respectful Satyanarayan Bhagwan (Vishnu) giving a blessing.

Follows the hooks described in engine/face.py (float, eyes, mouths, ids starting with "bg").
"""
import math

from face import finish, mouth_defs, mouths

INK = "#1d2b5a"
SKIN = "#4A80E6"


def _rays():
    out = []
    for k in range(24):
        a = math.radians(k * 15)
        x1, y1 = 300 + 150 * math.cos(a), 300 + 150 * math.sin(a)
        x2, y2 = 300 + 262 * math.cos(a), 300 + 262 * math.sin(a)
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>')
    return "".join(out)


PETAL = "M 0 0 C -40 -22 -42 -88 0 -124 C 42 -88 40 -22 0 0 Z"


def _lotus():
    back = "".join(f'<path d="{PETAL}" transform="translate(300 706) rotate({a}) scale(1.05)"/>' for a in (-72, -48, -24, 0, 24, 48, 72))
    front = "".join(f'<path d="{PETAL}" transform="translate(300 716) rotate({a}) scale(.86)"/>' for a in (-58, -30, 0, 30, 58))
    return (f'<g fill="url(#bgPetal)" stroke="#B8336A" stroke-width="3">{back}</g>'
            f'<g fill="url(#bgPetalLight)" stroke="#B8336A" stroke-width="3">{front}</g>')


def _garland():
    p0, p1, p2 = (236, 452), (300, 668), (364, 452)
    cols = ["#E2412E", "#FFF8E7", "#FF8F1F"]
    out = [f'<path d="M {p0[0]} {p0[1]} Q {p1[0]} {p1[1]} {p2[0]} {p2[1]}" stroke="#2E7D32" stroke-width="4" fill="none"/>']
    n = 13
    for i in range(n):
        t = i / (n - 1)
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
        c = cols[i % 3]
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="{c}" stroke="#7a2a12" stroke-width="2.5"/>'
                   f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="#FFD54F"/>')
    return "".join(out)


def _arm(d, width=42):
    return (f'<path d="{d}" stroke="{INK}" stroke-width="{width + 8}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" stroke="{SKIN}" stroke-width="{width}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')


def _chakra(cx, cy):
    flames = []
    for k in range(16):
        a = math.radians(k * 22.5)
        b1, b2 = a - math.radians(9), a + math.radians(9)
        p = [(cx + 46 * math.cos(b1), cy + 46 * math.sin(b1)), (cx + 64 * math.cos(a), cy + 64 * math.sin(a)),
             (cx + 46 * math.cos(b2), cy + 46 * math.sin(b2))]
        flames.append('<polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in p) + '"/>')
    spokes = "".join(
        f'<line x1="{cx + 9 * math.cos(math.radians(k * 45)):.1f}" y1="{cy + 9 * math.sin(math.radians(k * 45)):.1f}" '
        f'x2="{cx + 30 * math.cos(math.radians(k * 45)):.1f}" y2="{cy + 30 * math.sin(math.radians(k * 45)):.1f}"/>'
        for k in range(8))
    return (f'<g class="chakra"><g fill="#FF9F1A" stroke="#C25E00" stroke-width="2">{"".join(flames)}</g>'
            f'<circle cx="{cx}" cy="{cy}" r="48" fill="url(#bgGold)" stroke="#9A5B00" stroke-width="4"/>'
            f'<circle cx="{cx}" cy="{cy}" r="31" fill="#FFF1A8" stroke="#C77C00" stroke-width="3"/>'
            f'<g stroke="#C77C00" stroke-width="4" stroke-linecap="round">{spokes}</g>'
            f'<circle cx="{cx}" cy="{cy}" r="9" fill="#E2412E" stroke="#8E1B1B" stroke-width="2"/></g>')


def _palm(x, y):
    fingers = [(-28, -48, 14, 44), (-13, -58, 14, 54), (2, -56, 14, 52), (17, -46, 14, 42)]
    f = "".join(f'<rect x="{fx}" y="{fy}" width="{w}" height="{h}" rx="7"/>' for fx, fy, w, h in fingers)
    return (f'<g transform="translate({x} {y})" fill="{SKIN}" stroke="{INK}" stroke-width="3.5">'
            f'{f}<ellipse cx="36" cy="6" rx="10" ry="20" transform="rotate(28 36 6)"/>'
            '<rect x="-31" y="-14" width="64" height="58" rx="22"/>'
            '<circle cx="1" cy="14" r="6.5" fill="#E2412E" stroke="none"/></g>')


def svg(cls="bhag", idp="bg"):
    out = f"""<svg class="{cls}" viewBox="0 0 600 740" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Satyanarayan Bhagwan giving a blessing">
<defs>
  <radialGradient id="bgHalo" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#FFF6C2" stop-opacity=".95"/><stop offset=".55" stop-color="#FFD25A" stop-opacity=".55"/><stop offset="1" stop-color="#FFB300" stop-opacity="0"/></radialGradient>
  <linearGradient id="bgSkin" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5E95F2"/><stop offset="1" stop-color="#3567CF"/></linearGradient>
  <radialGradient id="bgFace" cx="45%" cy="38%" r="68%"><stop offset="0" stop-color="#76A9F8"/><stop offset="1" stop-color="#3A6ED6"/></radialGradient>
  <linearGradient id="bgGold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE680"/><stop offset=".5" stop-color="#FFC93C"/><stop offset="1" stop-color="#E39B12"/></linearGradient>
  <linearGradient id="bgCloth" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE14D"/><stop offset="1" stop-color="#F5A70F"/></linearGradient>
  <linearGradient id="bgPetal" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFB3CC"/><stop offset="1" stop-color="#E8507F"/></linearGradient>
  <linearGradient id="bgPetalLight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE0EA"/><stop offset="1" stop-color="#FF8FB1"/></linearGradient>
  <radialGradient id="bgGlow" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#FFFBE0" stop-opacity="1"/><stop offset="1" stop-color="#FFD54F" stop-opacity="0"/></radialGradient>
  {mouth_defs()}
</defs>
<g class="halo"><circle cx="300" cy="300" r="276" fill="url(#bgHalo)"/>
  <g stroke="#FFD54F" stroke-width="7" stroke-linecap="round" opacity=".6">{_rays()}</g></g>
<g class="float">
  {_lotus()}
  <!-- back arms: conch and chakra -->
  {_arm("M 236 452 Q 166 430 122 336")}
  <circle cx="118" cy="324" r="27" fill="{SKIN}" stroke="{INK}" stroke-width="4"/>
  <g transform="translate(104 300) rotate(-24)">
    <path d="M 0 0 C 34 -10 50 -44 32 -70 C 18 -90 -10 -84 -16 -62 C -22 -40 -10 -18 0 0 Z" fill="#FFFDF6" stroke="#7d8496" stroke-width="4"/>
    <path d="M 8 -62 C 22 -60 26 -46 16 -39 C 9 -35 2 -42 7 -48" stroke="#aab0bf" stroke-width="3.5" fill="none" stroke-linecap="round"/>
    <path d="M -6 -12 C 6 -8 18 -10 26 -20" stroke="#FFC93C" stroke-width="6" fill="none" stroke-linecap="round"/>
  </g>
  {_arm("M 364 452 Q 434 430 478 336")}
  <rect x="476" y="268" width="13" height="44" rx="6.5" fill="{SKIN}" stroke="{INK}" stroke-width="3.5"/>
  <circle cx="482" cy="324" r="27" fill="{SKIN}" stroke="{INK}" stroke-width="4"/>
  {_chakra(482, 236)}
  <!-- body -->
  <path d="M 226 446 C 250 428 350 428 374 446 L 390 560 C 360 582 240 582 210 560 Z" fill="url(#bgSkin)" stroke="{INK}" stroke-width="4"/>
  <path d="M 252 448 C 296 498 330 522 370 556" stroke="#FFFDF6" stroke-width="5" fill="none"/>
  <path d="M 252 446 C 268 488 332 488 348 446" stroke="url(#bgGold)" stroke-width="12" fill="none" stroke-linecap="round"/>
  <circle cx="300" cy="486" r="13" fill="#E2412E" stroke="#C77C00" stroke-width="4"/>
  {_garland()}
  <path d="M 214 548 C 260 568 340 568 386 548 L 389 574 C 340 594 260 594 211 574 Z" fill="url(#bgGold)" stroke="#9A5B00" stroke-width="3"/>
  <path d="M 148 622 C 148 560 220 546 300 546 C 380 546 452 560 452 622 C 452 656 380 670 300 670 C 220 670 148 656 148 622 Z" fill="url(#bgCloth)" stroke="#9A5B00" stroke-width="4"/>
  <path d="M 160 634 C 230 658 370 658 440 634" stroke="#E2412E" stroke-width="10" fill="none" stroke-linecap="round"/>
  <path d="M 168 612 C 236 630 364 630 432 612" stroke="#FFF1A8" stroke-width="4" fill="none" stroke-linecap="round" opacity=".7"/>
  <!-- gada (mace) in the front right hand -->
  <line x1="452" y1="648" x2="452" y2="436" stroke="#9A5B00" stroke-width="17" stroke-linecap="round"/>
  <line x1="452" y1="648" x2="452" y2="436" stroke="#FFC93C" stroke-width="11" stroke-linecap="round"/>
  <circle cx="452" cy="408" r="35" fill="url(#bgGold)" stroke="#9A5B00" stroke-width="4"/>
  <path d="M 432 386 C 426 400 426 416 432 430 M 452 374 L 452 442 M 472 386 C 478 400 478 416 472 430" stroke="#C77C00" stroke-width="3.5" fill="none"/>
  <circle cx="452" cy="368" r="9" fill="#E2412E" stroke="#9A5B00" stroke-width="3"/>
  {_arm("M 364 466 L 398 536 L 440 540", 40)}
  <circle cx="450" cy="540" r="24" fill="{SKIN}" stroke="{INK}" stroke-width="4"/>
  <path d="M 420 528 L 424 552" stroke="#FFC93C" stroke-width="11" stroke-linecap="round"/>
  <!-- blessing hand (abhaya mudra) -->
  <circle class="glow" cx="196" cy="414" r="78" fill="url(#bgGlow)"/>
  {_arm("M 236 466 L 204 540 L 196 478", 40)}
  <path d="M 180 484 L 212 480" stroke="#FFC93C" stroke-width="12" stroke-linecap="round"/>
  {_palm(194, 430)}
  <!-- head -->
  <path d="M 186 318 C 170 210 236 168 300 168 C 364 168 430 210 414 318 L 426 412 C 404 386 400 356 398 334 L 202 334 C 200 356 196 386 174 412 Z" fill="#1B2340"/>
  <circle cx="190" cy="318" r="22" fill="{SKIN}" stroke="{INK}" stroke-width="4"/>
  <circle cx="410" cy="318" r="22" fill="{SKIN}" stroke="{INK}" stroke-width="4"/>
  <circle cx="300" cy="306" r="112" fill="url(#bgFace)" stroke="{INK}" stroke-width="4"/>
  <path d="M 198 256 C 240 238 360 238 402 256 C 384 264 364 266 342 262 C 322 270 278 270 258 262 C 236 266 216 264 198 256 Z" fill="#1B2340"/>
  <!-- crown (kirit mukut) -->
  <path d="M 214 224 C 222 172 250 152 262 122 C 270 100 286 86 300 54 C 314 86 330 100 338 122 C 350 152 378 172 386 224 Z" fill="url(#bgGold)" stroke="#9A5B00" stroke-width="4"/>
  <path d="M 228 188 C 260 174 340 174 372 188 M 246 148 C 276 138 324 138 354 148" stroke="#C77C00" stroke-width="3.5" fill="none"/>
  <path d="M 192 254 C 240 228 360 228 408 254 L 404 224 C 356 200 244 200 196 224 Z" fill="url(#bgGold)" stroke="#9A5B00" stroke-width="3"/>
  <circle cx="197" cy="246" r="13" fill="url(#bgGold)" stroke="#9A5B00" stroke-width="3"/><circle cx="403" cy="246" r="13" fill="url(#bgGold)" stroke="#9A5B00" stroke-width="3"/>
  <circle cx="197" cy="246" r="5" fill="#E2412E"/><circle cx="403" cy="246" r="5" fill="#E2412E"/>
  <g fill="#FFFDF6" stroke="#C77C00" stroke-width="1.5">{"".join(f'<circle cx="{x}" cy="{238 - 16 * (1 - ((x - 300) / 110) ** 2):.1f}" r="5"/>' for x in range(212, 400, 22))}</g>
  <ellipse cx="300" cy="164" rx="15" ry="20" fill="#E2412E" stroke="#8E1B1B" stroke-width="3"/>
  <ellipse cx="295" cy="157" rx="4" ry="6" fill="#fff" opacity=".8"/>
  <circle cx="258" cy="202" r="9" fill="#2E9D4F" stroke="#145A2A" stroke-width="2.5"/>
  <circle cx="342" cy="202" r="9" fill="#2E9D4F" stroke="#145A2A" stroke-width="2.5"/>
  <circle cx="300" cy="110" r="8" fill="#E2412E" stroke="#8E1B1B" stroke-width="2.5"/>
  <circle cx="300" cy="48" r="10" fill="#E2412E" stroke="#C77C00" stroke-width="3"/>
  <!-- earrings -->
  <circle cx="190" cy="350" r="14" fill="url(#bgGold)" stroke="#9A5B00" stroke-width="3"/><circle cx="190" cy="372" r="6" fill="#E2412E"/>
  <circle cx="410" cy="350" r="14" fill="url(#bgGold)" stroke="#9A5B00" stroke-width="3"/><circle cx="410" cy="372" r="6" fill="#E2412E"/>
  <!-- face -->
  <path d="M 236 278 Q 262 264 284 276 M 316 276 Q 338 264 364 278" stroke="#1B2340" stroke-width="6" fill="none" stroke-linecap="round"/>
  <path d="M 288 238 L 291 282 Q 300 294 309 282 L 312 238" stroke="#FFFDF6" stroke-width="6" fill="none" stroke-linejoin="round"/>
  <line x1="300" y1="246" x2="300" y2="283" stroke="#E2412E" stroke-width="5" stroke-linecap="round"/>
  <g class="eyes">
  <path d="M 232 308 Q 262 284 292 308 Q 262 326 232 308 Z" fill="#fff" stroke="#1B2340" stroke-width="4"/>
  <path d="M 308 308 Q 338 284 368 308 Q 338 326 308 308 Z" fill="#fff" stroke="#1B2340" stroke-width="4"/>
  <circle cx="264" cy="307" r="12.5" fill="#2B1B12"/><circle cx="336" cy="307" r="12.5" fill="#2B1B12"/>
  <circle cx="268.5" cy="302" r="4.5" fill="#fff"/><circle cx="340.5" cy="302" r="4.5" fill="#fff"/>
  <path d="M 233 306 L 220 299 M 367 306 L 380 299" stroke="#1B2340" stroke-width="4" stroke-linecap="round"/>
  </g>
  <path d="M 296 322 Q 301 336 307 327" stroke="#2A4FA8" stroke-width="3.5" fill="none" stroke-linecap="round"/>
  <circle cx="238" cy="346" r="17" fill="#FF7FA8" opacity=".38"/><circle cx="362" cy="346" r="17" fill="#FF7FA8" opacity=".38"/>
  {mouths()}
</g>
</svg>"""
    return finish(out, idp)
