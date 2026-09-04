# 09 — Cebirsel Temeller
**Saf Matematik Profesörü I · Cebir, Düzen Teorisi, Kategori Teorisi**

## 3 cümlelik özet

Sistemin fikirler arasına koyduğu bağlar (`aynı`, `önkoşulu`, `genellemesi`…) keyfi etiket değildir;
her birinin uyması gereken katı kuralları vardır ve bu kurallardan biri bozulursa sistem *hata vermez*,
sessizce saçmalamaya başlar — örneğin binlerce farklı fikri "hepsi aynı şey" diye tek yığına çökertir.
Bu belge o kuralları tek tek yazar ve her birini "kodda şu kontrol olacak" cümlesine bağlar.
İkinci yarısı, ürünün kalbi olan çapraz-alan transferini (tıptaki bir yöntemin mühendislikte işe yaraması)
ölçülebilir bir sınavdan geçirir: **iyi analoji, adım adım akıl yürütmeyi koruyandır**;
korumayanı sistem kullanıcıya göstermeden önce yakalamak zorundadır.

---

## 0. Okuma kılavuzu

Her soyut sonuç numaralı bir kod kuralına (`K-01`…`K-32`) bağlanır; §7'de toplu tablo var.
Numarasız soyut iddia yok.

Notasyon: `a ≈ b` aynı · `a ⊥ b` çelişiyor · `a ⇏ b` çürütüyor · `a ≺ b` önkoşulu ·
`a ⊒ b` genellemesi · `a ↦ b` uygulaması. `R⁻¹` ters, `R∘S` bileşke, `R⁺` geçişli kapanış,
`R⁻` geçişli indirgeme.

---

## 1. Fikir atomunun cebirsel kimliği

### 1.1 İki atom ne zaman *eşittir*?

Üç farklı "eşitlik" birbirine karıştırılırsa sistem çöker. Ayırıyoruz:

| Seviye | Ad | Kriter | Kim kullanır |
|---|---|---|---|
| E0 | **Özdeşlik** (identity) | Aynı kitap, aynı sayfa, aynı ayıklama koşusu → aynı `atom_id` | Depolama, alıntı |
| E1 | **Ayırt edilemezlik** (indiscernibility) | İki atom, sistemin *tüm* bağıntılarında birbirinin yerine konabiliyor | Kongrüans denetimi |
| E2 | **Anlamsal aynılık** (`≈`) | İkisi de aynı iddiayı, aynı nicelleyicilerle, aynı kapsamda söylüyor | Kullanıcıya gösterim |

**Karar: kimlik kriteri E0'dır.** Kimlik içerik değil **kaynaktır**:
`atom_id = hash(kitap_id, konum_çapası, ayıklama_sürümü)`. Yeniden ayıklama yeni atom doğurur,
eskisi ölmez (`sürüm_ardılı` kenarı). Gerekçe: Doktrin 2 içeriği kimlik yapmayı yasaklar — içerik kimlik
olsaydı iki kitaptaki aynı cümle tek nesneye çöker, *hangi sayfadan geldiği* kaybolurdu.

> **K-01** — `atom_id` yalnızca kaynak çapasından türetilir; içerik alanı `atom_id` hesabına girmez.
> **K-02** — Atom kaydı **değişmez** (immutable). Güncelleme yok; yeni sürüm + `sürüm_ardılı` kenarı var.

### 1.2 Serbest yapı mı, bölüm yapısı mı?

Atomlar **serbest yapıda** (free structure) yaşar: `A = ⨆_{kitap} {ayıklanan oluşumlar}` — hiçbir iki
oluşum baştan özdeşleştirilmemiş, hiçbir denklem dayatılmamıştır. `≈` bu küme üzerinde **sonradan** üretilir
ve bir **bölüm yapısı** (quotient) doğurur: `K = A/≈`, elemanları **kavram düğümü**.

**Karar: iki katman da kalıcı tutulur. Bölüm birincil veri değil, türetilmiş görünümdür.**

```
A  (serbest)   ── atomlar, değişmez, sayfa çapalı, asla birleştirilmez
      │  π (bölüm izdüşümü, yeniden hesaplanabilir)
      ▼
K = A/≈        ── kavram düğümleri, gösterim ve akıl yürütme burada
```

Bölüme *taşınmıyoruz*: bölüm alma yıkıcıdır, `≈` ise bizde hatalı üretilir (LLM); yıkıcı işlem + hatalı
girdi = geri dönülemez kayıp. Serbest yapıda *kalmıyoruz*: kullanıcı 5 kitaptaki aynı fikri 5 kez görmemeli (Doktrin 1).

> **K-03** — Birincil tablo `atomlar`; `kavramlar` bir **materyalize görünümdür** ve
> `birlesme_kenarlari` tablosundan sıfırdan yeniden üretilebilir olmalıdır (rebuild testi CI'da koşar).
> **K-04** — Alıntı (kaynak gösterimi) daima `A` seviyesinden yapılır; `K` seviyesinde çapa yoktur.
> Kavram kartı, sınıfındaki atomların çapalarını *listeler*.

### 1.3 Kanonik temsilci

Kavram kartındaki cümle hangi atomdan gelir? Bu seçim **sınıfın fonksiyonu** olmalı, ekleme sırasının değil —
yoksa aynı kavram her yeniden inşada başka cümleyle görünür. Sıralama (sözlüksel, tam sıra):
`(−güven, −doğrulama_durumu, kitap_edinme_tarihi, atom_id)`.

> **K-05** — `temsilci(sınıf)` deterministik; `atom_id` son eşitlik-bozucu olduğu için sonuç her zaman tektir.
> Testi: aynı veriden iki kez inşa → aynı temsilciler (byte eşitliği).

### 1.4 Çok-sıralı (many-sorted) cebir

Atomların sortu (tipi) vardır: `S = {tanım, iddia, teorem, yöntem, formül, anekdot}`.
Bağıntılar sort-kısıtlıdır. Bu tablo bir *imza*dır (signature); ihlali ayıklama hatasıdır:

| Bağıntı | İzinli sortlar |
|---|---|
| `≈` | aynı sort (tek istisna: `iddia ≈ teorem` yalnız teoremin gayriresmî ifadesi ise, `[gevşek]` bayrağıyla) |
| `⊥`, `⇏` | `{iddia, teorem, formül}` × aynı küme. **Anekdot çelişemez.** |
| `≺` | `{tanım, teorem, yöntem}` → `{teorem, yöntem, formül}` |
| `⊒` | aynı sort |
| `↦` | `{yöntem, formül}` → `{iddia, teorem, problem}` (alan-aşan) |

> **K-06** — Bağıntı yazımında sort denetimi zorunlu. Sort ihlali → kenar reddedilir, ayıklama
> koşusu `sort_ihlali` sayacına yazılır. Bu sayaç bir kitapta %2'yi aşarsa o kitabın ayıklaması karantinaya alınır.
> **K-07** — `anekdot` sortlu bir atom `⊥`/`⇏` grafına asla giremez; anekdot çelişkisi diye bir şey yoktur,
> yalnızca `anlatı_gerilimi` (Katman 4'ün işi) vardır.

---

## 2. İlişki cebiri — yasa tablosu

### 2.1 Ana tablo

| Bağıntı | Yansımalı | Simetrik | Geçişli | Antisimetrik | Ters ilişki | Cebirsel tip |
|---|---|---|---|---|---|---|
| `≈` aynı | ✔ (zorunlu) | ✔ (zorunlu) | ✔ **hedef**, girdide yok | — | kendisi | Denklik → **kongrüans olmalı** |
| `⊥` çelişiyor | ✘ irrefleksif | ✔ (zorunlu) | ✘ **asla kapatma** | ✘ | kendisi | Simetrik, irrefleksif (tolerans değil: geçişsiz) |
| `⇏` çürütüyor | ✘ | ✘ asimetrik | ✘ | ✔ | `çürütülüyor` | Yönlü, çevrimsiz |
| `≺` önkoşulu | ✘ irrefleksif | ✘ asimetrik | ✔ (kapanış türetilir) | ✔ | `ardılı` (`≻`) | **Kesin kısmi sıralama** (DAG) |
| `⊒` genellemesi | ✔ | ✘ | ✔ | ✘ (yalnız ön-sıralama) | `özelleşmesi` (`⊑`) | **Ön-sıralama** (preorder) |
| `↦` uygulaması | ✘ | ✘ | ✔ *ilkece*, **kapatılmaz** | ✘ | `uygulanır` | Yönlü, derinlik sınırlı |

### 2.2 İhlal edilirse ne bozulur

| Yasa | İhlal edilirse görülen felaket |
|---|---|
| `≈` geçişli | **Zincirleme birleşme**: A≈B, B≈C, C≈D… tüm kütüphane tek kavrama çöker; "bu kitabın %94'ü sende var" hükmü her kitap için üretilir, ürün yalan söyler |
| `≈` kongrüans | Birleşen sınıf hem `X`'e `≈` hem `X`'e `⊥` olur; sistem aynı ekranda "bunlar aynı" ve "bunlar çelişiyor" der |
| `⊥` simetrik | Çelişki yalnız bir yönden görünür; kullanıcı A'yı okurken uyarı alır, B'yi okurken almaz |
| `⊥` geçişsiz | Kapanış alınırsa: A⊥B, B⊥C → A⊥C türetilir; oysa A ile C çoğu zaman **aynı** şeyi söyler. Çelişki grafı gürültüye boğulur |
| `≺` asiklik | Önkoşul DAG'ı çevrim içerir → topolojik sıra yok → okuma planı üretilemez, Doktrin 4 (tek satır plan) ölür |
| `≺` geçişli | "Bölüm 9 için ölçü teorisi lazım" çıkarımı yapılamaz; yalnız bir adım geri görülür |
| `≺` antisimetrik | A≺B ve B≺A → hangisini önce okuyacağını sistem bilemez, sonsuz döngüde kalır |
| `⊒` geçişli | Genelleme hiyerarşisi parçalanır; "bu fikrin daha genel hali kütüphanende var" bulunamaz |
| `↦` kapatılmaz | Kapatılırsa: 3-4 adımlık uygulama zincirleri üretilir, her adımda güven düşer, sistem "bu tıp kitabı senin derleyici problemini çözer" gibi sahte bağlar satar |

### 2.3 Bileşke yasaları (denetlenebilir değişmezler)

Aşağıdakiler graf üzerinde doğrudan sorguya çevrilebilir bütünlük kısıtlarıdır:

```
(L1)  ≈ ∘ R ∘ ≈  ⊆  R        her R için      ← KONGRÜANS YASASI (bu belgenin omurgası)
(L2)  ≺ ∘ ≺      ⊆  ≺
(L3)  ⊒ ∘ ⊒      ⊆  ⊒
(L4)  ≈ ∩ ⊥      =  ∅
(L5)  ≈ ∩ ≺      =  ∅
(L6)  ≺ ∩ ≻      =  ∅                        (asimetri)
(L7)  ⊒ ∩ ⊑      ⊆  ≈                        (karşılıklı genelleme ⇒ aynılık)
(L8)  ⇏ ∩ ⇏⁻¹    =  ∅                        (karşılıklı çürütme olamaz)
(L9)  ⊥          =  ⊥⁻¹                      (simetri)
```

> **K-08** — L1–L9 gecelik bütünlük işinde (integrity job) sorgu olarak koşar. Her ihlal bir
> `celiski_kaydi` üretir; kayıt otomatik silinmez, **incelemeye** düşer.
> **K-09** — L4, L5, L6 yazma zamanında (write-time) da denetlenir; ihlal eden kenar hiç yazılmaz.
> **K-10** — L7 bir *fırsat sinyalidir*: `a ⊒ b` ve `b ⊒ a` bulunduğunda sistem otomatik `≈` yazmaz,
> **birleşme adayı** üretir ve §3'teki kapıdan geçirir.

---

## 3. `aynı` — eşik geçişsizliği ve birleşme güvenliği

### 3.1 Problem

Gömme (embedding) çıktısı `benzer_θ(a,b) ⟺ sim(a,b) ≥ θ` verir. Bu bağıntı **yansımalı ve simetriktir
ama geçişli değildir** — adı *tolerans bağıntısı* (tolerance relation). Onu denklik sınıflarına çevirmenin
tek yolu geçişli kapanıştır ve **geçişli kapanış tam olarak tek-bağ kümelemesidir** (single-linkage):
zincirleme (chaining) ile çapı sınırsız sınıflar üretir.

Daha kötüsü, benzerlik grafı rastgele graf gibi davranır: `θ` düştükçe **perkolasyon eşiğinde ani faz geçişi**
olur, dev bileşen (giant component) bir anda belirir. `θ`'yı 0.86'dan 0.84'e çekmek "biraz daha çok birleşme"
değil, "kütüphanenin yarısı tek kavram" olabilir. Sessizce saçmalama tam olarak budur: hata mesajı yok.

### 3.2 Altı katmanlı savunma

**(1) Tam-bağ (complete-linkage) şartı.** Bir sınıf ancak *her* çifti eşiği geçiyorsa kurulur; bu,
sınıf çapını sınırlar ve zincirlemeyi matematiksel olarak imkânsızlaştırır.

**(2) Meet, join değil.** Bir küme üzerindeki denklik bağıntıları **tam kafes** oluşturur. Birleşim-bul
(union-find) bu kafeste **join** hesaplar — join tam da tehlikeli olan geçişli kapanıştır. **Meet (kesişim)
güvenlidir: iki denklik bağıntısının kesişimi her zaman denkliktir ve daima daha incedir.**
Karar: `≈` üç bağımsız sinyalden ayrı üretilip **kesiştirilir**:
- `≈_gömme` (embedding komşuluğu, tam-bağ)
- `≈_imza` (normalize edilmiş iddia imzası: nicelleyiciler + kapsam + yön)
- `≈_biçimsel` (formül/teorem için SymPy normal formu eşitliği — bkz. `03-dogrulama.md`)

`≈ := ≈_gömme ∩ ≈_imza ∩ ≈_biçimsel*` (`*`: yalnız uygulanabilir sortlarda; uygulanamıyorsa o çarpan atlanır
ama bu durum kenarda `zayıf_tanık` bayrağı bırakır).

**(3) İki eşik + histerezis.** `θ_hi` üstü otomatik birleşir, `θ_lo` altı reddedilir, arası **karar kuyruğuna**
düşer. Tek eşik, eşik civarındaki gürültüyü ikili karara çevirir; histerezis üçüncü bir "bilmiyorum" durumu
açar — Doktrin 7'deki `[doğrulanamadı]` ilkesinin cebirsel karşılığı.

**(4) Kongrüans kapısı (merge gate).** `birleştir(a,b)` yalnız şu 6 test geçerse uygulanır:

```
G1  sort(a) = sort(b)                                     (K-06)
G2  ¬(a ⊥ b) ve sınıfları arasında yasak-kenar yok
G3  a ≺⁺ b değil ve b ≺⁺ a değil                          (birleşme öz-önkoşul yaratmasın)
G4  KONGRÜANS: ∀c.  ¬( class(a) R c  ∧  class(b) R' c )   R,R' çelişen bağıntı çifti ise
                    çelişen çiftler: (≈,⊥) (≺,≻) (⊒,⊑ tekil olmayan bağlamda) (⇏, ≈)
G5  tam-bağ: min_{x,y ∈ birleşik sınıf} sim(x,y) ≥ θ_merge
G6  |birleşik sınıf| ≤ C_max  ve  benzerlik-çapı ≤ D_max
```

G4'ün cebirsel adı şudur: **`≈` yalnız denklik değil, tüm ilişkisel yapının kongrüansı olmak zorundadır.**
Kongrüans olmayan bir denklikle bölüm almak yapıyı yok eder — `K` üzerindeki bağıntılar iyi tanımlı olmaz.
G4 tam olarak "bölüm iyi tanımlı mı?" testidir.

**(5) Sıra bağımsızlığı.** Yasak-kenarlar (cannot-link) girince sonuç uygulama sırasına bağlanır (kısıtlı
kümeleme, NP-zor). Optimum aramıyoruz; **deterministik açgözlü** uyguluyoruz: adaylar `(güven ↓, atom_id ↑)`
sırasında işlenir, kapıdan geçemeyen `atlanan_birlesme` olarak loglanır. Sonuç, kenar kümesinin **fonksiyonu**
olur; yeniden inşa aynı sonucu verir.

**(6) Geri alınabilirlik.** Union-find yıkıcıdır. Sınıfları değil **birleşme kenarlarını** saklıyoruz;
geri alma = bir kenarı silmek + bileşenleri yeniden hesaplamak. Union-find yalnız bellek-içi hızlandırıcıdır.

### 3.3 Erken uyarı göstergeleri

Çöküş sessiz olduğu için ölçmek zorundayız:

| Gösterge | Alarm eşiği |
|---|---|
| `max |sınıf|` | `> √N` (N = toplam atom) → derhal durdur |
| En büyük sınıfın büyüme hızı | Tek kitap yüklemesinde `> %20` artış |
| Sınıf boyutu dağılımının kuyruğu | Kuvvet yasası üsteli `< 2` (dev bileşen habercisi) |
| Sınıf başına ayrı kitap sayısı | `> 12` ise incelemeye düşür (gerçek bir fikir 12 kitapta *olabilir*, ama nadirdir) |
| `atlanan_birlesme` oranı | `> %15` → `θ` yanlış kalibre |

> **K-11** — Birleşme yalnız `birlestir()` kapısından geçer; kapının 6 testi de kodda ayrı ayrı
> adlandırılmış, ayrı ayrı test edilmiş fonksiyonlardır.
> **K-12** — `≈` asla tek sinyalden üretilmez; en az iki bağımsız sinyalin **kesişimi** şarttır.
> **K-13** — Geçişli kapanış `≈` üzerinde **hiçbir yerde** doğrudan çağrılmaz; kod tabanında
> `transitive_closure` çağrısı `≈` grafına uygulanamaz (lint kuralı / tip seviyesinde ayrı graf tipi).
> **K-14** — Sınıflar `birlesme_kenarlari`'ndan türetilir; union-find yapısı diske yazılmaz.
> **K-15** — §3.3 göstergeleri her yükleme sonrası hesaplanır; `max|sınıf| > √N` **yüklemeyi geri alır**.
> **K-16** — `θ_hi`, `θ_lo`, `θ_merge`, `C_max`, `D_max` yapılandırma dosyasında; kod içinde sabit yok.

---

## 4. `önkoşulu` — kesin kısmi sıralama

### 4.1 Yasalar ve neden

`≺` kesin kısmi sıralama olmalı: irrefleksif + geçişli ⇒ asimetrik ⇒ graf bir **DAG**.
DAG olmasının ürün karşılığı: topolojik sıralama var ⇒ okuma planı var.

LLM çevrim üretir ("A'yı anlamak için B, B'yi anlamak için A" tipi karşılıklı bağımlılığı olduğu gibi yazar).
Çevrim tespiti **yazma zamanında** olmalı, gece toplu iş değil: her kenar eklemede artımlı topolojik sıra bakımı.
Çevrim bulununca "rastgele kenar sil" kabul edilemez; sıralama:
1. Çevrim uzunluğu 2 ise (`a ≺ b`, `b ≺ a`) → bu güçlü bir **`≈` adayı sinyalidir** (§3.2 kapısına gönder).
2. Değilse: çevrimdeki **en düşük güvenli** kenarı askıya al (`durum = askıda`, silme).
   Bu, minimum geri-besleme yay kümesinin (minimum feedback arc set, NP-zor) ucuz ve dürüst yaklaşığıdır.
3. Askıya alınan kenar kullanıcıya asla gösterilmez ama kaybolmaz; `askidaki_onkosullar` incelemeye düşer.

> **K-17** — `≺` kenarı ekleme işlemi atomiktir ve çevrim denetimi içerir; çevrim yaratan kenar
> **hiç yazılmaz**, `askidaki_onkosullar` tablosuna gider.
> **K-18** — 2-çevrim özel olarak ele alınır: silme değil, `≈` adayı üretimi.

### 4.2 Geçişli kapanış ne zaman alınır?

**Kapanış = sorgu zamanı, indirgeme = gösterim zamanı.** İkisi de birincil veri değildir.

Kapanış (`≺⁺`) tek bir yerde gerekli: "Bölüm 9 için neyi bilmem lazım?" = tüm atalar. Ama kapanış kenarları
**birinci sınıf olgu olarak saklanamaz**: türetilmiş kenarın sayfa çapası yoktur, Doktrin 2 ihlal edilir.
Çözüm: türetilmiş kenar `türetilmiş` bayrağı ve **türetim yolunu** taşır, çapası yoldaki kenarların çapalarıdır.
Hata birikir: yol güvenleri `p₁…p_k` ise türetilmiş güven `Π pᵢ` (bağımsızlık varsayımı iyimser olduğu için
ayrıca derinlik sınırı koyuyoruz):

> **K-19** — Türetilmiş `≺` kenarı: güven = yol güvenlerinin çarpımı; **derinlik ≤ 4**; güven `< 0.5` ise
> hiç üretilmez. Türetilmiş kenar `kaynak_yolu` alanı olmadan var olamaz.

### 4.3 Geçişli indirgeme neden zorunlu

`≺⁻` (geçişli indirgeme / Hasse diyagramı) iki şey için gerekli:

1. **Gösterim (Doktrin 1).** Kapanmış grafta bir düğümün 40 önkoşulu görünür; indirgenmişte 2 tanesi.
   "Bir ekran = bir karar" tam olarak indirgemenin ürettiği şeydir.
2. **Günlük plan (Doktrin 4).** "Bugün ne okuyayım?" = *bilinmeyenler kümesinin, indirgenmiş DAG'daki
   minimal elemanları*. Bir satırlık plan, matematiksel olarak minimal eleman seçimidir.
   Kapanmış grafta minimal elemanlar aynıdır ama "sıradaki adım" gürültülü görünür.

Kritik teknik nokta: **geçişli indirgeme yalnız DAG'da tektir.** Çevrim varsa indirgeme tek değildir;
yani UI her yenilemede farklı önkoşul gösterebilir. Çevrimsizlik estetik değil, **arayüz determinizmi şartıdır**.

> **K-20** — Kullanıcıya gösterilen her önkoşul listesi `≺⁻` üzerinden üretilir, `≺` veya `≺⁺` üzerinden değil.
> **K-21** — Günlük plan üreticisi: `min_{≺⁻}( atomlar \ bilinenler )`; bu kümeden §Katman 4 kriterleriyle tek eleman seçilir.
> **K-22** — `≺⁻` hesaplanmadan önce asiklik doğrulaması assert edilir; assert düşerse plan üretilmez,
> kullanıcıya "graf onarımda" denir. Sessizce yanlış plan üretmek yasak.

---

## 5. `genellemesi` — kafes mi, değil mi?

### 5.1 Ön-sıralama, kısmi sıralama değil

`⊒` yansımalı ve geçişlidir ama **antisimetrik değildir**: iki atom birbirini genelleyebilir. Yani `⊒` bir
**ön-sıralamadır** (preorder). Standart cebirsel hareket: karşılıklı genellemeyi denklik say, bölüm al,
kısmi sıralama elde et — ve o denklik tam olarak `≈`'dır (L7). Sonuç: **`⊒`, kavram düğümleri üzerinde
kısmi sıralamadır, atomlar üzerinde yalnız ön-sıralamadır** — §1.2'deki iki katmanlı tasarımın bağımsız gerekçesi.

> **K-23** — `⊒` sorguları daima `K` seviyesinde koşar. `A` seviyesinde `⊒` yalnız ham kenar deposudur.

### 5.2 Kafes değil: en küçük üst sınır yoktur, minimal üst sınır kümesi vardır

Kafes olması için her çiftin **tek** bir en küçük üst sınırı (join) olmalı. Bizde üç durum var:

| Durum | Anlamı | Ürün karşılığı |
|---|---|---|
| Tek minimal üst sınır | Ortak genelleme kütüphanede var ve tektir | "Bu iki fikrin ortak çatısı: X (Kitap K, s. 212)" — **göster** |
| Birden çok minimal üst sınır | İki farklı çerçeveleme; hiçbiri diğerinden genel değil | "Bu iki fikir iki farklı şekilde genellenebilir" — **ikisini de göster, seçtirme** |
| Hiç üst sınır yok | Ortak genelleme hiçbir kitapta yok | **BOŞLUK sinyali** — ürünün en değerli çıktılarından biri |

**Karar: kafes tamamlaması (Dedekind–MacNeille) YAPILMAZ.** Tamamlama sentetik eleman uydurur; onların sayfa
çapası yoktur → Doktrin 2 ihlali. Boşluğu kapatmıyoruz, **boşluk olarak raporluyoruz**: "Şu iki fikri birleştiren
genel ilke kütüphanende yok" cümlesi, uydurulmuş bir üst sınırdan kıyaslanamayacak kadar değerlidir.

> **K-24** — `ortak_genelleme(a,b)` bir **küme** döndürür (`MinUB`), tek değer değil.
> Boyu 0 → `boşluk` olayı yayınlanır; 1 → gösterilir; ≥2 → "iki çerçeve" kartı.
> **K-25** — Sentetik (kitapta karşılığı olmayan) genelleme düğümü veritabanına yazılamaz.
> İstisna: §5.3'teki türetilmiş genelleme, `[türetilmiş, doğrulanamadı]` etiketiyle ve
> yalnız *aday* tablosunda.

### 5.3 Yapılı atomlar için en küçük genelleme hesaplanabilir

`formül`/`teorem` atomları terim ağacına ayrıştırılabiliyorsa **anti-birleştirme** (anti-unification /
Plotkin'in en küçük genel genellemesi, LGG) gerçek bir algoritmadır ve *tek* sonuç verir:
`lgg(f(x,a), f(y,a)) = f(z,a)`. §5.2'nin "üst sınır yok" durumunda uydurmadan aday üretmenin tek meşru yolu
budur: sonuç sentetiktir ama **mekanik olarak türetilmiştir**, LLM uydurması değil.

> **K-26** — Yalnız ayrıştırılmış `formül`/`teorem` atomlarında `lgg` çalıştırılır; sonucu
> `aday_genellemeler` tablosuna `[türetilmiş]` etiketiyle yazılır, doğrulama hattından
> (`03-dogrulama.md`) geçmeden kullanıcıya gösterilmez.

---

## 6. Kategori teorisi ile TRANSFER katmanı

### 6.1 Bir alanı kategori olarak modelle

Alan `D` için kategori `C_D`:

- **Nesneler (objects):** `D` alanının kavram düğümleri — sortu `tanım` veya `nicelik` olanlar.
  Tıp: `doz`, `plazma_konsantrasyonu`, `hedef_aralık`, `yan_etki_şiddeti`.
  Mühendislik: `kontrol_parametresi`, `sistem_tepkisi`, `kabul_bandı`, `kararsızlık`.
- **Morfizmalar (morphisms):** `yöntem` sortlu atomlar. Her yöntem atomu bir ok `f: A → B` verir:
  "A'dan hareketle B'ye geçmenin meşru bir yolu".
  Tıp: `dozu_artır : doz → plazma_konsantrasyonu`, `ölç_ve_bekle : plazma_konsantrasyonu → gözlem`.
- **Birim (identity):** her nesnede `id_A` = "değiştirme, olduğu gibi taşı".
- **Bileşke:** yöntemleri ardışık uygulama. Serbest kategori (yöntem grafının serbest kategorisi),
  **doğrulanmış yöntem eşitlikleriyle bölümlenmiş**: kitap "şu iki yol aynı sonucu verir" diyorsa
  veya SymPy iki bileşik formülün eşitliğini gösteriyorsa, o iki yol tek morfizmadır.

Bu model **Katman 1'e şema borcu yükler**: yöntem atomu girdi/çıktı kavramını beyan etmezse kategori kurulamaz
ve transfer katmanı hiç çalışmaz.

> **K-27** — `yöntem` sortlu atom şeması `girdi_kavram_id` ve `cikti_kavram_id` alanlarını **zorunlu** taşır.
> İkisi de çıkarılamayan yöntem atomu `eksik_imza` bayrağıyla saklanır ve transfer motoruna girmez.
> **K-28** — `yol_esit?(p, q)` üç değerli bir kâhindir: `eşit / farklı / bilinmiyor`.
> "Bilinmiyor" asla "eşit" sayılmaz; ölçümlerde ayrı sayılır (kapsama metriği).

### 6.2 Analoji = funktor

Bir analoji, `F : C_kaynak → C_hedef` funktorudur:
- `F₀`: nesneleri nesnelere (`doz ↦ kontrol_parametresi`)
- `F₁`: morfizmaları morfizmalara (`dozu_artır ↦ parametreyi_artır`)
- **Funktoriyalite:** `F(g ∘ f) = F(g) ∘ F(f)` ve `F(id_A) = id_{F(A)}`.

**Funktoriyalite neden "iyi analoji" demektir:** isimleri eşleyen analoji hiçbir şey vermez. Değerli olan,
kaynak alanda üç adımlık akıl yürütüp sonucu taşımanın, her adımı ayrı taşıyıp hedefte yürütmekle **aynı**
sonucu vermesidir. Bu eşitlik funktoriyalitedir. Bozulursa analoji ilk adımda ikna eder, üçüncü adımda
yanlış cevap verir — ürünün en tehlikeli hata modu.

```
          f              g
     A ──────► B ──────────► C          (kaynak alan: tıp)
     │         │             │
  F  │      F  │          F  │
     ▼         ▼             ▼
   F(A) ────► F(B) ───────► F(C)        (hedef alan: mühendislik)
        F(f)          F(g)

  Kare kapanıyor mu?   F(g∘f) =? F(g)∘F(f)
```

Ek zorunluluk: nesneler `A/≈` sınıfları olduğundan **F bölümde iyi tanımlı olmalıdır**: `a ≈ a' ⇒ F(a) = F(a')`.
Bu, §3'teki kongrüans meselesinin bir üst kattaki tekrarıdır.

### 6.3 Kötü analojiyi yakalayan somut sınav

Aday analoji `(F₀, F₁)` geldiğinde şu sınav koşulur:

```
S0  İYİ TANIMLILIK:  a ≈ a' iken F(a) ≠ F(a')  bulunursa       → RET
    ve daha ağırı: F(a) ⊥ F(a')                                → SERT RET, analoji loglanır
S1  BİRİM:           ∀A. F(id_A) = id_{F(A)}                    → ihlal → RET (dejenere eşleme)
S2  KAPSAMA (ν):     eşlenen morfizma sayısı ≥ 3
                     ve en az 2 bileşke-yapılabilir çift
S3  KOMPOZİSYON (κ): örneklenen uzunluk-2 (ve varsa uzunluk-3) yollar üzerinde
                     κ = kapanan kare / (kapanan + bozulan)          (bilinmiyor sayılmaz)
                     κ ≥ 0.75
S4  SADAKAT (φ):     φ = |F₁ görüntüsündeki ayrık morfizma| / |eşlenen morfizma| ≥ 0.6
S5  TANIK:           en az 1 kapanan kare, dört köşesi de sayfa çapalı olarak gösterilebilir
```

`S3`'ün pratik hali: kitapta *adı konmuş bileşik yöntemler* vardır ("önce X, sonra Y — buna Z denir").
Bunlar hazır `g∘f = z` denklemleridir; sınav `F(z) = F(y)∘F(x)` mi diye bakar.

**Neden `S4` şart:** sabit funktor (her şeyi tek nesneye gönderen) funktoriyaliteyi kusursuz geçer ama hiçbir
şey söylemez — "her sistem bir geri besleme döngüsüdür" tipi boş analojiler tam olarak budur. Funktoriyalite
**gerek**, sadakat **yeter** tarafını taşır.

**Kötü analoji tipolojisi ve hangi test yakalar:**

| Tip | Örnek | Yakalayan test |
|---|---|---|
| Dekoratif metafor — nesne eşlemesi var, morfizma yok | "Hücre bir fabrikadır" | S2 (kapsama) |
| Çökmüş analoji — her şey aynı yere gidiyor | "Hepsi geri besleme" | S4 (sadakat) |
| **Tehlikeli analoji** — adımlar tutuyor, zincir bozuluyor | "Titrasyon = gradyan inişi" (durma ölçütü taşınmıyor) | S3 (kompozisyon) |
| Bölümü bozan analoji — kaynakta aynı olan iki şey hedefte çelişiyor | | S0 |
| Yön hatası — funktor doğru ama ters yönde | | Yön kuralı (§6.4) |

**Çıktının biçimi kritik:** S3 bozulduğunda elimizde *belirli bir kapanmayan kare* vardır — dört köşesi de
sayfa çapalı, insanca okunabilir bir açıklama. Sistem "bu analoji zayıf" demez; "tıptaki *durdurma ölçütü*
adımının mühendislikteki karşılığı yok (s. 88 ↔ s. 143)" der.

> **K-29** — Hiçbir transfer kartı S0–S5'i geçmeden kullanıcıya gösterilmez.
> Geçemeyen aday silinmez; `zayif_analojiler` tablosunda `red_nedeni` ve (varsa) **kapanmayan kare**
> ile saklanır — kalibrasyon verisidir.
> **K-30** — `κ`, `φ`, `ν` her transfer kartında saklanır ve kartın "güven" göstergesini besler;
> `κ < 1` olan kart "kısmi analoji" olarak etiketlenir, tam analoji gibi sunulamaz.

### 6.4 Yön

`C_kitap → C_kullanıcı_problemi` ile tersi aynı şey değildir. Ürünün istediği yön kitaptan Açık Sorular
Defteri'ne doğrudur; ters yön ilginç ama eyleme dönüşmez.

> **K-31** — Transfer motoru funktoru daima `kitap_alanı → açık_soru_alanı` yönünde arar.
> Ters yönde bulunan funktor `ters_transfer` olarak ayrı, düşük öncelikli bir akışa gider.

### 6.5 Doğal dönüşüm — iki analojiyi karşılaştırmak

Aynı kitap–problem çifti için iki aday analoji `F, G : C → D` çıktığında soru şu: bunlar gerçekten iki farklı
içgörü mü, yoksa aynı içgörünün iki adlandırması mı? Cevap **doğal dönüşümdür** (natural transformation):
her nesne `A` için hedefte bir ok `η_A : F(A) → G(A)` ve her `f : A → B` için doğallık karesinin kapanması:

```
   F(A) ──η_A──► G(A)
    │              │
 F(f)│              │G(f)
    ▼              ▼
   F(B) ──η_B──► G(B)          G(f) ∘ η_A  =  η_B ∘ F(f)
```

Ürün karşılığı, üç sonuçlu:

| Bulgu | Anlam | Davranış |
|---|---|---|
| `η` var ve tersinir (doğal izomorfizm) | İki analoji **aynı**; sadece terminoloji farklı | Tek kart göster, diğerini sessizce ele (Doktrin 1) |
| `η` var ama tersinmez | `G`, `F`'nin sistematik bir zayıflatması/güçlendirmesi | Tek kart + "daha genel/daha dar hali" satırı |
| `η` yok (doğallık kareleri kapanmıyor) | Gerçekten **iki farklı transfer** | İkisi de değerli; ama Doktrin 1 gereği aynı ekranda değil, biri "derinlik" katmanında |

`η_A`'nın var olması yetmez: hedef alanda **gerçek bir morfizma** (yani "F çerçevesinden G'ye geçiren" bir
yöntem atomu) olmalı. Uydurulmuş `η` yasaktır (Doktrin 2). Bu, transfer kartlarının tekilleştirilmesi
problemidir ve **§3'teki `≈` probleminin bir kat üstündeki tekrarıdır**: aynı kongrüans mantığı, aynı eşik
tuzağı, aynı çözüm (çoklu tanık + kapı + geri alınabilirlik).

> **K-32** — İki transfer kartı aynı `(kitap, açık_soru)` çifti için üretildiğinde doğallık sınavı
> koşar; kapanma oranı `≥ 0.75` ise kartlar tek karta indirgenir. `η` için hedef alanda
> tanık morfizma yoksa indirgeme yapılmaz (iki kart kalır).

### 6.6 Kullanmadığımız kategori teorisi (dürüstlük bölümü)

- **Kolimitler**: §5.2'deki ortak genelleme bir kolimit (pushout) sorusudur; boşluğu raporlamak yettiği için
  genel kolimit makinesi kurmuyoruz.
- **Kan genişlemesi**: kısmi analojiyi alana yaymanın doğru aracı; `AÇIK SORU:` sağlam tanık üretemiyoruz, v1'de yok.
- **Zenginleştirilmiş kategori**: güveni morfizma ağırlığı yapmanın doğru çerçevesi (`[0,1]` çarpımsal monoid).
  §4.2'deki çarpımsal güven bunun gayriresmî hali; resmîleştirmek v2 işi.

---

## 7. Kod kuralları — toplu tablo

| # | Kural | Nerede koşar |
|---|---|---|
| K-01 | `atom_id` yalnız kaynak çapasından | Ayıklama |
| K-02 | Atom değişmez; güncelleme yerine yeni sürüm | Şema |
| K-03 | `kavramlar` materyalize görünüm; rebuild testi CI'da | CI |
| K-04 | Alıntı daima atom seviyesinden | Sunum |
| K-05 | Kanonik temsilci deterministik (byte-eşit rebuild testi) | CI |
| K-06 | Bağıntı sort denetimi; `sort_ihlali > %2` → karantina | Yazma |
| K-07 | `anekdot` çelişki grafına giremez | Yazma |
| K-08 | L1–L9 gecelik bütünlük sorgusu | Toplu iş |
| K-09 | L4/L5/L6 yazma zamanı denetimi | Yazma |
| K-10 | L7 → `≈` adayı (otomatik yazma değil) | Toplu iş |
| K-11 | Tek birleşme kapısı, 6 adlandırılmış test | Birleştirme |
| K-12 | `≈` en az iki bağımsız sinyalin kesişimi | Birleştirme |
| K-13 | `≈` grafında geçişli kapanış çağrısı yasak (tip seviyesinde) | Derleme/lint |
| K-14 | Sınıflar kenarlardan türetilir; union-find diske yazılmaz | Depolama |
| K-15 | `max|sınıf| > √N` → yükleme geri alınır | Yükleme sonrası |
| K-16 | Tüm eşikler yapılandırmada, kodda sabit yok | Yapılandırma |
| K-17 | `≺` ekleme atomik + çevrim denetimli | Yazma |
| K-18 | 2-çevrim → `≈` adayı | Yazma |
| K-19 | Türetilmiş `≺`: çarpımsal güven, derinlik ≤ 4, ≥ 0.5, `kaynak_yolu` zorunlu | Sorgu |
| K-20 | Gösterim daima `≺⁻` üzerinden | Sunum |
| K-21 | Günlük plan = `≺⁻` minimal elemanları | Plan üretimi |
| K-22 | Asiklik assert düşerse plan üretilmez ("graf onarımda") | Plan üretimi |
| K-23 | `⊒` sorguları kavram seviyesinde | Sorgu |
| K-24 | `ortak_genelleme` küme döndürür; boş küme = boşluk sinyali | Sorgu |
| K-25 | Sentetik genelleme düğümü yazılamaz | Şema |
| K-26 | `lgg` yalnız ayrıştırılmış formül/teorem; `[türetilmiş]` etiketli aday | Türetme |
| K-27 | `yöntem` atomunda girdi/çıktı kavramı zorunlu | Şema/Ayıklama |
| K-28 | `yol_esit?` üç değerli; "bilinmiyor" ≠ "eşit" | Transfer |
| K-29 | Transfer kartı S0–S5 kapısından geçmeden gösterilmez | Transfer |
| K-30 | `κ, φ, ν` kartta saklanır; `κ < 1` → "kısmi analoji" etiketi | Transfer |
| K-31 | Funktor yönü: kitap alanı → açık soru alanı | Transfer |
| K-32 | Aynı çift için iki kart → doğallık sınavı; tanık yoksa indirgeme yok | Transfer |

---

## 8. Açık sorular

- `AÇIK SORU:` `θ_hi`/`θ_lo`/`θ_merge` bu belgeden çıkarılamaz; ilk 50 kitaplık külliyatta perkolasyon eğrisi
  (θ'ya karşı `max|sınıf|`) çizilip diz noktasının **üstünde** bir nokta seçilmeli — `02-yenilik-ve-graf.md` ile ortak iş.
- `AÇIK SORU:` S3'ün örnekleme stratejisi: tüm uzunluk-2 yollar `Σ deg²` maliyetli; örneklem büyüklüğü ve
  `κ`'nın güven aralığı belirlenmeli.
- `AÇIK SORU:` **En büyük tek risk** — LLM, yöntem atomlarının girdi/çıktı imzasını (K-27) ne oranda doğru
  çıkarıyor? %60'ın altındaysa kategorik transfer modeli pratikte kurulamaz ve yalnız nesne düzeyinde
  daha zayıf bir modele düşmek gerekir.
- `AÇIK SORU:` G4'teki "çelişen bağıntı çiftleri" listesi tam mı? `⇏` ile `⊒` etkileşimi netleşmedi.
