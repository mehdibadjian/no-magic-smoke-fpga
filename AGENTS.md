# For agents

Entry point for AI coding agents working with this repository. Humans want
[`README.md`](README.md).

This repo is a **reference book**, not an application. There is nothing to run and nothing
to deploy beyond the docs site. There are two reasons an agent ends up here, and they need
different things.

---

## 1. You are looking something up

You are helping with an FPGA task — a timing failure, an XDC file, a CDC question, a power
budget — and you want grounded facts rather than plausible recall.

**Use the `fpga-ultrafast` skill.** It is at
[`.claude/skills/fpga-ultrafast/`](.claude/skills/fpga-ultrafast/) and it exists because
the book is ~74,000 words: opening a section costs ~4,300 words of context to answer a
question that usually needs 40.

```bash
# what is covered
python3 .claude/skills/fpga-ultrafast/scripts/lookup.py --list

# find the right section (IDF-weighted, so "clock domain crossing" finds 2.3, not 1.3)
python3 .claude/skills/fpga-ultrafast/scripts/lookup.py --search "clock domain crossing"

# pull one block instead of the whole section
python3 .claude/skills/fpga-ultrafast/scripts/lookup.py --section 2.3 --block "Do the Math"
```

Every section has the same named blocks, so retrieval is structural rather than semantic:

| Block | What you get |
| --- | --- |
| `Bullet Points` | Cheat sheet: commands, attributes, thresholds, formulas. **Start here.** |
| `Do the Math` | A formula, worked, with units and a verdict |
| `The Real Artifact` | Complete pasteable XDC / RTL / Tcl / annotated report |
| `Code Detective` | A realistic bug **and its corrected code** |
| `Analogy → Silicon` | Which primitive a concept maps to |
| `Answers` | Reasoning on judgement calls |
| `There Are No Dumb Questions` | Edge cases |

**If the user gave you a symptom rather than a topic, read
[`.claude/skills/fpga-ultrafast/references/topic-index.md`](.claude/skills/fpga-ultrafast/references/topic-index.md)
first.** Symptoms rarely share vocabulary with their causes — "works for hours then
crashes" is a CDC problem and searching for "crashes" will not find it. That file maps
symptoms, tasks, Vivado commands and primitives to section IDs.

### Working outside this repo

The script auto-detects the book when run inside the repo. Elsewhere:

```bash
export NO_MAGIC_SMOKE_ROOT=/path/to/no-magic-smoke-fpga
# or: --book-root /path/to/no-magic-smoke-fpga
```

With no local copy, the book is published at
<https://mehdibadjian.github.io/no-magic-smoke-fpga/>, with section URLs of the form
`.../sections/2.3_cdc_minefield/`.

### What not to do with it

**Do not lift device-specific numbers out of this book into a real design.** Metastability
constants, VCO ranges, $T_{co}$, $\theta_{JC}$, SLL counts and speed-grade timing are all
presented as *labelled assumptions for a worked example* — the calculation is the
transferable part, the constant is not. [`docs/references.md`](docs/references.md) has a
table of which quantity comes from which datasheet or report, plus the primary-source
document IDs.

Where this book disagrees with AMD's documentation, the documentation is right.

---

## 2. You are writing or editing a section

**Use the `ultrafast-authoring` skill**
([`.claude/skills/ultrafast-authoring/`](.claude/skills/ultrafast-authoring/)) and read
[`AUTHORING.md`](AUTHORING.md) before writing prose, not after.

The short version: this book is generated with AI assistance, and the first pass came out
fluent and useless — eighteen sections with eighteen questions asked and **zero answered**,
no worked calculations, and sixty lines of deliberately-broken toy code in the whole book.
The contract exists because better prompting did not fix that; a checkable requirement did.

```bash
python3 tools/check_sections.py    # must report 0 errors
mkdocs build --strict              # must build with no warnings
```

The checker enforces structure, not correctness: required blocks, that every question
asked is answered in the same section, that the artifact is substantial enough to paste,
that at least three real tool or primitive names appear, that numbers carry units, and
that `toc.json` / `mkdocs.yml` / `authoring/section_spec.json` / disk all agree.

It also verifies the topic index above routes to every section, so a new section cannot be
invisible to retrieval.

### Adding a section touches four files

`docs/sections/N.M_name.md`, `toc.json`, `authoring/section_spec.json`, `mkdocs.yml`. The
checker names whichever you forget.

---

## Repository map

| Path | What it is |
| --- | --- |
| `docs/sections/` | The 18 sections. The book. |
| `docs/references.md` | Primary sources, verified document IDs, and the datasheet-values table |
| `AUTHORING.md` | The section contract, with the postmortem motivating each rule |
| `authoring/section_spec.json` | Machine-readable contract + per-section objectives |
| `tools/check_sections.py` | Enforces it. Runs in CI on every PR. |
| `.claude/skills/` | The two skills described above |
| `mkdocs.yml`, `toc.json` | Site nav and plan of record — kept in sync by the checker |

## Conventions

- **Prose is CC BY 4.0, code is MIT** (`LICENSE`, `LICENSE-CODE`). Code examples are MIT
  specifically so they paste into commercial designs without friction.
- **Do not commit `site/`** — it is build output and gitignored.
- **Do not invent a datasheet number** to make an example work. State it as an assumption
  and say where the real one comes from. This is the rule most worth internalising here.
- **Check before you claim a primitive exists on a family.** The first draft recommended
  `BUFR` and `BUFH`, which do not exist on UltraScale+ — a plausible 7-series memory that
  would have cost a reader a week.
