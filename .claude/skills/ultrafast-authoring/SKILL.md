---
name: ultrafast-authoring
description: >-
  Write or revise a section of the No Magic Smoke FPGA methodology book so it satisfies
  the repo's authoring contract and passes the CI check. Use this whenever adding a new
  section under docs/sections/, editing an existing one, expanding a chapter, fixing a
  technical error in the book, responding to a review comment on book content, or
  regenerating sections with a pipeline - and also when someone asks to write educational
  or Head First style technical content in this repo. The contract is mechanically
  enforced by tools/check_sections.py, so content written without it will fail the build:
  every question asked must be answered in the same section, every analogy must map to
  named silicon, every section needs a worked calculation and a complete pasteable
  artifact. Consult this before writing prose, not after.
---

# Authoring a section of No Magic Smoke

This book exists in its current form because a generation pipeline produced eighteen
sections in a convincing Head First *voice* with none of the Head First *machinery*:
eighteen questions asked and zero answered, no worked calculations, and sixty lines of
deliberately-broken toy code in the entire book. It read beautifully and taught nothing.

The fix was not better prompting. It was making the requirement checkable. That check is
`tools/check_sections.py`, and it is the reason this skill exists.

**Read `AUTHORING.md` in the repo root before writing.** It is the contract, and it
explains *why* each rule exists rather than just stating it — which matters, because a
rule you understand you can apply to a case it did not anticipate.

## The one rule everything else follows from

> **The analogy is the on-ramp, never the destination.**

An analogy earns its place by making the next paragraph land. If a reader can enjoy your
section without learning something they can type — a command, an attribute, a formula, a
primitive name — the section has failed, however good the prose is.

Mechanically: **no analogy may appear without a row in that section's `Analogy → Silicon`
table**, including the *where it breaks* column. That column is not decoration; it is what
stops a reader over-extending a metaphor into a wrong mental model. A heatsink is not
"like a hero" in any way that survives contact with $\theta_{SA}$.

## Required blocks, in order

Headings must match exactly — the checker greps for them. A `: subtitle` suffix is allowed
(`### Code Detective: The XDC Conflict`).

1. `# Section N.M: <title>` and the conversational hook
2. Concept prose — **naming real primitives**: not "clock buffer" but `BUFGCE`, not "the
   report" but `report_clock_interaction`
3. `> **Brain Power**` question, mid-section
4. `### Fireside Chat` — two concepts arguing
5. `### Analogy → Silicon` — the mapping table
6. `### Do the Math` — the worked calculation
7. `### The Real Artifact` — something complete and pasteable
8. `### Code Detective` — a realistic bug **and its corrected code**
9. `### Sharpen Your Pencil` — numbered exercises
10. `### Final Thoughts …` — the close
11. `### Answers` — full working for **every** question asked
12. `### There Are No Dumb Questions` — 3+ technical Q&A
13. `### Bullet Points` — the reference card
14. `[REVIEW_STATUS: ...]` trailer

## What the checker actually enforces

Run it early and often; it takes under a second:

```bash
python3 tools/check_sections.py
```

| Check | Why it exists |
| --- | --- |
| Every required heading present | The first draft had none of blocks 5–13 |
| `### Answers` mentions both `Brain Power` and `Sharpen Your Pencil` | 18 questions were asked and 0 answered |
| `Answers` is substantial (>150 words) | "Yes." is not showing your working |
| `Do the Math` contains an `=` | Assertions are not calculations |
| `The Real Artifact` has a code block of 20+ lines | A fragment is an illustration, not something usable |
| ≥3 code blocks total | Artifact + Code Detective + its fix |
| ≥3 distinct tool/primitive names | Generic nouns are the failure mode |
| ≥6 numbers with units | Analogy without quantity is not engineering |
| A table in the prose | The `Analogy → Silicon` mapping |
| `toc.json`, `mkdocs.yml`, `authoring/section_spec.json` and disk all agree | The generator once drifted onto 8 filenames that did not exist |

Warnings (not failures) flag hand-waving words like "magic" — if one fires, name the
mechanism instead. "Trace impedance is the magic number" became "the reflection
coefficient $\Gamma = (Z_L - Z_0)/(Z_L + Z_0)$", and the sentence got *shorter*.

## Writing the hard blocks

### `Do the Math`

State the formula symbolically, tabulate the givens **with their source**, substitute,
carry units, and end with what the number *means*.

The verdict is the point. A calculation that ends in a number teaches arithmetic; one that
ends in "so the land diameter, not the trace width, sets your layer count" teaches
engineering. Aim for a result that is *surprising* or that reverses an intuition — the
strongest examples in the book are the ones where the obvious move turns out to be wrong.

Never invent a datasheet figure to make an example land. Label it as an assumption and say
where the reader gets the real one. The transferable skill is the calculation, not the
constant.

### `The Real Artifact`

Complete enough to paste into a project: a full `.xdc`, a synthesizable module with ports
and comments explaining the pattern, a Tcl proc that runs against an open design, or a
verbatim tool report annotated line by line.

It must be correct as written. Caveats about device family or tool version go in comments
inside the block. Comments should explain *why* a line is there — the artifacts people
actually reuse are the ones that survive being read by someone who did not write them.

### `Code Detective`

Show the fix, written out. "Use `get_ports` instead" is a diagnosis; the corrected script
is a fix. Be precise about the mechanism — "blocking assignments are bad" is folklore,
whereas "`count = count + 1` updates immediately, so the `if` on the next line tests the
new value while `done <=` schedules for the end of the timestep" is a thing the reader can
reason with.

### `Answers`

Show the working, not the result. Where a question is genuinely open, say so and give the
reasoning a strong answer would contain.

Answers are also the right place to correct a misconception the question invites. If the
obvious answer is wrong, say why it is tempting first — a reader who was about to make
that mistake needs to recognise themselves in the description.

## Numbers, versions and honesty

- Device-specific figures name the family and, where it matters, the speed grade.
- Values varying by device or tool version are **givens for the worked example**, not
  constants: `"assume Tco = 0.4 ns from your report"`, never `"Tco is 0.4 ns"`.
- Tool message and rule IDs (`TIMING-*`, `CDC-*`, `DRC-*`) drift between releases. Name
  them, say which release you checked, and point at `report_methodology` / `report_cdc`.
- If you are unsure whether a primitive exists on the target family, check. The first
  draft recommended `BUFR` and `BUFH`, which do not exist on UltraScale+ — a plausible
  7-series memory that would have cost a reader a week.

## Voice

Keep it conversational. The Head First register was never this book's problem, and a
correction written in datasheet prose reads as a patch rather than as part of the text.
Contractions, second person and jokes are all fine. Vagueness is not.

## Adding a whole new section

Update all four, or the checker will tell you which you missed:

1. `docs/sections/N.M_name.md`
2. `toc.json` — id, title matching the file's `H1`, path
3. `authoring/section_spec.json` — with technical learning objectives
4. `mkdocs.yml` — nav

Then:

```bash
python3 tools/check_sections.py    # 0 errors
mkdocs build --strict              # no warnings
```

## The check is a floor, not a ceiling

Passing means the section has the right *shape*. It cannot tell you whether the
calculation is correct, whether the artifact would actually synthesise, or whether the
analogy illuminates anything. Those still need a human who knows FPGAs — which is exactly
why the contract is written down rather than assumed.
