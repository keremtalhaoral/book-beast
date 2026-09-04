# 10 — Analitik Titizlik: Sayılar Ne Zaman Yalan Söyler

> **Uzman:** Saf Matematik Profesörü II (Gerçel Analiz, Ölçü Teorisi, Olasılık)
> **Rol:** Denetçi. Bu belge yeni özellik önermez; diğer belgelerin ürettiği **sayıların anlamlı
> olup olmadığını** denetler ve her matematiksel itirazı somut bir mühendislik kuralına bağlar.

---

## 3 cümlelik özet

Uygulama kullanıcıya "bu kitabın %94'ü zaten sende var" gibi kesin görünen sayılar söyleyecek; bu sayı yanlış hesaplanırsa uygulama **kendinden emin bir yalancıya** dönüşür ve kullanıcı gerçekten yeni olan 11 sayfayı atlar. Bu belge o sayının ne zaman dürüst ne zaman uydurma olduğunu tespit eder: yüzdenin paydası cevabı belirler, "benzer" ile "aynı" farklı şeylerdir, ve kütüphaneye kitap eklemek asla eski bir kitabı daha yeni gösteremez. Sonuç: uyulması zorunlu 8 aksiyom, her biri için otomatik bir test, ve sistemin **"bilmiyorum" demek zorunda olduğu** koşulların listesi.

---

## 0. Notasyon ve denetlenen formül

`02-yenilik-ve-graf.md` bu belge yazılırken mevcut değildi; denetlenen formülü açıkça
**varsayıyorum**. 02 farklı bir formül önerse de §3'teki aksiyomlar bağlayıcıdır.

$\mathcal{A}$ atom evreni; $A_B$ yeni kitabın atomları ($n=\lvert A_B\rvert$); $L$ kütüphane atomları;
$\phi(a)\in S^{d-1}$ birim küredeki gömme; $\mathrm{sim}$ kosinüs benzerliği; $\tau$ "aynı fikir" eşiği;
$w(a)$ atom ağırlığı (sayfa kütlesi, §1.2).

$$N(B \mid L) \;=\; \frac{1}{n}\sum_{a \in A_B} \mathbf{1}\!\left[\max_{b \in L}\mathrm{sim}(a,b) < \tau\right], \qquad \text{ekranda: } 1-N(B\mid L)$$

Bu formül **dört yerinden** kırılgan: gösterge fonksiyonu (§4), kosinüs (§2), payda (§1.2),
eşiğin kalibrasyonsuzluğu (§5).

---

## 1. "Yenilik" iyi tanımlı bir ölçü müdür?

### 1.1 Toplanabilirlik: kısmen evet — ve tam da yanlış yerde hayır

Normalize **edilmemiş** sayaç formu $M(S)=\sum_{a\in S} w(a)\mathbf{1}[a\ \text{yeni}]$
sonlu evrende ağırlıklı sayma ölçüsüdür: $M(\emptyset)=0$, negatif değil, ayrık kümelerde
toplanabilir — **gerçek bir ölçüdür**, $M(A_B)$ ile bölününce olasılık ölçüsü olur.
Sorun, yeniliğin *neye karşı* ölçüldüğünde başlar. İki farklı büyüklük vardır:

- **Bağımsız yenilik** $N_{\text{sta}}(S)$: $S$ yalnız $L$'ye karşı ölçülür → **toplanabilir**.
- **Marjinal yenilik** $N_{\text{mar}}(S)$: $S$, $L \cup (A_B\setminus S)$'e karşı ölçülür → **submodüler**.

Kitabın 3. ve 7. bölümü aynı yeni fikri taşıyorsa, her biri tek başına yenidir ama
birleşimde o fikir bir kez sayılır: $N_{\text{mar}}(X\cup Y) \le N_{\text{mar}}(X)+N_{\text{mar}}(Y)$,
eşitlik ancak hiçbir fikri paylaşmadıklarında.

> ⚠️ **RİSK — Yüzdeler toplanmıyor.** Kullanıcı "Bölüm 3 %20 yeni, Bölüm 7 %15 yeni" görür,
> kitap sayfasında "kitap %22 yeni" yazar. $20+15\ne22$. Kullanıcı bunu hesap hatası sanar
> ve tüm sayılara güvenini kaybeder — haklı olarak: sistem ona iki farklı büyüklüğü aynı
> isimle sunmuştur.

**KURAL 1.1** — API ve arayüzde iki ayrı alan: `standalone_novelty` (toplanabilir, sıra bağımsız)
ve `marginal_novelty` (submodüler, seçime bağlı). Aynı ekranda ikisi birden gösterilmez:
bölüm listesinde `standalone`, "şunları oku" seçiminde `marginal`.
**Test:** `sum(standalone(ch)) == standalone(book)` (tam eşitlik); rastgele bölüm çiftleri için
`marginal(X ∪ Y) <= marginal(X) + marginal(Y) + 1e-9`.

**Submodülerlik bir hata değil, hediyedir.** $f(S)=\lvert\mathrm{Kapsam}(L\cup S)\rvert-\lvert\mathrm{Kapsam}(L)\rvert$
monoton submodüler bir kapsama fonksiyonudur; dolayısıyla doktrin #3'ün "şu 11 sayfayı oku"
problemi = sayfa bütçesi altında maksimum kapsama, ve açgözlü algoritma $1-1/e\approx0{,}632$
garantisi verir. **KURAL 1.1b** — Sayfa seçimi açgözlü submodüler maksimizasyonla yapılır;
dokümanda ve kod yorumunda "optimal" değil "$0{,}632$-yaklaşık" denir.

### 1.2 "%94" neyin yüzdesi? — Payda krizi

Aynı kitap, aynı kütüphane, beş payda, beş farklı sayı:

| # | Payda | Sonuç | Ne söyler |
|---|---|---|---|
| P1 | Atom sayısı | 24 / 400 → **%6 yeni** | Fikir çeşitliliği |
| P2 | Sayfa sayısı | 11 / 300 → **%3,7 yeni** | Okuma süresi |
| P3 | Token sayısı | **%4,1 yeni** | Metin kütlesi |
| P4 | Bilgi içeriği $\sum-\log p(a)$ | **%29 yeni** | Şaşırtıcılık |
| P5 | Transfer değeri (Açık Sorular'a katkı) | **%61 yeni** | Kullanıcıya faydası |

> ⚠️ **RİSK — Payda alışverişi.** Sistem aynı kitap için dürüstçe %3,7 ile %61 arasında
> **herhangi bir sayı** üretebilir. Bu bir yazılım hatası değil, sorunun **kötü konumlanmış
> (ill-posed)** olmasıdır: payda seçilmeden "%94" ifadesi, birimi olmayan bir sayı gibi anlamsızdır.

**Karar: payda P2 (sayfa kütlesi).** Gerekçe: doktrin #3 kullanıcıya bir **eylem** verir
(kaç sayfa okuyacağını); gösterilen yüzde o eylemle aynı birimden değilse iki sayı çelişir.

**KURAL 1.2 (tutarlılık değişmezi)** — Yüzde ile önerilen sayfa sayısı aynı büyüklükten türer:

```
assert abs((1 - shown_coverage) * total_pages - recommended_pages) <= 0.05 * total_pages
```

CI'da kırmızı yanan bir testtir: "%94'ü sende var" deyip 300 sayfadan 60 sayfa öneren bir
çıktı, kullanıcı görmeden önce derlemede yakalanır.

**KURAL 1.2b (çıplak yüzde yasağı)** — Hiçbir ekranda yalın yüzde yok; format daima mutlak
çapa taşır: **"%94'ü sende var — kalan 11 sayfa (300 sayfadan)."** Mutlak sayı, paydası
kaybolmuş bir oranın anlamını geri verir. P4 ve P5 atılmaz; `surprisal_score` ve
`transfer_score` adlarıyla iç sıralamada yaşar, **asla yüzde olarak gösterilmez**.

---

## 2. Fikir uzayı bir metrik uzay mı? — Hayır.

### 2.1 Kosinüs bir metrik değildir (somut karşı örnek)

$d_{\cos}=1-\mathrm{sim}$ ve $\mathbb{R}^2$'de üç birim vektör: $e_1=(1,0)$, $e_2=(0,1)$,
$m=\tfrac{1}{\sqrt2}(1,1)$.

$$d(e_1,e_2)=1{,}000, \quad d(e_1,m)=d(m,e_2)=1-\tfrac{1}{\sqrt2}=0{,}293, \quad 0{,}293+0{,}293=0{,}586 < 1{,}000$$

Üçgen eşitsizliği **ihlal edilmiştir** — yaklaşıklık hatası değil, yapısal bir olgu.
Buna karşılık **açısal uzaklık** $d_\theta=\arccos(\mathrm{sim})/\pi\in[0,1]$ küre üzerinde
geodeziktir ve **gerçek metriktir** (örnekte $45°+45°=90°$, eşitlik). Öklid kirişi
$\sqrt{2-2\cos}$ de metriktir.

### 2.2 Üçgen eşitsizliği olmadan sessizce bozulanlar

| Bileşen | Nasıl bozulur | Belirti |
|---|---|---|
| Metrik ağaçlar (VP/Ball/M-tree) | Budama üçgen eşitsizliğine **dayanır** | Komşular sessizce kaybolur, hata mesajı yok |
| HNSW / IVF | Yaklaşık geri çağırma daha da düşer | Recall@10 hedefin altına iner, ölçülmezse görünmez |
| $k$-ortalama | Centroid yalnız Öklid'de doğru minimizerdir | Kümeler anlamsız merkezlere kayar |
| DBSCAN | $\varepsilon$-top semantiği çöker | Kümeler rastgele kırılır |
| **Geçişli birleştirme** | $a\!\sim\!b,\ b\!\sim\!c \Rightarrow a\!\equiv\!c$ | **Bilgi kaybı — en tehlikelisi** |

Geçişli birleştirme felaketi: $d(a,b)=0{,}29$, $d(b,c)=0{,}29$ (ikisi de $\tau$ altında) ama
$d(a,c)=1{,}00$. Tek-bağlantı (single-linkage) kümeleme bu üçünü aynı fikir ilan eder;
sistem artık $a$ ile $c$'nin farklı olduğunu bilmez, $c$ "zaten sende var" sayılır ve
kullanıcı onu asla görmez. Kayıp **geri döndürülemez ve sessizdir**.

**KURAL 2.2a** — Algoritmik yolun tamamında (indeks, kümeleme, birleştirme, eşikleme)
$d_\theta=\arccos(\mathrm{clamp}(\mathrm{sim},-1,1))/\pi$ kullanılır; kosinüs yalnız sunumda kalır.
`clamp` şart — kayan nokta $\mathrm{sim}=1{,}0000001$ üretip `arccos`'u `NaN` yapar.
**Test:** rastgele $10^5$ üçlü için `d(a,c) <= d(a,b) + d(b,c) + 1e-9`.

**KURAL 2.2b (geçişlilik yasağı)** — Birleştirme **asla** geçişli kapanışla yapılmaz;
**tam bağlantı (complete linkage)** veya açık klik tabanlı birleştirme kullanılır: bir
eşdeğerlik sınıfının **her** ikili uzaklığı $\tau$ altında olmalıdır.
**Test:** birleştirme sonrası her sınıf için `max_pairwise_distance(cls) <= tau`.

### 2.3 Daha derin sorun: gömme bir yarı-metriktir (pseudometric)

Ayırt edilemezlerin özdeşliği ($d(a,b)=0\Rightarrow a=b$) sağlanmaz; dahası gömme uzayı
**yönsüzdür**: implikasyon yönünü, niceleyici sırasını ve olumsuzlamayı taşımaz.

- "$f$ süreklidir" ↔ "$f$ düzgün süreklidir" → kosinüs $\approx0{,}95$, **anlamca farklı**
- "$A\Rightarrow B$" ↔ "$B\Rightarrow A$" → kosinüs $\approx0{,}98$, **anlamca zıt**
- "yakınsar" ↔ "ıraksar" → kosinüs $\approx0{,}90$, **anlamca zıt**

> ⚠️ **RİSK — Yön körlüğü.** Matematik ve tıp için ölümcül (doktrin: "yanlış özetlenen bir
> teorem zehirlidir"). Yalnız gömmeye dayanan bir "aynı" kararı, teoremi tersine çeviren bir
> birleştirme üretebilir.

**KURAL 2.3** — Gömme **karar verici değil, aday üreticidir**. İki katman:
(1) *geri çağırma* — gömme, yüksek recall, atom başına en yakın $k=20$ aday;
(2) *karar* — LLM + sembolik doğrulama (`03-dogrulama.md`), yön/niceleyici/olumsuzlama açıkça sorgulanır.
Gömme skoru tek başına asla bir birleştirmeyi tetiklemez.
**Test:** mimari test — `merge()` fonksiyonu `verdict` argümanı olmadan çağrılamaz (tip sistemiyle zorunlu).

---

## 3. Aksiyomlar — sistemin uymak zorunda olduğu tam liste

Son sütun asıl önemli olandır: **aksiyom ihlal edilirse kullanıcı ne görür.**

| # | Aksiyom | Biçimsel ifade | İhlal eden formül | Kullanıcı ne görür |
|---|---|---|---|---|
| **A1** | Sınırlılık | $N\in[0,1]$ | Normalize edilmemiş sayaç, kırpılmamış z-skor | "%127'si yeni" |
| **A2** | Uç normalizasyon | $N(B\mid\emptyset)=1$; $A_B\subseteq L\Rightarrow N=0$ | Düzgünleştirilmiş payda | Hiç kitabı yokken "%12'si sende var" |
| **A3** | **Monotonluk (antitonluk)** | $L\subseteq L'\Rightarrow N(B\mid L')\le N(B\mid L)$ | Kütüphane üzerinden IDF; yüzdelik/z-skor normalizasyonu | "Rudin kitabın %8 **daha yeni** oldu" |
| **A4** | Permütasyon değişmezliği | $N$, $L$'nin **kümesine** bağlı; ekleme sırasına değil | Artımlı kümeleme, ilk-gelen-kazanır merkezler | Kütüphaneyi tekrar yükleyince farklı sayı |
| **A5** | İdempotens | $B\in L\Rightarrow N(B\mid L)=0$; $N(B'\mid L\cup B)=N(B'\mid L)$ | Tekilleştirmesiz alım | Aynı PDF iki kez → tüm sayılar bozuk |
| **A6** | Kararlılık | $\lvert N(B\mid L\cup\{a\})-N(B\mid L)\rvert\le\Delta$ | Sert eşik $\mathbf{1}[d<\tau]$ | Sayı 94 → 71 → 93 zıplar |
| **A7** | Ölçek değişmezliği | $\phi\to c\phi$ sonucu değiştirmez | Normalize edilmemiş nokta çarpımı | Model güncellemesinde toplu kayma |
| **A8** | **İlgisiz atom bağımsızlığı** | $\min_{b\in A_B}d(a,b)>d_{\max}\Rightarrow N$ değişmez | Global softmax, kütüphane geneli ortalama/std | "Yemek kitabı ekledim, ölçü teorisi kitabımın yeniliği düştü" |

**A3 en çok ihlal edilen aksiyomdur** çünkü "bu kitap kütüphanendeki ortalamadan daha yeni"
cümlesi doğal görünür — ama kütüphane değişince ortalama değişir, ortalama değişince
**eski skorlar yukarı gidebilir.**
**KURAL A3** — Gösterilen skor $(B,L)$'nin saf fonksiyonu ve $L$'de antiton olacak. Göreli/
yüzdelik/sıralama normalizasyonu gösterilen skorda **yasak**; iç sıralamada kullanılırsa
`relative_rank` gibi farklı bir adla ve yüzdesiz taşınır.
**Test:** 1000 rastgele senaryoda `N(B | L ∪ {b}) <= N(B | L) + 1e-9`.

**KURAL A4** — Kümeleme atom **kümesinin** deterministik fonksiyonu: içerik hash'ine göre
kanonik sıralama, deterministik eşitlik bozma, sabit tohum, periyodik tam yeniden hesap.
**Test:** aynı kütüphaneyi 20 farklı sırayla al, bölüntü **birebir aynı** olmalı.

**KURAL A8** — Skor çekirdeği **tıkız destekli**: $k(d)=0$ for $d>d_{\max}$; hiçbir global
normalizasyon (softmax dahil) yok. **Test:** $B$'nin her atomundan $d_{\max}$'tan uzak sentetik
bir atom ekle → $N$ bit-bit aynı kalmalı.

---

## 4. Kararlılık ve süreklilik — Lipschitz sınırı önerilebilir mi?

**Sürekliliği doğru ifade etmek.** Kütüphane ayrık bir nokta bulutudur; "küçük değişim"
topolojik anlamda tanımsızdır. Doğru çerçeve **sınırlı duyarlılık** (diferansiyel gizlilikteki gibi):
sayaç formunda tek atom eklemek en çok bir $B$-atomunu çevirir, dolayısıyla
$\Delta=\sup_a\lvert N(B\mid L\cup\{a\})-N(B\mid L)\rvert \le w_{\max}/\sum_a w(a)$.
400 atomlu kitapta $\Delta\approx0{,}25$ puan — **iyi haber**: tek atom sayıyı zıplatamaz,
tek kitap en fazla $m/n$ oynatır.

> ⚠️ **RİSK — Sonsuz Lipschitz sabiti.** $\mathbf{1}[d<\tau]$'nun $d=\tau$'daki Lipschitz sabiti
> sonsuzdur. Gömme modelinin doğal gürültüsü (aynı metni yeniden gömünce açısal uzaklıkta
> $\sigma_{\text{emb}}\approx0{,}01$ oynama) eşik civarındaki atomları her hesapta rastgele çevirir;
> kullanıcı hiçbir şey yapmadan sayı 94 → 92 → 94 gezinir.

**KURAL 4.2 (yumuşak kapsama rampası)** — Gösterge yerine parçalı doğrusal rampa:

$$c(a\mid L)=\mathrm{clip}\!\left(\frac{d_{\min}(a,L)-\tau_{\text{lo}}}{\tau_{\text{hi}}-\tau_{\text{lo}}},0,1\right),\qquad N=\frac{\sum_a w(a)\,c(a\mid L)}{\sum_a w(a)}$$

Bu, $d$'de $1/(\tau_{\text{hi}}-\tau_{\text{lo}})$-Lipschitz'tir ve **ilan edilebilir** bir sınır verir:
$\lvert\Delta N\rvert \le \frac{1}{\tau_{\text{hi}}-\tau_{\text{lo}}}\cdot\frac{\sum_a w(a)\lvert\Delta d_a\rvert}{\sum_a w(a)}$.
Rampa genişliği **ölçülerek** seçilir: aynı 500 metni 100 kez göm, $\sigma_{\text{emb}}$'i ölç,
$\tau_{\text{hi}}-\tau_{\text{lo}}\ge4\sigma_{\text{emb}}$ al.
**Test:** gömmelere $\mathcal{N}(0,\sigma_{\text{emb}})$ gürültü, 100 tekrar, `std(N) <= 0.005`.

**KURAL 4.3 (histerezis)** — Matematiksel süreklilik yetmez, **görüntülenen** sayı da titrememeli.
İki alan ayrılır: `true_novelty` (sürekli, tam hassasiyet) ve `displayed_novelty` (5 puanlık kova).
Görüntülenen değer ancak gerçek değer mevcut kovanın **1,5 puan dışına** çıkınca güncellenir.
**Test:** gerçek değerde ±1 puan salınım → `displayed_novelty` hiç değişmemeli.

> ⚠️ **RİSK — Sürümler arası uzaklık anlamsızdır.** Model v1 ile gömülmüş bir atom ile v2 ile
> gömülmüş bir atom arasındaki kosinüs hiçbir şey ifade etmez; iki farklı uzayda yaşıyorlar.
> Kısmi yeniden indeksleme bunu sessizce yapar.

**KURAL 4.4** — Her vektör `embedding_model_version` taşır; farklı sürümlü iki vektörle uzaklık
hesabı **istisna fırlatır** (sessiz hata yok). Model yükseltmesi gölge (shadow) tam yeniden hesap
gerektirir; bitince kullanıcıya tek seferlik "kütüphanen yeniden indekslendi" olayı gösterilir.
Sessiz kayma yasak.

---

## 5. Eşik kalibrasyonu — bir hipotez testi olarak "aynı" kararı

$H_0$: $a$ ve $b$ **farklı** fikirler. $H_1$: **aynı**.
**Tip I (yanlış pozitif, YP)** = farklı iki fikri birleştirmek → bilgi kaybı.
**Tip II (yanlış negatif, YN)** = aynı fikri iki kez saymak → sahte yenilik.

| | Yanlış pozitif (birleştirme) | Yanlış negatif (ayırma) |
|---|---|---|
| Görünürlük | **Sessiz** — kullanıcı kaybettiğini bilmez | Görünür — okur, "bunu biliyordum" der |
| Geri alınabilirlik | **Yok** — atlanan sayfa bir daha önerilmez | Var — 11 sayfa boşa okundu, o kadar |
| Doktrine etkisi | **#3'ü ihlal eder** ("reddetme yok") ve #7'yi | Yalnızca verimsizlik |
| Kendini düzeltme | Yok | Kullanıcı geri bildirimiyle düzelir |

**Yanlış pozitif belirgin şekilde daha pahalıdır**; simetrik ölçütler (F1, doğruluk) bu problem
için **yanlış hedeftir**.
**KURAL 5.1** — Eşik $c_{\text{YP}}/c_{\text{YN}}=10$ maliyet oranıyla optimize edilir; ROC üzerinde
çalışma noktası teğet eğimi $\frac{c_{\text{YP}}\pi_0}{c_{\text{YN}}\pi_1}$ olan noktadır.
Hedef: **YP oranı $\le$ %1**, geri çağırma ~%70 kabul. Model kartında F1 değil
`FPR@recall=0.70` raporlanır.

> ⚠️ **RİSK — Çoklu test.** 400 atom × 50.000 atomluk kütüphane $=2\times10^7$ karşılaştırma.
> %0,1 YP oranı bile **20.000 yanlış birleştirme** demektir. Ham eşik bu ölçekte çöker.

**KURAL 5.2 (iki aşama + FDR)** —
(1) ANN geri çağırma atom başına en iyi $k=20$ aday → test ailesi $8.000$'e iner.
(2) Bu aile üzerinde yanlış keşif oranı kontrolü: **birleştirme** kararı için
**Benjamini–Yekutieli**, $q=0{,}01$ — keyfi bağımlılık altında da garanti verir, bedeli
$H_m=\ln 8000+0{,}577\approx9{,}6$ katlık muhafazakârlıktır ve yanlış birleştirmenin
maliyeti karşısında bu bedel doğrudur. Yumuşak "ilişkili" kenarları için **Benjamini–Hochberg**,
$q=0{,}10$ yeter. Bonferroni kullanılmaz: geri çağırmayı sıfıra indirir.
(3) Test ailesi **kitap başına** ilan edilir ve loglanır.

> ⚠️ **RİSK — Alan körü tek eşik.** Matematik atomları sözlüksel olarak çok benzer ama anlamca
> ayrıktır ("sürekli"/"düzgün sürekli"); tarih anekdotları sözlüksel farklı ama anlamca aynı
> olabilir. Tek $\tau$ ile matematikte aşırı birleştirme (bilgi kaybı) ve tarihte aşırı ayırma
> (sahte yenilik) **aynı anda** olur.

**KURAL 5.3** — $\tau$, **(alan × atom tipi)** başına kalibre edilir (matematik×teorem,
matematik×tanım, tıp×yöntem, tarih×anekdot...). Her değerin yanında kalibrasyon kümesinin
kimliği ve elde edilen $(\text{FPR},\text{TPR})$ saklanır. Kalibrasyon kümesi: alan başına
**≥500 insan etiketli çift**, tabakalı örneklem. $\tau$ değişikliği kod değil **incelemeye tabi
config commit'idir**; sessiz otomatik yeniden kalibrasyon yasaktır.

**KURAL 5.4 (konformal çekimserlik)** — Sabit eşik dağılımdan bağımsız garanti vermez;
**bölünmüş konformal tahmin** verir. Karar **üç değerlidir**: `aynı` / `farklı` / `belirsiz`.
Güven bölgesine düşmeyen çiftler `belirsiz` olur ve **birleştirilmez** (muhafazakâr taraf:
sahte yenilik, bilgi kaybından iyidir) ama §6'daki belirsizlik hesabına girer.
`belirsiz` oranı bir sağlık metriğidir; %20'yi aşarsa alarm.

---

## 6. Belirsizliğin taşınması — tek sayı mı, aralık mı?

Her atomun bir çıkarım güveni $p_i$ var; yeni atom sayısı $X=\sum_i\mathrm{Bernoulli}(p_i)$,
yani **Poisson-binom**: $\mathbb{E}[X]=\sum p_i$, $\mathrm{Var}[X]=\sum p_i(1-p_i)$.

**Somut örnek.** $n=400$, ortalama $p=0{,}06$ → $\mathbb{E}[X]=24$,
$\mathrm{sd}=\sqrt{400\cdot0{,}06\cdot0{,}94}=4{,}75$; %95 aralığı $24\pm9{,}3$ → yenilik
$[\%3{,}7,\%8{,}3]$ → **"sende var" = %91,7 – %96,3**. Yani "%94" aslında **"%92–%96"**dır;
tek sayı olarak sunmak olmayan bir hassasiyet iddia etmektir.

> ⚠️ **RİSK — Korelasyonlu hatalar.** Bağımsızlık varsayımı **yanlıştır**: bozuk bir OCR sayfası,
> yanlış ayrıştırılmış bir bölüm, tablo/şekil yoğun bir kesit **blok halinde** hata üretir.
> Bağımsız Poisson-binom varyansı 2–5 kat küçük gösterir; sistem sahte bir kesinlikle konuşur.

Küme içi korelasyon $\rho$, sayfa başına ortalama atom $\bar m\approx3$ ile tasarım etkisi
$\mathrm{deff}=1+(\bar m-1)\rho$; $\rho=0{,}5$ için $\mathrm{deff}=2$, sd $\sqrt2$ kat büyür →
aralık **%90,7 – %97,3**.

**KURAL 6.2** — Belirsizlik parametrik formülle değil **bölüm seviyesinde blok bootstrap** ile
hesaplanır: atomlar değil **bölümler** yeniden örneklenir, 1000 tekrar, %5–%95 yüzdelikleri.
Bu, bölüm içi korelasyonu varsayım yapmadan yakalar.
**Test:** bir bölümün tüm atomlarını bozan senaryoda aralığın **genişlediği** doğrulanır —
genişlemiyorsa bootstrap yanlış seviyede yapılıyordur.

**KURAL 6.3 (sunum eşikleri)**

| %90 aralık genişliği | Gösterim |
|---|---|
| $\le$ 5 puan | Tek sayı: **"%94'ü sende var — 11 sayfa kalıyor"** |
| 5–20 puan | Aralık: **"%88–%96'sı sende var"** |
| > 20 puan | Sayı yok (aşağıya bak) |

**KURAL 6.3b (asimetrik aralık)** — Normal yaklaşım kullanılmaz; %96 ± %5 ekrana "%101" basar.
**Wilson skor aralığı** (veya Jeffreys) kullanılır — $[0,1]$ içinde kalır, uçlarda doğru davranır.
Kırpma ile düzeltilmiş normal aralık **yasak**: kırpma kapsama garantisini sessizce bozar.

**Ne zaman "bilmiyorum" demeliyiz?** Doktrin #7 gereği, aşağıdakilerden **herhangi biri**
sağlanırsa sayı gösterilmez:

| Tetikleyici | Eşik |
|---|---|
| Aralık genişliği | > 20 puan |
| `[doğrulanamadı]` atom oranı | > %30 |
| `belirsiz` (konformal çekimser) çift oranı | > %20 |
| Kitabın alanı için kalibre $\tau$ yok | herhangi |
| OCR güven ortalaması | < 0,80 |
| Kütüphane çok küçük | $\lvert L\rvert<200$ atom |

Çıktı: **"Bu kitabı henüz güvenilir şekilde ölçemedim. Ama Bölüm 7 tanıdık gelmiyor —
oradan başlayalım."** Sayı yok, eylem var: doktrin #3 (reddetme yok) ve #7 (sahte kesinlik yok)
birlikte korunur.
**KURAL 6.4** — Bu tablo config değil, tek bir fonksiyondur (`should_abstain(book_stats) -> bool`)
ve sayı gösteren her bileşen ondan geçer. **Test:** her tetikleyici için birim test, artı
çekimserlik durumunda arayüzde hiçbir yerde yüzde karakteri render edilmediğini doğrulayan
anlık görüntü (snapshot) testi.

---

## 7. İspatın yapısı — bağımlılık DAG'ı ve kapanış

$G=(V,E)$; $V$ atomlar, $E$ etiketli kenarlar. `önkoşul` alt grafı **DAG** olmalıdır.

> ⚠️ **RİSK — Çıkarılan graf döngü içerir.** Üç kaynak: (a) LLM çıkarım hatası, (b) kitabın
> döngüsel anlatımı ("bunu Bölüm 9'da ispatlayacağız"), (c) **gerçek eşdeğerlikler** —
> "kompakt ⟺ dizisel kompakt (metrik uzayda)" doğal olarak iki yönlüdür. Döngüyü sessizce bir
> kenar atarak kırmak, hangi kenarın atıldığına göre farklı okuma sıraları üretir ve
> A4'ü (permütasyon değişmezliği) ihlal eder.

**KURAL 7.1** — Alımda Tarjan SCC çalışır. Boyutu >1 olan her güçlü bağlı bileşen ya açık
`eşdeğerlik` etiketiyle **tek düğüme daraltılır** (condensation) ya da insan incelemesine
işaretlenir; kenar sessizce düşürülmez. **Test:** `assert is_dag(condensation(G))`.

**Kapanış.** $t$'yi anlamak için gereken küme, ters erişilebilirlik kapanışıdır:
$\mathrm{Cl}(t)=\{v\in V: v\rightsquigarrow t\}$ — `önkoşul` kenarları ters çevrilmiş grafta
$t$'den BFS, sorgu başına $O(V+E)$.

> ⚠️ **RİSK — Kapanış patlaması.** Lisansüstü bir metinde $\lvert\mathrm{Cl}(t)\rvert$ 800 atoma
> ulaşabilir: "bu teoremi anlamak için önce tüm analizi oku." Doğrudur ama işe yaramaz ve
> doktrin #1 ile #4'ü (tek karar, tek satır) ihlal eder.

> ⚠️ **RİSK — Geçişli kapanışı önceden hesaplama.** $\lvert V\rvert=10^5$ için bit-küme geçişli
> kapanış $10^{10}/8\approx1{,}25$ GB'tan başlar ve kareyle büyür. **KURAL 7.2:** tam geçişli
> kapanış materyalize **edilmez**; sorgu başına ters BFS (ms mertebesi), gerekirse 2-hop
> erişilebilirlik indeksi.

**Sınır kapanışı (frontier closure) — doğru büyüklük budur.** Kullanıcının okuması gereken
$\mathrm{Cl}(t)$ değil, **bilmediği** önkoşullardır. $\mathrm{mastery}(v,u)\in[0,1]$ kullanıcının
hakimiyeti olsun; ters BFS yapılır ama $\mathrm{mastery}(v,u)\ge m_0$ olan düğüm
**genişletilmez**:

$$\mathrm{Frontier}(t,u)=\{v:\ t\text{'den geriye, yalnız hakim olunmayan düğümlerden geçen bir yol var}\}$$

Kullanıcı ölçü teorisini biliyorsa onun önkoşulları hiç ziyaret edilmez; 800 atomluk kapanış
tipik olarak 9–30 atomluk bir sınıra iner. **"11 sayfa" sayısı buradan doğar.**

**KURAL 7.3** — Okuma önerisi $\mathrm{Frontier}(t,u)$ üzerinden üretilir; maliyeti
$\sum_{v\in\mathrm{Frontier}}\mathrm{pages}(v)$'dir ve bu, §1.2'deki tutarlılık değişmezinin
sağ tarafıdır — **aynı sayı** hem yüzdeyi hem öneriyi besler. **Testler:**
`Frontier(t,u) ⊆ Cl(t)`; tüm $\mathrm{Cl}(t)$'ye hakimse `Frontier == ∅`; **öğrenme monotonluğu:**
bir düğüme hakim olmak sınırı asla büyütmez (`Frontier(t, u+v) ⊆ Frontier(t, u)`) — A3'ün
öğrenme yolu üzerindeki karşılığı.

**KURAL 7.4 (okuma sırası)** — $\mathrm{Frontier}$'in topolojik sıralamaları geçerli okuma
sıralarıdır; aralarından sayfa atlamasını ($\sum_i\lvert\mathrm{page}(v_{i+1})-\mathrm{page}(v_i)\rvert$)
en aza indireni seçmek istenir, ama bu öncelik kısıtlı bir gezgin satıcı problemidir ve
**NP-zordur**. Açgözlü sezgisel kullanılır (uygun düğümler arasından sayfa numarası en yakın
olanı seç); dokümanda ve kodda **"optimal" denmez**.

> ⚠️ **RİSK — Ürünün en değerli bulgusunu kaçırmak.** Bir ispat tamamen bilinen lemmalardan
> kurulabilir ve yine de yepyeni olabilir; yeni olan **bağlantıdır**. Atom seviyesinde ölçen
> bir sistem böyle bir ispatı "%0 yeni" ilan eder.

**KURAL 7.5** — Yenilik iki bileşenle raporlanır:
$N_{\text{düğüm}}=\frac{\text{yeni atom kütlesi}}{\text{toplam atom kütlesi}}$ ve
$N_{\text{kenar}}=\frac{\lvert E_B\setminus E_L\rvert}{\lvert E_B\rvert}$ ($L$'de bulunmayan
bağımlılık ilişkilerinin oranı). Arayüz metni doğrudan buradan doğar:

> **"Fikirler tanıdık (%94'ü sende var) — ama bunları birleştirme biçimi yeni:
> 23 bağlantının 19'unu daha önce hiç görmedin. Bölüm 7, 11 sayfa."**

**Test:** $A_B\subseteq L$ ama $E_B\not\subseteq E_L$ olan sentetik bir kitapta sistem
"%0 yeni" **dememeli** ve kenar yeniliğini raporlamalıdır.

---

## 8. Aksiyom → test matrisi (uygulama özeti)

| Kural | Otomatik test | Kırmızı yandığında belirti |
|---|---|---|
| 1.1 | Bölüm toplamı = kitap (standalone) | Yüzdeler toplanmıyor |
| 1.2 | `(1-cov)*pages ≈ recommended_pages` | "%94" deyip 60 sayfa öneriyor |
| 2.2a | $10^5$ rastgele üçlü, üçgen eşitsizliği | ANN sessizce komşu kaybediyor |
| 2.2b | Sınıf içi maks. uzaklık $\le\tau$ | Farklı fikirler tek atoma çöküyor |
| 2.3 | `merge()` `verdict`siz çağrılamaz | Teorem tersine çevriliyor |
| A1–A2 | Fuzz: $N\in[0,1]$; boş kütüphane → $N=1$ | "%127 yeni"; sahte kapsama |
| A3 | 1000 rastgele senaryoda antitonluk | "Kitabın daha yeni oldu" |
| A4 | 20 karışık sıra → aynı bölüntü | Sayılar tekrar üretilemiyor |
| A5 | Aynı kitabı iki kez yükle | Kopya PDF tüm sayıları bozuyor |
| A6 | Gürültü enjeksiyonu, `std(N) ≤ 0.005` | Sayı zıplıyor |
| A7 / 4.4 | Vektör ölçekleme; karışık sürüm → istisna | Anlamsız uzaklıklar, toplu kayma |
| A8 | Uzak sentetik atom → bit-bit aynı | "Yemek kitabı analizimi etkiledi" |
| 5.4 | `belirsiz` oranı < %20 | Kalibrasyon bozulmuş |
| 6.2 | Bozuk bölüm → aralık genişlemeli | Sahte kesinlik |
| 6.4 | Çekimserlikte hiç yüzde render edilmiyor | Sistem "bilmiyorum" diyemiyor |
| 7.1 | `is_dag(condensation(G))` | Okuma sırası tutarsız |
| 7.3 | Hakimiyet ekle → sınır küçülmeli | "Öğrendikçe daha çok ödevim var" |
| 7.5 | Sentetik "yeni ispat, eski lemmalar" | Ürünün en iyi bulgusu görünmüyor |

---

## 9. Açık sorular

**AÇIK SORU 1 — Hakimiyet sönümü.** $\mathrm{mastery}(v,u)$ zamanla düşmeli mi (unutma eğrisi)?
Düşerse §7.3'teki öğrenme monotonluğu zamana bağlı hale gelir ve kullanıcı hiçbir şey yapmadan
sınırı büyür ("dün 11 sayfaydı, bugün 14") — psikolojik olarak kabul edilemez olabilir.
Önerim: sönüm olsun ama **gösterilen** sınır histerezisli (§4.3). Karar `06-arayuz.md` ile ortak.

**AÇIK SORU 2 — Transfer skorunun paydası.** §1.2'de P5'i yüzde olarak göstermeyi yasakladım
çünkü paydası yorumlanamaz; ama ürünün kalbi transfer (`07-transfer.md`). Yorumlanabilir bir
payda var mı — örn. "Açık Sorular Defteri'ndeki 7 sorudan 2'sine dokunuyor" (payda = açık soru
sayısı, tamamen dürüst)? Bunu öneriyorum; 07 ile teyit edilmeli.

**AÇIK SORU 3 — $\rho$'nun ölçülmesi.** §6.2'deki bölüm içi korelasyon etiketli veri olmadan
bilinmiyor. Blok bootstrap doğru cevabı verir ama **ne kadar** muhafazakâr olduğumuzu bilmiyoruz.
İlk 50 kitaptan sonra $\rho$ ölçülmeli ve §6.3'teki sunum eşikleri (5 / 20 puan) yeniden ayarlanmalı.
