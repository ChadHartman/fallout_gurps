#!/usr/bin/env python3

import json
import os
from weapon import Weapon


def convert_weapons(weapons):

    weapons.sort(key=lambda w: w.damage, reverse=True)
    cols_printed = False
    
    for weapon in weapons:

        f = "{:<36}\t{:<10}\t{:>6}\t{:<16}\t{:>10}\t{:>3}\t{:>6}\t{:>5}\t{:>9}\t{:>13}"

        if not cols_printed:
            print(f.format(
                "Name",
                "Skill",
                "Damage",
                "Ammo Type",
                "Atk/Reload",
                "AOE",
                "Weight",
                "Cost",
                "Skill Req",
                "Strength Req"))
            cols_printed = True

        print(f.format(
            weapon.name,
            weapon.skill,
            weapon.damage,
            weapon.ammo_type,
            weapon.attacks_until_reload,
            weapon.aoe,
            weapon.weight,
            weapon.cost,
            weapon.skill_req,
            weapon.str_req))
            


def load_weapons():

    weapons = []
    filepath = None

    # try:
    weapon_dir = "../out/weapons"
    for filename in os.listdir(weapon_dir):
        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(weapon_dir, filename)

        with open(filepath, 'r') as f:
            for json_obj in json.load(f):
                weapons.append(Weapon(filepath, json_obj))

    convert_weapons(weapons)

    # except Exception as e:
    #     print("Error in " + filepath)
    #     raise e


def main():
    load_weapons()


if __name__ == '__main__':
    main()
