# Contributing

Thanks for looking. This project has an unusual property for a book: **its quality bar is
executable.** Before you write anything, run the check:

```bash
python3 tools/check_sections.py
```

It should report `18 sections checked, 0 error(s), 0 warning(s)`. If it does not, that is
the first thing to fix.

## The most valuable contribution

**Technical corrections.** This is a study companion to AMD's documentation, and where the
two disagree, the documentation is right and this book is wrong. If you find:

- a claim that contradicts current AMD documentation,
- a primitive, command or attribute that does not exist (or no longer does — several
  7-series primitives were incorrectly recommended for UltraScale+ in the first draft),
- arithmetic that does not check out,
- a document number in [`docs/references.md`](docs/references.md) that has been renumbered
  or retired,

please [open an issue](https://github.com/mehdibadjian/no-magic-smoke-fpga/issues) — or a
pull request with the fix and the source you checked it against. Include the document ID
and version. That makes the correction verifiable instead of a difference of opinion.

## Editing or adding a section

Every section must satisfy the contract in [`AUTHORING.md`](AUTHORING.md). Read it first;
it is short, and it explains *why* each rule exists rather than just stating it.

The rules that catch people out:

1. **Every question you ask must be answered in the same section.** A `Brain Power` or
   `Sharpen Your Pencil` with no entry under `### Answers` fails the build. This is the
   single rule the first draft violated eighteen times out of eighteen.
2. **Every analogy needs a row in the `Analogy → Silicon` table**, including the
   *where it breaks* column. An unmapped metaphor is the failure mode this project exists
   to prevent.
3. **`The Real Artifact` must be complete**, not a fragment — the check enforces a minimum
   length, because a five-line snippet is an illustration, not something a reader can use.
4. **`Do the Math` must contain an actual equation** with units and a verdict. State your
   givens, and label device-specific values as assumptions rather than constants.
5. **`Code Detective` must show the fix**, written out. "Use `get_ports` instead" is a
   diagnosis; the corrected script is a fix.

### Numbers

Do not invent a datasheet figure to make an example land. If you need a value you cannot
verify, state it as a given for the worked example and say where the reader should get the
real one. The arithmetic is the lesson; the constant is not. See the table at the bottom
of [`docs/references.md`](docs/references.md).

Device-specific figures must name the family and, where it matters, the speed grade. Tool
message and rule IDs (`TIMING-*`, `CDC-*`, `DRC-*`) drift between Vivado releases — name
them, say which release you checked, and point the reader at `report_methodology` /
`report_cdc` to list the ones their install ships.

### Voice

Keep it. The conversational Head First register was never the problem with this book, and
a correction written in datasheet prose will read as a patch rather than as part of the
text. Contractions are fine. Second person is fine. Jokes are fine. Vagueness is not.

## Before you open a pull request

```bash
python3 tools/check_sections.py    # must pass with 0 errors
mkdocs build --strict              # must build with no warnings
```

If you changed `toc.json`, `mkdocs.yml` or added a file under `docs/sections/`, the checker
verifies all three agree with each other — that consistency check exists because the
generator once drifted onto eight filenames that did not exist and nothing noticed.

## Adding a new section

You will also need to add it to three places, and the checker will tell you if you miss
one:

- `toc.json` — the plan of record (id, title matching the file's `H1`, path)
- `authoring/section_spec.json` — with its technical learning objectives
- `mkdocs.yml` — the site navigation

## Scope

This guide covers the UltraFast design methodology for AMD FPGAs. Contributions that
extend it to other vendors' toolchains are out of scope — not because they lack value, but
because the whole premise is a companion to one specific methodology, and a book that
covers everything teaches nothing. A separate book, borrowing this repo's contract and
tooling, would be a fine thing to build; the tooling is MIT licensed for exactly that
reason.

## Code of conduct

Be straightforward and be kind. Assume the person you are correcting knows something you
do not. Technical disagreements get resolved by citing a document, not by seniority.
