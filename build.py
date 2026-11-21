#!/usr/bin/env python3
"""Eskişehir Evlilik Teklifi — statik site üreticisi.

Kullanım:
    python3 build.py            # dist/site (yayın) + dist/onizleme (önizleme)
Alan adı, telefon, GTM kimliği gibi her şey CONFIG içinde. E-posta adresi
SITE_EMAIL ortam değişkeninden okunur (boşsa sitede gösterilmez).
Fotoğraflar fotograflar/<galeri>/<dosya-adi>.jpg olarak konursa WebP'ye
çevrilir; galerilere, schema'ya ve görsel sitemap'e otomatik eklenir.
"""
import html, json, os, re, shutil, urllib.parse
from pathlib import Path

ROOT = Path(__file__).parent
CONFIG = dict(
    BASE="https://www.eskisehirevlilikteklifi.com/",
    ESKI_ALAN_ADLARI=[],   # eski Wix sitesi yayında kalıyor. İleride kapatıp yeni siteye yönlendirmek isterseniz: ["eskisehirevlilikteklifi.com.tr"]
    BRAND="Eskişehir Evlilik Teklifi",
    PARENT="The Vine Organizasyon",
    PARENT_URL="https://thevineorganizasyon.com.tr/",
    WA="905321531726",
    TEL1="+905321531726", TEL1_TXT="0532 153 17 26",
    TEL2="+905366751612", TEL2_TXT="0536 675 16 12",
    EMAIL=os.environ.get("SITE_EMAIL", ""),
    ADDR_STREET="İstiklal Mah. İki Eylül Cad. No:28/B, Gökdemir İş Merkezi Kat:2 No:73",
    ADDR_CITY="Odunpazarı/Eskişehir", ADDR_LOCALITY="Odunpazarı", ADDR_POST="26010",
    INSTAGRAM="https://www.instagram.com/eskisehirevlilikteklificom/",
    INSTAGRAM_TXT="@eskisehirevlilikteklificom",
    YOUTUBE="https://www.youtube.com/channel/UCCRGhy0iTrnocIUZMVK3LrA",
    INSTAGRAM_VINE="https://www.instagram.com/thevineorganizasyon/",
    YOUTUBE_VINE="https://www.youtube.com/@thevineorganizasyon",
    GTM_ID="GTM-XXXXXXX",      # Google Tag Manager kimliğiniz
    GSC_TOKEN="",              # Search Console HTML etiketi doğrulama kodu (isteğe bağlı)
    DATE="2026-11-20",
)
C = CONFIG
FONTS = ("https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,400;1,500"
         "&family=Great+Vibes&family=Manrope:wght@400;500;600;700&display=swap")


def esc(s):
    return html.escape(s, quote=True)


def strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


def wa(text):
    return "https://wa.me/%s?text=%s" % (C["WA"], urllib.parse.quote(text))


class Ctx:
    def __init__(self, slug, mode, absolute=False):
        self.slug, self.mode = slug, mode
        self.depth = len([x for x in slug.split("/") if x]) if slug else 0
        self.P = "../" * self.depth
        self.absolute = absolute and mode == "prod"   # 404 sayfası her adreste çalışsın
        if self.absolute:
            self.P = "/"

    def L(self, target=""):
        if self.absolute:
            return "/" + (target + "/" if target else "")
        if self.mode == "prod":
            u = self.P + (target + "/" if target else "")
            return u or "./"
        return self.P + (target + "/index.html" if target else "index.html")

    def A(self, path):
        return self.P + path


IC_SOHBET = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 12a8 8 0 0 1-11.6 7.1L4 20l1-4.1A8 8 0 1 1 20 12z"/><path d="M9 10.5h6M9 13.5h4"/></svg>'
IC_TEL = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 4h3l1.5 4-2 1.2a11 11 0 0 0 5.3 5.3l1.2-2 4 1.5v3a2 2 0 0 1-2.2 2A16 16 0 0 1 3 6.2 2 2 0 0 1 5 4z"/></svg>'


# ------------------------------------------------------------------ çizimler
def defs(u):
    return f'''<defs>
<radialGradient id="{u}a" cx="50%" cy="45%" r="55%"><stop offset="0" stop-color="#FFF4D6"/><stop offset=".45" stop-color="#E3C78E"/><stop offset="1" stop-color="#E3C78E" stop-opacity="0"/></radialGradient>
<filter id="{u}p" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<linearGradient id="{u}s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FBE6BF" stop-opacity=".95"/><stop offset="1" stop-color="#F3C67E" stop-opacity=".55"/></linearGradient>
</defs>'''


def stars(pts):
    return "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FBE6BF" opacity="{o}"/>' for x, y, r, o in pts)


def swag(u, x1, y1, x2, y2, sag, n, r=3.2):
    cx, cy = (x1 + x2) / 2, max(y1, y2) + sag
    out = [f'<path d="M{x1},{y1} Q{cx},{cy} {x2},{y2}" fill="none" stroke="#B9A98C" stroke-opacity=".55" stroke-width="1"/>']
    for i in range(1, n + 1):
        t = i / (n + 1)
        x = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * cx + t ** 2 * x2
        y = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * cy + t ** 2 * y2
        out.append(f'<circle cx="{x:.1f}" cy="{y + 3:.1f}" r="{r * 2.6:.1f}" fill="url(#{u}a)" opacity=".55"/>'
                   f'<circle cx="{x:.1f}" cy="{y + 3:.1f}" r="{r * .55:.1f}" fill="#FFF4D6"/>')
    return "".join(out)


def ill_balon(u):
    hexes = "".join(f'<path d="M{x-14},{y} l7,-12 h14 l7,12 l-7,12 h-14z" fill="none" stroke="#FBE6BF" stroke-opacity=".22"/>'
                    for x, y in [(130,200),(158,184),(186,170),(214,184),(242,200),(144,224),(228,224),(172,146),(200,146),(150,168),(222,168),(186,122)])
    return f'''<svg viewBox="0 0 360 320" role="img" aria-label="Işıklarla süslenmiş şeffaf balon ev (kubbe) ve önünde kırmızı halı çizimi">{defs(u)}
{stars([(40,40,1.2,.7),(80,22,1,.5),(300,30,1.3,.8),(330,80,1,.5),(250,18,1,.6),(20,110,1,.4)])}
<ellipse cx="180" cy="262" rx="150" ry="16" fill="#F3C67E" opacity=".10"/>
<path d="M20 262 H340" stroke="#B9A98C" stroke-opacity=".35"/>
<path d="M92 260 A94 94 0 1 1 268 260 Z" fill="#E9B8C8" fill-opacity=".10" stroke="url(#{u}s)" stroke-width="1.6"/>
{hexes}
<path d="M112 160 A80 80 0 0 1 170 104" fill="none" stroke="#FFFFFF" stroke-opacity=".35" stroke-width="3" stroke-linecap="round"/>
<rect x="164" y="186" width="32" height="74" fill="#F3C67E" fill-opacity=".18" stroke="#FBE6BF" stroke-opacity=".8"/>
<path d="M170 204 h20" stroke="#E8708A" stroke-width="2.4" stroke-linecap="round" filter="url(#{u}p)"/>
<g filter="url(#{u}p)">{swag(u,-10,40,180,30,40,7,2.8)}{swag(u,180,30,370,40,40,7,2.8)}</g>
<path d="M164 260 L150 316 H210 L196 260Z" fill="#C2414F" opacity=".75"/>
<g fill="#FBE6BF" opacity=".95" font-family="Albert Sans,Arial" font-weight="700" font-size="22"><text x="44" y="256">MARRY</text><text x="258" y="256">ME</text></g>
<g fill="url(#{u}a)"><circle cx="138" cy="286" r="9"/><circle cx="222" cy="286" r="9"/><circle cx="118" cy="304" r="9"/><circle cx="242" cy="304" r="9"/></g>
</svg>'''


def ill_bungalov(u):
    return f'''<svg viewBox="0 0 360 320" role="img" aria-label="Işık zincirleriyle süslenmiş ahşap bungalov çizimi">{defs(u)}
{stars([(60,30,1.2,.7),(110,60,1,.5),(310,40,1.1,.6),(40,120,1,.4),(200,26,1,.5)])}
<path d="M292 46 a22 22 0 1 0 14 38 a17 17 0 1 1 -14 -38z" fill="#FBE6BF" opacity=".85"/>
<ellipse cx="180" cy="276" rx="150" ry="14" fill="#F3C67E" opacity=".10"/>
<path d="M20 276 H340" stroke="#B9A98C" stroke-opacity=".35"/>
<g fill="#4A3E6A"><path d="M40 270 L62 196 L84 270Z"/><path d="M48 230 L62 170 L76 230Z"/><path d="M282 270 L304 186 L326 270Z"/><path d="M290 226 L304 160 L318 226Z"/></g>
<path d="M98 268 L180 92 L262 268Z" fill="#2E2446" stroke="url(#{u}s)" stroke-width="1.6"/>
<path d="M126 268 L180 150 L234 268Z" fill="#F3C67E" fill-opacity=".22" stroke="#F3C67E" stroke-opacity=".6"/>
<path d="M180 150 V268 M153 209 H207" stroke="#F3C67E" stroke-opacity=".45"/>
<rect x="88" y="266" width="184" height="6" rx="2" fill="#F3C67E" opacity=".55"/>
<g filter="url(#{u}p)">{swag(u,104,252,180,98,10,7,2.8)}{swag(u,180,98,256,252,10,7,2.8)}</g>
<circle cx="180" cy="232" r="22" fill="url(#{u}a)" opacity=".7"/>
<rect x="110" y="246" width="8" height="18" rx="2" fill="#FBE6BF"/><circle cx="114" cy="243" r="8" fill="url(#{u}a)"/>
<rect x="242" y="246" width="8" height="18" rx="2" fill="#FBE6BF"/><circle cx="246" cy="243" r="8" fill="url(#{u}a)"/>
</svg>'''


def ill_karavan(u):
    return f'''<svg viewBox="0 0 360 320" role="img" aria-label="Işık zinciri tavanı altında vintage karavan ve LOVE harfleri çizimi">{defs(u)}
<g filter="url(#{u}p)">{swag(u,-10,20,120,60,30,5,2.6)}{swag(u,120,60,250,30,30,5,2.6)}{swag(u,250,30,370,64,30,5,2.6)}</g>
<ellipse cx="180" cy="266" rx="160" ry="14" fill="#F3C67E" opacity=".10"/>
<path d="M10 266 H350" stroke="#B9A98C" stroke-opacity=".35"/>
<path d="M40 248 V156 q0 -24 26 -24 h132 q26 0 34 24 l10 40 v52 Z" fill="#F3C67E" fill-opacity=".18" stroke="url(#{u}s)" stroke-width="1.6"/>
<path d="M40 192 H242" stroke="#FBE6BF" stroke-opacity=".5"/>
<g fill="#FBE6BF" fill-opacity=".28" stroke="#FBE6BF" stroke-opacity=".6"><rect x="54" y="146" width="40" height="34" rx="6"/><rect x="104" y="146" width="40" height="34" rx="6"/><rect x="154" y="146" width="40" height="34" rx="6"/></g>
<g fill="#FFF8EC" opacity=".8"><circle cx="70" cy="214" r="4"/><circle cx="120" cy="222" r="4"/><circle cx="176" cy="212" r="4"/></g>
<circle cx="82" cy="250" r="15" fill="#1F1830" stroke="#F3C67E" stroke-opacity=".75" stroke-width="1.6"/><circle cx="206" cy="250" r="15" fill="#1F1830" stroke="#F3C67E" stroke-opacity=".75" stroke-width="1.6"/>
<path d="M18 262 L30 206 L42 262" fill="none" stroke="#FBE6BF" stroke-opacity=".6"/><path d="M24 234 h12" stroke="#FBE6BF" stroke-opacity=".4"/>
<rect x="96" y="262" width="110" height="10" rx="2" fill="#C2414F" opacity=".55"/>
<g fill="none" stroke="#FFF4D6" stroke-width="5.5" stroke-linejoin="round" filter="url(#{u}p)"><path d="M254 216 V256 H270"/><ellipse cx="284" cy="236" rx="9" ry="20"/><path d="M299 216 L307 256 L315 216"/><path d="M338 216 H324 V256 H338 M324 236 H336"/></g>
</svg>'''


def ill_gondol(u):
    return f'''<svg viewBox="0 0 360 320" role="img" aria-label="Köprü altından geçen ışıklı gondol çizimi">{defs(u)}
{stars([(40,40,1.2,.7),(120,24,1,.5),(300,36,1.2,.7),(330,90,1,.4),(220,20,1,.5)])}
<path d="M0 118 H360" stroke="#B9A98C" stroke-opacity=".35"/>
<path d="M30 118 V200 M330 118 V200" stroke="#B9A98C" stroke-opacity=".4"/>
<path d="M30 200 Q180 96 330 200" fill="none" stroke="url(#{u}s)" stroke-width="1.6"/>
<g filter="url(#{u}p)">{swag(u,40,124,180,124,22,6,2.6)}{swag(u,180,124,320,124,22,6,2.6)}</g>
<rect x="0" y="232" width="360" height="88" fill="#2A2140"/>
<g stroke="#F3C67E" stroke-opacity=".25"><path d="M40 262 h40 M120 282 h60 M220 258 h50 M280 290 h40"/></g>
<path d="M78 236 Q180 262 290 236 L300 226 Q180 252 66 226 Z" fill="#14101F" stroke="#F3C67E" stroke-opacity=".7" stroke-width="1.4"/>
<path d="M300 226 q14 -8 12 -26" fill="none" stroke="#F3C67E" stroke-opacity=".7" stroke-width="1.4"/>
<path d="M232 230 V150 l-6 -8" fill="none" stroke="#B9A98C" stroke-opacity=".7"/>
<circle cx="160" cy="226" r="16" fill="url(#{u}a)" opacity=".7"/>
<path d="M160 208 c-5 -8 -16 -5 -13 5 c2 5 13 11 13 11 s11 -6 13 -11 c3 -10 -8 -13 -13 -5z" fill="#D7A6A4" opacity=".9"/>
</svg>'''


def ill_sato(u):
    return f'''<svg viewBox="0 0 360 320" role="img" aria-label="Masal şatosu silueti önünde ışıklı teklif alanı çizimi">{defs(u)}
{stars([(30,40,1.2,.7),(90,20,1,.5),(310,30,1.2,.7),(340,100,1,.4),(250,16,1,.5)])}
<ellipse cx="180" cy="274" rx="150" ry="14" fill="#F3C67E" opacity=".10"/><path d="M20 274 H340" stroke="#B9A98C" stroke-opacity=".35"/>
<g fill="#2E2446" stroke="url(#{u}s)" stroke-width="1.3">
<path d="M110 270 V150 h28 V270"/><path d="M106 150 L124 104 L142 150Z"/>
<path d="M222 270 V150 h28 V270"/><path d="M218 150 L236 104 L254 150Z"/>
<path d="M138 270 V176 h84 V270"/><path d="M160 176 V128 h40 V176"/><path d="M155 128 L180 72 L205 128Z"/></g>
<path d="M168 270 v-30 a12 12 0 0 1 24 0 v30" fill="#F3C67E" fill-opacity=".35" stroke="#F3C67E" stroke-opacity=".7"/>
<g fill="#F3C67E" opacity=".7"><rect x="119" y="170" width="10" height="16" rx="5"/><rect x="231" y="170" width="10" height="16" rx="5"/><rect x="175" y="140" width="10" height="16" rx="5"/></g>
<g filter="url(#{u}p)">{swag(u,40,208,110,196,16,4,2.6)}{swag(u,250,196,320,208,16,4,2.6)}</g>
<path d="M40 208 V272 M320 208 V272" stroke="#B9A98C" stroke-opacity=".5"/>
</svg>'''


def ill_kavak(u):
    trees = "".join(f'<path d="M{x} 270 V{y+40}" stroke="#6E5F8E" stroke-width="2"/><ellipse cx="{x}" cy="{y+20}" rx="{w}" ry="{h}" fill="#4A3E6A"/>'
                    for x, y, w, h in [(44,96,16,74),(86,70,18,92),(276,78,18,88),(318,104,15,70)])
    return f'''<svg viewBox="0 0 360 320" role="img" aria-label="Kavak ağaçları arasında ışıklı bank ve teklif alanı çizimi">{defs(u)}
{stars([(150,30,1.2,.7),(210,20,1,.5),(190,60,1,.4),(130,70,1,.5)])}
<ellipse cx="180" cy="276" rx="150" ry="14" fill="#F3C67E" opacity=".10"/><path d="M20 276 H340" stroke="#B9A98C" stroke-opacity=".35"/>
{trees}
<g filter="url(#{u}p)">{swag(u,86,150,180,140,40,6,2.8)}{swag(u,180,140,276,150,40,6,2.8)}</g>
<rect x="130" y="236" width="100" height="6" rx="2" fill="#F3C67E" opacity=".75"/>
<rect x="130" y="216" width="100" height="5" rx="2" fill="#F3C67E" opacity=".5"/>
<path d="M138 242 v28 M222 242 v28" stroke="#F3C67E" stroke-opacity=".6"/>
<g fill="#D7A6A4" opacity=".9"><circle cx="122" cy="266" r="7"/><circle cx="112" cy="268" r="5"/><circle cx="238" cy="266" r="7"/><circle cx="248" cy="268" r="5"/></g>
<circle cx="180" cy="200" r="20" fill="url(#{u}a)" opacity=".75"/>
<path d="M180 214 c-5 -8 -16 -5 -13 5 c2 5 13 11 13 11 s11 -6 13 -11 c3 -10 -8 -13 -13 -5z" fill="none" stroke="#F3C67E" stroke-width="1.3"/>
</svg>'''


def ill_yuzuk(u):
    return f'''<svg viewBox="0 0 360 320" role="img" aria-label="Açık yüzük kutusu ve ışıklar çizimi">{defs(u)}
{stars([(40,40,1.2,.7),(100,24,1,.5),(300,30,1.2,.7),(330,96,1,.4),(220,18,1,.5),(30,130,1,.4)])}
<g filter="url(#{u}p)">{swag(u,20,40,180,46,40,7,2.8)}{swag(u,180,46,340,40,40,7,2.8)}</g>
<ellipse cx="180" cy="270" rx="120" ry="12" fill="#F3C67E" opacity=".10"/>
<path d="M110 196 h140 v62 a8 8 0 0 1 -8 8 h-124 a8 8 0 0 1 -8 -8z" fill="#2E2446" stroke="url(#{u}s)" stroke-width="1.6"/>
<path d="M110 196 L122 128 h116 L250 196" fill="#3B3058" stroke="url(#{u}s)" stroke-width="1.6"/>
<rect x="128" y="206" width="104" height="30" rx="6" fill="#1F1830"/>
<circle cx="180" cy="196" r="34" fill="url(#{u}a)" opacity=".55"/>
<ellipse cx="180" cy="210" rx="20" ry="9" fill="none" stroke="#FBE6BF" stroke-width="3"/>
<path d="M172 196 l8 -12 l8 12 l-8 6z" fill="#FFF8EC" stroke="#F3C67E" stroke-width="1"/>
</svg>'''


def ill_ada(u):
    return f'''<svg viewBox="0 0 360 320" role="img" aria-label="Nehir üzerindeki adada ışıklı restoran ve köprü çizimi">{defs(u)}
{stars([(40,40,1.2,.7),(110,24,1,.5),(300,36,1.2,.7),(330,90,1,.4),(220,20,1,.5)])}
<rect x="0" y="236" width="360" height="84" fill="#2A2140"/>
<g stroke="#F3C67E" stroke-opacity=".25"><path d="M30 268 h40 M110 290 h60 M240 262 h50 M270 296 h40"/></g>
<path d="M150 236 q50 -12 150 0 q-60 14 -150 0z" fill="#3B3058"/>
<path d="M180 232 V176 h96 V232" fill="#2E2446" stroke="url(#{u}s)" stroke-width="1.6"/>
<path d="M172 178 L228 146 L284 178" fill="none" stroke="url(#{u}s)" stroke-width="1.6"/>
<g fill="#F3C67E" fill-opacity=".55"><rect x="192" y="190" width="18" height="24" rx="3"/><rect x="219" y="190" width="18" height="24" rx="3"/><rect x="246" y="190" width="18" height="24" rx="3"/></g>
<path d="M20 238 Q85 200 160 236" fill="none" stroke="url(#{u}s)" stroke-width="1.6"/>
<path d="M40 228 v10 M70 214 v24 M100 210 v26 M130 220 v16" stroke="#B9A98C" stroke-opacity=".5"/>
<g filter="url(#{u}p)">{swag(u,180,176,228,146,8,3,2.4)}{swag(u,228,146,276,176,8,3,2.4)}{swag(u,20,236,160,236,24,6,2.4)}</g>
<path d="M228 134 c-5 -8 -16 -5 -13 5 c2 5 13 11 13 11 s11 -6 13 -11 c3 -10 -8 -13 -13 -5z" fill="#D7A6A4" opacity=".9"/>
</svg>'''


ILL = dict(ada=ill_ada, balon=ill_balon, bungalov=ill_bungalov, karavan=ill_karavan, gondol=ill_gondol,
           sato=ill_sato, kavak=ill_kavak, yuzuk=ill_yuzuk)

CITIES = [  # ad, slug, km, yön (derece, şematik)
    ("Bozüyük", "bozuyuk-evlilik-teklifi", 45, 292),
    ("Bilecik", "bilecik-evlilik-teklifi", 80, 318),
    ("Kütahya", "kutahya-evlilik-teklifi", 80, 232),
    ("Afyonkarahisar", "afyon-evlilik-teklifi", 130, 192),
    ("Bursa", "bursa-evlilik-teklifi", 150, 268),
]


def map_svg(u, vurgu=None):
    import math
    cx, cy, k = 250, 140, 1.05
    parts = [f'<svg viewBox="0 0 400 320" role="img" aria-label="Eskişehir merkezli hizmet bölgesi şeması: Bozüyük, Bilecik, Kütahya, Afyonkarahisar ve Bursa">{defs(u)}']
    for r in (50, 100, 150):
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r*k:.0f}" fill="none" stroke="#E3C78E" stroke-opacity=".14" stroke-dasharray="2 5"/>')
    parts.append(f'<text x="{cx + 100*k + 4:.0f}" y="{cy - 4}" fill="#CDBDB6" font-size="10" font-family="Manrope,Arial">100 km</text>')
    for ad, slug, km, deg in CITIES:
        a = math.radians(deg)
        x, y = cx + km * k * math.sin(a), cy - km * k * math.cos(a)
        on = vurgu == slug
        parts.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.0f}" y2="{y:.0f}" stroke="#E3C78E" stroke-opacity="{.85 if on else .3}" stroke-width="{1.6 if on else 1}"/>')
        parts.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{6 if on else 4}" fill="{"#E3C78E" if on else "#EBD3A0"}"/>')
        anchor, dx, ly = "end", -10, y - 8
        if deg == 192:
            anchor, dx, ly = "middle", 0, y + 22
        elif deg == 232:
            ly = y + 18
        elif deg == 268:
            anchor, dx, ly = "start", -4, y + 20
        parts.append(f'<text x="{max(x+dx, 4) if anchor != "end" else max(x+dx, 60):.0f}" y="{ly:.0f}" text-anchor="{anchor}" fill="{"#FFF8F2" if on else "#E4D6CF"}" font-size="{14 if on else 13}" font-family="Manrope,Arial" font-weight="{600 if on else 500}">{ad}, {km} km</text>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="16" fill="url(#{u}a)"/><circle cx="{cx}" cy="{cy}" r="6" fill="#FFF4D6"/>')
    parts.append(f'<text x="{cx+14}" y="{cy+28}" fill="#FFF8F2" font-size="19" font-family="Cormorant Garamond,Georgia,serif">Eskişehir</text>')
    parts.append('</svg>')
    return "".join(parts)


def strand(u):
    out, i = [], 0
    segs = [(-20, 12, 480, 12, 70), (480, 12, 980, 12, 70), (980, 12, 1460, 12, 70)]
    out.append(f'<svg viewBox="0 0 1440 150" preserveAspectRatio="xMidYMin slice" aria-hidden="true">{defs(u)}')
    for x1, y1, x2, y2, sag in segs:
        cx, cy = (x1 + x2) / 2, y1 + sag
        out.append(f'<path d="M{x1},{y1} Q{cx},{cy} {x2},{y2}" fill="none" stroke="#B9A98C" stroke-opacity=".45" stroke-width="1"/>')
        n = 11
        for j in range(1, n + 1):
            t = j / (n + 1)
            x = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * cx + t ** 2 * x2
            y = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * cy + t ** 2 * y2
            out.append(f'<g class="ampul" style="--i:{i}"><line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{y+7:.1f}" stroke="#B9A98C" stroke-opacity=".6"/>'
                       f'<circle cx="{x:.1f}" cy="{y+12:.1f}" r="13" fill="url(#{u}a)" opacity=".6"/><circle cx="{x:.1f}" cy="{y+12:.1f}" r="3.4" fill="#FFF4D6"/></g>')
            i += 1
    out.append('</svg>')
    return '<div class="zincir">' + "".join(out) + '</div>'


# ------------------------------------------------------------------ fotoğraflar
# ------------------------------------------------------------------ düzenlenebilir veriler (yönetim paneli bu dosyaları değiştirir)
VERI = ROOT / "veri"


def oku(ad):
    return json.loads((VERI / f"{ad}.json").read_text(encoding="utf-8"))


def norm(yol):
    return (yol or "").strip().lstrip("/")


def R(ref):
    """Görsel referansını img()'e verilecek argümanlara çevirir: dosya yolu ya da (galeri, ad)."""
    if not ref:
        return ("",)
    return (ref,) if isinstance(ref, str) else tuple(ref)


_G = oku("galeri")
GALERI, GALERI_DOSYA = {}, {}
for _g in _G["galeriler"]:
    _slots = []
    for _f in _g.get("fotolar") or []:
        if not _f or not _f.get("dosya"):
            continue
        _ad = Path(norm(_f["dosya"])).stem
        _slots.append((_ad, (_f.get("aciklama") or "").strip() or _g["baslik"]))
        GALERI_DOSYA[(_g["kod"], _ad)] = norm(_f["dosya"])
    GALERI[_g["kod"]] = (_g["baslik"], None, _slots)

GORSEL = oku("gorseller")

VIDEOS = {
    "teklif": dict(dosya="assets/video/balon-ev-evlilik-teklifi-eskisehir.mp4", poster="assets/video/balon-ev-evlilik-teklifi-eskisehir-poster.webp",
                   ad="Balon ev önünde evlilik teklifi, Eskişehir", aciklama="Işıklı MARRY ME harfleri ve kırmızı halıyla hazırlanan balon ev evlilik teklifi alanında evet anı.",
                   sure="PT10S", w=832, h=372),
    "reels": dict(dosya="assets/video/eskisehir-evlilik-teklifi-balon-ev-reels.mp4", poster="assets/video/eskisehir-evlilik-teklifi-balon-ev-reels-poster.webp",
                  ad="Her ayrıntısı aşk dolu bir evet için: Eskişehir evlilik teklifi", aciklama="Balon ev, MARRY ME harfleri ve maytaplarla hazırlanan evlilik teklifi anlarından kısa bir derleme.",
                  sure="PT8S", w=464, h=832),
    "dogum-gunu": dict(dosya="assets/video/balon-ev-dogum-gunu-love-eskisehir.mp4", poster="assets/video/balon-ev-dogum-gunu-love-eskisehir-poster.webp",
                       ad="Balon evde doğum günü ve LOVE harfleri, Eskişehir", aciklama="Balon evin içinde Happy Birthday neon yazısı ve dışında ışıklı LOVE harfleriyle hazırlanan sürpriz kutlama.",
                       sure="PT14S", w=832, h=372),
}
VIDEO = VIDEOS["teklif"]
FOTO = {}       # dosya yolu -> dict(gal, cikti, w, h, alt)
_KAYIT = []     # (yol, galeri klasörü, alt) işlenecek görseller


def slug(s, n=70):
    tr = str.maketrans("çğıöşüÇĞİÖŞÜâîûÂÎÛ", "cgiosuCGIOSUaiuAIU")
    s = re.sub(r"[’'`]", "", (s or "").translate(tr).lower())
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    if len(s) > n:
        s = s[:n].rsplit("-", 1)[0]
    return s


def kayit_ekle(yol, gal, alt):
    yol = norm(yol)
    if yol and all(k[0] != yol for k in _KAYIT):
        _KAYIT.append((yol, gal, alt))


def kayitlari_topla():
    """Sitede kullanılan tüm görselleri topla: önce galeriler (açıklamalarıyla), sonra paket ve sayfa görselleri."""
    for gal, (bas, _, slots) in GALERI.items():
        for ad, cap in slots:
            kayit_ekle(GALERI_DOSYA[(gal, ad)], gal, cap)
    for k, v in PAKET.items():
        for alan in ("foto", "vitrin_foto"):
            kayit_ekle(v.get(alan), "paket", f"{v['ad']}, Eskişehir evlilik teklifi")
    for o in GORSEL.get("ana_sayfa_slaytlar") or []:
        kayit_ekle((o or {}).get("gorsel"), "genel", (o or {}).get("aciklama") or f"Eskişehir evlilik teklifi, {(o or {}).get('etiket', '').lower()} konsepti")
    for alan in ("ana_sayfa_kapak", "tanitim_buyuk", "tanitim_kucuk", "rezervasyon_arka_plan", "ara_bant"):
        o = GORSEL.get(alan) or {}
        kayit_ekle(o.get("gorsel"), "genel", o.get("aciklama") or "Eskişehir evlilik teklifi organizasyonu")
    for o in GORSEL.get("mozaik") or []:
        kayit_ekle((o or {}).get("gorsel"), "genel", (o or {}).get("aciklama") or "Eskişehir evlilik teklifi kurulumu")
    for o in GORSEL.get("sayfa_kapaklari") or []:
        kayit_ekle(o.get("gorsel"), "kapak", o.get("aciklama") or f"Eskişehir evlilik teklifi, {o.get('baslik', '').replace(' sayfası', '').lower()}")


# Fotoğraf düzenlemesi: her derlemede yeniden uygulanır, böylece panelden yüklenen yeni fotoğraflar da aynı görünür.
# Sıcak ışık, derin siyahlar, hafif S-eğrisi ve kontrollü netleştirme. Kapatmak için FOTO_DUZENLE = False.
FOTO_DUZENLE = True


def _s_egrisi(guc=0.3, a=4.2):
    import math
    t0 = math.tanh(a / 2)
    return [int(round(255 * ((1 - guc) * (x / 255) + guc * (0.5 + 0.5 * math.tanh(a * (x / 255 - 0.5)) / t0))))
            for x in range(256)]


def duzenle(im):
    from PIL import Image, ImageOps, ImageEnhance, ImageChops
    im = ImageOps.autocontrast(im, cutoff=(0.4, 0.25), preserve_tone=True)
    im = im.point(_s_egrisi() * 3)
    L = im.convert("L")
    golge = L.point(lambda v: int(255 * 0.26 * (1 - v / 255) ** 2))   # gölgelere bordo
    acik = L.point(lambda v: int(255 * 0.20 * (v / 255) ** 2))        # açık tonlara altın
    im = Image.composite(ImageChops.soft_light(im, Image.new("RGB", im.size, (92, 14, 30))), im, golge)
    im = Image.composite(ImageChops.soft_light(im, Image.new("RGB", im.size, (242, 196, 109))), im, acik)
    return ImageEnhance.Color(im).enhance(1.08)


def process_photos(out):
    from PIL import Image, ImageOps, ImageFilter
    kayitlari_topla()
    kullanilan = set()
    for yol, gal, alt in _KAYIT:
        src = ROOT / yol
        if not src.exists():
            print("UYARI: görsel bulunamadı, atlandı:", yol)
            continue
        ad = slug(alt) or slug(src.stem) or "gorsel"
        base, i = ad, 2
        while (gal, ad) in kullanilan:
            ad, i = f"{base}-{i}", i + 1
        kullanilan.add((gal, ad))
        im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
        if FOTO_DUZENLE:
            im = duzenle(im)
        d = out / "img" / gal
        d.mkdir(parents=True, exist_ok=True)
        for w in (800, 1600):
            r = im.copy(); r.thumbnail((w, w * 2), Image.LANCZOS)
            r = r.filter(ImageFilter.UnsharpMask(radius=1.2, percent=55, threshold=3))
            r.save(d / f"{ad}-{w}.webp", "WEBP", quality=82, method=6)
        r = im.copy(); r.thumbnail((800, 1600))
        FOTO[yol] = dict(gal=gal, cikti=ad, w=r.size[0], h=r.size[1], alt=alt)


def coz(a, b=None):
    """Görseli bul. (galeri, ad) silinmiş ya da değiştirilmişse aynı galerinin ilk fotoğrafını kullan; sayfa hiç bozulmaz."""
    if b is None:
        return FOTO.get(norm(a)) if a else None
    yol = GALERI_DOSYA.get((a, b))
    if yol and yol in FOTO:
        return FOTO[yol]
    for ad, _ in (GALERI.get(a) or (None, None, []))[2]:
        y = GALERI_DOSYA.get((a, ad))
        if y in FOTO:
            return FOTO[y]
    return None


class _FotoVar:
    def __contains__(self, k):
        return coz(*R(k)) is not None

    def __len__(self):
        return len(FOTO)


FOTO_VAR = _FotoVar()


def foto_url(c, e, w=1600):
    return c.A(f"img/{e['gal']}/{e['cikti']}-{w}.webp")


def img(c, a, b=None, sizes="(max-width:760px) 100vw, 40vw", eager=False, alt=None):
    e = coz(a, b)
    if not e:
        return '<span class="foto-yok" aria-hidden="true"></span>'
    s800, s1600 = foto_url(c, e, 800), foto_url(c, e, 1600)
    load = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img src="{s800}" srcset="{s800} 800w, {s1600} 1600w" sizes="{sizes}" '
            f'width="{e["w"]}" height="{e["h"]}" alt="{esc(alt or e["alt"])}" {load}>')


def cap_of(gal, ad):
    e = coz(gal, ad)
    return e["alt"] if e else ""


def photo(c, gal, ad, cap=None):
    e = coz(gal, ad)
    if not e:
        return ""
    cap = cap or e["alt"]
    inner = (f'<button type="button" data-buyuk="{foto_url(c, e)}" data-alt="{esc(cap)}" aria-label="Büyüt: {esc(cap)}">'
             + img(c, gal, ad, "(max-width:760px) 50vw, 25vw") + '</button>')
    return f'<figure><div class="foto">{inner}</div><figcaption>{esc(cap)}</figcaption></figure>'


def gallery(c, gals, limit=None):
    items = [(g, ad) for g in gals for ad, _ in GALERI.get(g, (None, None, []))[2] if GALERI_DOSYA.get((g, ad)) in FOTO]
    return '<div class="galeri">' + "".join(photo(c, g, ad) for g, ad in items[:limit]) + '</div>'


def on_yukle(c, ref, sizes="100vw"):
    e = coz(*R(ref))
    if not e:
        return ""
    return (f'<link rel="preload" as="image" href="{foto_url(c, e, 800)}" imagesrcset="{foto_url(c, e, 800)} 800w, '
            f'{foto_url(c, e, 1600)} 1600w" imagesizes="{sizes}" fetchpriority="high">')


def polaroid(c, ref, yazi="", cls="", sizes="(max-width:860px) 46vw, 300px", eager=False, ek=""):
    """Fotoğrafı beyaz kenarlı, el yazısı alt yazılı bir hatıra karesi olarak gösterir."""
    e = coz(*R(ref))
    if not e:
        return ""
    yon = "dikey" if e["h"] > e["w"] * 1.05 else "yatay"
    alt = f"<figcaption>{esc(yazi)}</figcaption>" if yazi else ""
    sinif = " ".join(x for x in ("polaroid", yon, cls) if x)
    return f'<figure class="{sinif}"><div class="polaroid-foto">{img(c, *R(ref), sizes=sizes, eager=eager)}</div>{ek}{alt}</figure>'


def rozet(fiyat, ek="TL"):
    """Altın, yuvarlak fiyat rozeti."""
    return f'<span class="rozet"><b>{tl(fiyat)[:-3]}</b><small>{esc(ek)}</small></span>'


def video_html(c, key="teklif"):
    v = VIDEOS[key]
    cls = "video dikey" if v["h"] > v["w"] else "video"
    return (f'<figure class="{cls}"><video controls muted playsinline preload="none" poster="{c.A(v["poster"])}" width="{v["w"]}" height="{v["h"]}">'
            f'<source src="{c.A(v["dosya"])}" type="video/mp4"></video><figcaption>{esc(v["ad"])}</figcaption></figure>')


def video_schema(key="teklif"):
    B, v = C["BASE"], VIDEOS[key]
    return {"@type": "VideoObject", "name": v["ad"], "description": v["aciklama"],
            "thumbnailUrl": B + v["poster"], "contentUrl": B + v["dosya"],
            "uploadDate": C["DATE"] + "T12:00:00+03:00", "duration": v["sure"], "publisher": {"@id": B + "#isletme"}}


def image_schema(gal):
    out = []
    for ad, cap in GALERI.get(gal, (None, None, []))[2]:
        e = FOTO.get(GALERI_DOSYA.get((gal, ad)))
        if e:
            out.append({"@type": "ImageObject", "contentUrl": C["BASE"] + f"img/{e['gal']}/{e['cikti']}-1600.webp",
                        "caption": cap, "name": cap, "creditText": C["BRAND"],
                        "copyrightNotice": C["PARENT"], "creator": {"@id": C["BASE"] + "#isletme"}})
    return out


# müşteri yorumları: veri/yorumlar.json (yönetim panelinden eklenip çıkarılabilir)
YORUMLAR = [(y["ad"], y.get("tur") or "Organizasyon", y["metin"], y.get("kaynak") or "", bool(y.get("ana_sayfada")))
            for y in oku("yorumlar").get("yorumlar") or [] if y and y.get("ad") and y.get("metin")]


def yorum_html(items):
    out = []
    for n, k, t, kaynak, *_ in items:
        kay = '<br><span class="yorum-kaynagi">Kaynak: ' + esc(kaynak) + '</span>' if kaynak else ""
        metin = esc(t.strip(" \"“”"))
        out.append(f'<figure class="yorum"><blockquote>“{metin}”</blockquote><figcaption><strong>{esc(n)}</strong><br>{esc(k)}{kay}</figcaption></figure>')
    return "".join(out)


def ana_yorumlar():
    sec = [y for y in YORUMLAR if y[4]]
    return (sec or YORUMLAR)[:3]


# ------------------------------------------------------------------ paketler (güncel fiyat afişlerinden)
_PK = oku("paketler")
ESKI_FIYAT_GOSTER = bool(_PK.get("eski_fiyat_goster"))   # üstü çizili eski fiyat (bkz. İndirimli Satışlar Yönetmeliği)
PAKET = {}
for _k in _PK.get("paketler") or []:
    PAKET[_k["kod"]] = dict(ad=_k["ad"].strip(), fiyat=int(float(_k["fiyat"])), eski=int(float(_k["eski_fiyat"])) if _k.get("eski_fiyat") else None,
                            sayfa=_k["sayfa"], foto=norm(_k.get("foto")) or None, vitrin_foto=norm(_k.get("vitrin_foto")) or None,
                            icerik=[str(x).strip() for x in (_k.get("icerik") or []) if str(x).strip()], not_=(_k.get("not") or "").strip())
_EKSIK = {"balon-ev", "bungalov", "karavan", "kanlikavak", "gondol", "otel", "restoran", "balon-dogum-gunu",
          "balon-yildonumu", "bungalov-dogum-gunu", "bungalov-yildonumu"} - set(PAKET)
if _EKSIK:
    raise SystemExit("veri/paketler.json içinde eksik paket: " + ", ".join(sorted(_EKSIK)))
EN_DUSUK = min(v["fiyat"] for v in PAKET.values())
OZEL_GUN = ["balon-dogum-gunu", "bungalov-dogum-gunu", "balon-yildonumu", "bungalov-yildonumu"]


def tl(n):
    return f"{n:,.0f}".replace(",", ".") + " TL"


def paket_html(c, key, foto=True, h="h3", wa_metin=None, kisa=None):
    k = PAKET[key]
    f = ""
    if foto and k.get("foto") and k["foto"] in FOTO:
        f = f'<div class="paket-foto">{img(c, k["foto"], sizes="(max-width:700px) 60vw, 220px")}</div>'
    eski = f"<del>{tl(k['eski'])}</del>" if ESKI_FIYAT_GOSTER and k.get("eski") else ""
    not_ = f'<p class="paket-not">{esc(k["not_"])}</p>' if k.get("not_") else ""
    liste = k["icerik"][:kisa] if kisa else k["icerik"]
    li = "".join(f"<li>{esc(x)}</li>" for x in liste)
    if kisa and len(k["icerik"]) > kisa:
        li += f'<li class="daha"><a href="{c.L(k["sayfa"])}">ve {len(k["icerik"]) - kisa} kalem daha</a></li>'
    mesaj = wa_metin or f"Merhaba, {k['ad']} ({tl(k['fiyat'])}) için tarih ve bilgi almak istiyorum."
    return f'''<article class="paket">{f}<div class="paket-govde"><{h}>{esc(k["ad"])}</{h}>
<div class="paket-fiyat"><strong>{tl(k["fiyat"])}</strong>{eski}<span>güncel kampanya fiyatı</span></div>
<ul class="tik">{li}</ul>{not_}
<a class="dugme altin" href="{wa(mesaj)}" data-konum="paket-{key}" target="_blank" rel="noopener">{IC_SOHBET} Bu paketi sor</a></div></article>'''


def offer(key, url):
    k = PAKET[key]
    return {"@type": "Offer", "price": str(k["fiyat"]), "priceCurrency": "TRY", "url": url,
            "availability": "https://schema.org/InStock", "name": k["ad"]}


def mozaik(c, items):
    out = []
    for ref, cls in items:
        e = coz(*R(ref))
        if not e:
            continue
        cap = e["alt"]
        out.append(f'<figure class="{cls}"><button type="button" data-buyuk="{foto_url(c, e)}" data-alt="{esc(cap)}" aria-label="Büyüt: {esc(cap)}">'
                   f'{img(c, *R(ref), sizes="(max-width:700px) 50vw, 25vw")}</button><figcaption>{esc(cap)}</figcaption></figure>')
    return '<div class="mozaik">' + "".join(out) + "</div>"


# ------------------------------------------------------------------ ortak parçalar
NAV = [("Konseptler", "evlilik-teklifi-mekanlari"), ("Fiyatlar", "evlilik-teklifi-fiyatlari"),
       ("Galeri", "galeri"), ("Rehber", "blog"), ("İletişim", "iletisim")]
UZUM_SVG = ('<svg class="{cls}" viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            '<path d="M20 4c0 3-1 5-3 6"/><path d="M20 7c3-3 8-3 11 0-3 2-7 2-11 0z"/><circle cx="14" cy="15" r="3"/><circle cx="20" cy="15" r="3"/>'
            '<circle cx="26" cy="15" r="3"/><circle cx="17" cy="21" r="3"/><circle cx="23" cy="21" r="3"/><circle cx="20" cy="27" r="3"/><circle cx="20" cy="33" r="2.4"/></svg>')
LOGO_SVG = UZUM_SVG.replace("{cls}", "logo-isaret")


KALP_YOL = "M12 21s-8.5-5.2-8.5-11.3C3.5 6.6 5.9 4.5 8.6 4.5c1.5 0 2.7.7 3.4 1.9.7-1.2 1.9-1.9 3.4-1.9 2.7 0 5.1 2.1 5.1 5.2C20.5 15.8 12 21 12 21z"
KALP_SVG = f'<svg class="kalp" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.1" stroke-linejoin="round" aria-hidden="true"><path d="{KALP_YOL}"/></svg>'


def kalpler(n=9, tohum=3, alan="kenar"):
    """Kırmızı zeminlerde serpilmiş ince altın kalp çizgileri (süs, ekran okuyucudan gizli).
    alan="kenar": metnin dışında, sayfanın iki kenarında; alan="sag": sağ yarıda (iç sayfa başlıkları)."""
    import random
    rnd = random.Random(tohum)
    out = []
    for i in range(n):
        if alan == "sag":
            x = rnd.uniform(52, 97)
        else:
            x = rnd.uniform(.5, 5) if i % 2 == 0 else rnd.uniform(94, 98.5)
        out.append(f'<i style="--x:{x:.1f}%;--y:{rnd.uniform(6, 88):.1f}%;--s:{rnd.choice([18, 24, 30, 40, 56])}px;--r:{rnd.uniform(-22, 22):.0f}deg">{KALP_SVG}</i>')
    return f'<div class="kalpler" aria-hidden="true">{"".join(out)}</div>'


def isik_zinciri():
    return ""   # eski şablondan kaldı; yeni şablonda kullanılmıyor


def isik_parcaciklari(n=9):
    return kalpler(n)


def logo(c):
    return f'''<a class="logo" href="{c.L()}" aria-label="{C["BRAND"]} ana sayfa"><span class="logo-ad">The Vine</span><span class="logo-alt">Eskişehir Evlilik Teklifi</span></a>'''


def header(c):
    links = "".join(f'<a href="{c.L(s)}"{" aria-current=page" if c.slug == s else ""}>{n}</a>' for n, s in NAV)
    return f'''<header class="ust" id="ust"><div class="kap">{logo(c)}
<button class="menu-ac" type="button" aria-expanded="false" aria-controls="menu">Menü</button>
<nav id="menu" class="menu" aria-label="Ana menü">{links}<a class="dugme altin" href="{wa("Merhaba, evlilik teklifi için bilgi almak istiyorum.")}" data-konum="menu" target="_blank" rel="noopener">{IC_SOHBET} WhatsApp</a></nav>
</div></header>'''


SEHIR_SECENEK = ["Eskişehir (Tepebaşı / Odunpazarı)", "Eskişehir ilçeleri", "Kütahya", "Tavşanlı", "Bilecik", "Bozüyük", "Afyonkarahisar", "Bursa / İnegöl", "Diğer"]


def quick_form(c, fid):
    opts = "".join(f"<option>{s}</option>" for s in SEHIR_SECENEK)
    k = "".join(f'<label class="secenek"><input type="radio" name="konsept" value="{v}" data-ad="{PAKET[v]["ad"]}"><span>{a}<small>{tl(PAKET[v]["fiyat"])}</small></span></label>'
                for v, a in [("balon-ev", "Balon ev"), ("bungalov", "Bungalov"), ("karavan", "Karavan")])
    return f'''<form class="form" data-teklif aria-label="Hızlı fiyat talebi">
<fieldset><legend>Konsept</legend><div class="secenekler">{k}</div></fieldset>
<div class="iki"><div><label class="etiket" for="{fid}-s">Şehir</label><select id="{fid}-s" name="sehir">{opts}</select></div>
<div><label class="etiket" for="{fid}-t">Tarih</label><input id="{fid}-t" type="date" name="tarih"></div></div>
<div><label class="etiket" for="{fid}-n">Aklınızdakiler (isteğe bağlı)</label><textarea id="{fid}-n" name="not" placeholder="Örneğin: akşam saatinde, beyaz çiçekler, sürpriz pasta"></textarea></div>
<div><button class="dugme altin" type="submit" style="width:100%">{IC_SOHBET} WhatsApp'tan tarih sor</button></div>
<p class="form-sonuc" role="status"></p>
<p class="kucuk" style="margin:0">Bilgileriniz hazır bir mesaj olarak WhatsApp'ta açılır, sitede saklanmaz. Gondol, Kanlıkavak, otel ve restoran konseptleri için <a href="{c.L("teklif-al")}">ayrıntılı formu</a> kullanın.</p>
</form>'''


def cta_band(c, konu):
    bg = img(c, (GORSEL.get("rezervasyon_arka_plan") or {}).get("gorsel"), sizes="100vw")
    return f'''<section class="cagri" aria-labelledby="cagri-baslik"><div class="cagri-gorsel">{bg}</div><div class="kap cagri-ic">
<div><p class="ust-yazi">Rezervasyon</p><h2 id="cagri-baslik">Tarihinizi ayıralım</h2>
<p class="giris">Konsepti, şehri ve tarihi yazın; müsaitliği ve size uygun seçenekleri aynı gün WhatsApp'tan iletelim. Hafta sonları ve 14 Şubat gibi tarihler erken doluyor.</p>
<ul class="cagri-iletisim">
<li><a href="{wa("Merhaba, " + konu + " hakkında bilgi almak istiyorum.")}" data-konum="cagri" target="_blank" rel="noopener">WhatsApp: {C["TEL1_TXT"]}</a></li>
<li><a href="tel:{C["TEL1"]}" data-konum="cagri">Telefon: {C["TEL1_TXT"]}</a></li>
<li><a href="tel:{C["TEL2"]}" data-konum="cagri">Telefon: {C["TEL2_TXT"]}</a></li></ul></div>
<div class="cam">{quick_form(c, "hf")}</div>
</div></section>'''


def footer(c, konu):
    sehir = "".join(f'<li><a href="{c.L(s)}">{n} evlilik teklifi</a></li>' for n, s, *_ in CITIES)
    mail = f'<br><a href="mailto:{C["EMAIL"]}">{C["EMAIL"]}</a>' if C["EMAIL"] else ""
    return f'''<footer class="alt"><div class="kap"><div class="alt-izgara">
<div>{logo(c)}
<p>Eskişehir'de balon ev, bungalov, karavan, gondol, Kanlıkavak, otel ve restoran konseptleriyle evlilik teklifi organizasyonu.</p>
<address>{C["ADDR_STREET"]}, {C["ADDR_POST"]} {C["ADDR_CITY"]}<br>
<a href="tel:{C["TEL1"]}" data-konum="alt">{C["TEL1_TXT"]}</a> / <a href="tel:{C["TEL2"]}" data-konum="alt">{C["TEL2_TXT"]}</a>{mail}</address>
<div class="vine-imza"><img src="{c.A("assets/the-vine-logo.png")}" alt="The Vine Organizasyon logosu" width="48" height="48" loading="lazy"><span>Bir <a href="{C["PARENT_URL"]}" rel="noopener" target="_blank">The Vine Organizasyon</a> markası. 20 yıllık organizasyon deneyimi.</span></div></div>
<div><h2>Konseptler</h2><ul>
<li><a href="{c.L("balon-ev-evlilik-teklifi")}">Balon ev evlilik teklifi</a></li>
<li><a href="{c.L("bungalov-evlilik-teklifi")}">Bungalovda evlilik teklifi</a></li>
<li><a href="{c.L("karavan-evlilik-teklifi")}">Karavanda evlilik teklifi</a></li>
<li><a href="{c.L("gondolda-evlilik-teklifi")}">Gondolda evlilik teklifi</a></li>
<li><a href="{c.L("kanlikavak-parki-evlilik-teklifi")}">Kanlıkavak'ta evlilik teklifi</a></li>
<li><a href="{c.L("otel-odasinda-evlilik-teklifi")}">Otel odasında evlilik teklifi</a></li>
<li><a href="{c.L("gaga-restoran-evlilik-teklifi")}">Restoranda evlilik teklifi</a></li>
<li><a href="{c.L("sazova-parki-evlilik-teklifi")}">Sazova'da evlilik teklifi</a></li>
<li><a href="{c.L("ozel-gun-surprizleri")}">Doğum günü ve yıl dönümü</a></li></ul></div>
<div><h2>Şehirler ve rehber</h2><ul>{sehir}
<li><a href="{c.L("evlilik-teklifi-fiyatlari")}">Evlilik teklifi fiyatları</a></li>
<li><a href="{c.L("evlilik-teklifi-susleme")}">Evlilik teklifi süsleme</a></li>
<li><a href="{c.L("surpriz-evlilik-teklifi")}">Sürpriz evlilik teklifi</a></li>
<li><a href="{c.L("blog/evlilik-teklifi-sozleri")}">Evlilik teklifi sözleri</a></li>
<li><a href="{c.L("blog/evlilik-teklifi-fikirleri")}">Evlilik teklifi fikirleri</a></li></ul></div>
<div><h2>Kurumsal</h2><ul>
<li><a href="{c.L("galeri")}">Galeri</a></li><li><a href="{c.L("yorumlar")}">Müşteri yorumları</a></li>
<li><a href="{c.L("hakkimizda")}">Hakkımızda</a></li><li><a href="{c.L("sss")}">Sık sorulan sorular</a></li>
<li><a href="{c.L("blog")}">Blog</a></li><li><a href="{c.L("iletisim")}">İletişim</a></li>
<li><a href="{c.L("gizlilik")}">Gizlilik ve çerezler</a></li>
<li><a href="{C["INSTAGRAM"]}" rel="noopener" target="_blank">Instagram</a></li>
<li><a href="{C["YOUTUBE"]}" rel="noopener" target="_blank">YouTube</a></li></ul></div>
</div><div class="alt-son"><span>© 2026 {C["BRAND"]}</span><span>Eskişehir merkez, Kütahya, Bilecik, Bozüyük, Afyonkarahisar ve Bursa</span></div></div></footer>
<a class="yuzen-wa" href="{wa("Merhaba, " + konu + " hakkında bilgi almak istiyorum.")}" data-konum="yuzen" target="_blank" rel="noopener" aria-label="WhatsApp'tan yazın">{IC_SOHBET}</a>
<div class="mobil-bar" aria-label="Hızlı iletişim"><a class="dugme cizgi" href="tel:{C["TEL1"]}" data-konum="mobil-bar">{IC_TEL} Ara</a>
<a class="dugme altin" href="{wa("Merhaba, " + konu + " hakkında bilgi almak istiyorum.")}" data-konum="mobil-bar" target="_blank" rel="noopener">{IC_SOHBET} WhatsApp</a></div>
<div class="cerez" role="region" aria-label="Çerez tercihi"><p>Siteyi geliştirmek ve reklam ölçümü için çerez kullanıyoruz. Kabul etmezseniz yalnızca zorunlu çerezler çalışır. <a href="{c.L("gizlilik")}">Ayrıntılar</a></p>
<div class="dugmeler"><button class="dugme sarap" type="button" data-cerez="kabul">Kabul et</button><button class="dugme cizgi-koyu" type="button" data-cerez="red">Reddet</button></div></div>'''


def isletme():
    B = C["BASE"]
    d = {
        "@type": "LocalBusiness", "@id": B + "#isletme", "name": C["BRAND"],
        "alternateName": ["Eskişehir Evlenme Teklifi", C["PARENT"]],
        "description": "Eskişehir merkezli evlilik teklifi organizasyonu: balon ev, bungalov, karavan, gondol, Kanlıkavak, otel ve restoran konseptleri.",
        "url": B, "telephone": C["TEL1"],
        "image": B + "assets/og/ana-sayfa.jpg", "logo": B + "assets/logo-512.png",
        "address": {"@type": "PostalAddress", "streetAddress": C["ADDR_STREET"], "addressLocality": C["ADDR_LOCALITY"],
                    "addressRegion": "Eskişehir", "postalCode": C["ADDR_POST"], "addressCountry": "TR"},
        "areaServed": [{"@type": "City", "name": n} for n in ["Eskişehir", "Kütahya", "Tavşanlı", "Bilecik", "Bozüyük", "Afyonkarahisar", "Bursa", "İnegöl"]],
        "contactPoint": [{"@type": "ContactPoint", "telephone": C["TEL1"], "contactType": "reservations", "availableLanguage": "tr"},
                         {"@type": "ContactPoint", "telephone": C["TEL2"], "contactType": "customer service", "availableLanguage": "tr"}],
        "sameAs": [C["INSTAGRAM"], C["YOUTUBE"], C["INSTAGRAM_VINE"], C["YOUTUBE_VINE"], C["PARENT_URL"]],
        "parentOrganization": {"@type": "Organization", "name": C["PARENT"], "url": C["PARENT_URL"]},
        "knowsAbout": ["evlilik teklifi organizasyonu", "evlenme teklifi", "balon ev süsleme", "bungalov süsleme", "karavan süsleme", "sürpriz organizasyon"],
        "priceRange": f"{tl(EN_DUSUK)} - {tl(max(v['fiyat'] for v in PAKET.values()))}",
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Evlilik teklifi ve sürpriz paketleri", "itemListElement": [
            {"@type": "Offer", "price": str(v["fiyat"]), "priceCurrency": "TRY", "itemOffered": {"@type": "Service", "name": v["ad"], "url": B + v["sayfa"] + "/"}} for v in PAKET.values()]},
    }
    if C["EMAIL"]:
        d["email"] = C["EMAIL"]
    return d


def head(c, p):
    B = C["BASE"]
    canon = B + (p["slug"] + "/" if p["slug"] else "")
    if p.get("file"):
        canon = B + p["file"]
    og = B + f"assets/og/{p['og']}.jpg"
    graph = [isletme(), {"@type": "WebPage", "@id": canon + "#sayfa", "url": canon, "name": p["title"],
                         "description": p["desc"], "inLanguage": "tr-TR", "isPartOf": {"@id": B + "#site"},
                         "primaryImageOfPage": og, "dateModified": C["DATE"], "about": {"@id": B + "#isletme"}}]
    if not p["slug"]:
        graph.insert(0, {"@type": "WebSite", "@id": B + "#site", "url": B, "name": C["BRAND"], "inLanguage": "tr-TR",
                         "publisher": {"@id": B + "#isletme"}})
    elif p.get("crumbs"):
        items = [{"@type": "ListItem", "position": 1, "name": "Ana sayfa", "item": B}]
        for i, (n, s) in enumerate(p["crumbs"], start=2):
            items.append({"@type": "ListItem", "position": i, "name": n, "item": B + s + "/"})
        graph.append({"@type": "BreadcrumbList", "itemListElement": items})
    if p.get("faq"):
        graph.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in p["faq"]]})
    if p.get("service"):
        s = p["service"]
        svc = {"@type": "Service", "name": s["name"], "serviceType": "Evlilik teklifi organizasyonu",
               "provider": {"@id": B + "#isletme"}, "url": canon, "description": p["desc"],
               "areaServed": [{"@type": "City", "name": n} for n in s.get("area", ["Eskişehir"])]}
        if s.get("gal") and image_schema(s["gal"]):
            svc["image"] = image_schema(s["gal"])
        if p.get("paket"):
            svc["offers"] = offer(p["paket"], canon)
        elif s.get("paketler"):
            svc["offers"] = [offer(k, canon) for k in s["paketler"]]
        graph.append(svc)
    if p.get("place"):
        graph.append({"@type": "TouristAttraction", "name": p["place"], "address": {"@type": "PostalAddress", "addressLocality": "Eskişehir", "addressCountry": "TR"}})
    if p.get("article"):
        graph.append({"@type": "BlogPosting", "headline": strip_tags(p["h1"]), "description": p["desc"], "image": og,
                      "datePublished": C["DATE"], "dateModified": C["DATE"], "inLanguage": "tr-TR",
                      "author": {"@id": B + "#isletme"}, "publisher": {"@id": B + "#isletme"}, "mainEntityOfPage": canon})
    if p.get("video"):
        for key in (p["video"] if isinstance(p["video"], list) else ["teklif"]):
            graph.append(video_schema(key))
    if p.get("gallery_schema"):
        imgs = [i for g in GALERI for i in image_schema(g)]
        if imgs:
            graph.append({"@type": "ImageGallery", "name": "Evlilik teklifi galerisi", "url": canon, "image": imgs})
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    gtm = ""
    if c.mode == "prod":
        gtm = f'''<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}
gtag('consent','default',{{ad_storage:'denied',analytics_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',wait_for_update:500}});
try{{if(localStorage.getItem('cerez')==='kabul'){{gtag('consent','update',{{ad_storage:'granted',analytics_storage:'granted',ad_user_data:'granted',ad_personalization:'granted'}});}}}}catch(e){{}}
(function(w,d,s,l,i){{if(/X{{4}}/.test(i))return;w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s);j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','{C["GTM_ID"]}');</script>'''
    gsc = f'<meta name="google-site-verification" content="{esc(C["GSC_TOKEN"])}">' if C["GSC_TOKEN"] else ""
    robots = "noindex,follow" if p.get("noindex") else "index,follow,max-image-preview:large,max-snippet:-1"
    panel_yonlendir = ("<script>if(/(invite|recovery|confirmation|email_change)_token=/.test(location.hash))location.replace('/admin/'+location.hash)</script>"
                       if c.mode == "prod" and not p["slug"] and not p.get("file") else "")
    noscript = (f'<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={C["GTM_ID"]}" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>'
                if c.mode == "prod" and "XXXX" not in C["GTM_ID"] else "")
    return f'''<!DOCTYPE html>
<html lang="tr" data-wa="{C["WA"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(p["title"])}</title>
<meta name="description" content="{esc(p["desc"])}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="{robots}">
<meta property="og:type" content="{"article" if p.get("article") else "website"}">
<meta property="og:locale" content="tr_TR">
<meta property="og:site_name" content="{esc(C["BRAND"])}">
<meta property="og:title" content="{esc(p["title"])}">
<meta property="og:description" content="{esc(p["desc"])}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(strip_tags(p["h1"]))}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#7A0E1C">
<meta name="geo.region" content="TR-26"><meta name="geo.placename" content="Eskişehir">
{gsc}
<link rel="icon" href="{c.A("assets/favicon.svg")}" type="image/svg+xml">
<link rel="icon" href="{c.A("assets/favicon-32.png")}" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{c.A("assets/apple-touch-icon.png")}">
<link rel="manifest" href="{c.A("site.webmanifest")}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{c.A("assets/site.css")}?v=5">
{p["preload"](c) if callable(p.get("preload")) else p.get("preload", "")}
{gtm}
<script type="application/ld+json">{ld}</script>
</head>
<body>
{noscript}
<a class="atla" href="#icerik">İçeriğe geç</a>{panel_yonlendir}'''


def page_head_band(c, p):
    crumbs = [f'<li><a href="{c.L()}">Ana sayfa</a></li>']
    for i, (n, s) in enumerate(p.get("crumbs", [])):
        crumbs.append(f'<li aria-current="page">{esc(n)}</li>' if i == len(p["crumbs"]) - 1 else f'<li><a href="{c.L(s)}">{esc(n)}</a></li>')
    pk = PAKET.get(p.get("paket") or "")
    foto = ""
    if p.get("hero_foto") and p["hero_foto"] in FOTO_VAR:
        yazi = p.get("kart_yazisi") or (p["crumbs"][-1][0] if p.get("crumbs") else "")
        foto = (f'<div class="sayfa-bas-gorsel">'
                f'{polaroid(c, p["hero_foto"], yazi, sizes="(max-width:860px) 80vw, 440px", eager=True, ek=rozet(pk["fiyat"]) if pk else "")}</div>')
    b = ""
    if p.get("buttons", True):
        q = ("?konsept=" + p["konsept"]) if p.get("konsept") else ""
        b = f'''<div class="dugmeler"><a class="dugme altin" href="{wa("Merhaba, " + p["konu"] + " hakkında bilgi almak istiyorum.")}" data-konum="sayfa-bas" target="_blank" rel="noopener">{IC_SOHBET} WhatsApp'tan sor</a>
<a class="dugme cizgi" href="{c.L("teklif-al")}{q}">Fiyat teklifi al</a></div>'''
    cip = ""
    if pk and not foto:   # fotoğraf varsa fiyat, karenin köşesindeki altın rozette
        cip = f'<p class="fiyat-cip">Güncel kampanya fiyatı <strong>{tl(pk["fiyat"])}</strong></p>'
    return f'''{header(c)}<div class="sayfa-bas{" fotolu" if foto else ""}">{kalpler(7, len(p["slug"]), "sag")}<div class="kap sayfa-bas-ic">
<div class="sayfa-bas-metin"><nav aria-label="Sayfa yolu"><ol class="iz">{"".join(crumbs)}</ol></nav>
<h1>{p["h1"]}</h1><p class="giris">{p["lede"]}</p>{cip}{b}</div>{foto}</div></div>'''


def sss_html(faq, h="h2", baslik="Sık sorulan sorular"):
    items = "".join(f"<details><summary>{esc(q)}</summary><p>{a}</p></details>" for q, a in faq)
    return f'<{h}>{baslik}</{h}><div class="sss">{items}</div>'


def sidebar(c, p):
    links = "".join(f'<li><a href="{c.L(s)}">{esc(n)}</a></li>' for n, s in (p.get("yan_baglar") or []))
    if p.get("paket"):
        ust = paket_html(c, p["paket"], foto=False, h="h2")
    else:
        ust = f'''<div class="yan-iletisim"><h2>Tarihiniz müsait mi?</h2><p>Paketler {tl(EN_DUSUK)}'den başlıyor. Konsept, şehir ve tarihi yazın; aynı gün dönüş yapalım.</p>
<a class="dugme altin" href="{wa("Merhaba, " + p["konu"] + " için tarih sormak istiyorum.")}" data-konum="yan" target="_blank" rel="noopener">{IC_SOHBET} WhatsApp</a>
<a class="dugme cizgi" href="tel:{C["TEL1"]}" data-konum="yan">{IC_TEL} {C["TEL1_TXT"]}</a></div>'''
    return f'''<aside class="yan" aria-label="Paket ve iletişim">{ust}
{f'<nav class="yan-bag" aria-label="İlgili sayfalar"><h2>İlgili sayfalar</h2><ul>{links}</ul></nav>' if links else ""}
</aside>'''


def article_layout(c, p, inner):
    return f'<div class="bolum"><div class="kap icerik-izgara"><article class="icerik">{inner}</article>{sidebar(c, p)}</div></div>'


def render(p, mode):
    c = Ctx("" if p.get("file") else p["slug"], mode, absolute=bool(p.get("file")))
    out = [head(c, p)]
    out.append(p["custom_head"](c) if p.get("custom_head") else page_head_band(c, p))
    out.append('<main id="icerik">')
    out.append(p["body"](c))
    out.append("</main>")
    if not p.get("no_cta"):
        out.append(cta_band(c, p["konu"]))
    out.append(footer(c, p["konu"]))
    out.append('<dialog class="isik-kutu" aria-label="Fotoğraf"><button type="button">Kapat</button><img alt=""></dialog>')
    out.append(f'<script src="{c.A("assets/app.js")}?v=5" defer></script></body></html>')
    return "\n".join(out)


# ------------------------------------------------------------------ OG görselleri, ikonlar
def make_images(out, pages):
    """Paylaşım görselleri (WhatsApp, Instagram, Facebook bağlantı önizlemesi) ve ikonlar: kırmızı zemin, altın kalpler, hatıra karesi."""
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
    yazi = ROOT / "araclar" / "yazi"
    serif, italik, sans = yazi / "CrimsonText-SemiBold.ttf", yazi / "CrimsonText-Italic.ttf", yazi / "FiraSans-Medium.ttf"
    og = out / "assets" / "og"; og.mkdir(parents=True, exist_ok=True)

    def zemin(w, h):
        im = Image.new("RGB", (w, h), (78, 8, 17))
        isik = Image.new("RGB", (w, h), (0, 0, 0)); d = ImageDraw.Draw(isik)
        d.ellipse((int(-w * .15), int(-h * .5), int(w * .85), int(h * 1.2)), fill=(170, 24, 44))
        return Image.blend(im, isik.filter(ImageFilter.GaussianBlur(160)), .62)

    def kalp(d, x, y, s, renk, kalinlik=2):
        noktalar = []
        import math
        for i in range(73):
            t = i / 72 * 2 * math.pi
            hx = 16 * math.sin(t) ** 3
            hy = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
            noktalar.append((x + hx * s / 34, y - hy * s / 34))
        d.line(noktalar, fill=renk, width=kalinlik, joint="curve")

    def sar(d, metin, font, genislik):
        satir, cur = [], ""
        for k in metin.split():
            t = (cur + " " + k).strip()
            if d.textlength(t, font=font) <= genislik:
                cur = t
            else:
                satir.append(cur); cur = k
        satir.append(cur)
        return satir

    def kare_gorseli(p):
        ref = p.get("hero_foto")
        if not (ref and ref in FOTO_VAR):
            sl = [o for o in (GORSEL.get("ana_sayfa_slaytlar") or []) if o and o.get("gorsel") and o["gorsel"] in FOTO_VAR]
            ref = sl[0]["gorsel"] if sl else None
        e = coz(*R(ref)) if ref else None
        if not e:
            return None
        f = out / "img" / e["gal"] / f"{e['cikti']}-800.webp"
        return Image.open(f).convert("RGB") if f.exists() else None

    yapilan = set()
    for p in pages:
        if p["og"] in yapilan:
            continue
        yapilan.add(p["og"])
        im = zemin(1200, 630)
        d = ImageDraw.Draw(im)
        for x, y, s in ((1150, 70, 46), (60, 560, 34), (690, 585, 26), (640, 40, 22)):
            kalp(d, x, y, s, (242, 196, 109))
        foto = kare_gorseli(p)
        metin_gen = 1000
        if foto:
            metin_gen = 600
            fw = 380
            foto = ImageOps.fit(foto, (fw, int(fw * 1.05)), Image.LANCZOS)
            kagit = Image.new("RGB", (fw + 36, int(fw * 1.05) + 104), (255, 253, 249))
            kagit.paste(foto, (18, 18))
            kd = ImageDraw.Draw(kagit)
            alt = (p.get("crumbs") or [("Evlilik Teklifi", "")])[-1][0]
            fi = ImageFont.truetype(str(italik), 40)
            kd.text(((kagit.width - kd.textlength(alt, font=fi)) / 2, int(fw * 1.05) + 34), alt, font=fi, fill=(122, 14, 28))
            kagit = kagit.convert("RGBA").rotate(-5, resample=Image.BICUBIC, expand=True)
            golge = Image.new("RGBA", kagit.size, (0, 0, 0, 0))
            golge.paste((20, 0, 4, 120), (0, 0), kagit.split()[3])
            golge = golge.filter(ImageFilter.GaussianBlur(18))
            x0, y0 = 1200 - kagit.width - 50, (630 - kagit.height) // 2 + 10
            im.paste(golge, (x0 + 10, y0 + 18), golge)
            im.paste(kagit, (x0, y0), kagit)
        baslik = strip_tags(p["h1"])
        boy = 70 if len(baslik) < 30 else 58
        fb = ImageFont.truetype(str(serif), boy)
        satirlar = sar(d, baslik, fb, metin_gen)[:3]
        y = 400 - len(satirlar) * (boy + 6)
        for s in satirlar:
            d.text((80, y), s, font=fb, fill=(255, 253, 249)); y += boy + 6
        d.text((80, 452), "Bir an değil, bir hikâyedir.", font=ImageFont.truetype(str(italik), 36), fill=(242, 196, 109))
        d.text((80, 530), "Eskişehir Evlilik Teklifi   |   " + C["TEL1_TXT"], font=ImageFont.truetype(str(sans), 24), fill=(248, 227, 230))
        im.save(og / f"{p['og']}.jpg", "JPEG", quality=86, optimize=True, progressive=True)

    def isaret(s):
        im = Image.new("RGBA", (s * 4, s * 4), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((0, 0, s * 4 - 1, s * 4 - 1), radius=int(s * .88), fill=(122, 14, 28, 255))
        kalp(d, s * 2, s * 2.12, s * 2.3, (242, 196, 109, 255), max(2, int(s * .26)))
        return im.resize((s, s), Image.LANCZOS)
    isaret(32).save(out / "assets" / "favicon-32.png")
    isaret(180).save(out / "assets" / "apple-touch-icon.png")
    isaret(512).save(out / "assets" / "logo-512.png")
    isaret(192).save(out / "assets" / "icon-192.png")
    (out / "assets" / "favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect width="24" height="24" rx="5.4" fill="#7A0E1C"/>'
        f'<path d="{KALP_YOL}" transform="translate(3.6 3.4) scale(.7)" fill="none" stroke="#F2C46D" stroke-width="2.1" stroke-linejoin="round"/></svg>', encoding="utf-8")


def write_sitemap(out, pages):
    B = C["BASE"]
    rows = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for p in pages:
        if p.get("noindex") or p.get("file"):
            continue
        loc = B + (p["slug"] + "/" if p["slug"] else "")
        imgs = "".join(f"<image:image><image:loc>{B}img/{e['gal']}/{e['cikti']}-1600.webp</image:loc></image:image>"
                       for g in p.get("sitemap_gal", []) for ad, _ in GALERI.get(g, (None, None, []))[2]
                       for e in [FOTO.get(GALERI_DOSYA.get((g, ad)))] if e)
        rows.append(f"<url><loc>{loc}</loc><lastmod>{C['DATE']}</lastmod>{imgs}</url>")
    rows.append("</urlset>")
    (out / "sitemap.xml").write_text("\n".join(rows), encoding="utf-8")


YONLENDIRMELER = [  # eski Wix adresleri -> yeni sayfalar (301)
    ("/evlilikteklifi", "/"), ("/evlilik-teklifi", "/"),
    ("/doğumgünü", "/ozel-gun-surprizleri/"), ("/dogumgunu", "/ozel-gun-surprizleri/"), ("/nişan", "/ozel-gun-surprizleri/"),
    ("/nisan", "/ozel-gun-surprizleri/"), ("/yıldönümü", "/ozel-gun-surprizleri/"), ("/yildonumu", "/ozel-gun-surprizleri/"),
    ("/hakkımızda", "/hakkimizda/"), ("/contact", "/iletisim/"), ("/shop", "/evlilik-teklifi-fiyatlari/"),
    ("/product-page/restorant-konsepti", "/gaga-restoran-evlilik-teklifi/"),
    ("/product-page/kanlı-kavak-iskele-konsepti", "/kanlikavak-parki-evlilik-teklifi/"),
    ("/product-page/kanli-kavak-iskele-konsepti", "/kanlikavak-parki-evlilik-teklifi/"),
    ("/product-page/orman-konsepti", "/evlilik-teklifi-mekanlari/"), ("/product-page/balon-ev-konsepti", "/balon-ev-evlilik-teklifi/"),
    ("/product-page/bungalov-konsepti", "/bungalov-evlilik-teklifi/"), ("/product-page/otel-konsepti", "/otel-odasinda-evlilik-teklifi/"),
    ("/product-page/vosvos-konsepti", "/karavan-evlilik-teklifi/"), ("/product-page/sazova-konsepti", "/sazova-parki-evlilik-teklifi/"),
    ("/product-page/gondol-konsepti", "/gondolda-evlilik-teklifi/"), ("/product-page/meşale", "/evlilik-teklifi-susleme/"),
    ("/product-page/volkan", "/evlilik-teklifi-susleme/"), ("/product-page/gül-adet", "/evlilik-teklifi-susleme/"),
    ("/product-page/balon-süsleme", "/evlilik-teklifi-susleme/"), ("/product-page/helyum-balon-kalpli", "/evlilik-teklifi-susleme/"),
    ("/product-page/kemancı", "/teklif-al/"), ("/product-page/fotoğraf-çekimi", "/teklif-al/"), ("/product-page/video-çekimi", "/teklif-al/"),
    ("/product-page/drone-çekim", "/teklif-al/"), ("/product-page/*", "/evlilik-teklifi-fiyatlari/"),
]


def netlify_dosyalari(out):
    host = C["BASE"].split("//")[1].rstrip("/")
    kok = host[4:] if host.startswith("www.") else host
    satir = [f"https://{kok}/* https://{host}/:splat 301!", f"http://{kok}/* https://{host}/:splat 301!"]
    for eski in C["ESKI_ALAN_ADLARI"]:   # eski alan adı (www'li ve www'siz) -> yeni alan adı, aynı sayfa yolu korunur
        for h in (eski, "www." + eski):
            satir += [f"https://{h}/* https://{host}/:splat 301!", f"http://{h}/* https://{host}/:splat 301!"]
    from urllib.parse import quote
    for a, b in YONLENDIRMELER:
        for yol in dict.fromkeys([a, quote(a, safe="/*-")]):   # Türkçe karakterli adreslerin kodlanmış hali de
            satir.append(f"{yol} {b} 301!")
            if not yol.endswith("*"):
                satir.append(f"{yol}/ {b} 301!")
    (out / "_redirects").write_text("\n".join(satir) + "\n", encoding="utf-8")
    (out / "_headers").write_text('''/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: SAMEORIGIN
  Permissions-Policy: camera=(), microphone=(), geolocation=()
/assets/*
  Cache-Control: public, max-age=31536000
/img/*
  Cache-Control: public, max-age=31536000
/fotograflar/*
  X-Robots-Tag: noindex
/admin/*
  X-Robots-Tag: noindex
''', encoding="utf-8")


def build():
    import content
    pages = content.pages()
    dist = ROOT / "dist"
    if dist.exists():
        shutil.rmtree(dist)
    netlify = os.environ.get("NETLIFY") == "true"   # Netlify'da yalnızca yayın sürümü üretilir
    modlar = (("prod", "site"),) if netlify else (("prod", "site"), ("preview", "onizleme"))
    for mode, folder in modlar:
        out = dist / folder
        (out / "assets").mkdir(parents=True)
        shutil.copy(ROOT / "assets" / "site.css", out / "assets" / "site.css")
        shutil.copy(ROOT / "assets" / "app.js", out / "assets" / "app.js")
        shutil.copytree(ROOT / "assets" / "video", out / "assets" / "video")
        shutil.copy(ROOT / "assets" / "the-vine-logo.png", out / "assets" / "the-vine-logo.png")
        if mode == "prod":
            process_photos(out)
        elif (dist / "site" / "img").exists():
            shutil.copytree(dist / "site" / "img", out / "img")
        for p in pages:
            target = out / p["file"] if p.get("file") else (out / p["slug"] / "index.html" if p["slug"] else out / "index.html")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(render(p, mode), encoding="utf-8")
        make_images(out, pages)
        (out / "site.webmanifest").write_text(json.dumps({
            "name": C["BRAND"], "short_name": "Evlilik Teklifi", "lang": "tr", "start_url": "/",
            "display": "standalone", "background_color": "#7A0E1C", "theme_color": "#7A0E1C",
            "icons": [{"src": "assets/icon-192.png", "sizes": "192x192", "type": "image/png"},
                      {"src": "assets/logo-512.png", "sizes": "512x512", "type": "image/png"}]}, ensure_ascii=False), encoding="utf-8")
        if mode == "prod":
            write_sitemap(out, pages)
            (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /admin/\nDisallow: /fotograflar/\n\nSitemap: {C['BASE']}sitemap.xml\n", encoding="utf-8")
            shutil.copy(ROOT / "htaccess.txt", out / ".htaccess")
            netlify_dosyalari(out)
            # yönetim paneli ve panelde önizleme için orijinal fotoğraflar
            if (ROOT / "admin").exists():
                shutil.copytree(ROOT / "admin", out / "admin")
            shutil.copytree(ROOT / "fotograflar", out / "fotograflar")
    print("ok:", len(pages), "sayfa,", len(FOTO_VAR), "fotoğraf")


if __name__ == "__main__":
    import build as _b   # içerik modülüyle aynı örneği kullan
    _b.build()
