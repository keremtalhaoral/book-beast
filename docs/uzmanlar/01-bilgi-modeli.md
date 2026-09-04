# 01 — Bilgi Modeli: Fikir Atomu, Epistemik Durum ve İlişki Cebiri

> Uzman: Bilgi Mimarı & Epistemolog
> Durum: v1 tasarım — diğer 12 belge bu şemanın üstüne inşa eder.

## 3 cümlelik özet

**Fikir atomu**, tek bir yüklem taşıyan (single-predication), tek başına çürütülebilen ve tek bir karakter-aralığına çapalanmış en küçük bilgi birimidir; çekirdek şeması bütün alanlarda aynıdır, alan farkı yalnızca `ext` uzantısında yaşar. Her atom iki ayrı eksende etiketlenir — **kip** (analitik/ampirik/normatif/anlatısal/yöntemsel) ve **destek** (kanıtlanmış → çürütülmüş) — çünkü "değer yargısı" bir güven seviyesi değil, bir iddia türüdür ve ikisini karıştırmak sistemin epistemik omurgasını kırar. Çelişkide **kazanan ilan edilmez**: sistem önce çelişkiyi 5 tipe ayırır (eşadlılık / kapsam / zamansal yenilenme / gerçek / normatif), yalnızca sunum sırası için bir `credence` skoru hesaplar ve gerçek çelişkiyi kullanıcıya "ayrım noktası" (crux) ile birlikte tek ekranda gösterir.

## 1. Fikir atomu nedir?

**Tanım.** Fikir atomu, kitaptan çıkarılmış, (a) tek bir yüklemi olan, (b) bağlamdan koparıldığında hâlâ anlamlı kalan, (c) tek bir kaynak aralığına çapalanan, (d) tek başına doğrulanabilen veya çürütülebilen bilgi birimidir.

Atom bir *özet parçası* değildir. Atom bir **iddia taşıyıcısıdır** (truth-bearer) veya bir **işlem taşıyıcısıdır** (procedure-bearer). Kitabın "anlatım akışı" atomlarda saklanmaz — akış Katman 2'nin kenarlarında yeniden kurulur.

### 1.1 Çekirdek şema (bütün alanlarda ortak, değişmez)

```ts
type AtomId = string;        // "atm_" + ULID  (zaman-sıralı, çakışmasız)
type EditionId = string;     // "edn_" + ULID
type Iso8601 = string;

interface Atom {
  id:            AtomId;          // "atm_"+ULID, değişmez
  version:       number;          // atom güncellenmez, sürümlenir
  supersedes:    AtomId | null;   // önceki sürüm (aynı fikir, düzeltilmiş)
  type:          AtomType;        // §2
  claim:         string;          // kanonik ifade, ≤ 3 cümle / ≤ 60 kelime
  verbatim:      string | null;   // birebir alıntı — bazı tiplerde zorunlu (§8)
  body:          string | null;   // 40-200 kelime açıklama/bağlam
  terms:         TermRef[];       // normalize kavramlar (boş olabilir, null olamaz)
  qualifiers:    Qualifier[];     // geçerlilik koşulları — §6.2
  anchor:        SourceAnchor;    // §4
  edition:       EditionId;
  epistemic:     EpistemicState;  // §5
  domain:        Domain;          // ayrık birleşimin ayırıcısı
  ext:           DomainExtension; // §8 — `domain` alanına göre daraltılır
  status:        "draft" | "active" | "quarantined" | "retracted";
  provenance:    Provenance;      // §1.3
  fingerprint:   string;          // sha256(normalize(claim) + anchor.quote.exact)
  embedding_ref: string | null;   // vektör deposu anahtarı (Katman 2)
}

interface TermRef    { surface: string; concept: string | null; defined_by: AtomId | null }
interface Qualifier  { kind: "population"|"condition"|"regime"|"unit"|"time"|"assumption";
                       value: string }   // "n<30 örneklem", "düşük Reynolds", "1789 öncesi Fransa"
interface Provenance { extractor_model: string; prompt_version: string; extracted_at: Iso8601;
                       human_reviewed: boolean; review_note: string | null }
```

### 1.2 Zorunluluk özeti

- **Zorunlu:** `id`, `version`, `type`, `claim`, `anchor`, `edition`, `epistemic`, `domain`, `ext`, `status`, `provenance`, `fingerprint`. Eksikse atom yazılamaz.
- **Zorunlu ama boş dizi serbest:** `terms`, `qualifiers`. `null` yasak — boşluğu açıkça beyan et.
- **Tipe bağlı zorunlu:** `verbatim` → `theorem`, `definition`, `formula`, `quote`.
- **Opsiyonel:** `body`, `embedding_ref`, `supersedes`.

### 1.3 Değişmezlik kuralı

Atomlar **silinmez ve yerinde düzeltilmez**. Düzeltme = yeni sürüm + `supersedes`. Çürütülen atom `epistemic.support = "refuted"` alır ama grafta kalır; çünkü "bu kitap yanlış olduğu kanıtlanmış şeyi söylüyor" bilgisinin kendisi değerlidir. Yalnızca çıkarım hatası (kitapta olmayan şeyin uydurulması) `retracted` yapar.

## 2. Atom tipolojisi

11 tip. Tip, atomun **ne tür bir şey** olduğunu söyler; kip ve destek (§5) ne kadar güvenilir olduğunu söyler. İkisi bağımsızdır.

| # | Tip | Ne? | Ayırt edici alanlar | `verbatim` |
|---|---|---|---|---|
| 1 | `definition` | Bir terimi sabitler | `defines_term`, `definiens`, `scope` | zorunlu |
| 2 | `theorem` | Biçimsel, ispatlanabilir önerme | `hypotheses[]`, `conclusion`, `proof_ref`, `formal_statement` | zorunlu |
| 3 | `proof_idea` | İspatın taşıyıcı fikri | `proves` (AtomId), `technique` | hayır |
| 4 | `empirical_claim` | Dünya hakkında ölçülebilir iddia | `evidence[]`, `effect`, `sample`, `measurement` | hayır |
| 5 | `mechanism` | Nedensel/işleyiş açıklaması | `cause`, `effect`, `mediators[]`, `direction` | hayır |
| 6 | `method` | Nasıl yapılır (yordam) | `steps[]`, `inputs`, `outputs`, `preconditions[]`, `failure_modes[]` | hayır |
| 7 | `formula` | Sembolik ilişki | `latex`, `symbols[]`, `units`, `validity_range`, `sympy_check` | zorunlu |
| 8 | `heuristic` | Kanıtı zayıf ama işe yarar kural | `when_applies`, `known_exceptions[]` | hayır |
| 9 | `normative_claim` | Değer yargısı / olması gereken | `value_basis`, `stance_of` (yazar/okul), `opposing_positions[]` | hayır |
| 10 | `anecdote` | Tekil olay, örnek, vaka | `actors[]`, `time`, `place`, `illustrates` (AtomId) | hayır |
| 11 | `quote` | Yazarın kendi formülasyonu, aynen korunmalı | `speaker`, `rhetorical_role` | zorunlu |

**Kritik ayrımlar:**
- `theorem` ≠ `empirical_claim`: teorem aksiyomlardan türetilir, ampirik iddia dünyadan. Bir teoremi "veri destekliyor" demek kategori hatasıdır; sistem bu hatayı şema düzeyinde engeller (`theorem.ext` alanı `evidence[]` taşımaz).
- `method` ≠ `heuristic`: yöntemin önkoşulları ve çıktısı tanımlıdır; sezgisel kuralın istisnaları vardır.
- `normative_claim` asla `proved`/`refuted` desteği alamaz — yalnızca `stance` işaretlenir. Şema bunu kısıtlar.
- `anecdote` transfer motorunda **analoji taşıyıcısı** olarak birinci sınıf yurttaştır; "önemsiz hikâye" değildir. Çapraz-alan sıçramalarının çoğu anekdot–mekanizma eşleşmesinden çıkar.

## 3. Granülerlik kuralı

### 3.1 Temel kural: Tek Yüklem Kuralı

> Bir atom **tek bir yüklem** taşır. `claim` alanı tek bir bağımsız cümleye indirgenebilmelidir.

### 3.2 Bölme testleri (herhangi biri geçerse BÖL)

1. **Bağlaç testi.** `claim` içinde "ve / ayrıca / bunun yanında / hem … hem" ile bağlanmış, her biri tek başına doğru/yanlış olabilen iki yüklem varsa → böl.
2. **Karşı-örnek testi.** Tek bir karşı-örnek atomu **tamamen** yıkmalı. Karşı-örnek atomun yarısını ayakta bırakıyorsa → atom iki yüklem taşıyordu, böl.
3. **Çapa testi.** Parçalar farklı, bitişik olmayan karakter aralıklarını gerektiriyorsa → böl.
4. **Epistemik testi.** Parçalardan biri `proved`, diğeri `speculative` ise → böl. Tek atom tek destek seviyesi taşır.
5. **Uzunluk testi.** `claim` > 60 kelime veya > 3 cümle → bölmeyi dene; bölünemiyorsa `body`'ye taşı.

### 3.3 Birleştirme testleri (hepsi geçerse BİRLEŞTİR)

1. Aynı bölüm, aralarında ≤ 2 paragraf mesafe.
2. Biri diğeri olmadan anlamsız (bağlam bağımlılığı ≈ 1).
3. İkisi de aynı tip, aynı kip, aynı destek seviyesi.
4. Birleşik `claim` hâlâ ≤ 60 kelime.

Birleştirme yerine **alt-atom** de kullanılabilir: `theorem` + `proof_idea` ayrı atomlardır, `PROVES` kenarıyla bağlanır — birleştirilmez.

### 3.4 Transfer alt sınırı

Bir parça, Açık Sorular Defteri'ndeki bir soruya **tek başına** aday olamıyorsa fazla küçüktür. "Reynolds sayısı bir orandır" atom değildir; "Re < 2300'de akış laminerdir" atomdur.

### 3.5 Kitaptan kaç atom çıkar?

Ölçü birimi **atom yoğunluğu** = atom / 1000 kelime. Sayfa değil kelime kullanıyoruz çünkü sayfa formata bağlıdır.

| Kitap türü | Tipik kelime | Yoğunluk (atom/1000 kelime) | Beklenen atom |
|---|---|---|---|
| Matematik ders kitabı (Rudin tipi) | ~90k | 5 – 8 | 450 – 720 |
| Mühendislik ders kitabı | ~200k | 3 – 5 | 600 – 1000 |
| Felsefe klasiği / analitik metin | ~120k | 3 – 6 | 360 – 720 |
| Tarih monografisi | ~150k | 2 – 3.5 | 300 – 525 |
| Tıp kılavuzu / kanıt derlemesi | ~120k | 4 – 7 | 480 – 840 |
| Popüler kurgu-dışı | ~90k | 1.5 – 3 | 135 – 270 |
| Kişisel gelişim | ~60k | 0.8 – 2 | 50 – 120 |
| Sanat / anlatı incelemesi | ~80k | 1 – 2.5 | 80 – 200 |

**Alarm kuralı.** Gerçek yoğunluk bandın **altındaysa** sindirim eksik → yeniden çalıştır. **Üstündeyse** aşırı parçalama (over-splitting) → birleştirme turu çalıştır. İki denemede banda giremeyen kitap `quarantined` olur ve kullanıcıya "bu kitap beklenenden farklı yoğunlukta, gözden geçirilsin" rozeti gösterilir.

## 4. Kaynak çapası (source anchor)

### 4.1 Karar: kanonik birim **karakter ofsetidir**, sayfa değil

Yükleme sırasında her kitap tek bir **normalize metin akışına** (normalized text stream) dönüştürülür: Unicode NFC, tek boşluk, tire-birleştirme, dipnotlar ayrı akışa. Bu akıştaki her karakterin global bir indeksi vardır. Sayfa, konum, ilerleme oranı — hepsi bundan **türetilir**.

```ts
interface SourceAnchor {
  edition:    EditionId;
  char_start: number;   char_end: number;        // 1) KANONİK: normalize akışta aralık

  locator: {                                     // 2) yapısal konum (insan okur)
    chapter_idx: number; chapter_title: string;
    section_path: string[];                      // ["7","7.3","7.3.2"]
    paragraph_idx: number };

  native:                                        // 3) format-özel geri dönüş çapası
    | { kind: "epub"; cfi_start: string; cfi_end: string; spine_idref: string }
    | { kind: "pdf";  page: number; quads: number[][] }      // dört köşe — vurgulama
    | { kind: "html"; xpath_start: string; xpath_end: string; offset_start: number; offset_end: number }
    | { kind: "text" };                          // char aralığı yeterli

  quote: {                                       // 4) W3C TextQuoteSelector — sürüklenmeye dayanıklı
    prefix: string;                              // önceki 48 karakter
    exact:  string;                              // alıntı, ≤ 1200 karakter
    suffix: string;                              // sonraki 48 karakter
    hash:   string };                            // sha256(prefix|exact|suffix)

  print_page:  number | null;   // EPUB page-list / PDF gerçek sayfası; yoksa null
  pseudo_page: number;          // türetilmiş — §4.2
  progress:    number;          // 0..1 kitap içi konum
  anchor_status: "ok" | "drifted" | "lost";
}
```

### 4.2 EPUB'da sayfa yok — çözüm: sözde-sayfa (pseudo-page)

**Karar: 1 sözde-sayfa = 1800 normalize karakter.** Sabit, sürüm bağımsız, kitap bağımsız.

`pseudo_page = floor(char_start / 1800) + 1`

Neden gerekli: Doktrin 3 ("bu kitabın şu 11 sayfasını oku") sayısal bir sayfa niceliği ister. EPUB'da okuyucu yazı tipine göre sayfa değişir; sabit karakter tabanı bu kaymayı yok eder. Kullanıcıya "11 sayfa" derken kastedilen 11 × 1800 ≈ 19.800 karakterdir ve bu tahmin gerçek basılı sayfayla ±%15 içinde tutar.

**Gösterim kuralı:** `print_page` varsa o gösterilir ("s. 214"); yoksa sözde-sayfa gösterilir ("≈ s. 214") — **tilde işareti zorunlu**, kullanıcı tahmin olduğunu görmeli (Doktrin: emin olmadığını emin gibi sunma).

### 4.3 Kitap kimliği ve sürüklenme (drift)

`EditionId` = `hash(ISBN ?? "") + hash(normalize(ilk 100.000 karakter))`. Aynı kitabın farklı baskısı **farklı edition**'dır; atomlar edition'a bağlıdır, "kitap" (`work_id`) ise edition'ları toplayan üst kavramdır.

Kullanıcı aynı kitabın yeni dosyasını yüklerse **yeniden çapalama** (re-anchoring) çalışır:

1. `char_start` civarında `quote.exact` tam eşleşme aranır → bulunursa `ok`.
2. Bulunamazsa `±%2` kitap uzunluğu penceresinde tam eşleşme aranır.
3. Bulunamazsa `prefix + suffix` ile bulanık arama (normalize Levenshtein ≤ %10) → bulunursa `ok`, ofsetler güncellenir.
4. Hâlâ yoksa → `anchor_status = "drifted"`, konum bölüm seviyesine düşürülür.
5. Bölüm de eşleşmezse → `"lost"`.

**Doktrin 2 uygulaması:** `drifted` atom transfer önerisinde kullanılabilir ama **alıntı gösteremez** ve "konum doğrulanamadı" rozeti taşır. `lost` atom hiçbir üretimde kullanılamaz, yalnızca arşivde durur.

## 5. Epistemik durum

### 5.1 Karar: tek eksen değil, dört eksen

Tek bir "güven etiketi" yanlıştır çünkü "yazarın kanısı" ile "spekülatif" farklı şeylerdir: biri iddianın **türü**, diğeri **destek derecesi**.

```ts
interface EpistemicState {
  modality:     Modality;      // iddianın TÜRÜ
  support:      Support;       // destek DERECESİ
  verification: Verification;  // BİZİM ne doğruladığımız
  hedge:        Hedge;         // YAZARIN kendi kesinlik dili
  rationale:    string;        // ≤ 200 karakter — neden bu etiket
  assessed_by:  "rule" | "llm" | "human";
}

type Modality =
  | "analytic"    // tanım gereği doğru: matematik, mantık, terim uzlaşımı
  | "empirical"   // dünya hakkında, ölçümle yanlışlanabilir
  | "normative"   // olması gereken, değer yargısı
  | "procedural"  // nasıl yapılır, başarı/başarısızlıkla değerlendirilir
  | "narrative";  // tekil olay anlatısı, kaynak güvenilirliğiyle değerlendirilir

type Support =
  | "proved"          // biçimsel ispat var — YALNIZCA modality=analytic
  | "strong"          // çoklu bağımsız kanıt / meta-analiz / tekrarlanmış
  | "moderate"        // tek iyi çalışma veya uzman uzlaşısı, tekrar yok
  | "weak"            // dolaylı, küçük örneklem, tek vaka, seçilmiş örnek
  | "speculative"     // hipotez, mekanizma önerisi, düşünce deneyi
  | "contested"       // alanda aktif tartışma, iki güçlü taraf
  | "refuted"         // daha güçlü kanıtla yalanlanmış
  | "not_applicable"  // modality = normative | narrative
  | "unassessed";     // varsayılan — değerlendirici geçmedi

type Verification = "symbolic_ok" | "symbolic_fail" | "citation_ok"
                  | "citation_missing" | "human_ok" | "unverified";  // varsayılan: unverified
type Hedge        = "asserted" | "hedged" | "conjectured" | "attributed";
```

### 5.2 Atama kriterleri (işletilebilir)

| Sinyal | Nereye bakılır | Sonuç |
|---|---|---|
| `\begin{theorem}`, "Teorem", "Lemma", ispat bloğu | yapı | `modality=analytic`, aday `support=proved` |
| Ardından ispat yok, "ispat okuyucuya bırakıldı" da yok | yapı | `proved` → `moderate`, `verification=unverified` |
| "n=…", "p<…", "%95 GA", tablo/şekil atfı | metin | `modality=empirical`, aday `support=moderate` |
| Meta-analiz / sistematik derleme / ≥3 bağımsız çalışma atfı | atıf | `support=strong` |
| Tek vaka, "gördüğüm kadarıyla", "bir arkadaşım" | metin | `support=weak` |
| "olabilir, sanıyorum ki, muhtemelen, belki" | metin | `hedge=hedged`, tavan `support=speculative` |
| "bence, olmalıdır, doğru olan, ahlaken" | metin | `modality=normative`, `support=not_applicable` |
| "X'e göre", "X şöyle der" | metin | `hedge=attributed`, atom `stance_of` alır |
| Kitapta tarih verisi ve alan yarı-ömrü aşılmış (§6.4) | meta | `support` bir kademe düşer |
| Grafta `REFUTES` kenarı gelmiş ve karşı taraf daha yüksek `credence` | graf | `support=refuted` |

**Sert kısıtlar (şema düzeyinde zorlanır):**
- `support = "proved"` ⟹ `modality = "analytic"` **ve** (`type = "theorem" | "formula"`) **ve** `verification ∈ {symbolic_ok, human_ok}`.
- `modality = "normative"` ⟹ `support = "not_applicable"`. Değer yargısı ne kanıtlanır ne çürütülür; yalnızca konumlandırılır.
- `verification = "symbolic_fail"` ⟹ atom otomatik `status = "quarantined"` ve üretimde `[doğrulanamadı]` etiketi zorunlu.
- Varsayılan `unassessed` atomlar transfer önerisinde **kullanılabilir** ama "değerlendirilmedi" rozetiyle.

### 5.3 Kullanıcıya gösterim (tek kelimeye indirgeme)

Kullanıcı 4 eksen görmez; arayüz tek rozet gösterir. Öncelik sırasıyla:
**Yazarın görüşü** (`modality=normative`) · **Çürütülmüş** (`refuted`) · **Tartışmalı** (`contested`) ·
**Kanıtlanmış** (`proved`) · **Sağlam** (`strong`) · **Destekli** (`moderate`) ·
**Spekülatif** (`speculative` veya `hedge=conjectured`) · **Zayıf** (`weak`) · **Değerlendirilmedi** (`unassessed`).
`verification=symbolic_fail` ise rozete `[doğrulanamadı]` eklenir — rozetin kendisi ne olursa olsun.

## 6. Çelişki yönetimi

### 6.1 Temel karar: kazanan ilan edilmez

Sistem hakem değildir. Ama sessiz de kalmaz. **Çelişki bir birinci sınıf nesnedir** ve önce *sınıflandırılır*, sonra sunulur.

### 6.2 Çelişki tipolojisi (sırayla denenir; ilk eşleşen kazanır)

| # | Tip | Teşhis | Sistemin yaptığı |
|---|---|---|---|
| 1 | **Eşadlılık** (equivocation) | Aynı terim, iki atomda farklı `TermRef.concept` | Sahte çelişki. Terimler ayrıştırılır, kenar `SAME_TERM_DIFFERENT_SENSE` olur, kullanıcıya gösterilmez. |
| 2 | **Kapsam** (scope) | `qualifiers` kesişimi boş (farklı popülasyon/rejim/dönem) | İkisi de doğru. Kenar `QUALIFIES` olur; kullanıcıya "şu koşulda A, şu koşulda B" tek kartı gösterilir. |
| 3 | **Zamansal yenilenme** (supersession) | Aynı kapsam, `empirical`, yayın farkı > alan yarı-ömrü, yeni olan eskiyi atıfla reddediyor | Yeni atom `SUPERSEDES` eskiyi. Eski `refuted` olur ama silinmez. |
| 4 | **Gerçek çelişki** | Aynı kapsam, aynı terim anlamı, aynı dönem, zıt yüklem | **Kazanan yok.** `CONTRADICTS` kenarı + Çatışma Kartı (§6.5). |
| 5 | **Normatif çatışma** | En az biri `modality=normative` | Asla çözülmez. "İki konum" olarak sunulur, `credence` hesaplanmaz. |

### 6.3 `credence` — yalnızca sunum sırası için

`credence ∈ [0,1]`, **hakikat kararı değil, sıralama sinyali**. Çatışma Kartında hangi tarafın solda duracağını ve gövde metninde hangisinin önce anlatılacağını belirler. Asla "bu doğru" olarak sunulmaz.

```
credence = 0.45 · S(support)
         + 0.25 · min(1, bağımsız_teyit_sayısı / 3)
         + 0.20 · T(güncellik)
         + 0.10 · A(alan_otoritesi)
```

- `S`: proved 1.0 · strong 0.85 · moderate 0.6 · contested 0.5 · weak 0.3 · speculative 0.15 · refuted 0.0
- `bağımsız_teyit`: farklı **kitap ve farklı yazar**tan gelen `SUPPORTS` kenarı sayısı. Aynı yazarın iki kitabı 1 sayılır.
- `T = 0.5^(yaş / yarı_ömür)` — §6.4
- `A`: atomun alanı, kitabın birincil alanıyla eşleşiyorsa 1.0; komşu alansa 0.6; alan dışıysa 0.3. (Bir tarih kitabının nörobilim iddiası zayıf tartılır.)

### 6.4 Alan yarı-ömrü (güncellik ağırlığı)

| Alan | Yarı-ömür | Gerekçe |
|---|---|---|
| Matematik, mantık | ∞ (T = 1) | Teoremler eskimez |
| Tarih (olay) | 30 yıl | Yeni arşiv nadiren çıkar |
| Tarih (yorum), felsefe | ∞ (T = 1) | Yorum eskimez, tartışılır |
| Mühendislik temelleri | 25 yıl | |
| Mühendislik pratiği / yazılım | 5 yıl | |
| Makine öğrenmesi | 2 yıl | |
| Tıp (klinik) | 6 yıl | Kılavuzlar döner |
| Beslenme, psikoloji | 8 yıl | Tekrar krizi bandı |
| Sanat, edebiyat | ∞ (T = 1) | |
| Kişisel gelişim | 10 yıl | |

Yarı-ömrü ∞ olan alanlarda **tip 3 (zamansal yenilenme) hiç uygulanmaz** — 1900'de yazılmış bir teorem 2020'deki yüzünden eskimez.

### 6.5 Çatışma Kartı — kullanıcı ne görür?

Doktrin 1 gereği tek ekran, tek karar:

```
ÇELİŞKİ — aynı soruya iki cevap
  A · Kitap X, s. 212    [Sağlam]     "…"
  B · Kitap Y, ≈ s. 88   [Destekli]   "…"
  AYRIM NOKTASI: "X 2018 öncesi veriyle, Y 2023 kohortuyla çalışıyor.
                  Fark örneklemde, yöntemde değil."
  [ Defterime al ]   [ Sonra ]
```

- İki taraf **eşit görsel ağırlıkta** gösterilir; `credence` yalnızca sırayı belirler, boyutu değil.
- **Ayrım noktası zorunludur.** Sistem crux üretemiyorsa kart gösterilmez, çelişki `unresolved_unexplained` kuyruğuna düşer. Açıklanamayan çelişkiyi kullanıcıya atmak kafa karıştırmaktır — Doktrin 1 ihlali.
- Kullanıcı bir tarafı seçerse bu bir *hakikat kararı* değil, **kişisel duruş** olarak `user_stance` tablosuna yazılır ve sonraki üretimlerde o taraf öne alınır, ama diğeri asla silinmez.

## 7. İlişki taksonomisi (Katman 2)

### 7.1 Kenar da bir nesnedir

```ts
interface Relation {
  id: string;  type: RelationType;  from: AtomId;  to: AtomId;
  strength:   number;        // 0..1 — ilişki ne kadar SIKI
  confidence: number;        // 0..1 — tespit ne kadar GÜVENİLİR
  evidence:   string | null; // kenarı doğuran metin/gerekçe
  detector:   "embedding" | "llm" | "symbolic" | "rule" | "human";
  status:     "proposed" | "accepted" | "rejected";
}
```

`strength` ve `confidence` ayrıdır: zayıf ama kesin bir destek ile güçlü ama şüpheli bir destek farklı şeylerdir.

### 7.2 Tam liste

| Tip | Tanım | Simetrik | Geçişli | Ters kenar |
|---|---|---|---|---|
| `RESTATES` | Aynı iddia, farklı ifade | ✓ | ✓ | kendisi |
| `SAME_TERM_DIFFERENT_SENSE` | Aynı terim, farklı kavram | ✓ | ✗ | kendisi |
| `SUPPORTS` | Kanıt/argüman sağlar | ✗ | ✗ | `SUPPORTED_BY` |
| `CONTRADICTS` | Zıt yüklem, aynı kapsam | ✓ | ✗ | kendisi |
| `REFUTES` | Çürütür (asimetrik, üstün kanıtla) | ✗ | ✗ | `REFUTED_BY` |
| `SUPERSEDES` | Yeniler, eskisini geçersizleştirir | ✗ | ✓ | `SUPERSEDED_BY` |
| `QUALIFIES` | Geçerlilik koşulu ekler / sınırlar | ✗ | ✗ | `QUALIFIED_BY` |
| `PREREQUISITE_OF` | Anlamak için önce gerekir | ✗ | ✓ | `REQUIRES` |
| `GENERALIZES` | Daha geniş hâli | ✗ | ✓ | `SPECIALIZES` |
| `INSTANCE_OF` | Genel kuralın somut örneği | ✗ | ✗ | `HAS_INSTANCE` |
| `APPLIES_TO` | Yöntem/teorem bir probleme uygulanır | ✗ | ✗ | `SOLVED_BY` |
| `PROVES` | İspat fikri teoremi kanıtlar | ✗ | ✗ | `PROVED_BY` |
| `DEFINES` | Terimi tanımlar | ✗ | ✗ | `DEFINED_BY` |
| `USES_TERM` | Tanımlı terimi kullanır | ✗ | ✗ | `TERM_USED_BY` |
| `DERIVES_FROM` | Formül/sonuç ötekinden türer | ✗ | ✓ | `DERIVED_INTO` |
| `PART_OF` | Bütünün parçası (bölüm, adım) | ✗ | ✓ | `HAS_PART` |
| `EXEMPLIFIES` | Anekdot bir fikri örnekler | ✗ | ✗ | `EXEMPLIFIED_BY` |
| `ANALOGOUS_TO` | Yapısal benzeşim, farklı alan | ✓ | ✗ | kendisi |
| `OPPOSES_STANCE` | Normatif karşı konum | ✓ | ✗ | kendisi |

19 tip. Daha fazlası kullanıcıya değil, yalnızca mühendise yarar.

### 7.3 Cebirsel kısıtlar (zorunlu, ihlali hata)

1. **`PREREQUISITE_OF` bir DAG'dır.** Döngü tespit edilirse en düşük `confidence` kenar `rejected` yapılır. (Doktrin 7: önkoşul DAG'ı.)
2. **`RESTATES` bir denklik bağıntısıdır** → bağlı bileşenler **denklik sınıfı** oluşturur; her sınıfın bir **kanonik temsilcisi** (en yüksek `credence` + en iyi çapa) seçilir. Yenilik hesabı (belge 02) atomlar üzerinde değil, denklik sınıfları üzerinde çalışır — "%94'ü zaten kütüphanende" hükmü buradan çıkar.
3. **`GENERALIZES` geçişlidir ve döngüsüzdür**; `A GENERALIZES B` ⟹ `B` `A`'yı çürütemez, yalnızca `QUALIFIES` edebilir.
4. **`CONTRADICTS` geçişli değildir** — A ile B, B ile C çelişiyorsa A ile C çelişmez (hatta aynı olabilir). Bu kural kapatılmazsa graf çelişki gürültüsüne boğulur.
5. **`ANALOGOUS_TO` yalnızca farklı `domain` atomları arasında kurulur.** Aynı alandaki benzerlik `RESTATES` veya `GENERALIZES`'tır. Bu kısıt, transfer motorunun (belge 07) sinyalini temiz tutar.
6. **`REFUTES` yönü `credence` ile belirlenir**, ama otomatik `refuted` etiketi için eşik: `credence(from) − credence(to) ≥ 0.25`. Altındaysa kenar `CONTRADICTS`'a düşer ve Çatışma Kartına gider.

## 8. Alanlar arası fark: ortak çekirdek + alan uzantısı

### 8.1 Cevap

**Evet, aynı çekirdeği paylaşırlar — hayır, aynı şema değildirler.** Çekirdek (§1.1) her alanda birebir aynıdır ve **asla büyümez**. Alan farkı `ext` içinde, `domain` üzerinden ayrılan bir birleşim tipinde yaşar.

```ts
type Domain = "math" | "engineering" | "medicine" | "history"
            | "philosophy" | "art" | "self_dev" | "general";

type DomainExtension =
  | { domain: "math";        /* … */ }
  | { domain: "engineering"; /* … */ }
  | …;
```

### 8.2 Uzantı sözleşmesi (extension contract)

Her `ext` üç kancayı doldurmak **zorundadır**; çekirdek motor yalnızca bu üçünü okur, gerisi alana özgüdür:

| Kanca | Ne verir | Kim kullanır |
|---|---|---|
| `support_signal(): Support` | Alan kurallarına göre destek seviyesi önerisi | §5 etiketleyici |
| `granularity_hint(): number` | Beklenen atom/1000 kelime | §3.5 alarm |
| `anchor_requirement(): "verbatim" \| "paraphrase"` | Alıntı zorunlu mu | §4, Doktrin 2 |

### 8.3 Uzantı alanları

| Alan | `ext` alanları | Zorunlu `verbatim`? |
|---|---|---|
| `math` | `statement_kind` (definition/theorem/lemma/corollary/proof/example), `formal_statement` (LaTeX), `hypotheses[]`, `conclusion`, `symbols[]`, `proof_technique`, `sympy_check` | **Evet** |
| `engineering` | `assumptions[]`, `operating_range`, `units`, `tolerance`, `failure_modes[]`, `standard_ref` (ISO/ASTM) | Formül ise evet |
| `medicine` | `pico` {population, intervention, comparator, outcome}, `study_design`, `n`, `effect_size`, `ci`, `grade_level`, `guideline_ref` | Hayır |
| `history` | `time_span`, `geo_scope`, `evidence_kind` (arşiv/anlatı/arkeolojik/ikincil), `historiographic_school`, `source_distance` (birincil/ikincil/üçüncül) | Hayır |
| `philosophy` | `argument_form` {premises[], conclusion, form}, `position_name`, `opposing_positions[]`, `thought_experiment` | Alıntı tipiyse evet |
| `art` | `medium`, `movement`, `technique`, `exemplar_work`, `subjectivity` (0..1) | Hayır |
| `self_dev` | `prescription`, `claimed_mechanism`, `evidence_backing`, `actionability` (0..1), `cost_of_being_wrong` | Hayır |
| `general` | `{}` | Hayır |

### 8.4 Aynı çekirdek, farklı yorum

Çekirdek alanlar aynıdır ama **anlamları alana göre kalibre edilir**:

| Çekirdek alan | Matematikte | Tarihte |
|---|---|---|
| `claim` | Tam ve kesin önerme; kelime tasarrufu yasak | Yorumlanmış iddia; kesinlik iddiası yok |
| `verbatim` | **Zorunlu** — yeniden ifade teoremi bozar (Doktrin 7) | Opsiyonel |
| `epistemic.modality` | Neredeyse hep `analytic` | `empirical` (olay) veya `normative` (yorum) |
| `epistemic.support` | `proved` erişilebilir | `proved` **asla** erişilemez; tavan `strong` |
| `qualifiers` | `assumption` (hipotezler) baskın | `time`, `population`, `geo` baskın |
| `anchor.quote.exact` | Formül dâhil, karakter kaybı yasak | Cümle sınırına yuvarlanabilir |

**Neden tek çekirdekte ısrar ediyoruz:** Ürünün kalbi çapraz-alan transferidir (Doktrin/Bölüm 2). Bir tıp titrasyon mantığının bir optimizasyon problemine bağlanması, ancak iki atomun **aynı biçimde** temsil edilmesiyle mümkündür. Alan başına ayrı şema, `ANALOGOUS_TO` kenarını hesaplanamaz kılardı.

## 9. Yaşam döngüsü (özet)

```
ham metin → normalize akış + edition kimliği (§4.1) → aday atom çıkarımı (§1,§2)
  → granülerlik turu: böl/birleştir (§3.2-3.3) → yoğunluk alarmı (§3.5)
  → çapa doğrulama + quote hash (§4.3) → epistemik etiketleme: kural→llm→insan (§5.2)
  → sert kısıt denetimi; ihlal ⇒ quarantined
  → kenar üretimi (§7) → DAG döngü denetimi + denklik sınıfları (§7.3)
  → çelişki sınıflandırma → Çatışma Kartı (§6) → transfer eşlemesi (belge 07)
```

## 10. Açık sorular

`AÇIK SORU:` **Sözde-sayfa 1800 karakter** doğru sabit mi? Türkçe metinlerde sayfa başına karakter daha yüksek olabilir; dil bazlı sabit (TR ~1900 / EN ~1800) gerekebilir. İlk 20 kitapta ölçülüp kalibre edilmeli.

`AÇIK SORU:` **`credence` ağırlıkları (0.45/0.25/0.20/0.10)** ilk tahmindir. Kullanıcının Çatışma Kartı seçimleriyle öğrenilsin mi, yoksa sabit ve şeffaf mı kalsın? Şeffaflık lehine sabit tutmaya eğilimliyim.

`AÇIK SORU:` **Denklik sınıfı temsilcisi** en iyi çapaya göre mi, en yüksek `credence`'a göre mi seçilmeli? İkisi çeliştiğinde (iyi çapalı zayıf atom vs. çapası sürüklenmiş sağlam atom) kural belirsiz — belge 02 ile kararlaştırılmalı.

`AÇIK SORU:` Bir atom **birden fazla `domain`'e** ait olabilmeli mi (biyomühendislik, matematiksel finans)? `secondary_domains` eklemek `ANALOGOUS_TO` kısıtını (§7.3-5) bulanıklaştırır; ilk sürümde tek alanla gidip ölçmeyi öneriyorum.

`AÇIK SORU:` `qualifiers.value` serbest metin, ama kapsam çelişkisi teşhisi (§6.2-2) "kesişim boş mu" sorusunu soruyor — bu serbest metinle güvenilir yapılamaz. Sık qualifier'lar için denetimli sözlük (controlled vocabulary) gerekiyor; kapsamı belge 08 ile netleşmeli.
