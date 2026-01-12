# Timing Verification Notes

This document captures the first-pass timing estimates for the ALU datapath. The numbers below are *worst-case* propagation delay estimates based on 74HC-series logic assumptions and discrete-transistor gate estimates. They are intended to bound the manual-clock (or slow-clock) operating regime and identify critical paths to revisit once concrete SPICE/Logisim timing measurements are available.

## Gate-Level Delay Assumptions

These values are intentionally conservative and reflect typical 5V 74HC-family propagation delays or equivalent discrete-transistor CMOS implementations. Where mixed logic is used, the higher delay is applied.

| Element | Assumed worst-case delay | Rationale |
| --- | --- | --- |
| Basic gate (AND/OR/NAND/NOR/NOT) | 15 ns | Typical HC logic t<sub>pd</sub> bounds. |
| XOR (74HC86) | 18 ns | XOR gates are typically slower than basic gates. |
| 2:1 MUX (74HC157) | 20 ns | Single-stage multiplexer delay. |
| 4:1 MUX (74HC153) | 25 ns | Two-level select structure. |
| 8:1 MUX (74HC151) | 30 ns | Three-level select structure. |
| Discrete transistor gate (CMOS pair) | 25 ns | Conservative estimate vs. HC ICs. |

> **Note:** The system-level documentation assumes 5V HC logic throughout and lists the 74HC-series ICs used in the ALU datapath, so these values are aligned with that logic family and its expected operating range.【F:results/schematics_metrics.md†L147-L168】

## Worst-Case Propagation Delay Calculations

### 8-Bit Ripple Adder (Arithmetic Unit)

Carry path for a single full-adder bit (worst-case):
- Generate/propagate: XOR (A ⊕ B)
- Carry logic: AND + OR

Assuming the XOR is computed in parallel for each bit, the *carry-in to carry-out* path for each stage is:

```
Tcarry_bit ≈ AND (15 ns) + OR (15 ns) = 30 ns
```

Worst-case ripple across 8 bits:

```
Tcarry_8bit ≈ 8 × 30 ns = 240 ns
```

The MSB sum output adds the final XOR stage:

```
Tsum_MSB ≈ Tcarry_7bit + XOR (18 ns)
        ≈ 7 × 30 ns + 18 ns
        ≈ 228 ns
```

If the arithmetic result then passes through the final output selection MUX (2:1), add ~20 ns:

```
Tadder_out ≈ 240 ns + 20 ns ≈ 260 ns
```

### Logic Unit

Most logic ops are single-gate (AND/OR/NOR/XOR) followed by final selection. Using a conservative 2-gate depth plus final MUX:

```
Tlogic_out ≈ 2 × 15 ns + 20 ns ≈ 50 ns
```

### MUX-Only Path (Control/Selection Network)

For paths that traverse the full selection tree (8:1 → 4:1 → 2:1):

```
Tmux_chain ≈ 30 ns + 25 ns + 20 ns ≈ 75 ns
```

## Estimated Max Clock Rate

The worst-case arithmetic path (ripple carry + final selection) dominates:

```
Tcritical ≈ 260 ns
Fmax ≈ 1 / Tcritical ≈ 3.8 MHz
```

This aligns with the system-level estimate that the ALU is expected to run in the single-digit MHz range using 74HC logic, with manual clocking as a fallback for hardware bring-up or slow stepping.【F:results/schematics_metrics.md†L147-L150】

## Simulation & Waveform References

- **Logisim Evolution** simulations are referenced in the project’s simulation milestones (1-bit adders, carry chain, and 8-bit ripple adder propagation checks).【F:results/schematics_metrics.md†L337-L341】
- **LTSpice** simulation files are documented in the repository’s simulation milestones and referenced in the debugging log workflow for waveform capture and propagation-delay analysis.【F:results/schematics_metrics.md†L335-L340】【F:docs/build-notes/debugging_log/README.md†L52-L115】

## Critical Path Summary Table

| Path | Stages/Assumptions | Worst-Case Delay | Estimated Fmax |
| --- | --- | --- | --- |
| 8-bit Adder (carry-out to result) | 8 × (AND+OR) + 2:1 MUX | ~260 ns | ~3.8 MHz |
| MUX chain (selection only) | 8:1 + 4:1 + 2:1 | ~75 ns | ~13.3 MHz |
| Logic unit (gate + select) | 2 gate levels + 2:1 MUX | ~50 ns | ~20 MHz |

> These values are placeholders until measured propagation delays are extracted from LTSpice/Logisim waveforms or hardware scope captures.
