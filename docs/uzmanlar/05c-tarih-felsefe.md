# 05c — Tarih, Felsefe, Siyaset Teorisi ve Strateji

> Uzman: Tarihçi & Analitik Filozof
> Kapsam: felsefe, tarih, siyaset teorisi, sosyal bilimler, strateji.

## 3 cümlelik özet

Bu alanda "fikir atomu" bir cümle değil, bir **yapıdır**: felsefede öncül–çıkarım–sonuç iskeleti, tarihte ise iddianın **epistemik statüsü** (kayıt mı, nedensel yorum mu) atomun kendisi kadar önemlidir. Sistemin bu alandaki iki asli katkısı şunlar: (1) **gizli varsayımları** açığa çıkaran Köprü Denetimi, (2) her tarih iddiasını E0–E5 merdiveninde etiketleyip E3 ve üstünde **yazar atfını zorunlu** kılan olgu/yorum ayrımı. Çürütülmüş ama verimli fikirler (Marx, Freud, Malthus) atılmaz; `çürütüldü/verimli` statüsüyle **düşünce aracı** olarak saklanır ve steelman kuralı gereği her konum en güçlü hâliyle sunulur.

---

## 1. Neden bu alan ayrı bir belge gerektiriyor

Matematikte atom kendini doğrular (teorem ya doğrudur ya değil). Tıpta kanıt hiyerarşisi hazırdır. Tarih ve felsefede ne biri ne öteki var:

| Sorun | Matematikte | Burada |
|---|---|---|
| Doğruluk | İspatla kesin | Argüman gücüyle derecelendirilir |
| Çelişki | Hata sinyali | Çoğu zaman **perspektif farkı** |
| Özet | Sıkıştırma | Sıkıştırma **çarpıtma riski** taşır |
| Kaynak | Formül yeter | Öncül düzeyinde çapa gerekir |

Bu yüzden burada üç mekanizma tasarlanıyor: **argüman haritası**, **epistemik merdiven**, **steelman protokolü**.

---

## 2. Felsefe atomları — 6 tür

Ortak zarf (`01-bilgi-modeli.md`'deki temel alanlar: `id, kitap, bölüm, sayfa, güven, bağlar`) varsayılır. Aşağıda sadece **alana özel ek alanlar** tanımlanıyor.

### 2.1 KAVRAM
```
tür: KAVRAM
ad: "kategorik buyruk"
tanım_metinde: "<yazarın kendi cümlesi, birebir alıntı>" @s.421
işlev: neyi_ayırt_ediyor / hangi_problemi_çözmek_için_icat_edildi
sınır_örnekleri: [ örnek_içeride, örnek_dışarıda ]   ← kavramı yaşatan şey bu
yakın_kavramlar: [ "hipotetik buyruk" (karşıtı), "altın kural" (yakın-ama-değil) ]
```
**Karar:** sınır örnekleri **zorunlu alan**. Sınır örneği olmayan kavram, kullanıcının kafasında tanımdan ibaret kalır ve transfer edilemez.

### 2.2 AYRIM (distinction)
Felsefenin en transfer edilebilir ürünü budur. Ayrı bir tür olarak modellenmesinin sebebi: bir ayrım, iki kavramdan fazladır — bir **kesme aleti**dir.
```
tür: AYRIM
a: "de dicto"          b: "de re"
kesme_ölçütü: "yüklem tanıma mı bağlı, nesneye mi"
neden_önemli: "karıştırılınca hangi hata üretilir" ← zorunlu
karışma_vakası: "<metinden, ayrımın çözdüğü somut kafa karışıklığı>" @s.88
```

### 2.3 ARGÜMAN — ana yapı
```
tür: ARGÜMAN
ad: "Çin Odası"
öncüller:
  - { id: P1, metin: "...", çapa: s.417, kaynak: metinde }
  - { id: P2, metin: "...", çapa: s.418, kaynak: metinde }
  - { id: P3, metin: "...", çapa: —,     kaynak: GİZLİ, türetim: "Köprü Denetimi/Adım1" }
çıkarım:
  biçim: modus_tollens | tümevarım | IBE | analoji | reductio | transandantal
  adımlar: [ "P1+P3 ⇒ ara-sonuç A", "A+P2 ⇒ C" ]
sonuç: { metin: "...", çapa: s.419 }
geçerlilik: geçerli | geçersiz | belirsiz        ← biçim denetimi
öncül_desteği: güçlü | tartışmalı | zayıf         ← içerik denetimi
en_zayıf_halka: P2                                ← zorunlu, tek bir öncül seç
itirazlar: [ atom_id... ]
yazarın_yanıtı: [ atom_id... ]
```
**Karar:** `geçerlilik` ve `öncül_desteği` **ayrı alanlar**. Bir argüman geçerli ama öncülleri yanlış olabilir; kullanıcıya bu iki başarısızlık aynı renkte gösterilmemeli. `en_zayıf_halka` tek değerli — sistem argümanı okuyup nereden kırılacağına karar vermeye mecbur.

### 2.4 DÜŞÜNCE DENEYİ
```
tür: DUSUNCE_DENEYI
kurulum: "<senaryo, 2-3 cümle>" @s.164
sezgi_pompası: "okurdan çekilmek istenen yargı"
hedef_öncül: hangi_argümanın_hangi_öncülünü_destekliyor/yıkıyor
değişkeni_izole_ediyor: "sadece X değişiyor, Y sabit"  ← ablation study ile aynı mantık
sezgiye_itiraz: "sezgi güvenilmez çünkü ..." (varsa)
```

### 2.5 İTİRAZ
```
tür: İTİRAZ
hedef: { atom: arg_042, öncül: P2 }
tipi: karşı_örnek | öncül_reddi | geçersizlik | ikircik(equivocation) |
      kendine_gönderme | kayan_kuantör | sonuç_kabul_edilemez(reductio)
gücü: yıkıcı | budayıcı | rahatsız_edici
yanıtlandı_mı: evet(atom_id) | hayır | kısmen
```

### 2.6 KONUM (position)
Bir yazarın bir soruya verdiği toplu cevap. Argümanların üstünde bir düğüm.
```
tür: KONUM
soru: "Zihin fiziksel midir?"
cevap: "Hayır — işlevsel olarak açıklanamaz artık var"
taşıyıcı_argümanlar: [ arg_042, arg_051 ]
kabul_ettikleri: [ "fizik nedensel olarak kapalıdır" ]  ← rakiple ortak zemin
reddettikleri: [ ... ]
maliyeti: "bu konumu alırsan şundan vazgeçmen gerekir: ..."  ← zorunlu
rakip_konumlar: [ konum_id... ]
```
**Karar:** `maliyeti` zorunlu. Bedelsiz sunulan konum propagandadır; kullanıcı hangi takası yaptığını görmeli.

---

## 3. Argüman haritalama ve gizli varsayımlar

### 3.1 Çıkarma hattı (5 aşama)

1. **İddia avı.** Metindeki sonuç cümlelerini bul (belirteçler: *öyleyse, dolayısıyla, bu nedenle, sonuç olarak, demek ki*). Her sonuç bir argüman çekirdeğidir.
2. **Geriye yürüme.** Sonucun önündeki 1–3 paragrafta destek cümlelerini topla (*çünkü, zira, göz önüne alındığında, varsayalım ki*).
3. **Yeniden yazım.** Her öncülü tek yüklemli, kuantörü açık bir cümleye indir. Retorik süsleri at, **iddia gücünü değiştirme**.
4. **Köprü Denetimi** (aşağıda) → gizli öncüller.
5. **Bağlama.** İtirazlar, yazarın yanıtı, kitaptaki ve kütüphanedeki karşı argümanlar bağlanır.

### 3.2 Köprü Denetimi — gizli varsayımı açığa çıkarma protokolü

Bu belgenin en değerli parçası. Beş mekanik adım; her biri LLM'e ayrı bir soru olarak sorulur, tek promptta değil.

**Adım 1 — Terim envanteri.** Sonuçtaki her ana terimi öncüllerde ara. Öncüllerde *hiç geçmeyen* bir terim varsa, onu bağlayan bir **köprü öncül** gizlidir.
> "Beyin bir bilgisayardır → o hâlde bilinç simüle edilebilir." `simüle edilebilir` öncüllerde yok ⇒ gizli: *"Bilgisayarların yaptığı her şey simüle edilebilir."*

**Adım 2 — Kuantör ve kip denetimi.** Öncüllerde `bazı / çoğu / olabilir` varken sonuçta `tüm / her / -dır` görünüyorsa, aradaki farkı kapatan bir tümevarım varsayımı gizlidir. Bu, sosyal bilimlerde en sık gizli varsayım.

**Adım 3 — Değer sızıntısı (Hume kılıcı).** Sonuç normatifse (*-meli, -malı, haklıdır, meşrudur*) ve hiçbir öncül normatif değilse, gizli bir **değer öncülü** vardır. Onu yaz. Siyaset teorisi kitaplarının %80'inde bu adım bir şey bulur.

**Adım 4 — Yadsıma testi.** Aday varsayımı yadsı ve argümanı yeniden çalıştır. Argüman çöküyorsa varsayım **taşıyıcı**; ayakta kalıyorsa **süs** — süs olanı atoma dönüştürme, gürültü yapar.

**Adım 5 — Dönem denetimi.** Yazım yılı + bibliyografya + o dönemin tartışma gündemi verilir; sorulur: *"Yazarın çağında tartışmasız sayılan, bugün tartışmalı olan hangi kabulü bu argüman kullanıyor?"* (Örn. 19. yy ilerlemeciliği, Soğuk Savaş dönemi devlet-merkezciliği, davranışçılığın hüküm sürdüğü dönemde zihin dili yasağı.)

**Çıktı biçimi.** Bulunan her varsayım kendi atomu olur:
```
tür: VARSAYIM
metin: "Toplumsal kurumlar üyelerinin çıkarlarıyla açıklanabilir"
kaynak: TÜRETİLMİŞ      çapa: —      türetim: KöprüDenetimi/Adım3
taşıyıcı_mı: evet (yadsıma testi: arg_042 çöküyor)
yazar_kabul_eder_mi: muhtemelen(0.8) | reddeder | belirsiz
başka_yerde_geçiyor_mu: [ atom_id... ]   ← aynı gizli varsayımı paylaşan kitaplar
```
**Karar:** `kaynak: TÜRETİLMİŞ` etiketi zorunlu ve arayüzde farklı renkte. Doktrin kuralı 2 (kaynaksız cümle yok) burada şöyle karşılanır: çapa yerine **türetim izi** verilir. Sistem gizli varsayımı yazara ait bir cümle gibi göstermez.

**Ödül:** aynı gizli varsayımı paylaşan atomlar graf üzerinde kümelenince, "kütüphanendeki 6 siyaset kitabı aynı örtük kabul üzerine kurulu" gibi bir içgörü çıkar. Bu, `02-yenilik-ve-graf.md`'nin ölçtüğü "yenilik"in en değerli türüdür.

---

## 4. Tarih atomları ve epistemik merdiven

### 4.1 Beş tür
```
OLAY           : ne, ne zaman, nerede, kim.  alan: tarih_aralığı, aktörler, mekan
NEDEN_İDDİASI  : X → Y.  alan: mekanizma, karşı_olgusal, karşılaştırma_sınıfı
YAPISAL_ÖRÜNTÜ : dönem/eğilim/tip.  alan: kapsam(mekan+zaman), örnekler, karşı_örnekler
NİCEL          : sayı.  alan: değer_aralığı, ölçüm_yöntemi, kaynak_güveni
BİRİNCİL_KAYNAK: alıntı.  alan: belge, tarih, yazan_kim, çıkarı_neydi, hayatta_kalma_yanlılığı
```

### 4.2 E0–E5: epistemik statü merdiveni

Kullanıcının örneği tam olarak bu merdivenin iki ucunda duruyor.

| Statü | Ne | Örnek | Zorunlu ek alan | Sunum kuralı |
|---|---|---|---|---|
| **E0** Kayıt | Birden çok bağımsız birincil kaynakta doğrulanabilir | "1453'te İstanbul Osmanlı tarafından alındı" | — | Düz cümle, atıfsız |
| **E1** Olgu | Tek kaynak ya da kısmen tartışmalı, ama olgusal biçimde | "Büyük topları Urban döktü" | kaynak_sayısı | Düz cümle + kaynak notu |
| **E2** Nicel tahmin | Sayı, ama tahmin | "Ordu 50–80 bin" | değer_aralığı + yöntem | **Aralık olmadan gösterilmez** |
| **E3** Nedensel iddia | X yüzünden Y | "Fetih topçuluk sayesinde mümkün oldu" | mekanizma + karşı_olgusal | **Yazar atfı zorunlu** |
| **E4** Yapısal yorum | Dönemselleştirme, örüntü, tip | "Osmanlı bir Barut İmparatorluğu'dur" | rakip_çerçeve | Atıf + rakip çerçeve birlikte |
| **E5** Karşı-olgusal | "Olmasaydı ne olurdu" | "Top olmasa kuşatma başarısız olurdu" | dayanak | Açıkça spekülasyon etiketli |

**Karar (kullanıcının sorusunun cevabı):** İki cümle aynı atom şemasını paylaşır ama `statü` alanı farklıdır ve **sunum kuralı statüden türetilir**. E3'ten itibaren cümle asla yazarsız görünmez: sistem "Osmanlı'nın yükselişi barut sayesindeydi" demez; **"Hodgson'a göre (1974) …; Ágoston bunu reddediyor (2005)"** der. Bu tek kural, tarih özetlerindeki en yaygın zehirlenmeyi kapatır.

**Karar:** statü yukarı doğru asla otomatik terfi etmez. Bir E3 iddiası çok tekrarlandı diye E1 olmaz. Aşağı düşebilir (yeni kanıt), yukarı çıkamaz.

### 4.3 Olgu/yorum ayrımını yapan üç operasyonel test

1. **Yalanlama testi.** *"Hangi belge bulunsa bu cümle yanlışlanır?"* Somut bir belge tarif edilemiyorsa → E4 veya üstü.
2. **Yalın durma testi.** Cümle yazar adı olmadan durabiliyor mu? Duramıyorsa → E3+.
3. **Yüklü sözcük tarayıcısı.** `yükseliş, çöküş, altın çağ, gerileme, kaçınılmaz, yolunu açtı, sayesinde, yüzünden, olgunlaşmamış` → otomatik E3/E4 adayı, insan onayına değil, ek-alan zorunluluğuna tabi.

**AÇIK SORU:** Yalanlama testini LLM'e mi yaptıracağız yoksa yüklü-sözcük tarayıcısı + şablon yeter mi? Test maliyeti atom başına bir ekstra çağrı; öneri: sadece nedensel belirteç içeren cümlelerde çalıştırılsın (kitap başına tahminen %10–15 cümle).

---

## 5. Tarih yazımı (historiography) ve çelişki yönetimi

### 5.1 Yazarın merceği etiketlenmeli mi? — Evet, ama "yanlılık" olarak değil

**Karar:** her tarih/sosyal bilim kitabına, kitap düzeyinde bir **MERCEK** kaydı bağlanır. Adı "yanlılık" değil "mercek" — çünkü mercek kusur değil, kaçınılmazlıktır ve okurun bilmesi gereken şeydir.

```
tür: MERCEK   (kitap düzeyinde, tek kayıt)
analiz_birimi: birey | sınıf | kurum | devlet | coğrafya | kültür | teknoloji | ağ
nedensellik_ağırlığı: { maddi: .5, ideolojik: .1, kurumsal: .3, tesadüf: .1 }
zaman_ölçeği: olay | konjonktür | longue_durée
kapsam: "Akdeniz, 1300–1600"
kaynak_tabanı: arşiv | ikincil_sentez | nicel_seri | sözlü_tarih
normatif_duruş: "modernleşme ilerlemedir" [çıkarım, güven .7]
yazım_bağlamı: "1974, dünya-sistem tartışmasının ortasında"
dayanak: [ önsöz s.xii alıntısı, bibliyografya kompozisyonu, giriş bölümü ]
```
**Nasıl tespit edilir:** (a) önsöz ve giriş — yazarlar merceğini çoğu zaman kendi söyler; (b) bibliyografya kompozisyonu — kimlerle konuşuyor, kimlerle konuşmuyor; (c) nedensel cümlelerin özne dağılımı — cümlelerin öznesi hep "sınıf" mı, hep "sultan" mı; (d) yayın yılı + akademik tartışma bağlamı. Tüm mercek alanları `[çıkarım]` etiketli ve güven skorlu; kesin bilgi gibi sunulmaz.

### 5.2 İki kitap çeliştiğinde: ÇATIŞMA KARTI

Katman 2'nin `çelişiyor` kenarı burada yetersiz. **Karar:** `çelişiyor` kenarı dört alt-tipe ayrılır ve arayüz her birini farklı gösterir.

| Alt-tip | Ne demek | Sistem ne yapar |
|---|---|---|
| `olgusal-çelişki` | En az biri yanlış (tarih, sayı, kim) | Karar verilebilir. Kaynak gücüne bak, hangi tarafın daha yakın/bağımsız kaynağı var; çözülemezse "açık" bırak |
| `kapsam-farkı` | Farklı zaman/mekân, aynı sanılıyor | **Çelişki değil.** İkisini kapsam alanlarıyla yan yana koy |
| `çerçeve-farkı` | Farklı analiz birimi/ölçek | **Perspektif farkı.** İki mercek yan yana gösterilir |
| `değer-farkı` | Aynı olguya farklı normatif hüküm | Kanıtla çözülmez. Değer öncülleri açığa çıkarılır |

Çatışma Kartı çıktısı (tek ekran, doktrin kuralı 1'e uygun):
```
SORU     : Osmanlı'nın 16. yy askeri üstünlüğü neye dayanıyordu?
A (Hodgson, s.99)  → barut teknolojisinin erken benimsenmesi   [E3]
B (Ágoston, s.42)  → mali-idari kapasite; barut herkeste vardı [E3]
TİP      : çerçeve-farkı (teknoloji-merkezli ⟷ kurum-merkezli)
ORTAK    : ikisi de Osmanlı üstünlüğünü ve tarih aralığını kabul ediyor
AYIRAN   : "teknoloji yaygınken neden sadece biri ölçekledi?" sorusuna cevap
NE ÇÖZER : rakip devletlerin barut üretim ve tedarik serileri
```
**Karar:** `NE ÇÖZER` satırı zorunlu — hangi kanıt gelse tartışmanın kapanacağını söylemek, kullanıcıyı seyirciden yargıca dönüştürür. Bu satır yazılamıyorsa çatışma `değer-farkı`dır ve öyle etiketlenir.

---

## 6. Steelman protokolü

Sistem hiçbir konumu zayıflatarak özetlemez. Altı kural:

1. **En savunulabilir okuma.** Metin birden çok okumaya açıksa, en kolay çürütüleni değil, en güçlüsünü al.
2. **Onarım bütçesi.** Argümandaki boşluğu **yalnızca yazarın kabul edeceği** öncüllerle doldur. Yazarın reddedeceği bir öncül eklemek steelman değil, ikamedir.
3. **Kendi terimleriyle.** Kavramları yazarın tanımıyla kullan, rakibin tanımıyla değil. (Marx'ın "sermaye"si muhasebedeki sermaye değildir.)
4. **Güç kaynağını adlandır.** *"Bu konumun asıl gücü şu tek gözlemden gelir: …"* — tek cümle, zorunlu alan.
5. **En güçlü itiraz + yazarın yanıtı birlikte.** İtirazsız sunulan konum reklamdır; yanıtsız sunulan itiraz da haksızlıktır.
6. **Şeffaf onarım.** Metinde olmayan her güçlendirme `[sistem-onarımı]` işaretli ve gerekçeli olur.

**Kalite testi (iki soru, her steelman çıktısında çalışır):**
- *Yazar testi:* Yazar bunu okusa "evet, tam olarak" mı der, "evet ama" mı? İkincisi ise özet zayıflatmıştır.
- *Rakip testi:* Rakip bu özeti okuyunca çürütmesi **zorlaştı** mı? Kolaylaştıysa özet bir korkuluk (strawman) üretmiştir — reddedilir, yeniden üretilir.

**Yasak kalıplar:** iddiayı ılımlılaştırma ("Marx bir bakıma haklıydı"), bağlam düşürerek saçmalaştırma, jargonu atarken ayrımı yok etme, "bazıları der ki" ile sahiplenmeyi silme, en zayıf takipçisiyle özdeşleştirme.

**Karar:** her KONUM atomu **iki alanla birlikte** kaydedilir: `steelman` (en güçlü hâli) ve `en_iyi_itiraz`. İkisi de dolu değilse atom yayınlanmaz. Bu, brifingdeki "aşırı mükemmel sunum" beklentisinin operasyonel karşılığıdır.

---

## 7. Çürütülmüş ama verimli fikirler

Doktrin kuralı 3 gereği hiçbir şey atılmaz. Ama "yanlış" ile "işe yaramaz" karıştırılmamalı. Dört sınıf:

| Sınıf | Tanım | Örnek | Ne saklanır |
|---|---|---|---|
| `yanlış-öngörü/sağlam-mekanizma` | Tahminleri tutmadı, ayırt ettiği kuvvet gerçek | Marx: emek-değer teorisi ve kaçınılmaz çöküş yanlış; **sınıf çıkarı + ideoloji eleştirisi + sermaye yoğunlaşması** analitik olarak canlı | Mekanizma, öngörü değil |
| `yanlış-model/verimli-kelime-dağarcığı` | Kuramı test edilemez, sözlüğü kullanışlı | Freud: metapsikoloji çürük; **bilinçdışı güdü, savunma mekanizması, rasyonalizasyon** günlük analiz aracı | Sözlük, kuram değil |
| `yanlış-parametre/doğru-yapı` | Yapı doğru, sayılar yanlış | Malthus: teknolojiyi hesaba katmadı; **kaynak–büyüme geri besleme döngüsü** doğru form | Fonksiyonel form |
| `zorunlu-iskele` | Yanlıştı ama doğruya giden basamaktı | Esir/eter, flojiston, Lamarck | Neden çekici olduğu + nasıl yıkıldığı |

Atom alanları:
```
statü: çürütüldü/verimli
çürütülen: "kâr oranının düşme eğilimi yasası"     ← spesifik, kitap adı değil
çürüten: { kaynak, tarih, ne_gösterdi }
ayakta_kalan: "kurumların kimin çıkarına çalıştığını sorma alışkanlığı"
verimlilik_tipi: yanlış-öngörü/sağlam-mekanizma
hâlâ_kullanıldığı_yer: [ kurumsal analiz, teşvik tasarımı ]
kullanım_uyarısı: "tahmin aracı olarak kullanma; teşhis aracı olarak kullan"
```
**Karar:** `çürütülen` alanı **kitabı değil, tekil iddiayı** gösterir. "Marx çürütüldü" cümlesi sistemde yazılamaz — sadece belirli bir atom çürütülebilir. Bu, kuralı 3'ün graf düzeyindeki karşılığıdır: çürütme kenarı atom→atom, asla kitap→kitap.

**Sunum:** bu atomlar arayüzde farklı bir işaretle (araç simgesi) görünür ve başlıkları şu kalıptadır: *"Tahmin olarak yanlış, teşhis olarak keskin: …"*

---

## 8. Mühendise transfer — 10 somut yapı

`07-transfer.md` uzmanı bu tabloyu doğrudan kullanacak. Her satır: kaynak fikir → **yapısal çekirdek** (alandan arındırılmış form) → mühendislik karşılığı → yanlış-transfer uyarısı.

| # | Kaynak | Yapısal çekirdek | Mühendislik/strateji karşılığı | Yanlış transfer uyarısı |
|---|---|---|---|---|
| 1 | **Aşırı genişleme** (Kennedy, *Rise and Fall*; Roma limes tartışması) | Kapsam doğrusal büyürken savunma/bakım maliyeti süper-doğrusal büyür; gelir doymuştur | Servis/uç nokta/özellik yüzeyi genişlemesi; her yeni entegrasyon O(n²) bakım borcu. Ölç: *özellik başına marjinal bakım saati* | "Büyüme kötüdür" değil; **maliyet eğrisinin şekli** taşınıyor |
| 2 | **Chesterton'ın çiti** | Bir düzenlemenin sebebi bilinmeden kaldırılmaz | Anlaşılmayan legacy kod / garip retry / açıklanamayan flag silinmez; önce `git log -S` ve olay kayıtları | Değişimi engelleme gerekçesine dönüştürmek; kural **araştır sonra sil**, "silme" değil |
| 3 | **İkinci derece sonuçlar** (Kobra etkisi, Goodhart, Campbell) | Ölçüt hedefe dönüşünce ölçüt olmaktan çıkar; aktör ölçüte optimize eder | SLO/kapsam yüzdesi/velocity gaming; LLM eval'lerinin overfit edilmesi; her metrik yanına *bozulma göstergesi* | Metriği bırakmak değil; **ikili metrik** (hız + kalite) kurmak |
| 4 | **Vekil sorunu** (principal–agent; Hobbes, Olson) | Karar veren ile bedelini ödeyen farklı kişi olunca sistematik sapma çıkar | Nöbet tutmayan ekip mimari karar veriyorsa güvenilirlik düşer. Tasarım kuralı: **acıyı karar vericiye bağla** (you build it, you run it) | Kötü niyet varsaymak; bu bir **yapı** sorunu |
| 5 | **Kurumsal çürüme** (Michels'in oligarşi yasası; Pournelle'in demir kanunu) | Her organizasyonda amaca hizmet edenler ile organizasyona hizmet edenler ayrışır; ikinciler yönetimi ele geçirir | Platform/DevEx ekiplerinin kendi sürecini korumaya başlaması; süreç sayısının ürün çıktısından hızlı artması | Bürokrasi düşmanlığı değil; **periyodik amaç denetimi** önerisi |
| 6 | **Kavramsal ayrım gücü** (type/token; kullanım/zikretme; gerek/yeter koşul) | Doğru ayrım, tartışmanın tümünü çözebilir | `==` vs `equals` vs identity; cache anahtarı type mı token mı; "gerekli koşul" ile "yeterli koşul"u karıştıran alarm kuralları | Ayrımı jargon olarak taşımak; **karışma vakası** olmadan taşıma |
| 7 | **Karşı-olgusal muhakeme** (tarihçinin "olmasaydı") | Nedensel iddia ancak karşı-olgusal ile anlamlıdır | Post-mortem'de "şu deploy olmasaydı olay olur muydu?"; ablation study; feature flag ile A/B | Anlatısal karşı-olgusal ≠ test edilmiş karşı-olgusal; E5 etiketi taşınmalı |
| 8 | **Via negativa / Lindy** (Taleb; ayrıca Ockham) | Uzun yaşamış olan, beklenen kalan ömrü uzun olandır; eklemek yerine çıkarmak daha güvenilir | Bağımlılık seçimi: 12 yıllık kütüphane vs 6 aylık. Mimaride önce **kaldırma** aksiyonunu ara | Yeniliği tümden reddetme; kural sadece **belirsizlik altında** geçerli |
| 9 | **Belirsiz sınır / Sorites** | Kesin eşik olmayan bir yerde ikili karar zorlamak paradoks üretir | Alarm eşikleri, rate-limit, anomali tespiti: tek eşik yerine histerezis + süre penceresi | Karar vermekten kaçınma bahanesi değil; **eşiği açıkça keyfî ilan et** |
| 10 | **Theseus'un gemisi** | Parçaların tamamı değişince kimlik neye bağlı | Kademeli refactor sonrası servis "aynı" mı: sözleşme mi kimlik, uygulama mı? Semantic versioning tam da bu sorunun cevabıdır | Metafizik tartışmaya dalmak; sadece **kimlik ölçütünü yaz** |

**Karar:** transfer atomları `yapısal_çekirdek` alanını **alan-adı içermeyen** bir cümle olarak taşımak zorunda. "Roma" veya "imparatorluk" geçen bir çekirdek cümlesi henüz soyutlanmamıştır ve transfer motoruna verilmez.

---

## 9. Örnek atomlar (tam alanlı)

### 9.1 Felsefe — argüman atomu

```yaml
id: arg_0417
tür: ARGÜMAN
kitap: "Searle, Minds, Brains and Programs (1980)"
bölüm: "Çin Odası"          sayfa: 417-419
ad: "Çin Odası argümanı"

öncüller:
  - id: P1  metin: "Sözdizimi anlambilim için yeterli değildir."      çapa: s.418  kaynak: metinde
  - id: P2  metin: "Bilgisayar programları tümüyle sözdizimseldir."   çapa: s.418  kaynak: metinde
  - id: P3  metin: "Zihinlerin anlambilimsel içeriği vardır."         çapa: s.417  kaynak: metinde
  - id: P4  metin: "Odadaki kişi sistemin tamamını temsil eder."      çapa: —
            kaynak: GİZLİ  türetim: KöprüDenetimi/Adım1
            not: "sonuçtaki 'hiçbir program' ile öncüldeki 'odadaki kişi' arasındaki köprü"

çıkarım:
  biçim: modus_tollens
  adımlar: ["P1+P2 ⇒ program anlambilim üretemez", "+P3 ⇒ program zihin değildir"]
sonuç: { metin: "Doğru program çalıştırmak bir zihin oluşturmak için yeterli değildir", çapa: s.419 }

geçerlilik: geçerli
öncül_desteği: tartışmalı
en_zayıf_halka: P4
statü: canlı-tartışma

itirazlar:
  - { atom: itr_0418, tipi: öncül_reddi, ad: "Sistem Yanıtı — anlama kişide değil sistemde", gücü: budayıcı }
  - { atom: itr_0419, tipi: karşı_örnek, ad: "Robot Yanıtı — nedensel bağlantı eklenirse", gücü: rahatsız_edici }
yazarın_yanıtı:
  - { atom: yan_0420, metin: "Kişi tüm kuralları ezberlesin — sistem içselleşir, anlama yine yok", çapa: s.419 }

steelman: "Argümanın gücü tek gözlemden gelir: sembol manipülasyonunun kuralları,
           sembollerin neye gönderdiğinden tümüyle bağımsız tanımlanabilir.
           Anlam bu tanıma hiçbir yerde girmez."
en_iyi_itiraz: "Sistem Yanıtı — 'anlama' yükleminin taşıyıcısı parça değil bütün olabilir;
                Searle'ün içselleştirme yanıtı bütünün kimliğini P4 ile önvarsayıyor."
transfer:
  yapısal_çekirdek: "Bir sürecin biçimsel özellikleri, yorumlanmış içeriğini belirlemez."
  mühendislik: "Şema doğrulaması geçmiş veri anlamlı veri değildir; tip güvenliği anlam güvenliği değildir."
bağlar:
  - { tip: çelişiyor, hedef: arg_0301 "Turing testi davranışsal yeterlilik ölçütü" }
  - { tip: önkoşulu,  hedef: ayr_0102 "sözdizimi/anlambilim ayrımı" }
```

### 9.2 Tarih — nedensel iddia atomu

```yaml
id: hst_0099
tür: NEDEN_İDDİASI
statü: E3                      # nedensel iddia → yazar atfı zorunlu
kitap: "Hodgson, The Venture of Islam c.3 (1974)"   sayfa: 99

iddia: "Osmanlı'nın 16. yy yükselişi, barut teknolojisinin merkezî orduda erken ve
        ölçekli benimsenmesiyle açıklanır."
atıf_zorunlu: "Hodgson'a göre"          # bu cümle sistemde asla atıfsız gösterilemez
mekanizma: "top/tüfek + merkezî hazine → tımarlı süvariye bağımlılığın azalması →
            merkezîleşme → daha büyük seferberlik kapasitesi"
karşı_olgusal: "Barut olmasa merkezîleşme aynı hızda gerçekleşmezdi" [E5, dayanak: zayıf]
karşılaştırma_sınıfı: [ Safevi, Babür, Memlûk, Venedik ]
zaman_kapsamı: 1450–1600      mekan_kapsamı: Anadolu–Balkanlar–Doğu Akdeniz

destek:
  - { tür: NİCEL, id: hst_0100, metin: "Yeniçeri mevcudu 1527≈8.000 → 1609≈38.000",
      statü: E2, aralık: "±%15", yöntem: "maaş defterleri", çapa: s.101 }
  - { tür: BİRİNCİL_KAYNAK, id: hst_0101, belge: "1526 mevacib defteri",
      hayatta_kalma_yanlılığı: "merkez kayıtları taşrayı eksik temsil eder" }

çatışma:
  - hedef: hst_0210 (Ágoston 2005, s.42 — "barut herkeste vardı; fark mali-idari kapasite")
    tip: çerçeve-farkı
    ortak_zemin: "Osmanlı üstünlüğü ve tarih aralığı"
    ne_çözer: "rakip devletlerin güherçile/top üretim ve tedarik serileri"

mercek_kitap:
  analiz_birimi: kültür+kurum      zaman_ölçeği: longue_durée
  nedensellik_ağırlığı: { ideolojik: .4, kurumsal: .3, maddi: .3 }  [çıkarım, güven .7]

olgu_çekirdeği:                 # aynı paragrafın E0 kısmı ayrı atom
  - hst_0098: "1453'te İstanbul Osmanlı tarafından alındı"  [E0, atıfsız gösterilebilir]

transfer:
  yapısal_çekirdek: "Yeni bir teknolojiden avantaj, teknolojiye erişimden değil,
                     onu ölçekleyecek merkezî kaynak akışından doğar."
  mühendislik: "LLM'e erişim rekabet avantajı değildir; değerlendirme hattı, veri ve
                dağıtım kapasitesi avantajdır. Erişim yaygınlaşınca fark kurumdadır."
  açık_soru_eşleşmesi: "Rakipler aynı modele erişiyorsa savunma hendeğimiz nedir?"
```

---

## 10. Kararlar özeti ve açık sorular

**Kararlar**
1. Felsefede 6, tarihte 5 atom türü; ARGÜMAN atomu öncül–çıkarım–sonuç iskeletini zorunlu taşır.
2. `geçerlilik` ve `öncül_desteği` ayrı alanlar; `en_zayıf_halka` tek değerli ve zorunlu.
3. Gizli varsayımlar Köprü Denetimi'nin 5 adımıyla türetilir, `kaynak: TÜRETİLMİŞ` etiketiyle ayrı atom olur.
4. Tarih iddiaları E0–E5 ile etiketlenir; **E3 ve üstü asla yazar atfı olmadan gösterilmez**; statü yukarı terfi etmez.
5. `çelişiyor` kenarı dörde ayrılır; çerçeve/değer farkı **hata değil**, Çatışma Kartı ile sunulur.
6. Her KONUM atomu `steelman` + `en_iyi_itiraz` alanları dolu olmadan yayınlanmaz.
7. Çürütme kenarı **atom→atom**; "kitap çürütüldü" ifadesi sistemde üretilemez.
8. Transfer atomlarının `yapısal_çekirdek` alanı alan-adı içeremez.

**AÇIK SORULAR**
- **Ontoloji birleştirme:** Aynı kavram farklı kitaplarda farklı tanımlıysa (Marx'ın "sermaye"si ≠ Piketty'ninki) tek düğüm mü, kitap-bağlamlı ayrı düğümler mi? Önerim: ayrı düğüm + `aynı-ad-farklı-kavram` kenarı; `01-bilgi-modeli.md` ile uzlaştırılmalı.
- **Steelman doğrulaması:** "Yazar testi"ni otomatik çalıştırmanın yolu, konumun bilinen en iyi savunucusunun metnini karşı-okutmak. Kütüphanede o metin yoksa ne yapılır?
- **Mercek tespitinin maliyeti:** kitap başına önsöz+giriş+bibliyografya taraması gerekiyor; PDF'te bibliyografya çıkarımı güvenilmezse mercek güveni düşer. Eşik ne olmalı?
- **E2 aralıkları:** yazar aralık vermiyorsa sistem aralık uydurmaz; "tek nokta, yöntem bilinmiyor" mu diyeceğiz, yoksa atomu düşürecek miyiz? Önerim: göster ama `[aralıksız]` damgasıyla.
