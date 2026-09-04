# 05a — Matematik & Mühendislik Kitaplarının Okunması

**Uzman:** Mühendislik Profesörü (uygulamalı matematik & mühendislik bilimleri)
**Kapsam:** Katman 1 (sindirim) ve Katman 2'nin (bağlantı) bu alana özgü kuralları.

---

## 3 cümlelik özet

Bu alanda atom, "bir fikir" değil **koşulları, sonucu ve geçerlilik zarfı olan bir hüküm**dür; bir teoremin hipotezini kaybetmek teoremin kendisini kaybetmekten daha tehlikelidir, çünkü yanlış hüküm sessizce kullanılır. İspatlar bütün olarak saklanmaz; her ispat için **ispat fikri + anahtar hamle + 7 adımlık iskelet** çıkarılır ve tam metne sayfa çapası bırakılır — böylece hacim 20 kat düşerken yeniden üretilebilirlik korunur. Her kitap için zorunlu bir **notasyon sözlüğü** üretilir ve her atom hem kitaptaki hem kanonik biçimde saklanır; birim/boyut alanları makine tarafından doldurulur ve `03-dogrulama.md`'nin sembolik denetleyicisine ham girdi olur.

---

## 0. Sınır çizimi (ne yazmıyorum)

- Genel atom şeması `01-bilgi-modeli.md`'nin işi. Ben **alan uzantısı** (`alan: mat-muh`) tanımlıyorum: taban atoma eklenen alanlar.
- Kenar tiplerinin graf semantiği `02-yenilik-ve-graf.md`'de. Ben bu alanda hangi kenarların **hangi metinsel sinyalden** doğduğunu söylüyorum.
- Sembolik doğrulamanın nasıl çalıştığı `03-dogrulama.md`'de. Ben ona **hangi alanların çıkarılacağını** sipariş ediyorum (§7).

---

## 1. Bu tür bir kitapta atom nedir?

Atom = **tek başına yanlışlanabilir bir hüküm veya tek başına kullanılabilir bir işlem**. Ölçüt şudur: atomu bağlamından koparıp başka bir kitabın yanına koyduğunda hâlâ doğru mu ve hâlâ uygulanabilir mi? Değilse eksik alan var demektir.

### 1.1 Ortak uzantı alanları (her `mat-muh` atomunda)

| Alan | Tip | Not |
|---|---|---|
| `ifade_kitap` | LaTeX | Kitapta basıldığı gibi. **Asla değiştirilmez.** |
| `ifade_kanonik` | LaTeX | Notasyon sözlüğüyle normalize edilmiş biçim (§3). |
| `semboller[]` | liste | `{sembol, kanonik_kavram, rol, boyut, birim}` (§7). |
| `kosullar[]` | liste | Hipotezler. Her biri ayrı satır, her biri ayrı `[gerekli mi?]` bayrağı. |
| `sonuc` | metin | Koşullar sağlandığında ne iddia ediliyor. |
| `gecerlilik_zarfi` | metin | Sayısal/fiziksel aralık: `Re ∈ [4e3, 1e8]`, `x yeterince küçük`, `f iki kez türevlenebilir`. |
| `onkosul_atomlari[]` | id[] | Bu atomu **okumak** için gereken atomlar (§4). |
| `capa` | {kitap, bolum, sayfa, konum} | Doktrin 2. Çapasız atom yazılmaz. |
| `capa_guveni` | 0–1 | OCR/PDF sayfa eşlemesi şüpheliyse < 0.9 ve `[doğrulanamadı]`. |
| `dogrulama_durumu` | enum | `sembolik_gecti` / `boyutsal_gecti` / `denenmedi` / `basarisiz` / `kabul_edilmis_tutarsizlik` |

### 1.2 Tür bazlı ek alanlar

| Tür | Atom mu? | Ek alanlar | Kural |
|---|---|---|---|
| `tanim` | **Evet** (en yüksek öncelik) | `tanimlanan_kavram`, `tanimlayici_kosullar[]`, `denk_tanimlar[]`, `sinir_ornekleri[]` | Asla atlanmaz. Tüm graf tanımların üzerine kurulur. |
| `aksiyom` | Evet | `sistem_adi`, `bagimsizlik_notu` | Nadir ama kritik; hangi teoremlerin hangi aksiyoma dayandığı izlenir (ör. seçim aksiyomu). |
| `notasyon` | Evet (hafif) | `sembol`, `okunusu`, `kapsam_bolumleri`, `cakisma[]` | Kitap başına sözlüğe de yazılır (§3). |
| `lemma` | Evet | `hizmet_ettigi_teoremler[]` | Tek bir teoreme hizmet ediyorsa ve tekrar kullanılmıyorsa o teoremin `ispat_iskeleti` adımına indirgenir. |
| `teorem` | Evet | `kosullar[]`, `sonuc`, `keskin_mi`, `karsi_ornek_atomu`, `ispat` (§2) | Koşulsuz teorem atomu **geçersizdir**, üretimi engellenir. |
| `sonuc_onerme` (corollary) | Evet | `turetildigi_teorem`, `ek_varsayim` | Türetme kenarı zorunlu. |
| `ispat` | **Hayır** — teorem atomunun alt kaydı | `ispat_fikri`, `anahtar_hamle`, `iskelet[]`, `teknik_etiketleri[]`, `tam_metin_capa` | §2. |
| `turetme` | Evet | `baslangic_atomlari[]`, `adimlar[]`, `eklenen_varsayimlar[]`, `kaybedilen_genellik` | §6. |
| `formul` | Evet | `boyut_denklemi`, `birim_sistemi`, `boyutsuz_gruplar[]`, `hata_terimi` | Yaklaşıklıksa `hata_terimi` boş bırakılamaz. |
| `cozulmus_ornek` | Evet (seçilmiş olanlar) | `uygulanan_atomlar[]`, `sayisal_girdi`, `sayisal_cikti`, `sablon_id` | Her `sablon_id` için **ilk** örnek atomdur; sonrakiler `tekrar` işaretlenir (§5). |
| `alistirma` | Evet ama ayrı sınıf | §8 | Grafın hüküm katmanına girmez. |
| `tasarim_kurali` | Evet | `hangi_kosulda`, `emniyet_payi`, `kaynak_standart`, `ihlal_sonucu` | "Kirişte L/d > 20 ise sehim kontrolü zorunlu" tipi. Mühendislik kitabının en transfer-edilebilir atomudur. |
| `ampirik_sabit` | Evet | `deger`, `belirsizlik`, `birim`, `gecerli_aralik`, `veri_kaynagi`, `boyutsal_tutarli_mi` | Aralıksız ampirik sabit **yazılmaz**; aralıksız sabit zehirdir. |
| `karsi_ornek` | Evet | `hangi_kosulu_kiriyor`, `hangi_teorem` | Bir hipotezin gerekliliğini kanıtlar; asla atlanmaz (§5). |
| `uyari` | Evet | `yaygin_hata`, `dogrusu` | Kitaptaki "caution/pitfall/dikkat" kutuları. Ucuz ve çok değerli. |

**Karar:** `ispat` dışında her tür bağımsız atomdur. İspat bağımsız atom değildir, çünkü teoremsiz ispatın anlamı yoktur ve bağımsız olması grafı ikiye katlar.

---

## 2. İspat protokolü

### 2.1 Üç katmanlı saklama

Her teorem atomunun `ispat` alt kaydı **üç** parçadan oluşur:

1. `ispat_fikri` — 2–4 cümle. "Neden doğru olması gerektiğini" anlatır, adım saymaz.
2. `anahtar_hamle` — **tek cümle**. Bilseydin ispatın kalanını kendin kurabileceğin adım.
3. `iskelet[]` — en fazla **7 adım**, her adım ≤ 1 cümle + kullandığı atom id'si.

Artı: `tam_metin_capa` (sayfa aralığı) ve `teknik_etiketleri[]` (`ayrik_hiperduzlem`, `sabit_nokta`, `kompaktlik`, `hakim_yakinsama`, `enerji_yontemi`, `boyut_analizi`, `tumevarim`, `celiskiyle`, `perturbasyon`).

**Tam ispat metni saklanmaz** — kitabın sayfası zaten oradadır ve Doktrin 3 gereği sistem kullanıcıyı sayfaya yollar, sayfanın yerine geçmez.

### 2.2 Anahtar hamle nasıl çıkarılır (4 dedektör)

- **D1 — Dışarıdan gelen nesne.** İspatta, teorem ifadesinde geçmeyen bir nesne tanımlanıyorsa (yardımcı fonksiyon, akıllıca seçilmiş ε, test fonksiyonu, örtü, potansiyel/Lyapunov fonksiyonu, ayırıcı küme) anahtar hamle **odur**. Tek dedektörle vakaların çoğu kapanır.
- **D2 — Hipotezin ilk kullanıldığı yer.** Her hipotezi işaretle, ispatta ilk nerede kullanıldığını bul. Hiç kullanılmayan hipotez varsa ya çıkarım hatalıdır ya hipotez gereksizdir → `[doğrulanamadı]` + insan bayrağı.
- **D3 — İndirgeme adımı.** "Genelliği bozmadan", "bu durumu daha önce kanıtlanmış hale indirgiyoruz" → indirgeme anahtar hamledir.
- **D4 — Dilsel sinyaller.** "the trick is", "the key observation", "note that", "now comes the crucial point", "işin püf noktası". Yazarlar anahtar hamleyi genellikle işaret eder.

Birden fazla aday çıkarsa: **hipotezi tüketen** adım kazanır (D2 > D1 > D3 > D4).

### 2.3 Sıkıştırma kuralı

> **Yeniden üretim testi:** Bu alanı bilen ama bu ispatı görmemiş biri, `ispat_fikri + anahtar_hamle + iskelet + kullanılan atomlar` ile ispatı tahtada yeniden kurabiliyorsa sıkıştırma başarılıdır. Kuramıyorsa iskelete adım eklenir, 7 adımı aşarsa ispat **bölünür**: ara sonuç `lemma` atomuna terfi eder.

Uzun ispat için tek meşru büyüme yolu budur: derinleşmek değil, **lemmaya bölünmek**. 30 sayfalık bir ispat 4 lemma + 6 adımlık bir omurga olur.

### 2.4 İspatın tam metnine mutlaka gönderilecek 4 durum

1. İspat tekniği kitapta **tekrar kullanılıyorsa** (teknik, sonuçtan değerlidir).
2. İspat **yapıcıysa** (algoritma veriyorsa) — o zaman ayrıca `turetme` atomu üretilir.
3. Kullanıcının Açık Sorular Defteri'nde o `teknik_etiketi` geçiyorsa.
4. İspat, hipotezin **neden gerekli** olduğunu gösteriyorsa (genelde karşı-örnekle birlikte).

---

## 3. Notasyon cehennemi

### 3.1 Karar: Kitap başına notasyon sözlüğü **zorunludur**

Sindirimin 1. geçişinde, atomlardan önce üretilir. Atomlar bu sözlük olmadan yazılamaz.

| Alan | Örnek |
|---|---|
| `sembol` | `∇f` |
| `latex` | `\nabla f` |
| `kanonik_kavram` | `kavram:gradyan` |
| `anlam` | "f'in gradyanı, **sütun** vektör" |
| `ilk_gorunum` | s. 68 |
| `kapsam` | Bölüm 3–11 |
| `cakisma` | `σ`: Böl. 2–6 gerilme, Böl. 9 standart sapma |
| `varyant_yazimlar` | `grad f`, `Df^T`, `f'` |

### 3.2 Normalizasyon kuralı

- Her atom **iki** ifade taşır: `ifade_kitap` (aynen) ve `ifade_kanonik` (kanonik kavram id'lerine bağlı).
- **Kitaptaki biçim asla ezilmez.** Kullanıcı sayfayı açtığında gördüğüyle sistemin gösterdiği aynı olmalı; aksi halde çapa güveni çöker.
- Graf eşleşmesi (Katman 2) **yalnız** `ifade_kanonik` ve `kanonik_kavram` üzerinden yapılır. `∇f` ile `grad f` aynı düğüme bağlanır, aksi halde "yenilik" ölçümü çöp olur.
- Sunumda (Katman 4) varsayılan: **kullanıcının okuduğu kitabın notasyonu**. Başka kitaptan atom gösterilirken satır altına: `bu kitapta ∇f, senin okuduğunda grad f`.

### 3.3 Çakışma yönetimi

Aynı sembol, aynı kitapta iki anlam taşıyorsa → sembol **bölüm aralığına göre** ayrıştırılır, `cakisma` bayrağı konur ve o aralıktaki atomlar `capa_guveni -= 0.1` alır. Aynı kavram, farklı kitaplarda ters işaret konvansiyonuyla tanımlıysa (ör. mühendislikte basınç pozitif, mekanikte çekme pozitif) → `isaret_konvansiyonu` alanı zorunlu ve bu bir **`celisiyor` kenarı değildir**; `konvansiyon_farki` kenarıdır. Bu ayrımı yapmayan sistem sahte çelişki üretir.

---

## 4. Önkoşul çıkarımı

### 4.1 Altı sinyal

| # | Sinyal | Nereden | Güç |
|---|---|---|---|
| S1 | Açık beyan: "assumes familiarity with…", önsöz, "bu bölüm için gerekli" | Önsöz, bölüm girişi | çok yüksek |
| S2 | İç atıf: "by Theorem 3.2", "(4.17)'den" | Metin içi referanslar → kitap-içi DAG | yüksek |
| S3 | **Tanımsız sembol**: bir sembol kullanılıyor ama kitapta daha önce tanımlanmamış | Notasyon sözlüğü farkı | yüksek (dış önkoşul göstergesi) |
| S4 | **Tanımsız terim**: teknik terim tanımsız kullanılıyor, kanonik kavram kaydında var | Terim çıkarımı + kavram kaydı | orta |
| S5 | **Teknik talebi**: `hemen her yerde`, `hâkim yakınsama`, `σ-cebir`, `zayıf türev` → ölçü teorisi; `tensör indisi yükseltme` → diferansiyel geometri | `teknik_etiketleri` | yüksek |
| S6 | Alıştırma seviyesi sıçraması: bölüm alıştırmaları başka bir olgunluk istiyor | Alıştırma atomları | düşük (tek başına hüküm vermez) |

### 4.2 Sert / yumuşak ayrımı — ürünün kilit kararı

- **Sert önkoşul:** Onsuz *ifadeyi okuyamazsın*. İfadede geçen bir sembol/terim tanımsız kalır. → Okuma engeli.
- **Yumuşak önkoşul:** İfadeyi ve sonucu kullanabilirsin, *ispatı* takip edemezsin. → Engel değil, uyarı.

Bu ayrım Doktrin 3'ün (reddetme yok) matematik alanındaki karşılığıdır. Çıktı asla "Bölüm 9'u okuyamazsın" değildir:

> "Bölüm 9'un **sonuçları** okunabilir (s. 214–219, 6 sayfa). **İspatları** ölçü teorisi istiyor — sinyal: s. 216'da 'hâkim yakınsama teoremi' tanımsız kullanılıyor. Önce Ders X Böl. 2'yi (kütüphanende var) okursan ispatlar da açılır."

### 4.3 Hüküm üretimi

`onkosul` kenarı şu üç alansız yazılamaz: `siddet` (sert/yumuşak), `kanit_alintisi` (metinden birebir cümle), `kanit_capasi` (sayfa). Kanıtsız önkoşul hükmü üretimi **engellenir** — yoksa sistem "önce ölçü teorisi lazım" diye herkesi korkutur.

Eşik: bir bölümde ≥ 2 sert sinyal veya ≥ 4 yumuşak sinyal varsa bölüm seviyesinde önkoşul hükmü çıkar. Tek sinyal atom seviyesinde kalır.

---

## 5. Neyin atlanabileceği — kesin kural listesi

### ATLANABİLİR (A-kuralları)

| # | Kural |
|---|---|
| A1 | Tarihsel giriş / biyografi / teşekkür. (İstisna: tarihsel bölüm bir **kavram yanılgısını** anlatıyorsa `uyari` atomu olur.) |
| A2 | Aynı `sablon_id`'nin 2., 3., … çözülmüş örneği — yalnız sayılar değişiyorsa. |
| A3 | Tablo/nomogram ekleri, log tabloları, birim dönüşüm ekleri. (Ampirik **katsayı** tabloları hariç → `ampirik_sabit`.) |
| A4 | Kullanıcının kütüphanesinde zaten kanıtlanmış tekrar bölümleri ("Review of Calculus"). Kanonik kavram örtüşmesi ≥ %85 ise atla. |
| A5 | Aynı teoremin 2. alternatif ispatı — **yeni teknik etiketi getirmiyorsa**. |
| A6 | Örnek içindeki uzun aritmetik yürütme (girdi + çıktı + yöntem yeter). |
| A7 | Yazılım/araç öğreticileri (MATLAB sözdizimi vb.), kitap versiyonuna bağlı ekler. |
| A8 | Bölüm sonu özetleri (atomlar zaten üretildiyse bilgi taşımaz). |
| A9 | Uzun literatür taramaları / "further reading" — kaynak listesi olarak saklanır, atomlaştırılmaz. |

### ASLA ATLANAMAZ (N-kuralları)

| # | Kural | Neden |
|---|---|---|
| N1 | Her `tanim`. | Grafın taşıyıcı duvarı. |
| N2 | Teoremlerin **hipotezleri**. Sonucu alıp koşulu atmak en pahalı hatadır. | Sessizce yanlış kullanım. |
| N3 | `karsi_ornek`ler — özellikle bir hipotezin gerekliliğini gösterenler. | Hipotezin *neden* orada olduğunu tek onlar söyler. |
| N4 | İşaret ve birim konvansiyonları, koordinat sistemi seçimi. | Tüm bölümü sessizce ters çevirir. |
| N5 | Ampirik bağıntıların **geçerlilik aralığı** ve veri kaynağı. | Aralık dışı kullanım = mühendislik kazası. |
| N6 | Her yeni yöntemin **ilk** çözülmüş örneği. | Yöntemin uygulanış grameri orada. |
| N7 | Yaklaşıklıkların **hata terimi / mertebesi** ve ne zaman bozulduğu. | `O(h²)` atılırsa formül yalan olur. |
| N8 | İspatların `anahtar_hamle`si (ispatın kalanı değil). | Yeniden üretilebilirlik. |
| N9 | Sonradan kullanılacak sembollerin tanım cümleleri. | Notasyon çökmesi. |
| N10 | "Dikkat / yaygın hata" kutuları. | Ucuz, yoğun, doğrudan transfer edilebilir. |
| N11 | Emniyet katsayıları, sınır koşulları, tasarım kabulleri. | `tasarim_kurali` atomunun canı. |
| N12 | Bir sonucun **keskin (sharp/tight)** olup olmadığı beyanı. | Genelleme denemelerini yönlendirir. |

**Kesişim kuralı:** A ve N çakışırsa **N kazanır.** Örnek: tarihsel bir giriş bir işaret konvansiyonunu açıklıyorsa atlanmaz (N4 > A1).

---

## 6. Türetme zincirleri

### 6.1 Temsil

Kenar tipi: `turetilir(kaynak → hedef)`. Kenarın **kendi alanları vardır** — bu belgedeki en önemli tasarım kararı:

| Alan | Örnek |
|---|---|
| `adim_kisa` | "sürtünmesiz akış boyunca enerji korunumu integrali" |
| `eklenen_varsayimlar[]` | `["sürtünmesiz", "sıkıştırılamaz", "aynı akım çizgisi üzerinde", "kararlı"]` |
| `kaybedilen_genellik` | "3B alan denkleminden 1B skaler bağıntıya" |
| `tersine_cevrilebilir_mi` | hayır |
| `capa` | s. 174 |

`eklenen_varsayimlar` alanı olmadan türetme zinciri süs olur; onunla birlikte **geçerlilik zarfının otomatik hesabı** mümkün olur:

> `gecerlilik_zarfi(atom) = kök varsayımlar ∪ (zincirdeki her kenarın eklenen_varsayimlari)`

Bu hesap, "bu formülü buraya uygulayabilir miyim?" sorusunun makine cevabıdır ve Katman 3'ün (transfer) en sert filtresidir.

### 6.2 "Bu formül nereden geliyor?" ekranı

Doktrin 1 gereği tek ekran, tek karar. Gösterilen: **köken zinciri**, en fazla 4 sıçrama, her sıçrama tek satır.

```
Δp = f·(L/D)·(ρv²/2)                                    [Böl. 6, s. 347]
 ↑ boyut analizi + Moody deneyleri (f'in Re, ε/D'ye bağlılığı)  + [türbülanslı, tam gelişmiş]
Boyutsuz basınç düşüşü = Φ(Re, ε/D, L/D)                [Böl. 5, s. 293]
 ↑ Buckingham Π teoremi                                  + [7 değişken, 3 temel boyut]
Navier–Stokes + süreklilik                              [Böl. 4, s. 227]

Geçerlilik zarfı (birikmiş): Newtonsal akışkan · kararlı · tam gelişmiş · dairesel kesit · Re > 4000
[tam zinciri aç: 7 adım]   [kütüphanendeki 2 farklı türetme]
```

Kurallar: (a) 4 sıçramadan fazlası **katlanır**, (b) her satır çapalı, (c) **birikmiş geçerlilik zarfı her zaman gösterilir** — kullanıcının unuttuğu şey odur, (d) aynı formülün kütüphanede birden fazla türetmesi varsa sayısı belirtilir ama açılmaz (Doktrin 1).

### 6.3 Kütüphane çapında birleştirme

Farklı kitaplar aynı formüle farklı yollardan varır. Bunlar **ayrı türetme zincirleri** olarak saklanır, birleştirilmez; ama hedef atom aynı kanonik düğümdür. "Yenilik" hükmü burada üretilir: *formül tanıdık ama türetme yolu yeni* → bu kitap %94 tekrar olsa bile Bölüm 5 değerlidir.

---

## 7. Birim ve boyut — `03-dogrulama.md`'ye sipariş

Sindirim, doğrulayıcının işini yapmaz; ona **eksiksiz girdi** verir. Çıkarılması zorunlu 6 kalem:

1. **Sembol tablosu** — her sembol için `{sembol, kanonik_kavram, boyut_vektoru, birim_si, kitapta_kullanilan_birim, tipik_aralik}`.
2. **Boyut vektörü** — 7 elemanlı sabit sıra: `[M, L, T, Θ, I, N, J]`. Örnek: basınç `[1,-1,-2,0,0,0,0]`, boyutsuz `[0,0,0,0,0,0,0]`.
3. **Birim sistemi bayrağı** — `SI` / `US-customary` / `CGS` / `Gaussian` / `karışık`. Kitap bazında varsayılan, atom bazında istisna. (Gaussian ↔ SI elektromanyetizma karşılaştırmalarında sahte çelişki üreten şey budur.)
4. **Boyutsuz grup listesi** — `Re`, `Nu`, `Pr`, `Ma`, `Bi` … ve kitabın kendi tanımı (Nusselt'te karakteristik uzunluk seçimi kitaptan kitaba değişir → `karakteristik_uzunluk` alanı zorunlu).
5. **Aşkın fonksiyon argümanları** — `log`, `exp`, `sin`, `tanh` içindeki her ifade işaretlenir; doğrulayıcı bunların boyutsuz olmasını arar. En ucuz ve en verimli hata yakalayıcı budur.
6. **Boyutsal tutarsızlık beyanı** — `boyutsal_tutarli_mi: false` + `birime_bagli_sabit: {deger, birim}`. Manning denklemi (`k = 1.0 m^{1/3}/s`), Hazen–Williams, birçok ampirik bağıntı **kasıtlı olarak** boyutsal tutarsızdır. Bunlar `basarisiz` değil `kabul_edilmis_tutarsizlik` etiketi alır; sistem böyle bir formülü gösterirken **birimi zorunlu yazar**.

**Doğrulayıcıya net sipariş:** yukarıdaki 6 kalem doldurulduğunda boyutsal denetim saf bir fonksiyondur — `boyut(sol) == boyut(sağ)`, argümanlar boyutsuz, sabitlerin birimi bildirilmiş. Sembolik denetim (SymPy) ise `turetme.adimlar[]` üzerinde çalışır. Denetlenemeyen atom `denenmedi` ile geçer, **asla sessizce "doğru" sayılmaz.**

---

## 8. Alıştırmalar

**Karar: Alıştırma atomdur, ama hüküm değildir.** `alistirma` atomları grafın iddia katmanına girmez (yenilik/çelişki hesabına katılmaz); `test_eder` kenarıyla kavram atomlarına bağlanan ayrı bir sınıftır.

Alanlar: `hedef_atomlar[]`, `tur`, `zorluk (1–5)`, `cozum_kitapta_var_mi`, `beklenen_sure_dk`, `sonuc_iceriyor_mu`.

`tur` değerleri: `rutin` (şablon tekrarı) · `kavram` (tanımın sınırını yoklar) · `genelleme` (hipotezi gevşetir) · `karsi_ornek_avi` · `tasarim` (açık uçlu, mühendislik) · `hesaplama`.

### Seçim kuralı

Her yöntem/teorem atomu için en fazla **2** alıştırma saklanır: bir **minimal** (yöntemi ilk kez uygulatan) ve bir **sınır** (yöntemin bozulduğu/kırıldığı yer). Gerisi sayılır, saklanmaz: `alistirma_sayisi: 47`.

### Terfi kuralı (kritik)

Ders kitapları teoremleri alıştırmaya saklar: *"Exercise 4.12 shows that the converse fails."* Bir alıştırma **bir sonuç ifade ediyorsa** (`sonuc_iceriyor_mu: true`), o alıştırma ayrıca bir `teorem` veya `karsi_ornek` atomuna **terfi eder**, `kaynak_tipi: alistirma` etiketiyle ve `dogrulama_durumu: denenmedi` ile. Bunu yapmayan sistem kitabın içeriğinin ciddi bir kısmını kaybeder.

### Kullanım

1. **Aralıklı hatırlatma:** Kullanıcı bir atomu "anladım" işaretlediyse, o atomun `minimal` alıştırması 7/21/60 gün sonra günlük tek satırlık plana girebilir (Doktrin 4: 1 kitap + 1 eylem).
2. **Transfer:** Bir `tasarim` alıştırmasının yapısı Açık Sorular Defteri'ndeki bir problemle eşleşiyorsa, alıştırma "bunu kendi problemin için çöz" biçiminde sunulur. Bu, kitaptan işe geçişin en kısa yoludur.
3. **Önkoşul testi:** Bölüm 9'a girmeden Bölüm 6'nın `sinir` alıştırması sorulur; başarısızlık önkoşul hükmünü tetikler.

---

## 9. Örnek atomlar

> Kaynak: Boyd & Vandenberghe, *Convex Optimization* (Böl. 3, 5) ve White, *Fluid Mechanics* (Böl. 6).
> Sayfa numaraları **temsilidir**; gerçek sindirimde PDF çapasından üretilir ve `capa_guveni` taşır.

```yaml
- id: atom:bv-3.1.1-disbukey-fonksiyon
  tur: tanim
  alan: mat-muh
  capa: {kitap: "Boyd & Vandenberghe, Convex Optimization", bolum: "3.1.1", sayfa: 67}
  capa_guveni: 0.97
  tanimlanan_kavram: kavram:disbukey-fonksiyon
  ifade_kitap: "f: R^n → R is convex if dom f is convex and f(θx+(1−θ)y) ≤ θf(x)+(1−θ)f(y)"
  ifade_kanonik: "\\forall x,y \\in \\operatorname{dom} f,\\ \\theta\\in[0,1]:\\ f(\\theta x+(1-\\theta)y)\\le \\theta f(x)+(1-\\theta)f(y)"
  tanimlayici_kosullar:
    - "dom f dışbükey bir küme"           # sıkça atlanır, atlanırsa tanım yanlış
    - "eşitsizlik tüm x,y ve tüm θ∈[0,1] için"
  denk_tanimlar:
    - {ifade: "epi f dışbükey küme", capa: {sayfa: 75}}
    - {ifade: "∇²f(x) ⪰ 0 (f iki kez türevlenebilirse)", capa: {sayfa: 71}, ek_kosul: "C²"}
  sinir_ornekleri:
    - "f(x)=1/x, dom f = R\\{0} → dışbükey DEĞİL (tanım kümesi dışbükey değil)"
  semboller:
    - {sembol: "θ", kanonik_kavram: kavram:disbukey-birlesim-katsayisi, boyut: [0,0,0,0,0,0,0]}
  onkosul_atomlari: [atom:bv-2.1-disbukey-kume]
  dogrulama_durumu: denenmedi
  atlanabilir: false          # N1

- id: atom:bv-notasyon-nabla
  tur: notasyon
  capa: {kitap: "Boyd & Vandenberghe", bolum: "Appendix A", sayfa: 640}
  sembol: "∇f(x)"
  okunusu: "f'in x'teki gradyanı"
  kanonik_kavram: kavram:gradyan
  anlam: "R^n'de **sütun** vektör; Df(x) Jacobian'ın devriği"
  varyant_yazimlar: ["grad f", "Df(x)^T", "f_x"]
  kapsam_bolumleri: "tüm kitap"
  cakisma: "yok"
  not: "Bazı mühendislik kitaplarında ∇f satır vektörüdür; kütüphane karşılaştırmasında devrik farkı sahte çelişki üretir → konvansiyon_farki kenarı."

- id: atom:bv-5.3.2-slater-guclu-dualite
  tur: teorem
  capa: {kitap: "Boyd & Vandenberghe", bolum: "5.3.2", sayfa: 226}
  ifade_kanonik: "Dışbükey primal problem + Slater koşulu ⇒ d^* = p^* ve dual optimum erişilir (p^* > -∞ ise)."
  kosullar:
    - {k: "problem dışbükey: f_0, f_i dışbükey; h_i afin", gerekli_mi: true}
    - {k: "Slater: ∃x ∈ relint D, f_i(x) < 0 (afin olmayan i için), Ax = b", gerekli_mi: true,
       not: "afin kısıtlar için katı eşitsizlik GEREKMEZ — bu incelik en sık kaybedilen bilgidir"}
    - {k: "p^* sonlu", gerekli_mi: true}
  sonuc: "dualite açığı sıfır; dual optimum bir (λ*, ν*) tarafından erişilir"
  keskin_mi: "evet — Slater düşerse karşı-örnek var (atom:bv-5.3.2-karsiornek)"
  gecerlilik_zarfi: "yalnız dışbükey problemler; dışbükey olmayanda yalnız zayıf dualite (d^* ≤ p^*)"
  ispat:
    ispat_fikri: >
      Erişilebilir (u,v,t) değerlerinin kümesi A ile 'p*'tan iyi' bölge B ayrık iki dışbükey kümedir.
      Ayırıcı hiperdüzlem teoremi bir (λ,ν,μ) verir; Slater koşulu bu hiperdüzlemin dikey olamayacağını
      (μ ≠ 0) garanti eder, μ'ye bölünce tam olarak dual fonksiyonun p*'a ulaştığı görülür.
    anahtar_hamle: "Slater noktası, ayırıcı hiperdüzlemin dikey (μ=0) olmasını imkânsız kılar — normalize edip μ=1 alabilirsin."   # D1+D2
    iskelet:
      - "A = {(u,v,t) : ∃x, f_i(x)≤u_i, h_i(x)=v_i, f_0(x)≤t} dışbükey (dışbükeylikten)"
      - "B = {(0,0,s) : s < p^*} dışbükey; A ∩ B = ∅ (p^* tanımı)"
      - "Ayırıcı hiperdüzlem: (λ,ν,μ) ≠ 0, λ ⪰ 0, μ ≥ 0"
      - "μ = 0 varsay → Slater noktasında çelişki (katı eşitsizlik ihlali)"     # ANAHTAR
      - "μ > 0, μ=1'e normalize et → inf_x L(x,λ,ν) ≥ p^*"
      - "g(λ,ν) ≥ p^* ve zayıf dualiteden g ≤ p^* ⇒ eşitlik, optimum erişilir"
    teknik_etiketleri: [ayrik_hiperduzlem, celiskiyle, normalizasyon]
    tam_metin_capa: {sayfa: "234–236"}
  onkosul_atomlari: [atom:bv-2.5-ayirici-hiperduzlem, atom:bv-5.1-lagrange-dual, atom:bv-5.2.2-zayif-dualite]
  onkosul_siddet: {atom:bv-2.5-ayirici-hiperduzlem: yumusak}   # ifadeyi okumaya gerek yok, ispatı için gerekli
  dogrulama_durumu: denenmedi
  atlanabilir: false          # N2, N8, N12

- id: atom:bv-5.5.3-kkt-turetme
  tur: turetme
  capa: {kitap: "Boyd & Vandenberghe", bolum: "5.5.3", sayfa: 243}
  baslangic_atomlari: [atom:bv-5.3.2-slater-guclu-dualite, atom:bv-5.1-lagrange-dual]
  hedef_atom: atom:kkt-kosullari
  adimlar:
    - {a: "f_0(x*) = g(λ*,ν*) yaz (sıfır dualite açığı)", eklenen_varsayim: "güçlü dualite geçerli"}
    - {a: "g(λ*,ν*) = inf_x L(x,λ*,ν*) ≤ L(x*,λ*,ν*)", eklenen_varsayim: "-"}
    - {a: "L(x*,λ*,ν*) = f_0(x*) + Σλ*_i f_i(x*) ≤ f_0(x*) çünkü λ*⪰0, f_i(x*)≤0", eklenen_varsayim: "x* uygun"}
    - {a: "Zincirin iki ucu eşit ⇒ tüm eşitsizlikler eşitlik", eklenen_varsayim: "-"}
    - {a: "Eşitlik 2 ⇒ x*, L(·,λ*,ν*)'yi minimize eder ⇒ ∇_x L(x*,λ*,ν*) = 0", eklenen_varsayim: "f_i türevlenebilir"}
    - {a: "Eşitlik 3 ⇒ Σλ*_i f_i(x*) = 0, her terim ≤0 ⇒ λ*_i f_i(x*) = 0 (tamamlayıcı gevşeklik)", eklenen_varsayim: "-"}
  eklenen_varsayimlar_birlesik: ["türevlenebilirlik", "güçlü dualite (⇐ Slater)", "x* uygun"]
  kaybedilen_genellik: "türevlenemeyen problemlerde KKT yerine alt-gradyan koşulu gerekir"
  tersine_cevrilebilir_mi: "kısmen — dışbükey problemde KKT ⇒ optimallik (ters yön ayrı atom)"
  anahtar_gozlem: "İki eşitsizlik arasına sıkıştırılan zincirin çökmesi; tamamlayıcı gevşeklik buradan **bedava** gelir."
  dogrulama_durumu: sembolik_gecti     # SymPy: ∇L=0 ve tamamlayıcı gevşeklik cebirsel olarak yeniden üretildi

- id: atom:white-6.4-darcy-weisbach
  tur: formul
  capa: {kitap: "White, Fluid Mechanics", bolum: "6.4", sayfa: 347}
  ifade_kitap: "\\Delta p = f \\frac{L}{D} \\frac{\\rho V^2}{2}"
  ifade_kanonik: "\\Delta p = f\\,(L/D)\\,\\rho V^2/2"
  semboller:
    - {sembol: "Δp", kanonik_kavram: kavram:basinc-dususu, boyut: [1,-1,-2,0,0,0,0], birim_si: "Pa"}
    - {sembol: "f",  kanonik_kavram: kavram:darcy-surtunme-faktoru, boyut: [0,0,0,0,0,0,0], birim_si: "-",
       uyari: "Fanning faktörü f_F = f/4 — kitaplar arası en yaygın 4 kat hatası"}
    - {sembol: "L",  boyut: [0,1,0,0,0,0,0], birim_si: "m"}
    - {sembol: "D",  boyut: [0,1,0,0,0,0,0], birim_si: "m"}
    - {sembol: "ρ",  boyut: [1,-3,0,0,0,0,0], birim_si: "kg/m^3"}
    - {sembol: "V",  boyut: [0,1,-1,0,0,0,0], birim_si: "m/s", not: "kesit-ortalama hız"}
  boyut_denklemi: "sol [1,-1,-2,...] = sağ [0]+[0]+[1,-3,0]+[0,2,-2,0] = [1,-1,-2,...] ✓"
  birim_sistemi: SI
  boyutsuz_gruplar: ["Re = ρVD/μ", "ε/D", "L/D"]
  gecerlilik_zarfi: "kararlı · tam gelişmiş · dairesel kesit · sabit yoğunluk · Newtonsal"
  turetme_zinciri: [atom:white-5.3-buckingham-pi, atom:white-4.x-navier-stokes]
  hata_terimi: "yok (tanım gereği kesin; belirsizlik f'te)"
  dogrulama_durumu: boyutsal_gecti
  atlanabilir: false

- id: atom:white-6.6-colebrook
  tur: ampirik_sabit
  capa: {kitap: "White, Fluid Mechanics", bolum: "6.6", sayfa: 351}
  ifade_kanonik: "1/\\sqrt{f} = -2\\log_{10}\\!\\left(\\frac{\\varepsilon/D}{3.7} + \\frac{2.51}{Re\\sqrt{f}}\\right)"
  deger: "kapalı (implicit) bağıntı — sabitler: 3.7 ve 2.51"
  belirsizlik: "±%15 (Moody diyagramı okuma belirsizliği dahil)"
  gecerli_aralik: "Re > 4000 (türbülanslı) · 0 ≤ ε/D ≤ 0.05"
  veri_kaynagi: "Nikuradse kum-pürüz deneyleri + Colebrook–White (1939) ticari boru verisi"
  boyutsal_tutarli_mi: true
  askin_argumanlar: ["log10 argümanı: (ε/D)/3.7 + 2.51/(Re√f) → boyutsuz ✓"]
  cozum_notu: "kapalı; Swamee–Jain açık yaklaşımı %1 içinde (s. 352) — ayrı atom"
  dogrulama_durumu: boyutsal_gecti
  atlanabilir: false          # N5 — aralık atılırsa atom zehirli olur
  transfer_ipucu: "sabit-nokta iterasyonu ile çözülen kapalı denklem şablonu → Açık Soru #12 (titrasyon döngüsü) ile yapısal eşleşme adayı"

- id: atom:bv-alistirma-5.1
  tur: alistirma
  capa: {kitap: "Boyd & Vandenberghe", bolum: "Alıştırmalar 5", sayfa: 273}
  ifade_kanonik: "min x^2+1 s.t. (x-2)(x-4) \\le 0; primal/dual optimalleri, dual fonksiyonu ve Lagrange açığını çıkar."
  hedef_atomlar: [atom:bv-5.1-lagrange-dual, atom:bv-5.3.2-slater-guclu-dualite]
  tur_detay: minimal
  alistirma_turu: kavram
  zorluk: 2
  beklenen_sure_dk: 20
  cozum_kitapta_var_mi: false
  sonuc_iceriyor_mu: false          # terfi yok
  neden_saklandi: "tek değişkenli; dualiteyi elle çizilebilir hale getiren minimal örnek (N6 ruhu)"
```

---

## 10. İşleyiş sırası (4 geçiş)

1. **Geçiş 1 — İskelet & notasyon.** İçindekiler, teorem/tanım numaralandırması, notasyon sözlüğü, birim sistemi bayrağı. Atom üretilmez.
2. **Geçiş 2 — Atomlar.** Tanım → teorem → türetme → formül → örnek → alıştırma sırasıyla (tanımlar önce, çünkü herkes onlara bağlanır).
3. **Geçiş 3 — İç kenarlar.** `turetilir`, `onkosul`, `test_eder`, `karsi_ornek` — kitap içi. Sonra doğrulayıcıya (03) toplu gönderim.
4. **Geçiş 4 — Kütüphane kenarları.** Kanonik kavram üzerinden `ayni` / `genellemesi` / `celisiyor` / `konvansiyon_farki`; yenilik yüzdesi ve "şu 11 sayfayı oku" hükmü burada üretilir.

---

## 11. Açık sorular

- `AÇIK SORU:` PDF'ten formül çıkarımının güvenilirliği belirleyici darboğaz. OCR'lı taramada `ifade_kitap` üretilemezse atom yazılmalı mı, yoksa yalnız `capa` + düz metin özetiyle "zayıf atom" mu olmalı? Öneri: zayıf atom + `capa_guveni ≤ 0.5` + sembolik doğrulamaya hiç sokulmaması.
- `AÇIK SORU:` Kanonik kavram kaydı (`kavram:gradyan` vb.) nereden gelecek? Elle küratörlü çekirdek sözlük mü, kütüphaneden büyüyen açık sözlük mü? Ben çekirdek + büyüme öneriyorum ama sınırı `01-bilgi-modeli.md` çizmeli.
- `AÇIK SORU:` `anahtar_hamle` çıkarımının kalitesi ölçülebilir mi? Öneri: 30 klasik teoremden oluşan altın küme, insan tarafından etiketlenmiş anahtar hamlelerle; regresyon testi olarak koşulur.
- `AÇIK SORU:` Alıştırmaların telif durumu. Alıştırma metinlerinin birebir saklanması kullanıcının kendi kitabı için sorun değil, paylaşımda sorun olabilir. `07-transfer.md` ve mimari bunu netleştirmeli.
