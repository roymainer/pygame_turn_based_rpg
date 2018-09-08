from Shared.UIConstants import UIConstants
from UI.Menu import Menu


def get_string(model):
    string = model.get_name() + "_" + "HP:" + str(model.get_current_wounds()) + "/" + str(model.get_wounds())
    num_chars = len(string)
    delta_chars = UIConstants.MENU_MAX_CHARS - num_chars
    string = string.replace("_", " "*delta_chars)
    return string


class ModelsMenu(Menu):

    def __init__(self, image_path, image_size, models_list, position):

        self.__models_list = models_list
        # menu_options_list = []
        # for model in self.__models_list:
        #     string = get_string(model)
        #     menu_options_list.append(string)

        super(ModelsMenu, self).__init__(image_path, image_size, self.__models_list, position)
        self.unset_focused()

    def __repr__(self):
        return self.get_name()

    def get_model_by_index(self, index):
        return self.__models_list[index]

    def get_selectd_model(self):
        return self.__models_list[self.get_index()]

    def update_menu(self, game, models_list):

        # clear the menu
        while self.get_menu_items_count() > 0:
            self.remove_item_from_menu(0)
            self.__models_list = []

        # update models list
        self.__models_list = models_list

        # populate menu with new strings
        for model in self.__models_list:
            self.add_text_to_menu(model)

        for i in range(self.get_menu_items_count()):
            game.add_sprite_to_group(self.get_item_from_menu(i))

        return

    def kill(self):
        #

        super(ModelsMenu, self).kill()
