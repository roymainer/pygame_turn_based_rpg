import logging

import pygame
from Scenes.MainMenuScene import MainMenuScene
from Scenes.PlayingGameScene import PlayingGameScene
from Shared.GameConstants import *


def get_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # create file handler
    fh = logging.FileHandler('log.log')
    fh.setLevel(logging.INFO)

    # create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


class GameEngine:

    def __init__(self):

        self.logger = get_logger()

        pygame.init()
        # pygame.mixer.init()

        self.__screen = pygame.display.set_mode(SCREEN_SIZE)
        self.__clock = pygame.time.Clock()
        self.__playtime = 0
        self.__mainloop = True

        """ Sprites groups"""
        self.__all_sprites = pygame.sprite.LayeredUpdates()  # layered sprites
        # self.__player_sprites = pygame.sprite.Group()
        # self.__computer_sprites = pygame.sprite.Group()

        self.__mouse_position = None
        self.__mouse_buttons = None

        background = pygame.Surface(SCREEN_SIZE)
        self.__background = background.fill(WHITE)

        self.__scenes = (PlayingGameScene(self),
                         MainMenuScene(self))

        self.__current_scene = 0

        return

    def start(self):

        cycle_time = 0

        self.__screen.blit(self.__background, (0, 0))

        while self.__mainloop:
            milliseconds = self.__clock.tick(FPS)  # ms passed since last tick/frame
            seconds = milliseconds / 1000.0  # seconds since last tick/frame
            self.__playtime += seconds
            cycle_time += seconds

            if cycle_time > INTERVAL:
                self.__mouse_buttons = pygame.mouse.get_pressed()
                self.__mouse_position = pygame.mouse.get_pos()

                cycle_time = 0
                self.__all_sprites.clear(self.__screen, self.__background)

                current_scene = self.__scenes[self.__current_scene]
                current_scene.handle_events()
                current_scene.update()

                self.__all_sprites.update()
                # self.__all_sprites.update(seconds)
                self.__all_sprites.draw(self.__screen)

            pygame.display.set_caption("[FPS]: %.2f" % (self.__clock.get_fps()))
            # pygame.display.set_caption("[FPS]: %.2f action: %s" % (self.__clock.get_fps(), hero.get_action()))

            pygame.display.update()

        return

    def set_scene(self, scene):
        self.__current_scene = scene

    def stop(self):
        self.__mainloop = False

    # def add_sprite_to_group(self, sprite, group_type=None, layer=1):
    def add_sprite_to_group(self, sprite, layer=0):
        self.__all_sprites.add(sprite)
        if layer > 0:
            self.__all_sprites.change_layer(sprite, layer)
        # if group_type == PLAYER_GAME_OBJECTS:
        #     self.__player_sprites.add(sprite)
        # if group_type == COMPUTER_GAME_OBJECTS:
        #     self.__player_sprites.add(sprite)
        return

    # def remove_sprite_from_group(self, sprite, group_type=ALL_GAME_OBJECTS):
    def remove_sprite_from_group(self, sprite):
        # if group_type == ALL_GAME_OBJECTS:
        self.__all_sprites.remove(sprite)
        # if group_type == PLAYER_GAME_OBJECTS:
        #     self.__player_sprites.remove(sprite)
        # if group_type == COMPUTER_GAME_OBJECTS:
        #     self.__player_sprites.remove(sprite)

    # def get_sprites_group(self, group_type=ALL_GAME_OBJECTS):
    def get_sprites_group(self):
        # if group_type == ALL_GAME_OBJECTS:
        return self.__all_sprites
        # if group_type == PLAYER_GAME_OBJECTS:
        #     return self.__player_sprites
        # if group_type == COMPUTER_GAME_OBJECTS:
        #     return self.__player_sprites

    def empty_sprites_group(self):
        self.__all_sprites.empty()

    def set_background(self, background: pygame.Surface):
        self.__background = background

    # def get_mouse(self):
    #     return self.__mouse_position, self.__mouse_buttons

    # def collide_point(self, point: Tuple):
    #     pointer = MousePointer(point)
    #     focus_group = pygame.sprite.spritecollide(pointer, self.__all_sprites, False)
    #     if any(focus_group):
    #         return focus_group[0]
    #     else:
    #         return None
