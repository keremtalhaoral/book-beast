# bookbeast — dikey dilim (v0)

Tek kitabı uçtan uca işleyen en küçük boru hattı. Web arayüzü yok; amaç
mimariyi değil **çıkarım kalitesini** sınamak.

## Çalıştırma

```bash
python3 -m venv .venv && .venv/bin/pip install pymupdf sympy
.venv/bin/python bookbeast/ingest.py kitaplar/kitap.pdf   # S0-S3 → cikti/s3.json
.venv/bin/python bookbeast/chunk.py                        # S7    → cikti/s7.json
.venv/bin/python bookbeast/verify.py cikti/atomlar.json    # S9    → cikti/s9.json
```

## Aşamalar

| Aşama | Dosya | LLM? | Ne yapar |
|---|---|---|---|
| S0–S3 | `ingest.py` | hayır | PDF → normalleştirilmiş akış + sınıflandırılmış bloklar |
| S7 | `chunk.py` | hayır | bloklar → bölüm bazlı anlamsal parçalar |
| S8 | *(bekliyor)* | **evet** | parça → fikir atomları |
| S9 | `verify.py` | hayır | atomun `verbatim`'i akışta gerçekten var mı |

**S0–S3, S7 ve S9 tamamen deterministiktir.** Aynı PDF her zaman aynı çapaları
üretir; doktrin kural 2'nin ("kaynaksız cümle yok") dayanağı budur.

S8 henüz otomatik değil: bir Anthropic API anahtarı gerektiriyor. Şimdilik
atomlar elle üretilip `verify.py`'ye verilerek çıkarım kalitesi ölçülüyor.

## Ölçülen sonuç (DDIA Bölüm 8, 61 sayfa)

- 621 blok, **çapa doğruluğu 621/621**
- 65 anlamsal parça
- Örnek parçadan 12 atom → **12/12 birebir çapa doğrulaması geçti**
