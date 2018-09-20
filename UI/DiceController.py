import pygame
from Shared.Animator import Animator
from Shared.Button import Button
from Shared.GameConstants import GameConstants
from Shared.UIConstants import UIConstants
from UI.Text import Text
from UI.UIObject import UIObject


class ArrowButtonGenerator:
    def __init__(self):
        self.__animator = Animator(UIConstants.ARROW_BUTTON_SPRITE_SHEET)
        self.__buttons_list = self.__animator.get_animations_keys()

    def __get_arrow(self, key):
        image = self.__animator.get_sprite_by_key("{}_unpressed".format(key))
        pressed_image = self.__animator.get_sprite_by_key("{}_pressed".format(key))
        size = image.get_size()
        position = (0, 0)
        return Button(image, pressed_image, image, size, position)

    def get_up_arrow_button(self):
        return self.__get_arrow("up")

    def get_down_arrow_button(self):
        return self.__get_arrow("down")

    def get_left_arrow_button(self):
        return self.__get_arrow("left")

    def get_right_arrow_button(self):
        return self.__get_arrow("right")


class DiceController:

    def __init__(self, remaining_dice):
        arrow_button_generator = ArrowButtonGenerator()

        self.__name = "Dice Controller"
        self.__remaining_dice = remaining_dice
        self.__current_dice = 1

        self.__left_arrow_button = arrow_button_generator.get_left_arrow_button()
        self.__right_arrow_button = arrow_button_generator.get_right_arrow_button()
        self.__dice_text = Text(self.get_string(), (0, 0),
                                text_color=GameConstants.WHITE, font_size=UIConstants.TEXT_SIZE_LARGE)

        # position the text
        text_size = self.__dice_text.get_size()
        x = int(GameConstants.SCREEN_SIZE[0] / 2) - int(text_size[0] / 2)
        y = int(GameConstants.SCREEN_SIZE[1] / 2) - int(text_size[1] / 2)
        self.__dice_text.set_position((x, y))  # position middle of screen

        padx = 0
        arrow_size = self.__right_arrow_button.get_size()

        # position the right arrow
        x = self.__dice_text.get_position()[0] + text_size[0] + padx
        y = int(GameConstants.SCREEN_SIZE[1] / 2) - int(arrow_size[1] / 2)
        self.__right_arrow_button.set_position((x, y))

        # position the left arrow
        x = self.__dice_text.get_position()[0] - arrow_size[0] - padx
        self.__left_arrow_button.set_position((x, y))

        # background
        self.__background = UIObject(image=pygame.image.load(UIConstants.SPRITE_BLUE_MENU), position=(0, 0))
        self.__background.set_size(self.get_size())
        self.__background.set_position(self.get_position())

        self.__focused = True

    def __repr__(self):
        return self.__repr__()

    def get_current_dice(self):
        return self.__current_dice

    def get_string(self):
        string = "Dice:" + "{msg: >2}".format(msg=str(self.__current_dice)) \
                 + "/" + "{msg: >2}".format(msg=str(self.__remaining_dice))
        return string

    def set_string(self):
        self.__dice_text.set_string(self.get_string())

    def get_size(self):
        sizex = self.__left_arrow_button.get_size()[0] * 2 + self.__dice_text.get_size()[0]
        sizey = max(self.__left_arrow_button.get_size()[1], self.__dice_text.get_size()[1])
        return sizex, sizey

    def get_position(self):
        posx = self.__left_arrow_button.get_position()[0]
        posy = min(self.__left_arrow_button.get_position()[1], self.__dice_text.get_position()[1])
        return posx, posy

    def set_position(self, position):
        prev_pos = self.get_position()
        dx = position[0] - prev_pos[0]
        dy = position[1] - prev_pos[1]

        # update left arrow position
        pos = self.__left_arrow_button.get_position()
        self.__left_arrow_button.set_position((pos[0] + dx, pos[1] + dy))

        # update text position
        pos = self.__dice_text.get_position()
        self.__dice_text.set_position((pos[0] + dx, pos[1] + dy))

        # update right arrow position
        pos = self.__right_arrow_button.get_position()
        self.__right_arrow_button.set_position((pos[0] + dx, pos[1] + dy))

    def get_sprites(self):
        sprites = [self.__background, self.__dice_text, self.__left_arrow_button, self.__right_arrow_button]
        return sprites

    def get_dice(self):
        return self.get_current_dice()

    def increase_dice(self):
        if self.__current_dice == self.__remaining_dice:
            return
        else:
            self.__current_dice += 1
            self.set_string()
        self.set_string()

    def decrease_dice(self):
        if self.__current_dice == 0:
            return
        else:
            self.__current_dice -= 1
            self.set_string()
        self.set_string()

    def is_focused(self) -> bool:
        return self.__focused

    def set_focused(self) -> None:
        self.__focused = True

    def unset_focused(self) -> None:
        self.__focused = False

    def unmark_selected_item(self):
        return

    def mark_selected_item(self):
        return

    def destroy(self):
        self.__background.kill()
        self.__right_arrow_button.kill()
        self.__left_arrow_button.kill()
        self.__dice_text.kill()
