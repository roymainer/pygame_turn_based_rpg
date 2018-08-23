# TODO: weapon need to be a GameObject
import random
from Shared.Attibutes import Attributes


class Weapon:

    def __init__(self, name="", ws=0, bs=0, s=0, t=0, w=0, i=0, a=0, ld=0,
                 to_hit_re_roll=0, wounds_bonus=0, armor_piercing=0, great_weapon=0, ranged_weapon=0):
        self.__attributes = Attributes(name, ws, bs, s, t, w, i, a, ld)

        self.__to_hit_re_roll = to_hit_re_roll
        self.__wounds_bonus = wounds_bonus
        self.__armor_piercing = armor_piercing
        self.__great_weapon = great_weapon
        self.__ranged_weapon = ranged_weapon

    def get_name(self):
        return self.__attributes.get_name()

    def get_weapon_skill(self):
        return self.__attributes.get_weapon_skill()

    def get_ballistic_skill(self):
        return self.__attributes.get_ballistic_skill()

    def get_strength(self):
        return self.__attributes.get_strength()

    def get_wounds(self):
        return self.__attributes.get_wounds()

    def get_initiative(self):
        return self.__attributes.get_initiative()

    def get_attack(self):
        return self.__attributes.get_attack()

    def get_leadership(self):
        return self.__attributes.get_leadership()

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


# SWORD = Weapon(name="Sword", ws=0, bs=0, s=0, t=0, w=0, i=0, a=0, ld=0,
# to_hit_re_roll=0, wounds_bonus=0, armor_piercing=False, great_weapon=False, ranged_weapon=False)
WEAPON_NONE = Weapon(name="None")
SWORD = Weapon(name="Sword")
CLUB = Weapon(name="Club")
MACE = Weapon(name="Mace")
HALBERD = Weapon(name="Halberd", s=1, great_weapon=True)
GREAT_SWORD = Weapon(name="Great Sword", s=2, great_weapon=True)
BOW = Weapon("Bow", ranged_weapon=True)
HAND_WEAPON = random.choice([SWORD, CLUB, MACE])
