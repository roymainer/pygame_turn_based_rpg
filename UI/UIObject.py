import pygame
from pygame.sprite import Sprite
from typing import Tuple


class UIObject(Sprite):
    """
    UIObject Class is an extension to the Sprite Class

    Very similar to GameObject class, all UI classes will inherite from it
    """

    def __init__(self, image, position):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

        super(UIObject, self).__init__()  # call the Sprite class

    def __repr__(self):
        return "UIObject"

    def get_image(self) -> pygame.Surface:
        return self.image

    def get_rect(self) -> pygame.Rect:
        return self.rect

    def set_position(self, position):
        self.rect.topleft = position

    def get_position(self) -> Tuple:
        return self.rect.topleft

    def get_size(self) -> Tuple:
        return self.rect.size

    def set_size(self, size: Tuple) -> None:
        self.image = pygame.transform.scale(self.image, size)
        self.rect.size = size
