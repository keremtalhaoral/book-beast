# 04 — Sistem Mimarisi: Kitaptan Fikir Atomuna Boru Hattı

> Kıdemli Sistem Mühendisi · Katman 1'in (SİNDİRİM) mühendisliği ve uygulamanın iskeleti

---

## 3 cümlelik özet

Kitap dosyası, **11 aşamalı, içerik-adresli (content-addressed) ve idempotent bir boru hattından** geçer: alım → normalleştirme → yapı tespiti → blok sınıflandırma → matematik çıkarımı → eleme → parçalama → atom çıkarımı → çapa doğrulama → bağlantı → yayın; her aşama diske bir *eser* (artifact) yazar, bu yüzden çöken bir aşama sadece kendini tekrarlar, kitabı sıfırlamaz.
LLM çağrıları **kademelidir**: geniş geçiş Sonnet 5, teorem/formül yoğun parçalar ve transfer yargısı Opus 5, mekanik sınıflandırma Haiku 4.5 — dijital doğumlu 400 sayfalık bir kitap **~15 dakikada ve ~3 dolara**, taranmış bir kitap ~60 dakikada ve ~4,5 dolara sindirilir.
Kısmi başarısızlık **normal işletim durumudur**: kitap asla "başarısız" olmaz, "312 sayfası hazır, 88 sayfası taranmış ek — atlandı" olur (Doktrin kuralı 3: reddetme yok, sıkıştırma var).

---

## 0. Kapsamım ve sınırlarım

| Bana ait | Bana ait değil |
|---|---|
| Dosyadan atom taslağına kadar her aşama | Atomun içeriği/ontolojisi → `01-bilgi-modeli.md` |
| Kuyruk, durum makinesi, yeniden deneme, sürümleme | Şema, indeksler, türetilmiş veri, saklama → `08-veri-sistemi.md` |
| Model kademelemesi, maliyet, süre bütçesi | Graf algoritmaları, yenilik skoru → `02-yenilik-ve-graf.md` |
| Uygulama iskeleti, API sınırları, yerel kurulum | SymPy doğrulama kuralları → `03-dogrulama.md`, ekranlar → `06-arayuz.md` |

`08`'e **arayüz** veriyorum (bkz. §11), tablolarını yazmıyorum.

---

## 1. Boru hattı haritası

```
                 ┌──────────────────────────────────────────────────┐
  dosya  ──────► │ S0  ALIM        parmak izi, tekilleştirme, künye  │
                 ├──────────────────────────────────────────────────┤
                 │ S1  NORMALLEŞTİRME  → tek ara biçim: BookDoc      │
                 │     (PDF/EPUB/DjVu/tarama → blok akışı)          │
                 ├──────────────────────────────────────────────────┤
                 │ S2  YAPI        bölüm/altbölüm ağacı, sayfa eşlem │
                 ├──────────────────────────────────────────────────┤
                 │ S3  BLOK SINIFI paragraf|formül|şekil|tablo|      │
                 │                 dipnot|kaynakça|indeks|alıştırma  │
                 ├──────────────────────────────────────────────────┤
                 │ S4  MATEMATİK   formül → LaTeX (+güven skoru)     │
                 ├──────────────────────────────────────────────────┤
                 │ S5  ELEME       kaynakça/indeks/kolofon at        │
                 ├──────────────────────────────────────────────────┤
                 │ S6  PARÇALAMA   → işleme birimi (4–8k token)      │
                 ├──────────────────────────────────────────────────┤
                 │ S7  ATOM ÇIKARIMI   LLM · kademeli               │
                 ├──────────────────────────────────────────────────┤
                 │ S8  ÇAPA DOĞRULAMA  alıntı gerçekten o sayfada mı │
                 ├──────────────────────────────────────────────────┤
                 │ S9  SEMBOLİK DOĞRULAMA (03'ün kuralları koşar)    │
                 ├──────────────────────────────────────────────────┤
                 │ S10 GÖMME + BAĞLANTI (02'nin algoritması koşar)   │
                 ├──────────────────────────────────────────────────┤
                 │ S11 YAYIN       kitap `ready`, kullanıcıya görünür│
                 └──────────────────────────────────────────────────┘
```

S0–S6 CPU işi (Python), S7–S10 LLM/gömme işi, S11 işlem (transaction).
**S8 kilit taştır**: Doktrin kuralı 2'yi (kaynaksız cümle yok) mekanik olarak zorlayan tek yer.

---

## 2. Alım (S0–S1): format başına araç

Hedef: her format **tek bir ara biçime** iner — `BookDoc`: sıralı blok akışı, her blokta `{block_id, page, bbox, text, font_size, is_bold, column}`.

| Format | Araç | Neden (tek cümle) |
|---|---|---|
| Dijital doğumlu PDF | **PyMuPDF (fitz)** | Sayfa başına ~5 ms, bbox + font metriği verir; yapı tespitinin tamamı bu metriklere dayanıyor. |
| PDF tablo/sütun kenar durumu | **pdfplumber** (sadece şüpheli sayfada) | Yavaş ama çok sütunlu düzen ve tabloda PyMuPDF'ten belirgin daha doğru; sayfa başına düşülen bir kaçış yolu. |
| EPUB | **Calibre `ebook-convert` → EPUB3 + `ebooklib`** | Calibre bozuk EPUB'ları onarır, `ebooklib` içindekiler (NCX/nav) ağacını hazır verir — yapı tespiti bedavaya gelir. |
| MOBI/AZW3 | **Calibre → EPUB** ardından EPUB yolu | İkinci bir ayrıştırıcı yazmaya değmez. |
| DjVu | **`ddjvu` → PDF**, sonra tarama yolu | DjVu neredeyse her zaman taranmış; ayrı bir araç zinciri sürdürmek maliyet. |
| Taranmış PDF (düz metin) | **OCRmyPDF (Tesseract 5)** | Olgun, CPU'da koşar, PDF'e metin katmanı gömer → sonraki her aşama dijital doğumlu gibi çalışır. |
| Taranmış PDF (matematik/tablo yoğun) | **Marker** (birincil), **Nougat** (yedek) | Marker düzen + LaTeX'i tek geçişte üretir ve Nougat'tan hızlıdır; Nougat akademik dizgide daha iyi ama halüsinasyon eğilimli, o yüzden yedek. |
| Herhangi bir format, dijital katmanı bozuk | **Sayfanın görselini Sonnet 5 vision'a** | Son çare; sayfa başına maliyeti var, o yüzden kota ile sınırlı (§7). |

**Karar akışı (S1 girişinde, otomatik):**
```
metin katmanı var mı?           hayır → OCR yolu
  evet → sayfa başına <100 karakter mi?   evet → OCR yolu (sahte metin katmanı)
       → gömülü yazı tipleri anlamsız mı (cid: eşlemi bozuk)? evet → OCR yolu
       → matematik yoğunluk skoru > 0.15 mi? evet → Marker'ı da koştur, ikisini birleştir
       → hayır → saf PyMuPDF
```
`matematik yoğunluk skoru` = sayfada matematik yazı tipi (CMMI/CMSY/MathJax/STIX) glif oranı. Ucuz, deterministik, LLM gerektirmiyor.

**Tekilleştirme (S0):** `sha256(dosya)` + *içerik parmak izi* = normalleştirilmiş ilk 20 sayfanın metninin SimHash'i. Aynı kitabın farklı baskısı yeniden işlenir ama önceki sürüme `edition_of` bağı ile bağlanır — kullanıcı "bu kitabın 2. baskısı zaten kütüphanende" cevabını alır.

---

## 3. Matematik çıkarımı (S4): gerçekçi plan ve başarısızlık planı

Bu, boru hattının **en çok yalan söyleyen** aşaması. Bu yüzden tasarım "doğru çevir" değil, **"yanlış çevirdiğini bil"** üzerine kurulu.

**Üç kaynaklı strateji:**

1. **LaTeX kaynağı varsa (arXiv, bazı EPUB'lar):** doğrudan al, güven = 1.0. En iyi durum, hedeflenmeli.
2. **Dijital doğumlu PDF:** matematik yazı tipi glifleri + bbox'tan formül bölgesi tespit et, bölgenin görselini kes, **Marker**'a ver. Marker LaTeX üretir. Güven = Marker skoru.
3. **Taranmış:** bölge görseli → Marker; Marker düşük güven verirse aynı görsel **Sonnet 5 vision**'a ikinci görüş için gider.

**Sonra her LaTeX üç kapıdan geçer:**

| Kapı | Test | Başarısızlıkta |
|---|---|---|
| K1 · Sözdizimi | KaTeX ile render edilebiliyor mu? | Otomatik onarım denemesi (dengesiz parantez, `\left/\right`), sonra K1 tekrar. |
| K2 · Sembolik | SymPy `parse_latex` ayrıştırıyor mu? (03'ün kuralları) | Formül "görsel" olarak saklanır, sembolik iddia üretilmez. |
| K3 · Geri-render | Üretilen LaTeX'in görüntüsü ile kaynak kesitin algısal hash farkı < eşik | Güven düşürülür. |

**Başarısızlık planı — üç seviyeli aşağı düşme (graceful degradation):**

```
seviye 0  LaTeX + SymPy doğrulandı     → formül atomu üretilir, tam yetkili
seviye 1  LaTeX var, SymPy ayrıştıramadı → atom üretilir, [doğrulanamadı] etiketi
seviye 2  LaTeX yok/güvensiz           → formül GÖRSEL kırpıntı olarak saklanır,
                                          metin atomu "Bölüm 4.2'de bir eşitsizlik
                                          var" der ve görseli gösterir; asla
                                          uydurulmuş bir formül üretilmez
```

**Sert kural:** Seviye 2'deki bir formül hiçbir zaman LLM'e metin olarak gönderilmez. Bozuk LaTeX'i LLM'e vermek, halüsinasyonu üretmenin en hızlı yoludur. Onun yerine LLM'e `[FORMÜL#f_1a2b — s.148, çevrilemedi]` yer tutucusu gider; LLM bu yer tutucu hakkında iddia üretemez, sadece etrafındaki metinden yararlanır.

**Beklenti (dürüst):** dijital doğumlu matematik kitabında formüllerin ~%90'ı seviye 0–1'e ulaşır; iyi taranmış kitapta ~%65; kötü taranmış (eğri, lekeli) kitapta ~%35. Kötü tarama için ürün cevabı: **"Bu kitabın matematiği güvenilir şekilde okunamadı — düzyazısını sindirdim, formüllerini sayfa görseli olarak gösteriyorum."** Bu bir hata değil, bir üründür.

---

## 4. Yapı tespiti ve eleme (S2, S3, S5)

**Bölüm ağacı — üç kaynak, öncelik sırasıyla:**
1. **Gömülü ana hat** (PDF outline / EPUB nav): varsa kullan, %70 kitapta var, bedava.
2. **İçindekiler sayfası ayrıştırma:** ilk 25 sayfada "İçindekiler/Contents" başlığı + `metin ... nokta dizisi ... sayı` kalıbı → başlık+sayfa çiftleri; sonra bu sayfalara gidip başlığın gerçekten orada olduğunu doğrula (yanlış hizalanmış ToC'yi yakalar).
3. **Tipografik kümeleme:** gövde metni font boyutu medyanı hesaplanır; medyanın 1.15× üstündeki, kısa (<12 kelime), sayfa üstünde veya tek başına duran satırlar başlık adayı. Numaralandırma kalıbı (`^\d+(\.\d+)*\s`) seviyeyi verir.

Üçü de çelişirse (nadiren, ~%8) **Haiku 4.5**'e 30–50 aday başlık + bağlamı gönderilir ve sadece "başlık mı, hangi seviye?" sorusu sorulur. Ucuz, mekanik, LLM'in gerçekten iyi olduğu iş.

**Eleme (S5) — atoma dönüşmemesi gerekenler.** Sinyaller kombinasyonu, tek sinyale güvenilmez:

| Bölge | Tespit sinyalleri |
|---|---|
| Kaynakça | Başlık eşleşmesi (References/Bibliography/Kaynakça) **+** blok başına yıl-parantez yoğunluğu > 0.4 **+** ortalama satır uzunluğu düşük **+** asılı girinti (hanging indent) **+** kitabın son %15'inde |
| İndeks | 2–3 sütunlu düzen **+** satır başına sayı yoğunluğu > 0.5 **+** alfabetik monotonluk (ardışık satırların ilk harfi artan) **+** son %8 |
| Dipnot | Sayfa altında, gövdeden küçük font, üst simge referansı ile eşleşiyor → **elenmiyor**, ait olduğu paragrafa `footnotes[]` olarak bağlanıyor |
| Alıştırma/Problem | "Exercises/Problems/Alıştırmalar" başlığı + numaralı liste → **ayrı sınıf**: atom değil, ama `03`'ün doğrulama örneklem havuzu ve önkoşul DAG'ı için saklanır |
| Kolofon/telif/önsöz | İlk %3 + anahtar kelime | 
| Sembol listesi (Notation) | **Elenmiyor** — §5'teki *notasyon sözlüğüne* beslenir, matematik kitabında altın değerinde |

Alfabetik monotonluk testi indeksi tek başına %95 doğrulukla yakalar; yanlış pozitif riski (alfabetik sözlük bölümü olan bir kitap) için: elenen bölge > 40 sayfaysa insan onayı bayrağı kalkar (`needs_review`), kitap yine de yayınlanır.

---

## 5. Parçalama (S6)

**Karar: anlamsal bölüm-tabanlı parçalama, sabit hedef 6.000 token, sert tavan 12.000.** Kayan pencere varsayılan değil; sadece bölüm sınırı belirsizse (yapı skoru düşük) 800 token örtüşmeli 6k pencereye düşülür.

**"Bağlam penceresi 1M, neden parçalıyorsun?"** Çünkü sınır bağlam değil, **dikkat ve çapa doğruluğu**. Uzun bağlamda sayfa numarası atıflarının kayması ve birim başına atom veriminin düşmesi ölçülebilir bir olgudur; 6k'lık birim, üretilen her atomun 15–20 sayfalık dar bir pencereye çapalanmasını garantiler. Ayrıca yeniden işleme birimi küçük kalır (§10).

**Bölünme kuralları:**
- Bölünme noktaları önce `altbölüm sınırı`, sonra `paragraf sınırı`. **Asla** teorem–ispat çiftinin ortasından, tanım–örnek zincirinin ortasından bölünmez (S3 bu blokları `math_unit` olarak gruplamıştır).
- Bir altbölüm 12k'yı aşarsa: teorem sınırlarından bölünür, her parça `part 2/3` işaretlenir ve **önceki parçanın ürettiği atomların başlıkları** sonraki çağrıya bağlam olarak eklenir.
- Bir altbölüm 1.500 token'ın altındaysa komşusuyla birleştirilir (kısa altbölüm salvosu → aşırı çağrı → maliyet).

**Her LLM çağrısının zarfı (envelope) — bağlam korunumu üç katmanda:**

```
[ÖNBELLEKLİ ÖNEK — kitap ömrü boyunca sabit, ~8k token]
  · Atom ontolojisi + çıktı şeması (01'den)
  · Kitap künyesi: başlık, yazar, alan, seviye, yayın yılı
  · Kitabın tam bölüm ağacı (sadece başlıklar, ~1.5k)
  · NOTASYON SÖZLÜĞÜ: bu kitapta σ ne demek, ⊗ ne demek (S3'ten)
  · Kullanıcının Açık Sorular Defteri başlıkları (07 için ön-tohum)
[DEĞİŞKEN GÖVDE — çağrı başına]
  · Bulunduğun yer: "Böl. 7 → 7.3 Ölçülebilir Fonksiyonlar, s.148–161"
  · YÜRÜYEN DURUM: önceki 2 birimden üretilmiş atom başlıkları (~600 token)
  · Metin blokları — her biri [B#id | s.148] etiketli
```

`cache_control` kırılma noktası önekin sonuna konur. 40 çağrılık bir kitapta önek 39 kez %10 fiyatına okunur — tek başına çağrı başına ~7k token tasarrufu.

**Çapa korunumu:** LLM'den her atomda `source_blocks: ["B#412","B#413"]` ve `quote: "<en fazla 25 kelime birebir alıntı>"` istenir. S8, `quote`'u iddia edilen blokların metninde bulanık eşleştirir (normalize edilmiş, Levenshtein oranı ≥ 0.88). Eşleşmezse atom **düşürülmez**, `anchor_confidence: low` ile işaretlenir ve arayüzde `[çapa doğrulanamadı]` görünür. Doktrin: emin olmadığımızı eminmiş gibi sunmuyoruz.

---

## 6. Orkestrasyon (S0–S11)

**Kuyruk kararı: PostgreSQL tabanlı iş kuyruğu (`SELECT ... FOR UPDATE SKIP LOCKED`).** Redis/RabbitMQ değil — çünkü (a) zaten Postgres var, `docker compose` servis sayısı 2'de kalıyor (açık kaynak kurulabilirliği bir özelliktir), (b) hem TypeScript hem Python istemcisi 40 satır, (c) **iş durumu ile veri aynı işlemde (transaction) commit ediliyor** — kuyruk/DB tutarsızlığı sınıfı bütünüyle ortadan kalkıyor. 500 kitap/gün ölçeğinde Postgres kuyruğu fazlasıyla yeterli; darboğaz LLM gecikmesi.

**İş kaydı:**
```
job(id, book_id, stage, stage_version, input_hash, state, attempt,
    lease_until, worker_id, error_class, error_detail, created_at)
```

**İdempotency:** `UNIQUE(book_id, stage, stage_version, input_hash)`.
`input_hash = sha256(bir önceki aşamanın eser hash'i ‖ stage_version ‖ prompt_version ‖ model_id)`.
Eser üretimi **içerik-adresli**: `artifacts/<sha256>.json`. Bir iş iki kez koşarsa aynı hash'e yazar — yan etkisi yok. LLM çağrılarına `idempotency_key` de gider; bir yeniden deneme çift faturalanmaz.

**Yeniden deneme politikası — hata sınıfına göre, kör tekrar yok:**

| Hata sınıfı | Politika |
|---|---|
| `rate_limit` (429) | Üstel geri çekilme + `retry-after`, 6 deneme, kuyruk çapında token kovası |
| `transient` (5xx, ağ, zaman aşımı) | 4 deneme, 2ⁿ + jitter |
| `oom` / `timeout` (OCR devi) | 1 deneme, **yarı boyutlu parçayla** (sayfa aralığını ikiye böl) |
| `schema_invalid` (LLM şemayı bozdu) | 2 deneme; 2. denemede `strict: true` + hata metni geri beslenir; sonra bir kademe yukarı model |
| `refusal` / içerik | Yeniden deneme yok → `needs_review` |
| `permanent` (bozuk dosya, şifreli PDF) | 0 deneme → kullanıcıya net mesaj |

Lease modeli: iş 15 dk `lease_until` alır; çöken işçi (worker) süresi dolunca otomatik geri kuyruğa döner. Zehirli mesaj (poison pill) koruması: 3 lease kaybı → `quarantined`.

**Durum makinesi — kitap her an tam olarak nerede?**

```
uploaded → extracting → structured → digesting → linking → ready
                │            │            │          │
                └────────────┴────────────┴──────────┴──► partial
                                                       └──► needs_review
                             (permanent hata)          └──► blocked
```

**Kısmi başarısızlıkta kitabın durumu — aşama aşama:**

| Çöken aşama | Kitabın hali | Kullanıcı ne görür |
|---|---|---|
| S1 alım | `blocked` | "Bu dosya şifreli / bozuk. Şifresiz bir kopya yükle." Tek eylem, tek buton. |
| S1 kısmi OCR (88 sayfa okunamadı) | `partial` | "312 sayfa hazır. 88 sayfa okunamadı (ekler)." Kitap **kullanılabilir**. |
| S2 yapı | `partial` | Kitap düz bölüm listesi olarak işlenir; hiyerarşi yok, atomlar yine sayfa çapalı. |
| S4 matematik | `partial` + `math_degraded` | "Formüller görsel olarak saklandı." Sindirim tam. |
| S7 bazı birimler (örn. 40'ta 3) | `partial` | "Bölüm 9 sindirilemedi — tekrar dene" düğmesi, sadece o 3 birim koşar. |
| S7 tüm birimler | `needs_review` | "İşleme takıldı, kuyruğa alındı." Otomatik gece tekrarı. |
| S9 doğrulama | `ready` | Atomlar `[doğrulanamadı]` etiketli çıkar — bu bir başarısızlık değil, bir bilgi. |
| S10 bağlantı | `ready` | Kitap tek başına okunabilir, graf bağları gecikmeli gelir. |

**Doktrin uygulaması:** ilerleme çubuğu 11 aşama göstermez — tek satır gösterir: *"Bölüm 7 sindiriliyor · 12 bölümden 7'si"*. Kural 1 (bir ekran = bir karar) boru hattı için de geçerli.

---

## 7. Maliyet ve süre

**Referans kitap:** 400 sayfa, teknik, dijital doğumlu. Sayfa başına ~480 token → **~195.000 token ham metin**; eleme sonrası ~165k; ~30 işleme birimi.

| Aşama | Model | Girdi tok | Çıktı tok | Ham $ | Optimize $ |
|---|---|---|---|---|---|
| S0–S3 alım/yapı/sınıf | CPU (LLM yok) | — | — | ~$0.01 | ~$0.01 |
| S2b belirsiz başlık hakemliği | Haiku 4.5 | 35k | 5k | $0.06 | $0.03 |
| S4 matematik (dijital) | CPU + Marker | — | — | ~$0.02 | ~$0.02 |
| S7a geniş geçiş (30 birim) | **Sonnet 5** | 265k¹ | 145k | $2.98 | **$1.16**² |
| S7b titiz geçiş (teorem/formül birimleri, ~%25) | **Opus 5** | 75k | 55k | $1.75 | $0.94 |
| S8 çapa doğrulama | CPU | — | — | $0 | $0 |
| S9 sembolik doğrulama + onarım (sadece hatalı) | Opus 5 | 18k | 12k | $0.39 | $0.20 |
| S10 gömme (~700 atom) | yerel/harici gömme | — | — | ~$0.02 | ~$0.02 |
| S10b bağlantı yargısı (~250 aday çift) | Sonnet 5 | 110k³ | 28k | $0.50 | $0.17 |
| **Toplam** | | **~503k** | **~245k** | **$5.73** | **$2.55** |

¹ 265k = 165k gövde + 30 çağrı × ~3.3k değişken zarf; önbellekli 8k önek ayrıca 29 kez okunur.
² Önbellek (önek %10 fiyat) + elenen içeriğin hiç gönderilmemesi.
³ Adayların çoğu ortak önek paylaşır → yüksek önbellek isabeti.

**Taranmış kitap farkı:** +Marker/Tesseract CPU (dolar değil, dakika), + belirsiz sayfalar için Sonnet 5 vision (~60 sayfa × ~1.6k token görsel = 96k girdi, 22k çıktı) ≈ **+$0.41** → toplam **~$3.0**. Kötü taramada vision kotası 120 sayfaya çıkar → ~$3.6.

**Süre bütçesi (tek makine, işçi eşzamanlılığı 8):**

| | Dijital doğumlu | Taranmış |
|---|---|---|
| S0–S3 | 40–90 sn | — |
| OCR/Marker | — | 18–35 dk (CPU), 4–8 dk (GPU) |
| S4–S6 | 30–60 sn | 60–120 sn |
| S7 (30 birim ÷ 8 eşzamanlı, çağrı başına 45–90 sn) | 5–9 dk | 5–9 dk |
| S8–S10 | 2–4 dk | 2–4 dk |
| **Toplam** | **~9–15 dk** | **~28–50 dk (CPU)** |

**Maliyeti düşüren 3 somut kaldıraç:**

1. **Prompt önbelleği (prompt caching) — %25–30 tasarruf, kalite kaybı sıfır.** Kitap-ömürlü 8k'lık önek (ontoloji + şema + bölüm ağacı + notasyon sözlüğü) 29 çağrıda 0.1× fiyata okunur. Önek 5 dakikalık TTL'de sıcak kalır; S7 zaten yoğun koştuğu için ekstra bir şey yapmaya gerek yok. Doğrulama: `usage.cache_read_input_tokens` sıfırsa bir sessiz geçersizleştirici (timestamp, sırasız JSON) vardır.
2. **Model kademelemesi — %45 tasarruf.** Her şeyi Opus 5'e vermek $5.73 yerine ~$9.8 eder; §8'deki kademeleme aynı işi $2.55'e indirir. Kritik ayrım: *sınıflandırma* ucuz modelde, *yargı* pahalı modelde.
3. **Batch API (%50, her token — önbellek okumaları dahil) yalnız gecikmeye duyarsız iş için.** İlk yüklemede kullanılmaz (kullanıcı bekliyor). Kullanıldığı yerler: (a) 500 kitaplık yeniden işleme (§10), (b) gece koşan bağlantı yargısı S10b, (c) gömme sırt-doldurmaları. Yeniden işlemede tek başına $750 → $375.

**Bedava dördüncü kaldıraç:** elenen içerik (kaynakça+indeks+alıştırma) tipik teknik kitapta sayfaların **%14–22'si**. Bu içeriği LLM'e hiç göndermemek, hiçbir kalite kaybı olmadan girdi faturasının beşte birini siler. S5 kendini ilk kitapta amorti eder.

---

## 8. Model kademelemesi

| İş | Model | Gerekçe |
|---|---|---|
| Başlık mı değil mi, blok sınıfı hakemliği, dil tespiti, kısa normalleştirme | **Haiku 4.5** | Kalıp tanıma; en güçlü modelin marjinal faydası ölçülemez, fiyat farkı 5×. |
| Atom çıkarımı — düzyazı, tarih, felsefe, kişisel gelişim, tıp anlatısı | **Sonnet 5** | Uzun bağlamda tutarlı yapılandırılmış çıktı; bu metinlerde hata maliyeti düşük (Brifing §7: yanlış anekdot can sıkıcı). |
| Atom çıkarımı — teorem, ispat, tanım, formül, algoritma, klinik doz/titrasyon | **Opus 5** (`effort: high`, adaptive thinking) | Brifing §7: yanlış özetlenen teorem **zehirlidir**; önkoşul çıkarımı gerçek muhakeme ister. |
| Sembolik doğrulama hatasının onarımı | **Opus 5** (`effort: xhigh`) | Zaten dar bir küme; en zor vakalar burada. |
| Bağlantı türü yargısı (aynı/çelişiyor/önkoşulu/genellemesi) | **Sonnet 5**, düşük güvenli çiftler **Opus 5**'e yükseltilir | Aday üretimi gömme ile; LLM sadece ikili karar veriyor. |
| **Transfer yargısı** (atom → Açık Sorular Defteri) | **Opus 5** (`effort: xhigh`) | Ürünün kalbi ve çapraz-alan sıçraması; burada ucuzluk aramak ürünü öldürür. |
| Kullanıcıya gösterilen son metnin yazımı | **Opus 5** | Kullanıcının okuduğu tek cümleler bunlar. |

**Kademeleme kuralları:**
- **Yukarı yükseltme (escalation) otomatik ve ölçülü:** Sonnet 5 bir birimde şema hatası verirse, kendi çıkardığı atomların ortalama güveni < 0.6 ise, ya da birimde `math_unit` bloğu varsa → Opus 5. Yükseltme oranı > %35 olursa alarm: kademeleme kalibrasyonu bozulmuş demektir.
- **Aşağı düşürme yok.** Opus 5 gerektiren bir iş, bütçe bahanesiyle Sonnet'e verilmez; bütçe biterse iş **kuyrukta bekler**, kalitesiz koşmaz.
- `thinking: {type:"adaptive"}` her yerde açık; Opus 5'te thinking'i kapatmak yerine `effort` düşürülür.
- Yapılandırılmış çıktı `output_config.format` + tool'larda `strict: true` ile zorlanır — ayrıştırma hatası sınıfını neredeyse sıfırlar.
- Model kimliği (`model_id`) her esere damgalanır; §10'daki geçiş planı buna dayanıyor.

`AÇIK SORU:` Tıbbi doz/titrasyon içeriğinin **her zaman** Opus 5 gerektirip gerektirmediğine `05b-tip.md` karar vermeli; ben "evet" varsayıyorum.

---

## 9. Uygulama iskeleti

**İki çalışma zamanı, tek depo (monorepo).** Next.js kullanıcıya bakar; ağır alım Python'da koşar — çünkü PyMuPDF/Tesseract/Marker/SymPy ekosistemi orada, TypeScript'te taklidini yazmak akılsızlık.

```
book-beast/
├── apps/
│   └── web/                          # Next.js 15 (App Router) + TypeScript
│       ├── app/
│       │   ├── (okuma)/              # kullanıcı yüzeyi — 06'nın alanı
│       │   │   ├── bugun/            # günlük tek satır plan
│       │   │   ├── kitap/[id]/
│       │   │   └── defter/           # Açık Sorular Defteri
│       │   └── api/
│       │       ├── upload/           # imzalı yükleme URL'si üretir, iş kuyruklar
│       │       ├── books/[id]/status/# SSE: durum makinesi akışı
│       │       ├── books/[id]/retry/ # tek aşama yeniden deneme
│       │       └── webhooks/
│       ├── lib/                      # sunucu tarafı: db, kuyruk üreticisi, yetki
│       └── components/
├── services/
│   └── ingest/                       # Python 3.12 — S0..S6
│       ├── stages/                   # her aşama tek dosya, saf fonksiyon
│       │   ├── s0_intake.py  s1_normalize.py  s2_structure.py
│       │   ├── s3_blocks.py  s4_math.py  s5_prune.py  s6_chunk.py
│       ├── adapters/                 # pymupdf_, pdfplumber_, calibre_, ocr_, marker_
│       ├── worker.py                 # kuyruk tüketicisi, lease, retry
│       └── contracts/                # packages/contracts'tan üretilen pydantic
│   └── digest/                       # TypeScript işçi — S7..S11 (LLM)
│       ├── prompts/                  # sürümlü: v3/atom-extract.md
│       ├── tiering.ts                # §8 karar tablosu
│       └── anchor-verify.ts          # S8
├── packages/
│   ├── contracts/                    # TEK DOĞRULUK KAYNAĞI: zod → JSON Schema
│   │   └── (BookDoc, Block, Unit, AtomEnvelope, JobRecord)
│   ├── db/                           # 08'in sahibi: şema, migration, sorgular
│   └── llm/                          # Anthropic istemcisi: önbellek, retry, sayaç
├── infra/
│   ├── docker-compose.yml
│   └── Dockerfile.{web,ingest,digest}
└── docs/
```

**API sınırları — üç sert kural:**
1. **İstek yolunda (request path) LLM çağrısı yok.** Her `/api` uç noktası ya DB okur ya iş kuyruklar; hiçbiri model beklemez. İlerleme SSE ile akar.
2. **Aşamalar saf fonksiyondur:** `(input_artifact) -> output_artifact`. DB'ye yazan tek yer `worker`'dır. Bu, bir aşamayı CLI'dan tek dosya üstünde koşturmayı (`python -m ingest.stages.s2 kitap.pdf`) mümkün kılar — hata ayıklamanın tamamı buna dayanıyor.
3. **Şemalar `packages/contracts`'ta bir kez tanımlanır**, TS tipleri ve Python pydantic modelleri oradan üretilir. İki dilde elle senkronize edilen şema, üretimde patlar.

**Arka plan işleri nerede koşar:** `services/ingest` ve `services/digest` **ayrı konteynerlerde**, yatay ölçeklenir (`docker compose up --scale ingest=3`). Next.js sunucusunda arka plan işi koşmaz — serverless dağıtımda ilk kaybedilen şey odur. Zamanlanmış işler (gece bağlantı geçişi, karantina tekrarı) `digest` içindeki basit bir cron döngüsüyle, iş kuyruğuna yazarak.

**Yerel kurulum hedefi — üç komut:**
```
git clone … && cp .env.example .env      # tek zorunlu değişken: ANTHROPIC_API_KEY
docker compose up                        # postgres + web + ingest + digest
open http://localhost:3000
```
`docker compose up` migration'ları kendisi koşar, `ingest` imajı Tesseract dil paketleriyle gelir. Marker/GPU **isteğe bağlı profil** (`--profile gpu`); onsuz sistem Tesseract'a düşer ve çalışır. API anahtarı yoksa uygulama açılır, sindirim `blocked` durumunda net bir mesajla bekler — sessizce çökmez.

---

## 10. Yeniden işleme

Atom modeli **kesinlikle** gelişecek. Buna hazırlıklı olmayan bir mimari, 200. kitapta donar.

**Sürüm damgaları — her eserde beşi birden:**
```
extractor_version   S1–S3 kodu       (örn. "ext-4")
math_version        S4 kodu          ("math-2")
chunk_version       S6 kodu          ("chunk-3")
atom_schema_version 01'in ontolojisi ("atom-7")
prompt_version + model_id            ("p-v12" + "claude-opus-5")
```
`input_hash` bunları içerdiği için, **bir sürüm damgası değiştiğinde etkilenen aşama otomatik olarak "eski" sayılır** — ayrı bir geçersizleştirme mekanizmasına gerek yok.

**Dört seviyeli geçiş merdiveni — hepsi yeniden sindirim değildir:**

| Seviye | Ne değişti | Ne koşar | 500 kitabın maliyeti |
|---|---|---|---|
| **G0 · Şema göçü** | Alan yeniden adlandırıldı, enum eklendi | Saf kod dönüşümü, LLM yok | ~$0, dakikalar |
| **G1 · Türetilmiş yeniden hesap** | Gömme modeli, bağlantı eşiği, yenilik skoru | S10 tekrar | ~$85 (Batch) |
| **G2 · Hedefli yeniden yargı** | Sadece bir atom sınıfı değişti (örn. "teorem"in önkoşul alanı) | Sadece o sınıfın atomlarını üreten birimler | ~$180 (Batch) |
| **G3 · Tam yeniden sindirim** | Ontoloji kökten değişti | S6–S11 | ~$375 (Batch, $0.75/kitap) |

S0–S5'in eserleri (ham metin, bloklar, LaTeX) **kalıcıdır**; G3 bile OCR'ı tekrarlamaz. Yeniden işlemenin en pahalı kısmı zaten diskte duruyor.

**Kademeli geçiş protokolü:**
1. **Kanarya (canary): 20 kitap.** Alanlara göre seçilir (5 matematik, 3 tıp, 4 tarih/felsefe, 3 mühendislik, 2 sanat, 3 kişisel gelişim) ve içine **3 altın kitap** konur — atomları elle denetlenmiş referanslar.
2. **Gölge yazım (shadow write):** yeni sürüm `atom_set(book_id, version)` olarak yazılır, eski sürüm aktif kalır. Kullanıcı hiçbir şey görmez.
3. **Fark raporu:** atom sayısı deltası, kaybolan atomlar (en tehlikeli sinyal), çapa güveni ortalaması, `[doğrulanamadı]` oranı, 03'ün doğrulama geçme oranı, altın kitaplarda elle bakılan 30 atom.
4. **Kapı:** kaybolan atom oranı > %8 **veya** altın kitap regresyonu varsa geçiş durur.
5. **Dalgalar:** %5 → %25 → %100, her dalga arasında 24 saat. Aktif sürüm işaretçisi kitap başına tek satırlık bir güncelleme — geri alma (rollback) anlıktır.
6. **Emeklilik:** N-1 sürümü 30 gün saklanır, sonra silinir. İki sürümden fazlası asla canlı tutulmaz.

**Kullanıcı ne görür:** hiçbir şey — arka planda olur. Tek istisna, bir kitapta anlamlı yenilik ortaya çıkarsa: *"Ölçü Teorisi'nde daha önce kaçırdığım 3 fikir var."* Bu bir bildirim değil, bir keşiftir; kullanıcı isterse bakar.

---

## 11. `08-veri-sistemi.md`'ye arayüz (sözleşme, uygulama değil)

Depolama katmanından beklediğim beş şey, tablo tasarımına karışmadan:

1. **Eser deposu (artifact store):** `put(sha256, bytes) / get(sha256)`, değişmez (immutable), yerelde dosya sistemi, uzakta S3-uyumlu. Boyut: kitap başına ~15–60 MB (görsel kırpıntılar dahil).
2. **İş kuyruğu ilkelleri:** `enqueue`, `lease(stage, n, ttl)`, `complete`, `fail(class)`, `reap_expired`. `UNIQUE(book_id, stage, stage_version, input_hash)` garantisi bende değil, sende.
3. **Atom zarfı (envelope) — gövdeyi `01` tanımlar, zarfı ben:**
   ```
   { atom_id, book_id, atom_schema_version,
     anchor: { chapter_path:"7.3", page_start:148, page_end:151,
               source_blocks:["B#412"], quote, anchor_confidence },
     provenance: { stage_versions{...}, model_id, prompt_version,
                   created_at, verification_status },
     body: <01'in şeması> }
   ```
   `anchor` ve `provenance` **zorunlu ve boş geçilemez** — Doktrin kuralı 2 veritabanı kısıtı olarak yaşamalı, yalnız uygulama kodunda değil.
4. **Sürümlü atom kümeleri:** `atom_set(book_id, version, state: shadow|active|retired)`; aktif sürüm işaretçisi tek satırlık, atomik güncellenebilir (§10 geri alma).
5. **Olay günlüğü (event log):** `book_events(book_id, stage, from_state, to_state, at, detail)` — kullanıcıya gösterilen ilerleme ve bütün hata teşhisi bunun üstünde koşuyor.

---

## 12. Açık sorular

- `AÇIK SORU:` **DjVu gerçekten gerekli mi?** Kullanıcı kitlesinde payı %1'in altındaysa v1'de "desteklenmiyor, PDF'e çevirin" demek doğru karar; ölçmeden ekleme.
- `AÇIK SORU:` **Marker'ın lisansı ve GPU bağımlılığı** açık kaynak kurulabilirlik hedefiyle çelişiyor olabilir. Çelişirse: Tesseract varsayılan, Marker isteğe bağlı eklenti (`--profile gpu`) olarak kalır — mimari zaten buna izin veriyor.
- `AÇIK SORU:` **Transfer (S10c) boru hattına mı ait, talep anında mı koşmalı?** Açık Sorular Defteri sık değişiyorsa her değişimde 500 kitabı yeniden eşlemek pahalı; ben "atom→defter eşlemesi tembel (lazy) ve önbellekli" varsayıyorum. `07-transfer.md` karar versin.
- `AÇIK SORU:` **Bir kitabın tek bir işleme birimi kalıcı olarak çökerse eşik nedir?** %10'dan fazla birim çökmüşse kitap `partial` yerine `needs_review` olmalı diye düşünüyorum; ürün kararı `06-arayuz.md`'ye ait.
- `AÇIK SORU:` **Kullanıcı başına maliyet tavanı.** Ayda 20 kitap yükleyen bir kullanıcı ~$60 maliyet üretir; bu bir ürün/fiyat kararıdır, mimari değil — ama boru hattı bütçe kısıtı (kuyrukta bekletme) için hazır.
