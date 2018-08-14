from UI.Menu import Menu


def get_string(unit):
    return unit.get_name() + " "*20 + "HP: " + str(unit.get_wounds()) + "/" + str(unit.get_max_wounds())


class UnitsMenu(Menu):

    def __init__(self, image_path, image_size, units_list, position):

        self.__units_list = units_list
        menu_options_list = []
        for unit in self.__units_list:
            string = get_string(unit)
            menu_options_list.append(string)

        super(UnitsMenu, self).__init__(image_path, image_size, menu_options_list, position)
        self.unset_focused()

    def update_menu(self):

        # TODO: need to think, maybe this update should happen only when there is actual change to a unit

        # clear the menu
        while self.get_menu_items_count() > 0:
            self.remove_item_from_menu(0)

        # populate menu with new strings
        for unit in self.__units_list:
            string = get_string(unit)
            self.add_text_to_menu(string)

        return
