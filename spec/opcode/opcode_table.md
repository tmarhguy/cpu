# ALU Opcode Map

## Control Lines

* `M` (ADD/SUB): 0=ADD, 1=SUB (routes to B XOR network and Cin)
* `FUNC[3:0]`: selects logic sub-operation & arithmetic variants
* `SEL_ALU_SRC`: 0=Arithmetic, 1=Logic (can be derived from FUNC)
* `INV_OUT`: global post-mux inversion bit (derived from FUNC)
* `LOAD_A/B/R`: latch pulses or level enables

## Opcode Table (19 Operations)

| OPCODE Decimal | OPCODE Binary | FUNC[3:0] | Operation | Description | Implementation | Circuit Progress |
|----------------|---------------|-----------|-----------|-------------|----------------|------------------|
| 0 | 00000 | 0000 | ADD | A + B | Arithmetic: A + B | ✅ TRUE |
| 1 | 00001 | 0001 | SUB | A - B | Arithmetic: A - B (uses M=1) | ✅ TRUE |
| 2 | 00010 | 0010 | INC A | A + 1 | Arithmetic: A + 1 | ✅ TRUE |
| 3 | 00011 | 0011 | DEC A | A - 1 | Arithmetic: A - 1 (uses M=1) | ✅ TRUE |
| 4 | 00100 | 0100 | LSL / SLL | Shift left logical | Arithmetic: Shift A left by 1 bit | ✅ TRUE |
| 5 | 00101 | 0101 | LSR / SRL | Shift right logical | Arithmetic: Shift A right by 1 bit | ✅ TRUE |
| 6 | 00110 | 0110 | ASR | Arithmetic shift right | Arithmetic: Shift A right with sign extension | ✅ TRUE |
| 7 | 00111 | 0111 | REV A | Reverse A bits | Arithmetic: Reverse bit order of A | ✅ TRUE |
| 8 | 01000 | 1000 | NAND | A NAND B | Logic: Base NAND operation (INV_OUT=0) | ✅ TRUE |
| 9 | 01001 | 1001 | NOR | A NOR B | Logic: Base NOR operation (INV_OUT=0) | ✅ TRUE |
| 10 | 01010 | 1010 | XOR | A XOR B | Logic: Base XOR operation (INV_OUT=0) | ✅ TRUE |
| 11 | 01011 | 1011 | PASS A | Pass A through | Logic: Pass A to output unchanged | ✅ TRUE |
| 12 | 01100 | 1100 | PASS B | Pass B through | Logic: Pass B to output unchanged | ✅ TRUE |
| 13 | 01101 | 1101 | AND | A AND B | Logic: Implemented as NAND + invert (INV_OUT=1) | ✅ TRUE |
| 14 | 01110 | 1110 | OR | A OR B | Logic: Implemented as NOR + invert (INV_OUT=1) | ✅ TRUE |
| 15 | 01111 | 1111 | XNOR | A XNOR B | Logic: Implemented as XOR + invert (INV_OUT=1) | ✅ TRUE |
| 16 | 10000 | 0000 | CMP | Compare (A - B flags only) | Arithmetic: A - B for flags, no output | ✅ TRUE |
| 17 | 10001 | 0001 | NOT A | Invert A | Logic: Implemented as PASS A + invert (INV_OUT=1) | ✅ TRUE |
| 18 | 10010 | 0010 | NOT B | Invert B | Logic: Implemented as PASS B + invert (INV_OUT=1) | ✅ TRUE |

## Implementation Details

### Logic Operations via Inversion

The ALU implements several logic operations efficiently by using base operations with global inversion:

- **AND (Opcode 13)**: Implemented as `NOT(NAND(A,B))` = `AND(A,B)`
  - Uses NAND base operation with `INV_OUT=1`
  
- **OR (Opcode 14)**: Implemented as `NOT(NOR(A,B))` = `OR(A,B)`
  - Uses NOR base operation with `INV_OUT=1`
  
- **XNOR (Opcode 15)**: Implemented as `NOT(XOR(A,B))` = `XNOR(A,B)`
  - Uses XOR base operation with `INV_OUT=1`

- **NOT A (Opcode 17)**: Implemented as `NOT(PASS A)` = `NOT A`
  - Uses PASS A operation with `INV_OUT=1`

- **NOT B (Opcode 18)**: Implemented as `NOT(PASS B)` = `NOT B`
  - Uses PASS B operation with `INV_OUT=1`

This design reduces the number of discrete gate types needed while providing all standard logic operations.

### Arithmetic Operations

- **ADD (Opcode 0)**: Standard addition with carry propagation
- **SUB (Opcode 1)**: Subtraction using two's complement (B inverted + 1 via Cin)
- **INC A (Opcode 2)**: Increment A by 1
- **DEC A (Opcode 3)**: Decrement A by 1
- **CMP (Opcode 16)**: Compare operation that sets flags (EQUAL_FL, LESS_FL, GREAT_FL) but does not produce output data

### Shift Operations

- **LSL / SLL (Opcode 4)**: Logical shift left, fills right with 0
- **LSR / SRL (Opcode 5)**: Logical shift right, fills left with 0
- **ASR (Opcode 6)**: Arithmetic shift right, preserves sign bit

### Special Operations

- **REV A (Opcode 7)**: Reverses the bit order of A (bit 0 ↔ bit 7, bit 1 ↔ bit 6, etc.)

## Control Signal Mapping

The control unit decodes `FUNC[3:0]` (from OPCODE[3:0]) into:
- `SEL_ALU_SRC`: Selects Arithmetic (0) or Logic (1) bus
- `LOGIC_SEL[2:0]`: Selects specific logic operation (NAND, NOR, XOR, PASS A, PASS B)
- `M`: ADD/SUB mode for arithmetic (0=ADD/INC, 1=SUB/DEC)
- `INV_OUT`: Global inversion enable (0=direct, 1=inverted)
- `SHIFT_SEL[1:0]`: Selects shift operation type

## Notes

- All 19 operations are fully implemented in hardware ✅
- Opcodes 16-18 use the lower 4 bits (FUNC[3:0]) for operation selection
- The 5-bit binary opcode allows for future expansion up to 31 operations
