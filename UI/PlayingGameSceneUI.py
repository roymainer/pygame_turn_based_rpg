import pygame

from Shared.AnimatedObject import AnimatedObject
# from Shared.Bestiary import *
from Shared.GameConstants import GameConstants
from Shared.UIConstants import UIConstants
from Shared.Model import *
from UI.Menu import Menu
from UI.MenuPointer import MenuPointer
from UI.UnitsMenu import UnitsMenu

PLAYER_UNITS_MENU = 0
COMPUTER_UNITS_MENU = 1
ACTIONS_MENU = 2
MAGIC_MENU = 3
ITEMS_MENU = 4
SKILLS_MENU = 5

UP = 0
DOWN = 1


class PlayingGameSceneUI:

    def __init__(self, scene):
        self.scene = scene
        self.__menus = {PLAYER_UNITS_MENU: self.__add_player_units_menu(),
                        ACTIONS_MENU: None,
                        COMPUTER_UNITS_MENU: self.__add_computers_units_menu()}
        self.__player_markers = []
        self.__computer_markers = []
        self.__pointer = MenuPointer()

    def update_units_menu(self):
        tm = self.scene.get_turn_manager()

        player_units = tm.get_all_player_units()
        self.__menus[PLAYER_UNITS_MENU].update_menu(self.scene.get_game(), player_units)

        computer_units = tm.get_all_computer_units()
        self.__menus[COMPUTER_UNITS_MENU].update_menu(self.scene.get_game(), computer_units)

    def __add_player_units_menu(self):
        menu_size = (GameConstants.PLAYER_UNITS_MENU_WIDTH,
                     GameConstants.SCREEN_SIZE[1] - GameConstants.BATTLE_AREA_BOTTOM)

        characters_list = []
        tm = self.scene.get_turn_manager()
        player_units = tm.get_all_player_units()
        for scene_object in player_units:
            if scene_object.get_type() == GameConstants.PLAYER_GAME_OBJECTS:
                characters_list.append(scene_object)
        menu_position = (0, GameConstants.BATTLE_AREA_BOTTOM)
        menu = UnitsMenu(UIConstants.SPRITE_BLUE_MENU, menu_size, characters_list, menu_position)

        # add menu,  menu items and pointer to game engine sprites group
        self.scene.get_game().add_sprite_to_group(menu)
        for i in range(menu.get_menu_items_count()):
            self.scene.get_game().add_sprite_to_group(menu.get_item_from_menu(i))
        # self.get_game().add_sprite_to_group(menu.get_pointer())
        return menu

    def __add_computers_units_menu(self):
        menu_size = (GameConstants.COMPUTER_UNITS_MENU_WIDTH,
                     GameConstants.SCREEN_SIZE[1] - GameConstants.BATTLE_AREA_BOTTOM)

        characters_list = []
        tm = self.scene.get_turn_manager()
        computer_units = tm.get_all_computer_units()
        for scene_object in computer_units:
            if scene_object.get_type() == GameConstants.COMPUTER_GAME_OBJECTS:
                characters_list.append(scene_object)
        menu_position = (GameConstants.COMPUTER_FRONT_COLUMN - GameConstants.PADX, GameConstants.BATTLE_AREA_BOTTOM)
        menu = UnitsMenu(UIConstants.SPRITE_BLUE_MENU, menu_size, characters_list, menu_position)

        # add menu,  menu items and pointer to game engine sprites group
        self.scene.get_game().add_sprite_to_group(menu)
        for i in range(menu.get_menu_items_count()):
            self.scene.get_game().add_sprite_to_group(menu.get_item_from_menu(i))
        # self.get_game().add_sprite_to_group(menu.get_pointer())
        return menu

    def add_actions_menu(self, unit):
        if self.__menus[ACTIONS_MENU] is not None:
            self.__menus[ACTIONS_MENU].kill()  # delete the menu from any of it's groups
            self.__menus[ACTIONS_MENU] = None

        player_menu_size = self.__menus[PLAYER_UNITS_MENU].get_size()
        computer_menu_size = self.__menus[COMPUTER_UNITS_MENU].get_size()

        menu_size = (GameConstants.SCREEN_SIZE[0] - player_menu_size[0] - computer_menu_size[0],
                     player_menu_size[1])

        menu_actions_list = Model.get_unit_actions(unit)

        menu_position = (self.__menus[PLAYER_UNITS_MENU].get_rect().right, GameConstants.BATTLE_AREA_BOTTOM)
        menu = Menu(UIConstants.SPRITE_BLUE_MENU, menu_size, menu_actions_list, menu_position)

        game_engine = self.scene.get_game()
        # add menu,  menu items and pointer to game engine sprites group
        game_engine.add_sprite_to_group(menu)
        for i in range(menu.get_menu_items_count()):
            game_engine.add_sprite_to_group(menu.get_item_from_menu(i))
        self.__pointer.assign_pointer_to_menu(menu)
        game_engine.add_sprite_to_group(self.__pointer, 0)
        # noinspection PyTypeChecker
        self.__menus[ACTIONS_MENU] = menu

    def remove_actions_menu(self):
        self.__menus[ACTIONS_MENU].kill()  # remove the actions menu

    def set_focused_menu(self, menu):
        # remove focus from all other menus
        for _menu in self.__menus.values():
            _menu.unset_focused()

        menu.set_focused()
        menu.get_selected_item().unmark_string()  # unmark selected option text
        self.__pointer.assign_pointer_to_menu(menu)
        return

    def get_focused_menu(self):
        focused_menu = self.__menus[ACTIONS_MENU]  # default
        for menu in self.__menus.values():
            if menu is None:
                continue
            if menu.is_focused():
                focused_menu = menu
                break
        return focused_menu

    def __move_pointer(self, direction):
        focused_menu = self.get_focused_menu()
        if direction == UP:
            focused_menu.move_pointer_up()
        elif direction == DOWN:
            focused_menu.move_pointer_down()
        return

    def move_pointer_up(self):
        self.__move_pointer(UP)
        if self.__menus[COMPUTER_UNITS_MENU].is_focused():
            # TODO: what happens when many units are selected?
            tm = self.scene.get_turn_manager()
            unit_index = self.__menus[COMPUTER_UNITS_MENU].get_index()
            unit = tm.get_computer_unit(unit_index)  # fix unit offset
            self.add_computer_markers(unit)

    def move_pointer_down(self):
        self.__move_pointer(DOWN)
        if self.__menus[COMPUTER_UNITS_MENU].is_focused():
            # TODO: what happens when many units are selected?
            tm = self.scene.get_turn_manager()
            unit_index = self.__menus[COMPUTER_UNITS_MENU].get_index()
            unit = tm.get_computer_unit(unit_index)  # fix unit offset
            self.add_computer_markers(unit)

    def return_to_previous_menu(self):
        if self.__menus[COMPUTER_UNITS_MENU].is_focused() or self.__menus[PLAYER_UNITS_MENU].is_focused():
            self.set_focused_menu(menu=self.__menus[ACTIONS_MENU])
        return

    def add_menu_selection_to_current_action(self):
        focused_menu = self.get_focused_menu()
        focused_menu.get_selected_item().mark_string()  # mark the selected text
        current_action = self.scene.get_current_action()  # get current_action object from the scene
        if self.__menus[ACTIONS_MENU].is_focused():
            action_string = focused_menu.get_selected_item().get_string()  # get selected action string
            if action_string == ACTION_ATTACK:
                current_action.set_action(action_string)  # action is a string
                self.set_focused_menu(self.__menus[COMPUTER_UNITS_MENU])
                tm = self.scene.get_turn_manager()
                self.add_computer_markers(tm.get_computer_unit(0))  # return the first computer unit and mark it
            elif action_string == ACTION_MAGIC:
                # TODO: add this
                pass
        elif self.__menus[COMPUTER_UNITS_MENU].is_focused():
            # targets = self.__menus[COMPUTER_UNITS_MENU].get_selected_item()
            targets = self.__menus[COMPUTER_UNITS_MENU].get_selectd_unit()
            current_action.set_targets(targets)
            self.remove_computer_markers()
        elif self.__menus[PLAYER_UNITS_MENU].is_focused():
            targets = self.__menus[PLAYER_UNITS_MENU].get_selected_item()
            if type(targets) is not list:
                targets = [targets]
            current_action.set_targets(targets)

    def __add_marker(self, unit, green=True):

        if green:
            marker_spritesheet = UIConstants.MARKER_GREEN_SPRITE_SHEET
            marker_size = UIConstants.MARKER_GREEN_SIZE
        else:
            marker_spritesheet = UIConstants.MARKER_RED_SPRITE_SHEET
            marker_size = UIConstants.MARKER_RED_SIZE

        rect = pygame.Rect((0, 0), marker_size)  # create a temp rect
        rect.top = unit.get_rect().top - int(rect.height / 2)
        rect.left = unit.get_rect().centerx - int(rect.width / 2)
        position = rect.topleft  # draw the marker right above the focused_sprite

        marker = AnimatedObject(marker_spritesheet, marker_size,
                                position=position,
                                object_type=GameConstants.ALL_GAME_OBJECTS)

        # add to game engine sprites group
        game_engine = self.scene.get_game()
        game_engine.add_sprite_to_group(marker, marker.get_size())
        return marker

    def add_player_marker(self, player_units):
        if type(player_units) is not list:
            player_units = [player_units]

        self.remove_player_markers()

        for unit in player_units:
            self.__player_markers.append(self.__add_marker(unit, True))
            self.mark_player_item(unit)

    def add_computer_markers(self, computer_units):
        if type(computer_units) is not list:
            computer_units = [computer_units]

        self.remove_computer_markers()

        for unit in computer_units:
            self.__computer_markers.append(self.__add_marker(unit, False))

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

    def mark_player_item(self, unit):
        for i in range(self.__menus[PLAYER_UNITS_MENU].get_menu_items_count()):
            menu_unit = self.__menus[PLAYER_UNITS_MENU].get_unit_by_index(i)
            if menu_unit == unit:
                item = self.__menus[PLAYER_UNITS_MENU].get_item_from_menu(i)
                item.mark_string()

    def unmark_player_items(self):
        for i in range(self.__menus[PLAYER_UNITS_MENU].get_menu_items_count()):
            item = self.__menus[PLAYER_UNITS_MENU].get_item_from_menu(i)
            item.unmark_string()

    def unmark_computer_items(self):
        for i in range(self.__menus[COMPUTER_UNITS_MENU].get_menu_items_count()):
            item = self.__menus[COMPUTER_UNITS_MENU].get_item_from_menu(i)
            item.unmark_string()

