#!/usr/bin/env python3
"""Build a downloadable Czech localization package."""

from __future__ import annotations

import argparse
import plistlib
import re
import shutil
import tempfile
import zipfile
from pathlib import Path

ENTRY_RE = re.compile(
    r'^\s*"((?:\\.|[^"\\])*)"\s*=\s*"((?:\\.|[^"\\])*)"\s*;\s*$',
    re.MULTILINE,
)


def decode_quoted(value: str) -> str:
    replacements = {
        r"\\": "\\",
        r'\"': '"',
        r"\n": "\n",
        r"\r": "\r",
        r"\t": "\t",
    }
    return re.sub(r'\\(?:\\|"|n|r|t)', lambda m: replacements[m.group(0)], value)


def read_strings_fragment(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    entries = {
        decode_quoted(key): decode_quoted(value)
        for key, value in ENTRY_RE.findall(text)
    }
    declared = len(re.findall(r'^\s*"', text, re.MULTILINE))
    if not entries or len(entries) != declared:
        raise ValueError(
            f"{path}: parsed {len(entries)} entries, but found {declared} declarations"
        )
    return entries


def build(repo: Path, output: Path) -> None:
    source = repo / "translations" / "cs.lproj"
    main_updates = (
        repo / "translations" / "updates" / "macOS-DuckDuckGo-Localizable.cs.strings"
    )
    sync_updates = (
        repo / "translations" / "updates" / "SyncUI-macOS-Localizable.cs.strings"
    )

    with tempfile.TemporaryDirectory() as temporary:
        package = Path(temporary) / "DuckDuckGo-cs-localization"
        main_bundle = package / "main-app" / "cs.lproj"
        sync_bundle = package / "SyncUI-macOS" / "cs.lproj"
        shutil.copytree(source, main_bundle)
        sync_bundle.mkdir(parents=True)

        localizable = main_bundle / "Localizable.strings"
        with localizable.open("rb") as handle:
            translations = plistlib.load(handle)
        updates = read_strings_fragment(main_updates)
        translations.update(updates)
        with localizable.open("wb") as handle:
            plistlib.dump(translations, handle, fmt=plistlib.FMT_XML, sort_keys=False)

        sync_entries = read_strings_fragment(sync_updates)
        with (sync_bundle / "Localizable.strings").open("wb") as handle:
            plistlib.dump(sync_entries, handle, fmt=plistlib.FMT_XML, sort_keys=False)

        instructions = f"""Česká lokalizace DuckDuckGo pro macOS

main-app/cs.lproj
  Lokalizace hlavního balíčku aplikace. Obsahuje také {len(updates)}
  nejnovějších překladů ze složky translations/updates.

SyncUI-macOS/cs.lproj
  Samostatná lokalizace pro resource bundle SyncUI-macOS.
  Neumisťujte ji do hlavního cs.lproj, protože jde o jiný bundle.

Upozornění:
  Ruční zásah do podepsané aplikace poruší její elektronický podpis a po
  aktualizaci může být přepsán. Balíček je proto určen hlavně pro kontrolu,
  testování a předání překladů autorům aplikace.
"""
        (package / "ČTĚTE-MĚ.txt").write_text(instructions, encoding="utf-8")

        output.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
            for item in sorted(package.rglob("*")):
                if item.is_file():
                    archive.write(item, item.relative_to(package.parent))

    print(
        f"Created {output} ({len(translations)} main entries, "
        f"{len(sync_entries)} SyncUI entries)"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("dist/DuckDuckGo-cs-localization.zip"),
    )
    args = parser.parse_args()
    build(Path(__file__).resolve().parent.parent, args.output.resolve())


if __name__ == "__main__":
    main()
