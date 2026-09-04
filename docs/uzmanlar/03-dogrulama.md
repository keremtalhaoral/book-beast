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

## 0. Temel doktrin — 5 madde

| # | İlke | Sonucu |
|---|------|--------|
| D0 | **LLM'in "bu doğrudur" demesi kanıt değildir.** | Modelin öz-güven skoru (`confidence: 0.95`) hiçbir kapıya girdi olmaz; şemadan tamamen çıkarılmıştır. |
| D1 | **Doğrulayıcı üreticiden bağımsızdır.** | Doğrulayıcı yalnız (atom, ham sayfa metni) çiftini görür — üretimin gerekçesini görmez. |
| D2 | **Deterministik kontrol > olasılıksal kontrol.** | Sıra sabit: string eşleme → sembolik cebir → NLI. Ucuz ve kesin olan önce; pahalı ve bulanık olan sadece artakalanı görür. |
| D3 | **Sessizlik hatadır.** | Kontrol çalışmadıysa (timeout, parse, ağ) sonuç "geçti" değil `doğrulanamadı(çalışmadı)`dır. Fail-open yasak. |
| D4 | **Etiket veri modelinin parçasıdır.** | Atomda saklanır, kenarlara/transferlere yayılır (§4.3), sorgu filtresidir. |

## 1. Çapa doğrulama (anchor verification)

### 1.1 Doğrulanacak nesne

Her atom minimum şu çapa alanlarını taşır (tam atom şeması `01-bilgi-modeli.md`'de):

```
anchor {
  book_id: uuid ; edition_hash: sha256   # baskı değişirse çapa geçersizdir
  page: int (basılı) ; page_index: int (PDF fiziksel; offset ayrı tutulur)
  char_span: [start,end]                 # normalize edilmiş sayfa metni üzerinde
  quote: string ≤300 karakter, BİREBİR ; quote_sha: sha256(N(quote))
}
```

**Kural:** `quote` alanı boş olan atom doğrulama kapılarına bile girmez — üretim aşamasında
şema reddi (schema rejection) ile geri çevrilir.

### 1.2 Normalizasyon (N)

Sayfa metni ve alıntı **aynı** fonksiyondan geçer; aksi halde eşleşme oranı sahte düşer.

```
N(s):
  unicode NFKC · ligatür açma (ﬁ→fi, ﬂ→fl, ﬀ→ff)
  tırnak/tire birleştirme: “ ” ‘ ’ → " ' ; – — ‐ → -
  satır sonu tirelemesi kapatma: "integ-\nral" → "integral"
  boşluk dizileri → tek boşluk ; üstbilgi/altbilgi şeritlerini at (düzen analizi kutularıyla)
  Türkçe: casefold() — lower() DEĞİL (i/İ tuzağı)
  $...$ içeriği KORUNUR, sadece boşluğu normalize edilir
```

### 1.3 Boru hattı — beş kapı, sırayla

```
V1 SPAN-EXACT   quote_sha, sayfanın kayan pencere hash'lerinden birine eşit mi? Evet → span
                kesin (O(n), mikrosaniye).
V2 SPAN-FUZZY   Değilse rapidfuzz partial_ratio_alignment ile en iyi hizalama.
                ≥0.92 → span kabul, düzeltilmiş span'i atoma GERİ YAZ.
                0.75–0.92 → OCR şüphesi, §7'ye yönlendir.
                <0.75 → quote uydurulmuş; ATOM İMHA (karantina bile değil).
V3 LEX-COVER    claim_text'in içerik sözcüklerinin (stopword'süz) ne kadarı ±1 sayfalık
                pencerede geçiyor? cover = |içerik ∩ pencere| / |içerik|.
                cover < 0.45 → metin alıntıdan kopmuş, NLI zorunlu.
V4 NLI-ENTAIL   premise = ±1 sayfa penceresi (≈1500 token), hypothesis = claim_text.
                entail ≥0.90 ve contradiction ≤0.02 → DESTEKLENDİ.
                contradiction >0.15 → ÇELİŞKİ BAYRAĞI (atom kitabın kendisiyle çelişiyor).
V5 NUMBER-GUARD claim_text'teki her sayı, tarih, birim, özel isim ve matematik sembolü
                pencerede birebir (ya da bilinen eşdeğer formda) geçiyor mu?
                Geçmeyen tek bir sayı bile → `doğrulanamadı(sayı)`.
```

`V5` en yüksek getirili kapıdır: LLM'ler cümlenin tamamını değil, **içindeki sayıyı**
uydurur ("%23" → "%32", "1908" → "1912").

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

### 1.5 NLI seçimi

**Karar:** ayrı, küçük ve *kalibre edilmiş* bir çapraz-kodlayıcı (DeBERTa-v3-large-mnli
sınıfı, kendi altın kümemizde yeniden kalibre edilmiş). Gerekçe: aynı aileden büyük bir
LLM'e "bu destekleniyor mu?" diye sormak üreticiyle korele hata yapar — D1 bağımsızlığı ölür.
Uygulama notu: premise = ±1 sayfa penceresi; span düzeltmesi (`char_span`) her zaman
atoma geri yazılır; hiçbir kapı fail-open değildir (D3).
`AÇIK SORU:` Türkçe kitaplarda NLI kalitesi İngilizceye göre düşük olabilir; Türkçe
için eşiği 0.90 → 0.93 çekip `desteklendi(NLI)` oranını ölçmek gerekiyor.

## 2. Sembolik formül doğrulama (SymPy)

### 2.1 Formül atomunun zorunlu şeması

```
formula_atom {
  latex     : "\\tau = I\\alpha"
  sympy_src : "Eq(tau, I*alpha)"        # parse edilebilir olmak ZORUNDA
  symbols   : [{name:"tau",unit:"N*m",domain:"real"},
               {name:"I",unit:"kg*m**2",domain:"positive"},
               {name:"alpha",unit:"rad/s**2",domain:"real"}]
  assumptions: ["rigid_body","fixed_axis"]   # metinden çıkarılan geçerlilik koşulları
  anchor    : {...}
}
```

`sympy_src` veya `symbols[].unit` eksikse formül **doğrulanamaz** kabul edilir; tahmin
edilmez — birim uydurmak formül uydurmaktan daha sinsidir.

### 2.2 Dört kontrol

**(a) Boyut/birim tutarlılığı.** Her sembolün birimi 7 boyutlu SI vektörüne (M,L,T,I,Θ,N,J)
çevrilir; ifade ağacında boyut aritmetiği yapılır.

```
dim(a+b): eşit değilse HATA(boyut_toplama)   dim(a*b) = dim(a)+dim(b)
dim(a**n): n boyutsuz ve rasyonel olmalı     Eq(l,r): dim(l)==dim(r)
exp/log/sin/cos/tanh argümanı: dim == 0 olmalı
```
Uygulama: `pint` + SymPy ağaç yürüyüşü. Salt matematikte (birimsiz) kontrol atlanır ve
`unit:"1"` yazılır — atlama sessiz değil, kayda geçer.

**(b) Cebirsel özdeşlik.** Kitap "A = B" diyorsa:
```
d = simplify(A - B) ; d == 0 → geçti
değilse sırayla: ratsimp, trigsimp, powsimp, radsimp, cancel (her biri 5 sn timeout)
hepsi başarısız → (c)'ye düş
```
Timeout, "yanlış" değildir; `doğrulanamadı(timeout)` olur (D3).

**(c) Sayısal örneklemeli sağlama.** Cebir çözemediğinde ampirik kanıt:
```
N = 200 rastgele nokta, domain'e saygılı (positive → logüniform 1e-3..1e3;
    real → ±1e3; integer → 1..50) ; mpmath, 50 basamak
kabul: |A-B| ≤ 1e-30 + 1e-25*max(|A|,|B|)  (bağıl tolerans)
başarısız nokta ≥ 1 → FORMÜL YANLIŞ (veya hipotez eksik) → karşı-örneği sakla
tanımsız nokta > %20 → örnekleme alanı hatalı, domain çıkarımını gözden geçir
```
200 nokta *kanıt değildir*, ama tek bir karşı örnek **çürütmedir**; asimetri lehimizedir.
Bu yüzden `doğrulandı(sembolik)` yalnız (a)+(b) geçince verilir; sadece (c) geçerse
etiket `desteklendi(sayısal)` olur.

**(d) Sınır durum testleri.** Her formül için otomatik üretilen 6 test:
```
1. Sıfır: her değişken → 0 (tanımlıysa)   2. Tekillik: denominator==0 kökleri + limit
3. Sonsuzluk: limit(expr, x, ±oo) beklenen mi   4. İşaret: domain=positive iken sonucun
   işareti metindeki iddiayla uyumlu mu   5. Özel durum: bilinen indirgeme (v<<c → klasik
   limit; x→0 → Taylor 1. terim)   6. Ölçek: boyutsuz grup (Reynolds vb.) korunuyor mu
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

**Karantina (kesin tanım):** atom veritabanında kalır ve ham alıntısıyla görüntülenebilir;
ama (1) graf kenarı kuramaz, (2) transfer üretemez, (3) günlük plan satırına giremez,
(4) başka atomun kanıtı olamaz. Kural 3 gereği kitap reddedilmez — sadece o *atom* susturulur.

## 3. Teorem bütünlüğü — sessiz hipotez düşürme

Sistemin en tehlikeli hata sınıfı. "Her sürekli fonksiyon düzgün süreklidir" cümlesi
"kompakt kümede" düşünce yanlış olur ve **hiçbir string eşlemesi bunu yakalamaz** —
cümlenin her kelimesi kitapta geçiyordur.

### 3.1 Zorunlu ayrık şema

Teorem atomu tek bir metin bloğu olarak **saklanamaz**:

```
theorem_atom {
  name       : "Heine-Cantor"
  hypotheses : [{text:"X kompakt metrik uzay", anchor:{page:212,span:[...]}},
                {text:"f: X→Y sürekli",        anchor:{page:212,span:[...]}}]
  conclusion : {text:"f düzgün süreklidir",    anchor:{page:212,span:[...]}}
  quantifiers: ["∀ε>0 ∃δ>0"] ; scope: "metrik uzaylar"
  counterexample_if_dropped: {"X kompakt": "f(x)=1/x, X=(0,1]"}   # varsa
}
```
`hypotheses` dizisi boş olan bir teorem atomu şema düzeyinde reddedilir. Hipotezsiz
teorem yoktur; gerçekten yoksa o bir *tanım* veya *aksiyom*dur, farklı atom tipidir.

### 3.2 Sessiz düşürmeyi yakalayan dört detektör

**H1 — Koşul sözlüğü taraması (deterministik, ucuz).**
Alanına göre bakım yapılan bir tetikleyici sözlük tutulur:
```
analiz : kompakt, sınırlı, kapalı, düzgün, ölçülebilir, integrallenebilir,
         hemen her yerde, mutlak yakınsak, monoton, Lipschitz, türevlenebilir
cebir  : değişmeli, birimli, sonlu üretilmiş, Noetherian, karakteristik ≠ 2, tersinir
olasılık : bağımsız, aynı dağılımlı (i.i.d.), sonlu varyans, sıfır ortalama
lin.cebir: pozitif tanımlı, simetrik, tam ranklı, tekil olmayan, ortonormal
mühendislik: kararlı durum, laminer, adyabatik, küçük genlik, rijit, izotropik
```
Kural: bu sözcüklerden biri, teoremin çapa penceresinde (±3 cümle) geçiyor **ve**
`hypotheses[]` içinde geçmiyorsa → `hipotez_şüphesi` bayrağı. Kesin değil ama recall'ü yüksek.

**H2 — İki geçişli, çapraz-görmez çıkarım (independent re-extraction).**
Geçiş 1 teoremin ifadesini çıkarır. Geçiş 2 **ayrı bir çağrıdır**: geçiş 1'in çıktısını
görmeden aynı sayfadan *sadece koşulları* listeler. Fark (`H2 \ H1`) doğrudan düşürülmüş
hipotez adayıdır; boş değilse **otomatik birleştirilir** ve birleşik hipotezler yeniden
V1–V5'ten geçirilir.

**H3 — Karşı-örnek bankası (en güçlü ve tamamen mekanik).**
Kanonik teoremler için "hipotez X düşerse çöker" karşı örnekleri elle küratörlenmiş bir
bankada tutulur (ilk sürüm: analiz + lineer cebir + olasılıktan ~150 giriş). Teorem atomu
bankadaki bir imzayla eşleşirse (isim veya sonuç benzerliği), bankanın hipotez listesi
**beklenen küme** olur; eksik varsa → `doğrulanamadı(hipotez eksik)` ve eksik hipotezin
adı kullanıcıya gösterilir.

**H4 — Sayısal çürütme geri beslemesi.**
§2.2(c) bir karşı örnek bulduğunda, bu karşı örneğin hangi kısıtı ihlal ettiği aranır
(örn. karşı örnek noktası `x=0`, ve `x≠0` hipotezde yok). Bulunursa hipotez otomatik
önerilir ve H2 döngüsüne geri verilir.

### 3.3 Sunum kuralı

Teorem hiçbir yerde hipotezlerinden ayrı gösterilmez; kart formatı sabittir:

```
[VARSAYIMLAR]  X kompakt metrik uzay · f sürekli
[SONUÇ]        f düzgün süreklidir
[KAYNAK]       Rudin, Bl.4, s.212   [doğrulandı(alıntı)]
```
Yer darsa sonuç kısaltılır, **varsayımlar kısaltılmaz**. `06-arayuz.md` için bağlayıcı:
"bir ekran = bir karar" doktrini hipotez gizlemeyi meşrulaştırmaz.

## 4. Güven etiketleme

### 4.1 Dört etiket — kesin üretim koşulları

| Etiket | Ne zaman verilir | Anlamı (kullanıcıya) |
|---|---|---|
| `doğrulandı(sembolik)` | Formül: boyut ✓ + cebirsel özdeşlik ✓ | "Makine bunu matematiksel olarak sağladı." |
| `doğrulandı(alıntı)` | V1/V2 span ✓ + V5 sayı ✓ + V3 kapsama ≥0.45 | "Bu cümle kitapta bu sayfada yazıyor." |
| `desteklendi(NLI)` | span ✓ + V5 ✓ + NLI entail ≥0.90 (ve sayısal-sağlama sonuçları) | "Kitap bunu söylüyor ama başka kelimelerle; bu bizim ifademiz." |
| `doğrulanamadı` | Yukarıdakilerin hiçbiri, veya çelişki/timeout/OCR şüphesi | "Emin değiliz. Ham metne kendin bak." |

Ara etiket, yüzde, yıldız, 0–1 skoru **yoktur**. Dört kova, bitti — kalibre edilmemiş bir
sayı göstermek hiçbir şey göstermemekten kötüdür.

### 4.2 Arayüz talimatı (`06-arayuz.md` için normatif)

1. **Sessiz varsayılan:** `doğrulandı(*)` atomlar rozet **taşımaz** — doğruluk normdur, norm
   görsel gürültü üretmez (Kural 1).
2. **`desteklendi(*)`:** ince gri kesikli sol kenarlık; tık → kaynak paragraf açılır.
3. **`doğrulanamadı`:** kehribar üçgen + tek kelime etiket, ve **her zaman** yanında birebir
   alıntı. Bizim yeniden yazımımız değil, ham metin gösterilir.
4. **Yasak:** `doğrulanamadı` atom günlük plan satırına (Kural 4), transfer önerisine ve
   "yenilik" hükmüne (%94 hesabına) **giremez**; bunlar yalnız doğrulanmış atomlardan hesaplanır.
5. **Çapa tek tık ötede:** her atomun altında `Kitap · Bl.N · s.P`; tık → sayfa görüntüsü +
   vurgulanmış span. Çapa gösterilemiyorsa atom gösterilmez.
6. **Renk sabittir:** kehribar = doğrulanamadı, kırmızı = çelişki (§5 D4). Kırmızı başka hiçbir şeyde kullanılmaz.
7. **Toplu gösterim:** kitap kartında tek satır — `1.184 atom · %96 doğrulandı · 41 karantinada`,
   tıklanabilir filtre.

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

## 5. Uydurma savunma katmanları

Altı katman. Bağımsızlık kritiktir: aynı hata modunu paylaşan iki katman, bir katmandır.

| # | Katman | Yakalar | **Kaçırır** | Maliyet |
|---|---|---|---|---|
| **D1** | Çapa + alıntı eşleme (§1) | Tamamen uydurulmuş cümle; var olmayan sayfa; değiştirilmiş sayı/tarih | Kitapta gerçekten yazan ama **yanlış bağlamdan** alınmış cümle (yazarın çürütmek için kurduğu "kötü argüman" alıntısı) | Çok düşük (CPU) |
| **D2** | Sembolik doğrulama (§2) | Yanlış kopyalanmış formül, boyut hatası, işaret hatası, eksik katsayı | Boyutsal olarak tutarlı ama kavramsal olarak yanlış formül; kitabın kendi hatası | Düşük (CPU, ~2 sn/formül) |
| **D3** | Bağımsız yeniden çıkarım (self-consistency) | Kararsız/rastlantısal halüsinasyon; hipotez düşürme (§3 H2); atom sınırı kayması | **Sistematik** halüsinasyon — model aynı hatayı iki kez yapar (özellikle popüler ama yanlış hatırlanan teoremlerde) | Yüksek (LLM çağrısı ×2) |
| **D4** | Graf-içi çelişki taraması | Aynı kitabın iki yerinden çelişik iddia; kütüphanedeki yerleşik bilgiyle çatışma; birim/mertebe tutarsızlığı | Kütüphanenin tamamı aynı yanlışı içeriyorsa (ortak yanılgı); grafta henüz komşusu olmayan yeni alan | Orta (gömme + kNN, atom başına) |
| **D5** | Tuzak (canary) ve negatif kontrol | Uyum eğilimi (sycophancy) ve boşluk doldurma: kitapta olmayan bölüm/kavram sorulur, model "bulursa" o çıkarım turu şüpheli işaretlenir | Sadece **çıkarım turunun** sağlığını ölçer, tek tek atomları değil | Çok düşük (tur başına 3-5 sorgu) |
| **D6** | Kullanıcı geri bildirimi ("bu yanlış" tek tık) | Uzman gözünün gördüğü her şey; uzun kuyruk | Kullanıcının bilmediği alan; sessiz kullanıcı | Sıfır (asenkron) |

**Gerekçe:** D1–D2 deterministik ve modelden bağımsızdır — zemin budur. D3 model kaynaklı
*gürültüyü* siler ama *önyargıyı* silemez; onu D4 (dış tutarlılık) ve D5 (davranışsal sınama)
yakalar. D6 uzun vadede altın kümeyi besler.

**AÇIK SORU:** D1'in kaçırdığı "yanlış bağlam" hatası (yazarın reddettiği görüşü ona atfetmek)
için polarite/atıf detektörü gerekiyor. İlk sürümde "göre", "iddia eder", "savunanlar",
"yanılgı" gibi atıf işaretleyicileri pencerede aranıp atoma `attribution_risk: true`
düşülmesini öneriyorum; tam çözüm sürüm 2.

## 6. Değerlendirme takımı (eval harness)

### 6.1 Altın standart veri kümesi

**Kapsam:** 12 kitap × 20 sayfa = 240 sayfa; dağılım kullanıcı profiline göre: 5 matematik/
mühendislik, 2 tıp, 2 tarih/felsefe, 1 sanat, 1 kişisel gelişim, 1 **kasıtlı kötü tarama** (§7).

**Sayfa seçimi:** rastgele değil **tabakalı** — her kitaptan 5 yoğun-matematik, 5 düz nesir,
5 tablo/şekilli, 5 rastgele sayfa. Rastgele örnekleme matematik sayfalarını temsil etmez,
hata da tam orada.

**Etiketleme:** her sayfa 2 bağımsız insan tarafından atomlaştırılır (tip + çapa),
anlaşmazlığı üçüncü kişi çözer. Kabul kapısı: atom sınırlarında Cohen κ ≥ 0.70; altındaysa
**rehber yeniden yazılır**, veri kümesi kabul edilmez.

**Ek küme — çekişmeli (adversarial) set, 150 örnek, elle üretilir:**
```
A1 hipotezi düşürülmüş 40 teorem   → beklenen: doğrulanamadı(hipotez eksik)
A2 sayısı değiştirilmiş 30 iddia   → V5 ; A3 bozulmuş 30 formül (işaret/üs/katsayı) → D2
A4 var olmayan sayfaya çapalanmış 25 atom → V1/V2 imha
A5 bağlamı ters çevrilmiş 25 alıntı → bilinen zayıflık; yakalama oranını sadece ÖLÇ
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

Atom eşlemesi: gömme benzerliği ≥ 0.85 **ve** aynı sayfada çapa → eşleşti sayılır.

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

**Recall neden düşük tutulabilir:** ürün her fikri çıkarmak zorunda değil, çıkardığını doğru
çıkarmak zorunda. Precision için recall feda edilir — tersi asla.

### 6.4 Regresyon kapısı (CI)

Her PR'de altın kümenin sabit 200 atomluk alt kümesi + tüm çekişmeli küme koşar
(bütçe: ≤ 6 dk, ≤ 2 USD). Hallucination rate bir önceki `main`'e göre **artarsa** merge
bloklanır. Doğrulama boru hattına dokunan hiçbir PR eval koşmadan birleştirilemez.

## 7. Bozuk girdi: OCR, kırık LaTeX, kötü tarama

### 7.1 Sayfa sağlık skoru (page health) — sindirimden ÖNCE

Her sayfa için 6 sinyal — LLM çağrısından önce, saf CPU ile:

```
s1 sözlük oranı : sözlükte bulunan token / toplam (TR+EN + alan sözlüğü)
s2 tek-karakter oranı : "l ntegra l" tipi bozulma   s3 çöp karakter (� , tanımsız glif) oranı
s4 ortalama kelime uzunluğu: normalden ±3σ sapma    s5 tirelenmiş satır oranı (sütun bölme hatası)
s6 matematik bütünlüğü: $ sayısı çift mi, \begin/\end eşleşiyor mu, parantez dengesi
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
1. Parse kapısı: latex2sympy → SymPy AST. Başarısızsa formül atomu ÜRETİLMEZ;
   yerine "matematiksel içerik var, okunamadı" işareti bırakılır.
2. Deterministik ve sınırlı OCR→LaTeX düzeltme sözlüğü, kayıt altında:
   "∫"↔"f", "Σ"↔"E", "≤"↔"<", "α"↔"a", "μ"↔"u", "−"↔"-", "'"↔"′".
   Her düzeltme atoma `ocr_repairs: [...]` yazılır; ≥3 düzeltme → `doğrulanamadı(ocr)`.
3. Onarım ASLA LLM'e bırakılmaz — LLM burada makul ama yanlış formül üretmekte çok iyidir
   ve bu hata tipi hiçbir katmana yakalanmaz.
4. Boyut kontrolü (§2.2a) burada ikinci görev yapar: bozulmuş formüllerin çoğu boyutsal
   olarak tutarsızdır; boyut kapısı sessiz OCR hatasının en iyi dedektörüdür.
```

### 7.4 Sayfa numarası kayması (page offset)

Basılı sayfa no ile PDF indeksi farkı otomatik kalibre edilir: ilk 30 sayfada
üstbilgi/altbilgi'den sayı çıkarılır, mod alınır, offset sabitlenir; roma rakamlı ön bölüm
ayrı ele alınır. Offset ≥ 3 sayfada tutarsızsa kitap `çapa_güvensiz` işaretlenir ve **tüm**
atomları `desteklendi(NLI)` tavanına iner. Yanlış sayfa numarası veren çapa, çapasızlıktan kötüdür.

## 8. Maliyet

### 8.1 Varsayımlar

400 sayfalık teknik kitap ≈ 180.000 token, ≈1.200 atom, ≈120 formül, ≈60 teorem.
`AÇIK SORU:` birim fiyat varsayımı (küçük model ≈ 1 USD/M girdi-token, büyük model
≈ 3 USD/M mertebesi) yayın öncesi güncel fiyat listesinden **doğrulanmalıdır** — bu belgenin
kendi doktrini gereği, doğrulanmamış sayı `doğrulanamadı` etiketlidir. Aşağısı mertebe tahminidir.

### 8.2 Katman katman ek maliyet (kitap başına)

| Kontrol | Kapsam | Mekanizma | Ek maliyet |
|---|---|---|---|
| V1/V2/V3/V5 + sayfa sağlık | **her atom / her sayfa** | CPU (rapidfuzz, regex) | ~0 USD, ≈15 sn |
| V4 NLI | **sadece V3 < 0.45 olanlar** (≈%20 ≈ 240 atom) | küçük çapraz-kodlayıcı, kendi barındırdığımız | ≈0.01 USD, ≈40 sn GPU / ≈4 dk CPU |
| §2 SymPy (a,b,c,d) | **her formül** (120) | CPU, 10 sn timeout | ~0 USD, ≈6 dk |
| §3 H1 sözlük + H3 banka | **her teorem** | CPU | ~0 USD |
| §3 H2 çift geçiş | **teorem ∪ formül** (180) | LLM, ≈500 tok/atom | ≈0.10–0.30 USD |
| D4 graf çelişki | **her doğrulanmış atom** | gömme + kNN | ≈0.02 USD |
| D5 tuzak sorgular | **kitap başına 5 sorgu** | LLM | ≈0.01 USD |
| D3 tam çift-çıkarım | **örnekleme: %5 atom** | LLM | ≈0.15 USD |
| **Toplam ek** | | | **≈0.30–0.50 USD/kitap, ≈10-15 dk CPU** |

Referans: sindirimin kendisi (180K token okuma + atom üretimi) kitap başına kabaca
1.5–3 USD mertebesindedir. **Doğrulama, sindirimin %15–25'i kadar ek yük getirir** —
ürünün tek farklılaştırıcısı için ödenecek en ucuz bedel.

### 8.3 Her atoma mı, örnekleme mi? — karar kuralı

```
HER ATOMA (istisnasız):
  - maliyeti ~0 olan her deterministik kontrol (V1,V2,V3,V5, sağlık, H1, H3)
  - hatası "zehirli" olan her kontrol: formüllerde §2, teoremlerde §3
  Gerekçe: maliyet sıfıra yakınken örnekleme yapmak sadece hata kaçırmaktır.

ÖRNEKLEME (yalnız bunlar):
  - D3 tam çift-çıkarım: %5 rastgele + %100 (formül ∪ teorem ∪ D4-bayraklı)
  - İnsan denetimi: kitap başına 20 atom (hallucination rate tahmini)
  Oran sabit DEĞİL, adaptiftir:
     son 100 atomda hata > %2 → %5'ten %25'e ; sağlık ort. < 0.85 → ×2
     yeni alan / yayınevi / OCR profili → ilk kitap %100
```

### 8.4 Bütçe koruması

Doğrulama maliyeti sindirimin %40'ını aşarsa boru hattı durur ve olay kaydı üretilir.
Sınırsız doğrulama bütçesi sınırsız yeniden deneme demektir; yeniden denemenin kendisi bir
hata sinyalidir ve gizlenmemelidir.

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
3. `AÇIK SORU:` Kitabın **kendisi yanlışsa**? Sistem şu an kitaba sadıktır. D4 çelişki
   kenarı bunu yakalar ama "hangi kitap haklı" kararı bu belgenin kapsamı dışıdır;
   `07-transfer.md` ile ortak çözülmeli.
4. `AÇIK SORU:` Karşı-örnek bankasının bakım maliyeti (≈150 girdi × alan uzmanı saati) bütçelenmedi.
