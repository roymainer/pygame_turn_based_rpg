from Shared.Action import Spells
from Shared.GameConstants import GameConstants
from Shared.Rolls import get_d6_roll
from Shared.SpecialRule import HammerOfSigmarSR, ShieldOfFaithSR, SoulfireSR


def is_cast_successful(spell_cost, assigned_dice, wizard_level):
    roll = 0
    for dice in range(assigned_dice):
        roll += get_d6_roll()

    if roll <= 2:
        # see WHFB Rule Book 8th ed,p.32
        return False

    roll += wizard_level

    if roll >= spell_cost:
        return True
    return False


class Spell:

    def __init__(self, name="", valid_targets=GameConstants.TARGET_COMPUTER_ALL, cost=3):
        self.__name = name
        self.__valid_targets = valid_targets
        self.__is_cast = False
        self.__cost = cost
        self.__dice = 0

    def get_name(self) -> str:
        return self.__name

    def get_menu_item_string(self) -> str:
        # returns a string to be shown as a menu item
        string = self.__name + " ({})".format(str(self.__cost))
        return string

    def __repr__(self) -> str:
        return self.__name

    def set_valid_target(self, valid_targets):
        self.__valid_targets = valid_targets

    def get_valid_targets(self) -> int:
        return self.__valid_targets

    # noinspection PyMethodMayBeStatic
    def get_action(self):
        return Spells()

    def on_click(self, action_manager) -> None:
        self.set_is_cast()  # mark spell as cast

    def set_is_cast(self):
        self.__is_cast = True

    def get_is_cast(self):
        return self.__is_cast

    def reset_spell(self):
        self.__is_cast = False
        self.set_dice(0)  # reset the dice

    def set_dice(self, dice):
        self.__dice = dice

    def get_dice(self):
        return self.__dice

    def get_cost(self):
        return self.__cost


class HammerOfSigmar(Spell):
    """
    Empire Army Book 8th ed. p.36
    The Warrior Priest and his unit re-roll all failed To Wound rolls in close combat until the start of the next
    friendly Magic phase.
    """

    def __init__(self):
        super(HammerOfSigmar, self).__init__(name="Hammer Of Sigmar", cost=3)

    def on_click(self, action_manager):
        turn_manager = action_manager.get_turn_manager()
        wizard_level = turn_manager.get_current_model().get_wizard_level()
        unit = turn_manager.get_model_unit()

        self.set_is_cast()  # mark spell as cast

        if not is_cast_successful(self.get_cost(), self.get_dice(), wizard_level):
            return False

        for character in unit:
            character.add_special_rule(HammerOfSigmarSR())

        return True


class ShieldOfFaith(Spell):
    """
    Empire Army Book 8th ed. p.36
    The Warrior Priest and his unit have a 5+ ward save against all wounds inflicted in close combat
    until the start of the next friendly Magic phase.
    """

    def __init__(self):
        super(ShieldOfFaith, self).__init__(name="Shield Of Faith", cost=3)

    def on_click(self, action_manager):
        turn_manager = action_manager.get_turn_manager()
        wizard_level = turn_manager.get_current_model().get_wizard_level()
        unit = turn_manager.get_model_unit()

        self.set_is_cast()  # mark spell as cast

        if not is_cast_successful(self.get_cost(), self.get_dice(), wizard_level):
            return False

        # cast the spell
        for character in unit:
            character.add_special_rule(ShieldOfFaithSR())

        return True


class Soulfire(Spell):
    """
    Empire Army Book 8th ed. p.36
    The Warrior Priest and his unit gain the Flaming Attacks special rule until the start of the next friendly Magic
    phase. In addition, when cast, all enemy models suffer a Strength 4 hit. Undead and units with Daemonic special rule
    suffer Strength 5 hit instead, with no armour saves allowed.
    """

    def __init__(self):
        super(Soulfire, self).__init__(name="Soulfire", cost=3)

    def on_click(self, action_manager):
        turn_manager = action_manager.get_turn_manager()
        wizard_level = turn_manager.get_current_model().get_wizard_level()
        unit = turn_manager.get_model_unit()

        self.set_is_cast()  # mark spell as cast

        if not is_cast_successful(self.get_cost(), self.get_dice(), wizard_level):
            return False

        # assign soulfire to all models in current models unit
        for character in unit:
            character.add_special_rule(SoulfireSR())

        # hit all adjacent enemy models with soulfire
        enemy_unit = turn_manager.get_opponent_unit()
        targets = [x for x in enemy_unit if x.is_front_row()]  # get only front row targets
        for target in targets:
            strength = 4
            double_effect = False
            for sr in target.get_special_rules_list():
                if sr.is_undead() or sr.is_daemonic():
                    strength = 5
                if sr.is_flammable():
                    double_effect = True
            action_manager.wound_target(target, strength=strength,
                                        armor_saves_allowed=False,
                                        double_effect=double_effect)

        return True
