# Topic and symptom index

Routing table from *what the engineer is actually experiencing* to the section that
addresses it. Use this before `lookup.py --search`, because a symptom ("works for hours
then crashes") rarely shares vocabulary with its cause ("clock domain crossing").

Section IDs feed straight into `lookup.py --section <id> --block <block>`.

## By symptom

| Symptom | Likely section(s) | The thing to check first |
| --- | --- | --- |
| Works for hours, then fails, then works again after reset | **2.3** | `report_cdc -details` — treat every Critical as a bug |
| Works on one board, fails on another | 1.2, 2.1, 2.3 | Rail noise → jitter → clock uncertainty; or an unsynchronized crossing |
| Works at room temperature, fails when hot | 5.2, 2.1 | $T_j$ against the corner the design was signed off at |
| Timing passes but hardware is wrong | **2.2**, 4.3 | `check_timing -verbose` — unconstrained paths do not fail, they lie |
| WNS negative on hundreds of paths by a similar tiny amount | 2.1, 4.2 | TNS/WNS ratio ⇒ systemic cause: a clock, a constraint, or congestion |
| WNS negative on one path | 4.3 | Logic/route split decides the fix; see the decomposition table |
| Utilisation far higher than expected | **3.1**, 4.1 | `report_control_sets -verbose`; then look for `DONT_TOUCH` |
| Got LUTs where DSPs/BRAMs were expected | 3.1 | A reset on the accumulator or memory array breaks inference |
| Routing fails / congestion errors | **4.2** | `report_design_analysis -congestion`; level ≥ 5 needs action |
| Design is slow despite meeting timing | **6.2** | Efficiency = beats ÷ cycles is a different number from $F_{max}$ |
| Memory bandwidth far below spec | 6.2, 1.4 | Outstanding transactions and FIFO depth, not the controller |
| `DONE` pin never goes high | **3.3** | `INIT_B`, mode pins, `CFGBVS`/`CONFIG_VOLTAGE`, encryption key state |
| Boot takes seconds | 3.3 | `SPI_BUSWIDTH`, `CONFIGRATE`, `GENERAL.COMPRESS` |
| Board fails after a field update | 3.3 | Golden image, `CONFIGFALLBACK`, `TIMER_CFG`, `BOOTSTS` |
| Bug disappears when an ILA is added | **6.1**, 2.3 | That is evidence of timing/CDC marginality, not a dead end |
| Waveform shows values that "cannot happen" | 6.1, 2.3 | ILA sampling across clock domains fabricates values |
| State machine in an unreachable state | 2.3, 4.3 | Multi-bit CDC tearing, or asynchronous reset release |
| Simulation passes, hardware fails | **3.4** | Constraints, asynchronous inputs, reset release — in that order |
| Rail sags under load | **1.2** | PDN target impedance; decoupling above capacitor self-resonance |
| Device runs hot / throttles | 5.2, 5.1 | $\theta_{JA}$ chain; leakage feedback at temperature |
| AXI transfer hangs | **3.2** | `VALID` must not depend on `READY` — run the AXI Protocol Checker |
| Data corrupts only under backpressure | 3.2 | Payload must stay stable while `VALID && !READY` |
| Board unroutable / too many layers | **1.1** | Channel budget: land diameter dominates, not trace width |
| Clock error `[Place 30-574]` | 4.2, 1.3 | `IS_GLOBAL_CLK` on the pin — do not just demote the message |

## By task

| Task | Section | Artifact you can lift |
| --- | --- | --- |
| Write a constraints file from scratch | 2.2 | Full ordered XDC with the exception-precedence rules |
| Constrain a clock crossing | 2.3 | `set_max_delay -datapath_only` **plus** `set_bus_skew` |
| Pick a CDC synchronizer | 2.3 | XPM macro decision table |
| Choose an MMCM configuration | 1.3 | VCO/divider solving, plus a complete `clk_gen` module |
| Write DSP/BRAM/SRL-inferring RTL | 3.1 | Three-pattern reference module |
| Size a FIFO | 6.2 | Little's Law + outstanding transactions |
| Budget power | 5.1 | $\alpha CV^2f$ levers; SAIF flow |
| Specify a heatsink | 5.2 | Backwards $\theta_{SA}$ calculation |
| Set up configuration and security | 3.3 | Production bitstream property set |
| Instrument a design for debug | 6.1 | Netlist-based ILA insertion script |
| Floorplan an SSI device | 1.4 | Per-SLR pblocks + `USER_SLL_REG` + hop register RTL |
| Write a self-checking testbench | 3.4 | Clocking block, scoreboard, assertions, coverage, verdict |
| Diagnose congestion | 4.2 | `congestion_triage` procedure |
| Build a sign-off gate | 4.3 | Gate that fails on unconstrained endpoints and CDC criticals |

## By Vivado command

Reverse index — an agent that sees a command in a log or script can find what it means.

| Command | Section |
| --- | --- |
| `report_timing`, `report_timing_summary` | 2.1, 4.3 |
| `check_timing` | 2.2, 4.3 |
| `report_cdc` | 2.3 |
| `report_clock_interaction`, `report_clock_networks`, `report_clocks` | 1.3, 2.2 |
| `report_clock_utilization` | 1.3 |
| `report_control_sets` | 3.1, 4.1 |
| `report_utilization`, `report_utilization -slr` | 3.1, 4.1, 1.4 |
| `report_design_analysis` | 4.2, 4.3 |
| `report_qor_suggestions`, `write_qor_suggestions` | 4.1, 4.3 |
| `report_high_fanout_nets` | 2.1, 4.2 |
| `report_exceptions` | 2.2 |
| `report_methodology` | 4.3 |
| `report_power`, `read_saif`, `power_opt_design` | 5.1 |
| `report_drc` (`UCIO-1`, `NSTD-1`, `CFGBVS-1`) | 1.1, 3.3 |
| `report_ssn` | 1.1 |
| `create_pblock`, `resize_pblock` | 1.4, 4.2 |
| `create_debug_core`, `write_debug_probes` | 6.1 |
| `write_bitstream`, `write_cfgmem` | 3.3 |
| `synth_design`, `opt_design`, `place_design`, `phys_opt_design`, `route_design` | 4.1, 4.3 |

## By primitive or macro

| Primitive / macro | Section |
| --- | --- |
| `BUFGCE`, `BUFGCE_DIV`, `BUFGCTRL`, `BUFG_GT` | 1.3 |
| `MMCME4_BASE`, `PLLE4` | 1.3 |
| `DSP48E2` | 3.1 |
| `RAMB18E2`, `RAMB36E2`, `URAM288` | 3.1, 6.1 |
| `SRL16E`/`SRL32E` | 3.1 |
| `SYSMONE4` | 1.2, 5.2 |
| Laguna / `USER_SLL_REG` | 1.4 |
| `xpm_cdc_single`, `xpm_cdc_pulse`, `xpm_cdc_gray`, `xpm_cdc_handshake`, `xpm_cdc_array_single` | 2.3 |
| `xpm_cdc_sync_rst` | 1.3, 4.3 |
| `xpm_fifo_sync`, `xpm_fifo_async` | 3.2, 6.2 |

## Cross-cutting formulas

When an agent needs the formula rather than the discussion — `--block "Do the Math"` on:

| Quantity | Section |
| --- | --- |
| Setup / hold slack | 2.1 |
| Metastability MTBF | 2.3 |
| PDN target impedance, capacitor self-resonance | 1.2 |
| BGA escape channel budget | 1.1 |
| MMCM $F_{VCO} = F_{IN}M/D$ | 1.3 |
| SLR crossing budget, HBM bandwidth | 1.4 |
| Input delay and capture window | 2.2 |
| Control set → CLB overhead | 3.1 |
| AXI bandwidth, burst efficiency | 3.2 |
| Configuration time | 3.3 |
| Coupon collector (coverage closure) | 3.4 |
| Dynamic power $\alpha CV^2f$ | 5.1 |
| Junction temperature, $\theta_{SA}$ specification | 5.2 |
| ILA BRAM cost, capture window | 6.1 |
| Little's Law, outstanding transactions | 6.2 |
