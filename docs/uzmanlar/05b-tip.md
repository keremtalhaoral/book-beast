# 05b — Ampirik & Kanıt Temelli Kitaplar

> **Uzman:** Kanıta Dayalı Tıp Araştırmacısı
> **Kapsam:** tıp, biyoloji, beslenme, psikoloji, kişisel gelişim, popüler bilim
> **Bağımlılık:** `00-ORTAK-BRIFING.md` (4 kural), `01-bilgi-modeli.md` (atom şeması), `07-transfer.md` (transfer)

---

## 3 cümlelik özet

1. Ampirik kitaplardaki her iddia, düz bir "atom" değil, **PICO + etki büyüklüğü + kanıt seviyesi** taşıyan genişletilmiş bir atomdur; bu alanlar metinden çıkarılamıyorsa alan boş bırakılmaz, `[bildirilmemiş]` diye işaretlenir ve bu işaretin kendisi bir sinyaldir.
2. Sistem hiçbir iddiayı silmez veya reddetmez (Kural 3) — bunun yerine her iddiaya **kanıt gücü rozeti** ve gerekiyorsa **sahte bilim sinyal listesi** iliştirir; kullanıcı iddiayı görür, ne kadar dayandığını da görür.
3. Sistem **tıbbi tavsiye vermez**: "kitap X diyor, sayfa Y, kanıt seviyesi Z" der, "sen şunu yap" asla demez — bu sınır arayüzde donanımsal (hard-coded) bir kapıdır, model kararına bırakılmaz.

---

## 1. Ampirik atom şeması

Ortak atom şemasının (`01-bilgi-modeli.md`) `type: empirical_claim` uzantısı. Ampirik atom, normal iddia atomunun üstüne **13 alan** ekler.

### 1.1 Alanlar

| # | Alan | Tip | Zorunlu | Not |
|---|------|-----|---------|-----|
| 1 | `claim` | metin | ✔ | Tek cümle, yönlü ("X, Y'yi azaltır"). Nötr betimleme değil. |
| 2 | `population` (P) | metin + kod | ✔ | "45–70 yaş, tip-2 diyabetli erişkin". Belirtilmemişse `[bildirilmemiş]`. |
| 3 | `intervention` (I) | metin | ✔ | Müdahale/maruziyet. Doz ve süre varsa buraya. |
| 4 | `comparator` (C) | metin | ✔ | Plasebo / standart bakım / hiç / başka doz. **En sık eksik alan.** |
| 5 | `outcome` (O) | metin | ✔ | Ölçülen sonuç. **Vekil mi gerçek mi** ayrımı zorunlu (`outcome_kind`). |
| 6 | `outcome_kind` | enum | ✔ | `hard` (ölüm, kırık, MI) · `surrogate` (LDL, HbA1c, kortizol) · `self_report` (anket, günlük) |
| 7 | `effect_size` | yapı | — | `{value, unit, kind}`; kind ∈ {RR, OR, HR, mean_diff, Cohen_d, %change} |
| 8 | `confidence_interval` | yapı | — | `{low, high, level: 0.95}`. Yoksa `p_value` kabul edilir ama zayıf sayılır. |
| 9 | `sample_size` | tamsayı | — | `n`. Kollara ayrıysa `{arm_a, arm_b}`. |
| 10 | `study_design` | enum | ✔ | §2.1 tablosu. Metinde yoksa `unstated`. |
| 11 | `publication_year` | yıl | — | Çalışmanın yılı; kitabın yılı ayrı alan (`book_year`). |
| 12 | `evidence_level` | enum | ✔ | L1–L6, §2. **Türetilmiş alan**, model doğrudan yazmaz. |
| 13 | `warning_flags` | liste | ✔ | §3 sinyalleri. Boş liste geçerli bir değerdir. |

Ek olarak her ampirik atom ortak alanları taşır: `book_id`, `chapter`, `page_anchor` (Kural 2 — çapasız üretim yasak), `quote` (kitaptan birebir alıntı, ≤2 cümle).

### 1.2 Kaynak zinciri alanı

```
citation_chain:
  book_says:      "kitabın verdiği kaynak metni, birebir"
  resolved:       true | false | not_attempted
  identifier:     DOI / PMID / null
  resolution_note: "kitap 'Harvard çalışması' diyor, tanımlayıcı yok"
```

`resolved: false` **hata değil**, veridir: kitabın kaynak disiplininin ölçüsüdür. Kitap düzeyinde `unresolvable_citation_ratio` metriği bundan hesaplanır ve kitap kartında görünür.

### 1.3 Karar: PICO zorlanır, uydurulmaz

Model P/I/C/O alanlarını **metinden çıkarmakla** yükümlü; çıkaramadığında `[bildirilmemiş]` yazar. Uydurma kesinlikle yasak — çünkü eksik komparatör (C) bilgisinin kendisi, en güçlü sahte bilim sinyallerinden biridir (§3.1-S4) ve doldurulursa sinyal kaybolur.

---

## 2. Kanıt hiyerarşisi

### 2.1 Seviyeler

| Seviye | Rozet | Tasarım | Metindeki tipik ipuçları |
|--------|-------|---------|--------------------------|
| **L1** | Sağlam | Sistematik derleme / meta-analiz | "meta-analiz", "N çalışmanın derlemesi", "Cochrane" |
| **L2** | Güçlü | Randomize kontrollü çalışma (RKÇ) | "randomize", "çift kör", "plasebo kontrollü", "denekler rastgele atandı" |
| **L3** | Orta | Kohort / vaka-kontrol / prospektif gözlem | "N kişi K yıl izlendi", "takip çalışması", "ilişkilendirildi" |
| **L4** | Zayıf | Kesitsel, vaka serisi, hayvan, in vitro | "farelerde", "hücre kültüründe", "N hastada gözlendi", "anket" |
| **L5** | Görüş | Uzman görüşü, mekanizma temelli akıl yürütme | "bilindiği gibi", "fizyolojik olarak makul", "klinik deneyimim" |
| **L6** | Anekdot | Tek hasta hikâyesi, yazarın kendi deneyimi | "hastam Ayşe", "kendi üzerimde denedim", "bir okurum yazdı" |

### 2.2 Atama algoritması (sözde-kod)

```
evidence_level(atom):
    L = null

    # 1) Tasarım kelimeleri — en yüksek eşleşme kazanır
    L = tasarim_sozlugu_esles(atom.quote + atom.context_window)

    # 2) Sayısal kanıt yoksa tavan uygula
    if atom.effect_size == null and atom.sample_size == null:
        L = max(L, L4)          # sayı yoksa L3'ün üstüne çıkamaz

    # 3) Hayvan / in vitro tespiti insana genelleme varsa
    if hayvan_veya_hucre(atom) and atom.population insana_isaret_ediyor:
        L = L4;  flag(S3)

    # 4) Hiç kaynak yok
    if atom.citation_chain.book_says == null:
        L = L5 if mekanizma_dili(atom) else L6

    return L
```

**Karar: model seviye atamaz, sinyal üretir.** LLM'in görevi tasarım kelimelerini ve sayıları çıkarmak; seviye bu deterministik kuralla hesaplanır. Sebep: aynı paragrafın iki farklı çağrıda L2/L4 alması kullanıcı güvenini bitirir; kural tabanlı atama tekrarlanabilir.

### 2.3 Kitap kaynak vermiyorsa

Popüler kişisel gelişim kitaplarının çoğu bu durumda. Politika:

1. Atom **yine üretilir** (Kural 3 — reddetme yok).
2. `evidence_level = L5` (mekanizma/otorite dili) veya `L6` (anekdot).
3. `warning_flags` içine `S6: kaynaksız` girer.
4. Arayüzde iddia **soluk gri gövde + turuncu rozet** ile görünür; okunabilir, ama görsel olarak diğerlerinden ayrılır.
5. **Yine de transfer katmanına girer** — kaynaksız bir fikir kötü kanıttır ama iyi bir *hipotez* olabilir; `07-transfer.md` bunları `hypothesis_only` etiketiyle alır.

> Not: Kitap kaynak veriyor ama kaynak çözülemiyorsa (dipnotsuz "araştırmalar gösteriyor ki") bu L5 değil, **L4-tavanlı belirsiz** sayılır ve `S6` yerine `S7: izlenemez kaynak` bayrağı alır.

---

## 3. ⚠️ Sahte bilim filtresi

Bu bölüm **sansür değil, etiketleme** tasarlar. Sistem hiçbir iddiayı gizlemez, kısaltmaz veya "bu yanlış" demez. Sadece iddianın yapısal zayıflıklarını görünür kılar.

### 3.1 Sinyal listesi

| Kod | Sinyal | Tetikleyici desen | Ağırlık |
|-----|--------|-------------------|---------|
| **S1** | Tek çalışmaya dayanma | Bölüm boyunca tek bir çalışma adı, "çığır açan araştırma" | 2 |
| **S2** | Mekanizmadan sonuca atlama | "X, Y reseptörünü uyarır **bu yüzden** kilo verirsin" — ara sonuç ölçümü yok | 3 |
| **S3** | Hayvan → insan genellemesi | Fare/sıçan/hücre çalışması + insan tavsiyesi aynı paragrafta | 3 |
| **S4** | Komparatörsüz iddia | `comparator == [bildirilmemiş]` + kesin dil | 2 |
| **S5** | Korelasyondan nedensellik | Kohort verisi + "neden olur / sağlar / yol açar" fiili | 3 |
| **S6** | Kaynaksız kesinlik | Kaynak yok + "kanıtlanmıştır / bilim gösterdi ki" | 2 |
| **S7** | İzlenemez kaynak | "araştırmalar gösteriyor" + tanımlayıcı yok | 1 |
| **S8** | Mucize dili | "devrim", "her şeyi değiştirir", "%100", "tek çözüm", "doktorların söylemediği" | 2 |
| **S9** | Karşıt kanıtın yokluğu | Bölümde tek bir "ancak / bir başka çalışma / sınırlılık" cümlesi yok | 2 |
| **S10** | Vekil sonucun gerçek gibi sunulması | `outcome_kind == surrogate` + iddia sert sonuç dilinde ("kalp krizini önler") | 3 |
| **S11** | Etki büyüklüğü yok, sadece p | `effect_size == null` + "istatistiksel olarak anlamlı" | 1 |
| **S12** | Çıkar çatışması | Yazar aynı bölümde ürün/klinik/program satıyor | 2 |
| **S13** | Ölçeksiz sayı | Yüzde var, mutlak risk yok ("riski %50 azaltır" — 2/1000 → 1/1000) | 2 |
| **S14** | Otorite ile ikame | Kanıt yerine kurum/unvan adı ("Stanford'da öğretilir") | 1 |

### 3.2 Toplam skor → görsel sınıf

```
skor = Σ ağırlık(tetiklenen sinyaller)

skor 0        → rozet yok
skor 1–3      → "dikkat"    (sarı nokta)
skor 4–6      → "zayıf"     (turuncu rozet)
skor 7+       → "çok zayıf" (kırmızı rozet + zorunlu açılır liste)
```

Skor **atom düzeyinde** hesaplanır, ama kitap kartında **ortalaması** gösterilir: "Bu kitabın 214 iddiasının 61'i zayıf kanıtlı."

### 3.3 Etiketleme dili — sözlük

Bu ürünün sesi budur; **kelimeler sabittir**, model doğaçlama yapmaz.

**KULLANILACAK ifadeler** (yapısal, faili iddia olan):

| Sinyal | Görünen metin |
|--------|---------------|
| S1 | "Tek çalışmaya dayanıyor." |
| S2 | "Mekanizma anlatılmış, sonuç ölçülmemiş." |
| S3 | "Bulgu hayvan çalışmasından; insana genelleme kitabın yorumu." |
| S4 | "Neye kıyasla olduğu belirtilmemiş." |
| S5 | "Veri ilişki gösteriyor; cümle neden-sonuç kuruyor." |
| S6 | "Kaynak verilmemiş." |
| S9 | "Bölümde karşıt bulgu yer almıyor." |
| S10 | "Ölçülen ara gösterge (LDL); iddia sert sonuç (kalp krizi)." |
| S13 | "Göreli azalma verilmiş; mutlak risk verilmemiş." |

**YASAK ifadeler:**

- ✗ "Bu yanlış." / "Bu doğru değil." — sistem hakikat hakemi değil
- ✗ "Bilim dışı", "sahte bilim", "şarlatanlık" — yargı değil, yapı
- ✗ "Bu bölümü okuma" — Kural 3 ihlali
- ✗ "Ancak modern araştırmalar…" — sistemin kendi kanıt getirmesi; kaynak zinciri kopar (Kural 2)

**Ton kuralı:** etiket **iddiayı değil, iddianın dayanağını** tanımlar. Cümlenin öznesi hep kanıttır, yazar değil. "Yazar abartıyor" değil; "kanıt tek çalışma".

### 3.4 Neden sansür yok — gerekçe

Kişisel gelişim kitabındaki zayıf kanıtlı bir iddia yanlış olabilir ama **hipotez olarak değerli** olabilir; kullanıcı mühendis, hipotezi kendi alanında test edebilir. Sistemin işi kullanıcının yerine karar vermek değil, **karar için gereken metaveriyi bedava vermek**. Sansür ürünü bir filtreye indirir; etiketleme onu bir enstrümana çevirir.

---

## 4. Tekrarlanabilirlik krizi

### 4.1 Problem

2011 sonrası psikoloji ve beslenmede çok sayıda ünlü bulgu çöktü: ego tükenmesi (ego depletion), güç duruşu (power posing), hazırlama etkileri (social priming), yağ-kalp hipotezinin katı biçimi, mikrobiyom-tek çözüm anlatıları. 2008–2014 arası yazılmış popüler kitaplar bu bulguları **kesin gerçek** olarak aktarır.

### 4.2 Mekanizma: `replication_risk` alanı

Ampirik atoma **türetilmiş** bir alan daha eklenir:

```
replication_risk ∈ {low, moderate, high, known_failed}
```

Üç girdiden hesaplanır:

**(a) Alan güvenilirlik katsayısı** — sabit tablo, elle bakımlı:

| Alan | Katsayı | Gerekçe |
|------|---------|---------|
| Sosyal/hazırlama psikolojisi (social priming) | 0.35 | Tekrarlama oranı en düşük küme |
| Beslenme epidemiyolojisi | 0.40 | Gözlemsel + beyan edilen diyet kaydı |
| Genel deneysel psikoloji | 0.55 | RP:P ~%39 tekrarlama |
| Davranışsal ekonomi | 0.60 | Karışık |
| Klinik ilaç RKÇ | 0.80 | Ön kayıt (preregistration) yaygın |
| Fizyoloji / biyokimya (mekanizma) | 0.75 | Ölçüm sağlam, genelleme zayıf |

**(b) Yayın tarihi penceresi:**

```
if 1990 <= çalışma_yılı <= 2011 and alan ∈ {psikoloji, beslenme}:
    risk += 1 kademe          # "kriz öncesi" pencere
if çalışma_yılı >= 2016 and ön_kayıt_belirtisi:
    risk -= 1 kademe
```

**(c) İsim listesi (known-failed registry)** — proje içinde bakımlı, ~150 satırlık JSON: bulgu adı → durum → tekrarlama denemesi referansı. Ego tükenmesi, güç duruşu, Macbeth etkisi, kalem-ağızda gülümseme, glikoz-irade, çikolata-kilo (kasıtlı sahte çalışma), yaşlılık-hazırlama.

### 4.3 Örnek: 2010 kitabında "ego tükenmesi"

Sistem şunu yapar:

```
atom.claim              = "İrade sınırlı bir kaynaktır; kullandıkça tükenir."
atom.book_year          = 2010
atom.study_design       = RKÇ (laboratuvar)
atom.evidence_level     = L2      ← kitabın anlattığı tasarım gerçekten RKÇ
atom.replication_risk   = known_failed
atom.registry_note      = "2016 çok-merkezli tekrarlama (23 laboratuvar, n≈2141)
                           etkiyi bulamadı. Tartışma sürüyor."
```

Arayüzde iddia **çizilmez, silinmez**. Altına tek satır düşer:

> ⟳ **Sonradan tartışmalı hale geldi.** Kitap 2010; bu bulgunun büyük ölçekli tekrarlaması 2016'da başarısız oldu. Kitabın argümanı bu bulguya dayanıyorsa, argümanın kendisi de tartışmalıdır.

Son cümle önemli: sistem **etkinin yayılımını** işaretler — o bölümdeki diğer atomlar `depends_on` kenarıyla bu atoma bağlıysa hepsi ⟳ devralır (`02-yenilik-ve-graf.md` graf kenarları üzerinden yayılım).

### 4.4 Karar: tarih tek başına suç değil

Eski = yanlış değil. `replication_risk` yalnızca **alan katsayısı düşükse** tarihe bakar. 1985 tarihli bir farmakokinetik bulgusu için tarih penceresi çalışmaz; 2009 tarihli bir hazırlama etkisi için çalışır.

**AÇIK SORU:** Alan katsayısı tablosu ve known-failed listesi bakım yükü yaratır. Yılda bir elle güncelleme mi, yoksa kullanıcı bildirimi (crowd flag) mı? İlk sürümde elle, ~150 kayıtla başlanması öneriliyor.

---

## 5. 🚨 GÜVENLİK SINIRI — tıbbi tavsiye yasağı

**Bu bölüm belgenin zorunlu parçasıdır ve diğer bölümlerin hepsini geçersiz kılar.**

### 5.1 Tek cümlelik politika

> BookBeast **kitapların ne dediğini kaynağıyla aktarır**; kullanıcının bedeni, ilacı, dozu veya belirtisi hakkında **hiçbir öneride bulunmaz**.

### 5.2 Sistem NE YAPAR

- Kitaptaki iddiayı birebir, sayfa çapasıyla aktarır.
- Kanıt seviyesini, örneklem büyüklüğünü, etki büyüklüğünü gösterir.
- İki kitabın çelişkisini gösterir (§6).
- "Bu iddia hangi popülasyonda ölçüldü" sorusunu cevaplar.
- Kullanıcının kendi notunu iddianın yanına kaydetmesine izin verir.
- Kullanıcıya **doktoruna sorabileceği soruları** üretir — bu tavsiye değil, okuma çıktısıdır:
  > "Kitap 45–70 yaş tip-2 diyabetlilerde ölçmüş. Doktoruna sorulabilir: bu popülasyon benim durumumu kapsıyor mu?"

### 5.3 Sistem NE YAPMAZ (mutlak)

- ✗ Doz, ilaç, takviye, diyet **önermez** ("günde 2g al" — asla)
- ✗ Kullanıcının belirtilerini **yorumlamaz** ("bu muhtemelen X")
- ✗ İlaç bırakma/başlama/değiştirme hakkında **konuşmaz**
- ✗ "Sana uygun" / "senin durumunda" ifadelerini **kurmaz**
- ✗ Acil durum triyajı **yapmaz**
- ✗ Kitabın tavsiyesini **kendi sesiyle tekrarlamaz** — sadece alıntılar ve kaynağını gösterir

### 5.4 Tetikleme kapısı (hard gate)

Bu bir model istemi (prompt) değil, **kod kapısıdır**. Kullanıcı girdisi transfer/soru katmanına gitmeden önce sınıflandırıcıdan geçer:

```
personal_medical_intent(girdi):
    birinci_sahis  = /\b(ben|bende|bana|kendime|benim)\b/
    tibbi_nesne    = ilaç_adı | belirti_sözlüğü | doz_deseni | tanı_adı
    eylem_fiili    = /\b(alay[ıi]m|kullanay[ıi]m|b[ıi]rakay[ıi]m|uygulay[ıi]m|yapay[ıi]m)\b/

    if (birinci_sahis AND tibbi_nesne) OR (tibbi_nesne AND eylem_fiili):
        return true
```

Eşleşme → **normal cevap üretimi iptal**, yerine sabit yanıt bileşeni:

> **Bu soruya cevap veremem — ve vermemeliyim.**
> BookBeast bir kitap okuma aracı; klinik danışman değil. Senin durumunu bilmiyorum
> ve bilebilecek durumda değilim.
>
> Yapabileceğim şey şu: **kitabın ne dediğini** göstermek.
>
> [ Kitabın bu konudaki 4 iddiasını göster ]   [ Doktora sorulacak soruları çıkar ]

Kritik: kapı **sistem cevabını değil, üretimi** durdurur. Model önce cevabı yazıp sonra "ama tavsiye değildir" eklemez — o cevap hiç üretilmez.

### 5.5 Arayüzde görünüm

| Yer | Görünüm |
|-----|---------|
| Kitap yüklenirken tür `tıp/sağlık/beslenme` tespit edilirse | Tek satır, kapatılamaz üst bant: **"Bu kitap sağlıkla ilgili. BookBeast kitabı aktarır, tavsiye vermez."** |
| Her ampirik atom kartının alt kenarı | 11px gri: `bilgi · tavsiye değil` |
| Sağlık kitabından üretilen günlük plan satırı | Eylem fiili **okuma fiili** olmak zorunda: "Bölüm 6'yı oku" ✔ · "Magnezyum dene" ✗ — plan üreticide fiil beyaz listesi var |
| Kapı tetiklendiğinde | §5.4 bileşeni, tam genişlik, kırmızı sol kenar |
| Ayarlar | "Sağlık içeriği uyarıları" — **kapatılamaz**, sadece görünür |

**Karar: uyarı bandı kapatılamaz.** Kapatılabilir uyarı yok hükmündedir; ürün burada estetiği güvenliğe feda eder.

### 5.6 Kural 3 ile çelişki var mı?

Hayır. Kural 3 "sistem kitabı reddetmez" der — **kitap** reddedilmez, kitap tam olarak sindirilir ve aktarılır. Reddedilen şey **kullanıcının kişisel klinik sorusu**dur; bu bir içerik sansürü değil, rol sınırıdır. Sistem doktor değildir, doktor gibi konuşmaz.

---

## 6. Çelişen çalışmalar

İki kitap zıt bulgu veriyor. Ne yapılır?

### 6.1 Karar: kazanan ilan edilmez, gerilim gösterilir — ama gerilim ölçülür

"İkisi de olabilir" cevabı işe yaramaz (kullanıcı kafa karışıklığından nefret ediyor). "A kazandı" cevabı da yanlış (sistem hakem değil). Çözüm: **çelişkiyi tek ekranda, ölçülmüş biçimde** göstermek.

### 6.2 Çelişki kartı (contradiction card)

```
┌──────────────────────────────────────────────────────────┐
│  ÇELİŞKİ · doymuş yağ ve kardiyovasküler risk            │
├──────────────────────────────┬───────────────────────────┤
│  Kitap A (2004) s.112        │  Kitap B (2016) s.88      │
│  "Riski artırır"             │  "Bağımsız etkisi yok"    │
│                              │                           │
│  L3 kohort                   │  L1 meta-analiz           │
│  n = 12.400                  │  21 çalışma, n = 347.000  │
│  çalışma yılı 1998           │  çalışma yılı 2014        │
│  vekil sonuç (LDL)           │  sert sonuç (KV olay)     │
├──────────────────────────────┴───────────────────────────┤
│  Ağırlık: B daha güçlü zeminde (L1 > L3, sert > vekil).  │
│  Ama aynı soruyu sormuyorlar: A ikame besini             │
│  belirtmiyor, B karbonhidratla ikame varsayıyor.         │
│  → Gerçek çelişki değil; farklı komparatör.              │
└──────────────────────────────────────────────────────────┘
```

### 6.3 Sıralama kuralı (deterministik)

Sistem hangi tarafın "daha güçlü zeminde" olduğunu şu leksikografik sırayla söyler:

1. `evidence_level` (L1 > L2 > … > L6)
2. `outcome_kind` (hard > surrogate > self_report)
3. `replication_risk` (low > moderate > high > known_failed)
4. `sample_size` (büyük > küçük)
5. `publication_year` (yeni > eski) — **en son kriter**, tek başına asla belirleyici değil

Beraberlik → "eşit güçte, karar verilemiyor" yazılır. Bu geçerli bir çıktıdır.

### 6.4 Sözde-çelişki tespiti

Çelişki kaydedilmeden önce PICO karşılaştırması yapılır:

```
if A.population ≉ B.population:  → "farklı popülasyon, çelişki değil"
if A.comparator ≉ B.comparator:  → "farklı karşılaştırma, çelişki değil"
if A.outcome ≉ B.outcome:        → "farklı sonuç ölçütü, çelişki değil"
else:                            → gerçek çelişki, §6.2 kartı
```

Bu, ampirik alanlardaki "çelişkilerin" büyük kısmını eritir ve kullanıcıya **çelişkiden daha değerli** bir şey verir: iki çalışmanın neyi farklı ölçtüğünü.

### 6.5 Dil

- ✔ "B daha güçlü zeminde duruyor."
- ✔ "İkisi aynı soruyu sormuyor."
- ✗ "B doğru, A yanlış."
- ✗ "Bilim artık B diyor." — sistem bilimin sesi değil

---

## 7. Tıptan mühendisliğe transfer

`07-transfer.md` için hammadde. Her biri **yapısal**, metafor değil: tıptaki formel yapı mühendislikte aynı formel yapıya karşılık gelir.

### T1 — Doz-yanıt eğrisi → monoton olmayan parametre ayarı

**Tıp:** Etki doza monoton değildir; hormesis (düşük dozda faydalı, yüksek dozda zararlı) ve terapötik pencere (therapeutic window) vardır. Etkili doz ile toksik doz arasındaki oran = terapötik indeks.
**Mühendislik:** Öğrenme oranı, thread havuzu boyutu, cache TTL, retry sayısı — hepsi ters-U eğrisi. "Daha fazla daha iyi" varsayımı buralarda yanlış.
**Transfer edilen yapı:** *Bir parametrenin optimum aralığını, tek yönlü artışla değil, iki yönlü sınırla (alt eşik + toksisite eşiği) tanımla; aralarındaki oranı sistemin sağlamlık payı olarak raporla.*
**Somut soru:** "Bu servisin retry sayısının terapötik indeksi kaç?"

### T2 — Homeostaz ve negatif geri besleme → kontrol döngüsü tasarımı

**Tıp:** Vücut set-point etrafında düzenler; efektör, sensör, gecikme, kazanç (gain). Hastalık çoğu zaman **düzenlemenin bozulması**dır, değerin kendisi değil (ör. tip-2 diyabet = insülin direnci, insülin yokluğu değil).
**Mühendislik:** Autoscaling, backpressure, PID kontrolörler, rate limiter. Gecikmeli geri besleme salınım (oscillation) üretir — hem böbrekte hem autoscaler'da.
**Transfer edilen yapı:** *Bir metriğin sapmasını okurken önce "değer mi bozuk, düzenleyici mi bozuk" diye sor. Düzenleyici bozuksa değeri zorlamak durumu kötüleştirir.*
**Somut soru:** "Latency yüksek — kaynak mı yetersiz, yoksa autoscaler'ın kazancı mı fazla?"

### T3 — Triyaj → sınırlı kaynak altında sıralama

**Tıp:** Afet triyajında kaynak, iyileşme olasılığı en yüksek olana değil, **müdahalenin sonucu en çok değiştirdiği** hastaya gider. Zaten iyi olan ve zaten kaybedilen aynı kategoriye düşer: bekleyebilir.
**Mühendislik:** Bug önceliklendirme, teknik borç sırası, incident yanıtı. Yaygın hata: "en kötü olan önce" — oysa doğru ölçüt **müdahale kaldıracı** (etki × düzeltilebilirlik).
**Transfer edilen yapı:** *Sıralamayı şiddete göre değil, `Δ(sonuç | müdahale)` değerine göre yap.*
**Somut soru:** "Backlog'da şiddeti en yüksek olan değil, düzeltmenin en çok fark yarattığı hangisi?"

### T4 — Teşhis ağacı ve olabilirlik oranı (likelihood ratio) → hata ayıklama sırası

**Tıp:** İyi klinisyen en olası tanıyı değil, **en çok bilgi veren testi** ilk yapar. Bayes: ön-test olasılığı × LR = son-test olasılığı. Düşük LR'li test pahalıysa hiç yapılmaz.
**Mühendislik:** Debug sırası, log ekleme yeri, bisect. Yaygın hata: en tanıdık hipotezden başlamak.
**Transfer edilen yapı:** *Her tanı adımını "bu test hipotez uzayını kaça böler / maliyeti ne" oranıyla sırala. Binary search zaten bunun ekstrem hali.*
**Somut soru:** "Bu log satırını eklemek olasılık uzayını yarıya bölüyor mu, %5 mi kırpıyor?"

### T5 — Yanlış pozitifin maliyeti ve tarama paradoksu → alarm tasarımı

**Tıp:** Nadir hastalıkta %99 özgüllüklü test bile çoğunlukla yanlış pozitif verir (taban oranı yanılgısı). Aşırı tarama → gereksiz biyopsi, aşırı teşhis (overdiagnosis), hasta zararı. "Test etmemek" bazen doğru karardır.
**Mühendislik:** Alarm yorgunluğu (alert fatigue), flaky test, statik analiz gürültüsü, güvenlik uyarıları. Aynı matematik: nadir olay + yüksek hacim = pozitiflerin çoğu yanlış.
**Transfer edilen yapı:** *Bir alarmı eklemeden önce taban oranını tahmin et ve PPV hesapla; PPV düşükse alarm sistemin duyarlılığını topluca düşürür.*
**Somut soru:** "Bu uyarı ayda kaç kez doğru çıkacak? 1'den azsa ekleme."

### T6 — Antibiyotik direnci → optimizasyon baskısının uyum yaratması

**Tıp:** Bir baskı sürekli uygulandığında popülasyon ona uyum sağlar; direnç gelişir. Karşı önlemler: kombinasyon tedavisi, döngüsel (cycling) rejim, tam kür (yarım doz en kötüsü).
**Mühendislik:** Goodhart yasası, metrik oyunlama, spam filtresi ↔ spam yazarı, benchmark overfitting, WAF kuralları.
**Transfer edilen yapı:** *Adaptif bir rakip varsa tek ve sabit bir metrik/kural asla kalıcı değildir; ya kombinasyon ya rotasyon gerekir. Ve yarım uygulanan kural (yarım doz) hiç uygulamamaktan kötüdür — sadece dirençliyi seçer.*
**Somut soru:** "Bu metriği hedef yaparsam ekip nasıl uyum sağlar, ve yarım uygularsam ne seçilmiş olur?"

### T7 — Çalışma tasarımı → deney tasarımı (bonus, en doğrudan transfer)

**Tıp:** Randomizasyon, körleme, ön kayıt, birincil sonuç ölçütünü önceden ilan etme, ara analiz durdurma kuralları.
**Mühendislik:** A/B test, feature flag deneyi, kapasite testi. Yaygın hata: p-hacking'in mühendislik hali — deneyi anlamlı çıkana kadar izlemek (peeking).
**Transfer edilen yapı:** *Birincil metriği ve örneklem büyüklüğünü deneyden önce yaz, deney sırasında bakma.*

> `07-transfer.md` için not: T1, T4, T5 en yüksek transfer verimine sahip üçlü — hepsi doğrudan sayısal, hepsi mühendisin haftalık kararında geçiyor.

---

## 8. Örnek çıktı — tam bir ampirik atom

```yaml
atom_id: atm_9f2c41
type: empirical_claim

book_id: bk_0117
book_title: "Uyku ve Metabolizma"        # örnek
book_year: 2018
chapter: "Bölüm 4 — Kısa Uyku ve İnsülin"
page_anchor: { page: 96, para: 2 }
quote: >
  "On bir sağlıklı genç erkeği altı gece boyunca dört saat uykuya
   kısıtladığımızda, glukoz tolerans testleri prediyabetik aralığa kaydı."

claim: "Kısa süreli uyku kısıtlaması sağlıklı genç erişkinlerde glukoz toleransını bozar."

pico:
  population:   "11 sağlıklı erkek, 18–27 yaş, normal VKİ"
  intervention: "6 gece boyunca gecede 4 saat uyku"
  comparator:   "aynı denekler, toparlanma döneminde 12 saat uyku (çapraz geçiş)"
  outcome:      "oral glukoz tolerans testi (OGTT) eğri altı alanı"
  outcome_kind: surrogate

effect_size:
  kind: "%change"
  value: -40
  note: "glukoz temizlenme hızında azalma"
confidence_interval: null
p_value: 0.02
sample_size: 11

study_design: randomized_crossover
publication_year: 1999

citation_chain:
  book_says: "Spiegel, Leproult & Van Cauter, The Lancet, 1999"
  resolved: true
  identifier: "PMID:10543671"

evidence_level: L2
evidence_note: "Randomize çapraz geçiş; ancak n=11 ve vekil sonuç."

replication_risk: moderate
replication_note: >
  Alan: fizyoloji/metabolizma (kat. 0.75). Çekirdek bulgu birden çok
  laboratuvarda tekrarlandı; etkinin büyüklüğü daha küçük bildirildi.

warning_flags:
  - code: S10
    text: "Ölçülen ara gösterge (glukoz toleransı); iddia sert sonuca (diyabet) uzanıyor."
  - code: S1
    text: "Bölüm bu tek çalışmaya dayanıyor."

warning_score: 5          # → turuncu rozet: "zayıf"

graph_edges:
  - { rel: "supports",     target: atm_7a10bb }   # "uyku borcu birikir"
  - { rel: "contradicts",  target: atm_44e0d2 }   # başka kitap: etki geçici
  - { rel: "prerequisite", target: atm_2b91ff }   # insülin direnci tanımı

transfer_hooks:
  - open_question: "oq_004 — build sunucularının gece throttling'i"
    structure: "T1 doz-yanıt: kısıtlamanın etkisi eşik sonrası doğrusal değil"
    strength: 0.42
    label: hypothesis_only
```

### Bu atomun arayüzdeki hâli

```
Kısa uyku glukoz toleransını bozar.
Uyku ve Metabolizma · Bölüm 4 · s.96

  🟠 zayıf kanıt          RKÇ (çapraz geçiş) · n=11 · 1999
  ⟳ tekrarlama: orta risk

  · Ölçülen ara gösterge (glukoz toleransı); iddia sert sonuca uzanıyor.
  · Bölüm bu tek çalışmaya dayanıyor.

  ⚡ 1 çelişki var — "Uyku Üzerine" s.203 ile

                                          bilgi · tavsiye değil
```

Kart üç satır bilgi verir, dördüncüyü bir tık arkasında tutar (Kural 1).

---

## 9. Açık sorular

- `AÇIK SORU:` Alan güvenilirlik tablosu ve known-failed listesi kimin sorumluluğunda güncellenecek? Öneri: repo içinde `data/replication-registry.json`, PR ile katkıya açık.
- `AÇIK SORU:` PICO çıkarımı LLM'e bırakılıyor; ölçülmüş doğruluğu bilinmiyor. 100 paragraflık elle etiketlenmiş bir doğrulama kümesi (gold set) gerekiyor — hangi kitaplardan?
- `AÇIK SORU:` §5.4 kapısının Türkçe belirti/ilaç sözlüğü nereden gelecek? ATC kodları + Türkçe halk dili eşlemesi (baş dönmesi, çarpıntı, mide yanması) elle kurulmalı.
- `AÇIK SORU:` Kullanıcı zayıf kanıtlı atomları tamamen gizleyebilmeli mi (filtre)? Gizleme Kural 3'ü ihlal etmez (kitap reddedilmiyor, görünüm filtreleniyor) ama kullanıcıyı yankı odasına sokar. Öneri: filtre yok, sıralama var — güçlü kanıt üste çıkar.
