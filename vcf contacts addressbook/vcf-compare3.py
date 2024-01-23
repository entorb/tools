#!/usr/bin/env python3
"""
Convert vcf to sorted list of cleaned cards.

converts vcf to a list, sorted by Full Name FN field,
to allow for comparison of 2 backups of the same address book
"""

# TODO:
# ruff: noqa

import codecs
import os.path

import vobject  # pip install vobject

# file_in = '2020/ab-torben-nc-2020-06-24-nc-V18-a-EDIT.vcf'
# file_in = '2020/ab-torben-nc-2020-06-04.vcf'
# file_in = '2020/ab-torben-nc-2020-01-17.vcf'
# file_in = '2020/ab-torben-nc-2020-06-25-V3-iCloud-exp.vcf'
# file_in = "../2020/ab-torben-nc-2020-09-27.vcf"
# file_in = '../2021/ab-torben-nc-2021-01-15.vcf'
file_in = "vcf contacts addressbook/addressbook.vcf"

(fileBaseName, fileExtension) = os.path.splitext(file_in)
file_out = f"{fileBaseName}-out.txt"

obj = vobject.readComponents(codecs.open(file_in, encoding="utf-8").read())
# contacts = [contact for contact in obj]
contacts = list(obj)
d_all_cards_by_name = {}

l_tags_to_remove = ["rev", "uid", "adr", "prodid", "photo"]

for card in contacts:
    # card.prettyPrint()
    # TODO: remove field REV, PHOTO, ADR
    if "rev" in card.contents:
        del card.contents["rev"]
    if "uid" in card.contents:
        del card.contents["uid"]
    if "photo" in card.contents:
        del card.contents["photo"]
    if "adr" in card.contents:
        del card.contents["adr"]
    s = card.serialize()
    d = card.contents
    fn = d["fn"][0].value

    # TODO:    assert fn not in d_all_cards_by_name, f"ERROR: {fn} is not unique"

    d_all_cards_by_name[fn] = s

l_names = sorted(d_all_cards_by_name.keys())

with open(file_out, mode="w", encoding="utf-8", newline="\n") as fh_out:  # noqa: PTH123
    for name in l_names:
        card = d_all_cards_by_name[name]
        fh_out.write(card)
