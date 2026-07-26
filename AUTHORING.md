# Authoring Contract

This file is the spec that every section of this book must satisfy. It exists because
the first generation pass did **not** have one, and the result drifted: eighteen
sections came out in a convincing Head First *voice* but with none of the Head First
*machinery*, and almost no engineering content a reader could act on.

Read this before writing or regenerating any section. The machine-readable version is
[`authoring/section_spec.json`](authoring/section_spec.json), enforced by
[`tools/check_sections.py`](tools/check_sections.py) in CI.

---

## 1. What went wrong the first time

The pipeline emitted the same eight-block essay template for all eighteen sections:

| Block | Present in v1 | Problem |
| --- | --- | --- |
| Narrative intro with analogy | 18/18 | Fine. |
| Prose concept blocks | 18/18 | Fine, but this was *all* there was. |
| `Brain Power` question | 18/18 | **Zero of them were ever answered.** |
| `Fireside Chat` dialogue | 18/18 | Fine. |
| `Code Detective` snippet | 18/18 | 2–6 lines, and the answer is printed directly underneath. It is a reading comprehension prompt, not an exercise. |
| Analogy figures | 36 total | Every single figure is a metaphor picture. Not one timing diagram, floorplan, waveform, or report screenshot. |
| Worked numbers | **0/18** | Quantitative questions were asked rhetorically and never computed. |
| Runnable artifact | **0/18** | ~60 lines of code in the entire book, all of it deliberately broken toy snippets. |
| Answers / solutions | **0/18** | The reader has no way to check themselves. |

The net effect: the book *describes* FPGA engineering rather than *teaching* it. A reader
finishes a section able to repeat the analogy and unable to run a command, read a report,
size a FIFO, or write a constraint.

Head First's actual pedagogy is a loop — **concrete example → do it yourself → check your
answer → compress into a reference**. v1 shipped only the first half of the first step.

There was a second, mechanical symptom of the same root cause: `toc.json` listed eight
filenames that never existed on disk and section titles that disagreed with the
generated `H1`s. Nothing checked the plan against the output, so nobody noticed the
generator had wandered off its own outline.

## 2. The rule

> **The analogy is the on-ramp, never the destination.**

Every analogy must be cashed out, in the same section, into named silicon, named tool
commands, and numbers with units. If a reader can enjoy your section without ever
learning a command they can type, the section has failed.

Concretely: **no analogy may be introduced without a matching row in that section's
Analogy → Silicon table.**

## 3. Required blocks

Sections live in `docs/sections/` and must contain the following, in this order.
Headings must match exactly — the validator greps for them.

### 3.1 Opening (unchanged from v1)

`# Section N.M: <title>` followed by the conversational hook. Keep the voice. The voice
was never the problem.

### 3.2 Concept prose with named primitives

Explain the idea. But every concept block must name the real thing: not "clock buffer"
but `BUFGCE`, not "the memory" but `RAMB36E2` / `URAM288`, not "the report" but
`report_clock_interaction`. Generic nouns are a smell.

### 3.3 `### Analogy → Silicon`

A two- or three-column table mapping every metaphor used in the section to the actual
construct, plus how the analogy breaks down. The "where it breaks" column is mandatory —
it is what stops a reader from over-extending a metaphor into a wrong mental model.

```markdown
| In the story | In the silicon | Where the analogy breaks |
| --- | --- | --- |
| The express train | `BUFGCE` on a global clock spine | Trains cost fuel per trip; a BUFGCE costs power continuously whether or not data moves |
```

### 3.4 `### Do the Math`

At least one fully worked numeric example. Show the formula, substitute the numbers,
state the units, and state the verdict. Every given must be labelled as a given.

Requirements:

- Formula written out symbolically before substitution.
- Every number carries a unit.
- The source of each input is stated: report field, datasheet parameter, or "assume".
- End with what the number *means* — pass/fail, or what you'd change.

### 3.5 `### The Real Artifact`

A complete, self-contained thing the reader can paste into a project. Not a fragment.
One of:

- A full `.xdc` constraint set for a stated scenario.
- A synthesizable module with ports, resets, and comments explaining the coding pattern.
- A Tcl procedure that runs against an open design and prints something useful.
- A verbatim tool report excerpt, annotated line by line with what to look at.

It must be correct as written. If it needs a caveat (device family, Vivado version),
put the caveat in a comment inside the block.

### 3.6 `### Code Detective` (kept, but upgraded)

Keep the spot-the-flaw exercise, but the flaw must now be a realistic one at realistic
length, and the explanation must include **the fix**, written out, not just the
diagnosis. "Use `get_ports` instead" is not a fix; the corrected script is.

### 3.7 `### Sharpen Your Pencil`

A task the reader performs. Numbered steps. Must be doable with Vivado, a datasheet, a
calculator, or a text editor — no lab hardware required. Typical forms: compute a
budget, fill in a table, spot the missing constraint, size a resource, predict what a
report will say.

### 3.8 `### Final Thoughts` / closing (unchanged from v1)

### 3.9 `### Answers`

**Non-negotiable.** Answers for *every* question the section posed: each `Brain Power`,
each `Sharpen Your Pencil` step. Show the working, not just the result. If a question is
genuinely open-ended, say so and give the reasoning a strong answer would contain.

A section that asks a question it does not answer is not shippable.

### 3.10 `### There Are No Dumb Questions`

Three or more Q&A pairs, in the classic format. These are for the questions a reader
actually has and the prose glossed over — the "wait, but what about…" questions. They
must be technical. "Is this hard?" is not one of them.

### 3.11 `### Bullet Points`

The compressed reference card: the commands, properties, thresholds, and formulas from
the section, in a form someone can scan a year later. Include the literal command names
and attribute names.

## 4. Numbers and accuracy

- Any device-specific figure must name the device family and, where it matters, the
  speed grade — e.g. "UltraScale+, -2 speed grade".
- Numbers that vary by device or tool version must be presented as **givens for the
  worked example**, not as universal constants. `"assume Tco = 0.4 ns from your
  report"` is correct; `"Tco is 0.4 ns"` is not.
- Tool message and rule IDs (`TIMING-*`, `CDC-*`, `DRC-*`) drift between Vivado
  releases. Name them, but say which rule set they came from and point the reader at
  `report_methodology`/`report_cdc` to list the ones their install ships.
- Never invent a datasheet number to make an example land. Restate it as an assumption
  instead — the arithmetic is the lesson, not the constant.

## 5. Figures

Analogy figures stay; they are good and they are load-bearing for the format. But an
analogy figure never counts as the section's technical content. When a figure would
carry real information — a timing diagram, an SLR floorplan, a congestion heatmap, an
annotated report — prefer that, and reference it from the prose by what it shows, not
by what it looks like.

## 6. Plan/output consistency

`toc.json` is the plan of record. Filenames and titles in `toc.json` must match the
files on disk and their `H1`s. `tools/check_sections.py` fails the build when they
diverge, so that a generator wandering off its outline is caught in CI instead of at
review time.

## 7. Regeneration checklist

Before marking a section `APPROVED`:

- [ ] Every required heading from §3 is present.
- [ ] Every analogy has a row in the Analogy → Silicon table.
- [ ] At least one worked calculation with units and a verdict.
- [ ] At least one complete, correct, pasteable artifact.
- [ ] Every question asked is answered in `### Answers`.
- [ ] At least three real tool commands or attribute names a reader can type.
- [ ] `python3 tools/check_sections.py` passes.
