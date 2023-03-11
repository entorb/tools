#!/usr/bin/env python3
# by Dr. Torben Menke, 24.09.2019
"""
Cartesian product of dynamic parameters.

reads config.ini
extracts dynamic parameters (list of values per parameter, separated by ',' )
generates cartesian product of all dynamic parameter combinations
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
    l = s.split(",")
    l = [v.strip() for v in l]  # trim white spaces
    list_values.append(l)

with open("out.csv", "w", newline="\n") as fh:
    fh.write("\t".join(list_keys))
    fh.write("\n")

    # Cartesian product
    for combination in itertools.product(*list_values):
        fh.write("\t".join(combination))
        fh.write("\n")
