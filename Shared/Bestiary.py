import os

UNIT_TYPE_MELEE = 0
UNIT_TYPE_RANGE = 1
UNIT_TYPE_MAGIC = 2

ACTION_ATTACK = "Attack"
ACTION_SKILLS = "Skills"
ACTION_ITEMS = "Items"
ACTION_MAGIC = "Magic"

"""Armor types"""
ARMOR_NONE = "None"
ARMOR_LIGHT = "Light Armor"
ARMOR_LIGHT_AND_SHIELD = "Light Armor and Shield"
ARMOR_HEAVY = "Heavy Armor"
ARMOR_HEAVY_AND_SHIELD = "Heavy Armor and Shield"

""" Ward types """
WARD_NONE = "None"
WARD_SHIELD_ENCHANTED = "Enchanted Shield"
WARD_SHIELD_CHARMED = "Charmed Shield"
WARD_SHIELD_SPELL = "Spell Shield"
WARD_ARMOR_SCALES_GLITTERING = "Glittering Scales"
WARD_TALISMAN_OF_PRESERVATION = "Talisman of Preservation"
WARD_TALISMAN_OF_ENDURANCE = "Talisman of Endurance"
WARD_TALISMAN_OF_PROTECTION = "Talisman of Protection"


def get_sprite_sheet_path(file_name):
    return os.path.join("Assets", "Graphics", "Characters", file_name)


def get_unit_actions(unit):
    unit_type = unit.get_unit_type()
    if unit_type == UNIT_TYPE_MELEE:
        return [ACTION_ATTACK, ACTION_SKILLS, ACTION_ITEMS]
    if unit_type == UNIT_TYPE_RANGE:
        return [ACTION_ATTACK, ACTION_SKILLS, ACTION_ITEMS]
    if unit_type == UNIT_TYPE_MAGIC:
        return [ACTION_ATTACK, ACTION_MAGIC, ACTION_SKILLS, ACTION_ITEMS]
    return


class Bestiary:

    NAME = "Name",
    UNIT_TYPE = "Unit_Type"
    M = "M"
    WS = "WS"
    BS = "BS"
    S = "S"
    T = "T"
    W = "W"
    I = "I"
    A = "A"
    LD = "LD"
    ARMOR = "ARMOR"
    WARD = "WARD"

    SPRITE_SHEET = "Sprite_Sheet"
    SIZE = "Size"

    ARCHER = {NAME: "Archer", UNIT_TYPE: UNIT_TYPE_RANGE,
              M: 5, WS: 4, BS: 5, S: 3, T: 3, W: 1, I: 5, A: 1, LD: 8,
              ARMOR: ARMOR_NONE,
              WARD: [WARD_NONE],  # there can always be more than one ward
              SPRITE_SHEET: get_sprite_sheet_path("adventurer_sprite_sheet.png"),
              SIZE: (50 * 3, 37 * 3)}
    WARRIOR = {NAME: "Warrior", UNIT_TYPE: UNIT_TYPE_MELEE,
               M: 5, WS: 4, BS: 5, S: 3, T: 3, W: 1, I: 5, A: 1, LD: 8,
               # M: 5, WS: 9, BS: 5, S: 9, T: 3, W: 1, I: 5, A: 9, LD: 8,
               ARMOR: ARMOR_LIGHT,
               WARD: [WARD_NONE],
               SPRITE_SHEET: get_sprite_sheet_path("dark_sprite_sheet.png"),
               SIZE: (50 * 3, 37 * 3)}
    DWARF_MINER = {NAME: "Miner", UNIT_TYPE: UNIT_TYPE_MELEE,
                   M: 3, WS: 4, BS: 3, S: 3, T: 4, W: 1, I: 2, A: 1, LD: 9,
                   ARMOR: ARMOR_NONE,
                   WARD: [WARD_NONE],
                   SPRITE_SHEET: get_sprite_sheet_path("dark_sprite_sheet.png"),
                   SIZE: (50 * 3, 37 * 3)}
    SLIME = {NAME: "Slime", UNIT_TYPE: UNIT_TYPE_MELEE,
             M: 5, WS: 3, BS: 3, S: 3, T: 3, W: 1, I: 4, A: 1, LD: 5,
             ARMOR: ARMOR_NONE,
             WARD: [WARD_NONE],
             SPRITE_SHEET: get_sprite_sheet_path("slime_sprite_sheet.png"),
             SIZE: (100 * 1, 74 * 1)}
    SKELETON = {NAME: "Skeleton", UNIT_TYPE: UNIT_TYPE_MELEE,
                M: 4, WS: 2, BS: 2, S: 3, T: 3, W: 1, I: 2, A: 1, LD: 3,
                ARMOR: ARMOR_NONE,
                WARD: [WARD_NONE],
                SPRITE_SHEET: get_sprite_sheet_path("skeleton_sprite_sheet.png"),
                SIZE: (50 * 2, 37 * 2)}
