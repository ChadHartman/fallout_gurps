import math
import utils


# generated by utils.analyze_damages
__DAMAGES__ = [
    ("1d-2", 1.5),
    ("1d-1", 2.5),
    ("1d", 3.5),
    ("1d+1", 4.5),
    ("2d-2", 5.0),
    ("1d+2", 5.5),
    ("2d-1", 6.0),
    ("2d", 7.0),
    ("2d+1", 8.0),
    ("3d-2", 8.5),
    ("2d+2", 9.0),
    ("3d-1", 9.5),
    ("3d", 10.5),
    ("3d+1", 11.5),
    ("4d-2", 12.0),
    ("3d+2", 12.5),
    ("4d-1", 13.0),
    ("4d", 14.0),
    ("4d+1", 15.0),
    ("5d-2", 15.5),
    ("4d+2", 16.0),
    ("5d-1", 16.5),
    ("5d", 17.5),
    ("5d+1", 18.5),
    ("5d+2", 19.5),
    ("3dx2", 21.0),
    ("4dx2", 28.0),
    ("3dx3", 31.5),
    ("5dx2", 35.0),
    ("4dx3", 42.0),
    ("5dx3", 52.5)
]


class Damage(object):

    def __init__(self, obj):

        dmg = self.__convert_to_num__(
            utils.filter_unicode(obj["Damage per shot"]))

        rof = float(obj["Rate of fire"]) if "Rate of fire" in obj else 1.0
        rof = 1.0 if rof < 1.0 else rof

        # Gurps damge 1/10th of in game
        gurps_dmg = int(math.ceil(dmg * rof / 10.0))

        if gurps_dmg == 0:
            self.value = "0"
            return

        for d in __DAMAGES__:
            if d[1] > gurps_dmg:
                self.value = d[0]
                return

        self.value = str(gurps_dmg)

    def __convert_to_num__(self, value):
        if "(" in value:
            i = value.index("(")
            value = value[:i]
        elif "-" in value:
            i = value.index("-")
            value = value[:i]
        elif "/" in value:
            i = value.index("/")
            value = value[:i]

        value = value.replace(" ", "")

        damage = 0
        for n in value.split("+"):
            damage += int(n) if n.isdigit() else 0

        return damage

    def __str__(self):
        return self.value


class Weapon(object):
    """
    {
        'Rate of fire': '4',
        'Projectile explosive weapon name': 'Red Glare',
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
        self.damage = str(Damage(obj))
        self.ammo_type = obj["Ammunition used"] if "Ammunition used" in obj else ""
        self.weight = self.__parse_weight__(obj)
        self.cost = int(obj["Weapon value in caps"])
        self.skill_req = self.__parse_skill_req__(obj)
        self.str_req = self.__parse_str_req__(obj)
        self.aoe = self.__parse_aoe__(obj)
        self.skill = self.__parse_skill__(filepath)
        self.attacks_until_reload = self.__parse_aur__(obj)
        self.spread = float(obj["Weapon Spread"]
                            ) if "Weapon Spread" in obj else -1.0
        self.is_highlighted = obj["is_highlighted"] == "True"

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
        return int(math.ceil(max_weight * value / max_game_weight))

    def __parse_aoe__(self, obj):
        aoe = obj["AOE"] if "AOE" in obj else "0"
        value = 0 if"-" in aoe else float(aoe)

        # ranges 0 -> 1700
        # max 5

        max_range = 5
        max_game_aoe = 1700

        return int(math.ceil(max_range * value / max_game_aoe))

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
            return str(int(rate))

        return ""

    def __parse_name__(self, obj):

        name = "<unknown>"

        for key in obj:
            if "name" in key:
                name = obj[key]

        name = utils.filter_unicode(name).replace("(GRA)", "")

        return utils.remove_whitespace(name)
