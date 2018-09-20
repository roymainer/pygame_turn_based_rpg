import pygame

from Shared.GameConstants import GameConstants
from Shared.UIConstants import UIConstants
from UI.Text import Text


class TextFading(Text):

    counter = 0

    def __init__(self, string, position,
                 text_color=GameConstants.WHITE,
                 background_color=None,
                 font_size=UIConstants.TEXT_SIZE_SMALL):
        super(TextFading, self).__init__(string, position, text_color, background_color, font_size)
        self.__original_image = self.get_image().copy()
        self.__alpha = 255
        self.__index = TextFading.counter
        TextFading.counter += 1

    def update(self) -> None:
        text_size = self.get_size()  # get the original text size
        surface = pygame.Surface(text_size, pygame.SRCALPHA)  # create a new surface with the same size
        text_image = self.__original_image
        text_image.set_alpha(self.__alpha)
        text_rect = self.get_rect()
        surface.blit(text_image, text_rect)  # blit text on surface
        self.image = surface
        self.__alpha -= 25
        if self.__alpha <= 0:
            self.__alpha = 0
        super(TextFading, self).update()

        print("TextFading Object #"+str(self.__index) + ", Alpha: " + str(self.__alpha))

    def get_alpha(self) -> int:
        return self.__alpha

    def kill(self) -> None:
        print("Killing: " + self.__repr__())
        TextFading.counter -= 1
        print("TextFading Counter: " + str(TextFading.counter))
        self.__original_image = None
        super(TextFading, self).kill()
