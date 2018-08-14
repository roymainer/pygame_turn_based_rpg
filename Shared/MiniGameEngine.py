import os
import pygame

SCREEN_SIZE = (480, 320)
FPS = 60
BLACK = (0, 0, 0)
# SPRITE_SHEET = os.path.join("..", "Assets", "adventurer_sprite_sheet.png")
# ATLAS = os.path.join("..", "Assets", "adventurer_sprite_sheet.txt")
# SIZE = (200, 148)
# ACTION = "bow"
INTERVAL = .10  # how long one single sprite should be displayed in seconds


class MiniGameEngine:

    def __init__(self):
        pygame.init()
        self.__screen = pygame.display.set_mode(SCREEN_SIZE)
        self.__clock = pygame.time.Clock()
        self.__playtime = 0
        self.__cycletime = 0
        self.__images = []
        self.__all_sprites = pygame.sprite.LayeredUpdates()  # layered sprites

    def start(self):

        while 1:
            milliseconds = self.__clock.tick(FPS)  # ms passed since last tick/frame
            seconds = milliseconds / 1000.0  # seconds since last tick/frame
            self.__playtime += seconds
            self.__cycletime += seconds
            if self.__cycletime > INTERVAL:

                self.__screen.fill(BLACK)  # blit the background

                # draw single images if any
                for i in range(len(self.__images)):
                    image = self.__images[i]
                    rect = self.__rects[i]
                    self.__screen.blit(image, rect.topleft)

                self.__all_sprites.update()  # update all sprites
                self.__all_sprites.draw(self.__screen)  # draw all sprites

                self.__cycletime = 0  # reset cycletime counter

            pygame.display.set_caption("[FPS]: %.2f" % (self.__clock.get_fps()))
            pygame.display.flip()  # flip display

    def add_image(self, image, rect):
        self.__images.append(image)
        self.__rects.append(rect)

    def add_sprite(self, sprite):
        self.__all_sprites.add(sprite)
