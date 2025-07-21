Below is a **no‑hand‑waving, engineering‑ready MVP spec** for your discrete‑transistor 8‑bit CPU. Follow this and you’ll have a _demo‑able_, scope‑controlled silicon‑to‑software stack that recruiters (and professors) can run in a browser **and** watch on a scope.

---

## 0 ️⃣ High‑Level Goals (MVP)

| Goal                  | Target                                                                                                                               |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **Instruction Set**   | 16 instructions, 8‑bit opcode, 8‑bit operands                                                                                        |
| **Clock**             | 1.0 kHz–5 kHz stable (test at 3.3 V & 5 V)                                                                                           |
| **Transistor Budget** | ≤ 800 discrete MOSFETs (≈15 breadboards or 1‑layer PCB)                                                                              |
| **Core Modules**      | 4‑bit × 2 ALU slices (carry ripple), 2 general‑purpose registers, 1 program counter, 1 IR, 128‑byte RAM (static), hard‑wired control |
| **Demo Program**      | Fibonacci (0–12), result in memory, blinking LED on overflow                                                                         |
| **Software Stack**    | Python‑based assembler → hex binary → simulator (Py + WASM)                                                                          |
| **Measurement Proof** | Scope screenshot of ALU add cycle & instruction timing table                                                                         |
| **Deliverables**      | Schematics (KiCad), BOM CSV, test harness, README & GIF demo                                                                         |

---

## 1 ️⃣ Architectural Decisions

### 1.1 Data Path Width

- **8‑bit word size** (simpler address muxing, fits 7400‑series SRAM easily).

### 1.2 Register File

- 2 general‑purpose registers **R0, R1** (8 bits each).
- 1 accumulator **A** (shared with ALU output).
- 1 **Program Counter** (PC) 8 bits (wrap at 256).

### 1.3 ALU

- Uses **two 4‑bit ripple‑carry slices** (74HC283 equivalent with discrete transistors).
- Operations: ADD, SUB (2’s complement via XOR + ADD), AND, OR, XOR, NOT, SHL, SHR.

### 1.4 Control Logic

- **Hard‑wired micro‑sequencer**: 6 micro‑states per instruction (Fetch, Decode, Execute‑(n)).
- 4‑bit synchronous counter drives micro‑step lines.

### 1.5 Memory

- **Static RAM** 128 B (can bootstrap with 6264 or discrete latch array). 8‑bit address bus.
- Separate **32‑B ROM** (EEPROM or DIP switch) for micro‑code if you later micro‑program.

### 1.6 Bus

- **Single 8‑bit bidirectional data bus** with tri‑state transistor buffers (CD4050 or discrete n‑MOSFET pass arrays).
- Address bus 8 bit unidirectional.

### 1.7 Clock

- **Schmitt‑trigger RC oscillator** (4093) + divide‑by‑N flip‑flops for 1–10 kHz.
- Clock gating switch for _single‑step_ mode w/ debounced push‑button.

### 1.8 I/O for MVP

- Memory‑mapped LED register at address `0xF0`.
- Simple input DIP switch port at `0xF1`.
- Later: serial UART.

---

## 2 ️⃣ Instruction Set (v0.9)

| Opcode | Mnemonic  | Operands | Cycles | Description                  |
| ------ | --------- | -------- | ------ | ---------------------------- |
| `0x00` | `NOP`     | –        | 1      | No operation                 |
| `0x10` | `LDA imm` | #byte    | 2      | A ← imm                      |
| `0x11` | `LDA mem` | addr     | 4      | A ← M\[addr]                 |
| `0x12` | `STA mem` | addr     | 4      | M\[addr] ← A                 |
| `0x20` | `ADD mem` | addr     | 4      | A ← A + M\[addr]             |
| `0x21` | `SUB mem` | addr     | 4      | A ← A − M\[addr]             |
| `0x22` | `AND mem` | addr     | 4      | A ← A & M\[addr]             |
| `0x23` | `OR mem`  | addr     | 4      | A ← A ∨ M\[addr]             |
| `0x30` | `JMP`     | addr     | 3      | PC ← addr                    |
| `0x31` | `JZ`      | addr     | 3      | if Z == 1 then PC ← addr     |
| `0x32` | `JC`      | addr     | 3      | if Carry == 1 then PC ← addr |
| `0x40` | `INC`     | A        | 2      | A ← A + 1                    |
| `0x41` | `DEC`     | A        | 2      | A ← A − 1                    |
| `0x50` | `SHL`     | A        | 2      | A ← A << 1                   |
| `0x51` | `SHR`     | A        | 2      | A ← A >> 1                   |
| `0x60` | `OUT`     | addr     | 3      | M\[addr] ← A (LED map)       |
| `0xFF` | `HLT`     | –        | 1      | Halt clock (stop latch)      |

**Status Flags**: Zero, Carry, Negative (bit 7), Overflow (optional).

---

## 3 ️⃣ Build Phases & Milestones

| Phase                                | Duration           | Deliverable                                                               | Verification                                     |
| ------------------------------------ | ------------------ | ------------------------------------------------------------------------- | ------------------------------------------------ |
| **P0 Spec & Tooling**                | 3 days             | ISA doc, Python assembler skeleton, Py simulator v0.1 (no timing)         | Sim runs Fibonacci → matches expected            |
| **P1 ALU Slice**                     | 7 days             | Discrete 4‑bit adder + logic gates on breadboard                          | Scope: 4‑bit ADD 0x5 + 0x3 = 0x8 (carry etc.)    |
| **P2 Register File + Bus Buffers**   | 6 days             | Latches (74HC573 equiv) using transistors or HC chips; tri‑state controls | Write→Read round‑trip ≤ 120 ns (logic probe)     |
| **P3 Program Counter & Incrementer** | 4 days             | 8‑bit ripple counter + buffer                                             | Single‑step mode increments sequentially         |
| **P4 Control Sequencer**             | 10 days            | 6‑state micro‑cycle counter + PLA‑style decode                            | LED lines show T0‑T5; confirm via logic analyzer |
| **P5 Clock & Single‑Step**           | 2 days             | RC osc + flip‑flop gating                                                 | Scope: 0→1 edges stable ±5 %                     |
| **P6 Integration v0**                | 7 days             | Fetch + Decode + `NOP`                                                    | PC increments, bus idle stable                   |
| **P7 Core Instruction Set**          | 14 days            | Implement LDA/STA/ADD/SUB/JMP/JZ                                          | Run mini test ROM; compare to sim                |
| **P8 Memory Map + LED Port**         | 3 days             | LED register at 0xF0                                                      | `OUT 0xF0` flips LEDs in hardware                |
| **P9 Demo Program**                  | 5 days             | Fibonacci to 12, blink LED                                                | Observe LED blink pattern matches sim            |
| **P10 PCB/Perfboard**                | 14 days (parallel) | KiCad schematics, 1‑layer board, solder first batch                       | Bring‑up replicate breadboard tests              |
| **Launch**                           | –                  | GIF + scope screenshot + README + WASM sim embed                          | Deploy to personal site                          |

Total ≈ 8 weeks of part‑time evenings; breadboard reachable in 4–5 weeks.

---

## 4 ️⃣ Toolchain Details

### 4.1 Assembler (Python)

```bash
$ ./asm.py fib.asm -o fib.hex
```

- Two‑pass: labels / addresses.
- Output Intel‑HEX or raw binary.
- Auto‑generate `.include opcodes.yml` from spec.

### 4.2 Simulator

- Pure Python first → compile to WebAssembly via Pyodide for site embed.
- Supports cycle‑accurate mode (`--cycles`) vs functional mode.

### 4.3 Micro‑Test Suite

- `tests/*.asm` each validating one instruction → sim output JSON → compared to truth table.
- Hardware harness later: Raspberry Pi Pico toggles bus lines to assert same vectors.

---

## 5 ️⃣ Risk & Mitigation

| Risk                           | Plan                                                                                                               |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| **Clock skew at >5 kHz**       | Keep MVP target 1 kHz; if faster, upgrade buffers to 74HC logic.                                                   |
| **Bus contention**             | Design tri‑state control matrix spreadsheet before wiring; LED indicators for enable lines during step mode.       |
| **Transistor sourcing delays** | Order 1k MOSFETs (2N7000) + 100 BSS138 early; or temporarily use 74HC chips for non‑critical gates (still counts). |
| **Debug complexity**           | Logic analyzer (Saleae 8‑channel) mandatory; color‑coded wires for bus vs control.                                 |
| **Memory latency**             | Static RAM (SRAM 55 ns) plenty for 1–5 kHz.                                                                        |

---

## 6 ️⃣ Test & Measurement

| Instrument                   | Purpose                                          |
| ---------------------------- | ------------------------------------------------ |
| 8‑ch logic analyzer          | Capture T‑cycle vs bus lines                     |
| 100 MHz scope                | Validate clock stability & ALU carry chain delay |
| Multimeter                   | Voltage drop across bus drivers                  |
| Python harness + GPIO (Pico) | Automate write/read memory integrity test        |

---

## 7 ️⃣ Documentation Artifacts

1. **CPU_SPEC.pdf** — ISA, timing diagrams, pinout.
2. **SCHEMATIC.pdf + PCB Gerbers**.
3. **BOM.csv** — Source, unit price, qty.
4. **SIM_README.md** — build & run instructions, test vectors.
5. **demo.mp4** — Overhead camera + console overlay.
6. **metrics.json** — transistor_count, max_freq, power_draw.

---

## 8 ️⃣ Success Criteria (MVP Definition of Done)

- [ ] Executes **Fibonacci demo** end‑to‑end in hardware **without manual intervention**.
- [ ] **Assembler → HEX → EEPROM → CPU** workflow proven.
- [ ] Clock stable ±5 % for 30 min.
- [ ] ALU accuracy: passes 100‑vector testbench (add/sub/and/or/xor).
- [ ] README contains scope capture & transistor count table.
- [ ] WASM simulator on portfolio site runs same hex and matches LED output pattern in <200 ms.

---

**Build this MVP and you’ll have a flagship hardware achievement no recruiter will ignore.** Let me know if you want:

- Transistor‑level 4‑bit adder schematic
- Python assembler starter code
- KiCad netlist template

Just ask for the piece you want next.
