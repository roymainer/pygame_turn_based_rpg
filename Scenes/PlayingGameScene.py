import pygame

from Scenes.Scene import Scene
from Shared.GameConstants import GameConstants
from Shared.Character import Character
from Shared.Util import load_character


class PlayingGameScene(Scene):

    def __init__(self, game_engine):
        super(PlayingGameScene, self).__init__(game_engine)
        # TODO: load level, change background, set characters
        self.__game_engine = game_engine
        background = pygame.Surface(GameConstants.SCREEN_SIZE)
        self.__game_engine.set_background(background)
        self.load_level()

    def update(self):
        pass

    def load_level(self):

        # load adventurer
        load_character(self.__game_engine, self, "adventurer", GameConstants.PLAYER_TOP_BACK)
        load_character(self.__game_engine, self, "adventurer", GameConstants.PLAYER_MIDDLE_BACK)
        load_character(self.__game_engine, self, "adventurer", GameConstants.PLAYER_BOTTOM_BACK)
        load_character(self.__game_engine, self, "adventurer", GameConstants.PLAYER_TOP_FRONT)
        load_character(self.__game_engine, self, "adventurer", GameConstants.PLAYER_MIDDLE_FRONT)
        load_character(self.__game_engine, self, "adventurer", GameConstants.PLAYER_BOTTOM_FRONT)

        load_character(self.__game_engine, self, "slime", GameConstants.COMPUTER_TOP_BACK)
        load_character(self.__game_engine, self, "slime", GameConstants.COMPUTER_MIDDLE_BACK)
        load_character(self.__game_engine, self, "slime", GameConstants.COMPUTER_BOTTOM_BACK)
        load_character(self.__game_engine, self, "slime", GameConstants.COMPUTER_TOP_FRONT)
        load_character(self.__game_engine, self, "slime", GameConstants.COMPUTER_MIDDLE_FRONT)
        load_character(self.__game_engine, self, "slime", GameConstants.COMPUTER_BOTTOM_FRONT)



        return
