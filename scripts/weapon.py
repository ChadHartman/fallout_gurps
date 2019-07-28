import text_util
import math


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

        self.name = self.__parse_name__(obj)
        self.damage = self.__parse_dmg__(obj)
        self.ammo_type = obj["Ammunition used"] if "Ammunition used" in obj else ""
        self.weight = self.__parse_weight__(obj)
        self.cost = int(obj["Weapon value in caps"])
        self.skill_req = self.__parse_skill_req__(obj)
        self.str_req = self.__parse_str_req__(obj)
        self.aoe = self.__parse_aoe__(obj)
        self.skill = self.__parse_skill__(filepath)
        self.attacks_until_reload = self.__parse_aur__(obj)

    def __parse_str_req__(self, obj):
        value = int(obj["Strength required"])

        if value <= 5:
            return value * 2

        return {
            6: 11,
            7: 12,
            8: 13,
            9: 14,
            10: 14
        }[value]

    def __parse_weight__(self, obj):

        value = float(obj["Weapon weight"])
        max_weight = 15
        max_game_weight = 40
        return math.ceil(max_weight * value / max_game_weight)

    def __parse_aoe__(self, obj):
        aoe = obj["AOE"] if "AOE" in obj else "0"
        value = 0 if"-" in aoe else float(aoe)

        # ranges 0 -> 1700
        # max 5

        max_range = 5
        max_game_aoe = 1700

        return math.ceil(max_range * value / max_game_aoe)

    def __parse_skill_req__(self, obj):
        return {
            0: 8,
            25: 10,
            35: 11,
            45: 12,
            50: 12,
            55: 12,
            75: 13,
            85: 13,
            100: 14
        }[int(obj["Skill required"])]

    def __parse_skill__(self, filepath):
        name = filepath.split(".")[-2]
        name = name.split("/")[-1]
        return name.split("-")[0]

    def __parse_mag_cap__(self, obj):

        mag_cap = obj["Magazine capacity (shots per reload)"]

        if "(" in mag_cap:
            start = mag_cap.index("(")
            end = mag_cap.index(")")
            return float(mag_cap[start+1:end])

        return float(mag_cap)

    def __parse_aur__(self, obj):

        if "Magazine capacity (shots per reload)" in obj and "Rate of fire" in obj:
            mag_cap = self.__parse_mag_cap__(obj)
            rate_of_fire = obj["Rate of fire"]
            rate = math.ceil(float(mag_cap)/float(rate_of_fire))
            rate = rate if rate <= 20 else 20
            return str(rate)

        return ""

    def __parse_name__(self, obj):

        name = "<unknown>"

        for key in obj:
            if "name" in key:
                name = obj[key]

        name = name.replace("¹", "")\
            .replace("²", "")\
            .replace("³", "")\
            .replace("⁵", "")\
            .replace("(GRA)", "")

        return text_util.remove_whitespace(name)

    def __parse_dmg__(self, obj):

        if "Damage per second" in obj:
            return float(obj["Damage per second"])

        dmg_per_shot = obj["Damage per shot"]

        if "+" in dmg_per_shot and not "x" in dmg_per_shot:
            return float(dmg_per_shot.split("+")[1])

        elif "x" in dmg_per_shot:
            # 1 +(75x6)
            start = dmg_per_shot.index("(")
            end = dmg_per_shot.index(")")
            sub = dmg_per_shot[start+1:end]
            comps = sub.split("x")
            return float(comps[0])*float(comps[1])

        else:
            return 0.0
