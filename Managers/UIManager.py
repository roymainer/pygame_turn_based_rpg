import pygame

from Shared.Action import Skip
from Shared.AnimatedObject import AnimatedObject
from Shared.GameConstants import *
from Shared.Model import ACTION_ATTACK, ACTION_SPELLS, ACTION_SKILLS, ACTION_SHOOT, ACTION_SKIP  # ACTION_ITEMS
from Shared.UIConstants import UIConstants
from UI.Menu import Menu
from UI.MenuPointer import MenuPointer
from UI.ModelsMenu import ModelsMenu

PLAYER_MODELS_MENU = 0
COMPUTER_MODELS_MENU = 1
ACTIONS_MENU = 2
SPELLS_MENU = 3
ITEMS_MENU = 4
SKILLS_MENU = 5

UP = 0
DOWN = 1


# noinspection PyTypeChecker,PyUnboundLocalVariable
class UIManager:

    def __init__(self, scene):
        self.__scene = scene
        self.__menus = {PLAYER_MODELS_MENU: None,
                        COMPUTER_MODELS_MENU: None,
                        ACTIONS_MENU: None,
                        SKILLS_MENU: None,
                        SPELLS_MENU: None,
                        ITEMS_MENU: None}

        self.__player_markers = []
        self.__computer_markers = []
        self.__pointer = MenuPointer()

    def on_init(self):
        self.__add_player_models_menu()
        self.__add_computers_models_menu()
        self.set_focus_on_player_menu()

    # def update(self):
    #     turn_manager = self.__scene.get_turn_manager()
    #
    #     current_model = turn_manager.get_current_model()
    #     self.__add_marker(current_model)

    # -------- Menus -------- #
    def menu_item_pressed(self):
        mm = self.__scene.get_models_manager()

        focused_menu = self.__get_focused_menu()
        focused_menu.get_selected_item().mark_string()  # mark the selected text
        # current_model = self.__scene.get_turn_manager().get_current_model()
        current_model = self.__menus[PLAYER_MODELS_MENU].get_selected_object()

        # ----------------- ACTIONS MENU ----------------- #
        if focused_menu == self.__menus[ACTIONS_MENU]:
            action_string = focused_menu.get_selected_item().get_string()  # get selected action string

            if action_string == ACTION_ATTACK or action_string == ACTION_SHOOT:
                if action_string == ACTION_SHOOT:
                    weapon = current_model.get_ranged_weapon()
                else:
                    weapon = current_model.get_melee_weapon()

                action = weapon.get_action()
                valid_targets = weapon.get_valid_targets(current_model)
                current_model.set_action(action)
                self.set_computers_menu(valid_targets)

            elif action_string == ACTION_SKILLS:
                self.add_skills_menu(current_model)
                self.__set_focused_menu(self.__menus[SKILLS_MENU])

            elif action_string == ACTION_SPELLS:
                self.add_spells_menu(current_model)
                self.__set_focused_menu(self.__menus[SPELLS_MENU])

            elif action_string == ACTION_SKIP:
                current_model.set_action(Skip())
                current_model.set_targets(current_model)
                self.set_focus_on_player_menu()
                self.move_pointer_down()

        # ----------------- SKILLS/SPELLS MENU ----------------- #
        if focused_menu == self.__menus[SKILLS_MENU] or focused_menu == self.__menus[SPELLS_MENU]:
            actions_list = []
            if focused_menu == self.__menus[SKILLS_MENU]:
                actions_list = current_model.get_skills_list()
            elif focused_menu == self.__menus[SPELLS_MENU]:
                actions_list = current_model.get_spells_list()

            string = focused_menu.get_selected_item().get_string()  # get the selected skill string

            # get the models selected skill
            for action in actions_list:
                if action.get_name() == string:
                    break

            current_model.set_action(action)

            valid_targets = action.get_valid_targets()  # get valid targets from skill

            if valid_targets in [TARGET_COMPUTER_ALL, TARGET_COMPUTER_ALL_FRONT, TARGET_COMPUTER_ALL_BACK]:
                targets = mm.get_valid_targets_models(valid_targets)
                current_model.set_targets(targets)
            else:
                self.set_computers_menu(valid_targets)

        # ----------------- COMPUTER MODELS MENU ----------------- #
        if focused_menu == self.__menus[COMPUTER_MODELS_MENU]:
            targets = self.__menus[COMPUTER_MODELS_MENU].get_selectd_model()
            current_model.set_targets(targets)
            self.remove_computer_markers()
            self.__remove_sub_menus()
            # self.__set_focused_menu(self.__menus[ACTIONS_MENU])
            self.set_focus_on_player_menu()
            self.move_pointer_down()

        # ----------------- Player MODELS MENU ----------------- #
        if focused_menu == self.__menus[PLAYER_MODELS_MENU]:
            self.add_actions_menu()
            # noinspection PyTypeChecker
            self.__set_focused_menu(self.__menus[ACTIONS_MENU])

    def return_to_previous_menu(self):
        # self.__set_focused_menu(menu=self.__menus[ACTIONS_MENU])
        self.set_focus_on_player_menu()
        self.__remove_sub_menus()
        return

    def update_all_menus(self):
        phase_manager = self.__scene.get_phase_manager()

        if self.__menus[PLAYER_MODELS_MENU] is None:
            self.__add_player_models_menu()
        else:
            player_models = phase_manager.get_current_phase_player_models_list()
            self.__menus[PLAYER_MODELS_MENU].update_menu(self.__scene.get_game_engine(), player_models)

        if self.__menus[COMPUTER_MODELS_MENU] is None:
            self.__add_computers_models_menu()
        else:
            computer_models = phase_manager.get_current_phase_computer_models_list()
            self.__menus[COMPUTER_MODELS_MENU].update_menu(self.__scene.get_game_engine(), computer_models)

        self.add_actions_menu()
        self.set_focus_on_player_menu()

        return

    def add_actions_menu(self):
        if self.__menus[ACTIONS_MENU] is not None:
            self.__menus[ACTIONS_MENU].kill()  # delete the menu from any of it's groups
            self.__menus[ACTIONS_MENU] = None

        player_menu_size = self.__menus[PLAYER_MODELS_MENU].get_size()
        computer_menu_size = self.__menus[COMPUTER_MODELS_MENU].get_size()

        menu_size = (SCREEN_SIZE[0] - player_menu_size[0] - computer_menu_size[0],
                     player_menu_size[1])

        menu_actions_list = self.__scene.get_phase_manager().get_current_phase_actions_list()

        menu_position = (self.__menus[PLAYER_MODELS_MENU].get_rect().right, BATTLE_AREA_BOTTOM)
        menu = Menu(UIConstants.SPRITE_BLUE_MENU, menu_size, menu_actions_list, menu_position)

        game_engine = self.__scene.get_game_engine()
        # add menu,  menu items and pointer to game engine sprites group
        game_engine.add_sprite_to_group(menu)
        for i in range(menu.get_menu_items_count()):
            game_engine.add_sprite_to_group(menu.get_item_from_menu(i))

        menu.set_name("Actions Menu")

        # noinspection PyTypeChecker
        self.__menus[ACTIONS_MENU] = menu
        self.__set_focused_menu(menu)
        # self.__pointer.assign_pointer_to_menu(menu)

    def remove_actions_menu(self):
        self.__menus[ACTIONS_MENU].kill()  # remove the actions menu

    def add_skills_menu(self, model):
        skills_list = model.get_skills_list()
        self.__add_menu(SKILLS_MENU, skills_list)

    def add_spells_menu(self, model):
        spells_list = model.get_spells_list()
        self.__add_menu(SPELLS_MENU, spells_list)

    def add_items_menu(self, model):
        items_list = model.get_items_list()
        self.__add_menu(ITEMS_MENU, items_list)

    def __add_menu(self, menu_key, menu_items_list):

        menus_dict = {SKILLS_MENU: "Skills Menu", SPELLS_MENU: "Spells Menu", ITEMS_MENU: "Items Menu"}

        # delete either of these menus before adding a new one
        for menu in menus_dict.keys():
            if self.__menus[menu] is not None:
                self.__menus[menu].kill()  # delete the menu from any of it's groups
                self.__menus[menu] = None

        computer_menu = self.__menus[COMPUTER_MODELS_MENU]
        actions_menu = self.__menus[ACTIONS_MENU]

        menu_size = (int(actions_menu.get_size()[0]*3/4), actions_menu.get_size()[1])

        menu_position = (computer_menu.get_rect().left - int(menu_size[0]), BATTLE_AREA_BOTTOM)

        menu = Menu(UIConstants.SPRITE_BLUE_MENU, menu_size, menu_items_list, menu_position)

        game_engine = self.__scene.get_game_engine()
        game_engine.add_sprite_to_group(menu)
        for i in range(menu.get_menu_items_count()):
            game_engine.add_sprite_to_group(menu.get_item_from_menu(i))
        # self.__pointer.assign_pointer_to_menu(menu)

        menu.set_name(menus_dict[menu_key])

        self.__menus[menu_key] = menu

    def __set_focused_menu(self, menu):
        # remove focus from all other menus
        for _menu in self.__menus.values():
            if _menu is None:
                continue
            else:
                _menu.unset_focused()

        menu.set_focused()
        selected_item = menu.get_selected_item()
        if selected_item is None:
            return

        selected_item.unmark_string()  # unmark selected option text
        # verify that the pointer is on the front layer
        game_engine = self.__scene.get_game_engine()
        game_engine.remove_sprite_from_group(self.__pointer)  # remove from list
        game_engine.add_sprite_to_group(self.__pointer)  # return to list at higher layer
        self.__pointer.assign_pointer_to_menu(menu)
        return

    def set_focus_on_player_menu(self):
        menu = self.__menus[PLAYER_MODELS_MENU]
        self.__set_focused_menu(menu)

    def __get_focused_menu(self) -> Menu:
        focused_menu = self.__menus[ACTIONS_MENU]  # default
        for menu in self.__menus.values():
            if menu is None:
                continue
            if menu.is_focused():
                focused_menu = menu
                break
        return focused_menu

    def __add_player_models_menu(self):
        if self.__menus[PLAYER_MODELS_MENU] is not None:
            self.__menus[PLAYER_MODELS_MENU].kill()
            self.__menus[PLAYER_MODELS_MENU] = None

        menu_size = (PLAYER_UNITS_MENU_WIDTH,
                     SCREEN_SIZE[1] - BATTLE_AREA_BOTTOM)

        characters_list = []
        phase_manager = self.__scene.get_phase_manager()
        player_models = phase_manager.get_current_phase_player_models_list()
        for scene_object in player_models:
            if scene_object.get_type() == PLAYER_OBJECT:
                characters_list.append(scene_object)
        menu_position = (0, BATTLE_AREA_BOTTOM)
        menu = ModelsMenu(UIConstants.SPRITE_BLUE_MENU, menu_size, characters_list, menu_position)

        # add menu,  menu items and pointer to game engine sprites group
        self.__scene.get_game_engine().add_sprite_to_group(menu)
        for i in range(menu.get_menu_items_count()):
            self.__scene.get_game_engine().add_sprite_to_group(menu.get_item_from_menu(i))
        # self.get_game().add_sprite_to_group(menu.get_pointer())

        menu.set_name("Player Models Menu")

        self.__menus[PLAYER_MODELS_MENU] = menu

    def __add_computers_models_menu(self, valid_targets=TARGET_COMPUTER_ALL):
        if self.__menus[COMPUTER_MODELS_MENU] is not None:
            self.__menus[COMPUTER_MODELS_MENU].kill()
            self.__menus[COMPUTER_MODELS_MENU] = None

        menu_size = (COMPUTER_MODELS_MENU_WIDTH,
                     SCREEN_SIZE[1] - BATTLE_AREA_BOTTOM)

        characters_list = []
        # phase_manager = self.__scene.get_phase_manager()
        models_manager = self.__scene.get_models_manager()
        computer_models = models_manager.get_computer_sorted_models_list()
        for model in computer_models:
            if model.is_valid_target(valid_targets):
                characters_list.append(model)
        menu_position = (COMPUTER_FRONT_COLUMN - PADX, BATTLE_AREA_BOTTOM)
        menu = ModelsMenu(UIConstants.SPRITE_BLUE_MENU, menu_size, characters_list, menu_position)

        # add menu,  menu items and pointer to game engine sprites group
        self.__scene.get_game_engine().add_sprite_to_group(menu)
        for i in range(menu.get_menu_items_count()):
            self.__scene.get_game_engine().add_sprite_to_group(menu.get_item_from_menu(i))
        # self.get_game().add_sprite_to_group(menu.get_pointer())

        menu.set_name("Computer Models Menu")

        self.__menus[COMPUTER_MODELS_MENU] = menu

    def move_pointer_up(self):
        self.__move_pointer(UP)
        mm = self.__scene.get_models_manager()
        if self.__menus[COMPUTER_MODELS_MENU].is_focused():
            index = self.__menus[COMPUTER_MODELS_MENU].get_index()
            model = mm.get_computer_model_by_index(index)
            self.add_computer_markers(model)
        elif self.__menus[PLAYER_MODELS_MENU].is_focused():
            index = self.__menus[PLAYER_MODELS_MENU].get_index()
            model = mm.get_player_model_by_index(index)
            self.add_computer_markers(model)

    def move_pointer_down(self):
        self.__move_pointer(DOWN)
        mm = self.__scene.get_models_manager()
        if self.__menus[COMPUTER_MODELS_MENU].is_focused():
            index = self.__menus[COMPUTER_MODELS_MENU].get_index()
            model = mm.get_computer_model_by_index(index)
            self.add_computer_markers(model)
        elif self.__menus[PLAYER_MODELS_MENU].is_focused():
            index = self.__menus[PLAYER_MODELS_MENU].get_index()
            model = mm.get_player_model_by_index(index)
            self.add_computer_markers(model)

    def __move_pointer(self, direction):
        focused_menu = self.__get_focused_menu()
        if direction == UP:
            focused_menu.move_pointer_up()
        elif direction == DOWN:
            focused_menu.move_pointer_down()
        return

    # def set_computers_menu(self, action, action_manager, valid_targets):
    def set_computers_menu(self, valid_targets):
        self.__add_computers_models_menu(valid_targets)
        self.__set_focused_menu(self.__menus[COMPUTER_MODELS_MENU])
        mm = self.__scene.get_models_manager()
        # TODO: need to mark valid targets
        # return the first computer unit and mark it
        index = self.__menus[COMPUTER_MODELS_MENU].get_index()
        self.add_computer_markers(mm.get_computer_model_by_index(index))

    # -------- Markers -------- #
    def mark_player_item(self, model):
        for i in range(self.__menus[PLAYER_MODELS_MENU].get_menu_items_count()):
            menu_model = self.__menus[PLAYER_MODELS_MENU].get_model_by_index(i)
            if menu_model == model:
                item = self.__menus[PLAYER_MODELS_MENU].get_item_from_menu(i)
                item.mark_string()

    def unmark_player_items(self):
        for i in range(self.__menus[PLAYER_MODELS_MENU].get_menu_items_count()):
            item = self.__menus[PLAYER_MODELS_MENU].get_item_from_menu(i)
            item.unmark_string()

    def unmark_computer_items(self):
        for i in range(self.__menus[COMPUTER_MODELS_MENU].get_menu_items_count()):
            item = self.__menus[COMPUTER_MODELS_MENU].get_item_from_menu(i)
            item.unmark_string()

    def __remove_sub_menus(self):
        for key in [SKILLS_MENU, SPELLS_MENU, ITEMS_MENU]:
            if self.__menus[key] is not None:
                self.__menus[key].kill()
                self.__menus[key] = None
        return

    def __add_marker(self, model):

        # if model.is_player_model():
        marker_spritesheet = UIConstants.MARKER_GREEN_SPRITE_SHEET
        # else:
        #     marker_spritesheet = UIConstants.MARKER_RED_SPRITE_SHEET

        marker = AnimatedObject(marker_spritesheet, None,
                                position=(0, 0),
                                object_type=GAME_OBJECT)

        rect = pygame.Rect((0, 0), marker.get_size())  # create a temp rect
        rect.top = model.get_rect().top - int(rect.height)
        rect.left = model.get_rect().centerx - int(rect.width / 2)
        marker.set_position(rect.topleft)  # draw the marker right above the focused_sprite

        # add to game engine sprites group
        game_engine = self.__scene.get_game_engine()
        game_engine.add_sprite_to_group(marker)
        return marker

    def add_player_marker(self, player_models):
        if type(player_models) is not list:
            player_models = [player_models]

        self.remove_player_markers()

        for model in player_models:
            self.__player_markers.append(self.__add_marker(model))
            self.mark_player_item(model)

    def add_computer_markers(self, computer_models):
        if type(computer_models) is not list:
            computer_models = [computer_models]

        self.remove_computer_markers()

        for model in computer_models:
            self.__computer_markers.append(self.__add_marker(model))

    def remove_player_markers(self):
        for marker in self.__player_markers:
            marker.kill()
        self.__player_markers = []

        self.unmark_computer_items()

    def remove_computer_markers(self):
        for marker in self.__computer_markers:
            marker.kill()
        self.__computer_markers = []

        self.unmark_player_items()
