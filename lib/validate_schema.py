#!/usr/bin/env python3
"""Validate JSON Lines records against the pipeline's enrichment data contract."""

import sys
import json

REQUIRED_FIELDS = ["video_id", "cleaned_text"]
OPTIONAL_FIELDS = ["tech_terms", "book_names"]


def _check_required_keys(line_num, payload):
    """Return False and log an error if any required key is missing."""
    for field in REQUIRED_FIELDS:
        if field not in payload:
            print(f"❌ [Row {line_num}] Schema Failure: Missing mandatory key '{field}'.")
            return False
    return True


def _check_required_types(line_num, payload):
    """Return False and log an error if required fields have the wrong type."""
    if not isinstance(payload["video_id"], str) or not payload["video_id"].strip():
        print(f"❌ [Row {line_num}] Type Failure: 'video_id' must be a non-empty STRING.")
        return False

    if not isinstance(payload["cleaned_text"], str):
        print(f"❌ [Row {line_num}] Type Failure: 'cleaned_text' must be a STRING.")
        return False

    return True


def _check_optional_types(line_num, payload):
    """Return False and log an error if optional array fields are malformed."""
    for field in OPTIONAL_FIELDS:
        if field not in payload:
            continue

        if not isinstance(payload[field], list):
            print(f"❌ [Row {line_num}] Type Failure: '{field}' must be an ARRAY (Python list).")
            return False

        if not all(isinstance(item, str) for item in payload[field]):
            print(
                f"❌ [Row {line_num}] Type Failure: All elements inside '{field}' must be STRINGS."
            )
            return False

    return True


def validate_payload(line_num, payload):
    """
    Validate a single line of JSON data against the target API contract.
    Returns True if valid, False otherwise.
    """
    if not isinstance(payload, dict):
        print(f"❌ [Row {line_num}] Schema Failure: Record is not a valid JSON Object.")
        return False

    return (
        _check_required_keys(line_num, payload)
        and _check_required_types(line_num, payload)
        and _check_optional_types(line_num, payload)
    )


def main():
    """Read JSON Lines from stdin and validate each record against the schema contract."""
    print("🚀 Starting pipeline data contract validation...")
    total_records = 0
    failed_records = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        total_records += 1
        try:
            data = json.loads(line)
            if not validate_payload(total_records, data):
                failed_records += 1
        except json.JSONDecodeError:
            print(f"❌ [Row {total_records}] Syntax Failure: Line is not valid JSON Lines format.")
            failed_records += 1

    print("\n--- Validation Summary ---")
    if total_records == 0:
        print("⚠️ Warning: No records were processed via stdin.")
        sys.exit(1)
    elif failed_records > 0:
        print(f"🔴 Failure: {failed_records}/{total_records} records violated the schema contract.")
        sys.exit(1)
    else:
        print(f"🟢 Success: All {total_records} records successfully match the required data contract!")
        sys.exit(0)


if __name__ == '__main__':
    main()
