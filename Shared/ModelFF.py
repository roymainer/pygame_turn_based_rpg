"""
ModelFF class is an extension of the AnimatedObject class
It's based on Final Fantasy style models
it supports more actions (animations), character attributes and sounds (need to add)
Required Actions:
idle
attack
cast
run
hurt
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
ACTION_SPELLS = "Magic"


def get_model_actions(model):
    actions_list = [ACTION_ATTACK]
    if any(model.get_skills_list()):
        actions_list.append(ACTION_SKILLS)
    if any(model.get_spells_list()):
        actions_list.append(ACTION_SPELLS)
    if any(model.get_items_list()):
        actions_list.append(ACTION_ITEMS)
    return actions_list

    # model_type = model.get_model_type()
    # if model_type == MODEL_TYPE_MELEE:
    #     return [ACTION_ATTACK, ACTION_SKILLS, ACTION_ITEMS]
    # if model_type == MODEL_TYPE_RANGE:
    #     return [ACTION_ATTACK, ACTION_SKILLS, ACTION_ITEMS]
    # if model_type == MODEL_TYPE_MAGIC:
    #     return [ACTION_ATTACK, ACTION_SPELLS, ACTION_SKILLS, ACTION_ITEMS]
    # return


class ModelFF(AnimAttrObject):
    # TODO: add wards and inventory
    # TODO: instead of loading from a py file need to load from an encrypted file
    def __init__(self, sprite_sheet_file, position, object_type, model_type, size=None,
                 name="", m=0, ws=0, bs=0, s=0, t=0, w=0, i=0, a=0, ld=0,
                 armor=None, weapon=None, shield=None):

        self.__model_type = model_type
        self.__armor = armor
        self.__weapon = weapon
        self.__shield = shield
        # self.__wards = None
        self.__special_rules_list = []
        self.__skills_list = []
        self.__spells_list = []
        self.__items_list = []

        super(ModelFF, self).__init__(sprite_sheet_file, size, position, object_type, name, m, ws, bs, s, t, w, i, a,
                                      ld)

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

    def get_sprites(self):
        sprites = []
        if self.__weapon is not None:
            sprites.append(self.__weapon)  # background layer
            sprites.append(self)
        else:
            sprites.append(self)
        if self.__shield is not None:
            sprites.append(self.__shield)
        return sprites

    def set_action(self, action):
        # if self.__armor is not None:
        #     self.__armor.set_action(action)
        if self.__weapon is not None:
            self.__weapon.set_action(action)
        if self.__shield is not None:
            self.__shield.set_action(action)
        super(ModelFF, self).set_action(action)
        # self.__blit_images()
        return

    def add_skill(self, skill):
        self.__skills_list.append(skill)

    def get_skills_list(self):
        return self.__skills_list

    def add_special_rule(self, special_rule):
        self.__special_rules_list.append(special_rule)

    def get_special_rules_list(self):
        return self.__special_rules_list

    def remove_special_rule(self, special_rule_name):
        for i, o in enumerate(self.__special_rules_list):
            if o.get_name() == special_rule_name:
                del self.__special_rules_list[i]
                break

    def add_spell(self, spell):
        self.__spells_list.append(spell)

    def get_spells_list(self):
        return self.__spells_list

    def add_item(self, item):
        self.__items_list.append(item)

    def get_items_list(self):
        return self.__items_list

    def flip_x(self):
        # if self.__armor is not None:
        #     self.__armor.set_action(action)
        if self.__weapon is not None:
            self.__weapon.flip_x()
        if self.__shield is not None:
            self.__shield.flip_x()
        super(ModelFF, self).flip_x()

    def set_position(self, position):
        if self.__weapon is not None:
            self.__weapon.set_position(position)
        if self.__shield is not None:
            self.__shield.set_position(position)
        super(ModelFF, self).set_position(position)

    def kill(self):
        if self.__armor is not None:
            self.__armor.kill()
        if self.__weapon is not None:
            self.__weapon.kill()
        if self.__shield is not None:
            self.__weapon.kill()
        super(ModelFF, self).kill()