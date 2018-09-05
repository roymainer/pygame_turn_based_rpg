from Shared import Rolls
from Shared.Action import Attack, RangeAttack
from Shared.GameConstants import GameConstants
from Shared.Skill import Skill
from Shared.Spell import Spell
from UI.TextFloating import TextFloating

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

    # def __init__(self, model, action=None, targets=None):
    def __init__(self, turn_manager):
        self.__turn_manager = turn_manager
        # self.__model = model
        # self.__action = action
        # self.__targets = targets
        self.__action = None
        self.__targets = None
        self.__finished = False  # action is finished
        self.__texts = []

    def get_current_model(self):
        return self.__turn_manager.get_current_model()

    def get_turn_manager(self):
        return self.__turn_manager

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

        if self.get_current_model() is not None and self.__action is not None and self.__targets is not None:
            # if all parameters are different than None, the action is ready
            return True
        else:
            return False

    def perform_action(self):
        action = self.get_action()
        print("Perform Action: " + action.get_name())

        if isinstance(action, Attack):
            self.__close_combat_attacks()
        elif isinstance(action, RangeAttack):
            self.__range_attack()
        elif isinstance(action, Skill):
            self.__skill()
        elif isinstance(action, Spell):
            self.__cast()

        self.__clear_special_rules()  # clear any used up special rules

        self.__finished = True

    def is_finished(self):
        if self.__finished:  # if action is finished
            current_model = self.get_current_model()
            if current_model.is_animation_cycle_done():  # if the model finished it's action animation cycle

                """ Animate targets death """
                all_models = self.__turn_manager.get_all_models_list()
                target = None
                for model in all_models:
                    if model.is_killed():
                        model.set_action("die")  # animate death on all killed models
                        target = model
                    else:
                        model.set_action("idle")  # return all remaining models to idle state

                # current_model.set_action("idle")
                # target = self.__targets[0]
                #
                # for target in self.__targets:
                #     if target.is_killed():
                #         target.set_action("die")
                    # else:
                    #     target.set_action('idle')

                if target is None:
                    self.__finished = False  # reset the finish flag for next action
                    return True
                elif target.is_animation_cycle_done():
                    # wait for death animation to finish before continuing
                    self.__finished = False  # reset the finish flag for next action
                    return True  # return True cause animation also finished
        else:
            return self.__finished

    def set_texts(self, texts):
        self.__texts = texts

    def get_texts(self):
        return self.__texts

    def reset_action(self):
        for text in self.__texts:
            text.kill()

        self.__texts = []
        self.__targets = None
        self.__action = None

        return

    def wound_target(self, target, strength=4, armor_saves_allowed=False, double_effect=False):
        target.set_action("hurt")
        print("Rolling to wound:")
        roll = Rolls.get_d6_roll()
        if roll == 6:
            print("Target wounded!")
        elif roll == 1:
            print("Failed to wound target!")
            self.__add_text_blocked(target)
            return
        else:
            toughness = target.get_toughness()
            required_roll = TO_WOUND_CHART[strength][toughness]
            print("Required roll to wound: " + str(required_roll))
            if roll >= required_roll:
                print("Target wounded!")
            else:
                print("Failed to wound target!")
                self.__add_text_blocked(target)
                return

        if armor_saves_allowed:
            print("Target rolling to armor save:")
            roll = Rolls.get_d6_roll()
            if roll == 1:
                print("Target armor save throw failed")
            else:
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

                required_roll -= ARMOR_SAVE_MODIFIER[strength]  # Model/Weapon strength negates the armor save
                print("Required roll for armor save: " + str(required_roll))

                if roll >= required_roll:
                    print("Target armor save throw failed")
                    self.__add_text_blocked(target)
                    return

        saved_by_ward = self.__get_ward_saving_throw(target)
        if saved_by_ward:
            print("Target saved by ward!")
            self.__add_text_saved_by_ward(target)
            return

        target_wounds = target.get_current_wounds()
        if double_effect:
            print("Double damage!")
            wounds = 2
        else:
            wounds = 1
        self.__add_text_hit(target)
        target.set_wounds(target_wounds - wounds)
        return

    def __close_combat_attacks(self):
        current_model = self.get_current_model()
        number_of_attacks = current_model.get_attacks()
        for a in range(number_of_attacks):

            alive_targets = [x for x in self.__targets if not x.is_killed()]

            if not any(alive_targets):
                # if all targets eliminated return
                self.__finished = True
                return
            print("---------- ATTACK#{}/{} ----------".format(str(a+1), str(number_of_attacks)))

            current_model.set_action("attack")

            target = alive_targets[0]  # get the first remaining alive target
            target.set_action("hurt")

            hit = self.__get_roll_to_hit_close_combat(target)
            if not hit:
                # look for any re-roll to hit special rule the model has
                print(current_model.get_special_rules_list())
                for sr in current_model.get_special_rules_list():
                    if sr.re_roll_to_hit(target):
                        hit = self.__get_roll_to_hit_close_combat(target)
                        if hit:
                            print("Successfully re-rolled to hit with: {}".format(sr.get_name()))
                            break
            if hit:
                wound, killing_blow = self.__get_roll_to_wound(target)
                if not wound:
                    # look for an re-roll to wound special rule the model has
                    for sr in current_model.get_special_rules_list():
                        if sr.re_roll_to_wound(target, Attack):
                            wound, killing_blow = self.__get_roll_to_wound(target)
                            if wound:
                                print("Successfully re-rolled to wound with: {}".format(sr.get_name()))
                                break
                if wound and killing_blow:
                    # saved_by_ward = self.get_ward_saving_throw(target)
                    saved_by_ward = False
                    if saved_by_ward:
                        self.__add_text_saved_by_ward(target)
                        continue
                    else:
                        target.set_wounds(0)
                        self.__add_text("Killing Blow!", GameConstants.BRIGHT_RED, target)
                elif wound:
                    saved_by_armor = self.__get_armor_saving_throw(target)
                    if not saved_by_armor:
                        # TODO: return the wards
                        # saved_by_ward = self.get_ward_saving_throw(target)
                        saved_by_ward = False
                        if saved_by_ward:
                            self.__add_text_saved_by_ward(target)
                            continue
                        else:
                            self.__add_text_hit(target)
                            target_wounds = target.get_current_wounds()
                            weapon = current_model.get_melee_weapon()
                            double_damage = self.__is_double_damage(current_model, weapon, target)
                            if double_damage:
                                target.set_wounds(target_wounds - 2)
                            else:
                                target.set_wounds(target_wounds - 1)

                    else:
                        self.__add_text_blocked(target)
                else:
                    self.__add_text_blocked(target)
            else:
                self.__add_text_miss(target)

    def __range_attack(self):
        alive_targets = [x for x in self.__targets if not x.is_killed()]

        if not any(alive_targets):
            # if all targets eliminated return
            self.__finished = True
            return

        current_model = self.get_current_model()
        current_model.set_action("shoot")
        target = self.__targets[0]  # 1st target
        target.set_action("hurt")

        hit = self.__get_roll_to_hit_ranged(target)
        if hit:
            wound, killing_blow = self.__get_roll_to_wound(target)
            if wound and killing_blow:
                saved_by_ward = self.__get_ward_saving_throw(target)
                if saved_by_ward:
                    return
                else:
                    # killing blow ignores any armor save BUT NOT WARD SAVES
                    target.set_wounds(0)
                    self.__add_text("Killing Blow!", GameConstants.BRIGHT_RED, target)
            elif wound:
                saved_by_armor = self.__get_armor_saving_throw(target)
                if not saved_by_armor:
                    # saved_by_ward = self.get_ward_saving_throw(target)
                    # if saved_by_ward:
                    #     return
                    # else:
                    self.__add_text_hit(target)
                    target_wounds = target.get_wounds()
                    weapon = current_model.get_range_weapon()
                    double_damage = self.__is_double_damage(current_model, weapon, target)
                    if double_damage:
                        target.set_wounds(target_wounds - 2)
                    else:
                        target.set_wounds(target_wounds - 1)

    def __skill(self):

        current_model = self.get_current_model()
        current_model.set_action("cast")

        skill = self.__action
        self.__add_text(string=skill.get_name(), text_color=GameConstants.CYAN, target=current_model)
        skill.on_click(current_model, self.__targets)

    def __cast(self):
        current_model = self.get_current_model()
        current_model.set_action("cast")

        spell = self.__action
        self.__add_text(string=spell.get_name(), text_color=GameConstants.CYAN, target=current_model)
        spell.on_click(self)

    def __get_roll_to_hit_close_combat(self, target) -> bool:
        print("Rolling to hit:")
        roll = Rolls.get_d6_roll()
        if roll == 6:
            print("Target hit!")
            return True
        elif roll == 1:
            print("Missed target!")
            return False
        else:
            current_model = self.get_current_model()
            ws = current_model.get_weapon_skill()
            target_ws = target.get_weapon_skill()
            required_roll = TO_HIT_CHART_CLOSE_COMBAT[ws][target_ws]
            print("Required roll to hit: " + str(required_roll))
            if roll >= required_roll:
                print("Target hit!")
                return True
        print("Missed target!")
        return False

    # noinspection PyUnusedLocal
    def __get_roll_to_hit_ranged(self, target) -> bool:
        # TODO: target might be behind cover
        print("Rolling to hit:")
        roll = Rolls.get_d6_roll()
        if roll == 6:
            print("Target hit!")
            return True
        elif roll == 1:
            # self.__add_text_miss(target)
            print("Missed target!")
            return False
        else:
            current_model = self.get_current_model()
            bs = current_model.get_ballistic_skill()
            required_roll = TO_HIT_CHART_RANGED[bs]
            print("Required roll to hit: " + str(required_roll))
            if roll >= required_roll:
                print("Target hit!")
                return True
        # self.__add_text_miss(target)
        print("Missed target!")
        return False

    def __get_roll_to_wound(self, target) -> (bool, bool):
        print("Rolling to wound:")
        current_model = self.get_current_model()
        roll = Rolls.get_d6_roll()
        if roll == 6:
            print("Target wounded!")
            for sr in current_model.get_special_rules_list():
                if sr.is_killing_blow(target):
                    print("Killing Blow!")
                    return True, True
            return True, False
        elif roll == 1:
            print("Failed to wound target!")
            # self.__add_text_blocked(target)
            return False, False
        else:
            s = current_model.get_strength()
            for sr in current_model.get_special_rules_list():
                # get any strength bonus special rule the model has
                s += sr.get_strength_bonus()
            target_t = target.get_toughness()
            required_roll = TO_WOUND_CHART[s][target_t]
            print("Required roll to wound: " + str(required_roll))
            if roll >= required_roll:
                print("Target wounded!")
                return True, False
        # self.__add_text_blocked(target)
        print("Failed to wound target!")
        return False, False

    def __get_armor_saving_throw(self, target) -> bool:
        print("Target rolling to armor save:")
        roll = Rolls.get_d6_roll()
        if roll == 1:
            print("Target armor save throw failed")
            return False
        else:
            current_model = self.get_current_model()
            s = current_model.get_strength()
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

            required_roll -= ARMOR_SAVE_MODIFIER[s]  # Model/Weapon strength negates the armor save
            print("Required roll for armor save: " + str(required_roll))

            if roll >= required_roll:
                # self.__add_text_blocked(target)
                return True
        print("Target armor save throw failed")
        return False

    # noinspection PyMethodMayBeStatic
    def __get_ward_saving_throw(self, target) -> bool:
        print("Target rolling to ward save:")

        # TODO: finish ward saving throw
        print("Incomplete code!")
        return False

        # roll = Rolls.get_d6_roll()
        # if roll == 1:
        #     print("Target save throw failed")
        #     return False
        # else:
        #     target_wards = target.get_wards()  # always roll on the best ward, they don't accumulate
        #     # TODO: wards should be objects
        #     for ward in target_wards:
        #         if "ARMOR" in ward or "SHIELD" in ward or "TALISMAN" in ward:
        #
        #             if Bestiary.WARD_SHIELD_CHARMED in ward:
        #                 # charmed shield is single use only
        #                 target.remove_ward(ward)
        #
        #             required_roll = WARD_SAVES[ward]
        #             if roll >= required_roll:
        #                 print("Target saved by armor!")
        #                 return True
        #
        # print("Target save throw failed")
        # return False

    def __add_text(self, string, text_color, target):
        target_position = target.get_position()
        target_size = target.get_size()
        text = TextFloating(string, (0, 0), text_color, None, 28)
        text_size = text.get_size()

        # place beside the target
        # x = target_position[0] - int(text_size[0]) - 10,
        # y = target_position[1] + int(target_size[1]) / 2 - int(text_size[1]) / 2

        # place below the target or below previous text
        # x = target_position[0] + int(target_size[0]/2) - text_size[0]/
        if target_position[0] > int(GameConstants.SCREEN_SIZE[0]/2):
            x = target_position[0] - text_size[0] - 2
        else:
            x = target_position[0] + target_size[0] + 2

        if any(self.__texts):
            prev_text = self.__texts[-1]  # get previous text
            y = prev_text.get_position()[1]
            height = prev_text.get_size()[1]
            y = y + height + 10
        else:
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

    def __add_text_saved_by_ward(self, target):
        self.__add_text("Saved by ward", GameConstants.BRIGHT_YELLOW, target)

    def __clear_special_rules(self):
        current_model = self.get_current_model()
        current_model.clear_used_up_special_rules()
        for target in self.__targets:
            target.clear_used_up_special_rules()

    def __is_double_damage(self, model, weapon, target):

        flaming_attack = False
        flammable = False

        for sr in model.get_special_rules_list():
            if sr.is_flaming_attack():
                flaming_attack = True

        for sr in weapon.get_special_rules_list():
            if sr.is_flaming_attack():
                flaming_attack = True

        for sr in target.get_special_rules_list():
            if sr.is_flammable():
                flammable = True

        if flaming_attack and flammable:
            return True
