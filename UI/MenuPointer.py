import pygame

from Shared.UIConstants import UIConstants
from UI.UIObject import UIObject


class MenuPointer(UIObject):

    def __init__(self):

        pointer_image = pygame.image.load(UIConstants.SPRITE_MENU_POINTER)
        super(MenuPointer, self).__init__(pointer_image, (0, 0))

        self.__menu = None
        self.__button = None  # if pointer is assigned to a button
        self.__pointer_positions = None

    def __repr__(self) -> str:
        return "MenuPointer"

    def __set_pointer_positions(self) -> None:
        """
        Creates a list of every pointer position so it would point to each of the menu items
        :return: None
        """

        self.__set_pointer_size()
        pointer_size = self.get_size()

        positions = []

        padx = 2

        for i in range(self.__menu.get_ui_objects_list_count()):
            menu_item = self.__menu.get_ui_object_from_menu(i)  # get first item
            menu_item_size = menu_item.get_size()
            menu_item_position = menu_item.get_position()

            position = (menu_item_position[0] - pointer_size[0] - padx,  # left of menu item
                        menu_item_position[1] + menu_item_size[1] / 2 - pointer_size[1] / 2)  # center of menu item
            positions.append(position)

        self.__pointer_positions = positions

    def __set_pointer_position(self) -> None:
        """ When assigned to a single button """
        button_size = self.__button.get_size()
        button_position = self.__button.get_position()

        self.__set_pointer_size(button_size)
        pointer_size = self.get_size()

        padx = 2

        position = (button_position[0] - pointer_size[0] - padx,  # left of button
                    button_position[1] + button_size[1] / 2 - pointer_size[1] / 2)  # center on middle of button
        self.set_position(position)

    def __set_pointer_size(self, new_size=None) -> None:
        if new_size is None:
            menu_item = self.__menu.get_ui_object_from_menu(0)  # get first item
            new_size = menu_item.get_size()

        original_size = self.image.get_rect().size
        size_ratio = new_size[1]/original_size[1]
        new_size = (int(original_size[0]*size_ratio), int(new_size[1]))
        # new_size = (int(original_size[0]), int(menu_item_size[1]))

        self.set_size(new_size)

    def assign_pointer_to_menu(self, menu) -> None:
        self.__menu = menu
        if menu.get_ui_objects_list_count() == 0:
            return
        self.__set_pointer_positions()

    def assign_pointer_to_button(self, button) -> None:
        self.__button = button
        self.__set_pointer_position()

    def update(self) -> None:
        if self.__menu is None or self.__pointer_positions is None:
            return

        self.set_position(self.__pointer_positions[self.__menu.get_index()])
        return

    def get_button(self):
        return self.__button
