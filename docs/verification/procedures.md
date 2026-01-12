# Verification Procedures

This document defines how to verify hardware timing, electrical thresholds, and functional
pass/fail criteria for each operation. Record results for every test run in the template
sections below.

## Signal Timing Checks

### Propagation Delay

**Purpose:** Confirm that critical path propagation delays meet target limits.

**Procedure:**

1. Drive a known input transition on the source signal (clock edge, control line, or data line
   depending on the path).
2. Capture the time difference between the input transition crossing its threshold and the
   destination signal crossing its threshold.
3. Repeat across all critical paths identified in the timing analysis.

**Measurements:**

- `t_pd` (propagation delay) for each path.
- Worst-case `t_pd` for the system.

**Pass/Fail Criteria:**

- `t_pd` for each path must be less than or equal to the target delay budget for that path.
- Worst-case `t_pd` must be within the overall clock period margin.

### Setup/Hold (if applicable)

**Purpose:** Ensure data is stable relative to the sampling clock.

**Procedure:**

1. Sweep data transitions relative to the clock edge using a delay generator or timing
   adjustments in the testbench.
2. Identify the earliest stable time before the clock edge (setup) and the latest stable time
   after the clock edge (hold).

**Measurements:**

- `t_setup` and `t_hold` for sampled signals (register inputs, memory reads, etc.).

**Pass/Fail Criteria:**

- `t_setup` and `t_hold` must meet or exceed the minimum required values for the target clock
  rate and device characteristics.

### Results (Timing Test Run)

| Field | Value |
| --- | --- |
| Date | |
| Hardware setup | |
| Measurement tool | |
| Signals tested | |
| Worst-case `t_pd` | |
| `t_setup` / `t_hold` margins | |
| Outcome (pass/fail) | |
| Notes | |

## Voltage Thresholds & Noise Margin Targets

**Purpose:** Verify that logic levels meet threshold requirements and noise margins are
sufficient for reliable operation.

**Targets:**

- `V_IL(max)` and `V_IH(min)` for input thresholds.
- `V_OL(max)` and `V_OH(min)` for output thresholds.
- Noise margin targets: `NM_L = V_IL(max) - V_OL(max)` and `NM_H = V_OH(min) - V_IH(min)`.

**Procedure:**

1. Measure input threshold voltages by sweeping input voltages and monitoring logic state
   transitions.
2. Measure output levels under typical load conditions.
3. Compute noise margins for both logic low and logic high.

**Pass/Fail Criteria:**

- Measured thresholds must meet or exceed the target limits.
- Noise margins must meet the minimum target margin for both low and high levels.

### Results (Voltage/Noise Test Run)

| Field | Value |
| --- | --- |
| Date | |
| Hardware setup | |
| Measurement tool | |
| Measured `V_IL(max)` / `V_IH(min)` | |
| Measured `V_OL(max)` / `V_OH(min)` | |
| `NM_L` / `NM_H` | |
| Outcome (pass/fail) | |
| Notes | |

## Operation Pass/Fail Criteria

For each operation, the expected output must match the defined opcode behavior, and any
status flags must reflect the correct state.

### Arithmetic/Logic Operations

**Scope:** ADD, SUB, AND, OR, XOR, NOT, shifts/rotates (as implemented).

**Pass/Fail Criteria:**

- Output data matches the reference model for all test vectors.
- Status flags (zero, carry, negative, overflow as applicable) match expected values.

### Memory Operations

**Scope:** LOAD/STORE and related addressing modes.

**Pass/Fail Criteria:**

- Read data matches the written data across all addresses under test.
- Address decoding selects the correct target without aliasing.

### Control Flow Operations

**Scope:** Jumps, branches, calls/returns, interrupts (if implemented).

**Pass/Fail Criteria:**

- Program counter updates match expected control flow.
- Return addresses or interrupt vectors are correct.

### Results (Functional Test Run)

| Field | Value |
| --- | --- |
| Date | |
| Hardware setup | |
| Measurement tool | |
| Operations tested | |
| Vector coverage | |
| Outcome (pass/fail) | |
| Notes | |
