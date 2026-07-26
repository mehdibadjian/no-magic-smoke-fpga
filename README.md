# No Magic Smoke

**A brain-friendly guide to the AMD UltraFast Design Methodology** — FPGA engineering
taught the Head First way, with the arithmetic left in.

[![Docs](https://github.com/mehdibadjian/no-magic-smoke-fpga/actions/workflows/ci.yml/badge.svg)](https://github.com/mehdibadjian/no-magic-smoke-fpga/actions/workflows/ci.yml)
[![Read it](https://img.shields.io/badge/read-online-blue)](https://mehdibadjian.github.io/no-magic-smoke-fpga/)
[![Content: CC BY 4.0](https://img.shields.io/badge/content-CC%20BY%204.0-lightgrey)](LICENSE)
[![Code: MIT](https://img.shields.io/badge/code-MIT-lightgrey)](LICENSE-CODE)

📖 **Read it here → [mehdibadjian.github.io/no-magic-smoke-fpga](https://mehdibadjian.github.io/no-magic-smoke-fpga/)**

---

## What this is

Six chapters and eighteen sections covering the UltraFast design flow end to end — board
planning, constraints, RTL, implementation, power and thermal, debug and tuning — written
in the conversational Head First style, and structured so that **you learn a skill rather
than an anecdote**.

The organising rule is one line:

> **The analogy is the on-ramp, never the destination.**

A clock tree is introduced as a conductor's baton and then immediately cashed out into
`BUFGCE`, clock regions, insertion delay, and an MMCM divider calculation you do yourself.
Metastability is a coin landing on its edge for one paragraph, and then it is
$\mathrm{MTBF} = e^{t_r/\tau} / (T_0 f_{clk} f_{data})$ with the numbers filled in — which is
how you discover that one LUT between two synchronizer flops takes a design from safe for
$10^{51}$ seconds to safe for **22 seconds**.

Every section carries the same ten blocks, in the same order:

| Block | What it does |
| --- | --- |
| **Fireside Chat** | Two concepts argue, so the tension between them is concrete |
| **Brain Power** | A question mid-section — *always* answered later in the same section |
| **Analogy → Silicon** | Each metaphor, the real construct, and **where the analogy stops being true** |
| **Do the Math** | A worked calculation: formula, substitution, units, verdict |
| **The Real Artifact** | Something complete you can paste into a project |
| **Code Detective** | Spot the flaw — then read the *corrected* code, not just the diagnosis |
| **Sharpen Your Pencil** | Exercises needing a datasheet and a calculator, no lab hardware |
| **Answers** | Full working for every question asked |
| **There Are No Dumb Questions** | The "wait, but what about…" the prose glossed over |
| **Bullet Points** | The reference card — commands, attributes, thresholds, formulas |

## What it looks like

From §4.3, *Design Closure* — three failing paths, turned into three different decisions
by arithmetic rather than by instinct:

| Path | `Data Path Delay` | logic | route | `Logic Levels` | Slack |
| --- | --- | --- | --- | --- | --- |
| A | 2.910 ns | 2.331 ns (80 %) | 0.579 ns (20 %) | 12 | −0.431 ns |
| B | 2.870 ns | 0.574 ns (20 %) | 2.296 ns (80 %) | 3 | −0.391 ns |

> **Path B** — route-dominated, only 3 levels. Pipelining would split 574 ps of logic and
> leave 2.296 ns of routing untouched:
>
> `T_new ≈ 0.089 + 0.287 + 2.296 = 2.672 ns` ⟹ slack ≈ **−0.193 ns — still failing**, and
> you have paid a cycle of latency for it. Verdict: **do not pipeline.** Attack the route.
>
> **The rule extracted:** compute the post-fix delay *before* doing the fix. Two minutes of
> arithmetic routinely saves a day of implementation runs.

That is the shape of the whole book: a number, a decision, and the reason the obvious move
is wrong.

## Contents

Links go to the rendered site, where the formulas actually render.

| # | Chapter | Sections |
| --- | --- | --- |
| 1 | **Board and Device Planning** | [PCB layout](https://mehdibadjian.github.io/no-magic-smoke-fpga/sections/1.1_pcb_layout/) · [Power planning](https://mehdibadjian.github.io/no-magic-smoke-fpga/sections/1.2_power_planning/) · [Clocking](https://mehdibadjian.github.io/no-magic-smoke-fpga/sections/1.3_clocking/) · [SSI and HBM](https://mehdibadjian.github.io/no-magic-smoke-fpga/sections/1.4_ssi_hbm/) |
| 2 | **Constraints and Analysis** | [Setup and hold](https://mehdibadjian.github.io/no-magic-smoke-fpga/sections/2.1_timing_ballet/) · [Constraints](https://mehdibadjian.github.io/no-magic-smoke-fpga/sections/2.2_constraints/) · [CDC](https://mehdibadjian.github.io/no-magic-smoke-fpga/sections/2.3_cdc_minefield/) |
| 3 | **Design Creation** | [RTL coding](https://mehdibadjian.github.io/no-magic-smoke-fpga/sections/3.1_rtl_coding/) · [IP integration](https://mehdibadjian.github.io/no-magic-smoke-fpga/sections/3.2_ip_integration/) · [Configuration and security](https://mehdibadjian.github.io/no-magic-smoke-fpga/sections/3.3_security/) · [Verification](https://mehdibadjian.github.io/no-magic-smoke-fpga/sections/3.4_verification/) |
| 4 | **Implementation** | [Synthesis](https://mehdibadjian.github.io/no-magic-smoke-fpga/sections/4.1_synthesis/) · [Place and route](https://mehdibadjian.github.io/no-magic-smoke-fpga/sections/4.2_placement/) · [Design closure](https://mehdibadjian.github.io/no-magic-smoke-fpga/sections/4.3_closure/) |
| 5 | **Power and Thermal** | [Power](https://mehdibadjian.github.io/no-magic-smoke-fpga/sections/5.1_power/) · [Thermal](https://mehdibadjian.github.io/no-magic-smoke-fpga/sections/5.2_thermal/) |
| 6 | **Debug and Validation** | [Hardware debug](https://mehdibadjian.github.io/no-magic-smoke-fpga/sections/6.1_debug/) · [Performance tuning](https://mehdibadjian.github.io/no-magic-smoke-fpga/sections/6.2_tuning/) |

Roughly 74,000 words, 88 code blocks (Tcl, SystemVerilog, Verilog, Python), and a worked
calculation in every section.

## Who it is for

- **Engineers new to AMD FPGAs** who have read UG949 and want the *why* behind its rules.
- **Experienced designers** who want the arithmetic they have been eyeballing — PDN target
  impedance, control set overhead, latency-bandwidth products, junction temperature —
  written down once.
- **Anyone who has been told "just add a false path"** and wanted to know what that
  actually deletes.

It assumes you know digital logic and some HDL. It does not assume you know Vivado.

## The quality gate

This book was generated by an LLM pipeline, and the first pass came out **bad in an
instructive way**: eighteen sections in a convincing Head First *voice* with none of the
Head First *machinery*. Eighteen questions asked, **zero answered**. Zero worked
calculations. Sixty lines of code in the whole book, all of it deliberately broken toy
snippets. Thirty-six figures, every one a metaphor picture and not one a timing diagram.

It read beautifully and taught nothing.

The fix was not better prompting — it was making the requirement *checkable*:

- **[`AUTHORING.md`](AUTHORING.md)** — the section contract, with the postmortem that
  motivates each rule.
- **[`authoring/section_spec.json`](authoring/section_spec.json)** — the machine-readable
  form, plus per-section technical objectives.
- **[`tools/check_sections.py`](tools/check_sections.py)** — enforces it in CI. The build
  fails on an unanswered question, a missing calculation, an artifact that is a fragment
  rather than something pasteable, a section with no real tool commands in it, or a
  `toc.json` that no longer matches the files on disk.

```console
$ python3 tools/check_sections.py
18 sections checked, 0 error(s), 0 warning(s)
```

On the first pass that same command reported **207 errors**. If you take one thing from
this repo and it is not about FPGAs, take that: *if you cannot write a check for the
quality you claim to want, you will not get it.*

## Build it locally

```bash
git clone https://github.com/mehdibadjian/no-magic-smoke-fpga.git
cd no-magic-smoke-fpga

pip install mkdocs-material
mkdocs serve                      # http://127.0.0.1:8000

python3 tools/check_sections.py   # run the authoring contract checks
```

## For agents

The book ships with two [Agent Skills](.claude/skills/), so an AI assistant working on an
FPGA problem can pull grounded facts out of it instead of recalling plausible ones. Full
entry point: **[`AGENTS.md`](AGENTS.md)**.

**[`fpga-ultrafast`](.claude/skills/fpga-ultrafast/)** — retrieval. Triggers on FPGA,
Vivado, XDC, timing, CDC and UltraScale work. Because every section carries the same named
blocks, retrieval is structural rather than semantic: an agent asks for `Bullet Points`
and gets the commands and thresholds, or `Do the Math` and gets the formula worked
through, without loading 4,300 words to answer a 40-word question.

```console
$ python3 .claude/skills/fpga-ultrafast/scripts/lookup.py --search "clock domain crossing"
Sections matching 'clock domain crossing':

  2.3   CDC: Crossing the Clock Domain Minefield  (score 212)
        https://mehdibadjian.github.io/no-magic-smoke-fpga/sections/2.3_cdc_minefield/

$ python3 .claude/skills/fpga-ultrafast/scripts/lookup.py --section 2.3 --block math
```

It ships a [symptom index](.claude/skills/fpga-ultrafast/references/topic-index.md) too,
because symptoms rarely share vocabulary with their causes — *"works for hours, then
crashes, then works after a reset"* is a CDC problem, and no keyword search for "crashes"
will ever find §2.3.

**[`ultrafast-authoring`](.claude/skills/ultrafast-authoring/)** — writing. Encodes the
contract so an agent adding a section produces one that passes CI, rather than another
fluent essay with no answers in it. This is the skill that would have prevented the
original failure.

Both are kept honest by the same checker: `tools/check_sections.py` fails the build if the
topic index stops routing to every section, so a new section can never be invisible to
retrieval.

## Contributing

Corrections to technical content are the most valuable thing you can send. See
[`CONTRIBUTING.md`](CONTRIBUTING.md) — the short version is that new or edited sections
must satisfy [`AUTHORING.md`](AUTHORING.md), and `python3 tools/check_sections.py` must
pass before you open a pull request.

If you find a claim that contradicts current AMD documentation, **the documentation is
right and this book is wrong.** Open an issue and it gets fixed.

## References

Primary sources, verified document numbers, and the external work this leans on are in
**[References](https://mehdibadjian.github.io/no-magic-smoke-fpga/references/)**
([source](docs/references.md)) — including a table of every number you should take from a
datasheet rather than from this book.

## Licence

- **Book content** (prose, structure, figures) — [CC BY 4.0](LICENSE). Use it, adapt it,
  teach from it, translate it; just credit it.
- **Code** (`tools/`, `authoring/`, and the HDL/Tcl/Python examples in the text) —
  [MIT](LICENSE-CODE), so the examples paste into commercial designs without friction.

## Disclaimer

This is an **independent, unofficial study companion**. It is not affiliated with,
authorised by, endorsed by, or sponsored by AMD, Inc. AMD, Xilinx, UltraScale,
UltraScale+, UltraFast, Vivado, Alveo, Zynq, Kintex, Virtex and Artix are trademarks of
Advanced Micro Devices, Inc. *Head First* is a trademark of O'Reilly Media, Inc. All
trademarks are the property of their respective owners and are used here only to identify
the products discussed.

The content was **generated with AI assistance and reviewed by a human**, which is exactly
why the authoring contract and the CI checks exist. It is offered for education. It is not
engineering advice, it carries no warranty, and no calculation in it substitutes for your
device's datasheet or your own analysis. Verify before you commit silicon.
