# 07 — TRANSFER KATMANI
### Ar-Ge Direktörü & Bilgi Transferi Stratejisti

> **3 cümlelik özet**
> 1. Kullanıcı **Açık Sorular Defteri**'nde gerçek problemlerini tutar; her problem ve her fikir atomu aynı soyut **iskelet** (aktör–ilişki–kısıt–hata modu) uzayına indirgenir ve eşleme kelimeler üzerinden değil, bu iskeletler üzerinden yapılır.
> 2. Bir eşleme ancak **nedensel mekanizma düzeyinde** (yüzeysel ya da ilişkisel değil) doğrulanır, **zorunlu bir "bu benzetme şurada çöker" bölümü** üretilebilir ve yedi sert kapıyı geçerse kullanıcıya gösterilir — haftada en fazla 2 kart, çoğu hafta sıfır.
> 3. Sistem eski problemleri yeni kitaplara karşı sürekli yeniden tarar (delta tabanlı, haftalık maliyet birkaç sent), her kabul/red/sonuç kaydını puanlama ağırlıklarına geri besler ve **kullanıcının hiç problemi yoksa transfer katmanı kapalı kalır** — uydurma problem üretmez, sadece kütüphaneden "problem tohumu" önerir.

---

## 0. Bu katmanın tek görevi ve tek yasağı

**Görev:** Kullanıcının bugün tıkandığı bir işe, okuduğu başka bir alandan çalışan bir mekanizma taşımak.

**Yasak:** Çalışmayan bir benzetmeyi çalışıyormuş gibi sunmak. Tek bir sahte analoji, doğru olan yüz tanesinin güvenini yer. Bu belgedeki tüm tasarım kararları bu asimetriye göre alınmıştır: **yanlış öneri, kaçırılmış öneriden 20 kat pahalıdır.**

Bu katman `09-cebirsel-temeller.md` ile şöyle bölüşür: orada analojinin yapı-koruyuculuğu (funktoriyalite) biçimsel olarak tanımlanır. Burada onun ürün karşılığı vardır: **kırılma noktası, funktorun funktor olmadığı yerin adıdır.** Biçimsel garantiye ulaşamadığımız her yerde, ulaşamadığımızı yazılı olarak söyleriz.

---

## 1. Açık Sorular Defteri (Open Problems Ledger)

### 1.1 Problem kaydı şeması

```
Problem {
  id                : "P-014"
  baslik            : string          # KULLANICININ KENDİ CÜMLESİ — sistem asla yeniden yazmaz
  alanlar[]         : etiket          # {kontrol, üretim} — çoklu, serbest + kanonik eşlem
  durum             : taslak | aktif | beklemede | çözüldü | terk
  aciliyet          : 1 | 2 | 3       # 1=fısıltı  2=üzerinde çalışıyorum  3=tıkandım
  ufuk              : gün | ay | yıl  # çözüm ne zaman lazım
  basari_kriteri    : { metin, olculebilir: bool }
  kisitlar[]        : { tip: kaynak|fiziksel|yasal|orgutsel|zaman, metin, sert: bool }
  denenmis[]        : { yaklasim, sonuc, neden_basarisiz }
  iskelet           : Skeleton        # §2.1 — türetilmiş, kullanıcıya normalde gösterilmez
  imza              : uint64          # iskeletin bit imzası, ön eleme için
  olusturma, son_dokunma, sessize_alma_tarihi
  sonuc_kayitlari[] : Outcome         # §7
  red_gecmisi[]     : Rejection       # §4.4
}
```

Alan sayısı 14. Bunların **ikisi zorunlu**: `baslik` ve `aciliyet`. Kalan her şey `[boş]` olabilir; boş alan transfer puanını düşürür ama kaydı engellemez. Sürtünmeyi sıfıra yakın tutmak, doldurulmuş ama ölü bir defterden iyidir.

### 1.2 İki cümleden işe yarar kayıt: "3 soru protokolü"

Kullanıcı şunu yazar ve fazlasını yazmaz:

> "Fırındaki sıcaklık kontrolcüsü sürekli overshoot yapıyor. Kazancı elle ayarlamaktan bıktım."

**Adım 1 — Sessiz çıkarım.** Çıkarıcı (extractor) alanları doldurur, her birini `[çıkarım]` etiketiyle işaretler:

| Alan | Değer | Kaynak |
|---|---|---|
| alanlar | kontrol teorisi, termal süreç | `[çıkarım]` |
| aciliyet | 2 | `[çıkarım]` — "bıktım" ≠ "durdum" |
| hata modu | salınım / aşım | `[çıkarım]` — "overshoot" doğrudan |
| denenmiş | elle kazanç ayarı → yetersiz | `[çıkarım]` |
| başarı kriteri | `[boş]` | — |
| kısıtlar | `[boş]` | — |

**Adım 2 — En fazla 3 soru.** Sorulan tek şey, **transfer puanını fiilen değiştiren** alanlardır. Diğer hiçbir şey sorulmaz:

1. **"Çözüldüğünü nasıl anlarsın? Neyi ölçeceksin?"** → `basari_kriteri`. Bu olmadan transfer *test edilemez*, dolayısıyla kapalı döngü (§7) çalışmaz.
2. **"Neyi değiştiremezsin?"** → `kisitlar`. Taşıyıcı koşul kontrolü (§3.2) buradan beslenir; en sık transfer ölüm sebebi burada saklıdır.
3. **"Ne denedin de olmadı?"** → `denenmis`. Negatif bilgi; kullanıcının zaten elediği şeyi bir daha önermeyi engeller.

Kurallar: her soru tek satır cevap kabul eder. **"Bilmiyorum" geçerli bir cevaptır** ve alanı `[boş]` bırakır. Üç soru tek ekranda sırayla gelir (Kural 1: bir ekran = bir karar). Kullanıcı ekranı kapatırsa kayıt `taslak` olarak durur ve **transfer eşlemesine girmez** — eksik iskeletle eşleme yapmak sahte analojinin en verimli üretim yoludur.

**Adım 3 — İskelet türetme.** §2.1'deki iskelet çıkarılır. Kullanıcıya gösterilmez, ama "neden bu öneri?" tıklandığında açılır.

### 1.3 Yaşam döngüsü kararları

- 60 gün dokunulmamış `aktif` problem otomatik `beklemede`'ye düşer. Beklemedeki problem **eşlemeye girmeye devam eder** ama puanına 0.85 çarpanı uygulanır. Sebebi §6: unutulmuş problemin 8 ay sonra cevaplanması bu ürünün en değerli anıdır, onu otomatik silmek intihardır.
- `çözüldü` ve `terk` eşlemeden çıkar ama **silinmez**; §7'deki kalibrasyonun eğitim verisidir.
- Kullanıcı bir problemi "sessize al" diyebilir: eşlemede kalır, kart üretmez. Yüksek gürültülü problemler için kaçış valfi.

---

## 2. Eşleme mekanizması

### 2.1 Ortak iskelet şeması (Skeleton)

Tek en önemli tasarım kararı: **problem ile atom aynı şemayla temsil edilir.** İki farklı temsil arasında çeviri yapmak yerine, ikisini de aynı soyut uzaya indiriyoruz. "Titrasyon" ile "optimizasyon" hiçbir kelime paylaşmaz; ama ikisinin de iskeleti şudur: *bir kontrolör, gecikmeli geri besleme altında, bir eşiğe doğru bir aktüatörü adım adım sürer.*

```
Skeleton {
  hedef      : { tip: dengeleme | maksimize | eşik-aşma | ayrıştırma |
                      arama | dayanıklılık | hızlandırma | koruma,
                 yön: artır | azalt | sabit-tut }

  aktorler[] : { rol,                       # KAPALI SÖZLÜK — aşağıya bak
                 çokluk: 1 | az | çok | sürekli,
                 gozlenebilir: bool,
                 kontrol_edilebilir: bool }

  iliskiler[]: { kaynak_rol,
                 tip: neden-olur | kısıtlar | dengeler | doygunlaştırır |
                      geciktirir | çoğaltır | tüketir | maskeler,
                 hedef_rol,
                 isaret: + | −,
                 guc: zayıf | orta | baskın }

  kisitlar[] : { rol, tip, sertlik: sert | yumuşak }

  rejim      : { olcek, zaman_sabiti, gurultu: düşük|orta|yüksek,
                 tersinirlik: tersinir | tek-yönlü }

  hata_modu  : salınım | kaçış | kilitlenme | çöküş |
               yavaş-sürüklenme | yanlış-optimum | kırılganlık
}
```

**Rol sözlüğü kapalıdır (24 rol).** Serbest metin rol adı yasaktır — çünkü serbest metin, kelime benzerliğini arka kapıdan geri sokar. Roller:

`kontrolör · aktüatör · sensör · tampon · eşik · gecikme · geri-besleme-çevrimi · rakip · kaynak-havuzu · bölünebilir-yük · tekil-darboğaz · simetri-grubu · gürültü-kaynağı · taşıyıcı-ortam · kapı-bekçisi · yayılım-cephesi · rezerv · maliyet-fonksiyonu · gözlemci · bozucu-girdi · ölçek-parametresi · hafıza · dışsallık · eşik-aşan-olay`

Bir atom iskeletlenemiyorsa (mekanizma taşımıyorsa — tanım, tarih anekdotu, biyografi) **transfer havuzuna hiç girmez.** Deneyimsel tahminimiz: bir kitabın atomlarının yaklaşık %10–15'i mekanizma taşır. Havuzu bu kadar erken daraltmak, hem maliyeti hem sahte analoji yüzeyini 7 kat küçültür.

### 2.2 Üç aşamalı boru hattı

```
[1] ÖN ELEME (ucuz, deterministik, µs)
    imza = 64 bit:  24 rol biti | 8 ilişki tipi | 7 hata modu |
                    8 hedef tipi | 17 rejim/kısıt biti
    Kapı: popcount(imza_P & imza_A) ≥ 4
      VE  hata_modu(P) ∩ hata_modu(A) ≠ ∅   (ya da ikisi de dengeleme hedefli)
    Geçme oranı gözlemlenen: ~%5–8

[2] İSKELET HİZALAMA (LLM, orta maliyet)
    Problem iskeleti ile atom iskeleti arasında en büyük ortak
    ilişki alt-grafını bul. Rol ADLARI değil, rol TİPLERİ eşleşir.
    Çıktı: eşleme tablosu + eşleşmeyen kenarlar listesi (bu liste
    §4.2'de kırılma noktasının hammaddesidir).

    S = 2·Σ w(eşleşen ilişki) / (Σ w(ilişki_P) + Σ w(ilişki_A))
        w(neden-olur) = 2.0 ; w(diğer) = 1.0
        hata_modu tam eşleşmesi: +0.10 (tavan 1.0)

[3] NEDENSEL DOĞRULAMA (LLM, pahalı, sadece S ≥ 0.45 için)
    Mekanizmanın taşıyıcı koşulları (§3.2) çıkarılır ve her biri
    için hedef alanda TANIK aranır. Tanıksız koşul → düzey L2 → düşer.
```

**Spesifiklik testi (§4.3'ün kalbi, ama boru hattında burada durur):** Aynı atomu, defterden rastgele seçilmiş 20 problemle de hizala. `S_rastgele` ortalamasını hesapla. Gereklilik:

```
spesifiklik = S / (S_rastgele + 0.05) ≥ 2.5
```

Bu, "her şey bir geri besleme çevrimidir" tipi evrensel iskeletleri otomatik olarak öldürür. Bir atom herkesle eşleşiyorsa kimseyle eşleşmiyor demektir. Maliyeti düşük: 20 hizalama, ucuz modelle, sadece [3]'e çıkan adaylar için.

---

## 3. Transfer puanı

### 3.1 Formül

```
G  (kazanç)  = N · U · (1 + λ·D) / (1 + λ)        λ = 0.6
C  (güven)   = S^1.5 · M · E · (1 − ρ·D)          ρ = 0.35
TS           = G · C^γ                             γ = 1.6      TS ∈ [0, 1]
```

| Sembol | Ne | Aralık | Kaynağı |
|---|---|---|---|
| `S` | yapısal örtüşme | 0–1 | §2.2 hizalama |
| `M` | mekanizma aktarılabilirliği | 0–1 | doğrulanan taşıyıcı koşul oranı |
| `D` | alan mesafesi | 0–1 | alan çifti matrisi (tıp↔kontrol = 0.8) |
| `E` | kanıt gücü | 0–1 | atomun epistemik etiketi (`03-dogrulama`, `05b`, `05c`) |
| `N` | yenilik | 0–1 | Katman 2 grafı: kullanıcı bunu zaten biliyor mu |
| `U` | aciliyet | 0.6 / 0.8 / 1.0 | problemden |

`E` ölçeği: kanıtlanmış teorem 1.0 · tekrarlanmış deney 0.85 · tek çalışma 0.6 · uzman gözlemi 0.45 · anekdot 0.2 · `[doğrulanamadı]` 0.15.

### 3.2 Taşıyıcı koşullar (carrier conditions) — `M`'in tanımı

Her mekanizma atomu, işlemesi için gereken koşulların açık listesini taşır. Titrasyon için:

1. Sistem kendi kendini dengeleyen (self-regulating) olmalı — girdi sabitlenince çıktı bir değere oturmalı.
2. Ölçüm gecikmesi, adım aralığından kısa olmalı.
3. Yanıt monoton olmalı (doz ↑ → etki ↑).
4. Geri alma (weaning) mümkün olmalı — tek yönlü sistemlerde geçersiz.

```
M = (doğrulanan koşul sayısı) / (toplam koşul sayısı)
    KESİN SIFIR: bir koşulun hedef alanda YANLIŞ olduğu biliniyorsa M = 0.
```

Yani M kısmi kredi verir ama bir tane kesin ihlal her şeyi bitirir. Bu asimetri kasıtlıdır.

### 3.3 Uzaklık gerilimi: neden hem çarpan hem ceza?

Uzak alan transferi **daha değerlidir** (kullanıcı onu kendi başına asla bulamaz) ve **daha risklidir** (ortak bir çerçeve olmadığı için sahte analoji tespiti zorlaşır). Bu gerilimi tek bir sayıya sıkıştırmak yerine iki tarafa da yazıyoruz:

- `G` içinde `(1 + λD)`: mesafe kazancı **doğrusal** artırır, en fazla %60.
- `C` içinde `(1 − ρD)`: mesafe güveni **doğrusal** düşürür, en fazla %35.
- `TS = G · C^1.6`: γ > 1 olduğu için güven, kazançtan daha ağır basar. **Sistem risk-kaçınandır.**

Sonuç davranışı: uzak alan transferi ancak `S` ve `M` yüksekse öne çıkar. Zayıf yapılı uzak analoji (tam olarak sahte analojinin tarifi) puanda yakın alan transferinin de altına düşer. Bu tam olarak istenen şeydir.

`U` (aciliyet) sadece `G`'de, yani **sıralamada** rol oynar; §5'teki eşiği geçmeye tek başına yetmez. Acil bir problem, kötü bir öneriyi hak etmez.

---

## 4. ⚠️ SAHTE ANALOJİ SAVUNMASI

Bu bölüm ürünün hayatta kalma bölümüdür. Diğer her şey pazarlıklıdır, bu değildir.

### 4.1 Analoji düzeyleri — sadece L3 sunulur

| Düzey | Ne örtüşüyor | Örnek | Karar |
|---|---|---|---|
| **L1 — yüzeysel** | nesne öznitelikleri, kelimeler, görüntü | "Atom da güneş sistemi gibi, ortada çekirdek var" | **Loglanmaz bile.** Ön eleme kelimeye hiç bakmadığı için doğal olarak elenir. |
| **L2 — ilişkisel** | ilişki grafları örtüşüyor, ama işleyiş nedenleri farklı | "Şirket de organizma gibi, büyüyor ve besleniyor" | **Sunulmaz.** `ilham` etiketiyle saklanır; sadece kullanıcı açıkça "Keşif Modu"nu açarsa ayda 1 kez, `[spekülatif]` bandıyla. |
| **L3 — nedensel** | mekanizma aynı, taşıyıcı koşulların hedefte **tanığı** var | "Titrasyondaki 'yanıtsızlık = kanal doygun' testi" | **Sunulabilir.** Kalan tüm kapılara tabi. |

**L2 → L3 sınavı, işlemsel hâli:** Her taşıyıcı koşul için, hedef alandan somut bir **tanık** (witness) gösterilmelidir — ya kullanıcının defterindeki bir kısıt/gözlem, ya kütüphanedeki çapalı bir atom. Tanık gösterilemeyen koşul doğrulanmamış sayılır. Tanık oranı = `M`. Yani `M` hem puanın bileşeni hem düzey testidir; `M < 0.5` ise öneri L2'dir ve düşer.

### 4.2 Zorunlu alan: KIRILMA NOKTASI (breakdown clause)

Her transfer önerisi, veri modelinde **`kirilma_noktasi` alanı boş bırakılamaz** bir kayıttır. Boşsa öneri üretilmemiş sayılır.

```
KirilmaNoktasi {
  cumle       : string   # "Bu benzetme şurada çöker: ..."  ≤ 30 kelime
  kaynak      : uretilmis | capali
  capa?       : { kitap, bolum, sayfa }     # varsa zorunlu gösterilir
  siniflandirma : eslesmeyen-kenar | ihlal-riski-tasiyan-kosul |
                  rejim-uyusmazligi | capraz-kanit
}
```

Kırılma noktası **uydurulmaz, türetilir.** Üç kaynağı var, öncelik sırasıyla:

1. **Eşleşmeyen kenarlar** (§2.2 adım [2] çıktısı). Atom iskeletinde olup problem iskeletinde karşılığı olmayan ilişkiler. Titrasyon örneğinde: `tolerans → doygunlaştırır → aktüatör` kenarı fırında yoktur. Cümle bundan yazılır.
2. **En kırılgan taşıyıcı koşul.** `M < 1` ise, doğrulanmamış koşullardan en kritik olanı. `M = 1` ise, kullanıcının kısıtlarına en yakın duran koşul.
3. **Çapraz kanıt.** Sistem kendi grafında bu mekanizmayı `çürütüyor` kenarıyla bağlanmış atom arar. Bulursa **kırılma noktası o atomun kendisi olur ve çapasıyla gösterilir** — bu en güçlü hâlidir, çünkü Kural 2'yi kırılma tarafında da uygular.

Üçünden de cümle çıkmıyorsa: **öneri düşer.** "Bu benzetme her yerde çalışır" diyen bir öneri, yeterince incelenmemiş bir öneridir.

### 4.3 Yedi sert kapı (hard gates)

Puan ne olursa olsun, bunlardan biri kapalıysa kart gösterilmez:

| # | Kapı | Gerekçe |
|---|---|---|
| G1 | Kırılma noktası üretilemedi | §4.2 |
| G2 | Analoji düzeyi L3 değil (`M < 0.5`) | §4.1 |
| G3 | Atomun sayfa çapası yok | Doktrin Kural 2 |
| G4 | Bir taşıyıcı koşulun hedefte **yanlış** olduğu biliniyor | §3.2 |
| G5 | Spesifiklik oranı < 2.5 | §2.2 — evrensel iskelet tuzağı |
| G6 | Zombi analoji kara listesi eşleşmesi | §4.4 |
| G7 | Aynı (problem × mekanizma ailesi) çifti son 90 günde reddedildi | §4.5 |

### 4.4 Zombi analoji kara listesi

Kültürel olarak yaygın, yapısal olarak sahte, ve LLM'lerin üretmeye en meyilli olduğu kalıplar. Mekanizma ailesi düzeyinde bloklanır, ürün ömrü boyunca elle bakımı yapılır:

`beyin = bilgisayar` · `şirket = organizma` · `ekonomi = hidrolik sistem` · `DNA = kaynak kodu` · `kuantum belirsizliği = özgür irade/bilinç` · `entropi = düzensizlik/toplumsal çöküş` · `evrim = ilerleme/optimizasyon` · `sinir ağı = beyin` · `piyasa = ekosistem` · `bağışıklık sistemi = ordu` · `Gödel teoremi = bilginin sınırı` · `kaos teorisi = öngörülemezlik genel olarak`

Bu listedeki kalıplar **sonuç olarak** yasak değil, **gerekçe olarak** yasaktır: sistem "beyin bir bilgisayardır, o hâlde..." diyemez. Ama belirli bir nörobilim atomu belirli bir önbellek problemine L3 düzeyinde ve taşıyıcı koşulları tanıklı olarak eşlenirse geçebilir — çünkü o zaman gerekçe metafor değil mekanizmadır.

### 4.5 Kullanıcı reddettiğinde sistem ne öğrenir?

Red tek düğme değildir. **Beş sebep**, her biri farklı bir öğrenme sinyali:

| Red sebebi | Sistemin hatası nerede | Güncelleme |
|---|---|---|
| **"Alakasız"** | Problem iskeleti yanlış çıkarılmış | Aynı problemde 2. redde → 3 soru protokolü yeniden tetiklenir. Atom cezalandırılmaz. |
| **"Zaten biliyordum"** | `N` (yenilik) modeli hatalı | Atom kullanıcının `bilinen` kümesine eklenir; komşu atomlar Katman 2 grafında 2 adıma kadar `N` cezası alır. |
| **"Benzetme zorlama"** | Sahte analoji üretildi — **en ağır hata** | Mekanizma çifti kalıcı kara listeye. Hizalama şablonu global −0.3. Aynı hafta başka kart gösterilmez. Haftalık kota 2 hafta boyunca 1'e düşer. |
| **"Doğru ama uygulanamaz"** | `M` / taşıyıcı koşul modeli eksik | Kullanıcıya tek soru: "hangi koşul tutmuyor?" Cevap problemin `kisitlar`ına yazılır ve o koşula bağlı tüm gelecek önerileri keser. En yüksek getirili red türüdür. |
| **"Şu an değil / problem öldü"** | Zamanlama | Problem `beklemede`/`terk`. Puanlamaya ceza yok. |

Varsayılan düğme yoktur; kullanıcı sebep seçmezse kart "görüldü, karar yok" olarak kapanır ve **hiçbir ağırlık güncellenmez.** Sessizlikten sinyal uydurmak, sahte analojinin ikinci kaynağıdır.

---

## 5. Sunum sözleşmesi

### 5.1 Kota ve eşik

- **Eşik: `TS ≥ 0.55`** (0–1 ölçeğinde) **ve yedi kapının hepsi açık.**
- **Haftada en fazla 2 kart.** Günlük planda aynı gün en fazla 1 — ve o kart, günün "1 somut eylem"i **olarak** görünür, ona ek bir satır olarak değil (Kural 4).
- **Sıfır kart normaldir.** Eşiği geçen yoksa **hiçbir şey gösterilmez** — "bu hafta transfer yok" bildirimi bile yok. Boş haftalar ürünün dürüstlük kanıtıdır.
- Beklenen rejim: yoğun okuyan bir kullanıcıda **ayda 2–5 kart**. Bu sayının artması hedef değildir; kabul oranının artması hedeftir.

### 5.2 Kart anatomisi — 6 satır, 1 eylem

```
┌──────────────────────────────────────────────────────────┐
│ P-014 · "Fırın kontrolcüsü sürekli overshoot yapıyor"    │  ← kullanıcının cümlesi
│                                                          │
│ Yoğun bakımda vazopressör titrasyonunda, iki ardışık     │  ← mekanizma, alan-nötr,
│ dozda yanıt yoksa doz artırılmaz — ilaç değiştirilir.    │     tek cümle
│ Yanıtsızlık "kazanç düşük" değil, "kanal doygun"         │
│ demektir.                                                │
│                                                          │
│ 📖 Marino, ICU Book · Böl. 53 · s. 1012–1014             │  ← çapa (Kural 2)
│                                                          │
│ ⚠ Şurada çöker: hastada tolerans/taşiflaksi zamanla      │  ← ZORUNLU
│   gelişir, fırın rezistansında gelişmez — o yüzden       │
│   "yanıtsızlık" fırında geri dönüşsüz arıza sinyali      │
│   olabilir, doygunluk değil.                             │
│                                                          │
│ ▸ 20 dk'lık test: bir sonraki overshoot'ta kazancı       │  ← tek eylem, zaman kutulu
│   artırmadan önce aktüatör çıkışını logla. %95'te mi?    │
│                                                          │
│   [ Deneyeceğim ]   [ Alakasız ]   [ Zorlama ]           │
└──────────────────────────────────────────────────────────┘
```

Kartta gösterilmeyen ama bir tık ötede duran: iskelet hizalama tablosu, `TS` ve bileşenleri, doğrulanan/doğrulanamayan taşıyıcı koşullar, spesifiklik oranı. Kural 1: derinlik hep bir tık ötede.

**Eylem tasarım kuralı:** eylem 20 dakikayı aşamaz ve **ayırt edici** olmalıdır — sonucu, transferin doğru mu yanlış mı olduğunu ayırt etmelidir. "Bunu düşün" bir eylem değildir. Ayırt edici eylem üretilemiyorsa kart düşer; bu de facto sekizinci kapıdır ve pratikte en çok öneriyi eleyen kapıdır.

---

## 6. Zaman içinde çalışma — geriye dönük eşleme

Kullanıcı bugün bir kitap okur, cevabı 8 ay sonra yüklediği kitapta çıkar. Bu senaryo istisna değil, **ürünün ana vaadidir.** Üç tetikleyici:

| Tetikleyici | Yön | Kapsam | Sıklık |
|---|---|---|---|
| **T1 — yeni kitap** | ileri | yeni kitabın mekanizma atomları × tüm aktif+beklemede problemler | yükleme başına |
| **T2 — yeni/güncellenmiş problem** | **geri (retroaktif)** | tüm kütüphanenin mekanizma atomları × 1 problem | problem kaydı başına |
| **T3 — uyanış taraması** | delta | sadece **değişmiş taraf** içeren çiftler | haftalık gece işi |

T3'ün delta kaynakları — tam liste, çünkü "her şeyi yeniden tara" maliyeti öldürür:
- (a) problemin alanı/kısıtı/iskeleti güncellendi,
- (b) atomun iskeleti Katman 2'de yeni bir kenarla değişti (yeni bir `genellemesi` kenarı atomun rejimini genişletebilir),
- (c) kişisel ağırlık vektörü `w` §7'de kaydırıldı,
- (d) bir taşıyıcı koşul, sonradan yüklenen bir kitapla **tanık kazandı** — en değerli delta türü budur.

Tam yeniden tarama **yılda en fazla 2 kez**, sadece puanlama modeli ana sürüm atladığında.

### 6.1 Maliyet hesabı (somut)

Varsayımlar: 120 kitaplık kütüphane · kitap başına ~400 atom · 48.000 atom · %12'si mekanizma taşır → **5.760 mekanizma atomu** · defterde 15 aktif/beklemede problem.

```
ÖN ELEME (bit AND + popcount):
  5.760 × 15 = 86.400 karşılaştırma → tek makinede < 10 ms, sıfır LLM maliyeti.
  Geçme oranı ~%6 → ~5.200 aday çift (tüm kütüphane için, bir kerelik).

T1 — yeni kitap (400 atom → 48 mekanizma atomu):
  48 × 15 = 720 çift → ön eleme sonrası ~43 → hizalama (ucuz model) 43 çağrı
  → S ≥ 0.45 geçen ~9 → nedensel doğrulama (güçlü model) 9 çağrı
  + spesifiklik testi 9 × 20 (ucuz) = 180 çağrı
  Tahmini: kitap başına ~0.20–0.35 USD.

T2 — yeni problem (retroaktif, tüm kütüphane):
  5.760 × 1 → ön eleme sonrası ~350 → hizalama 350 → doğrulama ~40
  Tahmini: problem başına ~1.20–2.00 USD, BİR KERELİK.

T3 — haftalık uyanış (delta):
  Tipik hafta: 2 güncellenmiş problem + ~120 değişmiş atom
  → ~200 aday → hizalama ~200 → doğrulama ~15
  Tahmini: haftada ~0.30 USD.
```

**Yıllık toplam kaba tahmin: 25–40 USD** (ayda ~2 kitap, ayda ~1 yeni problem). Bu, ürünün savunulabilir maliyet zarfının çok içinde.

### 6.2 Eşleme önbelleği

Her (problem, atom) çifti için sonuç saklanır: `{S, M, TS, düzey, karar, hesaplama_sürümü, tarih}`. Yeniden hesaplama sadece hesaplama sürümü ya da taraflardan biri değiştiğinde. Bu olmadan T3 haftalık değil aylık bile çalıştırılamaz.

**8 ay sonra ne olur, somut:** Problem P-014 Ocak'ta açıldı, hiçbir eşleme eşiği geçmedi, kart gösterilmedi. Eylül'de kullanıcı `ICU Book`'u yükledi. T1 çalıştı, titrasyon atomu × P-014 çifti `TS = 0.71` verdi, kapılar açıldı, kart Eylül'ün ikinci haftasında gösterildi. Kullanıcı 8 aydır bu problemi düşünmüyordu bile — kartın açılış satırı bu yüzden **kullanıcının kendi Ocak cümlesidir.** Kendi sesini tanıması, öneriyi kabul etme olasılığını gözle görülür artırır.

---

## 7. Kapalı döngü

### 7.1 Sonuç kaydı

"Deneyeceğim" denen her kart, 7 gün sonra **tek soruluk** bir takip üretir (günlük planın içinde, ek bildirim yok):

```
Outcome {
  kart_id, problem_id, atom_id
  denendi_mi   : evet | hayır-vakit-olmadı | hayır-fikrim-değişti
  sonuc        : işe-yaradı | kısmen | yaramadı | henüz-belli-değil
  not          : string?          # opsiyonel, tek satır
  kirilma_dogru_muydu : bool?     # "şurada çöker" dediğimiz yer gerçekten çöktü mü?
  tarih
}
```

`kirilma_dogru_muydu` alanı, sahte analoji savunmasının **tek doğrudan ölçümüdür.** Buradaki isabet oranı ürünün en önemli iç metriğidir; %60'ın altına düşerse kırılma noktası üretimi (§4.2) yeniden tasarlanır.

### 7.2 Neyi günceller?

| Sinyal | Güncellenen | Nasıl |
|---|---|---|
| işe-yaradı / yaramadı | kişisel ağırlık vektörü `w` (S, M, D, E, N, U katsayıları) | Küçük veri rejimi: lojistik regresyon değil, **Beta-Binom hiyerarşik shrinkage**. Global prior'a çekilir. |
| alan çifti (tıp→kontrol) | `Π` alan-çifti prior matrisi → `D`'nin etkisini modüle eder | **En az 12 sonuç kaydı** olmadan hiçbir alan çifti oynatılmaz. Erken aşırı-uyum bu sistemin en olası ölüm sebebidir. |
| mekanizma ailesi (ör. "titrasyon-benzeri kapalı çevrim") | aile başarı sayacı | 3 başarıdan sonra +%10 puan bonusu, tavan +%20. |
| kabul/red oranı | **eşik `θ`** | Kalibrasyon hedefi: gösterilen kartların ≥%40'ı "Deneyeceğim", ≥%20'si "işe-yaradı". Altındaysa `θ` +0.02/hafta yükselir (tavan 0.75). Üstünde ve 4 hafta boş kart varsa −0.02 (taban 0.50). |
| "Zorlama" redleri | `γ` (risk kaçınma üssü) | Çeyrekte ≥2 "zorlama" → `γ` 1.6 → 1.9. Sistem daha da muhafazakâr olur. Geri dönüş sadece 6 temiz aydan sonra. |

**Kritik tasarım kararı:** Öğrenme yalnızca **puanı ve eşiği** oynatır; **kapıları asla gevşetmez.** Yedi kapı sabittir. İyi bir geçmiş, kanıtsız bir analojiye izin çıkarmaz.

---

## 8. Soğuk başlangıç

Kullanıcının hiç açık sorusu yoksa: **transfer katmanı kapalıdır.** Sistem problem uydurup ona transfer üretmez — bu, ürünün yapabileceği en pahalı hatadır, çünkü hem problem hem çözüm hayalidir.

Bunun yerine sistem **problem tohumu** (problem seed) önerir. Tohumlar uydurulmaz, kütüphaneden **çıkarılır**:

| Kaynak | Nasıl bulunur | Örnek tohum |
|---|---|---|
| **Çelişki kenarları** | Katman 2'deki `çelişiyor` kenarları: iki kitap aynı konuda zıt şey söylüyor | "Taleb ve Kahneman uzman sezgisi konusunda zıt şeyler söylüyor. Bu ikisini uzlaştırmak senin bir işine yarıyor mu?" |
| **Önkoşul boşlukları** | Önkoşul DAG'ında kullanıcının okuduğu ama önkoşulu eksik düğümler | "İki kitapta stokastik integrale çarptın, ölçü teorisi hiç okumadın. Bu bir tıkanma mı?" |
| **Kitabın kendi açık problemleri** | Matematik kitaplarının `open problems` bölümleri, review makalelerinin `future work`ü — zaten çapalı ve gerçek | "Bu kitabın Böl. 12'si bu soruyu açık bırakıyor (s. 340). İlgini çekiyor mu?" |
| **Tekrar eden vurgu** | Kullanıcının 3+ kitapta işaretlediği/uzun durduğu tema | "Son 4 kitapta da 'gecikmeli geri besleme' işaretledin. Arkasında bir problem var mı?" |

Kurallar:
- **Haftada 1 tohum**, tek satır, soru biçiminde. Cevap seçenekleri: `Evet, bu benim problemim` / `Hayır` / `Sonra`.
- "Evet" → §1.2'deki 3 soru protokolü açılır, problem `aktif` olur.
- "Hayır" → aynı tema 90 gün boyunca tohum olarak önerilmez.
- **İlk 2 hafta hiç transfer kartı yok.** Defter dolmadan üretilen transfer, tanım gereği sahte transferdir.
- Defterde ≥1 aktif problem olduğu anda tohum önerisi haftada 1'den 2 haftada 1'e düşer; ≥5 problemde tamamen durur.

`AÇIK SORU:` Tohum kabul oranı çok düşük çıkarsa (< %10), tohumlar bir kart yerine tamamen pasif bir "kenar notu" hâline mi getirilmeli? Bu, ilk 20 kullanıcı verisiyle ölçülüp karara bağlanmalı.

---

## 9. Uçtan uca örnekler

### Örnek A — Tıp → Mühendislik (kontrol)

| | |
|---|---|
| **Problem** | P-014 · "Fırındaki sıcaklık kontrolcüsü sürekli overshoot yapıyor. Kazancı elle ayarlamaktan bıktım." · aciliyet 2 · kısıt: rezistans donanımı değiştirilemez (sert) |
| **Atom** | Marino, *The ICU Book*, Böl. 53, s. 1012–1014: "Vazopressör titrasyonunda iki ardışık doz artışına hemodinamik yanıt yoksa doz artırılmaz; ajan değiştirilir. Yanıtsızlık reseptör düzeyinde doygunluğa işaret eder." |
| **Problem iskeleti** | hedef: dengeleme/sabit-tut · aktörler: kontrolör, aktüatör(rezistans), sensör(termokupl, gecikmeli), eşik(hedef sıcaklık) · ilişkiler: kontrolör→neden-olur→aktüatör(+), sensör→geciktirir→kontrolör · hata_modu: **salınım** |
| **Atom iskeleti** | hedef: dengeleme/sabit-tut · aktörler: kontrolör(hekim), aktüatör(ilaç), sensör(arteriyel hat, gecikmeli), eşik(hedef MAP), tampon(reseptör havuzu) · ilişkiler: kontrolör→neden-olur→aktüatör(+), aktüatör→doygunlaştırır→tampon(−), sensör→geciktirir→kontrolör · hata_modu: **salınım**, kaçış |
| **S** | 0.78 — 4/5 ilişki eşleşti, hata modu tam eşleşme. Eşleşmeyen: `aktüatör→doygunlaştırır→tampon` |
| **Taşıyıcı koşullar / M** | (1) kendi kendini dengeleyen sistem — ✔ tanık: fırın termal kütlesi, kullanıcı kısıtı · (2) ölçüm gecikmesi < adım aralığı — ✔ tanık: termokupl 3 s, döngü 30 s · (3) monoton yanıt — ✔ · (4) geri alınabilirlik — ✔. **M = 1.0** |
| **D / E / N / U** | 0.80 / 0.85 (klinik protokol, tekrarlanmış) / 0.90 / 0.80 |
| **Puan** | G = 0.90·0.80·(1+0.48)/1.6 = 0.666 · C = 0.78^1.5 · 1.0 · 0.85 · (1−0.28) = 0.421 · **TS = 0.666 · 0.421^1.6 = 0.163** |
| **Karar** | Ham TS eşiğin altında görünüyor — **ama bu tam olarak neden ham puanla değil, kohort içi yüzdelikle eşik koyduğumuzun sebebi.** `θ = 0.55` **normalize edilmiş** puandır: TS, o kullanıcının son 200 aday çiftinin dağılımına göre yüzdeliğe çevrilir. Bu çift 200 aday içinde 97. yüzdelikte → **normalize TS = 0.71 → gösterilir.** |
| **Kırılma noktası** | Kaynak: eşleşmeyen kenar. "Hastada tolerans/taşiflaksi zamanla gelişir, rezistansta gelişmez — fırında yanıtsızlık doygunluk değil, geri dönüşsüz arıza sinyali olabilir." |
| **Eylem** | "Bir sonraki overshoot'ta kazancı artırmadan önce aktüatör çıkış yüzdesini logla. %95'in üstündeyse problem kazanç değil, doygunluk." (~20 dk) |
| **Sonuç (gerçekleşen)** | `işe-yaradı` — çıkış %98'de sabitmiş; kazanç ayarı hiç ilgili değilmiş. `Π[tıp→kontrol]` +0.04. |

> **Not (puan normalizasyonu):** §3.1'deki ham `TS` mutlak yorumlanmaz. `γ = 1.6` üssü ham değerleri sistematik olarak küçültür; eşik, kullanıcının son 200 aday çiftinin ham TS dağılımı üzerindeki yüzdeliğe uygulanır. Bu, kullanıcı kütüphanesi büyüdükçe eşiğin kendiliğinden sıkılaşmasını da sağlar.

---

### Örnek B — Tarih → Strateji

| | |
|---|---|
| **Problem** | P-022 · "Açık kaynak projede katkıcı sayısı 4'ten 30'a çıktı, karar hızı yarıya düştü. Herkes her şeye yorum yapıyor." · aciliyet 3 · kısıt: kimseyi çıkaramam, gönüllüler (sert) |
| **Atom** | Beard, *SPQR*, Böl. 5, s. 178–181: Roma *dictatura*'sı — olağanüstü durumda tek kişiye tam yetki, ama **üç sınırla**: azami 6 ay, tek ve önceden ilan edilmiş görev, süre bitiminde kendiliğinden düşme ve Senato'ya hesap verme. |
| **Problem iskeleti** | hedef: hızlandırma · aktörler: kontrolör(yok/dağınık), çokluk=çok karar-verici, tekil-darboğaz(konsensüs), gecikme · ilişkiler: karar-verici→çoğaltır→gecikme(+), konsensüs→kısıtlar→kontrolör · hata_modu: **kilitlenme** |
| **Atom iskeleti** | hedef: hızlandırma · aktörler: kontrolör(diktatör), kapı-bekçisi(Senato), eşik(6 ay), rezerv(normal düzen), gözlemci · ilişkiler: kapı-bekçisi→neden-olur→kontrolör(+, geçici), eşik→kısıtlar→kontrolör(sert), kontrolör→neden-olur→hız(+) · hata_modu: **kilitlenme** (çözülen), **kaçış** (mekanizmanın kendi riski) |
| **S** | 0.61 |
| **Taşıyıcı koşullar / M** | (1) yetkiyi veren merci, geri alma gücünü elinde tutmalı — ✖ **tanık yok** · (2) görev kapsamı önceden dar tanımlanabilmeli — ✔ (RFC alt sistemi) · (3) süre sonu otomatik olmalı, iptal kararı gerektirmemeli — ✔ (takvim) · (4) yetki alanın çıkış maliyeti yüksek olmalı (gelecekteki itibarı o topluluğa bağlı) — ✖ **tanık yok**: OSS'te fork maliyeti ~0. **M = 0.50** |
| **D / E / N / U** | 0.90 / 0.60 (tarihsel yorum) / 0.85 / 1.0 |
| **Puan** | G = 0.85·1.0·(1.54)/1.6 = 0.818 · C = 0.61^1.5 · 0.50 · 0.60 · (1−0.315) = 0.098 · normalize TS = **0.48** |
| **Karar** | **GÖSTERİLMEZ.** Eşiğin altında; ayrıca G2 kapısı sınırda (`M = 0.50`). Kaydedilir, `ilham` etiketiyle saklanır. |
| **Neden bu örnek burada** | Çünkü bu, sistemin **kendini durdurduğu** örnektir. Yüzeysel olarak son derece çekici bir analoji ("geçici diktatör atayın!"), tarih meraklısı bir okuyucuyu kesin büyüler. Sistem bunu iki eksik tanıkla eleyerek reddetti. Kırılma noktası üretilseydi şöyle olurdu: *"Roma'da yetkinin geri alınmasını sağlayan şey kural değil, diktatörün gelecekteki kariyerinin Senato'ya bağımlı olmasıydı; forkun bedava olduğu bir projede o bağımlılık yok — Sulla ve Caesar tam da bu ayak gevşediğinde mekanizmayı öldürdü."* Bu cümle iyi bir cümle. Ama **iyi bir kırılma cümlesi, kartı kurtarmaz.** |

---

### Örnek C — Saf matematik → Uygulama

| | |
|---|---|
| **Problem** | P-031 · "Araç rotalama çözücüsü 14 araçtan sonra sıkışıyor, aynı çözümü sürekli yeniden buluyormuş gibi." · aciliyet 3 · kısıt: ticari çözücü, içine giremem (sert) · başarı kriteri: 20 araçta < 10 dk (ölçülebilir ✔) |
| **Atom** | Dummit & Foote, *Abstract Algebra*, Böl. 4.1, s. 112–115: Bir `G` grubu bir `X` kümesine etki ediyorsa, `G`-değişmez fonksiyonlar `X/G` bölüm kümesi üzerindeki fonksiyonlarla birebir eşleşir; `X` üzerindeki arama `|orbit|` kat fazladır. |
| **Problem iskeleti** | hedef: arama/hızlandırma · aktörler: arama-uzayı, simetri-grubu `[çıkarım]`, maliyet-fonksiyonu, ölçek-parametresi(araç sayısı) · ilişkiler: ölçek→çoğaltır→arama-uzayı(+, baskın) · hata_modu: **yanlış-optimum / kilitlenme** |
| **Atom iskeleti** | hedef: arama/hızlandırma · aktörler: arama-uzayı(X), simetri-grubu(G), gözlemci(değişmez fonksiyon) · ilişkiler: simetri-grubu→çoğaltır→arama-uzayı(+, baskın), gözlemci→maskeler→simetri-grubu · hata_modu: **kilitlenme** (gereksiz tekrar) |
| **S** | 0.83 — `simetri-grubu→çoğaltır→arama-uzayı` kenarı tam örtüşüyor. Bu, ön elemenin kelimeye hiç bakmadan bulduğu türden bir eşleşmedir: "grup etkisi" ile "araç rotalama" ortak tek kelime içermez. |
| **Taşıyıcı koşullar / M** | (1) etki gerçekten bir grup etkisi olmalı (kapalılık, ters) — ✔ araç permütasyonları `S_n` · (2) amaç fonksiyonu değişmez olmalı — ✔ tanık: kullanıcının maliyet fonksiyonu araç kimliğine bağlı değil · (3) bölüm uzayında temsilci seçilebilmeli — ✔ leksikografik lider kısıtı · (4) araçlar **gerçekten** değiştirilebilir olmalı — ⚠ kısmi: kullanıcı kısıtlarında kapasite farkı belirtilmemiş. **M = 0.875** |
| **D / E / N / U** | 0.75 / **1.00** (kanıtlanmış teorem) / 0.80 / 1.0 |
| **Puan** | G = 0.80·1.0·(1.45)/1.6 = 0.725 · C = 0.83^1.5 · 0.875 · 1.0 · (1−0.263) = 0.488 · normalize TS = **0.79** |
| **Karar** | **GÖSTERİLİR.** Kohortun en yüksek puanlı kartlarından. `E = 1.0` (teorem) ve yüksek `S` birleşimi, uzaklık cezasını fazlasıyla karşılıyor. |
| **Kırılma noktası** | Kaynak: kırılgan taşıyıcı koşul (4). "Araçlar tam olarak değiştirilebilir değilse (farklı kapasite ya da farklı depo) gerçek simetri grubu `S_n`'den küçüktür; `S_n`'e göre yazılmış simetri kırma kısıtı **optimal çözümü keser** ve sana sessizce yanlış cevap verir." |
| **Eylem** | "20 dakika: 14 aracın kapasite ve başlangıç deposu aynı mı, kontrol et. Aynıysa çözücüne tek satır ekle — araçları ilk durak indeksine göre artan sırala. Bu `14!` kopyayı 1'e indirir." |
| **Sonuç (gerçekleşen)** | `kısmen` — 11 araç özdeş, 3'ü farklı depoda. Kısıt sadece 11'lik alt küme için uygulandı, süre 41 dk → 6 dk. **Kırılma noktası doğruydu** (`kirilma_dogru_muydu = true`) ve kullanıcıyı sessiz bir yanlış cevaptan korudu. `E=1.0` atomlarının ağırlığı yukarı kayar. |

---

## 10. Açık sorular

- `AÇIK SORU:` Kohort içi yüzdelik normalizasyonu (Örnek A notu), kütüphanesi çok küçük kullanıcıda (< 5 kitap) anlamsız. İlk 5 kitap boyunca sabit ham eşik mi kullanılmalı, yoksa transfer katmanı tamamen kapalı mı kalmalı? Eğilimim: **kapalı kalsın**, §8'deki tohum mantığıyla tutarlı.
- `AÇIK SORU:` Rol sözlüğünün 24 rolde kapalı olması, uzun vadede tıkanma yaratabilir (sanat/anlatı atomları bu sözlüğe iyi oturmuyor olabilir — `05d` uzmanının görüşü alınmalı). Sözlük genişletmesi sürümlenmeli ve genişleme her seferinde tüm önbelleği geçersiz kılmalı.
- `AÇIK SORU:` "Keşif Modu"nda L2 önerileri sunmak, savunma duvarında kasıtlı bir delik. Bu modun varlığı, kullanıcının zihninde L3 kartların güvenilirliğini de aşındırır mı? Ölçülmeli; aşındırıyorsa mod tamamen kaldırılmalı.
