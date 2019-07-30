import math

__VALUES__ = {
    "AGL +1": "Agility +1",
    "AGL +1 Rad. Res +30": "Agility +1, Rad. Res +1",
    "AGL -1": "Agility -1",
    "AGL -1 Fire Res. +15 Psn. Res. +15 Rad. Res. +15": "Agility -1, Fire Res., Psn. Res., Rad. Res. +1",
    "AGL -2": "Agility -1",
    "AP +10": "",
    "AP +20": "",
    "Barter +5": "Barter +1",
    "CHR +1": "Charisma +1",
    "CHR +2": "Charisma +2",
    "CHR -1": "Charisma -1",
    "Crit. Chan. +2": "Crit. +1",
    "Crit. Chan. +5": "Crit. +1",
    "Crit. Chance +5% CH +1": "Crit. +1, Charisma +1",
    "Crit. chance +2": "Crit. +1",
    "Crit. chance +3%": "Crit. +1",
    "Critical Chance +5%": "Crit. +1",
    "Critical chance +3": "Crit. +1",
    "Crouch-Speed +20%": "",
    "DR +5": "DR +1",
    "END +1": "Endurance +1",
    "END +1 Carry Weight +25": "Endurance +1, Carry Weight +5",
    "Ener. Weap. +10": "Energy Weapons +1",
    "Ener. Weap. +5": "Energy Weapons +1",
    "Energy Resistance +10": "Energy DR +1",
    "Energy Weapons +2": "Energy Weapons +1",
    "Energy Weapons +5": "Energy Weapons +1",
    "Energy Weapons +5 Guns +5": "Energy Weapons +1, Guns +1",
    "Explos. +5": "Explosives +1",
    "Explosives +10": "Explosives +1",
    "Explosives +10 INT +2 PER +2 (with Four Eyes )": "Explosives +1, Intelligence +1, Perception +1(with Four Eyes)",
    "Fire Res. +15 Psn. Res. +15 Rad. Res. +15": "Fire Res., Psn. Res., Rad. Res. +1",
    "Fire Resistance +25": "Fire Res.",
    "Fire resistance +15": "Fire Res.",
    "Guns +10": "Guns +1",
    "Guns +2": "Guns +1",
    "Guns +3": "Guns +1",
    "Guns +5": "Guns +1",
    "HP +2": "Hit Points +2",
    "INT +1": "Intelligence +1",
    "INT +2": "Intelligence +1",
    "LCK +1": "Luck +1",
    "LCK +1 PER +3 (with Four Eyes )": "Luck +1, Perception +1 (with Four Eyes)",
    "LCK +1 Psn. Res. +30": "Luck +1, Psn. Res.",
    "Lockpick +5": "Lockpick +1",
    "Medicine +10": "Medicine +1",
    "Medicine +5": "Medicine +1",
    "Melee Weap. +2": "Melee Weapons +1",
    "Melee Weap. +5": "Melee Weapons +1",
    "Melee Weapons +2": "Melee Weapons +1",
    "Melee Weapons +3": "Melee Weapons +1",
    "Melee Weapons +5": "Melee Weapons +1",
    "PER +1": "Perception +1",
    "PER +2": "Perception +1",
    "PER +2 (with Four Eyes )": "Perception +1 (with Four Eyes)",
    "Poison resistance +85": "Psn. Res.",
    "Rad Res. +3": "Rad. Res. +1",
    "Rad Res. +5": "Rad. Res. +1",
    "Rad Res. +8": "Rad. Res. +1",
    "Rad. Res. + 40": "Rad. Res. +2",
    "Rad. Res. +10": "Rad. Res. +1",
    "Rad. Res. +15": "Rad. Res. +1",
    "Rad. Res. +20": "Rad. Res. +1",
    "Rad. Res. +25": "Rad. Res. +1",
    "Rad. Res. +30": "Rad. Res. +1",
    "Rad. Res. +40": "Rad. Res. +2",
    "Rad. Res. +5": "Rad. Res. +1",
    "Repair +5": "Repair +1",
    "Repair +5 INT +1 PER +2 (with Four Eyes )": "Repair +1, Intelligence +1, Perception +1 (with Four Eyes)",
    "STR +1": "Strength +1",
    "STR +1 AP +15": "Strength +1",
    "STR +2": "Strength +1",
    "Science +10": "Science +1",
    "Science +15": "Science +1",
    "Science +5": "Science +1",
    "Sneak +10": "Sneak +1",
    "Sneak +2": "Sneak +1",
    "Sneak +5": "Sneak +1",
    "Speech +10": "Speech +1",
    "Speech +2": "Speech +1",
    "Speech +5": "Speech +1",
    "Survival +2": "Survival +1",
    "Survival +5": "Survival +1",
    "Unarmed +3": "Unarmed +1",
    "from Sneak +15 to Sneak +25": "Sneak +1",
}


class Armor(object):
    def __init__(self, filepath, obj):

        self.name = obj["Name"]
        self.dr = self.__parse_dr__(obj)
        self.value = obj["Value"]

        self.category = filepath.split(".")[-2].split("/")[-1]
        self.effect = self.__parse_effect__(obj)
        self.weight = self.__parse_weight__(obj)
        self.faction = self.__parse_faction__(obj)
        self.is_highlighted = obj["is_highlighted"] == "True"

    def __parse_effect__(self, obj):
        value = obj["Effect"]
        if value == "—":
            return ""

        # Long keys first
        keys = list(__VALUES__.keys())
        keys.sort(key=lambda k: len(k), reverse=True)

        for key in keys:
            if key in value:
                value = value.replace(key, __VALUES__[key])

        return value

    def __parse_faction__(self, obj):
        value = obj["Faction"] if "Faction" in obj else ""
        return "" if value == "—" else value

    def __parse_dr__(self, obj):
        # ~1/2 DPS of Anti material rifle
        return int(math.ceil(int(obj["DT"]) / 4.0))

    def __parse_weight__(self, obj):
        # GURPs wieght is 1/10 of ingame weight
        return int(math.ceil(float(obj["Weight"]) / 10.0))
