ACTION_MANAGER = "Action Manager"
LEVEL_MANAGER = "Level Manager"
MODELS_MANAGER = "Models Manager"
PHASE_MANAGER = "Phase Manager"
TURN_MANAGER = "Turn Manager"
UI_MANAGER = "UI Manager"
MAGIC_MANAGER = "Magic Manager"
EVENTS_MANAGER = "Events Manager"


class Manager:

    def __init__(self, scene, name):
        self.__scene = scene
        self.__name = name

    def __repr__(self):
        return self.__name

    def get_game_engine(self):
        return self.__scene.get_game_engine()

    def get_action_manager(self):
        if self.__name == ACTION_MANAGER:
            return self
        return self.__scene.get_action_manager()

    def get_level_manager(self):
        if self.__name == LEVEL_MANAGER:
            return self
        return self.__scene.get_level_manager()

    def get_models_manager(self):
        if self.__name == MODELS_MANAGER:
            return self
        return self.__scene.get_models_manager()

    def get_phase_manager(self):
        if self.__name == PHASE_MANAGER:
            return self
        return self.__scene.get_phase_manager()

    def get_turn_manager(self):
        if self.__name == TURN_MANAGER:
            return self
        return self.__scene.get_turn_manager()

    def get_ui_manager(self):
        if self.__name == UI_MANAGER:
            return self
        return self.__scene.get_ui_manager()

    def get_magic_manager(self):
        if self.__name == MAGIC_MANAGER:
            return self
        return self.__scene.get_magic_manager()

    def get_events_manager(self):
        if self.__name == EVENTS_MANAGER:
            return self
        return self.__scene.get_events_manager()

    def acquire_lock(self, name):
        return self.__scene.acquire_lock(name)

    def release_lock(self, name):
        return self.__scene.release_lock(name)

    def destroy(self):
        pass
