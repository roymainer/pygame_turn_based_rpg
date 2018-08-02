"""
Object Class is an extension to the Sprite Class
"""

from typing import Tuple

import pygame
from pygame.sprite import Sprite


class GameObject(Sprite):

    image = []  # a list of all images

    def __init__(self, image, position):
        super(GameObject, self).__init__()  # call the parent class
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

    def update(self, seconds):
        pass

    def get_image(self) -> pygame.Surface:
        return self.image

    def get_rect(self) -> pygame.Rect:
        return self.rect

    def set_position(self, position):
        self.rect.x = position[0]
        self.rect.y = position[1]

    def get_position(self) -> Tuple:
        return self.rect.x, self.rect.y

    def get_size(self) -> Tuple:
        return self.rect.size
