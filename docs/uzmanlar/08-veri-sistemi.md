# 08 — Veri Sistemi

> **Veri Sistemleri Tasarımcısı (DDIA okulu)**
> Kapsam: depolama, veri yaşam döngüsü, soy (lineage), yeniden işleme, dışa aktarım.
> Kapsam **dışı**: alım boru hattı orkestrasyonu ve servis topolojisi → `04-mimari.md`.

---

## 3 cümlelik özet

Tek bir PostgreSQL örneği (pgvector + tsvector + normal tablolarla graf) bu ölçekte dört erişim deseninin de altından kalkar; ayrı vektör/graf/arama sistemleri kurmak 500 kitaplık tek kullanıcılı bir uygulamada bakım borcundan başka bir şey getirmez. Sistemin **değişmez gerçeği** yalnızca üç şeydir — yüklenen dosyanın baytları, ondan çıkarılan ham metin, ve kullanıcının kendi elleriyle yazdığı/düzelttiği her şey; atomlar, gömmeler, kenarlar ve yenilik puanları dahil geri kalan **her şey silinip sıfırdan yeniden inşa edilebilir olmak zorundadır** ve bu yeniden inşa, kullanıcının el emeğini bir kez bile ezmemelidir. Bunu sağlamak için her türetilmiş kayıt bir **üretim koşusu (derivation run)** kimliği taşır, yeni sürüm eskisinin yanında **kuşak (generation)** olarak inşa edilir ve tek bir atomik işlemle devreye alınır; kullanıcı düzeltmeleri ayrı bir **bindirme (overlay)** katmanında, atom kimliğinden bağımsız çapalarla saklanır.

---

## 1. Depolama motoru seçimi

### Karar

**Tek sistem: PostgreSQL 16+.** Ek uzantı olarak yalnızca `pgvector`. Graf için Apache AGE **kullanılmayacak**; graf, normal ilişkisel kenar tablosu + `RECURSIVE CTE` ile modellenecek. Tam metin için Postgres'in yerleşik `tsvector` + `pg_trgm`'i yeterli. Orijinal dosyalar veritabanında değil, **içerik-adresli dosya deposunda (content-addressed blob store)** tutulacak.

### Ölçek gerçeği — kararın dayanağı

| Büyüklük | 500 kitap için tahmin |
|---|---|
| Sayfa / ham metin | ~200.000 sayfa · ~500 MB |
| Fikir atomu | ~150.000 (ort. 300/kitap) |
| Gömme (1024-d, `halfvec`) | ~300 MB |
| Kenar (k=32 kNN) | ~5M taranan, ~1–2M saklanan |
| Orijinal PDF/EPUB blob | ~10–15 GB |
| **Postgres veri dizini** | **~4–6 GB** |

150 bin vektör, pgvector'ın HNSW indeksi için **küçük**. Tek bir dizüstünde tamamı RAM'e sığar; p95 kNN sorgusu tek haneli milisaniye. Qdrant/Weaviate ayrı bir süreç, ayrı bir yedek, ayrı bir sürüm uyumu ve ayrı bir "iki sistem birbirinden ayrı düştü" hata sınıfı demektir — 150 bin satır için bunların hiçbirini ödemeye değmez.

### Reddedilenler ve nedenleri

| Seçenek | Karar | Gerekçe |
|---|---|---|
| Qdrant / Weaviate / Milvus | **Hayır** | Ölçek 2–3 mertebe altında. Asıl maliyet: atom ile vektörü **tek işlemde (transaction)** tutamamak → çift yazım tutarsızlığı. |
| Neo4j | **Hayır** | Gezinme derinliğimiz 2–3. Cypher'ın kazancı, ikinci bir kayıt sisteminin maliyetini karşılamıyor. |
| Apache AGE | **Hayır** | Postgres içinde olması cazip ama paketleme/sürüm uyumu kırılgan; açık kaynak bir projede "herkesin kurabileceği kalite" doktrinini (Brifing §8) deler. Aynı sorguyu `RECURSIVE CTE` ile yazabiliyoruz. |
| Elasticsearch | **Hayır** | Tam metin aramamız "kitabımda geçen ifadeyi bul" düzeyinde. `tsvector` + `pg_trgm` fazlasıyla yeter; hibrit skorlama zaten SQL'de yapılıyor. |
| Blob'ları `bytea` olarak DB'de | **Hayır** | 15 GB'lık PDF veritabanını şişirir, `pg_dump`'ı kullanılamaz hale getirir, WAL'i patlatır. Dosyalar diskte, DB'de sadece hash + yol. |
| SQLite + sqlite-vec | **Not** | Tek dosyalık, sıfır bağımlılıklı "taşınabilir profil" için gerçek bir aday. Bkz. `AÇIK SORU 1`. |

### Dört erişim deseni, tek motorda

```
İLİŞKİSEL → tablolar, yabancı anahtar, kısıt (constraint)
VEKTÖR    → atom_embedding.vec  halfvec(1024), HNSW (cosine)
GRAF      → atom_edge(src, dst, rel) + RECURSIVE CTE, (src,rel) indeksi
TAM METİN → atom.tsv  tsvector GENERATED + GIN, artı pg_trgm (yazım toleransı)
```

Dördü de **aynı işlemin (transaction) içinde** güncellenebiliyor. DDIA'nın "türetilmiş veriyi ayrı sistemlere dağıtırsan senkronizasyon senin problemin olur" uyarısını bu ölçekte ödemeye gerek yok.

> **Tek istisna:** kenar üretimindeki toplu kNN taraması gerekirse bellek içi bir ANN indeksine (FAISS/hnswlib) çıkarılıp sonuç Postgres'e yazılabilir. Bu bir *hesaplama* aracıdır, kayıt sistemi değildir — kaybolursa kimse fark etmez.

---

## 2. Kayıt sistemi vs. türetilmiş veri

DDIA'nın en pahalıya mal olan ayrımı budur: **kayıt sistemi (system of record)** kaybolursa geri gelmez; **türetilmiş veri (derived data)** kaybolursa yeniden hesaplanır. Bu iki kümeyi karıştıran sistem, ilk model yükseltmesinde ya veriyi kaybeder ya yükseltmeyi yapamaz.

| Veri | Sınıf | Neden | Kaybolursa |
|---|---|---|---|
| Yüklenen dosyanın baytları (PDF/EPUB) | **Kayıt sistemi** | Kullanıcının mülkü, yeniden üretilemez | Telafisi yok |
| Ham çıkarılan metin + sayfa haritası | **Kayıt sistemi (uygulamada)** | Teorik olarak dosyadan türetilir; ama OCR maliyetli ve *deterministik değil* → dondurulur | Yeniden OCR (pahalı, farklı sonuç) |
| Açık Sorular Defteri girdileri | **Kayıt sistemi** | Kullanıcı yazdı | Telafisi yok |
| Kullanıcı düzeltmesi (atom metni düzeltildi) | **Kayıt sistemi** | İnsan emeği | Telafisi yok |
| Kullanıcı hükmü (kenar reddi/onayı, "bu alakasız") | **Kayıt sistemi** | İnsan emeği + eğitim sinyali | Telafisi yok |
| Okuma olayları (okundu, atlandı, süre) | **Kayıt sistemi** | Gözlemlenmiş gerçek, yeniden üretilemez | Telafisi yok |
| Fikir atomları | Türetilmiş | LLM + prompt + ham metin | Yeniden çıkar |
| Gömmeler (embeddings) | Türetilmiş | Model + atom metni | Yeniden hesapla |
| Atom kenarları (aynı/çelişiyor/önkoşul…) | Türetilmiş | kNN + LLM hakemliği | Yeniden kur |
| Önkoşul DAG'ı | Türetilmiş | Kenarların kapanışı | Yeniden kur |
| Yenilik puanları | Türetilmiş | Graf + kütüphane durumu | Yeniden hesapla |
| Transfer eşlemeleri (atom → açık soru) | Türetilmiş | Defter + atomlar | Yeniden kur |
| Günlük plan | Türetilmiş | Hepsinin üstünde | Yeniden kur |
| Formül doğrulama sonuçları | Türetilmiş | SymPy + atom | Yeniden çalıştır |
| Arama indeksleri (HNSW, GIN) | Türetilmiş | Tanımı gereği | `REINDEX` |

### Kural: `DROP` testi

> Sistemde şu komut her an, korkusuzca çalıştırılabilmelidir:
> ```sql
> TRUNCATE atom, atom_embedding, atom_edge, novelty_score,
>          transfer_link, prereq_edge, verification_result CASCADE;
> ```
> ve ardından `bookbeast rebuild --all` çalıştığında sistem, **kullanıcının hiçbir emeği kaybolmadan**, tam olarak eşdeğer bir duruma dönmelidir.

Bu neden hayati?

1. **Model yükseltmesi mümkün kalsın.** Türetilmiş veri kayıt sistemine karışmışsa (ör. kullanıcının düzelttiği metin atom satırının kendisinde tutuluyorsa) yeniden çıkarım "kullanıcıyı ezmeden" yapılamaz; sistem sonsuza dek ilk modelin kalitesine mahkûm olur.
2. **Hata düzeltmesi ucuzlar.** Kenar mantığındaki bir buga geri dönüşlü yama gerekmez: at, yeniden kur.
3. **Yedek küçülür.** Zorunlu yedek yalnızca kayıt sistemi; gerisi hesaplanabilir.
4. **Şema evrimi serbestleşir.** Türetilmiş tabloların göç yolu "yeniden üret"tir (§5).

---

## 3. Veri soyu (lineage) ve yeniden işleme

### 3.1 Her türetilmiş kayıt nereden geldiğini taşır

Merkezî fikir: satır başına 5 tane sürüm sütunu serpiştirmek yerine, **tek bir üretim koşusu (derivation run) kaydı** ve ona işaret eden bir yabancı anahtar.

```sql
-- Değişmez: bir kez yazılır, asla UPDATE edilmez.
CREATE TABLE derivation_run (
  run_id          uuid PRIMARY KEY,
  task            text NOT NULL,        -- 'atom_extract' | 'embed' | 'edge_judge' | 'novelty' | 'verify'
  model_id        text NOT NULL,        -- 'claude-<x>-<y>' | 'text-embed-<x>' | 'sympy-1.13'
  prompt_id       text,                 -- 'atom_extract.math'
  prompt_version  text,                 -- semver + git sha:  '4.2.0+a91f3c'
  code_version    text NOT NULL,        -- çıkarıcı kodunun git sha'sı
  params          jsonb NOT NULL,       -- temperature, chunk boyutu, k, eşikler
  params_hash     text NOT NULL,        -- yukarıdakilerin kanonik hash'i  → idempotency
  input_ref       text NOT NULL,        -- kaynak sürümü: source_text.content_hash
  started_at      timestamptz NOT NULL,
  finished_at     timestamptz,
  status          text NOT NULL,        -- running | succeeded | failed
  token_cost      integer,
  usd_cost        numeric(10,4)
);

-- Türetilmiş her tablo bu ikiliyi taşır:
--   produced_by uuid NOT NULL REFERENCES derivation_run(run_id)
--   generation  integer NOT NULL
```

Böylece "bu atom neden böyle çıktı?" sorusunun cevabı tek bir `JOIN`: hangi model, hangi prompt sürümü, hangi kod sha'sı, hangi kaynak metin hash'i, ne kadara mal oldu.

### 3.2 Eski ve yeni sürüm yan yana: kuşak (generation) modeli

Yeniden işleme **yerinde (in-place) yapılmaz**. Yeni kuşak, eskisinin yanında inşa edilir; kullanıcı boyunca eski kuşağı görür; bitince tek bir satır güncellemesiyle geçiş yapılır.

```sql
CREATE TABLE book (
  book_id            uuid PRIMARY KEY,
  content_hash       text NOT NULL UNIQUE,   -- dosyanın sha256'sı → idempotency
  title              text, author text, edition text,
  active_generation  integer NOT NULL DEFAULT 0,   -- OKUYUCULAR SADECE BUNU GÖRÜR
  building_generation integer,                     -- inşa hâlindeki (NULL = inşa yok)
  created_at         timestamptz NOT NULL
);

CREATE TABLE atom (
  atom_id     uuid PRIMARY KEY,
  book_id     uuid NOT NULL REFERENCES book,
  generation  integer NOT NULL,
  atom_key    text NOT NULL,       -- KUŞAKLAR ARASI KİMLİK (bkz. 3.3)
  kind        text NOT NULL,       -- iddia|tanım|teorem|yöntem|formül|anekdot
  anchor      jsonb NOT NULL,      -- {chapter, page_start, page_end, char_span, quote}
  body        text NOT NULL,
  payload     jsonb NOT NULL,      -- türe özgü alanlar (bkz. §5)
  payload_schema_version int NOT NULL,
  produced_by uuid NOT NULL REFERENCES derivation_run,
  UNIQUE (book_id, generation, atom_key)
);

-- Tüm okuma yolu bu görünümden geçer. Uygulama koduna ham `atom` yasak.
CREATE VIEW atom_live AS
  SELECT a.* FROM atom a
  JOIN book b ON b.book_id = a.book_id AND b.active_generation = a.generation;
```

Yeniden işleme akışı:

```
1. book.building_generation = active_generation + 1
2. Yeni kuşak atomları/gömmeleri/kenarları YAZILIR (kullanıcı hiçbirini görmez)
3. Kapı kontrolleri (gate) çalışır: §9'daki kalite eşikleri
4. Kullanıcı bindirmeleri (overlay) yeni kuşağa EŞLEŞTİRİLİR
5. TEK İŞLEM:  UPDATE book SET active_generation = building_generation,
                              building_generation = NULL
6. Eski kuşak N-1 tur boyunca saklanır (geri alma), sonra çöp toplama
```

Kullanıcı adım 5'in öncesinde tutarlı bir eski dünya, sonrasında tutarlı bir yeni dünya görür. **Yarı-işlenmiş bir kitap asla ekranda görünmez.** 500 kitap sırayla, kitap kitap geçirilir — bir kitabın başarısız olması diğerlerini bloke etmez.

> Kuşak, kitap başına ilerler. Kütüphane çapında tutarlılık gerektiren tek şey yenilik puanlarıdır; o da §6'daki `library_version` ile ayrıca yönetilir.

### 3.3 Kullanıcı emeğini korumak — bindirme (overlay) katmanı

**Kural: LLM'in yazdığı satıra kullanıcı asla yazmaz; kullanıcının yazdığı satırı LLM asla ezmez.** İki ayrı tablo, iki ayrı kayıt sınıfı.

```sql
CREATE TABLE user_override (
  override_id   uuid PRIMARY KEY,
  kind          text NOT NULL,   -- 'atom_edit' | 'atom_delete' | 'atom_pin' | 'atom_create'
                                 -- | 'edge_reject' | 'edge_confirm' | 'edge_create'
                                 -- | 'transfer_reject' | 'anchor_fix'
  -- ATOM KİMLİĞİNE DEĞİL, ÇAPAYA BAĞLANIR:
  target        jsonb NOT NULL,  -- {book_content_hash, page_start, page_end,
                                 --  quote_norm, claim_fingerprint, embedding_ref}
  patch         jsonb NOT NULL,  -- ne değişti (alan bazlı, tam satır değil)
  note          text,
  created_at    timestamptz NOT NULL,
  -- yeniden eşleşme durumu:
  bound_atom_key text,           -- son başarılı eşleşme
  match_state   text NOT NULL,   -- 'bound' | 'ambiguous' | 'orphaned'
  match_score   real
);
```

Kritik tasarım noktaları:

1. **Bindirme, `atom_id`'ye bağlanmaz.** `atom_id` her kuşakta yenidir; ona bağlanan her düzeltme ilk yeniden işlemede yetim kalır. Bağlanma noktası **çapa + parmak izidir**:
   `claim_fingerprint = simhash(normalize(atom.body))` ve `anchor = (content_hash, page aralığı, normalize edilmiş alıntı)`.
2. **`atom_key` deterministiktir:** `atom_key = blake3(book.content_hash ‖ chapter ‖ page_start ‖ normalized_quote)[0:16]`. Model değişse bile aynı sayfadaki aynı cümleden çıkan atom **aynı anahtarı alır** → düzeltmelerin çoğu (tahmin: %75–85) bedava eşleşir.
3. **Eşleşmeyenler için üç aşamalı geri düşüş:**
   `atom_key` tam eşleşme → sayfa aralığı örtüşmesi + gömme kosinüsü ≥ 0.88 → başarısız.
4. **Başarısız eşleşme SESSİZCE DÜŞÜRÜLMEZ.** `match_state='orphaned'` olur ve **Uzlaştırma Kutusu (reconciliation inbox)** denen bir ekranda kullanıcıya gösterilir: "Şu düzeltmeni yapmıştın, yeni sürümde karşılığını bulamadım. Şuna mı aitti? [en yakın 3 aday] / Sil / Sakla." Yetim bindirme **asla otomatik silinmez** — kullanıcı silene kadar tabloda durur.
5. **Reddedilen kenarlar kenar id'sine değil, imzaya bağlanır:**
   `edge_signature = (src_claim_fingerprint, dst_claim_fingerprint, relation)`. Yeniden işleme aynı ilişkiyi yeniden ürettiğinde, filtre bu imzaya bakar ve kenarı ölü doğurur. Kullanıcının "hayır, bunlar aynı şey değil" demesi **kalıcıdır**; her yükseltmede aynı yanlış kenarı yeniden reddetmek zorunda kalmak affedilmez bir tasarım hatasıdır.
6. **Okuma yolu bindirmeyi uygular:** `atom_live` üstüne `atom_effective` görünümü — türetilmiş satır + bağlı bindirme yaması. Kullanıcı arayüzünde düzeltilmiş alan "senin düzeltmen" rozetiyle işaretlenir, yeniden çıkarım onu değiştiremez.
7. **Bindirmeler dışa aktarımın birinci sınıf parçasıdır** (§7) ve `DROP` testinde asla silinmez.

> Bonus: `user_override` tablosu aynı zamanda ücretsiz bir **değerlendirme kümesidir (eval set)**. Yeni prompt sürümü, kullanıcının geçmişte düzelttiği yerleri düzelterek mi üretiyor? Bu, model yükseltmesinin en dürüst testi.

---

## 4. Olay günlüğü (event log)

### Karar: **Kısmî evet.** Tam olay kaynaklı (event-sourced) mimari **reddedildi**; kayıt sınıfı olaylar için değişmez ekleme-only günlük **kabul edildi**.

### Reddedilen: "tüm durum olay akışından türetilir"

Getirisi (zaman içinde geri alma, tam denetim izi, yeniden yansıtma) gerçek; ama maliyeti bu ürüne oturmuyor:

- Ekranı çizmek için yılların olay akışını yeniden oynatmak, anlık görüntü (snapshot) mekanizması eklemeyi zorunlu kılar — ve o anlık görüntü zaten mevcut durum tablolarıdır.
- Olay şeması evrimi durum şeması evriminden **daha zordur**: eski olay hiç değiştirilemez, yeni kod hepsini okumak zorundadır. §5'in karmaşıklığını ikiye katlar.
- "Hesabımı sil" ile değişmez günlük doğrudan çatışır (§7).

### Kabul edilen: iki sınıf olay, tek `event_log` tablosu

```sql
CREATE TABLE event_log (
  seq         bigserial PRIMARY KEY,      -- toplam sıra (total order)
  occurred_at timestamptz NOT NULL,
  actor       text NOT NULL,              -- 'user' | 'system'
  type        text NOT NULL,
  subject     jsonb NOT NULL,             -- {book_content_hash, atom_key, ...}
  payload     jsonb NOT NULL,
  schema_ver  int NOT NULL
);
```

| Olay sınıfı | Örnekler | Günlükteki rolü |
|---|---|---|
| **A — Kayıt sistemi olayları** | `book.uploaded`, `question.added`, `atom.edited`, `edge.rejected`, `reading.completed`, `plan.accepted` | **Otoritatif.** `user_override`, `open_question`, `reading_log` tabloları bu akışın materyalize görünümüdür. Kaybolursa telafi yok → yedeğin çekirdeği. |
| **B — Sistem olayları** | `run.started`, `run.failed`, `generation.promoted`, `novelty.recomputed` | **Sadece denetim + tetikleyici.** Durum türetilmez; teşhis ve §6'nın kirli-küme kuyruğu için kullanılır. 180 gün sonra budanabilir. |

Somut faydalar: **"Neden bu?" ekranı** (bir öneriyi üreten koşu + olay zinciri gösterilir — Brifing §7'nin dürüstlük kuralı denetlenebilir olur); **yükseltme regresyon testi** (A sınıfı olayları yeni model üstünde yeniden oynat, kullanıcı aynı şeyleri yeniden düzeltmek zorunda mı?); **felaket kurtarma** (A sınıfı olaylar + blob'lar = kullanıcı kaybı sıfır).

**Maliyet:** ~20–50 bin olay/yıl, birkaç yüz MB. İhmal edilebilir. Kabul.

---

## 5. Şema evrimi

### Karar: **melez.** Katı çekirdek + JSONB gövde + sürümlü JSON Schema.

`01-bilgi-modeli.md`'nin "fikir atomu" şeması kesinlikle değişecek (yeni atom türleri, yeni alanlar, teoremlerin önkoşul yapısının derinleşmesi). İki uçtan da kaçınıyoruz: her alan için `ALTER TABLE` (evrim yavaş, göç riskli) ve her şey JSONB (kısıt yok, sessiz bozulma).

```
KATI ÇEKİRDEK (sütun, kısıtlı, indeksli) — nadiren değişir
  atom_id · book_id · generation · atom_key · kind · anchor · body
  produced_by · payload_schema_version · confidence · verified_state

ESNEK GÖVDE (payload jsonb) — sık değişir
  kind='teorem'  → {hypotheses[], statement, prerequisites[], proof_sketch_ref}
  kind='formül'  → {latex, symbols{}, units{}, sympy_check, domain_constraints}
  kind='yöntem'  → {steps[], preconditions[], failure_modes[]}
  kind='anekdot' → {actors[], period, relevance_hint}
```

**Doğrulama:** `payload`, `atom_schema/<kind>/v<N>.json` (repoda, git'te sürümlü) JSON Schema'sına karşı **yazma anında** doğrulanır. Postgres `CHECK` kısıtı yalnızca kaba şeyleri tutar (`kind` enum'u, `anchor` zorunlu alanları); asıl doğrulama uygulama sınırında ve CI'da.

### Uyumluluk kuralları

| Yön | Kural |
|---|---|
| **Geriye (backward)** — yeni kod, eski veriyi okur | Okuma yolunda `upcast(payload, from_version → current)` saf fonksiyonu. Tembel (lazy) yükseltme: veri diskte eski kalabilir. |
| **İleriye (forward)** — eski kod, yeni veriyi okur | Tanımadığı alanları **kaybetmeden yoksayar**. Kısmî güncelleme hiçbir zaman tam satır yazımıyla yapılmaz (`jsonb_set`, tam `payload` değişimi değil). |

### Değişiklik sınıfları ve göç stratejisi

| Sınıf | Örnek | Strateji |
|---|---|---|
| **Ekleme** (alan eklendi, opsiyonel) | `formül.units` | Şema sürümünü artır, `upcast` varsayılan koyar. **Göç yok.** |
| **Yeniden adlandırma / tip değişimi** | `page` → `page_range` | **Genişlet–Göç Et–Daralt (expand–migrate–contract):** ① yeni alanı ekle, iki alana da yaz; ② arka planda geri doldur; ③ okuyucular yeni alana geçtikten sonra eskiyi kaldır. Üç ayrı dağıtım. |
| **Anlamsal değişim** (alanın anlamı değişti) | `confidence` ölçeği değişti | **Göç etme, yeniden üret.** Türetilmiş veri; yeni kuşak koş. |
| **Yeni atom türü** | `kind='karşı-örnek'` | Ekleme; eski kod bilmediği türü listeler ama özel görünüm vermez. |

**Çekirdek sütun değişikliği** (nadir) tek yol: `expand–migrate–contract`, her adımı ayrı bir sürümde, geri alınabilir. Türetilmiş tablolarda ise varsayılan strateji **`DROP` + yeniden üret**'tir — bu, §2'deki ayrımın en somut kazancıdır: şema göçünün %90'ı hiç yazılmaz.

**Göç dosyaları:** ileri (`up`) *ve* geri (`down`) yazılır, CI'da gerçek bir 500-kitaplık üretim anlık görüntüsünün kopyası üstünde çalıştırılır. Geri alınamayan göç birleştirilmez (merge edilmez).

---

## 6. Toplu vs. akış işleme — yenilik puanları

### Problem

Yenilik, mutlak değil **ilişkiseldir**: bir atomun yeniliği kütüphanenin geri kalanına göre tanımlıdır. Yeni bir kitap eklendiğinde, o kitapla örtüşen **eski** atomların yeniliği de düşer (monotonluk). Naif çözüm — her yüklemede 150 bin atomu yeniden puanlamak — 500. kitapta dakikalar sürer ve enerjinin çoğu hiç değişmeyen puanlara harcanır.

### Karar: **artımlı akış + periyodik uzlaştırma toplu işi** (DDIA'nın "türetilmiş veri = materyalize görünüm, batch job doğruyu geri getirir" düzeni)

| Ne zaman | Ne çalışır |
|---|---|
| **Yükleme anında** (saniyeler–dakikalar) | Yeni kitabın atomları puanlanır; **kirli küme (dirty set)** hesaplanır ve kuyruğa yazılır. Kullanıcı yeni kitabın hükmünü hemen görür. |
| **Yükleme sonrası artımlı iş** | Kirli kümedeki *eski* atomların puanları güncellenir. Sınırlı yayılma. |
| **Haftalık toplu iş** | Tüm kütüphane sıfırdan yeniden puanlanır; artımlı hesaptaki sapma düzeltilir. 150k atom için tek makinede dakikalar. |
| **Sorgu anında** | **Hiçbir şey.** Puan okunur, hesaplanmaz. |

Sorgu anında hesaplama reddedildi: ekran gecikmesini modele bağlar, aynı ekran iki kez farklı sayı gösterebilir, ve Brifing §1'in "sade, tek kararlık" vaadi kararsız sayılarla çelişir.

### Kirli küme: yayılmayı sınırlamak

Anahtar gözlem: yeni bir atom yalnızca **kendisine benzeyen** atomların yeniliğini değiştirebilir.

```
yeni_atomlar  A_new   (~300 adet)
for a in A_new:
    N(a) = kNN(a, k=64, cosine ≥ 0.72)      -- pgvector, ~ms
kirli = ⋃ N(a)  ∪  1-adım graf komşuları
```
Tipik `|kirli|` ≈ 3.000–15.000 (150.000 değil). Bu, tam yeniden hesabın ~%5–10'u.

```sql
CREATE TABLE novelty_score (
  atom_key            text NOT NULL,
  book_id             uuid NOT NULL,
  score               real NOT NULL,          -- 0..1
  computed_at         timestamptz NOT NULL,
  library_version     bigint NOT NULL,        -- hangi kütüphane durumuna göre
  method_version      text NOT NULL,          -- puanlama algoritmasının sürümü
  is_stale            boolean NOT NULL DEFAULT false,
  PRIMARY KEY (atom_key, book_id)
);

CREATE TABLE recompute_queue (       -- kirli küme kuyruğu
  atom_key text PRIMARY KEY,
  reason   text,                     -- 'new_neighbor' | 'edge_changed' | 'override' | 'full_sweep'
  enqueued_at timestamptz NOT NULL
);
```

`library_version`, kütüphaneye atom ekleyen/çıkaran her işlemde artan tek bir sayaçtır. Bir puanın `library_version`'ı güncel sayaçtan geriyse o puan **bayattır** ve arayüz bunu bilir.

### Arayüzün gördüğü şey

İki farklı sayı, ikisi de dürüst:

- **"Eklediğinde"** — `score @ library_version = V_k`, dondurulmuş, asla değişmez. Kitap kartında tarihsel kayıt olarak durur.
- **"Şimdi"** — güncel puan. Değişirse kullanıcı bir bildirim görür: *"Yeni eklediğin 3 kitap yüzünden X'in %94'lük örtüşmesi %97'ye çıktı — kalan 6 sayfa hâlâ okunmaya değer."*

Bu, monotonluğu **gizlemek** yerine ürün özelliğine çevirir; Brifing §6'nın kitap-değil-bölüm seviyesindeki hükmüyle de örtüşür.

### Materyalize görünüm mü, artımlı hesap mı?

**İkisi de, katman katman:**
- `novelty_score` = elle yönetilen materyalize görünüm (artımlı güncellenir). Postgres'in `MATERIALIZED VIEW`'ü kullanılmaz: `REFRESH` tam yeniden hesap yapar, artımlı değildir.
- Kitap/bölüm seviyesindeki toplamalar (`book_overlap_pct`, `chapter_novelty`) ise **gerçek `MATERIALIZED VIEW`**'dür — atom puanlarından ucuzca toplanır, kirli kitaplar için yenilenir.

---

## 7. Veri egemenliği ve dışa aktarım

> Bu bir özellik değil, **ahlaki zorunluluk**. Kullanıcı kitaplarını ve düşünce grafını bu uygulamadan **daha uzun süre** yaşatabilmelidir.

### İki dışa aktarım profili

| Profil | İçerik | Boyut (500 kitap) | Amaç |
|---|---|---|---|
| **`portable`** (varsayılan) | Yalnızca **kayıt sistemi**: blob'lar, ham metin, defter, bindirmeler, A sınıfı olaylar | ~16 GB | Taşınma, yedek. Türetilmiş veri hedef makinede yeniden kurulur. |
| **`full`** | `portable` + tüm türetilmiş tablolar + gömmeler + koşu geçmişi | ~22 GB | Bit-bit aynı duruma dönmek; yeniden LLM maliyeti ödemeden geri yükleme. |

### Format: dizin/tarball, açık ve okunabilir

```
bookbeast-export-2026-09-04/
  MANIFEST.json          # şema sürümü, sayımlar, üretim zamanı, bütünlük hash'i
  README.md              # formatın insan-okur açıklaması (BookBeast olmadan da anlaşılır)
  blobs/
    sha256/ab/cd/abcd…ef.pdf         # içerik-adresli, orijinal baytlar, değiştirilmemiş
  source_text/
    abcd…ef.jsonl                    # sayfa başına {page, text, char_offset}
  records/                           # KAYIT SİSTEMİ — hepsi JSONL, UTF-8, satır başına 1 nesne
    books.jsonl  open_questions.jsonl  user_overrides.jsonl
    reading_log.jsonl  events.jsonl
  derived/                           # yalnızca `full` profilinde
    atoms.jsonl  edges.jsonl  novelty.jsonl  transfer_links.jsonl
    embeddings.parquet               # atom_key, model_id, vec[]
    derivation_runs.jsonl
  schemas/                           # her JSONL'in JSON Schema'sı, sürümüyle
  CHECKSUMS.txt
```

Tasarım kararları:
- **JSONL, `pg_dump` değil.** `pg_dump` bir Postgres sürümüne bağlar; JSONL'i `jq` ile okuyabilir, pandas'a verebilir, 20 yıl sonra açabilirsin. (`pg_dump` yine de `full` içinde *ek* olarak bulunur, hız için.)
- **Blob'lar dokunulmadan.** Kullanıcının PDF'i çıktı içinde açılabilir bir PDF olarak durur; formatı bilmeyene bile işe yarar.
- **Kendini açıklayan.** `README.md` + `schemas/` sayesinde dışa aktarım, uygulamadan bağımsız bir arşivdir.
- **Aşamalı (streaming) yazım.** 22 GB'ı belleğe almadan, tabloları imleçle (cursor) gezerek yazar; `MANIFEST.json` en son yazılır (yarım kalan dışa aktarım geçersiz kalır).
- **Şifreleme opsiyonel:** `--encrypt` ile age/gpg. Varsayılan kapalı — kullanıcı ne aldığını görebilmeli.

### Geri yükleme (restore)

```
bookbeast restore ./bookbeast-export-2026-09-04
  ① MANIFEST + CHECKSUMS doğrula
  ② şema sürümü uyumu → gerekiyorsa upcast (§5)
  ③ kayıt sistemi tablolarını yükle, blob'ları içerik hash'iyle yerleştir
  ④ profil=full   → türetilmiş tabloları yükle, indeksleri kur (REINDEX)
     profil=portable → `rebuild --all` kuyruğa alınır (LLM maliyeti burada doğar,
                       kullanıcıya önceden tahmini $ tutarı gösterilir)
  ⑤ bindirmeleri yeniden bağla (§3.3), yetimler Uzlaştırma Kutusu'na
```

**Kabul testi (CI'da her sürümde):** boş bir makinede `restore` → türetilen graf, kaynak makinedeki grafla yapısal olarak eşdeğer; kullanıcı bindirmelerinin %100'ü bağlı. Bu test kırmızıysa sürüm çıkmaz.

### Silme

| Kapsam | Davranış |
|---|---|
| **Bir kitabı sil** | Blob dosyası silinir; `book` satırı **mezar taşına (tombstone)** dönüşür (`content_hash`, `deleted_at` kalır — aynı dosyayı yanlışlıkla yeniden yükleyip yeniden para harcamamak için). Atomlar/kenarlar/puanlar `CASCADE`. Etkilenen komşular kirli kuyruğa. |
| **Bir kitabı sil + izini de sil** | Mezar taşı da gider; `event_log`'daki ilgili olayların `payload`'ı **karartılır (redaction)**: `{redacted_at, reason}`. Olay satırı sıra bütünlüğü için kalır, içeriği gitmiştir. |
| **"Hesabımı sil"** | Blob dizini, veritabanı, indeksler, önbellekler, geçici dosyalar, dışa aktarım artıkları. Tek komut: `bookbeast purge --confirm`. Öncesinde **zorunlu** olarak `portable` dışa aktarım teklif edilir. Sonrasında rapor: silinen bayt/dosya/satır sayısı. |
| **LLM sağlayıcısı** | Anthropic API'ye giden metinlerin sağlayıcıda saklanmama ayarı belgelenir; hangi verinin dışarı çıktığı `PRIVACY.md`'de sayfa sayfa yazılır. Yerel model profili için bkz. `AÇIK SORU 2`. |

Değişmez günlük ile silme hakkı arasındaki gerilim, DDIA'nın da işaret ettiği yerde çözülür: **günlük değişmez kalır, içeriği karartılabilir.**

### Yedekleme

Günlük `pg_dump -Fc` (~1 GB) + blob dizini için `rsync --link-dest` (sabit bağlantılı artımlı); saklama 7 günlük / 4 haftalık / 12 aylık. Aylık otomatik **geri yükleme tatbikatı**: yedek geçici bir DB'ye yüklenir, satır sayıları ve §9.1 bütünlük kontrolleri koşar — *test edilmemiş yedek, yedek değildir.* Blob'lar içerik-adresli olduğu için tekilleştirme (deduplication) bedava.

---

## 8. Tutarlılık ve eşzamanlılık

Bu tek kullanıcılı bir uygulama; eşzamanlılık **insanlar arasında değil, arka plan işleriyle kullanıcı arasında**. Buna göre ölçeklenmiş kararlar:

### Kararlar

| Konu | Karar |
|---|---|
| Varsayılan izolasyon | `READ COMMITTED` (Postgres varsayılanı) |
| Kuşak devreye alma (§3.2 adım 5) | `SERIALIZABLE`, tek ve kısa işlem |
| Puan güncelleme | `READ COMMITTED` + `INSERT … ON CONFLICT DO UPDATE` (upsert) |
| Kitap başına boru hattı dışlaması | `pg_advisory_xact_lock(hashtext(book_id))` |
| Kullanıcı düzenlemeleri | İyimser eşzamanlılık (optimistic): `version` sütunu, `UPDATE … WHERE version = $beklenen`; uyuşmazlıkta arayüz "bu kayıt değişti, yeniden yükle" der |

`SERIALIZABLE`'ı her yere sermek gereksiz: yazma çatışması pratikte yok, ama serileştirme hatası her çağrı yerinde yeniden deneme mantığı gerektirir. Tek kritik nokta (kuşak flip'i) korunur, gerisi ucuz kalır.

### İdempotency — üç seviye

**1. Yükleme (ingest):**
```sql
book.content_hash UNIQUE          -- sha256(dosya baytları)
```
Aynı dosya ikinci kez yüklenirse yeni kitap **yaratılmaz**; mevcut kitabın durumu döner. Kullanıcı "Bu kitap zaten kütüphanende (12 Mart'ta eklendin). Yeniden işlemek ister misin?" mesajını görür. Dosya adı değişse de hash aynıdır.

*Aynı eser, farklı baskı/format* (PDF vs EPUB) farklı hash üretir → farklı kitap. Sistem bunları başlık+yazar+atom örtüşmesiyle sezer ve **kullanıcıya sorar**: "Bu, kütüphanendeki X'in başka bir baskısı olabilir. Birleştireyim mi?" Otomatik birleştirme yok — yanlış birleştirmeyi geri almak pahalıdır.

**2. İş (job) seviyesi:**
```sql
idempotency_key = blake3(task ‖ input_ref ‖ model_id ‖ prompt_version ‖ params_hash)
CREATE UNIQUE INDEX ON derivation_run (idempotency_key) WHERE status <> 'failed';
```
Aynı girdi + aynı model + aynı prompt = **API'ye tekrar gidilmez**, önceki koşunun sonucu kullanılır. Bu hem çökme sonrası yeniden başlatmayı güvenli kılar hem de kısmî yeniden işlemeyi ucuzlatır: prompt'un yalnızca `formül` şablonu değiştiyse, diğer türlerin koşuları önbellekten gelir.

**3. Yazma seviyesi:** tüm türetilmiş yazımlar `(book_id, generation, atom_key)` üzerinde upsert. Yarıda kesilmiş bir kuşak inşası, baştan çalıştırıldığında aynı satırlara yazar; yinelenen üretmez.

### "İşlenirken tekrar yüklendi" senaryosu

```
① content_hash zaten var mı?     → evet
② building_generation NULL mı?   → hayır, inşa sürüyor
③ Kullanıcıya: "Bu kitap şu an işleniyor (%40). İlerlemeyi göster."
   → YENİ İŞ BAŞLATILMAZ. Advisory lock zaten ikinci boru hattını engeller.
④ İnşa çökmüşse (heartbeat > 15 dk sessiz): run 'failed' işaretlenir,
   yarım kuşak satırları silinir (hiç görünmemişlerdi), yeniden başlatılır.
```

### "İki iş aynı atomu güncelliyor" senaryosu

Tasarım gereği **olamaz**: türetilmiş satırlar tek bir kuşak inşası tarafından, tek sahiplikle yazılır. Çakışan tek yer kullanıcı düzenlemesiyle arka plan işidir ve orada kural mutlaktır — **arka plan işi `user_override`'a hiç dokunmaz**; kullanıcı düzenlemesi kuşak satırını değil bindirmeyi yazar. İki yazar, iki ayrı tablo → çatışma yüzeyi sıfır.

---

## 9. Gözlemlenebilirlik ve veri kalitesi

Bu sistem gürültüyle değil **sessizce** bozulur: atomlar yavaşça sığlaşır, gömmeler bayatlar, graf çürür, sayfa çapaları kayar. Ölçülmeyen kalite düşüşü fark edilmez.

### 9.1 Otomatik veri kalitesi kontrolleri (her kuşak inşasından sonra, kapı görevi görür)

| # | Kontrol | Eşik | Aksiyon |
|---|---|---|---|
| 1 | **Çapa kapsamı** — atomların kaçı geçerli sayfa çapası taşıyor | %100 | Kırmızı → kuşak devreye alınmaz (Doktrin 2: kaynaksız cümle yok) |
| 2 | **Çapa doğruluğu** — `anchor.quote`, o sayfanın ham metninde gerçekten geçiyor mu (normalize edilmiş) | ≥ %98 | < %95 → devreye alma bloke |
| 3 | **Sayfa aralığı geçerliliği** — `page_end ≤ kitabın sayfa sayısı` | %100 | İhlal = üretim hatası, koşu başarısız |
| 4 | **Kitap içi yinelenme** — aynı kitapta kosinüs > 0,97 atom çifti oranı | < %3 | Aşımda çıkarım prompt'u parçalama sorunu var demektir |
| 5 | **Atom verimi** — 10 sayfa başına atom sayısı, kitabın türüne göre | ±%40 bant | Bandın dışı → o kitap manuel incelemeye |
| 6 | **Yetim atom** — hiçbir kenarı olmayan atom oranı | < %15 | Yüksekse gömme veya eşik bozulmuş |
| 7 | **Gömme tazeliği** — `model_id ≠ güncel` olan gömme oranı | %0 hedef | > %0 ise karışık uzayda benzerlik ölçülüyor — **sessiz ve tehlikeli** |
| 8 | **Gömme boyut/norm sağlığı** — NaN, sıfır vektör, beklenmeyen boyut | 0 adet | Herhangi biri = koşu başarısız |
| 9 | **Kenar tip tutarlılığı** — `önkoşul` kenarları döngü yaratıyor mu (DAG kontrolü) | 0 döngü | Döngü → kenarlar karantinaya |
| 10 | **Simetri kuralı** — `aynı` ve `çelişiyor` simetrik, `önkoşul`/`genellemesi` antisimetrik | %100 | İhlal düzeltilir, sayısı raporlanır |
| 11 | **Doğrulama kapsamı** — `kind='formül'` atomlarının kaçı SymPy'den geçti / `[doğrulanamadı]` etiketli | Etiketsiz belirsiz = 0 | Brifing §7 |
| 12 | **Bindirme yeniden bağlanma oranı** — yeniden işleme sonrası `bound` olan bindirme % | ≥ %90 | < %75 → yeniden işleme durdurulur, kimlik stratejisi bozuk demektir |
| 13 | **Yetim bindirme birikimi** — Uzlaştırma Kutusu derinliği | < 20 | Büyüyorsa insan emeği çöpe gidiyor |
| 14 | **Yenilik dağılımı kayması** — kuşaklar arası puan dağılımının KS mesafesi | < 0,15 | Aşım → puanlama anlamı değişti, kullanıcıya "yeniden ölçekleme oldu" denir |
| 15 | **Bayat puan oranı** — `library_version < güncel` olan puanlar | < %5 | Kirli kuyruk drenajı geride kalıyor |
| 16 | **Transfer isabet oranı** — önerilen transfer bağlantılarının kullanıcı tarafından reddedilme oranı (kayan 30 gün) | < %40 | Ürünün kalbi burası; trend yukarıysa alarm |
| 17 | **Referans bütünlüğü** — yetim yabancı anahtar, blob'suz kitap, kitapsız atom | 0 | Haftalık tarama |
| 18 | **Blob bütünlüğü** — diskteki dosyanın sha256'sı `content_hash` ile uyuşuyor mu | %100 | Aylık; sessiz disk bozulması (bit rot) yakalar |

### 9.2 Altın küme (golden set) — kalite düşüşünün tek dürüst ölçüsü

Alan başına elle etiketlenmiş **20 atom** (matematik, mühendislik, tıp, tarih, felsefe, sanat = 120 atom) ve **50 kenar hükmü**. Her prompt/model değişiminde otomatik koşulur:

```
altın_kesinlik  = doğru çıkarılan atom / çıkarılan atom
altın_duyarlılık= yakalanan altın atom / tüm altın atom
çapa_hatası     = doğru sayfadan sapma (ortalama |Δsayfa|)
```
Bu üçünden herhangi biri önceki sürüme göre **%5'ten fazla gerilerse yükseltme durur.** Kullanıcının `user_override` geçmişi bu kümeye sürekli beslenir — sistem kendi hatalarından bedava bir test seti üretir.

### 9.3 Kanarya yeniden işleme (canary reprocessing)

500 kitap asla topluca yeniden işlenmez. Sıra:

```
① 10 kitaplık kanarya (alanlar arası çeşitli) → kuşak inşa et, DEVREYE ALMA
② §9.1 kapıları + §9.2 altın küme + eski/yeni yan yana fark raporu
③ Kullanıcı 5 örneği gözle onaylar   ← insan kapısı, atlanamaz
④ Onay → 490 kitap sıraya, kitap başına kapı kontrolü, kitap başına flip
⑤ Herhangi bir kapı kırmızıysa o kitap eski kuşakta kalır, rapora düşer
```

### 9.4 İşletme metrikleri

`run_started`, `run_failed`, kuyruk derinliği, kitap başına p50/p95 süre, kitap başına $ maliyeti, kümülatif $ , API hata/oran-limiti sayacı, ölü mektup kuyruğu (dead-letter) derinliği, DB boyutu, blob dizini boyutu, HNSW sorgu p95, son başarılı yedek yaşı, son başarılı geri yükleme tatbikatı yaşı.

Tek kullanıcılı bir uygulamada Prometheus/Grafana yığını abartıdır: metrikler `metric_sample` tablosuna yazılır, uygulama içindeki tek bir **"Sistem Sağlığı"** ekranında gösterilir. Kırmızı kontrol varsa ana ekranda tek satırlık uyarı belirir — Doktrin 1'i (bir ekran = bir karar) bozmadan.

---

## Açık sorular

- `AÇIK SORU 1:` **Taşınabilir profil.** Postgres kurmak istemeyen bir kullanıcı için SQLite + `sqlite-vec` ile tek dosyalık bir profil mümkün. Aynı mantıksal şemayı iki motorda tutmanın bakım maliyeti, kurulum kolaylığının değerini aşar mı? Karar, ilk 3 dış kullanıcının kurulum deneyimine ertelenmeli.
- `AÇIK SORU 2:` **Yerel gömme modeli.** Gömmeler yerel bir modelle üretilirse (bge-m3 vb.) yeniden işleme maliyeti neredeyse sıfırlanır ve veri hiç dışarı çıkmaz — ama kalite düşer. Ölçülmeden karar verilmemeli; §9.2'nin altın kümesi bu karşılaştırmanın aracıdır.
- `AÇIK SORU 3:` **Kuşak saklama penceresi.** "Son N kuşak saklanır" kuralında N=2 önerildi (~%40 ek türetilmiş depolama). Kullanıcı geri almayı gerçekten kullanıyor mu, yoksa N=1 yeter mi — kullanım verisiyle ayarlanmalı.
- `AÇIK SORU 4:` **Atom kimliği dayanıklılığı.** `atom_key`'in çapa tabanlı tanımı, çıkarıcının atom **granülaritesini** değiştirmesine (bir atomu ikiye bölmek) karşı zayıf. Böl/birleştir olaylarını bindirme eşleştirmesinde nasıl temsil edeceğimiz, `01-bilgi-modeli.md`'nin atom tanımı netleştikten sonra çözülmeli.
