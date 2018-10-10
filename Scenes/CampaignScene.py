import logging
import pygame

from Managers.LevelManager import LevelManager
from Scenes.Scene import Scene
from Shared.Button import TextButton
from Shared.GameConstants import GameConstants
from Shared.UIConstants import UIConstants
from UI.MenuPointer import MenuPointer

logger = logging.getLogger().getChild(__name__)


class CampaignScene(Scene):

    def __init__(self, game_engine):
        super(CampaignScene, self).__init__(game_engine)
        logger.info("Init")
        self.__next_button = None
        self.__back_button = None
        self.__pointer = None

        self.__level_manager = LevelManager(self)
        self.__set_background()
        self.__create_buttons()
        self.__create_pointer()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logger.info("Quit")
                exit()

            if event.type == pygame.KEYDOWN:

                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    self.__move_pointer()
                if event.key == pygame.K_RETURN:
                    self.__button_pressed()

    def __set_background(self):
        game_engine = self.get_game_engine()
        background = self.__level_manager.get_act().get_campaign_background()
        game_engine.set_background(background)

    def __create_buttons(self):
        screen_size = GameConstants.SCREEN_SIZE

        position = (screen_size[0] * 15/20, screen_size[1] * 9/10)
        self.__next_button = TextButton(UIConstants.BLUE_BUTTON_SPRITE_SHEET, (100, 50),
                                        "Continue", UIConstants.FONT_SIZE_LARGE, position)

        position = (screen_size[0] * 2/20, screen_size[1] * 9/10)
        self.__back_button = TextButton(UIConstants.BLUE_BUTTON_SPRITE_SHEET, (100, 50),
                                        "Back", UIConstants.FONT_SIZE_LARGE, position)

        game_engine = self.get_game_engine()
        game_engine.add_sprite_to_group(self.__next_button)
        game_engine.add_sprite_to_group(self.__back_button)

    def __create_pointer(self):
        pointer = MenuPointer()
        game_engine = self.get_game_engine()
        game_engine.add_sprite_to_group(pointer)
        pointer.assign_pointer_to_button(self.__next_button)
        self.__pointer = pointer

    def __move_pointer(self):
        current_button = self.__pointer.get_button()
        if current_button == self.__next_button:
            new_button = self.__back_button
        else:
            new_button = self.__next_button

        self.__pointer.assign_pointer_to_button(new_button)

    def __button_pressed(self):
        button = self.__pointer.get_button()
        logger.info("Selected option: {}".format(button.get_name()))

        game_engine = self.get_game_engine()

        # battle
        if button == self.__next_button:
            from Scenes.PlayingGameScene import PlayingGameScene
            game_engine.set_scene(PlayingGameScene)

        else:
            from Scenes.MainMenuScene import MainMenuScene
            game_engine.set_scene(MainMenuScene)
