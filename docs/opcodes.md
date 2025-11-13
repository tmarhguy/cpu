# ALU Opcode Map

## Control Lines

* `M` (ADD/SUB): 0=ADD, 1=SUB (routes to B XOR network and Cin)
* `FUNC[3:0]`: selects logic sub-operation & arithmetic variants
* `SEL_ALU_SRC`: 0=Arithmetic, 1=Logic (can be derived from FUNC)
* `INV_OUT`: global post-mux inversion bit (derived from FUNC)
* `LOAD_A/B/R`: latch pulses or level enables

## 16-Code Opcode Map

| FUNC[3:0] | Operation | Description | Arithmetic/Logic | M | INV_OUT |
|-----------|-----------|-------------|------------------|---|---------|
| 0000 | ADD | A + B | Arithmetic | 0 | 0 |
| 0001 | SUB | A - B | Arithmetic | 1 | 0 |
| 0010 | INC A | A + 1 | Arithmetic | 0 | 0 |
| 0011 | DEC A | A - 1 | Arithmetic | 1 | 0 |
| 0100 | NAND | A NAND B | Logic (base=NAND) | - | 0 |
| 0101 | AND | A AND B | Logic (base=NAND) | - | 1 |
| 0110 | NOR | A NOR B | Logic (base=NOR) | - | 0 |
| 0111 | OR | A OR B | Logic (base=NOR) | - | 1 |
| 1000 | XNOR | A XNOR B | Logic (base=XNOR) | - | 0 |
| 1001 | XOR | A XOR B | Logic (base=XNOR) | - | 1 |
| 1010 | PASS A | Pass A through | Logic (base=PASS A) | - | 0 |
| 1011 | NOT A | Invert A | Logic (base=PASS A) | - | 1 |
| 1100 | PASS B | Pass B through | Logic (base=PASS B) | - | 0 |
| 1101 | NOT B | Invert B | Logic (base=PASS B) | - | 1 |
| 1110 | ZERO | Output 0x00 | Logic (base=ZERO) | - | 0 |
| 1111 | ONE | Output 0xFF | Logic (base=ZERO) | - | 1 |

## Implementation Notes

The control unit decodes `FUNC[3:0]` into:
- `SEL_ALU_SRC`: Selects Arithmetic (0) or Logic (1) bus
- `LOGIC_SEL[2:0]`: Selects specific logic operation
- `M`: ADD/SUB mode for arithmetic
- `INV_OUT`: Global inversion enable

