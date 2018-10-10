import pygame
from Managers.Manager import Manager, EVENTS_MANAGER
from Shared.Action import RangeAttack, Attack, Skills, Spells, Items, Skip
from Shared.GameConstants import GameConstants
import logging

from Shared.UIConstants import UIConstants
from UI.Text import Text

logger = logging.getLogger().getChild(__name__)


# noinspection PyMethodMayBeStatic
class EventsManager(Manager):

    def __init__(self, scene):
        self.__battle_is_over = False
        self.__clicked_to_continue = False
        self.__texts = []

        super(EventsManager, self).__init__(scene, EVENTS_MANAGER)

    def handle_events(self):

        if not self.acquire_lock(__name__):
            return

        # check if battle is over
        if not self.__battle_is_over:
            self.is_battle_over()

        if self.__clicked_to_continue:
            return True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logger.info("Quit")
                exit()
            if event.type == pygame.KEYDOWN:

                ui_manager = self.get_ui_manager()

                if event.key == pygame.K_ESCAPE:
                    ui_manager.return_to_previous_menu()

                if event.key == pygame.K_UP:
                    ui_manager.move_pointer_up()
                if event.key == pygame.K_DOWN:
                    ui_manager.move_pointer_down()

                if event.key == pygame.K_RETURN:
                    self.__menu_item_pressed()

                if event.key == pygame.K_RIGHT:
                    # ui_manager.menu_item_pressed(right=True)
                    self.__increase_dice(ui_manager)
                if event.key == pygame.K_LEFT:
                    # ui_manager.menu_item_pressed(left=True)
                    self.__decrease_dice(ui_manager)

    def __menu_item_pressed(self):
        ui_manager = self.get_ui_manager()
        models_manager = self.get_models_manager()

        ui_manager.mark_selected_item()  # mark the item selected by the player when pressed Enter

        # ----------------- Player MODELS MENU ----------------- #
        if ui_manager.is_focused_on_player_models_menu():
            self.__select_player_model(ui_manager)

        # ----------------- ACTIONS MENU ----------------- #
        elif ui_manager.is_focused_on_actions_menu():
            self.__select_action(ui_manager)

        # ----------------- SKILLS MENU ----------------- #
        elif ui_manager.is_focused_on_skills_menu():
            self.__select_skill(ui_manager, models_manager)

        # ----------------- SPELLS MENU ----------------- #
        elif ui_manager.is_focused_on_spells_menu():
            self.__select_spell(ui_manager)

        # ----------------- SPELLS MENU ----------------- #
        elif ui_manager.is_focused_on_dispel_menu():
            self.__dispel_spell(ui_manager)

        # ----------------- ITEMS MENU ----------------- #
        elif ui_manager.is_focused_on_items_menu():
            self.__select_item(ui_manager)

        # ----------------- DICE CONTROLLER ----------------- #
        elif ui_manager.is_focused_on_dice_controller():
            self.__set_spell_power(ui_manager, models_manager)

        # ----------------- DISPEL DICE CONTROLLER ----------------- #
        elif ui_manager.is_focused_on_dispel_dice_controller():
            self.__set_dispel_power(ui_manager)

        # ----------------- COMPUTER MODELS MENU ----------------- #
        elif ui_manager.is_focused_on_computer_models_menu():
            self.__set_computer_targets(ui_manager)

        # ----------------- CONTINUE BUTTON ----------------- #
        elif ui_manager.is_focused_on_continue_button():
            self.__clicked_to_continue = True

    def __select_player_model(self, ui_manager):
        current_model = ui_manager.get_selected_player_model()
        current_model.reset_action()
        logger.info("Select model: {}".format(current_model.get_name()))
        ui_manager.add_actions_menu()
        ui_manager.set_focus_on_actions_menu()

    def __select_action(self, ui_manager):
        current_model = ui_manager.get_selected_player_model()
        action = ui_manager.get_focused_menu().get_selected_object()
        logger.info("Select action: {}".format(action.get_name()))

        if isinstance(action, Attack) or isinstance(action, RangeAttack):
            if isinstance(action, Attack):
                weapon = current_model.get_melee_weapon()
            else:
                weapon = current_model.get_ranged_weapon()

            weapon_action = weapon.get_action()
            valid_targets = weapon.get_valid_targets(current_model)
            current_model.set_action(weapon_action)
            ui_manager.set_focus_on_computer_menu(valid_targets)

        elif isinstance(action, Skills):
            ui_manager.add_skills_menu(current_model)

        elif isinstance(action, Spells):
            ui_manager.add_spells_menu(current_model)

        elif isinstance(action, Items):
            ui_manager.add_items_menu(current_model)

        elif isinstance(action, Skip):
            current_model.set_action(Skip())
            current_model.set_action_ready()  # mark as ready to perform
            ui_manager.set_focus_on_player_menu()
            ui_manager.move_pointer_down()  # continue to next model

    def __select_skill(self, ui_manager, models_manager):
        skill = ui_manager.get_focused_menu().get_selected_object()
        logger.info("Select skill: {}".format(skill.get_name()))

        current_model = ui_manager.get_selected_player_model()
        current_model.set_action(skill)

        valid_targets = skill.get_valid_targets()  # get valid targets from skill

        # if skill affects more than one computer model, no need to manually select a target
        if valid_targets in [GameConstants.TARGET_COMPUTER_ALL,
                             GameConstants.TARGET_COMPUTER_ALL_FRONT,
                             GameConstants.TARGET_COMPUTER_ALL_BACK]:
            targets = models_manager.get_valid_targets_models(valid_targets)
            current_model.set_targets(targets)
            current_model.set_action_ready()  # skill is ready to use
        else:
            ui_manager.set_focus_on_computer_menu(valid_targets)

    def __select_spell(self, ui_manager):
        spell = ui_manager.get_focused_menu().get_selected_object()
        logger.info("Select spell: {}".format(spell.get_name()))

        current_model = ui_manager.get_selected_player_model()
        current_model.set_action(spell)
        ui_manager.add_dice_controller()

    def __dispel_spell(self, ui_manager):
        spell = ui_manager.get_focused_menu().get_selected_object()
        logger.info("Dispel spell: {}".format(spell.get_name()))

        current_model = ui_manager.get_selected_player_model()
        dispel_action = current_model.get_action()  # get the dispel action
        dispel_action.set_spell(spell)  # assign the target spell to the dispel action

        ui_manager.add_dispel_dice_controller()

    def __select_item(self, ui_manager):
        item = ui_manager.get_focused_menu().get_selected_object()
        logger.info("Select item: {}".format(item.get_name()))

        current_model = ui_manager.get_selected_player_model()
        current_model.set_action(item)

    def __set_spell_power(self, ui_manager, models_manager):
        assigned_dice = ui_manager.get_dice()
        logger.info("Assign spell power to: {}".format(assigned_dice))

        # assign dice to spell
        current_model = ui_manager.get_selected_player_model()
        spell = current_model.get_action()
        spell.set_dice(assigned_dice)

        # update remaining player power pool
        magic_manager = self.get_magic_manager()
        ppp = magic_manager.get_player_power_pool()
        magic_manager.set_player_power_pool(ppp - assigned_dice)

        # destroy the dice controller
        ui_manager.destroy_dice_controller()

        valid_targets = spell.get_valid_targets()  # get valid targets from skill

        # assign targets to spell to continue
        if valid_targets in [GameConstants.TARGET_COMPUTER_ALL,
                             GameConstants.TARGET_COMPUTER_ALL_FRONT,
                             GameConstants.TARGET_COMPUTER_ALL_BACK]:
            # if no need to select any single target, assign targets to spell and cast
            targets = models_manager.get_valid_targets_models(valid_targets)
            current_model.set_targets(targets)
            current_model.set_action_ready()

            ui_manager.get_focused_menu().unmark_selected_item()
            ui_manager.remove_sub_menus()
            ui_manager.set_focus_on_player_menu()
            ui_manager.move_pointer_down()
        else:
            # proceed to computer models menu and select a target
            ui_manager.__set_focus_on_computer_menu(valid_targets)

    def __set_dispel_power(self, ui_manager):
        assigned_dice = ui_manager.get_dispel_dice()
        logger.info("Assign dice to dispel: {}".format(assigned_dice))

        # assign dispel dice to spell
        current_model = ui_manager.get_selected_player_model()
        spell = current_model.get_action().get_spell()
        spell.set_dispel_dice(assigned_dice)

        # update remaining player dispel pool
        magic_manager = self.get_magic_manager()
        pdp = magic_manager.get_player_dispel_pool()
        magic_manager.set_player_dispel_pool(pdp - assigned_dice)

        # destroy the dice controller
        ui_manager.destroy_dispel_dice_controller()

        # assign target to dispel (self)
        current_model.set_targets(self)
        current_model.set_action_ready()

        ui_manager.get_focused_menu().unmark_selected_item()
        ui_manager.remove_sub_menus()
        ui_manager.set_focus_on_player_menu()
        ui_manager.move_pointer_down()

    def __set_computer_targets(self, ui_manager):
        targets = ui_manager.get_focused_menu().get_selected_object()
        current_model = ui_manager.get_selected_player_model()
        current_model.set_targets(targets)
        current_model.set_action_ready()

        ui_manager.remove_computer_markers()
        ui_manager.get_focused_menu().unmark_selected_item()
        ui_manager.remove_sub_menus()
        ui_manager.set_focus_on_player_menu()
        ui_manager.move_pointer_down()

    def __increase_dice(self, ui_manager):
        if ui_manager.is_focused_on_dice_controller():
            ui_manager.increase_dice()

        elif ui_manager.is_focused_on_dispel_dice_controller():
            ui_manager.increase_dispel_dice()

    def __decrease_dice(self, ui_manager):
        if ui_manager.is_focused_on_dice_controller():
            ui_manager.decrease_dice()

        elif ui_manager.is_focused_on_dispel_dice_controller():
            ui_manager.decrease_dispel_dice()

    def is_battle_over(self):

        models_manager = self.get_models_manager()
        ui_manager = self.get_ui_manager()
        game_engine = self.get_game_engine()

        player_models = models_manager.get_player_sorted_models_list()
        alive_player_models = [x for x in player_models if not x.is_killed()]

        computer_models = models_manager.get_computer_sorted_models_list()
        alive_computer_models = [x for x in computer_models if not x.is_killed()]

        if not any(alive_player_models):
            # All Player models are dead, player lost!
            logger.info("All player models are killed, battle is lost!")
            text = Text("Battle is lost...", (0, 0), GameConstants.RED, None, UIConstants.FONT_SIZE_XLARGE)

        elif not any(alive_computer_models):
            # all computer models are dead, player won!
            # TODO: also need to check that there are no more computer models in the level
            logger.info("All computer models are killed, battle is won!")
            text = Text("Battle is won!", (0, 0), GameConstants.WHITE, None, UIConstants.FONT_SIZE_XLARGE)

        else:
            return

        self.__battle_is_over = True

        # update text position to replace UI MENUS
        position = (int(GameConstants.SCREEN_SIZE[0] / 2) - int(text.get_size()[0] / 2),
                    GameConstants.BATTLE_AREA_BOTTOM + int(text.get_size()[1]))
        text.set_position(position)

        ui_manager.destroy()  # clear the UI
        ui_manager.add_game_over_controls(posy=text.get_position()[1]+text.get_size()[1])  # add continue button
        self.__texts.append(text)  # add battle over text to list
        game_engine.add_sprite_to_group(text)

        return

    def get_is_battle_over(self):
        return self.__battle_is_over
