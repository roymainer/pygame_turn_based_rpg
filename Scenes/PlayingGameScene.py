import pygame

from Scenes.Scene import Scene
# from Shared.Bestiary import Bestiary
from Shared import Bestiary
from Shared.AnimatedObject import AnimatedObject
from Shared.Character import Character
from Shared.GameConstants import GameConstants
from Shared.TurnManager import TurnManager
from Shared.UIConstants import UIConstants
from UI.Menu import Menu
from UI.Text import Text
from UI.UnitsMenu import UnitsMenu


def create_background():
    surface = pygame.Surface(GameConstants.SCREEN_SIZE)  # create an empty surface

    # load upper background
    background = pygame.image.load(GameConstants.DARK_LAIR)
    background = pygame.transform.smoothscale(background, (GameConstants.SCREEN_SIZE[0],
                                                           GameConstants.BATTLE_AREA_TOP))
    surface.blit(background, (0, 0))

    battleground_tile = pygame.image.load(GameConstants.CAVE_TILE)
    rows = 2
    columns = 8
    tile_width = int(GameConstants.SCREEN_SIZE[0] / columns)  # 800 / 8 = 100
    tile_height = int((GameConstants.BATTLE_AREA_BOTTOM - GameConstants.BATTLE_AREA_TOP) / rows)  # 200/ 2 = 100

    battleground_tile = pygame.transform.scale(battleground_tile,
                                               (tile_width, tile_height))

    y = GameConstants.BATTLE_AREA_TOP
    for row in range(rows):
        y += tile_height * row
        for column in range(columns):
            x = tile_width * column
            surface.blit(battleground_tile, (x, y))

    # load menu background
    # surface.blit(menu_background, (0, GameConstants.BATTLE_AREA_BOTTOM))

    return surface


class PlayingGameScene(Scene):

    def __init__(self, game_engine):
        super(PlayingGameScene, self).__init__(game_engine)
        background = create_background()
        self.get_game().set_background(background)

        self.__turn_manager = TurnManager()
        self.load_level()

        self.__marker = None
        self.__focused_sprite = None

        self.__player_units_menu = self.__add_player_units_menu()
        self.__action_menu = None
        self.__computer_units_menu = self.__add_computers_units_menu()

        self.__menu_item_selected = None

    def __add_player_units_menu(self):
        menu_size = (GameConstants.PLAYER_UNITS_MENU_WIDTH,
                     GameConstants.SCREEN_SIZE[1] - GameConstants.BATTLE_AREA_BOTTOM)

        characters_list = []
        for scene_object in self.get_scene_objects_list():
            if scene_object.get_type() == GameConstants.PLAYER_GAME_OBJECTS:
                characters_list.append(scene_object)
        menu_position = (0, GameConstants.BATTLE_AREA_BOTTOM)
        menu = UnitsMenu(UIConstants.SPRITE_BLUE_MENU, menu_size, characters_list, menu_position)

        # add menu,  menu items and pointer to game engine sprites group
        self.get_game().add_sprite_to_group(menu)
        for i in range(menu.get_menu_items_count()):
            self.get_game().add_sprite_to_group(menu.get_item_from_menu(i))
        self.get_game().add_sprite_to_group(menu.get_pointer())
        return menu

    def __add_actions_menu(self, unit):
        player_menu_size = self.__player_units_menu.get_size()
        computer_menu_size = self.__computer_units_menu.get_size()

        menu_size = (GameConstants.SCREEN_SIZE[0] - player_menu_size[0] - computer_menu_size[0],
                     player_menu_size[1])

        menu_actions_list = Bestiary.get_unit_actions(unit)

        menu_position = (self.__player_units_menu.get_rect().right, GameConstants.BATTLE_AREA_BOTTOM)
        menu = Menu(UIConstants.SPRITE_BLUE_MENU, menu_size, menu_actions_list, menu_position)

        # add menu,  menu items and pointer to game engine sprites group
        self.get_game().add_sprite_to_group(menu)
        for i in range(menu.get_menu_items_count()):
            self.get_game().add_sprite_to_group(menu.get_item_from_menu(i))
        self.get_game().add_sprite_to_group(menu.get_pointer())
        return menu

    def __add_computers_units_menu(self):
        menu_size = (GameConstants.COMPUTER_UNITS_MENU_WIDTH,
                     GameConstants.SCREEN_SIZE[1] - GameConstants.BATTLE_AREA_BOTTOM)

        characters_list = []
        for scene_object in self.get_scene_objects_list():
            if scene_object.get_type() == GameConstants.COMPUTER_GAME_OBJECTS:
                characters_list.append(scene_object)
        menu_position = (GameConstants.COMPUTER_FRONT_COLUMN - GameConstants.PADX, GameConstants.BATTLE_AREA_BOTTOM)
        menu = UnitsMenu(UIConstants.SPRITE_BLUE_MENU, menu_size, characters_list, menu_position)
        menu.unset_focused()

        # add menu,  menu items and pointer to game engine sprites group
        self.get_game().add_sprite_to_group(menu)
        for i in range(menu.get_menu_items_count()):
            self.get_game().add_sprite_to_group(menu.get_item_from_menu(i))
        self.get_game().add_sprite_to_group(menu.get_pointer())
        return menu

    def handle_events(self):



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                if event.key == pygame.K_UP:
                    self.__player_units_menu.move_pointer_up()
                if event.key == pygame.K_DOWN:
                    self.__player_units_menu.move_pointer_down()
                if event.key == pygame.K_RETURN:
                    self.__menu_item_selected = self.__player_units_menu.get_selected_item()

            if isinstance(self.__menu_item_selected, Text):
                print(self.__menu_item_selected.get_string())
                self.__menu_item_selected = None

    def update(self):
        # mouse_pos, mouse_clicked = self.get_game().get_mouse()
        #
        # focused_sprite = self.get_game().collide_point(mouse_pos)
        # if focused_sprite is not None:
        #     if self.__focused_sprite != focused_sprite:
        #         self.__focused_sprite = focused_sprite
        #         if self.__marker is not None:
        #             self.remove_marker()
        #         self.add_marker(focused_sprite)
        #         print("adding marker")
        # else:
        #     self.remove_marker()
        #     self.__focused_sprite = None

        focused_unit = self.__turn_manager.get_current_unit()
        if focused_unit is not None:
            if self.__focused_sprite != focused_unit:
                self.__focused_sprite = focused_unit
                if self.__marker is not None:
                    self.remove_marker()
                self.add_marker(focused_unit)
                print("Current Unit's turn: {}".format(focused_unit.get_name()))
                self.__add_actions_menu(focused_unit)
                self.__player_units_menu.unset_focused()
        else:
            self.remove_marker()
            self.__focused_sprite = None
            self.__action_menu.unset_focus()

    def load_level(self):
        # load adventurer
        object_type = GameConstants.PLAYER_GAME_OBJECTS
        self.load_character(Bestiary.Bestiary.ARCHER, GameConstants.PLAYER_TOP_BACK, object_type)
        self.load_character(Bestiary.Bestiary.ARCHER, GameConstants.PLAYER_MIDDLE_BACK, object_type)
        self.load_character(Bestiary.Bestiary.ARCHER, GameConstants.PLAYER_BOTTOM_BACK, object_type)
        self.load_character(Bestiary.Bestiary.WARRIOR, GameConstants.PLAYER_TOP_FRONT, object_type)
        self.load_character(Bestiary.Bestiary.WARRIOR, GameConstants.PLAYER_MIDDLE_FRONT, object_type)
        self.load_character(Bestiary.Bestiary.WARRIOR, GameConstants.PLAYER_BOTTOM_FRONT, object_type)

        object_type = GameConstants.COMPUTER_GAME_OBJECTS
        self.load_character(Bestiary.Bestiary.SLIME, GameConstants.COMPUTER_TOP_BACK, object_type)
        self.load_character(Bestiary.Bestiary.SLIME, GameConstants.COMPUTER_MIDDLE_BACK, object_type)
        self.load_character(Bestiary.Bestiary.SLIME, GameConstants.COMPUTER_BOTTOM_BACK, object_type)
        self.load_character(Bestiary.Bestiary.SLIME, GameConstants.COMPUTER_TOP_FRONT, object_type)
        self.load_character(Bestiary.Bestiary.SLIME, GameConstants.COMPUTER_MIDDLE_FRONT, object_type)
        self.load_character(Bestiary.Bestiary.SLIME, GameConstants.COMPUTER_BOTTOM_FRONT, object_type)

        return

    def load_character(self, character_attributes, position, object_type):
        sprite_sheet = character_attributes[Bestiary.Bestiary.SPRITE_SHEET]
        size = character_attributes[Bestiary.Bestiary.SIZE]
        new_position = (position[0] - size[0] / 2, position[1] - size[1] / 2)  # position is center, need compensate

        character = Character(attributes=character_attributes, spritesheet_file=sprite_sheet, size=size,
                              position=new_position, object_type=object_type)  # init adventurer

        self.add_scene_object(character)  # add to scene objects list
        if object_type == GameConstants.PLAYER_GAME_OBJECTS:
            self.__turn_manager.add_player_unit(character)
        elif object_type == GameConstants.COMPUTER_GAME_OBJECTS:
            self.__turn_manager.add_computer_unit(character)
        self.get_game().add_sprite_to_group(character, object_type)  # add to game engine sprites group
        return

    def add_marker(self, focused_sprite):
        rect = pygame.Rect((0, 0), GameConstants.TRIANGLE_TOP_DOWN_SIZE)  # create a temp rect
        rect.top = focused_sprite.get_rect().top - int(rect.height / 2)
        rect.left = focused_sprite.get_rect().centerx - int(rect.width / 2)
        position = rect.topleft  # draw the marker right above the focused_sprite
        self.__marker = AnimatedObject(GameConstants.TRIANGLE_TOP_DOWN_SHEET,
                                       GameConstants.TRIANGLE_TOP_DOWN_SIZE,
                                       position=position,
                                       object_type=GameConstants.ALL_GAME_OBJECTS)
        game_engine = self.get_game()
        game_engine.add_sprite_to_group(self.__marker, self.__marker.get_type())  # add to game engine sprites group

    def remove_marker(self):
        if self.__marker is None:
            return

        self.__marker.kill()
        self.__marker = None
