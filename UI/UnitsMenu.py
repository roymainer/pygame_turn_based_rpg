from Shared.UIConstants import UIConstants
from UI.Menu import Menu


def get_string(unit):
    string = unit.get_name() + "_" + "HP: " + str(unit.get_wounds()) + "/" + str(unit.get_max_wounds())
    num_chars = len(string)
    delta_chars = UIConstants.MENU_MAX_CHARS - num_chars
    string = string.replace("_", " "*delta_chars)
    return string


class UnitsMenu(Menu):

    def __init__(self, image_path, image_size, units_list, position):

        self.__units_list = units_list
        menu_options_list = []
        for unit in self.__units_list:
            string = get_string(unit)
            menu_options_list.append(string)

        super(UnitsMenu, self).__init__(image_path, image_size, menu_options_list, position)
        self.unset_focused()

    def __repr__(self):
        return "UnitsMenu"

    def get_unit_by_index(self, index):
        return self.__units_list[index]

    def get_selectd_unit(self):
        return self.__units_list[self.get_index()]

    def update_menu(self, game):

        # TODO: need to think, maybe this update should happen only when there is actual change to a unit

        # clear the menu
        while self.get_menu_items_count() > 0:
            self.remove_item_from_menu(0)

        # populate menu with new strings
        for unit in self.__units_list:
            string = get_string(unit)
            self.add_text_to_menu(string)

        for i in range(self.get_menu_items_count()):
            game.add_sprite_to_group(self.get_item_from_menu(i))

        return

    def kill(self):
        for unit_text_obj in self.__units_list:
            unit_text_obj.kill()
        super(UnitsMenu, self).kill()
