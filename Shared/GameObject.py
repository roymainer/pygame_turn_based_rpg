"""
Object Class is an extension to the Sprite Class
"""

import pygame
from pygame.sprite import Sprite
from typing import Tuple
from Shared.GameConstants import GameConstants


class GameObject(Sprite):

    image = []  # a list of all images

    def __init__(self, image, position, object_type=GameConstants.ALL_GAME_OBJECTS):
        super(GameObject, self).__init__()  # call the parent class
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.__object_type = object_type

    def __repr__(self):
        return "GameObject"

    # def update(self, seconds):
    #     pass

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

    def get_type(self):
        return self.__object_type

