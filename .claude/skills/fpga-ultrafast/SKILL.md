---
name: fpga-ultrafast
description: >-
  Look up AMD/Xilinx FPGA design methodology - timing closure, XDC constraints, clock
  domain crossing, RTL coding for synthesis, IP and AXI integration, synthesis and
  implementation strategy, placement and congestion, power and thermal budgeting,
  bitstream configuration and security, ILA/VIO debug, and performance tuning. Retrieves
  worked formulas, pasteable XDC/RTL/Tcl artifacts, Vivado commands and threshold values
  from an 18-section reference book. Use this whenever the work involves an FPGA, Vivado,
  Verilog/VHDL/SystemVerilog targeting AMD parts, UltraScale or UltraScale+ devices, an
  .xdc file, a timing or CDC report, or an FPGA board bring-up problem - and especially
  when asked "why is WNS negative", "how do I constrain this", "how deep should this FIFO
  be", "how many BRAMs will this cost", "why is my utilisation so high", or when a design
  works intermittently. Prefer this over answering from memory, because it supplies the
  actual command names, threshold numbers and formulas rather than plausible-sounding
  ones.
---

# AMD UltraFast FPGA methodology lookup

This skill front-ends *No Magic Smoke*, an 18-section reference on the AMD UltraFast
Design Methodology. The book is ~74,000 words, so read it through the retrieval script
rather than by opening files — a single section costs ~4,300 words of context to answer a
question that usually needs 40.

## Why retrieval beats recall here

FPGA work is full of details that are easy to half-remember and expensive to get wrong: a
primitive that exists in 7-series but not UltraScale+, a DRC rule ID, the direction of an
input-delay sign convention, whether a hold violation cares about clock period. Answering
from memory produces fluent, plausible, subtly wrong guidance — and in this domain the
cost of that lands on a board.

Every claim in this book is attached to a named command, a named primitive, or a worked
calculation. Retrieve those.

## The structure you are retrieving from

Every section carries the same named blocks, so you can go straight to the shape of answer
you need without reading prose:

| Block | Retrieve it when you need |
| --- | --- |
| `Bullet Points` | The cheat sheet: commands, attributes, thresholds, formulas. **Start here.** |
| `Do the Math` | A formula with worked substitution, units, and a verdict |
| `The Real Artifact` | Complete pasteable XDC / RTL / Tcl / annotated report |
| `Analogy → Silicon` | Which primitive a concept actually maps to |
| `Code Detective` | A realistic bug **and its corrected code** |
| `Answers` | Full reasoning on judgement calls ("should I pipeline this?") |
| `There Are No Dumb Questions` | Edge cases and "wait, but what about…" |
| `Sharpen Your Pencil` | Exercises, if you are teaching rather than solving |

## How to use it

**1. If the user describes a symptom, route it first.** Read
`references/topic-index.md`. Symptoms rarely share vocabulary with their causes — "works
for hours then crashes" is a CDC problem, and searching for "crashes" will not find it.
That file maps symptoms, tasks, Vivado commands and primitives to section IDs.

**2. Then retrieve.** `scripts/lookup.py` needs no dependencies:

```bash
python3 scripts/lookup.py --list
python3 scripts/lookup.py --search "clock domain crossing"
python3 scripts/lookup.py --section 2.3                          # Bullet Points by default
python3 scripts/lookup.py --section 2.3 --block "Do the Math"
python3 scripts/lookup.py --search metastability --block math    # search, then extract
python3 scripts/lookup.py --section 4.3 --full                   # rarely needed
```

Block names accept short aliases: `math`, `artifact`, `code`, `cheatsheet`, `answers`,
`faq`, `exercise`, `analogy`.

The script finds the book automatically when run inside this repo. Elsewhere, pass
`--book-root /path/to/no-magic-smoke-fpga` or set `NO_MAGIC_SMOKE_ROOT`. If neither is
available, the book is published at
<https://mehdibadjian.github.io/no-magic-smoke-fpga/> — section URLs follow the pattern
`.../sections/2.3_cdc_minefield/`.

**3. Answer with specifics.** Give the command the user should run, the property they
should set, or the calculation with their numbers substituted. Cite the section (e.g.
"§2.3") so they can read the reasoning.

## Judgement this book encodes

These are the recurring decision rules. They are worth knowing so you can recognise when a
lookup is warranted, but retrieve the section before acting on any of them — the details
and thresholds are what matter.

- **Read the logic/route split before choosing a timing fix.** Route-dominated →
  placement, fanout, replication. Logic-dominated → pipelining, retiming, RTL
  restructuring. Applying the wrong one costs a cycle of latency and closes nothing
  (§4.3).
- **Match the tool to the size of the deficit.** Under 50 ps → `phys_opt_design`. Over
  400 ps → architecture. A directive sweep on a −600 ps design is days spent proving you
  needed to pipeline (§4.1, §4.3).
- **Unconstrained paths do not fail, they lie** — and removing constraints *improves* WNS.
  A green report on an incomplete constraint set is a wrong answer (§2.2, §4.3).
- **`set_false_path` on a data crossing or a reset is a bug**, not a fix; it deletes
  recovery/removal analysis or lets the router stretch a synchronizer's settling time
  (§2.3, §4.3).
- **CDC failures never appear in WNS.** A clean timing report says nothing about them
  (§2.3).
- **Rarity is not safety.** Multi-bit tearing triggers on the *change*, not on how often
  it happens (§2.3).
- **Resets are a resource decision.** Reset control state, not datapath state; a reset on
  a shift register, memory array or DSP accumulator breaks inference (§3.1).
- **Widen before you accelerate.** On a bus bottleneck, width is usually the cheaper axis
  than frequency (§3.2).
- **Compute demand before buying the part** — HBM, device size, heatsink, flash interface
  (§1.4, §3.3, §5.2).

## When the book is wrong

It is a study companion, not a specification. Where it disagrees with AMD's
documentation, **the documentation wins.** Device-specific values — metastability
constants, VCO ranges, $T_{co}$, $\theta_{JC}$, SLL counts, speed-grade timing — are
presented in the book as *labelled assumptions for a worked example*, never as constants
to reuse. If a user needs a real number, tell them which report or datasheet to get it
from; `docs/references.md` in the repo has that table and the primary-source document IDs.
