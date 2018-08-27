from Shared.Rolls import *


class SpecialRules:

    def __init__(self, name=""):
        self.__name = name
        self.__targets = []

    def get_name(self):
        return self.__name

    def __repr__(self):
        return self.get_name()

    def get_targets(self):
        return self.__targets

    # noinspection PyMethodMayBeStatic
    def re_roll_to_hit(self, target):
        return False

    def re_roll_to_wound(self, target):
        return False

    def pass_fear_ld_test(self):
        return False


class AccusationSR(SpecialRules):
    def __init__(self, target):
        super(AccusationSR, self).__init__("Accusation")
        self.__target = target

    def re_roll_to_hit(self, target):
        if target == self.get_targets():
            return True
        return False

    def do_killing_blow(self, target):
        if target == self.__target:
            return True
        else:
            return False


class GrimResolveSR(SpecialRules):
    def __init__(self):
        super(GrimResolveSR, self).__init__(name="Grim Resolve")

    def pass_fear_ld_test(self):
        return True

    # noinspection PyMethodMayBeStatic
    def pass_terror_ld_test(self, ld):
        roll = get_2d6_roll()

        if roll == 2 or roll <= ld:
            return True

        return False


class ToolsOfJudgmentSR(SpecialRules):
    """
    Empire 8ed p.38
    When attacking wizards, or models with the Undead, Nehekharan Undead
    or Daemonic special rules, in CLOSE COMBAT, a witch hunter re-rolls failed rolls To Wound.
    """
    def __init__(self):
        super(ToolsOfJudgmentSR, self).__init__(name="Tools Of Judgment")

    def re_roll_to_wound(self, target):
        target_special_rules_list = target.get_special_rules_list
        for sr in target_special_rules_list:
            if isinstance(sr, Undead) or isinstance(sr, Demonic):
                return True
        return False


class Undead(SpecialRules):
    def __init__(self):
        super(Undead, self).__init__(name="Undead")


class Demonic(SpecialRules):
    def __init__(self):
        super(Demonic, self).__init__(name="Demonic")
