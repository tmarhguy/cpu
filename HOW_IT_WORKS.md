# How the ALU Actually Works

**Understanding the different implementations and execution layers**

Your ALU project has **multiple implementations** at different levels of abstraction. Here's the complete picture:

---

## 🎯 The Three Implementations

### 1. **Hardware (Physical)** - The Real Thing
**Location:** Physical PCB with 3,856 discrete transistors

**What it is:**
- Actual CMOS transistors (2N7000, BS250) on a 270×270mm PCB
- Pure combinational logic (no clock, no software)
- Signals propagate through transistors at ~400ns
- This is the **actual ALU** you built

**How it works:**
```
Inputs (A, B, FUNC) → Transistor gates → Adders → MUXes → Output
                                    ↓
                              Physical voltage levels
                              (0V = logic 0, 5V = logic 1)
```

**Status:** 95% complete (18/19 operations verified)

---

### 2. **FPGA (Synthesizable Hardware)** - Digital Implementation
**Location:** `sim/FPGA/src/ALU.sv`

**What it is:**
- SystemVerilog hardware description language (HDL)
- Synthesizes to FPGA logic blocks (LUTs, flip-flops)
- Runs at FPGA clock speed (~100MHz possible)
- Functionally equivalent to your discrete transistor design

**How it works:**
```systemverilog
module ALU #(parameter WIDTH = 8)(
    input  logic [WIDTH-1:0] A,
    input  logic [WIDTH-1:0] B,
    input  logic [4:0]       Opcode,
    output logic [WIDTH-1:0] Result,
    output logic             CarryOut,
    output logic             Zero,
    output logic             Negative
);

always @* begin
    case (Opcode)
        5'd0: temp_result = A + B;        // ADD
        5'd1: temp_result = A - B;        // SUB
        5'd8: temp_result = ~(A & B);     // NAND
        // ... etc
    endcase
end
```

**This gets synthesized to:**
- FPGA LUTs (Look-Up Tables)
- Carry chains
- Routing resources
- Actual hardware on FPGA chip

**Status:** Complete and ready for FPGA deployment

---

### 3. **Software Simulation (Golden Model)** - Verification Reference
**Location:** `test/test_alu.py` - Class `ALU8Bit`

**What it is:**
- Python software that **simulates** what the hardware does
- Used for verification and testing
- Not actual hardware - just a mathematical model
- The "golden model" that defines correct behavior

**How it works:**
```python
class ALU8Bit:
    def execute(self, opcode: str, a: int, b: int):
        if opcode == '00000':  # ADD
            result = a + b
            carry = result > 255
            return result & 0xFF, flags
        
        elif opcode == '00001':  # SUB
            result = a - b
            carry = result >= 0
            return result & 0xFF, flags
        
        # ... etc for all 19 operations
```

**This is pure software:**
- Python interpreter executes it
- No hardware involved
- Fast for testing (microseconds)
- Used by CLI tool and test suite

**Status:** Complete, 1.24M test vectors passing

---

## 🔄 How They All Connect

```
┌─────────────────────────────────────────────────────────────┐
│                     YOUR ALU PROJECT                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. PHYSICAL HARDWARE (The Real Thing)                      │
│     ┌──────────────────────────────────────┐               │
│     │  270×270mm PCB                       │               │
│     │  3,856 discrete transistors          │               │
│     │  ~400ns propagation delay            │               │
│     │  Status: 95% complete                │               │
│     └──────────────────────────────────────┘               │
│              ↑                                               │
│              │ Designed to match                            │
│              ↓                                               │
│  2. FPGA IMPLEMENTATION (Synthesizable HDL)                 │
│     ┌──────────────────────────────────────┐               │
│     │  sim/FPGA/src/ALU.sv                 │               │
│     │  SystemVerilog RTL                   │               │
│     │  Synthesizes to FPGA                 │               │
│     │  ~10ns on FPGA (much faster)         │               │
│     │  Status: Complete                    │               │
│     └──────────────────────────────────────┘               │
│              ↑                                               │
│              │ Verified against                             │
│              ↓                                               │
│  3. SOFTWARE SIMULATION (Golden Model)                      │
│     ┌──────────────────────────────────────┐               │
│     │  test/test_alu.py                    │               │
│     │  Python class ALU8Bit                │               │
│     │  Mathematical model                  │               │
│     │  Used by: CLI, test suite            │               │
│     │  Status: Complete, 1.24M tests pass  │               │
│     └──────────────────────────────────────┘               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔍 What Happens When You Run the CLI

### Command: `./alu_cli.py ADD 42 23`

**Step-by-step execution:**

1. **CLI parses arguments**
   ```python
   operation = "ADD"
   a = 42
   b = 23
   ```

2. **CLI calls ALU interface**
   ```python
   interface = ALUInterface()
   result, flags = interface.execute("ADD", 42, 23)
   ```

3. **Interface looks up opcode**
   ```python
   opcode = OPCODE_MAP["ADD"]  # Returns "00000"
   ```

4. **Calls software simulation**
   ```python
   alu = ALU8Bit()  # From test/test_alu.py
   result, flags = alu.execute("00000", 42, 23)
   ```

5. **Software simulation executes**
   ```python
   def add(self, a: int, b: int):
       result = a + b          # 42 + 23 = 65
       carry = result > 255    # 65 > 255? No, carry = False
       return 65, {carry: False, zero: False, ...}
   ```

6. **Result returned to CLI**
   ```python
   result = 65
   flags = {carry: False, zero: False, negative: False, overflow: False}
   ```

7. **CLI formats and displays**
   ```
   ======================================================================
   ALU Operation: ADD
   ======================================================================
   Inputs:
     A =  42
     B =  23
   Result:
     OUT =  65
   Flags:
     Carry (C):    0 (CLEAR)
     Zero (Z):     0 (CLEAR)
   ======================================================================
   ```

**Important:** The CLI currently uses **software simulation only**. It doesn't touch the physical hardware or FPGA.

---

## 🎮 Different Execution Modes

### Current: Software Simulation

```bash
./alu_cli.py ADD 42 23
```

**What happens:** Python software calculates result  
**Speed:** ~2ms (Python overhead)  
**Hardware used:** None (pure software)

### Future: FPGA Mode

```bash
./alu_cli.py --mode fpga --port /dev/ttyUSB0 ADD 42 23
```

**What would happen:**
1. CLI sends command to FPGA via serial port
2. FPGA executes operation in hardware
3. FPGA sends result back via serial
4. CLI displays result

**Speed:** ~1ms (including serial communication)  
**Hardware used:** FPGA running ALU.sv

### Physical Hardware Testing

**Currently:** Manual testing with multimeter/oscilloscope  
**Future:** Could add microcontroller interface

```
PC → USB → Microcontroller → Your PCB → Read outputs → USB → PC
```

---

## 📂 File Locations

### Software Simulation (What CLI uses now)
```
test/test_alu.py
├── class ALU8Bit          ← The "engine" for CLI
│   ├── add()              ← ADD operation
│   ├── sub()              ← SUB operation
│   ├── and_op()           ← AND operation
│   └── ... (19 operations total)
```

### FPGA Implementation (Hardware description)
```
sim/FPGA/src/
├── ALU.sv                 ← Main ALU module (SystemVerilog)
├── FPGA_Top.sv            ← Top-level wrapper
├── ClockDivider.sv        ← Clock management
└── Counter.sv             ← Counter for demos
```

### Physical Hardware (The real thing)
```
schematics/kicad/          ← PCB designs
media/pcb/                 ← PCB photos
media/photos/hardware/     ← Assembled hardware photos
```

---

## 🔬 Verification Flow

```
1. Design Operation (e.g., ADD)
   ↓
2. Implement in Software (test_alu.py)
   ↓
3. Write Tests (1.24M test vectors)
   ↓
4. Implement in HDL (ALU.sv)
   ↓
5. Simulate HDL (Vivado/ModelSim)
   ↓
6. Synthesize to FPGA
   ↓
7. Test on FPGA
   ↓
8. Design Physical Circuit (KiCad)
   ↓
9. Fabricate PCB
   ↓
10. Assemble and Test Hardware
```

**All three implementations must match!**

---

## 💡 Why Three Implementations?

### 1. Software Simulation (Python)
**Purpose:** Fast verification and testing  
**Pros:** Easy to modify, instant execution, perfect for development  
**Cons:** Not real hardware, can't measure timing

### 2. FPGA Implementation (SystemVerilog)
**Purpose:** Prototyping and performance testing  
**Pros:** Real hardware, fast execution, reconfigurable  
**Cons:** Requires FPGA board, different from discrete transistors

### 3. Physical Hardware (Discrete Transistors)
**Purpose:** Educational demonstration and understanding  
**Pros:** See every gate, understand every signal, educational value  
**Cons:** Slow, expensive, hard to modify

---

## 🚀 Future: Connecting CLI to Hardware

### Option 1: FPGA Integration

**Hardware needed:**
- FPGA board (Basys 3, Arty A7, etc.)
- USB cable

**Implementation:**
```python
def _execute_fpga(self, opcode: str, a: int, b: int):
    import serial
    ser = serial.Serial('/dev/ttyUSB0', 115200)
    
    # Send command: [5-bit opcode][8-bit A][8-bit B]
    command = f"{opcode}{a:08b}{b:08b}\n"
    ser.write(command.encode())
    
    # Read result: [8-bit result][4-bit flags]
    response = ser.readline().decode()
    result = int(response[:8], 2)
    flags = parse_flags(response[8:])
    
    ser.close()
    return result, flags
```

### Option 2: Physical Hardware Interface

**Hardware needed:**
- Your PCB
- Microcontroller (Arduino, Raspberry Pi Pico)
- GPIO connections

**Implementation:**
```python
def _execute_hardware(self, opcode: str, a: int, b: int):
    import RPi.GPIO as GPIO
    
    # Set inputs via GPIO
    set_gpio_value(A_PINS, a)
    set_gpio_value(B_PINS, b)
    set_gpio_value(FUNC_PINS, opcode)
    
    # Wait for propagation (~400ns)
    time.sleep(0.001)
    
    # Read outputs via GPIO
    result = read_gpio_value(OUT_PINS)
    flags = read_gpio_value(FLAG_PINS)
    
    return result, flags
```

---

## 📊 Performance Comparison

| Implementation | Speed | Accuracy | Cost | Educational Value |
|----------------|-------|----------|------|-------------------|
| **Software Simulation** | ~2ms | 100% | $0 | Low (abstract) |
| **FPGA** | ~10ns | 100% | $100 | Medium (configurable) |
| **Physical Hardware** | ~400ns | 95%* | $450 | High (see everything) |

*95% = 18/19 operations verified

---

## 🎓 Summary

**The "engine" you're looking for exists in THREE places:**

1. **`test/test_alu.py`** - Software simulation (what CLI uses now)
   - Pure Python code
   - Calculates results mathematically
   - Fast for testing

2. **`sim/FPGA/src/ALU.sv`** - FPGA implementation
   - SystemVerilog hardware description
   - Synthesizes to real FPGA hardware
   - Can run on FPGA board

3. **Your Physical PCB** - Discrete transistor implementation
   - 3,856 real transistors
   - Actual hardware, not simulation
   - The ultimate goal of the project

**Currently, the CLI uses #1 (software simulation).**

**Future enhancement: CLI can use #2 (FPGA) or #3 (physical hardware) with `--mode fpga` or `--mode hardware`.**

---

**Questions?**

- Software simulation: See `test/test_alu.py`
- FPGA implementation: See `sim/FPGA/src/ALU.sv`
- Physical hardware: See `schematics/kicad/` and `media/pcb/`
- CLI tool: See `alu_cli.py`

**Contact:** tmarhguy@gmail.com | tmarhguy@seas.upenn.edu
