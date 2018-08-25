from Shared.Model import *
from Shared.Armory import *


def get_sprite_sheet_path(file_name):
    return os.path.join("Assets", "Graphics", "Models", file_name)


# --------------------- EMPIRE --------------------- #
EMPIRE_ARCHER_SPRITE_SHEET = get_sprite_sheet_path("archer_sprite_sheet.png")
EMPIRE_ARCHER_SIZE = (50 * 3, 37 * 3)
EMPIRE_SWORDSMAN_SPRITE_SHEET = get_sprite_sheet_path("warrior_sprite_sheet.png")
EMPIRE_SWORDSMAN_SIZE = (50 * 3, 37 * 3)

# --------------------- UNDEAD --------------------- #
UNDEAD_SKELETON_HALBERD_SPRITE_SHEET = get_sprite_sheet_path("skeleton_sprite_sheet.png")
UNDEAD_SKELETON_HALBERD_SIZE = (50 * 2, 37 * 2)


# --------------------- MONSTERS --------------------- #
SLIME_SPRITE_SHEET = get_sprite_sheet_path("slime_sprite_sheet.png")
SLIME_SIZE = (100 * 1, 74 * 1)


def get_empire_archer():

    return Model(sprite_sheet_file=EMPIRE_ARCHER_SPRITE_SHEET, size=EMPIRE_ARCHER_SIZE,
                 position=(0, 0), object_type=GameConstants.PLAYER_GAME_OBJECTS, model_type=MODEL_TYPE_RANGE,
                 name="Empire Archer", m=4, ws=3, bs=3, s=3, t=3, w=1, i=3, a=1, ld=7,
                 armor=None, weapon=get_weapon_bow(), shield=None)


def get_empire_swordsman():
    return Model(sprite_sheet_file=EMPIRE_SWORDSMAN_SPRITE_SHEET, size=EMPIRE_SWORDSMAN_SIZE,
                 position=(0, 0), object_type=GameConstants.PLAYER_GAME_OBJECTS, model_type=MODEL_TYPE_MELEE,
                 name="Empire Swordsman", m=4, ws=4, bs=3, s=3, t=3, w=1, i=3, a=1, ld=7,
                 armor=get_armor_light(),
                 weapon=get_weapon_sword(),
                 shield=get_shield())


def get_undead_skeleton_halberd():
    return Model(sprite_sheet_file=UNDEAD_SKELETON_HALBERD_SPRITE_SHEET,
                 size=UNDEAD_SKELETON_HALBERD_SIZE, position=(0, 0),
                 object_type=GameConstants.COMPUTER_GAME_OBJECTS, model_type=MODEL_TYPE_MELEE,
                 name="Undead Halberd", m=4, ws=2, bs=2, s=3, t=3, w=1, i=2, a=1, ld=3,
                 armor=None, weapon=get_weapon_halberd(), shield=None)


def get_slime_monster():

    return Model(sprite_sheet_file=SLIME_SPRITE_SHEET, size=SLIME_SIZE,
                 position=(0, 0), object_type=GameConstants.PLAYER_GAME_OBJECTS, model_type=MODEL_TYPE_MELEE,
                 name="Slime", m=4, ws=4, bs=3, s=3, t=3, w=1, i=3, a=1, ld=7)
