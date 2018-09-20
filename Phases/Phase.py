import logging
from Shared.Action import Items, Skip, Skills
logger = logging.getLogger().getChild(__name__)

MAGIC_PHASE = "Magic Phase"
SHOOTING_PHASE = "Shooting Phase"
CLOSE_COMBAT_PHASE = "Close Combat Phase"

PHASES = [MAGIC_PHASE, SHOOTING_PHASE, CLOSE_COMBAT_PHASE]


# noinspection PyMethodMayBeStatic
class Phase:

    def __init__(self, phase_manager, name):
        self.__phase_manager = phase_manager
        self.__name = name
        self.__models_list = []

    def get_name(self):
        return self.__name

    def __repr__(self):
        return self.get_name()

    def is_phase_complete(self) -> bool:
        for model in self.__models_list:
            if not model.is_action_done() or not model.is_animation_cycle_done():
                # if any of the models, didn't finish it's action and animation, the phase isn't done
                return False
        logger.info("################ {} is complete ################".format(self.get_name()))
        return True

    def set_models_list(self, models) -> None:
        self.__models_list = models

    def get_models_list(self) -> list:
        return self.__models_list

    def refresh_models_list(self) -> None:
        pass

    # def get_player_models_list(self) -> list:
    #     all_models = self.get_models_list()
    #     player_models = [x for x in all_models if x.is_player_model()]
    #     return player_models

    # def get_computer_models_list(self) -> list:
    #     all_models = self.get_models_list()
    #     player_models = [x for x in all_models if not x.is_player_model()]
    #     return player_models

    def get_phase_actions_list(self, turn_manager) -> list:
        if not any(self.get_models_list()):
            return []

        actions_list = [Items(), Skip()]

        current_model = turn_manager.get_current_model()
        if any(current_model.get_skills_list()):
            actions_list.insert(0, Skills())

        return actions_list

    def get_next_phase_key(self):
        pass

    def get_player_power_pool(self):
        return self.__phase_manager.get_magic_manager().get_player_power_pool()

    def get_computer_power_pool(self):
        return self.__phase_manager.get_magic_manager().get_computer_power_pool()

    def get_wizards_list(self):
        models_manager = self.__phase_manager.get_models_manager()
        models = models_manager.get_wizards_list()
        self.set_models_list(models)

    def get_shooters_list(self):
        models_manager = self.__phase_manager.get_models_manager()
        models = models_manager.get_shooters_list()
        self.set_models_list(models)

    def get_all_models_list(self):
        models_manager = self.__phase_manager.get_models_manager()
        models = models_manager.get_all_models_sorted_list()
        self.set_models_list(models)
