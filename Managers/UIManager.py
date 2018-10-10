from Managers.Manager import Manager, UI_MANAGER
from Shared.AnimatedObject import AnimatedObject
from Shared.Button import TextButton
from Shared.GameConstants import GameConstants
from Shared.UIConstants import UIConstants
from UI.DiceController import DiceController
from UI.Menu import Menu
from UI.MenuPointer import MenuPointer
from UI.ModelsMenu import ModelsMenu
import logging
logger = logging.getLogger().getChild(__name__)

PLAYER_MODELS_MENU = 0
COMPUTER_MODELS_MENU = 1
ACTIONS_MENU = 2
SPELLS_MENU = 3
DISPEL_MENU = 4
ITEMS_MENU = 5
SKILLS_MENU = 6
DICE_CONTROLLER = 7
DISPEL_DICE_CONTROLLER = 8
CONTINUE_BUTTON = 9

UP = "Up"
DOWN = "Down"


# noinspection PyTypeChecker,PyUnboundLocalVariable
class UIManager(Manager):

    def __init__(self, scene):
        logger.info("Init")
        self.__menus = {PLAYER_MODELS_MENU: None,
                        COMPUTER_MODELS_MENU: None,
                        ACTIONS_MENU: None,
                        SKILLS_MENU: None,
                        SPELLS_MENU: None,
                        ITEMS_MENU: None,
                        DICE_CONTROLLER: None,
                        CONTINUE_BUTTON: None}

        self.__player_markers = []
        self.__computer_markers = []
        self.__pointer = MenuPointer()

        super(UIManager, self).__init__(scene, UI_MANAGER)

    def on_init(self):
        logger.info("On init:")
        self.__add_player_models_menu()
        self.__add_computers_models_menu()
        self.set_focus_on_player_menu()

    def return_to_previous_menu(self):
        # self.__set_focused_menu(menu=self.__menus[ACTIONS_MENU])
        self.get_focused_menu().unmark_selected_item()
        self.set_focus_on_player_menu()
        self.remove_sub_menus()
        return

    def update_all_menus(self):
        logger.info("Updating all menus")
        phase_manager = self.get_phase_manager()
        models_manager = self.get_models_manager()

        if self.__menus[PLAYER_MODELS_MENU] is None:
            self.__add_player_models_menu()
        else:
            player_models = phase_manager.get_current_phase_player_models_list()
            self.__menus[PLAYER_MODELS_MENU].update_menu(self.get_game_engine(), player_models)
            if any(player_models):
                model = self.__menus[PLAYER_MODELS_MENU].get_selected_object()
                self.__add_player_marker(model)

        if self.__menus[COMPUTER_MODELS_MENU] is None:
            self.__add_computers_models_menu()
        else:
            # computer_models = phase_manager.get_current_phase_computer_models_list()
            computer_models = models_manager.get_computer_sorted_models_list()
            self.__menus[COMPUTER_MODELS_MENU].update_menu(self.get_game_engine(), computer_models)

        self.add_actions_menu()
        self.set_focus_on_player_menu()

        return

    def get_selected_player_model(self):
        return self.__menus[PLAYER_MODELS_MENU].get_selected_object()

    def __add_player_models_menu(self):
        logger.info("Adding Player Models Menu")
        # kill previous player menu
        if self.__menus[PLAYER_MODELS_MENU] is not None:
            self.__menus[PLAYER_MODELS_MENU].kill()
            self.__menus[PLAYER_MODELS_MENU] = None

        menu_size = (GameConstants.PLAYER_UNITS_MENU_WIDTH,
                     GameConstants.SCREEN_SIZE[1] - GameConstants.BATTLE_AREA_BOTTOM)
        menu_position = (0, GameConstants.BATTLE_AREA_BOTTOM)

        player_models = self.get_phase_manager().get_current_phase_player_models_list()

        menu = ModelsMenu(UIConstants.SPRITE_BLUE_MENU, menu_size, player_models, menu_position)

        # add menu,  menu items and pointer to game engine sprites group
        self.get_game_engine().add_sprite_to_group(menu)
        self.get_game_engine().add_sprite_to_group(menu.get_table_header())
        for i in range(menu.get_ui_objects_list_count()):
            self.get_game_engine().add_sprite_to_group(menu.get_ui_object_from_menu(i))

        menu.set_name("Player Models Menu")

        self.__menus[PLAYER_MODELS_MENU] = menu

        if not any(player_models):
            # if phase no active player units, return
            return

        # mark the first model of the menu
        model = menu.get_object_from_menu(0)
        self.__add_player_marker(model)

    def __add_computers_models_menu(self):
        logger.info("Adding Computer Models Menu")
        if self.__menus[COMPUTER_MODELS_MENU] is not None:
            self.__menus[COMPUTER_MODELS_MENU].kill()
            self.__menus[COMPUTER_MODELS_MENU] = None

        menu_size = (GameConstants.COMPUTER_MODELS_MENU_WIDTH,
                     GameConstants.SCREEN_SIZE[1] - GameConstants.BATTLE_AREA_BOTTOM)
        menu_position = (GameConstants.COMPUTER_FRONT_COLUMN - GameConstants.PADX, GameConstants.BATTLE_AREA_BOTTOM)

        computer_models = self.get_models_manager().get_computer_sorted_models_list()

        menu = ModelsMenu(UIConstants.SPRITE_BLUE_MENU, menu_size, computer_models, menu_position)

        # add menu,  menu items and pointer to game engine sprites group
        self.get_game_engine().add_sprite_to_group(menu)
        self.get_game_engine().add_sprite_to_group(menu.get_table_header())
        for i in range(menu.get_ui_objects_list_count()):
            self.get_game_engine().add_sprite_to_group(menu.get_ui_object_from_menu(i))

        menu.set_name("Computer Models Menu")

        self.__menus[COMPUTER_MODELS_MENU] = menu

        # mark the first model of the menu
        model = menu.get_object_from_menu(0)
        self.__add_computer_markers(model)

    def add_actions_menu(self):
        logger.info("Adding Actions Menu")
        if self.__menus[ACTIONS_MENU] is not None:
            self.__menus[ACTIONS_MENU].kill()  # delete the menu from any of it's groups
            self.__menus[ACTIONS_MENU] = None

        player_menu_size = self.__menus[PLAYER_MODELS_MENU].get_size()
        computer_menu_size = self.__menus[COMPUTER_MODELS_MENU].get_size()

        menu_size = (GameConstants.SCREEN_SIZE[0] - player_menu_size[0] - computer_menu_size[0],
                     player_menu_size[1])

        menu_actions_list = self.get_phase_manager().get_current_phase_actions_list()

        menu_position = (self.__menus[PLAYER_MODELS_MENU].get_rect().right,
                         GameConstants.BATTLE_AREA_BOTTOM)
        menu = Menu(UIConstants.SPRITE_BLUE_MENU, menu_size, menu_actions_list, menu_position)

        game_engine = self.get_game_engine()
        # add menu,  menu items and pointer to game engine sprites group
        game_engine.add_sprite_to_group(menu)
        for i in range(menu.get_ui_objects_list_count()):
            game_engine.add_sprite_to_group(menu.get_ui_object_from_menu(i))

        menu.set_name("Actions Menu")

        # noinspection PyTypeChecker
        self.__menus[ACTIONS_MENU] = menu

    def add_skills_menu(self, model):
        logger.info("Adding Skills Menu")
        skills_list = model.get_skills_list()
        self.__add_sub_menu(SKILLS_MENU, skills_list)

    def add_spells_menu(self, model):
        logger.info("Adding Spells Menu")
        uncast_spells_list = model.get_uncast_spells_list()
        self.__add_sub_menu(SPELLS_MENU, uncast_spells_list)

    def add_items_menu(self, model):
        logger.info("Adding Items Menu")
        items_list = model.get_items_list()
        self.__add_sub_menu(ITEMS_MENU, items_list)

    def __add_sub_menu(self, menu_key, menu_items_list):
        menus_dict = {SKILLS_MENU: "Skills Menu", SPELLS_MENU: "Spells Menu", ITEMS_MENU: "Items Menu"}

        # delete either of these menus before adding a new one
        for menu in menus_dict.keys():
            if self.__menus[menu] is not None:
                self.__menus[menu].kill()  # delete the menu from any of it's groups
                self.__menus[menu] = None

        computer_menu = self.__menus[COMPUTER_MODELS_MENU]
        actions_menu = self.__menus[ACTIONS_MENU]

        menu_size = (int(actions_menu.get_size()[0]*3/4), actions_menu.get_size()[1])

        menu_position = (computer_menu.get_rect().left - int(menu_size[0]), GameConstants.BATTLE_AREA_BOTTOM)

        menu = Menu(UIConstants.SPRITE_BLUE_MENU, menu_size, menu_items_list, menu_position)
        menu.set_name(menu_key)

        game_engine = self.get_game_engine()
        game_engine.add_sprite_to_group(menu)
        for i in range(menu.get_ui_objects_list_count()):
            game_engine.add_sprite_to_group(menu.get_ui_object_from_menu(i))
        # self.__pointer.assign_pointer_to_menu(menu)

        menu.set_name(menus_dict[menu_key])

        self.__menus[menu_key] = menu
        self.__set_focused_menu(menu)

    # ----------------- Menu Focus Controllers ----------------- #
    def __set_focused_menu(self, menu):
        logger.info("Setting Focus on {}".format(menu.get_name()))
        # remove focus from all other menus
        for _menu in self.__menus.values():
            if _menu is None:
                continue
            else:
                _menu.unset_focused()

        menu.set_focused()
        menu.unmark_selected_item()  # unmark selected option text

        # verify that the pointer is on the front layer
        game_engine = self.get_game_engine()
        game_engine.remove_sprite_from_group(self.__pointer)  # remove from list
        game_engine.add_sprite_to_group(self.__pointer)  # return to list at higher layer
        self.__pointer.assign_pointer_to_menu(menu)
        return

    def set_focus_on_player_menu(self):
        self.__set_focused_menu(self.__menus[PLAYER_MODELS_MENU])

    def set_focus_on_computer_menu(self, valid_targets):
        self.__add_computers_models_menu()
        self.__set_focused_menu(self.__menus[COMPUTER_MODELS_MENU])
        mm = self.get_models_manager()
        # TODO: need to mark valid targets
        # return the first computer unit and mark it
        index = self.__menus[COMPUTER_MODELS_MENU].get_index()
        self.__add_computer_markers(mm.get_computer_model_by_index(index))

    def set_focus_on_actions_menu(self):
        self.__set_focused_menu(self.__menus[ACTIONS_MENU])

    def __set_focus_on_dice_menu(self):
        logger.info("Setting focus on Dice Controller")
        menu = self.__menus[DICE_CONTROLLER]
        # remove focus from all other menus
        for _menu in self.__menus.values():
            if _menu is None:
                continue
            else:
                _menu.unset_focused()

        menu.set_focused()

    def __set_focus_on_dispel_dice_menu(self):
        logger.info("Setting focus on Dice Controller")
        menu = self.__menus[DISPEL_DICE_CONTROLLER]
        for _menu in self.__menus.values():
            if _menu is None:
                continue
            else:
                _menu.unset_focused()

        menu.set_focused()

    def __set_focus_on_continue_button(self):
        logger.info("Setting focus on Continue Button")
        menu = self.__menus[CONTINUE_BUTTON]
        # remove focus from all other menus
        for _menu in self.__menus.values():
            if _menu is None:
                continue
            else:
                _menu.unset_focused()

        menu.set_focused()

    def get_focused_menu(self) -> Menu:
        focused_menu = self.__menus[ACTIONS_MENU]  # default
        for menu in self.__menus.values():
            if menu is None:
                continue
            if menu.is_focused():
                focused_menu = menu
                break
        return focused_menu

    def is_focused_on_player_models_menu(self) -> bool:
        return self.get_focused_menu() == self.__menus[PLAYER_MODELS_MENU]

    def is_focused_on_computer_models_menu(self) -> bool:
        return self.get_focused_menu() == self.__menus[COMPUTER_MODELS_MENU]

    def is_focused_on_actions_menu(self) -> bool:
        return self.get_focused_menu() == self.__menus[ACTIONS_MENU]

    def is_focused_on_skills_menu(self) -> bool:
        return self.get_focused_menu() == self.__menus[SKILLS_MENU]

    def is_focused_on_spells_menu(self) -> bool:
        return self.get_focused_menu() == self.__menus[SPELLS_MENU]

    def is_focused_on_dispel_menu(self) -> bool:
        return self.get_focused_menu() == self.__menus[DISPEL_MENU]

    def is_focused_on_items_menu(self) -> bool:
        return self.get_focused_menu() == self.__menus[ITEMS_MENU]

    def is_focused_on_dice_controller(self) -> bool:
        return self.get_focused_menu() == self.__menus[DICE_CONTROLLER]

    def is_focused_on_dispel_dice_controller(self) -> bool:
        return self.get_focused_menu() == self.__menus[DISPEL_DICE_CONTROLLER]

    def is_focused_on_continue_button(self) -> bool:
        return self.get_focused_menu() == self.__menus[CONTINUE_BUTTON]

    # ----------------- Menu Pointers Controllers ----------------- #
    def move_pointer_up(self):
        self.__move_pointer(UP)
        if self.__menus[COMPUTER_MODELS_MENU].is_focused():
            model = self.__menus[COMPUTER_MODELS_MENU].get_selected_object()
            self.__add_computer_markers(model)
        elif self.__menus[PLAYER_MODELS_MENU].is_focused():
            model = self.__menus[PLAYER_MODELS_MENU].get_selected_object()
            self.__add_player_marker(model)

    def move_pointer_down(self):
        self.__move_pointer(DOWN)
        if self.__menus[COMPUTER_MODELS_MENU].is_focused():
            model = self.__menus[COMPUTER_MODELS_MENU].get_selected_object()
            self.__add_computer_markers(model)
        elif self.__menus[PLAYER_MODELS_MENU].is_focused():
            model = self.__menus[PLAYER_MODELS_MENU].get_selected_object()
            self.__add_player_marker(model)

    def __move_pointer(self, direction):
        focused_menu = self.get_focused_menu()
        if not hasattr(focused_menu, "move_pointer_up"):
            return
        logger.info("{}: Move pointer {}".format(focused_menu.get_name(), direction))
        if direction == UP:
            focused_menu.move_pointer_up()
        elif direction == DOWN:
            focused_menu.move_pointer_down()
        return

    def remove_sub_menus(self):
        logger.info("Remove sub menus")
        for key in [SKILLS_MENU, SPELLS_MENU, ITEMS_MENU]:
            if self.__menus[key] is not None:
                self.__menus[key].kill()
                self.__menus[key] = None

        if self.__menus[DICE_CONTROLLER] is not None:
            self.destroy_dice_controller()

        if self.__menus[DISPEL_DICE_CONTROLLER] is not None:
            self.destroy_dispel_dice_controller()
        return

    def get_pointer(self):
        return self.__pointer

    # ----------------- Menu Items Markers ----------------- #
    def mark_selected_item(self):
        self.get_focused_menu().mark_selected_item()

    def __unmark_player_items(self):
        if self.__menus[PLAYER_MODELS_MENU] is not None:
            for ui_obj in self.__menus[PLAYER_MODELS_MENU].get_ui_objects_list():
                ui_obj.unmark_string()
            # for i in range(self.__menus[PLAYER_MODELS_MENU].get_menu_items_count()):
            #     item = self.__menus[PLAYER_MODELS_MENU].get_item_from_menu(i)
            #     item.unmark_string()

    def __unmark_computer_items(self):
        if self.__menus[COMPUTER_MODELS_MENU] is not None:
            for ui_obj in self.__menus[COMPUTER_MODELS_MENU].get_ui_objects_list():
                ui_obj.unmark_string()

            # for i in range(self.__menus[COMPUTER_MODELS_MENU].get_menu_items_count()):
            #     item = self.__menus[COMPUTER_MODELS_MENU].get_item_from_menu(i)
            #     item.unmark_string()

    # ----------------- Battlefield Models Markers ----------------- #
    def __add_marker(self, model):
        marker_spritesheet = UIConstants.MARKERS_SPRITE_SHEET
        marker = AnimatedObject(marker_spritesheet, None,
                                position=(0, 0),
                                object_type=GameConstants.GAME_OBJECT)

        model_position = model.get_position()
        model_size = model.get_size()

        if not hasattr(model, "is_player_model()"):
            return

        if model.is_player_model():
            marker.set_animation("green_marker_side")
            x = model_position[0] - marker.get_size()[0]

        else:
            marker.set_animation("red_marker_side")
            marker.flip_x()
            x = model_position[0] + model_size[0]

        y = model_position[1] + int(model_size[1] * 3 / 4) - (marker.get_size()[1] / 2)
        new_position = (x, y)
        marker.set_position(new_position)  # draw the marker right above the focused_sprite

        # add to game engine sprites group
        game_engine = self.get_game_engine()
        game_engine.add_sprite_to_group(marker)
        return marker

    def __add_player_marker(self, player_models):
        if type(player_models) is not list:
            player_models = [player_models]

        self.remove_player_markers()

        for model in player_models:
            self.__player_markers.append(self.__add_marker(model))
            # self.mark_player_item(model)

    def __add_computer_markers(self, computer_models):
        if type(computer_models) is not list:
            computer_models = [computer_models]

        self.remove_computer_markers()

        for model in computer_models:
            self.__computer_markers.append(self.__add_marker(model))

    def remove_player_markers(self):
        for marker in self.__player_markers:
            if marker is None:
                continue
            marker.kill()
        self.__player_markers = []

        self.__unmark_computer_items()

    def remove_computer_markers(self):
        for marker in self.__computer_markers:
            if marker is None:
                continue
            marker.kill()
        self.__computer_markers = []

        self.__unmark_player_items()

    # ----------------- Spell Dice Controller ----------------- #
    def add_dice_controller(self):
        logger.info("Add Dice Controller")
        magic_manager = self.get_magic_manager()
        remaining_dice = magic_manager.get_player_power_pool()
        menu = DiceController(remaining_dice)

        game_engine = self.get_game_engine()
        for item in menu.get_sprites():
            game_engine.add_sprite_to_group(item)

        self.__menus[DICE_CONTROLLER] = menu
        self.__set_focus_on_dice_menu()

    def get_dice(self):
        return self.__menus[DICE_CONTROLLER].get_dice()

    def increase_dice(self):
        self.__menus[DICE_CONTROLLER].increase_dice()

    def decrease_dice(self):
        self.__menus[DICE_CONTROLLER].decrease_dice()

    def destroy_dice_controller(self):
        logger.info("Destroy Dice Controller")
        dice_controller = self.__menus[DICE_CONTROLLER]
        dice_controller.destroy()
        self.__menus[DICE_CONTROLLER] = None

    # ----------------- Dispel Dice Controller ----------------- #
    def add_dispel_dice_controller(self):
        logger.info("Add Dispel Dice Controller")
        magic_manager = self.get_magic_manager()
        remaining_dispel_dice = magic_manager.get_player_dispel_pool()
        menu = DiceController(remaining_dispel_dice)

        game_engine = self.get_game_engine()
        for item in menu.get_sprites():
            game_engine.add_sprite_to_group(item)

        self.__menus[DISPEL_DICE_CONTROLLER] = menu
        self.__set_focus_on_dispel_dice_menu()

    def get_dispel_dice(self):
        return self.__menus[DISPEL_DICE_CONTROLLER].get_dice()

    def increase_dispel_dice(self):
        self.__menus[DISPEL_DICE_CONTROLLER].increase_dice()

    def decrease_dispel_dice(self):
        self.__menus[DISPEL_DICE_CONTROLLER].increase_dice()

    def destroy_dispel_dice_controller(self):
        logger.info("Destroy Dispel Dice Controller")
        ddc = self.__menus[DISPEL_DICE_CONTROLLER]
        ddc.destroy()
        self.__menus[DISPEL_DICE_CONTROLLER] = None

    # ----------------- End Battle Controllers ----------------- #
    def add_game_over_controls(self, posy=0):
        logger.info("Add Continue Controller")
        button = TextButton(string="Continue", position=(0, 0))
        position = (int(GameConstants.SCREEN_SIZE[0] / 2) - int(button.get_size()[0] / 2), posy + 50)
        button.set_position(position)
        self.__menus[CONTINUE_BUTTON] = button

        self.get_game_engine().add_sprite_to_group(button)
        self.__set_focus_on_continue_button()
        if self.__pointer is None:
            self.__pointer = MenuPointer()
            self.get_game_engine().add_sprite_to_group(self.__pointer)
        self.__pointer.assign_pointer_to_button(button)

    def destroy(self):
        # kill all menus
        for key in self.__menus.keys():
            if key == DICE_CONTROLLER:
                continue
            if self.__menus[key] is not None:
                self.__menus[key].kill()
                self.__menus[key] = None

        if self.__menus[DICE_CONTROLLER] is not None:
            self.destroy_dice_controller()

        if self.__menus[DISPEL_DICE_CONTROLLER] is not None:
            self.destroy_dispel_dice_controller()

        self.remove_player_markers()  # kill player markers
        self.remove_computer_markers()  # kill computer markers

        # kill the pointer
        self.__pointer.kill()
        self.__pointer = None
