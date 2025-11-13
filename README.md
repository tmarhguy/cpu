# 8-Bit Arithmetic Logic Unit (ALU) Design Project

Author: Tyrone Marhguy

Course: Computer Engineering, University of Pennsylvania

## 1. Project Description

This repository documents the design, implementation, and analysis of an 8-bit Arithmetic Logic Unit (ALU). The design is built from the ground up, starting with fundamental 1-bit adders and scaling into a multi-function 8-bit unit capable of 2's complement arithmetic.

The current implementation supports two primary operations: **ADD** and  **SUBTRACT** . **The architecture is built to be scalable, with a 4-bit master control signal allowing for a total of 16 potential operations (e.g., logical AND, OR, NOR, etc.)**^1^.

The core of this design is an 8-bit ripple-carry adder, which has been cleverly augmented with a simple XOR array to handle subtraction efficiently. **All design decisions are justified with transistor cost analysis to ensure an optimal and elegant solution**^2^^2^^2^.

## 2. Table of Contents

1. Project Description
2. Table of Contents
3. Current Features
4. Overall Architecture
5. Component Breakdown
   * 1-Bit Full Adder
   * 8-Bit Arithmetic Unit (Adder/Subtractor)
   * Control Unit (Decoder)
6. Key Design Decisions & Rationale
   * Implementing Subtraction (2's Complement)
   * Design Choice: XOR Array vs. MUX Array
7. Transistor Cost Analysis
8. Future Work & Next Steps

---

## 3. Current Features

* **8-Bit Word Size:** Operates on two 8-bit inputs, `<span class="citation-149">A[7:0]</span>` and `<span class="citation-149">B[7:0]</span>`^3^.
* **Arithmetic Operations:**
  * `ADD` (A + B)
  * `SUB` (A - B)
* **Scalable Control:** A 4-bit master control signal (`<span class="citation-148">ALUOp</span>`) is used, allowing for a total of 16 operations^4^.
* **Centralized Control Unit:** A dedicated decoder (Control Unit) translates the 4-bit `<span class="citation-147">ALUOp</span>` into the specific internal control signals required by the hardware^5^^5^^5^^5^.
* **Efficient 2's Complement:** Subtraction is implemented using an efficient XOR array, which is cheaper in transistor cost than a multiplexer-based alternative^6^^6^.

---

## 4. Overall Architecture

The ALU is composed of two main blocks that will operate in parallel, and a final multiplexer to select the output.

1. **Arithmetic Unit:** An 8-bit adder/subtractor module. This is the only unit fully implemented so far.
2. **Logical Unit:** (Future) A module to perform bitwise operations (AND, OR, NOR, etc.).
3. **Control Unit:** A decoder that takes the 4-bit `ALUOp` and generates all internal control signals.
4. **Final Output MUX:** An 8-bit 2-to-1 multiplexer that selects the final `ALU_Result` from either the Arithmetic Unit or the Logical Unit.

```
             A[7:0]   B[7:0]
                |        |
    ALUOp[3:0]  |        |
       |        |        |
   +---v---+    |        |
   | Control   +----v---v----+     +-------------+
   |   Unit |   | Arithmetic  |---->|             |
   +-------+   |    Unit     |  0  | 8-bit 2-to-1|
       |       +-------------+     |     MUX     |---> ALU_Result[7:0]
       |             |   |         |             |
       +------------>|   +-------->|      1      |
      (LogicSelect)  |  (ArithMode)  |             |
                     |             +-------------+
                     |                 ^
                     v                 |
               +-------------+         |
               |  Logical    |         |
               |    Unit     |---------+
               +-------------+        (FinalMuxSelect)
                     ^                    |
                     |                    |
                     +--------------------+
```

---

## 5. Component Breakdown

### 1-Bit Full Adder

The foundational block of the entire Arithmetic Unit is a 1-bit full adder.

* **Inputs:** `A`, `B`, `Cin`
* **Outputs:** `Sum`, `Cout`
* **Logic Derivation:** The Boolean expressions were derived using truth tables and Karnaugh maps^7^.
  * `Sum = A ⊕ B ⊕ Cin`
  * `Cout = AB + ACin + BCin`
* **Optimized `Cout`:** The carry-out logic was re-factored for a more efficient implementation:
  * `<span class="citation-144">Cout = AB + Cin(A ⊕ B)</span>` ^8^
* **Verification:** The logic for both Sum and Carry circuits was built and simulated, confirming correct behavior^9^^9^^9^^9^.

### 8-Bit Arithmetic Unit (Adder/Subtractor)

This unit is responsible for performing `A + B` and `A - B`.

* **Structure:** This unit consists of two main parts:
  1. **`B`-Input Logic:** An array of 8 XOR gates.
  2. **8-Bit Ripple-Carry Adder:** An array of 8 (1-bit Full Adders) "black-boxed" and daisy-chained together^10^^10^^10^^10^. **The **`<span class="citation-141">Cout</span>` of bit `<span class="citation-141">i</span>` is wired to the `<span class="citation-141">Cin</span>` of bit `<span class="citation-141">i+1</span>` ^11^.
* **Control:** This entire unit is controlled by a single 1-bit signal, `ArithMode`.
* **Operation:**
  * **The **`<span class="citation-140">ArithMode</span>` signal is fanned out to all 8 XOR gates and to the `<span class="citation-140">Cin</span>` of the *first* full adder (`<span class="citation-140">FA[0]</span>`)^12^^12^^12^^12^.
  * **When `ArithMode = 0` (ADD):**
    * `B_in` for each adder is `B[i] XOR 0 = B[i]` (B is passed through).
    * `Cin` for `FA[0]` is `0`.
    * The circuit computes: **`A + B + 0`**
  * **When `ArithMode = 1` (SUB):**
    * `<span class="citation-139">B_in</span>` for each adder is `<span class="citation-139">B[i] XOR 1 = NOT B[i]</span>` (B is inverted)^13^.
    * `<span class="citation-138">Cin</span>` for `<span class="citation-138">FA[0]</span>` is `<span class="citation-138">1</span>`^14^.
    * **The circuit computes: ** **`<span class="citation-137">A + NOT(B) + 1</span>`** **, which is 2's complement subtraction**^15^.

### Control Unit (Decoder)

This is the "brain" of the ALU. **Its design is currently in progress**^16^.

* **Input:** `ALUOp[3:0]`
* **Outputs (Internal Signals):**
  * `ArithMode (1-bit)`: Controls the Arithmetic Unit (0=ADD, 1=SUB).
  * `LogicSelect[... ]` (Future): Controls the Logical Unit (e.g., 00=AND, 01=OR).
  * `<span class="citation-135">FinalMuxSelect (1-bit)</span>` (Future): Controls the final output MUX (0=Arith, 1=Logic)^17^.
* **Example Logic:** The logic for the `ArithMode` signal will be derived from the `ALUOp` definitions. For example, if `ALUOp = 0001` is defined as SUB:
  * `ArithMode = (ALUOp == 0001)`

---

## 6. Key Design Decisions & Rationale

### Implementing Subtraction (2's Complement)

**The requirement to support subtraction (**`<span class="citation-134">A - B</span>`) ^18^was implemented using 2's complement arithmetic^19^, as this allows us to re-use the entire 8-bit adder. **The formula for 2's complement negation is **`<span class="citation-132">-B = NOT(B) + 1</span>`^20^.

This meant the hardware needed to accomplish two things conditionally:

1. Invert the `B` input (to get `NOT B`).
2. Set the initial carry-in (`Cin` of the first adder) to `1` (to perform the `+ 1`).

### Design Choice: XOR Array vs. MUX Array

**A "beautiful" **^21^ and efficient solution was found that solves both problems with a single control line.

* **MUX-Based Approach (Considered):** The most straightforward approach would be to use an 8-bit 2-to-1 MUX array.
  * A control signal (`Sub`) would select either `B` (for ADD) or `NOT B` (for SUB).
  * This would require a *separate* control signal to set the `Cin` of the first adder to `1` during subtraction.
  * **This was estimated to be costly, at approximately ****138T**^22^.
* **XOR-Based Approach (Implemented):** An XOR gate can be used as a "conditional inverter."
  * `B XOR 0 = B` (Pass-through)
  * `B XOR 1 = NOT B` (Invert)
  * **The Insight:** The *same* control signal used to select inversion (`1` for SUB) can also be wired *directly* to the `Cin` of the first adder. This elegantly handles both parts of the 2's complement operation simultaneously.
  * **This design is far more efficient, with the 8 XOR gates costing only ****96T**^23^.

---

## 7. Transistor Cost Analysis

A preliminary transistor cost analysis was performed to guide design decisions.

| **Gate** | **Transistor Cost (T)** |
| -------------- | ----------------------------- |
| NOT            | 2T                            |
| NAND           | 4T                            |
| NOR            | 4T                            |
| AND            | 6T                            |
| OR             | 6T                            |
| XOR            | 12T                           |
| XNOR           | 12T                           |

* **1-Bit Full Adder Cost:**
  * `Sum = A ⊕ B ⊕ C` (2 XOR gates): **$12 + 12 = 24T$**
  * `Cout = AB + C(A ⊕ B)` (2 AND, 1 OR, 1 XOR): **$6 + 6 + 6 + 12 = 30T$**
  * **Note: An alternate **`<span class="citation-128">Cout = AB+BC+AC</span>` ^24^ also costs **$3 \times 6T + 6T = 24T$** (if a 3-input OR is 6T). **The 30T calculation **^25^ seems to be the one used.
  * **Total Cost (1-bit FA): ~54T - 66T** (depending on implementation)^26^.
* **`B`-Inversion Logic Cost (8-bit):**
  * **MUX-based design: ****~138T** ^27^
  * **XOR-based design: **$8 \times 12T =$**96T** ^28^

This analysis clearly justifies the selection of the XOR-based design for subtraction.

---

## 8. Future Work & Next Steps

**The project is now focused on building the Control Unit **^29^ and expanding the ALU's capabilities.

1. **Implement Control Unit:** Build the decoder logic to translate all 16 `ALUOp` codes into their respective internal signals.
2. **Build Logical Unit:** Design and add the parallel Logical Unit to handle bitwise operations like `<span class="citation-122">AND</span>`, `<span class="citation-122">OR</span>`, `<span class="citation-122">NOR</span>`^30^.
3. **Add Final MUX:** Implement the 8-bit 2-to-1 MUX to select the final output from either the Arithmetic or Logical unit, controlled by a signal from the Control Unit^31^.
4. **Implement Overflow Detection:** Add logic to detect signed arithmetic overflow, as noted in the 8-bit adder design^32^.
5. **Implement Zero Flag:** Add an 8-input NOR gate to the final output to detect if the result is zero.
6. **Expand Operations:** Begin scaffolding for more complex operations like `<span class="citation-119">MUL</span>` (multiplication) and `<span class="citation-119">DIV</span>` (division)^33^.
