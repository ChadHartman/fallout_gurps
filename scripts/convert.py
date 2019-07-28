#!/usr/bin/env python3

import json
import os


class Weapon(object):
    """
    {
        'Rate of fire': '4',
        'Projectile explosive weapon name': 'Red Glare ¹',
        'Weapon weight': '20',
        'Weapon durability in shot until broken': '2245',
        'Skill required': '100',
        'Base ID': 'xx 004c3c',
        'Weapon value in caps': '15000',
        'Magazine capacity (shots per reload)': '13',
        'Image': '',
        'Weapon Spread': '0.5',
        'Damage per Action Point': '2.4',
        'Strength required': '6',
        'Action point cost': '25',
        'Damage per shot': '20 +40',
        'Damage per second': '240',
        'Ammunition used': 'Rocket',
        'Value to weight ratio': '750',
        'AOE': '500'
    }
    """

    def __init__(self, filepath, obj):
        for key in obj:
            if "name" in key:
                self.name = obj[key]
        self.damage = self.__convert_dmg__(
            obj["Damage per second"] if "Damage per second" in obj else 0)
        self.ammo_type = obj["Ammunition used"] if "Ammunition used" in obj else None
        self.weight = obj["Weapon weight"]
        self.cost = obj["Weapon value in caps"]
        self.skill_required = obj["Skill required"]
        self.str_req = obj["Strength required"]
        self.aoe = obj["AOE"] if "AOE" in obj else "0"
        self.skill = filepath.split("/")[-1].split("-")[0]

    def __convert_dmg__(self, value):
        return float(value)


def convert_weapons(weapons):

    weapons.sort(key=lambda w: w.damage, reverse=True)

    for weapon in weapons:
        print("{0: <40} {1: <16} {2: <16}".format(
            weapon.name, weapon.skill, weapon.damage))


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
