# 06 — Arayüz: Sadelik Doktrini, Ekran Envanteri ve Karmaşıklık Bütçesi

> Uzman: Ürün Tasarımcısı (Sadelik Doktrini)
> Durum: v1 tasarım — arkadaki 13 belgenin derinliği bu belgede **gizlenir**.
> Sorumlu olduğum doktrin kuralları: **1 (bir ekran = bir karar)** ve **4 (günlük plan tek satır)**.

## 3 cümlelik özet

BookBeast'in tamamı **beş yüzeyden** ibarettir — Bugün, Kitap Brifingi, Atom Kartı, Defter, Kütüphane — ve bunlardan yalnızca ilki her gün açılır; geri kalan her şey (13 uzmanın motoru, 19 ilişki tipi, dört eksenli epistemik durum, önkoşul DAG'ı) kullanıcıya hiçbir zaman doğrudan gösterilmez, yalnızca tek bir cümlenin gerekçesine dönüşür. **Fikir haritası grafiği çizilmeyecek**: graf görselleştirmeleri 50 düğümden sonra okunamaz spagettiye döner ve kullanıcının sorusu asla "graf neye benziyor" değil, "bu fikir nereye bağlanıyor" olduğu için yerine **tek kart + en fazla üç kapı** (iz sürme) düzeni gelir. Ürünün gelecekteki şişmesine karşı tek savunma §9'daki **karmaşıklık bütçesidir**: her ekranın sabit bir eleman puanı tavanı vardır, tavan asla yükseltilemez ve yeni bir şey eklemenin tek yolu eşdeğerini silmektir.

---

## 0. Tasarım anayasası — beş kural

Doktrin 1 ve 4'ü işletilebilir hâle getiren beş kural. Bunlar tasarım tercihi değil, kabul kriteridir.

| # | Kural | İşletilebilir ölçüt |
|---|---|---|
| A1 | **Bir ekran = bir karar** | Ekranda **1** birincil eylem, **1** derinlik şeridi (≤3 homojen kapı), **≤2** sessiz kaçış (geri / ertele). Sayım: birincil=1, şerit=1, kaçış=0. Toplam ≤ 3. |
| A2 | **Günlük plan tek satır** | Bugün ekranının plan bloğu **tek cümle**: 1 kitap + 1 sayfa aralığı + 1 süre. İkinci bir kitap asla aynı ekranda görünmez. |
| A3 | **Sessizlik varsayılandır** | İyi haber gösterilmez. Rozet, sayaç, yüzde, ilerleme çubuğu ancak kullanıcının kararını değiştiriyorsa görünür. |
| A4 | **Derinlik bir tık ötede, asla önde** | Her tık **en fazla bir katman** açar. Aynı anda **tek** katman-1 bloğu açık kalır (akordeon dışlayıcıdır). |
| A5 | **Metin arayüzdür** | Görsel bileşen değil, cümle tasarlanır. Cümle uzunluk tavanı: 25 kelime. Ekranda cümle tavanı: 3. |

**Yasak listesi (kalıcı):** sekme (tab), kenar çubuğu menüsü, gösterge paneli (dashboard), okuma serisi/streak, ilerleme rozeti, karşılama turu (onboarding tour), modal içinde modal, sonsuz akış (infinite feed), graf görselleştirmesi.

---

## 1. Ekran envanteri

### 1.1 Karar: 6 aday → 5 yüzey, biri silindi

| Aday | Karar | Gerekçe |
|---|---|---|
| Bugün | **Kalır** — karar ekranı | Uygulamanın kalbi. Günde bir kez açılan tek yüzey. |
| Kitap Brifingi | **Kalır** — karar ekranı | Doktrin 3'ün (sıkıştırma) yaşadığı yer. Hüküm burada verilir. |
| Fikir Haritası | **SİLİNDİ** | §4. Yerine Atom Kartı geldi. |
| Atom Kartı | **Eklendi** — karar ekranı | Fikir haritasının yerine geçen gezinme birimi. Yeni ekran değil, silinenin yerini alan. |
| Açık Sorular Defteri | **Kalır** — geçit + karar | Transferin girdisi. Bu olmadan ürün bir özetleyiciye düşer. |
| Kütüphane | **Kalır** — yalnız geçit | Kitaba erişmenin tek yolu. İçinde okunacak içerik yok. |
| Yükleme | **Ekran değil** — durum | §5. Kütüphane içinde yaşayan bir satır + bir bekleme durumu. |

**Ayrıca silinenler:** Ayarlar ekranı (→ hesap çekmecesinde 5 satır), Arama ekranı (→ masaüstünde komut paleti, mobilde Kütüphane başlığındaki alan), İstatistikler (→ kalıcı yasak, §9).

### 1.2 Yüzey sözleşmeleri

| Yüzey | Tek amacı | Maksimum bilgi | Kullanıcının tek kararı |
|---|---|---|---|
| **Bugün** | Bugün ne okunacağını ve nedenini söylemek | 1 kitap · 1 sayfa aralığı · 1 gerekçe cümlesi · 1 okuma emri | Başlıyorum / bugün olmaz |
| **Kitap Brifingi** | Yeni kitabın hükmünü vermek | Katman 0'da: 1 hüküm + 1 sayfa aralığı + 1 transfer sayısı | Bu sayfaları plana al / alma |
| **Atom Kartı** | Tek bir fikri ve gideceği 3 yeri göstermek | 1 iddia · 1 çapa · 3 kapı | Hangi kapıdan gireceğim / deftere bağlayacağım |
| **Defter** | Açık soruları tutmak ve beslemek | Soru listesi (≤ 12 aktif) | Soru ekle / kapat |
| **Kütüphane** | Kitaba ulaşmak | Kitap listesi + durum satırı | Hangi kitabı açacağım |

**Sınıf ayrımı:** *Karar ekranı* (Bugün, Brifing, Atom Kartı) A1'e tabidir. *Geçit* (Defter, Kütüphane) bir listedir, karar taşımaz, okunacak içerik barındırmaz. Sistemde **en fazla 2 geçit** olabilir. Üçüncüsü teklif edilirse cevap hayırdır.

---

## 2. "Bugün" ekranı — kalbin tam metni

### 2.1 Eleman sayımı

| # | Eleman | Kelime tavanı |
|---|---|---|
| 1 | Plan satırı (kitap + sayfa + süre) | 12 |
| 2 | Gerekçe (neden bu, neden bugün) | 25 |
| 3 | Okuma emri (tek somut eylem) | 15 |
| 4 | Birincil buton | 1 |
| 5 | Sessiz kaçış (ertele) | 2 |

**Toplam: 5 eleman, ≤ 55 kelime, 1 birincil eylem.** Selamlama yok, tarih yok, hava durumu yok, ilerleme yüzdesi yok, "5 günlük seri" yok.

### 2.2 Wireframe (gerçek metin)

```
┌──────────────────────────────────────────────────────────────┐
│                                                          ⋯   │
│                                                              │
│   Bugün: Konveks Optimizasyon — s. 214–226.                  │
│   13 sayfa, yaklaşık 35 dakika.                              │
│                                                              │
│   Defterindeki "ölçüm gürültüsünü nasıl bastırırım?"         │
│   sorusuna bu 13 sayfadaki dualite argümanı doğrudan         │
│   cevap veriyor. Kütüphanende bu argümanın başka             │
│   örneği yok.                                                │
│                                                              │
│   Okurken tek şeyi ara: s. 218'deki eşitsizliğin senin       │
│   sensör modelindeki karşılığı ne?                           │
│                                                              │
│                                                              │
│            ┌────────────────────────────┐                    │
│            │          Başla             │                    │
│            └────────────────────────────┘                    │
│                                                              │
│                     bugün olmaz                              │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

`⋯` menüsü: Kütüphane · Defter · Hesap. Üç satır, başka bir şey yok. Gezinme menüsü sürekli görünür bir çubuk değildir — Bugün ekranı gezinmeden arınmıştır.

### 2.3 "Başla" ne yapar?

Kitabı **çıplak bir görüntüleyicide** s. 214'ten açar. Görüntüleyicide vurgulama yok, not yok, araç çubuğu yok — tek bir buton var: **Bitirdim**. *BookBeast bir okuyucu uygulaması değildir;* görüntüleyici bir geçittir, özellik değildir (§9 kural 2).

### 2.4 Kapanış — günün tek yakalama anı

`Bitirdim` → tek soru, tek ekran:

```
┌──────────────────────────────────────────────────────────────┐
│   Bu 13 sayfa "ölçüm gürültüsünü nasıl bastırırım?"          │
│   sorunu değiştirdi mi?                                      │
│                                                              │
│      [ Evet — defteri güncelle ]        hayır                │
└──────────────────────────────────────────────────────────────┘
```

"Evet" → Defter'de o sorunun altına tek satırlık bir alan açılır. Bu, üründeki **tek** not alma yüzeyidir. Genel amaçlı not defteri yoktur ve olmayacaktır.

### 2.5 Bugün planı nasıl seçilir? (arayüz açısından)

Arka planda transfer motoru (07) bir sıra üretir. Arayüzün tek kuralı: **sıranın yalnızca ilk elemanı gösterilir.** "İkinci seçenek" düğmesi yoktur; "bugün olmaz" denirse sıradaki gelir ve o da tek başına gösterilir. Kullanıcı asla iki plan arasında karşılaştırma yapmaz — karşılaştırma karar değil, kaygıdır.

---

## 3. Kitap Brifingi — kademeli açılım (progressive disclosure)

### 3.1 Üç katmanlı düzen

| Katman | Ne var | Nasıl açılır | Kelime tavanı |
|---|---|---|---|
| **K0** | Hüküm + sayfa aralığı + transfer sayısı + 1 eylem | Varsayılan | 55 |
| **K1** | 3 blok: *Ne bulundu* · *Neyle çelişiyor* · *Deftere ne dokunuyor*. Her blok 1 özet satırı + ≤5 başlık. | Şeritteki kapıya tık. **Aynı anda tek blok açık.** | blok başına 120 |
| **K2** | Atom Kartı / Çatışma Kartı (tam nesne) | K1'deki başlığa tık | §4, §6.5 (belge 01) |
| **K3** | Kaynak sayfa görüntüsü + vurgulanan aralık | Atom Kartındaki çapaya tık | — |

**Kural (A4):** K0'dan K3'e tek tıkla atlanamaz. Her tık bir katman. Geri tuşu tam olarak bir katman kapatır.

### 3.2 K0 wireframe

```
┌──────────────────────────────────────────────────────────────┐
│  ←  Konveks Optimizasyon · Boyd & Vandenberghe               │
│                                                              │
│                                                              │
│   Bu kitabın %94'ü zaten kütüphanende — beş ayrı kitaptan.   │
│   Geri kalan %6 tek yerde toplanmış: Bölüm 7, 11 sayfa.      │
│   s. 214–226.                                                │
│                                                              │
│   Bu 11 sayfa defterindeki 2 soruya dokunuyor.               │
│                                                              │
│            ┌────────────────────────────┐                    │
│            │    Bugünün planına al      │                    │
│            └────────────────────────────┘                    │
│                                                              │
│   ──────────────────────────────────────────────────────     │
│   Ne bulundu ▾      Neyle çelişiyor ▾      Deftere ▾         │
└──────────────────────────────────────────────────────────────┘
```

Sayım (A1): birincil eylem 1 + derinlik şeridi 1 + geri (kaçış, sayılmaz) = **2 ≤ 3**. ✓

### 3.3 K1 açık hâli — "Neyle çelişiyor"

```
│   Ne bulundu ▸      Neyle çelişiyor ▾      Deftere ▸         │
│   ──────────────────────────────────────────────────────     │
│                                                              │
│   Kütüphanendeki 3 iddiayla çakışıyor. İkisi kapsam farkı    │
│   (ikisi de doğru), biri gerçek çelişki.                     │
│                                                              │
│   ⇄  Dualite boşluğu her konveks problemde sıfırdır          │
│      Sayısal Yöntemler, s. 88 ile karşı karşıya              │
│                                                              │
│   ·  Yakınsama hızı adım büyüklüğünden bağımsızdır           │
│      koşul farkı — ikisi de geçerli                          │
│                                                              │
│   ·  Slater koşulu gerekli değildir                          │
│      koşul farkı — ikisi de geçerli                          │
│                                                              │
```

Diğer iki blok başlığı kapanır (`▸`) ama yerinde durur — kullanıcı nerede olduğunu kaybetmez. Blok içinde **en fazla 5 satır**; fazlası varsa son satır: `+7 tane daha` (tek tık, aynı blok içinde uzar, yeni ekran açmaz).

### 3.4 K0 hükmünün cümle kalıbı (doktrin 3 — reddetme yok, sıkıştırma var)

```
"Bu kitabın %{örtüşme} zaten kütüphanende — {n} ayrı kitaptan.
 Geri kalan %{yenilik} {dağılım}: {yer}, {sayfa} sayfa. s. {a}–{b}.
 Bu {sayfa} sayfa defterindeki {k} soruya dokunuyor."
```

`{dağılım}` iki değerden birini alır: *"tek yerde toplanmış"* veya *"kitaba dağılmış"*. İkinci durumda sayfa aralığı yerine bölüm listesi gelir (≤3 bölüm).

**Sınır durumu — %100 örtüşme:** Sistem yine "okuma" demez. Metin: *"Yeni fikir bulamadım. Ama Bölüm 3, kütüphanendeki en dağınık konuyu tek bir anlatıda topluyor — 9 sayfa. Pekiştirme için değer."* Eylem butonu kalır, adı değişir: **Pekiştirme olarak al.**

---

## 4. Fikir haritası — karar: **graf çizilmeyecek**

### 4.1 Gerekçe

1. Kullanıcının gerçek sorusu hiçbir zaman "graf neye benziyor" değildir; "bu fikir nereye bağlanıyor" veya "buna kim karşı çıkıyor"dur. İkisi de yerel sorulardır, küresel bir resim gerektirmez.
2. Bir kitap ~300–800 atom üretiyor (belge 01, §3.5). 10 kitapta 5.000 düğüm. Kuvvet-yönlü yerleşim (force-directed layout) bu ölçekte kıl yumağıdır; filtre eklemek ise ekrana 6 kontrol getirir → A1 ihlali.
3. Graf, kullanıcıya *sistemin* yapısını gösterir. Kullanıcı sistemin yapısını umursamaz.

### 4.2 Yerine ne geliyor: **iz sürme** (tek kart, üç kapı)

Her an ekranda **bir** atom vardır ve ondan **en fazla üç** çıkış. 19 ilişki tipi kullanıcıya asla gösterilmez; sabit üç yuvaya indirgenir:

| Yuva | Etiket (kullanıcı diliyle) | Kaynak ilişki | Boşsa yerine |
|---|---|---|---|
| 1 | **Önce şu lazım** | `PREREQUISITE_OF` (yalnız kullanıcıda eksikse) | `DEFINES` |
| 2 | **Buna karşı çıkan** | `CONTRADICTS` / `REFUTES` | `QUALIFIES` |
| 3 | **Başka alandaki eşi** | `ANALOGOUS_TO` | `APPLIES_TO` |

Üçüncü yuva ürünün sihridir: çapraz-alan sıçraması burada görünür hâle gelir. Üçü de boşsa kart kapısız gösterilir — boş kapı yuvası çizilmez.

### 4.3 İz kuralları

- **Kırıntı (breadcrumb) en fazla 5 adım.** 6. adımda ilk adım düşer ve üstte tek satır kalır: `Bölüm 7 → dualite → titrasyon → …`
- **Döngü engeli:** izde daha önce görülmüş atom kapı olarak gösterilmez.
- **Çıkış her zaman tek tık:** kırıntının en soluna dönüş.

### 4.4 Atom Kartı wireframe

```
┌──────────────────────────────────────────────────────────────┐
│  ←  Bölüm 7 → dualite                                        │
│                                                              │
│   Güçlü dualite, Slater koşulunu sağlayan konveks            │
│   problemlerde dualite boşluğunu sıfırlar.                   │
│                                                              │
│   Konveks Optimizasyon · s. 226                              │
│                                                              │
│   ─────────────────────────────────────────────────────      │
│                                                              │
│   Önce şu lazım                                              │
│   → Slater koşulu nedir · aynı kitap, s. 197                 │
│                                                              │
│   Buna karşı çıkan                                        ⇄  │
│   → Sayısal Yöntemler, s. 88                                 │
│                                                              │
│   Başka alandaki eşi                                         │
│   → Titrasyonda durma kuralı · Klinik Farmakoloji, s. 141    │
│                                                              │
│                    [ Deftere bağla ]                         │
└──────────────────────────────────────────────────────────────┘
```

### 4.5 Tek istisna: önkoşul çubuğu

Önkoşul DAG'ı (doktrin 7) **graf olarak çizilmez**; topolojik sıralaması alınıp **numaralı liste** olarak gösterilir. Yalnızca masaüstünde, yalnızca Kitap Brifingi K1 içinde:

```
Bölüm 9'a hazır olmak için sıra:
1. Ölçü teorisi temelleri   — Analiz II, s. 61–78      ✓ okundun
2. Lebesgue integrali        — Analiz II, s. 112–140    ✓ okundun
3. Lp uzayları               — Fonksiyonel Analiz, s. 44 ← buradasın
4. Bölüm 9
```

Liste graf değildir: dallanma yoktur, tek yol gösterilir (en kısa hazırlık yolu). Alternatif yollar gizlenir.

---

## 5. Yükleme akışı — 20 dakikalık bekleme

### 5.1 Temel karar: kullanıcı beklemez, gider. Tasarım buna göre yapılır.

Amaç "bekleme ekranını eğlenceli kılmak" değil, **beklemeyi gereksiz kılmaktır.** Üç mekanizma:

1. **20 saniyede ön hüküm.** İçindekiler + bölüm başlıkları + ilk geçiş taramasıyla anında bir yargı verilir. Kullanıcı ilk 20 saniyede değer alır.
2. **Sekme kapatılabilir.** İşlem sunucuda sürer. Bu, ekranda açıkça yazılır — belirsizlik terk ettirir, iş yükü değil.
3. **Bitince tek bildirim.** Tarayıcı bildirimi veya e-posta. Kullanıcı seçer; varsayılan açık.

### 5.2 Yüzde yerine ad ve sayaç

İlerleme çubuğu ve yüzde **gösterilmez** (yanlış tahmin güveni öldürür). Yerine: **aşama adı + canlı sayaç + tahmini bitiş saati.**

| Aşama | Ekranda görünen | Tipik süre |
|---|---|---|
| 1 | Metin çıkarıldı · 612 sayfa | 40 sn |
| 2 | Fikir atomları çıkarılıyor · 312 atom, Bölüm 4 | 9 dk |
| 3 | Kütüphanenle karşılaştırılıyor · 5 kitap taranıyor | 5 dk |
| 4 | Defterine eşleniyor · 4 sorun kontrol ediliyor | 3 dk |
| 5 | Hüküm yazılıyor | 90 sn |

### 5.3 Bekleme wireframe

```
┌──────────────────────────────────────────────────────────────┐
│  Konveks Optimizasyon                                        │
│                                                              │
│  İlk bakış: 6 bölümün 2'si defterindeki sorulara değiyor.    │
│  Tam hüküm yaklaşık 14:35'te hazır.                          │
│                                                              │
│  Şu an: fikir atomları çıkarılıyor — 312 atom, Bölüm 4       │
│                                                              │
│  ─────────────────────────────────────────────────────       │
│  Yol boyunca bulunanlar                                      │
│  · s. 88'deki bir iddia kütüphanendekiyle çakışıyor          │
│  · Bölüm 7, kütüphanende hiç karşılığı olmayan tek bölüm     │
│                                                              │
│  Sekmeyi kapatabilirsin, işlem devam eder.                   │
│                                                              │
│                  [ Bitince haber ver ]                       │
└──────────────────────────────────────────────────────────────┘
```

- "Yol boyunca bulunanlar" **en fazla 3 satır**, tıklanamaz, kaybolmaz. Bunlar beklemeyi ödüle çevirir.
- Birden fazla kitap yüklenirse ekran değişmez; üstte tek satır: `Sırada 2 kitap daha.` Kuyruk ekranı yoktur.
- **Hata durumu:** "Bu PDF'in 40–95. sayfaları taranmış görüntü; metin çıkaramadım. Kalan 517 sayfayla devam ettim." — hata bir uyarı kutusu değil, bir cümledir.

---

## 6. Güven etiketleri — 9 rozet → 3 görünür işaret

### 6.1 Karar: iyi haber gösterilmez

Belge 01 §5.3 dokuz rozet tanımlıyor. Dokuzunu da göstermek ekranı rozet çöplüğüne çevirir ve daha kötüsü: her cümleye rozet koymak **hiçbir rozetin okunmaması** demektir. Kural: **sessizlik güvenilirlik anlamına gelir.**

| Belge 01 rozeti | Arayüzde |
|---|---|
| Kanıtlanmış · Sağlam · Destekli | **Hiçbir şey.** Sistem arkanda. |
| Zayıf · Spekülatif · Değerlendirilmedi | `doğrulanamadı` — gri, küçük, cümle sonunda |
| Tartışmalı · Çürütülmüş | `⇄` — kehribar, tıklanabilir → Çatışma Kartı |
| Yazarın görüşü | Rozet değil, **tipografi**: cümle italik ve tırnak içinde |

Üç görünür işaret. Biri rozet bile değil.

### 6.2 Yerleşim kuralları

1. İşaret **cümlenin sonunda**, gövde renginin %60 opaklığında, gövdeden bir punto küçük. Renkli kutu yok, kenarlık yok, ikon seti yok.
2. **Yeşil asla kullanılmaz.** Yeşil rozet, rozet çiftliğinin ilk adımıdır.
3. **Kırmızı yalnızca sistem hatası içindir**, epistemik durum için değil. Çürütülmüş bir iddia kullanıcının hatası değildir.
4. **Ekranda en fazla 2 işaret.** Üçüncüsünden itibaren hepsi toplanır ve ekranın altında tek satır olur:
   `Bu brifingdeki 5 iddiayı doğrulayamadım. [göster]`
5. `⇄` işareti taşıyan cümle tıklanabilir; tıklanınca Çatışma Kartı (belge 01 §6.5) açılır. Bu, `⇄`'nin tek işlevidir.
6. **Ton kuralı:** etiket kullanıcıyı değil sistemi suçlar. "Doğrulanamadı" değil de mümkünse "doğrulayamadım" — özne sistemdir.

### 6.3 Nerede zorunlu, nerede yasak

| Yer | Kural |
|---|---|
| Bugün ekranı gerekçesi | **İşaret yasak.** Gerekçe cümlesi yalnızca doğrulanmış atomlardan kurulur; kurulamıyorsa o kitap bugüne seçilmez. |
| Kitap Brifingi K0 | **İşaret yasak.** Hüküm cümlesi hep güvenli. |
| K1 blokları, Atom Kartı | **İşaret zorunlu** (varsa). |
| `verification = symbolic_fail` atom | Her yerde zorunlu `doğrulanamadı`; Bugün planına asla girmez. |

Bu, "yanlış özetlenen teorem zehirlidir" kuralının arayüz karşılığıdır: **zehirli olabilecek şey ön ekrana çıkamaz.**

---

## 7. Boş durumlar ve ilk 5 dakika

### 7.1 Karar: defter kitaptan önce gelir

Kullanıcıdan ilk istenen şey kitap değil, **bir soru**. Sebep: transfer motoru defter olmadan çalışamaz ve ilk kitap brifingi transfersiz verilirse kullanıcı ürünü "özetleyici" sanar — geri dönüşü olmayan bir yanlış izlenim.

### 7.2 Dakika 0 — tek alan

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│   Şu an hangi problemin üstünde çalışıyorsun?                │
│                                                              │
│   ┌────────────────────────────────────────────────────┐     │
│   │                                                    │     │
│   └────────────────────────────────────────────────────┘     │
│                                                              │
│   Örnekler — dokun, düzenle:                                 │
│   "ölçüm gürültüsünü nasıl bastırırım?"                      │
│   "bir sistemin kararlı olduğunu nasıl anlarım?"             │
│   "iyi bir karar nedir?"                                     │
│                                                              │
│                     ┌──────────────┐                         │
│                     │    Devam     │                         │
│                     └──────────────┘                         │
│                                                              │
│   Kitap istemeden önce bunu soruyorum: bu uygulama           │
│   kitapları senin sorularına göre okuyor.                    │
└──────────────────────────────────────────────────────────────┘
```

Bir soru yeter. "En az üç soru gir" gibi bir kapı **yoktur** — kapılar terk ettirir.

### 7.3 İlk 5 dakikanın tamamı

| Süre | Ekran | Kullanıcının işi |
|---|---|---|
| 0:00 | Tek soru alanı | 1 soru yazar |
| 0:20 | "İyi. Şimdi bir kitap." + sürükle-bırak alanı | Dosya seçer |
| 0:40 | Ön hüküm belirir | Okur, hiçbir şey yapmaz |
| 1:00 | Bekleme ekranı + "Yol boyunca bulunanlar" | İsterse 2. soru ekler (tek satır alan altta) |
| 1:00–20:00 | Uygulamayı kapatabilir | — |
| ~20:00 | Bildirim: "Konveks Optimizasyon hazır. %94'ü zaten sende." | Brifingi açar |

### 7.4 Boş durum kalıbı: **bir cümle + bir eylem**

Boş durum bir reklam panosu değil, **bir sorudur**. Ne çizim, ne özellik turu, ne kontrol listesi.

| Nerede boş | Ekranda görünen | Eylem |
|---|---|---|
| Kütüphane | "Henüz kitap yok." | `Kitap yükle` |
| Defter | "Defterin boş. Bir kitap ne için okunur?" | `Soru ekle` |
| Bugün — kitap yok | "Önce bir kitap lazım." | `Kitap yükle` |
| Bugün — soru yok | "Neyin üstünde çalıştığını bilmezsem sana kitap değil, özet veririm." | `Soru ekle` |
| Bugün — plan bitti | "Bugünlük bu kadar. Yarın devam." | *(eylem yok — bitmiş olmak bir durumdur, boşluk değil)* |
| Kitap Brifingi — transfer yok | "Bu kitap defterindeki sorulara değmiyor. Ama Bölüm 4'te hiç görmediğin 7 sayfa var." | `Yine de al` |

"Bugünlük bu kadar" ekranının eylemsiz olması bilinçlidir: kullanıcıyı uygulamada tutmaya çalışmıyoruz.

---

## 8. Mobil

### 8.1 Sınıflandırma

| Sınıf | Yüzey | Neden |
|---|---|---|
| **Birinci sınıf** — mobilde kusursuz | Bugün · Kitap Brifingi K0–K1 · Defter (okuma + tek satır soru ekleme) · Bekleme durumu ve bildirim | Kullanıcı bunları sırada, yolda, yatakta açar. Günlük temas noktası bunlar. |
| **İkinci sınıf** — çalışır, optimize edilmez | Atom Kartı ve iz sürme · Kütüphane · Çatışma Kartı | Ara sıra gerekir; dar ekranda kullanılabilir ama keyifli olmak zorunda değil. |
| **Masaüstüne bırakılır** | Dosya yükleme · K3 kaynak sayfa görüntüsü · önkoşul çubuğu · komut paleti/arama · dışa aktarma · hesap ayarları | Hepsi masa başı işi. Mobilde bunlar için tek satır: "Bunu bilgisayarda yap." |

### 8.2 Mobil kuralları

1. **Ekranın alt %25'i başparmak bölgesi**: birincil eylem hep orada, hep tam genişlik.
2. Mobilde **K2 akordeon değil, tam sayfadır** (push + geri). Dar ekranda akordeon iki katman derinlikte konum kaybettirir. K1 akordeon kalır.
3. Atom Kartında mobilde **kapılar dikey**, birer satır; yatay şerit yok.
4. Ekran başına **1 birincil eylem**, istisnasız. İkinci butonu olan mobil ekran tasarım hatasıdır.
5. **Yatay kaydırma yok.** Hiçbir yerde. Yatay kaydırılan liste, keşfedilmeyen listedir.
6. Bugün ekranı mobilde **tek ekrana sığar** — dikey kaydırma bile olmaz. Sığmıyorsa metin uzundur, ekran değil.

---

## 9. ⚠️ Karmaşıklık bütçesi

Bu bölüm projenin gelecekteki şişmesine karşı tek savunmadır. Diğer her bölüm tavsiyedir; bu bölüm **kuraldır**.

### 9.1 Para birimi: eleman puanı (EP)

| Eleman | EP |
|---|---|
| Metin bloğu (başlık, cümle, satır) | 1 |
| Etkileşimli kontrol (buton, bağlantı, alan, akordeon başlığı) | 2 |
| Liste | 1 + (görünen satır × 0,5) |
| Görünür işaret / rozet | 1 |
| Herhangi bir görsel, grafik, çizim | 3 |
| Sürekli görünen gezinme öğesi | 4 |

Son satır bilinçli olarak cezalıdır: kalıcı gezinme çubuğu, sadeliğin en yaygın sessiz katilidir.

### 9.2 Ekran bütçeleri (sabit — asla yükseltilmez)

| Yüzey | EP tavanı | Kelime tavanı | Birincil eylem | A1 seçenek sayımı |
|---|---|---|---|---|
| Bugün | **14** | 55 | 1 | 2 |
| Kapanış sorusu | **8** | 30 | 1 | 2 |
| Kitap Brifingi K0 | **14** | 55 | 1 | 2 |
| Kitap Brifingi K1 (açık) | **34** | 175 | 1 | 3 |
| Atom Kartı | **18** | 80 | 1 | 3 |
| Bekleme durumu | **12** | 60 | 0–1 | 1 |
| Defter (geçit) | **22** | — | 1 | 2 |
| Kütüphane (geçit) | **20** | — | 1 | 2 |
| Boş durum (her biri) | **6** | 25 | 1 | 1 |

**Toplam yüzey sayısı tavanı: 5** (+ görüntüleyici + kapanış sorusu, ikisi de yüzey sayılmaz çünkü tek butonludur).

### 9.3 Ekleme kuralları — yeni özellik isteyeni ne durdurur?

| # | Kural | Nasıl işler |
|---|---|---|
| 1 | **Sıfır toplam (zero-sum)** | Bir ekrana EP eklemek için aynı ekrandan eşdeğer EP çıkarmak zorunludur. Tavan yükseltilemez. Bu, ürünün ömrü boyunca geçerlidir. |
| 2 | **Yeni yüzey = eski yüzeyin ölümü** | Altıncı yüzey ancak beşinden biri silinerek eklenir. "Küçük bir ekran daha" diye bir şey yoktur. |
| 3 | **Üç soru testi** | (a) Bu, kullanıcının **bugün** vereceği kararı değiştiriyor mu? (b) Göstermezsek kullanıcı bir **hata** yapar mı? (c) Bunu mevcut bir elemanın **içine** gizleyebilir miyiz? — (a) ve (b) hayırsa özellik reddedilir. (c) evetse gizlenir, eklenmez. |
| 4 | **Sekme yasağı** | Sekme, karmaşıklığı ölçüme girmeden saklamanın adıdır. Sekmeye ihtiyaç duyulması, özelliğin fazla olduğunun kanıtıdır. |
| 5 | **Ayar tavanı: 5** | Toplam ayar sayısı 5'i geçemez (hesap · bildirim · veri dışa aktarma · tema · dil). Yeni ayar isteği = "varsayılanı seçemedik" itirafıdır. Varsayılanı seç. |
| 6 | **Sayı gerekçesi** | Ekrandaki her sayı için "kullanıcı bununla ne yapacak?" sorusu cevaplanmalı. Cevaplanamayan sayı silinir. |
| 7 | **Kalıcı yasak listesi** | Gösterge paneli, okuma serisi (streak), okunan sayfa grafiği, rozet/başarım, sosyal paylaşım, sohbet arayüzü, yapay zekâ asistanı balonu. Bunlar tartışmaya açılmaz. |
| 8 | **Bildirim tavanı: günde 1** | (Bugünün planı hazır.) İşlem bitti bildirimi kullanıcı açıkça istediyse +1. Toplam en fazla 2. |
| 9 | **Cümle tavanı** | Hiçbir arayüz cümlesi 25 kelimeyi geçemez; hiçbir karar ekranında 3'ten fazla cümle olamaz. |
| 10 | **30 günlük deneme süresi** | Yeni her eleman `geçici` etiketiyle girer. 30 gün sonunda kullanım oranı %20'nin altındaysa **otomatik silinir**, tartışma açılmaz. |
| 11 | **Bütçe bekçisi** | Her arayüz değişikliği §9.2 tablosunu günceller. Tablo aşılmışsa değişiklik birleştirilmez (merge edilmez). Tablo bu belgededir; belge kaynak koddur. |

### 9.4 Karşı-örnek: reddedilen üç makul öneri

| Öneri | Neden makul görünüyor | Neden reddedildi |
|---|---|---|
| "Bugün ekranına ikinci bir öneri koyalım, kullanıcı seçsin" | Esneklik | Doktrin 4 ihlali. İki plan = karşılaştırma = kaygı. Kullanıcı "bugün olmaz" der, sıradaki gelir. |
| "Kitap brifinginde tam bölüm listesi olsun" | Şeffaflık | K0'ı 55'ten ~200 kelimeye çıkarır. K1'e ait, K0'a değil. |
| "Okuma istatistikleri sekmesi ekleyelim" | Motivasyon | Kural 4 + kural 7. Ayrıca hiçbir sayı okuma kararını değiştirmez. |

---

## 10. Açık sorular

- `AÇIK SORU:` Kullanıcının kitabı BookBeast dışında (kâğıttan, Kindle'dan) okuduğu durumda "Bitirdim" akışı nasıl tetiklenir? Şu anki tasarım gömülü görüntüleyiciyi varsayıyor. Aday çözüm: Bugün ekranındaki `⋯` altında tek satır — "kendi kitabımdan okudum" — ama bu, bir EP daha demek.
- `AÇIK SORU:` Kullanıcı 12'den fazla açık soru tutmak isterse ne olur? Şu anki tavan 12 aktif soru; fazlası arşive düşer. Tavanın doğru sayı olduğu doğrulanmadı — belge 07 (transfer) bu sayıya duyarlı olabilir.
- `AÇIK SORU:` Bugün planı üst üste 5 gün "bugün olmaz" alırsa sistem ne yapar? Sessizce sıraya devam mı, yoksa tek bir soru mu sorar ("plan yanlış mı?")? İkincisi daha doğru görünüyor ama yeni bir ekran demek — kural 2'ye takılıyor.
- `AÇIK SORU:` Görüntüleyicinin DRM'li veya taranmış (görüntü) PDF'lerdeki davranışı belge 04'ün (mimari) kararına bağlı; arayüz tarafında yalnızca §5.3'teki hata cümlesi tasarlandı.
