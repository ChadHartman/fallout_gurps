#!/usr/bin/env python3

import json
import os
from armor import Armor


def convert_armor(armor):

    armor.sort(key=lambda a: int(a.weight), reverse=True)
    cols_printed = False
    f = "{:<32}\t{:<16}\t{:>2}\t{:>5}\t{:>5}\t{:<16}\t{}"

    for a in armor:

        if not cols_printed:
            print(f.format(
                "Name",
                "Category",
                "DR",
                "Weight",
                "Value",
                "Faction",
                "Effect"))
            cols_printed = True

        print(f.format(
            a.name,
            a.category,
            a.dr,
            a.weight,
            a.value,
            a.faction,
            a.effect))


def load_armor():

    armor = []
    filepath = None

    armor_dir = "../out/armor"
    for filename in os.listdir(armor_dir):
        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(armor_dir, filename)

        with open(filepath, 'r') as f:
            for json_obj in json.load(f):
                armor.append(Armor(filepath, json_obj))

    convert_armor(armor)


def main():
    load_armor()


if __name__ == '__main__':
    main()
