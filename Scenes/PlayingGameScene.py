import pygame

from Scenes.Scene import Scene
from Shared.GameConstants import GameConstants
from Shared.Util import load_character, Marker


class PlayingGameScene(Scene):

    def __init__(self, game_engine):
        super(PlayingGameScene, self).__init__(game_engine)
        # background = pygame.Surface(GameConstants.SCREEN_SIZE)
        # background.fill(GameConstants.WHITE)
        background = pygame.image.load(GameConstants.DARK_LAIR)
        self.get_game().set_background(background)
        self.load_level()
        self.__marker = None

    def update(self):

        if self.__marker is not None:
            self.remove_marker()

        mouse_pos, mouse_clicked = self.get_game().get_mouse()

        focused_sprite = self.get_game().collide_point(mouse_pos)
        if focused_sprite is not None:
            self.add_marker(focused_sprite)

        print("Marker: {}".format(self.__marker is not None))

    def load_level(self):

        # load adventurer
        type = GameConstants.PLAYER_GAME_OBJECTS
        load_character(self.get_game(), self, "adventurer", GameConstants.PLAYER_TOP_BACK, type)
        load_character(self.get_game(), self, "adventurer", GameConstants.PLAYER_MIDDLE_BACK, type)
        load_character(self.get_game(), self, "adventurer", GameConstants.PLAYER_BOTTOM_BACK, type)
        load_character(self.get_game(), self, "adventurer", GameConstants.PLAYER_TOP_FRONT, type)
        load_character(self.get_game(), self, "adventurer", GameConstants.PLAYER_MIDDLE_FRONT, type)
        load_character(self.get_game(), self, "adventurer", GameConstants.PLAYER_BOTTOM_FRONT, type)

        type = GameConstants.COMPUTER_GAME_OBJECTS
        load_character(self.get_game(), self, "slime", GameConstants.COMPUTER_TOP_BACK, type)
        load_character(self.get_game(), self, "slime", GameConstants.COMPUTER_MIDDLE_BACK, type)
        load_character(self.get_game(), self, "slime", GameConstants.COMPUTER_BOTTOM_BACK, type)
        load_character(self.get_game(), self, "slime", GameConstants.COMPUTER_TOP_FRONT, type)
        load_character(self.get_game(), self, "slime", GameConstants.COMPUTER_MIDDLE_FRONT, type)
        load_character(self.get_game(), self, "slime", GameConstants.COMPUTER_BOTTOM_FRONT, type)

        return

    def add_marker(self, focused_sprite):
        # image = focused_sprite.get_image()
        # pygame.draw.ellipse(image, GameConstants.BRIGHT_GREEN, image.get_rect(), 1)  # draw the ellipse

        rect = focused_sprite.get_rect()
        self.__marker = Marker(rect)
        self.get_game().add_sprite_to_group(self.__marker)
        return

    def remove_marker(self):
        self.__marker.kill()
        self.__marker = None
