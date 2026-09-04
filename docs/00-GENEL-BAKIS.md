# BookBeast — Genel Bakış

> **Bu tek sayfa yeter.** Altındaki 13 uzman belgesi derinlik içindir; okumak zorunda değilsin.
> Tasarım turu tamamlandı. Kod yazılmadı.

---

## Sistem tek paragrafta

Kitap yüklersin. Sistem onu **fikir atomlarına** ayırır — her biri tek bir iddia taşıyan,
tek başına çürütülebilen, kitaptaki tam yerine çapalanmış bilgi birimleri. Bu atomlar
kütüphanendeki eski atomlarla eşleşir. Sonuç bir hükümdür: *"bu kitabın %94'ü sende var,
şu 11 sayfa yeni."* Ayrıca senin **Açık Sorular Defteri**'ndeki gerçek problemlerine
karşı taranır — cevabı başka bir alandan gelebilir.

---

## Alınan 10 temel karar

| # | Karar | Neden |
|---|---|---|
| 1 | **Atom = tek yüklem.** Bölünemez, çürütülebilir, çapalı. | Bulanık atom bulanık karşılaştırma demek. |
| 2 | **Kip ve destek ayrı eksenler.** "Değer yargısı" bir güven seviyesi değil, iddia türüdür. | İkisini karıştırmak epistemik omurgayı kırar. |
| 3 | **Çelişkide kazanan ilan edilmez.** 5 çelişki tipi + "ayrım noktası" gösterilir. | Hakikat kararı kullanıcınındır, sistemin değil. |
| 4 | **İki ayrı sayı.** Gösterilen `%94` sayfa-ağırlıklı *kütle*; "Bölüm 7'yi oku" hükmü *üst-kuyruktan*. | Tek skora indirmek en büyük hata olurdu. |
| 5 | **LLM tanık değil sanıktır.** Her atom 4 bağımsız kapıdan geçer. | Doğrulanmamış iddia = zehir. |
| 6 | **Doğrulanamayan atom karantinada.** Silinmez ama kenar kuramaz, plana giremez. | Kural 3: reddetme yok. |
| 7 | **Graf çizilmeyecek.** Yerine tek kart + en fazla üç kapı ("iz sürme"). | 50 düğümden sonra graf okunamaz spagettidir. |
| 8 | **Tek PostgreSQL.** pgvector + tsvector + normal tablolarla graf. | Ayrı vektör/graf sistemleri bu ölçekte sadece bakım borcu. |
| 9 | **Kullanıcı emeği kutsal.** El düzeltmeleri ayrı *bindirme* katmanında; yeniden işleme onları bir kez bile ezemez. | Türetilmiş her şey yeniden inşa edilebilir; senin yazdığın değil. |
| 10 | **Transfer eşiği acımasız.** Haftada en fazla 2 kart, çoğu hafta sıfır. | Sahte analoji tüm güveni bitirir. |

---

## Beş ekran, o kadar

```
Bugün          → her gün açılan tek ekran. Ne okuyacaksın ve neden.
Kitap Brifingi → bir kitap işlendikten sonraki hüküm sayfası.
Atom Kartı     → tek fikir + en fazla üç kapı (iz sürme).
Defter         → Açık Sorular. Aktif tavan: 12 soru.
Kütüphane      → arşiv. Nadiren açılır.
```

Motorun tamamı — 19 ilişki tipi, dört eksenli epistemik durum, önkoşul DAG'ı —
kullanıcıya **hiçbir zaman** gösterilmez. Sadece tek bir cümlenin gerekçesine dönüşür.

**Karmaşıklık bütçesi:** her ekranın sabit eleman tavanı var. Tavan yükseltilemez.
Yeni bir şey eklemenin tek yolu eşdeğerini silmektir.

---

## Maliyet ve süre

| Kitap tipi | Süre | Maliyet |
|---|---|---|
| Dijital doğumlu, 400 sayfa | ~15 dk | ~$3 |
| Taranmış, 400 sayfa | ~60 dk | ~$4,5 |

500 kitaplık kütüphane ≈ **$1500–2000, tek seferlik.** Kitap başına bir kez.
Aylık 20 kitap yükleyen biri ≈ $60/ay.

---

## Matematiğin koyduğu 8 aksiyom

Sistem sana sayı söyleyecek. O sayı yanlışsa uygulama **kendinden emin bir yalancı**
olur. Bu yüzden 8 aksiyom ve her biri için otomatik test zorunlu kılındı:

| Aksiyom | Kural | İhlal edilirse kullanıcı ne görür |
|---|---|---|
| A1–A2 | Yenilik ∈ [0,1]; boş kütüphane → 1 | "%127 yeni" |
| **A3** | **Kitap eklemek eski bir kitabı daha yeni gösteremez** | "Kitabın daha yeni oldu" |
| A4 | Yükleme sırası sonucu değiştiremez | Sayılar tekrar üretilemiyor |
| A5 | Aynı kitabı iki kez yüklemek sayıları bozmaz | Kopya PDF her şeyi bozuyor |
| A6 | Puanlar zıplamaz (kararlılık) | Sayı her gün değişiyor |
| A7 | Karışık gömme sürümü → istisna fırlat | Sessizce anlamsız uzaklıklar |
| A8 | Alakasız atom sonucu etkilemez | "Yemek kitabı analizimi etkiledi" |

Ayrıca: belirli koşullarda sistem **yüzde göstermek yerine "bilmiyorum" demek zorunda.**

---

## Cebirin koyduğu tuzak uyarısı

`aynı` ilişkisi geçişli olmalı (A=B, B=C ⟹ A=C) ama LLM'in ürettiği "aynı" geçişli
değildir. Bu **eşik geçişsizliği** felakettir: yanlış birleşme zinciri binlerce farklı
fikri tek yığına çökertir ve sistem *hata vermez*, sessizce saçmalar.

Cebir profesörünün koyduğu kural: birleştirme eşiği (`θ_merge`) yüksek tutulur,
denklik sınıfları perkolasyon eğrisiyle izlenir, sınıf çapı sınırlanır.

Aynı profesör transfer katmanına ölçülebilir bir sınav getirdi:
**iyi analoji, adım adım akıl yürütmeyi koruyandır.** Korumayanı sistem sana
göstermeden önce yakalamak zorunda.

---

## ⚠️ Üç uzmanın bağımsız olarak yakaladığı ortak açık

Üç belge birbirinden habersiz aynı boşluğa işaret etti: **sistemin tüm eşikleri
İngilizce metin varsayıyor.**

- Sözde-sayfa sabiti (1800 karakter) Türkçe'de yanlış olabilir (~1900?)
- Türkçe NLI (doğrulama) kalitesi ölçülmedi
- Çapraz-dil "aynı fikir" tespiti çözülmedi — İngilizce ve Türkçe kitaptaki aynı
  fikir eşleşmezse kütüphanen ikiye bölünür ve yenilik hesabı yalan söyler

**Bu ilk 20 kitapla kalibre edilmeli.** Kod yazmadan önce çözülmesi gerekmiyor,
ama ölçülmeden "tamam" denemez.

---

## Uzmanlar arası çözülmesi gereken 6 düğüm

| Düğüm | Kim sordu | Kim karar verecek |
|---|---|---|
| Denklik sınıfı temsilcisi: en iyi çapa mı, en yüksek güven mi? | 01 | 02 |
| Kanonik kavram sözlüğü: elle küratörlü mü, kütüphaneden büyüyen mi? | 05a | 01 |
| Atom bölünüp birleşirse kullanıcı düzeltmesi nereye tutunur? | 08 | 01 |
| Aktif soru tavanı 12 doğru sayı mı? | 06 | 07 |
| 24 rollük sözlük sanat atomlarına oturuyor mu? | 07 | 05d |
| Eşikler (θ_hi/θ_lo/θ_merge) ne olacak? | 02 | ölçüm (ilk 50 kitap) |

Hiçbiri mimariyi değiştirmiyor — hepsi kalibrasyon ve sınır çizme işi.

---

## Sırada ne var

1. **Yukarıdaki 6 düğümü kapat** (kısa bir tur, kod gerektirmez)
2. **Türkçe kalibrasyon planı** — hangi 20 kitapla ölçüleceğine karar ver
3. **İskelet kurulum** — `docker compose up` ile ayağa kalkan boş Next.js + Postgres
4. **Tek kitaplık dikey dilim** — bir kitap → atomlar → doğrulama → brifing sayfası

En kritik risk mimaride değil, **çıkarım kalitesinde**. Bu yüzden 4. adım
(tek kitap uçtan uca) her şeyden önce gelmeli: fikir orada ya çalışır ya çalışmaz.

---

## Belge dizini

| Belge | Uzman |
|---|---|
| `uzmanlar/01-bilgi-modeli.md` | Bilgi Mimarı & Epistemolog |
| `uzmanlar/02-yenilik-ve-graf.md` | Uygulamalı Matematikçi |
| `uzmanlar/03-dogrulama.md` | Doğrulama Mühendisi |
| `uzmanlar/04-mimari.md` | Kıdemli Sistem Mühendisi |
| `uzmanlar/05a-matematik-muhendislik.md` | Mühendislik Profesörü |
| `uzmanlar/05b-tip.md` | Kanıta Dayalı Tıp Araştırmacısı |
| `uzmanlar/05c-tarih-felsefe.md` | Tarihçi & Analitik Filozof |
| `uzmanlar/05d-sanat-anlati.md` | Sanatçı & Anlatı Tasarımcısı |
| `uzmanlar/06-arayuz.md` | Ürün Tasarımcısı |
| `uzmanlar/07-transfer.md` | Ar-Ge Direktörü |
| `uzmanlar/08-veri-sistemi.md` | Veri Sistemleri Tasarımcısı |
| `uzmanlar/09-cebirsel-temeller.md` | Saf Matematik Profesörü I |
| `uzmanlar/10-analitik-titizlik.md` | Saf Matematik Profesörü II |
| `00-ORTAK-BRIFING.md` | Hepsinin uyduğu doktrin |
