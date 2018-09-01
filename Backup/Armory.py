import random

from Shared.Armor import *
from Shared.Shield import Shield
from Shared.Weapon import *


# --------------------- ARMOR --------------------- #
# def get_armor_none(): return Armor(sprite_sheet_file=ARMOR_NONE_SPRITE_SHEET, name="None")


def get_light_armor(): return LightArmor()


def get_heavy_armor(): return HeavyArmor()


def get_chaos_armor(): return ChaosArmor()


def get_dragon_armor(): return DragonArmor()


# --------------------- SHIELDS --------------------- #
# def get_shield_none(): return Shield(sprite_sheet_file=SHIELD_NONE_SPRITE_SHEET, name="None")


def get_shield(): return Shield()


# --------------------- WEAPONS --------------------- #
# TODO: extend this option
def get_hand_weapon(): return random.choice([get_sword()])


def get_sword(): return Sword()


def get_mace(): return Mace()


def get_club(): return Club()


def get_halberd(): return Halberd()


def get_great_sword(): return GreatSword()


def get_bow(): return Bow()


# def get_pistol(): return Pistol()
