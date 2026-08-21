#!/usr/bin/env python3
"""Dependency-free checks for repository structure and icon metadata."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
APP = ROOT / "app.py"
REQUIREMENTS = ROOT / "requirements.txt"
RUNTIME = ROOT / "runtime.txt"


def main() -> int:
    for path in (README, APP, REQUIREMENTS, RUNTIME):
        if not path.is_file():
            raise SystemExit(f"Missing required deployment file: {path.relative_to(ROOT)}")

    readme = README.read_text(encoding="utf-8")
    app = APP.read_text(encoding="utf-8")
    runtime = RUNTIME.read_text(encoding="utf-8").strip()

    if runtime != "python-3.11":
        raise SystemExit("runtime.txt must pin the supported Python major/minor runtime to python-3.11")

    icon_wall = readme.split("### Stack Icon Wall", 1)[-1].split("| Layer |", 1)[0]
    icon_urls = re.findall(r'<img\s+src="([^"]+)"\s+alt="([^"]+)"', icon_wall)
    if len(icon_urls) != 8:
        raise SystemExit(f"Expected 8 stack icons, found {len(icon_urls)}")

    alts = [alt for _, alt in icon_urls]
    if len(alts) != len(set(alts)):
        raise SystemExit("Stack Icon Wall contains duplicate alt labels")

    if "cdn.simpleicons.org/chroma" in icon_wall:
        raise SystemExit("README still references the unavailable Chroma Simple Icons slug")

    if "1.26043595e+08+Samarssj@users.noreply.github.com" in readme:
        raise SystemExit("README contains a malformed generated GitHub email")

    if "def icon(name: str)" not in app or "def plain_icon(name: str)" not in app:
        raise SystemExit("Application icon rendering helpers are missing")

    print("Smoke checks passed: runtime, README icon wall, and application icon helpers.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
