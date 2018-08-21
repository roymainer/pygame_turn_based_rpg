from Shared import Bestiary
import Rolls

""" Key (unit_ws) : value (dict : key (enemy_ws) : value (dice roll to hit)) """
# rows: unit's weapon skill, columns: target's weapon skill
TO_HIT_CHART_CLOSE_COMBAT = {
    1: {1: 4, 2: 4, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5},
    2: {1: 3, 2: 4, 3: 4, 4: 4, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5},
    3: {1: 3, 2: 3, 3: 4, 4: 4, 5: 4, 6: 4, 7: 5, 8: 5, 9: 5, 10: 5},
    4: {1: 3, 2: 3, 3: 3, 4: 4, 5: 4, 6: 4, 7: 4, 8: 4, 9: 5, 10: 5},
    5: {1: 3, 2: 3, 3: 3, 4: 3, 5: 4, 6: 4, 7: 4, 8: 4, 9: 4, 10: 4},
    6: {1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 4, 7: 4, 8: 4, 9: 4, 10: 4},
    7: {1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3, 7: 4, 8: 4, 9: 4, 10: 4},
    8: {1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3, 7: 3, 8: 4, 9: 4, 10: 4},
    9: {1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3, 7: 3, 8: 3, 9: 4, 10: 4},
    10: {1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3, 7: 3, 8: 3, 9: 3, 10: 4},
}

TO_HIT_CHART_RANGED = {1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1, 7: 0, 8: -1, 9: -2, 10: -3}

# rows: unit's strength, columns: target_toughness
TO_WOUND_CHART = {
    1: {1: 4, 2: 5, 3: 6, 4: 6, 5: 6, 6: 6, 7: 6, 8: 6, 9: 6, 10: 6},
    2: {1: 3, 2: 4, 3: 5, 4: 6, 5: 6, 6: 6, 7: 6, 8: 6, 9: 6, 10: 6},
    3: {1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 6, 7: 6, 8: 6, 9: 6, 10: 6},
    4: {1: 2, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 6, 8: 6, 9: 6, 10: 6},
    5: {1: 2, 2: 2, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 6, 9: 6, 10: 6},
    6: {1: 2, 2: 2, 3: 2, 4: 2, 5: 3, 6: 4, 7: 5, 8: 6, 9: 6, 10: 6},
    7: {1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 3, 7: 4, 8: 5, 9: 6, 10: 6},
    8: {1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 3, 8: 4, 9: 5, 10: 6},
    9: {1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 3, 9: 4, 10: 5},
    10: {1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 2, 9: 3, 10: 4},
}

# keys are armor types, values are required rolls
ARMOR_SAVES = {Bestiary.ARMOR_NONE: 7,
               Bestiary.ARMOR_LIGHT: 6,
               Bestiary.ARMOR_LIGHT_AND_SHIELD: 5,
               Bestiary.ARMOR_HEAVY: 5,
               Bestiary.ARMOR_HEAVY_AND_SHIELD: 4}

# keys are the attacking unit's strength
ARMOR_SAVE_MODIFIER = {1: 0, 2: 0, 3: 0, 4: -1, 5: -2, 6: -3, 7: -4, 8: -5, 9: -6, 10: -7}

WARD_SAVES = {Bestiary.WARD_NONE: 7,
              Bestiary.WARD_SHIELD_CHARMED: 2,  # charmed shield is one use only
              Bestiary.WARD_SHIELD_ENCHANTED: 7,  # enchanted shield is counted in armor saving throw
              }


class ActionManager:

    def __init__(self, unit, action=None, targets=None):
        self.__unit = unit
        self.__action = action
        self.__targets = targets
        self.__finished = False  # action is finished

    def get_unit(self):
        return self.__unit

    def set_action(self, action: str):
        self.__action = action

    def get_action(self):
        return self.__action

    def set_targets(self, targets):
        if type(targets) is list:
            self.__targets = targets
        else:
            self.__targets = [targets]

    def get_targets(self):
        return self.__targets

    def is_ready(self):
        if self.__finished:
            # action already finished
            return False

        if self.__unit is not None and self.__action is not None and self.__targets is not None:
            # if all parameters are different than None, the action is ready
            return True
        else:
            return False

    def get_roll_to_hit_close_combat(self, target) -> bool:
        print("Rolling to hit:")
        roll = Rolls.get_d6_roll()
        if roll == 6:
            print("Target hit!")
            return True
        elif roll == 1:
            print("Missed target!")
            return False
        else:
            ws = self.__unit.get_weapon_skill()
            target_ws = target.get_weapon_skill()
            required_roll = TO_HIT_CHART_CLOSE_COMBAT[ws][target_ws]
            if roll >= required_roll:
                print("Target hit!")
                return True
        print("Missed target!")
        return False

    # noinspection PyUnusedLocal
    def get_roll_to_hit_ranged(self, target) -> bool:
        # TODO: target might be behind cover
        print("Rolling to hit:")
        roll = Rolls.get_d6_roll()
        if roll == 6:
            print("Target hit!")
            return True
        elif roll == 1:
            print("Missed target!")
            return False
        else:
            bs = self.__unit.get_ballistic_skill()
            required_roll = TO_HIT_CHART_RANGED[bs]
            if roll >= required_roll:
                print("Target hit!")
                return True
        print("Missed target!")
        return False

    def get_roll_to_wound(self, target) -> bool:
        print("Rolling to wound:")
        roll = Rolls.get_d6_roll()
        if roll == 6:
            print("Target wounded!")
            return True
        elif roll == 1:
            print("Hit bounced off target!")
            return False
        else:
            s = self.__unit.get_strength()
            target_t = target.get_toughness()
            required_roll = TO_WOUND_CHART[s][target_t]
            if roll >= required_roll:
                print("Target wounded!")
                return True
        print("Hit bounced off target!")
        return False

    def get_armor_saving_throw(self, target) -> bool:
        print("Target rolling to armor save:")
        roll = Rolls.get_d6_roll()
        if roll == 1:
            print("Target armor save throw failed")
            return False
        else:
            s = self.__unit.get_strength()
            target_armor = target.get_armor()
            target_wards = target.get_wards()

            required_roll = ARMOR_SAVES[target_armor]  # the required target roll to be saved by the armor

            if Bestiary.WARD_SHIELD_ENCHANTED in target_wards:
                required_roll -= 1

            armor_modifier = ARMOR_SAVE_MODIFIER[s]
            roll += armor_modifier  # the stronger the weapon, the lower the chance that the armor will block
            if roll >= required_roll:
                print("Target saved by armor!")
                return True
        print("Target armor save throw failed")
        return False

    # noinspection PyMethodMayBeStatic
    def get_ward_saving_throw(self, target) -> bool:
        print("Target rolling to ward save:")
        roll = Rolls.get_d6_roll()
        if roll == 1:
            print("Target save throw failed")
            return False
        else:
            target_wards = target.get_wards()  # always roll on the best ward, they don't accumulate
            # TODO: wards should be objects
            for ward in target_wards:
                if "ARMOR" in ward or "SHIELD" in ward or "TALISMAN" in ward:

                    if Bestiary.WARD_SHIELD_CHARMED in ward:
                        # charmed shield is single use only
                        target.remove_ward(ward)

                    required_roll = WARD_SAVES[ward]
                    if roll >= required_roll:
                        print("Target saved by armor!")
                        return True

        print("Target save throw failed")
        return False

    def perform_action(self):
        unit_type = self.__unit.get_unit_type()
        action = self.get_action()
        print("Perform Action: " + action)

        """ ATTACK """
        if action == Bestiary.ACTION_ATTACK:
            self.__unit.set_action("attack")

            """ CLOSE_COMBAT """
            if unit_type == Bestiary.UNIT_TYPE_MELEE:
                self.close_combat_attacks()

            elif unit_type == Bestiary.UNIT_TYPE_RANGE:
                self.range_attack()

            self.__finished = True

    def close_combat_attacks(self):
        number_of_attacks = self.__unit.get_attacks()
        for a in range(number_of_attacks):

            alive_targets = [x for x in self.__targets if not x.is_killed()]

            if not any(alive_targets):
                # if all targets eliminated return
                self.__finished = True
                return

            # target = self.__targets[0]  # 1st target
            target = alive_targets[0]  # get the first remaining alive target

            hit = self.get_roll_to_hit_close_combat(target)
            if hit:
                wound = self.get_roll_to_wound(target)
                if wound:
                    saved_by_armor = self.get_armor_saving_throw(target)
                    if not saved_by_armor:
                        saved_by_ward = self.get_ward_saving_throw(target)
                        if saved_by_ward:
                            continue
                        else:
                            target_wounds = target.get_wounds()
                            target.set_wounds(target_wounds - 1)

    def range_attack(self):
        if not any(self.__targets):
            # if all targets eliminated return
            return

        target = self.__targets[0]  # 1st target
        hit = self.get_roll_to_hit_close_combat(target)
        if hit:
            wound = self.get_roll_to_wound(target)
            if wound:
                saved_by_armor = self.get_armor_saving_throw(target)
                if not saved_by_armor:
                    saved_by_ward = self.get_ward_saving_throw(target)
                    if saved_by_ward:
                        return
                    else:
                        target_wounds = target.get_wounds()
                        target.set_wounds(target_wounds - 1)

    def is_finished(self):
        if self.__finished:
            if self.__unit.is_animation_cycle_done():
                self.__unit.set_action("idle")

                target = self.__targets[0]

                """ Animate targets death """
                for target in self.__targets:
                    if target.is_killed():
                        target.set_action("die")

                if target.is_animation_cycle_done():
                    self.__finished = False
                    return True
        else:
            return self.__finished
