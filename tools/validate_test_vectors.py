#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

import jsonschema


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate ALU test vectors against the JSON schema."
    )
    parser.add_argument(
        "--schema",
        type=Path,
        default=Path("test/schema/test-vector.schema.json"),
        help="Path to the JSON schema file.",
    )
    parser.add_argument(
        "--vectors",
        type=Path,
        default=Path("test/vectors"),
        help="Directory containing test vector JSON files.",
    )
    return parser.parse_args()


def load_schema(schema_path: Path) -> dict:
    with schema_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    args = parse_args()
    if not args.schema.exists():
        raise FileNotFoundError(f"Schema not found: {args.schema}")

    schema = load_schema(args.schema)

    if not args.vectors.exists():
        print(f"No test vector directory found at {args.vectors}; skipping validation.")
        return 0

    json_files = sorted(args.vectors.rglob("*.json"))
    if not json_files:
        print(f"No test vector JSON files found in {args.vectors}; skipping validation.")
        return 0

    failures = []
    for json_file in json_files:
        try:
            with json_file.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
            jsonschema.validate(instance=data, schema=schema)
            print(f"Validated {json_file}")
        except (jsonschema.ValidationError, json.JSONDecodeError) as exc:
            failures.append(f"{json_file}: {exc}")

    if failures:
        for failure in failures:
            print(f"ERROR: {failure}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
