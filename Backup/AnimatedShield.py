import os
import random
from Shared.AnimAttrObject import AnimAttrObject
from Shared.GameConstants import GameConstants


def get_sprite_sheet_path(file_name):
    return os.path.join("Assets", "Graphics", "Armory", file_name)


# SHIELD_NONE_SPRITE_SHEET = None
SHIELD0_SPRITE_SHEET = get_sprite_sheet_path("shield_sprite_sheet.png")
SHIELD1_SPRITE_SHEET = get_sprite_sheet_path("shield1_sprite_sheet.png")
SHIELD2_SPRITE_SHEET = get_sprite_sheet_path("shield2_sprite_sheet.png")
SHIELD3_SPRITE_SHEET = get_sprite_sheet_path("shield3_sprite_sheet.png")


def get_random_shield_sprite_sheet():
    return random.choice([SHIELD0_SPRITE_SHEET])


class AnimGenericShield(AnimAttrObject):

    def __init__(self, sprite_sheet_file=None, size=None, position=(0, 0), object_type=GameConstants.ALL_GAME_OBJECTS,
                 name="Shield", m=0, ws=0, bs=0, s=0, t=0, w=0, i=0, a=0, ld=0, save_modifier=-1, to_hit_re_roll=0):
        super(AnimGenericShield, self).__init__(sprite_sheet_file, size, position, object_type,
                                                name, m, ws, bs, s, t, w, i, a, ld)

        self.__save_modifier = save_modifier
        self.__to_hit_re_roll = to_hit_re_roll

    def get_shield_save_modifier(self):
        return self.__save_modifier

    def get_to_hit_re_roll(self):
        # if the weapon grants a re-roll bonus to hit
        return self.__to_hit_re_roll


class AnimShield(AnimGenericShield):

    def __init__(self):
        super(AnimShield, self).__init__(get_random_shield_sprite_sheet())
