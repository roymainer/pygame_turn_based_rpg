import pygame

from Scenes.Scene import Scene
from Shared.AnimatedObject import AnimatedObject
from Shared.GameConstants import GameConstants
from Shared.Util import load_character


def create_background():
    surface = pygame.Surface(GameConstants.SCREEN_SIZE)  # create an empty surface

    # load upper background
    background = pygame.image.load(GameConstants.DARK_LAIR)
    background = pygame.transform.smoothscale(background, (GameConstants.SCREEN_SIZE[0],
                                                           GameConstants.BATTLE_AREA_TOP))
    surface.blit(background, (0, 0))

    # load battleground background
    # battleground = pygame.image.load(GameConstants.CAVE_TILE)
    # battleground = pygame.transform.scale(battleground,
    #                                       (GameConstants.SCREEN_SIZE[0],
    #                                        GameConstants.BATTLE_AREA_BOTTOM - GameConstants.BATTLE_AREA_TOP))
    # surface.blit(battleground, (0, GameConstants.BATTLE_AREA_TOP))

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
    menu_background = pygame.image.load(GameConstants.GAME_SCENE_MENU)
    menu_background = pygame.transform.smoothscale(menu_background,
                                                   (GameConstants.SCREEN_SIZE[0],
                                                    GameConstants.SCREEN_SIZE[1] - GameConstants.BATTLE_AREA_BOTTOM))
    surface.blit(menu_background, (0, GameConstants.BATTLE_AREA_BOTTOM))

    return surface


class PlayingGameScene(Scene):

    def __init__(self, game_engine):
        super(PlayingGameScene, self).__init__(game_engine)
        background = create_background()
        self.get_game().set_background(background)
        self.load_level()
        self.__marker = None
        self.__focused_sprite = None
        self.__player_units = []  # 
        self.__computer_units = []

    def update(self):

        mouse_pos, mouse_clicked = self.get_game().get_mouse()

        focused_sprite = self.get_game().collide_point(mouse_pos)
        if focused_sprite is not None:
            if self.__focused_sprite != focused_sprite:
                self.__focused_sprite = focused_sprite
                if self.__marker is not None:
                    self.remove_marker()
                self.add_marker(focused_sprite)
                print("adding marker")
        else:
            self.remove_marker()
            self.__focused_sprite = None

        # print("Marker: {}".format(self.__marker is not None))

    def load_level(self):

        # load adventurer
        object_type = GameConstants.PLAYER_GAME_OBJECTS
        load_character(self.get_game(), self, "adventurer", GameConstants.PLAYER_TOP_BACK, object_type)
        load_character(self.get_game(), self, "adventurer", GameConstants.PLAYER_MIDDLE_BACK, object_type)
        load_character(self.get_game(), self, "adventurer", GameConstants.PLAYER_BOTTOM_BACK, object_type)
        load_character(self.get_game(), self, "adventurer", GameConstants.PLAYER_TOP_FRONT, object_type)
        load_character(self.get_game(), self, "adventurer", GameConstants.PLAYER_MIDDLE_FRONT, object_type)
        load_character(self.get_game(), self, "adventurer", GameConstants.PLAYER_BOTTOM_FRONT, object_type)

        object_type = GameConstants.COMPUTER_GAME_OBJECTS
        load_character(self.get_game(), self, "slime", GameConstants.COMPUTER_TOP_BACK, object_type)
        load_character(self.get_game(), self, "slime", GameConstants.COMPUTER_MIDDLE_BACK, object_type)
        load_character(self.get_game(), self, "slime", GameConstants.COMPUTER_BOTTOM_BACK, object_type)
        load_character(self.get_game(), self, "slime", GameConstants.COMPUTER_TOP_FRONT, object_type)
        load_character(self.get_game(), self, "slime", GameConstants.COMPUTER_MIDDLE_FRONT, object_type)
        load_character(self.get_game(), self, "slime", GameConstants.COMPUTER_BOTTOM_FRONT, object_type)

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
