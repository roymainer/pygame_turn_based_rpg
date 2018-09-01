from Shared.Rolls import *


class SpecialRule:

    def __init__(self, name=""):
        self.__name = name
        self.__targets = []
        self.__to_remove = False

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

    def get_strength_bonus(self):
        return 0

    def pass_fear_ld_test(self):
        return False

    def set_to_remove(self, to_remove: bool):
        self.__to_remove = to_remove

    def get_to_remove(self):
        return self.__to_remove


# ------------------- General Special Rules ------------------- #
class AlwaysStrikesLast(SpecialRule):
    def __init__(self):
        super(AlwaysStrikesLast, self).__init__("Always Strikes Last")


class AccusationSR(SpecialRule):
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


class GrimResolveSR(SpecialRule):
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


class ToolsOfJudgmentSR(SpecialRule):
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


class Hatred(SpecialRule):
    """
    Warhammer Fantasy Rule Book P.71
    on first attack, re-roll all close combat to hit misses
    """
    def __init__(self):
        super(Hatred, self).__init__(name="Hatred")

    def re_roll_to_hit(self, target):
        self.set_to_remove(True)
        return True


class AncestralGrudge(Hatred):
    """
    Dwarfs Army Book p.32
    Rolling a D6 to determine is pointless, just add Hatred
    """
    def __init__(self):
        super(AncestralGrudge, self).__init__(name="Ancestral Grudge")


class Resolute(SpecialRule):
    """
    Dwarfs Army Book p.32
    +1 Strength during first turn of combat
    """
    def __init__(self):
        super(Resolute, self).__init__(name="Resolute")

    def get_strength_bonus(self):
        self.set_to_remove(True)
        return 1


class Undead(SpecialRule):
    def __init__(self):
        super(Undead, self).__init__(name="Undead")


class Demonic(SpecialRule):
    def __init__(self):
        super(Demonic, self).__init__(name="Demonic")
