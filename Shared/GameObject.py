"""
Object Class is an extension to the Sprite Class
"""

import pygame
from pygame.sprite import Sprite
from typing import Tuple
from Shared.GameConstants import GameConstants


class GameObject(Sprite):

    # image = []  # a list of all images

    def __init__(self, image, position, object_type=GameConstants.ALL_GAME_OBJECTS):
        self.image = image  # must get an image not a string (Example: to support Animator...)
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.__object_type = object_type

        super(GameObject, self).__init__()  # call the parent class

    def __repr__(self):
        return "GameObject"

    # def update(self, seconds):
    #     pass

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

    def set_type(self, object_type):
        self.__object_type = object_type

    def get_type(self):
        return self.__object_type

    def is_front_row(self):
        position = self.get_position()
        size = self.get_size()
        center_posx = position[0] + size[0]/2
        if center_posx in [GameConstants.PLAYERS_FRONT_COLUMN, GameConstants.COMPUTER_FRONT_COLUMN]:
            return True
        else:
            return False

    def is_valid_target(self, valid_targets):
        if valid_targets in [GameConstants.TARGET_COMPUTER_SINGLE_ANY, GameConstants.TARGET_COMPUTER_ALL]:
            return True
        elif valid_targets in [GameConstants.TARGET_COMPUTER_SINGLE_FRONT, GameConstants.TARGET_COMPUTER_ALL_FRONT]:
            return self.is_front_row()
        elif valid_targets in [GameConstants.TARGET_COMPUTER_SINGLE_BACK, GameConstants.TARGET_COMPUTER_ALL_BACK]:
            return not self.is_front_row()
