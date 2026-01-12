#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

MASK_8BIT = 0xFF

OPCODE_NAMES = {
    0: "ADD",
    1: "SUB",
    8: "NAND",
    9: "NOR",
    10: "XOR",
    11: "PASS A",
    12: "PASS B",
    13: "AND",
    14: "OR",
    15: "XNOR",
    17: "NOT A",
    18: "NOT B",
}


def mask8(value: int) -> int:
    return value & MASK_8BIT


def compute_add(a: int, b: int):
    total = a + b
    result = mask8(total)
    carry = total > MASK_8BIT
    overflow = ((a ^ result) & (b ^ result) & 0x80) != 0
    return result, carry, overflow


def compute_sub(a: int, b: int):
    diff = a - b
    result = mask8(diff)
    carry = a >= b
    overflow = ((a ^ b) & (a ^ result) & 0x80) != 0
    return result, carry, overflow


def compute_logic(opcode: int, a: int, b: int):
    if opcode == 8:  # NAND
        result = mask8(~(a & b))
    elif opcode == 9:  # NOR
        result = mask8(~(a | b))
    elif opcode == 10:  # XOR
        result = mask8(a ^ b)
    elif opcode == 11:  # PASS A
        result = mask8(a)
    elif opcode == 12:  # PASS B
        result = mask8(b)
    elif opcode == 13:  # AND
        result = mask8(a & b)
    elif opcode == 14:  # OR
        result = mask8(a | b)
    elif opcode == 15:  # XNOR
        result = mask8(~(a ^ b))
    elif opcode == 17:  # NOT A
        result = mask8(~a)
    elif opcode == 18:  # NOT B
        result = mask8(~b)
    else:
        raise ValueError(f"Unsupported logic opcode: {opcode}")
    return result


def opcode_to_int(opcode_value: str) -> int:
    opcode_value = opcode_value.strip().lower()
    if opcode_value.startswith("0b"):
        opcode_value = opcode_value[2:]
    return int(opcode_value, 2)


def compute_expected(vector: dict):
    a = vector["A"]
    b = vector["B"]
    opcode = opcode_to_int(vector["opcode"])
    if opcode == 0:
        result, carry, overflow = compute_add(a, b)
    elif opcode == 1:
        result, carry, overflow = compute_sub(a, b)
    elif opcode in OPCODE_NAMES:
        result = compute_logic(opcode, a, b)
        carry = False
        overflow = False
    else:
        raise ValueError(f"Unsupported opcode: {opcode}")

    zero = result == 0
    negative = (result & 0x80) != 0
    return {
        "expected_result": result,
        "expected_flags": {
            "carry": carry,
            "overflow": overflow,
            "zero": zero,
            "negative": negative,
        },
    }


def load_vectors(paths):
    vectors = []
    for path in paths:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        if not isinstance(data, list):
            raise ValueError(f"{path} must contain a JSON array")
        for entry in data:
            entry["_source"] = path
        vectors.extend(data)
    return vectors


def main():
    parser = argparse.ArgumentParser(description="Validate ALU JSON test vectors.")
    parser.add_argument(
        "paths",
        nargs="*",
        help="JSON vector files (defaults to test/*.json).",
    )
    args = parser.parse_args()

    if args.paths:
        paths = [Path(p) for p in args.paths]
    else:
        paths = sorted(Path(__file__).parent.glob("*.json"))

    if not paths:
        raise SystemExit("No JSON vector files found.")

    vectors = load_vectors(paths)
    failures = 0
    for vector in vectors:
        expected = compute_expected(vector)
        if vector["expected_result"] != expected["expected_result"]:
            failures += 1
            print(
                f"{vector['test_name']} ({vector['_source']}): expected_result mismatch "
                f"{vector['expected_result']} != {expected['expected_result']}"
            )
        for flag, value in expected["expected_flags"].items():
            if vector["expected_flags"][flag] != value:
                failures += 1
                print(
                    f"{vector['test_name']} ({vector['_source']}): flag {flag} mismatch "
                    f"{vector['expected_flags'][flag]} != {value}"
                )

    if failures:
        raise SystemExit(f"Vector validation failed with {failures} mismatch(es).")
    print(f"Validated {len(vectors)} vectors across {len(paths)} file(s).")


if __name__ == "__main__":
    main()
