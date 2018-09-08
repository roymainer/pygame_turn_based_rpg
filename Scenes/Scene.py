import pygame
from Shared.UIConstants import UIConstants
from UI.Text import Text


class Scene:

    def __init__(self, game_engine):
        self.__game_engine = game_engine  # save the game class/engine
        # self.__texts = []  # each scene has a list of text to display
        # self.__buttons = []  # a list of buttons
        self.__scene_objects = []

    def get_game_engine(self):
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

    def add_text(self, string, position, color=(255, 255, 255), background=(0, 0, 0),
                 size=UIConstants.TEXT_SIZE_SMALL):
        self.__texts.append(Text(string, position, color, background, size))

    def add_scene_object(self, game_object):
        self.__scene_objects.append(game_object)

    def get_scene_objects_list(self):
        return self.__scene_objects
