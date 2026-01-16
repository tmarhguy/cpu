#!/usr/bin/env python3
"""Test runner for JSON vectors in the test/ directory."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


# Expected order for execution and reporting
OPCODE_ORDER = [
    "ADD",
    "SUB",
    "INC_A",
    "DEC_A",
    "LSL",
    "LSR",
    "ASR",
    "REV_A",
    "NAND",
    "NOR",
    "XOR",
    "PASS_A",
    "PASS_B",
    "AND",
    "OR",
    "XNOR",
    "CMP",
    "NOT_A",
    "NOT_B",
]


@dataclass
class TestResult:
    vector_file: str
    test_name: str
    operation: str
    passed: bool
    expected_result: int
    actual_result: int
    expected_flags: Dict[str, bool]
    actual_flags: Dict[str, bool]
    message: str


class HardwareInterface:
    """Abstract interface for hardware/simulation evaluation."""

    def evaluate(self, test: Dict[str, Any]) -> Tuple[int, Dict[str, bool]]:
        raise NotImplementedError


class SimulatedALUHardware(HardwareInterface):
    """Simulated ALU evaluator for all 19 operations."""

    def evaluate(self, test: Dict[str, Any]) -> Tuple[int, Dict[str, bool]]:
        width = int(test.get("width", 8))
        mask = (1 << width) - 1
        msb = 1 << (width - 1)
        
        a = int(test.get("A", 0)) & mask
        b = int(test.get("B", 0)) & mask
        
        operation = normalize_operation(test)
        
        # Initialize flags
        carry = False
        overflow = False
        result = 0
        
        # Arithmetic Operations
        if operation == "ADD":
            raw = a + b
            result = raw & mask
            carry = raw > mask
            overflow = is_overflow_add(a, b, result, width)
            
        elif operation == "SUB":
            raw = a - b
            result = raw & mask
            carry = raw >= 0 # Borrow inverted? Standard ALU SUB often produces Carry=1 if no borrow (A >= B).
                             # Spec says M=1 (SUB) -> Cin=1, B inverted.
                             # A + ~B + 1. If result > mask, Carry=1. 
                             # This is equivalent to "Not Borrow".
                             # Let's stick to the previous implementation's logic: carry = raw >= 0
            if raw < 0:
                carry = False # Borrow occurred
            else:
                carry = True  # No borrow
            overflow = is_overflow_sub(a, b, result, width)
            
        elif operation == "INC_A":
            raw = a + 1
            result = raw & mask
            carry = raw > mask
            overflow = (a == (mask >> 1)) # Incrementing MAX_POSITIVE -> MIN_NEGATIVE
            
        elif operation == "DEC_A":
            raw = a - 1
            result = raw & mask
            # DEC A is A + 255 (if 8 bit). 
            # Carry behavior: A + 0xFF. If A>0, result causes carry. If A=0, result=255, no carry.
            carry = (a != 0)
            overflow = (a == msb) # Decrementing MIN_NEGATIVE -> MAX_POSITIVE
            
        elif operation == "CMP":
            # CMP is A - B but result is ignored (effectively). 
            # Flags are set exactly like SUB.
            raw = a - b
            result = 0 # Output not used/valid for CMP
            if raw < 0:
                carry = False
            else:
                carry = True
            overflow = is_overflow_sub(a, b, raw & mask, width)
            
        # Shift Operations
        elif operation in ("LSL", "SLL"):
            raw = a << 1
            result = raw & mask
            carry = bool(a & msb)
            
        elif operation in ("LSR", "SRL"):
            raw = a >> 1
            result = raw & mask
            carry = bool(a & 1)
            
        elif operation == "ASR":
            # Arithmetic Shift Right: replicate sign bit
            sign = a & msb
            raw = (a >> 1) | sign
            result = raw & mask
            carry = bool(a & 1)

        # Logic Operations (Carry/Overflow usually 0)
        elif operation == "AND":
            result = a & b
        elif operation == "OR":
            result = a | b
        elif operation == "XOR":
            result = a ^ b
        elif operation == "NAND":
            result = ~(a & b) & mask
        elif operation == "NOR":
            result = ~(a | b) & mask
        elif operation == "XNOR":
            result = ~(a ^ b) & mask
            
        elif operation == "NOT_A":
            result = (~a) & mask
        elif operation == "NOT_B":
            result = (~b) & mask
            
        elif operation == "PASS_A":
            result = a
        elif operation == "PASS_B":
            result = b
            
        elif operation == "REV_A":
            # Bit reverse
            bin_str = f"{a:0{width}b}"
            result = int(bin_str[::-1], 2)

        else:
            raise ValueError(f"Unsupported operation '{operation}'")

        # Zero and Negative flags are standard for RESULT (except CMP uses A-B result)
        if operation == "CMP":
             check_val = (a - b) & mask
        else:
             check_val = result

        zero = (check_val == 0)
        negative = bool(check_val & msb)
        
        flags = {
            "carry": carry,
            "overflow": overflow,
            "zero": zero,
            "negative": negative,
        }
        
        # Special case: CMP specific flags if your JSON expects specific keys
        # But usually Z/N/C/V key names are standard.
        
        return result, flags

def is_overflow_add(a, b, r, width):
    msb = 1 << (width - 1)
    a_sign = bool(a & msb)
    b_sign = bool(b & msb)
    r_sign = bool(r & msb)
    return (a_sign == b_sign) and (a_sign != r_sign)

def is_overflow_sub(a, b, r, width):
    msb = 1 << (width - 1)
    a_sign = bool(a & msb)
    b_sign = bool(b & msb)
    r_sign = bool(r & msb)
    return (a_sign != b_sign) and (a_sign != r_sign)

def normalize_operation(test: Dict[str, Any]) -> str:
    if "operation" in test:
        return str(test["operation"]).strip().upper().replace(" ", "_")
    
    opcode = str(test.get("opcode", "")).strip()
    
    # Map binary opcodes to names
    op_map = {
        "00000": "ADD",
        "00001": "SUB",
        "00010": "INC_A",
        "00011": "DEC_A",
        "00100": "LSL",
        "00101": "LSR",
        "00110": "ASR",
        "00111": "REV_A",
        "01000": "NAND",
        "01001": "NOR",
        "01010": "XOR",
        "01011": "PASS_A",
        "01100": "PASS_B",
        "01101": "AND",
        "01110": "OR",
        "01111": "XNOR",
        "10000": "CMP",
        "10001": "NOT_A",
        "10010": "NOT_B",
    }
    
    if opcode in op_map:
        return op_map[opcode]
        
    return "UNKNOWN"


def load_vectors(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if isinstance(data, dict) and "tests" in data:
        vectors = data["tests"]
    elif isinstance(data, list):
        vectors = data
    else:
        raise ValueError(f"Unsupported vector format in {path}")

    if not isinstance(vectors, list):
        raise ValueError(f"Unsupported vector format in {path}")

    return vectors


def evaluate_vectors(vector_file: Path, hw: HardwareInterface) -> List[TestResult]:
    results: List[TestResult] = []
    vectors = load_vectors(vector_file)
    
    # Sort vectors by opcode string (00000, 00001...) to match the requested execution order
    vectors.sort(key=lambda x: str(x.get("opcode", "")).strip())
    
    total = len(vectors)
    
    # Spinner animation
    spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    
    print(f"Processing {vector_file.name}...", end=" ", flush=True)

    for i, test in enumerate(vectors):
        # Update spinner every 2000 items (optimization)
        if i % 2000 == 0:
            spin_char = spinner[(i // 2000) % len(spinner)]
            sys.stdout.write(f"\rProcessing {vector_file.name}... {spin_char} ({int(i/total*100)}%)")
            sys.stdout.flush()

        test_name = str(test.get("test_name", "unnamed"))
        operation = normalize_operation(test)
        expected_result = int(test.get("expected_result", 0))
        expected_flags = {
            key: bool(value)
            for key, value in test.get("expected_flags", {}).items()
        }
        try:
            actual_result, actual_flags = hw.evaluate(test)
            passed = (expected_result == actual_result) and all(
                expected_flags.get(flag) == actual_flags.get(flag)
                for flag in expected_flags
            )
            message = "pass" if passed else "mismatch"
        except Exception as exc:  # pragma: no cover - defensive
            actual_result = -1
            actual_flags = {}
            passed = False
            message = f"error: {exc}"

        results.append(
            TestResult(
                vector_file=vector_file.name,
                test_name=test_name,
                operation=operation,
                passed=passed,
                expected_result=expected_result,
                actual_result=actual_result,
                expected_flags=expected_flags,
                actual_flags=actual_flags,
                message=message,
            )
        )
    
    sys.stdout.write(f"\rProcessing {vector_file.name}... Done!        \n")
    sys.stdout.flush()
    return results


def write_results_json(results: Iterable[TestResult], output_path: Path) -> None:
    payload = [asdict(result) for result in results]
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_results_csv(results: Iterable[TestResult], output_path: Path) -> None:
    rows = [asdict(result) for result in results]
    if not rows:
        output_path.write_text("", encoding="utf-8")
        return

    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def summarize(results: List[TestResult]) -> Tuple[int, int]:
    passed = sum(1 for result in results if result.passed)
    failed = len(results) - passed
    return passed, failed


def print_detailed_report(results: List[TestResult]) -> None:
    stats = {}
    for r in results:
        if r.operation not in stats:
            stats[r.operation] = {"pass": 0, "fail": 0, "total": 0}
        stats[r.operation]["total"] += 1
        if r.passed:
            stats[r.operation]["pass"] += 1
        else:
            stats[r.operation]["fail"] += 1

    print("\n" + "="*65)
    print(f"{'OPERATION':<15} | {'PASSED':<10} | {'FAILED':<10} | {'TOTAL':<10} | {'RATE':<5}")
    print("-" * 65)
    
    
    # Sort by opcode order from specification
    # Create a mapping for sort order
    order_map = {op: i for i, op in enumerate(OPCODE_ORDER)}
    
    # Sort keys based on the order map, putting unknown ops at the end
    sorted_ops = sorted(stats.keys(), key=lambda x: order_map.get(x, 999))
    
    for op in sorted_ops:
        s = stats[op]
        rate = (s["pass"] / s["total"]) * 100 if s["total"] > 0 else 0
        print(f"{op:<15} | {s['pass']:<10} | {s['fail']:<10} | {s['total']:<10} | {rate:5.1f}%")
    print("="*65 + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run ALU test vectors.")
    parser.add_argument(
        "--vectors-dir",
        default="test",
        help="Directory containing JSON test vectors.",
    )
    parser.add_argument(
        "--output-dir",
        default="results",
        help="Directory for CSV/JSON output files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    vectors_dir = Path(args.vectors_dir)
    output_dir = Path(args.output_dir)

    vector_files = sorted(vectors_dir.glob("*.json"))
    if not vector_files:
        print(f"No JSON vector files found in {vectors_dir}")
        return 1

    hw = SimulatedALUHardware()
    all_results: List[TestResult] = []

    start_time = datetime.now()
    print(f"Test Run Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    for vector_file in vector_files:
        results = evaluate_vectors(vector_file, hw)
        passed, failed = summarize(results)
        status = "PASS" if failed == 0 else "FAIL"
        print(f"{status} {vector_file.name}: {passed}/{len(results)}")
        all_results.extend(results)


    total_passed, total_failed = summarize(all_results)
    end_time = datetime.now()
    duration = end_time - start_time
    
    print(f"\nSummary: {total_passed} passed, {total_failed} failed")
    print(f"Completed: {end_time.strftime('%Y-%m-%d %H:%M:%S')} (Duration: {duration})")

    # Detailed Breakdown
    if all_results:
        print_detailed_report(all_results)

    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("Writing detailed results to disk...", end=" ", flush=True)
    
    json_path = output_dir / "test_results.json"
    csv_path = output_dir / "test_results.csv"
    write_results_json(all_results, json_path)
    write_results_csv(all_results, csv_path)
    
    print("Done!")
    print(f"Results saved to {output_dir}/ at {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

    return 0 if total_failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
