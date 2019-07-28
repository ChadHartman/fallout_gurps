
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
        self.ammo_type = obj["Ammunition used"] if "Ammunition used" in obj else None
        self.weight = obj["Weapon weight"]
        self.cost = obj["Weapon value in caps"]
        self.skill_required = obj["Skill required"]
        self.str_req = obj["Strength required"]
        self.aoe = obj["AOE"] if "AOE" in obj else "0"
        self.skill = filepath.split("/")[-1].split("-")[0]
        self.attacks_until_reload = self.__parse_aur__(obj)

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
            return float(mag_cap)/float(rate_of_fire)

        return None

    def __parse_name__(self, obj):

        for key in obj:
            if "name" in key:
                return obj[key]

        return "<unknown>"

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
