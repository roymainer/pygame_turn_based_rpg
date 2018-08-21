# TODO: need to be a GameObject
NAME = "Name",
ARMOR_RATING = "Armor Rating"  # the required d6 roll for armor save
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

NONE = {NAME: "None", ARMOR_RATING: 7, WS: 0, BS: 0, S: 0, T: 0, W: 0, I: 0, A: 0, LD: 0, TO_HIT_RE_ROLL: 0}
LIGHT_ARMOR = {NAME: "Light Armor", ARMOR_RATING: 6, WS: 0, BS: 0, S: 0, T: 0, W: 0, I: 0, A: 0, LD: 0, TO_HIT_RE_ROLL: 0}
HEAVY_ARMOR = {NAME: "Heavy Armor", ARMOR_RATING: 5, WS: 0, BS: 0, S: 0, T: 0, W: 0, I: 0, A: 0, LD: 0, TO_HIT_RE_ROLL: 0}
CHAOS_ARMOR = {NAME: "Chaos Armor", ARMOR_RATING: 5, WS: 0, BS: 0, S: 0, T: 0, W: 0, I: 0, A: 0, LD: 0, TO_HIT_RE_ROLL: 0}
DRAGON_ARMOR = {NAME: "Dragon Armor", ARMOR_RATING: 5, WS: 0, BS: 0, S: 0, T: 0, W: 0, I: 0, A: 0, LD: 0, TO_HIT_RE_ROLL: 0}


class Armor:

    def __init__(self, attributes):

        self.__name = attributes[NAME]
        self.__armor_rating = attributes[ARMOR_RATING]
        self.__WS = attributes[WS]
        self.__BS = attributes[BS]
        self.__S = attributes[S]
        self.__W = attributes[W]
        self.__I = attributes[I]
        self.__A = attributes[A]
        self.__to_hit_re_roll = attributes[TO_HIT_RE_ROLL]

    def get_name(self):
        return self.__name

    def get_armor_rating(self):
        return self.__armor_rating

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

    def get_leadership(self):
        return self.__L

    def get_to_hit_re_roll(self):
        return self.__to_hit_re_roll

