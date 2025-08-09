#!/usr/bin/env python3
"""Pre-commit hook to reject unfinished code markers and duplicate lines."""

from __future__ import annotations

import sys
from pathlib import Path

PLACEHOLDERS = ["TODO", "FIXME", "pass", "NotImplementedError", "placeholder", "..."]

def check_file(path: Path) -> list[str]:
    errors: list[str] = []
    previous: str | None = None
    if path.name == "no_placeholders.py":
        return errors
    try:
        text = path.read_text(encoding="utf-8").splitlines()
    except Exception:
        return errors
    for idx, line in enumerate(text, 1):
        stripped = line.strip()
        if "PLACEHOLDERS" in line:
            continue
        for token in PLACEHOLDERS:
            if token in line:
                errors.append(f"{path}:{idx}: found placeholder '{token}'")
        if previous is not None and stripped and stripped == previous and stripped not in {')', ']', '}'}:
            errors.append(f"{path}:{idx}: duplicate line '{stripped}'")
        previous = stripped
    return errors

def main(argv: list[str]) -> int:
    all_errors: list[str] = []
    for file_name in argv:
        path = Path(file_name)
        if path.is_file():
            all_errors.extend(check_file(path))
    if all_errors:
        print("\n".join(all_errors))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
