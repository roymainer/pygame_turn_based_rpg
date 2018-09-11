"""
Turn Manager

Handles the models turns in each phase
1. update current model
2.

"""
from Managers.Manager import Manager, TURN_MANAGER
from Shared.Action import Attack, RangeAttack  # , Spells, Skills, Items, Skip
from Shared.Model import Model


# def update_special_rules(current_model, game_engine, model_manager):
def update_special_rules(game_engine, model_manager):
    for model in model_manager.get_all_models_sorted_list():
        model.hide_models_special_rules()  # hide previous special rules
    # current_model.special_rules_to_texts()  # update current model sr texts
        model.special_rules_to_texts()
        for text in model.get_texts():
            game_engine.add_sprite_to_group(text, 0)


class TurnManager(Manager):

    def __init__(self, scene):

        self.__player_turn = True  # TODO: maybe roll a dice to see who starts first?

        self.__current_model_index = 0
        self.__current_model = None

        super(TurnManager, self).__init__(scene, TURN_MANAGER)

    def update(self):

        if self.__are_models_ready():
            # if all models are ready (with assigned actions and targets)

            game_engine = self.get_game_engine()
            action_manager = self.get_action_manager()
            model_manager = self.get_models_manager()
            ui_manager = self.get_ui_manager()

            ui_manager.remove_player_markers()  # hide player markers once action starts
            ui_manager.remove_computer_markers()  # hide computer markers

            """ Update current unit"""
            current_model = self.get_current_model()
            if current_model != self.__current_model:
                print("Current unit's turn:   {}".format(current_model.get_name()))
                self.__current_model = current_model  # update current model
                # TODO: move the following method back to ui_manager, update
                # ui_manager.add_player_marker(current_model)  # add a new marker for the model

                """ Set computer model action and targets"""
                if not current_model.is_player_model():
                    self.play_computer_turn(current_model)

            """ Perform models action """
            if current_model.is_ready() and not current_model.is_action_done():
                # if current model is ready to perform action and unless action is done, perform action
                action_manager.perform_action(current_model)

                """ Display special rules """
                update_special_rules(game_engine, model_manager)

                """ Blit action results texts"""
                for model in model_manager.get_all_models_sorted_list():
                    for text in model.get_action_results_texts():
                        game_engine.add_sprite_to_group(text)

            """ Animate targets death """
            if current_model.is_animation_cycle_done():
                all_models = model_manager.get_all_models_sorted_list()
                target = None
                for model in all_models:
                    if model.is_killed():
                        model.set_animation("die")  # animate death on all killed models
                        target = model
                    else:
                        model.set_animation("idle")  # return all remaining models to idle state

                if target is not None:
                    if target.is_animation_cycle_done():

                        """ Clear last action text """
                        for model in model_manager.get_all_models_sorted_list():
                            model.clear_action_results_texts()

                        """ clear all dead models """
                        model_manager.remove_dead_models()

                else:
                    """ Clear last action text """
                    for model in model_manager.get_all_models_sorted_list():
                        model.clear_action_results_texts()

            """ Advance to next model """
            # first make sure all models finished their animation cycle
            for model in model_manager.get_all_models_sorted_list():
                if not model.is_animation_cycle_done():
                    return

            self.__set_next_model_index()

    def __are_models_ready(self):
        phase_manager = self.get_phase_manager()
        # models_list = phase_manager.get_current_phase_models_list()
        models_list = phase_manager.get_current_phase_player_models_list()
        for model in models_list:
            if not model.is_ready():
                return False
        return True

    def set_current_model_index(self, index):
        self.__current_model_index = index

    def reset_current_model(self):
        self.__current_model = None

    def get_current_model(self) -> Model:
        phase_manager = self.get_phase_manager()
        current_phase_models_list = phase_manager.get_current_phase_models_list()

        # if self.__current_model_index not in range(len(current_phase_models_list)):
        #     self.__set_next_model_index()

        return current_phase_models_list[self.__current_model_index]

    def get_model_unit(self, model=None):
        mm = self.get_models_manager()
        if model is None:
            model = self.get_current_model()
        return mm.get_model_unit(model)

    def get_opponent_unit(self, model=None):
        mm = self.get_models_manager()
        if model is None:
            model = self.get_current_model()
        return mm.get_opponent_unit(model)

    def __set_next_model_index(self) -> None:
        phase_manager = self.get_phase_manager()
        current_phase_models_list = phase_manager.get_current_phase_models_list()
        self.__current_model_index += 1
        if self.__current_model_index not in range(len(current_phase_models_list)):
            self.__current_model_index = 0

    def play_computer_turn(self, model):
        # TODO: need to move to AI manager, send phase as parameter...

        phase_manager = self.get_phase_manager()

        action = Attack()  # default action

        # set model action
        model_actions_list = phase_manager.get_current_phase_actions_list()
        for action in model_actions_list:
            if type(action) == Attack or type(action) == RangeAttack:
                break
        model.set_action(action)

        # set action targets
        mm = self.get_models_manager()
        targets = mm.get_player_sorted_models_list()
        # TODO: improve the target selection process, lowest WS/ lowest wounds/...
        if not any(targets):
            return
        target = targets[0]
        model.set_targets(target)
        return
