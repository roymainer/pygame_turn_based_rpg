from Shared.ModelFF import ModelFF


class TurnManager:

    def __init__(self):
        self.__player_models = []  # used to keep player models in formation
        self.__computer_models = []  # used to keep computer models in formation
        self.__all_models_sorted = []  # all models sorted by initiative
        self.__current_model = 0  # index to current turn's model

    def __sort_all_models_list(self, sort_parameter: str= 'get_initiative'):
        # copy and exted both models lists into one
        all_models = list(self.__player_models)  # copy
        all_models.extend(list(self.__computer_models))  # extend

        from operator import methodcaller
        self.__all_models_sorted = sorted(all_models, key=methodcaller(sort_parameter), reverse=True)

        return

    def __add_model(self, models_list, new_model):

        if new_model.is_front_row():
            models_list.insert(0, new_model)  # Melee models are lower indexed (front line)
        else:
            models_list.append(new_model)

        self.__sort_all_models_list()  # sort the models each time we add another one
        return

    def add_player_model(self, new_model):
        self.__add_model(self.__player_models, new_model)

    def add_computer_model(self, new_model):
        self.__add_model(self.__computer_models, new_model)

    def get_current_model(self) -> ModelFF:
        if self.__current_model not in range(len(self.__all_models_sorted)):
            self.advance_to_next_model()
        return self.__all_models_sorted[self.__current_model]

    def advance_to_next_model(self):
        self.__current_model += 1
        if self.__current_model not in range(len(self.__all_models_sorted)):
            self.__sort_all_models_list()
            self.__current_model = 0
        # return self.__all_models_sorted[self.__current_model]

    def get_all_models_list(self):
        return self.__all_models_sorted

    def is_player_turn(self):
        current_model = self.__all_models_sorted[self.__current_model]
        return current_model in self.__all_models_sorted
    
    def get_player_model(self, index):
        return self.__player_models[index]

    def get_all_player_models(self) -> list:
        return self.__player_models

    def get_computer_model(self, index):
        return self.__computer_models[index]

    def get_all_computer_models(self):
        return self.__computer_models

    def get_current_model_unit(self) -> list:
        current_model = self.get_current_model()
        if current_model in self.__player_models:
            unit = self.get_all_player_models()
        elif current_model in self.__computer_models:
            unit = self.get_all_computer_models()

        return unit

    def get_opponent_unit(self) -> list:
        current_model = self.get_current_model()
        if current_model in self.__player_models:
            unit = self.get_all_computer_models()
        elif current_model in self.__computer_models:
            unit = self.get_all_player_models()

        return unit

    def remove_model(self, model):

        if model in self.__player_models:
            self.__player_models.remove(model)
        elif model in self.__computer_models:
            self.__computer_models.remove(model)

        if model in self.__all_models_sorted:
            # if self.__all_models_sorted[self.__current_model] == model:
            #     # if current turn's model is the model to remove, increment the index
            #     self.set_next_model()  # ignore the return value
            self.__all_models_sorted.remove(model)  # remove the model
            self.__sort_all_models_list()  # sort all models again
        return
