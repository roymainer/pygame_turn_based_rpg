"""
Character class is an extension of the AnimatedObject class
it supports more actions (animations), character attributes and sounds (need to add)
Required Actions:
idle
attack / shoot / cast
items
die
"""
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


class Model(AnimAttrObject):
    # TODO: add wards and inventory
    # TODO: instead of loading from a py file need to load from an encrypted file
    def __init__(self, sprite_sheet_file, size, position, object_type, model_type,
                 name="", m=0, ws=0, bs=0, s=0, t=0, w=0, i=0, a=0, ld=0,
                 armor=None, weapon=None, shield=None):
        super(Model, self).__init__(sprite_sheet_file, size, position, object_type, name, m, ws, bs, s, t, w, i, a, ld)

        self.__model_type = model_type
        self.__armor = armor
        self.__weapon = weapon
        self.__shield = shield
        # self.__wards = None
        # self.__inventory = None
        self.__current_wounds = self.get_wounds()

        self.set_action("idle")  # every character must have idle stance!

    def __repr__(self):
        return self.get_name()

    def set_wounds(self, wounds):
        self.__current_wounds = wounds

    def get_current_wounds(self):
        return self.__current_wounds

    def get_armor(self):
        return self.__armor

    def get_weapon(self):
        return self.__weapon

    def get_shield(self):
        return self.__shield

    def get_wards(self):
        # TODO: need to complete the models wards
        return []

    def get_model_type(self):
        return self.__model_type

    def is_front_row(self):
        position = self.get_position()
        if position[0] == GameConstants.PLAYERS_FRONT_COLUMN or position[0] == GameConstants.COMPUTER_FRONT_COLUMN:
            return True
        else:
            return False

    def is_killed(self):
        return self.get_current_wounds() <= 0
