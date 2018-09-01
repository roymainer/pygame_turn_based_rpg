import os
from Shared.GameConstants import GameConstants
from Shared.AnimAttrObject import AnimAttrObject


def get_sprite_sheet_path(file_name):
    return os.path.join("Assets", "Graphics", "Armory", file_name)


# ARMOR_NONE_SPRITE_SHEET = None
LIGHT_ARMOR_SPRITE_SHEET = get_sprite_sheet_path("armor_light_sprite_sheet.png")
HEAVY_ARMOR_SPRITE_SHEET = get_sprite_sheet_path("armor_heavy_sprite_sheet.png")
CHAOS_ARMOR_SPRITE_SHEET = get_sprite_sheet_path("armor_chaos_sprite_sheet.png")
DRAGON_ARMOR_SPRITE_SHEET = get_sprite_sheet_path("armor_dragon_sprite_sheet.png")


class AnimArmor(AnimAttrObject):

    def __init__(self, sprite_sheet_file, size=None, position=(0, 0), object_type=GameConstants.ALL_GAME_OBJECTS,
                 name="", m=0, ws=0, bs=0, s=0, t=0, w=0, i=0, a=0, ld=0, req_roll=7, to_hit_re_roll=0):
        super(AnimArmor, self).__init__(sprite_sheet_file, size, position, object_type,
                                        name, m, ws, bs, s, t, w, i, a, ld)

        self.__armor_save_req_roll = req_roll
        self.__to_hit_re_roll = to_hit_re_roll

    def get_required_roll(self):
        return self.__armor_save_req_roll

    def get_to_hit_re_roll(self):
        # if the weapon grants a re-roll bonus to hit
        return self.__to_hit_re_roll


class LightArmor(AnimArmor):
    def __init__(self):
        super(LightArmor, self).__init__(sprite_sheet_file=LIGHT_ARMOR_SPRITE_SHEET, name="Light Armor", req_roll=6)


class HeavyArmor(AnimArmor):
    def __init__(self):
        super(HeavyArmor, self).__init__(sprite_sheet_file=HEAVY_ARMOR_SPRITE_SHEET, name="Heavy Armor", req_roll=6)


class ChaosArmor(AnimArmor):
    def __init__(self):
        super(ChaosArmor, self).__init__(sprite_sheet_file=CHAOS_ARMOR_SPRITE_SHEET, name="Chaos Armor", req_roll=6)


class DragonArmor(AnimArmor):
    def __init__(self):
        super(DragonArmor, self).__init__(sprite_sheet_file=DRAGON_ARMOR_SPRITE_SHEET, name="Dragon Armor", req_roll=6)
