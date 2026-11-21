# -*- coding: utf-8 -*-
"""Sayfa içerikleri. Her sayfa ayrı bir arama niyetini hedefler."""
from build import (C, wa, esc, header, img, gallery, photo, video_html, map_svg, CITIES,
                   YORUMLAR, yorum_html, sss_html, article_layout, IC_SOHBET, IC_TEL, SEHIR_SECENEK, GALERI, FOTO_VAR,
                   PAKET, paket_html, tl, mozaik, VIDEOS, EN_DUSUK, GORSEL, R, ana_yorumlar, OZEL_GUN, on_yukle, UZUM_SVG,
                   isik_zinciri, isik_parcaciklari, coz, polaroid, rozet, kalpler, KALP_SVG)


def slaytlar():
    sl = [o for o in (GORSEL.get("ana_sayfa_slaytlar") or []) if o and o.get("gorsel")]
    if not sl and (GORSEL.get("ana_sayfa_kapak") or {}).get("gorsel"):
        sl = [{"gorsel": GORSEL["ana_sayfa_kapak"]["gorsel"], "etiket": ""}]
    return [o for o in sl if o["gorsel"] in FOTO_VAR]


def ozel_min():
    return min(PAKET[k]["fiyat"] for k in OZEL_GUN)


def ozel_max():
    return max(PAKET[k]["fiyat"] for k in OZEL_GUN)


TEKLIF_KISA = [("gondol", "gondol"), ("balon-ev", "balon ev"), ("bungalov", "bungalov"), ("karavan", "karavan"),
               ("kanlikavak", "Kanlıkavak"), ("otel", "otel"), ("restoran", "restoran")]


def en_uygun():
    k, ad = min(TEKLIF_KISA, key=lambda x: PAKET[x[0]]["fiyat"])
    return ad, PAKET[k]["fiyat"]


def gorsel(alan):
    return (GORSEL.get(alan) or {}).get("gorsel")


def ilgili(c, items):
    return '<div class="ilgili">' + "".join(
        f'<a href="{c.L(s)}"><strong>{esc(t)}</strong><span>{esc(d)}</span></a>' for t, s, d in items) + "</div>"


KONSEPT_ILGILI = {
    "balon": ("Balon evde evlilik teklifi", "balon-ev-evlilik-teklifi", "Şeffaf kubbe, neon yazı ve MARRY ME harfleri"),
    "bungalov": ("Bungalovda evlilik teklifi", "bungalov-evlilik-teklifi", "Işıklı A-frame bungalov, şömine ve sıcak bir iç mekân"),
    "karavan": ("Karavanda evlilik teklifi", "karavan-evlilik-teklifi", "Sarı vintage karavan, piknik köşesi ve ışık tavanı"),
    "fiyat": ("Evlilik teklifi fiyatları", "evlilik-teklifi-fiyatlari", "Fiyatı belirleyen etkenler ve hızlı teklif"),
    "mekan": ("Eskişehir evlilik teklifi mekanları", "evlilik-teklifi-mekanlari", "Özel konseptler ve şehrin sevilen noktaları"),
    "surpriz": ("Sürpriz evlilik teklifi", "surpriz-evlilik-teklifi", "Sır nasıl saklanır, bahane nasıl kurulur"),
    "gondol": ("Gondolda evlilik teklifi", "gondolda-evlilik-teklifi", "Porsuk üzerinde, köprü altında bir soru"),
    "sazova": ("Sazova'da evlilik teklifi", "sazova-parki-evlilik-teklifi", "Masal Şatosu'nun önünde bir an"),
    "kanlikavak": ("Kanlıkavak'ta evlilik teklifi", "kanlikavak-parki-evlilik-teklifi", "Yeşilin içinde sakin bir teklif"),
    "nasil": ("Evlilik teklifi nasıl yapılır?", "blog/evlilik-teklifi-nasil-yapilir", "Tarihten konuşmaya adım adım plan"),
    "yuzuk": ("Yüzük ölçüsü nasıl öğrenilir?", "blog/evlilik-teklifi-yuzugu", "Sürprizi bozmadan beş yöntem"),
}


def ilg(c, *keys):
    return "<h2>Bunlara da göz atın</h2>" + ilgili(c, [KONSEPT_ILGILI[k] for k in keys])


# ======================================================================== ANA SAYFA
def fiyat_ozet(n=None):
    sirali = sorted(TEKLIF_KISA, key=lambda x: PAKET[x[0]]["fiyat"])[:n]
    return ", ".join(ad + " " + tl(PAKET[k]["fiyat"]) for k, ad in sirali)


OZELLIK_IKON = {
    "elmas": '<path d="M6 3h12l3 5-9 13L3 8z"/><path d="M3 8h18M9 3l3 5 3-5M12 8v13"/>',
    "parilti": '<path d="M12 2.5l1.8 5.2 5.2 1.8-5.2 1.8L12 16.5l-1.8-5.2L5 9.5l5.2-1.8z"/><path d="M18.5 15l.8 2.2 2.2.8-2.2.8-.8 2.2-.8-2.2-2.2-.8 2.2-.8z"/>',
    "hediye": '<rect x="3.5" y="9" width="17" height="11.5" rx="1"/><path d="M2.5 9h19V6.5h-19zM12 6.5v14"/><path d="M12 6.5C10 3 6.5 3.2 7 5.4 7.4 7 12 6.5 12 6.5zM12 6.5c2-3.5 5.5-3.3 5-1.1-.4 1.6-5 1.1-5 1.1z"/>',
    "odul": '<circle cx="12" cy="9" r="6"/><path d="M12 5.8l1 2.1 2.3.3-1.7 1.6.4 2.3-2-1.1-2 1.1.4-2.3-1.7-1.6 2.3-.3z"/><path d="M8.5 14l-2 7.5 3.5-1.8 2 3M15.5 14l2 7.5-3.5-1.8-2 3"/>',
}
OZELLIKLER = [("elmas", "Özel konsept<br>dekorasyon"), ("parilti", "Kurulum ve<br>süsleme bizden"),
              ("hediye", "Sürprizi birlikte<br>planlıyoruz"), ("odul", "20 yıllık<br>deneyim")]


def home_head(c):
    oz = "".join(f'<li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{OZELLIK_IKON[k]}</svg><span>{t}</span></li>'
                 for k, t in OZELLIKLER)
    # Yönetim panelindeki "ana sayfa fotoğrafları" girişin iki yanında hatıra kareleri olarak durur (en çok 4)
    kareler = "".join(polaroid(c, o["gorsel"], o.get("etiket") or "", f"k{i + 1}", sizes=KARE_BOYUT, eager=(i == 0))
                      for i, o in enumerate(slaytlar()[:4]))
    return f'''{header(c)}<section class="kahraman" aria-labelledby="ana-baslik">{kalpler(10, 4)}
<div class="kap kahraman-ic">
<div class="kahraman-metin">
{KALP_SVG}
<h1 id="ana-baslik"><span class="h1-sehir">Eskişehir</span> <span class="h1-yazi">Evlilik Teklifi</span></h1>
<p class="imza">Bir an değil, bir hikâyedir.</p>
<div class="kahraman-kareler">{kareler}</div>
<p class="giris">Işıkları yanan bir balon ev, şömineli bir bungalov ya da Porsuk'ta bir gondol. Evlilik teklifi organizasyonunun süslemesini, kurulumunu ve zamanlamasını biz hazırlayalım; size yalnızca soruyu sormak kalsın.</p>
<div class="dugmeler"><a class="dugme altin" href="{wa("Merhaba, Eskişehir'de evlilik teklifi için tarih sormak istiyorum.")}" data-konum="kahraman" target="_blank" rel="noopener">{IC_SOHBET} WhatsApp'tan tarih sor</a>
<a class="dugme cizgi" href="{c.L("evlilik-teklifi-fiyatlari")}">Paketler {tl(EN_DUSUK)}'den</a></div>
</div>
</div>
<div class="kap kahraman-bilgi"><ul class="ozellikler" aria-label="Neden biz">{oz}</ul></div>
</section>'''


KARE_BOYUT = "(max-width:860px) 46vw, 320px"


def vitrin_kart(c, key, cls, baslik, alt, foto=True, fiyat=None, sayfa=None):
    k = PAKET[key]
    g, yaz = "", " yazili"
    ref = next((r for r in (k.get("vitrin_foto"), k.get("foto")) if r and r in FOTO_VAR), None) if foto else None
    if ref and ref in FOTO_VAR:
        sz = "(max-width:700px) 100vw, 50vw" if cls else "(max-width:700px) 100vw, 25vw"
        g, yaz = img(c, ref, sizes=sz), ""
    return (f'<a class="vitrin-kart {cls}{yaz}" href="{c.L(sayfa or k["sayfa"])}">{g}<div class="vitrin-icerik"><div><h3>{baslik}</h3><p>{alt}</p></div>'
            f'<div class="vitrin-fiyat"><strong>{fiyat or tl(k["fiyat"])}</strong></div></div></a>')


KONSEPTLER = [  # paket kodu, ad, kısa tanım
    ("balon-ev", "Balon ev", "Şeffaf kubbe, neon yazı ve ışıklı MARRY ME harfleri"),
    ("bungalov", "Bungalov", "Işıklı A-frame, şömine başında masa ve LOVE harfleri"),
    ("karavan", "Karavan", "Sarı vintage karavan, gramofon ve ışık tavanı"),
    ("gondol", "Gondol", "Porsuk'ta köprü altında pankart, meşale ve güller"),
    ("kanlikavak", "Kanlıkavak", "İskelede kalpli çiçek duvarı ve neon yazı"),
    ("otel", "Otel odası", "Kalpli balonlar ve güllerle yazılmış Marry Me"),
    ("restoran", "Restoran", "Romantik masa, fenerler, fotoğraf ve video çekimi"),
    ("balon-dogum-gunu", "Doğum günü ve yıl dönümü", "Happy birthday ya da Better together neon yazı"),
]


def konseptler(c):
    out, kullanilan = [], set()
    for k, ad, tanim in KONSEPTLER:
        pk = PAKET[k]
        ozel = k in OZEL_GUN
        link = c.L("ozel-gun-surprizleri" if ozel else pk["sayfa"])
        rz = rozet(ozel_min(), "TL'den") if ozel else rozet(pk["fiyat"])
        ref = next((r for r in (pk.get("vitrin_foto"), pk.get("foto")) if r and r in FOTO_VAR and r not in kullanilan), None)
        if ozel:   # doğum günü kutlamasının kendi karesi: videodan bir an
            v = VIDEOS["dogum-gunu"]
            foto = f'<img src="{c.A(v["poster"])}" alt="Balon evde Happy birthday neon yazısıyla doğum günü sürprizi" width="{v["w"]}" height="{v["h"]}" loading="lazy" decoding="async">'
        elif ref:
            kullanilan.add(ref)
            foto = img(c, ref, sizes="(max-width:700px) 44vw, 240px")
        else:
            foto = f'<span class="konsept-bos">{KALP_SVG}</span>'
        out.append(f'<li><a class="konsept" href="{link}"><span class="konsept-foto">{foto}{rz}</span>'
                   f'<span class="konsept-ad">{ad}</span><span class="konsept-tanim">{tanim}</span></a></li>')
    return '<ul class="konseptler">' + "".join(out) + '</ul>'


def ara_bant(c):
    o = GORSEL.get("ara_bant") or {}
    if not (o.get("gorsel") and o["gorsel"] in FOTO_VAR):
        return ""
    return f'''<section class="ara-bant" aria-labelledby="ara-b"><div class="ara-bant-gorsel" data-paralaks>{img(c, o["gorsel"], sizes="100vw")}</div>
<div class="kap ara-bant-ic">{KALP_SVG}<p class="imza">Evet dedirten anlar</p>
<h2 id="ara-b" class="ara-bant-soz">Sevdiğiniz kişi “evet” derken her şey yerli yerinde olsun.</h2>
<div class="dugmeler"><a class="dugme altin" href="{wa("Merhaba, evlilik teklifi için tarih sormak istiyorum.")}" data-konum="ara-bant" target="_blank" rel="noopener">{IC_SOHBET} Tarihinizi sorun</a></div></div></section>'''


def bolum_bas(kicker, hid, baslik, metin="", orta=True):
    m = f"<p>{metin}</p>" if metin else ""
    return (f'<div class="bolum-bas{" orta" if orta else ""}"><span class="imza-ust">{kicker}</span><h2 id="{hid}">{baslik}</h2>'
            f'<div class="susleme" aria-hidden="true"><span></span></div>{m}</div>')


def home_body(c):
    paketler = "".join(paket_html(c, k, kisa=6) for k in ("balon-ev", "bungalov", "karavan"))
    sehir = "".join(f'<li><a href="{c.L(s)}"><strong>{n}</strong><span>Eskişehir\'e {km} km</span></a></li>' for n, s, km, _ in CITIES)
    v = VIDEOS["reels"]
    duzen = ["genis", "uzun", "", "", "genis", "genis", "", ""]
    mz = mozaik(c, [((o or {}).get("gorsel"), duzen[n % len(duzen)]) for n, o in enumerate(GORSEL.get("mozaik") or [])])
    rehber = [("blog/evlilik-teklifi-sozleri", "Evlilik teklifi sözleri", "Kısa, romantik ve duygusal örnekler; kendi sözünüzü yazmak için üç adım.", ("balon-ev", "balon-ev-ici-teklif-sonrasi-kutlama")),
              ("blog/evlilik-teklifi-nasil-yapilir", "Evlilik teklifi nasıl yapılır?", "Tarihten konuşmaya, teklif gününe kadar yapılacaklar sırasıyla.", ("balon-ev", "balon-ev-evlilik-teklifi-siyah-beyaz")),
              ("blog/evlilik-teklifi-yuzugu", "Evlilik teklifi yüzüğü", "Hangi parmağa takılır, ölçü sürprizi bozmadan nasıl öğrenilir?", ("bungalov", "evlilik-teklifi-yuzuk-bungalov-onunde"))]
    rh = "".join(f'<a class="rehber" href="{c.L(s)}"><div class="rehber-foto">{img(c, *f, sizes="(max-width:700px) 100vw, 33vw")}</div><div class="rehber-govde"><h3>{t}</h3><p>{d}</p></div></a>' for s, t, d, f in rehber)
    sss = "".join(f"<details><summary>{esc(q)}</summary><p>{a}</p></details>" for q, a in HOME_FAQ)
    galeri_metin = (f'Daha fazlası için <a href="{c.L("galeri")}">galeriye</a>, <a href="{C["INSTAGRAM"]}" target="_blank" rel="noopener">Instagram’a</a> '
                    f've <a href="{C["YOUTUBE"]}" target="_blank" rel="noopener">YouTube kanalımıza</a> göz atın.')
    cift = (polaroid(c, gorsel("tanitim_buyuk"), "Hazırlık bizden", "kare-bir", sizes="(max-width:1000px) 70vw, 460px")
            + polaroid(c, gorsel("tanitim_kucuk"), "Soru sizden", "kare-iki", sizes="(max-width:1000px) 44vw, 260px"))
    return f'''<section class="bolum acik" aria-labelledby="hikaye-b"><div class="kap slogan-izgara">
<div><span class="imza-ust">Hoş geldiniz</span><h2 id="hikaye-b" class="slogan">Siz soruyu düşünün, gerisini biz hazırlayalım.</h2>
<p class="giris">Evlilik teklifi birkaç dakika sürüyor; hatırlanması bir ömür. {C["PARENT"]}'un 20 yıllık organizasyon deneyimiyle Eskişehir'de yalnızca evlilik teklifine odaklanıyoruz. Alanı siz gelmeden kuruyor, ışıkları yakıyor ve sürprizi sonuna kadar sizinle birlikte saklıyoruz.</p>
<p class="ince">Eskişehir merkezli çalışıyoruz; Kütahya, Bilecik, Bozüyük, Afyonkarahisar ve Bursa'dan gelen çiftlerin tekliflerini de uzaktan planlıyoruz.</p>
<a class="bag" href="{c.L("hakkimizda")}">Bizi tanıyın</a></div>
<div class="polaroid-cift">{cift}</div>
</div></section>

<section class="bolum kirmizi" aria-labelledby="konsept-b">{kalpler(8, 11)}<div class="kap">
{bolum_bas("Konseptlerimiz", "konsept-b", "Eskişehir'de evlilik teklifi konseptleri", "Her konseptin içeriği belli bir paketi var. Fotoğraflar kendi kurulumlarımızdan, fiyatlar güncel kampanya fiyatlarıdır.")}
{konseptler(c)}
<p class="bolum-son"><a class="dugme cizgi" href="{c.L("evlilik-teklifi-mekanlari")}">Tüm konseptleri ve mekanları gör</a></p>
</div></section>

<section class="bolum bordo" aria-labelledby="paket-b"><div class="kap">
{bolum_bas("Paketler ve fiyatlar", "paket-b", "Balon ev, bungalov ve karavan paketleri", "Süsleme, kurulum, pasta ve soft içecek pakete dahil. Paketin dışında bir isteğiniz varsa yazın, fiyatını ayrıca iletelim.")}
<div class="paketler">{paketler}</div>
<p class="bolum-son"><a class="bag" href="{c.L("evlilik-teklifi-fiyatlari")}">Tüm paketleri ve içeriklerini gör</a></p>
</div></section>

{ara_bant(c)}

<section class="bolum pudra" aria-labelledby="adim-b"><div class="kap video-izgara">
<div class="telefon"><video data-oto muted loop playsinline preload="none" poster="{c.A(v["poster"])}" width="{v["w"]}" height="{v["h"]}" aria-label="{esc(v["ad"])}"><source src="{c.A(v["dosya"])}" type="video/mp4"></video></div>
<div><span class="imza-ust">Nasıl çalışıyoruz</span><h2 id="adim-b">Her ayrıntısı aşk dolu bir evet için</h2>
<p class="giris">Planlamanın tamamını yalnızca sizinle yürütüyoruz; sevdiğiniz kişi hiçbir şeyden haberdar olmuyor.</p>
<ol class="adimlar">
<li><div><h3>WhatsApp'tan yazın</h3><p>Tarih, şehir ve aklınızdaki konsepti iletin. Müsaitliği aynı gün paylaşıyoruz.</p></div></li>
<li><div><h3>Detayları birlikte seçin</h3><p>Neon yazı, notlar, müzik ve ortak fotoğraflarınız. Alanı sevdiğiniz kişiye göre kuruyoruz.</p></div></li>
<li><div><h3>Kurulumu biz yapıyoruz</h3><p>Teklif saatinden önce alan hazır, ışıklar yanıyor. Siz yalnızca onu zamanında getiriyorsunuz.</p></div></li>
<li><div><h3>Soruyu siz soruyorsunuz</h3><p>Gerisi sizin anınız. Toparlama ve söküm de bizde.</p></div></li>
</ol></div>
</div></section>

<section class="bolum kirmizi" aria-labelledby="galeri-b">{kalpler(6, 21)}<div class="kap">
{bolum_bas("Galeri", "galeri-b", "Kurduğumuz teklif alanlarından", galeri_metin)}
{mz}
</div></section>

<section class="bolum acik" aria-labelledby="yorum-b"><div class="kap">
{bolum_bas("Sizden gelenler", "yorum-b", "Bizimle çalışanlar ne diyor")}
<div class="yorumlar">{yorum_html(ana_yorumlar())}</div>
<p class="yorum-kaynak">Yorumlar müşterilerimizin kendi sözleridir; her yorumun kaynağı altında yazılı. <a href="{c.L("yorumlar")}">Tüm yorumlar</a></p>
</div></section>

<section class="bolum bordo" aria-labelledby="bolge-b"><div class="kap iki-sutun">
<div><span class="imza-ust">Hizmet bölgemiz</span><h2 id="bolge-b">Eskişehir merkezli, yakın illere açık</h2>
<p class="ince">Tepebaşı ve Odunpazarı başta olmak üzere Eskişehir'in tüm ilçelerinden çiftlerle çalışıyoruz. Yakın illerden gelenler için yol, saat ve kurulum planını mesafeye göre yapıyoruz.</p>
<ul class="liste-bag">{sehir}</ul>
<p class="kucuk" style="margin-top:1.4rem">Eskişehir ilçeleri: Tepebaşı, Odunpazarı, Sivrihisar, Alpu, Çifteler, Seyitgazi, İnönü, Mihalıççık, Mahmudiye, Sarıcakaya, Beylikova, Günyüzü, Han ve Mihalgazi. Mesafeler karayoluyla yaklaşık değerlerdir; harita şematiktir.</p></div>
<div class="harita">{map_svg("hm")}</div>
</div></section>

<section class="bolum pudra" aria-labelledby="neden-b"><div class="kap">
<div class="iki-sutun" style="margin-bottom:clamp(3rem,6vw,5rem)"><div><span class="imza-ust">Karar verirken</span><h2 id="neden-b">Eskişehir'de en iyi evlilik teklifi organizasyonunu nasıl seçersiniz?</h2></div>
<div><p>Fotoğrafı güzel olan her alan, sizin anınız için doğru alan olmayabilir. Karar verirken şu üç soruyu sormanızı öneriyoruz:</p>
<ul class="tik"><li><strong>Alan gerçekten size mi ayrılıyor?</strong> Teklif sırasında yanınızdan başka çiftlerin geçmemesi, anın tadını belirler.</li>
<li><strong>Kurulumu kim yapıyor, ne zaman bitiyor?</strong> Siz geldiğinizde her şeyin yanıyor ve hazır olması gerekir.</li>
<li><strong>Sürpriz nasıl korunuyor?</strong> İletişimin yalnızca sizinle yürümesi, sevdiğiniz kişinin hiçbir şey sezmemesi için önemli.</li></ul>
<p>Fiyatları ve paket içeriklerini <a href="{c.L("evlilik-teklifi-fiyatlari")}">evlilik teklifi organizasyonu fiyatları</a> sayfasında, Eskişehir evlenme teklifi hazırlığına nereden başlayacağınızı <a href="{c.L("blog/evlilik-teklifi-nasil-yapilir")}">adım adım rehberimizde</a> bulabilirsiniz.</p></div></div>
<div class="rehberler">{rh}</div>
</div></section>

<section class="bolum acik" aria-labelledby="sss-b"><div class="kap sss-izgara">
<div><span class="imza-ust">Merak edilenler</span><h2 id="sss-b">Evlilik teklifi hakkında sık sorulanlar</h2>
<p class="ince">Aradığınız cevap burada yoksa WhatsApp'tan sorun; aynı gün dönüyoruz.</p>
<a class="bag" href="{c.L("sss")}">Tüm soruları gör</a></div>
<div class="sss">{sss}</div>
</div></section>'''


HOME_FAQ = [
    ("Evlilik teklifi organizasyonu ne kadar önceden ayarlanmalı?",
     "En az bir hafta önceden yazmanızı öneriyoruz. Takvim uygunsa son dakika taleplerini de değerlendiriyoruz; hafta sonları ve 14 Şubat gibi özel günler daha erken doluyor."),
    ("Eskişehir'de evlilik teklifi fiyatları ne kadar?",
     f"Güncel paket fiyatlarımız: {fiyat_ozet()}. Fiyata paketteki süsleme ve kurulum dahil; paket dışındaki istekler için fiyatı ayrıca iletiyoruz."),
    ("Hangi konsepti seçmeliyim?",
     "Göz alıcı ve büyük bir sahne istiyorsanız balon ev, sıcak ve kapalı bir ortam istiyorsanız bungalov, daha rahat bir hava istiyorsanız karavan iyi bir başlangıç. Şehrin içinde bir an için gondol ya da Kanlıkavak, baş başa bir gece için otel konsepti var. Kararsızsanız sevdiğiniz kişiyi anlatın, birlikte seçelim."),
    ("Yakın illerden gelen çiftlerle çalışıyor musunuz?",
     "Evet. Kütahya, Tavşanlı, Bilecik, Bozüyük, Afyonkarahisar, Bursa ve İnegöl'den gelen çiftlerle çalışıyoruz. Yol süresine göre saat planını birlikte yapıyoruz."),
    ("Sürpriz nasıl bozulmuyor?",
     "Tüm planlamayı yalnızca sizinle WhatsApp üzerinden yürütüyoruz. Sevdiğiniz kişiyi alana nasıl getireceğinizi de birlikte kurguluyoruz."),
    ("Teklifi kadınlar da yapabilir mi?",
     "Elbette. Teklifi kimin yaptığı fark etmez; hazırlık ve kurulum aynı özenle yapılır."),
]


# ======================================================================== KONSEPT SAYFALARI
def konsept(c, p, giris, gal, sonra="", ilg_keys=("fiyat", "surpriz", "mekan")):
    inner = giris + f'<h2>{GALERI[gal][0]} fotoğrafları</h2>' + gallery(c, [gal]) + sonra + sss_html(p["faq"]) + ilg(c, *ilg_keys)
    return article_layout(c, p, inner)


def balon_body(c):
    p = PAGES_BY["balon-ev-evlilik-teklifi"]
    giris = f'''<h2>Balon ev nedir?</h2>
<p>Balon ev, altıgen şeffaf panellerden oluşan bir kubbe. İçerisi dışarıdan görünüyor; akşam olup ışıklar yandığında kubbe, karanlığın ortasında parlayan bir fener gibi duruyor. Eskişehir'deki balon evimiz, ışıklı bungalovumuzla aynı bahçede yan yana.</p>
<h2>Balon ev evlilik teklifinde sizi neler bekliyor?</h2>
<p>Fotoğraflarda gördüğünüz düzen, en çok tercih edilen kurulum:</p>
<ul><li>Kubbeye uzanan kırmızı halı ve iki yanında fenerler</li>
<li>Kubbenin iki yanında ışıklı, dev MARRY ME harfleri</li>
<li>İçeride beyaz şömine, iki kişilik masa ve “Benimle evlenir misin?” neon yazısı</li>
<li>Lambader, yeşillikler ve ortak fotoğraflarınızı asabileceğimiz küçük bir pano</li>
<li>Bahçenin üzerinde ışık zincirleri</li></ul>
<p>Pakete pasta ve soft içecek, kutu içinde notlar, fotoğraf köşesi, volkan, meşale, ses sistemi ve ışıklı salıncak da dahil. Paket içeriğinin tamamı ve güncel fiyatı bu sayfadaki paket kartında; tarih sormak için <a href="{c.L("teklif-al")}?konsept=balon-ev">fiyat teklifi formunu</a> kullanabilirsiniz.</p>
<h2>En güzel saat hangisi?</h2>
<p>Balon ev, gün batımından sonra en etkili halini alıyor: ışıklar yanıyor, kubbe içeriden aydınlanıyor ve MARRY ME harfleri karanlıkta öne çıkıyor. Saati mevsime göre birlikte belirliyoruz; kış aylarında güneş erken battığı için akşamüstü saatleri de iyi sonuç veriyor.</p>
<h2>Balon ev kimler için?</h2>
<p>Sevdiği kişiye “vay” dedirtmek isteyenler, anı büyük bir sahneyle başlatmak isteyenler ve teklifin ardından içeride baş başa oturup kutlamak isteyenler için. Daha kapalı ve sıcak bir ortam istiyorsanız <a href="{c.L("bungalov-evlilik-teklifi")}">bungalov</a>, daha serbest bir hava istiyorsanız <a href="{c.L("karavan-evlilik-teklifi")}">karavan</a> konseptine de bakın.</p>'''
    sonra = f"<h2>Balon evde evet anı</h2>{video_html(c)}"
    return konsept(c, p, giris, "balon-ev", sonra, ("bungalov", "fiyat", "surpriz"))


def bungalov_body(c):
    p = PAGES_BY["bungalov-evlilik-teklifi"]
    giris = f'''<h2>Bungalovda evlilik teklifi nasıl görünüyor?</h2>
<p>Bungalovumuz, üçgen çatılı bir A-frame. Çatı kenarları geceleri kırmızı ışıkla çiziliyor, ön cephesi camlı. Önüne ışıklı LOVE ya da MARRY ME harflerini, kırmızı halıyı ve fenerleri diziyoruz; içeriyi ise şömine, iki koltuk, masa ve neon “Will you marry me” yazısıyla hazırlıyoruz.</p>
<h2>Bungalov konseptinde neler var?</h2>
<ul><li>Işıklı A-frame cephe, kırmızı halı ve fenerler</li>
<li>Önde ışıklı LOVE veya MARRY ME harfleri</li>
<li>İçeride şömine, iki kişilik masa, koltuklar ve neon yazı</li>
<li>Evet'in ardından bungalov önünde maytaplarla kutlama</li>
<li>Kapının yanında süslü bir bisiklet ve küçük detaylar</li></ul>
<p>Nostaljik gramofon, pasta ve soft içecek, kutu içinde notlar, fotoğraf köşesi, volkan, meşale ve ışıklı salıncak da pakete dahil. Tam liste ve güncel fiyat bu sayfadaki paket kartında.</p>
<h2>Neden bungalov?</h2>
<p>Bungalov, teklifi kapalı ve sıcak bir mekânda yapmak isteyenler için en rahat seçenek. Soğuk Eskişehir akşamlarında içeride şöminenin yanında oturmak, teklif kadar akılda kalan bir an oluyor. Dışarıda sahne kurup içeride kutlamaya geçmek de mümkün.</p>
<h2>Bungalov ile balon ev aynı yerde mi?</h2>
<p>Evet, ikisi aynı bahçede yan yana duruyor. Hangi alanın sizin anınıza daha uygun olduğuna fotoğraflara bakarak karar verebilir, <a href="{c.L("balon-ev-evlilik-teklifi")}">balon ev</a> sayfasındaki kurulumla karşılaştırabilirsiniz.</p>'''
    return konsept(c, p, giris, "bungalov", "", ("balon", "karavan", "fiyat"))


def karavan_body(c):
    p = PAGES_BY["karavan-evlilik-teklifi"]
    giris = f'''<h2>Karavan konsepti nasıl bir teklif?</h2>
<p>Papatya desenli, sarı bir vintage karavan; pek çok kişinin “vosvos” diye bildiği klasik minibüs formunda. Önüne piknik örtüsü, hasır minderler ve alçak bir masa seriyoruz; yanına küçük bir çadır ve süslü bir bisiklet koyuyoruz. Tepede ışık zincirlerinden bir tavan, yanda ışıklı LOVE harfleri. Sonuç, bir festival akşamı kadar rahat ama bir o kadar özel bir sahne.</p>
<h2>Karavan konseptinde neler var?</h2>
<ul><li>Sarı vintage karavan ve kapısı açık, süslenmiş iç kısım</li>
<li>Piknik örtüsü, minderler ve alçak masa</li>
<li>Çadır, bisiklet ve küçük dekor detayları</li>
<li>Işık zinciri tavanı ve ışıklı LOVE harfleri</li>
<li>Romantik masa, nostaljik gramofon, pasta ve soft içecek</li></ul>
<p>Kalpli kutu içinde notlar, fotoğraf köşesi, kırmızı halı ve fenerler, volkan, meşale ve ışıklı salıncak da pakete dahil. Güncel fiyat bu sayfadaki paket kartında.</p>
<h2>Karavan kimler için?</h2>
<p>Yolculuk, kamp ve doğa hikâyesi olan çiftler; büyük bir sahneden çok rahat ve sıcak bir an isteyenler; arkadaş grubuyla birlikte sürpriz kutlama planlayanlar. Daha kapalı bir ortam istiyorsanız <a href="{c.L("bungalov-evlilik-teklifi")}">bungalovu</a> düşünebilirsiniz.</p>
<h2>Hava ve mevsim</h2>
<p>Karavan konsepti açık havada kuruluyor. Tarihi seçerken hava durumunu birlikte takip ediyor, gerekirse saati ya da konsepti önceden konuşuyoruz.</p>'''
    return konsept(c, p, giris, "karavan", "", ("balon", "bungalov", "fiyat"))


# ======================================================================== MEKAN SAYFALARI
def mekanlar_body(c):
    p = PAGES_BY["evlilik-teklifi-mekanlari"]
    def kart(key, s, t, d, foto=None):
        g = img(c, *foto, sizes="(max-width:700px) 100vw, 380px") if foto else ""
        f = f'<p class="mekan-fiyat">{tl(PAKET[key]["fiyat"])}</p>' if key in PAKET else '<p class="mekan-fiyat">Fiyat için yazın</p>'
        return f'<a class="mekan" href="{c.L(s)}">{g}<div><h3>{t}</h3><p>{d}</p>{f}</div></a>'
    inner = f'''<h2>Size ayrılan özel teklif alanları</h2>
<p>Teklif anında yanınızdan kimsenin geçmemesini, her şeyin siz gelmeden hazır ve yanıyor olmasını istiyorsanız en rahat seçenek özel bir alan. Eskişehir'deki balon ev, bungalov ve karavan konseptlerimiz bunun için kuruldu; otel konseptinde ise süslemeyi kalacağınız odaya taşıyoruz:</p>
<div class="mekanlar">{kart("balon-ev", "balon-ev-evlilik-teklifi", "Balon ev", "Şeffaf kubbe, şömine, neon yazı ve MARRY ME harfleri.", ("balon-ev", "eskisehir-balon-ev-evlilik-teklifi-marry-me"))}{kart("bungalov", "bungalov-evlilik-teklifi", "Bungalov", "Işıklı A-frame, sıcak iç mekân, LOVE harfleri.", ("bungalov", "eskisehir-bungalov-evlilik-teklifi-marry-me"))}{kart("karavan", "karavan-evlilik-teklifi", "Karavan", "Sarı vintage karavan, gramofon, ışık tavanı.", ("karavan", "eskisehir-karavan-evlilik-teklifi-love"))}{kart("otel", "otel-odasinda-evlilik-teklifi", "Otel odası", "Kalpli balonlar, güllerle MARRY ME ve romantik notlar.", ("otel", "otel-odasi-evlilik-teklifi-marry-me-gul"))}</div>
<h2>Eskişehir'de evlilik tekliflerine sahne olan yerler</h2>
<p>Şehrin kendisi de romantik bir dekor. Yerel basına yansıyan pek çok teklif bu noktalarda yapıldı:</p>
<div class="mekanlar">{kart("gondol", "gondolda-evlilik-teklifi", "Porsuk'ta gondol", "Adalar'da köprünün altından geçerken sorulan soru. Gondol ücreti hariç.", ("gondol", "porsuk-gondol-evlilik-teklifi"))}{kart("kanlikavak", "kanlikavak-parki-evlilik-teklifi", "Kanlıkavak", "İskelede kalpli çiçek duvarı, neon yazı ve masa.", ("kanlikavak", "kanlikavak-iskele-evlilik-teklifi-kalp-cicek"))}{kart("restoran", "gaga-restoran-evlilik-teklifi", "Restoranda teklif", "Gaga gibi manzaralı bir masada akşam yemeği. Yemek hariç.")}{kart("sazova", "sazova-parki-evlilik-teklifi", "Sazova Parkı", "Masal Şatosu ve Korsan Gemisi'nin olduğu park.")}</div>
<p>Orman konsepti için de tarih ve detayları WhatsApp'tan sorabilirsiniz.</p>
<h2>Eskişehir'de evlenme teklifi edilecek diğer yerler</h2>
<ul><li><strong>Odunpazarı Evleri:</strong> Renkli tarihi evlerin arasındaki dar sokaklar, akşam yürüyüşüyle başlayan bir teklif için güzel bir dekor.</li>
<li><strong>Adalar ve Porsuk kıyısı:</strong> Gece ışıklandırmasıyla şehrin en romantik yürüyüş rotalarından biri.</li>
<li><strong>Kentpark:</strong> Geniş alanı ve su kenarıyla gündüz ya da gün batımı teklifleri için.</li>
<li><strong>Yazılıkaya:</strong> Han ilçesindeki tarihi alan; farklı ve sakin bir hikâye isteyenler için yerel basına da yansıyan bir teklif noktası.</li>
<li><strong>Bir sinema salonu:</strong> Film arasında perdeye yansıyan bir video; Eskişehir'de bu şekilde yapılmış teklifler de haber oldu.</li></ul>
<h2>Halka açık mı, özel mi?</h2>
<table><thead><tr><th></th><th>Halka açık mekân</th><th>Özel konsept alanı</th></tr></thead><tbody>
<tr><td>Kalabalık</td><td>Saate göre değişir, çevrede başkaları olabilir</td><td>Alan yalnızca size ayrılır</td></tr>
<tr><td>Süsleme</td><td>Alanın yönetiminin iznine bağlıdır</td><td>Konsepte göre tam kurulum</td></tr>
<tr><td>Hava durumu</td><td>Açık havaya bağlıdır</td><td>Balon ev ve bungalovda iç mekân seçeneği var</td></tr>
<tr><td>Sürpriz</td><td>Rastlantıyla bozulma ihtimali daha yüksek</td><td>Kontrol tamamen planlamada</td></tr></tbody></table>
<p>Halka açık bir noktada teklif etmek istiyorsanız da yazın; zamanlama ve kurgu için birlikte bakalım. Teklifi şehirde yapıp kutlamayı aynı akşam özel bir alanda sürdürmek de sık tercih edilen bir plan.</p>'''
    inner += sss_html(p["faq"]) + ilg(c, "fiyat", "surpriz", "nasil")
    return article_layout(c, p, inner)


def gondol_body(c):
    p = PAGES_BY["gondolda-evlilik-teklifi"]
    inner = f'''<h2>Porsuk'ta gondol: Eskişehir'in en bilinen teklif sahnesi</h2>
<p>Porsuk Çayı üzerinde gondol turu, şehrin simgelerinden biri. Adalar bölgesinde köprülerin altından geçen gondollar, yıllardır evlilik tekliflerine de sahne oluyor. Yerel basına yansıyan örneklerde senaryo genellikle aynı: gondol köprünün altına yaklaşırken arkadaşlar köprünün üstünden “Benimle evlenir misin?” yazılı bir pankart açıyor ve soru o an soruluyor.</p>
<figure class="icerik-foto foto-dar">{img(c, "gondol", "porsuk-gondol-evlilik-teklifi", "380px")}<figcaption class="kucuk">Porsuk'ta gondolda diz çökülen an</figcaption></figure>
<h2>Gondol paketinde neler var?</h2>
<ul class="tik">{"".join(f"<li>{x}</li>" for x in PAKET["gondol"]["icerik"])}</ul>
<p>Paket fiyatı <strong>{tl(PAKET["gondol"]["fiyat"])}</strong>. {esc(PAKET["gondol"]["not_"])}</p>
<h2>Gondolda teklifin güçlü ve zor yanları</h2>
<ul><li><strong>Güçlü yanı:</strong> Şehrin kalbinde, herkesin tanıdığı bir an. Köprüdeki pankart ve alkışlayan kalabalık sahneyi büyütüyor.</li>
<li><strong>Zor yanı:</strong> Sefer saatleri, sıra ve kalabalık size bağlı değil. Hafta sonları ve bayramlarda iskele çok yoğun olabiliyor.</li>
<li><strong>Mevsim:</strong> Gondol turlarına talep yazın artıyor. Soğuk kış günlerinde seferlerin durumunu önceden kontrol etmek gerekiyor.</li></ul>
<h2>Plan önerimiz</h2>
<p><strong>Gondol konsepti</strong> hizmetlerimiz arasında: kurguyu, süslemeyi, zamanlamayı ve köprüdeki ekibin yerini sizinle birlikte planlıyoruz. Gondol seferlerinin saatleri ve özel kullanım koşulları işletme tarafından belirlendiği için tarihinizi önceden netleştirmek gerekiyor. Pek çok çift teklifi gondolda yapıp akşamı <a href="{c.L("balon-ev-evlilik-teklifi")}">balon evde</a> ya da <a href="{c.L("bungalov-evlilik-teklifi")}">bungalovda</a> baş başa bir kutlamayla bitirmeyi seçiyor.</p>
<div class="not-kutu"><p>Gondolda teklif planlıyorsanız tarih ve saatinizi WhatsApp'tan yazın; size uygun kurguyu ve aynı akşam için kutlama seçeneklerini birlikte konuşalım.</p></div>'''
    inner += sss_html(p["faq"]) + ilg(c, "sazova", "kanlikavak", "balon")
    return article_layout(c, p, inner)


def sazova_body(c):
    p = PAGES_BY["sazova-parki-evlilik-teklifi"]
    inner = f'''<h2>Masal Şatosu'nun önünde bir soru</h2>
<p>Resmi adıyla Sazova Bilim, Kültür ve Sanat Parkı, Tepebaşı'nda, Kütahya yolu üzerinde. Masal Şatosu, Korsan Gemisi, göl kenarı ve geniş çimenlikleriyle Eskişehir'in en çok fotoğraflanan yerlerinden biri. Şato silueti, “masal gibi” bir teklif isteyenler için güçlü bir arka plan.</p>
<h2>Sazova'da teklif için pratik notlar</h2>
<ul><li><strong>Kalabalık:</strong> Park, gündüz saatlerinde aileler ve çocuklarla dolu oluyor. Akşamüstü ve hafta içi daha sakin.</li>
<li><strong>Saatler:</strong> Parkın açılış ve kapanış saatleri yaz ve kış döneminde farklı. Masal Şatosu gibi bölümlerin ayrıca giriş ücreti ve kendi saatleri var; gitmeden önce kontrol edin.</li>
<li><strong>Kurulum:</strong> Halka açık bir parkta süsleme ve kurulum, park yönetiminin iznine bağlı.</li></ul>
<h2>Plan önerimiz</h2>
<p><strong>Sazova konsepti</strong> hizmetlerimiz arasında; kurgu, süsleme ve zamanlamayı birlikte planlıyoruz. Parkın kuralları ve izinleri tarihe göre değişebildiği için uygunluğu önceden kontrol ediyoruz. Alternatif olarak Sazova'da kısa ve sade bir an kurgulayıp asıl sahneyi özel bir alanda hazırlamak da mümkün: parkta bir yürüyüş, ardından ışıkların yandığı bir <a href="{c.L("balon-ev-evlilik-teklifi")}">balon ev</a>. Masalsı bir hava istiyorsanız, şeffaf kubbe ve MARRY ME harfleri Sazova'daki şato kadar etkileyici bir dekor sunuyor.</p>
<div class="not-kutu"><p>Sazova'da ya da sonrasında özel bir alanda teklif planlıyorsanız tarihinizi yazın; kurguyu birlikte netleştirelim.</p></div>'''
    inner += sss_html(p["faq"]) + ilg(c, "gondol", "kanlikavak", "balon")
    return article_layout(c, p, inner)


def kanlikavak_body(c):
    p = PAGES_BY["kanlikavak-parki-evlilik-teklifi"]
    inner = f'''<h2>Yeşilin içinde sakin bir teklif</h2>
<p>Kanlıkavak Parkı, şehrin kuzeydoğusunda, geniş çim alanları ve yürüyüş yollarıyla bilinen bir park. <strong>Kanlıkavak iskele konseptimizde</strong> teklifi parkın iskelesinde, suyun kenarında kuruyoruz. Sazova ya da Adalar kadar turistik değil; bu da onu, kalabalıktan uzak ve daha kişisel bir an isteyen çiftler için ilginç bir seçenek yapıyor.</p>
<figure class="icerik-foto foto-dar">{img(c, "kanlikavak", "kanlikavak-iskele-evlilik-teklifi-kalp-cicek", "380px")}<figcaption class="kucuk">Kanlıkavak konsepti: kalpli çiçek süslemesi, neon yazı ve romantik masa</figcaption></figure>
<h2>Kanlıkavak paketinde neler var?</h2>
<ul class="tik">{"".join(f"<li>{x}</li>" for x in PAKET["kanlikavak"]["icerik"])}</ul>
<p>Paket fiyatı <strong>{tl(PAKET["kanlikavak"]["fiyat"])}</strong>.</p>
<h2>Kanlıkavak'ta teklif için pratik notlar</h2>
<ul><li><strong>Atmosfer:</strong> Açık ve yeşil; gün batımına yakın saatlerde yumuşak bir ışık.</li>
<li><strong>Kalabalık:</strong> Hafta sonu gündüzleri yürüyüşçüler ve aileler olabilir; akşamüstü daha sakin.</li>
<li><strong>Kurulum:</strong> Halka açık bir parkta süsleme ve kurulum, alanın yönetiminin iznine bağlı.</li></ul>
<h2>Plan önerimiz</h2>
<p>İskele konseptinin yanında, parkta bir yürüyüşle başlayıp teklifi özel bir alanda yapmak ya da parkta kısa bir sürprizle soruyu sorup kutlamayı <a href="{c.L("bungalov-evlilik-teklifi")}">bungalovda</a> sürdürmek mümkün. Doğa ve yeşil sizin için önemliyse <a href="{c.L("karavan-evlilik-teklifi")}">karavan konsepti</a> de aynı rahat havayı özel bir alanda sunuyor.</p>
<div class="not-kutu"><p>Kanlıkavak'ta ya da yakınında teklif düşünüyorsanız yazın; zamanlamayı ve kutlama seçeneklerini birlikte planlayalım.</p></div>'''
    inner += sss_html(p["faq"]) + ilg(c, "gondol", "sazova", "karavan")
    return article_layout(c, p, inner)


# ======================================================================== SÜRPRİZ, FİYAT, FORM
def surpriz_body(c):
    p = PAGES_BY["surpriz-evlilik-teklifi"]
    inner = f'''<h2>Sürprizin asıl işi: sır saklamak</h2>
<p>Romantik bir evlilik teklifinin en zor kısmı süsleme değil, sevdiğiniz kişinin hiçbir şey sezmemesi. Bu yüzden planlamayı yalnızca sizinle, WhatsApp üzerinden yürütüyoruz; telefonunuza gelen mesajlar bile sürprizi ele vermesin diye kısa ve sade tutuyoruz.</p>
<h2>Onu alana nasıl getireceksiniz?</h2>
<p>En çok işe yarayan bahaneler genellikle en sıradan olanlar:</p>
<ul><li>“Bir arkadaşın doğum günü var, kısa uğrayacağız.”</li>
<li>“Yeni açılan bir yerde akşam yemeği ayırttım.”</li>
<li>“Hafta sonu kafa dinlemek için şehir dışına çıkalım.”</li>
<li>“Bir fotoğraf çekimi için sözleştik.”</li></ul>
<p>Hangisini seçerseniz seçin, karşı tarafın o güne uygun giyinmesini sağlayacak bir ipucu bırakmayı unutmayın; çoğu kişi teklif fotoğraflarında güzel görünmek istiyor.</p>
<h2>Zamanlama</h2>
<p>Işıklı konseptlerde en etkili an, havanın karardığı saatler. Varış saatinizi, yol süresini ve gün batımını hesaba katarak birlikte belirliyoruz. Siz yola çıktığınızda alan hazır oluyor, ışıklar yanıyor.</p>
<h2>Sırdaşınızı seçin</h2>
<p>Planı bilen kişi sayısını olabildiğince az tutun. Bir yakın arkadaş ya da kardeş genellikle yeterli; teklif sonrası kutlamaya katılacak bir grup varsa onların ne zaman ve nereden geleceğini de birlikte planlıyoruz.</p>
<h2>Romantik ama size ait</h2>
<p>Ortak bir şarkı, ilk buluşmanızın tarihi, birlikte gittiğiniz bir şehrin adı... Alanı sizin hikâyenizden küçük detaylarla kişiselleştiriyoruz. Balon evdeki fotoğraf panosu, ortak fotoğraflarınızı asmak için iyi bir yer.</p>'''
    inner += sss_html(p["faq"]) + ilg(c, "nasil", "balon", "fiyat")
    return article_layout(c, p, inner)


def fiyat_body(c):
    p = PAGES_BY["evlilik-teklifi-fiyatlari"]
    satir = [("Gondol", "gondol", "Gondol ücreti dahil değil"), ("Balon ev", "balon-ev", ""), ("Bungalov", "bungalov", ""),
             ("Karavan", "karavan", ""), ("Kanlıkavak", "kanlikavak", ""), ("Otel odası", "otel", ""),
             ("Restoran", "restoran", "Yemek dahil değil"), ("Balon ev, doğum günü", "balon-dogum-gunu", ""),
             ("Balon ev, yıl dönümü", "balon-yildonumu", ""), ("Bungalov, doğum günü", "bungalov-dogum-gunu", ""),
             ("Bungalov, yıl dönümü", "bungalov-yildonumu", "")]
    rows = "".join(f'<tr><td><a href="{c.L(PAKET[k]["sayfa"])}">{a}</a></td><td>{tl(PAKET[k]["fiyat"])}</td><td>{n}</td></tr>' for a, k, n in satir)
    rows += f'<tr><td><a href="{c.L("sazova-parki-evlilik-teklifi")}">Sazova Parkı</a></td><td>Sorunuz</td><td>Tarihe ve izne göre</td></tr>'
    kartlar = "".join(paket_html(c, k) for k in ("balon-ev", "bungalov", "karavan", "kanlikavak", "gondol", "otel", "restoran"))
    inner = f'''<h2>Güncel paket fiyatları</h2>
<p>Eskişehir'deki evlilik teklifi paketlerimizin güncel kampanya fiyatları aşağıda. Fiyata paketteki süsleme ve kurulum dahil. Kampanya fiyatları dönemseldir; tarih sorarken güncelliğini birlikte teyit ediyoruz.</p>
<table class="fiyatlar-tablo"><thead><tr><th>Konsept</th><th>Fiyat</th><th>Not</th></tr></thead><tbody>{rows}</tbody></table>
<h2>Evlilik teklifi paketleri ve içerikleri</h2>
<div class="paketler ikili">{kartlar}</div>
<h2>Doğum günü ve yıl dönümü</h2>
<p>Balon ev ve bungalovda doğum günü ve yıl dönümü sürprizleri {tl(ozel_min())} ile {tl(ozel_max())} arasında. İçerikleri <a href="{c.L("ozel-gun-surprizleri")}">doğum günü ve yıl dönümü sürprizleri</a> sayfasında.</p>
<h2>Fiyatı ne değiştirir?</h2>
<ul><li><strong>Paket dışı istekler:</strong> Ek çiçek, farklı bir yazı ya da teklif sonrası kutlamaya katılacak kalabalık bir grup gibi istekler için fiyatı ayrıca iletiyoruz.</li>
<li><strong>Dahil olmayanlar:</strong> Gondol konseptinde gondol ücreti, restoran konseptinde yemek pakete dahil değil.</li>
<li><strong>Yoğun tarihler:</strong> 14 Şubat ve yılbaşı gibi günler erken doluyor; bu tarihler için olabildiğince erken yazın.</li></ul>
<h2>Bütçenize göre plan</h2>
<p>En uygun başlangıç {tl(en_uygun()[1])} ile {en_uygun()[0]} paketi. Bütçeniz belliyse baştan söyleyin; o bütçeyle en etkili düzeni birlikte kuralım. Hafta içi tarihler hem daha sakin hem de planlaması daha kolay.</p>
<div class="not-kutu"><p><strong>En hızlı yol:</strong> <a href="{c.L("teklif-al")}">Fiyat teklifi formunu</a> doldurun; konsept, şehir ve tarihi tek mesajda WhatsApp'a gönderin.</p></div>'''
    inner += sss_html(p["faq"]) + ilg(c, "balon", "bungalov", "otel")
    return article_layout(c, p, inner)


def teklif_body(c):
    konsept = [(k, a, tl(PAKET[k]["fiyat"])) for k, a in (("balon-ev", "Balon ev"), ("bungalov", "Bungalov"), ("karavan", "Karavan"),
               ("gondol", "Gondol"), ("kanlikavak", "Kanlıkavak"), ("otel", "Otel odası"), ("restoran", "Restoran"))]
    konsept += [("ozel-gun", "Doğum günü / yıl dönümü", tl(ozel_min()) + "'den"), ("sazova", "Sazova Parkı", "Fiyat için sorun"),
                ("karar-yok", "Karar vermedim", "Birlikte seçelim")]
    k = "".join(f'<label class="secenek"><input type="radio" name="konsept" value="{v}" data-ad="{a}"><span>{a}<small>{d}</small></span></label>' for v, a, d in konsept)
    ekstra = ["Ek çiçek / buket", "Farklı bir pasta", "Ek ikram", "Kendi şarkımız", "Maytap ile kutlama", "Ortak fotoğraflarla pano",
              "Arkadaş / aile katılımı", "Kendi yazımız (neon veya pano)"]
    e = "".join(f'<label class="isaret"><input type="checkbox" name="ekstra" value="{x}"> {x}</label>' for x in ekstra)
    s = "".join(f"<option>{x}</option>" for x in SEHIR_SECENEK)
    return f'''<div class="bolum"><div class="kap icerik-izgara"><div>
<form class="form" data-teklif aria-label="Konsepte göre fiyat teklifi formu">
<fieldset><legend>1. Konsept</legend><div class="secenekler">{k}</div></fieldset>
<div class="iki"><div><label class="etiket" for="ft-s">2. Şehir / ilçe</label><select id="ft-s" name="sehir">{s}</select></div>
<div><label class="etiket" for="ft-t">3. Tarih</label><input id="ft-t" type="date" name="tarih"></div></div>
<div class="iki"><div><label class="etiket" for="ft-h">Saat tercihi</label><select id="ft-h" name="saat"><option value="">Esnek</option><option>Gün batımı</option><option>Akşam</option><option>Gece</option></select></div><div></div></div>
<fieldset><legend>4. Paket dışı istekleriniz</legend><div class="isaret-liste">{e}</div></fieldset>
<div class="iki"><div><label class="etiket" for="ft-a">Adınız</label><input id="ft-a" type="text" name="ad" autocomplete="given-name"></div>
<div><label class="etiket" for="ft-p">Telefon (isteğe bağlı)</label><input id="ft-p" type="tel" name="telefon" autocomplete="tel"></div></div>
<div><label class="etiket" for="ft-n">Not</label><textarea id="ft-n" name="not" placeholder="Bütçe, renk tercihi, sevdiğiniz kişiye dair küçük bir ipucu..."></textarea></div>
<div><button class="dugme sarap" type="submit">{IC_SOHBET} Teklif talebini WhatsApp'a gönder</button></div>
<p class="form-sonuc" role="status"></p>
<p class="kucuk">Gönder dediğinizde seçimleriniz düzenli bir mesaj olarak WhatsApp'ta açılır; mesajı siz gönderirsiniz. Bilgileriniz bu sitede saklanmaz. Ayrıntılar: <a href="{c.L("gizlilik")}">gizlilik</a>.</p>
</form></div>
<aside class="yan"><div class="yan-bag"><h2>Sonra ne oluyor?</h2><ul>
<li>Mesajınız bize WhatsApp'tan ulaşıyor.</li><li>Tarihinizin müsaitliğini kontrol ediyoruz.</li>
<li>Paket fiyatını ve varsa ek isteklerin fiyatını aynı gün iletiyoruz.</li><li>Onayınızla tarihinizi ayırıyoruz.</li></ul></div>
<div class="yan-iletisim"><h2>Form yerine aramak isterseniz</h2><p>Hafta içi ve hafta sonu telefonla da ulaşabilirsiniz.</p><a class="dugme altin" href="tel:{C["TEL1"]}" data-konum="form-yan">{IC_TEL} {C["TEL1_TXT"]}</a>
<a class="dugme cizgi" href="tel:{C["TEL2"]}" data-konum="form-yan">{IC_TEL} {C["TEL2_TXT"]}</a></div></aside>
</div></div>'''


# ======================================================================== ŞEHİR SAYFALARI
def sehir(c, slug, inner):
    p = PAGES_BY[slug]
    harita = f'<figure class="harita" style="margin:1.6em 0">{map_svg("sm", slug)}</figure>'
    uz = next((y for y in YORUMLAR if "uzaktan" in y[1].lower()), YORUMLAR[0] if YORUMLAR else None)
    yorum = f'<blockquote>“{esc(uz[2])}”<br><span class="kucuk">{esc(uz[0])}, {esc(uz[1].lower())}</span></blockquote>' if uz else ""
    return article_layout(c, p, inner.replace("{HARITA}", harita).replace("{YORUM}", yorum) + sss_html(p["faq"]) + ilg(c, "balon", "bungalov", "karavan"))


def kutahya_body(c):
    return sehir(c, "kutahya-evlilik-teklifi", f'''<h2>Kütahya'dan Eskişehir'e: yaklaşık bir saatlik bir sürpriz</h2>
<p>Kütahya ile Eskişehir arası karayoluyla yaklaşık 80 km. Bu mesafe, teklif gününü küçük bir kaçamağa dönüştürmek için ideal: akşamüstü yola çıkıyorsunuz, hava kararırken ışıkları yanmış bir alana varıyorsunuz.</p>
{{HARITA}}
<h2>Tavşanlı ve Kütahya ilçelerinden gelen çiftler</h2>
<p>Tavşanlı başta olmak üzere Kütahya'nın ilçelerinden gelen çiftlerle de çalışıyoruz. Yol süresi ilçeye göre değiştiği için varış saatini birlikte hesaplıyor, kurulumu buna göre tamamlıyoruz.</p>
<h2>Uzaktan planlama nasıl işliyor?</h2>
<p>Planlamanın tamamı WhatsApp ve telefon üzerinden ilerliyor; teklif gününe kadar Eskişehir'e gelmeniz gerekmiyor. Konsepti fotoğraflardan seçiyor, detayları mesajla netleştiriyoruz.</p>
{{YORUM}}
<h2>Hangi konsept Kütahya'dan gelen çiftlere uygun?</h2>
<ul><li><a href="{c.L("balon-ev-evlilik-teklifi")}">Balon ev</a>: yolculuğun sonunda büyük ve ışıltılı bir sahne.</li>
<li><a href="{c.L("bungalov-evlilik-teklifi")}">Bungalov</a>: uzun yolun ardından sıcak ve kapalı bir mekân.</li>
<li><a href="{c.L("karavan-evlilik-teklifi")}">Karavan</a>: yol hikâyesine yakışan, rahat bir atmosfer.</li></ul>
<p>Kurulumu Kütahya'da sizin belirlediğiniz bir yerde istiyorsanız, bunun konsept ve tarihe göre mümkün olup olmadığını birlikte konuşabiliriz.</p>''')


def bilecik_body(c):
    return sehir(c, "bilecik-evlilik-teklifi", f'''<h2>Bilecik'ten gelen çiftler için evlilik teklifi</h2>
<p>Bilecik, Eskişehir'e Bozüyük üzerinden bağlanıyor; karayoluyla yaklaşık 80 km ve güzergâha göre bir ile bir buçuk saat arası. Hızlı tren hattı da iki şehri birbirine bağladığı için, araçsız gelen çiftler için de pratik bir seçenek.</p>
{{HARITA}}
<h2>Plan nasıl kuruluyor?</h2>
<p>Varış saatinizi, gün batımını ve yol süresini birlikte hesaplıyoruz. Siz Eskişehir'e girerken alan hazır, ışıklar yanıyor oluyor. Tüm planlama WhatsApp ve telefonla ilerliyor.</p>
{{YORUM}}
<h2>Söğüt, Osmaneli ve diğer ilçeler</h2>
<p>Bilecik merkez dışında Söğüt, Osmaneli, Pazaryeri ve diğer ilçelerden gelen çiftler için de aynı şekilde çalışıyoruz. Bozüyük'ten geliyorsanız <a href="{c.L("bozuyuk-evlilik-teklifi")}">Bozüyük evlilik teklifi</a> sayfasına bakın; mesafe çok daha kısa.</p>
<h2>Konsept önerimiz</h2>
<p>Bilecik'ten gelen çiftler çoğunlukla <a href="{c.L("bungalov-evlilik-teklifi")}">bungalov</a> ya da <a href="{c.L("balon-ev-evlilik-teklifi")}">balon ev</a> konseptini seçiyor: yolculuğun ardından kapalı, sıcak ve tamamen size ayrılmış bir alan.</p>
<p>Kurulumu Bilecik'te belirlediğiniz bir yerde istiyorsanız, konsept ve tarihe göre uygunluğunu birlikte değerlendirelim.</p>''')


def bozuyuk_body(c):
    return sehir(c, "bozuyuk-evlilik-teklifi", f'''<h2>Bozüyük'e en yakın evlilik teklifi alternatifi</h2>
<p>Bozüyük ile Eskişehir arası yaklaşık 45 km; arabayla 45-50 dakika. Bu kadar yakın bir mesafe, teklif akşamını Eskişehir'de geçirmeyi neredeyse bir şehir içi plan kadar kolaylaştırıyor.</p>
{{HARITA}}
<h2>Akşam planı örneği</h2>
<ol><li>Akşamüstü Bozüyük'ten yola çıkıyorsunuz; bahaneniz bir akşam yemeği ya da arkadaş buluşması.</li>
<li>Hava kararırken alana varıyorsunuz; ışıklar, harfler ve neon yazı hazır.</li>
<li>Soruyu soruyorsunuz, ardından içeride baş başa kutlama.</li>
<li>Aynı gece kısa bir yolla eve dönüyorsunuz.</li></ol>
<h2>Bozüyük'ten gelenler hangi konsepti seçiyor?</h2>
<p>Kısa yol, büyük sahneye zaman bırakıyor: <a href="{c.L("balon-ev-evlilik-teklifi")}">balon ev</a> ve önündeki MARRY ME harfleri, akşamın tamamını teklif etrafında kurmak isteyenler için iyi bir seçim. Daha sakin bir ortam isterseniz <a href="{c.L("bungalov-evlilik-teklifi")}">bungalov</a>, daha rahat bir hava isterseniz <a href="{c.L("karavan-evlilik-teklifi")}">karavan</a>.</p>
{{YORUM}}
<p>Bilecik merkezden geliyorsanız <a href="{c.L("bilecik-evlilik-teklifi")}">Bilecik evlilik teklifi</a> sayfasında ulaşım ve planlama notlarını bulabilirsiniz.</p>''')


def afyon_body(c):
    return sehir(c, "afyon-evlilik-teklifi", f'''<h2>Afyonkarahisar'dan gelen çiftler için evlilik teklifi</h2>
<p>Afyonkarahisar ile Eskişehir arası karayoluyla yaklaşık 130 km; arabayla bir saat elli dakika civarı. Teklifi küçük bir yolculukla birleştirmek isteyen çiftler için uygun bir mesafe.</p>
{{HARITA}}
<h2>Teklifi bir hafta sonu planına dönüştürün</h2>
<p>Afyon'dan gelen çiftlerin bir kısmı teklifi bir hafta sonu kaçamağıyla birleştiriyor: gündüz Eskişehir'de Odunpazarı sokakları ya da Porsuk kıyısında bir yürüyüş, akşam ise ışıkların yandığı bir teklif alanı. Saat planını yol süresine göre birlikte yapıyoruz.</p>
{{YORUM}}
<h2>Uzaktan planlama</h2>
<p>Konsepti fotoğraflardan seçiyor, detayları WhatsApp'tan netleştiriyoruz. Teklif gününe kadar Eskişehir'e gelmenize gerek kalmıyor.</p>
<h2>Konsept önerimiz</h2>
<ul><li><a href="{c.L("balon-ev-evlilik-teklifi")}">Balon ev</a>: uzun yolun sonunda büyük bir sahne.</li>
<li><a href="{c.L("bungalov-evlilik-teklifi")}">Bungalov</a>: sıcak, kapalı ve sakin.</li>
<li><a href="{c.L("karavan-evlilik-teklifi")}">Karavan</a>: yolculuğun ruhuna uygun, rahat bir atmosfer.</li></ul>
<p>Kurulumu Afyonkarahisar'da belirlediğiniz bir yerde istiyorsanız, konsept ve tarihe göre mümkün olup olmadığını birlikte konuşalım.</p>''')


# ======================================================================== GALERİ, YORUMLAR, SSS, İLETİŞİM
def galeri_body(c):
    sec = ""
    for g, slug in (("balon-ev", "balon-ev-evlilik-teklifi"), ("bungalov", "bungalov-evlilik-teklifi"), ("karavan", "karavan-evlilik-teklifi")):
        sec += f'<section class="bolum-alt" id="{g}"><h2>{GALERI[g][0]}</h2>{gallery(c, [g])}<p><a class="bag" href="{c.L(slug)}">{GALERI[g][0]} paketini incele</a></p></section>'
    sec += (f'<section class="bolum-alt" id="sehirde"><h2>Gondol, Kanlıkavak ve otel</h2>{gallery(c, ["gondol", "kanlikavak", "otel"])}'
            f'<p><a class="bag" href="{c.L("evlilik-teklifi-mekanlari")}">Tüm konseptleri gör</a></p></section>')
    return f'''<div class="bolum"><div class="kap">{sec}
<section class="bolum-alt" id="video"><h2>Videolar</h2>
<div class="videolar">{video_html(c, "reels")}<div class="yatay">{video_html(c, "teklif")}{video_html(c, "dogum-gunu")}</div></div>
<p style="margin-top:1.4rem">Daha fazla video için <a href="{C["YOUTUBE"]}" target="_blank" rel="noopener">YouTube kanalımıza</a> ve <a href="{C["INSTAGRAM"]}" target="_blank" rel="noopener">Instagram hesabımıza</a> göz atın.</p></section></div></div>'''


def yorumlar_body(c):
    return f'''<div class="bolum"><div class="kap"><div class="yorumlar">{yorum_html(YORUMLAR)}</div>
<div class="icerik" style="margin-top:3rem"><p class="yorum-kaynak">Bu yorumlar The Vine Organizasyon müşterilerinin <a href="{C["PARENT_URL"]}" target="_blank" rel="noopener">thevineorganizasyon.com.tr</a> adresinde yayımlanan değerlendirmelerinden alıntıdır; organizasyon türü her yorumun altında belirtilmiştir.</p>
<h2>Teklifiniz bizimle mi gerçekleşti?</h2><p>Deneyiminizi Google İşletme Profilimizde paylaşırsanız, sizden sonra gelecek çiftlere çok yardımcı olursunuz. Yorum bağlantısı için bize WhatsApp'tan yazabilirsiniz.</p></div></div></div>'''


SSS_TAM = [
    ("Evlilik teklifi organizasyonu ne kadar önceden ayarlanmalı?", HOME_FAQ[0][1]),
    ("Evlilik teklifi paketlerinin fiyatı ne kadar?", f"Güncel paket fiyatlarımız: {fiyat_ozet()}. Doğum günü ve yıl dönümü paketleri {tl(ozel_min())}'den başlıyor. Paket dışındaki istekler için fiyatı ayrıca iletiyoruz."),
    ("Paket fiyatına neler dahil değil?", "Gondol konseptinde gondol ücreti, restoran konseptinde yemek pakete dahil değil. Paket listesinde olmayan istekler için fiyatı ayrıca iletiyoruz."),
    ("Balon ev, bungalov ve karavan arasındaki fark ne?", "Balon ev şeffaf bir kubbe ve önünde ışıklı MARRY ME harfleriyle büyük bir sahne sunuyor. Bungalov kapalı, sıcak ve şömineli bir A-frame. Karavan ise sarı vintage bir karavan, piknik köşesi ve ışık tavanıyla daha rahat bir atmosfer."),
    ("Balon ev ile bungalov aynı yerde mi?", "Evet, ikisi aynı bahçede yan yana duruyor."),
    ("Teklif alanında başka çiftler de oluyor mu?", "Teklif saatinizde alan size ayrılıyor; anınızı başkalarıyla paylaşmıyorsunuz."),
    ("Hangi şehirlere hizmet veriyorsunuz?", "Eskişehir merkez ve ilçeleri ile Kütahya, Tavşanlı, Bilecik, Bozüyük, Afyonkarahisar, Bursa ve İnegöl'den gelen çiftlerle çalışıyoruz."),
    ("Kendi belirlediğimiz bir yerde kurulum yapılır mı?", "Konsepte, tarihe ve yerin uygunluğuna göre değerlendiriyoruz. Yeri ve tarihi yazın, mümkün olup olmadığını birlikte konuşalım."),
    ("Gondol, Sazova veya Kanlıkavak'ta teklif mümkün mü?", "Evet, gondol, Sazova ve Kanlıkavak konseptleri hizmetlerimiz arasında. Halka açık alanlarda kurulum, alanın kurallarına ve iznine bağlı olduğu için tarihinizi önceden netleştiriyoruz."),
    ("Otel odasında teklif yapıyor musunuz?", "Evet. Otel konseptinde odayı kalpli helyum balonlar, LOVE folyo balon, gül yapraklarıyla yazılmış Marry Me ve kalpli kutu içinde notlarla hazırlıyoruz."),
    ("Doğum günü veya yıl dönümü için de hizmet veriyor musunuz?", "Evet. Balon ev ve bungalovda Happy birthday ya da Better together neon yazılı doğum günü ve yıl dönümü paketlerimiz var."),
    ("Sürpriz nasıl gizli kalıyor?", HOME_FAQ[4][1]),
    ("Pasta ve içecek pakete dahil mi?", "Balon ev, bungalov, karavan ve Kanlıkavak paketlerinde pasta ve soft içecek dahil. Farklı bir pasta ya da ek ikram isterseniz planlama sırasında konuşalım."),
    ("Yüzüğü siz mi sağlıyorsunuz?", "Hayır, yüzük sizden. Biz yüzüğü sunacağınız anı ve alanı hazırlıyoruz. Ölçüyü nasıl öğreneceğinizi bilmiyorsanız evlilik teklifi yüzüğü rehberimize bakabilirsiniz."),
    ("Evlilik teklifi yüzüğü hangi ele takılır?", "Türkiye'de yaygın gelenek, teklif yüzüğünün sağ elin yüzük parmağına takılması; nikâhtan sonra alyans sol ele takılıyor. Kesin bir kural değil, bazı çiftler sol eli tercih ediyor."),
    ("Arkadaşlarımız ve ailemiz de katılabilir mi?", "Evet. Teklif sonrası kutlamaya katılacak kişilerin ne zaman ve nereden geleceğini sürprizi bozmayacak şekilde birlikte planlıyoruz."),
    ("Hava kötü olursa ne oluyor?", "Balon ev ve bungalovda iç mekân seçeneği var. Açık havada kurulan konseptlerde hava durumunu birlikte takip ediyor, gerekirse saati ya da konsepti önceden konuşuyoruz."),
    ("Teklifi kadınlar da yapabilir mi?", HOME_FAQ[5][1]),
]


def sss_body(c):
    return f'<div class="bolum"><div class="kap">{sss_html(SSS_TAM, "h2", "Evlilik teklifi hakkında sık sorulan sorular")}</div></div>'


def iletisim_body(c):
    adres = f'{C["ADDR_STREET"]}, {C["ADDR_POST"]} {C["ADDR_CITY"]}'
    maps = "https://www.google.com/maps/search/?api=1&query=" + __import__("urllib.parse").parse.quote(adres)
    mail = f'<li>E-posta: <a href="mailto:{C["EMAIL"]}">{C["EMAIL"]}</a></li>' if C["EMAIL"] else ""
    return f'''<div class="bolum"><div class="kap icerik-izgara"><div class="icerik">
<h2>Bize ulaşın</h2>
<ul><li>WhatsApp: <a href="{wa("Merhaba, evlilik teklifi için bilgi almak istiyorum.")}" data-konum="iletisim" target="_blank" rel="noopener">{C["TEL1_TXT"]}</a></li>
<li>Telefon: <a href="tel:{C["TEL1"]}" data-konum="iletisim">{C["TEL1_TXT"]}</a> ve <a href="tel:{C["TEL2"]}" data-konum="iletisim">{C["TEL2_TXT"]}</a></li>
{mail}<li>Instagram: <a href="{C["INSTAGRAM"]}" target="_blank" rel="noopener">{C["INSTAGRAM_TXT"]}</a> ve <a href="{C["INSTAGRAM_VINE"]}" target="_blank" rel="noopener">@thevineorganizasyon</a></li>
<li>YouTube: <a href="{C["YOUTUBE"]}" target="_blank" rel="noopener">Eskişehir Evlilik Teklifi</a> ve <a href="{C["YOUTUBE_VINE"]}" target="_blank" rel="noopener">@thevineorganizasyon</a></li></ul>
<h2>Ofis adresi</h2>
<address style="font-style:normal">{adres}</address>
<p><a class="bag" href="{maps}" target="_blank" rel="noopener">Haritada aç</a></p>
<p>Teklif alanlarımızın konumunu rezervasyon sırasında paylaşıyoruz.</p>
<h2>Bir {C["PARENT"]} markası</h2>
<p>{C["BRAND"]}, düğün, nişan, kına ve kurumsal organizasyonlarda 20 yıllık deneyime sahip <a href="{C["PARENT_URL"]}" target="_blank" rel="noopener">{C["PARENT"]}</a>'un yalnızca evlilik teklifine odaklanan markasıdır.</p>
</div><aside class="yan"><div class="yan-iletisim"><h2>En hızlı yol</h2><p>Konsept, şehir ve tarihi tek mesajla gönderin; müsaitliği aynı gün iletelim.</p>
<a class="dugme altin" href="{c.L("teklif-al")}">Fiyat teklifi formu</a>
<a class="dugme cizgi" href="{wa("Merhaba, evlilik teklifi için bilgi almak istiyorum.")}" data-konum="iletisim-yan" target="_blank" rel="noopener">{IC_SOHBET} WhatsApp</a></div></aside></div></div>'''


# ======================================================================== BLOG
def blog_body(c):
    yazilar = [("blog/evlilik-teklifi-sozleri", "Evlilik teklifi sözleri", "Kısa, romantik, duygusal ve esprili örnekler; kendi sözünüzü yazmak için üç adım."),
               ("blog/evlilik-teklifi-fikirleri", "Evlilik teklifi fikirleri", "Sade, romantik ve sürpriz fikirler; Eskişehir'e özel öneriler."),
               ("blog/evlilik-teklifi-yuzugu", "Evlilik teklifi yüzüğü", "Hangi ele ve parmağa takılır, ölçü gizlice nasıl öğrenilir."),
               ("blog/evlilik-teklifi-nasil-yapilir", "Evlilik teklifi nasıl yapılır, ne zaman edilir?", "Tarih, yüzük, mekân, konuşma ve B planı: adım adım plan."),
               ("blog/evlilik-teklifi-cicegi-pastasi-pozlari", "Evlilik teklifi çiçeği, pastası ve pozları", "Teklifin akılda kalan detayları için öneriler.")]
    kart = "".join(f'<a href="{c.L(s)}"><strong>{t}</strong><span>{d}</span></a>' for s, t, d in yazilar)
    return f'''<div class="bolum"><div class="kap"><div class="ilgili">{kart}
<a href="{c.L("evlilik-teklifi-mekanlari")}"><strong>Eskişehir evlilik teklifi mekanları</strong><span>Özel konseptler ve şehrin sevilen teklif noktaları.</span></a></div></div></div>'''


def nasil_body(c):
    p = PAGES_BY["blog/evlilik-teklifi-nasil-yapilir"]
    inner = f'''<p>Evlilik teklifi birkaç dakika sürüyor ama hazırlığı haftalar alabiliyor. Bu rehber, Eskişehir'de ya da başka bir şehirde teklif planlayan herkes için, işleri hangi sırayla yapmanız gerektiğini anlatıyor.</p>
<h2>Evlilik teklifi ne zaman edilir?</h2>
<p>Doğru zamanın takvimde bir karşılığı yok; ama bazı işaretler var. Geleceğe dair planları birlikte konuşmaya başladıysanız, birbirinizin ailesini tanıyorsanız ve evlilik fikri ikiniz için de sürpriz değil, sadece zamanlaması sürprizse, zaman gelmiş demektir. Teklifin kendisi sürpriz olmalı, evlilik fikri değil.</p>
<h2>1. Tarihi seçin</h2>
<p>Sizin için anlamlı bir tarih (tanışma yıl dönümü, ilk buluşma) güzel bir seçim. Ancak 14 Şubat ve yılbaşı gibi günlerde hem mekânlar hem organizasyon ekipleri erken doluyor. Özel bir tarihe bağlı değilseniz hafta içi bir akşam daha sakin bir an sunar. Organizasyonla çalışacaksanız en az bir hafta önceden yer ayırtın.</p>
<h2>2. Yüzüğü hazırlayın</h2>
<p>Ölçü en çok zorlanılan kısım. Sürprizi bozmadan ölçüyü öğrenmenin yollarını <a href="{c.L("blog/evlilik-teklifi-yuzugu")}">evlilik teklifi yüzüğü rehberimizde</a> anlattık. Yüzüğün teklif gününden önce elinizde olduğundan emin olun.</p>
<h2>3. Mekânı ve konsepti belirleyin</h2>
<p>Sevdiğiniz kişi kalabalığı mı sever, sakinliği mi? Büyük bir sahne mi onu mutlu eder, baş başa bir an mı? Bu soruların cevabı mekânı seçer. Eskişehir'de halka açık seçenekleri ve özel konseptleri <a href="{c.L("evlilik-teklifi-mekanlari")}">evlilik teklifi mekanları</a> sayfasında karşılaştırdık.</p>
<h2>4. Bir sırdaş seçin</h2>
<p>Planı bilen kişi sayısını az tutun. Bir yakın arkadaş, hem bahane kurmada hem de son dakika işlerinde en büyük yardımcınız olur.</p>
<h2>5. Bahaneyi kurun</h2>
<p>Onu teklif alanına nasıl getireceğinizi önceden düşünün. Bir akşam yemeği, bir arkadaş buluşması ya da kısa bir kaçamak en sık işe yarayan bahaneler. Örnekleri <a href="{c.L("surpriz-evlilik-teklifi")}">sürpriz evlilik teklifi</a> sayfamızda bulabilirsiniz.</p>
<h2>6. Ne söyleyeceğinizi hazırlayın</h2>
<p>Uzun bir konuşmaya gerek yok. Birlikte yaşadığınız bir anı, onu neden seçtiğiniz ve soru: üç cümle yeterli. Heyecandan unutmamak için bir iki kez kendi kendinize söyleyin.</p>
<h2>7. B planı yapın</h2>
<p>Açık havada bir teklif planlıyorsanız hava durumunu birkaç gün önceden takip edin. Gecikmeler için yolculuk süresine pay bırakın. Kapalı bir alternatif (örneğin bir bungalov) en rahat B planıdır.</p>
<h2>8. Evet'ten sonrasını düşünün</h2>
<p>Aileleri hemen aramak, arkadaşlarla kutlamak ya da baş başa kalmak... Teklifin ardından ne yapacağınızı önceden bilmek, anın keyfini çıkarmanızı kolaylaştırır.</p>
<h2>En sık yapılan hatalar</h2>
<ul><li>Planı çok fazla kişiye anlatmak</li><li>Yüzüğü son güne bırakmak</li><li>Hava durumunu hesaba katmamak</li>
<li>Karşı tarafın o gün nasıl giyineceğini düşünmemek</li><li>Teklif saatini trafiğe ve yola göre hesaplamamak</li></ul>
<div class="not-kutu"><p>Hazırlığın süsleme, kurulum ve zamanlama kısmını bize bırakmak isterseniz <a href="{c.L("teklif-al")}">fiyat teklifi formunu</a> doldurun.</p></div>'''
    return article_layout(c, p, inner + ilg(c, "surpriz", "yuzuk", "balon"))


def yuzuk_body(c):
    p = PAGES_BY["blog/evlilik-teklifi-yuzugu"]
    inner = f'''<p>Evlilik teklifi yüzüğü hakkında en çok sorulan iki soru: hangi ele ve parmağa takıldığı ve ölçünün sürprizi bozmadan nasıl öğrenileceği. İkisini de bu yazıda cevaplıyoruz.</p>
<h2>Evlilik teklifi yüzüğü hangi ele ve parmağa takılır?</h2>
<p>Türkiye'de yaygın gelenek, teklif yüzüğünün (çoğunlukla tek taş) <strong>sağ elin yüzük parmağına</strong> takılması; nikâhtan sonra alyans ise sol ele takılıyor. Bu kesin bir kural değil: bazı çiftler Batı geleneğini izleyerek teklif yüzüğünü baştan sol ele takmayı tercih ediyor. Teklif anında yüzüğü hangi ele takacağınızı önceden düşünmeniz, ölçüyü de o ele göre almanız yeterli.</p>
<h2>Tek taş mı, başka bir model mi?</h2>
<p>Tek taş, evlilik teklifinin klasik simgesi. Sevdiğiniz kişi sade takıları seviyorsa ince bir tek taş, daha gösterişli modelleri seviyorsa üç taş ya da tam tur modeller düşünülebilir. En doğru ipucu, şu an taktığı takılarda: renk (sarı, beyaz, rose), kalınlık ve tarz.</p>
<h2>Yüzük ölçüsü gizlice nasıl öğrenilir?</h2>
<p>Teklifin en teknik kısmı ölçü. İşte sürprizi bozmadan parmak ölçüsünü öğrenmenin en güvenilirden en riskliye doğru beş yolu.</p>
<h3>1. Taktığı bir yüzüğü kuyumcuya götürün</h3>
<p>En güvenilir yöntem. Sevdiğiniz kişinin aynı parmağa taktığı bir yüzüğü kısa süreliğine ödünç alın; kuyumcu iç çapını ölçüp size doğru ölçüyü söyler. Yüzüğün hangi parmakta takıldığından emin olun; parmaklar arasında ölçü farkı olabilir.</p>
<h3>2. Yüzüğün iç çapını kendiniz ölçün</h3>
<p>Yüzüğü alamıyorsanız, bir kâğıdın üzerine koyup iç çemberini kalemle çizin ya da iç çapını cetvelle milimetre olarak ölçün. Kuyumcu bu çizimden ya da ölçüden yaklaşık ölçüyü çıkarabilir.</p>
<h3>3. Bir yakınından yardım alın</h3>
<p>Annesi, kardeşi ya da yakın bir arkadaşı ölçüyü biliyor olabilir ya da doğal bir bahaneyle öğrenebilir. Sırdaşınızın ağzı sıkı olsun.</p>
<h3>4. Alışverişte doğal bir an yakalayın</h3>
<p>Birlikte gezerken bir takı vitrininin önünde durup “şunu bir dene” demek şüphe uyandırmadan ölçüyü öğrenmenin yollarından biri. Dikkat: çok sık yaparsanız sürpriz tahmin edilebilir.</p>
<h3>5. Uyurken ip ya da kâğıt şeritle ölçmek</h3>
<p>Sık anlatılan ama en riskli yöntem: hem uyandırma ihtimali var hem de ip esnediği için ölçü yanılabiliyor. Başka seçeneğiniz yoksa birkaç kez ölçüp ortalamasını alın.</p>
<h2>Emin değilseniz</h2>
<p>Çoğu yüzük modelinde ölçü sonradan ayarlanabiliyor; ancak tamamı taşlı tam tur modellerde bu zor olabiliyor. Satın alırken kuyumcunuza ölçü değişikliği imkânını sorun. Kararsız kaldığınızda bir tık bol bir ölçü, dar olandan daha rahat bir başlangıç olur.</p>
<div class="not-kutu"><p>Yüzük hazır olduğunda geriye anı kurmak kalıyor. <a href="{c.L("balon-ev-evlilik-teklifi")}">Balon ev</a>, <a href="{c.L("bungalov-evlilik-teklifi")}">bungalov</a> ve <a href="{c.L("karavan-evlilik-teklifi")}">karavan</a> konseptlerimize göz atın.</p></div>'''
    return article_layout(c, p, inner + ilg(c, "nasil", "surpriz", "fiyat"))


def gizlilik_body(c):
    return f'''<div class="bolum"><div class="kap icerik">
<p class="kucuk">Bu metin genel bilgilendirme amaçlı bir şablondur; yayına almadan önce bir hukuk danışmanına kontrol ettirmenizi öneririz.</p>
<h2>Veri sorumlusu</h2><p>{C["PARENT"]}, {C["ADDR_STREET"]}, {C["ADDR_POST"]} {C["ADDR_CITY"]}. Telefon: {C["TEL1_TXT"]}.</p>
<h2>Hangi verileri işliyoruz?</h2>
<p>Fiyat teklifi formu bilgilerinizi sunucumuza kaydetmez; doldurduğunuz alanlar cihazınızda bir WhatsApp mesajına dönüştürülür ve mesajı siz gönderirsiniz. WhatsApp üzerinden bize ilettiğiniz ad, telefon, tarih ve organizasyon tercihleri, talebinizi yanıtlamak ve organizasyonu planlamak amacıyla işlenir. WhatsApp hizmeti Meta tarafından sağlanır.</p>
<h2>Çerezler</h2>
<p>Sitede, yalnızca onay vermeniz halinde, ziyaret istatistikleri ve reklam ölçümü için Google Tag Manager aracılığıyla Google Analytics 4 ve reklam ölçüm çerezleri çalışır. Onay vermezseniz bu çerezler kullanılmaz. Tercihinizi tarayıcınızın site verilerini silerek değiştirebilirsiniz.</p>
<h2>Fotoğraflar</h2><p>Sitede yer alan çift fotoğrafları, ilgili kişilerin izniyle yayımlanmaktadır. Bir fotoğrafın kaldırılmasını istiyorsanız bize ulaşın.</p>
<h2>Haklarınız</h2>
<p>6698 sayılı Kişisel Verilerin Korunması Kanunu'nun 11. maddesi kapsamındaki haklarınızla ilgili taleplerinizi yukarıdaki iletişim bilgileri üzerinden bize iletebilirsiniz.</p>
</div></div>'''


def bulunamadi_body(c):
    return f'''<div class="bolum bos-sayfa"><div class="kap"><h2>Aradığınız sayfa burada değil</h2>
<p>Bağlantı değişmiş olabilir. Konseptlere ana sayfadan ulaşabilirsiniz.</p>
<div class="dugmeler" style="justify-content:center"><a class="dugme sarap" href="/">Ana sayfaya dön</a><a class="dugme cizgi-koyu" href="{wa("Merhaba, evlilik teklifi için bilgi almak istiyorum.")}" target="_blank" rel="noopener">WhatsApp'tan yaz</a></div></div></div>'''


# ======================================================================== SAYFA TANIMLARI
PAGES_BY = {}
FOTO_SEHIR = {"bursa-evlilik-teklifi": ("karavan", "eskisehir-karavan-evlilik-teklifi-love"),
              "kutahya-evlilik-teklifi": ("bungalov", "bungalov-onunde-love-harfleri-maytap"),
              "bilecik-evlilik-teklifi": ("balon-ev", "balon-ev-onunde-evlilik-teklifi-ani"),
              "bozuyuk-evlilik-teklifi": ("bungalov", "evlilik-teklifi-yuzuk-bungalov-onunde"),
              "afyon-evlilik-teklifi": ("karavan", "karavan-isik-tavani-altinda-evlilik-teklifi")}


def F(*qa):
    return list(qa)


def pages():
    P = []

    def add(**kw):
        kw.setdefault("og", (kw["slug"] or "ana-sayfa").replace("/", "-"))
        P.append(kw); PAGES_BY[kw["slug"]] = kw

    add(slug="", title="Eskişehir Evlilik Teklifi Organizasyonu | Balon Ev, Bungalov",
        desc="Eskişehir'de balon ev, bungalov ve karavan konseptli sürpriz evlilik teklifi organizasyonu. Kütahya, Bilecik, Bozüyük ve Afyon'dan çiftlere de hizmet.",
        h1="Eskişehir'de evlilik teklifi organizasyonu", konu="Eskişehir'de evlilik teklifi", body=home_body, custom_head=home_head,
        faq=HOME_FAQ, sitemap_gal=["balon-ev", "bungalov", "karavan"],
        preload='<link rel="preload" as="image" href="img/balon-ev/eskisehir-balon-ev-evlilik-teklifi-marry-me-800.webp" imagesrcset="img/balon-ev/eskisehir-balon-ev-evlilik-teklifi-marry-me-800.webp 800w, img/balon-ev/eskisehir-balon-ev-evlilik-teklifi-marry-me-1600.webp 1600w" imagesizes="(max-width:1000px) 360px, 440px">')

    add(slug="balon-ev-evlilik-teklifi", title="Balon Ev Evlilik Teklifi Eskişehir | Şeffaf Kubbede Sürpriz",
        desc="Eskişehir'de balon ev evlilik teklifi: şeffaf kubbe, şömine, \"Benimle evlenir misin?\" neon yazısı, ışıklı MARRY ME harfleri ve kırmızı halı. Fotoğraflar ve fiyat.",
        h1="Balon evde evlilik teklifi", lede="Şeffaf bir kubbe, içinde şömine ve neon yazı, önünde ışıklı MARRY ME harfleri ve kırmızı halı. Eskişehir'in en çok konuşulan teklif sahnesi.",
        crumbs=[("Mekanlar", "evlilik-teklifi-mekanlari"), ("Balon ev", "balon-ev-evlilik-teklifi")], ill="balon", konsept="balon-ev",
        konu="balon ev evlilik teklifi", body=balon_body, video=True, hero_foto=("balon-ev", "balon-ev-ici-benimle-evlenir-misin-neon"), sitemap_gal=["balon-ev"],
        service=dict(name="Balon ev evlilik teklifi organizasyonu", gal="balon-ev", area=["Eskişehir", "Kütahya", "Bilecik", "Bozüyük", "Afyonkarahisar"]),
        yan_baglar=[("Bungalovda evlilik teklifi", "bungalov-evlilik-teklifi"), ("Karavanda evlilik teklifi", "karavan-evlilik-teklifi"), ("Evlilik teklifi fiyatları", "evlilik-teklifi-fiyatlari"), ("Galeri", "galeri")],
        faq=F(("Balon ev kaç kişilik?", "Balon ev, iki kişilik bir teklif ve kutlama düzeni için kuruluyor. Teklif sonrası arkadaş veya aile katılımı planlıyorsanız düzeni birlikte konuşalım."),
              ("Balon evde neler hazır oluyor?", "Kırmızı halı, fenerler, ışıklı MARRY ME harfleri, içeride şömine, iki kişilik masa ve neon yazı. Çiçek, pasta, ikram ve müzik gibi eklemeleri tercihlerinize göre planlıyoruz."),
              ("Balon ev için en iyi saat hangisi?", "Gün batımından sonraki saatler. Işıklar ve kubbe karanlıkta en etkili halini alıyor; saati mevsime göre birlikte belirliyoruz."),
              ("Kışın balon evde teklif yapılır mı?", "Evet. Balon ev kapalı bir kubbe; içeride şömine düzeni var. Soğuk günlerde saat ve detayları birlikte planlıyoruz.")))

    add(slug="bungalov-evlilik-teklifi", title="Bungalovda Evlilik Teklifi Eskişehir | Işıklı A-Frame",
        desc="Eskişehir'de bungalov evlilik teklifi: ışıklı A-frame bungalov, LOVE ve MARRY ME harfleri, şömine, neon yazı ve maytaplı kutlama. Fotoğraflar ve fiyat teklifi.",
        h1="Bungalovda evlilik teklifi", lede="Çatısı ışıkla çizilmiş bir A-frame bungalov, önünde LOVE harfleri ve kırmızı halı, içinde şömine ve neon yazı. Sıcak, kapalı ve baş başa.",
        crumbs=[("Mekanlar", "evlilik-teklifi-mekanlari"), ("Bungalov", "bungalov-evlilik-teklifi")], ill="bungalov", konsept="bungalov",
        konu="bungalovda evlilik teklifi", body=bungalov_body, hero_foto=("bungalov", "eskisehir-bungalov-evlilik-teklifi-marry-me"), sitemap_gal=["bungalov"],
        service=dict(name="Bungalov evlilik teklifi organizasyonu", gal="bungalov", area=["Eskişehir", "Kütahya", "Bilecik", "Bozüyük", "Afyonkarahisar"]),
        yan_baglar=[("Balon evde evlilik teklifi", "balon-ev-evlilik-teklifi"), ("Karavanda evlilik teklifi", "karavan-evlilik-teklifi"), ("Evlilik teklifi fiyatları", "evlilik-teklifi-fiyatlari"), ("Galeri", "galeri")],
        faq=F(("Bungalovda teklif içeride mi dışarıda mı yapılıyor?", "İkisi de mümkün. Çoğu çift soruyu bungalovun önünde, ışıklı harflerin arasında soruyor; kutlamayı içeride şöminenin yanında sürdürüyor."),
              ("Bungalov soğuk havaya uygun mu?", "Evet, kapalı ve sıcak bir iç mekân. Bu yüzden kış aylarında en çok tercih edilen konseptlerden biri."),
              ("LOVE ve MARRY ME harfleri seçilebiliyor mu?", "Fotoğraflarda iki düzeni de görebilirsiniz. Hangisini istediğinizi planlama sırasında birlikte belirliyoruz."),
              ("Maytap kutlaması nasıl oluyor?", "Evet'in ardından bungalov önünde el maytaplarıyla kısa bir kutlama yapılabiliyor. İsterseniz fiyat formunda işaretleyin.")))

    add(slug="karavan-evlilik-teklifi", title="Karavanda (Vosvos) Evlilik Teklifi Eskişehir",
        desc="Eskişehir'de karavan ve vosvos evlilik teklifi: sarı vintage vosvos karavan, piknik köşesi, çadır, ışık zinciri tavanı ve ışıklı LOVE harfleri.",
        h1="Karavanda evlilik teklifi", lede="Papatya desenli sarı bir vintage karavan, önünde piknik köşesi, tepede ışık zincirlerinden bir tavan ve ışıklı LOVE harfleri. Rahat, samimi ve farklı.",
        crumbs=[("Mekanlar", "evlilik-teklifi-mekanlari"), ("Karavan", "karavan-evlilik-teklifi")], ill="karavan", konsept="karavan",
        konu="karavanda evlilik teklifi", body=karavan_body, hero_foto=("karavan", "eskisehir-karavan-evlilik-teklifi-love"), sitemap_gal=["karavan"],
        service=dict(name="Karavan evlilik teklifi organizasyonu", gal="karavan", area=["Eskişehir", "Kütahya", "Bilecik", "Bozüyük", "Afyonkarahisar"]),
        yan_baglar=[("Balon evde evlilik teklifi", "balon-ev-evlilik-teklifi"), ("Bungalovda evlilik teklifi", "bungalov-evlilik-teklifi"), ("Evlilik teklifi fiyatları", "evlilik-teklifi-fiyatlari"), ("Galeri", "galeri")],
        faq=F(("Karavan konsepti açık havada mı?", "Evet, karavan ve piknik köşesi açık havada kuruluyor. Tarihi seçerken hava durumunu birlikte takip ediyoruz."),
              ("Karavan konseptine arkadaşlarımız katılabilir mi?", "Evet. Rahat atmosferi nedeniyle teklif sonrası küçük bir kutlama için de uygun. Kişi sayısını planlamada konuşalım."),
              ("Karavanın içi de süsleniyor mu?", "Karavanın kapısı açık, içi de dekorla hazırlanıyor. Detayları tercihlerinize göre belirliyoruz.")))

    add(slug="evlilik-teklifi-mekanlari", title="Eskişehir Evlilik Teklifi Mekanları ve Edilecek Yerler",
        desc="Eskişehir evlilik teklifi mekanları: balon ev, bungalov ve karavan konseptleri ile gondol, Sazova ve Kanlıkavak gibi şehrin sevilen teklif noktaları.",
        h1="Eskişehir evlilik teklifi mekanları", lede="Size ayrılan özel konsept alanları ve şehrin evlilik tekliflerine sahne olan sevilen noktaları. Hangisinin sizin anınıza uyduğunu birlikte bulalım.",
        crumbs=[("Mekanlar", "evlilik-teklifi-mekanlari")], ill="yuzuk", konu="Eskişehir evlilik teklifi mekanları", body=mekanlar_body,
        yan_baglar=[("Balon ev", "balon-ev-evlilik-teklifi"), ("Bungalov", "bungalov-evlilik-teklifi"), ("Karavan", "karavan-evlilik-teklifi"), ("Gondol", "gondolda-evlilik-teklifi"), ("Sazova Parkı", "sazova-parki-evlilik-teklifi"), ("Kanlıkavak Parkı", "kanlikavak-parki-evlilik-teklifi"), ("Gaga Restoran", "gaga-restoran-evlilik-teklifi")],
        faq=F(("Eskişehir'de evlilik teklifi için en romantik yer neresi?", "Kişiye göre değişiyor. Büyük bir sahne için balon ev, şehrin kalbinde bir an için Porsuk'ta gondol, sakin bir an için bungalov ya da Kanlıkavak öne çıkıyor."),
              ("Halka açık bir yerde süsleme yapılabilir mi?", "Halka açık alanlarda süsleme ve kurulum, alanın yönetiminin iznine bağlı. Bu yüzden pek çok çift teklifi şehirde yapıp kutlamayı özel bir alanda sürdürüyor.")))

    add(slug="gondolda-evlilik-teklifi", title="Gondolda Evlilik Teklifi Eskişehir | Porsuk Çayı",
        desc="Eskişehir Porsuk Çayı'nda gondol evlilik teklifi: Adalar'da köprü altında sorulan soru, pratik notlar, mevsim ve aynı akşam için özel kutlama seçenekleri.",
        h1="Gondolda evlilik teklifi", lede="Porsuk Çayı'nda, Adalar'da bir köprünün altından geçerken sorulan soru. Eskişehir'in en bilinen teklif sahnelerinden biri için kurgu ve pratik notlar.",
        crumbs=[("Mekanlar", "evlilik-teklifi-mekanlari"), ("Gondol", "gondolda-evlilik-teklifi")], ill="gondol",
        konu="gondolda evlilik teklifi", body=gondol_body, place="Porsuk Çayı gondol turu, Adalar",
        yan_baglar=[("Balon evde evlilik teklifi", "balon-ev-evlilik-teklifi"), ("Sazova'da evlilik teklifi", "sazova-parki-evlilik-teklifi"), ("Sürpriz evlilik teklifi", "surpriz-evlilik-teklifi")],
        faq=F(("Gondolda evlilik teklifi yapılabilir mi?", "Evet, Porsuk'ta gondolda yapılan teklifler yerel basına da yansıdı. Sefer saatleri ve özel kullanım koşulları işletmeye bağlı olduğu için tarihinizi önceden kontrol etmek gerekiyor."),
              ("Gondol teklifi için en iyi zaman ne?", "Hafta içi ve akşamüstü saatleri daha sakin. Yaz aylarında talep artıyor, soğuk kış günlerinde seferlerin durumunu önceden öğrenmek gerekiyor."),
              ("Teklif sonrası kutlama nerede yapılabilir?", "Pek çok çift gondoldaki anın ardından akşamı balon evde ya da bungalovda baş başa bir kutlamayla tamamlıyor.")))

    add(slug="sazova-parki-evlilik-teklifi", title="Sazova Parkı'nda Evlilik Teklifi | Masal Şatosu, Eskişehir",
        desc="Sazova Parkı evlilik teklifi: Masal Şatosu önünde bir an için pratik notlar, kalabalık ve saat önerileri, kurulum izni ve aynı akşam özel kutlama seçenekleri.",
        h1="Sazova Parkı'nda evlilik teklifi", lede="Masal Şatosu, Korsan Gemisi ve geniş çimenlikler. Masal gibi bir teklif isteyenler için Sazova'da plan önerileri.",
        crumbs=[("Mekanlar", "evlilik-teklifi-mekanlari"), ("Sazova Parkı", "sazova-parki-evlilik-teklifi")], ill="sato",
        konu="Sazova'da evlilik teklifi", body=sazova_body, place="Sazova Bilim, Kültür ve Sanat Parkı",
        yan_baglar=[("Balon evde evlilik teklifi", "balon-ev-evlilik-teklifi"), ("Gondolda evlilik teklifi", "gondolda-evlilik-teklifi"), ("Kanlıkavak'ta evlilik teklifi", "kanlikavak-parki-evlilik-teklifi")],
        faq=F(("Sazova Parkı'nda teklif için hangi saat uygun?", "Gündüzleri park aileler ve çocuklarla kalabalık oluyor. Akşamüstü ve hafta içi saatler daha sakin; park saatlerini mevsime göre kontrol edin."),
              ("Sazova'da süsleme yapılabilir mi?", "Halka açık bir parkta süsleme ve kurulum, park yönetiminin iznine bağlı. Kısa bir an kurgulayıp asıl sahneyi özel bir alanda hazırlamak çoğu zaman daha rahat.")))

    add(slug="kanlikavak-parki-evlilik-teklifi", title="Kanlıkavak Parkı'nda Evlilik Teklifi | Eskişehir",
        desc="Kanlıkavak Parkı evlilik teklifi: yeşilin içinde sakin bir an için pratik notlar, saat önerileri ve teklifi özel bir alanda tamamlama seçenekleri.",
        h1="Kanlıkavak Parkı'nda evlilik teklifi", lede="Geniş çim alanları ve yürüyüş yollarıyla Kanlıkavak, kalabalıktan uzak bir an isteyenler için. Plan önerileri ve pratik notlar.",
        crumbs=[("Mekanlar", "evlilik-teklifi-mekanlari"), ("Kanlıkavak Parkı", "kanlikavak-parki-evlilik-teklifi")], ill="kavak",
        konu="Kanlıkavak'ta evlilik teklifi", body=kanlikavak_body, place="Kanlıkavak Parkı",
        yan_baglar=[("Karavanda evlilik teklifi", "karavan-evlilik-teklifi"), ("Bungalovda evlilik teklifi", "bungalov-evlilik-teklifi"), ("Sazova'da evlilik teklifi", "sazova-parki-evlilik-teklifi")],
        faq=F(("Kanlıkavak Parkı teklif için uygun mu?", "Daha sakin, yeşil bir an isteyenler için uygun. Akşamüstü saatleri hem ışık hem kalabalık açısından daha iyi."),
              ("Parkta kurulum yapılabilir mi?", "Halka açık bir alanda süsleme ve kurulum, alanın yönetiminin iznine bağlı. Teklifi parkta yapıp kutlamayı özel bir alanda sürdürmek de mümkün.")))

    add(slug="surpriz-evlilik-teklifi", title="Sürpriz Evlilik Teklifi Eskişehir | Romantik ve Size Özel",
        desc="Eskişehir'de sürpriz ve romantik evlilik teklifi: sır nasıl saklanır, onu alana nasıl getirirsiniz, zamanlama ve kişiselleştirme. Planlamayı birlikte yapalım.",
        h1="Sürpriz evlilik teklifi", lede="Romantik bir teklifin en zor kısmı süsleme değil, sırrı saklamak. Bahaneden zamanlamaya, sürprizi bozmadan planlamanın yolları.",
        crumbs=[("Sürpriz evlilik teklifi", "surpriz-evlilik-teklifi")], ill="yuzuk",
        konu="sürpriz evlilik teklifi", body=surpriz_body,
        yan_baglar=[("Evlilik teklifi nasıl yapılır?", "blog/evlilik-teklifi-nasil-yapilir"), ("Balon evde evlilik teklifi", "balon-ev-evlilik-teklifi"), ("Evlilik teklifi fiyatları", "evlilik-teklifi-fiyatlari")],
        faq=F(("Sürpriz evlilik teklifi için ne kadar önceden plan yapmalıyım?", "En az bir hafta önceden. Bu süre hem tarihin ayrılmasına hem de bahanenin doğal kurulmasına yetiyor."),
              ("Sevdiğim kişi bir şeyler sezerse ne yapmalıyım?", "Planı bilen kişi sayısını azaltın, telefonunuzu ortada bırakmayın ve bahaneyi değiştirmeyin. Küçük bir ipucu sezilse bile teklifin nasıl ve nerede yapılacağı sürpriz kalır.")))

    add(slug="evlilik-teklifi-fiyatlari", title="Evlilik Teklifi Organizasyonu Fiyatları 2026 | Eskişehir",
        desc="Eskişehir evlilik teklifi fiyatları: konsept, tarih, süsleme, ikram ve kişi sayısına göre nasıl değişir? Size özel fiyatı WhatsApp'tan aynı gün alın.",
        h1="Evlilik teklifi organizasyonu fiyatları", lede="Eskişehir'de evlilik teklifi organizasyonu fiyatını neyin belirlediğini açıkça anlatıyoruz. Konsept, şehir ve tarihi yazın; size özel fiyatı aynı gün iletelim.",
        crumbs=[("Fiyatlar", "evlilik-teklifi-fiyatlari")], ill="yuzuk", konu="evlilik teklifi fiyatları", body=fiyat_body,
        yan_baglar=[("Fiyat teklifi formu", "teklif-al"), ("Balon ev", "balon-ev-evlilik-teklifi"), ("Bungalov", "bungalov-evlilik-teklifi"), ("Karavan", "karavan-evlilik-teklifi")],
        faq=F(("Evlilik teklifi organizasyonu fiyatı ne kadar?", "Fiyat; konsept, tarih, süsleme, ikram ve kişi sayısına göre değişiyor. Konsept, şehir ve tarihi WhatsApp'tan yazdığınızda size özel fiyatı aynı gün iletiyoruz."),
              ("Bütçeme göre plan yapılabilir mi?", "Evet. Bütçenizi baştan paylaşırsanız, o bütçeyle en etkili düzeni birlikte kuruyoruz."),
              ("14 Şubat'ta fiyatlar değişiyor mu?", "14 Şubat ve yılbaşı gibi yoğun tarihler erken doluyor. Bu tarihler için olabildiğince erken yazmanızı öneriyoruz.")))

    add(slug="teklif-al", title="Evlilik Teklifi Fiyat Teklifi Al | Eskişehir",
        desc="Konsept, şehir, tarih ve eklemek istediklerinizi seçin; evlilik teklifi fiyat talebiniz hazır bir mesaj olarak WhatsApp'ta açılsın. Aynı gün dönüş.",
        h1="Konsepte göre fiyat teklifi alın", lede="Seçimlerinizi yapın, tek dokunuşla WhatsApp'a gönderin. Müsaitliği ve size özel fiyatı aynı gün iletiyoruz.",
        crumbs=[("Fiyat teklifi", "teklif-al")], konu="evlilik teklifi fiyatı", body=teklif_body, buttons=False, no_cta=True)

    for slug, ad, km_txt, lede, desc in [
        ("kutahya-evlilik-teklifi", "Kütahya", "80", "Kütahya ve Tavşanlı'dan gelen çiftler için Eskişehir'de, yaklaşık bir saatlik yolun sonunda ışıkları yanmış bir teklif alanı.",
         "Kütahya ve Tavşanlı'dan çiftler için evlilik teklifi: Eskişehir'e yaklaşık 80 km'de balon ev, bungalov ve karavan konseptleri. Uzaktan planlama, WhatsApp'tan fiyat."),
        ("bilecik-evlilik-teklifi", "Bilecik", "80", "Bilecik'ten gelen çiftler için Bozüyük üzerinden kısa bir yol ve Eskişehir'de size ayrılmış bir teklif alanı.",
         "Bilecik evlilik teklifi: Eskişehir'e yaklaşık 80 km'de balon ev, bungalov ve karavan konseptli sürpriz teklif. Uzaktan planlama, WhatsApp'tan aynı gün fiyat."),
        ("bozuyuk-evlilik-teklifi", "Bozüyük", "45", "Eskişehir'e yalnızca 45 km. Bozüyük'ten gelen çiftler için bir akşamlık, ışıl ışıl bir teklif planı.",
         "Bozüyük evlilik teklifi: Eskişehir'e yaklaşık 45 km'de balon ev, bungalov ve karavan konseptleri. Akşam planı örneği ve WhatsApp'tan aynı gün fiyat."),
        ("afyon-evlilik-teklifi", "Afyonkarahisar", "130", "Afyonkarahisar'dan gelen çiftler için teklifi küçük bir Eskişehir kaçamağıyla birleştiren bir plan.",
         "Afyon evlilik teklifi: Eskişehir'e yaklaşık 130 km'de balon ev, bungalov ve karavan konseptli sürpriz teklif. Hafta sonu planı ve uzaktan organizasyon."),
        ("bursa-evlilik-teklifi", "Bursa", "150", "Bursa ve İnegöl'den gelen çiftler için iki saatlik yolun sonunda, Eskişehir'de ışıkları yanmış bir teklif alanı.",
         "Bursa ve İnegöl'den çiftler için evlilik teklifi: Eskişehir'e yaklaşık 150 km'de balon ev, bungalov ve karavan konseptleri. Uzaktan planlama, WhatsApp'tan fiyat.")]:
        kisa = "Afyon" if ad == "Afyonkarahisar" else ad
        bodies = {"bursa-evlilik-teklifi": bursa_body, "kutahya-evlilik-teklifi": kutahya_body, "bilecik-evlilik-teklifi": bilecik_body, "bozuyuk-evlilik-teklifi": bozuyuk_body, "afyon-evlilik-teklifi": afyon_body}
        add(slug=slug, title=f"{kisa} Evlilik Teklifi Organizasyonu | Eskişehir'e {km_txt} km",
            desc=desc, h1=f"{kisa} evlilik teklifi", lede=lede, crumbs=[(f"{kisa} evlilik teklifi", slug)], ill="balon",
            konu=f"{kisa} evlilik teklifi", body=bodies[slug], hero_foto=FOTO_SEHIR[slug],
            service=dict(name=f"{kisa} evlilik teklifi organizasyonu", area=[ad] + {"Kütahya": ["Tavşanlı"], "Bursa": ["İnegöl"]}.get(ad, [])),
            yan_baglar=[("Balon ev", "balon-ev-evlilik-teklifi"), ("Bungalov", "bungalov-evlilik-teklifi"), ("Karavan", "karavan-evlilik-teklifi"), ("Fiyat teklifi formu", "teklif-al")],
            faq=F((f"{kisa}'dan gelen çiftler için planlama nasıl yapılıyor?" if ad != "Kütahya" else "Kütahya'dan gelen çiftler için planlama nasıl yapılıyor?",
                   "Planlamanın tamamı WhatsApp ve telefon üzerinden ilerliyor. Konsepti fotoğraflardan seçiyor, varış saatinizi yol süresine göre birlikte belirliyoruz."),
                  (f"{kisa} ile Eskişehir arası ne kadar sürüyor?",
                   {"Kütahya": "Karayoluyla yaklaşık 80 km, arabayla bir saat civarı.", "Bilecik": "Karayoluyla yaklaşık 80 km; güzergâha göre bir ile bir buçuk saat arası.",
                    "Bozüyük": "Karayoluyla yaklaşık 45 km, arabayla 45-50 dakika.", "Bursa": "Karayoluyla yaklaşık 150 km, arabayla iki saat civarı.", "Afyonkarahisar": "Karayoluyla yaklaşık 130 km, arabayla bir saat elli dakika civarı."}[ad]),
                  (f"Kurulum {kisa}'da yapılabilir mi?".replace("Kütahya'da", "Kütahya'da").replace("Bilecik'da", "Bilecik'te").replace("Bozüyük'da", "Bozüyük'te").replace("Afyon'da", "Afyon'da"),
                   "Teklif alanlarımız Eskişehir'de. Kendi şehrinizde bir yerde kurulum isterseniz, konsepte ve tarihe göre mümkün olup olmadığını birlikte konuşalım.")))
    # Türkçe ek düzeltmeleri
    for p in P:
        if p.get("faq"):
            p["faq"] = [(q.replace("Kütahya'dan", "Kütahya'dan").replace("Bilecik'dan", "Bilecik'ten").replace("Bozüyük'dan", "Bozüyük'ten").replace("Afyon'dan", "Afyon'dan"), a) for q, a in p["faq"]]

    add(slug="galeri", title="Evlilik Teklifi Galerisi | Balon Ev, Bungalov, Karavan Eskişehir",
        desc="Eskişehir'de kurduğumuz evlilik teklifi alanlarından gerçek fotoğraflar ve video: balon ev, bungalov ve karavan konseptleri.",
        h1="Evlilik teklifi galerisi", lede="Kendi kurulumlarımızdan gerçek kareler. Balon ev, bungalov ve karavan konseptlerini fotoğraflardan inceleyin.",
        crumbs=[("Galeri", "galeri")], hero_foto=("balon-ev", "balon-ev-onunde-evlilik-teklifi-ani"), konu="evlilik teklifi galerisi", body=galeri_body, gallery_schema=True, video=True,
        sitemap_gal=["balon-ev", "bungalov", "karavan"])

    add(slug="yorumlar", title="Müşteri Yorumları | Eskişehir Evlilik Teklifi, The Vine",
        desc="The Vine Organizasyon müşterilerinin gerçek yorumları. Eskişehir'de evlilik teklifi, nişan ve özel gün organizasyonu deneyimleri.",
        h1="Müşteri yorumları", lede="The Vine Organizasyon ile çalışan müşterilerimizin kendi sözleriyle deneyimleri.",
        crumbs=[("Yorumlar", "yorumlar")], konu="evlilik teklifi", body=yorumlar_body)

    add(slug="sss", title="Evlilik Teklifi Sık Sorulan Sorular | Eskişehir",
        desc="Eskişehir evlilik teklifi hakkında sık sorulanlar: rezervasyon, fiyat, konseptler, şehirler, hava durumu, sürpriz ve kutlama.",
        h1="Sık sorulan sorular", lede="Rezervasyondan hava durumuna, evlilik teklifi hakkında en çok sorulanlar ve cevapları.",
        crumbs=[("SSS", "sss")], konu="evlilik teklifi", body=sss_body, faq=SSS_TAM)

    add(slug="iletisim", title="İletişim | Eskişehir Evlilik Teklifi, The Vine Organizasyon",
        desc="Eskişehir evlilik teklifi için WhatsApp ve telefon: 0532 153 17 26, 0536 675 16 12. İstiklal Mah. İki Eylül Cad., Eskişehir.",
        h1="İletişim", lede="Tarih sormak, fiyat almak ya da sadece fikir danışmak için bize WhatsApp'tan ya da telefonla ulaşın.",
        crumbs=[("İletişim", "iletisim")], konu="evlilik teklifi", body=iletisim_body)

    add(slug="blog", title="Evlilik Teklifi Rehberi | Eskişehir Evlilik Teklifi Blog",
        desc="Evlilik teklifi sözleri, fikirleri, yüzüğü, çiçeği ve pastası; teklif nasıl yapılır ve ne zaman edilir. Teklif hazırlığı için rehber yazılar.",
        h1="Evlilik teklifi rehberi", lede="Teklif hazırlığını kolaylaştıran rehber yazılar.", crumbs=[("Blog", "blog")],
        konu="evlilik teklifi", body=blog_body, buttons=False)

    add(slug="blog/evlilik-teklifi-nasil-yapilir", title="Evlilik Teklifi Nasıl Yapılır, Ne Zaman Edilir? Adım Adım Plan",
        desc="Evlilik teklifi nasıl yapılır ve ne zaman edilir? Tarih, yüzük, mekân, sırdaş, bahane, konuşma ve B planı: teklif gününe kadar yapılacaklar sırasıyla.",
        h1="Evlilik teklifi nasıl yapılır? Adım adım plan", lede="Tarihten konuşmaya, teklif gününe kadar yapılacaklar sırasıyla.",
        crumbs=[("Blog", "blog"), ("Evlilik teklifi nasıl yapılır?", "blog/evlilik-teklifi-nasil-yapilir")], ill="yuzuk", article=True,
        konu="evlilik teklifi planı", body=nasil_body, buttons=False,
        yan_baglar=[("Sürpriz evlilik teklifi", "surpriz-evlilik-teklifi"), ("Evlilik teklifi yüzüğü", "blog/evlilik-teklifi-yuzugu"), ("Evlilik teklifi mekanları", "evlilik-teklifi-mekanlari")])

    add(slug="blog/evlilik-teklifi-yuzugu", title="Evlilik Teklifi Yüzüğü Hangi Parmağa Takılır? Ölçü Rehberi",
        desc="Evlilik teklifi yüzüğü hangi ele ve parmağa takılır, tek taş mı seçilmeli, yüzük ölçüsü sürprizi bozmadan nasıl öğrenilir? Kısa ve pratik rehber.",
        h1="Evlilik teklifi yüzüğü: hangi parmağa takılır, ölçü nasıl öğrenilir?", lede="Hangi ele takıldığından ölçünün gizlice nasıl alınacağına, yüzükle ilgili en çok sorulanlar.",
        crumbs=[("Blog", "blog"), ("Evlilik teklifi yüzüğü", "blog/evlilik-teklifi-yuzugu")], ill="yuzuk", article=True,
        konu="evlilik teklifi", body=yuzuk_body, buttons=False,
        yan_baglar=[("Evlilik teklifi nasıl yapılır?", "blog/evlilik-teklifi-nasil-yapilir"), ("Sürpriz evlilik teklifi", "surpriz-evlilik-teklifi")])

    add(slug="blog/evlilik-teklifi-sozleri", title="Evlilik Teklifi Sözleri: Kısa, Romantik ve Duygusal Örnekler",
        desc="En güzel evlilik teklifi sözleri: kısa, romantik, duygusal ve esprili evlenme teklifi sözü örnekleri ve kendi teklif konuşmanızı yazmak için üç adım.",
        h1="Evlilik teklifi sözleri", lede="Kısa, romantik, duygusal ve esprili örnekler. Olduğu gibi kullanın ya da kendi hikâyenize göre değiştirin.",
        crumbs=[("Blog", "blog"), ("Evlilik teklifi sözleri", "blog/evlilik-teklifi-sozleri")], ill="yuzuk", article=True,
        konu="evlilik teklifi", body=sozler_body, buttons=False,
        yan_baglar=[("Evlilik teklifi fikirleri", "blog/evlilik-teklifi-fikirleri"), ("Evlilik teklifi nasıl yapılır?", "blog/evlilik-teklifi-nasil-yapilir"), ("Balon evde evlilik teklifi", "balon-ev-evlilik-teklifi")])

    add(slug="blog/evlilik-teklifi-fikirleri", title="Evlilik Teklifi Fikirleri: Sade, Romantik ve Sürpriz Öneriler",
        desc="En güzel evlilik teklifi fikirleri: sade evlilik teklifi fikirleri, romantik ve sürpriz öneriler, Eskişehir'de gondol, Sazova ve Odunpazarı fikirleri.",
        h1="Evlilik teklifi fikirleri", lede="Sadeden görkemliye evlilik teklifi fikirleri ve Eskişehir'de teklif planlayanlar için şehre özel öneriler.",
        crumbs=[("Blog", "blog"), ("Evlilik teklifi fikirleri", "blog/evlilik-teklifi-fikirleri")], ill="yuzuk", article=True,
        konu="evlilik teklifi fikirleri", body=fikirler_body, buttons=False,
        yan_baglar=[("Evlilik teklifi sözleri", "blog/evlilik-teklifi-sozleri"), ("Eskişehir evlilik teklifi mekanları", "evlilik-teklifi-mekanlari"), ("Sürpriz evlilik teklifi", "surpriz-evlilik-teklifi")])

    add(slug="blog/evlilik-teklifi-cicegi-pastasi-pozlari", title="Evlilik Teklifi Çiçeği, Pastası ve Fotoğraf Pozları",
        desc="Evlilik teklifi çiçeği ne olmalı, teklif pastası nasıl seçilir, en sevilen evlilik teklifi pozları neler? Gerçek fotoğraflarla öneriler.",
        h1="Evlilik teklifi çiçeği, pastası ve pozları", lede="Teklifin akılda kalan küçük detayları: elindeki çiçek, ardından kesilen pasta ve yıllarca bakılacak kareler.",
        crumbs=[("Blog", "blog"), ("Çiçek, pasta ve pozlar", "blog/evlilik-teklifi-cicegi-pastasi-pozlari")], ill="yuzuk", article=True,
        konu="evlilik teklifi", body=detay_body, buttons=False,
        yan_baglar=[("Evlilik teklifi süsleme", "evlilik-teklifi-susleme"), ("Galeri", "galeri"), ("Evlilik teklifi sözleri", "blog/evlilik-teklifi-sozleri")])

    add(slug="evlilik-teklifi-susleme", title="Evlilik Teklifi Süsleme Eskişehir | MARRY ME Harfleri, Neon",
        desc="Eskişehir evlilik teklifi süsleme ve dekorasyonu: ışıklı MARRY ME ve LOVE harfleri, neon yazı, kırmızı halı, fenerler, ışık zinciri, çiçek ve balon süsleme.",
        h1="Evlilik teklifi süsleme", lede="Işıklı MARRY ME ve LOVE harfleri, neon yazı, kırmızı halı, fenerler ve ışık zincirleri. Teklif alanını oluşturan her parça.",
        crumbs=[("Evlilik teklifi süsleme", "evlilik-teklifi-susleme")], hero_foto=("balon-ev", "eskisehir-balon-ev-evlilik-teklifi-marry-me"),
        konu="evlilik teklifi süslemesi", body=susleme_body, sitemap_gal=["balon-ev", "bungalov", "karavan"],
        service=dict(name="Evlilik teklifi süsleme ve dekorasyonu", area=["Eskişehir", "Kütahya", "Bilecik", "Bozüyük", "Afyonkarahisar", "Bursa"]),
        yan_baglar=[("Balon ev", "balon-ev-evlilik-teklifi"), ("Bungalov", "bungalov-evlilik-teklifi"), ("Karavan", "karavan-evlilik-teklifi"), ("Fiyat teklifi formu", "teklif-al")],
        faq=F(("Evlilik teklifi süslemesinde neler var?", "Işıklı MARRY ME veya LOVE harfleri, neon yazı, kırmızı halı, fenerler, ışık zincirleri, çiçek ve isteğe göre balon süsleme ile maytap. Konsepte ve tercihlerinize göre birlikte seçiyoruz."),
              ("Kendi evimizde veya bahçemizde süsleme yapılır mı?", "Yeri, tarihi ve aklınızdaki düzeni yazın; süslemenin o alana uygun olup olmadığını birlikte değerlendirelim."),
              ("Neon yazıya kendi cümlemizi yazdırabilir miyiz?", "Kendi cümlenizi kullanmak istiyorsanız planlama sırasında belirtin; uygunluğunu ve süresini birlikte konuşalım.")))

    add(slug="gaga-restoran-evlilik-teklifi", title="Gaga Restoran'da Evlilik Teklifi | Eskişehir Fener Adası",
        desc="Eskişehir Gaga Restaurant'ta evlilik teklifi: Porsuk Çayı'ndaki Fener Adası'nda romantik akşam yemeği, restoranda teklif kurgusu ve sürpriz kutlama önerileri.",
        h1="Gaga Restoran'da evlilik teklifi", lede="Porsuk Çayı'ndaki Fener Adası'nda, köprüyle geçilen bir restoranda romantik bir akşam yemeği ve bir soru.",
        crumbs=[("Mekanlar", "evlilik-teklifi-mekanlari"), ("Gaga Restoran", "gaga-restoran-evlilik-teklifi")], ill="ada",
        konu="restoranda evlilik teklifi", body=gaga_body, place="Gaga Restaurant, Fener Adası",
        yan_baglar=[("Gondolda evlilik teklifi", "gondolda-evlilik-teklifi"), ("Balon evde evlilik teklifi", "balon-ev-evlilik-teklifi"), ("Evlilik teklifi sözleri", "blog/evlilik-teklifi-sozleri")],
        faq=F(("Gaga Restaurant'ta evlilik teklifi yapılabilir mi?", "Restoranda teklif için kurgu, süsleme ve zamanlamayı birlikte planlıyoruz. Masa rezervasyonu ve mekânda yapılabilecek süslemeler restoranın kurallarına bağlı olduğu için tarihinizi önceden netleştirmenizi öneriyoruz."),
              ("Restoranda teklif için en iyi an hangisi?", "Tatlı servisi ya da kahve gibi akşamın doğal bir arası. Manzaralı bir masa ve sade bir süsleme, anı kalabalık bir sahneden daha etkili kılabilir.")))

    add(slug="ozel-gun-surprizleri", title="Eskişehir Doğum Günü ve Yıl Dönümü Sürprizi | Balon Ev",
        desc="Eskişehir'de balon ev, bungalov ve karavanda doğum günü ve yıl dönümü sürprizi: neon yazı, pasta, balon süsleme ve ışıklarla romantik kutlama.",
        h1="Doğum günü ve yıl dönümü sürprizleri", lede="Evlilik teklifi için kurduğumuz alanlarda doğum günü ve yıl dönümü sürprizleri. Konsept aynı, hikâye farklı.",
        crumbs=[("Özel gün sürprizleri", "ozel-gun-surprizleri")], hero_foto=("balon-ev", "balon-ev-ici-benimle-evlenir-misin-neon"),
        konu="doğum günü veya yıl dönümü sürprizi", body=ozel_gun_body,
        service=dict(name="Doğum günü ve yıl dönümü sürpriz organizasyonu", area=["Eskişehir"]),
        yan_baglar=[("Balon ev", "balon-ev-evlilik-teklifi"), ("Bungalov", "bungalov-evlilik-teklifi"), ("Fiyat teklifi formu", "teklif-al")],
        faq=F(("Balon evde doğum günü kutlaması yapılabilir mi?", "Evet. Neon yazı, pasta, balon süsleme ve ışıklarla iki kişilik ya da küçük bir grup için doğum günü sürprizi hazırlıyoruz."),
              ("Yıl dönümü sürprizinde evlilik teklifi de yapılabilir mi?", "Elbette. Yıl dönümü, teklif için en doğal bahanelerden biri; sevdiğiniz kişi bir kutlamaya geldiğini düşünürken sürprizi teklife dönüştürebilirsiniz.")))

    add(slug="hakkimizda", title="Hakkımızda | Eskişehir Evlilik Teklifi, The Vine Organizasyon",
        desc="Eskişehir Evlilik Teklifi, The Vine Organizasyon çatısı altında yalnızca evlilik teklifine odaklanan bir marka. Konseptlerimiz ve nasıl çalıştığımız.",
        h1="Hakkımızda", lede="Eskişehir'de yalnızca evlilik teklifine odaklanan bir ekip; arkasında 20 yıllık organizasyon deneyimi.",
        crumbs=[("Hakkımızda", "hakkimizda")], konu="evlilik teklifi", body=hakkimizda_body, buttons=False)

    add(slug="gizlilik", title="Gizlilik ve Çerez Politikası | Eskişehir Evlilik Teklifi",
        desc="Kişisel verilerin işlenmesi, çerezler ve haklarınız hakkında bilgilendirme.", h1="Gizlilik ve çerezler",
        lede="Hangi verileri neden işlediğimizi ve çerez tercihlerinizi açıkça anlatıyoruz.", crumbs=[("Gizlilik", "gizlilik")],
        konu="evlilik teklifi", body=gizlilik_body, buttons=False, noindex=True, og="ana-sayfa")

    add(slug="404", file="404.html", title="Sayfa bulunamadı | Eskişehir Evlilik Teklifi", desc="Aradığınız sayfa bulunamadı.",
        h1="Sayfa bulunamadı", lede="Bu adreste bir sayfa yok.", konu="evlilik teklifi", body=bulunamadi_body, buttons=False,
        noindex=True, og="ana-sayfa", no_cta=True)
    # ---- tasarım v2: paketler, görseller, videolar
    G = PAGES_BY
    G[""].update(h1="Eskişehir Evlilik Teklifi",
        desc=f"Eskişehir'de balon ev, bungalov, karavan, gondol ve otel konseptli evlilik teklifi organizasyonu. Paketler {tl(EN_DUSUK)}'den; yakın illere de hizmet.",
        video=["reels"], sitemap_gal=["balon-ev", "bungalov", "karavan", "gondol", "kanlikavak", "otel"],
        preload=lambda c: on_yukle(c, (slaytlar() or [{}])[0].get("gorsel"), KARE_BOYUT))
    G["balon-ev-evlilik-teklifi"].update(paket="balon-ev", hero_foto=("balon-ev", "balon-ev-onunde-evlilik-teklifi-ani"))
    G["bungalov-evlilik-teklifi"].update(paket="bungalov")
    G["karavan-evlilik-teklifi"].update(paket="karavan")
    G["gondolda-evlilik-teklifi"].update(paket="gondol", sitemap_gal=["gondol"],
        service=dict(name="Gondolda evlilik teklifi organizasyonu", gal="gondol", area=["Eskişehir"]))
    G["kanlikavak-parki-evlilik-teklifi"].update(paket="kanlikavak", sitemap_gal=["kanlikavak"],
        lede="Kanlıkavak iskelesinde kalpli çiçek duvarı, neon yazı ve romantik bir masa. Kalabalıktan uzak, suyun kenarında bir an.",
        service=dict(name="Kanlıkavak evlilik teklifi organizasyonu", gal="kanlikavak", area=["Eskişehir"]))
    G["gaga-restoran-evlilik-teklifi"].update(paket="restoran", service=dict(name="Restoranda evlilik teklifi organizasyonu", area=["Eskişehir"]))
    G["ozel-gun-surprizleri"].update(video=["dogum-gunu"], hero_foto=("bungalov", "bungalov-onunde-love-harfleri-maytap"),
        desc=f"Eskişehir'de balon ev ve bungalovda doğum günü ve yıl dönümü sürprizi: Happy birthday ve Better together neon yazı, yaş pasta ve ışıklar. {tl(ozel_min())}'den.",
        service=dict(name="Doğum günü ve yıl dönümü sürpriz organizasyonu", area=["Eskişehir"], paketler=["balon-dogum-gunu", "balon-yildonumu", "bungalov-dogum-gunu", "bungalov-yildonumu"]))
    G["galeri"].update(video=["teklif", "reels", "dogum-gunu"], sitemap_gal=["balon-ev", "bungalov", "karavan", "gondol", "kanlikavak", "otel"],
        desc="Eskişehir'de kurduğumuz evlilik teklifi alanlarından gerçek fotoğraflar ve videolar: balon ev, bungalov, karavan, gondol, Kanlıkavak ve otel.",
        lede="Kendi kurulumlarımızdan gerçek kareler ve videolar. Konseptleri fotoğraflardan inceleyin.")
    G["evlilik-teklifi-fiyatlari"].update(
        title=f"Evlilik Teklifi Fiyatları 2026 | Eskişehir, {tl(EN_DUSUK)}'den",
        desc=f"Eskişehir evlilik teklifi fiyatları: {fiyat_ozet(4)}. Tüm paket içerikleri ve güncel kampanya fiyatları.",
        lede="Eskişehir'deki tüm evlilik teklifi paketlerimizin güncel fiyatları ve içerikleri. Tarihinizi yazın, müsaitliği aynı gün iletelim.",
        sitemap_gal=["balon-ev", "bungalov", "karavan", "gondol", "kanlikavak", "otel"],
        service=dict(name="Evlilik teklifi organizasyonu paketleri", area=["Eskişehir"], paketler=["gondol", "balon-ev", "bungalov", "karavan", "kanlikavak", "otel", "restoran"]),
        faq=F(("Evlilik teklifi organizasyonu fiyatı ne kadar?", f"Eskişehir'de güncel paket fiyatlarımız: {fiyat_ozet()}. Fiyata paketteki süsleme ve kurulum dahil."),
              ("En uygun evlilik teklifi paketi hangisi?", f"{tl(en_uygun()[1])} ile {en_uygun()[0]} paketi. Özel bir alanda teklif istiyorsanız balon ev paketi {tl(PAKET['balon-ev']['fiyat'])}."),
              ("Paket fiyatına neler dahil değil?", "Gondol konseptinde gondol ücreti, restoran konseptinde yemek pakete dahil değil. Paket listesinde olmayan istekler için fiyatı ayrıca iletiyoruz."),
              ("14 Şubat'ta fiyatlar değişiyor mu?", "14 Şubat ve yılbaşı gibi yoğun tarihler erken doluyor. Bu tarihler için olabildiğince erken yazın; fiyatın güncelliğini tarih sorarken birlikte teyit ediyoruz.")))
    G["teklif-al"].update(lede="Konsepti seçin, tarihi yazın ve tek dokunuşla WhatsApp'a gönderin. Müsaitliği aynı gün iletiyoruz.")
    G["evlilik-teklifi-mekanlari"].update(
        desc="Eskişehir evlilik teklifi mekanları: balon ev, bungalov, karavan ve otel konseptleri ile gondol, Kanlıkavak, Sazova ve restoran gibi şehrin sevilen noktaları.",
        hero_foto=("bungalov", "bungalov-onunde-love-harfleri-evet"))
    G["evlilik-teklifi-mekanlari"]["yan_baglar"] = G["evlilik-teklifi-mekanlari"]["yan_baglar"] + [("Otel odası", "otel-odasinda-evlilik-teklifi")]

    add(slug="otel-odasinda-evlilik-teklifi", title="Otel Odasında Evlilik Teklifi Eskişehir | Balon ve Güller",
        desc=f"Eskişehir'de otel odasında evlilik teklifi: kalpli helyum balonlar, LOVE folyo balon, gül yapraklarıyla Marry Me ve romantik notlar. Paket {tl(PAKET['otel']['fiyat'])}.",
        h1="Otel odasında evlilik teklifi", lede="Kalpli helyum balonlar, gül yapraklarıyla yazılmış Marry Me ve romantik notlar. Kapı açıldığında başlayan, baş başa bir teklif.",
        crumbs=[("Mekanlar", "evlilik-teklifi-mekanlari"), ("Otel odası", "otel-odasinda-evlilik-teklifi")], konsept="otel", paket="otel",
        konu="otel odasında evlilik teklifi", body=otel_body, sitemap_gal=["otel"],
        service=dict(name="Otel odasında evlilik teklifi organizasyonu", gal="otel", area=["Eskişehir"]),
        yan_baglar=[("Balon evde evlilik teklifi", "balon-ev-evlilik-teklifi"), ("Bungalovda evlilik teklifi", "bungalov-evlilik-teklifi"), ("Evlilik teklifi fiyatları", "evlilik-teklifi-fiyatlari")],
        faq=F(("Otel odasında evlilik teklifi için neler hazırlanıyor?", "10 adet helyum kalpli balon, LOVE folyo balon, gül yapraklarıyla Marry Me süslemesi, yerlerde kalpli balonlar, fotoğraf köşesi ve kalpli kutu içinde romantik notlar."),
              ("Oda süslemesi ne zaman yapılıyor?", "Siz odaya gelmeden önce. Saatini otelin giriş saatine ve sizin akşam planınıza göre birlikte belirliyoruz."),
              ("Hangi otelde yapılabilir?", "Eskişehir'de kalacağınız otelde. Odaya önceden girilip süsleme yapılabilmesi otelin onayına bağlı olduğu için uygunluğu tarih sorarken birlikte kontrol ediyoruz.")))
    G["otel-odasinda-evlilik-teklifi"]["og"] = "otel-odasinda-evlilik-teklifi"
    # yönetim panelindeki "Sayfa kapakları" (boş bırakılan sayfa, fotoğrafsız şarap rengi başlıkla açılır)
    for o in GORSEL.get("sayfa_kapaklari") or []:
        if o and o.get("sayfa") in G:
            G[o["sayfa"]]["hero_foto"] = o.get("gorsel") or None
    return P


# ======================================================================== ANAHTAR KELİME GENİŞLETMESİ (Google Trends verisine göre)
def sozler_body(c):
    p = PAGES_BY["blog/evlilik-teklifi-sozleri"]
    kisa = ["Hayatımın geri kalanını seninle geçirmek istiyorum. Benimle evlenir misin?",
            "Her sabah seninle uyanmak istiyorum. Evet der misin?",
            "Bugüne kadarki en güzel kararım sendin. Sıradaki kararı birlikte verelim mi?",
            "Seninle her şey ev gibi. Gerçekten bir evimiz olsun mu?",
            "Kalbimi çoktan sana verdim, şimdi de elimi uzatıyorum.",
            "Bir ömür boyu yol arkadaşım olur musun?",
            "Sen yanımdayken her gün bayram. Bu bayramı ömür boyu sürdürelim mi?",
            "Seni sevmek en kolay işim. Seninle evlenmek en büyük hayalim.",
            "İkimizin hikâyesine bir “evet” eksik.",
            "Bundan sonraki bütün yıl dönümlerimizi seninle kutlamak istiyorum."]
    romantik = ["Seninle tanıştığım gün bir şeyin başladığını biliyordum; bugün o şeyin adını koymak istiyorum.",
                "Gözlerine her baktığımda aynı cevabı buluyorum: sen. Şimdi senin cevabını duymak istiyorum.",
                "Dünyanın neresinde olursak olalım, eve dönmek seninle olsun istiyorum.",
                "Yıllar geçsin, saçlarımız beyazlasın; ben yine bu soruyu sormaktan mutlu olacağım.",
                "Senin gülüşünle başlayan her gün benim için bir armağan. Bu armağanı ömür boyu almak istiyorum.",
                "Hayallerimin hepsinde sen varsın. Şimdi onları gerçeğe dönüştürmeye ne dersin?",
                "Bir yıldız kadar uzak değil, bir yüzük kadar yakınım sana."]
    duygusal = ["Seninle geçirdiğim her gün bana sevginin ne olduğunu yeniden öğretti. Zor günlerde elimi bırakmadın, güzel günlerde gülüşünle her şeyi daha da güzelleştirdin. Bu yüzden bugün, sana bütün kalbimle soruyorum: Benimle evlenir misin?",
                "Bu yere seni tesadüfen getirmedim. Burası bizim hikâyemizin yeni sayfası olsun istedim. Ben o sayfayı seninle yazmak, her satırında seninle olmak istiyorum.",
                "Yanında kendim olabiliyorum. Hiçbir şeyi saklamadan, hiçbir şeyden korkmadan. Ömrümün geri kalanında da böyle olmak, seninle olmak istiyorum."]
    esprili = ["Kumanda sende kalabilir, yeter ki evet de.",
               "Çayını demleyecek, kahveni pişirecek, ömür boyu seni güldürecek birini arıyorsan... başvurum burada.",
               "Bulaşık sırası konusunda uzlaşmaya hazırım. Benimle evlenir misin?",
               "Bu yüzük geri iade edilemez, sen de edilemezsin. Evet mi?"]
    ul = lambda xs: "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in xs) + "</ul>"
    inner = f'''<p>“Evlilik teklifi sözleri”, teklif hazırlığında en çok aranan konuların başında geliyor. Aşağıdaki cümleleri olduğu gibi kullanabilir ya da kendi hikâyenize göre değiştirebilirsiniz. En etkili söz, sizin ağzınızdan çıkan söz.</p>
<h2>Kısa evlilik teklifi sözleri</h2>{ul(kisa)}
<h2>Romantik evlilik teklifi sözleri</h2>{ul(romantik)}
<h2>Duygusal ve uzun evlilik teklifi konuşmaları</h2>{"".join(f"<blockquote>{esc(x)}</blockquote>" for x in duygusal)}
<h2>Esprili evlenme teklifi sözleri</h2>
<p>Sevdiğiniz kişi gülmeyi seviyorsa, gerginliği bir gülümsemeyle kırmak iyi gelebilir:</p>{ul(esprili)}
<h2>Kendi teklif sözünüzü yazmak için üç adım</h2>
<ol><li><strong>Bir anı:</strong> İlk buluşmanız, birlikte güldüğünüz bir an ya da zor bir günde yanınızda olması.</li>
<li><strong>Neden o:</strong> Onu diğer herkesten ayıran tek bir özellik.</li>
<li><strong>Soru:</strong> “Benimle evlenir misin?” Sade ve net.</li></ol>
<p>Üç cümle yeterli. Heyecandan unutmamak için sözünüzü bir iki kez kendi kendinize söyleyin; kâğıda yazıp cebinizde taşımak da işe yarar.</p>
<h2>Sözlerinizi alana taşıyın</h2>
<p>Seçtiğiniz cümle neon yazıda, bir kartta ya da ortak fotoğraflarınızın asıldığı panoda yer alabilir. <a href="{c.L("balon-ev-evlilik-teklifi")}">Balon evde</a> “Benimle evlenir misin?”, <a href="{c.L("bungalov-evlilik-teklifi")}">bungalovda</a> “Will you marry me” neon yazısı kullanıyoruz; kendi cümlenizi eklemek isterseniz <a href="{c.L("teklif-al")}">fiyat formunda</a> belirtin.</p>'''
    return article_layout(c, p, inner + ilg(c, "fikir", "nasil", "yuzuk"))


def fikirler_body(c):
    p = PAGES_BY["blog/evlilik-teklifi-fikirleri"]
    inner = f'''<p>En güzel evlilik teklifi, sevdiğiniz kişiye en çok benzeyen teklif. Aşağıdaki fikirleri sadeden görkemliye doğru sıraladık; Eskişehir'de teklif planlayanlar için şehre özel önerileri de ekledik.</p>
<h2>Sade evlilik teklifi fikirleri</h2>
<ul><li><strong>İlk buluşma yerinde:</strong> Tanıştığınız kafeye ya da ilk yürüyüş yaptığınız sokağa geri dönün.</li>
<li><strong>Evde akşam yemeği:</strong> Mumlar, sevdiği yemek ve tatlıyla birlikte gelen bir yüzük.</li>
<li><strong>Fotoğraf albümü:</strong> Birlikte geçen yılların fotoğrafları, son sayfada tek bir soru.</li>
<li><strong>Sabah kahvesiyle:</strong> Her günkü rutinin içine saklanmış bir sürpriz; en sade ama en samimi fikirlerden biri.</li>
<li><strong>Mektupla:</strong> Elle yazılmış bir mektup; son cümlesi sorunun kendisi.</li></ul>
<h2>Romantik evlilik teklifi fikirleri</h2>
<ul><li><strong>Işıklı bir kubbede:</strong> Şeffaf bir <a href="{c.L("balon-ev-evlilik-teklifi")}">balon ev</a>, kırmızı halı ve ışıklı MARRY ME harfleri.</li>
<li><strong>Şömine başında:</strong> Kapalı ve sıcak bir <a href="{c.L("bungalov-evlilik-teklifi")}">bungalovda</a> neon yazının altında.</li>
<li><strong>Işık tavanı altında piknik:</strong> Sarı bir vintage <a href="{c.L("karavan-evlilik-teklifi")}">karavanın</a> önünde, minderler ve LOVE harfleriyle.</li>
<li><strong>Gün batımında:</strong> Havanın karardığı an ışıkların yandığı bir kurgu.</li>
<li><strong>Yıl dönümünde:</strong> Zaten kutlama yapacağınız bir akşam, şüphe uyandırmadan sürpriz için en kolay fırsat.</li></ul>
<h2>Sürpriz evlilik teklifi fikirleri</h2>
<ul><li><strong>Arkadaşlarla:</strong> Teklif anında arkadaşların bir köşeden çıkıp kutlamaya katılması.</li>
<li><strong>Pankartla:</strong> Bir köprüden ya da balkondan açılan “Benimle evlenir misin?” pankartı.</li>
<li><strong>Sinemada:</strong> Film arasında perdeye yansıyan kısa bir video.</li>
<li><strong>Maytaplarla:</strong> Evet'in hemen ardından ışıl ışıl bir kutlama.</li></ul>
<p>Sürprizin bozulmaması için püf noktalarını <a href="{c.L("surpriz-evlilik-teklifi")}">sürpriz evlilik teklifi</a> sayfamızda anlattık.</p>
<h2>Eskişehir'e özel evlilik teklifi fikirleri</h2>
<ul><li><strong>Porsuk'ta gondol:</strong> Adalar'da köprünün altından geçerken sorulan soru. Ayrıntılar: <a href="{c.L("gondolda-evlilik-teklifi")}">gondolda evlilik teklifi</a>.</li>
<li><strong>Sazova'da şato önünde:</strong> Masal gibi bir arka plan. Ayrıntılar: <a href="{c.L("sazova-parki-evlilik-teklifi")}">Sazova Parkı'nda evlilik teklifi</a>.</li>
<li><strong>Odunpazarı sokaklarında:</strong> Renkli tarihi evlerin arasında akşam yürüyüşü.</li>
<li><strong>Kanlıkavak'ta:</strong> Yeşilin içinde daha sakin bir an. Ayrıntılar: <a href="{c.L("kanlikavak-parki-evlilik-teklifi")}">Kanlıkavak Parkı</a>.</li>
<li><strong>Tarihi bir mekânda:</strong> Han ilçesindeki Yazılıkaya gibi tarihi alanlar, farklı bir hikâye isteyenlerin seçimi oluyor.</li></ul>
<h2>Hangi fikir size uygun?</h2>
<table><thead><tr><th>Sevdiğiniz kişi...</th><th>Önerimiz</th></tr></thead><tbody>
<tr><td>Kalabalıktan hoşlanmıyorsa</td><td>Bungalov veya evde sade bir teklif</td></tr>
<tr><td>Büyük bir an hayal ediyorsa</td><td>Balon ev, MARRY ME harfleri ve kırmızı halı</td></tr>
<tr><td>Doğayı ve yolculuğu seviyorsa</td><td>Karavan konsepti veya açık havada bir teklif</td></tr>
<tr><td>Arkadaşlarıyla kutlamayı seviyorsa</td><td>Teklifin ardından arkadaşların katıldığı bir kutlama</td></tr></tbody></table>'''
    return article_layout(c, p, inner + ilg(c, "soz", "surpriz", "balon"))


def detay_body(c):
    p = PAGES_BY["blog/evlilik-teklifi-cicegi-pastasi-pozlari"]
    inner = f'''<p>Teklifin kendisi birkaç dakika sürse de, akılda kalan küçük detaylar: elindeki çiçek, ardından kesilen pasta ve yıllarca bakılacak fotoğraflar. Bu yazıda üçünü de ele alıyoruz.</p>
<h2>Evlilik teklifi çiçeği</h2>
<p>Kırmızı gül hâlâ en klasik seçim; tutkuyu ve aşkı anlatıyor. Daha zarif bir görünüm istiyorsanız beyaz ya da açık pembe tonlar, sevdiği bir çiçek varsa doğrudan o çiçek en kişisel seçim olur.</p>
<ul><li><strong>Buket:</strong> Soruyu sorduğunuz anda vermek için.</li>
<li><strong>Yol ve çevre süslemesi:</strong> Kırmızı halının iki yanı ya da masanın üzeri için.</li>
<li><strong>Tek gül:</strong> Sade bir teklifte en etkili detaylardan biri.</li></ul>
<h2>Evlilik teklifi pastası</h2>
<p>Evet'in ardından kesilen küçük bir pasta, kutlamayı tamamlıyor. Üzerinde “Benimle evlenir misin?” ya da sadece “Evet” yazan, iki kişilik bir pasta çoğu zaman yeterli. Teklif sonrası arkadaşlarınız da gelecekse boyutu buna göre seçin. Pasta ve ikram seçeneklerini <a href="{c.L("teklif-al")}">fiyat formunda</a> işaretleyebilirsiniz.</p>
<h2>Evlilik teklifi fotoğraf pozları</h2>
<p>Teklif anını bir arkadaşınızın ya da anlaştığınız bir fotoğrafçının çekmesini planlıyorsanız, en çok tercih edilen kareler şunlar:</p>
<ul><li><strong>Diz çöküş anı:</strong> Yandan, ikinizi ve arka plandaki ışıkları birlikte gösteren kare.</li>
<li><strong>Yüzüklü el:</strong> Arka planda bulanık ışıklar, önde yüzüklü el. Sade ama çok sevilen bir poz.</li>
<li><strong>Harflerin arasında:</strong> MARRY ME ya da LOVE harflerinin ortasında, kırmızı halının üzerinde.</li>
<li><strong>Maytaplarla:</strong> Kollar yukarıda, ellerde maytaplar, arkada ışıklı bir bungalov.</li>
<li><strong>Siyah beyaz:</strong> Duyguyu öne çıkaran, zamansız bir kare.</li></ul>
<p>Bu pozların gerçek örneklerini <a href="{c.L("galeri")}">galerimizde</a> görebilirsiniz.</p>
<div class="galeri" style="margin-top:1rem">{photo(c, "bungalov", "evlilik-teklifi-yuzuk-bungalov-onunde")}{photo(c, "balon-ev", "balon-ev-evlilik-teklifi-siyah-beyaz")}{photo(c, "bungalov", "bungalov-onunde-love-harfleri-maytap")}</div>'''
    return article_layout(c, p, inner + ilg(c, "soz", "fikir", "susleme"))


def susleme_body(c):
    p = PAGES_BY["evlilik-teklifi-susleme"]
    inner = f'''<h2>Teklif alanını oluşturan parçalar</h2>
<p>Fotoğraflarımızda gördüğünüz kurulumlar, birkaç temel parçanın bir araya gelmesiyle oluşuyor. Hepsini konsepte ve tercihlerinize göre birlikte seçiyoruz:</p>
<table><thead><tr><th>Süsleme</th><th>Ne işe yarar?</th></tr></thead><tbody>
<tr><td>Işıklı MARRY ME ve LOVE harfleri</td><td>Sahnenin merkezi; uzaktan görünür, fotoğrafta öne çıkar.</td></tr>
<tr><td>Neon yazı</td><td>“Benimle evlenir misin?” ya da “Will you marry me”; iç mekânda sıcak bir ışık verir.</td></tr>
<tr><td>Kırmızı halı ve fenerler</td><td>Sevdiğiniz kişiyi soruya doğru yürüten yol.</td></tr>
<tr><td>Işık zincirleri</td><td>Alanın üzerinde yıldızlı bir tavan etkisi.</td></tr>
<tr><td>Çiçek ve buket</td><td>Masada, yolda ve soruyu sorduğunuz anda elinizde.</td></tr>
<tr><td>Fotoğraf panosu</td><td>Ortak fotoğraflarınızla alanı size özel hale getirir.</td></tr>
<tr><td>Balon süsleme</td><td>Kalp ve renkli balonlarla daha neşeli bir hava.</td></tr>
<tr><td>Maytap</td><td>Evet'in ardından kısa ve ışıltılı bir kutlama.</td></tr></tbody></table>
<h2>Konsepte göre süsleme</h2>
<ul><li><a href="{c.L("balon-ev-evlilik-teklifi")}">Balon ev</a>: MARRY ME harfleri, kırmızı halı, fenerler; içeride şömine, neon yazı ve iki kişilik masa.</li>
<li><a href="{c.L("bungalov-evlilik-teklifi")}">Bungalov</a>: Işıklı A-frame cephe, LOVE veya MARRY ME harfleri; içeride neon yazı ve şömine.</li>
<li><a href="{c.L("karavan-evlilik-teklifi")}">Karavan</a>: Işık zinciri tavanı, LOVE harfleri, piknik köşesi ve çadır.</li></ul>
<h2>Kendi belirlediğiniz bir yerde süsleme</h2>
<p>Teklifi evinizde, bahçenizde ya da bir mekânda yapmak istiyorsanız, süslemenin o alana uygun olup olmadığını birlikte değerlendiriyoruz. Yeri, tarihi ve aklınızdaki düzeni WhatsApp'tan yazmanız yeterli.</p>
<h2>Fotoğraflardan örnekler</h2>
<div class="galeri">{photo(c, "balon-ev", "eskisehir-balon-ev-evlilik-teklifi-marry-me")}{photo(c, "bungalov", "bungalov-ici-will-you-marry-me-neon")}{photo(c, "karavan", "eskisehir-karavan-evlilik-teklifi-love")}</div>'''
    inner += sss_html(p["faq"]) + ilg(c, "fiyat", "balon", "fikir")
    return article_layout(c, p, inner)


def bursa_body(c):
    return sehir(c, "bursa-evlilik-teklifi", f'''<h2>Bursa'dan Eskişehir'e: iki saatlik bir sürpriz</h2>
<p>Bursa ile Eskişehir arası karayoluyla yaklaşık 150 km; arabayla iki saat civarı. Yol İnegöl ve Bozüyük üzerinden geçtiği için teklif gününü küçük bir yolculuğa dönüştürmek kolay.</p>
{{HARITA}}
<h2>İnegöl'den gelen çiftler</h2>
<p>İnegöl, Bursa'nın Eskişehir'e en yakın ilçelerinden biri. İnegöl'den gelen çiftler için yol süresi daha kısa; akşam planını buna göre kuruyoruz.</p>
<h2>Uzaktan planlama</h2>
<p>Konsepti fotoğraflardan seçiyor, detayları WhatsApp ve telefonla netleştiriyoruz. Teklif gününe kadar Eskişehir'e gelmenize gerek yok.</p>
{{YORUM}}
<h2>Konsept önerimiz</h2>
<ul><li><a href="{c.L("balon-ev-evlilik-teklifi")}">Balon ev</a>: yolun sonunda ışıl ışıl, büyük bir sahne.</li>
<li><a href="{c.L("bungalov-evlilik-teklifi")}">Bungalov</a>: uzun yolun ardından sıcak ve kapalı bir mekân.</li>
<li><a href="{c.L("karavan-evlilik-teklifi")}">Karavan</a>: yolculuk hikâyesine uygun, rahat bir atmosfer.</li></ul>
<p>Kurulumu Bursa'da belirlediğiniz bir yerde istiyorsanız, konsept ve tarihe göre mümkün olup olmadığını birlikte konuşalım.</p>''')


KONSEPT_ILGILI.update({
    "soz": ("Evlilik teklifi sözleri", "blog/evlilik-teklifi-sozleri", "Kısa, romantik ve duygusal örnekler"),
    "fikir": ("Evlilik teklifi fikirleri", "blog/evlilik-teklifi-fikirleri", "Sadeden görkemliye, Eskişehir'e özel fikirler"),
    "susleme": ("Evlilik teklifi süsleme", "evlilik-teklifi-susleme", "MARRY ME harfleri, neon yazı, kırmızı halı"),
    "detay": ("Çiçek, pasta ve pozlar", "blog/evlilik-teklifi-cicegi-pastasi-pozlari", "Teklifin akılda kalan detayları"),
})
KONSEPT_ILGILI["yuzuk"] = ("Evlilik teklifi yüzüğü", "blog/evlilik-teklifi-yuzugu", "Hangi parmağa takılır, ölçü nasıl öğrenilir")


# ======================================================================== ESKİ SİTEDEN GELEN KONSEPTLER VE SAYFALAR
def gaga_body(c):
    p = PAGES_BY["gaga-restoran-evlilik-teklifi"]
    inner = f'''<h2>Porsuk'un ortasında bir adada akşam yemeği</h2>
<p>Gaga Restaurant, Porsuk Çayı üzerindeki Fener Adası'nda; restorana kıyıdan bir köprüyle yürüyerek geçiliyor. Kahvaltıdan akşam yemeğine kadar hizmet veren, manzarası ve şık atmosferiyle bilinen, özel davetlere de sık sık ev sahipliği yapan bir mekân. Bu yüzden “romantik bir akşam yemeğinde evlilik teklifi” isteyen çiftlerin ilk aklına gelen adreslerden biri.</p>
<h2>Restoranda evlilik teklifi nasıl kurgulanır?</h2>
<ul><li><strong>Masa ve zamanlama:</strong> Manzaralı bir masa ve tatlı servisi gibi doğal bir an, sorunun en rahat sorulduğu zaman.</li>
<li><strong>Küçük ama etkili detaylar:</strong> Masada çiçek, kişisel bir not ya da yüzüğün sunulacağı özel bir kutu.</li>
<li><strong>Sürpriz kutlama:</strong> Evet'in ardından arkadaşların ya da ailenin masaya katılması.</li>
<li><strong>Kapanış:</strong> Akşamı köprüden geçerek Porsuk kıyısında bir yürüyüşle ya da ışıkların yandığı <a href="{c.L("balon-ev-evlilik-teklifi")}">balon evde</a> baş başa bir kutlamayla bitirmek.</li></ul>
<h2>Restoran konsepti paketi</h2>
<ul class="tik">{"".join(f"<li>{x}</li>" for x in PAKET["restoran"]["icerik"])}</ul>
<p>Paket fiyatı <strong>{tl(PAKET["restoran"]["fiyat"])}</strong>. Yemek pakete dahil değildir. Masa rezervasyonu ve mekânda yapılabilecek süslemeler restoranın kurallarına ve onayına bağlı olduğu için tarihinizi önceden netleştirmenizi öneriyoruz.</p>
<div class="not-kutu"><p>Gaga Restaurant bağımsız bir işletmedir; masa rezervasyonu ve mekân kuralları için doğrudan restoranla görüşmeniz gerekir. Teklif kurgusu ve süsleme için bize WhatsApp'tan yazabilirsiniz.</p></div>'''
    inner += sss_html(p["faq"]) + ilg(c, "gondol", "balon", "fikir")
    return article_layout(c, p, inner)


def ozel_gun_body(c):
    p = PAGES_BY["ozel-gun-surprizleri"]
    kart = "".join(paket_html(c, k) for k in ("balon-dogum-gunu", "bungalov-dogum-gunu", "balon-yildonumu", "bungalov-yildonumu"))
    inner = f'''<h2>Aynı ışıklar, başka bir kutlama</h2>
<p>Evlilik teklifi için kurduğumuz alanlar, sevdiğiniz kişiye yapacağınız diğer sürprizler için de çok uygun. Balon evin içinde neon bir “Happy birthday” yazısı, bungalovun önünde ışıklı LOVE harfleri, şömine başında bir masa; konsept aynı, hikâye farklı.</p>
{video_html(c, "dogum-gunu")}
<h2>Doğum günü ve yıl dönümü paketleri</h2>
<p>Doğum günü paketlerinde “Happy birthday”, yıl dönümü paketlerinde “Better together” neon yazısı var. Yaş pasta ve soft içecek dört pakete de dahil.</p>
<div class="paketler ikili">{kart}</div>
<h2>Doğum günü sürprizi</h2>
<p>Sevdiğiniz kişiyi sıradan bir akşam yemeği bahanesiyle getirip balon evin kapısında karşılamak, en çok tercih edilen kurgulardan biri.</p>
<h2>Yıl dönümü sürprizi</h2>
<p>Tanışma ya da evlilik yıl dönümünüz için <a href="{c.L("bungalov-evlilik-teklifi")}">bungalovda</a> şömine başında bir akşam ya da <a href="{c.L("balon-ev-evlilik-teklifi")}">balon evde</a> ortak fotoğraflarınızla süslenmiş bir masa. Yıl dönümü aynı zamanda evlilik teklifi için de en doğal bahanelerden biri.</p>
<h2>Nişan</h2>
<p>Teklifin ardından gelen nişan için daha kalabalık bir davet planlıyorsanız, düğün, nişan ve kına organizasyonlarında 20 yıllık deneyime sahip <a href="{C["PARENT_URL"]}" target="_blank" rel="noopener">{C["PARENT"]}</a> ekibiyle çalışabilirsiniz.</p>'''
    inner += sss_html(p["faq"]) + ilg(c, "balon", "susleme", "fiyat")
    return article_layout(c, p, inner)


def hakkimizda_body(c):
    return f'''<div class="bolum"><div class="kap icerik-izgara"><div class="icerik">
<h2>Biz kimiz?</h2>
<p>{C["BRAND"]}, Eskişehir'de yalnızca evlilik teklifine odaklanan bir organizasyon markası. Düğün, nişan, kına ve kurumsal organizasyonlarda 20 yıllık deneyime sahip <a href="{C["PARENT_URL"]}" target="_blank" rel="noopener">{C["PARENT"]}</a> çatısı altında çalışıyoruz.</p>
<h2>Ne yapıyoruz?</h2>
<p>Teklifin kurgusunu, süslemesini, kurulumunu ve zamanlamasını üstleniyoruz. <a href="{c.L("balon-ev-evlilik-teklifi")}">Balon ev</a>, <a href="{c.L("bungalov-evlilik-teklifi")}">bungalov</a>, <a href="{c.L("karavan-evlilik-teklifi")}">karavan</a> ve <a href="{c.L("otel-odasinda-evlilik-teklifi")}">otel</a> konseptlerimizin yanında <a href="{c.L("gondolda-evlilik-teklifi")}">gondol</a>, <a href="{c.L("sazova-parki-evlilik-teklifi")}">Sazova</a>, <a href="{c.L("kanlikavak-parki-evlilik-teklifi")}">Kanlıkavak</a> ve <a href="{c.L("gaga-restoran-evlilik-teklifi")}">restoran</a> gibi şehrin sevilen noktalarında da teklif planlıyoruz.</p>
<h2>Nasıl çalışıyoruz?</h2>
<ul><li>Planlamayı yalnızca sizinle yürütüyoruz; sürpriz bozulmasın diye.</li>
<li>Konsepti fotoğraflardan birlikte seçiyor, detayları WhatsApp'tan netleştiriyoruz.</li>
<li>Siz gelmeden alan hazır, ışıklar yanıyor oluyor; toparlama ve söküm de bizde.</li></ul>
<h2>Bizi takip edin</h2>
<p>Kurulumlarımızı <a href="{C["INSTAGRAM"]}" target="_blank" rel="noopener">Instagram</a> ve <a href="{C["YOUTUBE"]}" target="_blank" rel="noopener">YouTube</a> hesaplarımızda paylaşıyoruz.</p>
</div><aside class="yan"><div class="yan-iletisim"><h2>Tanışalım</h2><p>Aklınızdaki teklifi anlatın, birlikte kuralım.</p>
<a class="dugme altin" href="{wa("Merhaba, evlilik teklifi için bilgi almak istiyorum.")}" data-konum="hakkimizda" target="_blank" rel="noopener">{IC_SOHBET} WhatsApp</a></div></aside></div></div>'''


def otel_body(c):
    p = PAGES_BY["otel-odasinda-evlilik-teklifi"]
    inner = f'''<h2>Kapı açıldığında</h2>
<p>Tavana yükselen kırmızı kalpli balonlar, yatağın üzerinde gül yapraklarıyla yazılmış “Marry Me”, yerlerde kalpli balonlar ve gümüş LOVE harfleri. Otel konsepti, teklifi baş başa ve kapalı bir ortamda yapmak isteyenler için en sade ve en romantik seçeneklerden biri.</p>
<figure class="icerik-foto foto-dar">{img(c, "otel", "otel-odasi-evlilik-teklifi-marry-me-gul", "380px")}<figcaption class="kucuk">Otel odasında gül yapraklarıyla MARRY ME ve LOVE balonları</figcaption></figure>
<h2>Otel paketinde neler var?</h2>
<ul class="tik">{"".join(f"<li>{x}</li>" for x in PAKET["otel"]["icerik"])}</ul>
<p>Paket fiyatı <strong>{tl(PAKET["otel"]["fiyat"])}</strong>.</p>
<h2>Kimler için uygun?</h2>
<p>Bir şehir kaçamağının ortasında, bir yıl dönümü akşamında ya da başka bir şehirden Eskişehir'e gelen çiftler için. Kütahya, Bilecik, Afyonkarahisar veya Bursa'dan gelip geceyi Eskişehir'de geçirecekseniz, otel konsepti yolculuğu da teklifin bir parçası yapıyor. Soğuk ve yağışlı günlerde hava durumundan hiç etkilenmemesi de bir artı.</p>
<h2>Otel ve süsleme saati</h2>
<p>Hangi otelde kalacağınızı, giriş saatinizi ve süslemenin ne zaman yapılacağını tarih sorarken birlikte netleştiriyoruz. Odaya sizden önce girilip süsleme yapılabilmesi otelin onayına bağlı olduğu için otel rezervasyonunuzu yaptığınızda bize haber verin.</p>
<h2>Teklif anı için birkaç öneri</h2>
<ul><li>Odaya girmeden önce kapıda kısa bir bahane: “Bir şeyi arabada unuttum.”</li>
<li>Kalpli kutudaki notlara ortak anılarınızdan küçük cümleler yazın.</li>
<li>Akşam yemeğinden dönüşte odaya girmek, ışıkların ve balonların en etkili göründüğü an.</li></ul>'''
    inner += sss_html(p["faq"]) + ilg(c, "balon", "bungalov", "fiyat")
    return article_layout(c, p, inner)


KONSEPT_ILGILI["otel"] = ("Otel odasında evlilik teklifi", "otel-odasinda-evlilik-teklifi", "Kalpli balonlar ve güllerle Marry Me")
KONSEPT_ILGILI["gaga"] = ("Gaga Restoran'da evlilik teklifi", "gaga-restoran-evlilik-teklifi", "Porsuk'taki adada romantik bir akşam yemeği")
