#!/usr/bin/env python3
# by Dr. Torben Menke, 24.09.2019
"""
Cartesian product of dynamic parameters.

reads config.ini
extracts dynamic parameters (list of values per parameter, sep. by ," )
generates cartesian product of dynamic parameters
"""
import itertools
from configparser import ConfigParser

config = ConfigParser()
config.read("cartesian-csv-gen.ini")

listOfKeys: list[str] = []
listsOfValues: list[str] = []

for k in config.options("dynamic"):
    s = config.get("dynamic", k)
    listOfKeys.append(k)
    l = s.split(",")
    l = [v.strip() for v in l]  # trim white spaces
    listsOfValues.extend(l)

with open("out.csv", "w", newline="\n") as fh:
    fh.write("\t".join(listOfKeys))
    fh.write("\n")

    # Cartesian product of the listsOfDynVars
    for combination in itertools.product(*listsOfValues):
        fh.write("\t".join(combination))
        fh.write("\n")
