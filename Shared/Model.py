"""
Character class is an extension of the AnimatedObject class
it supports more actions (animations), character attributes and sounds (need to add)
Required Actions:
idle
attack / shoot / cast
items
die
"""

from Shared.AnimatedObject import AnimatedObject
from Shared.Armor import *
from Shared.GameConstants import GameConstants
from Shared.Shield import *
from Shared.Weapon import *

SPRITE_SHEET = "Sprite_Sheet"
SIZE = "Size"

MODEL_TYPE_MELEE = 0
MODEL_TYPE_RANGE = 1
MODEL_TYPE_MAGIC = 2

ACTION_ATTACK = "Attack"
ACTION_SKILLS = "Skills"
ACTION_ITEMS = "Items"
ACTION_MAGIC = "Magic"


def get_model_actions(model):
    model_type = model.get_model_type()
    if model_type == MODEL_TYPE_MELEE:
        return [ACTION_ATTACK, ACTION_SKILLS, ACTION_ITEMS]
    if model_type == MODEL_TYPE_RANGE:
        return [ACTION_ATTACK, ACTION_SKILLS, ACTION_ITEMS]
    if model_type == MODEL_TYPE_MAGIC:
        return [ACTION_ATTACK, ACTION_MAGIC, ACTION_SKILLS, ACTION_ITEMS]
    return


class Model(AnimatedObject):
    # TODO: add wards and inventory
    def __init__(self, sprite_sheet_file, size, position, object_type, model_type, attributes: Attributes,
                 armor=ARMOR_NONE, weapon=HAND_WEAPON, shield=SHIELD_NONE):
        sprite_sheet_file = sprite_sheet_file
        size = size
        super(Model, self).__init__(sprite_sheet_file, size, position, object_type)

        self.set_action("idle")  # every character must have idle stance!
        self.__model_type = model_type

        # TODO: instead of loading from a py file need to load from an encrypted file
        self.__attributes = attributes
        self.__current_wounds = self.__attributes.get_wounds()

        self.__armor = armor
        self.__weapon = weapon
        self.__shield = shield
        # self.__wards = None
        # self.__inventory = None

    def __repr__(self):
        return "Character"

    def get_name(self):
        return self.__attributes.get_name()

    def get_move(self):
        return self.__attributes.get_move()

    def get_weapon_skill(self):
        return self.__attributes.get_weapon_skill()

    def get_ballistic_skill(self):
        return self.__attributes.get_ballistic_skill()

    def get_strength(self):
        return self.__attributes.get_strength()

    def get_toughness(self):
        return self.__attributes.get_toughness()

    def set_wounds(self, wounds):
        self.__current_wounds = wounds

    def get_wounds(self):
        return self.__current_wounds

    def get_max_wounds(self):
        return self.__attributes.get_wounds()

    def get_initiative(self):
        return self.__attributes.get_initiative()

    def get_attacks(self):
        return self.__attributes.get_attack()

    def get_leadership(self):
        return self.__attributes.get_leadership()

    def set_armor(self, armor):
        self.__armor = armor

    def get_armor(self):
        # return self.__attributes[Bestiary.ARMOR]
        return self.__armor

    def set_weapon(self, weapon):
        self.__weapon = weapon

    def get_weapon(self):
        return self.__weapon

    def set_shield(self, shield):
        self.__shield = shield

    def get_shield(self):
        return self.__shield

    def get_model_type(self):
        return self.__model_type

    def is_front_row(self):
        position = self.get_position()
        if position[0] == GameConstants.PLAYERS_FRONT_COLUMN or position[0] == GameConstants.COMPUTER_FRONT_COLUMN:
            return True
        else:
            return False

    def is_killed(self):
        return self.get_wounds() <= 0
