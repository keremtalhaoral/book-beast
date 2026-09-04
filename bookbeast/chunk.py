"""Aşama S7: normalleştirilmiş bloklar → anlamsal parçalar (chunk).

04-mimari.md kararı: parça sınırı = en alt başlık (h3) seviyesi.
Bağlam penceresine sığmayan parça alt-parçalara bölünür ama başlık
yolu (`section`) her alt-parçada tekrarlanır — bağlam korunumu için.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict

MAX_CHARS = 24_000   # ~6k token; 04-mimari.md §5


@dataclass
class Chunk:
    idx: int
    section: list[str]
    start: int
    end: int
    pages: tuple[int, int]
    text: str
    n_code: int


def chunk(artifact: dict) -> list[Chunk]:
    blocks = artifact["blocks"]
    groups: list[list[dict]] = []
    cur: list[dict] = []
    for b in blocks:
        # Yeni bir başlık (h1-h3) yeni parça başlatır
        if b["kind"] in ("chapter", "h1", "h2", "h3") and cur:
            groups.append(cur)
            cur = []
        cur.append(b)
    if cur:
        groups.append(cur)

    out: list[Chunk] = []
    for g in groups:
        body = [b for b in g if b["kind"] not in ("caption",)]
        if not body:
            continue
        text = "\n".join(b["text"] for b in body)
        if len(text) < 40:          # yalnız başlıktan ibaret grup
            continue
        # Aşırı uzun parçayı böl (başlık yolu korunarak)
        pieces = [body] if len(text) <= MAX_CHARS else [
            body[i:i + max(1, len(body) // (len(text) // MAX_CHARS + 1))]
            for i in range(0, len(body), max(1, len(body) // (len(text) // MAX_CHARS + 1)))
        ]
        for p in pieces:
            if not p:
                continue
            t = "\n".join(b["text"] for b in p)
            out.append(Chunk(
                idx=len(out),
                section=p[0]["section"],
                start=p[0]["start"], end=p[-1]["end"],
                pages=(p[0]["page"], p[-1]["page"]),
                text=t,
                n_code=sum(1 for b in p if b["kind"] == "code"),
            ))
    return out


if __name__ == "__main__":
    import sys
    art = json.load(open("cikti/s3.json"))
    cs = chunk(art)
    print(f"{len(cs)} parça\n")
    for c in cs:
        path = " › ".join(c.section[-2:]) if c.section else "(başlıksız)"
        print(f"  #{c.idx:3d}  s.{c.pages[0]:2d}-{c.pages[1]:2d}  {len(c.text):6,d} kr  "
              f"{'kod ' if c.n_code else '    '}{path[:64]}")
    json.dump([asdict(c) for c in cs], open("cikti/s7.json", "w"),
              ensure_ascii=False, indent=1)
    print(f"\ntoplam {sum(len(c.text) for c in cs):,} karakter → cikti/s7.json")
