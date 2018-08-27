from Shared.SpecialRules import AccusationSR
from Shared.GameConstants import GameConstants


class Skill:

    def __init__(self, name="", valid_targets=None):
        self.__name = name
        self.__valid_targets = valid_targets
        # self.__max_turns = turns
        # self.__remaining_turns = turns
        # self.__targets = []
        # self.__active = active

    def get_name(self):
        return self.__name

    def get_valid_targets(self):
        return self.__valid_targets

    def on_click(self, model, targets):
        pass

    # def add_target(self, target):
    #     self.__targets.append(target)
    #
    # def set_targets(self, targets):
    #     if type(targets) is list:
    #         self.__targets = targets
    #     else:
    #         self.add_target(targets)
    #
    # def get_targets(self):
    #     return self.__targets
    #
    # def re_roll_to_hit(self, target):
    #     return False
    #
    # def do_killing_blow(self, target):
    #     return False
    #
    # def pass_fear_ld_test(self):
    #     return False


class AccusationSkill(Skill):

    def __init__(self):
        super(AccusationSkill, self).__init__("Accusation", valid_targets=GameConstants.TARGET_SINGLE_ANY)
        self.__model = None

    def on_click(self, model, targets):
        if type(targets) is list:
            target = targets[0]
        self.__model = model  # set model
        self.__model.remove_special_rule(self.get_name())  # remove previous accusation special rule from model
        self.__model.add_special_rule(AccusationSkill(target))


class SniperSkill(Skill):
    def __init__(self):
        super(SniperSkill, self).__init__("Snipe", valid_targets=GameConstants.TARGET_SINGLE_ANY)

    def on_click(self, model, targets):
        pass


