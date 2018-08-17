import pygame

from Shared.UIConstants import UIConstants
from UI.UIObject import UIObject


class MenuPointer(UIObject):

    def __init__(self):

        pointer_image = pygame.image.load(UIConstants.SPRITE_MENU_POINTER)
        super(MenuPointer, self).__init__(pointer_image, (0, 0))

        # self.__menu = menu
        # self.__pointer_positions = self.__get_pointer_positions()
        self.__menu = None
        self.__pointer_positions = None
        # self.__index = 0  # index of pointed menu item
        # self.set_position(self.__pointer_positions[0])  # update position to point the first menu item

    def __repr__(self):
        return "MenuPointer"

    def __get_pointer_positions(self):
        """
        Creates a list of every pointer position so it would point to each of the menu items
        :return: pointer positions list
        """

        self.__set_pointer_size()
        pointer_size = self.get_size()

        positions = []

        padx = 10

        for i in range(self.__menu.get_menu_items_count()):
            menu_item = self.__menu.get_item_from_menu(i)  # get first item
            menu_item_size = menu_item.get_size()
            menu_item_position = menu_item.get_position()

            position = (menu_item_position[0] - pointer_size[0] - padx,  # left of menu item
                        menu_item_position[1] + menu_item_size[1] / 2 - pointer_size[1] / 2)  # center of menu item
            positions.append(position)

        self.__pointer_positions = positions

    def __set_pointer_size(self):
        menu_item = self.__menu.get_item_from_menu(0)  # get first item
        menu_item_size = menu_item.get_size()

        original_size = self.image.get_rect().size
        size_ratio = menu_item_size[1]/original_size[1]
        new_size = (int(original_size[0]*size_ratio), menu_item_size[1])

        self.set_size(new_size)

    def assign_pointer_to_menu(self, menu):
        self.__menu = menu
        self.__get_pointer_positions()

    def update(self):
        if self.__menu is None or self.__pointer_positions is None:
            return

        self.set_position(self.__pointer_positions[self.__menu.get_index()])
        return

    # def move_up(self):
    #     self.set_position(self.__pointer_positions[self.__index])
    #
    # def move_down(self):
    #     self.set_position(self.__pointer_positions[self.__index])

    # def get_pointer_index(self):
    #     return self.__index
