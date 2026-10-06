#!/usr/bin/env python3
"""Compare localization-key snapshots without depending on locale sort order."""

from __future__ import annotations

import sys
from pathlib import Path


def read_lines(path: Path) -> set[str]:
    return {line for line in path.read_text(encoding="utf-8").splitlines() if line}


def write_lines(path: Path, lines: set[str]) -> None:
    content = "\n".join(sorted(lines))
    path.write_text(content + ("\n" if content else ""), encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 5:
        print(
            f"usage: {sys.argv[0]} OLD NEW ADDED REMOVED",
            file=sys.stderr,
        )
        return 2

    old_path, new_path, added_path, removed_path = map(Path, sys.argv[1:])
    old = read_lines(old_path)
    new = read_lines(new_path)
    write_lines(added_path, new - old)
    write_lines(removed_path, old - new)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
