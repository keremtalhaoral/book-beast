# 02 — Yenilik Puanı ve Atom Grafı

> **Uzman:** Uygulamalı Matematikçi (Graf Teorisi & Bilgi Erişimi)
> **Kapsam:** "Bu kitabın %94'ü zaten sende var, şu 11 sayfayı oku" hükmünü üreten motor.

---

## 3 cümlelik özet

Bir atomun yeniliği, kütüphanedeki **birbirinden bağımsız** komşuların onu ne kadar
*gerektirdiğiyle* ölçülür — noisy-OR kapsama, tekil maksimum benzerlik değil.
Kitap seviyesinde iki ayrı sayı üretiriz: kullanıcıya gösterilen `%94` **sayfa-ağırlıklı
kapsanma oranıdır** (kütle), "Bölüm 7'yi oku" hükmü ise **üst-kuyruk yenilik değerinden**
gelir (kuyruk); bu ikisini karıştırmak sistemin en büyük tasarım hatası olurdu.
1.8 milyar çiftin tamamı asla hesaplanmaz: HNSW + tür/alan bloklama + kademeli hakem
zinciri ile yeni kitap başına maliyeti `O(m log n)`'e, LLM çağrısını ~64'e indiririz.

---

## 1. Notasyon ve temel nesneler

| Sembol | Anlam |
|---|---|
| `a` | Yeni kitabın bir fikir atomu |
| `L` | Kütüphane (mevcut tüm atomlar), `\|L\| = n` |
| `B` | Yeni kitap, `\|B\| = m` atom (tipik m ≈ 120) |
| `sim(a,e)` | Karma benzerlik, `[0,1]` |
| `κ(a←e)` | `e`'nin `a`'yı **kapsama gücü** (yönlü), `[0,1]` |
| `c(a)` | `a`'nın toplam kapsanmışlığı, `[0,1]` |
| `ν(a) = 1 − c(a)` | **Yenilik puanı** |
| `pg(a)` | `a`'nın sayfa ağırlığı (kapladığı sayfa payı) |
| `T(a)` | Açık Sorular Defteri'ne transfer yakınlığı `[0,1]` |
| `E(a)` | Kanıt gücü `[0,1]` (Katman 1'den gelir) |

Graf `G = (V, E)`: düğümler atomlar, kenarlar brifingdeki 6 ilişki
(`aynı · çelişiyor · önkoşulu · genellemesi · uygulaması · çürütüyor`).
Her kenarın bir güveni `p ∈ (0,1]` vardır. **Güvensiz kenar yoktur, sadece düşük `p` vardır.**

---

## 2. Yenilik puanı formülü

### 2.1 Neden tekil maksimum yanlış

`ν(a) = 1 − max_e sim(a,e)` cazip ama çöp üretir. İki nedenle:

1. **Parça parça kapsanma.** Bir fikir üç ayrı kitapta yarım yarım anlatılmış olabilir;
   hiçbiriyle benzerliği 0.9'u geçmez ama birlikte fikri tümüyle içerirler.
   Maksimum bunu göremez ve atomu "yeni" ilan eder.
2. **Yön körlüğü.** Kosinüs simetriktir, kapsama değildir. "Sürekli fonksiyon" tanımı ile
   "düzgün sürekli fonksiyon" tanımı arasındaki benzerlik yüksektir; ama ikincisi birinciyi
   kapsar, birincisi ikincisini kapsamaz. Simetrik ölçüt bu asimetriyi yok eder.

### 2.2 Kapsama gücü (yönlü)

```
κ(a ← e) = σ(sim(a,e)) · ent(e ⊨ a) · θ(e) · μ(tür(a), tür(e))

σ(s)  = 1 / (1 + exp(−α·(s − s₀)))        keskinleştirici, α = 12, s₀ = 0.78
ent(·) = cross-encoder/NLI gerektirme olasılığı, [0,1]   (bkz. §3)
θ(e)  = kaynak güveni  = 0.6 + 0.4·E(e)   (zayıf kanıtlı atom zayıf kapsar)
μ(·)  = tür uyum matrisi                   (bkz. tablo)
```

`σ` şart: ham kosinüs 0.65 "aynı konudan bahsediyor" demektir, "aynı şeyi söylüyor" demez.
Lojistik keskinleştirici, 0.78 civarında hızlı yükselen bir eşik davranışı verir; altı
neredeyse 0, üstü hızla 1.

**Tür uyum matrisi `μ`** (satır = kapsanan `a`, sütun = kapsayan `e`):

|  | tanım | teorem | yöntem | formül | iddia | anekdot |
|---|---|---|---|---|---|---|
| **tanım**   | 1.00 | 0.35 | 0.10 | 0.20 | 0.30 | 0.00 |
| **teorem**  | 0.15 | 1.00 | 0.10 | 0.55 | 0.40 | 0.00 |
| **yöntem**  | 0.10 | 0.25 | 1.00 | 0.30 | 0.35 | 0.05 |
| **formül**  | 0.10 | 0.60 | 0.20 | 1.00 | 0.20 | 0.00 |
| **iddia**   | 0.25 | 0.55 | 0.30 | 0.30 | 1.00 | 0.20 |
| **anekdot** | 0.00 | 0.00 | 0.05 | 0.00 | 0.30 | 1.00 |

Okunuşu: bir anekdot hiçbir teoremi kapsayamaz (0.00) — bir tarih hikâyesi okumuş olmak
teoremi bildiğin anlamına gelmez. Bir formül bir teoremi büyük ölçüde kapsar (0.60) ama
tersi zayıftır (0.55) çünkü teorem ifadesi çoğu zaman formülü içerir.

### 2.3 Bağımsız temsilciler — çifte sayımı önlemek

Beş komşunun üçü zaten birbirinin kopyasıysa, kapsamayı üç kez artırmamalı.

```
1. N_k(a) ← ANN top-k komşu, sim ≥ τ_taban
2. N_k(a) içindeki atomları KENDİ aralarında `aynı` ilişkisine göre kümele
   (union-find; aynı eşdeğerlik sınıfındakiler tek sayılır)
3. Her sınıftan en yüksek κ değerli tek temsilciyi al → R(a)
```

`R(a)` = **bağımsız kapsayıcılar kümesi.** Kullanıcıya gösterilen "5 farklı kitaptan"
ifadesi doğrudan `{kitap(r) : r ∈ R(a)}` kümesinin boyutudur — türetilmiş bir sayı değil,
hesabın kendi içinden çıkan gerçek bir nicelik.

### 2.4 Nihai formül

```
c(a) = 1 − Π_{r ∈ R(a)} ( 1 − κ(a ← r) )          ← noisy-OR
ν(a) = 1 − c(a)
```

Noisy-OR seçildi çünkü: (i) `[0,1]`'de kalır, kırpma gerektirmez; (ii) tek bir güçlü
kapsayıcı (κ=0.95) ile beş zayıf kapsayıcının (κ=0.45 ×5) birlikte etkisini
doğru sıralar; (iii) bağımsızlık varsayımı §2.3'teki temsilci seçimiyle zaten
zorlanmıştır, yani varsayım keyfî değil, inşa edilmiştir.

**Sayısal örnek.** `R(a)` = 3 temsilci, κ = (0.55, 0.40, 0.30)
→ `c = 1 − 0.45·0.60·0.70 = 0.811` → `ν = 0.189`. Atom "büyük ölçüde biliniyor" bandında.

### 2.5 Bölüm seviyesine toplama

**Ortalama kullanmıyoruz.** 40 sıradan atomun içindeki 3 mücevheri ortalama boğar ve bu
doğrudan Doktrin 3'ü ("reddetme yok, sıkıştırma var") ihlal eder.
**Maksimum da kullanmıyoruz.** Tek gürültülü/yanlış-çıkarılmış atom bütün bölümü
"yepyeni" ilan eder; gürültüye karşı sıfır dayanıklılık.

Seçim: **üst-kuyruk ortalaması (CVaR / superquantile), q = 0.20.**

```
N_bölüm = ( 1 / ⌈q·|Ch|⌉ ) · Σ_{a ∈ top-q(Ch, ν)} ν(a) · ω(a)

ω(a) = tür ağırlığı (teorem 1.0, yöntem 0.9, tanım 0.8, formül 0.9, iddia 0.7, anekdot 0.4)
```

CVaR, maksimum ile ortalama arasında sürekli bir aile oluşturur (`q→0` maksimum,
`q→1` ortalama); `q = 0.20` yaklaşık 24 atomluk bir bölümde en iyi 5 atoma bakar —
tek bir hatalı atomun hükmü çevirmesine izin vermeyecek kadar geniş, mücevheri
boğmayacak kadar dar.

Yanına iki yardımcı sayı: `Y_bölüm` = `ν ≥ τ_yeni` olan atom sayısı,
`S_bölüm` = bu atomların kapladığı benzersiz sayfa sayısı. Arayüz cümlesi
("11 sayfa") `S_bölüm`'den değil §6'daki optimizasyondan çıkar; `S_bölüm` sadece üst sınırdır.

### 2.6 Kitap seviyesi — iki farklı sayı

Bu ayrım belgenin en kritik kararıdır.

```
KÜTLE   (kullanıcıya gösterilen %94):
  P_bilinen = Σ_a pg(a)·1[ c(a) ≥ τ_dup ]  /  Σ_a pg(a)

KUYRUK  (okuma kararını veren):
  V_kitap = Σ_{a ∈ top-m(B, S)} S(a)          m = 12,  S(·) §8'deki birleşik skor
```

**Neden sayfa-ağırlıklı?** Kullanıcı atom okumaz, sayfa okur. Atom-sayısı ağırlıklı bir
oran, formül yoğun 2 sayfayı 20 sayfalık anlatıyla eşitler ve "%94" yalan olur.

**Neden iki sayı?** `P_bilenen = 0.94` ve `V_kitap = yüksek` aynı anda tutarlıdır ve
tam olarak Doktrin 3'ün cümlesidir. Tek skorla bu ifade edilemez.
Kitap seviyesinde asla tek bir "kitap puanı" göstermeyiz — o sayı hiçbir karar vermez.

---

## 3. Çift tespiti boru hattı

Beş kademe, her kademe bir öncekinin çıktısını 5–20× daraltır.

```
K0  NORMALİZE + TAM ÇİFT
    Kanonik iddia cümlesi → SimHash(64 bit). Hamming ≤ 3 → doğrudan `aynı`.
    Alıntı/tekrar baskıları burada elenir. Maliyet ihmal edilebilir.

K1a ANN (yoğun)      HNSW, M=32, efConstruction=200, efSearch=128
                     top-k = 64, cosine ≥ τ_taban = 0.62
K1b LSH (seyrek)     MinHash 128 perm, 5-gram karakter shingle, b=16 × r=8
                     Jaccard ≥ 0.55.  → Formül/notasyon tekrarını yakalar;
                     yoğun gömme sembol dizilerinde zayıftır, bu kanal onu telafi eder.
    ADAY = K1a ∪ K1b

K2  ÇAPRAZ KODLAYICI (cross-encoder) — YÖNLÜ
    Girdi: (öncül = e, sonuç = a). Çıktı: P(e ⊨ a) ve P(a ⊨ e) ayrı ayrı.
    6 katmanlı, ONNX int8 quantize, ~1.5 ms/çift.
    p < 0.55 → ilgisiz, at.   p > 0.85 → kabul, LLM'e gitme.
    0.55 ≤ p ≤ 0.85 → BELİRSİZ BANT → K3.

K3  LLM HAKEM (sadece belirsiz bant)
    Çıktı tek etiket: {aynı, a⊂e, e⊂a, çelişiyor, tamamlayıcı, ilgisiz}
    + tek cümle gerekçe + her iki tarafın sayfa çapası.
    "tamamlayıcı" etiketi kritik: aynı değil ama birlikte a'yı kapsıyorlar.

K4  BİRLEŞTİRME
    `aynı` kenarları union-find'a yazılır → eşdeğerlik sınıfları.
    Yönlü `⊂` kenarları κ hesabına ent(·) olarak girer.
```

### 3.1 Eşiklerin kalibrasyonu

**Altın küme.** Alan başına 50, toplam 400 çift (200 pozitif / 200 negatif), zorluk
dengeli: her alandan 25 "kolay negatif" (rastgele) + 25 "zor negatif"
(aynı konu, farklı iddia — asıl tehlike bunlar).

**Yöntem.** Cross-encoder ham skoru olasılığa çevrilir (**Platt ölçekleme**, iki parametre,
altın küme üzerinde lojistik regresyon). Sonra eşik, maliyet matrisiyle seçilir:

```
Yanlış BİRLEŞTİRME (aslında yeni, "zaten var" dedik)  maliyet = 3
Yanlış AYIRMA      (aslında var, "yeni" dedik)         maliyet = 1
```

3:1 oranı doğrudan Doktrin 3'ten gelir: sistem bir fikri yanlışlıkla gizlerse kullanıcı
onu asla göremez ve bunu fark edemez; fazladan bir fikir gösterirse kullanıcı 30 saniye
kaybeder. **Hedef: precision(aynı) ≥ 0.95 kısıtı altında recall'u maksimize et.**

**Sürekli kalibrasyon.** Belirsiz bandın merkezine en yakın çiftlerden haftada en fazla
**5 tanesi** kullanıcıya sorulur ("bu ikisi aynı fikir mi?"). Aktif öğrenme; cevaplar
altın kümeye eklenir, Platt parametreleri her 50 yeni etikette yeniden fit edilir.
Sınır: haftada 5 — Doktrin 1, kullanıcıyı sorguya çekmeyiz.

---

## 4. Gömme stratejisi

### 4.1 Ne gömülür

**Atomun tamamı değil, kanonik iddia cümlesi.** Atomun tam metni kitabın üslubunu,
yazarın tercihlerini ve bölüm bağlamını taşır; aynı fikri iki farklı kitapta
uzaklaştıran şey tam olarak budur. "Aynı fikir" ilişkisi iddia düzeyinde tanımlıdır.

Her atom **üç temsille** indekslenir:

| Vektör | İçerik | Kullanım |
|---|---|---|
| `v_iddia` (1024d) | Tek cümlelik kanonik iddia | Ana ANN indeksi |
| `v_bağlam` (1024d) | İddia + bölüm başlığı + alan etiketi | Belirsizlik giderme |
| `h_sözlük` (128 perm) | Terim/sembol çekirdeği MinHash | LSH kanalı |
| `h_yapı` | Kanonik formül AST hash'i | Sembolik eşleşme |

```
sim(a,e) = w₁·cos(v_iddia) + w₂·cos(v_bağlam) + w₃·yapısal(a,e)
w = (0.60, 0.15, 0.25)      formül içeren atomlarda
w = (0.80, 0.20, 0.00)      formülsüz atomlarda (w₃ payı w₁'e devredilir)
```

**Boyut ekonomisi.** Matryoshka kesimli model: ANN kaba elemesi ilk **256 boyutla**
yapılır (4× hızlı, 4× az bellek), top-64 aday tam **1024 boyutla** yeniden puanlanır.

### 4.2 Matematiksel notasyon problemi

`∀ε>0 ∃δ>0 : |x−a|<δ ⟹ |f(x)−f(a)|<ε` metnini bir gömme modeline vermek gürültü
üretir; tokenizer sembolleri parçalar, benzerlik anlamdan değil sembol yoğunluğundan gelir.
Üç katmanlı çözüm:

**(1) Kanonikleştirme.** Formül SymPy ile ayrıştırılır, ifade ağacına çevrilir; serbest
değişkenler bağlanma sırasına göre yeniden adlandırılır (`x₁, x₂, …` — de Bruijn ruhu),
sabitler normalize edilir, birimler ayrıştırılır. `f''(x) > 0` ile `g''(t) > 0` aynı
kanonik dizeyi verir. Bu dize hash'lenir → `h_yapı`.

**(2) Nesirleştirme (verbalization).** Atom üretilirken formülün **doğal dil karşılığı**
bir kez LLM ile yazılır ve kalıcı olarak saklanır:
`f'' > 0` → "fonksiyonun ikinci türevi her yerde pozitiftir, yani dışbükeydir".
**Gömme bu nesirden alınır, formülden değil.** Sembol hiç gömme modeline girmez.

**(3) Yapısal eşleşme ayrı kanalda.** Formül kimliği vektör uzayında değil, sembolik
indekste aranır:

```
yapısal(a,e) = 1                             h_yapı eşitse
             = 1 − TED(A_a, A_e)/max(|A_a|,|A_e|)    aksi halde
TED = ağaç düzenleme mesafesi (tree edit distance), sadece K1b adaylarında hesaplanır
```

Böylece "Cauchy–Schwarz eşitsizliği" iki kitapta farklı harflerle yazılmış olsa da
`h_yapı` üzerinden birebir eşleşir — gömme modelinin yeteneğine hiç bağlı kalmadan.

### 4.3 Alan uyarlaması

Tam ince ayar (fine-tune) yapmıyoruz — kullanıcı verisi gizlidir ve tek kullanıcıda
overfit riski yüksektir. Bunun yerine kütüphane 5.000 atomu geçtiğinde:
**whitening (ZCA) + öğrenilmiş köşegen ölçekleme.** Kullanıcının onayladığı `aynı`
çiftlerinden `d` parametreli bir köşegen metrik öğrenilir (kontrastif kayıp, dakikalar).
Geri alınabilir, denetlenebilir, ucuz.

`AÇIK SORU:` Çok dilli kitaplarda (Türkçe kitap + İngilizce kitap aynı fikir) çapraz-dil
hizalama kalitesi ölçülmeli; ilk 200 çiftlik çapraz-dil altın kümesi kurulana kadar
çapraz-dil `aynı` kararları belirsiz banda zorlanmalı (yani her zaman LLM hakeme gitmeli).

---

## 5. Önkoşul DAG'ı

### 5.1 Kenar üretimi

| Kaynak | Nasıl | Başlangıç güveni `p` |
|---|---|---|
| Açık önkoşul | Katman 1 çıkarımı ("bu teorem ölçü teorisi gerektirir") | 0.85 |
| Terim–tanım kuralı | Atom `t` terimini kullanıyor, `d(t)` tanım atomu var → `d(t) → a` | 0.75 |
| Kitap içi sıra | Aynı kitapta önce gelen, sonrakini önceler | 0.25 |
| Kanıt zinciri | Teorem ispatında atıf yapılan lemma | 0.90 |

Kitap-içi-sıra kenarları kasten **çok düşük güvenlidir**: yazarın sırası pedagojik
gerçeği değil, editoryal tercihi yansıtır. Bunlar döngü kırmada ilk feda edilenlerdir.

### 5.2 Döngü çıkarsa ne yaparız

Döngüler **iki farklı şeyin** işaretidir ve ikisi farklı işlem görür:

**Tür A — gerçek karşılıklı bağımlılık (co-requisite).** "İç çarpım" ve "norm"
gerçekten birbirini gerektirir; bu bir hata değil, pedagojik bir olgudur.
→ **Tarjan ile güçlü bağlı bileşenleri (SCC) bul, her SCC'yi tek bir süper-düğüme daralt
(condensation).** Daraltılmış graf **tanım gereği** asiklinktir; DAG'ı ondan kurarız.
Süper-düğüm kullanıcıya "bu üç kavram birlikte öğrenilir" olarak sunulur — ki bu doğru
olan da budur.

**Tür B — çıkarım hatası.** SCC içindeki kenarların güvenleri düşükse veya SCC 6
düğümden büyükse bu bir hatadır, olgu değil.
→ **Minimum geri-besleme yay kümesi (Minimum Feedback Arc Set)** aranır. NP-zor olduğu
için **Eades–Lin–Smyth doğrusal-zamanlı sezgiseli** ile bir düğüm sıralaması üretilir;
sıralamaya ters düşen kenarlar aday hatadır, **en düşük `p`'liden başlanarak** SCC
kırılana kadar düşürülür.

Düşürülen kenar **silinmez**: `[şüpheli önkoşul]` etiketiyle saklanır, grafta pasif durur
ve kullanıcının haftalık 5 sorusundan biri olabilir. Doktrin 2 — hiçbir şey sessizce kaybolmaz.

**Karar kuralı:** `|SCC| ≤ 5 ve min p ≥ 0.70` → Tür A (daralt). Aksi halde Tür B (kır).

### 5.3 Topolojik sıralamadan okuma sırası

Bir DAG'ın topolojik sıralaması tek değildir (tipik olarak milyonlarca geçerli sıra
vardır); ürünün işi **doğru olanı değil, en iyisini** seçmektir.
**Kahn algoritması + öncelik kuyruğu:**

```
hazır ← giriş-derecesi 0 olan düğümler
while hazır boş değil:
    v ← argmax_{u ∈ hazır} öncelik(u)
    sıraya ekle v
    v'nin çıkan kenarlarını sil, yeni hazır olanları kuyruğa at

öncelik(u) = 0.45·T(u)              transfer yakınlığı (Açık Sorular Defteri)
           + 0.30·kilit(u)          u okununca hazır hale gelen düğüm sayısı, log-normalize
           + 0.15·ν(u)              yenilik
           − 0.10·konu_değişimi(u)  bir önceki düğümle farklı alandaysa ceza
```

`kilit(u)` terimi kritiktir: bir tanımı okumak 14 teoremi açıyorsa, o tanım kendi başına
sıkıcı olsa bile öne alınmalıdır. Bu, DAG'daki **darboğaz düğümlerini** (bottleneck)
otomatik olarak öne çeker. `konu_değişimi` cezası bağlam değiştirme maliyetini modeller —
kullanıcı kafa karışıklığından nefret ediyor.

---

## 6. "Şu 11 sayfayı oku" hesabı

### 6.1 Problem formülasyonu

Bu **saf küme kapsama (set cover) değildir** — çünkü sayfalar tek boyutlu ve sıralıdır,
ve okunan şey rastgele bir küme değil, **bitişik aralıklardır**.

```
Girdi:   kitap sayfaları 1..P
         yüksek yenilikli atomlar A = { a : ν(a) ≥ τ_yeni }
         her a bir sayfa aralığı span(a) = [l_a, r_a] kaplar
         kazanç g(a) = S(a)               (§8 birleşik skor)
Karar:   en fazla k adet ayrık aralık I₁..I_k seç
Amaç:    maksimize  Σ_{a: span(a) ⊆ ∪I_j} g(a)  −  μ·k
Kısıt:   Σ_j |I_j| ≤ B          (sayfa bütçesi)

Başlangıç: B = 15, k = 3, μ = 0.5, τ_yeni = 0.55
```

`μ·k` terimi: her ayrı aralık okuma sürtünmesi yaratır (kitabı açıp kapama, bağlam
kurma). 3 ayrı 4 sayfa, tek 12 sayfadan pahalıdır. Cezasız formülasyon kullanıcıya
"7, 44, 91, 158 ve 203. sayfaları oku" gibi işe yaramaz bir çıktı verir.

### 6.2 Bu problem TAM olarak çözülebilir

Aralıklar tek boyutta bitişik olduğu için problem dinamik programlamaya (DP) düşer:

```
D[i][b][j] = ilk i sayfayı ele almış, b sayfa bütçesi harcamış,
             j aralık kullanmışken elde edilen en yüksek kazanç

D[i][b][j] = max(
    D[i−1][b][j],                                    sayfa i'yi alma
    max_{t≥1} ( D[i−t][b−t][j−1] + kazanç(i−t+1 .. i) − μ )   [i−t+1, i] aralığını al
)
```

`P ≈ 400`, `B ≈ 40`, `k ≈ 4`, iç döngü `t ≤ B` → yaklaşık `400·40·4·40 = 2.56M` işlem.
Milisaniyeler. **Yani burada yaklaşık algoritmaya gerek yoktur; optimumu buluruz.**
Bu, bir kitap için verilen en görünür hükmün matematiksel olarak *kesin* olması demektir.

### 6.3 Açgözlü algoritma (ölçek/genelleme durumu için)

Çok kitaplı birleşik plan üretiminde (aralıklar artık tek bir sıralı eksende değil)
DP çöker; oradaki hâl klasik **bütçeli maksimum kapsamadır** ve açgözlü çalışır:

```
SEÇİLEN ← ∅ ;  kalan_bütçe ← B
while kalan_bütçe > 0 and SEÇİLEN < k:
    her aday aralık I için (|I| ≤ kalan_bütçe):
        marj(I) ← ( Σ_{a yeni kapsanan} g(a) − μ ) / |I|      ← YOĞUNLUK, toplam değil
    I* ← argmax marj(I)
    if marj(I*) ≤ 0: break
    SEÇİLEN ← SEÇİLEN ∪ {I*} ;  kalan_bütçe −= |I*|
# köprüleme: iki seçili aralık arası boşluk ≤ 3 sayfa ise birleştir
# (μ tasarrufu > köprü sayfa maliyeti olduğunda)
```

Kazanç fonksiyonu submodülerdir (aynı atom iki kez sayılmaz), bütçe kısıtı doğrusaldır
→ yoğunluk-açgözlü + tekil-en-iyi karşılaştırması **(1 − 1/e) ≈ 0.632** garantisi verir.
Toplam kazanca göre değil **yoğunluğa** göre seçmek zorunludur; toplam kazanç açgözlüsünün
hiçbir garantisi yoktur (bütün bütçeyi tek büyük aralığa yatırır).

### 6.4 Önkoşul kapanışı

Seçilen aralıktaki atomların DAG önkoşulları kontrol edilir:

- Önkoşul kütüphanede zaten var → sorun yok.
- Önkoşul **aynı kitapta ve seçilmemiş** → aralığa dahil etmenin maliyeti hesaplanır;
  ucuzsa bütçeden karşılanır.
- Önkoşul **hiçbir yerde yok** → ayrı bir "önce şunu bil" satırı olur, ana aralığa
  karıştırılmaz.

Doktrin 1 gereği ekranda tek karar kalır: "Bölüm 7, sayfa 142–152 (11 sayfa)".
Önkoşul uyarısı bir tık ötede durur.

---

## 7. Graf sorguları

| # | Soru | Algoritma | Maliyet | Önbellek |
|---|---|---|---|---|
| 1 | Bu fikri hangi kitaplar destekliyor / çürütüyor? | Tip-filtreli 1–2 hop komşuluk, `E(·)` ile sıralama | `O(deg²)` | anlık |
| 2 | En merkezi 10 fikrim | **Kişiselleştirilmiş PageRank** (`destekler`, `genellemesi`, `önkoşulu` kenarları; d=0.85) | Forward-Push, `O(1/ε)` | gecelik |
| 3 | Kütüphanemdeki boşluklar (A) — eksik temel | DAG'da **askıda önkoşul**: hiçbir atomun kapsamadığı önkoşul referansları | `O(V+E)` | gecelik |
| 4 | Boşluklar (B) — eksik köprü | **Leiden** topluluk tespiti → topluluk çiftleri arası kenar yoğunluğu ≈ 0 olanlar | `O(E log V)` | haftalık |
| 5 | Boşluklar (C) — karşılanmamış ihtiyaç | Açık Sorular Defteri'ndeki soruya en yakın atomun `sim < 0.5` olması | `O(\|Q\|·log n)` | anlık |
| 6 | Bu iki fikir nasıl bağlanıyor? | **Dijkstra**, kenar maliyeti `w = −log p` → en olası yol (çarpımı maksimize eder) | `O(E log V)` | anlık |
| 7 | Bu atomu okumak için ne bilmeliyim? | DAG'da **ters ulaşılabilirlik** (atalar), BFS | `O(V+E)` yerel | anlık |
| 8 | Çelişki kümelerim | `çelişiyor` alt-grafında bağlı bileşenler + **yapısal denge** (dengesiz üçgen tespiti) | `O(E)` | gecelik |
| 9 | Bu kitap hangi bilgi kümemi büyütüyor? | Topluluk ataması + **modülerlik değişimi** `ΔQ` | `O(m·deg)` | kitap başına |
| 10 | Hangi fikrim en kırılgan? | PageRank yüksek **ama** tek kaynaklı (`\|R(a)\| = 1`) atomlar | `O(V)` | gecelik |

**Neden PageRank, neden derece değil.** Derece merkeziliği en çok tekrarlanan fikri
ödüllendirir; bu genelde "popüler kitapların ortak klişesidir". PageRank ise
*üzerine çok şey inşa edilmiş* fikri ödüllendirir — `önkoşulu` kenarları yönlü
akıtıldığında bu tam olarak "temel" kavramına karşılık gelir.

**#10 pratik ama az bilinen sorgu:** merkezî olup tek kaynağa dayanan fikirler,
kütüphanenin en riskli noktalarıdır — o tek kitap yanılıyorsa bütün yapı yanılır.
Bu sorgu ürünün kendi epistemik dürüstlüğüdür.

---

## 8. Ölçekleme: 1.8 milyar çiftten kurtulmak

`n = 60.000` atom → `n(n−1)/2 ≈ 1.8×10⁹` çift. Bu sayı hiçbir zaman hesaplanmaz.

### 8.1 İki temel karar

**(1) Graf artımlı (incremental) kurulur, asla baştan kurulmaz.** Yeni kitap eklendiğinde
sadece `m = 120` yeni atom sorgulanır. Maliyet `O(m · log n)`, `O(n²)` değil.

**(2) Bloklama (blocking).** Aday üretimi türle ve alanla ön-filtrelenir: anekdot
teoremle asla karşılaştırılmaz (`μ = 0`). Bu tek başına ~3× tasarruf sağlar ve
*doğruluktan hiçbir şey kaybettirmez* çünkü elenen çiftlerin κ'sı zaten sıfırdır.

### 8.2 Kademe bütçesi (yeni bir kitap, m = 120)

| Kademe | Girdi | Çıktı | Birim | Toplam |
|---|---|---|---|---|
| K0 SimHash | 120 | 120 | ~0 | ihmal |
| K1 HNSW+LSH | 120 sorgu × 64 | ~7.700 çift | 0.4 ms/sorgu | **50 ms** |
| Bloklama + `τ_taban` | 7.700 | ~800 çift | ~0 | ihmal |
| K2 Cross-encoder | 800 | ~180 kabul | 1.5 ms | **1.2 sn** |
| K3 LLM hakem | ~64 (belirsiz bant) | 64 karar | ~1.5 sn | **~40 sn** (paralel 8) |

**Kitap başına toplam: ~1 dakika, ~64 LLM çağrısı.** Kabul edilebilir.

### 8.3 İlk toplu kurulum (500 kitap)

`500 × 64 = 32.000` hakem çağrısı — bir kereye mahsus. **Batch API** ile yapılır
(%50 indirim, gecikme önemsiz). Kütüphane büyüdükçe belirsiz bant *daralır*
(kalibrasyon iyileşir), yani maliyet süper-doğrusal değil, alt-doğrusal büyür.

### 8.4 Bellek ve indeks

```
Vektörler:  60.000 × 1024 × 4B = 246 MB (float32)
            → int8 skaler quantization = 61 MB, cos kaybı < 0.01
HNSW grafı: 60.000 × 32 × 4B ≈ 7.7 MB
MinHash:    60.000 × 128 × 4B = 31 MB
TOPLAM:     ~100 MB → tek makinede, RAM'de, sharding'siz.
```

500 kitap ölçeğinde dağıtık hiçbir şeye ihtiyaç yoktur. Bu bir "ölçek problemi" değil,
bir "algoritma seçimi problemi"dir.

### 8.5 Artımlı güncelleme

- Yeni atom eklendiğinde **sadece komşularının** `ν` değeri değişebilir → `O(k)` yeniden
  hesap, tüm kütüphane değil.
- Eşdeğerlik sınıfları **union-find** ile tutulur → birleştirme neredeyse `O(1)` (ters
  Ackermann).
- PageRank baştan hesaplanmaz: **Forward-Push** ile yerel artımlı güncelleme; tam
  yeniden hesap gecelik toplu işte.
- HNSW silme desteklemez → silinen atomlar `tombstone` işaretlenir, indeks 30 günde bir
  yeniden kurulur (60k düğüm için ~2 dakika).

---

## 9. Sıralama: kullanıcıya ne, hangi sırayla gösterilir

### 9.1 Birleşik skor — çarpımsal, toplamsal değil

```
S(a) = ν(a)^0.35 · T(a)^0.40 · E(a)^0.15 · A(a)^0.10

ν  yenilik                       (§2)
T  transfer yakınlığı            (Açık Sorular Defteri'ne; belge 07)
E  kanıt gücü                    (belge 01/03)
A  eyleme dönüştürülebilirlik    (somut bir adım üretiyor mu?)
```

Ağırlıklar toplamı 1 → **ağırlıklı geometrik ortalama**, sonuç `[0,1]`'de kalır.

**Neden çarpımsal?** Toplamsal skor telafiye izin verir ve bu tam olarak istemediğimiz
şeydir: "yepyeni ama senin hiçbir probleminle ilgisi yok" bir atom (ν=1, T=0) toplamsal
skorda üst sıraya çıkar ve kullanıcının ekranını çöple doldurur. Geometrik ortalamada
herhangi bir faktörün sıfıra yaklaşması skoru sıfıra çeker — **her faktör bir vetodur.**

`T` en yüksek ağırlığı alır (0.40) çünkü brifing açıktır: transfer ürünün kalbidir.
Yenilik ikincidir — yeni ama kullanılamayan bilgi, ürünün satmadığı şeydir.

Sıfır koruması: her faktöre `ε = 0.02` taban eklenir, böylece tek eksik sinyal
(ör. henüz hesaplanmamış `A`) atomu tümden yok etmez.

### 9.2 Normalizasyon

Ham skorlar **asla** doğrudan çarpılmaz. `ν`, `T`, `E`, `A` farklı dağılımlardan gelir
(`T` tipik olarak 0.2 civarında yığılır, `ν` iki tepeli). Her faktör önce
**kütüphane içi yüzdelik dilime (rank/percentile normalization)** çevrilir. Bu, tek bir
alt sistemin kalibrasyonu bozulduğunda sıralamanın tümden çökmesini engeller.

### 9.3 Çeşitlendirme ve gösterim kısıtları

Ham `S` sıralaması aynı kümeden 5 atomu art arda gösterir. **MMR (Maximal Marginal
Relevance)**, `λ = 0.7`:

```
seç: argmax_a [ λ·S(a) − (1−λ)·max_{b ∈ SEÇİLEN} sim(a,b) ]
```

Üstüne sert kısıtlar (Doktrin 1):

- Ekranda en fazla **3** atom.
- Kitap başına en fazla **2** atom.
- Aynı Leiden topluluğundan en fazla **2** atom.
- `E(a) < 0.3` olan atom asla ilk sırada gösterilmez — `[doğrulanamadı]` etiketiyle
  bir tık öteye taşınır (Doktrin 2 ve §7 madde 7).

---

## 10. Parametre özeti

| Parametre | Anlam | Başlangıç | Duyarlılık |
|---|---|---|---|
| `α`, `s₀` | σ keskinleştirici | 12, 0.78 | **Yüksek** — %94 rakamını doğrudan belirler |
| `k` | ANN komşu sayısı | 64 | Orta |
| `τ_taban` | ANN aday eşiği (kosinüs) | 0.62 | Orta |
| `τ_dup` | "bilinen" sayılma eşiği (`c`) | 0.70 | **Yüksek** |
| `τ_yeni` | "yeni" sayılma eşiği (`ν`) | 0.55 | **Yüksek** |
| K2 alt/üst bant | LLM hakeme gitme aralığı | 0.55 / 0.85 | Maliyeti belirler |
| `q` | Bölüm CVaR dilimi | 0.20 | Orta |
| `B`, `k_aralık`, `μ` | Sayfa bütçesi, aralık sayısı, ceza | 15, 3, 0.5 | Orta |
| `w₁,w₂,w₃` | Benzerlik karışımı | 0.60/0.15/0.25 | Orta |
| MinHash | perm, band × satır | 128, 16×8 | Düşük |
| PageRank `d` | sönümleme | 0.85 | Düşük |
| MMR `λ` | çeşitlilik | 0.70 | Düşük |
| Maliyet oranı | yanlış-birleştirme : yanlış-ayırma | 3 : 1 | **Yüksek** — doktrinden gelir |

**Duyarlılık uyarısı:** "Yüksek" işaretli beş parametre kullanıcıya gösterilen
`%94` sayısını doğrudan hareket ettirir. Bunlar sabit kod değil, **yapılandırma**
olmalı ve altın küme üzerinde ölçülmeden değiştirilmemelidir.

---

## 11. Sağlık ölçütleri (nasıl bileceğiz ki çalışıyor?)

| Ölçüt | Hedef | Nasıl ölçülür |
|---|---|---|
| `aynı` kararı precision | ≥ 0.95 | Altın küme, haftalık |
| `aynı` kararı recall | ≥ 0.80 | Altın küme |
| DAG döngüsüzlük | %100 (condensation sonrası) | Tarjan, her yazımda |
| Tür B döngü oranı | ≤ %3 kenarların | Gecelik |
| Sayfa tahmini isabeti | kullanıcı "değdi" oranı ≥ %70 | Okuma sonrası tek soru |
| LLM hakem/kitap | ≤ 80 çağrı | Telemetri |
| Kitap sindirim süresi | ≤ 3 dk (graf kısmı) | Telemetri |

---

## 12. Açık sorular

`AÇIK SORU 1:` Çapraz-dil `aynı` tespiti (§4.3). Ölçülmeden güvenilmemeli.

`AÇIK SORU 2:` "Kapsanmışlık" kullanıcının **hatırlaması** değil, kütüphanesinde
**bulunması** anlamına geliyor. Kullanıcı 3 yıl önce okuduğu kitabı unutmuş olabilir.
Unutma eğrisiyle `κ`'yı çarpmak (`κ' = κ · exp(−t/τ_unutma)`) doğru olabilir ama
bu bir aralıklı tekrar sistemi tasarımı gerektirir — kapsamım dışında, belge 07'ye not.

`AÇIK SORU 3:` `A(a)` (eyleme dönüştürülebilirlik) faktörünün nereden geleceği bende
tanımlı değil; belge 01 veya 07 bunu üretmeli. Üretilmezse `A = 1` sabitiyle çalışırız
ve §9.1 üç faktöre iner (ağırlıklar 0.39/0.44/0.17 olarak yeniden ölçeklenir).

`AÇIK SORU 4:` `μ` tür uyum matrisi (§2.2) benim mühendislik sezgimle dolduruldu.
Alan uzmanları (05a–05d) kendi alanları için satır düzeltmesi önerebilir; özellikle
`anekdot` satırı tarih/felsefe için fazla cezalandırıcı olabilir.
