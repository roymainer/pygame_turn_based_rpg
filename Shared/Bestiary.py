import os


def get_sprite_sheet_path(file_name):
    return os.path.join("Assets", "Graphics", "Characters", file_name)


def get_unit_actions(unit):
    unit_type = unit.get_unit_type()
    if unit_type == Bestiary.UNIT_TYPE_MELEE:
        return ["Attack", "Skills", "Items"]
    if unit_type == Bestiary.UNIT_TYPE_RANGE:
        return ["Attack", "Skills", "Items"]
    return


class Bestiary:

    UNIT_TYPE_MELEE = 0
    UNIT_TYPE_RANGE = 1

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

    SPRITE_SHEET = "Sprite_Sheet"
    SIZE = "Size"

    ARCHER = {NAME: "Archer", UNIT_TYPE: UNIT_TYPE_RANGE,
              M: 5, WS: 4, BS: 5, S: 3, T: 3, W: 1, I: 5, A: 1, LD: 8,
              SPRITE_SHEET: get_sprite_sheet_path("adventurer_sprite_sheet.png"),
              SIZE: (50 * 3, 37 * 3)}
    WARRIOR = {NAME: "Warrior", UNIT_TYPE: UNIT_TYPE_RANGE,
               M: 5, WS: 4, BS: 5, S: 3, T: 3, W: 1, I: 5, A: 1, LD: 8,
               SPRITE_SHEET: get_sprite_sheet_path("dark_sprite_sheet.png"),
               SIZE: (50 * 3, 37 * 3)}
    DWARF_MINER = {NAME: "Miner", UNIT_TYPE: UNIT_TYPE_MELEE,
                   M: 3, WS: 4, BS: 3, S: 3, T: 4, W: 1, I: 2, A: 1, LD: 9,
                   SPRITE_SHEET: get_sprite_sheet_path("dark_sprite_sheet.png"),
                   SIZE: (50 * 3, 37 * 3)}
    SLIME = {NAME: "Slime", UNIT_TYPE: UNIT_TYPE_MELEE,
             M: 5, WS: 3, BS: 3, S: 3, T: 3, W: 1, I: 4, A: 1, LD: 5,
             SPRITE_SHEET: get_sprite_sheet_path("slime_sprite_sheet.png"),
             SIZE: (100 * 1, 74 * 1)}
