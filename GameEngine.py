import logging

import pygame
from Scenes.MainMenuScene import MainMenuScene
from Scenes.PlayingGameScene import PlayingGameScene
from Shared.GameConstants import GameConstants


def get_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # create file handler
    fh = logging.FileHandler('log.log', mode='w')
    fh.setLevel(logging.INFO)

    # create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # create formatter and add it to the handlers
    # formatter = logging.Formatter('%(asctime)s - %(name)15s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(name)25s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


class GameEngine:

    def __init__(self):

        self.logger = get_logger().getChild(__name__)
        self.logger.info("Pygame init:")
        pygame.init()
        # pygame.mixer.init()

        self.__screen = pygame.display.set_mode(GameConstants.SCREEN_SIZE)
        self.__clock = pygame.time.Clock()
        self.__playtime = 0
        self.__mainloop = True

        """ Sprites groups"""
        self.__all_sprites = pygame.sprite.LayeredUpdates()  # layered sprites

        self.__mouse_position = None
        self.__mouse_buttons = None

        background = pygame.Surface(GameConstants.SCREEN_SIZE)
        self.__background = background.fill(GameConstants.WHITE)

        self.__scenes = (PlayingGameScene(self),
                         MainMenuScene(self))

        self.__current_scene = 1

        return

    def start(self):

        cycle_time = 0

        self.__screen.blit(self.__background, (0, 0))

        while self.__mainloop:
            milliseconds = self.__clock.tick(GameConstants.FPS)  # ms passed since last tick/frame
            seconds = milliseconds / 1000.0  # seconds since last tick/frame
            self.__playtime += seconds
            cycle_time += seconds

            if cycle_time > GameConstants.INTERVAL:
                self.__mouse_buttons = pygame.mouse.get_pressed()
                self.__mouse_position = pygame.mouse.get_pos()

                cycle_time = 0
                self.__all_sprites.clear(self.__screen, self.__background)

                current_scene = self.__scenes[self.__current_scene]
                current_scene.handle_events()
                current_scene.update()

                self.__all_sprites.update()
                self.__all_sprites.draw(self.__screen)

                print("Number of sprites: {}".format(self.__all_sprites.sprites().count()))

            pygame.display.set_caption("[FPS]: %.2f" % (self.__clock.get_fps()))

            # pygame.display.update()
            pygame.display.flip()

        return

    def set_scene(self, scene):
        self.__current_scene = scene

    def stop(self):
        self.__mainloop = False

    def add_sprite_to_group(self, sprite, layer=0):
        self.__all_sprites.add(sprite)
        if layer > 0:
            self.__all_sprites.change_layer(sprite, layer)
        return

    def remove_sprite_from_group(self, sprite):
        self.__all_sprites.remove(sprite)

    def get_sprites_group(self):
        return self.__all_sprites

    def empty_sprites_group(self):
        self.__all_sprites.empty()

    def set_background(self, background: pygame.Surface):
        self.__background = background
