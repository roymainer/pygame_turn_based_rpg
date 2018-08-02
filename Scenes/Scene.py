import pygame
from Shared.GameConstants import GameConstants
from Shared.Text import Text


class Scene:

    def __init__(self, game_engine):
        self.__game_engine = game_engine  # save the game class/engine
        # self.__texts = []  # each scene has a list of text to display
        # self.__buttons = []  # a list of buttons
        self.__game_objects = []

    def get_game(self):
        return self.__game_engine

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__game_engine.stop()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__game_engine.stop()
        pass

    def clear(self):
        """ Abstract method to clear scene elements screen """
        pass

    def update(self):
        """ Abstract method to update scene elements """
        pass

    def render(self):
        """ Abstract method to render scene elements """
        pass

    def add_text(self, string, x=0, y=0, color=(255, 255, 255), background=(0, 0, 0),
                 size=GameConstants.TEXT_SIZE_SMALL):
        self.__texts.append(Text(string, x, y, color, background, size))

    def add_game_object(self, game_object):
        self.__game_objects.append(game_object)


