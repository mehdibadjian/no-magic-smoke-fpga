# References

This guide is a study companion, not a substitute for primary documentation. Where the
two disagree, **the vendor documentation is right and this book is wrong** — tell us, and
we will fix it.

Document numbers were checked in July 2026. AMD revises, renumbers and retires documents
between tool releases, so treat the number as a search key rather than a permanent
address: search [docs.amd.com](https://docs.amd.com) for the document ID and pick the
version matching *your* Vivado release. Device-specific values (VCO bands, $\tau$ and
$T_0$ for metastability, SLL counts, thermal resistances, speed-grade timing) must come
from the datasheet for your exact part — the numbers in this book are labelled as
worked-example givens for a reason.

---

## The methodology itself

The document this guide is a companion to:

| ID | Title | Why it matters here |
| --- | --- | --- |
| **UG949** | *UltraFast Design Methodology Guide for FPGAs and SoCs* | The source methodology. Every chapter of this book maps to a part of it. |
| **UG1292** | *UltraFast Design Methodology Timing Closure Quick Reference Guide* | The condensed checklist version. Chapters 2 and 4 lean on it heavily. |

## Vivado Design Suite user guides

| ID | Title | Used in |
| --- | --- | --- |
| **UG901** | *Vivado Design Suite User Guide: Synthesis* | §3.1 (inference, attributes), §4.1 (directives, `DONT_TOUCH`, retiming) |
| **UG903** | *Vivado Design Suite User Guide: Using Constraints* | §1.3, §2.1, §2.2, §2.3 — XDC ordering, exception precedence, CDC constraints |
| **UG904** | *Vivado Design Suite User Guide: Implementation* | §4.2, §4.3 — placement, routing, `phys_opt_design`, incremental flow |
| **UG906** | *Vivado Design Suite User Guide: Design Analysis and Closure Techniques* | §2.1, §4.2, §4.3 — reading timing reports, congestion levels, QoR suggestions |
| **UG907** | *Vivado Design Suite User Guide: Power Analysis and Optimization* | §5.1 — `report_power`, SAIF flow, `power_opt_design` |
| **UG908** | *Vivado Design Suite User Guide: Programming and Debugging* | §6.1 — ILA, VIO, capture control, `create_debug_core` |
| **UG835** | *Vivado Design Suite Tcl Command Reference Guide* | Every Tcl artifact in the book |
| **UG912** | *Vivado Design Suite Properties Reference Guide* | The object properties used throughout (`IS_GLOBAL_CLK`, `LOGIC_LEVELS`, `IOBANK`, …) |
| **UG974** | *UltraScale Architecture Libraries Guide* | §1.3, §2.3, §6.1 — primitives and the **XPM** parameterized macros (`xpm_cdc_*`, `xpm_fifo_*`) |
| **UG1037** | *Vivado Design Suite: AXI Reference Guide* | §3.2, §6.2 — AXI concepts and AMD's AXI tooling |

## UltraScale / UltraScale+ architecture guides

| ID | Title | Used in |
| --- | --- | --- |
| **UG570** | *UltraScale Architecture Configuration User Guide* | §3.3 — configuration sequence, mode pins, multi-boot, encryption, authentication |
| **UG571** | *UltraScale Architecture SelectIO Resources User Guide* | §1.1 — I/O standards, banking rules, $V_{CCO}$, `SLEW`/`DRIVE` |
| **UG572** | *UltraScale Architecture Clocking Resources User Guide* | §1.3 — `BUFGCE`, `BUFGCE_DIV`, `BUFGCTRL`, MMCM/PLL, clock regions |
| **UG573** | *UltraScale Architecture Memory Resources User Guide* | §3.1, §6.1 — `RAMB18E2`/`RAMB36E2`, `URAM288`, inference rules |
| **UG574** | *UltraScale Architecture Configurable Logic Block User Guide* | §3.1, §4.1 — the CLB structure behind the control set arithmetic |
| **UG578** | *UltraScale Architecture GTH/GTY Transceivers User Guide* | §1.4, §5.1 — transceiver clocking and power |
| **UG579** | *UltraScale Architecture DSP Slice User Guide* | §3.1 — `DSP48E2` pipeline registers, 27×18 multiplier, pre-adder |
| **UG580** | *UltraScale Architecture System Monitor User Guide* | §1.2, §5.2 — SYSMON, the temperature transfer function, alarm registers |
| **UG583** | *UltraScale Architecture PCB Design User Guide* | §1.1, §1.2 — stackup, decoupling, PDN, breakout routing |

## LogiCORE IP product guides

| ID | Title | Used in |
| --- | --- | --- |
| **PG057** | *FIFO Generator* | §3.2, §6.2 |
| **PG059** | *AXI Interconnect* | §3.2 — width/clock conversion and its cost |
| **PG037** | *AXI Performance Monitor* | §6.2 — the APM, and what its stall counters mean |
| **PG150** | *UltraScale Architecture-Based FPGAs Memory IP* | §6.2 — DDR4 controller behaviour |
| **PG276** | *AXI High Bandwidth Memory Controller* | §1.4 — the HBM AXI port count, width and clocking that the bandwidth arithmetic uses |

## Standards

| Reference | Relevance |
| --- | --- |
| **ARM IHI 0022**, *AMBA AXI and ACE Protocol Specification* | §3.2 — the authoritative source for the four handshake rules, including "`VALID` must not depend on `READY`" |
| **IEEE 1800**, *SystemVerilog Language Reference Manual* | §3.1, §3.4 — event regions and scheduling semantics, which is what makes the testbench race in §3.4 a *specified* non-determinism rather than a simulator quirk |
| **IEEE 1364.1**, *Verilog Register Transfer Level Synthesis* | §3.1 — what synthesis is required to infer |
| **JEDEC JESD235**, *High Bandwidth Memory (HBM) DRAM* | §1.4 — HBM stack organisation |

## Books and papers

The external work this guide's technical content leans on:

- **Clifford E. Cummings**, *"Nonblocking Assignments in Verilog Synthesis, Coding Styles
  That Kill!"*, SNUG 2000. — The definitive treatment of the `=` vs `<=` bug in §3.1.
- **Clifford E. Cummings**, *"Clock Domain Crossing (CDC) Design & Verification Techniques
  Using SystemVerilog"*, SNUG 2008. — Background for all of §2.3.
- **Clifford E. Cummings**, *"Simulation and Synthesis Techniques for Asynchronous FIFO
  Design"*, SNUG 2002. — Gray-coded pointers and why they work.
- **Ryan Donohue**, *"Synchronization in Digital Logic Circuits"*. — A clear derivation of
  the metastability MTBF formula used in §2.3.
- **Howard Johnson & Martin Graham**, *High-Speed Digital Design: A Handbook of Black
  Magic* (Prentice Hall, 1993). — Transmission lines, return paths and edge rates in §1.1.
- **Eric Bogatin**, *Signal and Power Integrity — Simplified* (Prentice Hall). — PDN
  target impedance and capacitor self-resonance in §1.2.
- **John D. C. Little**, *"A Proof for the Queuing Formula $L = \lambda W$"*, Operations
  Research 9(3), 1961. — The result that sizes every buffer in §6.2.
- **Peter Alfke**, *"Efficient Shift Registers, LFSR Counters, and Long Pseudo-Random
  Sequence Generators"*, Xilinx application note. — Background on SRL usage in §3.1.

## On the format

- **Kathy Sierra & Bert Bates**, the *Head First* series (O'Reilly). — The pedagogy this
  book borrows: concrete example → do it yourself → check your answer → compress into a
  reference. The devices used here (*Brain Power*, *Sharpen Your Pencil*, *There Are No
  Dumb Questions*, *Bullet Points*) are theirs. This project is an independent homage and
  is not affiliated with or endorsed by O'Reilly Media.

  Their design principles are set out in the *"How to use this book"* introduction that
  opens every Head First title, and it is worth reading once even if you never write a
  book — the argument for why an unanswered question is worse than no question is the
  reason [`AUTHORING.md`](https://github.com/mehdibadjian/no-magic-smoke-fpga/blob/main/AUTHORING.md)
  exists.

---

## A note on numbers in this book

Every worked example states its givens, and every device-specific figure is presented as
an *assumption for the arithmetic* rather than as a constant. This is deliberate, and the
authoring contract requires it: the transferable skill is the calculation, not the
constant. Specifically, do not lift these from the book into a real design —

| Quantity | Get it from |
| --- | --- |
| $\tau$, $T_0$ (metastability constants) | The device datasheet / AMD's metastability data for your family and speed grade |
| MMCM/PLL VCO range | The device datasheet, per speed grade |
| SLL count per SLR boundary, Laguna sites | The device datasheet; `report_design_analysis` for what you used |
| $T_{co}$, $T_{su}$, $T_h$ | Your own `report_timing` output |
| $\theta_{JC}$ | The package thermal data for your device |
| $\theta_{SA}$ | The heatsink vendor, **at the airflow your chassis actually delivers** |
| Bitstream size | Your own `write_bitstream` log |
| Congestion levels, control set counts | Your own `report_design_analysis` / `report_control_sets` |

---

*Found an error, a stale document number, or a claim that contradicts the current
documentation?* [Open an issue](https://github.com/mehdibadjian/no-magic-smoke-fpga/issues).
Corrections to technical content are the most valuable contribution you can make here.
