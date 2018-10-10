import os
import shelve
import logging

logger = logging.getLogger().getChild(__name__)


# noinspection PyTypeChecker
class SavedGameHandler:

    LEVEL_NUMBER = "level_number"

    def __init__(self):
        logger.info("Init")
        my_path = "C:\Dev\Python\game_development\pygame_turn_based_rpg"
        self.__filename = os.path.join(my_path, "savegame")

    def save(self, _save_dict=None):
        assert _save_dict is not None, "Got None instead of dictionary obj!"
        assert any(_save_dict), "Got empty save_dict!"

        logger.info("Saving dictionary: {}".format(_save_dict))

        save_game_shelf_file = shelve.open(self.__filename)  # open save game file

        # update savegame file with new dictionary values
        for key, val in _save_dict.items():
            save_game_shelf_file[key] = val

        save_game_shelf_file.close()  # close save game file
        return

    def load(self, key=None):
        assert key is not None, "Got None instead of dictionary key!"

        save_game_shelf_file = shelve.open(self.__filename)  # open save game file

        if key not in save_game_shelf_file:
            return None

        val = save_game_shelf_file[key]  # get value from key

        save_game_shelf_file.close()  # close save game file

        return val


if __name__ == "__main__":

    save_game_handler = SavedGameHandler()
    # save_dict = {get_dictionary_keys()[0]: '1', get_dictionary_keys()[1]: '1'}
    save_dict = {"level_number": "1"}
    save_game_handler.save(save_dict)

    # print("Act: {}".format(save_game_handler.load(get_dictionary_keys()[0])))
    print("Level: {}".format(save_game_handler.load("level_number")))
