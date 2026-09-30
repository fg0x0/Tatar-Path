# Translation needed — Mongolian

**Currently: nothing.** Recorded here so the question does not get re-asked.

Generated 2026-09-30 by classifying every tracked `.md` as entirely English,
bilingual, or mixed.

| File | Status |
|---|---|
| `README.md` | Bilingual. English first, then `Монгол хэл дээр` — both halves written, neither generated. |
| `docs/concept.html` | **Entirely Mongolian.** The design document is Mongolian-first; there is no English version, and none is planned unless the concept is pitched outside Mongolia. |

## If that changes

This repo is a concept with no code yet. When Tatar Path grows a CLI, the things
that will need Mongolian are the ones an operator reads while working — usage
text, error messages, and any quick start — not the design document, which is
already Mongolian.

Two rules carried over from the rest of the Tatar family:

- **Never machine-translate.** The Mongolian here is written; a transliterated
  stand-in is worse than an honest gap.
- **If a bilingual README gains a section on one side, add it to the other.**
  The sibling repos gate this in CI (`check-readme-parity`); this repo has no
  such check yet because both halves are currently level.
