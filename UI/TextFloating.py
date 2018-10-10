import pygame

from Shared.GameConstants import GameConstants
from Shared.UIConstants import UIConstants
from UI.UIObject import UIObject


class TextFloating(UIObject):

    def __init__(self, string, position,
                 text_color=GameConstants.WHITE,
                 background_color=None,
                 font_size=UIConstants.FONT_SIZE_SMALL):
        self.__text_color = text_color
        self.__background_color = background_color
        self.__font_size = font_size

        self.__string = string
        # font_obj = pygame.font.Font(None, self.__font_size)
        font_obj = pygame.font.Font(UIConstants.MONOSPACE_FONT, self.__font_size)
        # font_obj = pygame.font.Font("joystix monospace.ttf", self.__font_size)
        self.image = font_obj.render(string, False, self.__text_color, self.__background_color)

        self.rect = self.image.get_rect()
        self.rect.topleft = position

        super(TextFloating, self).__init__(image=self.image, position=self.rect.topleft)  # init the Sprite object

    def __repr__(self) -> str:
        return "Text"

    def update(self, *args) -> None:
        position = self.get_position()
        new_position = (position[0], position[1] - 10)
        self.set_position(new_position)

    def get_string(self) -> str:
        return self.__string

    def set_string(self, string: str) -> None:
        self.__string = string  # update text string

        # font_obj = pygame.font.Font(None, self.__font_size)  # create a new font object
        font_obj = pygame.font.Font(UIConstants.MONOSPACE_FONT, self.__font_size)  # create a new font object

        self.image = font_obj.render(self.__string, False, self.__text_color, self.__background_color)

        topleft = self.rect.topleft  # save previous position
        self.rect = self.image.get_rect()  # create a new rect
        self.rect.topleft = topleft  # update new rects position

    def mark_string(self) -> None:
        # font_obj = pygame.font.Font(None, self.__font_size)  # create a new font object
        font_obj = pygame.font.Font(UIConstants.MONOSPACE_FONT, self.__font_size)  # create a new font object

        self.image = font_obj.render(self.__string, False, GameConstants.BRIGHT_GREEN, self.__background_color)

        topleft = self.rect.topleft  # save previous position
        self.rect = self.image.get_rect()  # create a new rect
        self.rect.topleft = topleft  # update new rects position

    def unmark_string(self) -> None:
        # font_obj = pygame.font.Font(None, self.__font_size)  # create a new font object
        font_obj = pygame.font.Font(UIConstants.MONOSPACE_FONT, self.__font_size)  # create a new font object

        self.image = font_obj.render(self.__string, False, self.__text_color, self.__background_color)

        topleft = self.rect.topleft  # save previous position
        self.rect = self.image.get_rect()  # create a new rect
        self.rect.topleft = topleft  # update new rects position
