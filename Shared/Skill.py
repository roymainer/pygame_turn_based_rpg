from Shared.Action import Skills
from Shared.GameConstants import GameConstants


class Skill:

    def __init__(self, name="", valid_targets=None):
        self.__name = name
        self.__valid_targets = valid_targets

    def get_name(self):
        return self.__name

    def get_menu_item_string(self):
        # returns a string to be shown as a menu item
        return self.__name

    def __repr__(self):
        return self.__name

    def get_valid_targets(self):
        return self.__valid_targets

    def get_action(self):
        return Skills()

    def on_click(self, model, targets):
        pass


class AccusationSkill(Skill):

    def __init__(self):
        super(AccusationSkill, self).__init__("Accusation", valid_targets=GameConstants.TARGET_COMPUTER_SINGLE_ANY)
        self.__model = None

    def on_click(self, model, targets):
        if type(targets) is list:
            targets = targets[0]
        self.__model = model  # set model
        self.__model.remove_special_rule(self.get_name())  # remove previous accusation special rule from model
        self.__model.add_special_rules(AccusationSkill(targets))


class SniperSkill(Skill):
    def __init__(self):
        super(SniperSkill, self).__init__("Snipe", valid_targets=GameConstants.TARGET_COMPUTER_SINGLE_ANY)

    def on_click(self, model, targets):
        pass


