"""Aşama S9: çapa doğrulama — doktrin kural 2'nin uygulayıcısı.

03-dogrulama.md: "LLM çıktısı bu boru hattında tanık değil sanıktır."
Bir atom, `verbatim` alanının normalleştirilmiş akışta GERÇEKTEN bulunduğu
makineyle kanıtlanana kadar `dogrulanamadi` sayılır.

İki geçiş:
  P1 — birebir eşleşme (exact)
  P2 — tipografik gürültüye toleranslı eşleşme (satır sonu tiresi, boşluk)
       P2 ile bulunan atom `dogrulandi(alinti)` alır ama `capa_guveni` düşer.
"""
from __future__ import annotations

import json
import re
import unicodedata

SOFT = "‐‑‒–­⁃"   # tire aileleri


def denoise(s: str) -> str:
    """Karşılaştırma için gürültüyü sil. Ofset üretmez, sadece eşleştirir."""
    s = unicodedata.normalize("NFC", s)
    for ch in SOFT:
        s = s.replace(ch, "-")
    s = re.sub(r"-\s+", "", s)        # "ambig- uous" -> "ambiguous"
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def _build_map(text: str) -> tuple[str, list[int]]:
    """Gürültüsüz metin + her karakterin orijinal ofseti."""
    out, idx = [], []
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        if ch in SOFT:
            ch = "-"
        if ch == "-" and i + 1 < n and text[i + 1].isspace():
            j = i + 1
            while j < n and text[j].isspace():
                j += 1
            i = j                       # tireyi ve ardından geleni yut
            continue
        if ch.isspace():
            if out and out[-1] == " ":
                i += 1
                continue
            out.append(" "); idx.append(i)
        else:
            out.append(ch.lower()); idx.append(i)
        i += 1
    return "".join(out), idx


def verify(atoms: list[dict], text: str) -> list[dict]:
    clean, omap = _build_map(text)
    for a in atoms:
        v = a["verbatim"]
        # P1 — birebir
        p = text.find(v)
        if p >= 0:
            a.update(capa_start=p, capa_end=p + len(v),
                     dogrulama="dogrulandi(alinti)", capa_guveni=1.0, gecis="P1")
            continue
        # P2 — toleranslı
        q = denoise(v)
        p = clean.find(q)
        if p >= 0:
            s, e = omap[p], omap[min(p + len(q) - 1, len(omap) - 1)] + 1
            a.update(capa_start=s, capa_end=e,
                     dogrulama="dogrulandi(alinti)", capa_guveni=0.8, gecis="P2")
            continue
        a.update(capa_start=None, capa_end=None,
                 dogrulama="dogrulanamadi", capa_guveni=0.0, gecis="-")
    return atoms


if __name__ == "__main__":
    import sys
    art = json.load(open("cikti/s3.json"))
    # normalleştirilmiş akışı bloklardan yeniden kur (s3 metni taşımıyor)
    text = "\n".join(b["text"] for b in art["blocks"])
    atoms = verify(json.load(open(sys.argv[1])), text)

    ok = sum(1 for a in atoms if a["dogrulama"].startswith("dogrulandi"))
    p1 = sum(1 for a in atoms if a.get("gecis") == "P1")
    p2 = sum(1 for a in atoms if a.get("gecis") == "P2")
    print(f"ÇAPA DOĞRULAMA: {ok}/{len(atoms)} geçti   (P1 birebir: {p1}, P2 toleranslı: {p2})\n")
    for a in atoms:
        mark = "✓" if a["dogrulama"].startswith("dogrulandi") else "✗"
        loc = f"{a['capa_start']}–{a['capa_end']}" if a["capa_start"] is not None else "BULUNAMADI"
        print(f" {mark} {a['id']}  {a['gecis']:2s} {loc:>14s}  {a['kip']:9s} {a['destek']:16s} {a['iddia'][:52]}")
        if a["dogrulama"] == "dogrulanamadi":
            print(f"      ↳ karantina: {a['verbatim'][:70]}")
    json.dump(atoms, open("cikti/s9.json", "w"), ensure_ascii=False, indent=1)
