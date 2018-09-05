from Shared.Action import Skills
from Shared.GameConstants import GameConstants
from Shared.SpecialRule import AccusationSR


class Skill:

    def __init__(self, name="", valid_targets=None):
        self.__name = name
        self.__valid_targets = valid_targets

    def get_name(self) -> str:
        return self.__name

    def get_menu_item_string(self) -> str:
        # returns a string to be shown as a menu item
        return self.__name

    def __repr__(self) -> str:
        return self.__name

    def get_valid_targets(self) -> int:
        return self.__valid_targets

    # noinspection PyMethodMayBeStatic
    def get_action(self):
        return Skills()

    def on_click(self, model, targets) -> None:
        pass


class SniperSkill(Skill):
    def __init__(self):
        super(SniperSkill, self).__init__("Snipe", valid_targets=GameConstants.TARGET_COMPUTER_SINGLE_ANY)

    def on_click(self, model, targets):
        pass


class AccusationSkill(Skill):
    """
    Empire Army Book p.37
    Select a single target, the witch hunter may re-roll all failed to-hit rolls against the target.
    Every hit he inflicts has the killing blow special rule, even if they were from a shooting attack.
    Finally the witch hunter may also choose to shoot at the target as if he had the sniper special rule.
    """

    def __init__(self):
        super(AccusationSkill, self).__init__("Accusation", valid_targets=GameConstants.TARGET_COMPUTER_SINGLE_ANY)
        self.__model = None

    def on_click(self, model, targets) -> None:
        if type(targets) is list:
            target = targets[0]
        else:
            target = targets
        self.__model = model  # set model
        self.__model.remove_special_rule(self.get_name())  # remove previous accusation special rule from model
        self.__model.add_special_rules(AccusationSR(target))
