import pygame
from pygame.sprite import Sprite
from Shared.GameConstants import GameConstants


class Text(Sprite):

    def __init__(self, string, x=0, y=0,
                 color=(255, 255, 255),
                 background=(0, 0, 0),
                 size=GameConstants.TEXT_SIZE_SMALL):

        self.__text = string

        font_obj = pygame.font.Font(None, size)
        self.image = font_obj.render(text=string,
                                     antialias=False,
                                     color=color,
                                     background=background)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        super(Text, self).__init__()  # init the Sprite base class

        return

    def get_text(self):
        return self.__text
