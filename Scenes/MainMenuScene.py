import logging

import pygame
from pygame.sprite import Sprite

from Scenes.Scene import Scene
from Shared.Button import TextButton
from Shared.GameConstants import GameConstants
from Shared.UIConstants import UIConstants
from UI.Menu import Menu
from UI.MenuPointer import MenuPointer

logger = logging.getLogger().getChild(__name__)

MENU_OPTIONS = ["Campaign", "Custom Battle", "Quit"]


class MainMenuScene(Scene):

    def __init__(self, game_engine):
        super(MainMenuScene, self).__init__(game_engine)
        logger.info("Init")
        self.__main_menu = None
        self.__pointer = None

        self.__create_background()
        self.__create_main_menu()
        self.__create_main_menu_pointer()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logger.info("Quit")
                exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    self.__main_menu.move_pointer_up()
                if event.key == pygame.K_DOWN:
                    self.__main_menu.move_pointer_down()
                if event.key == pygame.K_RETURN:
                    self.__menu_item_pressed()
                if event.key == pygame.K_ESCAPE:
                    logger.info("Quit")
                    exit()

    def __create_background(self):
        background = pygame.image.load(GameConstants.MAIN_MENU_BACKGROUND)
        background = pygame.transform.smoothscale(background, GameConstants.SCREEN_SIZE)
        self.get_game_engine().set_background(background)
        return

    def __create_main_menu(self):
        logger.info("Creating main menu")

        size = (100, 500)
        position = (100, 100)

        menu_button_size = (100, 50)
        menu_options = []
        for string in MENU_OPTIONS:
            menu_options.append(TextButton(UIConstants.BLUE_BUTTON_SPRITE_SHEET, menu_button_size, string,
                                           UIConstants.FONT_SIZE_LARGE, position))
        menu = Menu(UIConstants.SPRITE_BLUE_MENU, size, menu_options, position)

        menu.update_size()  # update the menu size according to buttons
        menu.center_buttons()  # center buttons

        # reposition main menu
        posx = int(GameConstants.SCREEN_SIZE[0] / 10)
        posy = int(GameConstants.SCREEN_SIZE[1] / 10)
        menu.set_position((posx, posy))
        menu.set_name("Main Menu")

        self.__main_menu = menu

        game_engine = self.get_game_engine()
        game_engine.add_sprite_to_group(menu)
        for menu_item in menu.get_ui_objects_list():
            if isinstance(menu_item, Sprite):
                game_engine.add_sprite_to_group(menu_item)
            else:
                for sprite in menu_item.get_sprites():
                    game_engine.add_sprite_to_group(sprite)

    def __create_main_menu_pointer(self):
        pointer = MenuPointer()
        game_engine = self.get_game_engine()
        # game_engine.remove_sprite_from_group(pointer)
        game_engine.add_sprite_to_group(pointer)
        pointer.assign_pointer_to_menu(self.__main_menu)
        self.__pointer = pointer

    def __menu_item_pressed(self):
        button = self.__main_menu.get_selected_object()
        button_name = button.get_string()
        logger.info("Selected option: {}".format(button_name))
        game_engine = self.get_game_engine()

        # Campaign
        if button_name == MENU_OPTIONS[0]:
            from Scenes.CampaignScene import CampaignScene
            game_engine.set_scene(CampaignScene)
            # from Scenes.PlayingGameScene import PlayingGameScene
            # game_engine.set_scene(PlayingGameScene)

        # Custom Battle
        elif button_name == MENU_OPTIONS[1]:
            from Scenes.CustomBattleScene import CustomBattleScene
            game_engine.set_scene(CustomBattleScene)

        # Quit (always last option)
        elif button_name == MENU_OPTIONS[-1]:
            exit(0)
