# TODO: weapon need to be a GameObject
import os
from Shared.Action import Attack, RangeAttack
from Shared.AnimAttrObject import AnimAttrObject
from Shared.GameConstants import GameConstants
from Shared.SpecialRule import AlwaysStrikesLast


def get_sprite_sheet_path(file_name):
    return os.path.join("Assets", "Graphics", "Armory", file_name)


# WEAPON_NONE_SPRITE_SHEET = None
SWORD_SPRITE_SHEET = get_sprite_sheet_path("weapon_sword_sprite_sheet.png")
MACE_SPRITE_SHEET = get_sprite_sheet_path("weapon_mace_sprite_sheet.png")
CLUB_SPRITE_SHEET = get_sprite_sheet_path("weapon_club_sprite_sheet.png")
HALBERD_SPRITE_SHEET = get_sprite_sheet_path("weapon_halberd_sprite_sheet.png")
GREAT_SWORD_SPRITE_SHEET = get_sprite_sheet_path("weapon_great_sword_sprite_sheet.png")
BOW_SPRITE_SHEET = get_sprite_sheet_path("weapon_bow_sprite_sheet.png")


class AnimatedWeapon(AnimAttrObject):

    def __init__(self, sprite_sheet_file, size=None, position=(0, 0), object_type=GameConstants.ALL_GAME_OBJECTS,
                 name="", m=0, ws=0, bs=0, s=0, t=0, w=0, i=0, a=0, ld=0,
                 to_hit_re_roll=0, wounds_bonus=0, armor_piercing=False, great_weapon=False, ranged_weapon=False):
        super(AnimatedWeapon, self).__init__(sprite_sheet_file, size, position, object_type,
                                             name, m, ws, bs, s, t, w, i, a, ld)

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

    def get_action(self):
        if self.__ranged_weapon:
            return RangeAttack()
        return Attack()

    def get_valid_targets(self, model):

        if model.is_front_row():
            if self.__great_weapon:
                # front row models with great weapons can hit any single enemy model
                targets = GameConstants.TARGET_PLAYER_SINGLE_ANY
            else:
                # front row models with smaller weapons can only hit the front row
                targets = GameConstants.TARGET_PLAYER_SINGLE_FRONT
        else:
            if self.__great_weapon:
                # back row models with great weapons can hit enemy models at the front row
                targets = GameConstants.TARGET_PLAYER_SINGLE_FRONT
            else:
                targets = None

        if targets is not None and model.get_type() == GameConstants.PLAYER_GAME_OBJECTS:
            # add offset to return computer models as targets
            targets += (GameConstants.TARGET_COMPUTER_SINGLE_ANY - GameConstants.TARGET_PLAYER_SINGLE_ANY)

        return targets


class RangeWeapon(AnimatedWeapon):
    def __init__(self, sprite_sheet_file, size=None, position=(0, 0), object_type=GameConstants.ALL_GAME_OBJECTS,
                 name="", m=0, ws=0, bs=0, s=0, t=0, w=0, i=0, a=0, ld=0,
                 to_hit_re_roll=0, wounds_bonus=0, armor_piercing=False):
        super(RangeWeapon, self).__init__(sprite_sheet_file, size, position, object_type,
                                          name, m, ws, bs, s, t, w, i, a, ld,
                                          to_hit_re_roll, wounds_bonus, armor_piercing, great_weapon=False,
                                          ranged_weapon=True)

    def get_valid_targets(self, model):
        targets = GameConstants.TARGET_PLAYER_SINGLE_ANY
        if targets is not None and model.get_type() == GameConstants.PLAYER_GAME_OBJECTS:
            # add offset to return computer models as targets
            targets += (GameConstants.TARGET_COMPUTER_SINGLE_ANY - GameConstants.TARGET_PLAYER_SINGLE_ANY)
        return targets


class Sword(AnimatedWeapon):
    def __init__(self):
        super(Sword, self).__init__(sprite_sheet_file=SWORD_SPRITE_SHEET, name="Sword")


class Mace(AnimatedWeapon):
    def __init__(self):
        super(Mace, self).__init__(sprite_sheet_file=MACE_SPRITE_SHEET, name="Mace")


class Club(AnimatedWeapon):
    def __init__(self):
        super(Club, self).__init__(sprite_sheet_file=CLUB_SPRITE_SHEET, name="Mace")


class Halberd(AnimatedWeapon):
    def __init__(self):
        super(Halberd, self).__init__(sprite_sheet_file=HALBERD_SPRITE_SHEET, name="Halberd", s=1, great_weapon=True)


class GreatSword(AnimatedWeapon):
    def __init__(self):
        super(GreatSword, self).__init__(sprite_sheet_file=GREAT_SWORD_SPRITE_SHEET, name="Great Sword", s=2,
                                         great_weapon=True, special_rules=AlwaysStrikesLast)


class Bow(RangeWeapon):
    def __init__(self):
        super(Bow, self).__init__(sprite_sheet_file=BOW_SPRITE_SHEET, name="Bow")
