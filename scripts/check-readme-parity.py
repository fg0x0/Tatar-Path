#!/usr/bin/env python3
"""README-ийн хоёр хэлний хэсгийн БҮТЭЦ таарч байгаа эсэхийг шалгана.

Энэ репод README нь англи хэсэг, дараа нь «Монгол хэл дээр» хэсэгтэй. Хоёуланг
нь ГАРААР арчилдаг тул нэгийг нь шинэчлээд нөгөөг мартах нь Tatar-ийн бусад
репод дахин дахин гарсан алдаа. Агуулгыг машинаар харьцуулах боломжгүй (өөр хэл
дээр байх нь зорилго), харин БҮТЭЦ таарах ёстой: нэг талд хэсэг нэмэгдвэл
нөгөөд нь мөн нэмэгдэнэ.

Шалгах зүйл: гарчиг, хүснэгтийн мөр, ``` кодын блокийн тоо.

Хэрэглээ:  python3 scripts/check-readme-parity.py [README.md]
Гаралт  :  таарвал 0, зөрвөл 1, файл/хэсэг олдохгүй бол 2.
"""
import re
import sys
from pathlib import Path

# Гарчиг нь markdown («## Монгол хэл дээр») эсвэл HTML («<h2 id="mongol">…</h2>»)
# аль нь ч байж болно — README-д зангуу (anchor) хэрэгтэй тул HTML хэлбэр
# хэрэглэсэн. HTML хэлбэрийг доорх HEADING хэв тоолохгүй тул хасалт хийхгүй.
MN = re.compile(r"^(?:#{1,3}\s*|<h[1-3][^>]*>)\s*Монгол хэл дээр", re.M)
MN_IS_MARKDOWN = re.compile(r"^#{1,3}\s*Монгол хэл дээр", re.M)
FENCE = re.compile(r"^\s*```")
HEADING = re.compile(r"^(#{2,4})\s+\S")
ROW = re.compile(r"^\s*\|.*\|\s*$")
SEP = re.compile(r"^\s*\|[\s:|-]+\|\s*$")

LABELS = {"headings": "гарчиг", "rows": "хүснэгтийн мөр", "code": "кодын блок"}


def measure(body):
    c = {k: 0 for k in LABELS}
    infence = False
    for line in body.split("\n"):
        if FENCE.match(line):
            if not infence:
                c["code"] += 1
            infence = not infence
            continue
        if infence:
            continue
        if HEADING.match(line):
            c["headings"] += 1
        if ROW.match(line) and not SEP.match(line):
            c["rows"] += 1
    return c


def main(argv):
    path = Path(argv[1] if len(argv) > 1 else "README.md")
    if not path.is_file():
        print(f"check-readme-parity: файл алга: {path}", file=sys.stderr)
        return 2
    src = path.read_text(encoding="utf-8")
    m = MN.search(src)
    if not m:
        print("check-readme-parity: «Монгол хэл дээр» гарчиг олдсонгүй.\n"
              "  Гарчиг өөрчлөгдсөн бол энэ скриптийн MN хэвийг зас.", file=sys.stderr)
        return 2

    en, mn = measure(src[: m.start()]), measure(src[m.start():])
    # «Монгол хэл дээр» гарчиг өөрөө тоологдохгүй — гэхдээ зөвхөн markdown
    # хэлбэртэй үед л HEADING хэвд баригдсан байна.
    if MN_IS_MARKDOWN.search(src):
        mn["headings"] -= 1

    bad = [f"  {LABELS[k]:16} EN={en[k]:<4} MN={mn[k]:<4} (зөрүү {abs(en[k]-mn[k])})"
           for k in LABELS if en[k] != mn[k]]
    summary = ("  EN [" + " ".join(f"{k}={en[k]}" for k in LABELS) + "]\n"
               "  MN [" + " ".join(f"{k}={mn[k]}" for k in LABELS) + "]")
    if not bad:
        print("check-readme-parity: OK — хоёр хэсгийн бүтэц таарч байна")
        print(summary)
        return 0
    print("check-readme-parity: ХОЁР ХЭСГИЙН БҮТЭЦ ЗӨРЖ БАЙНА", file=sys.stderr)
    print("\n".join(bad), file=sys.stderr)
    print("\n  Нэг талд хэсэг/хүснэгт/кодын блок нэмсэн бол нөгөөд нь ч нэм.\n"
          "  Монгол текстийг машинаар орчуулж БОЛОХГҮЙ — хүн бичнэ.\n" + summary,
          file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
