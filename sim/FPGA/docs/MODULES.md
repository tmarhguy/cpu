# Module Documentation

**Detailed Documentation of All FPGA Modules**

---

## Table of Contents

- [Top-Level Modules](#top-level-modules)
- [Arithmetic Modules](#arithmetic-modules)
- [Logic Modules](#logic-modules)
- [Control Modules](#control-modules)
- [Utility Modules](#utility-modules)

---

## Top-Level Modules

### `main` - Main ALU Module

**Location**: `verilog/circuit/main.v`

**Description**: Top-level ALU module implementing all 19 operations. This is the primary interface for the ALU.

**Ports**:

| Port | Width | Direction | Description |
|------|-------|-----------|-------------|
| `A_IN` | 8 | Input | Operand A |
| `B_IN` | 8 | Input | Operand B |
| `GND` | 1 | Input | Ground reference |
| `logisimClockTree0` | 5 | Input | Clock tree (for compatibility) |
| `OVERALL` | 8 | Output | Final ALU result |
| `SUM` | 8 | Output | Arithmetic result |
| `LOGIC_OUT` | 8 | Output | Logic operation result |
| `C_OUT` | 1 | Output | Carry/Borrow flag |
| `EQUAL_FL` | 1 | Output | Zero flag (A == B for CMP) |
| `GREAT_FL` | 1 | Output | Greater than flag (A > B) |
| `LESS_FL` | 1 | Output | Less than flag (A < B) |
| `ASR` | 8 | Output | Arithmetic shift right result |
| `LSL` | 8 | Output | Logical shift left result |
| `LSR` | 8 | Output | Logical shift right result |
| `REV_A` | 8 | Output | Bit-reversed A |
| `M` | 1 | Output | ADD/SUB mode signal |

**Functionality**:
- Decodes opcode (from internal counter or external)
- Routes operands to appropriate unit (Arithmetic/Logic/Shift)
- Selects final output via multiplexer
- Generates flags (Carry, Zero, Comparison)

**Operation Selection**:
The ALU uses an internal 5-bit counter (`logisimClockTree0`) to select operations. In a real implementation, this would be replaced with an external opcode input.

---

### `logisimTopLevelShell` - Top-Level Wrapper

**Location**: `verilog/toplevel/logisimTopLevelShell.v`

**Description**: Wrapper module for FPGA integration. Provides clock generation and I/O adaptation.

**Ports**:

| Port | Width | Direction | Description |
|------|-------|-----------|-------------|
| `fpgaGlobalClock` | 1 | Input | FPGA global clock input |

**Functionality**:
- Generates synthesized clock from FPGA clock
- Provides tick generator for Logisim compatibility
- Instantiates main ALU module
- Adapts signals for FPGA I/O

---

## Arithmetic Modules

### `Adder` - 8-Bit Ripple-Carry Adder

**Location**: `verilog/arith/Adder.v`

**Description**: Parameterized adder module implementing ripple-carry addition.

**Parameters**:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `nrOfBits` | 1 | Number of bits (8 for ALU) |
| `extendedBits` | 1 | Extended bits for carry |

**Ports**:

| Port | Width | Direction | Description |
|------|-------|-----------|-------------|
| `dataA` | `nrOfBits` | Input | Operand A |
| `dataB` | `nrOfBits` | Input | Operand B |
| `carryIn` | 1 | Input | Carry input |
| `result` | `nrOfBits` | Output | Sum result |
| `carryOut` | 1 | Output | Carry output |

**Implementation**:
```verilog
assign {carryOut, result} = dataA + dataB + carryIn;
```

**Usage**:
- Used for ADD, SUB, INC, DEC operations
- SUB: B is inverted and carryIn = 1 (2's complement)
- INC: B = 0, carryIn = 1
- DEC: B = 0xFF, carryIn = 1 (via 2's complement)

**Performance**:
- **Latency**: 1 cycle (combinational)
- **Critical Path**: Through 8-bit ripple-carry chain
- **Optimization**: Could use carry-lookahead for better performance

---

## Logic Modules

### `AND_GATE` - 2-Input AND Gate

**Location**: `verilog/gates/AND_GATE.v`

**Description**: Standard 2-input AND gate.

**Ports**:
- `input1`, `input2`: Input signals
- `result`: AND output

### `AND_GATE_3_INPUTS` - 3-Input AND Gate

**Location**: `verilog/gates/AND_GATE_3_INPUTS.v`

**Description**: 3-input AND gate for control logic.

### `AND_GATE_4_INPUTS` - 4-Input AND Gate

**Location**: `verilog/gates/AND_GATE_4_INPUTS.v`

**Description**: 4-input AND gate for opcode decoding.

### `NAND_GATE_BUS` - 8-Bit NAND Bus

**Location**: `verilog/gates/NAND_GATE_BUS.v`

**Description**: 8-bit wide NAND operation (bitwise).

**Ports**:
- `input1[7:0]`, `input2[7:0]`: 8-bit operands
- `result[7:0]`: 8-bit NAND result

**Usage**: Base operation for NAND and AND (with inversion).

### `NOR_GATE` - 2-Input NOR Gate

**Location**: `verilog/gates/NOR_GATE.v`

**Description**: Standard 2-input NOR gate.

### `NOR_GATE_8_INPUTS` - 8-Input NOR Gate

**Location**: `verilog/gates/NOR_GATE_8_INPUTS.v`

**Description**: 8-input NOR gate for zero detection.

**Usage**: Detects when all 8 bits are zero (zero flag generation).

### `NOR_GATE_BUS` - 8-Bit NOR Bus

**Location**: `verilog/gates/NOR_GATE_BUS.v`

**Description**: 8-bit wide NOR operation (bitwise).

**Usage**: Base operation for NOR and OR (with inversion).

### `OR_GATE` - 2-Input OR Gate

**Location**: `verilog/gates/OR_GATE.v`

**Description**: Standard 2-input OR gate.

### `XOR_GATE_BUS_ONEHOT` - 8-Bit XOR Bus

**Location**: `verilog/gates/XOR_GATE_BUS_ONEHOT.v`

**Description**: 8-bit wide XOR operation (bitwise).

**Usage**: 
- Base operation for XOR and XNOR (with inversion)
- Used for 2's complement subtraction (B XOR M)

---

## Control Modules

### Control Unit (Embedded in `main`)

**Description**: The control unit is embedded within the `main` module. It decodes the opcode and generates control signals.

**Control Signals Generated**:

| Signal | Width | Description |
|--------|-------|-------------|
| `M` | 1 | ADD/SUB mode (0=ADD, 1=SUB) |
| `INV_OUT` | 1 | Global inversion enable |
| `SEL_ALU_SRC` | 2 | ALU source selection (Arithmetic/Logic/Shift) |
| `LOGIC_SEL` | 3 | Logic operation selection |

**Opcode Decoding**:

The control unit decodes a 5-bit opcode (currently from internal counter) into:
- Operation category (Arithmetic/Logic/Special)
- Specific operation within category
- Control signals for datapath

---

## Multiplexer Modules

### `Multiplexer_bus_2` - 2:1 8-Bit Multiplexer

**Location**: `verilog/plexers/Multiplexer_bus_2.v`

**Description**: 2-to-1 multiplexer for 8-bit buses.

**Ports**:
- `muxIn_0[7:0]`, `muxIn_1[7:0]`: Input buses
- `sel`: Selection signal
- `muxOut[7:0]`: Output bus
- `enable`: Enable signal

**Usage**: Operation selection, operand selection.

### `Multiplexer_bus_4` - 4:1 8-Bit Multiplexer

**Location**: `verilog/plexers/Multiplexer_bus_4.v`

**Description**: 4-to-1 multiplexer for 8-bit buses.

**Usage**: Shift operation selection, output routing.

### `Multiplexer_bus_8` - 8:1 8-Bit Multiplexer

**Location**: `verilog/plexers/Multiplexer_bus_8.v`

**Description**: 8-to-1 multiplexer for 8-bit buses.

**Usage**: Logic operation selection.

---

## Utility Modules

### `LogisimCounter` - Counter Module

**Location**: `verilog/memory/LogisimCounter.v`

**Description**: Counter module for opcode generation (Logisim compatibility).

**Note**: In a real implementation, this would be replaced with external opcode input.

### Clock Generation Modules

**Location**: `verilog/base/`

**Modules**:
- `synthesizedClockGenerator.v`: Generates clock from FPGA clock
- `logisimTickGenerator.v`: Generates ticks for Logisim compatibility
- `LogisimClockComponent.v`: Clock tree component

**Note**: These are primarily for Logisim compatibility. In a real FPGA implementation, use standard clocking resources.

---

## Module Hierarchy

```
logisimTopLevelShell
└── main (ALU Core)
    ├── Adder (8-bit ripple-carry)
    ├── NAND_GATE_BUS
    ├── NOR_GATE_BUS
    ├── XOR_GATE_BUS_ONEHOT
    ├── NOR_GATE_8_INPUTS (zero detection)
    ├── Multiplexer_bus_2 (multiple instances)
    ├── Multiplexer_bus_4 (multiple instances)
    ├── Multiplexer_bus_8
    ├── AND_GATE (multiple instances)
    ├── AND_GATE_3_INPUTS (multiple instances)
    ├── AND_GATE_4_INPUTS (multiple instances)
    ├── OR_GATE (multiple instances)
    ├── NOR_GATE (multiple instances)
    └── LogisimCounter (opcode generation)
```

---

## Design Notes

### Auto-Generated Code

The Verilog code was auto-generated from Logisim Evolution. As such:
- Wire names are verbose (`s_logisimNet*`, `s_logisimBus*`)
- Some modules are Logisim-specific (clock generation)
- Code structure follows Logisim's internal representation

### Optimization Opportunities

1. **Rename Wires**: Replace auto-generated names with meaningful names
2. **Remove Logisim Dependencies**: Replace clock generation with standard FPGA clocking
3. **External Opcode Input**: Replace counter with external opcode port
4. **Module Refactoring**: Break down `main` module into smaller, more manageable modules

### Industry Standards

For production use, consider:
- Following naming conventions (e.g., `_i` for inputs, `_o` for outputs)
- Adding parameter definitions
- Including synthesis directives
- Adding reset/power-on initialization
- Implementing proper clock domain crossing if needed

---

## References

- [Verilog HDL Reference Manual](https://www.xilinx.com/support/documentation/sw_manuals/xilinx14_7/ug901-vivado-synthesis.pdf)
- [FPGA Design Best Practices](https://www.xilinx.com/support/documentation/sw_manuals/xilinx2020_1/ug949-vivado-design-methodology.pdf)
