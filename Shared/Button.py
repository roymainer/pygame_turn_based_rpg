from typing import Tuple

import pygame

from Shared.Animator import Animator
from Shared.GameConstants import GameConstants
from Shared.UIConstants import UIConstants
from UI.UIObject import UIObject


class Button(UIObject):

    def __init__(self, sprite_sheet: pygame.Surface, size: Tuple, position: Tuple):
        self.__animator = Animator(sprite_sheet, sprite_size=size)
        # self.__sprites_options = self.__animator.get_animations_keys()
        image = self.__animator.get_sprite_by_key("default")
        super(Button, self).__init__(image=pygame.transform.scale(image, size), position=position)

    def set_button(self, key):
        key = key + "_unpressed"
        self.set_image(self.__animator.get_sprite_by_key(key))

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

    def __init__(self, sprite_sheet=UIConstants.BLUE_BUTTON_SPRITE_SHEET, size=(50, 50), string="",
                 font_size=UIConstants.FONT_SIZE_LARGE, position=(0, 0)):
        self.__string = string
        self.__font_size = font_size
        super(TextButton, self).__init__(sprite_sheet, size, position)

        # Create an image with a string
        font_obj = pygame.font.Font(UIConstants.MONOSPACE_FONT, self.__font_size)
        self.__text_image = font_obj.render(self.__string, False, GameConstants.WHITE, None)

        # blit over button image
        self.__blit_text_over_image()

        self.__focused = False

    def __blit_text_over_image(self):
        image = self.get_image()
        image_position = self.get_position()
        text_rect = self.__text_image.get_rect()

        image = pygame.transform.smoothscale(image, (text_rect.width + 20, text_rect.height + 20))

        image.blit(self.__text_image, (text_rect.left + 10, text_rect.top + 10))  # blit text image over button image
        rect = image.get_rect()
        self.set_size((rect.width, rect.height))
        self.set_image(image)
        self.set_position(image_position)

    def set_focused(self):
        super(TextButton, self).set_focused()
        self.__blit_text_over_image()
        self.__focused = True

    def set_pressed(self):
        super(TextButton, self).set_pressed()
        self.__blit_text_over_image()

    def unset_button(self):
        super(TextButton, self).unset_button()
        self.__blit_text_over_image()

    def __repr__(self):
        return "TextButton: {}".format(self.get_string())

    def get_string(self):
        return self.__string

    def get_menu_item_string(self):
        return self.get_string()
    
    def is_focused(self) -> bool:
        return self.__focused

    def unset_focused(self) -> None:
        self.unset_button()
        self.__focused = False

    def unmark_selected_item(self):
        return

    def mark_selected_item(self):
        return
