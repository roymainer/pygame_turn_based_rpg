from Shared.Acts import get_act_object
from Managers.Manager import Manager, LEVEL_MANAGER
from Shared.GameConstants import GameConstants
import logging

from Shared.SavedGameHandler import SavedGameHandler

logger = logging.getLogger().getChild(__name__)


class LevelManager(Manager):
    
    def __init__(self, scene):
        logger.info("Init")
        self.__save_game_handler = SavedGameHandler()
        self.__act = self.set_act()
        super(LevelManager, self).__init__(scene, LEVEL_MANAGER)

    def set_act(self):
        level = self.__save_game_handler.load(SavedGameHandler.LEVEL_NUMBER)
        act = get_act_object(level)
        act_obj = act(level)
        return act_obj

    def get_act(self):
        return self.__act

    def load_level_models(self):
        logger.info("Load level")

        models_dict = self.__act.get_next_round_models()

        # ---- load player models ---- #
        object_type = GameConstants.PLAYER_OBJECT
        player_models_dict = models_dict[object_type]
        for key_position, model_func in player_models_dict.items():
            self.set_model(model_func(), key_position, object_type)

        # ---- load computer models ---- #
        object_type = GameConstants.COMPUTER_OBJECT
        computer_models_dict = models_dict[object_type]
        for key_position, model_func in computer_models_dict.items():
            self.set_model(model_func(), key_position, object_type, flip_x=True)

        mm = self.get_models_manager()
        mm.apply_special_rules_on_models()

        return
    
    def set_model(self, model, position, object_type, flip_x=False):
        """
        Creates the model object
        Adds the model to the model manager
        Adds the sprite to the Game Engine sprites list
        :param model:
        :param position:
        :param object_type:
        :param flip_x:
        :return:
        """
        logger.info("Set Model: {}".format(model.get_name()))

        size = model.get_size()

        new_position = (position[0] - size[0] / 2, position[1] - size[1] / 2)  # position is center, need compensate
        model.set_position(new_position)
        model.set_type(object_type)

        if flip_x:
            model.flip_x()

        models_manager = self.get_models_manager()
        models_manager.add_model(model)

        game_engine = self.get_game_engine()
        game_engine.add_sprite_to_group(model)  # add to game engine sprites group
        return
