#!/usr/bin/env python3
"""
Playground for the vobject module.
"""

import codecs
from pprint import pprint

import vobject  # pip install vobject

fileIn = "ab-torben-nc-2023-02-05.vcf"
obj = vobject.readComponents(  # type: ignore
    codecs.open(fileIn, encoding="utf-8").read(),
)
contacts: list[vobject.base.Component] = list(obj)  # type: ignore

card = contacts[0]
n = card.contents["n"]
pprint(card.contents["fn"])
pprint(card.contents["n"][0])
pprint(type(n[0]))
pprint(len(n))
pass
