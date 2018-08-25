# TODO: weapon need to be a GameObject
from Shared.AnimAttrObject import AnimAttrObject
from Shared.GameConstants import GameConstants


class Weapon(AnimAttrObject):

    def __init__(self, sprite_sheet_file, size=None, position=(0, 0), object_type=GameConstants.ALL_GAME_OBJECTS,
                 name="", m=0, ws=0, bs=0, s=0, t=0, w=0, i=0, a=0, ld=0,
                 to_hit_re_roll=0, wounds_bonus=0, armor_piercing=0, great_weapon=0, ranged_weapon=0):
        super(Weapon, self).__init__(sprite_sheet_file, size, position, object_type, name, m, ws, bs, s, t, w, i, a, ld)

        self.__to_hit_re_roll = to_hit_re_roll
        self.__wounds_bonus = wounds_bonus
        self.__armor_piercing = armor_piercing
        self.__great_weapon = great_weapon
        self.__ranged_weapon = ranged_weapon

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
