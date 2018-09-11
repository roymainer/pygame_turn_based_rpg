from Managers.Manager import Manager, MODELS_MANAGER
from Shared.GameConstants import TARGET_COMPUTER_ALL, TARGET_COMPUTER_ALL_FRONT, TARGET_COMPUTER_ALL_BACK, \
    TARGET_PLAYER_ALL, TARGET_PLAYER_ALL_FRONT, TARGET_PLAYER_ALL_BACK


def get_combined_list(player_list, computer_list, player_turn) -> list:
    if player_turn:
        list_a = player_list
        list_b = computer_list
    else:
        list_a = computer_list
        list_b = player_list

    combined_list = list(list_a)  # copy list1
    combined_list.extend(list(list_b))  # extend with list2
    return combined_list


def get_sorted_models_list(_list, sort_parameter: str = 'get_initiative') -> list:
    from operator import methodcaller
    _list = sorted(_list, key=methodcaller(sort_parameter), reverse=True)  # highest values first
    return _list


class ModelsManager(Manager):

    def __init__(self, scene):
        # TODO: could replace lists with pygame.sprite.OrderedUpdates(), sprite.kill() will remove from all lists!
        self.__player_wizards_list = []  # player wizards
        self.__player_shooter_list = []  # player shooters
        self.__player_all_models_list = []  # used to keep player models in formation

        self.__computer_wizards_list = []
        self.__computer_shooter_list = []
        self.__computer_all_models_list = []  # used to keep computer models in formation

        self.__current_model_index = 0  # index to current turn's model
        
        super(ModelsManager, self).__init__(scene, MODELS_MANAGER)

    def add_model(self, model) -> None:
        if model.is_player_model():
            if model.is_front_row():
                self.__player_all_models_list.insert(0, model)  # Melee models are lower indexed (front line)
            else:
                self.__player_all_models_list.append(model)

            if model.is_wizard():
                self.__player_wizards_list.append(model)
            if model.is_shooter():
                self.__player_shooter_list.append(model)
        else:
            if model.is_front_row():
                self.__computer_all_models_list.insert(0, model)  # Melee models are lower indexed (front line)
            else:
                self.__computer_all_models_list.append(model)
            if model.is_wizard():
                self.__computer_wizards_list.append(model)
            if model.is_shooter():
                self.__computer_shooter_list.append(model)

        return

    def remove_model(self, model):
        if model.is_player_model():
            self.__player_all_models_list.remove(model)
            if model.is_wizard():
                self.__player_wizards_list.remove(model)
            if model.is_shooter():
                self.__player_shooter_list.remove(model)
        else:
            self.__computer_all_models_list.remove(model)
            if model.is_wizard():
                self.__computer_wizards_list.remove(model)
            if model.is_shooter():
                self.__computer_shooter_list.remove(model)

        model.destroy(model_unit=self.get_model_unit(model), opponent_unit=self.get_opponent_unit(model))
        return

    # ---- Wizards ---- #
    def get_wizards_list(self, player_turn=True) -> list:
        # wizards don't act by initiative, the player can choose any wizard and any spell
        _list = get_combined_list(player_list=self.get_player_wizards(),
                                  computer_list=self.get_computer_wizards(),
                                  player_turn=player_turn)
        return _list

    def get_player_wizards(self) -> list:
        # wizards = [x for x in self.__player_models if x.is_wizard()]
        return self.__player_wizards_list

    def get_computer_wizards(self) -> list:
        # wizards = [x for x in self.__computer_models if x.is_wizard()]
        return self.__computer_wizards_list

    # ---- Shooters ---- #
    def get_shooters_list(self, player_turn=True) -> list:
        player_shooters_sorted = self.get_player_sorted_shooters_list()
        computer_shooters_sorted = self.get_computer_sorted_shooters_list()

        _list = get_combined_list(player_list=player_shooters_sorted,
                                  computer_list=computer_shooters_sorted,
                                  player_turn=player_turn)
        return _list

    def get_player_sorted_shooters_list(self) -> list:
        # shooters = [x for x in self.__player_models if x.is_shooter()]
        return get_sorted_models_list(self.__player_shooter_list)

    def get_computer_sorted_shooters_list(self) -> list:
        # shooters = [x for x in self.__computer_models if x.is_shooter()]
        return get_sorted_models_list(self.__computer_shooter_list)

    # ---- All ---- #
    def get_all_models_sorted_list(self, player_turn=True) -> list:
        player_models_sorted_list = self.get_player_sorted_models_list()
        computer_shooters_sorted = self.get_computer_sorted_models_list()

        _list = get_combined_list(player_list=player_models_sorted_list,
                                  computer_list=computer_shooters_sorted,
                                  player_turn=player_turn)
        return _list

    def get_player_sorted_models_list(self) -> list:
        return get_sorted_models_list(self.__player_all_models_list)

    def get_computer_sorted_models_list(self) -> list:
        return get_sorted_models_list(self.__computer_all_models_list)

    def get_player_model_by_index(self, index):
        return self.get_player_sorted_models_list()[index]

    def get_computer_model_by_index(self, index):
        return self.get_computer_sorted_models_list()[index]

    def reset_models_actions(self):
        for model in self.get_all_models_sorted_list():
            model.reset_action()

    def clear_used_up_special_rules(self):
        for model in self.get_all_models_sorted_list():
            model.clear_used_up_special_rules()

    def remove_dead_models(self):
        all_models = self.get_all_models_sorted_list()
        for model in all_models:
            model_unit = self.get_model_unit(model)
            opponent_unit = self.get_opponent_unit(model)
            if model.is_killed():
                model.destroy(model_unit, opponent_unit)
                self.remove_model(model)

        # self.set_phase()  # refresh phase with available models

    def get_model_unit(self, model) -> list:
        unit = []
        if model in self.__player_all_models_list:
            unit = self.get_player_sorted_models_list()
        elif model in self.__computer_all_models_list:
            unit = self.get_computer_sorted_models_list()
        return unit

    def get_opponent_unit(self, model) -> list:
        unit = []
        if model in self.__player_all_models_list:
            unit = self.get_computer_sorted_models_list()
        elif model in self.__computer_all_models_list:
            unit = self.get_player_sorted_models_list()
        return unit

    def get_valid_targets_models(self, valid_targets):
        all_player_models = self.get_player_sorted_models_list()
        all_computer_models = self.get_computer_sorted_models_list()

        valid_models = []

        if valid_targets == TARGET_COMPUTER_ALL:
            valid_models = all_computer_models
        elif valid_targets == TARGET_COMPUTER_ALL_FRONT:
            valid_models = [x for x in all_computer_models if x.is_front_row()]
        elif valid_targets == TARGET_COMPUTER_ALL_BACK:
            valid_models = [x for x in all_computer_models if not x.is_front_row()]
        elif valid_targets == TARGET_PLAYER_ALL:
            valid_models = all_player_models
        elif valid_targets == TARGET_PLAYER_ALL_FRONT:
            valid_models = [x for x in all_player_models if x.is_front_row()]
        elif valid_targets == TARGET_PLAYER_ALL_BACK:
            valid_models = [x for x in all_player_models if not x.is_front_row()]

        return valid_models

    def apply_special_rules_on_models(self):

        all_models_list = self.get_all_models_sorted_list(True)
        for model in all_models_list:
            unit = self.get_model_unit(model)
            enemy_unit = self.get_opponent_unit(model)  # get enemy unit

            for sr in model.get_special_rules_list():
                sr.on_init(model=model, unit=unit, enemy_unit=enemy_unit)
