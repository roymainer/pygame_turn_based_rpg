from Shared.Action import Attack, RangeAttack
from Shared.Rolls import *


class SpecialRule:

    def __init__(self, name=""):
        self.__name = name
        self.__targets = []
        self.__used_up = False

    def get_name(self) -> str:
        return self.__name

    def __repr__(self) -> str:
        return self.get_name()

    def get_targets(self) -> list:
        return self.__targets

    def set_targets(self, targets: list) -> None:
        self.__targets = targets

    def add_target(self, target) -> None:
        self.__targets.append(target)

    # noinspection PyMethodMayBeStatic
    def re_roll_to_hit(self, target) -> bool:
        return False

    def re_roll_to_wound(self, target, attack_type) -> bool:
        return False

    def get_strength_bonus(self) -> int:
        return 0

    def get_panic_ld_test_result(self) -> bool:
        return False

    def get_fear_ld_test_result(self) -> bool:
        return False

    def get_terror_ld_test_result(self, ld) -> bool:
        return False

    def is_killing_blow(self, target) -> bool:
        return False

    def get_ward_save(self, attack, model) -> bool:
        return False

    def set_used_up(self) -> None:
        self.__used_up = True

    def is_used_up(self) -> bool:
        return self.__used_up

    def is_flaming_attack(self) -> bool:
        return False

    def is_flammable(self):
        return False

    def is_undead(self) -> bool:
        return False

    def is_daemonic(self) -> bool:
        return False

    def on_init(self, model, unit, enemy_unit):
        return

    def on_kill(self, model, unit, enemy_unit):
        return


# ------------------- General Special Rules ------------------- #
class AlwaysStrikesLast(SpecialRule):
    def __init__(self):
        super(AlwaysStrikesLast, self).__init__("Always Strikes Last")


class Hatred(SpecialRule):
    """
    Warhammer Fantasy Rule Book P.71
    on first attack, re-roll all close combat to hit misses
    """
    def __init__(self):
        super(Hatred, self).__init__(name="Hatred")

    def re_roll_to_hit(self, target) -> bool:
        self.set_used_up()
        return True


class Parry(SpecialRule):
    """
    Rules Book p.88
    If a warrior is fighting with a hand weapon and a shield, then he has a 6+ ward save,
    representing his chance to parry the blow.
    restrictions:
    close combat only
    doesn't apply against stomp attack
    doesn't apply to frenzied warriors
    """

    def __init__(self):
        super(Parry, self).__init__(name="Parry")

    def get_ward_save(self, attack, model):
        attack_type = attack.get_attack_type()
        if attack_type in [Attack.ATTACK_TYPE_STOMP, Attack.ATTACK_TYPE_THUNDER_STOMP]:
            return False

        if model.is_frenzied():
            return False

        roll = get_d6_roll()
        if roll >= 6:
            return True
        else:
            return False


class Flammable(SpecialRule):
    def __init__(self):
        super(Flammable, self).__init__("Flammable")

    def is_flammable(self):
        return True


class Frenzied(SpecialRule):
    """
    Rule book p.69
    Frenzied troops have the Extra Attack and Immune to Psychology special rules
    """

    def __init__(self):
        super(Frenzied, self).__init__(name="Frenzied")


class ExtraAttack(SpecialRule):
    def __init__(self):
        super(ExtraAttack, self).__init__(name="Extra Attack")


class ImmuneToPsychology(SpecialRule):
    def __init__(self):
        super(ImmuneToPsychology, self).__init__(name="Immune To Psychology")

    def get_panic_ld_test_result(self):
        return True

    def get_fear_ld_test_result(self):
        return True

    def get_terror_ld_test_result(self, ld):
        return True


class TerrorToFear(SpecialRule):
    def __init__(self):
        super(TerrorToFear, self).__init__(name="Terror To Fear")

    def get_terror_ld_test_result(self, ld):
        # TODO: need to actually pass the fear test to the function in oreder to return a valid result
        return self.get_fear_ld_test_result()


# ------------------- Empire Special Rules ------------------- #
class AccusationSR(SpecialRule):

    def __init__(self, target):
        super(AccusationSR, self).__init__("Accusation")
        self.set_targets([target])

    def re_roll_to_hit(self, target) -> bool:
        if target == self.get_targets():
            return True
        return False

    def is_killing_blow(self, target) -> bool:
        if target == self.get_targets()[0]:
            return True
        else:
            return False


class GrimResolveSR(SpecialRule):
    def __init__(self):
        super(GrimResolveSR, self).__init__(name="Grim Resolve")

    def on_init(self, model, unit, enemy_unit):
        for model in unit:
            model.add_special_rule(TerrorToFear())
            self.add_target(model)

    def get_fear_ld_test_result(self) -> bool:
        return True

    # noinspection PyMethodMayBeStatic
    def get_terror_ld_test_result(self, ld) -> bool:
        roll = get_2d6_roll()
        if roll == 2 or roll <= ld:
            return True
        return False

    def on_kill(self, model, unit, enemy_unit):
        for target in self.get_targets():
            target.remove_special_rule("Terror To Fear")


class ToolsOfJudgmentSR(SpecialRule):
    """
    Empire 8ed p.38
    When attacking wizards, or models with the Undead, Nehekharan Undead
    or Daemonic special rules, in CLOSE COMBAT, a witch hunter re-rolls failed rolls To Wound.
    """
    def __init__(self):
        super(ToolsOfJudgmentSR, self).__init__(name="Tools Of Judgment")

    def re_roll_to_wound(self, target, attack_type) -> bool:
        if type(attack_type) == RangeAttack:
            return False
        for sr in target.get_special_rules_list():
            if isinstance(sr, Undead) or isinstance(sr, Daemonic) or target.is_wizard():
                return True
        return False


class RighteousFury(SpecialRule):
    """
    Empire 8ed p.36
    A warrior priest and unit he is currently in, has the Hatred special rule.
    However, other characters in the unit do not gain the Hatred special rule.
    """
    def __init__(self):
        super(RighteousFury, self).__init__(name="Righteous Fury")

    def on_init(self, model, unit, enemy_unit):
        for character in unit:
            character.add_special_rule(Hatred())

    def on_kill(self, model, unit, enemy_unit):
        for character in unit:
            character.remove_special_rule("Hatred")


class HammerOfSigmarSR(SpecialRule):
    """
    Empire Army Book p.37
    The Warrior Priest and his unit re-roll all failed To Wound rolls in close combat until the start of the next
    friendly Magic phase.
    """
    def __init__(self):
        super(HammerOfSigmarSR, self).__init__(name="Hammer Of Sigmar")
        self.set_used_up()  # remove by end of turn

    def re_roll_to_wound(self, target, attack_type):
        if type(attack_type) == RangeAttack:
            return False
        else:
            return True


class ShieldOfFaithSR(SpecialRule):
    """
    Empire Army Book 8th ed. p.36
    The Warrior Priest and his unit have a 5+ ward save against all wounds inflicted in close combat
    until the start of the next friendly Magic phase.
    """
    def __init__(self):
        super(ShieldOfFaithSR, self).__init__(name="Shield Of Faith")
        self.set_used_up()  # remove by end of turn

    def get_ward_save(self, attack, model):
        roll = get_d6_roll()
        if roll >= 5:
            return True
        else:
            return False


class SoulfireSR(SpecialRule):
    """
    Empire Army Book 8th ed. p.36
    The Warrior Priest and his unit gain the Flaming Attacks special rule until the start of the next friendly Magic
    phase. In addition, when cast, all enemy models suffer a Strength 4 hit. Undead and units with Daemonic special rule
    suffer Strength 5 hit instead, with no armour saves allowed.
    """

    def __init__(self):
        super(SoulfireSR, self).__init__(name="Soulfire")
        self.set_used_up()  # remove by end of turn

    def is_flaming_attack(self):
        return True


# ------------------- Dwarf Special Rules ------------------- #
class AncestralGrudge(SpecialRule):
    """
    Dwarfs Army Book p.32
    Rolling a D6 to determine is pointless, just add Hatred
    """
    def __init__(self):
        super(AncestralGrudge, self).__init__(name="Ancestral Grudge")

    def re_roll_to_hit(self, target) -> bool:
        self.set_used_up()
        return True


class Resolute(SpecialRule):
    """
    Dwarfs Army Book p.32
    +1 Strength during first turn of combat
    """
    def __init__(self):
        super(Resolute, self).__init__(name="Resolute")

    def get_strength_bonus(self) -> int:
        # print("Got +1 Strength using Resolute Special Rule")
        self.set_used_up()
        return 1


class Undead(SpecialRule):
    def __init__(self):
        super(Undead, self).__init__(name="Undead")

    def is_undead(self):
        return True


class Daemonic(SpecialRule):
    def __init__(self):
        super(Daemonic, self).__init__(name="Daemonic")

    def is_daemonic(self):
        return True
