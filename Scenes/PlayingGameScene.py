import pygame

from Scenes.Scene import Scene
from Shared.Bestiary import *
from Shared.Character import Character
from Shared.GameConstants import GameConstants
from Shared.TurnManager import TurnManager
from Shared.UnitAction import UnitAction
from UI.PlayingGameSceneUI import PlayingGameSceneUI


class PlayingGameScene(Scene):

    def __init__(self, game_engine):
        super(PlayingGameScene, self).__init__(game_engine)

        self.__turn_manager = TurnManager()  # 1st load the turn manager
        self.load_level()  # 2nd load the level which will populate the turn manager with units
        self.__UI = PlayingGameSceneUI(self)  # 3rd, the UI will be created with units menus

        self.__current_unit = None
        self.__current_action = None

        self.create_background()

    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__UI.return_to_previous_menu()
                if event.key == pygame.K_UP:
                    self.__UI.move_pointer_up()
                    # need to add move computer marker up
                if event.key == pygame.K_DOWN:
                    self.__UI.move_pointer_down()
                    # need to add move computer marker down
                if event.key == pygame.K_RETURN:
                    self.__UI.add_menu_selection_to_current_action()

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

        current_unit = self.__turn_manager.get_current_unit()
        if current_unit is not None:
            if current_unit != self.__current_unit:
                self.__UI.update_units_menu()
                self.__current_unit = current_unit  # store the current unit
                self.__current_action = UnitAction(current_unit)  # create a new action for the unit
                self.__UI.add_player_marker(current_unit)  # add a new marker for the unit
                print("Current Unit's turn: {}".format(current_unit.get_name()))
                self.__UI.add_actions_menu(current_unit)  # add new actions menu for the unit
        else:
            # if current unit is none
            # TODO: this code should never be reached, I need to check if there are no more computer/player units
            self.__current_unit = None  # remove the current unit
            self.__current_action = None  # remove the current action
            self.__UI.remove_marker()  # delete the marker
            self.__UI.remove_actions_menu()  # remove the actions menu

        if self.__current_action.is_ready():
            self.__current_action.perform_action()

        if self.__current_action.is_finished():
            self.__current_unit.set_action("idle")
            self.__current_action = None  # remove the current action
            self.__current_unit = None  # remove the current unit
            self.__turn_manager.set_next_unit()  # advance the turn manager to next unit

    def get_current_action(self):
        return self.__current_action

    def load_level(self):
        # load adventurer
        object_type = GameConstants.PLAYER_GAME_OBJECTS
        self.load_character(Bestiary.ARCHER, GameConstants.PLAYER_TOP_BACK, object_type)
        self.load_character(Bestiary.ARCHER, GameConstants.PLAYER_MIDDLE_BACK, object_type)
        self.load_character(Bestiary.ARCHER, GameConstants.PLAYER_BOTTOM_BACK, object_type)  # maintain this order
        self.load_character(Bestiary.WARRIOR, GameConstants.PLAYER_TOP_FRONT, object_type)
        self.load_character(Bestiary.WARRIOR, GameConstants.PLAYER_MIDDLE_FRONT, object_type)
        self.load_character(Bestiary.WARRIOR, GameConstants.PLAYER_BOTTOM_FRONT, object_type)

        object_type = GameConstants.COMPUTER_GAME_OBJECTS
        self.load_character(Bestiary.SLIME, GameConstants.COMPUTER_TOP_BACK, object_type)
        self.load_character(Bestiary.SLIME, GameConstants.COMPUTER_MIDDLE_BACK, object_type)
        self.load_character(Bestiary.SLIME, GameConstants.COMPUTER_BOTTOM_BACK, object_type)
        self.load_character(Bestiary.SKELETON, GameConstants.COMPUTER_TOP_FRONT, object_type, turn_left=True)
        self.load_character(Bestiary.SKELETON, GameConstants.COMPUTER_MIDDLE_FRONT, object_type, turn_left=True)
        self.load_character(Bestiary.SKELETON, GameConstants.COMPUTER_BOTTOM_FRONT, object_type, turn_left=True)

        return

    def load_character(self, character_attributes, position, object_type, turn_left=False):
        sprite_sheet = character_attributes[Bestiary.SPRITE_SHEET]
        size = character_attributes[Bestiary.SIZE]
        new_position = (position[0] - size[0] / 2, position[1] - size[1] / 2)  # position is center, need compensate

        character = Character(attributes=character_attributes, spritesheet_file=sprite_sheet, size=size,
                              position=new_position, object_type=object_type)  # init adventurer

        if turn_left:
            character.turn_left()

        # self.add_scene_object(character)  # add to scene objects list
        if object_type == GameConstants.PLAYER_GAME_OBJECTS:
            self.__turn_manager.add_player_unit(character)
        elif object_type == GameConstants.COMPUTER_GAME_OBJECTS:
            self.__turn_manager.add_computer_unit(character)
        self.get_game().add_sprite_to_group(character, object_type)  # add to game engine sprites group
        return

    def create_background(self):
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

        self.get_game().set_background(surface)
        return

    def get_turn_manager(self):
        return self.__turn_manager
