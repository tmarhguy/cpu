# Flag Implementation Guide

**A pressure-free roadmap for implementing comprehensive flag generation**

---

## 🎯 Current Situation

### What You Have Now

**Flags:** LESS, EQUAL, POSITIVE (GREATER), COUT  
**Status:** Working for CMP and SUB operations only  
**Hardware:** 95% complete (18/19 operations verified)

### What's Missing

**Standard ALU flags** that work for **all operations**:
- **Zero (Z):** Result is zero
- **Negative (N):** Result is negative (MSB = 1)
- **Carry (C):** Arithmetic carry/borrow
- **Overflow (V):** Signed overflow

---

## 🧭 Understanding the Two Flag Systems

### System 1: Comparison Flags (What you have)

**Purpose:** Specifically for comparing two numbers  
**Operations:** CMP, SUB  
**Flags:**
- **EQUAL:** A == B (this is actually the **Zero flag**! Result == 0)
- **LESS:** A < B (derived from carry/borrow)
- **POSITIVE/GREATER:** Result > 0 (this is **NOT Zero AND NOT Negative**)
- **COUT:** Carry from subtraction

**Key Insight:** Your EQUAL flag **IS** the Zero flag! When you compare A and B:
- If A == B, then A - B = 0, so EQUAL = Z = 1
- If A != B, then A - B ≠ 0, so EQUAL = Z = 0

**Example:**
```
CMP 100, 35:
  Result = 65 (100 - 35)
  EQUAL = 0 (result not zero, so 100 ≠ 35)  ← This IS the Zero flag!
  LESS = 0 (100 is not less than 35)
  GREATER = 1 (100 > 35)
  COUT = 1 (no borrow needed)

CMP 50, 50:
  Result = 0 (50 - 50)
  EQUAL = 1 (result is zero, so 50 == 50)  ← Zero flag = 1!
  LESS = 0
  GREATER = 0
  COUT = 1
```

### System 2: Standard ALU Flags (What you need to add)

**Purpose:** Status information for **any** operation  
**Operations:** ALL 19 operations  
**Flags:**
- **Zero (Z):** OUT == 0
- **Negative (N):** OUT[7] == 1 (MSB set)
- **Carry (C):** Carry out from arithmetic
- **Overflow (V):** Signed overflow

**Example:**
```
ADD 200, 100:
  Result = 44 (wrapped around)
  Z = 0 (result not zero)
  N = 0 (MSB = 0, positive)
  C = 1 (carry occurred: 300 > 255)
  V = 0 (no signed overflow)

AND 0xFF, 0x00:
  Result = 0
  Z = 1 (result is zero!)
  N = 0 (MSB = 0)
  C = 0 (no carry in logic ops)
  V = 0 (no overflow in logic ops)
```

---

## 🎨 The Big Picture: Two Approaches

### Option 1: Keep Both Systems (Recommended)

**Pros:**
- ✅ Comparison flags already work
- ✅ No need to change existing hardware
- ✅ Add standard flags alongside
- ✅ More complete ALU

**Cons:**
- More outputs (but EQUAL = ZERO, so really 6 unique flags)
- Slightly more complex

**Flag outputs:**
```
Comparison Flags (existing):
  - LESS
  - EQUAL (this IS the Zero flag!)
  - POSITIVE/GREATER
  - COUT

Standard Flags (add these):
  - ZERO (Z) ← Already have this as EQUAL!
  - NEGATIVE (N) ← Need to add
  - CARRY (C) ← Already have this as COUT!
  - OVERFLOW (V) ← Need to add
```

**Actually, you already have 2 of the 4 standard flags!**
- EQUAL = ZERO (Z)
- COUT = CARRY (C)

**You only need to add:**
- NEGATIVE (N) - super easy, just wire OUT[7]
- OVERFLOW (V) - medium complexity

### Option 2: Replace with Standard Flags Only

**Pros:**
- ✅ Industry-standard interface
- ✅ Simpler (4 flags total)
- ✅ Matches textbook ALUs

**Cons:**
- ❌ Lose comparison-specific flags
- ❌ Need to derive LESS/EQUAL from Z/N/C/V
- ❌ More rework

**Flag outputs:**
```
Standard Flags only:
  - ZERO (Z)
  - NEGATIVE (N)
  - CARRY (C)
  - OVERFLOW (V)

Derive comparisons:
  EQUAL = Z
  LESS = (N != V)  [for signed]
  LESS = !C        [for unsigned]
```

---

## 🛠️ Implementation Roadmap (No Pressure!)

### Phase 1: Understand What You Need (1 day)

**Goal:** Clarify requirements

**Tasks:**
1. ✅ Read this document
2. Decide: Keep both systems or replace?
3. Sketch flag generation logic on paper
4. Review existing flag hardware

**No hardware changes yet!**

---

### Phase 2: Design Flag Logic (2-3 days)

**Goal:** Design the circuits on paper

#### Zero Flag (Z)

**Logic:** `Z = (OUT == 0)`

**Implementation:**
```
Z = NOR(OUT[7], OUT[6], OUT[5], OUT[4], OUT[3], OUT[2], OUT[1], OUT[0])
```

**Circuit:**
- 8-input NOR gate
- Can build from 2-input NORs: ((A|B)|(C|D))|((E|F)|(G|H))
- Transistor count: ~16T

**Works for:** ALL operations

---

#### Negative Flag (N)

**Logic:** `N = OUT[7]`

**Implementation:**
```
N = OUT[7]  (just wire it!)
```

**Circuit:**
- Direct connection from OUT[7]
- Optional buffer for drive strength
- Transistor count: 0-2T

**Works for:** ALL operations

---

#### Carry Flag (C)

**Logic:** Depends on operation type

**Implementation:**
```
Arithmetic (ADD, SUB, INC, DEC):
  C = Carry out from adder

Shift operations (LSL, LSR, ASR):
  LSL: C = A[7] (bit shifted out left)
  LSR: C = A[0] (bit shifted out right)
  ASR: C = A[0] (bit shifted out right)

Logic operations (AND, OR, XOR, etc.):
  C = 0 (no carry)

Special operations:
  CMP: C = Carry from subtraction
  REV: C = 0
```

**Circuit:**
- MUX to select carry source based on opcode
- Already have carry from adder (COUT)
- Need to add shift carry capture
- Transistor count: ~40T (4:1 MUX)

**Complexity:** Medium

---

#### Overflow Flag (V)

**Logic:** Signed overflow detection

**Implementation:**
```
For ADD:
  V = (A[7] == B[7]) && (A[7] != OUT[7])
  "Both inputs same sign, output different sign"

For SUB:
  V = (A[7] != B[7]) && (A[7] != OUT[7])
  "Inputs different signs, output wrong sign"

For other ops:
  V = 0
```

**Circuit:**
- XOR and AND gates
- MUX to select based on operation
- Transistor count: ~20T

**Complexity:** Medium

---

### Phase 3: Simulate in Software (1 day)

**Goal:** Verify logic before building hardware

**Update `test/test_alu.py`:**

```python
def _flags(self, result: int, carry: bool = False, overflow: bool = False):
    """Calculate ALL flags"""
    result_8bit = result & self.mask
    
    return {
        # Standard flags (add these)
        'zero': result_8bit == 0,
        'negative': bool(result_8bit & 0x80),
        'carry': carry,
        'overflow': overflow,
        
        # Comparison flags (keep these)
        'equal': result_8bit == 0,  # Same as zero for CMP
        'less': carry == False,      # For unsigned comparison
        'positive': result_8bit > 0 and not (result_8bit & 0x80),
        'cout': carry
    }
```

**Test all 19 operations:**
```bash
./run_tests.sh              # Quick test (1,900 tests)
./run_tests.sh exhaustive   # Exhaustive test (1,247,084 tests)
```

**No hardware changes yet!**

---

### Phase 4: Design PCB Changes (2-3 days)

**Goal:** Plan the hardware modifications

**Option A: Separate Flag Board (Recommended)**

Create a small addon PCB:
- Inputs: OUT[7:0], COUT, Opcode[4:0]
- Outputs: Z, N, C, V (+ existing LESS, EQUAL, POSITIVE)
- Size: ~50×50mm
- Transistors: ~80T total

**Pros:**
- ✅ Don't modify main board
- ✅ Can test independently
- ✅ Easy to debug
- ✅ Modular design

**Option B: Modify Main Board**

Add flag logic to existing PCB:
- Find empty space on 270×270mm board
- Route new connections
- Add ~80 transistors

**Pros:**
- ✅ Integrated solution
- ✅ No extra boards

**Cons:**
- ❌ Harder to modify
- ❌ Risk breaking existing circuits

---

### Phase 5: Build and Test (1-2 weeks, no rush!)

**Goal:** Implement hardware incrementally

**Step 1: Build Zero Flag First**
- Simplest flag (just 8-input NOR)
- Test with all operations
- Verify: AND 0xFF, 0x00 → Z=1

**Step 2: Add Negative Flag**
- Just wire OUT[7] to N
- Test with signed numbers
- Verify: SUB 10, 20 → N=1

**Step 3: Add Carry Flag**
- Connect adder carry
- Add shift carry MUX
- Test arithmetic and shifts

**Step 4: Add Overflow Flag**
- Build overflow detection logic
- Test signed arithmetic
- Verify: ADD 127, 1 → V=1

**Take your time with each step!**

---

## 📊 Transistor Budget

| Flag | Transistors | Complexity | Priority | Status |
|------|-------------|------------|----------|--------|
| **Zero (Z)** | 0T | N/A | High | ✅ Already have as EQUAL! |
| **Negative (N)** | ~2T | Very Low | High | ❌ Need to add |
| **Carry (C)** | 0T | N/A | High | ✅ Already have as COUT! |
| **Overflow (V)** | ~20T | Medium | Medium | ❌ Need to add |
| **Total** | **~22T** | | | |

**Impact:** Only +22T (0.6% increase from 3,856T) - Much less than expected!  
**Board space:** ~5×5mm  
**Assembly time:** ~30 minutes

**Great news:** You already have 2 of the 4 standard flags working!

---

## 🎯 Recommended Approach

### My Suggestion: Incremental Addition

**Phase 1: Add Zero and Negative flags first**
- Easiest to implement (~18T total)
- Immediately useful for all operations
- Low risk

**Phase 2: Add Carry flag**
- More complex but valuable
- Reuse existing COUT signal
- Add shift carry capture

**Phase 3: Add Overflow flag (optional)**
- Useful for signed arithmetic
- Can skip if not needed
- Educational value

**Keep existing comparison flags**
- They already work
- Useful for CMP operation
- No need to remove

---

## 🧪 Testing Strategy

### Software Testing (Do this first!)

```bash
# Test Zero flag
./alu_cli.py AND 0xFF 0x00  # Should set Z=1
./alu_cli.py XOR 0xAA 0xAA  # Should set Z=1
./alu_cli.py ADD 1 1        # Should set Z=0

# Test Negative flag
./alu_cli.py SUB 10 20      # Should set N=1
./alu_cli.py ADD 200 100    # Should set N=0

# Test Carry flag
./alu_cli.py ADD 200 100    # Should set C=1
./alu_cli.py LSL 0x80       # Should set C=1

# Test Overflow flag
./alu_cli.py ADD 127 1      # Should set V=1
./alu_cli.py SUB 128 1      # Should set V=1
```

### Hardware Testing

**For each flag:**
1. Build circuit on breadboard first
2. Test with known inputs
3. Verify with multimeter/oscilloscope
4. Integrate into main board
5. Test all 19 operations

---

## 💡 Practical Examples

### Example 1: Zero Flag in Action

```
Operation: AND 0xFF, 0x00
Result: 0x00

Flags:
  Z = 1  ← Result is zero!
  N = 0  ← MSB is 0
  C = 0  ← No carry in logic ops
  V = 0  ← No overflow

Use case: Check if two values have no common bits set
```

### Example 2: Carry Flag in Arithmetic

```
Operation: ADD 200, 100
Result: 44 (300 wrapped to 44)

Flags:
  Z = 0  ← Result not zero
  N = 0  ← MSB is 0 (positive)
  C = 1  ← Overflow! 300 > 255
  V = 0  ← No signed overflow

Use case: Detect unsigned overflow
```

### Example 3: Overflow Flag in Signed Math

```
Operation: ADD 127, 1
Result: 128 (0x80)

Flags:
  Z = 0  ← Result not zero
  N = 1  ← MSB is 1 (looks negative!)
  C = 0  ← No unsigned overflow
  V = 1  ← Signed overflow! 127+1 should be 128, but got -128

Use case: Detect signed overflow (127 is max positive 8-bit signed)
```

---

## 🚫 What NOT to Do

### Don't:
- ❌ Rush to modify hardware immediately
- ❌ Change everything at once
- ❌ Skip software simulation
- ❌ Remove existing flags that work
- ❌ Feel pressured to finish quickly

### Do:
- ✅ Take your time
- ✅ Test in software first
- ✅ Build incrementally
- ✅ Keep existing flags
- ✅ Document as you go

---

## 📚 Reference: Flag Truth Tables

### Zero Flag

| Operation | Result | Z |
|-----------|--------|---|
| ADD 1, 1 | 2 | 0 |
| SUB 5, 5 | 0 | 1 |
| AND 0xFF, 0x00 | 0 | 1 |
| XOR 0xAA, 0xAA | 0 | 1 |

### Negative Flag

| Operation | Result | N |
|-----------|--------|---|
| SUB 10, 20 | 246 (-10) | 1 |
| ADD 100, 50 | 150 | 1 |
| AND 0x80, 0xFF | 0x80 | 1 |
| LSL 0x80 | 0x00 | 0 |

### Carry Flag

| Operation | Result | C |
|-----------|--------|---|
| ADD 200, 100 | 44 | 1 |
| SUB 10, 20 | 246 | 0 |
| LSL 0x80 | 0x00 | 1 |
| LSR 0x01 | 0x00 | 1 |

### Overflow Flag

| Operation | Result | V |
|-----------|--------|---|
| ADD 127, 1 | 128 | 1 |
| ADD 100, 50 | 150 | 0 |
| SUB 128, 1 | 127 | 1 |
| SUB 100, 50 | 50 | 0 |

---

## 🎓 Learning Resources

### Understanding Flags

1. **Zero Flag:** Easy - just check if all bits are 0
2. **Negative Flag:** Easy - just check MSB
3. **Carry Flag:** Medium - depends on operation type
4. **Overflow Flag:** Tricky - signed vs unsigned overflow

### Recommended Reading

- Your own spec: `spec/alu-spec.md`
- Flag generation: `spec/README.md` (lines 114-356)
- Truth tables: `spec/truth-tables/compare.md`

---

## 💡 Key Insight: You're Closer Than You Think!

**The Big Revelation:**

Your EQUAL flag **IS** the Zero flag! Here's why:

```
When comparing A and B:
  Operation: A - B
  
  If A == B:
    Result = 0
    EQUAL = 1 (because result is zero)
    This IS the Zero flag!
  
  If A != B:
    Result ≠ 0
    EQUAL = 0 (because result is not zero)
```

**What this means:**
- ✅ Zero flag: Already working (it's your EQUAL flag)
- ✅ Carry flag: Already working (it's your COUT flag)
- ❌ Negative flag: Need to add (~2 transistors)
- ❌ Overflow flag: Need to add (~20 transistors)

**You only need to add 2 flags, not 4!**

**Total work:** ~22 transistors instead of ~80 transistors  
**Reduction:** 73% less work than expected!

---

## 🎯 Summary: Your Path Forward

### Immediate (This Week)
1. Read this document thoroughly
2. Decide: Keep both flag systems or replace?
3. Update software simulation (`test_alu.py`)
4. Test all operations in software

### Short Term (Next 2 Weeks)
1. Design flag circuits on paper
2. Calculate transistor count
3. Plan PCB layout (separate board recommended)
4. Order components if needed

### Medium Term (Next Month)
1. Build Zero flag (easiest first!)
2. Build Negative flag
3. Test with existing operations
4. Document results

### Long Term (When Ready)
1. Add Carry flag
2. Add Overflow flag (optional)
3. Full integration testing
4. Update documentation

---

## 💬 Final Advice

**Take your time.** Your ALU is already 95% complete and working. Adding comprehensive flags is an **enhancement**, not a requirement.

**Start small.** Build Zero flag first - it's the easiest and immediately useful.

**Test in software first.** Update `test_alu.py` and verify logic before touching hardware.

**Keep what works.** Your comparison flags (LESS, EQUAL, POSITIVE, COUT) are valuable - keep them!

**No pressure.** This is your project. Work at your own pace. Even without additional flags, your ALU is already impressive.

---

## 📞 Questions?

**Stuck on flag logic?** Check `spec/README.md` lines 321-367  
**Need circuit help?** Review existing flag hardware in `schematics/kicad/`  
**Software questions?** See `test/test_alu.py`

**Email:** tmarhguy@gmail.com | tmarhguy@seas.upenn.edu  
Twitter: [@marhguy_tyrone](https://twitter.com/marhguy_tyrone) | Instagram: [@tmarhguy](https://instagram.com/tmarhguy) | Substack: [@tmarhguy](https://tmarhguy.substack.com)

---

**Remember:** Your ALU already works. Flags are just the cherry on top! 🎂

**Document Version:** 1.0  
**Last Updated:** January 2026  
**Author:** AI Assistant for Tyrone Marhguy
