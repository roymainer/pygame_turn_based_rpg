from UI.Menu import Menu
from UI.Text import Text

TITLE_STRING = "----- Name ----- WS BS S T   W I A LD"


# def get_string(model):
#     # string = model.get_name() + "_" + "HP:" + str(model.get_current_wounds()) + "/" + str(model.get_wounds())
#     string = model.get_name() + "_{}  {}  {}  {}  {}  {}  {}  {}".format(model.get_weapon_skill(),
#                                                                          model.get_ballistic_skill(),
#                                                                          model.get_strength(),
#                                                                          model.get_toughness(),
#                                                                          model.get_wounds(),
#                                                                          model.get_initiative(),
#                                                                          model.get_attacks(),
#                                                                          model.get_leadership())
#     num_chars = len(string)
#     delta_chars = UIConstants.MENU_MAX_CHARS - num_chars
#     string = string.replace("_", " "*delta_chars)
#     return string


class ModelsMenu(Menu):

    def __init__(self, image_path, image_size, models_list, position):

        self.__models_list = models_list
        self.__table_header = None

        super(ModelsMenu, self).__init__(image_path, image_size, self.__models_list, position)

        self.set_table_header()

        self.unset_focused()

    def __repr__(self):
        return self.get_name()

    def get_model_by_index(self, index):
        return self.__models_list[index]

    def get_selectd_model(self):
        return self.__models_list[self.get_index()]

    def update_menu(self, game, models_list):

        # clear the menu
        while self.get_ui_objects_list_count() > 0:
            self.remove_item_from_menu(0)
            self.__models_list = []

        # update models list
        self.__models_list = models_list

        # populate menu with new strings
        for model in self.__models_list:
            self.add_ui_object_to_menu(model)

        # add to game engine
        game.add_sprite_to_group(self.__table_header)
        for i in range(self.get_ui_objects_list_count()):
            game.add_sprite_to_group(self.get_ui_object_from_menu(i))

        return

    def set_table_header(self):
        # add table header
        self.__table_header = Text(TITLE_STRING, (0, 0))
        padx = 15
        pady = 5

        position = (self.get_position()[0] + padx, self.get_position()[1] + pady)

        self.__table_header.set_position(position)

    def get_table_header(self):
        return self.__table_header

    def kill(self):
        self.__table_header.kill()
        self.__table_header = None
        super(ModelsMenu, self).kill()
