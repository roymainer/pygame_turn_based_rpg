from Managers.Manager import Manager, LEVEL_MANAGER
from Shared.Bestiary import *
from Shared.GameConstants import GameConstants
import logging
logger = logging.getLogger().getChild(__name__)


class LevelManager(Manager):
    
    def __init__(self, scene):
        logger.info("Init")
        super(LevelManager, self).__init__(scene, LEVEL_MANAGER)
    
    def load_level(self):
        logger.info("Load level")

        # ---- load player models ---- #
        object_type = GameConstants.PLAYER_OBJECT
        self.set_model(get_empire_witch_hunter(), GameConstants.PLAYER_TOP_FRONT, object_type)
        self.set_model(get_warrior_priest(), GameConstants.PLAYER_MIDDLE_FRONT, object_type)
        self.set_model(get_empire_witch_hunter(), GameConstants.PLAYER_BOTTOM_FRONT, object_type)
        # self.set_model(get_empire_witch_hunter(), GameConstants.PLAYER_TOP_BACK, object_type)
        # self.set_model(get_warrior_priest(), GameConstants.PLAYER_MIDDLE_BACK, object_type)
        # self.set_model(get_empire_witch_hunter(), GameConstants.PLAYER_BOTTOM_BACK, object_type)

        # ---- load computer models ---- #
        object_type = GameConstants.COMPUTER_OBJECT
        self.set_model(get_dwarf_hero(), GameConstants.COMPUTER_TOP_FRONT, object_type, flip_x=True)
        self.set_model(get_dwarf_hero(), GameConstants.COMPUTER_MIDDLE_FRONT, object_type, flip_x=True)
        self.set_model(get_dwarf_hero(), GameConstants.COMPUTER_BOTTOM_FRONT, object_type, flip_x=True)
        self.set_model(get_dwarf_hero(), GameConstants.COMPUTER_TOP_BACK, object_type, flip_x=True)
        self.set_model(get_dwarf_hero(), GameConstants.COMPUTER_MIDDLE_BACK, object_type, flip_x=True)
        self.set_model(get_dwarf_hero(), GameConstants.COMPUTER_BOTTOM_BACK, object_type, flip_x=True)

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
