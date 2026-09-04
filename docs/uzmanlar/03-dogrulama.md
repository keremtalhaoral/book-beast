# 03 — Doğrulama Mimarisi

> Uzman: Doğrulama Mühendisi (Biçimsel Yöntemler)
> Kapsam: Brifing Kural 2 ("Kaynaksız cümle yok") ve Bölüm 7 (matematik/mühendislik titizliği)

## 3 cümlelik özet

Sistemdeki hiçbir atom, bir makine tarafından bağımsızca doğrulanmadan kullanıcıya
"doğru" diye gösterilmez; LLM çıktısı bu boru hattında **tanık değil sanıktır**.
Her atom dört bağımsız kapıdan geçer — çapa/alıntı eşleme, sembolik (SymPy) kontrol,
hipotez bütünlüğü kontrolü, graf-içi çelişki taraması — ve bu kapıların sonucuna göre
`doğrulandı(sembolik)` / `doğrulandı(alıntı)` / `desteklendi(NLI)` / `doğrulanamadı`
etiketlerinden **tam birini** taşır.
Doğrulanamayan atom silinmez, **karantinaya alınır**: grafta kenar kuramaz, transfer
üretemez, günlük plana giremez; sadece ham alıntısıyla, açık uyarıyla gösterilebilir.

---

## 0. Temel doktrin — 5 madde

| # | İlke | Sonucu |
|---|------|--------|
| D0 | **LLM'in "bu doğrudur" demesi kanıt değildir.** | Modelin öz-değerlendirme skoru (`confidence: 0.95`) hiçbir kapıda girdi olarak kullanılmaz. Şemadan tamamen çıkarılmıştır. |
| D1 | **Doğrulayıcı, üreticiden bağımsız olmalı.** | Atomu üreten çağrı ile doğrulayan mekanizma aynı bağlamı paylaşmaz. Doğrulayıcı yalnız (atom, ham sayfa metni) çiftini görür — üretimin gerekçesini görmez. |
| D2 | **Deterministik kontrol > olasılıksal kontrol.** | Sıralama sabittir: string eşleme → sembolik cebir → NLI. Ucuz ve kesin olan önce çalışır; pahalı ve bulanık olan sadece artakalanı görür. |
| D3 | **Sessizlik hatadır.** | Bir kontrol çalışmadıysa (timeout, parse hatası, ağ hatası) sonuç "geçti" değil `doğrulanamadı(çalışmadı)` olur. Fail-open yasak. |
| D4 | **Etiket veri modelinin parçasıdır, sunumun süsü değildir.** | Etiket atomda saklanır, kenarlara ve transferlere yayılır (§4.3), sorgu filtresi olarak kullanılabilir. |

---

## 1. Çapa doğrulama (anchor verification)

### 1.1 Doğrulanacak nesne

Her atom minimum şu çapa alanlarını taşır (tam atom şeması `01-bilgi-modeli.md`'de):

```
anchor {
  book_id      : uuid
  edition_hash : sha256   # baskı değişirse çapa geçersizdir
  page         : int      # basılı sayfa no
  page_index   : int      # PDF fiziksel sayfa no (offset ayrı tutulur)
  char_span    : [start, end]   # normalize edilmiş sayfa metni üzerinde
  quote        : string   # ≤ 300 karakter, kitaptan BİREBİR
  quote_sha    : sha256(normalize(quote))
}
```

**Kural:** `quote` alanı boş olan atom hiçbir zaman doğrulama kapılarına bile girmez —
üretim aşamasında şema reddi (schema rejection) ile geri çevrilir.

### 1.2 Normalizasyon (N) — her karşılaştırmadan önce

Sayfa metni ve alıntı **aynı** fonksiyondan geçer. Aksi halde eşleşme oranı sahte düşer.

```
N(s):
  unicode NFKC
  ligatür açma: ﬁ→fi, ﬂ→fl, ﬀ→ff
  tırnak/tire birleştirme: “ ” ‘ ’ → " '   ; – — ‐ → -
  satır sonu tirelemesi kapatma:  "integ-\nral" → "integral"
  tüm boşluk dizileri → tek boşluk
  sayfa üstbilgi/altbilgi/sayfa numarası şeritlerini at (düzen analizinden gelen kutu bilgisiyle)
  Türkçe için: casefold (i/İ tuzağına dikkat, lower() değil casefold())
  matematik satırları için: $...$ içeriği KORUNUR, sadece boşluk normalize edilir
```

### 1.3 Boru hattı — beş kapı, sırayla

```
V1  SPAN-EXACT      quote_sha, sayfanın kayan pencere hash'lerinden birine eşit mi?
                    Evet → span kesin. O(n), mikrosaniye.
V2  SPAN-FUZZY      Değilse: rapidfuzz partial_ratio_alignment ile en iyi hizalama.
                    score ≥ 0.92 → span kabul, düzeltilmiş span'i atoma GERİ YAZ.
                    0.75 ≤ score < 0.92 → OCR şüphesi → §7'ye yönlendir.
                    score < 0.75 → quote uydurulmuş. ATOM REDDEDİLİR (silinir, karantina bile değil).
V3  LEXICAL-COVER   Atomun claim_text'indeki içerik sözcükleri (stopword ve
                    fonksiyon sözcükleri çıkarıldıktan sonra) ne kadarı ±1 sayfalık
                    pencerede geçiyor? cover = |içerik ∩ pencere| / |içerik|
                    cover < 0.45 → atom metni alıntıdan kopmuş, NLI'ya zorunlu gönder.
V4  NLI-ENTAIL      premise = ±1 sayfa penceresi (≈1500 token), hypothesis = claim_text.
                    P(entailment) ≥ 0.90 ve P(contradiction) ≤ 0.02 → DESTEKLENDİ.
                    P(contradiction) > 0.15 → ÇELİŞKİ BAYRAĞI (atom kitabın kendisiyle çelişiyor).
V5  NUMBER-GUARD    claim_text'teki her sayı, tarih, birim, özel isim ve matematiksel
                    sembol pencerede birebir (veya bilinen eşdeğer formda) geçiyor mu?
                    Geçmeyen tek bir sayı bile → atom `doğrulanamadı(sayı)`.
```

`V5` küçük ama en yüksek getirili kapıdır: LLM'lerin en sık uydurduğu şey cümlenin
tamamı değil, cümlenin **içindeki sayıdır** ("%23" → "%32", "1908" → "1912").

### 1.4 Karar tablosu

| V1/V2 | V3 | V4 | V5 | Sonuç etiketi |
|---|---|---|---|---|
| exact | ≥0.45 | — | geçti | `doğrulandı(alıntı)` |
| fuzzy ≥0.92 | ≥0.45 | — | geçti | `doğrulandı(alıntı)` |
| fuzzy ≥0.92 | <0.45 | entail ≥0.90 | geçti | `desteklendi(NLI)` |
| fuzzy ≥0.92 | herhangi | entail <0.90 | — | `doğrulanamadı(destek yok)` |
| herhangi | herhangi | contradiction >0.15 | — | `doğrulanamadı(çelişki)` + insan kuyruğu |
| herhangi | herhangi | — | başarısız | `doğrulanamadı(sayı)` |
| fuzzy <0.75 | — | — | — | **atom imha** (log'a düşer, ürüne girmez) |

### 1.5 Sözde-kod

```python
def verify_anchor(atom, book):
    page = N(book.page_text(atom.anchor.page_index))
    q    = N(atom.quote)

    span = exact_span(page, q) or fuzzy_span(page, q)   # (span, score)
    if span is None or span.score < 0.75:
        return REJECT("quote_not_in_page", score=span.score if span else 0)
    atom.anchor.char_span = span.range                   # düzeltilmiş span geri yazılır
    if 0.75 <= span.score < 0.92:
        return LABEL("doğrulanamadı(ocr_şüphesi)", route=OCR_QUEUE)

    window = N(book.window(atom.anchor.page_index, radius=1))

    if not numbers_and_symbols_subset(atom.claim_text, window):
        return LABEL("doğrulanamadı(sayı)")

    if lexical_cover(atom.claim_text, window) >= 0.45:
        return LABEL("doğrulandı(alıntı)")

    nli = NLI(premise=window, hypothesis=atom.claim_text)   # kalibre edilmiş sınıflandırıcı
    if nli.contradiction > 0.15:  return LABEL("doğrulanamadı(çelişki)", route=HUMAN_QUEUE)
    if nli.entailment  >= 0.90:   return LABEL("desteklendi(NLI)")
    return LABEL("doğrulanamadı(destek yok)")
```

**Karar:** NLI için ayrı, küçük ve *kalibre edilmiş* bir sınıflandırıcı kullanılır
(DeBERTa-v3-large-mnli sınıfı bir çapraz-kodlayıcı, kendi altın kümemizde yeniden
kalibre edilmiş). Gerekçe: aynı aileden büyük bir LLM'e "bu destekleniyor mu?" diye
sormak, üreticiyle korele hata yapar — bağımsızlık kaybolur.
`AÇIK SORU:` Türkçe kitaplarda NLI kalitesi İngilizceye göre düşük olabilir; Türkçe
için eşiği 0.90 → 0.93 çekip `desteklendi(NLI)` oranını ölçmek gerekiyor.

---

## 2. Sembolik formül doğrulama (SymPy)

### 2.1 Formül atomunun zorunlu şeması

```
formula_atom {
  latex        : "\\tau = I\\alpha"
  sympy_src    : "Eq(tau, I*alpha)"          # parse edilebilir olmak ZORUNDA
  symbols      : [ {name:"tau", unit:"N*m",     domain:"real"},
                   {name:"I",   unit:"kg*m**2", domain:"positive"},
                   {name:"alpha",unit:"rad/s**2",domain:"real"} ]
  assumptions  : ["rigid_body", "fixed_axis"]  # metinden çıkarılan geçerlilik koşulları
  anchor       : {...}
}
```

`sympy_src` veya `symbols[].unit` eksikse formül **doğrulanamaz** kabul edilir; tahmin
edilmez. Birim uydurmak, formül uydurmaktan daha sinsi bir hatadır.

### 2.2 Dört kontrol

**(a) Boyut/birim tutarlılığı.** Her sembolün birimi 7 boyutlu SI vektörüne
(M, L, T, I, Θ, N, J) çevrilir; ifade ağacı üzerinde boyut aritmetiği yapılır.

```
dim(a+b) : dim(a) == dim(b) değilse HATA(boyut_toplama)
dim(a*b) : dim(a) + dim(b)
dim(a**n): n boyutsuz ve rasyonel olmalı; değilse HATA(üs_boyutlu)
exp/log/sin/cos/tanh argümanı: dim == 0 olmalı; değilse HATA(aşkın_fonksiyon_boyutlu)
Eq(l, r) : dim(l) == dim(r) olmalı
```
Uygulama: `pint` + SymPy ağaç yürüyüşü. Salt matematik formüllerinde (birimsiz) bu
kontrol atlanır ve `unit: "1"` yazılır — atlama sessiz değil, kayda geçer.

**(b) Cebirsel özdeşlik.** Kitap "A = B" diyorsa:
```
d = simplify(A - B)
d == 0  → geçti
değilse: sırayla ratsimp, trigsimp, powsimp, radsimp, cancel dene (her biri 5 sn timeout)
hepsi başarısız → (c)'ye düş
```
Timeout, "yanlış" değildir; `doğrulanamadı(timeout)` olur (D3).

**(c) Sayısal örneklemeli sağlama.** Cebir çözemediğinde ampirik kanıt:
```
N = 200 rastgele nokta, her sembolün domain'ine saygılı
   (positive → logüniform 1e-3..1e3, real → ±1e3, integer → 1..50)
mpmath ile 50 basamak hassasiyette değerlendir
kabul: |A-B| ≤ 1e-30 + 1e-25 * max(|A|,|B|)   (bağıl tolerans)
başarısız nokta ≥ 1 → FORMÜL YANLIŞ (veya hipotez eksik) → karşı-örneği sakla
tanımsız nokta > %20 → örnekleme alanı hatalı, domain çıkarımını gözden geçir
```
200 nokta *kanıt değildir*, ama tek bir karşı örnek **çürütmedir** — ve asimetri bizim
lehimizedir. Bu yüzden `doğrulandı(sembolik)` etiketi sadece (a)+(b) geçtiğinde verilir;
sadece (c) geçerse etiket `desteklendi(sayısal)` olur (arayüzde `desteklendi` ailesinde gösterilir).

**(d) Sınır durum testleri.** Her formül için otomatik üretilen 6 test:
```
1. Sıfır testi:        her değişken → 0 (tanımlıysa)
2. Tekillik taraması:  denominator(expr) == 0 çözümleri; her kök için limit hesapla
3. Sonsuzluk davranışı: limit(expr, x, oo) ve limit(expr, x, -oo) sonlu/beklenen mi
4. İşaret testi:       domain=positive sembollerle sonuç işareti metindeki iddiayla uyumlu mu
5. Özel durum:         bilinen indirgeme (v<<c → klasik limit, x→0 → Taylor 1. terim)
6. Ölçek değişmezliği: boyutsuz grup varsa (Reynolds vb.) ölçekleme altında korunuyor mu
```
Bulunan her tekillik atoma `singularities: [...]` olarak yazılır ve bu, önkoşul DAG'ında
"bu formül x=L'de geçersiz" uyarısına dönüşür.

### 2.3 Doğrulanamayan formüller ne olur?

| Durum | Etiket | Ürün davranışı |
|---|---|---|
| (a)+(b) geçti | `doğrulandı(sembolik)` | Tam yetki: türev iddia üretebilir, transfer kurabilir. |
| (a) geçti, (b) çözemedi, (c) geçti | `desteklendi(sayısal)` | Gösterilir, "sayısal olarak sağlandı" notu; türev iddia üretemez. |
| (a) başarısız | `doğrulanamadı(boyut)` | **Kırmızı bayrak.** İnsan kuyruğuna girer. Boyut hatası ya OCR ya çıkarım hatasıdır; ikisi de düzeltilebilir. |
| (c) karşı örnek buldu | `doğrulanamadı(çürütüldü)` | Karantina + karşı örnek kaydedilir. Sıklıkla sebep **düşürülmüş hipotezdir** → §3'e yönlendirilir. |
| parse/timeout | `doğrulanamadı(çalışmadı)` | Karantina, yeniden deneme kuyruğu. |

**Karantinanın anlamı (kesin tanım):** atom veritabanında kalır, ham alıntısıyla
görüntülenebilir, ama (1) graf kenarı kuramaz, (2) transfer önerisi üretemez,
(3) günlük plan satırına giremez, (4) başka bir atomun kanıtı olarak gösterilemez.
Brifing Kural 3 gereği kitap reddedilmez — sadece o *atom* susturulur.

---

## 3. Teorem bütünlüğü — sessiz hipotez düşürme

Bu, sistemin en tehlikeli hata sınıfıdır. "Her sürekli fonksiyon düzgün süreklidir"
cümlesi, "kompakt kümede" düşünce yanlış olur ve **hiçbir string eşlemesi bunu yakalamaz** —
çünkü cümlenin her kelimesi kitapta geçiyordur.

### 3.1 Zorunlu ayrık şema

Teorem atomu tek bir metin bloğu olarak **saklanamaz**:

```
theorem_atom {
  name        : "Heine-Cantor"
  hypotheses  : [ {text:"X kompakt metrik uzay", anchor:{page:212, span:[...]}, kind:"nesne"},
                  {text:"f: X→Y sürekli",        anchor:{page:212, span:[...]}, kind:"nesne"} ]
  conclusion  : {text:"f düzgün süreklidir",     anchor:{page:212, span:[...]}}
  quantifiers : ["∀ε>0 ∃δ>0"]
  scope       : "metrik uzaylar"
  counterexample_if_dropped : { "X kompakt": "f(x)=1/x, X=(0,1]" }   # varsa
}
```
`hypotheses` dizisi boş olan bir teorem atomu şema düzeyinde reddedilir. Hipotezsiz
teorem yoktur; gerçekten yoksa o bir *tanım* veya *aksiyom*dur, farklı atom tipidir.

### 3.2 Sessiz düşürmeyi yakalayan dört detektör

**H1 — Koşul sözlüğü taraması (deterministik, ucuz).**
Alanına göre bakım yapılan bir tetikleyici sözlük tutulur:
```
analiz    : kompakt, sınırlı, kapalı, sürekli, düzgün, ölçülebilir, integrallenebilir,
            hemen her yerde, mutlak yakınsak, monoton, Lipschitz, türevlenebilir
cebir     : değişmeli, birimli, sonlu üretilmiş, Noetherian, karakteristik ≠ 2, tersinir
olasılık  : bağımsız, aynı dağılımlı (i.i.d.), sonlu varyans, ölçülebilir, sıfır ortalama
lineer cbr: pozitif tanımlı, simetrik, tam ranklı, tekil olmayan, ortonormal
mühendis. : kararlı durum, laminer, adyabatik, küçük genlik, rijit, izotropik
```
Kural: bu sözcüklerden biri, teoremin çapa penceresinde (±3 cümle) geçiyor **ve**
`hypotheses[]` içinde geçmiyorsa → `hipotez_şüphesi` bayrağı. Kesin değil ama recall'ü yüksek.

**H2 — İki geçişli, çapraz-görmez çıkarım (independent re-extraction).**
Geçiş 1: teoremin ifadesini çıkarır. Geçiş 2: **ayrı bir çağrı**, ayrı prompt, geçiş 1'in
çıktısını görmeden, aynı sayfadan *sadece koşulları* çıkarır ("bu ifadenin geçerli olması
için sayfada belirtilen tüm ön koşulları listele"). İki listenin farkı (`H2 \ H1`) doğrudan
düşürülmüş hipotez adayıdır. Fark boş değilse insan kuyruğu değil, **otomatik birleştirme**
yapılır ve birleşik hipotezler yeniden V1–V5'ten geçirilir.

**H3 — Karşı-örnek bankası (en güçlü ve tamamen mekanik).**
Kanonik teoremler için "hipotez X düşerse çöker" karşı örnekleri elle küratörlenmiş bir
bankada tutulur (ilk sürüm: analiz + lineer cebir + olasılıktan ~150 giriş). Sistem bir
teorem atomunu bankadaki bir imzayla eşleştirirse (isim veya sonuç cümlesi benzerliği),
bankadaki hipotez listesini **beklenen küme** olarak alır ve eksikleri sayar.
Eksik varsa → `doğrulanamadı(hipotez eksik)`, eksik hipotez adı kullanıcıya gösterilir.

**H4 — Sayısal çürütme geri beslemesi.**
§2.2(c) bir karşı örnek bulduğunda, bu karşı örneğin hangi kısıtı ihlal ettiği aranır
(örn. karşı örnek noktası `x=0`, ve `x≠0` hipotezde yok). Bulunursa hipotez otomatik
önerilir ve H2 döngüsüne geri verilir.

### 3.3 Sunum kuralı

Teorem hiçbir yerde hipotezlerinden ayrı gösterilmez. Kart formatı sabittir:

```
[VARSAYIMLAR]  X kompakt metrik uzay · f sürekli
[SONUÇ]        f düzgün süreklidir
[KAYNAK]       Rudin, Bl.4, s.212   [doğrulandı(alıntı)]
```
Yer darsa sonuç kısaltılır, **varsayımlar kısaltılmaz**. Bu, `06-arayuz.md` için bağlayıcı
bir kısıttır: "bir ekran = bir karar" doktrini hipotez gizlemeyi meşrulaştırmaz.

---

## 4. Güven etiketleme

### 4.1 Dört etiket — kesin üretim koşulları

| Etiket | Ne zaman verilir | Anlamı (kullanıcıya) |
|---|---|---|
| `doğrulandı(sembolik)` | Formül: boyut ✓ + cebirsel özdeşlik ✓ | "Makine bunu matematiksel olarak sağladı." |
| `doğrulandı(alıntı)` | V1/V2 span ✓ + V5 sayı ✓ + V3 kapsama ≥0.45 | "Bu cümle kitapta bu sayfada yazıyor." |
| `desteklendi(NLI)` | span ✓ + V5 ✓ + NLI entail ≥0.90 (ve sayısal-sağlama sonuçları) | "Kitap bunu söylüyor ama başka kelimelerle; bu bizim ifademiz." |
| `doğrulanamadı` | Yukarıdakilerin hiçbiri, veya çelişki/timeout/OCR şüphesi | "Emin değiliz. Ham metne kendin bak." |

Ara etiket, yüzde, yıldız, 0–1 skoru **yoktur**. Dört kova, bitti. Kalibre edilmemiş bir
sayı göstermek, hiçbir şey göstermemekten kötüdür.

### 4.2 Arayüz talimatı (`06-arayuz.md` için normatif)

1. **Sessiz varsayılan:** `doğrulandı(*)` atomlar rozet **taşımaz**. Doğruluk normdur;
   norm görsel gürültü üretmemeli. (Kural 1 ile uyum.)
2. **`desteklendi(NLI)`** ince gri kesikli sol kenarlık taşır. Tıklanınca kaynak paragraf açılır.
3. **`doğrulanamadı`** kehribar sarısı üçgen + tek kelime etiket taşır ve **her zaman**
   yanında birebir alıntı görünür. Bizim yeniden yazımımız gösterilmez, ham metin gösterilir.
4. **Yasak:** `doğrulanamadı` atom günlük plan satırına (Kural 4), transfer önerisine ve
   "yenilik" hükmüne (%94 hesabına) **giremez**. Bunlar sadece doğrulanmış atomlar üzerinden hesaplanır.
5. **Çapa her zaman tek tık ötede:** her atomun altında `Kitap · Bl.N · s.P` metni; tık →
   sayfa görüntüsü + vurgulanmış span. Çapa görünür değilse atom görünmez.
6. **Renk anlamı sabittir:** kehribar = doğrulanamadı, kırmızı = çelişki (§5 D4).
   Kırmızı başka hiçbir şey için kullanılmaz.
7. **Toplu gösterim:** kitap kartında tek satır sağlık göstergesi:
   `1.184 atom · 96% doğrulandı · 41 karantinada`. Bu satır tıklanabilir bir filtredir.

### 4.3 Etiket yayılımı (propagation)

Türetilmiş her nesne, dayandığı atomların **en zayıf** etiketini alır:

```
label(kenar)     = min(label(atom_a), label(atom_b))       # sıra: sembolik > alıntı > NLI > yok
label(transfer)  = min over kaynak atomlar
label(plan satırı) = min over gösterilen her şey ;  = doğrulanamadı ise satır ÜRETİLMEZ
```
Bir çelişki kenarı özel durumdur: iki uç da `doğrulandı(alıntı)` ise çelişki **gerçektir**
(iki kitap birbiriyle çelişiyor) ve ürünün en değerli çıktılarından biridir — bastırılmaz,
öne çıkarılır. Uçlardan biri `doğrulanamadı` ise çelişki muhtemelen bizim hatamızdır → gizlenir.

---

## 5. Uydurma savunma katmanları

Beş bağımsız katman. Bağımsızlık kritik: aynı hata modunu paylaşan iki katman, bir katmandır.

| # | Katman | Yakalar | **Kaçırır** | Maliyet |
|---|---|---|---|---|
| **D1** | Çapa + alıntı eşleme (§1) | Tamamen uydurulmuş cümle; var olmayan sayfa; değiştirilmiş sayı/tarih | Kitapta gerçekten yazan ama **yanlış bağlamdan** alınmış cümle (yazarın çürütmek için kurduğu "kötü argüman" alıntısı) | Çok düşük (CPU) |
| **D2** | Sembolik doğrulama (§2) | Yanlış kopyalanmış formül, boyut hatası, işaret hatası, eksik katsayı | Boyutsal olarak tutarlı ama kavramsal olarak yanlış formül; kitabın kendi hatası | Düşük (CPU, ~2 sn/formül) |
| **D3** | Bağımsız yeniden çıkarım (self-consistency) | Kararsız/rastlantısal halüsinasyon; hipotez düşürme (§3 H2); atom sınırı kayması | **Sistematik** halüsinasyon — model aynı hatayı iki kez yapar (özellikle popüler ama yanlış hatırlanan teoremlerde) | Yüksek (LLM çağrısı ×2) |
| **D4** | Graf-içi çelişki taraması | Aynı kitabın iki yerinden çelişik iddia; kütüphanedeki yerleşik bilgiyle çatışma; birim/mertebe tutarsızlığı | Kütüphanenin tamamı aynı yanlışı içeriyorsa (ortak yanılgı); grafta henüz komşusu olmayan yeni alan | Orta (gömme + kNN, atom başına) |
| **D5** | Tuzak (canary) ve negatif kontrol | Uyum eğilimi (sycophancy) ve boşluk doldurma: kitapta olmayan bölüm/kavram sorulur, model "bulursa" o çıkarım turu şüpheli işaretlenir | Sadece **çıkarım turunun** sağlığını ölçer, tek tek atomları değil | Çok düşük (tur başına 3-5 sorgu) |
| **D6** | Kullanıcı geri bildirimi ("bu yanlış" tek tık) | Uzman gözünün gördüğü her şey; uzun kuyruk | Kullanıcının bilmediği alan; sessiz kullanıcı | Sıfır (asenkron) |

**Katman tasarımı gerekçesi:** D1 ve D2 deterministiktir ve modelden bağımsızdır — bunlar
zemindir. D3 model kaynaklı gürültüyü siler ama model kaynaklı **önyargıyı** silemez;
onu D4 (dış tutarlılık) ve D5 (davranışsal sınama) yakalar. D6 uzun vadede altın kümeyi besler.

**AÇIK SORU:** D1'in kaçırdığı "yanlış bağlam" hatası (yazarın reddettiği bir görüşü
yazarın görüşü diye sunmak) için bir polarite/atıf detektörü gerekiyor. İlk sürümde
"göre", "iddia eder", "savunanlar", "yanılgı" gibi atıf işaretleyicileri sayfa penceresinde
aranıp atoma `attribution_risk: true` düşülmesini öneriyorum; tam çözüm sürüm 2.

---

## 6. Değerlendirme takımı (eval harness)

### 6.1 Altın standart veri kümesi

**Kapsam:** 12 kitap × 20 sayfa = 240 sayfa. Kitap dağılımı brifingdeki kullanıcı profiline
göre ağırlıklandırılır: 5 matematik/mühendislik, 2 tıp, 2 tarih/felsefe, 1 sanat,
1 kişisel gelişim, 1 **kasıtlı kötü tarama** (§7 testi için).

**Sayfa seçimi (yanlılık önleme):** rastgele değil, **tabakalı**: her kitaptan
5 yoğun-matematik sayfası, 5 düz nesir, 5 tablo/şekil içeren, 5 rastgele. Rastgele
örnekleme matematik sayfalarını yeterince temsil etmez ve tam da orada hata yapıyoruz.

**Etiketleme protokolü:** her sayfa 2 bağımsız insan tarafından atomlaştırılır
(iddia/tanım/teorem/yöntem/formül/anekdot + çapa). Anlaşmazlık üçüncü kişi tarafından çözülür.
Kabul kapısı: atom sınırlarında Cohen κ ≥ 0.70; altında ise **rehber yeniden yazılır**,
veri kümesi kabul edilmez. Ölçemediğimiz tutarlılıkla sistem ölçemeyiz.

**Ek küme — çekişmeli (adversarial) set, 150 örnek, elle üretilir:**
```
A1  hipotezi düşürülmüş 40 teorem      (beklenen: doğrulanamadı/hipotez eksik)
A2  sayısı değiştirilmiş 30 iddia      (beklenen: V5 yakalar)
A3  bozulmuş 30 formül (işaret/üs/katsayı)  (beklenen: D2 yakalar)
A4  var olmayan sayfaya çapalanmış 25 atom  (beklenen: V1/V2 imha)
A5  bağlamı ters çevrilmiş 25 alıntı        (beklenen: bilinen zayıflık, ölç)
```

### 6.2 Metrikler

| Metrik | Tanım | Neden |
|---|---|---|
| **Atom precision** | üretilen ∩ altın / üretilen | Uydurma atom oranı |
| **Atom recall** | üretilen ∩ altın / altın | Kaçırılan fikir oranı |
| **Anchor accuracy@page** | doğru sayfaya çapalı atom oranı | Kural 2'nin doğrudan ölçümü |
| **Span IoU** | span kesişim/birleşim ortalaması | Vurgulamanın kalitesi |
| **Hallucination rate (kritik)** | `doğrulandı(*)` etiketli ama insan "yanlış" diyen atom oranı | **En önemli metrik.** Yanlış güven verilen oran. |
| **Hypothesis completeness** | teoremlerde çıkarılan hipotez / altın hipotez | §3'ün ölçümü |
| **Contradiction detection rate** | A1+A3 çekişmeli kümede yakalanan / toplam | Savunmanın etkinliği |
| **False quarantine rate** | doğru olduğu halde `doğrulanamadı` olan oran | Aşırı-savunmanın maliyeti |
| **ECE (calibration)** | Etiket kovaları arasında gerçek doğruluk monoton mu | Etiketler anlamlı mı |

Atom eşlemesi için: gömme benzerliği ≥ 0.85 **ve** çapa aynı sayfada → eşleşti sayılır.

### 6.3 Kabul eşikleri (yayın kapısı)

| Metrik | Eşik | Aşılmazsa |
|---|---|---|
| Hallucination rate (kritik) | **≤ 0.5%** | **Yayın yok.** Pazarlık edilemez. |
| Anchor accuracy@page | ≥ 98% | Yayın yok |
| Hypothesis completeness (mat/müh) | ≥ 95% | Matematik kitapları için özellik kapatılır |
| Atom precision | ≥ 90% | Yayın yok |
| Atom recall | ≥ 70% | Uyarı; recall düşük olabilir (Kural 3: sıkıştırma) |
| Contradiction detection rate | ≥ 85% | Uyarı + savunma katmanı revizyonu |
| False quarantine rate | ≤ 8% | Uyarı; eşikler gevşetilir |
| Etiket monotonluğu | doğrulandı > desteklendi > doğrulanamadı, her ikili arasında ≥ 10 puan fark | Etiket şeması yeniden tasarlanır |

**Recall neden düşük tutulabilir:** ürün her fikri çıkarmak zorunda değil, çıkardığını
doğru çıkarmak zorunda. Precision için recall feda edilir — tersi asla.

### 6.4 Regresyon kapısı (CI)

Her PR'de altın kümenin sabit 200 atomluk alt kümesi + tüm çekişmeli küme koşar.
Bütçe: ≤ 6 dakika, ≤ 2 USD. Hallucination rate bir önceki `main`'e göre **artarsa** merge bloklanır.
Kural: doğrulama boru hattına dokunan hiçbir PR eval koşmadan birleştirilemez.

---

## 7. Bozuk girdi: OCR, kırık LaTeX, kötü tarama

### 7.1 Sayfa sağlık skoru (page health) — sindirimden ÖNCE

Her sayfa metni için 6 sinyal, LLM çağrısından önce, saf CPU ile:

```
s1 sözlük oranı      : sözlükte bulunan token / toplam token   (TR+EN sözlük, alan sözlüğü)
s2 tek-karakter oranı: yalnız harf tokenlarının oranı ("l ntegra l" tipi bozulma)
s3 kontrol/çöp karakter oranı: � ve tanımsız glif oranı
s4 ortalama kelime uzunluğu: normalden ±3σ sapma (birleşmiş/parçalanmış kelime)
s5 satır sonu tutarlılığı: tirelenmiş satır oranı, aşırıysa sütun bölme hatası
s6 matematik bütünlüğü : $ sayısı tek mi, \begin/\end eşleşiyor mu, parantez dengesi
```

```
health = 0.35*s1 + 0.15*(1-s2) + 0.20*(1-s3) + 0.10*f(s4) + 0.10*(1-s5) + 0.10*s6
```

### 7.2 Üç seviyeli karantina

| Seviye | Koşul | Davranış |
|---|---|---|
| **TEMİZ** | health ≥ 0.85 | Normal boru hattı. |
| **ŞÜPHELİ** | 0.60 ≤ health < 0.85 | Sindirim yapılır ama üretilen tüm atomlar tavanı `desteklendi(NLI)` ile sınırlanır — `doğrulandı(alıntı)` verilemez. Fuzzy eşik 0.92 → 0.88'e gevşetilir (OCR gürültüsü toleransı). |
| **KARANTİNA** | health < 0.60 | Sindirim **yapılmaz**. Sayfa OCR yeniden işleme kuyruğuna girer. Kullanıcıya: "s.113–140 okunamadı, yeniden taranması gerekiyor" — sessizce atlanmaz. |

### 7.3 Kırık LaTeX / matematik

```
1. Parse kapısı: latex2sympy → SymPy AST. Başarısızsa formül atomu ÜRETİLMEZ,
   bunun yerine "matematiksel içerik var, okunamadı" işareti bırakılır.
2. Yaygın OCR→LaTeX düzeltme sözlüğü (deterministik, sınırlı, kayıt altında):
   "∫" ↔ "f", "Σ" ↔ "E", "≤" ↔ "<", "α" ↔ "a", "μ" ↔ "u", "−" ↔ "-", "'" ↔ "′"
   Her düzeltme atoma `ocr_repairs: [...]` olarak yazılır; ≥3 düzeltme yapıldıysa
   formül otomatik `doğrulanamadı(ocr)` olur.
3. Onarım ASLA LLM'e "bunu düzelt" diye bırakılmaz — LLM burada makul ama yanlış
   formül üretmekte çok iyidir ve bu hata tipi hiçbir katmana yakalanmaz.
4. Boyut kontrolü (§2.2a) burada ikinci görev yapar: OCR bozulmuş formüllerin çoğu
   boyutsal olarak tutarsızdır. Boyut kapısı, sessiz OCR hatasının en iyi dedektörüdür.
```

### 7.4 Sayfa numarası kayması (page offset)

Basılı sayfa numarası ile PDF indeksi arasındaki fark otomatik kalibre edilir: ilk 30
sayfada üstbilgi/altbilgi'den sayı çıkarılır, mod bulunur, offset sabitlenir; roma
rakamlı ön bölüm ayrı ele alınır. Offset ≥ 3 sayfada tutarsızsa kitap `çapa_güvensiz`
işaretlenir ve **tüm** atomları `desteklendi(NLI)` tavanına iner. Yanlış sayfa numarası
veren bir çapa, çapasızlıktan kötüdür.

---

## 8. Maliyet

### 8.1 Varsayımlar

400 sayfalık teknik kitap, ≈180.000 token, ≈1.200 atom, ≈120 formül, ≈60 teorem.
Fiyat birim varsayımı (`AÇIK SORU:` yayın öncesi güncel fiyat listesinden doğrulanmalı):
küçük model ≈ 1 USD / M girdi-token, büyük model ≈ 3 USD / M girdi-token mertebesi.
Aşağıdaki rakamlar **mertebe tahminidir**, sözleşme değildir.

### 8.2 Katman katman ek maliyet (kitap başına)

| Kontrol | Kapsam | Mekanizma | Ek maliyet |
|---|---|---|---|
| V1/V2 span eşleme | **her atom** | CPU (rapidfuzz) | ~0 USD, ≈8 sn |
| V3 kapsama | **her atom** | CPU | ~0 USD |
| V5 sayı koruması | **her atom** | CPU + regex | ~0 USD |
| Sayfa sağlık skoru | **her sayfa** | CPU | ~0 USD, ≈5 sn |
| V4 NLI | **sadece V3 < 0.45 olanlar** (≈%20 ≈ 240 atom) | küçük çapraz-kodlayıcı, kendi barındırdığımız | ≈0.01 USD, ≈40 sn GPU / ≈4 dk CPU |
| §2 SymPy (a,b,c,d) | **her formül** (120) | CPU, 10 sn timeout | ~0 USD, ≈6 dk |
| §3 H1 sözlük | **her teorem** | CPU | ~0 USD |
| §3 H2 çift geçiş | **sadece teorem+formül atomları** (180) | LLM, ≈500 tok/atom | ≈0.10–0.30 USD |
| §3 H3 karşı-örnek bankası | **her teorem** | CPU eşleme | ~0 USD |
| D4 graf çelişki | **her doğrulanmış atom** | gömme + kNN | ≈0.02 USD |
| D5 tuzak sorgular | **kitap başına 5 sorgu** | LLM | ≈0.01 USD |
| D3 tam çift-çıkarım | **örnekleme: %5 atom** | LLM | ≈0.15 USD |
| **Toplam ek** | | | **≈0.30–0.50 USD/kitap, ≈10-15 dk CPU** |

Referans: sindirim katmanının kendisi (180K token okuma + atom üretimi) kitap başına
kabaca 1.5–3 USD mertebesindedir. **Doğrulama, sindirimin %15–25'i kadar ek maliyet getirir.**
Bu, ürünün tek farklılaştırıcısı için ödenecek en ucuz bedeldir.

### 8.3 Her atoma mı, örnekleme mi? — karar kuralı

```
HER ATOMA (istisnasız):
  - deterministik ve maliyeti ~0 olan her kontrol (V1,V2,V3,V5, sağlık, H1, H3)
  - hata sonucu "zehirli" olan her kontrol: formüllerde §2, teoremlerde §3
  Gerekçe: maliyet sıfıra yakınsa örnekleme yapmak sadece hata kaçırmaktır.

ÖRNEKLEME (yalnız bunlar):
  - D3 tam çift-çıkarım: %5 rastgele + %100 (formül ∪ teorem ∪ D4-bayraklı)
  - İnsan denetimi: kitap başına 20 atom, hallucination rate tahmini için
  Örnekleme oranı sabit değil, ADAPTİFTİR:
     kitabın son 100 atomunda hata oranı > %2  →  oran %5 → %25
     sağlık skoru ortalaması < 0.85            →  oran ×2
     yeni bir alan/yayınevi/OCR profili        →  ilk kitap için oran %100
```

### 8.4 Bütçe koruması

Doğrulama maliyeti sindirim maliyetinin %40'ını aşarsa boru hattı durur ve olay kaydı
üretilir. Sınırsız doğrulama bütçesi, sınırsız yeniden deneme demektir; yeniden denemenin
kendisi bir hata sinyalidir ve gizlenmemelidir.

---

## 9. Diğer uzmanlara bağlayıcı çıktılar

| Belge | Talep |
|---|---|
| `01-bilgi-modeli.md` | Atom şeması `quote`, `quote_sha`, `char_span`, `edition_hash`, `label` alanlarını **zorunlu** içermeli. Teorem atomu `hypotheses[]`/`conclusion` ayrımını şema düzeyinde zorlamalı. Modelin öz-güven skoru şemada **yer almamalı**. |
| `02-yenilik-ve-graf.md` | Kenar kurma yalnız `doğrulandı(*)` ∪ `desteklendi(*)` atomlar üzerinde. "%94 zaten var" hesabı karantina atomlarını **paydaya da paya da** katmamalı. |
| `04-mimari.md` | Doğrulama ayrı ve senkron bir kapı (gate) olmalı, asenkron "sonra bakarız" işi değil. Etiketsiz atom API'den çıkamaz. |
| `06-arayuz.md` | §4.2'deki 7 madde bağlayıcıdır. |
| `08-veri-sistemi.md` | Etiket ve `verification_run_id` sürümlenmeli: eşikler değiştiğinde eski etiketler geçersizleşir ve yeniden değerlendirme kuyruğa girer. |
| `05a/05b/05c/05d` | Her alan uzmanı kendi §3.2-H1 tetikleyici sözlüğünü ve varsa karşı-örnek bankası girdilerini vermeli. |

## 10. Açık sorular

1. `AÇIK SORU:` Türkçe NLI kalitesi ölçülmedi; eşikler dil bazında ayrılmalı mı?
2. `AÇIK SORU:` "Yanlış bağlam" (yazarın çürüttüğü görüşü ona atfetme) için polarite
   detektörünün tasarımı sürüm 2'ye bırakıldı — ölçülmemiş bir risk.
3. `AÇIK SORU:` Kitabın **kendisi yanlışsa** ne olur? Şu an sistem kitaba sadıktır ve
   bunu doğru sayar. D4 çelişki kenarı bunu bir gün yakalar; ama "hangi kitap haklı"
   kararı bu belgenin kapsamı dışında ve `07-transfer.md` ile ortak çözülmeli.
4. `AÇIK SORU:` Karşı-örnek bankasının bakım maliyeti (150 girdi × alan uzmanı saati)
   bütçelenmedi.
