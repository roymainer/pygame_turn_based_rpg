import Rolls
from Shared import Bestiary
from Shared.GameConstants import GameConstants
from UI.Text import Text

""" Key (model_ws) : value (dict : key (enemy_ws) : value (dice roll to hit)) """
# rows: model's weapon skill, columns: target's weapon skill
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

# rows: model's strength, columns: target_toughness
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
# ARMOR_SAVES = {Bestiary.ARMOR_NONE: 7,
#                Bestiary.ARMOR_LIGHT: 6,
#                Bestiary.ARMOR_LIGHT_AND_SHIELD: 5,
#                Bestiary.ARMOR_HEAVY: 5,
#                Bestiary.ARMOR_HEAVY_AND_SHIELD: 4}

# keys are the attacking model's strength
ARMOR_SAVE_MODIFIER = {1: 0, 2: 0, 3: 0, 4: -1, 5: -2, 6: -3, 7: -4, 8: -5, 9: -6, 10: -7}


class ActionManager:

    def __init__(self, model, action=None, targets=None):
        self.__model = model
        self.__action = action
        self.__targets = targets
        self.__finished = False  # action is finished
        self.__texts = []

    def get_model(self):
        return self.__model

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

        if self.__model is not None and self.__action is not None and self.__targets is not None:
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
            self.__add_text_miss(target)
            print("Missed target!")
            return False
        else:
            ws = self.__model.get_weapon_skill()
            target_ws = target.get_weapon_skill()
            required_roll = TO_HIT_CHART_CLOSE_COMBAT[ws][target_ws]
            print("Required roll to hit: " + str(required_roll))
            if roll >= required_roll:
                print("Target hit!")
                return True
        self.__add_text_miss(target)
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
            self.__add_text_miss(target)
            print("Missed target!")
            return False
        else:
            bs = self.__model.get_ballistic_skill()
            required_roll = TO_HIT_CHART_RANGED[bs]
            print("Required roll to hit: " + str(required_roll))
            if roll >= required_roll:
                print("Target hit!")
                return True
        self.__add_text_miss(target)
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
            self.__add_text_blocked(target)
            return False
        else:
            s = self.__model.get_strength()
            target_t = target.get_toughness()
            required_roll = TO_WOUND_CHART[s][target_t]
            print("Required roll to wound: " + str(required_roll))
            if roll >= required_roll:
                print("Target wounded!")
                return True
        self.__add_text_blocked(target)
        print("Hit bounced off target!")
        return False

    def get_armor_saving_throw(self, target) -> bool:
        print("Target rolling to armor save:")
        roll = Rolls.get_d6_roll()
        if roll == 1:
            print("Target armor save throw failed")
            return False
        else:
            s = self.__model.get_strength()
            target_armor = target.get_armor()
            target_shield = target.get_shield()

            if target_armor is None:
                armor_req_roll = 7
            else:
                armor_req_roll = target_armor.get_required_roll()

            if target_shield is None:
                shield_save_modifier = 0
            else:
                shield_save_modifier = target_shield.get_shield_save_modifier()

            # the required target roll to be saved by the armor
            required_roll = armor_req_roll + shield_save_modifier
            print("Required roll for armor save: " + str(required_roll))

            armor_modifier = ARMOR_SAVE_MODIFIER[s]  # Model/Weapon strength negates the armor save
            roll += armor_modifier
            print("Roll + Strength Modifier: " + str(roll))
            if roll >= required_roll:
                self.__add_text_blocked(target)
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
        model_type = self.__model.get_model_type()
        action = self.get_action()
        print("Perform Action: " + action)

        """ ATTACK """
        if action == Bestiary.ACTION_ATTACK:
            self.__model.set_action("attack")

            """ CLOSE_COMBAT """
            if model_type == Bestiary.MODEL_TYPE_MELEE:
                self.close_combat_attacks()

            elif model_type == Bestiary.MODEL_TYPE_RANGE:
                self.range_attack()

            self.__finished = True

    def close_combat_attacks(self):
        number_of_attacks = self.__model.get_attacks()
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
                            self.__add_text_hit(target)
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
                        self.__add_text_hit(target)
                        target_wounds = target.get_wounds()
                        target.set_wounds(target_wounds - 1)

    def is_finished(self):
        if self.__finished:
            if self.__model.is_animation_cycle_done():
                self.__model.set_action("idle")

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

    def __add_text(self, string, text_color, target):
        target_position = target.get_position()
        target_size = target.get_size()
        text = Text(string, (0, 0), text_color, None, 28)
        text_size = text.get_size()

        # place beside the target
        # x = target_position[0] - int(text_size[0]) - 10,
        # y = target_position[1] + int(target_size[1]) / 2 - int(text_size[1]) / 2

        # place below the target
        x = target_position[0] + int(target_size[0]/2) - text_size[0]/2
        y = target_position[1] + int(target_size[1]) - int(text_size[1]) / 2

        new_position = (x, y)
        text.set_position(new_position)
        self.__texts.append(text)

    def __add_text_miss(self, target):
        self.__add_text("Miss", GameConstants.BRIGHT_YELLOW, target)

    def __add_text_hit(self, target):
        self.__add_text("Hit", GameConstants.BRIGHT_YELLOW, target)

    def __add_text_blocked(self, target):
        self.__add_text("Blocked", GameConstants.BRIGHT_YELLOW, target)

    def set_texts(self, texts):
        self.__texts = texts

    def get_texts(self):
        return self.__texts

    def destroy(self):
        for text in self.__texts:
            text.kill()
