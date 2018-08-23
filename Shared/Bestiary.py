import os

from Shared.Model import *
from Shared.Shield import *
from Shared.Weapon import *


def get_sprite_sheet_path(file_name):
    return os.path.join("Assets", "Graphics", "Units", file_name)


def get_empire_archer():
    __EMPIRE_ARCHER_SPRITE_SHEET = get_sprite_sheet_path("archer_sprite_sheet.png")
    __EMPIRE_ARCHER_SIZE = (50 * 3, 37 * 3)
    __EMPIRE_ARCHER_ATTRIBUTES = Attributes(name="Empire Archer", m=4, ws=3, bs=3, s=3, t=3, w=1, i=3, a=1, ld=7)
    return Model(sprite_sheet_file=__EMPIRE_ARCHER_SPRITE_SHEET, size=__EMPIRE_ARCHER_SIZE,
                 position=(0, 0), object_type=GameConstants.PLAYER_GAME_OBJECTS, model_type=MODEL_TYPE_RANGE,
                 attributes=__EMPIRE_ARCHER_ATTRIBUTES, armor=ARMOR_NONE, weapon=BOW, shield=SHIELD_NONE)


def get_empire_swordsman():
    __EMPIRE_SWORDSMAN_SPRITE_SHEET = get_sprite_sheet_path("warrior_sprite_sheet.png")
    __EMPIRE_SWORDSMAN_SIZE = (50 * 3, 37 * 3)
    __EMPIRE_SWORDSMAN_ATTRIBUTES = Attributes(name="Empire Swordsman", m=4, ws=4, bs=3, s=3, t=3, w=1, i=3, a=1, ld=7)
    return Model(sprite_sheet_file=__EMPIRE_SWORDSMAN_SPRITE_SHEET, size=__EMPIRE_SWORDSMAN_SIZE,
                 position=(0, 0), object_type=GameConstants.PLAYER_GAME_OBJECTS, model_type=MODEL_TYPE_MELEE,
                 attributes=__EMPIRE_SWORDSMAN_ATTRIBUTES, armor=LIGHT_ARMOR, weapon=BOW, shield=SHIELD)


def get_undead_skeleton_halberd():
    __UNDEAD_SKELETON_HALBERD_SPRITE_SHEET = get_sprite_sheet_path("skeleton_sprite_sheet.png")
    __UNDEAD_SKELETON_HALBERD_SIZE = (50 * 2, 37 * 2)
    __UNDEAD_SKELETON_HALBERD_ATTRIBUTES = Attributes(name="Undead Halberd", m=4, ws=2, bs=2, s=3, t=3, w=1, i=2, a=1,
                                                      ld=3)
    return Model(sprite_sheet_file=__UNDEAD_SKELETON_HALBERD_SPRITE_SHEET,
                 size=__UNDEAD_SKELETON_HALBERD_SIZE, position=(0, 0),
                 object_type=GameConstants.COMPUTER_GAME_OBJECTS, model_type=MODEL_TYPE_MELEE,
                 attributes=__UNDEAD_SKELETON_HALBERD_ATTRIBUTES, armor=ARMOR_NONE, weapon=HALBERD,
                 shield=SHIELD_NONE)


def get_slime_monster():
    __SLIME_SPRITE_SHEET = get_sprite_sheet_path("slime_sprite_sheet.png")
    __SLIME_SIZE = (100 * 1, 74 * 1)
    __SLIME_ATTRIBUTES = Attributes(name="Slime", m=4, ws=4, bs=3, s=3, t=3, w=1, i=3, a=1, ld=7)
    return Model(sprite_sheet_file=__SLIME_SPRITE_SHEET, size=__SLIME_SIZE,
                 position=(0, 0), object_type=GameConstants.PLAYER_GAME_OBJECTS, model_type=MODEL_TYPE_MELEE,
                 attributes=__SLIME_ATTRIBUTES, armor=ARMOR_NONE, weapon=WEAPON_NONE, shield=SHIELD_NONE)
