import pygame

from Shared.GameConstants import WHITE
from Shared.UIConstants import UIConstants
from UI.Text import Text
from UI.UIObject import UIObject
from typing import Tuple


class Menu(UIObject):

    def __init__(self, image_path: str,
                 size: Tuple,
                 menu_options=None,
                 position=(0, 0)):

        self.__padx = 15  # padding between menu left side and item left side
        self.__pady = 15  # padding between menu items

        image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(image, size)
        super(Menu, self).__init__(self.image, position)

        self.__menu_items_list = []
        self.__menu_objects_list = []  # save the objects as reference
        self.add_menu_items(menu_options)

        self.__menu_item_selected = None  # the selected menu item
        self.__focused = True  # active menu True/False

        self.__index = 0  # index of selected menu item

    def __repr__(self) -> str:
        return self.get_name()

    def add_text_to_menu(self, item) -> None:

        # calc item position
        if any(self.__menu_items_list):
            # if list is not empty
            last_item = self.__menu_items_list[-1]  # get the last item in the list
            position = (last_item.get_position()[0],
                        last_item.get_position()[1] + last_item.get_size()[1] + self.__pady)
        else:
            # if there are no items in the list (this is the new item added)
            position = (self.get_position()[0] + self.__padx, self.get_position()[1] + self.__pady)

        menu_item = Text(item.get_menu_item_string(), position, WHITE, None, UIConstants.TEXT_SIZE_SMALL)

        self.__menu_items_list.append(menu_item)
        self.__menu_objects_list.append(item)

    def move_pointer_up(self) -> None:
        # only change the index, the pointer will update it's position accordingly
        if self.__index == 0:
            # if pointing at top menu item, overlap to bottom item
            self.__index = len(self.__menu_items_list) - 1  # move to the last position
        else:
            self.__index -= 1

    def move_pointer_down(self) -> None:
        # only change the index, the pointer will update it's position accordingly
        if self.__index == len(self.__menu_items_list) - 1:  # if pointing to the last menu item
            self.__index = 0
        else:
            self.__index += 1

    def get_index(self) -> int:
        if self.__index not in range(self.get_menu_items_count()):
            self.__index = 0
        return self.__index

    def add_menu_items(self, menu_items) -> None:
        for item in menu_items:
            # self.add_text_to_menu(item.get_name())
            self.add_text_to_menu(item)

    def get_selected_item(self) -> Text:
        return self.get_item_from_menu(self.__index)

    def get_selected_object(self):
        return self.get_object_from_menu(self.__index)

    def get_menu_items_count(self) -> int:
        return len(self.__menu_items_list)

    def get_item_from_menu(self, index):
        if not any(self.__menu_items_list):
            # if list is empty
            return None

        if index not in range(self.get_menu_items_count()):
            index = 0
        return self.__menu_items_list[index]

    def get_object_from_menu(self, index):
        if index not in range(self.get_menu_items_count()):
            index = 0
        return self.__menu_objects_list[index]

    def remove_item_from_menu(self, index) -> None:
        item = self.__menu_items_list[index]
        item.kill()
        self.__menu_items_list.remove(item)

        obj = self.__menu_objects_list[index]
        self.__menu_objects_list.remove(obj)

    def is_focused(self) -> bool:
        return self.__focused

    def set_focused(self) -> None:
        self.__focused = True

    def unset_focused(self) -> None:
        self.__focused = False

    def update(self) -> None:
        pass
    
    def kill(self) -> None:
        for item in self.__menu_items_list:
            item.kill()
            
        super(Menu, self).kill()
