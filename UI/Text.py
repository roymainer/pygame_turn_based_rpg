import pygame
# from pygame.sprite import Sprite
from Shared.GameConstants import GameConstants
from UI.UIObject import UIObject


class Text(UIObject):

    def __init__(self, string, position,
                 text_color=GameConstants.WHITE,
                 background_color=None,
                 font_size=GameConstants.TEXT_SIZE_SMALL):

        self.__text_color = text_color
        self.__background_color = background_color
        self.__font_size = font_size

        self.__string = string
        font_obj = pygame.font.Font(None, self.__font_size)
        self.image = font_obj.render(string, False, self.__text_color, self.__background_color)

        self.rect = self.image.get_rect()
        self.rect.topleft = position

        super(Text, self).__init__(image=self.image, position=self.rect.topleft)  # init the Sprite object

    def get_string(self):
        return self.__string

    def set_string(self, string):
        self.__string = string  # update text string

        font_obj = pygame.font.Font(None, self.__font_size)  # create a new font object

        self.image = font_obj.render(text=self.__string,
                                     antialias=False,
                                     color=self.__text_color,
                                     background=self.__background_color)

        topleft = self.rect.topleft  # save previous position
        self.rect = self.image.get_rect()  # create a new rect
        self.rect.topleft = topleft  # update new rects position

# class Text(Sprite):
#     """
#     Text class (Sprite)
#
#     This class is actually a sprite. Much more useful for Game Engine.
#     """
#
#     def __init__(self, string, x=0, y=0,
#                  color=(255, 255, 255),
#                  background=None,
#                  size=GameConstants.TEXT_SIZE_SMALL):
#         """
#         Text class init method
#
#         :param string: Text string
#         :param x: x or left position
#         :param y: y or top position
#         :param color: Text color
#         :param background: Text background color (default: None)
#         :param size: Text font size (default: 17)
#         """
#
#         self.__text = string
#
#         font_obj = pygame.font.Font(None, size)
#         self.image = font_obj.render(text=string,
#                                      antialias=False,
#                                      color=color,
#                                      background=background)
#         self.rect = self.image.get_rect()
#         self.rect.x = x
#         self.rect.y = y
#
#         super(Text, self).__init__()  # init the Sprite base class
#
#         return
#
#     def get_text(self):
#         return self.__text
#
#     def get_rect(self):
#         return self.rect
