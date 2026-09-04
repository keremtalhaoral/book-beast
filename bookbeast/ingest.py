"""Aşama S0-S3: PDF → normalleştirilmiş metin akışı + sınıflandırılmış bloklar.

Tasarım kaynakları:
  docs/uzmanlar/04-mimari.md  — aşama ayrımı, içerik-adresli eser
  docs/uzmanlar/01-bilgi-modeli.md — kanonik çapa = normalleştirilmiş
                                     akıştaki karakter ofseti

Bu aşamada LLM kullanılmaz. Tamamen deterministiktir: aynı PDF her zaman
aynı eseri üretir. Çapaların güvenilirliği buna dayanır.
"""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from dataclasses import asdict, dataclass, field

import pymupdf

STAGE_VERSION = "S0-S3/1"

# Yazı tipi imzası → blok türü. Kitaba özgü; her kitap için kalibre edilir.
# (04-mimari.md §3: yapı tespiti yazı tipi metriğine dayanır)
BODY_FONTS = ("MinionPro-Regular", "MinionPro-It")
CODE_FONTS = ("UbuntuMono",)
HEAD_FONTS = ("MyriadPro-SemiboldCond", "MyriadPro-Cond")


@dataclass
class Block:
    """Sınıflandırılmış metin bloğu. `start`/`end` kanonik çapadır."""
    kind: str          # chapter|h1|h2|h3|body|code|caption|list_item|sidebar
    text: str
    start: int
    end: int
    page: int          # 1 tabanlı, PDF'teki fiziksel sayfa
    level: int = 0     # başlıklar için derinlik, diğerleri 0
    section: list[str] = field(default_factory=list)  # üstündeki başlık yolu


@dataclass
class NormalizedDoc:
    source_sha256: str
    stage_version: str
    page_count: int
    text: str
    blocks: list[Block]

    def artifact(self) -> dict:
        return {
            "source_sha256": self.source_sha256,
            "stage_version": self.stage_version,
            "page_count": self.page_count,
            "char_count": len(self.text),
            "blocks": [asdict(b) for b in self.blocks],
        }


def _normalize(s: str) -> str:
    """Unicode ve tipografi normalleştirmesi.

    Çapa kararlılığı için bu fonksiyon ASLA uzunluğu değiştiren bir dönüşüm
    yapmamalı ki ofsetler kaymasın — o yüzden tire birleştirme burada değil,
    blok metni üretilirken ayrı alanda yapılır.
    """
    s = unicodedata.normalize("NFC", s)
    # Aynı genişlikte güvenli değişimler (uzunluk korunur)
    return (s.replace("’", "'").replace("‘", "'")
             .replace("“", '"').replace("”", '"')
             .replace(" ", " ").replace("ﬁ", "fi").replace("ﬂ", "fl"))


def _classify(font: str, size: float) -> tuple[str, int]:
    """Yazı tipi + punto → (blok türü, başlık derinliği)."""
    f = font.split("+")[-1]
    if any(c in f for c in CODE_FONTS):
        return "code", 0
    if any(h in f for h in HEAD_FONTS):
        if size >= 22: return "chapter", 0
        if size >= 17: return "h1", 1
        if size >= 14: return "h2", 2
        if size >= 10.5: return "h3", 3
        return "caption", 0          # 9pt SemiboldCond → şekil/tablo etiketi
    if any(b in f for b in BODY_FONTS):
        return ("body", 0) if size >= 10.2 else ("caption", 0)
    return "body", 0


_BULLET_ONLY = re.compile(r"^[••\s]+$")


def ingest(pdf_path: str) -> NormalizedDoc:
    sha = hashlib.sha256(open(pdf_path, "rb").read()).hexdigest()
    doc = pymupdf.open(pdf_path)

    blocks: list[Block] = []
    buf: list[str] = []
    cursor = 0
    section: list[str] = []

    for pno, page in enumerate(doc, start=1):
        for pblock in page.get_text("dict")["blocks"]:
            if pblock["type"] != 0:
                continue
            # Blok içindeki baskın imzayı bul (satır satır değil, blok bazlı)
            parts, sizes, fonts = [], [], []
            for line in pblock["lines"]:
                for span in line["spans"]:
                    if not span["text"].strip():
                        continue
                    parts.append(span["text"])
                    sizes.append(span["size"])
                    fonts.append(span["font"])
            if not parts:
                continue

            raw = _normalize(" ".join(parts))
            raw = re.sub(r"\s+", " ", raw).strip()
            if not raw or _BULLET_ONLY.match(raw):
                continue  # PyMuPDF'in ayrı blok yaptığı yalnız-madde-imi artığı

            # Baskın imza = en çok karakter taşıyan span'in imzası
            dom = max(range(len(parts)), key=lambda i: len(parts[i]))
            kind, level = _classify(fonts[dom], sizes[dom])

            start = cursor
            buf.append(raw)
            cursor += len(raw) + 1  # +1: aralarına konan "\n"
            end = start + len(raw)

            if kind in ("chapter", "h1", "h2", "h3"):
                section = section[: max(level - 1, 0)] + [raw]

            blocks.append(Block(kind=kind, text=raw, start=start, end=end,
                                page=pno, level=level, section=list(section)))

    return NormalizedDoc(sha, STAGE_VERSION, doc.page_count, "\n".join(buf), blocks)


def verify_anchors(nd: NormalizedDoc) -> tuple[int, int]:
    """Her bloğun çapası gerçekten o metni gösteriyor mu? (Doktrin kural 2)"""
    ok = sum(1 for b in nd.blocks if nd.text[b.start:b.end] == b.text)
    return ok, len(nd.blocks)


if __name__ == "__main__":
    import sys
    nd = ingest(sys.argv[1])
    ok, total = verify_anchors(nd)
    print(f"sha256      : {nd.source_sha256[:16]}…")
    print(f"sayfa       : {nd.page_count}")
    print(f"karakter    : {len(nd.text):,}")
    print(f"blok        : {total}")
    print(f"çapa doğru  : {ok}/{total}  {'✓' if ok == total else '✗ KIRIK'}")
    from collections import Counter
    for k, n in Counter(b.kind for b in nd.blocks).most_common():
        print(f"  {k:10s} {n:5d}")
    out = sys.argv[2] if len(sys.argv) > 2 else "cikti/s3.json"
    json.dump(nd.artifact(), open(out, "w"), ensure_ascii=False, indent=1)
    print(f"\neser → {out}")
