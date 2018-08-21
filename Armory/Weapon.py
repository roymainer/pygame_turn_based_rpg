# TODO: weapon need to be a GameObject
NAME = "Name",
M = "M"
WS = "WS"
BS = "BS"
S = "S"
T = "T"
W = "W"
I = "I"
A = "A"
LD = "LD"
TO_HIT_RE_ROLL = "To hit re-roll"
WOUNDS_BONUS = "Wounds bonus"
ARMOR_PIERCING = "Armor Piercing"
GREAT_WEAPON = "Great Weapon"
RANGED_WEAPON = "Ranged Weapon"


class Weapon:

    def __init__(self, weapon_attributes):

        self.__name = weapon_attributes[NAME]
        self.__WS = weapon_attributes[WS]
        self.__BS = weapon_attributes[BS]
        self.__S = weapon_attributes[S]
        self.__W = weapon_attributes[W]
        self.__I = weapon_attributes[I]
        self.__A = weapon_attributes[A]
        self.__LD = weapon_attributes[LD]
        self.__to_hit_re_roll = weapon_attributes[TO_HIT_RE_ROLL]
        self.__wounds_bonus = weapon_attributes[WOUNDS_BONUS]
        self.__armor_piercing = weapon_attributes[ARMOR_PIERCING]
        self.__great_weapon = weapon_attributes[GREAT_WEAPON]  # great weapon can reach the back row
        self.__ranged_weapon = weapon_attributes[RANGED_WEAPON]

    def get_name(self):
        return self.__name

    def get_weapon_skill(self):
        return self.__WS

    def get_ballistic_skill(self):
        return self.__BS

    def get_strength(self):
        return self.__S

    def get_wounds(self):
        return self.__W

    def get_initiative(self):
        return self.__I

    def get_attack(self):
        return self.__A

    def get_leadership(self):
        return self.__LD

    def get_to_hit_re_roll(self):
        # if the weapon grants a re-roll bonus to hit
        return self.__to_hit_re_roll

    def get_to_wound(self):
        # if the weapon grants a wounds bonus
        return self.__wounds_bonus

    def is_armor_piercing(self):
        return self.__armor_piercing

    def is_great_weapon(self):
        return self.__great_weapon

    def is_ranged_weapon(self):
        return self.__ranged_weapon
