#!/usr/bin/env python3

import json


class Character(object):
    def __init__(self):
        base_value = 5
        self.skill_offset = -1
        self.base_strength = base_value
        self.base_perception = base_value
        self.base_endurance = base_value
        self.base_charisma = base_value
        self.base_intelligence = base_value
        self.base_agility = base_value
        self.base_luck = base_value

    @property
    def strength(self):
        return self.base_strength

    @property
    def agility(self):
        return self.base_agility

    @property
    def rad_resistance(self):
        return self.base_endurance - 3

    @property
    def dodge(self):
        return round((2*self.agility)/4.0)

    @property
    def carry_weight(self):
        return round((self.strength*self.strength) / 5.0)

    @property
    def hit_points(self):
        return self.strength

    @property
    def base_barter(self):
        return self.base_charisma+self.skill_offset

    @property
    def base_energy_weapons(self):
        return self.base_perception+self.skill_offset

    @property
    def base_explosives(self):
        return self.base_perception+self.skill_offset

    @property
    def base_guns(self):
        return self.base_agility+self.skill_offset

    @property
    def base_lockpick(self):
        return self.base_perception+self.skill_offset

    @property
    def base_medicine(self):
        return self.base_intelligence+self.skill_offset

    @property
    def base_melee_weapons(self):
        return self.base_strength+self.skill_offset

    @property
    def base_repair(self):
        return self.base_intelligence+self.skill_offset

    @property
    def base_science(self):
        return self.base_intelligence+self.skill_offset

    @property
    def base_sneak(self):
        return self.base_agility+self.skill_offset

    @property
    def base_speech(self):
        return self.base_charisma+self.skill_offset

    @property
    def base_survival(self):
        return self.base_endurance+self.skill_offset

    @property
    def base_unarmed(self):
        return self.base_endurance+self.skill_offset


def main():
    character = Character()
    for prop in dir(character):
        if prop.startswith("__"):
            continue
        print(prop, ":", character.__getattribute__(prop))
    # print(json.dumps(character.__dict__, indent=4))


if __name__ == "__main__":
    main()
