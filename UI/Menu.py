import pygame

from Shared.GameConstants import GameConstants
from Shared.MiniGameEngine import MiniGameEngine
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
        self.add_menu_items(menu_options)

        self.__menu_item_selected = None  # the selected menu item
        self.__focused = True  # active menu True/False

        self.__index = 0  # index of selected menu item

    def __repr__(self):
        return "Menu"

    def add_text_to_menu(self, string):

        # calc item position
        if any(self.__menu_items_list):
            # if list is not empty
            last_item = self.__menu_items_list[-1]  # get the last item in the list
            position = (last_item.get_position()[0],
                        last_item.get_position()[1] + last_item.get_size()[1] + self.__pady)
        else:
            # if there are no items in the list (this is the new item added)
            position = (self.get_position()[0] + self.__padx, self.get_position()[1] + self.__pady)

        menu_item = Text(string, position, GameConstants.WHITE, None, UIConstants.TEXT_SIZE_SMALL)

        self.__menu_items_list.append(menu_item)

    def move_pointer_up(self):
        # only change the index, the pointer will update it's position accordingly
        if self.__index == 0:
            # if pointing at top menu item, overlap to bottom item
            self.__index = len(self.__menu_items_list) - 1  # move to the last position
        else:
            self.__index -= 1

    def move_pointer_down(self):
        # only change the index, the pointer will update it's position accordingly
        if self.__index == len(self.__menu_items_list) - 1:  # if pointing to the last menu item
            self.__index = 0
        else:
            self.__index += 1

    def get_index(self):
        if self.__index not in range(self.get_menu_items_count()):
            self.__index = 0
        return self.__index

    def add_menu_items(self, menu_items):
        for item in menu_items:
            self.add_text_to_menu(item)

    def get_selected_item(self):
        return self.get_item_from_menu(self.__index)

    def get_menu_items_count(self):
        return len(self.__menu_items_list)

    def get_item_from_menu(self, index):
        if index not in range(self.get_menu_items_count()):
            index = 0
        return self.__menu_items_list[index]

    def remove_item_from_menu(self, index):
        item = self.__menu_items_list[index]
        item.kill()
        self.__menu_items_list.remove(item)

    def is_focused(self):
        return self.__focused

    def set_focused(self):
        self.__focused = True

    def unset_focused(self):
        self.__focused = False

    def update(self):
        pass
    
    def kill(self):
        for item in self.__menu_items_list:
            item.kill()
            
        super(Menu, self).kill()


if __name__ == "__main__":

    SCREEN_SIZE = (480, 320)
    FPS = 60
    BLACK = (0, 0, 0)
    INTERVAL = .10  # how long one single sprite should be displayed in seconds

    menu_image = pygame.image.load(UIConstants.SPRITE_BLUE_MENU)
    menu_size = (120, 120)
    _menu_options = ["Attack", "Magic", "Defend", "Item"]
    menu_position = (SCREEN_SIZE[0]/4-menu_size[0]/2, SCREEN_SIZE[1]/4-menu_size[1]/2)

    mini_game_engine = MiniGameEngine()

    menu = Menu(menu_image, menu_size, _menu_options, menu_position)

    mini_game_engine.add_sprite(menu)  # add menu to engine
    for i in range(menu.get_menu_items_count()):
        mini_game_engine.add_sprite(menu.get_item_from_menu(i))

    # mini_game_engine.add_sprite(menu.get_pointer())

    mini_game_engine.start()
