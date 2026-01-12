# Opcode Implementation Status

This table tracks the implementation status of each ALU opcode and links to the
current simulation artifacts and test-vector documentation.

**Status definitions**
- **Designed**: Specified in the opcode map.
- **Simulated**: Covered by the Logisim ALU model.
- **Verified**: Backed by concrete test vectors (not yet available).
- **Hardware-tested**: Validated on physical hardware (not yet recorded).
- **Legend**: ✅ complete, ⏳ pending.

| Opcode (dec/bin) | Operation | Designed | Simulated | Verified | Hardware-tested | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| 0 / `00000` | ADD | ✅ | ✅ | ⏳ | ⏳ | Spec: [opcode_table.md](../../spec/opcode/opcode_table.md); Simulation: [logisim/top/alu_top.circ](../../logisim/top/alu_top.circ); Test vectors: [test/README.md](../../test/README.md) |
| 1 / `00001` | SUB | ✅ | ✅ | ⏳ | ⏳ | Spec: [opcode_table.md](../../spec/opcode/opcode_table.md); Simulation: [logisim/top/alu_top.circ](../../logisim/top/alu_top.circ); Test vectors: [test/README.md](../../test/README.md) |
| 2 / `00010` | INC A | ✅ | ✅ | ⏳ | ⏳ | Spec: [opcode_table.md](../../spec/opcode/opcode_table.md); Simulation: [logisim/top/alu_top.circ](../../logisim/top/alu_top.circ); Test vectors: [test/README.md](../../test/README.md) |
| 3 / `00011` | DEC A | ✅ | ✅ | ⏳ | ⏳ | Spec: [opcode_table.md](../../spec/opcode/opcode_table.md); Simulation: [logisim/top/alu_top.circ](../../logisim/top/alu_top.circ); Test vectors: [test/README.md](../../test/README.md) |
| 4 / `00100` | LSL / SLL | ✅ | ✅ | ⏳ | ⏳ | Spec: [opcode_table.md](../../spec/opcode/opcode_table.md); Simulation: [logisim/top/alu_top.circ](../../logisim/top/alu_top.circ); Test vectors: [test/README.md](../../test/README.md) |
| 5 / `00101` | LSR / SRL | ✅ | ✅ | ⏳ | ⏳ | Spec: [opcode_table.md](../../spec/opcode/opcode_table.md); Simulation: [logisim/top/alu_top.circ](../../logisim/top/alu_top.circ); Test vectors: [test/README.md](../../test/README.md) |
| 6 / `00110` | ASR | ✅ | ✅ | ⏳ | ⏳ | Spec: [opcode_table.md](../../spec/opcode/opcode_table.md); Simulation: [logisim/top/alu_top.circ](../../logisim/top/alu_top.circ); Test vectors: [test/README.md](../../test/README.md) |
| 7 / `00111` | REV A | ✅ | ✅ | ⏳ | ⏳ | Spec: [opcode_table.md](../../spec/opcode/opcode_table.md); Simulation: [logisim/top/alu_top.circ](../../logisim/top/alu_top.circ); Test vectors: [test/README.md](../../test/README.md) |
| 8 / `01000` | NAND | ✅ | ✅ | ⏳ | ⏳ | Spec: [opcode_table.md](../../spec/opcode/opcode_table.md); Simulation: [logisim/top/alu_top.circ](../../logisim/top/alu_top.circ); Test vectors: [test/README.md](../../test/README.md) |
| 9 / `01001` | NOR | ✅ | ✅ | ⏳ | ⏳ | Spec: [opcode_table.md](../../spec/opcode/opcode_table.md); Simulation: [logisim/top/alu_top.circ](../../logisim/top/alu_top.circ); Test vectors: [test/README.md](../../test/README.md) |
| 10 / `01010` | XOR | ✅ | ✅ | ⏳ | ⏳ | Spec: [opcode_table.md](../../spec/opcode/opcode_table.md); Simulation: [logisim/top/alu_top.circ](../../logisim/top/alu_top.circ); Test vectors: [test/README.md](../../test/README.md) |
| 11 / `01011` | PASS A | ✅ | ✅ | ⏳ | ⏳ | Spec: [opcode_table.md](../../spec/opcode/opcode_table.md); Simulation: [logisim/top/alu_top.circ](../../logisim/top/alu_top.circ); Test vectors: [test/README.md](../../test/README.md) |
| 12 / `01100` | PASS B | ✅ | ✅ | ⏳ | ⏳ | Spec: [opcode_table.md](../../spec/opcode/opcode_table.md); Simulation: [logisim/top/alu_top.circ](../../logisim/top/alu_top.circ); Test vectors: [test/README.md](../../test/README.md) |
| 13 / `01101` | AND | ✅ | ✅ | ⏳ | ⏳ | Spec: [opcode_table.md](../../spec/opcode/opcode_table.md); Simulation: [logisim/top/alu_top.circ](../../logisim/top/alu_top.circ); Test vectors: [test/README.md](../../test/README.md) |
| 14 / `01110` | OR | ✅ | ✅ | ⏳ | ⏳ | Spec: [opcode_table.md](../../spec/opcode/opcode_table.md); Simulation: [logisim/top/alu_top.circ](../../logisim/top/alu_top.circ); Test vectors: [test/README.md](../../test/README.md) |
| 15 / `01111` | XNOR | ✅ | ✅ | ⏳ | ⏳ | Spec: [opcode_table.md](../../spec/opcode/opcode_table.md); Simulation: [logisim/top/alu_top.circ](../../logisim/top/alu_top.circ); Test vectors: [test/README.md](../../test/README.md) |
| 16 / `10000` | CMP | ✅ | ✅ | ⏳ | ⏳ | Spec: [opcode_table.md](../../spec/opcode/opcode_table.md); Simulation: [logisim/top/alu_top.circ](../../logisim/top/alu_top.circ); Test vectors: [test/README.md](../../test/README.md) |
| 17 / `10001` | NOT A | ✅ | ✅ | ⏳ | ⏳ | Spec: [opcode_table.md](../../spec/opcode/opcode_table.md); Simulation: [logisim/top/alu_top.circ](../../logisim/top/alu_top.circ); Test vectors: [test/README.md](../../test/README.md) |
| 18 / `10010` | NOT B | ✅ | ✅ | ⏳ | ⏳ | Spec: [opcode_table.md](../../spec/opcode/opcode_table.md); Simulation: [logisim/top/alu_top.circ](../../logisim/top/alu_top.circ); Test vectors: [test/README.md](../../test/README.md) |
