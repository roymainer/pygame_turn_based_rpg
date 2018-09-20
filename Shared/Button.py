from typing import Tuple

import pygame

from Shared.Animator import Animator
from UI.UIObject import UIObject


class Button(UIObject):

    def __init__(self, sprite_sheet: pygame.Surface, size: Tuple, position: Tuple):
        self.__animator = Animator(sprite_sheet)
        self.__sprites_options = self.__animator.get_animations_keys()
        image = self.__animator.get_sprite_by_key("default")
        super(Button, self).__init__(image=pygame.transform.scale(image, size), position=position)

    def set_focused(self) -> None:
        self.image = self.__animator.get_sprite_by_key("focused")

    def set_pressed(self) -> None:
        self.image = self.__animator.get_sprite_by_key("pressed")

    def unset_button(self) -> None:
        self.image = self.__animator.get_sprite_by_key("default")

    def on_click(self):
        pass


class TextButton(Button):
    """
    Same as regular Button class, but blits a Text over the image button surface
    """

    def __init__(self, sprite_sheet, string, size, position):
        self.__string = string
        super(TextButton, self).__init__(sprite_sheet, string, size, position)
        text =

        image = self.get_image()

    def __repr__(self):
        return "TextButton: {}".format(self.get_string())

    def get_string(self):
        return self.__string
