#!/usr/bin/env python3
"""
Convert UTF-8 to ANSI.
"""

import sys
from pathlib import Path

for d in ("in", "out", "done", "error"):
    p = Path(d)
    p.mkdir(exist_ok=True)

for f in Path("in").glob("*.*"):
    print(f.name)

    try:
        with f.open(encoding="utf-8") as fh:
            cont = fh.read()
    except UnicodeEncodeError:
        f.rename(f"error/{f.name}")
        print(f"ERROR reading '{f.name}' as UTF-8")
        sys.exit()

    try:
        with Path(f"out/{f.name}").open(
            mode="w", encoding="ansi", newline="\r\n"
        ) as fh:
            fh.write(cont)
        f.rename(f"done/{f.name}")
    except UnicodeEncodeError:
        f.rename(f"error/{f.name}")
        print(f"ERROR converting '{f.name}' to ANSI")
        Path(f"out/{f.name}").unlink()
