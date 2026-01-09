# Component Inventory - ALU Top Circuit

Detailed breakdown of all components used in the `alu_top.circ` Logisim circuit.

**Analysis Date:** 2026-01-08  
**Circuit File:** `logisim/top/alu_top.circ`  
**Total Components:** 315

---

## Gates (86 total)

### AND Gates (30 total)

| Input Size | Bit Width | Count | Notes |
|------------|-----------|-------|-------|
| 2-input    | 1-bit     | 10    | Standard 2-input AND |
| 3-input    | 1-bit     | 1     | 3-input AND gate |
| 4-input    | 1-bit     | 19    | 4-input AND gate (most common) |

**Input Sizes Used:** 2, 3, 4  
**NOT Used:** 5, 6, 7, 8+ inputs

### OR Gates (8 total)

| Input Size | Bit Width | Count | Notes |
|------------|-----------|-------|-------|
| 2-input    | 1-bit     | 7     | Standard 2-input OR |
| 3-input    | 1-bit     | 1     | 3-input OR gate |

**Input Sizes Used:** 2, 3  
**NOT Used:** 4, 5, 6, 7, 8+ inputs

### NOT Gates (41 total)

| Bit Width | Count | Notes |
|-----------|-------|-------|
| 1-bit     | 40    | Single-bit inverters |
| 8-bit     | 1     | 8-bit wide inverter |

**Note:** NOT gates are unary operators (no input count attribute).

### NAND Gates (1 total)

| Input Size | Bit Width | Count | Notes |
|------------|-----------|-------|-------|
| 2-input    | 8-bit     | 1     | 8-bit wide NAND |

### NOR Gates (3 total)

| Input Size | Bit Width | Count | Notes |
|------------|-----------|-------|-------|
| 2-input    | 1-bit     | 1     | Standard NOR |
| 2-input    | 8-bit     | 1     | 8-bit wide NOR |
| 8-input    | 1-bit     | 1     | 8-input NOR (zero detection) |

**Input Sizes Used:** 2, 8  
**NOT Used:** 3, 4, 5, 6, 7 inputs

### XOR Gates (3 total)

| Input Size | Bit Width | Count | Notes |
|------------|-----------|-------|-------|
| 2-input    | 8-bit     | 3     | 8-bit wide XOR |

---

## Multiplexers (6 total)

| Type      | Select Bits | Width | Count | Notes |
|-----------|-------------|-------|-------|-------|
| 2:1 MUX   | 1-bit       | 8-bit | 2     | 2-to-1 multiplexer |
| 4:1 MUX   | 2-bit       | 8-bit | 3     | 4-to-1 multiplexer |
| 8:1 MUX   | 3-bit       | 8-bit | 1     | 8-to-1 multiplexer |

**MUX Types Used:**
- 2:1 MUX (1-bit select, 8-bit data)
- 4:1 MUX (2-bit select, 8-bit data)  
- 8:1 MUX (3-bit select, 8-bit data)

**NOT Used:**
- 16:1 MUX (4-bit select)
- Higher order MUXes

---

## Arithmetic Components (1 total)

| Component | Width | Count | Notes |
|-----------|-------|-------|-------|
| Adder     | 1-bit | 1     | Single-bit adder (likely part of larger adder chain) |

---

## Wiring & Interconnect Components

### Splitters (47 total)

| Fanout | Incoming | Count | Notes |
|--------|----------|-------|-------|
| 3      | 3        | 2     | 3-way splitter |
| 4      | 4        | 22    | 4-way splitter (most common) |
| 5      | 5        | 10    | 5-way splitter |
| 8      | 8        | 10    | 8-way splitter |
| Unspecified | - | 3     | Default splitter |

**Fanout Sizes Used:** 3, 4, 5, 8  
**NOT Used:** 2, 6, 7, 9+ fanouts

### Tunnels (126 total)

| Width | Count | Notes |
|-------|-------|-------|
| 1-bit (default) | 67 | Single-bit signal tunnels |
| 2-bit | 3 | 2-bit bus tunnels |
| 3-bit | 3 | 3-bit bus tunnels |
| 5-bit | 11 | 5-bit bus tunnels (likely control signals) |
| 8-bit | 42 | 8-bit bus tunnels (data buses) |

---

## I/O Components

### Pins (21 total)

| Type | Width | Count | Notes |
|------|-------|-------|-------|
| Input/Output | 1-bit | 7 | Single-bit I/O pins |
| Input/Output | 2-bit | 1 | 2-bit I/O pin |
| Input/Output | 8-bit | 13 | 8-bit I/O pins (data ports) |

### LEDs (20 total)

| Type | Count | Notes |
|------|-------|-------|
| LED | 20 | Display indicators (likely for debugging/monitoring) |

---

## Other Components

| Component     | Count | Notes |
|---------------|-------|-------|
| Bit Extender  | 2     | Extends 1-bit to 8-bit |
| Clock         | 1     | Clock source |
| Constant      | 2     | 8-bit constant values |
| Counter       | 1     | 5-bit counter (0-31) |
| Text          | 2     | Label annotations |

---

## Summary Statistics

### Gate Summary
- **Total Gates:** 86
  - AND: 30
  - OR: 8
  - NOT: 41
  - NAND: 1
  - NOR: 3
  - XOR: 3

### Multiplexer Summary
- **Total MUXes:** 6
  - 2:1 MUX: 2
  - 4:1 MUX: 3
  - 8:1 MUX: 1

### Component Size Patterns

**AND Gates:**
- ✅ Used: 2-input, 3-input, 4-input
- ❌ Not used: 5-input, 6-input, 7-input, 8+ inputs

**OR Gates:**
- ✅ Used: 2-input, 3-input
- ❌ Not used: 4-input, 5-input, 6-input, 7-input, 8+ inputs

**NOR Gates:**
- ✅ Used: 2-input, 8-input
- ❌ Not used: 3-input, 4-input, 5-input, 6-input, 7-input

**Multiplexers:**
- ✅ Used: 2:1, 4:1, 8:1
- ❌ Not used: 16:1, 32:1, or higher order MUXes

**Splitters:**
- ✅ Used: 3-way, 4-way, 5-way, 8-way
- ❌ Not used: 2-way, 6-way, 7-way, 9+ way

---

## Design Notes

1. **Gate Input Limitations:** The design avoids gates with 5+ inputs, preferring to use multiple smaller gates or different circuit topologies.

2. **Bit Widths:** Most gates operate on 1-bit signals, with wider 8-bit operations handled by specialized components (XOR, NAND, NOR) or by parallel 1-bit implementations.

3. **MUX Usage:** The multiplexer hierarchy (2:1, 4:1, 8:1) suggests a tree-based selection strategy for routing multiple data paths.

4. **Wiring Complexity:** The large number of tunnels (126) indicates significant signal routing throughout the design.

---

*Generated by: `tools/analyze_components.py`*

