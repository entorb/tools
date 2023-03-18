#!/usr/bin/env python3
# by Dr. Torben Menke, 24.09.2019
"""
Cartesian product of multiple lists.

* reads several lists from `cartesian-csv-gen.ini`
* generates Cartesian product of all combinations

see README.md for example
"""

import itertools
from configparser import ConfigParser

config = ConfigParser()
config.read("cartesian-csv-gen.ini")

list_keys: list[str] = []
list_values: list[list[str]] = []

for k in config.options("dynamic"):
    s = config.get("dynamic", k)
    list_keys.append(k)
    values = s.split(",")
    values = [v.strip() for v in values]  # trim white spaces
    list_values.append(values)

with open("out.tsv", "w", newline="\n") as fh:
    fh.write("\t".join(list_keys))
    fh.write("\n")

    # Cartesian product
    for combination in itertools.product(*list_values):
        fh.write("\t".join(combination))
        fh.write("\n")
