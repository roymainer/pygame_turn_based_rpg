import os
import random

from Shared.Armor import Armor
from Shared.Shield import Shield
from Shared.Weapon import Weapon


def get_sprite_sheet_path(file_name):
    return os.path.join("Assets", "Graphics", "Armory", file_name)


def __get_random_shield():
    return random.choice([SHIELD0_SPRITE_SHEET, SHIELD1_SPRITE_SHEET, SHIELD2_SPRITE_SHEET,
                          SHIELD3_SPRITE_SHEET])


# ARMOR_NONE_SPRITE_SHEET = None
LIGHT_ARMOR_SPRITE_SHEET = get_sprite_sheet_path("armor_light_sprite_sheet.png")
HEAVY_ARMOR_SPRITE_SHEET = get_sprite_sheet_path("armor_heavy_sprite_sheet.png")
CHAOS_ARMOR_SPRITE_SHEET = get_sprite_sheet_path("armor_chaos_sprite_sheet.png")
DRAGON_ARMOR_SPRITE_SHEET = get_sprite_sheet_path("armor_dragon_sprite_sheet.png")

# SHIELD_NONE_SPRITE_SHEET = None
SHIELD0_SPRITE_SHEET = get_sprite_sheet_path("shield0_sprite_sheet.png")
SHIELD1_SPRITE_SHEET = get_sprite_sheet_path("shield1_sprite_sheet.png")
SHIELD2_SPRITE_SHEET = get_sprite_sheet_path("shield2_sprite_sheet.png")
SHIELD3_SPRITE_SHEET = get_sprite_sheet_path("shield3_sprite_sheet.png")

# WEAPON_NONE_SPRITE_SHEET = None
WEAPON_SWORD_SPRITE_SHEET = get_sprite_sheet_path("weapon_sword_sprite_sheet.png")
WEAPON_MACE_SPRITE_SHEET = get_sprite_sheet_path("weapon_mace_sprite_sheet.png")
WEAPON_CLUB_SPRITE_SHEET = get_sprite_sheet_path("weapon_club_sprite_sheet.png")
WEAPON_HALBERD_SPRITE_SHEET = get_sprite_sheet_path("weapon_halberd_sprite_sheet.png")
WEAPON_GREAT_SWORD_SPRITE_SHEET = get_sprite_sheet_path("weapon_great_sword_sprite_sheet.png")
WEAPON_BOW_SPRITE_SHEET = get_sprite_sheet_path("weapon_bow_sprite_sheet.png")


# --------------------- ARMOR --------------------- #
# def get_armor_none(): return Armor(sprite_sheet_file=ARMOR_NONE_SPRITE_SHEET, name="None")


def get_armor_light(): return Armor(sprite_sheet_file=LIGHT_ARMOR_SPRITE_SHEET, name="Light Armor",
                                    req_roll=6)


def get_armor_heavy(): return Armor(sprite_sheet_file=HEAVY_ARMOR_SPRITE_SHEET, name="Heavy Armor",
                                    req_roll=5)


def get_armor_chaos(): return Armor(sprite_sheet_file=CHAOS_ARMOR_SPRITE_SHEET, name="Chaos Armor",
                                    req_roll=5)


def get_armor_dragon(): return Armor(sprite_sheet_file=DRAGON_ARMOR_SPRITE_SHEET, name="Dragon Armor",
                                     req_roll=5)


# --------------------- SHIELDS --------------------- #
# def get_shield_none(): return Shield(sprite_sheet_file=SHIELD_NONE_SPRITE_SHEET, name="None")


def get_shield(): return Shield(sprite_sheet_file=__get_random_shield(), name="Shield", save_modifier=-1)


# --------------------- WEAPONS --------------------- #
# def get_weapon_none(): return Weapon(sprite_sheet_file=WEAPON_NONE_SPRITE_SHEET, name="None")


def get_weapon_sword(): return Weapon(sprite_sheet_file=WEAPON_SWORD_SPRITE_SHEET, name="Sword")


def get_weapon_mace(): return Weapon(sprite_sheet_file=WEAPON_MACE_SPRITE_SHEET, name="Mace")


def get_weapon_club(): return Weapon(sprite_sheet_file=WEAPON_CLUB_SPRITE_SHEET, name="Club")


def get_weapon_halberd(): return Weapon(sprite_sheet_file=WEAPON_HALBERD_SPRITE_SHEET, name="Halberd",
                                        s=2, armor_piercing=True, great_weapon=True)


def get_weapon_great_sword(): return Weapon(sprite_sheet_file=WEAPON_GREAT_SWORD_SPRITE_SHEET, name="Great Sword",
                                            s=2, armor_piercing=2, great_weapon=True)


def get_weapon_bow(): return Weapon(sprite_sheet_file=WEAPON_BOW_SPRITE_SHEET, name="Bow", ranged_weapon=True)
