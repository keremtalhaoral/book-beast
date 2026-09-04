# BookBeast — Ortak Brifing

> Bu belgeyi projedeki **her uzman** okur. Tasarım kararlarının ortak zemini budur.
> Kendi belgeni yazmadan önce burayı oku ve buradaki doktrine uy.

---

## 1. Uygulama nedir?

Kullanıcı kitap yükler (matematik, mühendislik, tıp, tarih, felsefe, sanat, kişisel gelişim).
Sistem her kitabı **olağanüstü bir derinlikte** sindirir, önceki kitaplarla **bağ kurar**,
ve kullanıcıya **sade, tek kararlık** bir okuma planı verir.

Bu bir "kitap özetleyici" **değildir**. Özet çıkarmak ticari olarak değersizdir.

## 2. Uygulamayı benzersiz kılan tek şey: TRANSFER

Sistem "bu kitap ne anlatıyor?" sorusunu sormaz. Şunu sorar:

> "Kullanıcının şu an üzerinde çalıştığı açık problemler var.
>  Bu kitap onlardan hangisine ne veriyor?"

Kullanıcı **Açık Sorular Defteri** tutar (üzerinde çalıştığı gerçek problemler).
Her kitap bu deftere karşı indekslenir. Tıptaki bir titrasyon mantığı, mühendislikteki
bir optimizasyon problemine çözüm önerebilir. Bu çapraz-alan sıçraması ürünün kalbidir.

## 3. Kullanıcı kim?

Ağırlıklı olarak **matematik ve mühendislik** okuyan biri. Zaman zaman tarih, felsefe,
sanat, tıp, kişisel gelişim de okuyor ve bu bilgiyi **işe dönüştürmek** istiyor.
Ciddi, iddialı, uzun vadeli bir okuyucu. Kafasının karışmasından nefret ediyor.

## 4. Sarsılmaz doktrin (4 kural — hiçbir tasarım bunları ihlal edemez)

| # | Kural | Anlamı |
|---|-------|--------|
| 1 | **Bir ekran = bir karar** | Aynı anda 3'ten fazla seçenek gösterilmez. Derinlik hep bir tık ötede durur, asla önde değil. |
| 2 | **Kaynaksız cümle yok** | Her iddia kitap + bölüm + sayfa çapası taşır. Çapasız üretim yasak. |
| 3 | **Reddetme yok, sıkıştırma var** | Sistem asla "bu kitabı okuma" demez. "Bu kitabın şu 11 sayfasını oku" der. Tek bir değerli bakış açısı bile kitabı önemli kılar. |
| 4 | **Günlük plan tek satır** | 1 kitap + 1 somut eylem. Fazlası kafa karıştırır. |

## 5. Dört katmanlı mimari

```
KATMAN 1 — SİNDİRİM    Kitap → "fikir atomları"
                       (iddia / tanım / teorem / yöntem / formül / anekdot)
                       Her atom sayfa çapalı.

KATMAN 2 — BAĞLANTI    Atomlar birbirine bağlanır:
                       aynı · çelişiyor · önkoşulu · genellemesi · uygulaması · çürütüyor

KATMAN 3 — TRANSFER    Atomlar kullanıcının Açık Sorular Defteri'ne eşlenir.
                       ← ürünü benzersiz kılan katman

KATMAN 4 — SUNUM       Tek karar, tek ekran, sıfır kafa karışıklığı.
```

## 6. "Yenilik" ve "gereksiz kitap" nasıl ele alınır?

Yeni kitabın atomları mevcut atom grafına karşı eşlenir. Çıktı **kitap seviyesinde değil,
bölüm/fikir seviyesinde** bir hükümdür:

> "Bu kitabın %94'ü zaten kütüphanende var — 5 farklı kitaptan.
>  Ama Bölüm 7'de daha önce hiç görmediğin bir şey var: 11 sayfa. Sadece onu oku."

## 7. Matematik ve mühendislik için özel titizlik

Yanlış özetlenen bir tarih anekdotu can sıkıcıdır; **yanlış özetlenen bir teorem zehirlidir.**

- Formüller sembolik olarak doğrulanır (SymPy — birim ve tutarlılık testi)
- Teoremlerin **önkoşulları** çıkarılır → önkoşul DAG'ı ("Bölüm 9 için önce ölçü teorisi lazım")
- Doğrulanamayan her şey açıkça `[doğrulanamadı]` etiketi taşır
- Sistem asla emin olmadığı bir şeyi eminmiş gibi sunmaz

## 8. Teknik zemin

- **Web uygulaması** — Next.js + TypeScript (mobil tarayıcıda da çalışır)
- **Açık kaynak** — MIT lisansı, temiz commit geçmişi, herkesin kurabileceği kalitede
- Kullanıcının kitapları gizlidir; veri egemenliği kullanıcıdadır
- LLM sağlayıcısı: Anthropic Claude API (model seçimi maliyet analizine tabidir)

## 9. Belgeni nasıl yazacaksın?

- **Türkçe** yaz. Teknik terimlerin İngilizce karşılığını parantezde ver.
- **Somut ol.** "İyi bir veri modeli olmalı" değil; şemayı yaz, alanları say, örnek ver.
- **Karar ver.** Seçenek listeleme, seçimini yap ve gerekçesini bir cümlede söyle.
- **Kısa tut.** 250–450 satır arası hedefle. Dolgu cümle yok.
- Belgenin başına **"3 cümlelik özet"** koy — kullanıcı sadece onu okuyacak.
- Emin olmadığın yeri açıkça `AÇIK SORU:` diye işaretle.
- Kod yazma. Bu tur **sadece tasarım** turu. Şema, sözde-kod, tablo ve diyagram serbest.

## 10. Uzman kadrosu (kimin ne yazdığını bil, tekrar etme)

| Belge | Uzman |
|---|---|
| `01-bilgi-modeli.md` | Bilgi Mimarı & Epistemolog |
| `02-yenilik-ve-graf.md` | Uygulamalı Matematikçi (Graf & Bilgi Erişimi) |
| `03-dogrulama.md` | Doğrulama Mühendisi (Biçimsel Yöntemler) |
| `04-mimari.md` | Kıdemli Sistem Mühendisi |
| `05a-matematik-muhendislik.md` | Mühendislik Profesörü |
| `05b-tip.md` | Kanıta Dayalı Tıp Araştırmacısı |
| `05c-tarih-felsefe.md` | Tarihçi & Analitik Filozof |
| `05d-sanat-anlati.md` | Sanatçı & Anlatı Tasarımcısı |
| `06-arayuz.md` | Ürün Tasarımcısı (Sadelik Doktrini) |
| `07-transfer.md` | Ar-Ge Direktörü (Transfer Stratejisti) |
| `08-veri-sistemi.md` | Veri Sistemleri Tasarımcısı (DDIA okulu) |
| `09-cebirsel-temeller.md` | Saf Matematik Profesörü I (Cebir & Kategori Teorisi) |
| `10-analitik-titizlik.md` | Saf Matematik Profesörü II (Analiz & Ölçü Teorisi) |

Hepsi `docs/uzmanlar/` altına yazılır.
