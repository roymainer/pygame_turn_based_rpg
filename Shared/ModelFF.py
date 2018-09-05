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
from Shared.GameConstants import GameConstants
from Shared.UIConstants import UIConstants
from Shared.AnimAttrObject import AnimAttrObject
from UI.Text import Text

SPRITE_SHEET = "Sprite_Sheet"
SIZE = "Size"

MODEL_TYPE_MELEE = 0
MODEL_TYPE_RANGE = 1
MODEL_TYPE_MAGIC = 2

ACTION_ATTACK = "Attack"
ACTION_SHOOT = "Shoot"
ACTION_SKILLS = "Skills"
ACTION_SPELLS = "Spells"
ACTION_ITEMS = "Items"


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

        self.__texts = []

        super(ModelFF, self).__init__(sprite_sheet_file, size, position, object_type, name, m, ws, bs, s, t, w, i, a,
                                      ld)

        self.__current_wounds = self.get_wounds()
        self.set_action("idle")  # every character must have idle stance!

    def __repr__(self) -> str:
        return self.get_name()

    def special_rules_to_texts(self) -> None:
        for sr in self.get_special_rules_list():
            text = Text(string=sr.get_name(),
                        position=(0, 0),
                        font_size=UIConstants.TEXT_SIZE_TINY)

            text_size = text.get_size()

            for target in sr.get_targets():
                # if the special rules applies for specific target like accusation, print near target
                target_position = target.get_position()
                target_size = target.get_size()

                # if any(self.__texts):
                #     position = (self.__texts[-1].get_position()[0],
                #                 self.__texts[-1].get_position()[1] - text_size[1] - 2)
                # else:
                position = (target_position[0] - text_size[0] - 5, target_position[1] + target_size[1] - 2)
                text.set_position(position)
                self.__texts.append(text)
            else:
                # if the special rule applies for the model itself, show near model
                model_position = self.get_position()
                model_size = self.get_size()
                if any(self.__texts):
                    position = (self.__texts[-1].get_position()[0],
                                self.__texts[-1].get_position()[1] - text_size[1] - 2)
                else:
                    position = (model_position[0] + model_size[0] + 5, model_position[1] + model_size[1] - 2)

                text.set_position(position)
                self.__texts.append(text)

    def get_texts(self) -> list:
        return self.__texts

    def hide_models_special_rules(self):
        for text in self.__texts:
            text.kill()

        self.__texts = []

    def get_menu_item_string(self) -> str:
        string = self.get_name() + "_" + "HP:" + str(self.get_current_wounds()) + "/" + str(self.get_wounds())
        num_chars = len(string)
        delta_chars = UIConstants.MENU_MAX_CHARS - num_chars
        string = string.replace("_", " " * delta_chars)
        return string

    def set_wounds(self, wounds) -> None:
        self.__current_wounds = wounds

    def get_current_wounds(self) -> int:
        return self.__current_wounds

    def get_initiative(self) -> int:
        for sr in self.get_special_rules_list():
            if sr.get_name() == "Always Strikes Last":
                return 0
        return super(ModelFF, self).get_initiative()

    def set_armor(self, armor) -> None:
        self.__armor = armor

    def get_armor(self):
        return self.__armor

    def add_weapon(self, weapon) -> None:
        self.__weapons.append(weapon)
        self.add_action(weapon.get_action())
        self.add_special_rules(weapon.get_special_rules_list())

    def get_weapons(self) -> list:
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

    def add_action(self, new_action) -> None:
        for action in self.__actions_list:
            if type(action) == type(new_action):
                return
        self.__actions_list.append(new_action)

    def set_action(self, action) -> None:
        if action == "die":
            self.set_last_animation()
        super(ModelFF, self).set_action(action)

    def get_actions_list(self) -> list:
        return self.__actions_list

    def add_skill(self, skill) -> None:
        self.__skills_list.append(skill)
        self.add_action(skill.get_action())

    def get_skills_list(self) -> list:
        return self.__skills_list

    def add_special_rules(self, special_rules) -> None:
        if type(special_rules) is not list:
            special_rules = [special_rules]
        for sr in special_rules:
            self.add_special_rule(sr)

    def remove_special_rule(self, special_rule_name: str) -> None:
        for i, o in enumerate(self.get_special_rules_list()):
            if o.get_name() == special_rule_name:
                del self.get_special_rules_list()[i]
                break

    def add_spell(self, spell) -> None:
        self.__spells_list.append(spell)
        self.add_action(spell.get_action())

    def get_spells_list(self) -> list:
        return self.__spells_list

    def add_item(self, item) -> None:
        self.__items_list.append(item)

    def get_items_list(self) -> list:
        return self.__items_list

    def is_frenzied(self) -> bool:
        for sr in self.get_special_rules_list():
            if sr.get_name() == "Frenzied":
                return True
        return False

    def is_killed(self) -> bool:
        return self.get_current_wounds() <= 0

    def destroy(self, tm):
        for text in self.__texts:
            text.kill()

        if self.get_type() == GameConstants.PLAYER_GAME_OBJECTS:
            unit = tm.get_all_player_models()
            enemy_unit = tm.get_all_computer_models()
        else:
            unit = tm.get_all_computer_models()
            enemy_unit = tm.get_all_player_models()
        for sr in self.get_special_rules_list():
            sr.on_kill(self, unit, enemy_unit)

        super(ModelFF, self).kill()
