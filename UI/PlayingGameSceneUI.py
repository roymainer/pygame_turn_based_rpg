import pygame

from Shared.AnimatedObject import AnimatedObject
from Shared.Bestiary import *
from Shared.GameConstants import GameConstants
from Shared.UIConstants import UIConstants
from UI.Menu import Menu
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

    def __add_player_units_menu(self):
        menu_size = (GameConstants.PLAYER_UNITS_MENU_WIDTH,
                     GameConstants.SCREEN_SIZE[1] - GameConstants.BATTLE_AREA_BOTTOM)

        characters_list = []
        for scene_object in self.scene.get_scene_objects_list():
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
        for scene_object in self.scene.get_scene_objects_list():
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

        player_menu_size = self.__menus[PLAYER_UNITS_MENU].get_size()
        computer_menu_size = self.__menus[COMPUTER_UNITS_MENU].get_size()

        menu_size = (GameConstants.SCREEN_SIZE[0] - player_menu_size[0] - computer_menu_size[0],
                     player_menu_size[1])

        menu_actions_list = get_unit_actions(unit)

        menu_position = (self.__menus[PLAYER_UNITS_MENU].get_rect().right, GameConstants.BATTLE_AREA_BOTTOM)
        menu = Menu(UIConstants.SPRITE_BLUE_MENU, menu_size, menu_actions_list, menu_position)

        # add menu,  menu items and pointer to game engine sprites group
        self.scene.get_game().add_sprite_to_group(menu)
        for i in range(menu.get_menu_items_count()):
            self.scene.get_game().add_sprite_to_group(menu.get_item_from_menu(i))
        self.scene.get_game().add_sprite_to_group(menu.get_pointer())
        self.__menus[ACTIONS_MENU] = menu

    def remove_actions_menu(self):
        self.__menus[ACTIONS_MENU].kill()  # remove the actions menu

    def get_focused_menu(self):
        focused_menu = self.__menus[ACTIONS_MENU]  # default

        for menu in self.__menus.values():
            if menu is None:
                continue
            if menu.is_focused():
                focused_menu = menu
                break

        return focused_menu

    def focus_on_actions_menu(self):
        for menu in self.__menus.values():
            menu.unset_focused()  # remove focus from all other menus
        self.__menus[COMPUTER_UNITS_MENU].remove_pointer()  # delete the computer units menu pointer
        self.__menus[ACTIONS_MENU].set_focused()  # set focus to actions menu
        return

    def focus_on_computer_units_menu(self):
        # once the player selects an action/magic, the focus should move to computer units menu to select a target
        for menu in self.__menus.values():
            menu.unset_focused()  # remove focus from all other menus
        self.__menus[COMPUTER_UNITS_MENU].set_focused()
        self.__menus[COMPUTER_UNITS_MENU].set_pointer()
        self.scene.get_game().add_sprite_to_group(self.__menus[COMPUTER_UNITS_MENU].get_pointer())
        return

    def __move_pointer(self, direction):
        focused_menu = self.get_focused_menu()
        if direction == UP:
            focused_menu.move_pointer_up()
        elif direction == DOWN:
            focused_menu.move_pointer_down()
        return

    def move_pointer_up(self):
        self.__move_pointer(UP)

    def move_pointer_down(self):
        self.__move_pointer(DOWN)

    def return_to_previous_menu(self):
        if self.__menus[COMPUTER_UNITS_MENU].is_focused() or self.__menus[PLAYER_UNITS_MENU].is_focused():
            self.__menus[COMPUTER_UNITS_MENU].unset_focused()
            self.__menus[COMPUTER_UNITS_MENU].remove_pointer()
            self.__menus[PLAYER_UNITS_MENU].unset_focused()
            self.__menus[PLAYER_UNITS_MENU].remove_pointer()
            self.__menus[ACTIONS_MENU].set_focused()
        return

    def add_menu_selection_to_current_action(self):
        focused_menu = self.get_focused_menu()
        current_action = self.scene.get_current_action()
        if self.__menus[ACTIONS_MENU].is_focused():
            current_action.set_action(focused_menu.get_selected_item())
            if focused_menu.get_selected_item().get_string() == ACTION_ATTACK:
                self.focus_on_computer_units_menu()
        elif self.__menus[COMPUTER_UNITS_MENU].is_focused():
            targets = self.__menus[COMPUTER_UNITS_MENU].get_selected_item()
            current_action.set_targets(targets)
        elif self.__menus[PLAYER_UNITS_MENU].is_focused():
            targets = self.__menus[PLAYER_UNITS_MENU].get_selected_item()
            current_action.set_targets(targets)

    def add_player_marker(self, focused_sprite):
        if any(self.__player_markers):
            self.remove_player_markers()  # delete any old markers

        rect = pygame.Rect((0, 0), UIConstants.MARKER_GREEN_SIZE)  # create a temp rect
        rect.top = focused_sprite.get_rect().top - int(rect.height / 2)
        rect.left = focused_sprite.get_rect().centerx - int(rect.width / 2)
        position = rect.topleft  # draw the marker right above the focused_sprite
        self.__player_markers.append(AnimatedObject(UIConstants.MARKER_GREEN_SPRITE_SHEET,
                                                    UIConstants.MARKER_GREEN_SIZE,
                                                    position=position,
                                                    object_type=GameConstants.ALL_GAME_OBJECTS))
        # add to game engine sprites group
        game_engine = self.scene.get_game()
        for marker in self.__player_markers:
            game_engine.add_sprite_to_group(marker, marker.get_type())

    def __remove_markers(self, markers):
        for marker in markers:
            if marker is not None:
                marker.kill()
        return

    def remove_player_markers(self):
        self.__remove_markers(self.__player_markers)
        self.__player_markers = []

    def remove_computer_markers(self):
        self.__remove_markers(self.__computer_markers)
        self.__computer_markers = []
