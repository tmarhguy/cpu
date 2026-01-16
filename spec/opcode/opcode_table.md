# ALU Opcode Map

## Control Lines

* `M` (ADD/SUB): 0=ADD, 1=SUB (routes to B XOR network and Cin)
* `FUNC[3:0]`: selects logic sub-operation & arithmetic variants (lower 4 bits of opcode)
* `SEL_ALU_SRC`: 0=Arithmetic, 1=Logic (can be derived from FUNC)
* `INV_OUT`: global post-mux inversion bit (derived from FUNC)
* `LOAD_A/B/R`: latch pulses or level enables

## Opcode Table (19 Operations)

| OPCODE Decimal | OPCODE Binary | FUNC[3:0] | Operation | Description | Implementation | Circuit Progress |
|----------------|---------------|-----------|-----------|-------------|----------------|------------------|
| 0 | 00000 | 0000 | ADD | A + B | Arithmetic: A + B | Complete |
| 1 | 00001 | 0001 | SUB | A - B | Arithmetic: A - B (uses M=1) | Complete |
| 2 | 00010 | 0010 | INC A | A + 1 | Arithmetic: A + 1 | Complete |
| 3 | 00011 | 0011 | DEC A | A - 1 | Arithmetic: A - 1 (uses M=1) | Complete |
| 4 | 00100 | 0100 | LSL / SLL | Shift left logical | Arithmetic: Shift A left by 1 bit | Complete |
| 5 | 00101 | 0101 | LSR / SRL | Shift right logical | Arithmetic: Shift A right by 1 bit | Complete |
| 6 | 00110 | 0110 | ASR | Arithmetic shift right | Arithmetic: Shift A right with sign extension | Complete |
| 7 | 00111 | 0111 | REV A | Reverse A bits | Arithmetic: Reverse bit order of A | Complete |
| 8 | 01000 | 1000 | NAND | A NAND B | Logic: Base NAND operation (INV_OUT=0) | Complete |
| 9 | 01001 | 1001 | NOR | A NOR B | Logic: Base NOR operation (INV_OUT=0) | Complete |
| 10 | 01010 | 1010 | XOR | A XOR B | Logic: Base XOR operation (INV_OUT=0) | Complete |
| 11 | 01011 | 1011 | PASS A | Pass A through | Logic: Pass A to output unchanged | Complete |
| 12 | 01100 | 1100 | PASS B | Pass B through | Logic: Pass B to output unchanged | Complete |
| 13 | 01101 | 1101 | AND | A AND B | Logic: Implemented as NAND + invert (INV_OUT=1) | Complete |
| 14 | 01110 | 1110 | OR | A OR B | Logic: Implemented as NOR + invert (INV_OUT=1) | Complete |
| 15 | 01111 | 1111 | XNOR | A XNOR B | Logic: Implemented as XOR + invert (INV_OUT=1) | Complete |
| 16 | 10000 | 0000 | CMP | Compare (A - B flags only) | Arithmetic: A - B for flags, no output | Complete |
| 17 | 10001 | 0001 | NOT A | Invert A | Logic: Implemented as PASS A + invert (INV_OUT=1) | Complete |
| 18 | 10010 | 0010 | NOT B | Invert B | Logic: Implemented as PASS B + invert (INV_OUT=1) | Complete |

## Implementation Details

### Logic Operations via Inversion

The ALU implements several logic operations efficiently by using base operations with global inversion enabled via the `INV_OUT` control signal. This design reduces the number of discrete gate types needed while providing all standard logic operations:

- **AND (Opcode 13)**: Implemented as `NOT(NAND(A,B))` = `AND(A,B)`
  - Uses NAND base operation with `INV_OUT=1`
  - Example: `NAND(A,B) = NOT(A AND B)`, so `NOT(NAND(A,B)) = A AND B`
  
- **OR (Opcode 14)**: Implemented as `NOT(NOR(A,B))` = `OR(A,B)`
  - Uses NOR base operation with `INV_OUT=1`
  - Example: `NOR(A,B) = NOT(A OR B)`, so `NOT(NOR(A,B)) = A OR B`

- **XNOR (Opcode 15)**: Implemented as `NOT(XOR(A,B))` = `XNOR(A,B)`
  - Uses XOR base operation with `INV_OUT=1`
  - Example: `XOR(A,B) = NOT(A XNOR B)`, so `NOT(XOR(A,B)) = A XNOR B`

- **NOT A (Opcode 17)**: Implemented as `NOT(PASS A)` = `NOT A`
  - Uses PASS A operation with `INV_OUT=1`
  - Simply inverts all bits of A

- **NOT B (Opcode 18)**: Implemented as `NOT(PASS B)` = `NOT B`
  - Uses PASS B operation with `INV_OUT=1`
  - Simply inverts all bits of B

### Arithmetic Operations

- **ADD (Opcode 0)**: Standard addition with carry propagation
  - Output: A + B
  
- **SUB (Opcode 1)**: Subtraction using two's complement
  - Implementation: A - B = A + (NOT B) + 1
  - Uses M=1 to invert B and set Cin=1
  
- **INC A (Opcode 2)**: Increment A by 1
  - Output: A + 1
  
- **DEC A (Opcode 3)**: Decrement A by 1
  - Implementation: A - 1 = A + (NOT 0) + 1 = A + 11111111 + 1 = A - 1
  - Uses M=1 with B=0 to achieve subtraction
  
- **CMP (Opcode 16)**: Compare operation that sets flags but does not produce output data
  - Performs A - B internally
  - Sets flags: EQUAL_FL (A==B), LESS_FL (A<B), GREAT_FL (A>B)
  - Output bus is not used/valid for this operation

### Shift Operations

- **LSL / SLL (Opcode 4)**: Logical shift left
  - Shifts A left by 1 bit, fills rightmost bit with 0
  - Equivalent to multiplying by 2
  
- **LSR / SRL (Opcode 5)**: Logical shift right
  - Shifts A right by 1 bit, fills leftmost bit with 0
  - Equivalent to dividing by 2 (unsigned)
  
- **ASR (Opcode 6)**: Arithmetic shift right
  - Shifts A right by 1 bit, preserves sign bit (MSB)
  - Equivalent to dividing by 2 (signed)

### Special Operations

- **REV A (Opcode 7)**: Reverses the bit order of A
  - Bit 0 ↔ Bit 7, Bit 1 ↔ Bit 6, Bit 2 ↔ Bit 5, Bit 3 ↔ Bit 4
  - Example: `0b10110001` → `0b10001101`

### Pass Operations

- **PASS A (Opcode 11)**: Passes A through unchanged
  - Used as base for NOT A operation when inverted
  
- **PASS B (Opcode 12)**: Passes B through unchanged
  - Used as base for NOT B operation when inverted

## Control Signal Mapping

The control unit decodes `FUNC[3:0]` (the lower 4 bits of the 5-bit opcode) into:

- `SEL_ALU_SRC`: Selects Arithmetic (0) or Logic (1) bus
  - Opcodes 0-7, 16: Arithmetic path
  - Opcodes 8-15, 17-18: Logic path
  
- `LOGIC_SEL[2:0]`: Selects specific logic operation
  - 000: NAND (base)
  - 001: NOR (base)
  - 010: XOR (base)
  - 011: PASS A
  - 100: PASS B
  
- `M`: ADD/SUB mode for arithmetic
  - 0: ADD/INC operations
  - 1: SUB/DEC operations
  
- `INV_OUT`: Global inversion enable
  - 0: Direct output (base operations)
  - 1: Inverted output (AND, OR, XNOR, NOT A, NOT B)
  
- `SHIFT_SEL[1:0]`: Selects shift operation type (for opcodes 4-6)

## Opcode EncodingThe opcode is encoded as a 5-bit binary value (0-18 currently used, allowing expansion to 31 operations):

- **Bits [4:3]**: Category selection
  - `00`: Arithmetic operations (ADD, SUB, INC, DEC, shifts, REV)
  - `01`: Logic operations with base operations (NAND, NOR, XOR, PASS)
  - `10`: Comparison and inversion operations (CMP, NOT A, NOT B)
  - `11`: Reserved for future operations

- **Bits [3:0]**: Function code (FUNC[3:0])
  - Determines specific operation within category
  - Used for control signal generation

## Status

**All 19 operations are fully implemented in hardware**

- Core arithmetic operations: Complete
- Logic operations: Complete
- Shift operations: Complete
- Comparison and flags: Complete
- Special operations: Complete