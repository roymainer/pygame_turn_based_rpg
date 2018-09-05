from Shared.Action import Spells
from Shared.GameConstants import GameConstants
from Shared.SpecialRule import HammerOfSigmarSR, ShieldOfFaithSR, SoulfireSR


class Spell:

    def __init__(self, name="", valid_targets=GameConstants.TARGET_COMPUTER_ALL):
        self.__name = name
        self.__valid_targets = valid_targets

    def get_name(self) -> str:
        return self.__name

    def get_menu_item_string(self) -> str:
        # returns a string to be shown as a menu item
        return self.__name

    def __repr__(self) -> str:
        return self.__name

    def set_valid_target(self, valid_targets):
        self.__valid_targets = valid_targets

    def get_valid_targets(self) -> int:
        return self.__valid_targets

    # noinspection PyMethodMayBeStatic
    def get_action(self):
        return Spells()

    def on_click(self, turn_manager) -> None:
        pass


class HammerOfSigmar(Spell):
    """
    Empire Army Book 8th ed. p.36
    The Warrior Priest and his unit re-roll all failed To Wound rolls in close combat until the start of the next
    friendly Magic phase.
    """
    def __init__(self):
        super(HammerOfSigmar, self).__init__("Hammer Of Sigmar")

    def on_click(self, turn_manager):

        unit = turn_manager.get_current_model_unit()

        for character in unit:
            character.add_special_rule(HammerOfSigmarSR())


class ShieldOfFaith(Spell):
    """
    Empire Army Book 8th ed. p.36
    The Warrior Priest and his unit have a 5+ ward save against all wounds inflicted in close combat
    until the start of the next friendly Magic phase.
    """
    def __init__(self):
        super(ShieldOfFaith, self).__init__("Shield Of Faith")

    def on_click(self, turn_manager):
        unit = turn_manager.get_current_model_unit()

        for character in unit:
            character.add_special_rule(ShieldOfFaithSR())


class Soulfire(Spell):
    """
    Empire Army Book 8th ed. p.36
    The Warrior Priest and his unit gain the Flaming Attacks special rule until the start of the next friendly Magic
    phase. In addition, when cast, all enemy models suffer a Strength 4 hit. Undead and units with Daemonic special rule
    suffer Strength 5 hit instead, with no armour saves allowed.
    """
    def __init__(self):
        super(Soulfire, self).__init__(name="Soulfire")

    def on_click(self, action_mananger):

        turn_manager = action_mananger.get_turn_manager()

        # assign soulfire to all models in current models unit
        unit = turn_manager.get_current_model_unit()
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
                if sr.is_flamable():
                    double_effect = True
            action_mananger.wound_target(target, strength=strength, armor_saves_allowed=False, double_effect=double_effect)

        return
