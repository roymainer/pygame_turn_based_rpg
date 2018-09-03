import random

from Shared.Action import Attack, RangeAttack
from Shared.GameConstants import GameConstants
from Shared.Attributes import Attributes
from Shared.SpecialRule import AlwaysStrikesLast


class Weapon(Attributes):

    def __init__(self, name="", m=0, ws=0, bs=0, s=0, t=0, w=0, i=0, a=0, ld=0,
                 to_hit_re_roll=0, wounds_bonus=0, armor_piercing=False, great_weapon=False, ranged_weapon=False):
        super(Weapon, self).__init__(name, m, ws, bs, s, t, w, i, a, ld)

        self.__to_hit_re_roll = to_hit_re_roll
        self.__wounds_bonus = wounds_bonus
        self.__armor_piercing = armor_piercing
        self.__great_weapon = great_weapon
        self.__ranged_weapon = ranged_weapon

    def get_to_hit_re_roll(self) -> bool:
        # if the weapon grants a re-roll bonus to hit
        return self.__to_hit_re_roll

    def get_to_wound(self) -> int:
        # if the weapon grants a wounds bonus
        return self.__wounds_bonus

    def is_armor_piercing(self) -> bool:
        return self.__armor_piercing

    def is_great_weapon(self) -> bool:
        return self.__great_weapon

    def is_ranged_weapon(self) -> bool:
        return self.__ranged_weapon

    def get_action(self):
        if self.__ranged_weapon:
            return RangeAttack()
        return Attack()

    def get_valid_targets(self, model) -> int:

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


class RangeWeapon(Weapon):
    def __init__(self, name="", m=0, ws=0, bs=0, s=0, t=0, w=0, i=0, a=0, ld=0,
                 to_hit_re_roll=0, wounds_bonus=0, armor_piercing=False):
        super(RangeWeapon, self).__init__(name, m, ws, bs, s, t, w, i, a, ld, to_hit_re_roll, wounds_bonus,
                                          armor_piercing, great_weapon=False, ranged_weapon=True)

    def get_valid_targets(self, model):
        targets = GameConstants.TARGET_PLAYER_SINGLE_ANY
        if targets is not None and model.get_type() == GameConstants.PLAYER_GAME_OBJECTS:
            # add offset to return computer models as targets
            targets += (GameConstants.TARGET_COMPUTER_SINGLE_ANY - GameConstants.TARGET_PLAYER_SINGLE_ANY)
        return targets


def get_hand_weapon():
    return random.choice([Sword()])


class Sword(Weapon):
    def __init__(self):
        super(Sword, self).__init__(name="Sword")


class Mace(Weapon):
    def __init__(self):
        super(Mace, self).__init__(name="Mace")


class Club(Weapon):
    def __init__(self):
        super(Club, self).__init__(name="Mace")


class Halberd(Weapon):
    def __init__(self):
        super(Halberd, self).__init__(name="Halberd", s=1, great_weapon=True)


class GreatSword(Weapon):
    def __init__(self):
        super(GreatSword, self).__init__(name="Great Sword", s=2, great_weapon=True)
        self.add_special_rule(AlwaysStrikesLast)


class Bow(RangeWeapon):
    def __init__(self):
        super(Bow, self).__init__(name="Bow")
        
        
class Pistol(RangeWeapon):
    def __init__(self):
        super(Pistol, self).__init__(name="Pistol", s=4, armor_piercing=True)

