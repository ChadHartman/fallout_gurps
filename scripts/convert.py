#!/usr/bin/env python3

import json
import os
from weapon import Weapon


def convert_weapons(weapons):

    weapons.sort(key=lambda w: w.damage, reverse=True)

    for weapon in weapons:
        print(weapon.__dict__)
        # print("{0: <40} {1: <16} {2: <16}".format(
        #     weapon.name, weapon.skill, weapon.damage))


def load_weapons():

    weapons = []
    filepath = None

    try:
        weapon_dir = "../out/weapons"
        for filename in os.listdir(weapon_dir):
            if not filename.endswith(".json"):
                continue

            filepath = os.path.join(weapon_dir, filename)

            with open(filepath, 'r') as f:
                for json_obj in json.load(f):
                    weapons.append(Weapon(filepath, json_obj))

        convert_weapons(weapons)

    except Exception as e:
        print("Error in " + filepath)
        raise e


def main():
    load_weapons()


if __name__ == '__main__':
    main()
