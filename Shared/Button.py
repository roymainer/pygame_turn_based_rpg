from typing import Tuple

import pygame
from UI.UIObject import UIObject


class Button(UIObject):

    def __init__(self, image: pygame.Surface,
                 pressed_image: pygame.Surface,
                 focused_image: pygame.Surface,
                 size: Tuple,
                 position: Tuple):

        self.__button_image = pygame.transform.scale(image, size)
        self.__button_pressed_image = pygame.transform.scale(pressed_image, size)
        self.__button_focused_image = pygame.transform.scale(focused_image, size)

        super(Button, self).__init__(image=pygame.transform.scale(image, size), position=position)

    def set_focused(self):
        self.image = self.__button_focused_image

    def set_pressed(self):
        self.image = self.__button_pressed_image

    def unset_button(self):
        self.image = self.__button_image
