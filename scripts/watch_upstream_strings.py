#!/usr/bin/env python3
"""Build a stable manifest of macOS localization keys in apple-browsers."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def xcstrings_keys(path: Path) -> list[str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        print(f"warning: cannot parse {path}: {error}", file=sys.stderr)
        return []
    strings = data.get("strings", {})
    return sorted(strings) if isinstance(strings, dict) else []


def legacy_strings_keys(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-16")
    return sorted(set(re.findall(r'^\s*"((?:\\.|[^"\\])*)"\s*=', text, re.MULTILINE)))


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} APPLE_BROWSERS_DIR OUTPUT", file=sys.stderr)
        return 2

    root, output = Path(sys.argv[1]), Path(sys.argv[2])
    macos = root / "macOS"
    if not macos.is_dir():
        print(f"missing upstream macOS directory: {macos}", file=sys.stderr)
        return 1

    rows: list[str] = []
    for path in sorted(macos.rglob("*.xcstrings")):
        relative = path.relative_to(root).as_posix()
        rows.extend(f"{relative}\t{key}" for key in xcstrings_keys(path))
    for path in sorted(macos.rglob("*.strings")):
        relative = path.relative_to(root).as_posix()
        rows.extend(f"{relative}\t{key}" for key in legacy_strings_keys(path))

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(sorted(set(rows))) + "\n", encoding="utf-8")
    print(f"wrote {len(set(rows))} localization keys to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
