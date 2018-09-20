import pygame
import logging
from Scenes.Scene import Scene
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

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    self.__main_menu.move_pointer_up()
                if event.key == pygame.K_DOWN:
                    self.__main_menu.move_pointer_down()
                if event.key == pygame.K_RETURN:
                    self.__menu_item_pressed()

    def __create_background(self):
        background = pygame.image.load(GameConstants.MAIN_MENU_BACKGROUND)
        background = pygame.transform.smoothscale(background, GameConstants.SCREEN_SIZE)
        self.get_game_engine().set_background(background)
        return

    def __create_main_menu(self):
        logger.info("Creating main menu")

        size = (100, 500)
        position = (0, 0)

        # TODO: create ButtonsMenu
        menu = Menu(UIConstants.SPRITE_BLUE_MENU, size, MENU_OPTIONS, position)

        # position the menu in the middle of the screen
        posx = int(GameConstants.SCREEN_SIZE[0]/2) - int(menu.get_size()[0]/2)
        posy = int(GameConstants.SCREEN_SIZE[1]/2) - int(menu.get_size()[1]/2)
        menu.set_position((posx, posy))
        menu.set_name("Main Menu")

        self.__main_menu = menu

        game_engine = self.get_game_engine()
        game_engine.add_sprite_to_group(menu)
        for i in range(menu.get_menu_items_count()):
            game_engine.add_sprite_to_group(menu.get_item_from_menu(i))

    def __create_main_menu_pointer(self):
        pointer = MenuPointer()
        game_engine = self.get_game_engine()
        # game_engine.remove_sprite_from_group(pointer)
        game_engine.add_sprite_to_group(pointer)
        pointer.assign_pointer_to_menu(self.__main_menu)
        self.__pointer = pointer

    def __menu_item_pressed(self):
        pass
