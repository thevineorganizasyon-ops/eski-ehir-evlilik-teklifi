# Eskişehir Evlilik Teklifi: Kurulum ve SEO Yol Haritası

Bu pakette yayına hazır site (`site/` klasörü) ve siteyi yeniden üretmek için kaynak dosyalar (`kaynak/`) var.

## 1. Yayına almadan önce netleşmesi gerekenler

| Konu | Durum | Ne yapılmalı |
|---|---|---|
| Alan adı | Site, yeni alan adı `www.eskisehirevlilikteklifi.com` için hazır | Alan adı satın alınacak (yalnızca alan adı; hosting Netlify'da ücretsiz). Eski Wix sitesi `.com.tr` yayında kalıyor. |
| Google Tag Manager kimliği | Yer tutucu: `GTM-XXXXXXX` | GTM hesabı açın, kimliği `BASE`'in altındaki `GTM_ID` satırına yazın, yeniden üretin. Kimlik girilene kadar hiçbir izleme kodu yüklenmez. |
| E-posta | Sitede gösterilmiyor | İsterseniz `SITE_EMAIL` ortam değişkeniyle eklenebilir. |
| Posta kodu | 26010 (onaylandı) | Google İşletme Profili'nde de 26010 olmalı (`ADDR_POST`). |
| Fotoğraf izinleri | Sitede yüzü görünen çiftler var | Her çiftten yayın için yazılı (WhatsApp mesajı yeterli olabilir) izin alın. KVKK açısından önemli. |
| Gizlilik metni | Şablon | Yayından önce bir hukukçuya kontrol ettirin. |
| Üstü çizili fiyatlar | Kapalı; sitede yalnızca güncel fiyat görünüyor | Afişlerdeki "%50 indirimli" eski fiyatları göstermek için `build.py`'de `ESKI_FIYAT_GOSTER = True` yapın. Yapmadan önce: Türkiye'deki indirimli satış kuralları, indirimden önceki fiyatın son 30 günün en düşük fiyatı olmasını istiyor. Eski fiyatla gerçekten satış yapılmadıysa bu satırı kapalı bırakın. |
| Fotoğraf ve video çekimi | Restoran paketinde "Fotoğraf & video çekimi" yazıyor (afişteki gibi) | Diğer paketlerde de varsa yönetim panelinden ilgili paketlerin içeriğine madde olarak ekleyin; restoranda yoksa oradan çıkarın. |
| Otel paketi | Oda ücretinin dahil olup olmadığı sitede yazmıyor | Netleşince otel sayfasının SSS bölümüne bir cevap ekleyin. |
| Sazova fiyatı | Güncel afiş yok, sitede "Fiyat için sorun" | Fiyat belli olunca bana yazın; Sazova'yı panele paket olarak ekleyelim. |
| Yönetim paneli | Hazır (`/admin/`) | Bir kerelik Netlify kurulumu gerekiyor: `YONETIM-PANELI.md`. |

## 2. Wix'ten taşıma (sıra önemli)

Wix'e kendi HTML dosyalarınızı yükleyemezsiniz; bu yüzden site, alan adınızın yönlendirileceği yeni bir hostinge kuruluyor.

1. **Önce yedek alın:** Eski site Search Console'a bağlıysa **Performans** raporunu (son 16 ay) dışa aktarın. Hangi aramalardan geldiğinizi görmek, yeni dönemde karşılaştırma için değerli.
2. **Barındırma:** Önerilen yol ücretsiz **Netlify**. Yönetim paneli yalnızca bu yolla kendiliğinden çalışır; adımlar `YONETIM-PANELI.md` dosyasının sonunda. Panel istemiyorsanız cPanel'li sıradan bir Linux hosting de olur (3. bölüm).
3. **Siteyi yayına alın** ve Netlify'ın (ya da hostingin) geçici adresinden kontrol edin.
4. **Alan adını bağlayın:** Yeni `.com` adresinin DNS ayarlarını aldığınız firmanın panelinden Netlify'a çevirin. Değişikliğin yayılması birkaç saat sürebilir.
4b. **Eski Wix sitesi yayında kalıyor:** İki site aynı aramalarda yarışır. Eski siteye yeni siteye giden belirgin bir bağlantı koyun, Google İşletme Profili'ndeki web sitesi adresini yeni siteye çevirin. İleride eski siteyi kapatmaya karar verirseniz `build.py` içindeki `ESKI_ALAN_ADLARI` satırına `.com.tr` adresini yazıp alan adını Netlify'a bağlamanız yeterli; eski adreslere gelenler yeni sitedeki doğru sayfaya yönlenir.
5. **Yönlendirmeleri test edin:** Eski adresler (`/evlilikteklifi`, `/shop`, `/product-page/balon-ev-konsepti` vb.) yeni sayfalara açılmalı.
6. **Wix aboneliğini en son iptal edin:** Yeni site sorunsuz çalıştıktan sonra.
7. **Bağlantıları güncelleyin:** Instagram (@eskisehirevlilikteklificom) ve YouTube açıklamalarındaki bağlantıları yeni sayfalara çevirin.

**Eski adreslerin yönlendirmeleri** (Netlify için `_redirects`, Apache hosting için `.htaccess` içinde hazır, kalıcı 301)

| Eski adres (Wix) | Yeni sayfa |
|---|---|
| `/evlilikteklifi` | Ana sayfa |
| `/doğumgünü`, `/nişan`, `/yıldönümü` | `/ozel-gun-surprizleri/` |
| `/hakkımızda` | `/hakkimizda/` |
| `/contact` | `/iletisim/` |
| `/shop` | `/evlilik-teklifi-fiyatlari/` |
| `/product-page/balon-ev-konsepti` | `/balon-ev-evlilik-teklifi/` |
| `/product-page/bungalov-konsepti` | `/bungalov-evlilik-teklifi/` |
| `/product-page/vosvos-konsepti` | `/karavan-evlilik-teklifi/` |
| `/product-page/gondol-konsepti` | `/gondolda-evlilik-teklifi/` |
| `/product-page/sazova-konsepti` | `/sazova-parki-evlilik-teklifi/` |
| `/product-page/kanlı-kavak-iskele-konsepti` | `/kanlikavak-parki-evlilik-teklifi/` |
| `/product-page/restorant-konsepti` | `/gaga-restoran-evlilik-teklifi/` |
| `/product-page/otel-konsepti` | `/otel-odasinda-evlilik-teklifi/` |
| `/product-page/orman-konsepti` | `/evlilik-teklifi-mekanlari/` |
| Süsleme ürünleri (meşale, volkan, gül, balon) | `/evlilik-teklifi-susleme/` |
| Kemancı, fotoğraf, video, drone | `/teklif-al/` |
| Diğer tüm `/product-page/...` | `/evlilik-teklifi-fiyatlari/` |

Eski mağazadaki fiyatlar yeni siteye **taşınmadı**; güncel olup olmadıkları bilinmiyor.

## 3. Sunucuya yükleme (yalnızca Netlify yerine cPanel hosting kullanacaksanız)

Netlify kullanıyorsanız bu bölümü atlayın; `YONETIM-PANELI.md` içindeki kurulum yeterli.

1. Hosting panelinden (cPanel vb.) **Dosya Yöneticisi**'ni açın, alan adının kök klasörüne (`public_html`) girin.
2. `site/` klasörünün **içindeki her şeyi** yükleyin. `.htaccess` gizli bir dosyadır; "gizli dosyaları göster" seçeneğini açıp yüklendiğinden emin olun.
3. SSL sertifikasını (Let's Encrypt, çoğu panelde ücretsiz) etkinleştirin. `.htaccess` tüm trafiği `https://www.` adresine yönlendirir.
4. Kontrol: `https://www.ALANADI/`, `https://www.ALANADI/balon-ev-evlilik-teklifi/` ve olmayan bir adres (404 sayfası) açılıyor mu?

## 4. Google Search Console

1. search.google.com/search-console → **Alan** türünde mülk ekleyin, DNS kaydıyla doğrulayın (en sağlam yöntem). Eski Wix sitesi için zaten bir mülk varsa aynı mülkü kullanmaya devam edin; geçmiş veriler korunur.
2. **Site haritaları** → `sitemap.xml` gönderin. Site haritasında 30 sayfa ve 12 fotoğraf var.
3. **URL denetimi** → ana sayfa ve üç konsept sayfası için "Dizine eklenmesini iste".
4. İlk 2-3 hafta **Performans** raporunda hangi aramalarda göründüğünüzü izleyin.

## 5. Google Tag Manager + Google Analytics 4

Site, ziyaretçi onayına göre çalışan **Consent Mode v2** ile hazır. Siteden GTM'e şu olaylar gönderiliyor:

| Olay adı | Ne zaman | Önerilen kullanım |
|---|---|---|
| `teklif_formu_gonder` | Fiyat formu WhatsApp'a gönderildiğinde (konsept, şehir bilgisiyle) | GA4 **anahtar etkinlik** (dönüşüm), Google Ads ve Meta dönüşümü |
| `whatsapp_tikla` | Herhangi bir WhatsApp bağlantısı tıklandığında (`konum` bilgisiyle) | GA4 anahtar etkinlik |
| `telefon_tikla` | Telefon numarası tıklandığında | GA4 anahtar etkinlik |
| `galeri_ac` | Galeride fotoğraf büyütüldüğünde | İlgi ölçümü |
| `cerez_karar` | Çerez bildirimi kabul/red | Kontrol |

GTM'de yapılacaklar:
1. **Google etiketi** (GA4 ölçüm kimliğiyle), tetikleyici: Tüm sayfalar.
2. Yukarıdaki her olay için **Özel etkinlik** tetikleyicisi + **GA4 etkinliği** etiketi. `konsept`, `sehir`, `konum` değerlerini Veri Katmanı Değişkeni olarak ekleyin.
3. GA4'te `teklif_formu_gonder`, `whatsapp_tikla`, `telefon_tikla` olaylarını **anahtar etkinlik** olarak işaretleyin.
4. Meta reklamları için Meta Pixel'i de GTM üzerinden, aynı tetikleyicilerle (`Lead` olayı) ekleyin. Koda ayrıca dokunmaya gerek yok.

## 6. Google İşletme Profili (yerel SEO'nun en önemli parçası)

"Eskişehir evlilik teklifi" aramalarında haritadaki ilk üç sonuç, çoğu zaman sitenin kendisinden daha çok tıklanır.

- Profilde web sitesi olarak yeni siteyi (veya evlilik teklifi hizmeti için bu sayfayı) gösterin.
- **Hizmetler** bölümüne ekleyin: Evlilik teklifi organizasyonu, Balon ev evlilik teklifi, Bungalov evlilik teklifi, Karavan evlilik teklifi.
- Hizmet bölgeleri: Eskişehir, Kütahya, Tavşanlı, Bilecik, Bozüyük, Afyonkarahisar.
- Ad, adres ve telefon, sitedekiyle **birebir aynı** yazılmalı.
- Her hafta en az 3-5 yeni fotoğraf ve ayda 2-4 gönderi paylaşın.
- **Yorumlar:** Her tekliften sonra çifte yorum bağlantısını WhatsApp'tan gönderin. "Balon ev", "bungalov" gibi kelimeleri kendiliğinden kullanmaları sıralamaya yardımcı olur (yorum yazdırmak ya da ödül karşılığı istemek Google kurallarına aykırıdır).

## 7. Bağlantı (backlink) ve dijital PR

1. **The Vine ana sitesi** (`thevineorganizasyon.com.tr`): menüye ve evlilik teklifi bölümüne yeni siteye giden bağlantı ekleyin. En hızlı ve en değerli ilk bağlantı bu.
2. **Instagram ve YouTube** profil bağlantıları ve video açıklamaları → yeni site.
3. **Yerel basın:** Eskişehir'deki evlilik teklifleri İHA, DHA ve yerel gazetelerde düzenli olarak haber oluyor. Çiftin izniyle, ilginç teklifleri yerel muhabirlere fotoğraflarıyla iletin; haberde siteye bağlantı istemek değerli bir kazanç.
4. **Dizinler:** Armut, Düğün.com, Yandex Haritalar, Apple Haritalar, Bing Places. Her yerde aynı ad, adres, telefon.
5. **İş birlikleri:** Eskişehir'deki kuyumcular, çiçekçiler ve fotoğrafçılarla karşılıklı tavsiye sayfaları.

## 8. İçerik takvimi (ayda 2 yazı önerisi)

- 14 Şubat'ta evlilik teklifi: Eskişehir için fikirler (Ocak başında yayınlayın)
- Kışın evlilik teklifi: sıcak ve kapalı mekân önerileri
- Evlilik teklifinde ne giyilir? (her iki taraf için)
- Kız isteme ile evlilik teklifi arasındaki fark
- Teklif sonrası Eskişehir'de kutlama yemeği için öneriler
- Yıl dönümünde evlilik teklifi
- Her yeni teklif için galeriye fotoğraf ve kısa bir hikâye (çift izniyle)

## 9. Teknik özet (yapılanlar)

**Tasarım (v2):** Şarap kırmızısı, şampanya altını, fildişi ve gece siyahı; başlıklarda Cormorant Garamond, metinde Manrope. Tüm görseller kendi kurulumlarınızdan; çizimler kaldırıldı. Ana sayfa: tam ekran fotoğraflı giriş, fiyatlı konsept vitrini, paket kartları, Reels videosu, fotoğraf mozaiği. Konsept sayfalarında yanda sabit duran paket kartı (içerik, fiyat, WhatsApp).


- 30 dizine açık sayfa: ana sayfa, 3 konsept, süsleme, doğum günü ve yıl dönümü, 4 mekân (gondol, Sazova, Kanlıkavak, Gaga Restoran), mekanlar rehberi, hakkımızda, sürpriz teklif, fiyatlar, fiyat formu, 5 şehir (Kütahya/Tavşanlı, Bilecik, Bozüyük, Afyonkarahisar, Bursa/İnegöl), galeri, yorumlar, SSS, iletişim, blog ve 5 rehber yazı.
- Her sayfada ayrı başlık, açıklama, kanonik adres, Open Graph görseli (paylaşım kartı).
- Schema.org: LocalBusiness, Service, FAQPage, BreadcrumbList, BlogPosting, ImageObject, ImageGallery, VideoObject, TouristAttraction.
- Görsel arama: açıklayıcı dosya adları, alt metinler, WebP (800 ve 1600 px), görsel site haritası.
- Hız: çerçeve/kütüphane yok; ana sayfanın ilk yükü yaklaşık 250 KB (yazı tipleri hariç). Fotoğraflar tembel yükleniyor, video yalnızca oynatılınca iniyor.
- Mobil uyum, klavye erişimi, azaltılmış hareket desteği, mobilde sabit Ara / WhatsApp çubuğu.
- KVKK çerez bildirimi ve Google Consent Mode v2.

## 10. Anahtar kelime haritası (Google Trends verisiyle)

Kaynak: Google Trends, Türkiye, Kasım 2021 - Kasım 2026. Değerler 0-100 arası göreli ilgidir (100 = o listedeki en çok aranan); gerçek arama sayısı değildir.

**Temel bulgular**
- "Evlilik teklifi", "evlenme teklifi"nden yaklaşık iki kat fazla aranıyor. Ana kelime "evlilik teklifi"; "evlenme teklifi" her sayfada ikinci kelime olarak geçiyor.
- "Evlilik teklifi" ile ilgili en çok aranan konular: sözleri (100), organizasyon (94), yüzüğü (85), fikirleri (48), mekanları (30). "Evlenme teklifi" tarafında "edilecek yerler" (36) öne çıkıyor.
- Yükselen aramalar: evlilik teklifi pastaları, pozları, yüzüğü hangi parmağa / hangi ele takılır, evlilik teklifi organizasyonu.
- "Evlilik teklifi organizasyonu" aramasının en güçlü ilgili sorgusu: "evlilik teklifi organizasyonu fiyatları".
- Şehir + evlilik teklifi aramalarında Kütahya ve Bursa birbirine yakın, Afyon onların yaklaşık üçte ikisi. "Eskişehir evlilik teklifi" ve "Bilecik evlilik teklifi" Trends eşiğinin altında kalıyor (arama sayısı az ama alıcı niyeti çok yüksek). Bu yüzden yerel aramalarda asıl kazanç Google İşletme Profili ve harita sonuçlarından gelir.
- Bölgeye göre ilgi (nüfusa oranla): Bilecik 84, Bursa 83, Eskişehir 76, Kütahya 74, Afyonkarahisar 68.
- Mevsim: aramalar yaz aylarında (özellikle Haziran-Temmuz) zirve yapıyor, Şubat'ta 14 Şubat etkisiyle ikinci bir yükseliş var, Mart en düşük ay. Yeni içerikleri Ocak ve Mayıs başında yayınlamak en iyi zamanlama.

**Kelime → sayfa eşleştirmesi** (her kelime tek bir sayfayı hedefler, sayfalar birbiriyle yarışmaz)

| Arama | Niyet | Hedef sayfa |
|---|---|---|
| eskişehir evlilik teklifi, eskişehir evlilik teklifi organizasyonu, eskişehir evlenme teklifi, romantik / sürpriz / en iyi evlilik teklifi eskişehir | Hizmet | `/` (ana sayfa) |
| evlilik teklifi organizasyonu fiyatları, eskişehir evlilik teklifi fiyatları | Fiyat | `/evlilik-teklifi-fiyatlari/` |
| eskişehir evlilik teklifi mekanları, evlenme teklifi edilecek yerler | Mekân | `/evlilik-teklifi-mekanlari/` |
| balon ev evlilik teklifi | Hizmet | `/balon-ev-evlilik-teklifi/` |
| bungalovda evlilik teklifi | Hizmet | `/bungalov-evlilik-teklifi/` |
| karavanda evlilik teklifi, vosvos evlilik teklifi | Hizmet | `/karavan-evlilik-teklifi/` |
| evlilik teklifi süsleme, marry me harfleri, evlilik teklifi dekorasyonu | Hizmet | `/evlilik-teklifi-susleme/` |
| gondol evlilik teklifi | Mekân | `/gondolda-evlilik-teklifi/` |
| sazova evlilik teklifi | Mekân | `/sazova-parki-evlilik-teklifi/` |
| kanlıkavak evlilik teklifi, kanlıkavak iskele | Mekân | `/kanlikavak-parki-evlilik-teklifi/` |
| gaga evlilik teklifi, restoranda evlilik teklifi | Mekân | `/gaga-restoran-evlilik-teklifi/` |
| eskişehir doğum günü sürprizi, yıl dönümü sürprizi | Hizmet | `/ozel-gun-surprizleri/` |
| sürpriz evlilik teklifi, romantik evlilik teklifi | Hizmet/bilgi | `/surpriz-evlilik-teklifi/` |
| kütahya / tavşanlı evlilik teklifi | Yerel | `/kutahya-evlilik-teklifi/` |
| bilecik evlilik teklifi | Yerel | `/bilecik-evlilik-teklifi/` |
| bozüyük evlilik teklifi | Yerel | `/bozuyuk-evlilik-teklifi/` |
| afyon evlilik teklifi | Yerel | `/afyon-evlilik-teklifi/` |
| bursa / inegöl evlilik teklifi | Yerel | `/bursa-evlilik-teklifi/` |
| evlilik teklifi sözleri, evlenme teklifi sözleri | Bilgi (en yüksek hacim) | `/blog/evlilik-teklifi-sozleri/` |
| evlilik teklifi fikirleri, sade evlilik teklifi fikirleri, en güzel evlilik teklifi | Bilgi | `/blog/evlilik-teklifi-fikirleri/` |
| evlilik teklifi yüzüğü, yüzüğü hangi parmağa / ele takılır, yüzük ölçüsü | Bilgi | `/blog/evlilik-teklifi-yuzugu/` |
| evlilik teklifi nasıl yapılır, ne zaman edilir | Bilgi | `/blog/evlilik-teklifi-nasil-yapilir/` |
| evlilik teklifi çiçeği, pastaları, pozları | Bilgi (yükselen) | `/blog/evlilik-teklifi-cicegi-pastasi-pozlari/` |

Bilerek hedeflenmeyenler: "rüyada evlilik teklifi almak / görmek" (çok aranıyor ama rüya tabiri arayan kişi müşteri değil) ve ünlülerin teklif haberleri.

**Bilgi sayfalarının işi:** "Evlilik teklifi sözleri" gibi aramalar Türkiye genelinden çok trafik getirir. Bu sayfalar Eskişehir ve yakın illerdeki okuyucuyu konsept sayfalarına ve WhatsApp'a yönlendirir; ayrıca Google'ın siteyi "evlilik teklifi" konusunda uzman görmesini sağlar.

## 11. Gerçekçi beklenti

Google'da ilk sıra kimse tarafından garanti edilemez. "Balon ev evlilik teklifi Eskişehir", "Bozüyük evlilik teklifi" gibi rakibi az aramalarda birkaç hafta içinde görünmeye başlamak mümkün. "Eskişehir evlilik teklifi" gibi ana aramalarda kalıcı üst sıralar; İşletme Profili, düzenli yorum, ana siteden bağlantı ve basın haberleriyle genellikle 3-6 ay içinde oluşur.

## 12. Siteyi güncellemek

**Fiyatlar, paket içerikleri, fotoğraflar ve yorumlar:** yönetim panelinden (`/admin/`). Kullanımı `YONETIM-PANELI.md` dosyasında. Panel bu bilgileri `veri/` klasöründeki dosyalarda tutar (`paketler.json`, `galeri.json`, `gorseller.json`, `yorumlar.json`); her kayıttan sonra Netlify siteyi `python3 build.py` ile yeniden üretir.

**Sayfa yazıları ve tasarım:** `content.py` (sayfa metinleri), `build.py` (şablonlar, iletişim bilgileri, videolar) ve `assets/site.css`. Bunlar için bana yazmanız yeterli.

**Videolar:** `build.py`'deki `VIDEOS` sözlüğü. Yeni bir video için mp4 ve kapak görselini `assets/video/` içine koyup bir satır eklenir.
