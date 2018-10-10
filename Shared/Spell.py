from Shared.Action import Spells, Attack
from Shared.GameConstants import GameConstants
from Shared.Rolls import get_d6_roll
from Shared.SpecialRule import HammerOfSigmarSR, ShieldOfFaithSR, SoulfireSR


class Spell:

    def __init__(self, name="", valid_targets=GameConstants.TARGET_COMPUTER_ALL, cost=3):
        self.__name = name
        self.__valid_targets = valid_targets
        self.__is_cast = False
        self.__cost = cost
        self.__dice = 0
        self.__casting_result = 0
        self.__dispel_dice = 0
        self.__dispelling_model = None

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

    def __get_cast_result(self, wizard_level) -> int:
        casting_result = 0
        for dice in range(self.get_dice()):
            casting_result += get_d6_roll()

        if casting_result <= 2:
            # see WHFB Rule Book 8th ed, p.32
            return 0

        casting_result += wizard_level
        return casting_result

    def __get_dispel_result(self, wizard_level) -> int:
        dispel_result = 0
        for dice in range(self.get_dispel_dice()):
            dispel_result += get_d6_roll()

        if dispel_result <= 2:
            # see WHFB rule book 8th ed, p.35
            return 0

        dispel_result += wizard_level
        return dispel_result

    def __is_dispelled(self):
        pass

    def __is_cast_successful(self, casting_result):

        spell_cost = self.get_cost()

        if casting_result >= spell_cost:
            self.__casting_result = casting_result
            return True
        return False

    def on_click(self, action_manager) -> (bool, bool):
        """
        :param action_manager:
        :return: cast successfully: (True, False), miscast: (False, False), dispelled: (False, True)
        """
        turn_manager = action_manager.get_turn_manager()
        wizard_level = turn_manager.get_current_model().get_wizard_level()

        self.set_is_cast()  # mark spell as cast

        cast_result = self.__get_cast_result(wizard_level)
        dispel_result = self.__get_dispel_result(wizard_level)

        if cast_result < self.get_cost():
            return False, False  # cast failed

        elif dispel_result >= cast_result:
            return False, True  # dispelled

        return True, False  # cast successfully

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

    def set_dispel_dice(self, dice):
        self.__dispel_dice = dice

    def get_dispel_dice(self):
        return self.__dispel_dice

    def set_dispelling_model(self, model):
        self.__dispelling_model = model

    def get_dispelling_model(self):
        return self.__dispelling_model


class HammerOfSigmar(Spell):
    """
    Empire Army Book 8th ed. p.36
    The Warrior Priest and his unit re-roll all failed To Wound rolls in close combat until the start of the next
    friendly Magic phase.
    """

    def __init__(self):
        super(HammerOfSigmar, self).__init__(name="Hammer Of Sigmar", cost=3)

    def on_click(self, action_manager) -> (bool, bool):

        cast_success, dispelled = super(HammerOfSigmar, self).on_click(action_manager)
        if not cast_success:
            return cast_success, dispelled

        turn_manager = action_manager.get_turn_manager()
        unit = turn_manager.get_model_unit()
        for character in unit:
            character.add_special_rule(HammerOfSigmarSR())

        return True, False


class ShieldOfFaith(Spell):
    """
    Empire Army Book 8th ed. p.36
    The Warrior Priest and his unit have a 5+ ward save against all wounds inflicted in close combat
    until the start of the next friendly Magic phase.
    """

    def __init__(self):
        super(ShieldOfFaith, self).__init__(name="Shield Of Faith", cost=3)

    def on_click(self, action_manager):
        cast_success, dispelled = super(ShieldOfFaith, self).on_click(action_manager)
        if not cast_success:
            return cast_success, dispelled

        turn_manager = action_manager.get_turn_manager()
        unit = turn_manager.get_model_unit()

        # cast the spell
        for character in unit:
            character.add_special_rule(ShieldOfFaithSR())

        return True, False


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

        cast_success, dispelled = super(Soulfire, self).on_click(action_manager)
        if not cast_success:
            return cast_success, dispelled

        turn_manager = action_manager.get_turn_manager()
        unit = turn_manager.get_model_unit()

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
            # TODO: might need to change attack type
            action_manager.wound_target(target, attack=Attack(), strength=strength,
                                        armor_saves_allowed=False,
                                        double_effect=double_effect)

        return True, False
