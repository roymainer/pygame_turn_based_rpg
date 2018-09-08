from Shared.Bestiary import *
from Shared.GameConstants import *


class LevelManager:
    
    def __init__(self, scene):
        self.__scene = scene
    
    def load_level(self):

        # ---- load player models ---- #
        object_type = PLAYER_OBJECT
        self.set_model(get_empire_witch_hunter(), PLAYER_TOP_FRONT, object_type)
        self.set_model(get_warrior_priest(), PLAYER_MIDDLE_FRONT, object_type)
        self.set_model(get_empire_witch_hunter(), PLAYER_BOTTOM_FRONT, object_type)

        # ---- load computer models ---- #
        object_type = COMPUTER_OBJECT
        self.set_model(get_dwarf_hero(), COMPUTER_TOP_FRONT, object_type, flip_x=True)
        self.set_model(get_dwarf_hero(), COMPUTER_MIDDLE_FRONT, object_type, flip_x=True)
        self.set_model(get_dwarf_hero(), COMPUTER_BOTTOM_FRONT, object_type, flip_x=True)

        mm = self.__scene.get_models_manager()
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
        size = model.get_size()

        new_position = (position[0] - size[0] / 2, position[1] - size[1] / 2)  # position is center, need compensate
        model.set_position(new_position)
        model.set_type(object_type)

        if flip_x:
            model.flip_x()

        models_manager = self.__scene.get_models_manager()
        models_manager.add_model(model)

        game_engine = self.__scene.get_game_engine()
        game_engine.add_sprite_to_group(model)  # add to game engine sprites group
        return
