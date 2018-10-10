import pygame

from Shared.Button import Button, TextButton
from Shared.GameConstants import GameConstants
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
        self.__pady = 20  # padding between menu items

        image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(image, size)
        super(Menu, self).__init__(self.image, position)

        self.__menu_ui_objects_list = []
        self.__menu_objects_list = []  # save the (models/actions) objects as reference
        self.add_menu_items(menu_options)

        self.__menu_item_selected = None  # the selected menu item
        self.__focused = True  # active menu True/False

        self.__index = 0  # index of selected menu item

    def __repr__(self) -> str:
        return self.get_name()

    def add_ui_object_to_menu(self, item) -> None:

        # calc item position
        if any(self.__menu_ui_objects_list):
            # if list is not empty
            last_item = self.__menu_ui_objects_list[-1]  # get the last item in the list
            position = (last_item.get_position()[0],
                        last_item.get_position()[1] + last_item.get_size()[1] + self.__pady)
        else:
            # if there are no items in the list (this is the new item added)
            position = (self.get_position()[0] + self.__padx, self.get_position()[1] + self.__pady)

        if isinstance(item, Text) or isinstance(item, Button) or isinstance(item, TextButton):
            menu_item = item
            menu_item.set_position(position)
        else:
            menu_item = Text(item.get_menu_item_string(), position,
                             GameConstants.WHITE, None, UIConstants.FONT_SIZE_SMALL)

        self.__menu_ui_objects_list.append(menu_item)
        self.__menu_objects_list.append(item)

    def move_pointer_up(self) -> None:
        # only change the index, the pointer will update it's position accordingly
        if self.__index == 0:
            # if pointing at top menu item, overlap to bottom item
            self.__index = len(self.__menu_ui_objects_list) - 1  # move to the last position
        else:
            self.__index -= 1

    def move_pointer_down(self) -> None:
        # only change the index, the pointer will update it's position accordingly
        if self.__index == len(self.__menu_ui_objects_list) - 1:  # if pointing to the last menu item
            self.__index = 0
        else:
            self.__index += 1

    def get_index(self) -> int:
        if self.__index not in range(self.get_ui_objects_list_count()):
            self.__index = 0
        return self.__index

    def add_menu_items(self, menu_items) -> None:
        for item in menu_items:
            # self.add_text_to_menu(item.get_name())
            self.add_ui_object_to_menu(item)

    def get_selected_item(self) -> Text:
        return self.get_ui_object_from_menu(self.__index)

    def get_selected_object(self):
        return self.get_object_from_menu(self.__index)

    def get_ui_objects_list(self) -> list:
        return self.__menu_ui_objects_list

    def get_ui_objects_list_count(self) -> int:
        return len(self.__menu_ui_objects_list)

    def get_ui_object_from_menu(self, index):
        if not any(self.__menu_ui_objects_list):
            # if list is empty
            return None

        if index not in range(self.get_ui_objects_list_count()):
            index = 0
        return self.__menu_ui_objects_list[index]

    def get_object_from_menu(self, index):
        if index not in range(self.get_ui_objects_list_count()):
            index = 0
        return self.__menu_objects_list[index]

    def remove_item_from_menu(self, index) -> None:
        item = self.__menu_ui_objects_list[index]
        item.kill()
        self.__menu_ui_objects_list.remove(item)

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

    def mark_selected_item(self):
        self.get_selected_item().mark_string()

    def unmark_selected_item(self):
        selected_item = self.get_selected_item()
        if selected_item is not None:
            selected_item.unmark_string()

    def set_position(self, new_position):
        position = self.get_position()
        dx = new_position[0] - position[0]
        dy = new_position[1] - position[1]

        for ui_obj in self.get_ui_objects_list():
            pos = ui_obj.get_position()
            new_pos = (pos[0] + dx, pos[1] + dy)
            ui_obj.set_position(new_pos)

        super(Menu, self).set_position(new_position)

    def update_size(self):
        pad = 20
        x = 0
        max_y = 0

        for ui_obj in self.get_ui_objects_list():
            ui_rect = ui_obj.get_rect()
            x = max(x, ui_rect.width)
            max_y = max(max_y, ui_rect.bottom)

        rect = self.get_rect()
        y = max_y - rect.top
        self.set_size((x + 2*pad, y + pad))

    def center_buttons(self):
        menu_rect = self.get_rect()

        for ui_obj in self.get_ui_objects_list():
            size = ui_obj.get_size()
            pos = ui_obj.get_position()
            ui_obj.set_position((menu_rect.centerx - int(size[0]/2), pos[1]))

    def kill(self) -> None:
        for item in self.__menu_ui_objects_list:
            item.kill()
            
        super(Menu, self).kill()
