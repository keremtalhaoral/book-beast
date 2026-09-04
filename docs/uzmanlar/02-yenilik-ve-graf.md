# 02 — Yenilik Puanı ve Atom Grafı

> **Uzman:** Uygulamalı Matematikçi (Graf Teorisi & Bilgi Erişimi)
> **Kapsam:** "Bu kitabın %94'ü zaten sende var — şu 11 sayfayı oku" hükmünü üreten motor.

---

## 3 cümlelik özet

Bir atomun yeniliği, kütüphanedeki **birbirinden bağımsız** komşuların onu ne kadar
*gerektirdiğiyle* ölçülür — noisy-OR kapsama ile, tekil maksimum benzerlikle değil.
Kitap seviyesinde iki ayrı sayı üretilir: kullanıcıya gösterilen `%94` **sayfa-ağırlıklı
kapsanma oranıdır** (kütle), "Bölüm 7'yi oku" hükmü ise **üst-kuyruk yenilik değerinden**
gelir (kuyruk); bu ikisini tek skora indirmek sistemin yapabileceği en büyük hata olurdu.
1.8 milyar çiftin tamamı asla hesaplanmaz — HNSW + tür bloklama + kademeli hakem zinciri
maliyeti kitap başına `O(m log n)`'e ve ~64 LLM çağrısına indirir.

---

## 1. Notasyon

| Sembol | Anlam |
|---|---|
| `a`, `L`, `B` | Yeni atom; kütüphane (`n` atom); yeni kitap (`m ≈ 120` atom) |
| `sim(a,e)` | Karma benzerlik `[0,1]`, **simetrik** |
| `κ(a←e)` | `e`'nin `a`'yı kapsama gücü `[0,1]`, **yönlü** |
| `c(a)`, `ν(a)` | Kapsanmışlık; **yenilik** `ν = 1 − c` |
| `pg(a)`, `T(a)`, `E(a)` | Sayfa ağırlığı; transfer yakınlığı; kanıt gücü |

Graf `G=(V,E)`: düğümler atomlar, kenarlar brifingdeki 6 ilişki; her kenarın güveni
`p ∈ (0,1]`. **Güvensiz kenar yoktur, sadece düşük `p`'li kenar vardır.**

---

## 2. Yenilik puanı formülü

### 2.1 Neden tekil maksimum yanlış

`ν(a) = 1 − max_e sim(a,e)` cazip ama çöp üretir. **(i) Parça parça kapsanma:** bir fikir
üç kitapta yarım yarım anlatılmışsa hiçbiriyle benzerlik 0.9'u geçmez, ama birlikte fikri
tümüyle içerirler. **(ii) Yön körlüğü:** kosinüs simetriktir, kapsama değildir — "düzgün
süreklilik" tanımı "süreklilik" tanımını kapsar, tersi doğru değildir.

### 2.2 Kapsama gücü (yönlü)

```
κ(a ← e) = σ(sim(a,e)) · ent(e ⊨ a) · θ(e) · μ(tür(a), tür(e))

σ(s)   = 1 / (1 + exp(−α·(s − s₀)))     keskinleştirici, α = 12, s₀ = 0.78
ent(·) = cross-encoder gerektirme olasılığı [0,1]   (§3)
θ(e)   = 0.6 + 0.4·E(e)                 zayıf kanıtlı atom zayıf kapsar
μ(·)   = tür uyum matrisi (aşağıda)
```

`σ` şarttır: ham kosinüs 0.65 "aynı konudan bahsediyor" demektir, "aynı şeyi söylüyor"
demez; lojistik keskinleştirici 0.78 civarında eşik davranışı verir.

**Tür uyum matrisi `μ`** (satır = kapsanan `a`, sütun = kapsayan `e`):

| a \ e | tanım | teorem | yöntem | formül | iddia | anekdot |
|---|---|---|---|---|---|---|
| **tanım** | 1.00 | 0.35 | 0.10 | 0.20 | 0.30 | 0.00 |
| **teorem** | 0.15 | 1.00 | 0.10 | 0.55 | 0.40 | 0.00 |
| **yöntem** | 0.10 | 0.25 | 1.00 | 0.30 | 0.35 | 0.05 |
| **formül** | 0.10 | 0.60 | 0.20 | 1.00 | 0.20 | 0.00 |
| **iddia** | 0.25 | 0.55 | 0.30 | 0.30 | 1.00 | 0.20 |
| **anekdot** | 0.00 | 0.00 | 0.05 | 0.00 | 0.30 | 1.00 |

Bir anekdot hiçbir teoremi kapsayamaz (0.00): hikâyeyi okumuş olmak teoremi bilmek değildir.

### 2.3 Bağımsız temsilciler ve nihai formül

Beş komşunun üçü birbirinin kopyasıysa kapsamayı üç kez artırmamalı:

```
1. N_k(a) ← ANN top-k komşu, sim ≥ τ_taban
2. N_k(a) içindekileri KENDİ aralarında `aynı` ilişkisiyle kümele (union-find)
3. Her sınıftan en yüksek κ'lı tek temsilci → R(a) = bağımsız kapsayıcılar

c(a) = 1 − Π_{r ∈ R(a)} ( 1 − κ(a ← r) )        ← noisy-OR
ν(a) = 1 − c(a)
```

Noisy-OR seçildi çünkü `[0,1]`'de kalır (kırpma yok), tek güçlü kapsayıcı (κ=0.95) ile
beş zayıf kapsayıcıyı doğru sıralar ve bağımsızlık varsayımı 2. adımda **inşa edilmiştir**,
keyfî değildir. Örnek: `κ = (0.55, 0.40, 0.30)` → `c = 1 − 0.45·0.60·0.70 = 0.811`,
`ν = 0.189`.

Kullanıcıya gösterilen **"5 farklı kitaptan"** ifadesi doğrudan `|{kitap(r) : r ∈ R(a)}|`
sayısıdır — sonradan uydurulmuş değil, hesabın kendi içinden çıkan gerçek nicelik.

### 2.4 Bölüm seviyesine toplama — CVaR

**Ortalama kullanılmaz:** 40 sıradan atom içindeki 3 mücevheri boğar; bu doğrudan
Doktrin 3'ün ihlalidir. **Maksimum da kullanılmaz:** tek gürültülü atom bütün bölümü
"yepyeni" ilan eder. Seçim: **üst-kuyruk ortalaması (CVaR / superquantile), `q = 0.20`.**

```
N_bölüm = ( 1 / ⌈q·|Ch|⌉ ) · Σ_{a ∈ top-q(Ch, ν)} ν(a)·ω(a)
ω = tür ağırlığı: teorem 1.0 · yöntem 0.9 · formül 0.9 · tanım 0.8 · iddia 0.7 · anekdot 0.4
```

CVaR, maksimum (`q→0`) ile ortalama (`q→1`) arasında sürekli bir ailedir; `q=0.20`
24 atomluk bir bölümde en iyi 5 atoma bakar — tek hatalı atomun hükmü çevirmesine izin
vermeyecek kadar geniş, mücevheri boğmayacak kadar dar.

### 2.5 Kitap seviyesi — iki ayrı sayı (belgenin en kritik kararı)

```
KÜTLE  (kullanıcıya gösterilen %94)
  P_bilinen = Σ_a pg(a)·1[ c(a) ≥ τ_dup ]  /  Σ_a pg(a)

KUYRUK (okuma kararını veren)
  V_kitap = Σ_{a ∈ top-12(B, S)} S(a)          S = §9 birleşik skor
```

**Neden sayfa-ağırlıklı?** Kullanıcı atom değil sayfa okur; atom-sayısı ağırlıklı bir oran,
formül yoğun 2 sayfayı 20 sayfalık anlatıyla eşitler ve "%94" yalan olur.
**Neden iki sayı?** `P_bilinen = 0.94` ile yüksek `V_kitap` aynı anda tutarlıdır ve tam
olarak Doktrin 3'ün cümlesidir; tek skorla bu ifade edilemez. Bu yüzden kitap seviyesinde
asla tek bir "kitap puanı" göstermeyiz — o sayı hiçbir karar vermez.

---

## 3. Çift tespiti boru hattı

Beş kademe; her kademe bir öncekini 5–20× daraltır.

```
K0  NORMALİZE + TAM ÇİFT
    Kanonik iddia cümlesi → SimHash(64 bit); Hamming ≤ 3 → doğrudan `aynı`.
    Alıntı ve baskı tekrarları burada elenir, maliyeti ihmal edilebilir.

K1a ANN (yoğun)   HNSW M=32, efC=200, efS=128, top-k=64, cos ≥ τ_taban=0.62
K1b LSH (seyrek)  MinHash 128 perm, 5-gram shingle, b=16×r=8, Jaccard ≥ 0.55
                  → formül/notasyon tekrarını yakalar; yoğun gömme sembol
                    dizilerinde zayıftır, bu kanal onu telafi eder.
    ADAY = K1a ∪ K1b

K2  ÇAPRAZ KODLAYICI (cross-encoder) — YÖNLÜ
    Girdi (öncül=e, sonuç=a) → P(e ⊨ a) ve P(a ⊨ e) AYRI AYRI. 6 katman, ONNX int8, 1.5 ms.
    p < 0.55 → at.   p > 0.85 → kabul.   Arada → BELİRSİZ BANT → K3.

K3  LLM HAKEM (yalnız belirsiz bant)
    Tek etiket: {aynı, a⊂e, e⊂a, çelişiyor, tamamlayıcı, ilgisiz} + tek cümle gerekçe
    + iki tarafın sayfa çapası. "tamamlayıcı" kritik: aynı değil ama birlikte a'yı kapsıyorlar.

K4  BİRLEŞTİRME
    `aynı` kenarları union-find'a → eşdeğerlik sınıfları.
    Yönlü `⊂` kenarları κ hesabına ent(·) olarak girer.
```

### 3.1 Eşiklerin kalibrasyonu

**Altın küme:** alan başına 50, toplam 400 çift (200+/200−). Negatiflerin yarısı **zor
negatif** olmalı (aynı konu, farklı iddia) — asıl tehlike onlardır.

**Yöntem:** cross-encoder ham skoru **Platt ölçekleme** ile olasılığa çevrilir (2 parametre,
lojistik regresyon). Eşik maliyet matrisiyle seçilir: yanlış **birleştirme** (aslında yeni,
"zaten var" dedik) maliyeti **3**, yanlış **ayırma** maliyeti **1**. Bu 3:1 oranı doğrudan
Doktrin 3'ten gelir — yanlışlıkla gizlenen fikri kullanıcı asla göremez ve kaybını fark
bile edemez; fazladan gösterilen fikir 30 saniye kaybettirir.
**Hedef: `precision(aynı) ≥ 0.95` kısıtı altında recall'u maksimize et.**

**Sürekli kalibrasyon:** belirsiz bandın merkezine en yakın çiftlerden **haftada en fazla
5 tanesi** kullanıcıya sorulur ("bu ikisi aynı fikir mi?"); her 50 yeni etikette Platt
parametreleri yeniden fit edilir. Haftada 5 sınırı Doktrin 1'dendir.

---

## 4. Gömme stratejisi

### 4.1 Ne gömülür

**Atomun tamamı değil, kanonik iddia cümlesi.** Tam metin kitabın üslubunu ve bölüm
bağlamını taşır; aynı fikri iki farklı kitapta uzaklaştıran şey tam olarak budur.

| Temsil | İçerik | Kullanım |
|---|---|---|
| `v_iddia` (1024d) | Tek cümlelik kanonik iddia | Ana ANN indeksi |
| `v_bağlam` (1024d) | İddia + bölüm başlığı + alan | Belirsizlik giderme |
| `h_sözlük` (128 perm) | Terim/sembol çekirdeği MinHash | LSH kanalı |
| `h_yapı` | Kanonik formül AST hash'i | Sembolik eşleşme |

```
sim(a,e) = w₁·cos(v_iddia) + w₂·cos(v_bağlam) + w₃·yapısal(a,e)
w = (0.60, 0.15, 0.25) formüllü atomlarda · (0.80, 0.20, 0.00) formülsüzlerde
```

**Boyut ekonomisi:** Matryoshka kesimli model — ANN kaba eleme ilk **256 boyutla**
(4× hızlı, 4× az bellek), top-64 aday tam **1024 boyutla** yeniden puanlanır.

### 4.2 Matematiksel notasyon problemi

`∀ε>0 ∃δ>0 : |x−a|<δ ⟹ |f(x)−f(a)|<ε` metnini gömme modeline vermek gürültü üretir;
tokenizer sembolleri parçalar, benzerlik anlamdan değil sembol yoğunluğundan doğar.

**(1) Kanonikleştirme.** Formül SymPy ile ayrıştırılır; serbest değişkenler bağlanma
sırasına göre yeniden adlandırılır (`x₁, x₂, …` — de Bruijn ruhu), sabitler ve birimler
normalize edilir. `f''(x) > 0` ile `g''(t) > 0` aynı kanonik dizeyi verir → `h_yapı`.

**(2) Nesirleştirme.** Atom üretilirken formülün **doğal dil karşılığı** bir kez LLM ile
yazılır ve kalıcı saklanır: `f'' > 0` → "ikinci türev her yerde pozitif, yani dışbükey".
**Gömme bu nesirden alınır; sembol gömme modeline hiç girmez.**

**(3) Yapısal eşleşme ayrı kanalda.** Formül kimliği vektör uzayında değil sembolik
indekste aranır:

```
yapısal(a,e) = 1                                     h_yapı eşitse
             = 1 − TED(A_a, A_e)/max(|A_a|,|A_e|)    aksi halde
TED = ağaç düzenleme mesafesi; yalnız K1b adaylarında hesaplanır
```

Böylece Cauchy–Schwarz iki kitapta farklı harflerle yazılmış olsa da `h_yapı` üzerinden
birebir eşleşir — gömme modelinin yeteneğine hiç bağlı kalmadan.

**Alan uyarlaması:** tam ince ayar yapılmaz (kullanıcı verisi gizli, tek kullanıcıda
overfit riski yüksek). Kütüphane 5.000 atomu geçtiğinde **whitening (ZCA) + öğrenilmiş
köşegen ölçekleme**: onaylanmış `aynı` çiftlerinden `d` parametreli köşegen metrik
öğrenilir (kontrastif kayıp, dakikalar). Geri alınabilir, denetlenebilir, ucuz.

---

## 5. Önkoşul DAG'ı

### 5.1 Kenar üretimi

| Kaynak | Nasıl | `p` |
|---|---|---|
| Kanıt zinciri | İspatta atıf yapılan lemma | 0.90 |
| Açık önkoşul | Katman 1 çıkarımı ("ölçü teorisi gerekir") | 0.85 |
| Terim–tanım | Atom `t` terimini kullanıyor, `d(t)` tanımı var → `d(t) → a` | 0.75 |
| Kitap içi sıra | Aynı kitapta önce gelen sonrakini önceler | 0.25 |

Kitap-içi-sıra kenarları kasten çok düşük güvenlidir: yazarın sırası pedagojik gerçeği
değil editoryal tercihi yansıtır; döngü kırmada ilk feda edilenler bunlardır.

### 5.2 Döngü çıkarsa

Döngüler **iki farklı şeyin** işaretidir ve farklı işlem görürler.

**Tür A — gerçek karşılıklı bağımlılık.** "İç çarpım" ile "norm" gerçekten birbirini
gerektirir; bu hata değil pedagojik olgudur. → **Tarjan ile güçlü bağlı bileşenleri (SCC)
bul, her SCC'yi tek süper-düğüme daralt (condensation).** Daraltılmış graf **tanım gereği**
asikliktir; DAG ondan kurulur. Süper-düğüm kullanıcıya "bu üç kavram birlikte öğrenilir"
diye sunulur — doğru olan da budur.

**Tür B — çıkarım hatası.** SCC'nin kenar güvenleri düşükse ya da SCC 5 düğümden büyükse
bu hatadır. → **Minimum geri-besleme yay kümesi (Minimum Feedback Arc Set)**; NP-zor
olduğundan **Eades–Lin–Smyth doğrusal-zamanlı sezgiseli** ile bir düğüm sıralaması
üretilir, sıralamaya ters düşen kenarlar aday hatadır ve **en düşük `p`'liden başlanarak**
SCC kırılana dek düşürülür.

**Karar kuralı:** `|SCC| ≤ 5 ve min p ≥ 0.70` → Tür A (daralt); aksi halde Tür B (kır).
Düşürülen kenar **silinmez**, `[şüpheli önkoşul]` etiketiyle pasif saklanır ve haftalık
5 sorudan biri olabilir. Doktrin 2 — hiçbir şey sessizce kaybolmaz.

### 5.3 Topolojik sıralamadan okuma sırası

Bir DAG'ın topolojik sıralaması tek değildir (tipik olarak milyonlarca geçerli sıra vardır);
ürünün işi geçerli olanı değil **en iyisini** seçmektir. **Kahn + öncelik kuyruğu:**

```
hazır ← giriş-derecesi 0 olan düğümler
while hazır ≠ ∅:
    v ← argmax_{u ∈ hazır} öncelik(u);  sıraya ekle;  v'nin kenarlarını sil

öncelik(u) = 0.45·T(u)             transfer yakınlığı
           + 0.30·kilit(u)         u okununca hazır hale gelen düğüm sayısı (log-norm)
           + 0.15·ν(u)             yenilik
           − 0.10·konu_değişimi(u) önceki düğümden farklı alandaysa ceza
```

`kilit(u)` kritiktir: bir tanım 14 teoremi açıyorsa kendisi sıkıcı olsa bile öne alınır —
bu, DAG'daki **darboğaz düğümlerini** otomatik öne çeker. `konu_değişimi` cezası bağlam
değiştirme maliyetini modeller; kullanıcı kafa karışıklığından nefret ediyor.

---

## 6. "Şu 11 sayfayı oku" hesabı

### 6.1 Formülasyon

Bu **saf küme kapsama değildir** — sayfalar tek boyutlu ve sıralıdır; okunan şey rastgele
bir küme değil **bitişik aralıklardır**.

```
Girdi: sayfalar 1..P; A = { a : ν(a) ≥ τ_yeni }; span(a) = [l_a, r_a]; kazanç g(a) = S(a)
Karar: en fazla k ayrık aralık I₁..I_k
Amaç:  maks  Σ_{a: span(a) ⊆ ∪I_j} g(a)  −  μ·k
Kısıt: Σ_j |I_j| ≤ B          Başlangıç: B=15, k=3, μ=0.5, τ_yeni=0.55
```

`μ·k` terimi olmazsa çıktı "7, 44, 91, 158 ve 203. sayfaları oku" olur — işe yaramaz.
Her ayrı aralık okuma sürtünmesi yaratır; 3×4 sayfa, tek 12 sayfadan pahalıdır.

### 6.2 Bu problem TAM olarak çözülebilir

Aralıklar tek boyutta bitişik olduğundan problem dinamik programlamaya düşer:

```
D[i][b][j] = ilk i sayfa işlenmiş, b bütçe harcanmış, j aralık kullanılmışken en iyi kazanç
D[i][b][j] = max( D[i−1][b][j],                                        sayfa i'yi alma
                  max_{t≥1} ( D[i−t][b−t][j−1] + kazanç(i−t+1…i) − μ )  [i−t+1,i] aralığını al )
```

`P≈400, B≈40, k≈4`, iç döngü `t ≤ B` → ~2.6M işlem, milisaniyeler. **Yani burada yaklaşık
algoritmaya gerek yoktur, optimumu buluruz** — ürünün en görünür hükmü matematiksel olarak
kesin olur.

### 6.3 Açgözlü algoritma (çok kitaplı genel durum)

Birleşik plan üretiminde aralıklar tek eksende olmadığından DP çöker; oradaki hâl klasik
**bütçeli maksimum kapsamadır** ve açgözlü çalışır:

```
SEÇİLEN ← ∅ ;  kalan ← B
while kalan > 0 ve |SEÇİLEN| < k:
    her aday aralık I için (|I| ≤ kalan):
        marj(I) ← ( Σ_{yeni kapsanan a} g(a) − μ ) / |I|      ← YOĞUNLUK, toplam değil
    I* ← argmax marj(I);  if marj(I*) ≤ 0: break
    SEÇİLEN += I* ;  kalan −= |I*|
# köprüleme: iki seçili aralık arası boşluk ≤ 3 sayfa ise birleştir (μ tasarrufu > köprü maliyeti)
```

Kazanç submodüler (aynı atom iki kez sayılmaz) + bütçe doğrusal → yoğunluk-açgözlü,
tekil-en-iyi ile karşılaştırıldığında **(1 − 1/e) ≈ 0.632** garantisi verir. Toplam kazanca
göre seçmenin hiçbir garantisi yoktur — bütçeyi tek büyük aralığa yatırır.

### 6.4 Önkoşul kapanışı

Seçilen aralıktaki atomların DAG önkoşulları: kütüphanede varsa sorun yok; **aynı kitapta
ve seçilmemişse** dahil etme maliyeti hesaplanır, ucuzsa bütçeden karşılanır; **hiçbir
yerde yoksa** ayrı bir "önce şunu bil" satırı olur, ana aralığa karıştırılmaz. Ekranda tek
karar kalır: "Bölüm 7, sayfa 142–152 (11 sayfa)"; uyarı bir tık ötede durur.

---

## 7. Graf sorguları

| # | Soru | Algoritma | Maliyet | Tazelik |
|---|---|---|---|---|
| 1 | Bu fikri hangi kitaplar destekliyor/çürütüyor? | Tip-filtreli 1–2 hop komşuluk, `E(·)` sıralaması | `O(deg²)` | anlık |
| 2 | En merkezi 10 fikrim | **Kişiselleştirilmiş PageRank** (`önkoşulu`+`genellemesi`+`destekler`, d=0.85) | Forward-Push | gecelik |
| 3 | Boşluk (A) — eksik temel | DAG'da **askıda önkoşul**: hiçbir atomun karşılamadığı önkoşul referansı | `O(V+E)` | gecelik |
| 4 | Boşluk (B) — eksik köprü | **Leiden** topluluk tespiti → arası kenar yoğunluğu ≈ 0 olan topluluk çiftleri | `O(E log V)` | haftalık |
| 5 | Boşluk (C) — karşılanmamış ihtiyaç | Açık Sorular Defteri'ndeki soruya en yakın atom `sim < 0.5` | `O(\|Q\|·log n)` | anlık |
| 6 | Bu iki fikir nasıl bağlanır? | **Dijkstra**, `w = −log p` → olasılık çarpımını maksimize eden en olası yol | `O(E log V)` | anlık |
| 7 | Bunu okumak için ne bilmeliyim? | DAG'da **ters ulaşılabilirlik** (atalar), BFS | `O(V+E)` yerel | anlık |
| 8 | Çelişki kümelerim | `çelişiyor` alt-grafında bağlı bileşenler + **yapısal denge** (dengesiz üçgen) | `O(E)` | gecelik |
| 9 | Bu kitap hangi kümemi büyütüyor? | Topluluk ataması + **modülerlik değişimi `ΔQ`** | `O(m·deg)` | kitap başına |
| 10 | En kırılgan fikrim hangisi? | PageRank yüksek **ama** `\|R(a)\| = 1` (tek kaynaklı) | `O(V)` | gecelik |

**Neden PageRank, derece değil:** derece merkeziliği en çok tekrarlanan fikri ödüllendirir
(genelde popüler kitapların ortak klişesi); PageRank *üzerine çok şey inşa edilmiş* fikri
ödüllendirir — `önkoşulu` kenarları yönlü akıtıldığında bu tam olarak "temel" demektir.
**#10 ürünün epistemik dürüstlüğüdür:** merkezî olup tek kaynağa dayanan fikirler
kütüphanenin en riskli noktalarıdır; o tek kitap yanılıyorsa bütün yapı yanılır.

---

## 8. Ölçekleme: 1.8 milyar çiftten kurtulmak

`n = 60.000` → `n(n−1)/2 ≈ 1.8×10⁹` çift; bu sayı hiçbir zaman hesaplanmaz.
**(1) Graf artımlı kurulur, asla baştan kurulmaz** — yeni kitapta sadece `m = 120` atom
sorgulanır, `O(m log n)`. **(2) Bloklama** — aday üretimi tür ve alanla ön-filtrelenir,
anekdot teoremle asla karşılaştırılmaz (`μ=0`); ~3× tasarruf, **doğruluktan sıfır kayıp**,
çünkü elenen çiftlerin κ'sı zaten sıfırdır.

| Kademe (bir kitap, m=120) | Girdi | Çıktı | Birim | Toplam |
|---|---|---|---|---|
| K0 SimHash | 120 | 120 | ~0 | ihmal |
| K1 HNSW+LSH | 120 × 64 | ~7.700 çift | 0.4 ms/sorgu | **50 ms** |
| Bloklama + `τ_taban` | 7.700 | ~800 çift | ~0 | ihmal |
| K2 Cross-encoder | 800 | ~180 kabul | 1.5 ms | **1.2 sn** |
| K3 LLM hakem | ~64 | 64 karar | ~1.5 sn | **~40 sn** (8 paralel) |

**Kitap başına ~1 dakika, ~64 LLM çağrısı.** İlk toplu kurulum (500 kitap):
`500 × 64 = 32.000` çağrı, bir kereye mahsus, **Batch API** ile (%50 indirim, gecikme
önemsiz). Kütüphane büyüdükçe kalibrasyon iyileşir, belirsiz bant *daralır* — maliyet
alt-doğrusal büyür.

```
BELLEK
Vektörler  60.000 × 1024 × 4B = 246 MB → int8 quantize = 61 MB (cos kaybı < 0.01)
HNSW grafı 60.000 × 32 × 4B ≈ 7.7 MB   MinHash 60.000 × 128 × 4B = 31 MB
TOPLAM ~100 MB → tek makinede, RAM'de, sharding'siz.
```

**Artımlı güncelleme:** yeni atomda sadece komşuların `ν`'sü değişir (`O(k)`); eşdeğerlik
sınıfları union-find ile neredeyse `O(1)`; PageRank Forward-Push ile yerel güncellenir, tam
hesap gecelik toplu işte; HNSW silme desteklemediğinden silinenler `tombstone` işaretlenir
ve indeks 30 günde bir yeniden kurulur (60k düğüm ≈ 2 dakika).

500 kitap ölçeğinde dağıtık hiçbir şeye ihtiyaç yoktur: bu bir ölçek problemi değil,
bir algoritma seçimi problemidir.

---

## 9. Sıralama: ne, hangi sırayla gösterilir

```
S(a) = ν(a)^0.35 · T(a)^0.40 · E(a)^0.15 · A(a)^0.10        ağırlıklı geometrik ortalama

ν yenilik (§2) · T transfer yakınlığı (belge 07) · E kanıt gücü (belge 01/03)
A eyleme dönüştürülebilirlik (somut bir adım üretiyor mu?)
```

**Neden çarpımsal?** Toplamsal skor telafiye izin verir ve istemediğimiz tam da budur:
"yepyeni ama hiçbir problemine değmeyen" bir atom (ν=1, T=0) toplamsal skorda üste çıkar ve
ekranı çöple doldurur. Geometrik ortalamada herhangi bir faktörün sıfıra yaklaşması skoru
sıfıra çeker — **her faktör bir vetodur.** `T` en yüksek ağırlığı alır (0.40): brifing
açıktır, transfer ürünün kalbidir; yenilik ikincidir, çünkü yeni ama kullanılamayan bilgi
ürünün satmadığı şeydir. Sıfır koruması: her faktöre `ε = 0.02` taban eklenir.

**Normalizasyon:** ham skorlar asla doğrudan çarpılmaz — `ν, T, E, A` farklı dağılımlardan
gelir (`T` 0.2 civarında yığılır, `ν` iki tepelidir). Her faktör önce **kütüphane içi
yüzdelik dilime (rank normalization)** çevrilir; böylece tek bir alt sistemin kalibrasyonu
bozulduğunda sıralama tümden çökmez.

**Çeşitlendirme:** ham `S` sıralaması aynı kümeden 5 atomu art arda gösterir. **MMR**,
`λ = 0.7`: `argmax_a [ λ·S(a) − (1−λ)·max_{b ∈ SEÇİLEN} sim(a,b) ]`. Üstüne sert kısıtlar
(Doktrin 1): ekranda en fazla **3** atom · kitap başına en fazla **2** · aynı Leiden
topluluğundan en fazla **2** · `E(a) < 0.3` olan atom asla ilk sırada gösterilmez,
`[doğrulanamadı]` etiketiyle bir tık öteye taşınır (Doktrin 2).

---

## 10. Parametreler ve sağlık ölçütleri

| Parametre | Anlam | Başlangıç | Duyarlılık |
|---|---|---|---|
| `α`, `s₀` | σ keskinleştirici | 12, 0.78 | **Yüksek** |
| `τ_dup` / `τ_yeni` | "bilinen" (`c`) / "yeni" (`ν`) eşiği | 0.70 / 0.55 | **Yüksek** |
| Maliyet oranı | yanlış-birleştirme : yanlış-ayırma | 3 : 1 | **Yüksek** |
| K2 bandı | LLM hakeme gitme aralığı | 0.55 – 0.85 | Maliyeti belirler |
| `k` / `τ_taban` | ANN komşu sayısı / aday eşiği | 64 / 0.62 | Orta |
| `q` | Bölüm CVaR dilimi | 0.20 | Orta |
| `B`, `k_aralık`, `μ` | Sayfa bütçesi, aralık sayısı, ceza | 15, 3, 0.5 | Orta |
| `w₁,w₂,w₃` | Benzerlik karışımı | 0.60/0.15/0.25 | Orta |
| MinHash · PageRank `d` · MMR `λ` | — | 128·16×8 / 0.85 / 0.70 | Düşük |

"Yüksek" işaretli üç satır kullanıcıya gösterilen `%94` sayısını doğrudan hareket ettirir;
bunlar sabit kod değil **yapılandırma** olmalı ve altın küme üzerinde ölçülmeden
değiştirilmemelidir.

| Sağlık ölçütü | Hedef | Ölçüm |
|---|---|---|
| `aynı` precision / recall | ≥ 0.95 / ≥ 0.80 | Altın küme, haftalık |
| DAG döngüsüzlük (condensation sonrası) | %100 | Tarjan, her yazımda |
| Tür B döngü oranı | ≤ %3 kenar | Gecelik |
| Sayfa tahmini isabeti ("değdi" oranı) | ≥ %70 | Okuma sonrası tek soru |
| LLM hakem/kitap · graf süresi | ≤ 80 çağrı · ≤ 3 dk | Telemetri |

---

## 11. Açık sorular

`AÇIK SORU 1:` **Çapraz-dil `aynı` tespiti.** Türkçe ve İngilizce kitaptaki aynı fikrin
hizalanma kalitesi ölçülmedi; 200 çiftlik çapraz-dil altın kümesi kurulana kadar bu
kararlar **zorla belirsiz banda** itilmeli (her zaman LLM hakeme gitmeli).

`AÇIK SORU 2:` **Kapsanmışlık ≠ hatırlama.** `c(a)` fikrin kütüphanede *bulunması* demek,
kullanıcının *hatırlaması* değil. Unutma eğrisiyle çarpmak (`κ' = κ·exp(−t/τ_unutma)`)
doğru olabilir ama aralıklı tekrar sistemi tasarımı gerektirir — belge 07'ye not.

`AÇIK SORU 3:` **`A(a)` nereden gelecek?** Eyleme dönüştürülebilirlik faktörünü belge 01
veya 07 üretmeli; üretilmezse `A = 1` sabitiyle çalışırız ve §9 üç faktöre iner
(ağırlıklar 0.39 / 0.44 / 0.17 olarak yeniden ölçeklenir).

`AÇIK SORU 4:` **`μ` tür uyum matrisi (§2.2)** mühendislik sezgimle dolduruldu; alan
uzmanları (05a–05d) kendi satırlarını düzeltmeli — özellikle `anekdot` satırı tarih ve
felsefe için fazla cezalandırıcı olabilir.
