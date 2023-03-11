#!/usr/bin/env python3
"""
Export a filtered AB.

Containing only cards having a bday
fields: BDAY FN N
"""

import codecs
import re

import vobject  # pip install vobject

file_in = "ab-torben-nc-2023-02-05.vcf"
file_out = "out.vcf"

obj = vobject.readComponents(codecs.open(file_in, encoding="utf-8").read())  # type: ignore
contacts: list[vobject.base.Component] = list(obj)  # type: ignore

contacts_filtered: list[vobject.base.Component] = []

for card in contacts:
    # card.prettyPrint()
    # s = card.serialize()
    # d = card.contents

    if "bday" not in card.contents:
        continue

    # bday: remove 'VALUE': ['DATE']
    card.contents["bday"][0].params = {}  # type: ignore

    # remove all fields but "bday", "n"
    for key in card.contents.copy():  # loop over copy, to allow for deleting keys
        if key not in ("n", "bday"):
            del card.contents[key]

    # recreate fn based on n
    card.add("fn")
    n = card.contents["n"][0]
    fn = f"{n.value.given} {n.value.additional} {n.value.family}"  # type: ignore
    fn = re.sub(r"\s+", " ", fn)
    card.fn.value = fn  # type: ignore

    contacts_filtered.append(card)

with open(file_out, mode="w", encoding="utf-8", newline="\n") as fhOut:
    for card in contacts_filtered:
        fhOut.write(card.serialize())
