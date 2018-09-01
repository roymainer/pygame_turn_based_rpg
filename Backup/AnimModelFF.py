"""
AnimModelFF class is an extension of the AnimatedObject class
It's based on Final Fantasy style models
it supports weapons which are animated sprites!
it supports more actions (animations), character attributes and sounds (need to add)
Required Actions:
idle
attack
cast
run
hurt
die
"""
from Shared.AnimAttrObject import AnimAttrObject
from Shared.GameConstants import GameConstants
from Shared.SpecialRule import AlwaysStrikesLast

SPRITE_SHEET = "Sprite_Sheet"
SIZE = "Size"

MODEL_TYPE_MELEE = 0
MODEL_TYPE_RANGE = 1
MODEL_TYPE_MAGIC = 2

ACTION_ATTACK = "Attack"
ACTION_SHOOT = "Shoot"
ACTION_SKILLS = "Skills"
ACTION_ITEMS = "Items"
ACTION_SPELLS = "Magic"


class ModelFF(AnimAttrObject):
    # TODO: add wards and inventory
    # TODO: instead of loading from a py file need to load from an encrypted file
    def __init__(self, sprite_sheet_file, position=(0, 0), object_type=None, size=None,
                 name="", m=0, ws=0, bs=0, s=0, t=0, w=0, i=0, a=0, ld=0):

        self.__armor = None
        self.__weapons = []
        self.__shield = None
        # self.__wards = None
        self.__actions_list = []
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

    def get_initiative(self):
        for sr in self.get_special_rules_list():
            if isinstance(sr, AlwaysStrikesLast):
                # if a unit has the always strikes last special rule, modify the initiative
                return 0
        return super(ModelFF, self).get_initiative()

    def set_armor(self, armor):
        self.__armor = armor

    def get_armor(self):
        return self.__armor

    def add_weapon(self, weapon):
        self.__weapons.append(weapon)
        self.add_action(weapon.get_action())
        self.add_special_rules(weapon.get_special_rules_list())

    def get_weapons(self):
        return self.__weapons

    def get_melee_weapon(self):
        for weapon in self.__weapons:
            if not weapon.is_ranged_weapon():
                return weapon

    def get_ranged_weapon(self):
        for weapon in self.__weapons:
            if weapon.is_ranged_weapon():
                return weapon

    def set_shield(self, shield):
        self.__shield = shield

    def get_shield(self):
        return self.__shield

    # def get_wards(self):
    #     # TODO: need to complete the models wards
    #     return []

    def get_sprites(self):
        sprites = []
        if self.__weapons is not None:
            for weapon in self.__weapons:
                sprites.append(weapon)  # background layer
                sprites.append(self)
        else:
            sprites.append(self)
        if self.__shield is not None:
            sprites.append(self.__shield)
        return sprites

    def set_action(self, action):
        # if self.__armor is not None:
        #     self.__armor.set_action(action)
        if self.__weapons is not None:
            for weapon in self.__weapons:
                weapon.set_action(action)
        if self.__shield is not None:
            self.__shield.set_action(action)
        super(ModelFF, self).set_action(action)
        return

    def add_action(self, new_action):
        for action in self.__actions_list:
            if type(action) == type(new_action):
                return
        self.__actions_list.append(new_action)

    def get_actions_list(self):
        return self.__actions_list

    def add_skill(self, skill):
        self.__skills_list.append(skill)
        self.add_action(skill.get_action())

    def get_skills_list(self):
        return self.__skills_list

    def add_special_rules(self, special_rules):
        if type(special_rules) is not list:
            special_rules = [special_rules]
        for sr in special_rules:
            self.add_special_rule(sr)

    def remove_special_rule(self, special_rule_name):
        for i, o in enumerate(self.__special_rules_list):
            if o.get_name() == special_rule_name:
                del self.__special_rules_list[i]
                break

    def add_spell(self, spell):
        self.__spells_list.append(spell)
        self.add_action(spell.get_action())

    def get_spells_list(self):
        return self.__spells_list

    def add_item(self, item):
        self.__items_list.append(item)

    def get_items_list(self):
        return self.__items_list

    def flip_x(self):
        # if self.__armor is not None:
        #     self.__armor.set_action(action)
        if self.__weapons is not None:
            for weapon in self.__weapons:
                weapon.flip_x()
        if self.__shield is not None:
            self.__shield.flip_x()
        super(ModelFF, self).flip_x()

    def set_position(self, position):
        if self.__weapons is not None:
            for weapon in self.__weapons:
                weapon.set_position(position)
        if self.__shield is not None:
            self.__shield.set_position(position)
        super(ModelFF, self).set_position(position)

    def is_front_row(self):
        position = self.get_position()
        if position[0] == GameConstants.PLAYERS_FRONT_COLUMN or position[0] == GameConstants.COMPUTER_FRONT_COLUMN:
            return True
        else:
            return False

    def kill(self):
        if self.__armor is not None:
            self.__armor.kill()
        if self.__weapons is not None:
            for weapon in self.__weapons:
                weapon.kill()
        if self.__shield is not None:
            self.__shield.kill()
        super(ModelFF, self).kill()

    def is_killed(self):
        return self.get_current_wounds() <= 0
