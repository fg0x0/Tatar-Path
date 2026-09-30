#!/usr/bin/env python3
"""Invariants for the concept document.

This repo ships one self-contained HTML page and nothing else, so the things
that can silently break it are narrow and worth pinning:

  * dead CSS   a duplicated custom property hides a broken value behind a good
               one. This happened before: a `--tx3:#77melon` (not a colour at
               all) sat in the file, invisible because the next declaration
               overrode it.
  * dead links every section has an id and the table of contents points at them;
               a renamed id leaves a nav entry that goes nowhere.
  * printing   the page is a pitch document, so it gets sent to people as PDF.
               Without the print stylesheet it prints blank from a dark theme.

Usage:  python3 scripts/check-concept.py [docs/concept.html]
Exit :  0 all invariants hold, 1 something broke, 2 the file is unreadable.
"""

import re
import sys
from pathlib import Path


def main(argv) -> int:
    path = Path(argv[1] if len(argv) > 1 else "docs/concept.html")
    if not path.is_file():
        print("check-concept: no such file: %s" % path, file=sys.stderr)
        return 2
    src = path.read_text(encoding="utf-8")
    problems = []
    ok = []

    style = re.search(r"<style>(.*?)</style>", src, re.S)
    if not style:
        problems.append("no <style> block")
    else:
        css = style.group(1)
        if css.count("{") != css.count("}"):
            problems.append("unbalanced braces in CSS (%d vs %d)" % (css.count("{"), css.count("}")))
        else:
            ok.append("CSS braces balanced")

        bad = [
            c for c in re.findall(r"#[0-9A-Za-z]+", css)
            if not re.fullmatch(r"#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})", c)
        ]
        if bad:
            problems.append("invalid colour literal(s): " + ", ".join(sorted(set(bad))))
        else:
            ok.append("every colour literal is valid")

        dups = set()
        for block in re.finditer(r"\{([^{}]*)\}", css):
            props = re.findall(r"(?:^|;)\s*(--[a-z0-9-]+)\s*:", block.group(1))
            dups |= {p for p in props if props.count(p) > 1}
        if dups:
            problems.append("custom property declared twice in one block: " + ", ".join(sorted(dups)))
        else:
            ok.append("no duplicated custom properties")

    ids = set(re.findall(r'id="([^"]+)"', src))
    dead = sorted({h for h in re.findall(r'href="#([^"]+)"', src) if h not in ids})
    if dead:
        problems.append("nav link(s) pointing at a missing id: " + ", ".join(dead))
    else:
        ok.append("every in-page link resolves")

    all_ids = re.findall(r'id="([^"]+)"', src)
    dup_ids = sorted({i for i in all_ids if all_ids.count(i) > 1})
    if dup_ids:
        problems.append("duplicate id(s): " + ", ".join(dup_ids))
    else:
        ok.append("no duplicate ids")

    if "@media print{" not in src.replace("@media print {", "@media print{"):
        problems.append("no @media print block - the page prints blank from a dark theme")
    else:
        ok.append("print stylesheet present")

    dates = re.findall(r"20\d{2}-\d{2}-\d{2}", src)
    if len(dates) > 1:
        problems.append("the date appears %d times (%s) - keep it in one place" % (len(dates), ", ".join(sorted(set(dates)))))
    else:
        ok.append("the date appears once")

    for line in ok:
        print("  PASS  " + line)
    for line in problems:
        print("  FAIL  " + line, file=sys.stderr)
    print("\n%s: %d ok, %d failed" % (path.name, len(ok), len(problems)))
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
