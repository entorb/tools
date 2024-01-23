#!/usr/bin/env python3
"""
Convert UTF-8 to ANSI.
"""

# TODO:
# ruff: noqa

import glob
import os

for d in ("in", "out", "done", "error"):
    os.makedirs(d, exist_ok=True)  # = mkdir -p

for f in glob.glob("in/*.*"):
    (filepath, fileName) = os.path.split(f)
    print(fileName)

    try:
        with open(f, encoding="utf-8") as fh:
            cont = fh.read()
    except UnicodeEncodeError:
        os.rename(f, f"error/{fileName}")
        print(f"ERROR reading '{fileName}' as UTF-8")
        exit()

    try:
        with open(f"out/{fileName}", mode="w", encoding="ansi", newline="\r\n") as fh:
            fh.write(cont)
        os.rename(f, f"done/{fileName}")
    except UnicodeEncodeError:
        os.rename(f, f"error/{fileName}")
        print(f"ERROR converting '{fileName}' to ANSI")
        os.remove(f"out/{fileName}")
