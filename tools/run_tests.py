#!/usr/bin/env python3
"""Test runner for JSON vectors in the test/ directory."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


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
    """Simulated ALU evaluator for add/sub operations."""

    def evaluate(self, test: Dict[str, Any]) -> Tuple[int, Dict[str, bool]]:
        width = int(test.get("width", 8))
        mask = (1 << width) - 1
        a = int(test["A"]) & mask
        b = int(test["B"]) & mask

        operation = normalize_operation(test)
        if operation not in {"ADD", "SUB"}:
            raise ValueError(f"Unsupported operation '{operation}'")

        if operation == "ADD":
            raw = a + b
            result = raw & mask
            carry = raw > mask
        else:
            raw = a - b
            result = raw & mask
            carry = raw >= 0

        a_signed = to_signed(a, width)
        b_signed = to_signed(b, width)
        result_signed = to_signed(result, width)

        if operation == "ADD":
            overflow = (
                (a_signed >= 0 and b_signed >= 0 and result_signed < 0)
                or (a_signed < 0 and b_signed < 0 and result_signed >= 0)
            )
        else:
            overflow = (
                (a_signed >= 0 and b_signed < 0 and result_signed < 0)
                or (a_signed < 0 and b_signed >= 0 and result_signed >= 0)
            )

        flags = {
            "carry": carry,
            "overflow": overflow,
            "zero": result == 0,
            "negative": bool(result & (1 << (width - 1))),
        }
        return result, flags


def to_signed(value: int, width: int) -> int:
    sign_bit = 1 << (width - 1)
    if value & sign_bit:
        return value - (1 << width)
    return value


def normalize_operation(test: Dict[str, Any]) -> str:
    if "operation" in test:
        return str(test["operation"]).strip().upper()
    opcode = str(test.get("opcode", "")).strip()
    if opcode in {"0000", "00000000"}:
        return "ADD"
    if opcode in {"11111111", "0001"}:
        return "SUB"
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

    for test in vectors:
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

    for vector_file in vector_files:
        results = evaluate_vectors(vector_file, hw)
        passed, failed = summarize(results)
        status = "PASS" if failed == 0 else "FAIL"
        print(f"{status} {vector_file.name}: {passed}/{len(results)}")
        all_results.extend(results)

    total_passed, total_failed = summarize(all_results)
    print(f"Summary: {total_passed} passed, {total_failed} failed")

    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "test_results.json"
    csv_path = output_dir / "test_results.csv"
    write_results_json(all_results, json_path)
    write_results_csv(all_results, csv_path)
    print(f"Wrote results to {json_path} and {csv_path}")

    return 0 if total_failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
